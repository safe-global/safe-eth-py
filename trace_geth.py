import requests
import time
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


def decode_trace(trace, next_trace) -> DecodedCallTrace:
    decoded_call_trace = None
    if trace['op'] in ('CALL', 'CALLCODE'):
        return decode_call_trace(trace, next_trace)
    elif trace['op'] in ('DELEGATECALL', 'STATICCALL'):
        return decode_delegate_call_trace(trace, next_trace)
    return None


def decode_tx():
    node_url = 'http://localhost:8545'
    tx_hash = '0x0142c3f42220d839af4f1dbb7b9ab9482669ab8714c785fdd418d954077f9816'
    post = trace_transaction(tx_hash, disable_stack=False)
    response = requests.post(node_url, json=post)
    gas = response.json()['result']['gas']
    failed = response.json()['result']['failed']
    return_value = response.json()['result']['returnValue']
    struct_logs = response.json()['result']['structLogs']
    for i in range(len(struct_logs) - 1):
        decoded_call_trace = decode_trace(struct_logs[i], struct_logs[i + 1])
        if decoded_call_trace:
            print(decoded_call_trace)

def decode_block(block):
    for tx in block:
        struct_logs = tx['result']['structLogs']
        for i in range(len(struct_logs) - 1):
            decoded_call_trace = decode_trace(struct_logs[i], struct_logs[i + 1])
            if decoded_call_trace:
                print(decoded_call_trace)


def decode_blocks():
    node_url = 'http://localhost:8545'
    first_block = 7235792
    for block_number in range(first_block, 7241099):
        print('Block\t%d' % block_number)
        post = trace_block_by_number(block_number, disable_stack=False)
        response = requests.post(node_url, json=post)
        # Decode json
        start = time.time()
        print('Start', start)
        response_json = response.json()
        end = time.time()
        print('Elapsed', end - start)
        decode_block(response_json['result'])

# decode_tx()
decode_blocks()
