import requests
from hexbytes import HexBytes
from typing import List, NamedTuple, Set, Tuple, Union, Dict


node_url = 'http://localhost:8545'


def query_trace_transaction(tx_hash: str):
    response = requests.post(node_url, json={"method": "trace_replayTransaction",
                                             "params": [tx_hash,
                                                        ["trace"]],
                                             "id": 1,
                                             "jsonrpc": "2.0"})
    return response.json()['result']


def query_trace_block_by_number(block_number: int):
    response = requests.post(node_url, json={"method": "trace_replayBlockTransactions",
                                             "params": ['0x%x' % block_number,
                                                        ["trace"]],
                                             "id": 1,
                                             "jsonrpc": "2.0"})
    return response.json()['result']


def query_trace_block_fast_by_number(block_number: int):
    response = requests.post(node_url, json={"method": "trace_block",
                                             "params": ['0x%x' % block_number],
                                             "id": 1,
                                             "jsonrpc": "2.0"})
    return response.json()['result']


class DecodedCallTrace(NamedTuple):
    call_type: str
    from_: str
    to: str
    input_: bytes
    value: int
    gas: int
    result: bytes
    error: bytes


def decode_transaction_trace(trace: Dict[str, any]) -> List[DecodedCallTrace]:
    decoded_call_traces = []
    for sub_trace in trace:
        if 'action' in sub_trace:
            data = sub_trace['action']
            call_type = data['callType'] if 'callType' in data else sub_trace['type']
            if call_type == 'suicide':
                # Self-destruct has no `to`, `value`...
                # Just `address`, `balance` and `refundAddress`
                continue
            from_ = data['from']
            to = data['to'] if 'to' in data else None  # Contract creation
            input_ = HexBytes(data['input']) if 'input' in data else None  # A contract creation has `init` instead of `input`
            value = int(data['value'], 16)
            gas = int(data['gas'], 16)
            result = None  # If there's error, no result
            error = None  # If there's error, no result
            if 'error' in sub_trace:
                error = sub_trace['error']
            else:
                if 'address' in sub_trace['result']:  # It's a contract creation
                    result_key = 'address'
                else:
                    result_key = 'output'
                result = HexBytes(sub_trace['result'][result_key])

        decoded_call_traces.append(DecodedCallTrace(call_type, from_, to,
                                                    input_, value, gas,
                                                    result, error))
    return decoded_call_traces


def get_decoded_traces_for_tx(tx_hash: str):
    trace = query_trace_transaction(tx_hash)['trace']
    for decoded in decode_transaction_trace(trace):
        print(decoded)


def decode_block(block) -> Dict[str, List[DecodedCallTrace]]:
    tx_hash_with_decoded_traces = {}
    for tx in block:
        tx_hash = tx['transactionHash']
        if tx_hash and 'trace' not in tx_hash:  # trace_block
            tx_hash_with_decoded_traces[tx_hash] = decode_transaction_trace([tx])
        elif tx_hash:  # replay_trace_block
            tx_hash_with_decoded_traces[tx_hash] = decode_transaction_trace(tx['trace'])
    return tx_hash_with_decoded_traces


def decode_blocks(first_block: int, last_block: int):
    for block_number in range(first_block, last_block):
        print('Block\t%d' % block_number)
        block_traces = query_trace_block_fast_by_number(block_number)
        decode_block(block_traces)


# get_decoded_traces_for_tx('0x0142c3f42220d839af4f1dbb7b9ab9482669ab8714c785fdd418d954077f9816')
# decode_blocks(7235792, 7241099)
decode_blocks(7244570, 7244794)
