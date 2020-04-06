import json
import logging

from django.test import TestCase

from eth_account import Account
from solc import compile_standard

from ..safe import Safe
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestGanache(SafeTestCaseMixin, TestCase):
    def test_nested_ganache_bug(self):
        # Test estimation with a contract that uses a lot of gas
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
        Nester = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = Nester.constructor().transact({'from': self.w3.eth.accounts[0]})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        nester = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        safe = Safe(self.deploy_test_safe(owners=[self.ethereum_test_account.address],
                                          initial_funding_wei=self.w3.toWei(0.1, 'ether')).safe_address,
                    self.ethereum_client)
        nester_tx = nester.functions.useGas(80).buildTransaction({'gasPrice': 1, 'from': safe.address})
        nester_data = nester_tx['data']
        nester_gas = nester_tx['gas']
        tx_gas = nester_gas

        refund_receiver = Account.create().address
        safe_tx = safe.build_multisig_tx(nester.address, 0, nester_data,
                                         gas_price=1, refund_receiver=refund_receiver)
        safe_tx.sign(self.ethereum_test_account.key)

        # Trigger negative gas error on Ganache
        gas_estimated = safe_tx.w3_tx.estimateGas()
