from hexbytes import HexBytes

trace_block_2191709_mock = [
    {
        "action": {
            "from": "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
            "gas": 69000,
            "value": 1000801159649151900,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x7b5A4767158DfBbaFcDE969F2B4d7FBCC19b5d3c",
        },
        "blockHash": HexBytes(
            "0x4169fc8dfb9ece41c90044ebc9b8e2daed9f5e08c0ba3746e337732aa48b3bc3"
        ),
        "blockNumber": 2191709,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8888796bdf74b616f8900d41094bd8213b1c73385916ce4c8f5bb020f3acba3c"
        ),
        "transactionPosition": 0,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2a65Aca4D5fC5B5C859090a6c34d164135398226",
            "gas": 69000,
            "value": 511624720000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x038a877d4fB63A195c22783888DA2041911Ed818",
        },
        "blockHash": HexBytes(
            "0x4169fc8dfb9ece41c90044ebc9b8e2daed9f5e08c0ba3746e337732aa48b3bc3"
        ),
        "blockNumber": 2191709,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x878d326c7cc7fd39cf7875d2ec3a69a910409d313eab3764fe253b9fed5acd60"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7B60F3f033e6D7808428C9f2dBC81682ff24984F",
            "gas": 108562,
            "value": 286012610000000000,
            "callType": "call",
            "input": HexBytes(
                "0x0f2c9329000000000000000000000000fbb1b73c4f0bda4f67dca266ce6ef42f520fbb98000000000000000000000000e592b0d8baa2cb677034389b76a71b0d1823e0d1"
            ),
            "to": "0xE94b04a0FeD112f3664e45adb2B8915693dD5FF3",
        },
        "blockHash": HexBytes(
            "0x4169fc8dfb9ece41c90044ebc9b8e2daed9f5e08c0ba3746e337732aa48b3bc3"
        ),
        "blockNumber": 2191709,
        "result": {
            "gasUsed": 8562,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x849da57a0cbed360cb0367f95650c0f2cf5e37b394a519748779d825cffba6fe"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE94b04a0FeD112f3664e45adb2B8915693dD5FF3",
            "gas": 83248,
            "value": 0,
            "callType": "call",
            "input": HexBytes("0x16c72721"),
            "to": "0x2BD2326c993DFaeF84f696526064FF22eba5b362",
        },
        "blockHash": HexBytes(
            "0x4169fc8dfb9ece41c90044ebc9b8e2daed9f5e08c0ba3746e337732aa48b3bc3"
        ),
        "blockNumber": 2191709,
        "result": {
            "gasUsed": 197,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x849da57a0cbed360cb0367f95650c0f2cf5e37b394a519748779d825cffba6fe"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE94b04a0FeD112f3664e45adb2B8915693dD5FF3",
            "gas": 2300,
            "value": 286012610000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xFBb1b73C4f0BDa4f67dcA266ce6Ef42f520fBB98",
        },
        "blockHash": HexBytes(
            "0x4169fc8dfb9ece41c90044ebc9b8e2daed9f5e08c0ba3746e337732aa48b3bc3"
        ),
        "blockNumber": 2191709,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x849da57a0cbed360cb0367f95650c0f2cf5e37b394a519748779d825cffba6fe"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "value": 5000000000000000000,
            "author": "0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5",
            "rewardType": "block",
        },
        "blockHash": HexBytes(
            "0x4169fc8dfb9ece41c90044ebc9b8e2daed9f5e08c0ba3746e337732aa48b3bc3"
        ),
        "blockNumber": 2191709,
        "result": None,
        "subtraces": 0,
        "traceAddress": [],
        "type": "reward",
    },
]

