"""Converts a number to a string without trailing zeros.
This method may return scientific notation of very big numbers.
If that is a problem, consider other methods:
https://stackoverflow.com/a/37736333
"""

from numbers import Number
from System.Globalization import CultureInfo


def tolist(obj):
    # type: (object) -> list
    """Converts an object to a list if it is not a list"""
    if isinstance(obj, list):
        return obj
    return [obj]


def number_to_string(num):
    # type: (Number) -> str
    """Converts a number to a string without trailing zeros"""
    s = str(num)
    if s == '0':
        return '0'
    return s.rstrip('0').rstrip('.')


def validate_number(obj):
    # type: (object) -> None
    """Validates that object is a Number"""
    try:
        if isinstance(obj, bool):
            raise TypeError('<bool> is not a Number')
        float(obj)
    except Exception:
        raise TypeError(
            'Object <{}> is not a Number'.format(type(obj).__name__)
        )


# input number or list of numbers
input_numbers = tolist(IN[0])

# get local decimal separator, in case it is not a dot
decimal_separator = \
    CultureInfo.CurrentCulture.NumberFormat.NumberDecimalSeparator

output_strings = []
for num in input_numbers:
    validate_number(num)
    string_from_number = number_to_string(num)
    localized_string = string_from_number.replace('.', decimal_separator)
    output_strings.append(localized_string)

OUT = output_strings
