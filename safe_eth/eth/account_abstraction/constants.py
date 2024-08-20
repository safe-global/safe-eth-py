from hexbytes import HexBytes

# Entrypoint v0.6.0 and v0.7.0 events ----------------------------------------------------

# AccountDeployed (index_topic_1 bytes32 userOpHash, index_topic_2 address sender, address factory, address paymaster)
ACCOUNT_DEPLOYED_TOPIC = HexBytes(
    "0xd51a9c61267aa6196961883ecf5ff2da6619c37dac0fa92122513fb32c032d2d"
)

# Deposited (index_topic_1 address account, uint256 totalDeposit)
DEPOSIT_EVENT_TOPIC = HexBytes(
    "0x2da466a7b24304f47e87fa2e1e5a81b9831ce54fec19055ce277ca2f39ba42c4"
)

# Safe (L2 not required) >= 1.4.1 events -------------------------------------------------

# ExecutionFromModuleSuccess (index_topic_1 address module)
EXECUTION_FROM_MODULE_SUCCESS_TOPIC = HexBytes(
    "0x6895c13664aa4f67288b25d7a21d7aaa34916e355fb9b6fae0a139a9085becb8"
)

# ExecutionFromModuleFailure (index_topic_1 address module)
EXECUTION_FROM_MODULE_FAILURE_TOPIC = HexBytes(
    "0xacd2c8702804128fdb0db2bb49f6d127dd0181c13fd45dbfe16de0930e2bd375"
)