trace_block_13191781_mock = [
    {
        "action": {
            "from": "0x061A9D627028fE708E1b77e591b9bdF41392D4Ba",
            "gas": 36942,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000010c6b61dbf44a083aec3780acf769c77be747e23000000000000000000000000000000000000000000000000000000012a05f200"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 26917,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x0ba656badfa135dec7389317fefac737f75276bbbea10e103837d87f9e853aec"
        ),
        "transactionPosition": 0,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "gas": 29233,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000010c6b61dbf44a083aec3780acf769c77be747e23000000000000000000000000000000000000000000000000000000012a05f200"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 19628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x0ba656badfa135dec7389317fefac737f75276bbbea10e103837d87f9e853aec"
        ),
        "transactionPosition": 0,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4091243E3fB5E637D06c265C6EAe1Be7fb8460Ce",
            "gas": 262809,
            "value": 96000000000000000,
            "callType": "call",
            "input": HexBytes(
                "0xab834bab0000000000000000000000007be8076f4ea4a4ad08075c2508e481d6c946d12b0000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce0000000000000000000000002c4965962223405a7b3520b4cdcf2a401620d28d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300ef850ca7754437cfce52fe0c47e5f890fb183000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007be8076f4ea4a4ad08075c2508e481d6c946d12b0000000000000000000000002c4965962223405a7b3520b4cdcf2a401620d28d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000005b3256965e7c3cf26e11fcaf296dfc8807c01073000000000000000000000000300ef850ca7754437cfce52fe0c47e5f890fb1830000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fa00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001550f7dca700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000613a09af00000000000000000000000000000000000000000000000000000000000000009b10f6948e4ee3e346be766de489e25b43d0e52025c59350fd5ad70f5a497d7900000000000000000000000000000000000000000000000000000000000000fa00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001550f7dca700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000613a08e300000000000000000000000000000000000000000000000000000000000000008efd10aa1e620120adc5284569a80f5e2a58de8f7d4acd89bbc932aeb07547c40000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006a0000000000000000000000000000000000000000000000000000000000000074000000000000000000000000000000000000000000000000000000000000007e0000000000000000000000000000000000000000000000000000000000000088000000000000000000000000000000000000000000000000000000000000009200000000000000000000000000000000000000000000000000000000000000940000000000000000000000000000000000000000000000000000000000000001b000000000000000000000000000000000000000000000000000000000000001b2b701b34eaf05a2adc84f6c281fedfe6f3170c7bf9fa6fda7f313806bf050e2160a1849a6933219e5fceefbbaf38c0e4525856005b5a869bd432e5408348a1c92b701b34eaf05a2adc84f6c281fedfe6f3170c7bf9fa6fda7f313806bf050e2160a1849a6933219e5fceefbbaf38c0e4525856005b5a869bd432e5408348a1c929b2f895343cadfb3f5101bef6484b1f01c83dc9000000000000000000000000000000000000000000000000000000000000000000000000000000000000006423b872dd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce00000000000000000000000000000000000000000000000000000000000008df00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006423b872dd0000000000000000000000002c4965962223405a7b3520b4cdcf2a401620d28d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008df00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006400000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000064000000000000000000000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "error": "Reverted",
        "result": {"gasUsed": 27856, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xbe99757628bfc3d5c7ee4e42c2629ddd13ac52354e6abb189efe5e277dce05b3"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4091243E3fB5E637D06c265C6EAe1Be7fb8460Ce",
            "gas": 276407,
            "value": 99000000000000000,
            "callType": "call",
            "input": HexBytes(
                "0xab834bab0000000000000000000000007be8076f4ea4a4ad08075c2508e481d6c946d12b0000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce0000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300ef850ca7754437cfce52fe0c47e5f890fb183000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007be8076f4ea4a4ad08075c2508e481d6c946d12b0000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf200000000000000000000000000000000000000000000000000000000000000000000000000000000000000005b3256965e7c3cf26e11fcaf296dfc8807c01073000000000000000000000000300ef850ca7754437cfce52fe0c47e5f890fb1830000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fa000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000015fb7f9b8c38000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000613a0a15000000000000000000000000000000000000000000000000000000000000000067f00b2bff164f875757b4e04c91d204178ea3a194bac0ad2664b89e9db0ec2f00000000000000000000000000000000000000000000000000000000000000fa000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000015fb7f9b8c38000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000613a088900000000000000000000000000000000000000000000000000000000000000009a6ae9e029e0337dfbb4b063a35c4884bbd52effd759ccf202f028f7c7a88dd50000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006a0000000000000000000000000000000000000000000000000000000000000074000000000000000000000000000000000000000000000000000000000000007e0000000000000000000000000000000000000000000000000000000000000088000000000000000000000000000000000000000000000000000000000000009200000000000000000000000000000000000000000000000000000000000000940000000000000000000000000000000000000000000000000000000000000001b000000000000000000000000000000000000000000000000000000000000001b6ea4d9de0a1eda9a6107324f9560b731cbb2a27c2b2fd3d736836f7b00ab88b52b1f5898f794406b993e625218e8d442c58a41ffecca83ef439b7c3d0707b5dc6ea4d9de0a1eda9a6107324f9560b731cbb2a27c2b2fd3d736836f7b00ab88b52b1f5898f794406b993e625218e8d442c58a41ffecca83ef439b7c3d0707b5dc29b2f895343cadfb3f5101bef6484b1f01c83dc9000000000000000000000000000000000000000000000000000000000000000000000000000000000000006423b872dd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce0000000000000000000000000000000000000000000000000000000000000b6200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006423b872dd0000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b6200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006400000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000064000000000000000000000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 201933, "output": HexBytes("0x")},
        "subtraces": 6,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
            "gas": 227471,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xc45527910000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf2"
            ),
            "to": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2782,
            "output": HexBytes(
                "0x000000000000000000000000892c0feffe706b811a8437ab9e2293fa5f7b907a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
            "gas": 223931,
            "value": 0,
            "callType": "call",
            "input": HexBytes("0x97204d8e"),
            "to": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2613,
            "output": HexBytes(
                "0x000000000000000000000000f9e266af4bca5890e2781812cc6a6e89495a79f2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
            "gas": 218434,
            "value": 0,
            "callType": "call",
            "input": HexBytes("0x5c60da1b"),
            "to": "0x892C0FEfFE706b811a8437aB9e2293FA5F7b907A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2525,
            "output": HexBytes(
                "0x000000000000000000000000f9e266af4bca5890e2781812cc6a6e89495a79f2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
            "gas": 2300,
            "value": 2475000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x5b3256965e7C3cF26E11FCAf296DfC8807C01073",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
            "gas": 2300,
            "value": 96525000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x8bdBF4B19cb840e9Ac9B1eFFc2BfAd47591B5bF2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",
            "gas": 173586,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x1b0f7ba9000000000000000000000000300ef850ca7754437cfce52fe0c47e5f890fb18300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000006423b872dd0000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf20000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce0000000000000000000000000000000000000000000000000000000000000b6200000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x892C0FEfFE706b811a8437aB9e2293FA5F7b907A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 98215,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [5],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x892C0FEfFE706b811a8437aB9e2293FA5F7b907A",
            "gas": 167709,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x1b0f7ba9000000000000000000000000300ef850ca7754437cfce52fe0c47e5f890fb18300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000006423b872dd0000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf20000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce0000000000000000000000000000000000000000000000000000000000000b6200000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xF9e266af4BcA5890e2781812cc6a6E89495a79f2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 94955,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 2,
        "traceAddress": [5, 0],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x892C0FEfFE706b811a8437aB9e2293FA5F7b907A",
            "gas": 159793,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x69dc9ff30000000000000000000000007be8076f4ea4a4ad08075c2508e481d6c946d12b"
            ),
            "to": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2553,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [5, 0, 0],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0x892C0FEfFE706b811a8437aB9e2293FA5F7b907A",
            "gas": 156423,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd0000000000000000000000008bdbf4b19cb840e9ac9b1effc2bfad47591b5bf20000000000000000000000004091243e3fb5e637d06c265c6eae1be7fb8460ce0000000000000000000000000000000000000000000000000000000000000b6200000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x300Ef850CA7754437cFcE52Fe0C47e5f890FB183",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 86058, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [5, 0, 1],
        "transactionHash": HexBytes(
            "0x7798b6ef9f281c87d45bdeabda70e4b9f24085c15aaac8e75a9f4480fb2feeef"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF598b81Ef8c7b52a7F2a89253436e72ec6DC871f",
            "gas": 84000,
            "value": 140949999999999984,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xb0BE4D6159d6480980bCCe0f8b4F0d487e8450BD",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xe0cf30aaa01f5cd786db4b14daf61aac44143778926d5e33ce416a2709d3713b"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xf60c2Ea62EDBfE808163751DD0d8693DCb30019c",
            "gas": 186128,
            "value": 109720000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xe74B4E405768BcC2B6deda7710f659ba7924A245",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xf092fb03ceca9ff7e01e5b6483bfac47a7db6d8bf0a32ac44b45f8a8f0b0b665"
        ),
        "transactionPosition": 4,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9E5D17e8E34d2568200C154895ba63523b3560C8",
            "gas": 129000,
            "value": 0,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x9E5D17e8E34d2568200C154895ba63523b3560C8",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x565d69c19ae671197d53591caff0d945b72f4ac0a1a6d917bda7e2179906055d"
        ),
        "transactionPosition": 5,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE851D0A60f038a8B2FF25649cFF4Aa4209c993CE",
            "gas": 40631,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f5c48fb2f53b8c2d43a4d4a8eca7abfed364e1e90000000000000000000000000000000000000000000000f0fd3f0144b363e800"
            ),
            "to": "0xE41d2489571d322189246DaFA5ebDe1F4699F498",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 30250,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x13a3a8911e7314c8c38bdb634abab5c503aca77bab0755c36fb3d1a8e61e7820"
        ),
        "transactionPosition": 6,
        "type": "call",
    },
    {
        "action": {
            "from": "0xd5351b44102aaBB21022440e29B4295B56016ddF",
            "gas": 0,
            "value": 135417422759250043,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xa6eeFBd51A818DCBc77d6e8eF6Bd59ab61c403dF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc3f27af4f5b8a3063b6dbd0a08019100867afb00f47227cc6e03a9c647777483"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5041ed759Dd4aFc3a72b8192C143F72f4724081A",
            "gas": 398392,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000296897c5b419c2217719dc699d244e595d675d0700000000000000000000000000000000000000000000000000000000971a1930"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 26917,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7011ea340523e70f4a18f178c20367816cab4e45aa7d31e705bdb5b51265548f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "gas": 385036,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000296897c5b419c2217719dc699d244e595d675d0700000000000000000000000000000000000000000000000000000000971a1930"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 19628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x7011ea340523e70f4a18f178c20367816cab4e45aa7d31e705bdb5b51265548f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9AA65464b4cFbe3Dc2BDB3dF412AeE2B3De86687",
            "gas": 228392,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000086ff7ab903e3c557aee37b383c0ceabf9ee5690700000000000000000000000000000000000000000000000000000000e880f062"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x58d69c294aaa1503e06c4a69c895cd4fbc47e03f0a341a26c7255609d6b58c79"
        ),
        "transactionPosition": 9,
        "type": "call",
    },
    {
        "action": {
            "from": "0x3B794929566e3Ba0f25e4263e1987828b5c87161",
            "gas": 29000,
            "value": 13239660934222264,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xcAE2c1225481162eFF4c0807c7607724E5c29c9D",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7b5e1ecaffd9bab57d8b59bf476d031bb2517192139b84362db866b88d40a295"
        ),
        "transactionPosition": 10,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1f8F16a29251fA399D89e1005E3f95427Bf5B1dE",
            "gas": 0,
            "value": 4676123280340692,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x043aD94aeC8f88a62B6b0f130ccC61aC39f77A3c",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2542cee5c144aada422aa08df4b458c594baae89061d0ae41d8b9678c527f51d"
        ),
        "transactionPosition": 11,
        "type": "call",
    },
    {
        "action": {
            "from": "0x307082e6926E4c004F3c821cb1Af08b8A2D80242",
            "gas": 53404,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000007726f93410e15e64113e3303deb73721f36a01ef00000000000000000000000000000000000000000000000000000000b2d05e00"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6e90803bf18163a7797d9b35fd5403c485784bf8c9480b2e1fc9b5d81194d8d2"
        ),
        "transactionPosition": 12,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC55EdDadEeB47fcDE0B3B6f25BD47D745BA7E7fa",
            "gas": 0,
            "value": 118400000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x1645521a6df217605d9949AafB84927018868cDf",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x973702b743a2e3b8caae347f74f2729b5a9cd20a5c8472b94c6758daac4407ee"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc9f5296Eb3ac266c94568D790b6e91ebA7D76a11",
            "gas": 228404,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000009f71bcf338be16007ea0502e60aa5b527677a0fc0000000000000000000000000000000000000000000000000000000002faf080"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xd80a9b37571313117f0d34fe3152f1ad4fee03f1a6c629ff7d2bf966a37ed14f"
        ),
        "transactionPosition": 14,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc9f5296Eb3ac266c94568D790b6e91ebA7D76a11",
            "gas": 228356,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000274de18b0e2c24864cfdbd0db156de962b48045e000000000000000000000000000000000000000000000035fe46d2f741100000"
            ),
            "to": "0xa117000000f279D81A1D3cc75430fAA017FA5A2e",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 29842,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x5cf28c6818d072ea14ac6f5923431202a3af58e73c833d525d75af61078ef37d"
        ),
        "transactionPosition": 15,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc9f5296Eb3ac266c94568D790b6e91ebA7D76a11",
            "gas": 40,
            "value": 7088000000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x5EE7BC4c49c653778597900143702691E8AFCE48",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xe8385591d43060730b568d5762656d72c4597f3c63c17e03143abb4cd2ce2549"
        ),
        "transactionPosition": 16,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc9f5296Eb3ac266c94568D790b6e91ebA7D76a11",
            "gas": 228024,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd00000000000000000000000053ab688f20fdc725325b06c788226794acc47628000000000000000000000000c9f5296eb3ac266c94568d790b6e91eba7d76a11000000000000000000000000000000000000000000000000000000746a528800"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 26530, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x072f7a1f91c6281907b0b0a001bb2a58cb0e199bcf72f439b816ee7e83d1a978"
        ),
        "transactionPosition": 17,
        "type": "call",
    },
    {
        "action": {
            "from": "0x18db8B99c1d6E439fa44Fd87Bfb1109e345e98Da",
            "gas": 193674,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x38ed17390000000000000000000000000000000000000000033b2e3c9fd0803ce80000000000000000000000000000000000000000000000000000000000000281c5b6a100000000000000000000000000000000000000000000000000000000000000a000000000000000000000000018db8b99c1d6e439fa44fd87bfb1109e345e98da00000000000000000000000000000000000000000000000000000000613a117b000000000000000000000000000000000000000000000000000000000000000300000000000000000000000085f17cf997934a597031b2e18a9ab6ebd4b9f6a4000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7"
            ),
            "to": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "error": "Reverted",
        "result": {
            "gasUsed": 16268,
            "output": HexBytes(
                "0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002b556e69737761705632526f757465723a20494e53554646494349454e545f4f55545055545f414d4f554e54000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xfac7403428a8213f3fc296412eb3f259086d80dd83be2d819b574b145b8d4855"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
            "gas": 185741,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes("0x0902f1ac"),
            "to": "0x6469B34a2a4723163C4902dbBdEa728D20693C12",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2517,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000002c158b1afbb13485d76c9cfe00000000000000000000000000000000000000000000000238fbe7ba3db69d46700000000000000000000000000000000000000000000000000000000613a0ab4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xfac7403428a8213f3fc296412eb3f259086d80dd83be2d819b574b145b8d4855"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
            "gas": 178382,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes("0x0902f1ac"),
            "to": "0x06da0fd433C1A5d7a4faa01111c044910A184553",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2517,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000005d91462602980322d2f000000000000000000000000000000000000000000000000000058ee2871cbb700000000000000000000000000000000000000000000000000000000613a0a97"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xfac7403428a8213f3fc296412eb3f259086d80dd83be2d819b574b145b8d4855"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC098B2a3Aa256D2140208C3de6543aAEf5cd3A94",
            "gas": 42000,
            "value": 903856630000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xAcF288a55C9e807e6B5d7DD4cB4f314eBe1E14FA",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6b460cc1afa1311f9d698fb3b45a68ad537a30630b20db06a394e1d7de3c5a02"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xEE022C4a3A8855356E78a3960A34842dC868B754",
            "gas": 48380,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000008abdfb25f4d46e59c4a85e3da026679999f00291000000000000000000000000000000000000000000000000000000069275d6c0"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x9665b3325bd3a57d61c7d185f1eb428b61ef244561fa15fbb0237a4e67f593ea"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0x6871EaCd33fbcfE585009Ab64F0795d7152dc5a0",
            "gas": 34024,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd00000000000000000000000041335ee132cdde75acac48f1489161128440444c0000000000000000000000006871eacd33fbcfe585009ab64f0795d7152dc5a00000000000000000000000000000000000000000000000000000000a0b9329c9"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 26530, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x3204a5a8a2c34a8f8224375968a440858aee459ca50278e33073939d9d2f0a79"
        ),
        "transactionPosition": 21,
        "type": "call",
    },
    {
        "action": {
            "from": "0x84ee5a99a08D98e2966B1a889fDCaB1CF3F7C589",
            "gas": 0,
            "value": 17790313368673531,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x1AB18ac546Cf48509D4cd41d48B41cc859A269A5",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x62dacd69eab666668088561b6d87e3f703973992b0f00666e09585af3264ea4d"
        ),
        "transactionPosition": 22,
        "type": "call",
    },
    {
        "action": {
            "from": "0xfa35113163bFD33c18A01d1A62d4D14a1Ed30a42",
            "gas": 126069,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x2e95b6c80000000000000000000000006286a9e6f7e745a6d884561d88f94542d6715698000000000000000000000000000000000000000000000b5a0ebbfe5a15da000000000000000000000000000000000000000000000000000015b1e91b911a8aeb0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000140000000000000003b6d034084d1f4bbd0fb53b9a09e95e051f2fe1bf3e01e6a"
            ),
            "to": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "error": "Reverted",
        "result": {
            "gasUsed": 93884,
            "output": HexBytes(
                "0x08c379a0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000164d696e2072657475726e206e6f742072656163686564"
            ),
        },
        "subtraces": 5,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 120771,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd000000000000000000000000fa35113163bfd33c18a01d1a62d4d14a1ed30a4200000000000000000000000084d1f4bbd0fb53b9a09e95e051f2fe1bf3e01e6a000000000000000000000000000000000000000000000b5a0ebbfe5a15da0000"
            ),
            "to": "0x6286A9e6f7e745A6D884561D88F94542d6715698",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 20711,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 97641,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes("0x0902f1ac"),
            "to": "0x84d1f4BBD0FB53b9a09e95E051f2fe1bF3e01e6A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000003cac63f6efb193364d5d200000000000000000000000000000000000000000000000755b352de71f2c1a600000000000000000000000000000000000000000000000000000000613a0acf"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 94841,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000015a3896d5772879700000000000000000000000011111112542d85b3ef69ae05771c2dccff4faa2600000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x84d1f4BBD0FB53b9a09e95E051f2fe1bF3e01e6A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 47804, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x84d1f4BBD0FB53b9a09e95E051f2fe1bF3e01e6A",
            "gas": 80163,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000011111112542d85b3ef69ae05771c2dccff4faa2600000000000000000000000000000000000000000000000015a3896d57728797"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 12862,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 0],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x84d1f4BBD0FB53b9a09e95E051f2fe1bF3e01e6A",
            "gas": 66901,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a0823100000000000000000000000084d1f4bbd0fb53b9a09e95e051f2fe1bf3e01e6a"
            ),
            "to": "0x6286A9e6f7e745A6D884561D88F94542d6715698",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 585,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000003d6204e2af973493ed5d2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 1],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x84d1f4BBD0FB53b9a09e95E051f2fe1bF3e01e6A",
            "gas": 65919,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a0823100000000000000000000000084d1f4bbd0fb53b9a09e95e051f2fe1bf3e01e6a"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000007400fc9711a803a0f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 2],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 47597,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x2e1a7d4d00000000000000000000000000000000000000000000000015a3896d57728797"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 9219, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "gas": 2300,
            "value": 1559240998711887767,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 79, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 31832,
            "value": 1559240998711887767,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xfa35113163bFD33c18A01d1A62d4D14a1Ed30a42",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0xd1118a18e43777636ccef0cafa5de58c3b0c6800454606342ba46a662828a8c6"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xACc300998060e519d10977e25f8ef2455f5330f7",
            "gas": 28478,
            "value": 10000000000000000,
            "callType": "call",
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 23974, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1ea951dcaf2bda8a8fb8251b2592561f35af0c879d78f34cd4ef9110f1b1b4c7"
        ),
        "transactionPosition": 24,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc4F9F5F9910a59A58dB92a5ceEd80Ce1725C8855",
            "gas": 80836,
            "value": 80000000000000000,
            "callType": "call",
            "input": HexBytes(
                "0xba93c39c000000000000000000000000fc7b1dad07111c77c5d619043d75ac9a19680760000000000000000000000000c4f9f5f9910a59a58db92a5ceed80ce1725c88550000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000011c37937e080000000000000000000000000000000000000000000000000000011c37937e0800000000000000000000000000000000000000000000000000000000000010ea46140000000000000000000000000000000000000000000000000000000000c94a6e000000000000000000000000000000000000000000000000000000000000003f00000000000000000000000000000000000000000000000000000000000000000024cf29ee0de9b595a6dbddea0e2896d74de8ecbff141582259bb6b1513730200000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000000000000000000000000000041f8a8837c1fa4ec249ce079090fede86bfbf2273d2523186e0621e44af760eaf13d0c18a82851be01f690eee7cb71e8e2c470cf6552a5063deec2dc96ab6c193d1b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xa18607cA4A3804CC3Cd5730eafeFcC47a7641643",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 78872, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x28790ea8588f1c24cbc3dacb95bad48556df979755563626652a9b3aa55799bf"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa18607cA4A3804CC3Cd5730eafeFcC47a7641643",
            "gas": 68089,
            "value": 80000000000000000,
            "callType": "call",
            "input": HexBytes(
                "0xecc0661a000000000000000000000000c4f9f5f9910a59a58db92a5ceed80ce1725c88550000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000011c37937e080000000000000000000000000000000000000000000000000000011c37937e0800000000000000000000000000000000000000000000000000000000000010ea4614000000000000000000000000000000000000000000000000000000000000003f00000000000000000000000000000000000000000000000000000000000000000024cf29ee0de9b595a6dbddea0e2896d74de8ecbff141582259bb6b1513730200000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041f8a8837c1fa4ec249ce079090fede86bfbf2273d2523186e0621e44af760eaf13d0c18a82851be01f690eee7cb71e8e2c470cf6552a5063deec2dc96ab6c193d1b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xfc7b1daD07111c77c5d619043D75aC9A19680760",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 67101, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x28790ea8588f1c24cbc3dacb95bad48556df979755563626652a9b3aa55799bf"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xfc7b1daD07111c77c5d619043D75aC9A19680760",
            "gas": 64354,
            "value": 80000000000000000,
            "callType": "delegatecall",
            "input": HexBytes(
                "0xecc0661a000000000000000000000000c4f9f5f9910a59a58db92a5ceed80ce1725c88550000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000011c37937e080000000000000000000000000000000000000000000000000000011c37937e0800000000000000000000000000000000000000000000000000000000000010ea4614000000000000000000000000000000000000000000000000000000000000003f00000000000000000000000000000000000000000000000000000000000000000024cf29ee0de9b595a6dbddea0e2896d74de8ecbff141582259bb6b1513730200000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041f8a8837c1fa4ec249ce079090fede86bfbf2273d2523186e0621e44af760eaf13d0c18a82851be01f690eee7cb71e8e2c470cf6552a5063deec2dc96ab6c193d1b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x20EF25713c37855fbB8ED483eFDDFF9407442650",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 64354, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x28790ea8588f1c24cbc3dacb95bad48556df979755563626652a9b3aa55799bf"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xfc7b1daD07111c77c5d619043D75aC9A19680760",
            "gas": 46228,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c4f9f5f9910a59a58db92a5ceed80ce1725c88550000000000000000000000000000000000000000000000000000000010ea4614"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 44017,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0x28790ea8588f1c24cbc3dacb95bad48556df979755563626652a9b3aa55799bf"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "gas": 38374,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c4f9f5f9910a59a58db92a5ceed80ce1725c88550000000000000000000000000000000000000000000000000000000010ea4614"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 36728,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0, 0],
        "transactionHash": HexBytes(
            "0x28790ea8588f1c24cbc3dacb95bad48556df979755563626652a9b3aa55799bf"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0211677061fB97872dD015d23fe44F3A0066Ccc3",
            "gas": 25197,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa22cb465000000000000000000000000e987cbec33f573b020e7c5672f8008d847ab8b420000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x9640C1a69eadD073D273D75028a1D233CD63016C",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 25197, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xaaae290a863c7a364941fa047c5c18d0ea0e30f1cb3401537e274576a227b1b0"
        ),
        "transactionPosition": 26,
        "type": "call",
    },
    {
        "action": {
            "from": "0xAe45a8240147E6179ec7c9f92c5A18F9a97B3fCA",
            "gas": 0,
            "value": 5975748000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x61296A581598F58fA5841B44904D376eDA01127A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc1338a392bbb9271c0de47705148127ed3685159918424a2431e085d67b0ef26"
        ),
        "transactionPosition": 27,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E9bABdb4743DbaAf287352BC9D3d8c31B0ff327",
            "gas": 162307,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x875b4f6300000000000000000000000000000000000000000000000000000000000000600000000000000000000000002f8a0eecb02a2aa17e3db6de777ea0d941984cfa0000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000000500000000000000000000000000000000000000000000000000000000000000fa00000000000000000000000000000000000000000000000000000000000002b0000000000000000000000000000000000000000000000000000000000000019d000000000000000000000000000000000000000000000000000000000000055a00000000000000000000000000000000000000000000000000000000000001bd00000000000000000000000000000000000000000000000000000000000000414fbe56bde7330228ad9399e9513544bcee5376331067d3ef651d2b41fb14df10039175fd80a5131928082c52e1f9fd497c3dc7b7d09334d6e5663b09728579721b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x00D07C53E70338c376cF6ab2A5218d8643115084",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 160190, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x662483ec1961250e0f24c9adffcf8d96d43418f573448867ecbdf65a31dd331c"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7F9Bb16Bb280D93e6e465420fD02d28b3A8fbc5f",
            "gas": 211566,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x5f5755290000000000000000000000000000000000000000000000000000000000000080000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a00000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000136f6e65496e6368563346656544796e616d6963000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004476f38446e3da000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000009f7fe35818eae00000000000000000000000011ededebf63bef0ea2d2d071bdf88f71543ec6fb000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000c42e95b6c8000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a00000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004511aa72b8812440000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000140000000000000003b6d0340643b47d668f7bd78e0eeaa574b0d185c46ef079c00000000000000000000000000000000000000000000000000000000ab"
            ),
            "to": "0x881D40237659C251811CEC9c364ef91dC08D300C",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 179647, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x881D40237659C251811CEC9c364ef91dC08D300C",
            "gas": 196872,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd0000000000000000000000007f9bb16bb280d93e6e465420fd02d28b3a8fbc5f00000000000000000000000074de5d4fcbf63e00296fd95d33236b979401663100000000000000000000000000000000000000000000004e184ccf4dc2aa7a88"
            ),
            "to": "0x217ddEad61a42369A266F1Fb754EB5d3EBadc88a",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 38792,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x881D40237659C251811CEC9c364ef91dC08D300C",
            "gas": 149180,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xe35473350000000000000000000000004fed27eac9c2477b8c14ee8bada444bd4654f8330000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000022492f5f0370000000000000000000000007f9bb16bb280d93e6e465420fd02d28b3a8fbc5f000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004476f38446e3da000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000009f7fe35818eae00000000000000000000000011ededebf63bef0ea2d2d071bdf88f71543ec6fb000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000c42e95b6c8000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a00000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004511aa72b8812440000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000140000000000000003b6d0340643b47d668f7bd78e0eeaa574b0d185c46ef079c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 117818, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
            "gas": 141939,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x92f5f0370000000000000000000000007f9bb16bb280d93e6e465420fd02d28b3a8fbc5f000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004476f38446e3da000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000009f7fe35818eae00000000000000000000000011ededebf63bef0ea2d2d071bdf88f71543ec6fb000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000c42e95b6c8000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a00000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004511aa72b8812440000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000140000000000000003b6d0340643b47d668f7bd78e0eeaa574b0d185c46ef079c00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x4fEd27Eac9C2477B8c14Ee8baDA444BD4654F833",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 112694, "output": HexBytes("0x")},
        "subtraces": 5,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
            "gas": 138838,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0xdd62ed3e00000000000000000000000074de5d4fcbf63e00296fd95d33236b979401663100000000000000000000000011111112542d85b3ef69ae05771c2dccff4faa26"
            ),
            "to": "0x217ddEad61a42369A266F1Fb754EB5d3EBadc88a",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 3241,
            "output": HexBytes(
                "0xffffffffffffffffffffffffffffffffffffffffffff650eadd360798758cea6"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 0],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
            "gas": 131716,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x2e95b6c8000000000000000000000000217ddead61a42369a266f1fb754eb5d3ebadc88a00000000000000000000000000000000000000000000004e184ccf4dc2aa7a8800000000000000000000000000000000000000000000000004511aa72b8812440000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000140000000000000003b6d0340643b47d668f7bd78e0eeaa574b0d185c46ef079c"
            ),
            "to": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 85953,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000004734857e2fb2007"
            ),
        },
        "subtraces": 5,
        "traceAddress": [1, 0, 1],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 128791,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd00000000000000000000000074de5d4fcbf63e00296fd95d33236b9794016631000000000000000000000000643b47d668f7bd78e0eeaa574b0d185c46ef079c00000000000000000000000000000000000000000000004e184ccf4dc2aa7a88"
            ),
            "to": "0x217ddEad61a42369A266F1Fb754EB5d3EBadc88a",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 14892,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 0],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 111388,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes("0x0902f1ac"),
            "to": "0x643b47D668f7BD78E0EeaA574b0d185c46Ef079C",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000003f3c270741545064e830000000000000000000000000000000000000000000000003e47aebd48870924000000000000000000000000000000000000000000000000000000006139fc25"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 1],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 108589,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004734857e2fb200700000000000000000000000011111112542d85b3ef69ae05771c2dccff4faa2600000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x643b47D668f7BD78E0EeaA574b0d185c46Ef079C",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 48105, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1, 0, 1, 2],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x643b47D668f7BD78E0EeaA574b0d185c46Ef079C",
            "gas": 93696,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000011111112542d85b3ef69ae05771c2dccff4faa2600000000000000000000000000000000000000000000000004734857e2fb2007"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 12862,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 2, 0],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x643b47D668f7BD78E0EeaA574b0d185c46Ef079C",
            "gas": 80434,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a08231000000000000000000000000643b47d668f7bd78e0eeaa574b0d185c46ef079c"
            ),
            "to": "0x217ddEad61a42369A266F1Fb754EB5d3EBadc88a",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 886,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000441dabd436307b0c90b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 2, 1],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x643b47D668f7BD78E0EeaA574b0d185c46Ef079C",
            "gas": 79156,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a08231000000000000000000000000643b47d668f7bd78e0eeaa574b0d185c46ef079c"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000039d46665658be91d"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 2, 2],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 61048,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x2e1a7d4d00000000000000000000000000000000000000000000000004734857e2fb2007"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 9219, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 0, 1, 3],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "gas": 2300,
            "value": 320679540780900359,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 79, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 3, 0],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
            "gas": 45283,
            "value": 320679540780900359,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 40, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 1, 4],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
            "gas": 37538,
            "value": 2805945981832878,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x11eDedebF63bef0ea2d2D071bdF88F71543ec6fB",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 2],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
            "gas": 37015,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a0823100000000000000000000000074de5d4fcbf63e00296fd95d33236b9794016631"
            ),
            "to": "0x217ddEad61a42369A266F1Fb754EB5d3EBadc88a",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 886,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 3],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74de5d4FCbf63E00296fd95d33236B9794016631",
            "gas": 28967,
            "value": 317873594799067481,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x7F9Bb16Bb280D93e6e465420fD02d28b3A8fbc5f",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 4],
        "transactionHash": HexBytes(
            "0x7cd9fdf8ba8f3378d428e1cbb353a28142b28946840353df07b1140b5849b850"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0xb5d85CBf7cB3EE0D56b3bB207D5Fc4B82f43F511",
            "gas": 0,
            "value": 67660500000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x59b6E0185a290aC466A6c4B60093e33afeC7169b",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xfc4763a159754d4839c1ca85382ba5f66be2cbfc33df28005e33c4928b541f97"
        ),
        "transactionPosition": 30,
        "type": "call",
    },
    {
        "action": {
            "from": "0x3cD751E6b0078Be393132286c442345e5DC49699",
            "gas": 0,
            "value": 70391500000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x1521A41240C40Cf441cc68dD7E0EED06e3dC72fF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x709198fe8195723ab00c2edf265ded5267dff4a7dcda49098a4783b4473b115e"
        ),
        "transactionPosition": 31,
        "type": "call",
    },
    {
        "action": {
            "from": "0xddfAbCdc4D8FfC6d5beaf154f18B778f892A0740",
            "gas": 0,
            "value": 119404330000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xA837149C978776B322fC7A6245a46AE89a4c5385",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xaa0a0d4f8bf778e909c48dcd13397140bfb791d86acf35a14f5271e44cfeac8f"
        ),
        "transactionPosition": 32,
        "type": "call",
    },
    {
        "action": {
            "from": "0x71660c4005BA85c37ccec55d0C4493E66Fe775d3",
            "gas": 228404,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f068633504bf13523ed3c976c33bd842502b377b0000000000000000000000000000000000000000000000000000000037131f00"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 44017,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xb3d846d3937d048de62e482bc19d5fc8447a74fdd3b709b64b52b33da0ffcdab"
        ),
        "transactionPosition": 33,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "gas": 217704,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f068633504bf13523ed3c976c33bd842502b377b0000000000000000000000000000000000000000000000000000000037131f00"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 36728,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xb3d846d3937d048de62e482bc19d5fc8447a74fdd3b709b64b52b33da0ffcdab"
        ),
        "transactionPosition": 33,
        "type": "call",
    },
    {
        "action": {
            "from": "0x538CD83410D14d615590fb370E008F839CEA6024",
            "gas": 0,
            "value": 45600000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xCF5A1c6E4e157d63883f3aE9E62cAD2729838580",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1ef77ab2e12ad5808999b5ee99ee93aa24a559849c7e2a9096ffbe7d56353b9b"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0C86284199fB87A0b391b02883b6613816393bFE",
            "gas": 50968,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x095ea7b30000000000000000000000007a250d5630b4cf539739df2c5dacb4c659f2488dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 38367,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc7c7d796f48e336a5d895e064116ef21f1ba73826ab7b4cba208df47c03ce4ac"
        ),
        "transactionPosition": 35,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "gas": 43040,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x095ea7b30000000000000000000000007a250d5630b4cf539739df2c5dacb4c659f2488dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 31078,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xc7c7d796f48e336a5d895e064116ef21f1ba73826ab7b4cba208df47c03ce4ac"
        ),
        "transactionPosition": 35,
        "type": "call",
    },
    {
        "action": {
            "from": "0x02736d5c8dcea65539993d143A3DE90ceBcA9c3c",
            "gas": 160566,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xac9650d800000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000000000000000000000000000104414bf389000000000000000000000000ba7970f10d9f0531941dced1dda7ef3016b24e5b000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000002710000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000613a11bc0000000000000000000000000000000000000000000000375c21cee45ab3852000000000000000000000000000000000000000000000000000eab1df8814dbac000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004449404b7c00000000000000000000000000000000000000000000000000eab1df8814dbac00000000000000000000000002736d5c8dcea65539993d143a3de90cebca9c3c00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 128244,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000f66df78215e6a80000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 156855,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x414bf389000000000000000000000000ba7970f10d9f0531941dced1dda7ef3016b24e5b000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000002710000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000613a11bc0000000000000000000000000000000000000000000000375c21cee45ab3852000000000000000000000000000000000000000000000000000eab1df8814dbac0000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 107077,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000f66df78215e6a8"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 147471,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x128acb08000000000000000000000000e592427a0aece92de3edee1f18e0157c0586156400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000375c21cee45ab3852000000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000002736d5c8dcea65539993d143a3de90cebca9c3c000000000000000000000000000000000000000000000000000000000000002bba7970f10d9f0531941dced1dda7ef3016b24e5b002710c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000"
            ),
            "to": "0xC00C5977395664267c118d71569DCCF4BC37bF5F",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 99638,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000375c21cee45ab38520ffffffffffffffffffffffffffffffffffffffffffffffffff0992087dea1958"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC00C5977395664267c118d71569DCCF4BC37bF5F",
            "gas": 110017,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000e592427a0aece92de3edee1f18e0157c0586156400000000000000000000000000000000000000000000000000f66df78215e6a8"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 29962,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC00C5977395664267c118d71569DCCF4BC37bF5F",
            "gas": 77191,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a08231000000000000000000000000c00c5977395664267c118d71569dccf4bc37bf5f"
            ),
            "to": "0xbA7970f10D9f0531941DcEd1dda7ef3016B24e5b",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 2577,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000037a542567ad1af50e9ee7"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 1],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC00C5977395664267c118d71569DCCF4BC37bF5F",
            "gas": 73864,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xfa461e330000000000000000000000000000000000000000000000375c21cee45ab38520ffffffffffffffffffffffffffffffffffffffffffffffffff0992087dea1958000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000002736d5c8dcea65539993d143a3de90cebca9c3c000000000000000000000000000000000000000000000000000000000000002bba7970f10d9f0531941dced1dda7ef3016b24e5b002710c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000"
            ),
            "to": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 22278, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0, 2],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 69034,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd00000000000000000000000002736d5c8dcea65539993d143a3de90cebca9c3c000000000000000000000000c00c5977395664267c118d71569dccf4bc37bf5f0000000000000000000000000000000000000000000000375c21cee45ab38520"
            ),
            "to": "0xbA7970f10D9f0531941DcEd1dda7ef3016B24e5b",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 18222,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 0],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC00C5977395664267c118d71569DCCF4BC37bF5F",
            "gas": 51301,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a08231000000000000000000000000c00c5977395664267c118d71569dccf4bc37bf5f"
            ),
            "to": "0xbA7970f10D9f0531941DcEd1dda7ef3016B24e5b",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 577,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000037a8b81897bff4fc22407"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 3],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 50754,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x49404b7c00000000000000000000000000000000000000000000000000eab1df8814dbac00000000000000000000000002736d5c8dcea65539993d143a3de90cebca9c3c"
            ),
            "to": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 18173, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 49257,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x70a08231000000000000000000000000e592427a0aece92de3edee1f18e0157c05861564"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000f66df78215e6a8"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 48288,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x2e1a7d4d00000000000000000000000000000000000000000000000000f66df78215e6a8"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 9223, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "gas": 2300,
            "value": 69363754077644456,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 83, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 1, 0],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "gas": 32209,
            "value": 69363754077644456,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x02736d5c8dcea65539993d143A3DE90ceBcA9c3c",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x2407e6b8a5be763a5f8c280f1ae10ff000ebaf75e1530a0f3651987ba311b2ba"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0x73800459807528072A3B2eD217c1De72F28514f3",
            "gas": 734311,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xcb133b0f0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000d8800000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000005000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0xC0981Df196dc6c6fb8673B912B07956256D7e9fF",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 734311, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xf5e2ebf727d16274508ca3bd5f26929327e3a1fec8b6aafae19d42972547c153"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC0981Df196dc6c6fb8673B912B07956256D7e9fF",
            "gas": 716086,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd00000000000000000000000073800459807528072a3b2ed217c1de72f28514f3000000000000000000000000c0981df196dc6c6fb8673b912b07956256d7e9ff0000000000000000000000000000000000000000000000000000000000000d88"
            ),
            "to": "0xdEcC60000ba66700a009b8F9F7D82676B5cfA88A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 76963, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xf5e2ebf727d16274508ca3bd5f26929327e3a1fec8b6aafae19d42972547c153"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC0981Df196dc6c6fb8673B912B07956256D7e9fF",
            "gas": 453672,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes("0x95d89b41"),
            "to": "0xa6233451039230fAe712371dD7526f6Df7625E1f",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 3294,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000449524f4e00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xf5e2ebf727d16274508ca3bd5f26929327e3a1fec8b6aafae19d42972547c153"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC0981Df196dc6c6fb8673B912B07956256D7e9fF",
            "gas": 444267,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0x0f14d01a00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000034000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000d8800000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000002200000000000000000000000000000000000000000000000000000000000000260000000000000000000000000000000000000000000000000000000000000000743617069746f6c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000641737472616c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000084d6564696576616c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000055761746572000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000757617272696e6700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c4469637461746f72736869700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000856616c68616c6c61000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000449524f4e00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x787D1B8bFe2142af127e62dcc15D63D6D708f85F",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 191993,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000006cd646174613a6170706c69636174696f6e2f6a736f6e3b6261736536342c65794a755957316c496a6f67496c4e6c644852735a57316c626e5167497a4d304e6a51694c4341695a47567a59334a7063485270623234694f694169553256306447786c6257567564484d6759584a6c49474567644856796269426959584e6c5a43426a61585a7062476c7a595852706232346763326c74645778686447397949484e3062334a6c5a43426c626e5270636d5673655342766269426a61474670626977675a3238675a6d3979644767675957356b49474e76626e46315a58497549697767496d6c745957646c496a6f67496d526864474536615731685a32557663335a6e4b3368746244746959584e6c4e6a51735545684f4d6c7035516a52695633683159336f7761574649556a426a5247393254444e6b4d3252354e544e4e655456325932316a646b31715158644e517a6c365a47316a61556c49516e6c61574535735932356162464659546e646156303477565731474d4746584f446c4a626d684f59566331576c52586248564a527a4673576c685261556c49576e426157475244596a4e6e4f556c715157644e51304636546c52425a3031365658644a616a5134597a4e534e574a485653744d626c49305a454e434e306c48576e4269523363325355644b63316c58546e4a5065554a74596a49314d457858576d68695632787a5a5652765a324a584f5856694d3035335756644f62453935516d31694d6a55775446684f6347567456545a4a524556355930686e4e325a5564335a6a4d314931596b64564b314249536d785a4d31466e5a444a73613252485a7a6c4a616b563354554e5661556c4861477868563252765a455177615531555158644b55306c6e576d317363324a454d476c6b4d6d68775a45645661556c444f43745153464a735a5568525a3256454d476c4e56454670535568724f556c715358644a61554a71596b6447656d4e364d476c6b5347677753576f3152466c59516e426b527a6c7a55454d354d46705961444251616e6777576c686f4d456c495a7a6c4a616b563353576c434e5642545354424e51306c6e57544a3461474d7a54546c4a626c49305a454e4a4b314659546a426a62555a7a55454d354d46705961444251616e6777576c686f4d456c495a7a6c4a616b563353576c434e56425453544a4e51306c6e57544a3461474d7a54546c4a626c49305a454e4a4b315258566d746856315979575664334f45777a556d786c5346457255456853624756495557646c524442705456524261556c49617a6c4a616d643353576c43616d4a48526e706a656a42705a45686f4d456c714e56685a57464a7359327033646d5248566a526b524451345a4564574e475244516a525155306c3454554e4a5a3256554d476c4e5645463353576c43616d4a48526e706a656a42705a45686f4d456c714e56685a5745703559566331626c42444f54426157476777554770344d4670596144424a534763355357704664306c70516a565155306c345457704261556c48546e4e5a5745353655464e4b4d47564955576c5161314a7757544e53614752484f586c6a4d6d687759305233646d5248566a526b524451345a4564574e475244516a525155306c3454554e4a5a3256554d476c4e5646463353576c43616d4a48526e706a656a42705a45686f4d456c714e56645a563368765756643463316c5564335a6b523159305a4551304f45777a546a4a61656a51394969776959585230636d6c696458526c6379493657337367496e527959576c3058335235634755694f69416955326c365a53497349434a32595778315a53493649434a445958427064473973496942394c43423749434a30636d4670644639306558426c496a6f67496c4e7761584a706443497349434a32595778315a53493649434a4263335279595777694948307349487367496e527959576c3058335235634755694f6941695157646c49697767496e5a686248566c496a6f67496b316c5a476c6c646d4673496942394c43423749434a30636d4670644639306558426c496a6f67496c4a6c63323931636d4e6c49697767496e5a686248566c496a6f67496c646864475679496942394c43423749434a30636d4670644639306558426c496a6f67496b3176636d46735a53497349434a32595778315a53493649434a5859584a796157356e496942394c43423749434a30636d4670644639306558426c496a6f67496b6476646d5679626d316c626e51694c434169646d4673645755694f69416952476c6a6447463062334a7a61476c77496942394c43423749434a30636d4670644639306558426c496a6f67496c4a6c5957787449697767496e5a686248566c496a6f67496c5a686247686862477868496942395858303d00000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xf5e2ebf727d16274508ca3bd5f26929327e3a1fec8b6aafae19d42972547c153"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC0981Df196dc6c6fb8673B912B07956256D7e9fF",
            "gas": 245691,
            "value": 0,
            "callType": "staticcall",
            "input": HexBytes(
                "0xc87b56dd0000000000000000000000000000000000000000000000000000000000000d88"
            ),
            "to": "0xdEcC60000ba66700a009b8F9F7D82676B5cfA88A",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 217795,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000006cd646174613a6170706c69636174696f6e2f6a736f6e3b6261736536342c65794a755957316c496a6f67496c4e6c644852735a57316c626e5167497a4d304e6a51694c4341695a47567a59334a7063485270623234694f694169553256306447786c6257567564484d6759584a6c49474567644856796269426959584e6c5a43426a61585a7062476c7a595852706232346763326c74645778686447397949484e3062334a6c5a43426c626e5270636d5673655342766269426a61474670626977675a3238675a6d3979644767675957356b49474e76626e46315a58497549697767496d6c745957646c496a6f67496d526864474536615731685a32557663335a6e4b3368746244746959584e6c4e6a51735545684f4d6c7035516a52695633683159336f7761574649556a426a5247393254444e6b4d3252354e544e4e655456325932316a646b31715158644e517a6c365a47316a61556c49516e6c61574535735932356162464659546e646156303477565731474d4746584f446c4a626d684f59566331576c52586248564a527a4673576c685261556c49576e426157475244596a4e6e4f556c715157644e51304636546c52425a3031365658644a616a5134597a4e534e574a485653744d626c49305a454e434e306c48576e4269523363325355644b63316c58546e4a5065554a74596a49314d457858576d68695632787a5a5652765a324a584f5856694d3035335756644f62453935516d31694d6a55775446684f6347567456545a4a524556355930686e4e325a5564335a6a4d314931596b64564b314249536d785a4d31466e5a444a73613252485a7a6c4a616b563354554e5661556c4861477868563252765a455177615531555158644b55306c6e576d317363324a454d476c6b4d6d68775a45645661556c444f43745153464a735a5568525a3256454d476c4e56454670535568724f556c715358644a61554a71596b6447656d4e364d476c6b5347677753576f3152466c59516e426b527a6c7a55454d354d46705961444251616e6777576c686f4d456c495a7a6c4a616b563353576c434e5642545354424e51306c6e57544a3461474d7a54546c4a626c49305a454e4a4b314659546a426a62555a7a55454d354d46705961444251616e6777576c686f4d456c495a7a6c4a616b563353576c434e56425453544a4e51306c6e57544a3461474d7a54546c4a626c49305a454e4a4b315258566d746856315979575664334f45777a556d786c5346457255456853624756495557646c524442705456524261556c49617a6c4a616d643353576c43616d4a48526e706a656a42705a45686f4d456c714e56685a57464a7359327033646d5248566a526b524451345a4564574e475244516a525155306c3454554e4a5a3256554d476c4e5645463353576c43616d4a48526e706a656a42705a45686f4d456c714e56685a5745703559566331626c42444f54426157476777554770344d4670596144424a534763355357704664306c70516a565155306c345457704261556c48546e4e5a5745353655464e4b4d47564955576c5161314a7757544e53614752484f586c6a4d6d687759305233646d5248566a526b524451345a4564574e475244516a525155306c3454554e4a5a3256554d476c4e5646463353576c43616d4a48526e706a656a42705a45686f4d456c714e56645a563368765756643463316c5564335a6b523159305a4551304f45777a546a4a61656a51394969776959585230636d6c696458526c6379493657337367496e527959576c3058335235634755694f69416955326c365a53497349434a32595778315a53493649434a445958427064473973496942394c43423749434a30636d4670644639306558426c496a6f67496c4e7761584a706443497349434a32595778315a53493649434a4263335279595777694948307349487367496e527959576c3058335235634755694f6941695157646c49697767496e5a686248566c496a6f67496b316c5a476c6c646d4673496942394c43423749434a30636d4670644639306558426c496a6f67496c4a6c63323931636d4e6c49697767496e5a686248566c496a6f67496c646864475679496942394c43423749434a30636d4670644639306558426c496a6f67496b3176636d46735a53497349434a32595778315a53493649434a5859584a796157356e496942394c43423749434a30636d4670644639306558426c496a6f67496b6476646d5679626d316c626e51694c434169646d4673645755694f69416952476c6a6447463062334a7a61476c77496942394c43423749434a30636d4670644639306558426c496a6f67496c4a6c5957787449697767496e5a686248566c496a6f67496c5a686247686862477868496942395858303d00000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0xf5e2ebf727d16274508ca3bd5f26929327e3a1fec8b6aafae19d42972547c153"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0x3907f6bC753b6A0B0ff1C68cdd3595A940a4C16A",
            "gas": 0,
            "value": 35400000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x9e8b2990f80ce4bAEF5cD6b7049e8cCF02813eB1",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc883289f103aa8ce65340eb880b4e99598707090af3f35ac38d983d59b3c272c"
        ),
        "transactionPosition": 38,
        "type": "call",
    },
    {
        "action": {
            "from": "0x3A49309413793b32F6A308769220147feDbFfa5f",
            "gas": 24984,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0xa22cb465000000000000000000000000e1f3bdd68f24934fe154fcf2c885b58d7cb0eaf60000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0xdDA32aabBBB6c44eFC567baC5F7C35f185338456",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 24984, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc05e8ce528fd257471f3961ee467d56f80a17f75be6a0b8d11a2bfe25fdb8763"
        ),
        "transactionPosition": 39,
        "type": "call",
    },
    {
        "action": {
            "from": "0xd34AE229C5E8493bFC25FA17a7a04A3d72d0a455",
            "gas": 0,
            "value": 200000000000000000,
            "callType": "call",
            "input": HexBytes("0x"),
            "to": "0x77ACC06250552c8A96e9560670328974386D632F",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xaae3e3d36a7d210372e22920a103a5cbe695d6c273bfa46eb7bc7bf903c669c4"
        ),
        "transactionPosition": 40,
        "type": "call",
    },
    {
        "action": {
            "from": "0xecbeCd7369D708B2fb6489220dd045144F168328",
            "gas": 24659,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x095ea7b30000000000000000000000008692e782ea478623f3342e0fb3936f6530c5d54f00000000000000000000000000000000000000000000000000000005b5d429bc"
            ),
            "to": "0x3C4B6E6e1eA3D4863700D7F76b36B7f3D3f13E3d",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 24659,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x31aecc7e3c6c9062caf6532ec45a9239b85490fa85396d8c00cfc39f55e9138b"
        ),
        "transactionPosition": 41,
        "type": "call",
    },
    {
        "action": {
            "from": "0x229D6a31d0CF2225837DB8C82A6c78De5cDe114d",
            "gas": 20840,
            "value": 0,
            "callType": "call",
            "input": HexBytes(
                "0x23b872dd000000000000000000000000229d6a31d0cf2225837db8c82a6c78de5cde114d000000000000000000000000bc1eb4359ab755af079f6ef77e3faac465e53eda0000000000000000000000000000000000000000000000000000000000010cdd"
            ),
            "to": "0x50f5474724e0Ee42D9a4e711ccFB275809Fd6d4a",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 20840, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xb26b3e31995258eecbd92e61f1d222bd16369c83eae85a4760776cb5adef26cf"
        ),
        "transactionPosition": 42,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1B320348DcF5Fe741161c87BD321f4170Bf5FE45",
            "gas": 495819,
            "value": 0,
            "callType": "call",
            "input": HexBytes("0xddd81f82"),
            "to": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 376538,
            "output": HexBytes(
                "0x0000000000000000000000001f4e3e948830f342c9e575155f7929b3512d0788"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x87a0b62f5d2350e2161abfc9071c68a964272ec288c1e00d564437a01d48ef53"
        ),
        "transactionPosition": 43,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
            "gas": 450467,
            "value": 0,
            "init": HexBytes(
                "0x608060405234801561001057600080fd5b506040516105d03803806105d08339810160409081528151602083015191830151909201610046836401000000006100e0810204565b61005882640100000000610102810204565b81600160a060020a03168160405180828051906020019080838360005b8381101561008d578181015183820152602001610075565b50505050905090810190601f1680156100ba5780820380516001836020036101000a031916815260200191505b50915050600060405180830381855af491505015156100d857600080fd5b505050610165565b60018054600160a060020a031916600160a060020a0392909216919091179055565b600054600160a060020a038281169116141561011d57600080fd5b60008054600160a060020a031916600160a060020a038316908117825560405190917fbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b91a250565b61045c806101746000396000f3006080604052600436106100825763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663025313a281146100c85780633659cfe6146100f95780634555d5c91461011c5780634f1ef286146101435780635c60da1b1461019d5780636fde8202146101b2578063f1739cae146101c7575b600061008c6101e8565b9050600160a060020a03811615156100a357600080fd5b60405136600082376000803683855af43d806000843e8180156100c4578184f35b8184fd5b3480156100d457600080fd5b506100dd6101f7565b60408051600160a060020a039092168252519081900360200190f35b34801561010557600080fd5b5061011a600160a060020a0360043516610206565b005b34801561012857600080fd5b50610131610239565b60408051918252519081900360200190f35b60408051602060046024803582810135601f810185900485028601850190965285855261011a958335600160a060020a031695369560449491939091019190819084018382808284375094975061023e9650505050505050565b3480156101a957600080fd5b506100dd6101e8565b3480156101be57600080fd5b506100dd6102f2565b3480156101d357600080fd5b5061011a600160a060020a0360043516610301565b600054600160a060020a031690565b60006102016102f2565b905090565b61020e6101f7565b600160a060020a031633600160a060020a031614151561022d57600080fd5b61023681610391565b50565b600290565b6102466101f7565b600160a060020a031633600160a060020a031614151561026557600080fd5b61026e82610206565b30600160a060020a03168160405180828051906020019080838360005b838110156102a357818101518382015260200161028b565b50505050905090810190601f1680156102d05780820380516001836020036101000a031916815260200191505b50915050600060405180830381855af491505015156102ee57600080fd5b5050565b600154600160a060020a031690565b6103096101f7565b600160a060020a031633600160a060020a031614151561032857600080fd5b600160a060020a038116151561033d57600080fd5b7f5a3e66efaa1e445ebd894728a69d6959842ea1e97bd79b892797106e270efcd96103666101f7565b60408051600160a060020a03928316815291841660208301528051918290030190a161023681610401565b600054600160a060020a03828116911614156103ac57600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a038316908117825560405190917fbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b91a250565b6001805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a03929092169190911790555600a165627a7a723058205f26049bbc794226b505f589b2ee1130db54310d79dd8a635c6f6c61e305a77700290000000000000000000000001b320348dcf5fe741161c87bd321f4170bf5fe45000000000000000000000000f9e266af4bca5890e2781812cc6a6e89495a79f200000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000044485cc9550000000000000000000000001b320348dcf5fe741161c87bd321f4170bf5fe45000000000000000000000000a5409ec958c83c3f309868babaca7c86dcb077c100000000000000000000000000000000000000000000000000000000"
            ),
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 317883,
            "code": HexBytes(
                "0x6080604052600436106100825763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663025313a281146100c85780633659cfe6146100f95780634555d5c91461011c5780634f1ef286146101435780635c60da1b1461019d5780636fde8202146101b2578063f1739cae146101c7575b600061008c6101e8565b9050600160a060020a03811615156100a357600080fd5b60405136600082376000803683855af43d806000843e8180156100c4578184f35b8184fd5b3480156100d457600080fd5b506100dd6101f7565b60408051600160a060020a039092168252519081900360200190f35b34801561010557600080fd5b5061011a600160a060020a0360043516610206565b005b34801561012857600080fd5b50610131610239565b60408051918252519081900360200190f35b60408051602060046024803582810135601f810185900485028601850190965285855261011a958335600160a060020a031695369560449491939091019190819084018382808284375094975061023e9650505050505050565b3480156101a957600080fd5b506100dd6101e8565b3480156101be57600080fd5b506100dd6102f2565b3480156101d357600080fd5b5061011a600160a060020a0360043516610301565b600054600160a060020a031690565b60006102016102f2565b905090565b61020e6101f7565b600160a060020a031633600160a060020a031614151561022d57600080fd5b61023681610391565b50565b600290565b6102466101f7565b600160a060020a031633600160a060020a031614151561026557600080fd5b61026e82610206565b30600160a060020a03168160405180828051906020019080838360005b838110156102a357818101518382015260200161028b565b50505050905090810190601f1680156102d05780820380516001836020036101000a031916815260200191505b50915050600060405180830381855af491505015156102ee57600080fd5b5050565b600154600160a060020a031690565b6103096101f7565b600160a060020a031633600160a060020a031614151561032857600080fd5b600160a060020a038116151561033d57600080fd5b7f5a3e66efaa1e445ebd894728a69d6959842ea1e97bd79b892797106e270efcd96103666101f7565b60408051600160a060020a03928316815291841660208301528051918290030190a161023681610401565b600054600160a060020a03828116911614156103ac57600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a038316908117825560405190917fbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b91a250565b6001805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a03929092169190911790555600a165627a7a723058205f26049bbc794226b505f589b2ee1130db54310d79dd8a635c6f6c61e305a7770029"
            ),
            "address": "0x1f4E3e948830F342c9E575155f7929b3512D0788",
        },
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x87a0b62f5d2350e2161abfc9071c68a964272ec288c1e00d564437a01d48ef53"
        ),
        "transactionPosition": 43,
        "type": "create",
    },
    {
        "action": {
            "from": "0x1f4E3e948830F342c9E575155f7929b3512D0788",
            "gas": 394870,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x485cc9550000000000000000000000001b320348dcf5fe741161c87bd321f4170bf5fe45000000000000000000000000a5409ec958c83c3f309868babaca7c86dcb077c100000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xF9e266af4BcA5890e2781812cc6a6E89495a79f2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 45120, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x87a0b62f5d2350e2161abfc9071c68a964272ec288c1e00d564437a01d48ef53"
        ),
        "transactionPosition": 43,
        "type": "call",
    },
    {
        "action": {
            "from": "0x26B675Fc79EA35805b6594857c429CFe2D5f1509",
            "gas": 495819,
            "value": 0,
            "callType": "call",
            "input": HexBytes("0xddd81f82"),
            "to": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 376538,
            "output": HexBytes(
                "0x00000000000000000000000050198a0c9de7d342fdbb24f57242dddf25b2d1b6"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x73c429f04ca56cd06ec53cfdaf845faf6f284e368eeeb310b1b7b825fa70a6db"
        ),
        "transactionPosition": 44,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa5409ec958C83C3f309868babACA7c86DCB077c1",
            "gas": 450467,
            "value": 0,
            "init": HexBytes(
                "0x608060405234801561001057600080fd5b506040516105d03803806105d08339810160409081528151602083015191830151909201610046836401000000006100e0810204565b61005882640100000000610102810204565b81600160a060020a03168160405180828051906020019080838360005b8381101561008d578181015183820152602001610075565b50505050905090810190601f1680156100ba5780820380516001836020036101000a031916815260200191505b50915050600060405180830381855af491505015156100d857600080fd5b505050610165565b60018054600160a060020a031916600160a060020a0392909216919091179055565b600054600160a060020a038281169116141561011d57600080fd5b60008054600160a060020a031916600160a060020a038316908117825560405190917fbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b91a250565b61045c806101746000396000f3006080604052600436106100825763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663025313a281146100c85780633659cfe6146100f95780634555d5c91461011c5780634f1ef286146101435780635c60da1b1461019d5780636fde8202146101b2578063f1739cae146101c7575b600061008c6101e8565b9050600160a060020a03811615156100a357600080fd5b60405136600082376000803683855af43d806000843e8180156100c4578184f35b8184fd5b3480156100d457600080fd5b506100dd6101f7565b60408051600160a060020a039092168252519081900360200190f35b34801561010557600080fd5b5061011a600160a060020a0360043516610206565b005b34801561012857600080fd5b50610131610239565b60408051918252519081900360200190f35b60408051602060046024803582810135601f810185900485028601850190965285855261011a958335600160a060020a031695369560449491939091019190819084018382808284375094975061023e9650505050505050565b3480156101a957600080fd5b506100dd6101e8565b3480156101be57600080fd5b506100dd6102f2565b3480156101d357600080fd5b5061011a600160a060020a0360043516610301565b600054600160a060020a031690565b60006102016102f2565b905090565b61020e6101f7565b600160a060020a031633600160a060020a031614151561022d57600080fd5b61023681610391565b50565b600290565b6102466101f7565b600160a060020a031633600160a060020a031614151561026557600080fd5b61026e82610206565b30600160a060020a03168160405180828051906020019080838360005b838110156102a357818101518382015260200161028b565b50505050905090810190601f1680156102d05780820380516001836020036101000a031916815260200191505b50915050600060405180830381855af491505015156102ee57600080fd5b5050565b600154600160a060020a031690565b6103096101f7565b600160a060020a031633600160a060020a031614151561032857600080fd5b600160a060020a038116151561033d57600080fd5b7f5a3e66efaa1e445ebd894728a69d6959842ea1e97bd79b892797106e270efcd96103666101f7565b60408051600160a060020a03928316815291841660208301528051918290030190a161023681610401565b600054600160a060020a03828116911614156103ac57600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a038316908117825560405190917fbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b91a250565b6001805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a03929092169190911790555600a165627a7a723058205f26049bbc794226b505f589b2ee1130db54310d79dd8a635c6f6c61e305a777002900000000000000000000000026b675fc79ea35805b6594857c429cfe2d5f1509000000000000000000000000f9e266af4bca5890e2781812cc6a6e89495a79f200000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000044485cc95500000000000000000000000026b675fc79ea35805b6594857c429cfe2d5f1509000000000000000000000000a5409ec958c83c3f309868babaca7c86dcb077c100000000000000000000000000000000000000000000000000000000"
            ),
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {
            "gasUsed": 317883,
            "code": HexBytes(
                "0x6080604052600436106100825763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663025313a281146100c85780633659cfe6146100f95780634555d5c91461011c5780634f1ef286146101435780635c60da1b1461019d5780636fde8202146101b2578063f1739cae146101c7575b600061008c6101e8565b9050600160a060020a03811615156100a357600080fd5b60405136600082376000803683855af43d806000843e8180156100c4578184f35b8184fd5b3480156100d457600080fd5b506100dd6101f7565b60408051600160a060020a039092168252519081900360200190f35b34801561010557600080fd5b5061011a600160a060020a0360043516610206565b005b34801561012857600080fd5b50610131610239565b60408051918252519081900360200190f35b60408051602060046024803582810135601f810185900485028601850190965285855261011a958335600160a060020a031695369560449491939091019190819084018382808284375094975061023e9650505050505050565b3480156101a957600080fd5b506100dd6101e8565b3480156101be57600080fd5b506100dd6102f2565b3480156101d357600080fd5b5061011a600160a060020a0360043516610301565b600054600160a060020a031690565b60006102016102f2565b905090565b61020e6101f7565b600160a060020a031633600160a060020a031614151561022d57600080fd5b61023681610391565b50565b600290565b6102466101f7565b600160a060020a031633600160a060020a031614151561026557600080fd5b61026e82610206565b30600160a060020a03168160405180828051906020019080838360005b838110156102a357818101518382015260200161028b565b50505050905090810190601f1680156102d05780820380516001836020036101000a031916815260200191505b50915050600060405180830381855af491505015156102ee57600080fd5b5050565b600154600160a060020a031690565b6103096101f7565b600160a060020a031633600160a060020a031614151561032857600080fd5b600160a060020a038116151561033d57600080fd5b7f5a3e66efaa1e445ebd894728a69d6959842ea1e97bd79b892797106e270efcd96103666101f7565b60408051600160a060020a03928316815291841660208301528051918290030190a161023681610401565b600054600160a060020a03828116911614156103ac57600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a038316908117825560405190917fbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b91a250565b6001805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a03929092169190911790555600a165627a7a723058205f26049bbc794226b505f589b2ee1130db54310d79dd8a635c6f6c61e305a7770029"
            ),
            "address": "0x50198a0C9De7d342FDbb24F57242dDDf25B2d1b6",
        },
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x73c429f04ca56cd06ec53cfdaf845faf6f284e368eeeb310b1b7b825fa70a6db"
        ),
        "transactionPosition": 44,
        "type": "create",
    },
    {
        "action": {
            "from": "0x50198a0C9De7d342FDbb24F57242dDDf25B2d1b6",
            "gas": 394870,
            "value": 0,
            "callType": "delegatecall",
            "input": HexBytes(
                "0x485cc95500000000000000000000000026b675fc79ea35805b6594857c429cfe2d5f1509000000000000000000000000a5409ec958c83c3f309868babaca7c86dcb077c100000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xF9e266af4BcA5890e2781812cc6a6E89495a79f2",
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": {"gasUsed": 45120, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x73c429f04ca56cd06ec53cfdaf845faf6f284e368eeeb310b1b7b825fa70a6db"
        ),
        "transactionPosition": 44,
        "type": "call",
    },
    {
        "action": {
            "author": "0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c",
            "rewardType": "block",
            "value": 2000000000000000000,
        },
        "blockHash": HexBytes(
            "0x8f9809f6012f85803956a419e2e54914dfdebba33e4f7a0d1574b12e92499c0e"
        ),
        "blockNumber": 13191781,
        "result": None,
        "subtraces": 0,
        "traceAddress": [],
        "type": "reward",
    },
]

