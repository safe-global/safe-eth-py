from enum import Enum
from logging import getLogger
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

from eth_account import Account
from ethereum.utils import check_checksum, checksum_encode
from hexbytes import HexBytes
from packaging.version import Version

from py_eth_sig_utils.eip712 import encode_typed_data

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import (get_old_safe_contract,
                                  get_paying_proxy_contract,
                                  get_paying_proxy_deployed_bytecode,
                                  get_proxy_factory_contract,
                                  get_safe_contract)
from gnosis.eth.ethereum_client import EthereumClient, EthereumClientProvider
from gnosis.eth.utils import get_eth_address_with_key

from .exceptions import (CannotEstimateGas, InvalidChecksumAddress,
                         InvalidPaymentToken)
from .safe_create2_tx import SafeCreate2Tx, SafeCreate2TxBuilder
from .safe_creation_tx import InvalidERC20Token, SafeCreationTx
from .safe_tx import SafeTx
from .signatures import signature_split

logger = getLogger(__name__)


class SafeCreationEstimate(NamedTuple):
    gas: int
    gas_price: int
    payment: int


class SafeOperation(Enum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2


class SafeServiceProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            from django.conf import settings
            ethereum_client = EthereumClientProvider()
            cls.instance = SafeService(ethereum_client,
                                       settings.SAFE_CONTRACT_ADDRESS,
                                       settings.SAFE_OLD_CONTRACT_ADDRESS,
                                       settings.SAFE_PROXY_FACTORY_ADDRESS,
                                       settings.SAFE_VALID_CONTRACT_ADDRESSES)
        return cls.instance

    @classmethod
    def del_singleton(cls):
        if hasattr(cls, "instance"):
            del cls.instance


class SafeService:
    def __init__(self, ethereum_client: EthereumClient,
                 master_copy_address: str,
                 master_copy_old_address: str,
                 proxy_factory_address: str,
                 valid_master_copy_addresses: Set[str]):

        self.ethereum_client = ethereum_client
        self.w3 = self.ethereum_client.w3
        self.master_copy_address = master_copy_address
        self.master_copy_old_address = master_copy_old_address
        self.proxy_factory_address = proxy_factory_address
        self.provided_valid_master_copy_addresses = set(valid_master_copy_addresses)

        for address in self.valid_master_copy_addresses:
            if address and not check_checksum(address):
                raise InvalidChecksumAddress('Master copy %s has invalid checksum' % address)

        if not check_checksum(proxy_factory_address):
            raise InvalidChecksumAddress('Proxy factory %s has invalid checksum' % proxy_factory_address)

        if not master_copy_address:
            logger.warning('Master copy address for SafeService is None')

        if not master_copy_old_address:
            logger.warning('Old Master copy address for SafeService is None')

    @property
    def valid_master_copy_addresses(self):
        return self.provided_valid_master_copy_addresses.union([self.master_copy_address,
                                                                self.master_copy_old_address]) - {None}

    #FIXME Use Safe_tx hash method
    @staticmethod
    def get_hash_for_safe_tx(safe_address: str, to: str, value: int, data: bytes,
                             operation: int, safe_tx_gas: int, data_gas: int, gas_price: int,
                             gas_token: str, refund_receiver: str, nonce: int, safe_version: str = '1.0.0') -> HexBytes:

        data = data.hex() if data else ''
        gas_token = gas_token or NULL_ADDRESS
        refund_receiver = refund_receiver or NULL_ADDRESS
        to = to or NULL_ADDRESS

        data_gas_name = 'baseGas' if Version(safe_version) >= Version('1.0.0') else 'dataGas'

        data = {
            'types': {
                'EIP712Domain': [
                    {'name': 'verifyingContract', 'type': 'address'},
                ],
                'SafeTx': [
                    {'name': 'to', 'type': 'address'},
                    {'name': 'value', 'type': 'uint256'},
                    {'name': 'data', 'type': 'bytes'},
                    {'name': 'operation', 'type': 'uint8'},
                    {'name': 'safeTxGas', 'type': 'uint256'},
                    {'name': data_gas_name, 'type': 'uint256'},
                    {'name': 'gasPrice', 'type': 'uint256'},
                    {'name': 'gasToken', 'type': 'address'},
                    {'name': 'refundReceiver', 'type': 'address'},
                    {'name': 'nonce', 'type': 'uint256'}
                ]
            },
            'primaryType': 'SafeTx',
            'domain': {
                'verifyingContract': safe_address,
            },
            'message': {
                'to': to,
                'value': value,
                'data': data,
                'operation': operation,
                'safeTxGas': safe_tx_gas,
                data_gas_name: data_gas,
                'gasPrice': gas_price,
                'gasToken': gas_token,
                'refundReceiver': refund_receiver,
                'nonce': nonce,
            },
        }

        return HexBytes(encode_typed_data(data))

    @classmethod
    def check_hash(cls, tx_hash: str, signatures: bytes, owners: List[str]) -> bool:
        for i, owner in enumerate(sorted(owners, key=lambda x: x.lower())):
            v, r, s = signature_split(signatures, i)
            if EthereumClient.get_signing_address(tx_hash, v, r, s) != owner:
                return False
        return True

    def build_safe_creation_tx(self, s: int, owners: List[str], threshold: int, gas_price: int,
                               payment_token: Optional[str], payment_receiver: str,
                               payment_token_eth_value: float = 1.0,
                               fixed_creation_cost: Optional[int] = None) -> SafeCreationTx:
        try:
            safe_creation_tx = SafeCreationTx(w3=self.w3,
                                              owners=owners,
                                              threshold=threshold,
                                              signature_s=s,
                                              master_copy=self.master_copy_old_address,
                                              gas_price=gas_price,
                                              funder=payment_receiver,
                                              payment_token=payment_token,
                                              payment_token_eth_value=payment_token_eth_value,
                                              fixed_creation_cost=fixed_creation_cost)
        except InvalidERC20Token as exc:
            raise InvalidPaymentToken('Invalid payment token %s' % payment_token) from exc

        assert safe_creation_tx.tx_pyethereum.nonce == 0
        return safe_creation_tx

    def build_safe_create2_tx(self, salt_nonce: int, owners: List[str], threshold: int, gas_price: int,
                              payment_token: Optional[str],
                              payment_receiver: Optional[str] = None,  # If none, it will be `tx.origin`
                              payment_token_eth_value: float = 1.0,
                              fixed_creation_cost: Optional[int] = None) -> SafeCreate2Tx:
        try:
            safe_creation_tx = SafeCreate2TxBuilder(w3=self.w3,
                                                    master_copy_address=self.master_copy_address,
                                                    proxy_factory_address=self.proxy_factory_address
                                                    ).build(owners=owners,
                                                            threshold=threshold,
                                                            salt_nonce=salt_nonce,
                                                            gas_price=gas_price,
                                                            payment_receiver=payment_receiver,
                                                            payment_token=payment_token,
                                                            payment_token_eth_value=payment_token_eth_value,
                                                            fixed_creation_cost=fixed_creation_cost)
        except InvalidERC20Token as exc:
            raise InvalidPaymentToken('Invalid payment token %s' % payment_token) from exc

        return safe_creation_tx

    def check_master_copy(self, address) -> bool:
        return self.retrieve_master_copy_address(address) in self.valid_master_copy_addresses

    def check_proxy_code(self, address) -> bool:
        """
        Check if proxy is valid
        :param address: address of the proxy
        :return: True if proxy is valid, False otherwise
        """
        deployed_proxy_code = self.w3.eth.getCode(address)
        proxy_code_fns = (get_paying_proxy_deployed_bytecode,
                          get_proxy_factory_contract(self.w3,
                                                     self.proxy_factory_address).functions.proxyRuntimeCode().call)
        for proxy_code_fn in proxy_code_fns:
            if deployed_proxy_code == proxy_code_fn():
                return True
        return False

    def check_funds_for_tx_gas(self, safe_address: str, safe_tx_gas: int, data_gas: int, gas_price: int,
                               gas_token: str) -> bool:
        """
        Check safe has enough funds to pay for a tx
        :param safe_address: Address of the safe
        :param safe_tx_gas: Start gas
        :param data_gas: Data gas
        :param gas_price: Gas Price
        :param gas_token: Gas Token, to use token instead of ether for the gas
        :return: True if enough funds, False, otherwise
        """
        if gas_token == NULL_ADDRESS:
            balance = self.ethereum_client.get_balance(safe_address)
        else:
            balance = self.ethereum_client.erc20.get_balance(safe_address, gas_token)
        return balance >= (safe_tx_gas + data_gas) * gas_price

    def deploy_master_contract(self, deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key
        deployer_address = deployer_account or self.ethereum_client.private_key_to_address(deployer_private_key)

        safe_contract = self.get_contract()
        tx = safe_contract.constructor().buildTransaction({'from': deployer_address})
        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)

        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        contract_address = tx_receipt.contractAddress

        # Init master copy
        master_safe = self.get_contract(contract_address)
        tx = master_safe.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            ["0x0000000000000000000000000000000000000002", "0x0000000000000000000000000000000000000003"],
            2,             # Threshold. Maximum security
            NULL_ADDRESS,  # Address for optional DELEGATE CALL
            b'',           # Data for optional DELEGATE CALL
            NULL_ADDRESS,  # Payment token
            0,             # Payment
            NULL_ADDRESS   # Refund receiver
        ).buildTransaction({'from': deployer_address})

        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)

        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        logger.info("Deployed and initialized Safe Master Contract=%s by %s", contract_address, deployer_address)
        return contract_address

    def deploy_old_master_contract(self, deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key
        deployer_address = deployer_account or self.ethereum_client.private_key_to_address(deployer_private_key)

        safe_contract = get_old_safe_contract(self.w3)
        tx = safe_contract.constructor().buildTransaction({'from': deployer_address})
        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)

        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        contract_address = tx_receipt.contractAddress

        # Init master copy
        master_safe = get_old_safe_contract(self.w3, contract_address)
        tx = master_safe.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            ["0x0000000000000000000000000000000000000002", "0x0000000000000000000000000000000000000003"],
            2,             # Threshold. Maximum security
            NULL_ADDRESS,  # Address for optional DELEGATE CALL
            b''            # Data for optional DELEGATE CALL
        ).buildTransaction({'from': deployer_address})

        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)

        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        logger.info("Deployed and initialized Old Safe Master Contract=%s by %s", contract_address, deployer_address)
        return contract_address

    def deploy_paying_proxy_contract(self, initializer=b'', deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy proxy contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param initializer: Initializer
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key
        deployer_address = deployer_account or self.ethereum_client.private_key_to_address(deployer_private_key)

        safe_proxy_contract = get_paying_proxy_contract(self.w3)
        tx = safe_proxy_contract.constructor(self.master_copy_address, initializer,
                                             NULL_ADDRESS,
                                             NULL_ADDRESS, 0).buildTransaction({'from': deployer_address})

        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)
        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status
        return tx_receipt.contractAddress

    def deploy_proxy_contract(self, initializer=b'', deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy proxy contract using the `Proxy Factory Contract`.
        Takes deployer_account (if unlocked in the node) or the deployer private key
        :param initializer: Initializer
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key
        deployer_address = deployer_account or self.ethereum_client.private_key_to_address(deployer_private_key)

        proxy_factory_contract = get_proxy_factory_contract(self.w3, self.proxy_factory_address)
        create_proxy_fn = proxy_factory_contract.functions.createProxy(self.master_copy_address, initializer)
        contract_address = create_proxy_fn.call()
        tx = create_proxy_fn.buildTransaction({'from': deployer_address})

        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)
        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt.status
        return contract_address

    def deploy_proxy_contract_with_nonce(self, salt_nonce: int, initializer: bytes, gas: int, gas_price: int,
                                         deployer_private_key=None) -> Tuple[bytes, Dict[str, any], str]:
        """
        Deploy proxy contract using `create2` withthe `Proxy Factory Contract`.
        Takes `deployer_account` (if unlocked in the node) or the `deployer_private_key`
        :param salt_nonce: Uint256 for `create2` salt
        :param initializer: Data for safe creation
        :param gas: Gas
        :param gas_price: Gas Price
        :param deployer_private_key: Private key of an ethereum account
        :return: Tuple(tx-hash, tx, deployed contract address)
        """
        assert deployer_private_key

        proxy_factory_contract = get_proxy_factory_contract(self.w3, self.proxy_factory_address)
        create_proxy_fn = proxy_factory_contract.functions.createProxyWithNonce(self.master_copy_address, initializer,
                                                                                salt_nonce)
        contract_address = create_proxy_fn.call()

        deployer_account = Account.privateKeyToAccount(deployer_private_key)
        nonce = self.ethereum_client.get_nonce_for_account(deployer_account.address, 'pending')
        # Auto estimation of gas does not work. We use a little more gas just in case
        tx = create_proxy_fn.buildTransaction({'from': deployer_account.address, 'gasPrice': gas_price,
                                               'nonce': nonce, 'gas': gas + 50000})
        signed_tx = deployer_account.signTransaction(tx)
        tx_hash = self.ethereum_client.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash, tx, contract_address

    def deploy_proxy_factory_contract(self, deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy proxy factory contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key
        deployer_address = deployer_account or self.ethereum_client.private_key_to_address(deployer_private_key)

        proxy_factory_contract = get_proxy_factory_contract(self.w3)
        tx = proxy_factory_contract.constructor().buildTransaction({'from': deployer_address})

        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_private_key,
                                                                  public_key=deployer_account)

        tx_receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt.status
        contract_address = tx_receipt.contractAddress
        logger.info("Deployed and initialized Proxy Factory Contract=%s by %s", contract_address, deployer_address)
        return contract_address

    def estimate_safe_creation(self, number_owners: int, gas_price: int, payment_token: Optional[str],
                               payment_receiver: str = NULL_ADDRESS,
                               payment_token_eth_value: float = 1.0,
                               fixed_creation_cost: Optional[int] = None) -> SafeCreationEstimate:
        s = 15
        owners = [get_eth_address_with_key()[0] for _ in range(number_owners)]
        threshold = number_owners
        safe_creation_tx = self.build_safe_creation_tx(s, owners, threshold, gas_price, payment_token,
                                                       payment_receiver,
                                                       payment_token_eth_value=payment_token_eth_value,
                                                       fixed_creation_cost=fixed_creation_cost)
        return SafeCreationEstimate(safe_creation_tx.gas, safe_creation_tx.gas_price, safe_creation_tx.payment)

    def estimate_tx_data_gas(self, safe_address: str, to: str, value: int, data: bytes,
                             operation: int, gas_token: str, estimate_tx_gas: int) -> int:
        data = data or b''
        safe_contract = self.get_contract(safe_address)
        threshold = self.retrieve_threshold(safe_address)

        # Every byte == 0 -> 4  Gas
        # Every byte != 0 -> 68 Gas
        # numbers < 256 (0x00(31*2)..ff) are 192 -> 31 * 4 + 1 * 68
        # numbers < 65535 (0x(30*2)..ffff) are 256 -> 30 * 4 + 2 * 68

        # Calculate gas for signatures
        # (array count (3 -> r, s, v) + ecrecover costs) * signature count
        signature_gas = threshold * (1 * 68 + 2 * 32 * 68 + 6000)

        safe_tx_gas = estimate_tx_gas
        data_gas = 0
        gas_price = 1
        gas_token = gas_token or NULL_ADDRESS
        signatures = b''
        refund_receiver = NULL_ADDRESS
        data = HexBytes(safe_contract.functions.execTransaction(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
        ).buildTransaction({
            'gas': 1,
            'gasPrice': 1
        })['data'])

        # TODO If nonce>0 add 5000, else 20000
        nonce_gas = 20000
        hash_generation_gas = 1500
        data_gas = signature_gas + self.ethereum_client.estimate_data_gas(data) + nonce_gas + hash_generation_gas

        # Add aditional gas costs
        if data_gas > 65536:
            data_gas += 64
        else:
            data_gas += 128

        data_gas += 32000  # Base tx costs, transfer costs...

        return data_gas

    def estimate_tx_gas_with_safe(self, safe_address: str, to: str, value: int, data: bytes, operation: int,
                                  block_identifier='pending') -> int:
        """
        Estimate tx gas using safe `requiredTxGas` method
        :return: int: Estimated gas
        :raises: CannotEstimateGas: If gas cannot be estimated
        :raises: ValueError: Cannot decode received data
        """

        data = data or b''

        def parse_revert_data(result: bytes) -> int:
            # 4 bytes - error method id
            # 32 bytes - position
            # 32 bytes - length
            # Last 32 bytes - value of revert (if everything went right)
            gas_estimation_offset = 4 + 32 + 32
            estimated_gas = result[gas_estimation_offset:]

            # Estimated gas must be 32 bytes
            if len(estimated_gas) != 32:
                logger.warning('Safe=%s Problem estimating gas, returned value is %s for tx=%s',
                               safe_address, result.hex(), tx)
                raise CannotEstimateGas('Received %s for tx=%s' % (result.hex(), tx))

            return int(estimated_gas.hex(), 16)

        # Add 10k, else we will fail in case of nested calls
        try:
            tx = self.get_contract(safe_address).functions.requiredTxGas(
                to,
                value,
                data,
                operation
            ).buildTransaction({
                'from': safe_address,
                'gas': int(1e7),
                'gasPrice': 0,
            })
            # If we build the tx web3 will not try to decode it for us
            # Ganache 6.3.0 and Geth are working like this
            result: HexBytes = self.w3.eth.call(tx, block_identifier=block_identifier)
            return parse_revert_data(result)
        except ValueError as exc:  # Parity
            """
            Parity throws a ValueError, e.g.
            {'code': -32015,
             'message': 'VM execution error.',
             'data': 'Reverted 0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000
                      000000000000000000000000000000000000000000000002c4d6574686f642063616e206f6e6c792062652063616c6c656
                      42066726f6d207468697320636f6e74726163740000000000000000000000000000000000000000'}
            """
            error_dict = exc.args[0]
            data = error_dict.get('data')
            if not data:
                raise exc
            elif isinstance(data, str) and 'Reverted ' in data:
                # Parity
                result = HexBytes(data.replace('Reverted ', ''))
                return parse_revert_data(result)

            key = list(data.keys())[0]
            result = data[key]['return']
            if result == '0x0':
                raise exc
            else:
                # Ganache-Cli with no `--noVMErrorsOnRPCResponse` flag enabled
                logger.warning('You should use `--noVMErrorsOnRPCResponse` flag with Ganache-cli')
                estimated_gas_hex = result[138:]
                assert len(estimated_gas_hex) == 64
                estimated_gas = int(estimated_gas_hex, 16)
                return estimated_gas

    def estimate_tx_gas_with_web3(self, safe_address: str, to: str, value: int, data: bytes) -> int:
        """
        Estimate tx gas using web3
        """
        return self.ethereum_client.estimate_gas(safe_address, to, value, data, block_identifier='pending')

    def estimate_tx_gas(self, safe_address: str, to: str, value: int, data: bytes, operation: int) -> int:
        """
        Estimate tx gas. Use the max of calculation using safe method and web3 if operation == CALL or
        use just the safe calculation otherwise
        """
        # Costs to route through the proxy and nested calls
        proxy_gas = 1000
        # https://github.com/ethereum/solidity/blob/dfe3193c7382c80f1814247a162663a97c3f5e67/libsolidity/codegen/ExpressionCompiler.cpp#L1764
        # This was `false` before solc 0.4.21 -> `m_context.evmVersion().canOverchargeGasForCall()`
        # So gas needed by caller will be around 35k
        old_call_gas = 35000
        safe_gas_estimation = (self.estimate_tx_gas_with_safe(safe_address, to, value, data, operation)
                               + proxy_gas + old_call_gas)
        # We cannot estimate DELEGATECALL (different storage)
        if SafeOperation(operation) == SafeOperation.CALL:
            try:
                web3_gas_estimation = (self.estimate_tx_gas_with_web3(safe_address, to, value, data)
                                       + proxy_gas + old_call_gas)
            except ValueError:
                web3_gas_estimation = 0
            return max(safe_gas_estimation, web3_gas_estimation)

        else:
            return safe_gas_estimation

    def estimate_tx_operational_gas(self, safe_address: str, data_bytes_length: int):
        """
        Estimates the gas for the verification of the signatures and other safe related tasks
        before and after executing a transaction.
        Calculation will be the sum of:
          - Base cost of 15000 gas
          - 100 of gas per word of `data_bytes`
          - Validate the signatures 5000 * threshold (ecrecover for ecdsa ~= 4K gas)
        :param safe_address: Address of the safe
        :param data_bytes_length: Length of the data (in bytes, so `len(HexBytes('0x12'))` would be `1`
        :return: gas costs per signature * threshold of Safe
        """
        threshold = self.retrieve_threshold(safe_address)
        return 15000 + data_bytes_length // 32 * 100 + 5000 * threshold

    def get_contract(self, safe_address=None):
        if safe_address:
            return get_safe_contract(self.w3, address=safe_address)
        else:
            return get_safe_contract(self.w3)

    def get_refund_receiver(self) -> str:
        return NULL_ADDRESS

    def is_master_copy_deployed(self) -> bool:
        return self.ethereum_client.is_contract(self.master_copy_address)

    def is_proxy_factory_deployed(self) -> bool:
        return self.ethereum_client.is_contract(self.proxy_factory_address)

    def is_safe_deployed(self, address: str) -> bool:
        return self.ethereum_client.is_contract(address)

    def retrieve_master_copy_address(self, safe_address, block_identifier='pending') -> str:
        return checksum_encode(self.w3.eth.getStorageAt(safe_address, 0, block_identifier=block_identifier)[-20:])

    def retrieve_is_hash_approved(self, safe_address, owner: str, safe_hash: bytes, block_identifier='pending') -> bool:
        return self.get_contract(safe_address
                                 ).functions.approvedHashes(owner,
                                                            safe_hash).call(block_identifier=block_identifier) == 1

    def retrieve_is_message_signed(self, safe_address, message_hash: bytes, block_identifier='pending') -> bool:
        return self.get_contract(safe_address
                                 ).functions.signedMessages(message_hash).call(block_identifier=block_identifier)

    def retrieve_is_owner(self, safe_address, owner: str, block_identifier='pending') -> bool:
        return self.get_contract(safe_address).functions.isOwner(owner).call(block_identifier=block_identifier)

    def retrieve_nonce(self, safe_address, block_identifier='pending') -> int:
        return self.get_contract(safe_address).functions.nonce().call(block_identifier=block_identifier)

    def retrieve_owners(self, safe_address, block_identifier='pending')-> List[str]:
        return self.get_contract(safe_address).functions.getOwners().call(block_identifier=block_identifier)

    def retrieve_threshold(self, safe_address, block_identifier='pending') -> int:
        return self.get_contract(safe_address).functions.getThreshold().call(block_identifier=block_identifier)

    def retrieve_version(self, safe_address, block_identifier='pending') -> str:
        return self.get_contract(safe_address).functions.VERSION().call(block_identifier=block_identifier)

    def build_multisig_tx(self,
                          safe_address: str,
                          to: str,
                          value: int,
                          data: bytes,
                          operation: int,
                          safe_tx_gas: int,
                          data_gas: int,
                          gas_price: int,
                          gas_token: str,
                          refund_receiver: str,
                          signatures: bytes,
                          safe_nonce: Optional[int] = None,
                          safe_version: Optional[str] = None) -> SafeTx:

        safe_nonce = safe_nonce or self.retrieve_nonce(safe_address)
        safe_version = safe_version or self.retrieve_version(safe_address)
        return SafeTx(self.ethereum_client, safe_address, to, value, data, operation, safe_tx_gas, data_gas, gas_price,
                      gas_token, refund_receiver, signatures=signatures, safe_nonce=safe_nonce,
                      safe_version=safe_version)

    def send_multisig_tx(self,
                         safe_address: str,
                         to: str,
                         value: int,
                         data: bytes,
                         operation: int,
                         safe_tx_gas: int,
                         data_gas: int,
                         gas_price: int,
                         gas_token: str,
                         refund_receiver: str,
                         signatures: bytes,
                         tx_sender_private_key: str,
                         tx_gas=None,
                         tx_gas_price=None,
                         block_identifier='pending') -> Tuple[bytes, Dict[str, any]]:
        """
        Send multisig tx to the Safe
        :param tx_gas: Gas for the external tx. If not, `(safe_tx_gas + data_gas) * 2` will be used
        :param tx_gas_price: Gas price of the external tx. If not, `gas_price` will be used
        :return: Tuple(tx_hash, tx)
        :raises: InvalidMultisigTx: If user tx cannot go through the Safe
        """

        safe_tx = self.build_multisig_tx(safe_address,
                                         to,
                                         value,
                                         data,
                                         operation,
                                         safe_tx_gas,
                                         data_gas,
                                         gas_price,
                                         gas_token,
                                         refund_receiver,
                                         signatures)

        tx_sender_address = Account.privateKeyToAccount(tx_sender_private_key).address
        safe_tx.call(tx_sender_address=tx_sender_address)

        return safe_tx.execute(tx_sender_private_key=tx_sender_private_key,
                               tx_gas=tx_gas,
                               tx_gas_price=tx_gas_price,
                               block_identifier=block_identifier)
