from typing import Any, List, TypedDict


class ParameterDecoded(TypedDict):
    name: str
    type: str
    value: Any


class DataDecoded(TypedDict):
    method: str
    parameters: List[ParameterDecoded]
