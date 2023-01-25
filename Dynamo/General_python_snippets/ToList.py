"""Converts an object to a list if it is not iterable or string."""


def tolist(obj):
    # type: (list | None ) -> list
    """Converts an object to a list if it is not iterable or string."""
    if hasattr(obj, '__iter__') and not isinstance(obj, str):
        return obj
    return [obj]


# Example
tolist("item")  # ["item"]
tolist(["list", "of", "items"])  # ["list", "of", "items"]
