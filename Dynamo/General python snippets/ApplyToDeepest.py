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


# Examples
a = 4
b = [4, [2, 5, [3, 4]], 7]
print(apply_to_deepest(my_square, a))  # 16
print(apply_to_deepest(my_square, b))  # [16, [4, 25, [9, 16]], 49]
