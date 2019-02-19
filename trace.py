import requests
from hexbytes import HexBytes
from typing import List, NamedTuple, Set, Tuple, Union, Dict



def trace_transaction(tx_hash: str, disable_memory=True,
                          disable_storage=True, disable_stack=True):
    return {"id": 1,
            "method": "debug_traceTransaction",
            "params": [tx_hash,
                       {"disableMemory": disable_memory,
                        "disableStorage": disable_storage,
                        "disableStack": disable_stack}
                       ]
            }


def trace_block_by_number(block_number: int, disable_memory=True,
                          disable_storage=True, disable_stack=True):
    return {"id": 1,
            "method": "debug_traceBlockByNumber",
            "params": ['0x%x' % block_number,
                       {"disableMemory": disable_memory,
                        "disableStorage": disable_storage,
                        "disableStack": disable_stack}
                       ]
            }


class DecodedCallTrace(NamedTuple):
    op: str
    gas: int
    address: str
    value: int
    args_offset: int
    args_length: int
    ret_offset: int
    ret_length: int

def decode_call_trace(trace: Dict[str, any], next_trace: Dict[str, any]) -> DecodedCallTrace:
    """
    Takes a trace and decodes it. It needs next trace for return value
    Structure for CALL and CALLCODE:
    gas | addr | value | argsOffset | argsLength | retOffset | retLength
    """
    # TODO Check stack is present
    gas, address, value, args_offset, args_length, ret_offset, ret_length = reversed(trace['stack'][-7:])
    gas = int(gas, 16)
    # TODO checksum encoded address
    address = HexBytes(address.lstrip('0')).hex()
    value = int(value, 16)
    args_offset = int(args_offset, 16)
    args_length = int(args_length, 16)
    ret_offset = int(ret_offset, 16)
    ret_length = int(ret_length, 16)
    return DecodedCallTrace(trace['op'], gas, address, value, args_offset, args_length,
                            ret_offset, ret_length)

def decode_delegate_call_trace(trace: Dict[str, any], next_trace: Dict[str, any]) -> DecodedCallTrace:
    """
    Takes a trace and decodes it. It needs next trace for return value
    Structure for CALL and CALLCODE:
    gas | addr | argsOffset | argsLength | retOffset | retLength
    """
    # TODO Check stack is present
    gas, address, args_offset, args_length, ret_offset, ret_length = reversed(trace['stack'][-6:])
    gas = int(gas, 16)
    # TODO checksum encoded address
    address = HexBytes(address.lstrip('0')).hex()
    value = 0  # No value in DELEGATECALL
    args_offset = int(args_offset, 16)
    args_length = int(args_length, 16)
    ret_offset = int(ret_offset, 16)
    ret_length = int(ret_length, 16)
    return DecodedCallTrace(trace['op'], gas, address, value, args_offset, args_length,
                            ret_offset, ret_length)


node_url = 'http://localhost:8545'
tx_hash = '0x0142c3f42220d839af4f1dbb7b9ab9482669ab8714c785fdd418d954077f9816'
post = trace_transaction(tx_hash, disable_stack=False)
response = requests.post(node_url, json=post)
gas = response.json()['result']['gas']
failed = response.json()['result']['failed']
return_value = response.json()['result']['returnValue']
struct_logs = response.json()['result']['structLogs']
for i, trace in enumerate(struct_logs):
    if trace['op'] in ('CALL', 'CALLCODE'):
        print(decode_call_trace(trace, struct_logs[i + 1]))
    elif trace['op'] in ('DELEGATECALL', 'STATICCALL'):
        print(decode_delegate_call_trace(trace, struct_logs[i + 1]))
    elif trace['op'] == 'CREATE':
        print('CREATE')
