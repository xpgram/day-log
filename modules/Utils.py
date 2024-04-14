from typing import TypeVar

T = TypeVar('T')
Y = TypeVar('Y')


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

def inverseMap(d: dict[T, Y]) -> dict[Y, T]:
    """Given a dictionary of keys to values, returns a new dictionary of values to keys.
    Maps without strictly unique values are not accomodatable; raises KeyError."""
    result = {}
    for key, value in d.items():
        if result.get(value):
            raise KeyError("Failed to inverse map: key has already be set; value is not strictly unique.")
        result[value] = key
    return result

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

def getToken(stream: str, delim=' ') -> tuple[str, str]:
    "Returns a tuple containing the next stream token and the remaining input stream."

    index = stream.find(delim)
    index = len(stream) if index == -1 else index

    token = stream[:index]
    reducedStream = stream[index + len(delim):]
    return (token, reducedStream)

def getTokens(stream: str, numTokens=1, delim=' ') -> tuple[list[str], str]:
    """Returns a tuple containing an array of up to length n of the next n tokens, and the
    remaining input stream."""
    tokens = []

    for i in range(0, numTokens):
        token, stream = getToken(stream, delim)
        if token == '':
            break
        tokens.append(token)

    return (tokens, stream)
