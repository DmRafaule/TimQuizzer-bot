def in_percent(value: int, amount: int, suffix: str = "", prefix: str = "\t") -> str:
    return prefix + str(round(value * 100 / amount)) + "%" + suffix


def in_absolute(value: int, amount: int, suffix: str = "", prefix: str = "\t") -> str:
    return prefix + str(value) + suffix
