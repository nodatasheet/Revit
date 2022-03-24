"""Convert number to string without trailing zeros.
This method may return scientific notation with very big numbers.
If this is a problem, consider other methods:
https://stackoverflow.com/a/37736333
"""


def num_to_str(nmbr):
    # type: (None) -> str
    """Number to string without trailing zeros"""
    s = str(nmbr)
    return '0' if s == '0' else s.rstrip('0').rstrip('.')


# input number or list of numbers
inp_nmbr = IN[0]

if hasattr(inp_nmbr, '__iter__'):
    s = map(num_to_str, inp_nmbr)
else:
    s = num_to_str(inp_nmbr)

OUT = s
