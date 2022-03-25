"""Apply function to every deepest item in the list.
If object is a list, function is applied to every deepest item in the list.
If object is a single item, function is applied to it."""


def apply_to_deepest(fun, item):
    """Apply function to every deepest item in list"""
    if hasattr(item, '__iter__'):
        return [apply_to_deepest(fun, x) for x in item]
    else:
        return fun(item)


# Example
def my_square(x):
    return x * x


a = 4  # single item
b = [4, [2, 5, [3, 4]], 7]  # list of items

print (apply_to_deepest(my_square, a))
print (apply_to_deepest(my_square, b))
