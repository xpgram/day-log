
# TODO Some of these concern lists and dictionaries: should they be broken off?

def shift(array: list[T]) -> tuple[T, list[T]]:
    """Returns the first value of array a and the remaining values as a new list, or None and [] if
    a was empty to begin with."""
    value = array[0] if len(array) > 0 else None
    array = array[1:]
    return (value, array)

def get(index, array: list[T]) -> T | None:
    "Returns the value held by 'array' at 'index' if one exists, returns None if not."
    return array[index] if index >= 0 and index < len(array) else None

def findKey(pred, d) -> str | None:
    "Returns the first key to dictionary d where f( d[k] ) returns True, returns None otherwise."
    results = [k for k, v in d.items() if pred(v) == True]
    return results[0] if results else None

def stringToInt(s) -> int | None:
    "Converts a given string to a number, or returns None on failure."
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

def destructure(dict, *keys):
    """Returns a list of values for the given keys in the order they appear as arguments to this
    function."""
    return list(dict[key] for key in keys)
