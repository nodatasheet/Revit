"""Convert object to list if it is not a list."""


def tolist(obj1):
    # type: (list | None ) -> list
    """Converts object to list if it is not iterable."""
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]


# Example
tolist("item")  # ["item"]
tolist(["list", "of", "items"])  # ["list", "of", "items"]
