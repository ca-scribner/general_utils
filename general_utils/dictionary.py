def dictionaries_intersect(*dictionaries):
    """
    Returns True if any dictionaries passed share keys, otherwise returns False
    """
    if len(dictionaries) <= 1:
        raise ValueError(f"Invalid input.  Got {len(dictionaries)} dictionaries - must specify at least 2")
    total_count = 0
    keys = set()
    for d in dictionaries:
        total_count += len(d)
        keys.update(list(d.keys()))
    return not (len(keys) == total_count)