"""Convert object to list if it is not a list."""


def tolist(obj1):
    # type: (list | None ) -> list
    """Convert to list if not list."""
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]


# Example
a = "item"
b = ["list", "of", "items"]

print (tolist(a))
print (tolist(b))
