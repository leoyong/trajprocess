import numbers


def isnumbrer(x):
    if isinstance(x, numbers.Number) and not isinstance(x, bool):
        return True
    else:
        return False