import math


def truncate(number: float, decimals: int = 2) -> float:
    factor = 10**decimals
    return math.trunc(number * factor) / factor
