transaction_data_mock = {
    "method": "multiSend",
    "parameters": [
        {
            "name": "transactions",
            "type": "bytes",
            "value": "0x00c68877b75c3f9b950a798f9c9df4cde121c432ed000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000247de7edef00000000000000000000000034cfac646f301356faa8b21e94227e3583fe3f5f00c68877b75c3f9b950a798f9c9df4cde121c432ed00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000024f08a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf44",
            "decodedValue": [
                {
                    "operation": "CALL",
                    "to": "0xc68877B75c3f9b950a798f9C9dF4cDE121C432eD",
                    "value": 0,
                    "data": "0x7de7edef00000000000000000000000034cfac646f301356faa8b21e94227e3583fe3f5f",
                    "decodedData": {
                        "method": "changeMasterCopy",
                        "parameters": [
                            {
                                "name": "_masterCopy",
                                "type": "address",
                                "value": "0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F",
                            }
                        ],
                    },
                },
                {
                    "operation": "CALL",
                    "to": "0xc68877B75c3f9b950a798f9C9dF4cDE121C432eD",
                    "value": 0,
                    "data": "0xf08a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf44",
                    "decodedData": {
                        "method": "setFallbackHandler",
                        "parameters": [
                            {
                                "name": "handler",
                                "type": "address",
                                "value": "0xd5D82B6aDDc9027B22dCA772Aa68D5d74cdBdF44",
                            }
                        ],
                    },
                },
            ],
        }
    ],
}

transaction_mock = {
    "safe": "0xAedF684C1c41B51CbD228116e11484425d2FACB9",
    "to": "0xAedF684C1c41B51CbD228116e11484425d2FACB9",
    "value": "0",
    "data": "0xe318b52b0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c6b82ba149cfa113f8f48d5e3b1f78e933e16dfd0000000000000000000000003066786706ff0b6e71044e55074dbae7d01573cb",
    "operation": 0,
    "gasToken": "0x0000000000000000000000000000000000000000",
    "safeTxGas": 0,
    "baseGas": 0,
    "gasPrice": "0",
    "refundReceiver": "0x0000000000000000000000000000000000000000",
    "nonce": 5,
    "executionDate": "2024-01-24T15:22:55Z",
    "submissionDate": "2024-01-24T15:22:07.408155Z",
    "modified": "2024-01-24T15:22:55Z",
    "blockNumber": 32106343,
    "transactionHash": "0x27ac6f19a73da17d632259563aafb5092ace7e44c932ca1ed2336b2da83b30ca",
    "safeTxHash": "0x06c88df42a8ab64b2b2c5e2b5c8c4df384c267b39929a8416d1518db23f91783",
    "proposer": "0xc6b82bA149CFA113f8f48d5E3b1F78e933e16DfD",
    "executor": "0xc6b82bA149CFA113f8f48d5E3b1F78e933e16DfD",
    "isExecuted": True,
    "isSuccessful": True,
    "ethGasPrice": "3219910388",
    "maxFeePerGas": "3219910389",
    "maxPriorityFeePerGas": "3219910378",
    "gasUsed": 84977,
    "fee": "273618325041076",
    "origin": "{}",
    "dataDecoded": {
        "method": "swapOwner",
        "parameters": [
            {
                "name": "prevOwner",
                "type": "address",
                "value": "0x0000000000000000000000000000000000000001",
            },
            {
                "name": "oldOwner",
                "type": "address",
                "value": "0xc6b82bA149CFA113f8f48d5E3b1F78e933e16DfD",
            },
            {
                "name": "newOwner",
                "type": "address",
                "value": "0x3066786706Ff0B6e71044e55074dBAE7D01573cB",
            },
        ],
    },
    "confirmationsRequired": 1,
    "confirmations": [
        {
            "owner": "0xc6b82bA149CFA113f8f48d5E3b1F78e933e16DfD",
            "submissionDate": "2024-01-24T15:22:55Z",
            "transactionHash": None,
            "signature": "0x000000000000000000000000c6b82ba149cfa113f8f48d5e3b1f78e933e16dfd000000000000000000000000000000000000000000000000000000000000000001",
            "signatureType": "APPROVED_HASH",
        }
    ],
    "trusted": True,
    "signatures": "0x000000000000000000000000c6b82ba149cfa113f8f48d5e3b1f78e933e16dfd000000000000000000000000000000000000000000000000000000000000000001",
}

transaction_data_decoded_mock = {
    "method": "approve",
    "parameters": [
        {
            "name": "spender",
            "type": "address",
            "value": "0xe6fC577E87F7c977c4393300417dCC592D90acF8",
        },
        {
            "name": "value",
            "type": "uint256",
            "value": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
        },
    ],
}
