"""A function for testing approximate equality of two numbers.
Same as math.isclose in Python v3.5 (and newer)
https://www.python.org/dev/peps/pep-0485
"""


def almost_equal(a, b, rel_tol=1e-09, abs_tol=0.0):
    """A function for testing approximate equality of two numbers.
    Same as math.isclose in Python v3.5 (and newer)
    https://www.python.org/dev/peps/pep-0485
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


# Examples:
almost_equal(5.2, 5.2)  # True
almost_equal(5.201, 5.202)  # False
almost_equal(5.201, 5.202, 0.1)  # True
