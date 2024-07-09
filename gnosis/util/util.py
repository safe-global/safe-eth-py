from typing import Any, Iterable, Sequence


def chunks(elements: Sequence[Any], n: int) -> Iterable[Any]:
    """
    :param elements: List
    :param n: Number of elements per chunk
    :return: Yield successive n-sized chunks from l
    """
    for i in range(0, len(elements), n):
        yield elements[i : i + n]
