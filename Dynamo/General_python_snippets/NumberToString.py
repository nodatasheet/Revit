"""Convert number to string without trailing zeros.
This method may return scientific notation of very big numbers.
If that is a problem, consider other methods:
https://stackoverflow.com/a/37736333
"""


def num_to_str(num):
    # type: (None) -> str
    """Number to string without trailing zeros"""
    s = str(num)
    return '0' if s == '0' else s.rstrip('0').rstrip('.')


# input number or list of numbers
input_num = IN[0]

if hasattr(input_num, '__iter__'):
    str_from_num = map(num_to_str, input_num)
else:
    str_from_num = num_to_str(input_num)

OUT = str_from_num
