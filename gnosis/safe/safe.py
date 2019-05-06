from enum import Enum
from logging import getLogger
from typing import List, NamedTuple, Optional

from eth_account import Account
from eth_account.signers.local import LocalAccount
from ethereum.utils import checksum_encode
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import (get_delegate_constructor_proxy_contract,
                                  get_old_safe_contract, get_safe_contract)
from gnosis.eth.ethereum_client import EthereumClient, EthereumTxSent
from gnosis.eth.utils import get_eth_address_with_key
from gnosis.safe.proxy_factory import ProxyFactory

from .exceptions import CannotEstimateGas, InvalidPaymentToken
from .safe_create2_tx import SafeCreate2Tx, SafeCreate2TxBuilder
from .safe_creation_tx import InvalidERC20Token, SafeCreationTx
from .safe_tx import SafeTx

logger = getLogger(__name__)


class SafeCreationEstimate(NamedTuple):
    gas: int
    gas_price: int
    payment: int


class SafeOperation(Enum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2


class Safe:
    def __init__(self, address: str, ethereum_client: EthereumClient):
        assert Web3.isChecksumAddress(address), '%s is not a valid address' % address

        self.ethereum_client = ethereum_client
        self.w3 = self.ethereum_client.w3
        self.address = address

    @staticmethod
    def create(ethereum_client: EthereumClient, deployer_account: LocalAccount,
               master_copy_address: str, owners: List[str], threshold: int,
               proxy_factory_address: Optional[str] = None,
               payment_token: str = NULL_ADDRESS, payment: int = 0,
               payment_receiver: str = NULL_ADDRESS) -> EthereumTxSent:

        """
        Deploy new Safe proxy pointing to the specified `master_copy` address and configured
        with the provided `owners` and `threshold`. By default, payment for the deployer of the tx will be `0`.
        If `proxy_factory_address` is set deployment will be done using the proxy factory instead of calling
        the `constructor` of a new `DelegatedProxy`
        Using `proxy_factory_address` is recommended, as it takes less gas.
        (Testing with `Ganache` and 1 owner 261534 without proxy vs 229022 with Proxy)
        """

        assert owners, 'At least one owner must be set'
        assert threshold >= len(owners), 'Threshold=%d must be >= %d' % (threshold, len(owners))

        initializer = get_safe_contract(ethereum_client.w3, NULL_ADDRESS).functions.setup(
            owners,
            threshold,
            NULL_ADDRESS,  # Contract address for optional delegate call
            b'',  # Data payload for optional delegate call
            payment_token,
            payment,
            payment_receiver
        ).buildTransaction({'gas': 1, 'gasPrice': 1})['data']

        if proxy_factory_address:
            proxy_factory = ProxyFactory(proxy_factory_address, ethereum_client)
            return proxy_factory.deploy_proxy_contract(deployer_account, master_copy_address, initializer=initializer)

        proxy_contract = get_delegate_constructor_proxy_contract(ethereum_client.w3)
        tx = proxy_contract.constructor(master_copy_address,
                                        initializer).buildTransaction({'from': deployer_account.address})
        tx['gas'] = tx['gas'] * 100000
        tx_hash = ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.privateKey)
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        contract_address = tx_receipt.contractAddress
        return EthereumTxSent(tx_hash, tx, contract_address)

    @staticmethod
    def deploy_master_contract(ethereum_client: EthereumClient, deployer_account: LocalAccount) -> EthereumTxSent:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: deployed contract address
        """

        safe_contract = get_safe_contract(ethereum_client.w3)
        constructor_data = safe_contract.constructor().buildTransaction()['data']
        initializer_data = safe_contract.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            ["0x0000000000000000000000000000000000000002", "0x0000000000000000000000000000000000000003"],
            2,  # Threshold. Maximum security
            NULL_ADDRESS,  # Address for optional DELEGATE CALL
            b'',  # Data for optional DELEGATE CALL
            NULL_ADDRESS,  # Payment token
            0,  # Payment
            NULL_ADDRESS  # Refund receiver
        ).buildTransaction({'to': NULL_ADDRESS})['data']

        return ethereum_client.deploy_and_initialize_contract(deployer_account, constructor_data,
                                                              initializer_data)

    @staticmethod
    def deploy_old_master_contract(ethereum_client: EthereumClient, deployer_account: LocalAccount) -> EthereumTxSent:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: deployed contract address
        """

        safe_contract = get_old_safe_contract(ethereum_client.w3)
        constructor_data = safe_contract.constructor().buildTransaction()['data']
        initializer_data = safe_contract.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            ["0x0000000000000000000000000000000000000002", "0x0000000000000000000000000000000000000003"],
            2,  # Threshold. Maximum security
            NULL_ADDRESS,  # Address for optional DELEGATE CALL
            b''  # Data for optional DELEGATE CALL
        ).buildTransaction({'to': NULL_ADDRESS})['data']

        return ethereum_client.deploy_and_initialize_contract(deployer_account, constructor_data,
                                                              initializer_data)

    @staticmethod
    def estimate_safe_creation(ethereum_client: EthereumClient, old_master_copy_address: str,
                               number_owners: int, gas_price: int, payment_token: Optional[str],
                               payment_receiver: str = NULL_ADDRESS,
                               payment_token_eth_value: float = 1.0,
                               fixed_creation_cost: Optional[int] = None) -> SafeCreationEstimate:
        s = 15
        owners = [get_eth_address_with_key()[0] for _ in range(number_owners)]
        threshold = number_owners
        safe_creation_tx = SafeCreationTx(w3=ethereum_client.w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=old_master_copy_address,
                                          gas_price=gas_price,
                                          funder=payment_receiver,
                                          payment_token=payment_token,
                                          payment_token_eth_value=payment_token_eth_value,
                                          fixed_creation_cost=fixed_creation_cost)
        return SafeCreationEstimate(safe_creation_tx.gas, safe_creation_tx.gas_price, safe_creation_tx.payment)

    @staticmethod
    def estimate_safe_creation_2(ethereum_client: EthereumClient,
                                 master_copy_address: str, proxy_factory_address: str,
                                 number_owners: int, gas_price: int,
                                 payment_token: Optional[str], payment_receiver: str = NULL_ADDRESS,
                                 payment_token_eth_value: float = 1.0,
                                 fixed_creation_cost: Optional[int] = None) -> SafeCreationEstimate:
        salt_nonce = 15
        owners = [get_eth_address_with_key()[0] for _ in range(number_owners)]
        threshold = number_owners
        safe_creation_tx = SafeCreate2TxBuilder(w3=ethereum_client.w3,
                                                master_copy_address=master_copy_address,
                                                proxy_factory_address=proxy_factory_address
                                                ).build(owners=owners,
                                                        threshold=threshold,
                                                        salt_nonce=salt_nonce,
                                                        gas_price=gas_price,
                                                        payment_receiver=payment_receiver,
                                                        payment_token=payment_token,
                                                        payment_token_eth_value=payment_token_eth_value,
                                                        fixed_creation_cost=fixed_creation_cost)
        return SafeCreationEstimate(safe_creation_tx.gas, safe_creation_tx.gas_price, safe_creation_tx.payment)

    @staticmethod
    def build_safe_creation_tx(ethereum_client: EthereumClient, master_copy_old_address: str, s: int, owners: List[str],
                               threshold: int, gas_price: int,
                               payment_token: Optional[str], payment_receiver: str,
                               payment_token_eth_value: float = 1.0,
                               fixed_creation_cost: Optional[int] = None) -> SafeCreationTx:
        try:
            safe_creation_tx = SafeCreationTx(w3=ethereum_client.w3,
                                              owners=owners,
                                              threshold=threshold,
                                              signature_s=s,
                                              master_copy=master_copy_old_address,
                                              gas_price=gas_price,
                                              funder=payment_receiver,
                                              payment_token=payment_token,
                                              payment_token_eth_value=payment_token_eth_value,
                                              fixed_creation_cost=fixed_creation_cost)
        except InvalidERC20Token as exc:
            raise InvalidPaymentToken('Invalid payment token %s' % payment_token) from exc

        assert safe_creation_tx.tx_pyethereum.nonce == 0
        return safe_creation_tx

    @staticmethod
    def build_safe_create2_tx(ethereum_client: EthereumClient, master_copy_address: str, proxy_factory_address: str,
                              salt_nonce: int, owners: List[str], threshold: int, gas_price: int,
                              payment_token: Optional[str],
                              payment_receiver: Optional[str] = None,  # If none, it will be `tx.origin`
                              payment_token_eth_value: float = 1.0,
                              fixed_creation_cost: Optional[int] = None) -> SafeCreate2Tx:
        """
        Prepare safe proxy deployment for being relayed. It calculates and sets the costs of deployment to be returned
        to the sender of the tx. If you are an advanced user you may prefer to use `create` function
        """
        try:
            safe_creation_tx = SafeCreate2TxBuilder(w3=ethereum_client.w3,
                                                    master_copy_address=master_copy_address,
                                                    proxy_factory_address=proxy_factory_address
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

    def check_funds_for_tx_gas(self, safe_tx_gas: int, base_gas: int, gas_price: int, gas_token: str) -> bool:
        """
        Check safe has enough funds to pay for a tx
        :param safe_tx_gas: Safe tx gas
        :param base_gas: Data gas
        :param gas_price: Gas Price
        :param gas_token: Gas Token, to use token instead of ether for the gas
        :return: `True` if enough funds, `False` otherwise
        """
        if gas_token == NULL_ADDRESS:
            balance = self.ethereum_client.get_balance(self.address)
        else:
            balance = self.ethereum_client.erc20.get_balance(self.address, gas_token)
        return balance >= (safe_tx_gas + base_gas) * gas_price

    def estimate_tx_base_gas(self, to: str, value: int, data: bytes,
                             operation: int, gas_token: str, estimate_tx_gas: int) -> int:
        """
        Calculate gas costs that are independent of the transaction execution(e.g. base transaction fee,
        signature check, payment of the refund...)
        :param to:
        :param value:
        :param data:
        :param operation:
        :param gas_token:
        :param estimate_tx_gas: gas calculated with `estimate_tx_gas`
        :return:
        """
        data = data or b''
        safe_contract = self.get_contract()
        threshold = self.retrieve_threshold()
        nonce = self.retrieve_nonce()

        # Every byte == 0 -> 4  Gas
        # Every byte != 0 -> 68 Gas
        # numbers < 256 (0x00(31*2)..ff) are 192 -> 31 * 4 + 1 * 68
        # numbers < 65535 (0x(30*2)..ffff) are 256 -> 30 * 4 + 2 * 68

        # Calculate gas for signatures
        # (array count (3 -> r, s, v) + ecrecover costs) * signature count
        # ecrecover for ecdsa ~= 4K gas, we use 6K
        ecrecover_gas = 6000
        signature_gas = threshold * (1 * 68 + 2 * 32 * 68 + ecrecover_gas)

        safe_tx_gas = estimate_tx_gas
        base_gas = 0
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
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
        ).buildTransaction({
            'gas': 1,
            'gasPrice': 1
        })['data'])

        # If nonce == 0, nonce storage has to be initialized
        if nonce == 0:
            nonce_gas = 20000
        else:
            nonce_gas = 5000

        # Keccak costs for the hash of the safe tx
        hash_generation_gas = 1500

        base_gas = signature_gas + self.ethereum_client.estimate_data_gas(data) + nonce_gas + hash_generation_gas

        # Add additional gas costs
        if base_gas > 65536:
            base_gas += 64
        else:
            base_gas += 128

        base_gas += 32000  # Base tx costs, transfer costs...
        return base_gas

    def estimate_tx_gas_with_safe(self, to: str, value: int, data: bytes, operation: int,
                                  block_identifier='pending') -> int:
        """
        Estimate tx gas using safe `requiredTxGas` method
        :return: int: Estimated gas
        :raises: CannotEstimateGas: If gas cannot be estimated
        :raises: ValueError: Cannot decode received data
        """

        safe_address = self.address
        data = data or b''

        def parse_revert_data(result: bytes) -> int:
            # 4 bytes - error method id
            # 32 bytes - position
            # 32 bytes - length
            # Last 32 bytes - value of revert (if everything went right)
            gas_estimation_offset = 4 + 32 + 32
            gas_estimation = result[gas_estimation_offset:]

            # Estimated gas must be 32 bytes
            if len(gas_estimation) != 32:
                logger.warning('Safe=%s Problem estimating gas, returned value is %s for tx=%s',
                               safe_address, result.hex(), tx)
                raise CannotEstimateGas('Received %s for tx=%s' % (result.hex(), tx))

            return int(gas_estimation.hex(), 16)

        # Add 10k, else we will fail in case of nested calls
        try:
            tx = self.get_contract().functions.requiredTxGas(
                to,
                value,
                data,
                operation
            ).buildTransaction({
                'from': safe_address,
                'gas': int(1e7),
                'gasPrice': 0,
            })
            # If we build the tx Web3 will not try to decode it for us
            # Ganache >= 6.3.0 and Geth are working like this
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

    def estimate_tx_gas_with_web3(self, to: str, value: int, data: bytes) -> int:
        """
        Estimate tx gas using web3
        """
        return self.ethereum_client.estimate_gas(self.address, to, value, data, block_identifier='pending')

    def estimate_tx_gas(self, to: str, value: int, data: bytes, operation: int) -> int:
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
        safe_gas_estimation = (self.estimate_tx_gas_with_safe(to, value, data, operation)
                               + proxy_gas + old_call_gas)
        # We cannot estimate DELEGATECALL (different storage)
        if SafeOperation(operation) == SafeOperation.CALL:
            try:
                web3_gas_estimation = (self.estimate_tx_gas_with_web3(to, value, data)
                                       + proxy_gas + old_call_gas)
            except ValueError:
                web3_gas_estimation = 0
            return max(safe_gas_estimation, web3_gas_estimation)

        else:
            return safe_gas_estimation

    def estimate_tx_operational_gas(self, data_bytes_length: int):
        """
        DEPRECATED. `estimate_tx_base_gas` already includes this
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
        threshold = self.retrieve_threshold()
        return 15000 + data_bytes_length // 32 * 100 + 5000 * threshold

    def get_contract(self):
        return get_safe_contract(self.w3, address=self.address)

    def retrieve_code(self) -> HexBytes:
        return self.w3.eth.getCode(self.address)

    def retrieve_master_copy_address(self, block_identifier='pending') -> str:
        return checksum_encode(self.w3.eth.getStorageAt(self.address, 0, block_identifier=block_identifier)[-20:])

    def retrieve_is_hash_approved(self, owner: str, safe_hash: bytes, block_identifier='pending') -> bool:
        return self.get_contract().functions.approvedHashes(owner,
                                                            safe_hash).call(block_identifier=block_identifier) == 1

    def retrieve_is_message_signed(self, message_hash: bytes, block_identifier='pending') -> bool:
        return self.get_contract().functions.signedMessages(message_hash).call(block_identifier=block_identifier)

    def retrieve_is_owner(self, owner: str, block_identifier='pending') -> bool:
        return self.get_contract().functions.isOwner(owner).call(block_identifier=block_identifier)

    def retrieve_nonce(self, block_identifier='pending') -> int:
        return self.get_contract().functions.nonce().call(block_identifier=block_identifier)

    def retrieve_owners(self, block_identifier='pending')-> List[str]:
        return self.get_contract().functions.getOwners().call(block_identifier=block_identifier)

    def retrieve_threshold(self, block_identifier='pending') -> int:
        return self.get_contract().functions.getThreshold().call(block_identifier=block_identifier)

    def retrieve_version(self, block_identifier='pending') -> str:
        return self.get_contract().functions.VERSION().call(block_identifier=block_identifier)

    def build_multisig_tx(self,
                          to: str,
                          value: int,
                          data: bytes,
                          operation: int = SafeOperation.CALL.value,
                          safe_tx_gas: int = 0,
                          base_gas: int = 0,
                          gas_price: int = 0,
                          gas_token: str = NULL_ADDRESS,
                          refund_receiver: str = NULL_ADDRESS,
                          signatures: bytes = b'',
                          safe_nonce: Optional[int] = None,
                          safe_version: Optional[str] = None) -> SafeTx:
        """
        Allows to execute a Safe transaction confirmed by required number of owners and then pays the account
        that submitted the transaction. The fees are always transfered, even if the user transaction fails
        :param to: Destination address of Safe transaction
        :param value: Ether value of Safe transaction
        :param data: Data payload of Safe transaction
        :param operation: Operation type of Safe transaction
        :param safe_tx_gas: Gas that should be used for the Safe transaction
        :param base_gas: Gas costs for that are independent of the transaction execution
        (e.g. base transaction fee, signature check, payment of the refund)
        :param gas_price: Gas price that should be used for the payment calculation
        :param gas_token: Token address (or `0x000..000` if ETH) that is used for the payment
        :param refund_receiver: Address of receiver of gas payment (or `0x000..000`  if tx.origin).
        :param signatures: Packed signature data ({bytes32 r}{bytes32 s}{uint8 v})
        :param safe_nonce: Nonce of the safe (to calculate hash)
        :param safe_version: Safe version (to calculate hash)
        :return:
        """

        safe_nonce = safe_nonce or self.retrieve_nonce()
        safe_version = safe_version or self.retrieve_version()
        return SafeTx(self.ethereum_client, self.address, to, value, data, operation, safe_tx_gas, base_gas, gas_price,
                      gas_token, refund_receiver, signatures=signatures, safe_nonce=safe_nonce,
                      safe_version=safe_version)

    def send_multisig_tx(self,
                         to: str,
                         value: int,
                         data: bytes,
                         operation: int,
                         safe_tx_gas: int,
                         base_gas: int,
                         gas_price: int,
                         gas_token: str,
                         refund_receiver: str,
                         signatures: bytes,
                         tx_sender_private_key: str,
                         tx_gas=None,
                         tx_gas_price=None,
                         block_identifier='pending') -> EthereumTxSent:
        """
        Build and send Safe tx
        :param tx_gas: Gas for the external tx. If not, `(safe_tx_gas + data_gas) * 2` will be used
        :param tx_gas_price: Gas price of the external tx. If not, `gas_price` will be used
        :return: Tuple(tx_hash, tx)
        :raises: InvalidMultisigTx: If user tx cannot go through the Safe
        """

        safe_tx = self.build_multisig_tx(to,
                                         value,
                                         data,
                                         operation,
                                         safe_tx_gas,
                                         base_gas,
                                         gas_price,
                                         gas_token,
                                         refund_receiver,
                                         signatures)

        tx_sender_address = Account.privateKeyToAccount(tx_sender_private_key).address
        safe_tx.call(tx_sender_address=tx_sender_address)

        tx_hash, tx = safe_tx.execute(tx_sender_private_key=tx_sender_private_key,
                                      tx_gas=tx_gas,
                                      tx_gas_price=tx_gas_price,
                                      block_identifier=block_identifier)

        return EthereumTxSent(tx_hash, tx, None)
