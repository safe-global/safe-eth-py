from enum import Enum


class SafeOperationEnum(Enum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2
