import logging

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes
from packaging.version import Version
from web3 import Web3

from gnosis.eth.constants import GAS_CALL_DATA_BYTE, NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.utils import get_eth_address_with_key

from ..exceptions import (
    CannotEstimateGas,
    CannotRetrieveSafeInfoException,
    CouldNotPayGasWithToken,
    InvalidInternalTx,
)
from ..safe import Safe, SafeOperation
from ..signatures import signature_to_bytes, signatures_to_bytes
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestSafe(SafeTestCaseMixin, TestCase):
    def test_create(self):
        owners = [self.ethereum_test_account.address]
        threshold = 1
        master_copy_address = self.safe_contract_address

        ethereum_tx_sent = Safe.create(
            self.ethereum_client,
            self.ethereum_test_account,
            master_copy_address,
            owners,
            threshold,
            proxy_factory_address=self.proxy_factory_contract_address,
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_master_copy_address(), master_copy_address)
        self.assertEqual(safe.retrieve_owners(), owners)
        self.assertEqual(safe.retrieve_threshold(), threshold)

    def test_check_funds_for_tx_gas(self):
        safe = self.deploy_test_safe()
        safe_tx_gas = 2
        base_gas = 4
        gas_price = 10
        self.assertFalse(
            safe.check_funds_for_tx_gas(safe_tx_gas, base_gas, gas_price, NULL_ADDRESS)
        )
        self.send_ether(safe.address, (safe_tx_gas + base_gas) * gas_price)
        self.assertTrue(
            safe.check_funds_for_tx_gas(safe_tx_gas, base_gas, gas_price, NULL_ADDRESS)
        )

    def test_estimate_safe_creation(self):
        number_owners = 4
        gas_price = self.gas_price
        payment_token = NULL_ADDRESS
        safe_creation_estimate = Safe.estimate_safe_creation(
            self.ethereum_client,
            self.safe_contract_V0_0_1_address,
            number_owners,
            gas_price,
            payment_token,
        )
        self.assertGreater(safe_creation_estimate.gas_price, 0)
        self.assertGreater(safe_creation_estimate.gas, 0)
        self.assertGreater(safe_creation_estimate.payment, 0)
        self.assertEqual(safe_creation_estimate.payment_token, payment_token)

    def test_estimate_safe_creation_2(self):
        number_owners = 4
        gas_price = self.gas_price
        payment_token = NULL_ADDRESS
        safe_creation_estimate = Safe.estimate_safe_creation_2(
            self.ethereum_client,
            self.safe_contract_address,
            self.proxy_factory_contract_address,
            number_owners,
            gas_price,
            payment_token,
        )
        self.assertGreater(safe_creation_estimate.gas_price, 0)
        self.assertGreater(safe_creation_estimate.gas, 0)
        self.assertGreater(safe_creation_estimate.payment, 0)
        self.assertEqual(safe_creation_estimate.payment_token, payment_token)

        salt_nonce = 167
        owners = [Account.create().address for _ in range(number_owners)]
        threshold = 1
        safe_creation_2 = Safe.build_safe_create2_tx(
            self.ethereum_client,
            self.safe_contract_address,
            self.proxy_factory_contract_address,
            salt_nonce,
            owners,
            threshold,
            gas_price,
            payment_token,
            fallback_handler=Account.create().address,
        )
        self.assertAlmostEqual(
            safe_creation_2.gas, safe_creation_estimate.gas, delta=1000
        )

    def test_retrieve_master_copy_address(self):
        # Test with master copy starting by 0x00
        master_copy_address = "0x004e2e9E6D637b8138B022D16083093Cb2Ee76aa"
        ethereum_tx_send = self.proxy_factory.deploy_proxy_contract(
            self.ethereum_test_account, master_copy_address
        )
        safe = Safe(ethereum_tx_send.contract_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_master_copy_address(), master_copy_address)

    def test_send_multisig_tx(self):
        # Create Safe
        w3 = self.w3
        funder_account = self.ethereum_test_account
        funder = funder_account.address
        owners_with_keys = [get_eth_address_with_key(), get_eth_address_with_key()]
        # Signatures must be sorted!
        owners_with_keys.sort(key=lambda x: x[0].lower())
        owners = [x[0] for x in owners_with_keys]
        keys = [x[1] for x in owners_with_keys]
        threshold = len(owners_with_keys)

        safe = self.deploy_test_safe(threshold=threshold, owners=owners)
        my_safe_address = safe.address

        # The balance we will send to the safe
        safe_balance = w3.toWei(0.02, "ether")

        # Send something to the owner[0], who will be sending the tx
        owner0_balance = safe_balance
        self.send_tx({"to": owners[0], "value": owner0_balance}, funder_account)

        my_safe_contract = get_safe_contract(w3, my_safe_address)
        safe = Safe(my_safe_address, self.ethereum_client)

        to = funder
        value = safe_balance // 2
        data = HexBytes("")
        operation = 0
        safe_tx_gas = 100000
        base_gas = 300000
        gas_price = 1
        gas_token = NULL_ADDRESS
        refund_receiver = NULL_ADDRESS
        nonce = None
        safe_multisig_tx = safe.build_multisig_tx(
            to=to,
            value=value,
            data=data,
            operation=operation,
            safe_tx_gas=safe_tx_gas,
            base_gas=base_gas,
            gas_price=gas_price,
            gas_token=gas_token,
            refund_receiver=refund_receiver,
            safe_nonce=nonce,
        )
        safe_multisig_tx_hash = safe_multisig_tx.safe_tx_hash

        nonce = safe.retrieve_nonce()
        self.assertEqual(
            safe.build_multisig_tx(
                to=to,
                value=value,
                data=data,
                operation=operation,
                safe_tx_gas=safe_tx_gas,
                base_gas=base_gas,
                gas_price=gas_price,
                gas_token=gas_token,
                refund_receiver=refund_receiver,
                safe_nonce=nonce,
            ).safe_tx_hash,
            safe_multisig_tx_hash,
        )
        # Just to make sure we are not miscalculating tx_hash
        contract_multisig_tx_hash = my_safe_contract.functions.getTransactionHash(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            nonce,
        ).call()

        self.assertEqual(safe_multisig_tx_hash, contract_multisig_tx_hash)

        for private_key in keys:
            safe_multisig_tx.sign(private_key)

        signatures = safe_multisig_tx.signatures
        self.assertEqual(set(safe_multisig_tx.signers), set(owners))

        # Check owners are the same
        contract_owners = my_safe_contract.functions.getOwners().call()
        self.assertEqual(set(contract_owners), set(owners))
        self.assertEqual(w3.eth.get_balance(owners[0]), owner0_balance)

        # with self.assertRaises(CouldNotPayGasWithEther):
        # Ganache v7 does not raise CouldNotPayGasWithEther anymore
        with self.assertRaises(InvalidInternalTx):
            safe.send_multisig_tx(
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                base_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signatures,
                tx_sender_private_key=keys[0],
                tx_gas_price=self.gas_price,
            )

        # Send something to the safe
        self.send_tx({"to": my_safe_address, "value": safe_balance}, funder_account)

        ethereum_tx_sent = safe.send_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
            tx_sender_private_key=keys[0],
            tx_gas_price=self.gas_price,
        )

        tx_receipt = w3.eth.wait_for_transaction_receipt(ethereum_tx_sent.tx_hash)
        self.assertTrue(tx_receipt["status"])
        owner0_new_balance = w3.eth.get_balance(owners[0])
        gas_used = tx_receipt["gasUsed"]
        gas_cost = gas_used * self.gas_price
        estimated_payment = (base_gas + gas_used) * gas_price
        real_payment = owner0_new_balance - (owner0_balance - gas_cost)
        # Estimated payment will be bigger, because it uses all the tx gas. Real payment only uses gas left
        # in the point of calculation of the payment, so it will be slightly lower
        self.assertTrue(estimated_payment > real_payment > 0)
        self.assertTrue(
            owner0_new_balance
            > owner0_balance - ethereum_tx_sent.tx["gas"] * self.gas_price
        )
        self.assertEqual(safe.retrieve_nonce(), 1)

    def test_send_multisig_tx_gas_token(self):
        # Create safe with one owner, fund the safe and the owner with `safe_balance`
        receiver, _ = get_eth_address_with_key()
        threshold = 1
        funder_account = self.ethereum_test_account
        funder = funder_account.address
        safe_balance_ether = 0.02
        safe_balance = self.w3.toWei(safe_balance_ether, "ether")
        owner_account = self.create_account(initial_ether=safe_balance_ether)
        owner = owner_account.address

        safe = self.deploy_test_safe(
            threshold=threshold, owners=[owner], initial_funding_wei=safe_balance
        )
        my_safe_address = safe.address

        # Give erc20 tokens to the funder
        amount_token = int(1e18)
        erc20_contract = self.deploy_example_erc20(amount_token, funder)
        self.assertEqual(
            self.ethereum_client.erc20.get_balance(funder, erc20_contract.address),
            amount_token,
        )

        signature_packed = signature_to_bytes(1, int(owner, 16), 0)

        to = receiver
        value = safe_balance
        data = HexBytes("")
        operation = 0
        safe_tx_gas = 100000
        base_gas = 300000
        gas_price = 2
        gas_token = erc20_contract.address
        refund_receiver = NULL_ADDRESS

        with self.assertRaises(CouldNotPayGasWithToken):
            safe.send_multisig_tx(
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                base_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signature_packed,
                tx_sender_private_key=owner_account.key,
                tx_gas_price=self.gas_price,
            )

        # Give erc20 tokens to the safe
        self.ethereum_client.erc20.send_tokens(
            my_safe_address, amount_token, erc20_contract.address, funder_account.key
        )

        safe.send_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signature_packed,
            tx_sender_private_key=owner_account.key,
            tx_gas_price=self.gas_price,
        )

        safe_token_balance = self.ethereum_client.erc20.get_balance(
            my_safe_address, erc20_contract.address
        )

        # Token was used for tx gas costs. Sender must have some tokens now and safe should have less
        self.assertLess(safe_token_balance, amount_token)
        owner_token_balance = self.ethereum_client.erc20.get_balance(
            owner, erc20_contract.address
        )
        self.assertGreater(owner_token_balance, 0)

        # All ether on safe was transferred to receiver
        receiver_balance = self.w3.eth.get_balance(receiver)
        self.assertEqual(receiver_balance, safe_balance)

    def test_estimate_tx_base_gas(self):
        safe = self.deploy_test_safe()
        to = Account().create().address
        value = int("abc", 16)
        data = HexBytes("0xabcdef")
        operation = 1
        gas_token = NULL_ADDRESS
        estimate_tx_gas = int("ccdd", 16)
        base_gas = safe.estimate_tx_base_gas(
            to, value, data, operation, gas_token, estimate_tx_gas
        )
        self.assertGreater(base_gas, 0)

        data = HexBytes(
            "0xabcdefbb"
        )  # A byte that was 00 now is bb, so -4 + GAS_CALL_DATA_BYTE
        data_gas2 = safe.estimate_tx_base_gas(
            to, value, data, operation, gas_token, estimate_tx_gas
        )
        self.assertEqual(data_gas2, base_gas + GAS_CALL_DATA_BYTE - 4)

    def test_estimate_tx_gas(self):
        to = Account().create().address
        value = 123
        data = HexBytes("0xabcdef")
        operation = 1
        safe = self.deploy_test_safe(initial_funding_wei=value + 23000)

        safe_tx_gas = safe.estimate_tx_gas(to, value, data, operation)
        self.assertGreater(safe_tx_gas, 0)
        operation = 0
        safe_tx_gas = safe.estimate_tx_gas(to, value, data, operation)
        self.assertGreater(safe_tx_gas, 0)

    def test_estimate_tx_gas_nested_transaction(self):
        """
        Test estimation with a contract that uses a lot of gas
        """

        # Uncomment this to regenerate the contract. I hardcoded it to prevent the app testing depending on solc
        # Remember to install `py-solc` and have `solidity` in your system
        """
        from solc import compile_standard
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {
                "Nester.sol": {
                    "content": '''
                        contract Nester {
                            uint256[] public data;
                            constructor() public payable {}
                            function nested(uint256 level, uint256 count) external {
                                if (level == 0) {
                                    for (uint256 i = 0; i < count; i++) {
                                        data.push(i);
                                    }
                                    return;
                                }
                                this.nested(level - 1, count);
                            }
                            function useGas(uint256 count) public {
                                this.nested(6, count);
                                this.nested(8, count);
                            }
                        }
                    '''
                }
            },
            "settings":
                {
                    "outputSelection": {

                        "*": {
                            "*": [
                                "metadata", "evm.bytecode"
                                , "evm.bytecode.sourceMap"
                            ]
                        }
                    }
                }
        })
        contract_data = compiled_sol['contracts']['Nester.sol']['Nester']
        bytecode = contract_data['evm']['bytecode']['object']
        abi = json.loads(contract_data['metadata'])['output']['abi']
        """

        bytecode = "60806040526102fe806100136000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063022952b81461004657806350d1f08214610074578063f0ba8440146100ac575b600080fd5b6100726004803603602081101561005c57600080fd5b81019080803590602001909291905050506100ee565b005b6100aa6004803603604081101561008a57600080fd5b8101908080359060200190929190803590602001909291905050506101d9565b005b6100d8600480360360208110156100c257600080fd5b81019080803590602001909291905050506102a7565b6040518082815260200191505060405180910390f35b3073ffffffffffffffffffffffffffffffffffffffff166350d1f0826006836040518363ffffffff1660e01b81526004018083815260200182815260200192505050600060405180830381600087803b15801561014a57600080fd5b505af115801561015e573d6000803e3d6000fd5b505050503073ffffffffffffffffffffffffffffffffffffffff166350d1f0826008836040518363ffffffff1660e01b81526004018083815260200182815260200192505050600060405180830381600087803b1580156101be57600080fd5b505af11580156101d2573d6000803e3d6000fd5b5050505050565b600082141561022c5760008090505b8181101561022657600081908060018154018082558091505060019003906000526020600020016000909190919091505580806001019150506101e8565b506102a3565b3073ffffffffffffffffffffffffffffffffffffffff166350d1f08260018403836040518363ffffffff1660e01b81526004018083815260200182815260200192505050600060405180830381600087803b15801561028a57600080fd5b505af115801561029e573d6000803e3d6000fd5b505050505b5050565b600081815481106102b457fe5b90600052602060002001600091509050548156fea264697066735822122091b08fac39dd94b262ed9adf68b679a88140319e98d18d4c918bd5a1d93527fc64736f6c63430006040033"
        abi = [
            {"inputs": [], "stateMutability": "payable", "type": "constructor"},
            {
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "data",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "level", "type": "uint256"},
                    {"internalType": "uint256", "name": "count", "type": "uint256"},
                ],
                "name": "nested",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "count", "type": "uint256"}
                ],
                "name": "useGas",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ]

        nester_contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = nester_contract.constructor().transact(
            {"from": self.w3.eth.accounts[0]}
        )
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        nester = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

        safe = self.deploy_test_safe(
            owners=[self.ethereum_test_account.address],
            initial_funding_wei=self.w3.toWei(0.1, "ether"),
        )
        nester_tx = nester.functions.useGas(80).build_transaction(
            {"gasPrice": 1, "from": safe.address, "gas": 1}
        )
        nester_data = nester_tx["data"]

        safe_tx_gas_no_call = safe.estimate_tx_gas_with_safe(
            nester.address, 0, nester_data, SafeOperation.CALL.value
        )
        safe_tx_gas = safe.estimate_tx_gas_by_trying(
            nester.address, 0, nester_data, SafeOperation.CALL.value
        )
        self.assertGreater(safe_tx_gas, safe_tx_gas_no_call)

        base_gas = safe.estimate_tx_base_gas(
            nester.address,
            0,
            nester_data,
            SafeOperation.CALL.value,
            NULL_ADDRESS,
            safe_tx_gas,
        )

        refund_receiver = Account.create().address
        safe_tx = safe.build_multisig_tx(
            nester.address,
            0,
            nester_data,
            safe_tx_gas=safe_tx_gas,
            base_gas=base_gas,
            gas_price=1,
            refund_receiver=refund_receiver,
        )
        safe_tx.sign(self.ethereum_test_account.key)

        self.assertTrue(
            safe_tx.call(tx_sender_address=self.ethereum_test_account.address)
        )

        safe_tx_hash, safe_w3_tx = safe_tx.execute(self.ethereum_test_account.key)
        self.w3.eth.wait_for_transaction_receipt(safe_tx_hash)

        # Tx was successfully executed if refund_receiver gets ether
        self.assertGreater(self.ethereum_client.get_balance(refund_receiver), 0)

    def test_estimate_tx_gas_with_web3(self):
        safe = self.deploy_test_safe(
            owners=[self.ethereum_test_account.address],
            initial_funding_wei=self.w3.toWei(0.1, "ether"),
        )
        to = Account.create().address
        value = self.w3.toWei(0.01, "ether")
        data = b""
        gas_estimated_web3 = safe.estimate_tx_gas_with_web3(to, value, data)
        gas_estimated_safe = safe.estimate_tx_gas_with_safe(to, value, data, 0)
        self.assertGreater(
            gas_estimated_safe, gas_estimated_web3
        )  # Web3 estimation should use less gas
        self.assertGreater(gas_estimated_web3, 0)
        self.assertGreater(gas_estimated_safe, 0)

        with self.assertRaises(CannotEstimateGas):
            deployed_erc20 = self.deploy_example_erc20(100, Account.create().address)
            transfer_data = deployed_erc20.functions.transfer(
                to, 200
            ).build_transaction({"gas": 0})["data"]
            safe.estimate_tx_gas_with_web3(deployed_erc20.address, value, transfer_data)

    def test_estimate_tx_operational_gas(self):
        for threshold in range(2, 5):
            safe = self.deploy_test_safe(threshold=threshold, number_owners=6)
            tx_signature_gas_estimation = safe.estimate_tx_operational_gas(0)
            self.assertGreaterEqual(tx_signature_gas_estimation, 20000)

    def test_retrieve_code(self):
        self.assertEqual(
            Safe(NULL_ADDRESS, self.ethereum_client).retrieve_code(), HexBytes("0x")
        )
        self.assertIsNotNone(self.deploy_test_safe().retrieve_code())

    def test_retrieve_fallback_handler(self):
        random_fallback_handler = Account.create().address
        safe = self.deploy_test_safe(fallback_handler=random_fallback_handler)
        self.assertEqual(safe.retrieve_fallback_handler(), random_fallback_handler)

    def test_retrieve_guard(self):
        # Test guard in a Safe < 1.2
        owner_account = Account.create()
        safe_v1_1_1 = self.deploy_test_safe_v1_1_1()
        self.assertEqual(safe_v1_1_1.retrieve_guard(), NULL_ADDRESS)
        self.assertLess(Version(safe_v1_1_1.retrieve_version()), Version("1.3.0"))

        safe = self.deploy_test_safe(owners=[owner_account.address])
        self.assertEqual(safe.retrieve_guard(), NULL_ADDRESS)
        self.assertGreaterEqual(Version(safe.retrieve_version()), Version("1.3.0"))

        guard_address = Account.create().address
        set_guard_data = HexBytes(
            safe.contract.functions.setGuard(guard_address).build_transaction(
                {"gas": 1, "gasPrice": 1}
            )["data"]
        )
        set_guard_tx = safe.build_multisig_tx(safe.address, 0, set_guard_data)
        set_guard_tx.sign(owner_account.key)
        set_guard_tx.execute(self.ethereum_test_account.key)
        self.assertEqual(safe.retrieve_guard(), guard_address)

    def test_retrieve_info(self):
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        safe_v1_0_0 = self.deploy_test_safe_v1_0_0(owners=owners, threshold=threshold)
        safe_v1_3_0 = self.deploy_test_safe(owners=owners, threshold=threshold)

        for safe, master_copy_address in (
            (safe_v1_0_0, self.safe_contract_V1_0_0_address),
            (safe_v1_3_0, self.safe_contract_address),
        ):
            self.assertEqual(safe.retrieve_master_copy_address(), master_copy_address)
            self.assertEqual(safe.retrieve_nonce(), 0)
            self.assertCountEqual(safe.retrieve_owners(), owners)
            self.assertEqual(safe.retrieve_threshold(), threshold)
            self.assertEqual(safe.retrieve_modules(), [])

            # Versions must be semantic, like 0.1.0, so we count 3 points
            self.assertTrue(safe.retrieve_version().count("."), 3)

            for owner in owners:
                self.assertTrue(safe.retrieve_is_owner(owner))

    def test_retrieve_all_info(self):
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        safe_v1_0_0 = self.deploy_test_safe_v1_0_0(owners=owners, threshold=threshold)
        safe_v1_3_0 = self.deploy_test_safe(owners=owners, threshold=threshold)

        for safe, master_copy_address in (
            (safe_v1_0_0, self.safe_contract_V1_0_0_address),
            (safe_v1_3_0, self.safe_contract_address),
        ):
            safe_info = safe.retrieve_all_info()
            self.assertEqual(safe_info.master_copy, master_copy_address)
            self.assertEqual(safe_info.nonce, 0)
            self.assertCountEqual(safe_info.owners, owners)
            self.assertEqual(safe_info.threshold, threshold)
            self.assertEqual(safe_info.modules, [])

            invalid_address = Account.create().address
            invalid_safe = Safe(invalid_address, self.ethereum_client)
            with self.assertRaisesMessage(
                CannotRetrieveSafeInfoException, invalid_address
            ):
                invalid_safe.retrieve_all_info()

    def test_retrieve_modules(self):
        safe = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        safe_contract = safe.contract
        module_address = Account.create().address
        self.assertEqual(safe.retrieve_modules(), [])

        tx = safe_contract.functions.enableModule(module_address).build_transaction(
            {"from": self.ethereum_test_account.address, "gas": 0, "gasPrice": 0}
        )
        safe_tx = safe.build_multisig_tx(safe.address, 0, tx["data"])
        safe_tx.sign(self.ethereum_test_account.key)
        safe_tx.execute(
            tx_sender_private_key=self.ethereum_test_account.key,
            tx_gas_price=self.gas_price,
        )
        self.assertEqual(safe.retrieve_modules(), [module_address])

        more_modules = [Account.create().address for _ in range(2)]
        for more_module in more_modules:
            # Test pagination
            tx = safe_contract.functions.enableModule(more_module).build_transaction(
                {"from": self.ethereum_test_account.address, "gas": 0, "gasPrice": 0}
            )
            safe_tx = safe.build_multisig_tx(safe.address, 0, tx["data"])
            safe_tx.sign(self.ethereum_test_account.key)
            safe_tx.execute(
                tx_sender_private_key=self.ethereum_test_account.key,
                tx_gas_price=self.gas_price,
            )

        self.assertCountEqual(
            safe.retrieve_modules(pagination=1), [module_address] + more_modules
        )

    def test_retrieve_is_hash_approved(self):
        safe = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        safe_contract = safe.contract
        fake_tx_hash = Web3.keccak(text="Knopfler")
        another_tx_hash = Web3.keccak(text="Marc")
        tx = safe_contract.functions.approveHash(fake_tx_hash).build_transaction(
            {"from": self.ethereum_test_account.address}
        )

        self.ethereum_client.send_unsigned_transaction(
            tx, private_key=self.ethereum_test_account.key
        )
        self.assertTrue(
            safe.retrieve_is_hash_approved(
                self.ethereum_test_account.address, fake_tx_hash
            )
        )
        self.assertFalse(
            safe.retrieve_is_hash_approved(
                self.ethereum_test_account.address, another_tx_hash
            )
        )

    def test_retrieve_is_message_signed(self):
        safe = self.deploy_test_safe_v1_1_1(owners=[self.ethereum_test_account.address])
        safe_contract = safe.contract
        message = b"12345"
        message_hash = safe_contract.functions.getMessageHash(message).call()
        sign_message_data = HexBytes(
            safe_contract.functions.signMessage(message).build_transaction({"gas": 0})[
                "data"
            ]
        )
        safe_tx = safe.build_multisig_tx(safe.address, 0, sign_message_data)
        safe_tx.sign(self.ethereum_test_account.key)
        safe_tx.execute(tx_sender_private_key=self.ethereum_test_account.key)
        self.assertTrue(safe.retrieve_is_message_signed(message_hash))

    def test_retrieve_is_owner(self):
        safe = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        self.assertTrue(safe.retrieve_is_owner(self.ethereum_test_account.address))
        self.assertFalse(safe.retrieve_is_owner(Account.create().address))

    def test_token_balance(self):
        funder_account = self.ethereum_test_account
        funder = funder_account.address
        amount = 200
        deployed_erc20 = self.deploy_example_erc20(amount, funder)

        safe = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe.address

        balance = self.ethereum_client.erc20.get_balance(
            my_safe_address, deployed_erc20.address
        )
        self.assertEqual(balance, 0)

        transfer_tx = deployed_erc20.functions.transfer(
            my_safe_address, amount
        ).build_transaction({"from": funder})
        self.send_tx(transfer_tx, funder_account)

        balance = self.ethereum_client.erc20.get_balance(
            my_safe_address, deployed_erc20.address
        )
        self.assertEqual(balance, amount)

    # TODO Test approve tx from another contract
    def test_send_previously_approved_tx(self):
        number_owners = 4
        accounts = [
            self.create_account(initial_ether=0.01) for _ in range(number_owners)
        ]
        accounts.sort(key=lambda x: x.address.lower())
        owners = [account.address for account in accounts]

        safe = self.deploy_test_safe(
            threshold=2, owners=owners, initial_funding_wei=self.w3.toWei(0.01, "ether")
        )
        safe_address = safe.address
        safe = Safe(safe_address, self.ethereum_client)
        safe_instance = get_safe_contract(self.w3, safe_address)

        to, _ = get_eth_address_with_key()
        value = self.w3.toWei(0.001, "ether")
        data = b""
        operation = 0
        safe_tx_gas = 500000
        data_gas = 500000
        gas_price = 1
        gas_token = NULL_ADDRESS
        refund_receiver = NULL_ADDRESS
        nonce = safe.retrieve_nonce()

        self.assertEqual(nonce, 0)

        safe_tx_hash = safe.build_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            safe_nonce=nonce,
        ).safe_tx_hash

        safe_tx_contract_hash = safe_instance.functions.getTransactionHash(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            nonce,
        ).call()

        self.assertEqual(safe_tx_hash, safe_tx_contract_hash)

        approve_hash_fn = safe_instance.functions.approveHash(safe_tx_hash)
        for account in accounts[:2]:
            self.send_tx(
                approve_hash_fn.build_transaction({"from": account.address}), account
            )

        for owner in (owners[0], owners[1]):
            is_approved = safe.retrieve_is_hash_approved(owner, safe_tx_hash)
            self.assertTrue(is_approved)

        # Prepare signatures. v must be 1 for previously signed and r the owner
        signatures = (1, int(owners[0], 16), 0), (1, int(owners[1], 16), 0)
        signature_bytes = signatures_to_bytes(signatures)

        safe.send_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signature_bytes,
            self.ethereum_test_account.key,
        )

        balance = self.w3.eth.get_balance(to)
        self.assertEqual(value, balance)
