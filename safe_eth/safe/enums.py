from enum import IntEnum
from typing import Union


class SafeOperationEnum(IntEnum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2


SafeOperationLike = Union[SafeOperationEnum, int]
