from enum import IntEnum


class SafeOperationEnum(IntEnum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2


SafeOperationLike = SafeOperationEnum | int