trace_block_15630274_mock = [
    {
        "action": {
            "from": "0xA7B5cA022774BD02842932e4358DDCbea0CCaADe",
            "callType": "call",
            "gas": 118862,
            "input": HexBytes(
                "0xa0712d6800000000000000000000000000000000000000000000000000000000000000cb"
            ),
            "to": "0xcb6B570B8AeAbE38B449Aff31f901B8E1B91e396",
            "value": 253000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "error": "Reverted",
        "result": {
            "gasUsed": 30842,
            "output": HexBytes(
                "0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001c4552433732313a20746f6b656e20616c7265616479206d696e74656400000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x71453e4f713dd1f102cbdbbf9d7a9995f75ee1f57ab5ded1f7e3cae93dab4c2b"
        ),
        "transactionPosition": 0,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2393eAbFB6885e83822f79cbf5Bd1FC05C95FE54",
            "callType": "call",
            "gas": 107737,
            "input": HexBytes(
                "0x3300000000000000000da13006ec0000000280a9d4e297b21218010201f4ff010088e6a0c2ddd26feeb64f039a2c41296fcb3f5640a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48c02aaa39b223fe8d0a0e5c4f27ead9083c756cc203"
            ),
            "to": "0x9507c04B10486547584C37bCBd931B2a4FeE9A41",
            "value": 15630274,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 60937, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9507c04B10486547584C37bCBd931B2a4FeE9A41",
            "callType": "call",
            "gas": 98772,
            "input": HexBytes(
                "0x128acb080000000000000000000000009507c04b10486547584c37bcbd931b2a4fee9a410000000000000000000000000000000000000000000000000000000000000001fffffffffffffffffffffffffffffffffffffffffffffffd7f562b1d684dede800000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000001f40000000000000000000000000000000000000000000000000000000da13006ec00000000000000000000000000000000000000000000000280a9d4e297b2121800000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 53152,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000da13006ecfffffffffffffffffffffffffffffffffffffffffffffffd7f562b1d684dede8"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "call",
            "gas": 75814,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000009507c04b10486547584c37bcbd931b2a4fee9a4100000000000000000000000000000000000000000000000280a9d4e297b21218"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8862,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "staticcall",
            "gas": 66219,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000020613b1edf2a"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 64454,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000020613b1edf2a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1, 0],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "call",
            "gas": 64129,
            "input": HexBytes(
                "0xfa461e330000000000000000000000000000000000000000000000000000000da13006ecfffffffffffffffffffffffffffffffffffffffffffffffd7f562b1d684dede8000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000001f40000000000000000000000000000000000000000000000000000000da13006ec00000000000000000000000000000000000000000000000280a9d4e297b2121800000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x9507c04B10486547584C37bCBd931B2a4FeE9A41",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 13863, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 2],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9507c04B10486547584C37bCBd931B2a4FeE9A41",
            "callType": "call",
            "gas": 60026,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f56400000000000000000000000000000000000000000000000000000000da13006ec"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 10417,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 2, 0],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 58355,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f56400000000000000000000000000000000000000000000000000000000da13006ec"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 9628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 0],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "staticcall",
            "gas": 49849,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000206edc4ee616"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 3],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 48340,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000206edc4ee616"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 3, 0],
        "transactionHash": HexBytes(
            "0x55cb57ee60fca9739fc9e90010b0889701c4cebd58a053fa6bfe156484c48244"
        ),
        "transactionPosition": 1,
        "type": "call",
    },
    {
        "action": {
            "from": "0x81FfD37ed3ab472F9bC1d3135D583dC594Bf4795",
            "callType": "call",
            "gas": 14,
            "input": HexBytes("0x"),
            "to": "0x81FfD37ed3ab472F9bC1d3135D583dC594Bf4795",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x649cdb70fa7f1a5a32e154e07ec74183bb15a370cead1461ceda940146902f84"
        ),
        "transactionPosition": 2,
        "type": "call",
    },
    {
        "action": {
            "from": "0xf896736D814F87C3A94eDc7F4D16b1D0b87aCDf7",
            "callType": "call",
            "gas": 607121,
            "input": HexBytes(
                "0xabcffc2600000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000002a000000000000000000000000000000000000000000000000000000000000008a0000000000000000000000000a888d9616c2222788fa19f05f77221a290eef704000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000160000000000000000000000000f896736d814f87c3a94edc7f4d16b1d0b87acdf70000000000000000000000000000000000000000000000000000dd9a755500060000000000000000000000000000000000000000000000000c576c02cb1573a5000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000000000000100000000000000000000000041684b361557e9282e0373ca51260d9331e518c900000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000dd9a75550006000000000000000000000000000000000000000000000000000000000000006000000000000000000000000096c195f6643a3d797cb90cb6ba0ae2776d51b5f30000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000005e0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000a888d9616c2222788fa19f05f77221a290eef704000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0000000000000000000000000000000000000000000000000c576c02cb1573a5000000000000000000000000f896736d814f87c3a94edc7f4d16b1d0b87acdf7000000000000000000000000000000000000000000000000000000006333f8f300000000000000000000000000000000000000000000000000000000000005400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000002a00000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000c00000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535000000000000000000000000a888d9616c2222788fa19f05f77221a290eef704000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000041684b361557e9282e0373ca51260d9331e518c90000000000000000000000000000000000000000000000000000dd9a7555000600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000060100000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c806df3b2bbb68adc8b0e302443692037ed9f91b42000000000000000000000063000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000006b175474e89094c44da98b954eedeac495271d0f0000000000000000000000000000000000000000000000000000000043df21290000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000005010000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060594a405d53811d3bc4766596efd80fd545a2700000000000000000000000006b175474e89094c44da98b954eedeac495271d0f000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000003dba93b155bdf0d4f2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000006000000000000000000000000096c195f6643a3d797cb90cb6ba0ae2776d51b5f30000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000008c7b22536f75726365223a22646578746f6f6c73222c2244617461223a227b5c22736f757263655c223a5c22646578746f6f6c735c227d222c22416d6f756e74496e555344223a22313134392e333439363232303437393835222c22416d6f756e744f7574555344223a22313134362e36313133323031323135323637222c22526566657272616c223a22227d0000000000000000000000000000000000000000"
            ),
            "to": "0x617Dee16B86534a5d792A4d7A62FB491B544111E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 564703,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000c695eab806c1ab400000000000000000000000000000000000000000000000000000000000899b4"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x617Dee16B86534a5d792A4d7A62FB491B544111E",
            "callType": "call",
            "gas": 591492,
            "input": HexBytes(
                "0x23b872dd000000000000000000000000f896736d814f87c3a94edc7f4d16b1d0b87acdf700000000000000000000000041684b361557e9282e0373ca51260d9331e518c90000000000000000000000000000000000000000000000000000dd9a75550006"
            ),
            "to": "0xA888D9616C2222788fa19f05F77221A290eEf704",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 91897,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x617Dee16B86534a5d792A4d7A62FB491B544111E",
            "callType": "call",
            "gas": 492407,
            "input": HexBytes(
                "0xd9c45357000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000005e0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000a888d9616c2222788fa19f05f77221a290eef704000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0000000000000000000000000000000000000000000000000c576c02cb1573a5000000000000000000000000f896736d814f87c3a94edc7f4d16b1d0b87acdf7000000000000000000000000000000000000000000000000000000006333f8f300000000000000000000000000000000000000000000000000000000000005400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000002a00000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000c00000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535000000000000000000000000a888d9616c2222788fa19f05f77221a290eef704000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000041684b361557e9282e0373ca51260d9331e518c90000000000000000000000000000000000000000000000000000dd9a7555000600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000060100000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c806df3b2bbb68adc8b0e302443692037ed9f91b42000000000000000000000063000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000006b175474e89094c44da98b954eedeac495271d0f0000000000000000000000000000000000000000000000000000000043df21290000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000005010000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060594a405d53811d3bc4766596efd80fd545a2700000000000000000000000006b175474e89094c44da98b954eedeac495271d0f000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000003dba93b155bdf0d4f2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000006000000000000000000000000096c195f6643a3d797cb90cb6ba0ae2776d51b5f30000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001e"
            ),
            "to": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 450179, "output": HexBytes("0x")},
        "subtraces": 23,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 478270,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xA888D9616C2222788fa19f05F77221A290eEf704",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2632,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000dd9a75550006"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 474576,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea5350000000000000000000000000000000000000000000000000000dd9a75550006"
            ),
            "to": "0xA888D9616C2222788fa19f05F77221A290eEf704",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 33710,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 438113,
            "input": HexBytes(
                "0xeb22d54f00000000000000000000000059a16ece7143459801c3b3f24dc8a0cdfb9565710000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535000000000000000000000000a888d9616c2222788fa19f05f77221a290eef7040000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0xA9249f4D7e84B206d010Bc90211a11fDA57785b4",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 16861,
            "output": HexBytes(
                "0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000600ed4459d89ce0000000000000000000000000000000000000000000000000000001dc618188100000000000000000000000000000000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000001e"
            ),
        },
        "subtraces": 4,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA9249f4D7e84B206d010Bc90211a11fDA57785b4",
            "callType": "staticcall",
            "gas": 428167,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000001dc618188100000000000000000000000000000000000000000000000000600ed4459d89ce000000000000000000000000000000000000000000000000000000006333f437"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA9249f4D7e84B206d010Bc90211a11fDA57785b4",
            "callType": "staticcall",
            "gas": 420835,
            "input": HexBytes("0x0dfe1681"),
            "to": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2381,
            "output": HexBytes(
                "0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 1],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA9249f4D7e84B206d010Bc90211a11fDA57785b4",
            "callType": "staticcall",
            "gas": 418090,
            "input": HexBytes("0xd21220a7"),
            "to": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2357,
            "output": HexBytes(
                "0x000000000000000000000000a888d9616c2222788fa19f05f77221a290eef704"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 2],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA9249f4D7e84B206d010Bc90211a11fDA57785b4",
            "callType": "staticcall",
            "gas": 415370,
            "input": HexBytes("0x0dfe1681"),
            "to": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 381,
            "output": HexBytes(
                "0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 3],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 420581,
            "input": HexBytes(
                "0x70a082310000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535"
            ),
            "to": "0xA888D9616C2222788fa19f05F77221A290eEf704",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2632,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000060ec6ebaf289d4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 3],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 417202,
            "input": HexBytes(
                "0x671a11b50000000000000000000000000000000000000000000000000000dd9a7555000600000000000000000000000000000000000000000000000000600ed4459d89ce0000000000000000000000000000000000000000000000000000001dc618188100000000000000000000000000000000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000001e"
            ),
            "to": "0xA9249f4D7e84B206d010Bc90211a11fDA57785b4",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1070,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000043df2129"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 4],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 413064,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 9815,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 5],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 399482,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 5, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 402924,
            "input": HexBytes("0x0dfe1681"),
            "to": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 381,
            "output": HexBytes(
                "0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 6],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 401554,
            "input": HexBytes(
                "0x022c0d9f0000000000000000000000000000000000000000000000000000000043df2129000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041684b361557e9282e0373ca51260d9331e518c900000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 66787, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1, 7],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "callType": "call",
            "gas": 388513,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000041684b361557e9282e0373ca51260d9331e518c90000000000000000000000000000000000000000000000000000000043df2129"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 35517,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 7, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 381710,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000041684b361557e9282e0373ca51260d9331e518c90000000000000000000000000000000000000000000000000000000043df2129"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 34728,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 7, 0, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "callType": "staticcall",
            "gas": 352929,
            "input": HexBytes(
                "0x70a082310000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000001d8238f758"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 7, 1],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 346685,
            "input": HexBytes(
                "0x70a082310000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000001d8238f758"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 7, 1, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4D42FD2fe2Eb1e4C7eec64272a1f715dce0eA535",
            "callType": "staticcall",
            "gas": 351229,
            "input": HexBytes(
                "0x70a082310000000000000000000000004d42fd2fe2eb1e4c7eec64272a1f715dce0ea535"
            ),
            "to": "0xA888D9616C2222788fa19f05F77221A290eEf704",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2632,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000060ec6ebaf289d4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 7, 2],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 333822,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000043df2129"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 8],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 327876,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000043df2129"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 8, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 328243,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2602,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 9],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 325070,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000043df2129"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 10],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 319261,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000043df2129"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 10, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 322773,
            "input": HexBytes(
                "0x095ea7b3000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000000000000000043df2129"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 27867,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 11],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 316997,
            "input": HexBytes(
                "0x095ea7b3000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000000000000000043df2129"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 27078,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 11, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 291013,
            "input": HexBytes(
                "0x52bbbe2900000000000000000000000000000000000000000000000000000000000000e000000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041684b361557e9282e0373ca51260d9331e518c900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f8f306df3b2bbb68adc8b0e302443692037ed9f91b420000000000000000000000630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000006b175474e89094c44da98b954eedeac495271d0f0000000000000000000000000000000000000000000000000000000043df212900000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xBA12222222228d8Ba445958a75a0704d566BF2C8",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 113825,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000003dba93b155bdf0d4f2"
            ),
        },
        "subtraces": 3,
        "traceAddress": [1, 12],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBA12222222228d8Ba445958a75a0704d566BF2C8",
            "callType": "call",
            "gas": 259390,
            "input": HexBytes(
                "0x01ec954a000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000006b175474e89094c44da98b954eedeac495271d0f0000000000000000000000000000000000000000000000000000000043df212906df3b2bbb68adc8b0e302443692037ed9f91b420000000000000000000000630000000000000000000000000000000000000000000000000000000000ee7fbf00000000000000000000000041684b361557e9282e0373ca51260d9331e518c900000000000000000000000041684b361557e9282e0373ca51260d9331e518c900000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000002949c2b5d922a7d65cb4d000000000000000000000000000000000000000000000000000002a601af2e47000000000000000000000000000000000000000000000000000002bbe7c65fa7"
            ),
            "to": "0x06Df3b2bbB68adc8B0e302443692037ED9f91b42",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 33575,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000003dba93b155bdf0d4f2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 12, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBA12222222228d8Ba445958a75a0704d566BF2C8",
            "callType": "call",
            "gas": 215110,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000000000000000043df2129"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 10792,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 12, 1],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 211010,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000000000000000043df2129"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 9997,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 12, 1, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBA12222222228d8Ba445958a75a0704d566BF2C8",
            "callType": "call",
            "gas": 203036,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000041684b361557e9282e0373ca51260d9331e518c900000000000000000000000000000000000000000000003dba93b155bdf0d4f2"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 28174,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 12, 2],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 176836,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 602,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000003dba93b155bdf0d4f2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 13],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 174027,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 602,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000003dba93b155bdf0d4f2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 14],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 164881,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 15],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 157690,
            "input": HexBytes(
                "0x128acb0800000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000003dba93b155bdf0d4f200000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000000000000000000000000000000000000000006000000000000000000000000060594a405d53811d3bc4766596efd80fd545a2700000000000000000000000006b175474e89094c44da98b954eedeac495271d0f000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
            ),
            "to": "0x60594a405d53811d3BC4766596EFD80fd545A270",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 82248,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000003dba93b155bdf0d4f2fffffffffffffffffffffffffffffffffffffffffffffffff38d11c4729c0b38"
            ),
        },
        "subtraces": 4,
        "traceAddress": [1, 16],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x60594a405d53811d3BC4766596EFD80fd545A270",
            "callType": "call",
            "gas": 120253,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000041684b361557e9282e0373ca51260d9331e518c90000000000000000000000000000000000000000000000000c72ee3b8d63f4c8"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 27962,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 16, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x60594a405d53811d3BC4766596EFD80fd545A270",
            "callType": "staticcall",
            "gas": 91856,
            "input": HexBytes(
                "0x70a0823100000000000000000000000060594a405d53811d3bc4766596efd80fd545a270"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2602,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000001a70d7d7eb6dde38a5829"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 16, 1],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x60594a405d53811d3BC4766596EFD80fd545A270",
            "callType": "call",
            "gas": 88499,
            "input": HexBytes(
                "0xfa461e3300000000000000000000000000000000000000000000003dba93b155bdf0d4f2fffffffffffffffffffffffffffffffffffffffffffffffff38d11c4729c0b38000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000041684b361557e9282e0373ca51260d9331e518c9000000000000000000000000000000000000000000000000000000000000006000000000000000000000000060594a405d53811d3bc4766596efd80fd545a2700000000000000000000000006b175474e89094c44da98b954eedeac495271d0f000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
            ),
            "to": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 9511, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 16, 2],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 84342,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000060594a405d53811d3bc4766596efd80fd545a27000000000000000000000000000000000000000000000003dba93b155bdf0d4f2"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 6274,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 16, 2, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x60594a405d53811d3BC4766596EFD80fd545A270",
            "callType": "staticcall",
            "gas": 78503,
            "input": HexBytes(
                "0x70a0823100000000000000000000000060594a405d53811d3bc4766596efd80fd545a270"
            ),
            "to": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 602,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000001a74b38126833a17b2d1b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 16, 3],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 74453,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000c72ee3b8d63f4c8"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 17],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 72828,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000c72ee3b8d63f4c8"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 18],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 71757,
            "input": HexBytes(
                "0x2e1a7d4d0000000000000000000000000000000000000000000000000c72ee3b8d63f4c8"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 9195, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 19],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "value": 897041215342769352,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 55, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 19, 0],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 52299,
            "input": HexBytes("0x"),
            "to": "0x96c195F6643A3D797cb90cb6BA0Ae2776D51b5F3",
            "value": 2691123646028308,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 20],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "call",
            "gas": 45081,
            "input": HexBytes("0x"),
            "to": "0xf896736D814F87C3A94eDc7F4D16b1D0b87aCDf7",
            "value": 894350091696741044,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 21],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0x41684b361557E9282E0373CA51260D9331e518C9",
            "callType": "staticcall",
            "gas": 44527,
            "input": HexBytes(
                "0x70a0823100000000000000000000000041684b361557e9282e0373ca51260d9331e518c9"
            ),
            "to": "0xA888D9616C2222788fa19f05F77221A290eEf704",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2632,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 22],
        "transactionHash": HexBytes(
            "0x0829191d1e4da5fcf7001059a66f51183c8fa6c343e4a470d9398306c8095ed0"
        ),
        "transactionPosition": 3,
        "type": "call",
    },
    {
        "action": {
            "from": "0xb8DEC574677e4F59Df452bfAACF5011F1B597ea3",
            "callType": "call",
            "gas": 73368,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c7807e24338b41a34d849492920f2b9d0e4de2cd0000000000000000000000000000000000000000000000000291f66b34670000"
            ),
            "to": "0x0d438F3b5175Bebc262bF23753C1E53d03432bDE",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13006,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xfa5183ed2496b4604a8a000039677bc139744f1049201e48cddd0dfddfe0f365"
        ),
        "transactionPosition": 4,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC241FB19Cf9f9bd9765d99c231a1A16bBe83156E",
            "callType": "call",
            "gas": 73368,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c7807e24338b41a34d849492920f2b9d0e4de2cd000000000000000000000000000000000000000000000000027f7d0bdb920000"
            ),
            "to": "0x0d438F3b5175Bebc262bF23753C1E53d03432bDE",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13006,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x4c8e5be08977569c9fcbe1ca050459a2b8c67fc6a6e642b113764ae5256af3a7"
        ),
        "transactionPosition": 5,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00A25fbfF2D0173A29cE577f1871f1F2c028e672",
            "callType": "call",
            "gas": 73356,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c7807e24338b41a34d849492920f2b9d0e4de2cd000000000000000000000000000000000000000000000000021c044493571800"
            ),
            "to": "0x0d438F3b5175Bebc262bF23753C1E53d03432bDE",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13006,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x874d6a00a710e0e8cb6c9e4c394b6f1b0502ca7517af206ed75aab7028cfca57"
        ),
        "transactionPosition": 6,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa483254773CFe94d502557099945Caf90725473f",
            "callType": "call",
            "gas": 183050,
            "input": HexBytes(
                "0x1cff79cd000000000000000000000000ebd64b5f2e3028fb887d40cc69570d2c59b16bdc000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000c404764a8a00000000000000000000000000000000000000000000004468500d55f04e8b0700000000000000000000000000000000000000000005196da08b776a800000000000000000000000000000000000000000000000142156bb9e6f4fd832d5bf890000000000000000000000000000000000000000000000000015e6c584e8d260000000000000000000000000000000000000000000000000000000006333f48e66000000000000000000000000000000000000000000000000000000000104e300000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 8196,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 64675, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "delegatecall",
            "gas": 178927,
            "input": HexBytes(
                "0x04764a8a00000000000000000000000000000000000000000000004468500d55f04e8b0700000000000000000000000000000000000000000005196da08b776a800000000000000000000000000000000000000000000000142156bb9e6f4fd832d5bf890000000000000000000000000000000000000000000000000015e6c584e8d260000000000000000000000000000000000000000000000000000000006333f48e66000000000000000000000000000000000000000000000000000000000104e3"
            ),
            "to": "0xEbD64b5f2e3028fb887D40cc69570d2C59b16bdc",
            "value": 8196,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 63335,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000004468500d55f04e8b07000000000000000000000000000000000000000000000000001a85d17de53061"
            ),
        },
        "subtraces": 2,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 175754,
            "input": HexBytes(
                "0x128acb0800000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000004468500d55f04e8b070000000000000000000000000000000000000000142156bb9e6f4fd832d5bf8900000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000060fa0bb6e2cb1ae1309eb828215322e997e900993704559ef888f3c68337af15f300000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000514910771af9ca656af840dff83e8264ecf986ca"
            ),
            "to": "0xa6Cc3C2531FdaA6Ae1A3CA84c2855806728693e8",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 52682,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000004468500d55f04e8b07ffffffffffffffffffffffffffffffffffffffffffffffff93f02483dee07e06"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa6Cc3C2531FdaA6Ae1A3CA84c2855806728693e8",
            "callType": "call",
            "gas": 150190,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf90000000000000000000000000000000000000000000000006c0fdb7c211f81fa"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8862,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa6Cc3C2531FdaA6Ae1A3CA84c2855806728693e8",
            "callType": "staticcall",
            "gas": 140595,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a6cc3c2531fdaa6ae1a3ca84c2855806728693e8"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 655,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000006007887d398665287216"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 1],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa6Cc3C2531FdaA6Ae1A3CA84c2855806728693e8",
            "callType": "call",
            "gas": 139178,
            "input": HexBytes(
                "0xfa461e3300000000000000000000000000000000000000000000004468500d55f04e8b07ffffffffffffffffffffffffffffffffffffffffffffffff93f02483dee07e0600000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000060fa0bb6e2cb1ae1309eb828215322e997e900993704559ef888f3c68337af15f300000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000514910771af9ca656af840dff83e8264ecf986ca"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 13309, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0, 2],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 136429,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000a6cc3c2531fdaa6ae1a3ca84c2855806728693e800000000000000000000000000000000000000000000004468500d55f04e8b07"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12700,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 0],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa6Cc3C2531FdaA6Ae1A3CA84c2855806728693e8",
            "callType": "staticcall",
            "gas": 125444,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a6cc3c2531fdaa6ae1a3ca84c2855806728693e8"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 655,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000604bf0cd46dc5576fd1d"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 3],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 113873,
            "input": HexBytes("0x"),
            "to": "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5",
            "value": 1486864370461342,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0xac7f47a0babae1284b8e16945ea02907cf3e7efa571cc3922ca1fed5fe4e57a6"
        ),
        "transactionPosition": 7,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFF82BF5238637B7E5E345888BaB9cd99F5Ebe331",
            "callType": "call",
            "gas": 204230,
            "input": HexBytes(
                "0x1cff79cd000000000000000000000000a2657323a987e02b1c4e8e64aa3844f0e48dbff8000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000c404764a8a00000000000000000000000000000000000000000000010d10f01a7b1db0922d00000000000000000000000000000000000000000000000000020c46733887f0000000000000000000000000000000000000000000000ccd57af7c2d0cfb859200000000000000000000000000000000000000000000000000019e7b4be9f2fe000000000000000000000000000000000000000000000000000000006333f48b660000000000000000000000000000000000000000000000000000000001335300000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 52484,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 69351, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "delegatecall",
            "gas": 199753,
            "input": HexBytes(
                "0x04764a8a00000000000000000000000000000000000000000000010d10f01a7b1db0922d00000000000000000000000000000000000000000000000000020c46733887f0000000000000000000000000000000000000000000000ccd57af7c2d0cfb859200000000000000000000000000000000000000000000000000019e7b4be9f2fe000000000000000000000000000000000000000000000000000000006333f48b6600000000000000000000000000000000000000000000000000000000013353"
            ),
            "to": "0xA2657323a987e02B1C4e8e64AA3844f0e48dBff8",
            "value": 52484,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 67987,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000010d10f01a7b1db0922d000000000000000000000000000000000000000000000000001a2b5fa3fc973f"
            ),
        },
        "subtraces": 2,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 196254,
            "input": HexBytes(
                "0x128acb0800000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000010d10f01a7b1db0922d000000000000000000000000000000000000000000000ccd57af7c2d0cfb859200000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000006041eb661e632bf0d55dfe02085b906a8a326fe309442573b563e0f0f2ed64720b00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000111111111117dc0aa78b770fa6a738034120c302"
            ),
            "to": "0x9feBc984504356225405e26833608b17719c82Ae",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 57334,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000010d10f01a7b1db0922dffffffffffffffffffffffffffffffffffffffffffffffffffffffff54e86a41"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9feBc984504356225405e26833608b17719c82Ae",
            "callType": "call",
            "gas": 168614,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf900000000000000000000000000000000000000000000000000000000ab1795bf"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 10417,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 165247,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf900000000000000000000000000000000000000000000000000000000ab1795bf"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 9628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0, 0],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9feBc984504356225405e26833608b17719c82Ae",
            "callType": "staticcall",
            "gas": 157489,
            "input": HexBytes(
                "0x70a082310000000000000000000000009febc984504356225405e26833608b17719c82ae"
            ),
            "to": "0x111111111117dC0aa78b770fA6A738034120C302",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 510,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000001f0e7e21f51f8c1bb91b9"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 1],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9feBc984504356225405e26833608b17719c82Ae",
            "callType": "call",
            "gas": 156215,
            "input": HexBytes(
                "0xfa461e3300000000000000000000000000000000000000000000010d10f01a7b1db0922dffffffffffffffffffffffffffffffffffffffffffffffffffffffff54e86a410000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000006041eb661e632bf0d55dfe02085b906a8a326fe309442573b563e0f0f2ed64720b00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000111111111117dc0aa78b770fa6a738034120c302"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14913, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0, 2],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 153200,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf90000000000000000000000009febc984504356225405e26833608b17719c82ae00000000000000000000000000000000000000000000010d10f01a7b1db0922d"
            ),
            "to": "0x111111111117dC0aa78b770fA6A738034120C302",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 14304,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 0],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9feBc984504356225405e26833608b17719c82Ae",
            "callType": "staticcall",
            "gas": 140902,
            "input": HexBytes(
                "0x70a082310000000000000000000000009febc984504356225405e26833608b17719c82ae"
            ),
            "to": "0x111111111117dC0aa78b770fA6A738034120C302",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 510,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000001f1f4f30f6c73df6c23e6"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 3],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 129794,
            "input": HexBytes("0x"),
            "to": "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5",
            "value": 1241303378070017,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0x7aa71de1165fd9ec3a8b959699727d95fe593a06d7eb6f5be08fa3d7415aa42f"
        ),
        "transactionPosition": 8,
        "type": "call",
    },
    {
        "action": {
            "from": "0xD21e14023e8d247e2Ac4C7aDfC1d25441E492278",
            "callType": "call",
            "gas": 30080,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000067ccb725b4a13e0c1f8e3a5e4efc758fe21f38af0000000000000000000000000000000000000000000000000000000018701a80"
            ),
            "to": "0x467719aD09025FcC6cF6F8311755809d45a5E5f3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12851,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7904630f15ed02f242085f15b35e46e67143e7dd149a4e7a52ffa955a2f85d99"
        ),
        "transactionPosition": 9,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0edE5Fe301B7f576306e6Fb71A6f6a68547De291",
            "callType": "call",
            "gas": 80256,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000003ce9bb52894e2d4bc3b659b4f7a35f7556cb9fdd000000000000000000000000000000000000000000000000000000003b9aca00"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x24036cd410f94faabb55cf432c6011e9f6e7c3d27617a1ea5c4071e407a05b92"
        ),
        "transactionPosition": 10,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4b121b149Fa9D07342cE43AEa89F3d1f75a107Da",
            "callType": "call",
            "gas": 80244,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000003ce9bb52894e2d4bc3b659b4f7a35f7556cb9fdd000000000000000000000000000000000000000000000000000000003489c51d"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2d56ca1e01c6a843884439032fb0e881b10e8c63607f72b8f0719bc6e5608dea"
        ),
        "transactionPosition": 11,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4BbEF72ed57B043e633121976Dc71B7c481FCA73",
            "callType": "call",
            "gas": 80232,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000003ce9bb52894e2d4bc3b659b4f7a35f7556cb9fdd00000000000000000000000000000000000000000000000000000002f96b422e"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7ad91e43ef805dff57fde8087fbc9e0b88b0bc7f8905254c968cc743c3cfdab9"
        ),
        "transactionPosition": 12,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA6807d794411D9a80bc435dfC4CDa0Ba0DddE979",
            "callType": "call",
            "gas": 236545,
            "input": HexBytes(
                "0x2e7a21ce000000000000000000000000b0f4a77bde7fee134265307c5cc19abff0ba409b0000000000000000000000000000000000000000000002d2baaac40963d00000000000000000000000000000000000000000000000000821c8e965ac1180000000000000000000000000000000000000000000000000081e5c08fa801380000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000003865c048cedf0"
            ),
            "to": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 106592, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "staticcall",
            "gas": 226825,
            "input": HexBytes("0x3850c7bd"),
            "to": "0xB0F4a77Bde7fEE134265307C5CC19abfF0ba409B",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2696,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000821c92eac2b21a64f19fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffb900600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "call",
            "gas": 221701,
            "input": HexBytes(
                "0x128acb0800000000000000000000000098c3d3183c4b8a650614ad179a1a98be0a8d6b8e00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000002d2baaac40963d0000000000000000000000000000000000000000000000000081e5c08fa801380000000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xB0F4a77Bde7fEE134265307C5CC19abfF0ba409B",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 85732,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000002d2baaac40963d00000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff462c6662"
            ),
        },
        "subtraces": 4,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB0F4a77Bde7fEE134265307C5CC19abfF0ba409B",
            "callType": "call",
            "gas": 185368,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000098c3d3183c4b8a650614ad179a1a98be0a8d6b8e00000000000000000000000000000000000000000000000000000000b9d3999e"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB0F4a77Bde7fEE134265307C5CC19abfF0ba409B",
            "callType": "staticcall",
            "gas": 158043,
            "input": HexBytes(
                "0x70a08231000000000000000000000000b0f4a77bde7fee134265307c5cc19abff0ba409b"
            ),
            "to": "0x3506424F91fD33084466F402d5D97f05F8e3b4AF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2679,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000003b39ba9e502b68f23ead4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB0F4a77Bde7fEE134265307C5CC19abfF0ba409B",
            "callType": "call",
            "gas": 154653,
            "input": HexBytes(
                "0xfa461e330000000000000000000000000000000000000000000002d2baaac40963d00000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff462c666200000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 16098, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "call",
            "gas": 150300,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000b0f4a77bde7fee134265307c5cc19abff0ba409b0000000000000000000000000000000000000000000002d2baaac40963d00000"
            ),
            "to": "0x3506424F91fD33084466F402d5D97f05F8e3b4AF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13599,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 0],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB0F4a77Bde7fEE134265307C5CC19abfF0ba409B",
            "callType": "staticcall",
            "gas": 138173,
            "input": HexBytes(
                "0x70a08231000000000000000000000000b0f4a77bde7fee134265307c5cc19abff0ba409b"
            ),
            "to": "0x3506424F91fD33084466F402d5D97f05F8e3b4AF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 679,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000003b66e648fc6bff2f3ead4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 3],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5",
            "value": 992154701590000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x1b46582c3a74483e15f3eb783af8535f482bc4564b94ec42052568641b55d6d3"
        ),
        "transactionPosition": 13,
        "type": "call",
    },
    {
        "action": {
            "from": "0x46340b20830761efd32832A74d7169B29FEB9758",
            "callType": "call",
            "gas": 328392,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000e9c353dcbc3bfc0429d63e22c042a46dacfe6a5300000000000000000000000000000000000000000000000000000000055d4a80"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x9f22bd44194f4149cea1d3ca9b180f973407b287e542beeecb9576e23879a294"
        ),
        "transactionPosition": 14,
        "type": "call",
    },
    {
        "action": {
            "from": "0x46340b20830761efd32832A74d7169B29FEB9758",
            "callType": "call",
            "gas": 328392,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000001cc25e012db2c60f6b35fe889eff58bf8d021e9600000000000000000000000000000000000000000000000000000000825182e0"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 44017,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x026e0528519b6ec3a9257f394c67f3bb4aa37b425bae9cbd7030c0fe4e997a9f"
        ),
        "transactionPosition": 15,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 316130,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000001cc25e012db2c60f6b35fe889eff58bf8d021e9600000000000000000000000000000000000000000000000000000000825182e0"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 36728,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x026e0528519b6ec3a9257f394c67f3bb4aa37b425bae9cbd7030c0fe4e997a9f"
        ),
        "transactionPosition": 15,
        "type": "call",
    },
    {
        "action": {
            "from": "0x46340b20830761efd32832A74d7169B29FEB9758",
            "callType": "call",
            "gas": 329000,
            "input": HexBytes("0x"),
            "to": "0xF26A1896377568742767A777C53357442Ebf9af1",
            "value": 900000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xbe0cd9c33f8c5285aabc7dbe705ae4b41598072ce541cb948c20eefadcd5d6c4"
        ),
        "transactionPosition": 16,
        "type": "call",
    },
    {
        "action": {
            "from": "0x46340b20830761efd32832A74d7169B29FEB9758",
            "callType": "call",
            "gas": 329000,
            "input": HexBytes("0x"),
            "to": "0x1E3a01AE80b3B7B8576AE26880D16fFA8d2d1FA4",
            "value": 7070000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xd455e7c376623ff7004818166cb7b52166d7c0439ae31c75aa53341fcd3b57d6"
        ),
        "transactionPosition": 17,
        "type": "call",
    },
    {
        "action": {
            "from": "0x8a2376824Dd78BBD73ae0646039E0f2D7d9eF561",
            "callType": "call",
            "gas": 138441,
            "input": HexBytes(
                "0x7ff36ab500000000000000000000000000000000000000001741d4bd0b135072c04c86480000000000000000000000000000000000000000000000000000000000000080000000000000000000000000398b7a15e6254b51f84f06673f7a93f06d1f9de200000000000000000000000000000000000000000000000000000000633410630000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000048878490702f1ba61ab02546f93fc92e04c36007"
            ),
            "to": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "value": 255464174780706438,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 120956,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000038b97503ea46e86000000000000000000000000000000000000000017426d2811f68424876f5923"
            ),
        },
        "subtraces": 4,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "staticcall",
            "gas": 131549,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x2430c43867EcAE58A4B2C2e41d08C916A062b700",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000e12a8b89c699adc80e044d8c40000000000000000000000000000000000000000000000021ff21fad56960d7e000000000000000000000000000000000000000000000000000000006333f42b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "call",
            "gas": 118557,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 255464174780706438,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 23974, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "call",
            "gas": 93746,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000002430c43867ecae58a4b2c2e41d08c916a062b700000000000000000000000000000000000000000000000000038b97503ea46e86"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "call",
            "gas": 83763,
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000017426d2811f68424876f59230000000000000000000000000000000000000000000000000000000000000000000000000000000000000000398b7a15e6254b51f84f06673f7a93f06d1f9de200000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x2430c43867EcAE58A4B2C2e41d08C916A062b700",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 67151, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2430c43867EcAE58A4B2C2e41d08C916A062b700",
            "callType": "call",
            "gas": 69289,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000398b7a15e6254b51f84f06673f7a93f06d1f9de2000000000000000000000000000000000000000017426d2811f68424876f5923"
            ),
            "to": "0x48878490702f1BA61aB02546F93fc92e04c36007",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 32260,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2430c43867EcAE58A4B2C2e41d08C916A062b700",
            "callType": "staticcall",
            "gas": 36912,
            "input": HexBytes(
                "0x70a082310000000000000000000000002430c43867ecae58a4b2c2e41d08c916a062b700"
            ),
            "to": "0x48878490702f1BA61aB02546F93fc92e04c36007",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000dfb664b7457a4585c58d57fa1"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2430c43867EcAE58A4B2C2e41d08C916A062b700",
            "callType": "staticcall",
            "gas": 35980,
            "input": HexBytes(
                "0x70a082310000000000000000000000002430c43867ecae58a4b2c2e41d08c916a062b700"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000002237db6fd953a7c04"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 2],
        "transactionHash": HexBytes(
            "0x7da753a1abc52d90449a075dc7753ef7fd8ed4504b36908e75570abd1ce73a06"
        ),
        "transactionPosition": 18,
        "type": "call",
    },
    {
        "action": {
            "from": "0x950C40afcECEd6911609D4f6Ae81a48749681452",
            "callType": "call",
            "gas": 285804,
            "input": HexBytes(
                "0x5eaa9cedee4fcdeed773931af0bcd16cfcea5b366682ffbd4994cf78b4f0a6a40b570340000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000004be00000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000001d8ce2c9c15fff000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000953706f745072696365000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000036f686d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000036574680000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 272740, "output": HexBytes("0x")},
        "subtraces": 6,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "callType": "call",
            "gas": 271215,
            "input": HexBytes(
                "0x699f200ffa522e460446113e8fd353d7fa015625a68bc0369712213a42e006346440891e"
            ),
            "to": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2466,
            "output": HexBytes(
                "0x000000000000000000000000e8218cacb0a5421bc6409e498d9f8cc8869945ea"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "callType": "staticcall",
            "gas": 265108,
            "input": HexBytes(
                "0x733bdef0000000000000000000000000950c40afceced6911609d4f6ae81a48749681452"
            ),
            "to": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 9759,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000062e10133"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "callType": "delegatecall",
            "gas": 256070,
            "input": HexBytes(
                "0x733bdef0000000000000000000000000950c40afceced6911609d4f6ae81a48749681452"
            ),
            "to": "0xf98624E9924CAA2cbD21cC6288215Ec2ef7cFE80",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 4741,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000062e10133"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "callType": "call",
            "gas": 254956,
            "input": HexBytes(
                "0xb59e14d45d9fadfc729fd027e395e5157ef1b53ef9fa4a8f053043c5f159307543e7cc97"
            ),
            "to": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2428,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000056bc75e2d63100000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "callType": "staticcall",
            "gas": 252084,
            "input": HexBytes(
                "0x70a08231000000000000000000000000950c40afceced6911609d4f6ae81a48749681452"
            ),
            "to": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8585,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000072faf9150e708553f"
            ),
        },
        "subtraces": 1,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "callType": "delegatecall",
            "gas": 247679,
            "input": HexBytes(
                "0x70a08231000000000000000000000000950c40afceced6911609d4f6ae81a48749681452"
            ),
            "to": "0xf98624E9924CAA2cbD21cC6288215Ec2ef7cFE80",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8070,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000072faf9150e708553f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "callType": "staticcall",
            "gas": 101988,
            "input": HexBytes(
                "0x70a08231000000000000000000000000e8218cacb0a5421bc6409e498d9f8cc8869945ea"
            ),
            "to": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8585,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000cd186b8a8676d039d9e"
            ),
        },
        "subtraces": 1,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "callType": "delegatecall",
            "gas": 99928,
            "input": HexBytes(
                "0x70a08231000000000000000000000000e8218cacb0a5421bc6409e498d9f8cc8869945ea"
            ),
            "to": "0xf98624E9924CAA2cbD21cC6288215Ec2ef7cFE80",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8070,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000cd186b8a8676d039d9e"
            ),
        },
        "subtraces": 0,
        "traceAddress": [4, 0],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
            "callType": "call",
            "gas": 90356,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000950c40afceced6911609d4f6ae81a487496814520000000000000000000000000000000000000000000000000b1a2bc2ec500000"
            ),
            "to": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 62631,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [5],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "callType": "delegatecall",
            "gas": 88475,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000950c40afceced6911609d4f6ae81a487496814520000000000000000000000000000000000000000000000000b1a2bc2ec500000"
            ),
            "to": "0xf98624E9924CAA2cbD21cC6288215Ec2ef7cFE80",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 62113,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [5, 0],
        "transactionHash": HexBytes(
            "0x6935c24a01508d4296c6d75809d66f8f55acc4916c7487ee984096baac7e4f72"
        ),
        "transactionPosition": 19,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0809616c35784DB5f758e0338e9d9B25A2fd1932",
            "callType": "call",
            "gas": 477472,
            "input": HexBytes(
                "0x355ec1520000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000045592c2b869be4ecc00000000000000000000000000000000000000000000000000000000255aca508000000000000000000000000000000000000000000000000000000000000002b514910771af9ca656af840dff83e8264ecf986ca000bb8a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000"
            ),
            "to": "0x000000000dFDe7deaF24138722987c9a6991e2D4",
            "value": 15630274,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 97062, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0x000000000dFDe7deaF24138722987c9a6991e2D4",
            "callType": "call",
            "gas": 462272,
            "input": HexBytes(
                "0x128acb08000000000000000000000000000000000dfde7deaf24138722987c9a6991e2d40000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000045592c2b869be4ecc000000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000002b514910771af9ca656af840dff83e8264ecf986ca000bb8a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000"
            ),
            "to": "0xFAD57d2039C21811C8F2B5D5B65308aa99D31559",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 88906,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000045592c2b869be4ecc0fffffffffffffffffffffffffffffffffffffffffffffffffffffffdaa364769"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFAD57d2039C21811C8F2B5D5B65308aa99D31559",
            "callType": "call",
            "gas": 420054,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000000000000dfde7deaf24138722987c9a6991e2d40000000000000000000000000000000000000000000000000000000255c9b897"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 26917,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 406359,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000000000000dfde7deaf24138722987c9a6991e2d40000000000000000000000000000000000000000000000000000000255c9b897"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 19628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFAD57d2039C21811C8F2B5D5B65308aa99D31559",
            "callType": "staticcall",
            "gas": 390225,
            "input": HexBytes(
                "0x70a08231000000000000000000000000fad57d2039c21811c8f2b5d5b65308aa99d31559"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2655,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000f7f92dd2a37ae8d7b4c"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFAD57d2039C21811C8F2B5D5B65308aa99D31559",
            "callType": "call",
            "gas": 386850,
            "input": HexBytes(
                "0xfa461e33000000000000000000000000000000000000000000000045592c2b869be4ecc0fffffffffffffffffffffffffffffffffffffffffffffffffffffffdaa3647690000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000002b514910771af9ca656af840dff83e8264ecf986ca000bb8a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000"
            ),
            "to": "0x000000000dFDe7deaF24138722987c9a6991e2D4",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14611, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 2],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0x000000000dFDe7deaF24138722987c9a6991e2D4",
            "callType": "call",
            "gas": 377802,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000fad57d2039c21811c8f2b5d5b65308aa99d31559000000000000000000000000000000000000000000000045592c2b869be4ecc0"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 11345,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFAD57d2039C21811C8F2B5D5B65308aa99D31559",
            "callType": "staticcall",
            "gas": 371834,
            "input": HexBytes(
                "0x70a08231000000000000000000000000fad57d2039c21811c8f2b5d5b65308aa99d31559"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 655,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000fc4ec0955be4a72680c"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 3],
        "transactionHash": HexBytes(
            "0x44348924e614dec6d93d35139ee2e7984fcda0f13d81a1b927e0f42b0c1b93f0"
        ),
        "transactionPosition": 20,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE1A612Fc97CCAa4c65Ea2f86eeC1974776343578",
            "callType": "call",
            "gas": 44000,
            "input": HexBytes("0x"),
            "to": "0xBf864026C2f50ADe50AC9C6a139724Bb72bFd14C",
            "value": 1136218530785000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa9ca435c275811c7b8b253ebb42590b309497a3d8285cb9789b35f6f212c56c0"
        ),
        "transactionPosition": 21,
        "type": "call",
    },
    {
        "action": {
            "from": "0x42d1542cFbE0392ad63bf681FcbE48a06804Dc62",
            "callType": "call",
            "gas": 278356,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000016b2e1230fe07a340d4e541bb55d025136d54b2f0000000000000000000000000000000000000000000000eb45995db1cb500000"
            ),
            "to": "0x0b38210ea11411557c13457D4dA7dC6ea731B88a",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12946,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x115923f7c2ac2e9dfde3ecad01b3c549e5274c8f5c2424b4c1d5f315265fc528"
        ),
        "transactionPosition": 22,
        "type": "call",
    },
    {
        "action": {
            "from": "0x19e4A1C4095c90800afE8DF09512E361755BC161",
            "callType": "call",
            "gas": 723148,
            "input": HexBytes(
                "0x7af5352f0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000000000000000000000000044f5dab062ba940000000000000000000000000000000000000000000000000000000a8e6a4f06326000000000000000000000000000000000000000000000000000000000000d59f800000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c90000000000000000000000000000000000000000000000128f61e352842811c00000000000000000000000000000000000000000000010002b299d7893ae80000000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea910000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e0000000000000000000000000000000000000000000010002b299d7893ae8000000000000000000000000000000000000000000000000012db2ca253583c1d000000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91"
            ),
            "to": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 250132, "output": HexBytes("0x")},
        "subtraces": 6,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "staticcall",
            "gas": 706444,
            "input": HexBytes(
                "0x70a082310000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91"
            ),
            "to": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2666,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000a1052abd79074f2d"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "staticcall",
            "gas": 693272,
            "input": HexBytes("0x0902f1ac"),
            "to": "0xD6c783B257E662CA949b441a4FcB08a53fc49914",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000003fbe4251744a378394e2a0000000000000000000000000000000000000000000004c86e68e0c2fc7608c6000000000000000000000000000000000000000000000000000000006333ec4b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "staticcall",
            "gas": 685775,
            "input": HexBytes("0x0902f1ac"),
            "to": "0xcB0bC7C879bb3E9CFEB9d8EFef653F33B3d242e9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2470,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000ec90113cc16446f57ea0f9000000000000000000000000000000000000000000011181d0ded8cc0fab8b37000000000000000000000000000000000000000000000000000000006333f44f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "call",
            "gas": 678276,
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000002600000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c90000000000000000000000000000000000000000000000128f27a8dfa6c87379000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f0000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea910000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f000000000000000000000000000000000000000000000012db2ca253583c1d000000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91"
            ),
            "to": "0xcB0bC7C879bb3E9CFEB9d8EFef653F33B3d242e9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 204115, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xcB0bC7C879bb3E9CFEB9d8EFef653F33B3d242e9",
            "callType": "call",
            "gas": 652238,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f"
            ),
            "to": "0x579CEa1889991f68aCc35Ff5c3dd0621fF29b0C9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30046,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xcB0bC7C879bb3E9CFEB9d8EFef653F33B3d242e9",
            "callType": "call",
            "gas": 621639,
            "input": HexBytes(
                "0x10d1e85c0000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000002600000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c90000000000000000000000000000000000000000000000128f27a8dfa6c87379000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f0000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea910000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f000000000000000000000000000000000000000000000012db2ca253583c1d000000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91"
            ),
            "to": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 68322,
            "output": HexBytes(
                "0x10d1e85c0000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000002600000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c90000000000000000000000000000000000000000000000128f27a8dfa6c87379000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f0000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea910000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914000000000000000000000000579cea1889991f68acc35ff5c3dd0621ff29b0c9000000000000000000000000853d955acef822db058eb8505911ed77f175b99e000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f000000000000000000000000000000000000000000000012db2ca253583c1d000000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91"
            ),
        },
        "subtraces": 3,
        "traceAddress": [3, 1],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "call",
            "gas": 607207,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914000000000000000000000000000000000000000000000ffff9cf90b1a26c9f1f"
            ),
            "to": "0x579CEa1889991f68aCc35Ff5c3dd0621fF29b0C9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8146,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1, 0],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "call",
            "gas": 597491,
            "input": HexBytes(
                "0x022c0d9f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000012db2ca253583c1d000000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea9100000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xD6c783B257E662CA949b441a4FcB08a53fc49914",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 43646, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [3, 1, 1],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xD6c783B257E662CA949b441a4FcB08a53fc49914",
            "callType": "call",
            "gas": 577420,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91000000000000000000000000000000000000000000000012db2ca253583c1d00"
            ),
            "to": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 11123,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1, 1, 0],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xD6c783B257E662CA949b441a4FcB08a53fc49914",
            "callType": "staticcall",
            "gas": 565869,
            "input": HexBytes(
                "0x70a08231000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914"
            ),
            "to": "0x579CEa1889991f68aCc35Ff5c3dd0621fF29b0C9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000040be41ee6d5551aa5ed49"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1, 1, 1],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xD6c783B257E662CA949b441a4FcB08a53fc49914",
            "callType": "staticcall",
            "gas": 564938,
            "input": HexBytes(
                "0x70a08231000000000000000000000000d6c783b257e662ca949b441a4fcb08a53fc49914"
            ),
            "to": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 666,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000004b5933c3e6fa439ebc6"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1, 1, 2],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "call",
            "gas": 553574,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e90000000000000000000000000000000000000000000000128f27a8dfa6c87379"
            ),
            "to": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8323,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1, 2],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xcB0bC7C879bb3E9CFEB9d8EFef653F33B3d242e9",
            "callType": "staticcall",
            "gas": 554061,
            "input": HexBytes(
                "0x70a08231000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e9"
            ),
            "to": "0x579CEa1889991f68aCc35Ff5c3dd0621fF29b0C9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000ec801142f1d3955312035f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 2],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0xcB0bC7C879bb3E9CFEB9d8EFef653F33B3d242e9",
            "callType": "staticcall",
            "gas": 553006,
            "input": HexBytes(
                "0x70a08231000000000000000000000000cb0bc7c879bb3e9cfeb9d8efef653f33b3d242e9"
            ),
            "to": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 666,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000011194600681abb673fecb"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 3],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "staticcall",
            "gas": 476472,
            "input": HexBytes(
                "0x70a082310000000000000000000000000352086e5ce73fc2ec4c41fef56361f7def6ea91"
            ),
            "to": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 666,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000ed0a24312a7af8b4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0352086e5Ce73fc2eC4C41fef56361F7dEF6Ea91",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5",
            "value": 1167926018433314,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [5],
        "transactionHash": HexBytes(
            "0x96cca7a715699d94646169b9be9e40b8ec08dd09258fdde7b9fd65413d000282"
        ),
        "transactionPosition": 23,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7BEB799366052d6dc32D774617dfB8C455D3b173",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x54D7eD95a8cd1282b14a2C843b146CeF93e0AFd6",
            "value": 31124609545948299,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x786c4a7a2bc4393c10859e181e0b89bfd794e1a44e45dcea3650f1049cfdc79b"
        ),
        "transactionPosition": 24,
        "type": "call",
    },
    {
        "action": {
            "from": "0x8e8f818d3371F797A2Db7eDB32803607c8b3c6A9",
            "callType": "call",
            "gas": 231369,
            "input": HexBytes(
                "0x2e7a21ce000000000000000000000000ff29d3e552155180809ea3a877408a46200580860000000000000000000000000000000000000000000000ecbc4ca2a472dc000000000000000000000000000000000000000000000000059c675993e79ec0000000000000000000000000000000000000000000000000059137495acc4b400000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000029ae7fcfef700"
            ),
            "to": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 93629, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "staticcall",
            "gas": 221730,
            "input": HexBytes("0x3850c7bd"),
            "to": "0xFf29D3E552155180809ea3A877408A4620058086",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2696,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000059c6a283eaf05b7cb0afffffffffffffffffffffffffffffffffffffffffffffffffffffffffffb7309000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000004c000000000000000000000000000000000000000000000000000000000000004c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "call",
            "gas": 216606,
            "input": HexBytes(
                "0x128acb0800000000000000000000000098c3d3183c4b8a650614ad179a1a98be0a8d6b8e00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000ecbc4ca2a472dc000000000000000000000000000000000000000000000000059137495acc4b40000000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xFf29D3E552155180809ea3A877408A4620058086",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 72769,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000ecbc4ca2a472dc0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffe3330796"
            ),
        },
        "subtraces": 4,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFf29D3E552155180809ea3A877408A4620058086",
            "callType": "call",
            "gas": 180791,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000098c3d3183c4b8a650614ad179a1a98be0a8d6b8e000000000000000000000000000000000000000000000000000000001cccf86a"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFf29D3E552155180809ea3A877408A4620058086",
            "callType": "staticcall",
            "gas": 163309,
            "input": HexBytes(
                "0x70a08231000000000000000000000000ff29d3e552155180809ea3a877408a4620058086"
            ),
            "to": "0x940a2dB1B7008B6C776d4faaCa729d6d4A4AA551",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2591,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000c64da1376a54df96570f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFf29D3E552155180809ea3A877408A4620058086",
            "callType": "call",
            "gas": 160006,
            "input": HexBytes(
                "0xfa461e330000000000000000000000000000000000000000000000ecbc4ca2a472dc0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffe333079600000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 13756, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "call",
            "gas": 155569,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000ff29d3e552155180809ea3a877408a46200580860000000000000000000000000000000000000000000000ecbc4ca2a472dc0000"
            ),
            "to": "0x940a2dB1B7008B6C776d4faaCa729d6d4A4AA551",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 11257,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 0],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFf29D3E552155180809ea3A877408A4620058086",
            "callType": "staticcall",
            "gas": 145832,
            "input": HexBytes(
                "0x70a08231000000000000000000000000ff29d3e552155180809ea3a877408a4620058086"
            ),
            "to": "0x940a2dB1B7008B6C776d4faaCa729d6d4A4AA551",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 591,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000c73a5d840cf95272570f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 3],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5",
            "value": 733271126112000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xc1ae5ff001e58d2090cb3e21686172064f481229594bccef528c8a7787852b85"
        ),
        "transactionPosition": 25,
        "type": "call",
    },
    {
        "action": {
            "from": "0x000F422887eA7d370FF31173FD3B46c8F66A5B1c",
            "callType": "call",
            "gas": 29000,
            "input": HexBytes("0x"),
            "to": "0x5a2337c1eF439CFdB7347F509B1F0e55AaE20414",
            "value": 35896069711583952,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x03d1ad74410f3ec5b02abdd9fa4eb2f27510bc0739a88c406b989e5944d73fd7"
        ),
        "transactionPosition": 26,
        "type": "call",
    },
    {
        "action": {
            "from": "0x96B5Ea9aCF9C45fc9898291911fEE702f5CA261E",
            "callType": "call",
            "gas": 9000,
            "input": HexBytes("0x"),
            "to": "0x96B5Ea9aCF9C45fc9898291911fEE702f5CA261E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xd01a08701962a549fe8688b8808269ed28bcb1be5c7f28a26ac868fa2e543344"
        ),
        "transactionPosition": 27,
        "type": "call",
    },
    {
        "action": {
            "from": "0xd5cf0Cb9a8DF9B46f077f561d8b76c34A69bD82F",
            "callType": "call",
            "gas": 477028,
            "input": HexBytes(
                "0x11f6bff20000000000000000000000000000000000000000000000000302aa7766ef80fc000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000007e6782e37278994d1e99f1a5d03309b4b249d919000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000031c2ab99605e535e96097188bc79752e1b3e581700000000000000000000000000000000000000000000003d353cdc1e89880000"
            ),
            "to": "0x585C3d4Da9b533C7e3dF8AC7356C882859298cEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 93935, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x585C3d4Da9b533C7e3dF8AC7356C882859298cEe",
            "callType": "staticcall",
            "gas": 461557,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x7E6782E37278994d1e99f1a5d03309B4b249d919",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2517,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000001b97cca471f0670000000000000000000000000000000000000000000000023c1a01f74d951a73662000000000000000000000000000000000000000000000000000000006331d087"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x585C3d4Da9b533C7e3dF8AC7356C882859298cEe",
            "callType": "call",
            "gas": 455157,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000007e6782e37278994d1e99f1a5d03309b4b249d9190000000000000000000000000000000000000000000000000302aa7766ef80fc"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12862,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x585C3d4Da9b533C7e3dF8AC7356C882859298cEe",
            "callType": "call",
            "gas": 441655,
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003dcf2c3279fc533bde00000000000000000000000031c2ab99605e535e96097188bc79752e1b3e581700000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x7E6782E37278994d1e99f1a5d03309B4b249d919",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 65500, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7E6782E37278994d1e99f1a5d03309B4b249d919",
            "callType": "call",
            "gas": 421451,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000031c2ab99605e535e96097188bc79752e1b3e581700000000000000000000000000000000000000000000003dcf2c3279fc533bde"
            ),
            "to": "0xeEAA40B28A2d1b0B08f6f97bB1DD4B75316c6107",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30185,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 0],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7E6782E37278994d1e99f1a5d03309B4b249d919",
            "callType": "staticcall",
            "gas": 391118,
            "input": HexBytes(
                "0x70a082310000000000000000000000007e6782e37278994d1e99f1a5d03309b4b249d919"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000001bc7f74be85f5f0fc"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 1],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7E6782E37278994d1e99f1a5d03309B4b249d919",
            "callType": "staticcall",
            "gas": 390169,
            "input": HexBytes(
                "0x70a082310000000000000000000000007e6782e37278994d1e99f1a5d03309b4b249d919"
            ),
            "to": "0xeEAA40B28A2d1b0B08f6f97bB1DD4B75316c6107",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 585,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000002383d0f3425f5553fa84"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 2],
        "transactionHash": HexBytes(
            "0x1bfd4d5ff57aa8a53dd33874ab86fda8f2116d9176e465aa03c1b4aa664a31eb"
        ),
        "transactionPosition": 28,
        "type": "call",
    },
    {
        "action": {
            "from": "0x392027fDc620d397cA27F0c1C3dCB592F27A4dc3",
            "callType": "call",
            "gas": 16846,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000d7fb6add631c1a8c897fa8b92e2f349789539a60000000000000000000000000000000000000000000000045af756742af316858"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13345,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x23e0c28a9b9aac51dcde3800f62f204697372e83e07de431c42bb84d4ac1270e"
        ),
        "transactionPosition": 29,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFd54078bAdD5653571726C3370AfB127351a6f26",
            "callType": "call",
            "gas": 69000,
            "input": HexBytes("0x"),
            "to": "0x70108219110dCCC337B9Ac90f6Db612ab1AE91B4",
            "value": 1266669401104800,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7b8604005b12dc2df0399229cf67c42c8e6fcaed43e041b144a14addc5016603"
        ),
        "transactionPosition": 30,
        "type": "call",
    },
    {
        "action": {
            "from": "0xdB0E89a9B003A28A4055ef772E345E8089987bfd",
            "callType": "call",
            "gas": 69000,
            "input": HexBytes("0x"),
            "to": "0xBe83E7Db6C6fb4F5DB4F22294FAF3868Ca443F2B",
            "value": 41617733000800,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1a5dcfb543029f5d549f78cd215208f8297b5ba9c618e4835555f24eaf6a97ed"
        ),
        "transactionPosition": 31,
        "type": "call",
    },
    {
        "action": {
            "from": "0xf2c758db6EF6DDC43CFb0bA2db73ce8Baf21a6e3",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x595063172C85B1e8AC2fe74Fcb6b7dC26844CC2D",
            "value": 2228410000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x27bc92882541be215a93a9d32b7b0dcab330f5a6d17769e33a5a07aba9f2d0bd"
        ),
        "transactionPosition": 32,
        "type": "call",
    },
    {
        "action": {
            "from": "0xf363119ea245Ef9BCba0a0aDDB73245D46c60960",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x595063172C85B1e8AC2fe74Fcb6b7dC26844CC2D",
            "value": 1234330035000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x9bf0c37de713bf58a538605ca5eba0d0f8f647c09922fd5d4f7e2f6b1410ea23"
        ),
        "transactionPosition": 33,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7f2328BF075C94EE27029aA0051F05AE2f6a4468",
            "callType": "call",
            "gas": 142563,
            "input": HexBytes(
                "0x7ff36ab500000000000000000000000000000000000000000017c656433967b7ac4c555e00000000000000000000000000000000000000000000000000000000000000800000000000000000000000007f2328bf075c94ee27029aa0051f05ae2f6a4468000000000000000000000000000000000000000000000000000000006333fb3f0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000135783b60cf5d71daff7a377f9eb7db8d2deab9e"
            ),
            "to": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "value": 19365266496712552,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 135063,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000044cc9b76846f680000000000000000000000000000000000000000001903d9c752d12325d2ebdd"
            ),
        },
        "subtraces": 4,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "staticcall",
            "gas": 135607,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x4f4d050d5C86dD32D276a8D066fA1932EB241c1b",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000c4835c0f884e25302ba0d4d60000000000000000000000000000000000000000000000021a956a29d6c079f0000000000000000000000000000000000000000000000000000000006333f44f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "call",
            "gas": 122615,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 19365266496712552,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 23974, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "call",
            "gas": 97804,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000004f4d050d5c86dd32d276a8d066fa1932eb241c1b0000000000000000000000000000000000000000000000000044cc9b76846f68"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "callType": "call",
            "gas": 87821,
            "input": HexBytes(
                "0x022c0d9f0000000000000000000000000000000000000000001903d9c752d12325d2ebdd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000007f2328bf075c94ee27029aa0051f05ae2f6a446800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x4f4d050d5C86dD32D276a8D066fA1932EB241c1b",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 81258, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4f4d050d5C86dD32D276a8D066fA1932EB241c1b",
            "callType": "call",
            "gas": 73283,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000007f2328bf075c94ee27029aa0051f05ae2f6a44680000000000000000000000000000000000000000001903d9c752d12325d2ebdd"
            ),
            "to": "0x135783B60cf5d71DAFF7a377f9eb7dB8D2dEAb9e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 46015,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4f4d050d5C86dD32D276a8D066fA1932EB241c1b",
            "callType": "staticcall",
            "gas": 27366,
            "input": HexBytes(
                "0x70a082310000000000000000000000004f4d050d5c86dd32d276a8d066fa1932eb241c1b"
            ),
            "to": "0x135783B60cf5d71DAFF7a377f9eb7dB8D2dEAb9e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 886,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000c46a5835c0fb540d05cde8f9"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 1],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4f4d050d5C86dD32D276a8D066fA1932EB241c1b",
            "callType": "staticcall",
            "gas": 26088,
            "input": HexBytes(
                "0x70a082310000000000000000000000004f4d050d5c86dd32d276a8d066fa1932eb241c1b"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000021ada36c54d44e958"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 2],
        "transactionHash": HexBytes(
            "0xa08f2afe43351449e3a45e9ee9c823ccb9eafbf048634a9888675f6dc81349df"
        ),
        "transactionPosition": 34,
        "type": "call",
    },
    {
        "action": {
            "from": "0x33030E58c1Ceb9b9d3EE8A0b2A248674C9cB17c7",
            "callType": "call",
            "gas": 118862,
            "input": HexBytes(
                "0xa0712d6800000000000000000000000000000000000000000000000000000000000000c9"
            ),
            "to": "0xcb6B570B8AeAbE38B449Aff31f901B8E1B91e396",
            "value": 253000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "error": "Reverted",
        "result": {
            "gasUsed": 30842,
            "output": HexBytes(
                "0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001c4552433732313a20746f6b656e20616c7265616479206d696e74656400000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6450d56ae3625b1a2033ab80bab1d64b836e7d29b5ff3eb767c9bd99c428ebb5"
        ),
        "transactionPosition": 35,
        "type": "call",
    },
    {
        "action": {
            "from": "0xf16E9B0D03470827A95CDfd0Cb8a8A3b46969B91",
            "callType": "call",
            "gas": 78356,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000013bf71c7cfb27eeea495e7b6b3908a454c407a8000000000000000000000000000000000000000000000002623de13f9a1a60000"
            ),
            "to": "0xa8c8CfB141A3bB59FEA1E2ea6B79b5ECBCD7b6ca",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 17770,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1c50f2c97fc372bb0abd48e60a5e67325238dc060e0615f8687b884689684d38"
        ),
        "transactionPosition": 36,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d",
            "callType": "call",
            "gas": 185472,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000007c9e3ec1a3cd5eea12f58ecb8628aa0b833cbe3d0000000000000000000000000000000000000000000001b176ca936057700000"
            ),
            "to": "0xdeFA4e8a7bcBA345F687a2f1456F5Edd9CE97202",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 20107,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xb85966637dbaf8ccbbde674ec7e0619149e6ae2b634e0d5d65034acf668ce98a"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0xdeFA4e8a7bcBA345F687a2f1456F5Edd9CE97202",
            "callType": "delegatecall",
            "gas": 175482,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000007c9e3ec1a3cd5eea12f58ecb8628aa0b833cbe3d0000000000000000000000000000000000000000000001b176ca936057700000"
            ),
            "to": "0xe5E8E834086F1a964f9A089eB6Ae11796862e4CE",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12861,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xb85966637dbaf8ccbbde674ec7e0619149e6ae2b634e0d5d65034acf668ce98a"
        ),
        "transactionPosition": 37,
        "type": "call",
    },
    {
        "action": {
            "from": "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
            "callType": "call",
            "gas": 185472,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000985bf21e4071c77df0c5279c35ac767c58266fe1000000000000000000000000000000000000000000000008f5a4b1700f45f000"
            ),
            "to": "0x3845badAde8e6dFF049820680d1F14bD3903a5d0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12580,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x0f7abee5077bf4aeac14a55c12c7df7a043d9700cc57761b344c2365b28b6d2c"
        ),
        "transactionPosition": 38,
        "type": "call",
    },
    {
        "action": {
            "from": "0x28C6c06298d514Db089934071355E5743bf21d60",
            "callType": "call",
            "gas": 185472,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f22c97a596e29b16c1c09dec88a17a40bbd5b49e00000000000000000000000000000000000000000000011f4adcf0767be90000"
            ),
            "to": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30445,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x40c38fceedcd1b03ce32979fb9f4175fb3aa95d6d5bb119d684e2d88e62cf094"
        ),
        "transactionPosition": 39,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9696f59E4d72E237BE84fFD425DCaD154Bf96976",
            "callType": "call",
            "gas": 185532,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f43cc69028290cac643acda26447e0438a4a2439000000000000000000000000000000000000000000000000000000004153a200"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6a6c52cc60b4ea3ce990bd2bec1943dfe2950c3f3be52d3ac7e1e71a44ed92a3"
        ),
        "transactionPosition": 40,
        "type": "call",
    },
    {
        "action": {
            "from": "0x6f6fF053e3B2B9b5403bca233D8a7Ce8484056f9",
            "callType": "call",
            "gas": 32271,
            "input": HexBytes(
                "0xfd9f1e100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000006f6ff053e3b2b9b5403bca233d8a7ce8484056f9000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000002200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333dfda000000000000000000000000000000000000000000000000000000006335a1da0000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000e3566a0fef0c02070000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000f13f29330dca76be26a6c7e268da836aef978e110000000000000000000000000000000000000000000000000000000000000172000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000066b214cb09e4000000000000000000000000000000000000000000000000000066b214cb09e40000000000000000000000000006f6ff053e3b2b9b5403bca233d8a7ce8484056f9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c68af0bb14000000000000000000000000000000000000000000000000000002c68af0bb140000000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000058d15e176280000000000000000000000000000000000000000000000000000058d15e1762800000000000000000000000000092c39077bf09cb8149b0222a27785f724ec3d27f"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 32271,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xeee941aaa821ed7b70144ad564c2c98bcb2a8e1e2181513a6d5bc653e81e0259"
        ),
        "transactionPosition": 41,
        "type": "call",
    },
    {
        "action": {
            "from": "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
            "callType": "call",
            "gas": 186128,
            "input": HexBytes("0x"),
            "to": "0xFC74E21DD6869B1A503B2e8a617708a5B131ACDd",
            "value": 14533160000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x26eee3ca714b8e19ef6a4b385205d7dd1a5df344f2e34cf232d1eae7cb751857"
        ),
        "transactionPosition": 42,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d",
            "callType": "call",
            "gas": 185508,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000002181cc46014d5454e5a00aa76f4a4e4c87afd48f000000000000000000000000000000000000000000000000000000037e5f5f5b"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xfe0c93f002b5fb58804d65bcc9872ebf0324748d62c336a32897c9b5ec12aec3"
        ),
        "transactionPosition": 43,
        "type": "call",
    },
    {
        "action": {
            "from": "0x28C6c06298d514Db089934071355E5743bf21d60",
            "callType": "call",
            "gas": 185520,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000006f433ab671281533ad8d5d0a84de89ac7c64aae2000000000000000000000000000000000000000000000000000000001017df80"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xcbbc531dfdc6414a5a25934ce98e99b58bc94667bca379678f727a08f906d653"
        ),
        "transactionPosition": 44,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4976A4A02f38326660D17bf34b431dC6e2eb2327",
            "callType": "call",
            "gas": 186128,
            "input": HexBytes("0x"),
            "to": "0xF74B5172bE54e9f2f6BFFF064d018232F711bAE2",
            "value": 1253099010000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x44fea50e87ce67241229764d98c575bc45591a476e7b63cb4d90cd0bfead6f0d"
        ),
        "transactionPosition": 45,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9696f59E4d72E237BE84fFD425DCaD154Bf96976",
            "callType": "call",
            "gas": 186128,
            "input": HexBytes("0x"),
            "to": "0xdbb36ee008FA0C6e6836989438c2B7C968fCF06d",
            "value": 93445500000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x43fd9fbe65bf1ed170514d3ac991c9ce572013cae49f788062dcbabca9b1db51"
        ),
        "transactionPosition": 46,
        "type": "call",
    },
    {
        "action": {
            "from": "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
            "callType": "call",
            "gas": 185532,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c6c2c79d29630643e2589f0f7de7bba99f34d4970000000000000000000000000000000000000000000000000000000005aca300"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xefc24ceb70523ebc5dc119060a22210c6637ded58f15766fdde2677bb7a2de66"
        ),
        "transactionPosition": 47,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d",
            "callType": "call",
            "gas": 186128,
            "input": HexBytes("0x"),
            "to": "0x81f6E9966F3786970927d5B847c68A9830CB14fE",
            "value": 499040000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x7e815928c663b393494c33d16e2f894f90635aa23ed2fb1c665699eadc4a9884"
        ),
        "transactionPosition": 48,
        "type": "call",
    },
    {
        "action": {
            "from": "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
            "callType": "call",
            "gas": 185520,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000fedc8c9f518ab32212bed05081ac2be860cc2ae70000000000000000000000000000000000000000000000000000000042d11a40"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x9a8c4f892501af624e016a637e1721a30d43556ae87f899d39229ecf2008bedf"
        ),
        "transactionPosition": 49,
        "type": "call",
    },
    {
        "action": {
            "from": "0x28C6c06298d514Db089934071355E5743bf21d60",
            "callType": "call",
            "gas": 186128,
            "input": HexBytes("0x"),
            "to": "0xFCf820d0847E485d9d858234b1E8E48542E9bCf8",
            "value": 374026950000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xe442135f00989923b0ea29109a72623e7d8adf8fce34412abab1d34144dfb4e6"
        ),
        "transactionPosition": 50,
        "type": "call",
    },
    {
        "action": {
            "from": "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
            "callType": "call",
            "gas": 186128,
            "input": HexBytes("0x"),
            "to": "0x9F6a0ea6938f4797861556Dbd65444765BeDF95f",
            "value": 435757510000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x65991660a702fa60c4480f2170a30d50a5bdb9e26069677916179e5a5adbdad0"
        ),
        "transactionPosition": 51,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB8bfA0945B50f8704A6a53DFeB39462CE536e043",
            "callType": "call",
            "gas": 48380,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000b12739d65f4f02c9f5e628e1a26fd5014f1aaef3000000000000000000000000000000000000000000000000000000011d20b4d0"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x3584a9ad3d5cd88ba7bbb1ab5b33ea3b5221a4d73ae536ee39708410fd9c31d8"
        ),
        "transactionPosition": 52,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9430801EBAf509Ad49202aaBC5F5Bc6fd8A3dAf8",
            "callType": "call",
            "gas": 21000,
            "input": HexBytes("0x"),
            "to": "0x7f36c020f878AC4c08E142625DD8d44B418D4CCe",
            "value": 20000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xcc09909856ce2eae7d5c3d81d7d7409daa3df331956cc2168ad9cde80e567ad9"
        ),
        "transactionPosition": 53,
        "type": "call",
    },
    {
        "action": {
            "from": "0xaaD69e7B638205f2f1E3dc563BCC91D4b18d9284",
            "callType": "call",
            "gas": 223160,
            "input": HexBytes(
                "0x5cf5402600000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000001b6ea1d2adadd700000000000000000000000017ef75aa22dd5f6c2763b8304ab24f40ee54d48a000000000000000000000000000000000000000000000000000046ef8897bbf00000000000000000000000000000000000000000000000000000000000000128d9627aa40000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000001b6ea1d2adadd700000000000000000000000000000000000000000000004d85081e7c27870c1900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000017ef75aa22dd5f6c2763b8304ab24f40ee54d48a869584cd000000000000000000000000be5998d3d0e9409474ef18abc30436574604b0c500000000000000000000000000000000000000000000006eeddaaaf96333f452000000000000000000000000000000000000000000000000"
            ),
            "to": "0xe66B31678d6C16E9ebf358268a790B763C133750",
            "value": 7799460277348807,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 140343,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000004feacbab4dd993243a"
            ),
        },
        "subtraces": 4,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe66B31678d6C16E9ebf358268a790B763C133750",
            "callType": "call",
            "gas": 207549,
            "input": HexBytes("0x"),
            "to": "0x382fFCe2287252F930E1C8DC9328dac5BF282bA1",
            "value": 77994602773488,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe66B31678d6C16E9ebf358268a790B763C133750",
            "callType": "call",
            "gas": 195816,
            "input": HexBytes(
                "0xd9627aa40000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000001b6ea1d2adadd700000000000000000000000000000000000000000000004d85081e7c27870c1900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000017ef75aa22dd5f6c2763b8304ab24f40ee54d48a869584cd000000000000000000000000be5998d3d0e9409474ef18abc30436574604b0c500000000000000000000000000000000000000000000006eeddaaaf96333f452"
            ),
            "to": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
            "value": 7721465674575319,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 104912,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000004feacbab4dd993243a"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
            "callType": "delegatecall",
            "gas": 187266,
            "input": HexBytes(
                "0xd9627aa40000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000001b6ea1d2adadd700000000000000000000000000000000000000000000004d85081e7c27870c1900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000017ef75aa22dd5f6c2763b8304ab24f40ee54d48a869584cd000000000000000000000000be5998d3d0e9409474ef18abc30436574604b0c500000000000000000000000000000000000000000000006eeddaaaf96333f452"
            ),
            "to": "0xf9b30557AfcF76eA82C04015D80057Fa2147Dfa9",
            "value": 7721465674575319,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 99158,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000004feacbab4dd993243a"
            ),
        },
        "subtraces": 4,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
            "callType": "call",
            "gas": 173481,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 7721465674575319,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 6874, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 0],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
            "callType": "call",
            "gas": 166520,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000ee9b50b74a132912cf55e7699ef3aa7ae2b00e0c000000000000000000000000000000000000000000000000001b6ea1d2adadd7"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
            "callType": "staticcall",
            "gas": 155948,
            "input": HexBytes("0x0902f1ac"),
            "to": "0xee9b50B74A132912cf55e7699Ef3Aa7aE2b00E0C",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000227138af4348284e2a500000000000000000000000000000000000000000000000000bae2583d6d60e90000000000000000000000000000000000000000000000000000000006333f413"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 2],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
            "callType": "call",
            "gas": 152998,
            "input": HexBytes(
                "0x022c0d9f00000000000000000000000000000000000000000000004feacbab4dd993243a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e66b31678d6c16e9ebf358268a790b763c13375000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xee9b50B74A132912cf55e7699Ef3Aa7aE2b00E0C",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 67085, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1, 0, 3],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xee9b50B74A132912cf55e7699Ef3Aa7aE2b00E0C",
            "callType": "call",
            "gas": 137442,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000e66b31678d6c16e9ebf358268a790b763c13375000000000000000000000000000000000000000000000004feacbab4dd993243a"
            ),
            "to": "0x17EF75AA22dD5f6C2763b8304Ab24f40eE54D48a",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 32260,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 3, 0],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xee9b50B74A132912cf55e7699Ef3Aa7aE2b00E0C",
            "callType": "staticcall",
            "gas": 105065,
            "input": HexBytes(
                "0x70a08231000000000000000000000000ee9b50b74a132912cf55e7699ef3aa7ae2b00e0c"
            ),
            "to": "0x17EF75AA22dD5f6C2763b8304Ab24f40eE54D48a",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 468,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000022214de397fa4ebb0616"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 3, 1],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xee9b50B74A132912cf55e7699Ef3Aa7aE2b00E0C",
            "callType": "staticcall",
            "gas": 104199,
            "input": HexBytes(
                "0x70a08231000000000000000000000000ee9b50b74a132912cf55e7699ef3aa7ae2b00e0c"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000bc99425a983bc67"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 3, 2],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe66B31678d6C16E9ebf358268a790B763C133750",
            "callType": "staticcall",
            "gas": 91978,
            "input": HexBytes(
                "0x70a08231000000000000000000000000e66b31678d6c16e9ebf358268a790b763c133750"
            ),
            "to": "0x17EF75AA22dD5f6C2763b8304Ab24f40eE54D48a",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 468,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000004feacbab4dd993243a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe66B31678d6C16E9ebf358268a790B763C133750",
            "callType": "call",
            "gas": 90270,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000aad69e7b638205f2f1e3dc563bcc91d4b18d928400000000000000000000000000000000000000000000004feacbab4dd993243a"
            ),
            "to": "0x17EF75AA22dD5f6C2763b8304Ab24f40eE54D48a",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8360,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x4800c6b73f11809fad7a7e26176b1da773af4048a924d2433db9d15e7c94d08d"
        ),
        "transactionPosition": 54,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa20E41dD2340E1d738A6555bfaF2f856f4A25637",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x4202a383E8834695d5d6Ccf95Ec010eaA99Ebc1a",
            "value": 1559892055469761500,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x01e1313588dbb6ca10ad1842229e04b3f023cdcc40c02541bb3f6e621f5d1399"
        ),
        "transactionPosition": 55,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC298Bf0C5dcF8AB55eE568FfBe8b503Da7114675",
            "callType": "call",
            "gas": 418033,
            "input": HexBytes(
                "0x7c025200000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000180000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da71146750000000000000000000000000000000000000000000000001d6978c44b2528e0000000000000000000000000000000000000000000000000000000009efb83660000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000dc0c2d6d529883fcacb870d5a8b12dd737459eed4776d18198b0c09094b6511c754bdb8b88b24ea1650f8e68d682822c8badb4259c731807321bc1be3c15c5d2a6e00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000008600000000000000000000000000000000000000000000000000000000000000b4080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a4b757fed600000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000002dc6c0288931fa76d7b0482f0fd0bca9a50bf0d22b9fef0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000604df92bd0800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000500000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000005600000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001408000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000064eb5625d9000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af9000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000800000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af90000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000002841e9a2e9200000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e4010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000a0969e970000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f4cf0000000000000000000000000000000000000000000000000000018382f200d00267616e64616c6674686562726f776e67786d786e690014248b18d01be8000000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000416751eb6bb914a1aaf5dd5f8ce8a17f0214f7cab8536359c5429b91c5251169173ad587504ef1ff24550c3def4cfb352a62d926f4a5187431be1612a4b9f4b6501b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002800000000000000000000000000000000000000000000000000000000000004480000000000000000000000000000000000000000000000000000000000001040000000000000000000000000000000000000000000000000000000000000064ec77bbdb000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000000000320000000000000000000000000000003200000000000000000000000000000000000000000000000000000000a09be57f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000024432ce0a7c00000000000000000000000000000000000000000000000000000000000000808000000000000000000000000000000000000000000000000000000000000044000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a405971224000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000010000000000000000000000000000000100000000000000000000000000000000000000000000000000000000007a229500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004470bdb947000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a0969e960000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000016414284aab00000000000000000000000000000000000000000000000000000000000000808000000000000000000000000000000000000000000000000000000000000024000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000000000000100000000000000000000000000000001000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000044a9059cbb0000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e26b9977"
            ),
            "to": "0x1111111254fb6c44bAC0beD2854e76F90643097d",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 367685,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b0000000000000000000000000000000000000000000000001d6978c44b2528e0000000000000000000000000000000000000000000000000000000000000c547"
            ),
        },
        "subtraces": 4,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1111111254fb6c44bAC0beD2854e76F90643097d",
            "callType": "call",
            "gas": 406252,
            "input": HexBytes(
                "0x23b872dd000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da711467500000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e0000000000000000000000000000000000000000000000001d6978c44b2528e0"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 15025,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1111111254fb6c44bAC0beD2854e76F90643097d",
            "callType": "call",
            "gas": 379504,
            "input": HexBytes(
                "0x2636f7f8000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675c2d6d529883fcacb870d5a8b12dd737459eed4776d18198b0c09094b6511c754bdb8b88b24ea1650f8e68d682822c8badb4259c731807321bc1be3c15c5d2a6e00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000008600000000000000000000000000000000000000000000000000000000000000b4080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a4b757fed600000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000002dc6c0288931fa76d7b0482f0fd0bca9a50bf0d22b9fef0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000604df92bd0800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000500000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000005600000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001408000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000064eb5625d9000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af9000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000800000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af90000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000002841e9a2e9200000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e4010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000a0969e970000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f4cf0000000000000000000000000000000000000000000000000000018382f200d00267616e64616c6674686562726f776e67786d786e690014248b18d01be8000000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000416751eb6bb914a1aaf5dd5f8ce8a17f0214f7cab8536359c5429b91c5251169173ad587504ef1ff24550c3def4cfb352a62d926f4a5187431be1612a4b9f4b6501b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002800000000000000000000000000000000000000000000000000000000000004480000000000000000000000000000000000000000000000000000000000001040000000000000000000000000000000000000000000000000000000000000064ec77bbdb000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000000000320000000000000000000000000000003200000000000000000000000000000000000000000000000000000000a09be57f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000024432ce0a7c00000000000000000000000000000000000000000000000000000000000000808000000000000000000000000000000000000000000000000000000000000044000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a405971224000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000010000000000000000000000000000000100000000000000000000000000000000000000000000000000000000007a229500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004470bdb947000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a0969e960000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000016414284aab00000000000000000000000000000000000000000000000000000000000000808000000000000000000000000000000000000000000000000000000000000024000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000000000000100000000000000000000000000000001000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000044a9059cbb0000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 302058, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 365155,
            "input": HexBytes(
                "0xb757fed600000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000002dc6c0288931fa76d7b0482f0fd0bca9a50bf0d22b9fef0000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 92260, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 358652,
            "input": HexBytes(
                "0x70a0823100000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000082813198b8d0d44a32"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 355384,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x74C99F3f5331676f6AEc2756e1F39b4FC029a83E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000008263c81ff485af2152000000000000000000000000000000000000000000000000000002c8dd66a6b2000000000000000000000000000000000000000000000000000000006333f437"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 351652,
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a02d7ce3000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x74C99F3f5331676f6AEc2756e1F39b4FC029a83E",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 84284, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [1, 0, 2],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74C99F3f5331676f6AEc2756e1F39b4FC029a83E",
            "callType": "call",
            "gas": 332961,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000a02d7ce3"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 2, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74C99F3f5331676f6AEc2756e1F39b4FC029a83E",
            "callType": "staticcall",
            "gas": 291528,
            "input": HexBytes(
                "0x70a0823100000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000082813198b8d0d44a32"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 2, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74C99F3f5331676f6AEc2756e1F39b4FC029a83E",
            "callType": "staticcall",
            "gas": 290597,
            "input": HexBytes(
                "0x70a0823100000000000000000000000074c99f3f5331676f6aec2756e1f39b4fc029a83e"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1031,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000002c83d3929cf"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 2, 2],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74C99F3f5331676f6AEc2756e1F39b4FC029a83E",
            "callType": "staticcall",
            "gas": 284478,
            "input": HexBytes("0xe380f728"),
            "to": "0x9DEB29c9a4c7A88a3C0257393b7f3335338D9A9D",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2342,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000000000000001e"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 2, 3],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 273216,
            "input": HexBytes(
                "0xdf92bd0800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000500000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000005600000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001408000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000064eb5625d9000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af9000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000800000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af90000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000002841e9a2e9200000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e4010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000a0969e970000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f4cf0000000000000000000000000000000000000000000000000000018382f200d00267616e64616c6674686562726f776e67786d786e690014248b18d01be8000000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000416751eb6bb914a1aaf5dd5f8ce8a17f0214f7cab8536359c5429b91c5251169173ad587504ef1ff24550c3def4cfb352a62d926f4a5187431be1612a4b9f4b6501b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002800000000000000000000000000000000000000000000000000000000000004480000000000000000000000000000000000000000000000000000000000001040000000000000000000000000000000000000000000000000000000000000064ec77bbdb000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000000000320000000000000000000000000000003200000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 159328, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 265948,
            "input": HexBytes(
                "0xec77bbdb000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000000000320000000000000000000000000000003200000000000000000000000000000000000000000000000000000000a09be57f"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2143,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a02d7ce3"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 1, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 261072,
            "input": HexBytes(
                "0x70a08231000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1031,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a02d7ce3"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 1, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 262522,
            "input": HexBytes(
                "0xeb5625d9000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af900000000000000000000000000000000000000000000000000000000a02d7ce3"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 26419, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 1, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 257138,
            "input": HexBytes(
                "0x095ea7b3000000000000000000000000e2e3441004e7d377a2d97142e75d465e0dd36af900000000000000000000000000000000000000000000000000000000a02d7ce3"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24953, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 1, 1, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 231593,
            "input": HexBytes(
                "0x1e9a2e9200000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e4010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a02d7ce300000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000a0969e970000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f4cf0000000000000000000000000000000000000000000000000000018382f200d00267616e64616c6674686562726f776e67786d786e690014248b18d01be8000000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000416751eb6bb914a1aaf5dd5f8ce8a17f0214f7cab8536359c5429b91c5251169173ad587504ef1ff24550c3def4cfb352a62d926f4a5187431be1612a4b9f4b6501b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xE2e3441004E7D377A2D97142e75d465e0dD36aF9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 121182, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [1, 1, 2],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE2e3441004E7D377A2D97142e75d465e0dD36aF9",
            "callType": "call",
            "gas": 224393,
            "input": HexBytes(
                "0x23b872dd000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e40100000000000000000000000000000000000000000000000000000000a02d7ce3"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 12124, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 1, 2, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE2e3441004E7D377A2D97142e75d465e0dD36aF9",
            "callType": "call",
            "gas": 208301,
            "input": HexBytes(
                "0xbdeb0ad90000000000000000000000000000000000000000000000000000000000000040000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e4010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a02d7ce300000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000a0969e970000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f4cf0000000000000000000000000000000000000000000000000000018382f200d00267616e64616c6674686562726f776e67786d786e690014248b18d01be8000000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000416751eb6bb914a1aaf5dd5f8ce8a17f0214f7cab8536359c5429b91c5251169173ad587504ef1ff24550c3def4cfb352a62d926f4a5187431be1612a4b9f4b6501b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xe8A8700faFd46CBE81AA983D180fE2EE89D3E401",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 100932,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 1, 2, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8A8700faFd46CBE81AA983D180fE2EE89D3E401",
            "callType": "delegatecall",
            "gas": 202334,
            "input": HexBytes(
                "0xbdeb0ad90000000000000000000000000000000000000000000000000000000000000040000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e8a8700fafd46cbe81aa983d180fe2ee89d3e4010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da7114675000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a02d7ce300000000000000000000000000000000000000000000000000000000a09be57f00000000000000000000000000000000000000000000000000000000a0969e970000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006333f4cf0000000000000000000000000000000000000000000000000000018382f200d00267616e64616c6674686562726f776e67786d786e690014248b18d01be8000000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000416751eb6bb914a1aaf5dd5f8ce8a17f0214f7cab8536359c5429b91c5251169173ad587504ef1ff24550c3def4cfb352a62d926f4a5187431be1612a4b9f4b6501b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x13F257714B2234C7865d5aBe0ec656423BF8be88",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 98140,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 1, 2, 1, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe8A8700faFd46CBE81AA983D180fE2EE89D3E401",
            "callType": "call",
            "gas": 146492,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000a028399b"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 44017,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 1, 2, 1, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 137072,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000a028399b"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 36728,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 1, 2, 1, 0, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 115495,
            "input": HexBytes(
                "0x32ce0a7c00000000000000000000000000000000000000000000000000000000000000808000000000000000000000000000000000000000000000000000000000000044000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef00000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a405971224000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000010000000000000000000000000000000100000000000000000000000000000000000000000000000000000000007a229500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004470bdb947000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a0969e9600000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 5992, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 112176,
            "input": HexBytes(
                "0x70bdb947000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000a0969e96"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2284,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 2, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 109677,
            "input": HexBytes(
                "0x70a08231000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 2, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 107233,
            "input": HexBytes(
                "0x70a08231000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 0, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 108586,
            "input": HexBytes(
                "0x05971224000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000100000000000000000000000000000000000000000000000000000000007a2295"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 660, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 2, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 108736,
            "input": HexBytes(
                "0x14284aab00000000000000000000000000000000000000000000000000000000000000808000000000000000000000000000000000000000000000000000000000000024000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb480000000000000000000000000000000100000000000000000000000000000001000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000044a9059cbb0000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 32829, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [1, 3],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "staticcall",
            "gas": 105607,
            "input": HexBytes(
                "0x70a08231000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 3, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 103227,
            "input": HexBytes(
                "0x70a08231000000000000000000000000288931fa76d7b0482f0fd0bca9a50bf0d22b9fef"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 3, 0, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf",
            "callType": "call",
            "gas": 103196,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d00000000000000000000000000000000000000000000000000000000a028399b"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 28717,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 3, 1],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 100851,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d00000000000000000000000000000000000000000000000000000000a028399b"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 27928,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 3, 1, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1111111254fb6c44bAC0beD2854e76F90643097d",
            "callType": "staticcall",
            "gas": 81585,
            "input": HexBytes(
                "0x70a082310000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b"
            ),
        },
        "subtraces": 1,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 79580,
            "input": HexBytes(
                "0x70a082310000000000000000000000001111111254fb6c44bac0bed2854e76f90643097d"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000a028399b"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1111111254fb6c44bAC0beD2854e76F90643097d",
            "callType": "call",
            "gas": 78469,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da711467500000000000000000000000000000000000000000000000000000000a028399b"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 28717,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 76510,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c298bf0c5dcf8ab55ee568ffbe8b503da711467500000000000000000000000000000000000000000000000000000000a028399b"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 27928,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0x62699a9a1862cffb6de9b5a515e0d88b794f0063d30a18012284fc4e80dfb228"
        ),
        "transactionPosition": 56,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1CbbC8199ec810670b187A93603d8d7495a419fd",
            "callType": "call",
            "gas": 62865,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000030741289523c2e4d2a62c7d6722686d14e723851000000000000000000000000000000000000000000000024287c0615218c0000"
            ),
            "to": "0xdebe620609674F21B1089042527F420372eA98A5",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 15089,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8201ab74775e340545466eb56aca74a66663cfed5ed882305448008b2958d858"
        ),
        "transactionPosition": 57,
        "type": "call",
    },
    {
        "action": {
            "from": "0x31f8982fEC8a8Af5799868E2Ab61738C5Cf5F7e0",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x4329952703f3451b6bd4192681cc1ac12a9b49c59f8f1cc341916e43edc50528"
        ),
        "transactionPosition": 58,
        "type": "call",
    },
    {
        "action": {
            "from": "0xD947b1482A70606955A5519E42F7E443fFb118ff",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x442faeeac16b6f7d65fd7c446d34a43ce76c75afeef160bbd6b55f91cdc7af67"
        ),
        "transactionPosition": 59,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7d1Bf93a23aEc882A2e2ad066CAa939D7278a777",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa3345c931a6eefc7ed7fb9871fae9aa58e584b2605fda35a731a2821a5e2d9f9"
        ),
        "transactionPosition": 60,
        "type": "call",
    },
    {
        "action": {
            "from": "0x42dBb58C41464594983Eeb58Ea9ec61B10C9DA6B",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x02dbd77c4d9f4628dbd6c7b6e8aff8a8a0926885b0cfb92470d33e148360da77"
        ),
        "transactionPosition": 61,
        "type": "call",
    },
    {
        "action": {
            "from": "0x70446D32D69C1C2a5b8FBe672541fCdF9f45C199",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2bd16eb236b0e6ae85530081508a6621caddd08bdce97bde5bbd02c16eaa10b8"
        ),
        "transactionPosition": 62,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe5e7f6783180d786E471862eeecf532337441834",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xead0f6f356d5a7a0a2564f300f72f214128a5332b7f65d8851770435f89874d9"
        ),
        "transactionPosition": 63,
        "type": "call",
    },
    {
        "action": {
            "from": "0x84092801Ee8381905D2d090903570d82b490047c",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x5add90f1d02771bbeae1852b626c67c26461b0369d000f5aaa74570195a3af54"
        ),
        "transactionPosition": 64,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1CbFe2D7180533E0FD23aa182C5dE630B24c6D56",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xee24a81eeb1987a70dfb2ab5715a72fedeaead74789e62ee8969b3064a835c54"
        ),
        "transactionPosition": 65,
        "type": "call",
    },
    {
        "action": {
            "from": "0x53a6FdEf8bdcc806613CdF84fFF68D8e5AD3D9ef",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa5156879bac0e5aa75b3e12d0b076faf27003d4ddbbf4832581e10904c0f1622"
        ),
        "transactionPosition": 66,
        "type": "call",
    },
    {
        "action": {
            "from": "0xbD2c2F2BA4AC64217183f70AE970286282C4D896",
            "callType": "call",
            "gas": 24639,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24639, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xefd2df30d83664509cb1660f10b757c9a4e331c3fb90594b3e9b3169cd8addf1"
        ),
        "transactionPosition": 67,
        "type": "call",
    },
    {
        "action": {
            "from": "0x077D360f11D220E4d5D831430c81C26c9be7C4A4",
            "callType": "call",
            "gas": 69000,
            "input": HexBytes("0x"),
            "to": "0x54296C42aAAEfD12786c05d38BB889C0015D83a2",
            "value": 48420970000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x722282ce78cf93070d5c6eae9a11bf55cf48412f7a7dae849fc3f156d0626841"
        ),
        "transactionPosition": 68,
        "type": "call",
    },
    {
        "action": {
            "from": "0x26cE7c1976C5eec83eA6Ac22D83cB341B08850aF",
            "callType": "call",
            "gas": 48268,
            "input": HexBytes(
                "0x5c19a95c0000000000000000000000006037667a4ee835a0b78258d0cb6ae4c3dd0fa9dcdd0bea13000000000000000000000000000000000000000000000002b5e57320f9bf0e8f"
            ),
            "to": "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 27417, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa3faa931dc47cf4357667d1d0b45e855a9b200628287c5584c468de7792c514d"
        ),
        "transactionPosition": 69,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40",
            "callType": "delegatecall",
            "gas": 44432,
            "input": HexBytes(
                "0xdd0bea13000000000000000000000000000000000000000000000002b5e57320f9bf0e8f"
            ),
            "to": "0x6037667A4Ee835a0b78258D0cb6Ae4c3DD0fA9dC",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24239, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xa3faa931dc47cf4357667d1d0b45e855a9b200628287c5584c468de7792c514d"
        ),
        "transactionPosition": 69,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40",
            "callType": "call",
            "gas": 40729,
            "input": HexBytes(
                "0x2e1a7d4d000000000000000000000000000000000000000000000002b5e57320f9bf0e8f"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14017, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xa3faa931dc47cf4357667d1d0b45e855a9b200628287c5584c468de7792c514d"
        ),
        "transactionPosition": 69,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40",
            "value": 50000497023416995471,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 77, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0xa3faa931dc47cf4357667d1d0b45e855a9b200628287c5584c468de7792c514d"
        ),
        "transactionPosition": 69,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40",
            "callType": "call",
            "gas": 19998,
            "input": HexBytes("0x"),
            "to": "0x26cE7c1976C5eec83eA6Ac22D83cB341B08850aF",
            "value": 50000497023416995471,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0xa3faa931dc47cf4357667d1d0b45e855a9b200628287c5584c468de7792c514d"
        ),
        "transactionPosition": 69,
        "type": "call",
    },
    {
        "action": {
            "from": "0x6C2eDA9deDBC76A2Dd4b0E05cE5F5ae68B97e60e",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x41F3cbBaA1EDA77EccE61E3f6814a843f77CD1eD",
            "value": 53521723674731263,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc411f2adb10200988181ee0bfcfa82ae6816c3081a252ee1f3e1b711514713e7"
        ),
        "transactionPosition": 70,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF062b3fEf2C936e554aaD3Fb0B4009c444A78220",
            "callType": "call",
            "gas": 24647,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x160C404B2b49CBC3240055CEaEE026df1e8497A0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24647, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xcc7ff6ce29157a48eb5a666a5d6f1b2d3f686532282ad858afb22828b9cc80dd"
        ),
        "transactionPosition": 71,
        "type": "call",
    },
    {
        "action": {
            "from": "0x6962CA99bdf7349CB1fd18fB39bE16F6EFeF1100",
            "callType": "call",
            "gas": 33061,
            "input": HexBytes(
                "0x42842e0e0000000000000000000000006962ca99bdf7349cb1fd18fb39be16f6efef11000000000000000000000000003516d0795d3515aced88f94d53978460efdbab8c0000000000000000000000000000000000000000000000000000000000001f5c"
            ),
            "to": "0xe17827609Ac34443B3987661f4e037642F6BD9bA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 32697, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x68b57d91e9bd524d1d8ab7be1dd9aabb89f46856a1c6d05b0d49ca98fd2ceb6a"
        ),
        "transactionPosition": 72,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe17827609Ac34443B3987661f4e037642F6BD9bA",
            "callType": "delegatecall",
            "gas": 25360,
            "input": HexBytes(
                "0x42842e0e0000000000000000000000006962ca99bdf7349cb1fd18fb39be16f6efef11000000000000000000000000003516d0795d3515aced88f94d53978460efdbab8c0000000000000000000000000000000000000000000000000000000000001f5c"
            ),
            "to": "0x64aa40D6865079379e41cA7CF9A001C5B962B94F",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 25360, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x68b57d91e9bd524d1d8ab7be1dd9aabb89f46856a1c6d05b0d49ca98fd2ceb6a"
        ),
        "transactionPosition": 72,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA7E5a837382C4B2A484BD2AFAdc8B5A5f6d74e87",
            "callType": "call",
            "gas": 1028936,
            "input": HexBytes("0x3ccfd60b"),
            "to": "0x189Dcc34ad4f90aD4a35160850406fEe3c16c0D7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 78703, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2e8602f0b166026645e4ec9d9caef4c414b375cd47481a601fda4702bc544f06"
        ),
        "transactionPosition": 73,
        "type": "call",
    },
    {
        "action": {
            "from": "0x189Dcc34ad4f90aD4a35160850406fEe3c16c0D7",
            "callType": "delegatecall",
            "gas": 1005686,
            "input": HexBytes("0x3ccfd60b"),
            "to": "0x63583366554d67319eCE65e1AA031a6817B14123",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 71378, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x2e8602f0b166026645e4ec9d9caef4c414b375cd47481a601fda4702bc544f06"
        ),
        "transactionPosition": 73,
        "type": "call",
    },
    {
        "action": {
            "from": "0x189Dcc34ad4f90aD4a35160850406fEe3c16c0D7",
            "callType": "call",
            "gas": 951882,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000a7e5a837382c4b2a484bd2afadc8b5a5f6d74e870000000000000000000000000000000000000000000009695691b976a671c71c"
            ),
            "to": "0x38B0e3A59183814957D83dF2a97492AED1F003e2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30748,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x2e8602f0b166026645e4ec9d9caef4c414b375cd47481a601fda4702bc544f06"
        ),
        "transactionPosition": 73,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa5D404f1C6Cf7861869C4Ff954FB653087368b49",
            "callType": "call",
            "gas": 24737,
            "input": HexBytes(
                "0x095ea7b3000000000000000000000000c6a22cc9acd40b4f31467a3580d4d69c3387f3490000000000000000000000000000000000000000000000000000012309ce5400"
            ),
            "to": "0xa393473d64d2F9F026B60b6Df7859A689715d092",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 24737,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x0faf55ac01d551b886aecf3a06dba27048b570a3109f8adf1f9c4947285562bc"
        ),
        "transactionPosition": 74,
        "type": "call",
    },
    {
        "action": {
            "from": "0xEFCfF30414a3C4720e1a84141fbBA1f16bA8652C",
            "callType": "call",
            "gas": 47555,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000073c414e24ae42cb848fd3049bc05a4998e6b96fa0000000000000000000000000000000000000000000000000000000055670a98"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x67698eb06a875e2708a10665f74bd0184d07173053e5f0754e38194d6ba8db1b"
        ),
        "transactionPosition": 75,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0FeaAa5677679bdAa363FB37E72122613FC59F38",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x30e9c3076Cd4E7453b8F2AEC6B7BC0b759b72231",
            "value": 100000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2714ef67d21fa20ca7bf28cea66db566e0ad68d5aed03c501ac683720e9e680c"
        ),
        "transactionPosition": 76,
        "type": "call",
    },
    {
        "action": {
            "from": "0xD4a08cF067c83d1B2Cc1D26831569b7850804bE7",
            "callType": "call",
            "gas": 95032,
            "input": HexBytes(
                "0x647077ee000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000209b000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000633d2eca000000000000000000000000000000000000000000000000000000000000004119339d6d991b6998d0050f817a01b707af126f0bc3ca5d7d896a2fdda0b81da744d6dd52cec6ab22711a16609b8e21d052ea1e4550353e0d7cc7f8cd043244e21c00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xC45f3c76FeeEa53aAE5AFA9b51F166E025145400",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 92850, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1194635c792344c2a88b105ef26bfb5e8f8c3295910978ba45f655b285ca9772"
        ),
        "transactionPosition": 77,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC45f3c76FeeEa53aAE5AFA9b51F166E025145400",
            "callType": "staticcall",
            "gas": 76323,
            "input": HexBytes(
                "0x6352211e000000000000000000000000000000000000000000000000000000000000209b"
            ),
            "to": "0x1AFEF6b252cc35Ec061eFe6a9676C90915a73F18",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2916,
            "output": HexBytes(
                "0x000000000000000000000000d4a08cf067c83d1b2cc1d26831569b7850804be7"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x1194635c792344c2a88b105ef26bfb5e8f8c3295910978ba45f655b285ca9772"
        ),
        "transactionPosition": 77,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC45f3c76FeeEa53aAE5AFA9b51F166E025145400",
            "callType": "call",
            "gas": 46095,
            "input": HexBytes(
                "0x40c10f19000000000000000000000000d4a08cf067c83d1b2cc1d26831569b7850804be70000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x7Eb72B7EC6961C0fad45Ff174403a2B3dc5018f1",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 39532, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x1194635c792344c2a88b105ef26bfb5e8f8c3295910978ba45f655b285ca9772"
        ),
        "transactionPosition": 77,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC45f3c76FeeEa53aAE5AFA9b51F166E025145400",
            "callType": "staticcall",
            "gas": 6821,
            "input": HexBytes("0x18160ddd"),
            "to": "0x7Eb72B7EC6961C0fad45Ff174403a2B3dc5018f1",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2477,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000001701"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x1194635c792344c2a88b105ef26bfb5e8f8c3295910978ba45f655b285ca9772"
        ),
        "transactionPosition": 77,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5164370B3BA971474d10da1D409ce8872Cb8ca97",
            "callType": "call",
            "gas": 31157,
            "input": HexBytes(
                "0xfd9f1e100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000005164370b3ba971474d10da1d409ce8872cb8ca97000000000000000000000000868b0635a8858db9d984b5a27559f961fd2736c0000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000002200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333ef3600000000000000000000000000000000000000000000000000000000633d29960000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000013229eed22a7d62618cf13c76c1ffc2168fc47c98453dcc6134f5c88888888888888888888888880000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000030000000000000000000000007941d5347148563ca41886c7780e8b2456b839b000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000de0b6b3a76400000000000000000000000000005164370b3ba971474d10da1d409ce8872cb8ca97"
            ),
            "to": "0xBb62D5b69AE3A747EcD019aD3bE5EC06D84A21e9",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 31157,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x5ccd14a8f0e349a08db8f5484c94284d93d6ab9a50eb2c44d7abace37ef7724e"
        ),
        "transactionPosition": 78,
        "type": "call",
    },
    {
        "action": {
            "from": "0xEAF7057423F7758600a5f8c1DE8446068803771C",
            "callType": "call",
            "gas": 265131,
            "input": HexBytes(
                "0x5ae401dc000000000000000000000000000000000000000000000000000000006333fb27000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000e442712a67000000000000000000000000000000000000000000000485ed8c2ddea7c00000000000000000000000000000000000000000000000000000008bf45601ee05700000000000000000000000000000000000000000000000000000000000000080000000000000000000000000eaf7057423f7758600a5f8c1de8446068803771c0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000064df3aab3b21cc275bb76c4a581cf8b726478ee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000412210e8a00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 39393671999522160,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 215637,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000008b4215e5e6780a0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "delegatecall",
            "gas": 259652,
            "input": HexBytes(
                "0x42712a67000000000000000000000000000000000000000000000485ed8c2ddea7c00000000000000000000000000000000000000000000000000000008bf45601ee05700000000000000000000000000000000000000000000000000000000000000080000000000000000000000000eaf7057423f7758600a5f8c1de8446068803771c0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000064df3aab3b21cc275bb76c4a581cf8b726478ee0"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 39393671999522160,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 205016,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000008b4215e5e6780a"
            ),
        },
        "subtraces": 6,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 250769,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x397973Ba6E752943EA9146F88414D1f379fd427e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000003ab50b3c4a14fac426f2940000000000000000000000000000000000000000000000070980a4445369543e000000000000000000000000000000000000000000000000000000006333f383"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 236497,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 39197683581614090,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 23974, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 212476,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000397973ba6e752943ea9146f88414d1f379fd427e000000000000000000000000000000000000000000000000008b4215e5e6780a"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 202911,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x397973Ba6E752943EA9146F88414D1f379fd427e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 504,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000003ab50b3c4a14fac426f2940000000000000000000000000000000000000000000000070980a4445369543e000000000000000000000000000000000000000000000000000000006333f383"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 3],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 201562,
            "input": HexBytes(
                "0x70a08231000000000000000000000000397973ba6e752943ea9146f88414d1f379fd427e"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000070a0be65a394fcc48"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 4],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 199360,
            "input": HexBytes(
                "0x022c0d9f000000000000000000000000000000000000000000000485ed8c2ddea7c1d93a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000eaf7057423f7758600a5f8c1de8446068803771c00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x397973Ba6E752943EA9146F88414D1f379fd427e",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 147662, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [0, 5],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x397973Ba6E752943EA9146F88414D1f379fd427e",
            "callType": "call",
            "gas": 183079,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000eaf7057423f7758600a5f8c1de8446068803771c000000000000000000000000000000000000000000000485ed8c2ddea7c1d93a"
            ),
            "to": "0x64Df3aAB3b21cC275bB76c4A581Cf8B726478ee0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 112330,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 5, 0],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x397973Ba6E752943EA9146F88414D1f379fd427e",
            "callType": "staticcall",
            "gas": 71883,
            "input": HexBytes(
                "0x70a08231000000000000000000000000397973ba6e752943ea9146f88414d1f379fd427e"
            ),
            "to": "0x64Df3aAB3b21cC275bB76c4A581Cf8B726478ee0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 975,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000003ab0854ebde71c1c65195a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 5, 1],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x397973Ba6E752943EA9146F88414D1f379fd427e",
            "callType": "staticcall",
            "gas": 70518,
            "input": HexBytes(
                "0x70a08231000000000000000000000000397973ba6e752943ea9146f88414d1f379fd427e"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000070a0be65a394fcc48"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 5, 2],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "delegatecall",
            "gas": 57148,
            "input": HexBytes("0x12210e8a"),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 39393671999522160,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 7468, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 49035,
            "input": HexBytes("0x"),
            "to": "0xEAF7057423F7758600a5f8c1DE8446068803771C",
            "value": 195988417908070,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0xc717b2b2671d626c53271c1c0666c280e363b1488c1b04d5aefa79ea8601dff8"
        ),
        "transactionPosition": 79,
        "type": "call",
    },
    {
        "action": {
            "from": "0x3F478216041713A4B1EcB672515cc1b039BBE790",
            "callType": "call",
            "gas": 274494,
            "input": HexBytes(
                "0x6a76120200000000000000000000000040a2accbd92bca938b02010e17a5b8929b49130d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000003c2f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000064000000000000000000000000000000000000000000000000000000000000004c48d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000046b00469788fe6e9e9681c6ebf3bf78e7fd26fc01544600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044bd86e508736166652e657468000000000000000000000000000000000000000000000000000000000000000000000000d662e05ce522b3861b70fc376f60bf50e200abfa00a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c4bf6213e4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000005bacaa20000000000000000000000000000000000000000000000012dfc9a7680524000000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000100142b9e197e79ca94c077397bec601d9758e6ad54bfb308c529fb1ccb649664629507b80014ff96094ee587f52aed4ea98ccdce3ed4cef1139f4cbc45abf4cf3efca2d62b9a7cace73dca2d91ef5456d3fcecc2549d7cfeb33bf495a2505190b3cc6a55a90d3f5817150ad9c8d4fb3c6157c5ab99a2bd90bde5385608e212b9f0c0eb5e6c10b114900b7f894fcd9ba6126d9495341e2b09a684d822a04ba9e3bf40757bdb25323893eeac40649684dae8d5ac9be1b5688df2c8c77ffb1df3a8920c9493e26704a190c539948597a25dd0eadc3e9d3c04eef5e8bbb84dff18696e8fd0248ce2387d7c823f3b28280a73edcfd1b00d103210f5ca8f817b8c90519736c3b51ea1b6472ba406c4456d5b01c3b59343e564aae747fdd47ff6dc8ff4629d28252544a7e92977dccd4b30fb02073f088b2ad1cf0b7f5b2205842f5a78ba2580459420e11a06505b18e5ee6f8ded5bb92ee903d2eaf5d63bbecd73e213ca0870e463abf45cb18f85a835919099f45c6c56581232b3be9c06448420b35c94f4f3628f31b808b09ced67b073ab97919ba14e9389e154be4fe2b10fcdd327302fdc9a0b8cea5373715d2fce8d9ddd244f4259aafb0a21305edfdda956dd84359d69bacd790ff82f7310dd382bf3f53e885e74f5dad9b3aeb7fe96ce926ff47f8e2791b9d07b3e620189a36bf17e30c874e66b205c79492a16cd5a9c5bb65b700a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640087b83f9aef04d6a9b38aab1023696e3b35434a8ba4c1611b39074722e31473dd333d27000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000410ff58feb0cba6ef7e22c415a7936b8a81fa384ebc5d2ec3718cc5e72730ddcdd296b0b29dd3aba9c64edde30f65ea98066a2cfa3412f9877d6bf3fded867ffd01b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x826f446C587159897Db0aE01192dA1691f12007f",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 228534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x826f446C587159897Db0aE01192dA1691f12007f",
            "callType": "delegatecall",
            "gas": 265117,
            "input": HexBytes(
                "0x6a76120200000000000000000000000040a2accbd92bca938b02010e17a5b8929b49130d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000003c2f80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000064000000000000000000000000000000000000000000000000000000000000004c48d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000046b00469788fe6e9e9681c6ebf3bf78e7fd26fc01544600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044bd86e508736166652e657468000000000000000000000000000000000000000000000000000000000000000000000000d662e05ce522b3861b70fc376f60bf50e200abfa00a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c4bf6213e4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000005bacaa20000000000000000000000000000000000000000000000012dfc9a7680524000000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000100142b9e197e79ca94c077397bec601d9758e6ad54bfb308c529fb1ccb649664629507b80014ff96094ee587f52aed4ea98ccdce3ed4cef1139f4cbc45abf4cf3efca2d62b9a7cace73dca2d91ef5456d3fcecc2549d7cfeb33bf495a2505190b3cc6a55a90d3f5817150ad9c8d4fb3c6157c5ab99a2bd90bde5385608e212b9f0c0eb5e6c10b114900b7f894fcd9ba6126d9495341e2b09a684d822a04ba9e3bf40757bdb25323893eeac40649684dae8d5ac9be1b5688df2c8c77ffb1df3a8920c9493e26704a190c539948597a25dd0eadc3e9d3c04eef5e8bbb84dff18696e8fd0248ce2387d7c823f3b28280a73edcfd1b00d103210f5ca8f817b8c90519736c3b51ea1b6472ba406c4456d5b01c3b59343e564aae747fdd47ff6dc8ff4629d28252544a7e92977dccd4b30fb02073f088b2ad1cf0b7f5b2205842f5a78ba2580459420e11a06505b18e5ee6f8ded5bb92ee903d2eaf5d63bbecd73e213ca0870e463abf45cb18f85a835919099f45c6c56581232b3be9c06448420b35c94f4f3628f31b808b09ced67b073ab97919ba14e9389e154be4fe2b10fcdd327302fdc9a0b8cea5373715d2fce8d9ddd244f4259aafb0a21305edfdda956dd84359d69bacd790ff82f7310dd382bf3f53e885e74f5dad9b3aeb7fe96ce926ff47f8e2791b9d07b3e620189a36bf17e30c874e66b205c79492a16cd5a9c5bb65b700a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640087b83f9aef04d6a9b38aab1023696e3b35434a8ba4c1611b39074722e31473dd333d27000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000410ff58feb0cba6ef7e22c415a7936b8a81fa384ebc5d2ec3718cc5e72730ddcdd296b0b29dd3aba9c64edde30f65ea98066a2cfa3412f9877d6bf3fded867ffd01b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 223320,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x826f446C587159897Db0aE01192dA1691f12007f",
            "callType": "delegatecall",
            "gas": 239379,
            "input": HexBytes(
                "0x8d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000046b00469788fe6e9e9681c6ebf3bf78e7fd26fc01544600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044bd86e508736166652e657468000000000000000000000000000000000000000000000000000000000000000000000000d662e05ce522b3861b70fc376f60bf50e200abfa00a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c4bf6213e4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000005bacaa20000000000000000000000000000000000000000000000012dfc9a7680524000000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000100142b9e197e79ca94c077397bec601d9758e6ad54bfb308c529fb1ccb649664629507b80014ff96094ee587f52aed4ea98ccdce3ed4cef1139f4cbc45abf4cf3efca2d62b9a7cace73dca2d91ef5456d3fcecc2549d7cfeb33bf495a2505190b3cc6a55a90d3f5817150ad9c8d4fb3c6157c5ab99a2bd90bde5385608e212b9f0c0eb5e6c10b114900b7f894fcd9ba6126d9495341e2b09a684d822a04ba9e3bf40757bdb25323893eeac40649684dae8d5ac9be1b5688df2c8c77ffb1df3a8920c9493e26704a190c539948597a25dd0eadc3e9d3c04eef5e8bbb84dff18696e8fd0248ce2387d7c823f3b28280a73edcfd1b00d103210f5ca8f817b8c90519736c3b51ea1b6472ba406c4456d5b01c3b59343e564aae747fdd47ff6dc8ff4629d28252544a7e92977dccd4b30fb02073f088b2ad1cf0b7f5b2205842f5a78ba2580459420e11a06505b18e5ee6f8ded5bb92ee903d2eaf5d63bbecd73e213ca0870e463abf45cb18f85a835919099f45c6c56581232b3be9c06448420b35c94f4f3628f31b808b09ced67b073ab97919ba14e9389e154be4fe2b10fcdd327302fdc9a0b8cea5373715d2fce8d9ddd244f4259aafb0a21305edfdda956dd84359d69bacd790ff82f7310dd382bf3f53e885e74f5dad9b3aeb7fe96ce926ff47f8e2791b9d07b3e620189a36bf17e30c874e66b205c79492a16cd5a9c5bb65b700a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640087b83f9aef04d6a9b38aab1023696e3b35434a8ba4c1611b39074722e31473dd333d27000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a7640000000000000000000000000000000000000000000000"
            ),
            "to": "0x40A2aCCbd92BCA938b02010E17A5b8929b49130D",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 201030, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x826f446C587159897Db0aE01192dA1691f12007f",
            "callType": "call",
            "gas": 232202,
            "input": HexBytes(
                "0xbd86e508736166652e657468000000000000000000000000000000000000000000000000000000000000000000000000d662e05ce522b3861b70fc376f60bf50e200abfa"
            ),
            "to": "0x469788fE6E9E9681C6ebF3bF78e7Fd26Fc015446",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24983, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x826f446C587159897Db0aE01192dA1691f12007f",
            "callType": "call",
            "gas": 204798,
            "input": HexBytes(
                "0xbf6213e4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000005bacaa20000000000000000000000000000000000000000000000012dfc9a7680524000000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000100142b9e197e79ca94c077397bec601d9758e6ad54bfb308c529fb1ccb649664629507b80014ff96094ee587f52aed4ea98ccdce3ed4cef1139f4cbc45abf4cf3efca2d62b9a7cace73dca2d91ef5456d3fcecc2549d7cfeb33bf495a2505190b3cc6a55a90d3f5817150ad9c8d4fb3c6157c5ab99a2bd90bde5385608e212b9f0c0eb5e6c10b114900b7f894fcd9ba6126d9495341e2b09a684d822a04ba9e3bf40757bdb25323893eeac40649684dae8d5ac9be1b5688df2c8c77ffb1df3a8920c9493e26704a190c539948597a25dd0eadc3e9d3c04eef5e8bbb84dff18696e8fd0248ce2387d7c823f3b28280a73edcfd1b00d103210f5ca8f817b8c90519736c3b51ea1b6472ba406c4456d5b01c3b59343e564aae747fdd47ff6dc8ff4629d28252544a7e92977dccd4b30fb02073f088b2ad1cf0b7f5b2205842f5a78ba2580459420e11a06505b18e5ee6f8ded5bb92ee903d2eaf5d63bbecd73e213ca0870e463abf45cb18f85a835919099f45c6c56581232b3be9c06448420b35c94f4f3628f31b808b09ced67b073ab97919ba14e9389e154be4fe2b10fcdd327302fdc9a0b8cea5373715d2fce8d9ddd244f4259aafb0a21305edfdda956dd84359d69bacd790ff82f7310dd382bf3f53e885e74f5dad9b3aeb7fe96ce926ff47f8e2791b9d07b3e620189a36bf17e30c874e66b205c79492a16cd5a9c5bb65b7"
            ),
            "to": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 75351, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0, 1],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "staticcall",
            "gas": 188502,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a0b937d5c8e32a80e3a8ed4227cd020221544ee6"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2886,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000295bd306348cee3284339a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 1, 0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x826f446C587159897Db0aE01192dA1691f12007f",
            "callType": "call",
            "gas": 130274,
            "input": HexBytes(
                "0x0087b83f9aef04d6a9b38aab1023696e3b35434a8ba4c1611b39074722e31473dd333d27000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a7640000"
            ),
            "to": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 93862, "output": HexBytes("0x")},
        "subtraces": 7,
        "traceAddress": [0, 0, 2],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "call",
            "gas": 119997,
            "input": HexBytes(
                "0x095ea7b30000000000000000000000008cf60b289f8d31f737049b590b5e4285ff0bd1d10000000000000000000000000000000000000000000000000de0b6b3a7640000"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 25285,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "staticcall",
            "gas": 94401,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a0b937d5c8e32a80e3a8ed4227cd020221544ee6"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 886,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000295bd306348cee3284339a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 1],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "staticcall",
            "gas": 92834,
            "input": HexBytes(
                "0x70a08231000000000000000000000000826f446c587159897db0ae01192da1691f12007f"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2886,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 2],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "call",
            "gas": 85106,
            "input": HexBytes(
                "0x468721a70000000000000000000000005afe3855358e112b5647b952709e6165e1c1eeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006423b872dd000000000000000000000000a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x8CF60B289f8d31F737049B590b5E4285Ff0Bd1D1",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 41825,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 0, 2, 3],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x8CF60B289f8d31F737049B590b5E4285Ff0Bd1D1",
            "callType": "delegatecall",
            "gas": 79018,
            "input": HexBytes(
                "0x468721a70000000000000000000000005afe3855358e112b5647b952709e6165e1c1eeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006423b872dd000000000000000000000000a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 36946,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 0, 2, 3, 0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0x8CF60B289f8d31F737049B590b5E4285Ff0Bd1D1",
            "callType": "call",
            "gas": 74535,
            "input": HexBytes(
                "0x23b872dd000000000000000000000000a0b937d5c8e32a80e3a8ed4227cd020221544ee6000000000000000000000000826f446c587159897db0ae01192da1691f12007f0000000000000000000000000000000000000000000000000de0b6b3a7640000"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 32341,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 3, 0, 0],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "call",
            "gas": 43002,
            "input": HexBytes(
                "0x095ea7b30000000000000000000000008cf60b289f8d31f737049b590b5e4285ff0bd1d10000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 3285,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 4],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "staticcall",
            "gas": 39062,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a0b937d5c8e32a80e3a8ed4227cd020221544ee6"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 886,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000295bd2f853d63a8b20339a"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 5],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6",
            "callType": "staticcall",
            "gas": 37498,
            "input": HexBytes(
                "0x70a08231000000000000000000000000826f446c587159897db0ae01192da1691f12007f"
            ),
            "to": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 886,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000de0b6b3a7640000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 6],
        "transactionHash": HexBytes(
            "0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0"
        ),
        "transactionPosition": 80,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE0F06628c2791D1D1Ce7152EB6c7f4f363aaB666",
            "callType": "call",
            "gas": 73199,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000003319ed9a3a12e4cbc6c183464c05a0e9950ce53b000000000000000000000000000000000000000000000000000000000bebc200"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x68c46c1ff47dbafc55b1792d90ead3cb2f77e40162701f5f591cf4e939816ddf"
        ),
        "transactionPosition": 81,
        "type": "call",
    },
    {
        "action": {
            "from": "0xcE87E19d211a00955FBB7dF1613F647e43728083",
            "callType": "call",
            "gas": 13162,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000099a4b1b291610c6cff40fd1533c5a046b7128633000000000000000000000000000000000000000000000028fb9b8a8a53500000"
            ),
            "to": "0xE1BDA0c3Bfa2bE7f740f0119B6a34F057BD58Eba",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13162,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x001dab67b0430ee38bbc51020b3ed3e1ea437fddc46f21f558bb07b7599377c7"
        ),
        "transactionPosition": 82,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4dAC3A5DD68e22fbf178566804bb3B0C00bF07fd",
            "callType": "call",
            "gas": 199133,
            "input": HexBytes(
                "0xfb0f3ee1000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000567cbd30698000000000000000000000000001b45abfd4a82c438f1bb63b691ac7c662efcf0c6000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000aeab9ecbfae9a0ec5d6035c887d4d115abcae1d00000000000000000000000000000000000000000000000000000000000001fb700000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333f20f00000000000000000000000000000000000000000000000000000000635b7f0f0000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000e434d9a806d01ead0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002e00000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000026a74d6728000000000000000000000000000000a26b00c1f0df003000390027140000faa71900000000000000000000000000000000000000000000000000007bb0f7b08000000000000000000000000000efe00956a448d2ec6a1dc60576386e823ae7451f0000000000000000000000000000000000000000000000000000000000000041d31cd770264207b90dc1c19a43992583c7548475ad941b1bae866acf292e8a7d66fc7d0d362bb09dbc05008ce83e91ad342aee68a9583a4a1eb09f013129f7e41b00000000000000000000000000000000000000000000000000000000000000360c6ebe"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 1700000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 196962,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 5,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "staticcall",
            "gas": 174950,
            "input": HexBytes(
                "0x0e1d31dc833f3ae65130a500c920351e96a7a3f34a7431f5303ddfd886000229eb5d31b50000000000000000000000004dac3a5dd68e22fbf178566804bb3b0c00bf07fd0000000000000000000000001b45abfd4a82c438f1bb63b691ac7c662efcf0c60000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x004C00500000aD104D7DBd00e3ae0A5C00560C00",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 257,
            "output": HexBytes(
                "0x0e1d31dc00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 145017,
            "input": HexBytes(
                "0x4ce34aa2000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000aeab9ecbfae9a0ec5d6035c887d4d115abcae1d00000000000000000000000001b45abfd4a82c438f1bb63b691ac7c662efcf0c60000000000000000000000004dac3a5dd68e22fbf178566804bb3b0c00bf07fd0000000000000000000000000000000000000000000000000000000000001fb70000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 115736,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 136844,
            "input": HexBytes(
                "0x23b872dd0000000000000000000000001b45abfd4a82c438f1bb63b691ac7c662efcf0c60000000000000000000000004dac3a5dd68e22fbf178566804bb3b0c00bf07fd0000000000000000000000000000000000000000000000000000000000001fb7"
            ),
            "to": "0xaEab9eCBfae9A0ec5D6035c887D4D115aBcAe1D0",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 109620, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 21310,
            "input": HexBytes("0x"),
            "to": "0x0000a26b00c1F0DF003000390027140000fAa719",
            "value": 42500000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 85, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 11718,
            "input": HexBytes("0x"),
            "to": "0xeFE00956A448d2EC6A1Dc60576386E823AE7451F",
            "value": 136000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 2373,
            "input": HexBytes("0x"),
            "to": "0x1b45aBFD4a82c438f1BB63b691Ac7c662Efcf0C6",
            "value": 1521500000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x6041f8446dfb2733b9169dd85f070e339dc5e50cacb3a46b42b113f165518d6c"
        ),
        "transactionPosition": 83,
        "type": "call",
    },
    {
        "action": {
            "from": "0xE6DBd9495b077A63807E7b17FB45751545910894",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x727bf745e7afb11Bf40Ca3b2B11c63e00EA656c2",
            "value": 5000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x39b30da08a37c206724acdd1420d14bae4183d081df0cef044c3dd778f8946f0"
        ),
        "transactionPosition": 84,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9BaBfAF25025E304Bc7408A39cf5E40d0120BeaA",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x0C649D071C687288A325A8aA82EF42a917fE8A0F",
            "value": 500000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x2a72ae1dae981a2568da14d1b5ecf2d495df086dc1bc6399eaad348e20b5b51c"
        ),
        "transactionPosition": 85,
        "type": "call",
    },
    {
        "action": {
            "from": "0xd7cD7a7555d2aa59c514c18F353E97bDa2a2dAfb",
            "callType": "call",
            "gas": 73199,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000ddff626f546da128f773dd794159d627c0a1a5f9000000000000000000000000000000000000000000000000000000001dcd6500"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6b32636fdf28aed992d59d3f74bf179f047724845fac716ea1f9413dfc119ce6"
        ),
        "transactionPosition": 86,
        "type": "call",
    },
    {
        "action": {
            "from": "0x864D77785594CA373F64Ae773B4c7a5FD0FC15D9",
            "callType": "call",
            "gas": 51256,
            "input": HexBytes(
                "0x379607f5000000000000000000000000000000000000000000000000000000000165aa80"
            ),
            "to": "0x3333336D579A0107849Eb68C9f1c0B92D48C2889",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 50899, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x6095a3a6e9d6444901e9d66abb6a48cda862d7770ef319e8ed8c5be4ee9e772f"
        ),
        "transactionPosition": 87,
        "type": "call",
    },
    {
        "action": {
            "from": "0x3333336D579A0107849Eb68C9f1c0B92D48C2889",
            "callType": "call",
            "gas": 30547,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000864d77785594ca373f64ae773b4c7a5fd0fc15d9000000000000000000000000000000000000000000000000000000000165aa80"
            ),
            "to": "0x888888848B652B3E3a0f34c96E00EEC0F3a23F72",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30547,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x6095a3a6e9d6444901e9d66abb6a48cda862d7770ef319e8ed8c5be4ee9e772f"
        ),
        "transactionPosition": 87,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0e9B3bDC2Ad4CDa19c1a1E87B70E40C1fAA70103",
            "callType": "call",
            "gas": 460178,
            "input": HexBytes(
                "0x9a2b8115000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000007a919134c04000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000010a4bcb00e2a000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000008c0000000000000000000000000000000000000000000000000003c6568f12e8000000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000007c4357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000005800000000000000000000000000000000000000000000000000001442a668038da0000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba20000000000000000000000000000000000000000000000000000000000000000937dce60c0607487ab48e8940888e0126e20895d36d0fb34ff61fd5bf290607a75ce861c356fc18ea3c95aeacd97fda964599ed5e55bbfca4c3b76f17d4444e5000000000000000000000000000000000000000000000000000000000000001b0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000852cd374bd4a959bab1cde357eee70a40000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000633544cc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c076154ff00cf910c8ce2f3b67bd9b496205b2e585d6f304478368c0d702d5e8153d541a06a4ea5a942fc877429cbdb26d08d5ea225988a4481f4efad04794b27d000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000354a6ba7a18000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008a000000000000000000000000000000000000000000000000003c6568f12e8000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000003c6568f12e80009a3d1fd36a96fc3997cae2aa27d09d2f272561a88e1737e5de8a71315fcaf608000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e2c284391c000000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000006c4357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000004800000000000000000000000000000000000000000000000000000acf9dd96d2c80000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000000041b33bb943baf52b1809711cecd805a2c9ff0d811f8ff88c77a6626407eb83e463c5cdab7a45ee31550d2242fd51b799889b97249409295c5f38b7b213765108000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000006d4951d3ca876c4d680448dfbdcb651500000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000635b80bd000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c094ad694e53a2a6802023b2a97afcf3489f46b2afc0f4642b627c9ae8cce959aa3e72370dbcb40a33a99e4c6e232527b1e9100d7958085d681e42e57570e8ec87000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000003e2c284391c000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e2c284391c000445cdd01dba01567c9168748699323dc53f6352df130f4c2b8fa4c2c2e189b6b000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "value": 34500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 405658, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "callType": "staticcall",
            "gas": 440886,
            "input": HexBytes(
                "0xb1283e77000000000000000000000000000000000000000000000000000000000000000e"
            ),
            "to": "0xadd91d3EbF809f0058D59Db2AC3632B3ce55f0bA",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 4722,
            "output": HexBytes(
                "0x000000000000000000000000aeb21626259f7980f5dbd08701fbc555265c7b6a00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "callType": "delegatecall",
            "gas": 422800,
            "input": HexBytes(
                "0xbcb00e2a000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000008c0000000000000000000000000000000000000000000000000003c6568f12e8000000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000007c4357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000005800000000000000000000000000000000000000000000000000001442a668038da0000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba20000000000000000000000000000000000000000000000000000000000000000937dce60c0607487ab48e8940888e0126e20895d36d0fb34ff61fd5bf290607a75ce861c356fc18ea3c95aeacd97fda964599ed5e55bbfca4c3b76f17d4444e5000000000000000000000000000000000000000000000000000000000000001b0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000852cd374bd4a959bab1cde357eee70a40000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000633544cc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c076154ff00cf910c8ce2f3b67bd9b496205b2e585d6f304478368c0d702d5e8153d541a06a4ea5a942fc877429cbdb26d08d5ea225988a4481f4efad04794b27d000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000354a6ba7a18000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008a000000000000000000000000000000000000000000000000003c6568f12e8000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000003c6568f12e80009a3d1fd36a96fc3997cae2aa27d09d2f272561a88e1737e5de8a71315fcaf608000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e2c284391c000000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000006c4357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000004800000000000000000000000000000000000000000000000000000acf9dd96d2c80000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000000041b33bb943baf52b1809711cecd805a2c9ff0d811f8ff88c77a6626407eb83e463c5cdab7a45ee31550d2242fd51b799889b97249409295c5f38b7b213765108000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000006d4951d3ca876c4d680448dfbdcb651500000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000635b80bd000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c094ad694e53a2a6802023b2a97afcf3489f46b2afc0f4642b627c9ae8cce959aa3e72370dbcb40a33a99e4c6e232527b1e9100d7958085d681e42e57570e8ec87000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000003e2c284391c000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e2c284391c000445cdd01dba01567c9168748699323dc53f6352df130f4c2b8fa4c2c2e189b6b000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xAeB21626259f7980F5dBD08701FBC555265C7b6a",
            "value": 34500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 374609, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "callType": "call",
            "gas": 399181,
            "input": HexBytes(
                "0x357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000005800000000000000000000000000000000000000000000000000001442a668038da0000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba20000000000000000000000000000000000000000000000000000000000000000937dce60c0607487ab48e8940888e0126e20895d36d0fb34ff61fd5bf290607a75ce861c356fc18ea3c95aeacd97fda964599ed5e55bbfca4c3b76f17d4444e5000000000000000000000000000000000000000000000000000000000000001b0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000852cd374bd4a959bab1cde357eee70a40000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000633544cc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c076154ff00cf910c8ce2f3b67bd9b496205b2e585d6f304478368c0d702d5e8153d541a06a4ea5a942fc877429cbdb26d08d5ea225988a4481f4efad04794b27d000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000354a6ba7a18000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008a000000000000000000000000000000000000000000000000003c6568f12e8000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000003c6568f12e80009a3d1fd36a96fc3997cae2aa27d09d2f272561a88e1737e5de8a71315fcaf608000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd"
            ),
            "to": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "value": 17000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 160460, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "delegatecall",
            "gas": 385404,
            "input": HexBytes(
                "0x357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000005800000000000000000000000000000000000000000000000000001442a668038da0000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba20000000000000000000000000000000000000000000000000000000000000000937dce60c0607487ab48e8940888e0126e20895d36d0fb34ff61fd5bf290607a75ce861c356fc18ea3c95aeacd97fda964599ed5e55bbfca4c3b76f17d4444e5000000000000000000000000000000000000000000000000000000000000001b0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000852cd374bd4a959bab1cde357eee70a40000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000633544cc000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c076154ff00cf910c8ce2f3b67bd9b496205b2e585d6f304478368c0d702d5e8153d541a06a4ea5a942fc877429cbdb26d08d5ea225988a4481f4efad04794b27d000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000354a6ba7a18000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008a000000000000000000000000000000000000000000000000003c6568f12e8000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000003c6568f12e80009a3d1fd36a96fc3997cae2aa27d09d2f272561a88e1737e5de8a71315fcaf608000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd"
            ),
            "to": "0x6D7812d41A08BC2a910B562d8B56411964A4eD88",
            "value": 17000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 152762, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [1, 0, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "staticcall",
            "gas": 341650,
            "input": HexBytes("0x2c436e5b"),
            "to": "0xF849de01B080aDC3A814FaBE1E2087475cF2E354",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 281,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 0, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "call",
            "gas": 340127,
            "input": HexBytes(
                "0xbc553f0f0000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad00000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000008b"
            ),
            "to": "0xF849de01B080aDC3A814FaBE1E2087475cF2E354",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 55995,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 0, 0, 1],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF849de01B080aDC3A814FaBE1E2087475cF2E354",
            "callType": "call",
            "gas": 327872,
            "input": HexBytes(
                "0x42842e0e0000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad00000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000008b"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 48707, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 0, 0, 1, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "callType": "call",
            "gas": 275950,
            "input": HexBytes(
                "0x150b7a02000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e3540000000000000000000000005b61824a3dce92a045697a6728b14578ce80f6ad000000000000000000000000000000000000000000000000000000000000008b00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 793,
            "output": HexBytes(
                "0x150b7a0200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0, 0, 1, 0, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "call",
            "gas": 274917,
            "input": HexBytes("0x"),
            "to": "0xD823C605807cC5E6Bd6fC0d7e4eEa50d3e2d66cd",
            "value": 85000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 55, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 0, 2],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "call",
            "gas": 263193,
            "input": HexBytes("0x"),
            "to": "0x5B61824a3DCe92A045697A6728B14578CE80F6AD",
            "value": 16915000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0, 0, 3],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "callType": "call",
            "gas": 240573,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba20000000000000000000000000e9b3bdc2ad4cda19c1a1e87b70e40c1faa70103000000000000000000000000000000000000000000000000000000000000008b"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 28791, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "callType": "call",
            "gas": 201143,
            "input": HexBytes(
                "0x357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000004800000000000000000000000000000000000000000000000000000acf9dd96d2c80000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000000041b33bb943baf52b1809711cecd805a2c9ff0d811f8ff88c77a6626407eb83e463c5cdab7a45ee31550d2242fd51b799889b97249409295c5f38b7b213765108000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000006d4951d3ca876c4d680448dfbdcb651500000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000635b80bd000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c094ad694e53a2a6802023b2a97afcf3489f46b2afc0f4642b627c9ae8cce959aa3e72370dbcb40a33a99e4c6e232527b1e9100d7958085d681e42e57570e8ec87000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000003e2c284391c000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e2c284391c000445cdd01dba01567c9168748699323dc53f6352df130f4c2b8fa4c2c2e189b6b000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd"
            ),
            "to": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "value": 17500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 148401, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "delegatecall",
            "gas": 196908,
            "input": HexBytes(
                "0x357a150b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000004800000000000000000000000000000000000000000000000000000acf9dd96d2c80000000000000000000000000000000000000000000000000000000063341e790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000000041b33bb943baf52b1809711cecd805a2c9ff0d811f8ff88c77a6626407eb83e463c5cdab7a45ee31550d2242fd51b799889b97249409295c5f38b7b213765108000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000006d4951d3ca876c4d680448dfbdcb651500000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000635b80bd000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c094ad694e53a2a6802023b2a97afcf3489f46b2afc0f4642b627c9ae8cce959aa3e72370dbcb40a33a99e4c6e232527b1e9100d7958085d681e42e57570e8ec87000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000003e2c284391c000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e2c284391c000445cdd01dba01567c9168748699323dc53f6352df130f4c2b8fa4c2c2e189b6b000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000001388000000000000000000000000d823c605807cc5e6bd6fc0d7e4eea50d3e2d66cd"
            ),
            "to": "0x6D7812d41A08BC2a910B562d8B56411964A4eD88",
            "value": 17500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 147253, "output": HexBytes("0x")},
        "subtraces": 4,
        "traceAddress": [1, 2, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "staticcall",
            "gas": 167886,
            "input": HexBytes("0x2c436e5b"),
            "to": "0xF849de01B080aDC3A814FaBE1E2087475cF2E354",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 281,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 0, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "call",
            "gas": 166363,
            "input": HexBytes(
                "0xbc553f0f00000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d00000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f26000000000000000000000000000000000000000000000000000000000000002b"
            ),
            "to": "0xF849de01B080aDC3A814FaBE1E2087475cF2E354",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 66961,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1, 2, 0, 1],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF849de01B080aDC3A814FaBE1E2087475cF2E354",
            "callType": "call",
            "gas": 161253,
            "input": HexBytes(
                "0x42842e0e00000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d00000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba2000000000000000000000000000000000000000000000000000000000000002b"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 64173, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 2, 0, 1, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "callType": "call",
            "gas": 96710,
            "input": HexBytes(
                "0x150b7a02000000000000000000000000f849de01b080adc3a814fabe1e2087475cf2e35400000000000000000000000096707ebb51fe5a0de19e90e66058d111a348b42d000000000000000000000000000000000000000000000000000000000000002b00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 793,
            "output": HexBytes(
                "0x150b7a0200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2, 0, 1, 0, 0],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "call",
            "gas": 92820,
            "input": HexBytes("0x"),
            "to": "0xD823C605807cC5E6Bd6fC0d7e4eEa50d3e2d66cd",
            "value": 87500000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 55, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 2, 0, 2],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x74312363e45DCaBA76c59ec49a7Aa8A65a67EeD3",
            "callType": "call",
            "gas": 83065,
            "input": HexBytes("0x"),
            "to": "0x96707eBB51FE5a0dE19E90E66058D111A348b42D",
            "value": 17412500000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 2, 0, 3],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83C8F28c26bF6aaca652Df1DbBE0e1b56F8baBa2",
            "callType": "call",
            "gas": 54406,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000083c8f28c26bf6aaca652df1dbbe0e1b56f8baba20000000000000000000000000e9b3bdc2ad4cda19c1a1e87b70e40c1faa70103000000000000000000000000000000000000000000000000000000000000002b"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 6891, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 3],
        "transactionHash": HexBytes(
            "0x55a3788904325310606d880fc3b68094eb916aed5aae56dddf4fd3b89fd11a3a"
        ),
        "transactionPosition": 88,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2D28eaC15fB119a78900fa08B17CddA18f7fb5EC",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0xE905b9c4415cAb3654cb730F588c1a4aC29C59c1",
            "value": 50000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x01f3743105a053d772c45a726f91919344cd093bbe448ba2c1cca4527151357b"
        ),
        "transactionPosition": 89,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc03e957cebAABec10ccbA9C3271d10EdeA20073e",
            "callType": "call",
            "gas": 139431,
            "input": HexBytes(
                "0xfb0f3ee1000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004020611e32200000000000000000000000000062b261590e0d65285b194948b37eeaade9c8b888000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c0000000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f2600000000000000000000000000000000000000000000000000000000000000dc00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333f3f300000000000000000000000000000000000000000000000000000000635b80f40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002a0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002e000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000001b0028e44b0000000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000001b0028e44b00000000000000000000000000067c86de418948c7a5d72b7f664b551c5f95e274e0000000000000000000000000000000000000000000000000000000000000041baad6522fe4f325eee64b02f4eb8587569a900957cf30d4759e9597480d6acd277cb84c8ab8513cbe3de6b9e445a6b69aa84d297e1a7ab8d5532e99c8ca0498d1c00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 19000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 137260,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 5,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "staticcall",
            "gas": 116180,
            "input": HexBytes(
                "0x0e1d31dc4c98b72308d658b56c06a929c6791ca92d00f414faf9dd10dbc333a05ffa4ea7000000000000000000000000c03e957cebaabec10ccba9c3271d10edea20073e00000000000000000000000062b261590e0d65285b194948b37eeaade9c8b8880000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x004C00500000aD104D7DBd00e3ae0A5C00560C00",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 257,
            "output": HexBytes(
                "0x0e1d31dc00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 86247,
            "input": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000016d1884381d94b372e6020a28bf41bbabe8c1f2600000000000000000000000062b261590e0d65285b194948b37eeaade9c8b888000000000000000000000000c03e957cebaabec10ccba9c3271d10edea20073e00000000000000000000000000000000000000000000000000000000000000dc0000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 56034,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 78993,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000062b261590e0d65285b194948b37eeaade9c8b888000000000000000000000000c03e957cebaabec10ccba9c3271d10edea20073e00000000000000000000000000000000000000000000000000000000000000dc"
            ),
            "to": "0x16d1884381d94B372e6020a28BF41BBaBe8C1F26",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 49918, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 21310,
            "input": HexBytes("0x"),
            "to": "0x0000a26b00c1F0DF003000390027140000fAa719",
            "value": 475000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 85, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 11718,
            "input": HexBytes("0x"),
            "to": "0x67C86dE418948C7a5d72b7f664b551C5F95e274e",
            "value": 475000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 2373,
            "input": HexBytes("0x"),
            "to": "0x62B261590e0D65285b194948B37eEAaDE9C8B888",
            "value": 18050000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0xd3e569ea90565e790bc87900f674290be212c552d25bb413f600e1fe169209dd"
        ),
        "transactionPosition": 90,
        "type": "call",
    },
    {
        "action": {
            "from": "0x26A548330E548cE1b938DaC9f5130222f522b5e4",
            "callType": "call",
            "gas": 0,
            "input": HexBytes("0x"),
            "to": "0x0F8922e5C5ccC3fa8B9F7f13f3189Ca7397721f9",
            "value": 60771415537162015,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x933463ae7b1fc39d4f252d31c938b5a9d768d01f521d3b254ae116de2764a6d6"
        ),
        "transactionPosition": 91,
        "type": "call",
    },
    {
        "action": {
            "from": "0x108954d73D674997EEbaeb96CefAC4a41744D188",
            "callType": "call",
            "gas": 118862,
            "input": HexBytes(
                "0xa0712d6800000000000000000000000000000000000000000000000000000000000000cb"
            ),
            "to": "0xcb6B570B8AeAbE38B449Aff31f901B8E1B91e396",
            "value": 253000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "error": "Reverted",
        "result": {
            "gasUsed": 30842,
            "output": HexBytes(
                "0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001c4552433732313a20746f6b656e20616c7265616479206d696e74656400000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x5327768b86412dc5a79b2c38a3780e61aa13894875f154d2aa275bc75e32c606"
        ),
        "transactionPosition": 92,
        "type": "call",
    },
    {
        "action": {
            "from": "0x258bC09d202e4b62fA8D84B1CdCfd06c9Dc7429B",
            "callType": "call",
            "gas": 24615,
            "input": HexBytes(
                "0xa22cb4650000000000000000000000001e0049783f008a0085193e00003d00cd54003c710000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x34Bc797F40Df0445c8429d485232874B15561728",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24615, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x255c5f1233a9c41794535147e6b7d00db8f45f10f2e95779108214ab2c7730b1"
        ),
        "transactionPosition": 93,
        "type": "call",
    },
    {
        "action": {
            "from": "0xf3140BDbC0C880c3eE641aD72cF445D354A59012",
            "callType": "call",
            "gas": 128783,
            "input": HexBytes(
                "0xfb0f3ee10000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000152edcb679280000000000000000000000000007eb77bfd9afc2046053619464194132ad2c63c65000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000dcf68c8ebb18df1419c7dff17ed33505faf8a20c000000000000000000000000000000000000000000000000000000000000050200000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333f22500000000000000000000000000000000000000000000000000000000635b7f250000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000d5afb58f4e1adbfe0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002e0000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000096a2934a7a0000000000000000000000000000000a26b00c1f0df003000390027140000faa719000000000000000000000000000000000000000000000000001c3e7b9df6e0000000000000000000000000004e5a0d50de3675b70cff0fab90c8960ade6a93ab000000000000000000000000000000000000000000000000000000000000004115002781e0b70a8751b75afbbebea027d4e13a14d4580e4e064b94573e19caf205a9094da325d1d95d3211118001c3c491b150adf023f7299d3244f3ca2b06421b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 106000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 126612,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 5,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "staticcall",
            "gas": 105699,
            "input": HexBytes(
                "0x0e1d31dc666cfc8249d1bd06f0859946c6891d5b7ffc3dac55a9873c99eb4bcb645084dc000000000000000000000000f3140bdbc0c880c3ee641ad72cf445d354a590120000000000000000000000007eb77bfd9afc2046053619464194132ad2c63c650000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x004C00500000aD104D7DBd00e3ae0A5C00560C00",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 257,
            "output": HexBytes(
                "0x0e1d31dc00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 75766,
            "input": HexBytes(
                "0x4ce34aa2000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000dcf68c8ebb18df1419c7dff17ed33505faf8a20c0000000000000000000000007eb77bfd9afc2046053619464194132ad2c63c65000000000000000000000000f3140bdbc0c880c3ee641ad72cf445d354a5901200000000000000000000000000000000000000000000000000000000000005020000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 39057,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 68675,
            "input": HexBytes(
                "0x23b872dd0000000000000000000000007eb77bfd9afc2046053619464194132ad2c63c65000000000000000000000000f3140bdbc0c880c3ee641ad72cf445d354a590120000000000000000000000000000000000000000000000000000000000000502"
            ),
            "to": "0xDCf68c8eBB18Df1419C7DFf17ed33505Faf8A20C",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 32941, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 27540,
            "input": HexBytes("0x"),
            "to": "0x0000a26b00c1F0DF003000390027140000fAa719",
            "value": 2650000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 85, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 17948,
            "input": HexBytes("0x"),
            "to": "0x4E5a0d50De3675b70Cff0FAB90C8960aDE6A93AB",
            "value": 7950000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 6329, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4E5a0d50De3675b70Cff0FAB90C8960aDE6A93AB",
            "callType": "delegatecall",
            "gas": 12960,
            "input": HexBytes("0x"),
            "to": "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            "value": 7950000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 1504, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 2373,
            "input": HexBytes("0x"),
            "to": "0x7EB77BfD9AFC2046053619464194132AD2c63c65",
            "value": 95400000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x5dcf7fc06962ebc0ceec7c661099bb9f2f318757bf5972334e126b0bc728ff87"
        ),
        "transactionPosition": 94,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB59bff945A74a427c74Fb27Ae423fCF81Da27c24",
            "callType": "call",
            "gas": 140774,
            "input": HexBytes(
                "0xfb90b320000000000000000000000000ecdb63c30d46e8c86bf1292fa7d4519535b161c3000000000000000000000000000000000000000000000000000000000000611c"
            ),
            "to": "0xFfa397285Ce46FB78C588a9e993286AaC68c37cD",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 70774, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xbbbbb6c3d6bda93e291f424649832ac28143649b52e6406f43e696f29f582421"
        ),
        "transactionPosition": 95,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFfa397285Ce46FB78C588a9e993286AaC68c37cD",
            "gas": 104430,
            "init": HexBytes(
                "0x3d602d80600a3d3981f3363d3d373d3d3d363d73059ffafdc6ef594230de44f824e2bd0a51ca5ded5af43d82803e903d91602b57fd5bf3"
            ),
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "address": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "code": HexBytes(
                "0x363d3d373d3d3d363d73059ffafdc6ef594230de44f824e2bd0a51ca5ded5af43d82803e903d91602b57fd5bf3"
            ),
            "gasUsed": 9031,
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xbbbbb6c3d6bda93e291f424649832ac28143649b52e6406f43e696f29f582421"
        ),
        "transactionPosition": 95,
        "type": "create",
    },
    {
        "action": {
            "from": "0xFfa397285Ce46FB78C588a9e993286AaC68c37cD",
            "callType": "call",
            "gas": 95177,
            "input": HexBytes(
                "0x19ab453c000000000000000000000000ecdb63c30d46e8c86bf1292fa7d4519535b161c3"
            ),
            "to": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 25290, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xbbbbb6c3d6bda93e291f424649832ac28143649b52e6406f43e696f29f582421"
        ),
        "transactionPosition": 95,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "callType": "delegatecall",
            "gas": 91096,
            "input": HexBytes(
                "0x19ab453c000000000000000000000000ecdb63c30d46e8c86bf1292fa7d4519535b161c3"
            ),
            "to": "0x059FFAFdC6eF594230dE44F824E2bD0A51CA5dED",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 22621, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0xbbbbb6c3d6bda93e291f424649832ac28143649b52e6406f43e696f29f582421"
        ),
        "transactionPosition": 95,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe3E0596AC55Ae6044b757baB27426F7dC9e018d4",
            "callType": "call",
            "gas": 708016,
            "input": HexBytes(
                "0xc9807539000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000003200000000000000000000000000000000000000000000000000000000000000400010100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002800000000000000000000000fdbbdb75150c57aeca759e59855f1a380001eff00402030408090d010b0a070e050c00060f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000001e6971e7000000000000000000000000000000000000000000000000000000001e6971e7000000000000000000000000000000000000000000000000000000001e6971e7000000000000000000000000000000000000000000000000000000001e69caea000000000000000000000000000000000000000000000000000000001e69caea000000000000000000000000000000000000000000000000000000001e6bac54000000000000000000000000000000000000000000000000000000001e6bac54000000000000000000000000000000000000000000000000000000001e6bac54000000000000000000000000000000000000000000000000000000001e727466000000000000000000000000000000000000000000000000000000001e74bd35000000000000000000000000000000000000000000000000000000001e7628bd000000000000000000000000000000000000000000000000000000001e79dc57000000000000000000000000000000000000000000000000000000001e7f0ea7000000000000000000000000000000000000000000000000000000001e8771d3000000000000000000000000000000000000000000000000000000001e8771d3000000000000000000000000000000000000000000000000000000001e8771d300000000000000000000000000000000000000000000000000000000000000069aa926428fccd8977bcb6b11035c187e97ee848c5adb189ed174491b9b06023d9632e89194313abb8ca2141807171b8445da8bd343fd82b2a072dcf0d9540e9b685dc31daf22087673024ac91f7ea567f5695052974a415ceb8cade87b1543bd25c5d1bae1d24697ebd9ad3a906178302a030841bf8dc8d36d01c1b2671aa205151dca68d41d948c3e55a32d478b7547606abadc0cf75a9ff27985996b7cd43a911f3c5ac6eb80669f35c20e7fd7c5ffe4fa3e7184e226545dbcbeae8cd10f4a000000000000000000000000000000000000000000000000000000000000000678eef8eb9c42c8cc6025ffc2a19f9addea104d4b0fe8e08a269511f05444480f26f5925d3fba3538e5f8a25bc8fc9da702b136708def12df0503c96873ad84ef1c3f98959954de0100670a69067fc1c302f4e322441a090f0e9e1e0fdb9ae1b94fda056891a8fbea5b3e35bf49cc700957a2f2bbb2e0aec2aec91672eca9a1a07cdd0091038349fdbfcde7a631d2f944a0ed92391b8b2bc841bcb124ac627a3274940dc5e5311b01114be956436868efcb4fbf7b24e09096659f75d7b195f545"
            ),
            "to": "0xbd9350a3a2fd6e3Ad0a053a567f2609a1bf6c505",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 144515, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x09424eb20228cd916606a02acdb6f1d182249a5950a73282c8197780b5491b16"
        ),
        "transactionPosition": 96,
        "type": "call",
    },
    {
        "action": {
            "from": "0x10e163Df55fFD8C19332CC5FbFdd3135bB31a243",
            "callType": "call",
            "gas": 56900,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000004f5febe16e4238c9ed1b5ed8cca8bf2d08a3d1da0000000000000000000000000000000000000000000007aa67eb2c2e14a00000"
            ),
            "to": "0x12b6893cE26Ea6341919FE289212ef77e51688c8",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30715,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa76abd7792a83a4b898f2058c2406840ccc59451d99b12e56653b4c7b2b01900"
        ),
        "transactionPosition": 97,
        "type": "call",
    },
    {
        "action": {
            "from": "0xB59bff945A74a427c74Fb27Ae423fCF81Da27c24",
            "callType": "call",
            "gas": 478200,
            "input": HexBytes(
                "0x2da034090000000000000000000000000304536d9ed7fe3abd2076f913a994dc84e939c4000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7"
            ),
            "to": "0xecdB63C30D46e8c86bf1292fA7D4519535b161c3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 47948, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x105e7cf0b25cd24261c036abc2b46a5936eea632eb96de89c63e616f8b3be881"
        ),
        "transactionPosition": 98,
        "type": "call",
    },
    {
        "action": {
            "from": "0xecdB63C30D46e8c86bf1292fA7D4519535b161c3",
            "callType": "call",
            "gas": 457673,
            "input": HexBytes(
                "0x3ef13367000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7"
            ),
            "to": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 34644, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x105e7cf0b25cd24261c036abc2b46a5936eea632eb96de89c63e616f8b3be881"
        ),
        "transactionPosition": 98,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "callType": "delegatecall",
            "gas": 447928,
            "input": HexBytes(
                "0x3ef13367000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec7"
            ),
            "to": "0x059FFAFdC6eF594230dE44F824E2bD0A51CA5dED",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 31975, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x105e7cf0b25cd24261c036abc2b46a5936eea632eb96de89c63e616f8b3be881"
        ),
        "transactionPosition": 98,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "callType": "staticcall",
            "gas": 435734,
            "input": HexBytes(
                "0x70a082310000000000000000000000000304536d9ed7fe3abd2076f913a994dc84e939c4"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 5031,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000004c4b40"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0x105e7cf0b25cd24261c036abc2b46a5936eea632eb96de89c63e616f8b3be881"
        ),
        "transactionPosition": 98,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0304536d9Ed7fE3aBD2076f913a994DC84E939C4",
            "callType": "call",
            "gas": 429793,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000ecdb63c30d46e8c86bf1292fa7d4519535b161c300000000000000000000000000000000000000000000000000000000004c4b40"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 20501, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0, 1],
        "transactionHash": HexBytes(
            "0x105e7cf0b25cd24261c036abc2b46a5936eea632eb96de89c63e616f8b3be881"
        ),
        "transactionPosition": 98,
        "type": "call",
    },
    {
        "action": {
            "from": "0x441aD8454FE01cA70402D69b73fC7D7fc2299857",
            "callType": "call",
            "gas": 119134,
            "input": HexBytes(
                "0xfb0f3ee1000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030f5f94ecf94000000000000000000000000000ef134569ec50879f253411c42149ec09638e69fd000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c000000000000000000000000003727ac93ed1ff0472ec91619cfaa011f76a5baae000000000000000000000000000000000000000000000000000000000000110700000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006332600e000000000000000000000000000000000000000000000000000000006359ed0e0000000000000000000000000000000000000000000000000000000000000000360c6ebe000000000000000000000000000000000000000079371e3299f47f650000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002e000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000015c2a7b13fd0000000000000000000000000000000a26b00c1f0df003000390027140000faa719000000000000000000000000000000000000000000000000004147f713bf70000000000000000000000000008d207b47a26fd218b99f97f171353e448960bfc9000000000000000000000000000000000000000000000000000000000000004154603c8825c5587da4291ad4083a7ccbf02a8014f9771da687da69d5c45e887b3c2ecd2729c35e6e7103e6f8634a8deb69de92f542ad4aaeb3978e98557b6ead1b00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 245000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 116963,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 5,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "staticcall",
            "gas": 96201,
            "input": HexBytes(
                "0x0e1d31dcee980086f6c3b9878113b148263e15e5bedf1bb9d7ad259b403875fc313392fb000000000000000000000000441ad8454fe01ca70402d69b73fc7d7fc2299857000000000000000000000000ef134569ec50879f253411c42149ec09638e69fd0000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x004C00500000aD104D7DBd00e3ae0A5C00560C00",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 257,
            "output": HexBytes(
                "0x0e1d31dc00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 66268,
            "input": HexBytes(
                "0x4ce34aa20000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000003727ac93ed1ff0472ec91619cfaa011f76a5baae000000000000000000000000ef134569ec50879f253411c42149ec09638e69fd000000000000000000000000441ad8454fe01ca70402d69b73fc7d7fc229985700000000000000000000000000000000000000000000000000000000000011070000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 35737,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 59326,
            "input": HexBytes(
                "0x23b872dd000000000000000000000000ef134569ec50879f253411c42149ec09638e69fd000000000000000000000000441ad8454fe01ca70402d69b73fc7d7fc22998570000000000000000000000000000000000000000000000000000000000001107"
            ),
            "to": "0x3727aC93ED1FF0472eC91619CfaA011F76A5BAAe",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 29621, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 21310,
            "input": HexBytes("0x"),
            "to": "0x0000a26b00c1F0DF003000390027140000fAa719",
            "value": 6125000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 85, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 11718,
            "input": HexBytes("0x"),
            "to": "0x8D207b47A26Fd218b99f97f171353e448960BFc9",
            "value": 18375000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 2373,
            "input": HexBytes("0x"),
            "to": "0xEF134569EC50879F253411C42149eC09638E69fD",
            "value": 220500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x0978cbeb211b934581d2d2e5f552c61cef51e564923379f99ad6a80dd841b861"
        ),
        "transactionPosition": 99,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7A4907BDE575123Fb406b3C70BEa0940d03eea2e",
            "callType": "call",
            "gas": 115633,
            "input": HexBytes(
                "0xfb0f3ee1000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f18a03b360000000000000000000000000000a660a7ad59d9529700f13c614403b5929802bae3000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c0000000000000000000000000012b180b635dd9f07a78736fb4e43438fcdb41555000000000000000000000000000000000000000000000000000000000000136e00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006332aaab0000000000000000000000000000000000000000000000000000000063578f640000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000d08c8d595c90e7980000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002e000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000001b48eb57e00000000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000003691d6afc000000000000000000000000000008e07e198ef6d77cd77cfbc4e9366503eadfdeed000000000000000000000000000000000000000000000000000000000000004182ac12cec0351f0d9477a2c90b881b278ea8eb56a26857d0fc221e0763703a5b0c20febed24a4fd2f46042bafc463efa58bb683592e86a90dd01018cbdd6f1e21c00000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 19200000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 113462,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 5,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "staticcall",
            "gas": 92754,
            "input": HexBytes(
                "0x0e1d31dcae2211d6472fbc23ce9eb74b2c2269d1ecfa912fa52452ed4347b6dcd524f7150000000000000000000000007a4907bde575123fb406b3c70bea0940d03eea2e000000000000000000000000a660a7ad59d9529700f13c614403b5929802bae30000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x004C00500000aD104D7DBd00e3ae0A5C00560C00",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 257,
            "output": HexBytes(
                "0x0e1d31dc00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 62821,
            "input": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000012b180b635dd9f07a78736fb4e43438fcdb41555000000000000000000000000a660a7ad59d9529700f13c614403b5929802bae30000000000000000000000007a4907bde575123fb406b3c70bea0940d03eea2e000000000000000000000000000000000000000000000000000000000000136e0000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30831,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 55933,
            "input": HexBytes(
                "0x23b872dd000000000000000000000000a660a7ad59d9529700f13c614403b5929802bae30000000000000000000000007a4907bde575123fb406b3c70bea0940d03eea2e000000000000000000000000000000000000000000000000000000000000136e"
            ),
            "to": "0x12b180b635dD9f07a78736fB4E43438fcdb41555",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 24715, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 22693,
            "input": HexBytes("0x"),
            "to": "0x0000a26b00c1F0DF003000390027140000fAa719",
            "value": 480000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 85, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 13101,
            "input": HexBytes("0x"),
            "to": "0x08E07e198eF6d77cd77cFBC4E9366503EADfDEed",
            "value": 960000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 1405, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 2373,
            "input": HexBytes("0x"),
            "to": "0xA660a7AD59D9529700f13c614403B5929802Bae3",
            "value": 17760000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0xebbe947f3619e7001cd9997f61f16acfd545b5074c84fad092e5a2b363c05512"
        ),
        "transactionPosition": 100,
        "type": "call",
    },
    {
        "action": {
            "from": "0x845Aa04Faf21F7d445632Cdb85750322553A1395",
            "callType": "call",
            "gas": 51568,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f8f3c1dbc6575874b2c0bcaea553b05d2600cfe600000000000000000000000000000000000000000000000000000000b2d05e00"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 26917,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x80f46ae07bde59613b16e0ba77882743390b6eb682410a30c780a3288810ea84"
        ),
        "transactionPosition": 101,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 43631,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000f8f3c1dbc6575874b2c0bcaea553b05d2600cfe600000000000000000000000000000000000000000000000000000000b2d05e00"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 19628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x80f46ae07bde59613b16e0ba77882743390b6eb682410a30c780a3288810ea84"
        ),
        "transactionPosition": 101,
        "type": "call",
    },
    {
        "action": {
            "from": "0x6A0Ac34A3726daFF83a83E5e454A4a976e33FFac",
            "callType": "call",
            "gas": 29799,
            "input": HexBytes(
                "0x4b14557e0000000000000000000000006a0ac34a3726daff83a83e5e454a4a976e33ffac000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001158e460913d00000"
            ),
            "to": "0x64192819Ac13Ef72bF6b5AE239AC672B43a9AF08",
            "value": 20000000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 29486, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xfe4632252c3a16367eadbea91e279e6d36a3cc25976d54758f466b46dcd18803"
        ),
        "transactionPosition": 102,
        "type": "call",
    },
    {
        "action": {
            "from": "0x64192819Ac13Ef72bF6b5AE239AC672B43a9AF08",
            "callType": "delegatecall",
            "gas": 22170,
            "input": HexBytes(
                "0x4b14557e0000000000000000000000006a0ac34a3726daff83a83e5e454a4a976e33ffac000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001158e460913d00000"
            ),
            "to": "0x71356E37e0368Bd10bFDbF41dC052fE5FA24cD05",
            "value": 20000000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 22170, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xfe4632252c3a16367eadbea91e279e6d36a3cc25976d54758f466b46dcd18803"
        ),
        "transactionPosition": 102,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9077f38Ad1E19a15153e2316Ad9Edb9399a06696",
            "callType": "call",
            "gas": 101392,
            "input": HexBytes(
                "0xec91be730000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0xE6A0bD3C8d6f664a6a1D1Ff70e723d352804A2f4",
            "value": 70000000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 60527, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8da3b9c6101c5aa3606595adb35c1be3c175656596ae4509b9583b71ff59995f"
        ),
        "transactionPosition": 103,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7Ec084f5975a49c5A1E7D3C5870D877d8F98d4Ca",
            "callType": "call",
            "gas": 31375,
            "input": HexBytes(
                "0x095ea7b30000000000000000000000001111111254fb6c44bac0bed2854e76f90643097dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 24420,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xe7af46ff8f590b99f434e17a4f4bef83fbcd0c813fc880169ba10e2b7f9d259e"
        ),
        "transactionPosition": 104,
        "type": "call",
    },
    {
        "action": {
            "from": "0x33be5E9723187141A089432dA6D1583aC14Bbcc4",
            "callType": "call",
            "gas": 187348,
            "input": HexBytes(
                "0x32389b7100000000000000000000000000000000000000000000000000000000000000400000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000060000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000070000000000000000000000000000000000000000000000000000000000000002000000000000000000000000209e639a0ec166ac7a1a4ba41968fa967db30221000000000000000000000000000000000000000000000000000000000000120400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000209e639a0ec166ac7a1a4ba41968fa967db3022100000000000000000000000000000000000000000000000000000000000016ab00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f30000000000000000000000000000000000000000000000000000000000000a0400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000000000000000000000000000000000000000000fe00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f3000000000000000000000000000000000000000000000000000000000000069600000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f3000000000000000000000000000000000000000000000000000000000000011b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000000000000000000000000000000000000000008840000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x0000000000c2d145a2526bD8C716263bFeBe1A72",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 184996,
            "output": HexBytes(
                "0x32389b7100000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0000000000c2d145a2526bD8C716263bFeBe1A72",
            "callType": "call",
            "gas": 165597,
            "input": HexBytes(
                "0x4ce34aa2000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000070000000000000000000000000000000000000000000000000000000000000002000000000000000000000000209e639a0ec166ac7a1a4ba41968fa967db3022100000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f000000000000000000000000000000000000000000000000000000000000120400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000209e639a0ec166ac7a1a4ba41968fa967db3022100000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f00000000000000000000000000000000000000000000000000000000000016ab00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f0000000000000000000000000000000000000000000000000000000000000a0400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f00000000000000000000000000000000000000000000000000000000000000fe00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f000000000000000000000000000000000000000000000000000000000000069600000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f000000000000000000000000000000000000000000000000000000000000011b00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000fde881c7b76ad10b59a82247e1cd3cbad0d739f300000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f00000000000000000000000000000000000000000000000000000000000008840000000000000000000000000000000000000000000000000000000000000001"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 165477,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 7,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 157103,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f0000000000000000000000000000000000000000000000000000000000001204"
            ),
            "to": "0x209e639a0EC166Ac7a1A4bA41968fa967dB30221",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 29627, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 126879,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f00000000000000000000000000000000000000000000000000000000000016ab"
            ),
            "to": "0x209e639a0EC166Ac7a1A4bA41968fa967dB30221",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 16027, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 107581,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f0000000000000000000000000000000000000000000000000000000000000a04"
            ),
            "to": "0xFDe881c7B76ad10B59a82247E1cD3CBAd0d739F3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 45509, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 2],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 61723,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f00000000000000000000000000000000000000000000000000000000000000fe"
            ),
            "to": "0xFDe881c7B76ad10B59a82247E1cD3CBAd0d739F3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14809, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 3],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 46085,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f0000000000000000000000000000000000000000000000000000000000000696"
            ),
            "to": "0xFDe881c7B76ad10B59a82247E1cD3CBAd0d739F3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14809, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 4],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 30447,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f000000000000000000000000000000000000000000000000000000000000011b"
            ),
            "to": "0xFDe881c7B76ad10B59a82247E1cD3CBAd0d739F3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14809, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 5],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 14809,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000033be5e9723187141a089432da6d1583ac14bbcc4000000000000000000000000689fd9a89c8ac640ee7ce6d1132447e68191e61f0000000000000000000000000000000000000000000000000000000000000884"
            ),
            "to": "0xFDe881c7B76ad10B59a82247E1cD3CBAd0d739F3",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 14809, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 6],
        "transactionHash": HexBytes(
            "0x8f14db912558c6ea8e4aac57d92e3dc907409b4a3b5745989dfb4ef05658d3a7"
        ),
        "transactionPosition": 105,
        "type": "call",
    },
    {
        "action": {
            "from": "0x43e4715ae093a4C86B5eCdDb52216c4f879e9672",
            "callType": "call",
            "gas": 256368,
            "input": HexBytes(
                "0x1cff79cd000000000000000000000000fc588723ead01d032b837229577f6a532e5a0c20000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000c41f3cc1fe0000000000000000000000000000000000000000000000000000000aca87a03400000000000000000000000000000000000000000000000011996b3dff2fb9000000000000000000000000000000000000006db804f4fa6c673cecb87e7d867e0000000000000000000000000000000000000000000000000de0b6b3a7640000000000000000000000000000000000000000000000000000000000006333f4940000000000000000000000000000000000006db9cb19d7e48cb4977f3ae42ebf00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 10245,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "error": "Reverted",
        "result": {"gasUsed": 9506, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xc96ca0a60cede355f1e6a01572c372cb5bfe2ae57ea368824955977983949202"
        ),
        "transactionPosition": 106,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "delegatecall",
            "gas": 248631,
            "input": HexBytes(
                "0x1f3cc1fe0000000000000000000000000000000000000000000000000000000aca87a03400000000000000000000000000000000000000000000000011996b3dff2fb9000000000000000000000000000000000000006db804f4fa6c673cecb87e7d867e0000000000000000000000000000000000000000000000000de0b6b3a7640000000000000000000000000000000000000000000000000000000000006333f4940000000000000000000000000000000000006db9cb19d7e48cb4977f3ae42ebf"
            ),
            "to": "0xfc588723eAD01D032B837229577f6A532e5a0c20",
            "value": 10245,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "error": "Reverted",
        "result": {
            "gasUsed": 5680,
            "output": HexBytes(
                "0x08c379a0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000023135000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xc96ca0a60cede355f1e6a01572c372cb5bfe2ae57ea368824955977983949202"
        ),
        "transactionPosition": 106,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 241971,
            "input": HexBytes("0x3850c7bd"),
            "to": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2696,
            "output": HexBytes(
                "0x0000000000000000000000000000000000006db716140d536c0000016b7fab84000000000000000000000000000000000000000000000000000000000003204700000000000000000000000000000000000000000000000000000000000001f300000000000000000000000000000000000000000000000000000000000002d000000000000000000000000000000000000000000000000000000000000002d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xc96ca0a60cede355f1e6a01572c372cb5bfe2ae57ea368824955977983949202"
        ),
        "transactionPosition": 106,
        "type": "call",
    },
    {
        "action": {
            "from": "0x69181A03fD84D1e2679Eb520DFDE72C97e1Ce524",
            "callType": "call",
            "gas": 399982,
            "input": HexBytes("0x"),
            "to": "0x69181A03fD84D1e2679Eb520DFDE72C97e1Ce524",
            "value": 259,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x3e0cf9f9dd09599dcd4288a08b3cb5fae027c589e85a408ee8426e19efd6a1d1"
        ),
        "transactionPosition": 107,
        "type": "call",
    },
    {
        "action": {
            "from": "0x8b803E4C274933cED6b2b70A2aBf7e6A678d4784",
            "callType": "call",
            "gas": 61715,
            "input": HexBytes(
                "0x3f2e5fc30000000000000000000000008b803e4c274933ced6b2b70a2abf7e6a678d47840000000000000000000000000000000000000000000000000012795f58d50000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000018382f1d90900000000000000000000000000000000000000000000000000000000000147d2"
            ),
            "to": "0x5427FEFA711Eff984124bFBB1AB6fbf5E3DA1820",
            "value": 5200000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 59531, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x1b800abc991f002b6cadcbc7db318d16d9f555741580eb3f57e5fcf4e0cc0288"
        ),
        "transactionPosition": 108,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5427FEFA711Eff984124bFBB1AB6fbf5E3DA1820",
            "callType": "call",
            "gas": 12207,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 5200000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 6874, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x1b800abc991f002b6cadcbc7db318d16d9f555741580eb3f57e5fcf4e0cc0288"
        ),
        "transactionPosition": 108,
        "type": "call",
    },
    {
        "action": {
            "from": "0xe821C366F3091B09D5AB066ceEf038dF63c4781a",
            "callType": "call",
            "gas": 2753576,
            "input": HexBytes(
                "0xd17c1c9f000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000d6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006400000000000000000000000000000000000000000000000000000000000019f90000000000000000000000000000000000000000000000000000000000001a040000000000000000000000000000000000000000000000000000000000001a050000000000000000000000000000000000000000000000000000000000001a060000000000000000000000000000000000000000000000000000000000001a070000000000000000000000000000000000000000000000000000000000001a080000000000000000000000000000000000000000000000000000000000001a090000000000000000000000000000000000000000000000000000000000001a0a0000000000000000000000000000000000000000000000000000000000001a0b0000000000000000000000000000000000000000000000000000000000001a0c0000000000000000000000000000000000000000000000000000000000001a0d0000000000000000000000000000000000000000000000000000000000001a0f0000000000000000000000000000000000000000000000000000000000001a100000000000000000000000000000000000000000000000000000000000001a110000000000000000000000000000000000000000000000000000000000001a120000000000000000000000000000000000000000000000000000000000001a130000000000000000000000000000000000000000000000000000000000001a140000000000000000000000000000000000000000000000000000000000001a150000000000000000000000000000000000000000000000000000000000001a160000000000000000000000000000000000000000000000000000000000001a170000000000000000000000000000000000000000000000000000000000001a180000000000000000000000000000000000000000000000000000000000001a190000000000000000000000000000000000000000000000000000000000001a1a0000000000000000000000000000000000000000000000000000000000001a1b0000000000000000000000000000000000000000000000000000000000001a1c0000000000000000000000000000000000000000000000000000000000001a1d0000000000000000000000000000000000000000000000000000000000001a1e0000000000000000000000000000000000000000000000000000000000001a1f0000000000000000000000000000000000000000000000000000000000001a200000000000000000000000000000000000000000000000000000000000001a210000000000000000000000000000000000000000000000000000000000001a220000000000000000000000000000000000000000000000000000000000001a230000000000000000000000000000000000000000000000000000000000001a240000000000000000000000000000000000000000000000000000000000001a250000000000000000000000000000000000000000000000000000000000001a260000000000000000000000000000000000000000000000000000000000001a270000000000000000000000000000000000000000000000000000000000001a280000000000000000000000000000000000000000000000000000000000001a290000000000000000000000000000000000000000000000000000000000001a2a0000000000000000000000000000000000000000000000000000000000001a2b0000000000000000000000000000000000000000000000000000000000001a2c0000000000000000000000000000000000000000000000000000000000001a2d0000000000000000000000000000000000000000000000000000000000001a2e0000000000000000000000000000000000000000000000000000000000001a2f0000000000000000000000000000000000000000000000000000000000001a300000000000000000000000000000000000000000000000000000000000001a310000000000000000000000000000000000000000000000000000000000001a320000000000000000000000000000000000000000000000000000000000001a330000000000000000000000000000000000000000000000000000000000001a340000000000000000000000000000000000000000000000000000000000001a350000000000000000000000000000000000000000000000000000000000001a360000000000000000000000000000000000000000000000000000000000001a370000000000000000000000000000000000000000000000000000000000001a470000000000000000000000000000000000000000000000000000000000001a480000000000000000000000000000000000000000000000000000000000001a490000000000000000000000000000000000000000000000000000000000001a4a0000000000000000000000000000000000000000000000000000000000001a4b0000000000000000000000000000000000000000000000000000000000001a4c0000000000000000000000000000000000000000000000000000000000001a4d0000000000000000000000000000000000000000000000000000000000001a4e0000000000000000000000000000000000000000000000000000000000001a4f0000000000000000000000000000000000000000000000000000000000001a500000000000000000000000000000000000000000000000000000000000001a510000000000000000000000000000000000000000000000000000000000001a520000000000000000000000000000000000000000000000000000000000001a530000000000000000000000000000000000000000000000000000000000001a540000000000000000000000000000000000000000000000000000000000001a560000000000000000000000000000000000000000000000000000000000001a570000000000000000000000000000000000000000000000000000000000001a580000000000000000000000000000000000000000000000000000000000001a590000000000000000000000000000000000000000000000000000000000001a5a0000000000000000000000000000000000000000000000000000000000001a5b0000000000000000000000000000000000000000000000000000000000001a5c0000000000000000000000000000000000000000000000000000000000001a5d0000000000000000000000000000000000000000000000000000000000001a5e0000000000000000000000000000000000000000000000000000000000001a5f0000000000000000000000000000000000000000000000000000000000001a600000000000000000000000000000000000000000000000000000000000001a610000000000000000000000000000000000000000000000000000000000001a620000000000000000000000000000000000000000000000000000000000001a630000000000000000000000000000000000000000000000000000000000001a640000000000000000000000000000000000000000000000000000000000001a650000000000000000000000000000000000000000000000000000000000001a660000000000000000000000000000000000000000000000000000000000001a670000000000000000000000000000000000000000000000000000000000001a680000000000000000000000000000000000000000000000000000000000001a690000000000000000000000000000000000000000000000000000000000001a6a0000000000000000000000000000000000000000000000000000000000001a6b0000000000000000000000000000000000000000000000000000000000001a6d0000000000000000000000000000000000000000000000000000000000001a6e0000000000000000000000000000000000000000000000000000000000001a6f0000000000000000000000000000000000000000000000000000000000001a700000000000000000000000000000000000000000000000000000000000001a710000000000000000000000000000000000000000000000000000000000001a720000000000000000000000000000000000000000000000000000000000001a730000000000000000000000000000000000000000000000000000000000001a740000000000000000000000000000000000000000000000000000000000001a750000000000000000000000000000000000000000000000000000000000001a760000000000000000000000000000000000000000000000000000000000001a770000000000000000000000000000000000000000000000000000000000001a780000000000000000000000000000000000000000000000000000000000000064000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000000000000000000000000000000000000000000000000f08eaef31e0be600000"
            ),
            "to": "0x7BB5178af214B8c5E714EE29D40045E37Bc89d42",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 2753576, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x3b339b91dfa35453d68ac18d34a0fcb0cbd1ffd92ba1d39cc1a5fd43ecbd1a31"
        ),
        "transactionPosition": 109,
        "type": "call",
    },
    {
        "action": {
            "from": "0x431B5A84aCC1297Eda88259f300262F1bc3A74f3",
            "callType": "call",
            "gas": 228990,
            "input": HexBytes(
                "0x1cff79cd0000000000000000000000004095d53a4cf4dedd3ad40773e474670d9d0b5729000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000c41f3cc1fe0000000000000000000000000000000000000000000000000f2658c2709e49c20000000000000000000000000000000000000000000003a24f89b18d5ec000000000000000000000000000000000000000000000010e210db096b52d97d583cd00000000000000000000000000000000000000000000000000000f9ba76d261b000000000000000000000000000000000000000000000000000000006333f4890000000000000000000000000000000000000000010dfbfe16d4a33121f01a7700000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 56323,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 82860, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "delegatecall",
            "gas": 221688,
            "input": HexBytes(
                "0x1f3cc1fe0000000000000000000000000000000000000000000000000f2658c2709e49c20000000000000000000000000000000000000000000003a24f89b18d5ec000000000000000000000000000000000000000000000010e210db096b52d97d583cd00000000000000000000000000000000000000000000000000000f9ba76d261b000000000000000000000000000000000000000000000000000000006333f4890000000000000000000000000000000000000000010dfbfe16d4a33121f01a77"
            ),
            "to": "0x4095d53a4Cf4dedd3AD40773E474670d9D0B5729",
            "value": 56323,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 79019,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000f2658c2709e49c2000000000000000000000000000000000000000000000000000a6ba3764af2c7"
            ),
        },
        "subtraces": 2,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 215449,
            "input": HexBytes("0x3850c7bd"),
            "to": "0x83abECf7204d5Afc1Bea5dF734f085f2535a9976",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2696,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000010d67bfafcc5b3f3ec59516fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe52bf00000000000000000000000000000000000000000000000000000000000000210000000000000000000000000000000000000000000000000000000000000049000000000000000000000000000000000000000000000000000000000000004900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 212444,
            "input": HexBytes(
                "0x128acb0800000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f2658c2709e49c20000000000000000000000000000000000000000010e210db096b52d97d583cd00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000600144c077fd2dde35c67fba088eb0bb1691583dabe3fa4f749daca977e76ad8ef00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
            ),
            "to": "0x83abECf7204d5Afc1Bea5dF734f085f2535a9976",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 72444,
            "output": HexBytes(
                "0xfffffffffffffffffffffffffffffffffffffffffffff27e52fbce309d3d31c50000000000000000000000000000000000000000000000000f2658c2709e49c2"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83abECf7204d5Afc1Bea5dF734f085f2535a9976",
            "callType": "call",
            "gas": 175185,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000000000000000000000000d81ad0431cf62c2ce3b"
            ),
            "to": "0x7A58c0Be72BE218B41C608b7Fe7C5bB630736C71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12726,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1, 0],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83abECf7204d5Afc1Bea5dF734f085f2535a9976",
            "callType": "staticcall",
            "gas": 159327,
            "input": HexBytes(
                "0x70a0823100000000000000000000000083abecf7204d5afc1bea5df734f085f2535a9976"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000053caa64af12990fbd"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1, 1],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83abECf7204d5Afc1Bea5dF734f085f2535a9976",
            "callType": "call",
            "gas": 156060,
            "input": HexBytes(
                "0xfa461e33fffffffffffffffffffffffffffffffffffffffffffff27e52fbce309d3d31c50000000000000000000000000000000000000000000000000f2658c2709e49c2000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000600144c077fd2dde35c67fba088eb0bb1691583dabe3fa4f749daca977e76ad8ef00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf9000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
            ),
            "to": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 13664, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 1, 2],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
            "callType": "call",
            "gas": 153018,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000056178a0d5f301baf6cf3e1cd53d9863437345bf900000000000000000000000083abecf7204d5afc1bea5df734f085f2535a99760000000000000000000000000000000000000000000000000f2658c2709e49c2"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13025,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1, 2, 0],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0x83abECf7204d5Afc1Bea5dF734f085f2535a9976",
            "callType": "staticcall",
            "gas": 141978,
            "input": HexBytes(
                "0x70a0823100000000000000000000000083abecf7204d5afc1bea5df734f085f2535a9976"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000054bd0bd718337597f"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1, 3],
        "transactionHash": HexBytes(
            "0x21254fad192705300b69839b7ca07262aeafb1a7e3d1ebc45ad41e29a5f9838c"
        ),
        "transactionPosition": 110,
        "type": "call",
    },
    {
        "action": {
            "from": "0xeA3d9B4743e20CE41777149A16e4eC97185d1487",
            "callType": "call",
            "gas": 62416,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000001a1a806cc98a7fbb0070683cb0bca738463f15f600000000000000000000000000000000000000000000000000000000931ab100"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 26917,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x0d91e50454b46c7858661116271beec901957ce1c5edeb680ea8443650728953"
        ),
        "transactionPosition": 111,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 54309,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000001a1a806cc98a7fbb0070683cb0bca738463f15f600000000000000000000000000000000000000000000000000000000931ab100"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 19628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x0d91e50454b46c7858661116271beec901957ce1c5edeb680ea8443650728953"
        ),
        "transactionPosition": 111,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1905D4567D88b371983e442ADF2fDC7EEa5ae3a8",
            "callType": "call",
            "gas": 162998,
            "input": HexBytes(
                "0x5ae401dc000000000000000000000000000000000000000000000000000000006333fb4b000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000e404e45aaf00000000000000000000000012b6893ce26ea6341919fe289212ef77e51688c8000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000046791fc84e07d000000000000000000000000000000000000000000000000000000055da8108b01b96000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004449404b7c0000000000000000000000000000000000000000000000000055da8108b01b960000000000000000000000001905d4567d88b371983e442adf2fdc7eea5ae3a800000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 130303,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000005671cbdb1ae2370000000000000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "delegatecall",
            "gas": 159115,
            "input": HexBytes(
                "0x04e45aaf00000000000000000000000012b6893ce26ea6341919fe289212ef77e51688c8000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000046791fc84e07d000000000000000000000000000000000000000000000000000000055da8108b01b960000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 108970,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000005671cbdb1ae237"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 149731,
            "input": HexBytes(
                "0x128acb0800000000000000000000000068b3465833fb72a70ecdf485e0e4c7bd8665fc450000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000046791fc84e07d0000000000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000400000000000000000000000001905d4567d88b371983e442adf2fdc7eea5ae3a8000000000000000000000000000000000000000000000000000000000000002b12b6893ce26ea6341919fe289212ef77e51688c8002710c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000"
            ),
            "to": "0xF1B5Cf831CED19136472b2b385F30384cE14a982",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 101567,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000046791fc84e07d00000ffffffffffffffffffffffffffffffffffffffffffffffffffa98e3424e51dc9"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF1B5Cf831CED19136472b2b385F30384cE14a982",
            "callType": "call",
            "gas": 112197,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000068b3465833fb72a70ecdf485e0e4c7bd8665fc45000000000000000000000000000000000000000000000000005671cbdb1ae237"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 29962,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 0],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF1B5Cf831CED19136472b2b385F30384cE14a982",
            "callType": "staticcall",
            "gas": 79371,
            "input": HexBytes(
                "0x70a08231000000000000000000000000f1b5cf831ced19136472b2b385f30384ce14a982"
            ),
            "to": "0x12b6893cE26Ea6341919FE289212ef77e51688c8",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2952,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000086eefe0170e4d3401fc4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 1],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF1B5Cf831CED19136472b2b385F30384cE14a982",
            "callType": "call",
            "gas": 75674,
            "input": HexBytes(
                "0xfa461e33000000000000000000000000000000000000000000000046791fc84e07d00000ffffffffffffffffffffffffffffffffffffffffffffffffffa98e3424e51dc9000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000400000000000000000000000001905d4567d88b371983e442adf2fdc7eea5ae3a8000000000000000000000000000000000000000000000000000000000000002b12b6893ce26ea6341919fe289212ef77e51688c8002710c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 23411, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 0, 2],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 70794,
            "input": HexBytes(
                "0x23b872dd0000000000000000000000001905d4567d88b371983e442adf2fdc7eea5ae3a8000000000000000000000000f1b5cf831ced19136472b2b385f30384ce14a982000000000000000000000000000000000000000000000046791fc84e07d00000"
            ),
            "to": "0x12b6893cE26Ea6341919FE289212ef77e51688c8",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 19334,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 2, 0],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0xF1B5Cf831CED19136472b2b385F30384cE14a982",
            "callType": "staticcall",
            "gas": 51996,
            "input": HexBytes(
                "0x70a08231000000000000000000000000f1b5cf831ced19136472b2b385f30384ce14a982"
            ),
            "to": "0x12b6893cE26Ea6341919FE289212ef77e51688c8",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 952,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000873577213932db101fc4"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0, 3],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "delegatecall",
            "gas": 51151,
            "input": HexBytes(
                "0x49404b7c0000000000000000000000000000000000000000000000000055da8108b01b960000000000000000000000001905d4567d88b371983e442adf2fdc7eea5ae3a8"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 18174, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 49646,
            "input": HexBytes(
                "0x70a0823100000000000000000000000068b3465833fb72a70ecdf485e0e4c7bd8665fc45"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000005671cbdb1ae237"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 48678,
            "input": HexBytes(
                "0x2e1a7d4d000000000000000000000000000000000000000000000000005671cbdb1ae237"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 9223, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 24331968365388343,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 83, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 1, 0],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 32599,
            "input": HexBytes("0x"),
            "to": "0x1905D4567D88b371983e442ADF2fDC7EEa5ae3a8",
            "value": 24331968365388343,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x42e688c14cfee7fe51d9aeff3e9e95f2689ba0dc3ab6ad34a1e02e4689e15ec7"
        ),
        "transactionPosition": 112,
        "type": "call",
    },
    {
        "action": {
            "from": "0x62DE18b42c4D169ee0b18330ccF694b19cd94034",
            "callType": "call",
            "gas": 34838,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000030ce4f2704f242d1aeb13e808635210ae0091339000000000000000000000000000000000000000000000000000000e8d4a51000"
            ),
            "to": "0x08e0fAFf8bB80eaf8c30A99920355028b5bD6789",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 16023,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xd7b59c62a21ce4542e64e25428db05c2421434702c27553d15b57abad944ed63"
        ),
        "transactionPosition": 113,
        "type": "call",
    },
    {
        "action": {
            "from": "0xa651E44Af3Ed093B0E2A7c9687E37da1AA5dEffb",
            "callType": "call",
            "gas": 316429,
            "input": HexBytes(
                "0x5ae401dc000000000000000000000000000000000000000000000000000000006333f56300000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000e4472b43f300000000000000000000000000000000000000000000000002039e99c42720800000000000000000000000000000000000000000000000000331a13222b52f3b0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000a651e44af3ed093b0e2a7c9687e37da1aa5deffb0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000007db5af2b9624e1b3b4bb69d6debd9ad1016a58ac00000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 145133996264071296,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 256556,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000033209deca789655"
            ),
        },
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "delegatecall",
            "gas": 310198,
            "input": HexBytes(
                "0x472b43f300000000000000000000000000000000000000000000000002039e99c42720800000000000000000000000000000000000000000000000000331a13222b52f3b0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000a651e44af3ed093b0e2a7c9687e37da1aa5deffb0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000007db5af2b9624e1b3b4bb69d6debd9ad1016a58ac"
            ),
            "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "value": 145133996264071296,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 254378,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000033209deca789655"
            ),
        },
        "subtraces": 7,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 294052,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 145133996264071296,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 23974, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 270027,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000004a08cf0a7bca217c24b9ee99c0395052f3707d6800000000000000000000000000000000000000000000000002039e99c4272080"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 258908,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a651e44af3ed093b0e2a7c9687e37da1aa5deffb"
            ),
            "to": "0x7db5af2B9624e1b3B4Bb69D6DeBd9aD1016A58Ac",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 45293,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000300f7f0e38f2afe"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 210231,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x4a08CF0a7bcA217c24b9EE99c0395052f3707d68",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2504,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000005c1b47599f8c26654d0000000000000000000000000000000000000000000000325967e2c9058065de000000000000000000000000000000000000000000000000000000006333f083"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 3],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 206914,
            "input": HexBytes(
                "0x70a082310000000000000000000000004a08cf0a7bca217c24b9ee99c0395052f3707d68"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000325b6b8162c9a7865e"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 4],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "call",
            "gas": 204713,
            "input": HexBytes(
                "0x022c0d9f00000000000000000000000000000000000000000000000003ac462cdb1d29840000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a651e44af3ed093b0e2a7c9687e37da1aa5deffb00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x4a08CF0a7bcA217c24b9EE99c0395052f3707d68",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 137786, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [0, 5],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4a08CF0a7bcA217c24b9EE99c0395052f3707d68",
            "callType": "call",
            "gas": 190810,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000a651e44af3ed093b0e2a7c9687e37da1aa5deffb00000000000000000000000000000000000000000000000003ac462cdb1d2984"
            ),
            "to": "0x7db5af2B9624e1b3B4Bb69D6DeBd9aD1016A58Ac",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 92639,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 5, 0],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4a08CF0a7bcA217c24b9EE99c0395052f3707d68",
            "callType": "staticcall",
            "gas": 98997,
            "input": HexBytes(
                "0x70a082310000000000000000000000004a08cf0a7bca217c24b9ee99c0395052f3707d68"
            ),
            "to": "0x7db5af2B9624e1b3B4Bb69D6DeBd9aD1016A58Ac",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13293,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000005c179b5748134c7d92"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 5, 1],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x4a08CF0a7bcA217c24b9EE99c0395052f3707d68",
            "callType": "staticcall",
            "gas": 85506,
            "input": HexBytes(
                "0x70a082310000000000000000000000004a08cf0a7bca217c24b9ee99c0395052f3707d68"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000325b6b8162c9a7865e"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 5, 2],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "callType": "staticcall",
            "gas": 68390,
            "input": HexBytes(
                "0x70a08231000000000000000000000000a651e44af3ed093b0e2a7c9687e37da1aa5deffb"
            ),
            "to": "0x7db5af2B9624e1b3B4Bb69D6DeBd9aD1016A58Ac",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13293,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000063301cfae07c153"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 6],
        "transactionHash": HexBytes(
            "0xa24679dfdcba768b6ed93dfd63de2d9132e7880ed5c29667280d69da866ce9f8"
        ),
        "transactionPosition": 114,
        "type": "call",
    },
    {
        "action": {
            "from": "0xcfa8Cdc7Ea3aEd89c99bA831fBE8DaFD25ECcFC8",
            "callType": "call",
            "gas": 321410,
            "input": HexBytes(
                "0xb6f9de95000000000000000000000000000000000000000000000000000014ccd4ce26a00000000000000000000000000000000000000000000000000000000000000080000000000000000000000000cfa8cdc7ea3aed89c99ba831fbe8dafd25eccfc8000000000000000000000000000000000000000000000000000000006333f4e80000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000ce3f08e664693ca792cace4af1364d5e220827b2"
            ),
            "to": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "value": 22500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 321245, "output": HexBytes("0x")},
        "subtraces": 7,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "call",
            "gas": 306401,
            "input": HexBytes("0xd0e30db0"),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 22500000000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 23974, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "call",
            "gas": 281505,
            "input": HexBytes(
                "0xa9059cbb0000000000000000000000005716d2cbf2f44b5b9e3ed7b7a6eb58ce5996f318000000000000000000000000000000000000000000000000004fefa17b724000"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "staticcall",
            "gas": 270580,
            "input": HexBytes(
                "0x70a08231000000000000000000000000cfa8cdc7ea3aed89c99ba831fbe8dafd25eccfc8"
            ),
            "to": "0xCE3f08e664693ca792caCE4af1364D5e220827B2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 68381,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000214cde6c7d0fa"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "staticcall",
            "gas": 199132,
            "input": HexBytes("0x0902f1ac"),
            "to": "0x5716D2cbF2f44b5b9e3Ed7b7a6eB58Ce5996F318",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2517,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000087158802a2b36758d00000000000000000000000000000000000000000000000002514655d246c79b000000000000000000000000000000000000000000000000000000006333f1a3"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "staticcall",
            "gas": 196084,
            "input": HexBytes(
                "0x70a082310000000000000000000000005716d2cbf2f44b5b9e3ed7b7a6eb58ce5996f318"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000871a86fcba6a8b58d"
            ),
        },
        "subtraces": 0,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "call",
            "gas": 193984,
            "input": HexBytes(
                "0x022c0d9f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000015e515e68656000000000000000000000000cfa8cdc7ea3aed89c99ba831fbe8dafd25eccfc800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
            ),
            "to": "0x5716D2cbF2f44b5b9e3Ed7b7a6eB58Ce5996F318",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 173739, "output": HexBytes("0x")},
        "subtraces": 3,
        "traceAddress": [5],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5716D2cbF2f44b5b9e3Ed7b7a6eB58Ce5996F318",
            "callType": "call",
            "gas": 180105,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000cfa8cdc7ea3aed89c99ba831fbe8dafd25eccfc8000000000000000000000000000000000000000000000000000015e515e68656"
            ),
            "to": "0xCE3f08e664693ca792caCE4af1364D5e220827B2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 114301,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [5, 0],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5716D2cbF2f44b5b9e3Ed7b7a6eB58Ce5996F318",
            "callType": "staticcall",
            "gas": 66970,
            "input": HexBytes(
                "0x70a082310000000000000000000000005716d2cbf2f44b5b9e3ed7b7a6eb58ce5996f318"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000871a86fcba6a8b58d"
            ),
        },
        "subtraces": 0,
        "traceAddress": [5, 1],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5716D2cbF2f44b5b9e3Ed7b7a6eB58Ce5996F318",
            "callType": "staticcall",
            "gas": 66022,
            "input": HexBytes(
                "0x70a082310000000000000000000000005716d2cbf2f44b5b9e3ed7b7a6eb58ce5996f318"
            ),
            "to": "0xCE3f08e664693ca792caCE4af1364D5e220827B2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 22381,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000002513071ed503c26"
            ),
        },
        "subtraces": 0,
        "traceAddress": [5, 2],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c17e776CD218252ADFca8D4e761D3fe757e9778",
            "callType": "staticcall",
            "gas": 22381,
            "input": HexBytes(
                "0x70a08231000000000000000000000000cfa8cdc7ea3aed89c99ba831fbe8dafd25eccfc8"
            ),
            "to": "0xCE3f08e664693ca792caCE4af1364D5e220827B2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 22381,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000000022ab2fcae5750"
            ),
        },
        "subtraces": 0,
        "traceAddress": [6],
        "transactionHash": HexBytes(
            "0xde5bb7799c83b55de96081265617a7d4fcd4d2ffa3dea999b4671599cba56ed9"
        ),
        "transactionPosition": 115,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1afA7bbcBDbb2E31B7FB70DFdbE15E88c26582bD",
            "callType": "call",
            "gas": 296055,
            "input": HexBytes(
                "0x00000000010100000000000000000000000000000000000000000000000003c0a459d367eef1004c88e6a0c2ddd26feeb64f039a2c41296fcb3f564003000034290850efa2d7e130e55bbc1db2b48bc5c03097f50301001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d00"
            ),
            "to": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "value": 15630274,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 223995, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "callType": "call",
            "gas": 266631,
            "input": HexBytes(
                "0x128acb08000000000000000000000000c7ee7c66636f407586afa431c19a916e049289420000000000000000000000000000000000000000000000000000000000000001fffffffffffffffffffffffffffffffffffffffffffffffffc3f5ba62c98110f00000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000004c88e6a0c2ddd26feeb64f039a2c41296fcb3f564003000034290850efa2d7e130e55bbc1db2b48bc5c03097f50301001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d00"
            ),
            "to": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 198611,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000000000001470b2aafffffffffffffffffffffffffffffffffffffffffffffffffc3f5ba62c98110f"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "call",
            "gas": 235610,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c7ee7c66636f407586afa431c19a916e0492894200000000000000000000000000000000000000000000000003c0a459d367eef1"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 12862,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "staticcall",
            "gas": 219617,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 9815,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000206edc4ee616"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 1],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 209057,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000206edc4ee616"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 1, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "call",
            "gas": 209187,
            "input": HexBytes(
                "0xfa461e33000000000000000000000000000000000000000000000000000000001470b2aafffffffffffffffffffffffffffffffffffffffffffffffffc3f5ba62c98110f0000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000004c88e6a0c2ddd26feeb64f039a2c41296fcb3f564003000034290850efa2d7e130e55bbc1db2b48bc5c03097f50301001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d000000000000000000000000000000000000000000"
            ),
            "to": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 138818, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 2],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "callType": "call",
            "gas": 202536,
            "input": HexBytes(
                "0x128acb0800000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f56400000000000000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffeb8f4d56000000000000000000000000fffd8963efd1fc6a506488495d951d5263988d2500000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000034290850efa2d7e130e55bbc1db2b48bc5c03097f50301001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d00"
            ),
            "to": "0x290850efa2d7E130E55bbc1db2b48Bc5C03097F5",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 135217,
            "output": HexBytes(
                "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffeb8f4d56000000000000000000000000000000000000000000000f666bac1c563e2f4c8b"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 2, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x290850efa2d7E130E55bbc1db2b48Bc5C03097F5",
            "callType": "call",
            "gas": 163984,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640000000000000000000000000000000000000000000000000000000001470b2aa"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 18417,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 2, 0, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 160689,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640000000000000000000000000000000000000000000000000000000001470b2aa"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 17628,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 0, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x290850efa2d7E130E55bbc1db2b48Bc5C03097F5",
            "callType": "staticcall",
            "gas": 142523,
            "input": HexBytes(
                "0x70a08231000000000000000000000000290850efa2d7e130e55bbc1db2b48bc5c03097f5"
            ),
            "to": "0xDF2C7238198Ad8B389666574f2d8bc411A4b7428",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2657,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000001d9fd346bfbeb4f54d099"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 1],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x290850efa2d7E130E55bbc1db2b48Bc5C03097F5",
            "callType": "call",
            "gas": 139146,
            "input": HexBytes(
                "0xfa461e33ffffffffffffffffffffffffffffffffffffffffffffffffffffffffeb8f4d56000000000000000000000000000000000000000000000f666bac1c563e2f4c8b00000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000034290850efa2d7e130e55bbc1db2b48bc5c03097f50301001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d00000000000000000000000000"
            ),
            "to": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 69032, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [0, 2, 0, 2],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "callType": "call",
            "gas": 133677,
            "input": HexBytes(
                "0x128acb08000000000000000000000000290850efa2d7e130e55bbc1db2b48bc5c03097f50000000000000000000000000000000000000000000000000000000000000001fffffffffffffffffffffffffffffffffffffffffffff0999453e3a9c1d0b37500000000000000000000000000000000000000000000000000000001000276a400000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d00"
            ),
            "to": "0xFBbA47B4C4ded47AA154a1b6DC06ec207166Fc13",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 65520,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000000000003b5b9d07a200c9efffffffffffffffffffffffffffffffffffffffffffff0999453e3a9c1d0b375"
            ),
        },
        "subtraces": 4,
        "traceAddress": [0, 2, 0, 2, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFBbA47B4C4ded47AA154a1b6DC06ec207166Fc13",
            "callType": "call",
            "gas": 97319,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000290850efa2d7e130e55bbc1db2b48bc5c03097f5000000000000000000000000000000000000000000000f666bac1c563e2f4c8b"
            ),
            "to": "0xDF2C7238198Ad8B389666574f2d8bc411A4b7428",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 13649,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 2, 0, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFBbA47B4C4ded47AA154a1b6DC06ec207166Fc13",
            "callType": "staticcall",
            "gas": 83012,
            "input": HexBytes(
                "0x70a08231000000000000000000000000fbba47b4c4ded47aa154a1b6dc06ec207166fc13"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2534,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000003ea45452556a5ece"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 2, 0, 1],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFBbA47B4C4ded47AA154a1b6DC06ec207166Fc13",
            "callType": "call",
            "gas": 79758,
            "input": HexBytes(
                "0xfa461e3300000000000000000000000000000000000000000000000003b5b9d07a200c9efffffffffffffffffffffffffffffffffffffffffffff0999453e3a9c1d0b3750000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000001cfbba47b4c4ded47aa154a1b6dc06ec207166fc130400000003789d0000000000"
            ),
            "to": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 7975, "output": HexBytes("0x")},
        "subtraces": 2,
        "traceAddress": [0, 2, 0, 2, 0, 2],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "callType": "staticcall",
            "gas": 77879,
            "input": HexBytes("0x0dfe1681"),
            "to": "0xFBbA47B4C4ded47AA154a1b6DC06ec207166Fc13",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 266,
            "output": HexBytes(
                "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 2, 0, 2, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xc7EE7c66636f407586afa431C19A916e04928942",
            "callType": "call",
            "gas": 76765,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000fbba47b4c4ded47aa154a1b6dc06ec207166fc1300000000000000000000000000000000000000000000000003b5b9d07a200c9e"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 6062,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 2, 0, 2, 1],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xFBbA47B4C4ded47AA154a1b6DC06ec207166Fc13",
            "callType": "staticcall",
            "gas": 71275,
            "input": HexBytes(
                "0x70a08231000000000000000000000000fbba47b4c4ded47aa154a1b6dc06ec207166fc13"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000000425a0e22cf8a6b6c"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 2, 0, 3],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x290850efa2d7E130E55bbc1db2b48Bc5C03097F5",
            "callType": "staticcall",
            "gas": 70560,
            "input": HexBytes(
                "0x70a08231000000000000000000000000290850efa2d7e130e55bbc1db2b48bc5c03097f5"
            ),
            "to": "0xDF2C7238198Ad8B389666574f2d8bc411A4b7428",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 657,
            "output": HexBytes(
                "0x00000000000000000000000000000000000000000001e963a01818418d841d24"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 2, 0, 3],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            "callType": "staticcall",
            "gas": 71905,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 1315,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000206ef0bf98c0"
            ),
        },
        "subtraces": 1,
        "traceAddress": [0, 3],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "callType": "delegatecall",
            "gas": 70052,
            "input": HexBytes(
                "0x70a0823100000000000000000000000088e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            ),
            "to": "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 529,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000206ef0bf98c0"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0, 3, 0],
        "transactionHash": HexBytes(
            "0xaec61e6113da706f407a6defb998476591cd3e85ccf3bfb4fb2d2a2561df136c"
        ),
        "transactionPosition": 116,
        "type": "call",
    },
    {
        "action": {
            "from": "0x6905030bAB047B4A65b28DB078e8d844b83d6FBF",
            "callType": "call",
            "gas": 55889,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000bce0b0d02dbc78efabbff56d0aae6c3732f9fdfd000000000000000000000000000000000000000000000d21679750a2b2f20f80"
            ),
            "to": "0x557B933a7C2c45672B610F8954A3deB39a51A8Ca",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 30033,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x74563c253a5758f5b99e36a2fe1cbbf15292694724f764050525a36e4b44f966"
        ),
        "transactionPosition": 117,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0c5c550F937CDD6d93876d9A2DBA0d22E81aa8A9",
            "callType": "call",
            "gas": 169189,
            "input": HexBytes(
                "0x75090ebf000000000000000000000000000000000000000000000000000062726f6e7a6500000000000000000000000000000000000000000000000000000000001e848000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c5c550f937cdd6d93876d9a2dba0d22e81aa8a9"
            ),
            "to": "0xd588b586D61C826A0e87919b3D1a239206d58bf2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 105485, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8f3155286a4d53ce966c4456465b446d097849026ad885a26ed80833b6799d6e"
        ),
        "transactionPosition": 118,
        "type": "call",
    },
    {
        "action": {
            "from": "0x2A038e100F8B85DF21e4d44121bdBfE0c288A869",
            "callType": "call",
            "gas": 177348,
            "input": HexBytes(
                "0x0175b1c4159735dd5b7ac6cf82f37afdcee2d07ebad0c8cc38284b7b69874157147caf090000000000000000000000000615dbba33fe61a31c7ed131bda6655ed76748b1000000000000000000000000d169005c938f82fc3cd9b195de76d3d9f86f8bce0000000000000000000000000000000000000000000000002f2e1cc70fc5e4000000000000000000000000000000000000000000000000000000000000000038"
            ),
            "to": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 105711, "output": HexBytes("0x")},
        "subtraces": 6,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "callType": "call",
            "gas": 167106,
            "input": HexBytes(
                "0x40c10f19000000000000000000000000d169005c938f82fc3cd9b195de76d3d9f86f8bce0000000000000000000000000000000000000000000000002f2e1cc70fc5e400"
            ),
            "to": "0x0615Dbba33Fe61a31c7eD131BDA6655Ed76748B1",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 32018,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "callType": "staticcall",
            "gas": 132404,
            "input": HexBytes("0x6f307dc3"),
            "to": "0x0615Dbba33Fe61a31c7eD131BDA6655Ed76748B1",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 371,
            "output": HexBytes(
                "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "callType": "staticcall",
            "gas": 129084,
            "input": HexBytes(
                "0x70a082310000000000000000000000000615dbba33fe61a31c7ed131bda6655ed76748b1"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 2534,
            "output": HexBytes(
                "0x000000000000000000000000000000000000000000000166616225a8ec99f0d2"
            ),
        },
        "subtraces": 0,
        "traceAddress": [2],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "callType": "call",
            "gas": 126033,
            "input": HexBytes(
                "0x0039d6ec000000000000000000000000d169005c938f82fc3cd9b195de76d3d9f86f8bce0000000000000000000000000000000000000000000000002f2e1cc70fc5e400000000000000000000000000ba8da9dcf11b50b03fd5284f164ef5cdef910705"
            ),
            "to": "0x0615Dbba33Fe61a31c7eD131BDA6655Ed76748B1",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 36924,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000002f2e1cc70fc5e400"
            ),
        },
        "subtraces": 1,
        "traceAddress": [3],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0x0615Dbba33Fe61a31c7eD131BDA6655Ed76748B1",
            "callType": "call",
            "gas": 115701,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000ba8da9dcf11b50b03fd5284f164ef5cdef9107050000000000000000000000000000000000000000000000002f2e1cc70fc5e400"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 27962,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [3, 0],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "callType": "call",
            "gas": 89199,
            "input": HexBytes(
                "0x2e1a7d4d0000000000000000000000000000000000000000000000002f2e1cc70fc5e400"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 9235, "output": HexBytes("0x")},
        "subtraces": 1,
        "traceAddress": [4],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "callType": "call",
            "gas": 2300,
            "input": HexBytes("0x"),
            "to": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "value": 3399686410000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 95, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [4, 0],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0xBa8Da9dcF11B50B03fd5284f164Ef5cdEF910705",
            "callType": "call",
            "gas": 70674,
            "input": HexBytes("0x"),
            "to": "0xd169005c938F82fC3Cd9b195DE76D3d9f86F8bce",
            "value": 3399686410000000000,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 0, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [5],
        "transactionHash": HexBytes(
            "0x8bb5786ab0733d9657e3eace0c126794be48d22982492dc6e7107642314483a4"
        ),
        "transactionPosition": 119,
        "type": "call",
    },
    {
        "action": {
            "from": "0x7c0Df51526C6956f29b36AC24fc863085Dbe7e7B",
            "callType": "call",
            "gas": 55799,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000dc1599407324607d6589144f86a9cb45095ce8000000000000000000000000000000000000000000000000000000001e06fe9d73"
            ),
            "to": "0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 29997,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x95b640dc515fe47ec62bc86e907579a46ae2762d76662a5afe3018d2d85e4763"
        ),
        "transactionPosition": 120,
        "type": "call",
    },
    {
        "action": {
            "from": "0xee401129DffB0FF1D73F3B05989DeDa2C60296A1",
            "callType": "call",
            "gas": 73211,
            "input": HexBytes(
                "0xa9059cbb00000000000000000000000099a27546703b8b908cb3f24d474cdbd65caf647e00000000000000000000000000000000000000000000000000000002541b2640"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x72462461c4c7dd13689fb6251251230d30e2b57dbe47af652279e197bb68cf8f"
        ),
        "transactionPosition": 121,
        "type": "call",
    },
    {
        "action": {
            "from": "0x9A0b967411a09eB6c5cc7795c0138091581DfEbA",
            "callType": "call",
            "gas": 167487,
            "input": HexBytes(
                "0xe7acab24000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000006600000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000052000000000000000000000000000000000000000000000000000000000000005a000000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000002200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333525d000000000000000000000000000000000000000000000000000000006334a3d80000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000ebfe23a8b7cb6c970000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004c072fc6318000000000000000000000000000000000000000000000000000004c072fc631800000000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000004000000000000000000000000baeec315f9d7f8db2645edfd5633360f152279bce83e91e11dabf311f0e63aa97f6c83dea882d884b714c17b3dc1b69d8d0363360000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e69464f470000000000000000000000000000000000000000000000000000001e69464f470000000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003cd28c9e8e0000000000000000000000000000000000000000000000000000003cd28c9e8e000000000000000000000000000334919cc1bd89a61d955f2d39206fff9551b4e5e0000000000000000000000000000000000000000000000000000000000000041db276a0cfc04800bd6e36f646b92760d983192cc2f5b061c219a8e998b1bcfa260dd911b2dcfdc272b7192c6a35eadba0a3055539730a4783eb4961e63dff75d1b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000031300000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000e9da13a855afc6fb2500b63e4c1e10216604598f970ad683d22ad79f58135cc3f921f2ff93ba5b2af0555858b85d256545aaa5dbcdb9f957a013fa0d0f30aff9a27d116759165fc0b157bd209ebecaf1eb86efbd8cf646687a2a9cc6ad90081de079c02a49a619f0b2d8d8f4f1c70c6196f1907d756e36640d39303f736c5d5ac1914cedbe1390dfb0fa65df9a5c52dd3aeec7f92d671f9cbc083085b9222e50eea29b71f257558d794d4c22c7770b762804c08f53afffc39860055e9d6d1196ac03369c55216f2115da19deea4925482cea0149891824b1a7466552f50ee8c126978e1b572d62bf99bc091c234418b7fca4e036f602af1bea2cbe13a63cbbb4b8df0c85d745e90a0c5ddeb4f5906f65ac99ae98be03bf59c2fb58da22a719fa988a4ea115d5628d4f6d9aa80065b40e516cbf1840c6b2836456038f35d34a84f3fd7c5a8ee0ede9ff4266dfaf8577e61f51f3db80cf5296ce0d5c184c85b155bb3c3f56ff50aefa7c2f032abb19b585037b0469e8237b477a59b6cb20b207b1e282eced56605b9ccb31ad257428b14ee7c9d64350cb1e737763d61a3672b3382a3f1b34dec3f0f02006bab7ea4631daea9c01c2c0f69f3a794812840a9701558"
            ),
            "to": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 165367,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 2,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "staticcall",
            "gas": 140720,
            "input": HexBytes(
                "0x33131570bbf48a31e03ad1226ce6296638b5d576e8a1edd0e5b132dc4cc951518ddac39a0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000660000000000000000000000000000000000000000000000000000000000000068000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000052000000000000000000000000000000000000000000000000000000000000005a000000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000002200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000006333525d000000000000000000000000000000000000000000000000000000006334a3d80000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000ebfe23a8b7cb6c970000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004c072fc6318000000000000000000000000000000000000000000000000000004c072fc631800000000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000004000000000000000000000000baeec315f9d7f8db2645edfd5633360f152279bce83e91e11dabf311f0e63aa97f6c83dea882d884b714c17b3dc1b69d8d0363360000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e69464f470000000000000000000000000000000000000000000000000000001e69464f470000000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003cd28c9e8e0000000000000000000000000000000000000000000000000000003cd28c9e8e000000000000000000000000000334919cc1bd89a61d955f2d39206fff9551b4e5e0000000000000000000000000000000000000000000000000000000000000041db276a0cfc04800bd6e36f646b92760d983192cc2f5b061c219a8e998b1bcfa260dd911b2dcfdc272b7192c6a35eadba0a3055539730a4783eb4961e63dff75d1b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000031300000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000e9da13a855afc6fb2500b63e4c1e10216604598f970ad683d22ad79f58135cc3f921f2ff93ba5b2af0555858b85d256545aaa5dbcdb9f957a013fa0d0f30aff9a27d116759165fc0b157bd209ebecaf1eb86efbd8cf646687a2a9cc6ad90081de079c02a49a619f0b2d8d8f4f1c70c6196f1907d756e36640d39303f736c5d5ac1914cedbe1390dfb0fa65df9a5c52dd3aeec7f92d671f9cbc083085b9222e50eea29b71f257558d794d4c22c7770b762804c08f53afffc39860055e9d6d1196ac03369c55216f2115da19deea4925482cea0149891824b1a7466552f50ee8c126978e1b572d62bf99bc091c234418b7fca4e036f602af1bea2cbe13a63cbbb4b8df0c85d745e90a0c5ddeb4f5906f65ac99ae98be03bf59c2fb58da22a719fa988a4ea115d5628d4f6d9aa80065b40e516cbf1840c6b2836456038f35d34a84f3fd7c5a8ee0ede9ff4266dfaf8577e61f51f3db80cf5296ce0d5c184c85b155bb3c3f56ff50aefa7c2f032abb19b585037b0469e8237b477a59b6cb20b207b1e282eced56605b9ccb31ad257428b14ee7c9d64350cb1e737763d61a3672b3382a3f1b34dec3f0f02006bab7ea4631daea9c01c2c0f69f3a794812840a9701558"
            ),
            "to": "0x004C00500000aD104D7DBd00e3ae0A5C00560C00",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 702,
            "output": HexBytes(
                "0x0e1d31dc00000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 0,
        "traceAddress": [0],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x00000000006c3852cbEf3e08E8dF289169EdE581",
            "callType": "call",
            "gas": 99476,
            "input": HexBytes(
                "0x4ce34aa2000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004c072fc63180000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000baeec315f9d7f8db2645edfd5633360f152279bc0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba00000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f000000000000000000000000000000000000000000000000000000000000031300000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba0000000000000000000000000000a26b00c1f0df003000390027140000faa71900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e69464f470000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba000000000000000000000000334919cc1bd89a61d955f2d39206fff9551b4e5e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003cd28c9e8e000"
            ),
            "to": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 89138,
            "output": HexBytes(
                "0x4ce34aa200000000000000000000000000000000000000000000000000000000"
            ),
        },
        "subtraces": 4,
        "traceAddress": [1],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 92288,
            "input": HexBytes(
                "0x23b872dd00000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba000000000000000000000000000000000000000000000000004c072fc6318000"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 15025,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 0],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 73921,
            "input": HexBytes(
                "0x23b872dd0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba00000000000000000000000045c2188ec89cce1f0d08b41ffe6c7efb7e72479f0000000000000000000000000000000000000000000000000000000000000313"
            ),
            "to": "0xBaEEc315F9d7f8DB2645edfD5633360F152279Bc",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 44479, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [1, 1],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 29350,
            "input": HexBytes(
                "0x23b872dd0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba0000000000000000000000000000a26b00c1f0df003000390027140000faa7190000000000000000000000000000000000000000000000000001e69464f47000"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 10225,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 2],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x1E0049783F008A0085193E00003D00cd54003c71",
            "callType": "call",
            "gas": 18442,
            "input": HexBytes(
                "0x23b872dd0000000000000000000000009a0b967411a09eb6c5cc7795c0138091581dfeba000000000000000000000000334919cc1bd89a61d955f2d39206fff9551b4e5e0000000000000000000000000000000000000000000000000003cd28c9e8e000"
            ),
            "to": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {
            "gasUsed": 8225,
            "output": HexBytes(
                "0x0000000000000000000000000000000000000000000000000000000000000001"
            ),
        },
        "subtraces": 0,
        "traceAddress": [1, 3],
        "transactionHash": HexBytes(
            "0x8c3c3b6fe342720d958411dba2d29cbd22d07cac74be21a099d12c439201c993"
        ),
        "transactionPosition": 122,
        "type": "call",
    },
    {
        "action": {
            "from": "0x5d6436E05d8CF62b5b20Df1d06ae7E18C0904EF9",
            "callType": "call",
            "gas": 51601,
            "input": HexBytes(
                "0xa9059cbb000000000000000000000000c006496a40fde758225b64d5f79370367e2db3ff0000000000000000000000000000000000000000000000000000000020d7e5e0"
            ),
            "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "value": 0,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 41601, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x3760e7fda19d27167d343d18150e4bc3d421d041cf9b8b1ee8bbb648768478a5"
        ),
        "transactionPosition": 123,
        "type": "call",
    },
    {
        "action": {
            "from": "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5",
            "callType": "call",
            "gas": 5000,
            "input": HexBytes("0x"),
            "to": "0xeBec795c9c8bBD61FFc14A6662944748F299cAcf",
            "value": 40101722876475633,
        },
        "blockHash": HexBytes(
            "0xa1dd687d41a835a1e173b5f69f656eaad52570ca864dfaeece6bec72e17bc624"
        ),
        "blockNumber": 15630274,
        "result": {"gasUsed": 55, "output": HexBytes("0x")},
        "subtraces": 0,
        "traceAddress": [],
        "transactionHash": HexBytes(
            "0x3894b0d1325a8a91171a2e0a58394287066fef3174945e4ff56eacfc0e4bda58"
        ),
        "transactionPosition": 124,
        "type": "call",
    },
]
