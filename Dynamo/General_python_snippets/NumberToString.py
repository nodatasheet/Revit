"""Converts number to string without trailing zeros.
This method may return scientific notation of very big numbers.
If that is a problem, consider other methods:
https://stackoverflow.com/a/37736333
"""

from numbers import Number
from System.Globalization import CultureInfo


def tolist(obj):
    # type: (object) -> list
    """Converts object to list if it is not a list"""
    if isinstance(obj, list):
        return obj
    return [obj]


def number_to_string(num):
    # type: (Number) -> str
    """Converts number to string without trailing zeros"""
    s = str(num)
    return '0' if s == '0' else s.rstrip('0').rstrip('.')


def validate_type(obj, expected_type):
    # type: (object, type) -> None
    """Validates that object is of expected type"""
    if not isinstance(obj, expected_type):
        raise TypeError(
            'Expected <{}>, got <{}>'.format(expected_type.__name__,
                                             type(obj).__name__)
        )


# input number or list of numbers
input_numbers = tolist(IN[0])

# local separator, in case it is not a dot
decimal_separator = \
    CultureInfo.CurrentCulture.NumberFormat.NumberDecimalSeparator

output_strings = []
for num in input_numbers:
    validate_type(num, Number)
    string_from_number = number_to_string(num)
    localized_string = string_from_number.replace('.', decimal_separator)
    output_strings.append(localized_string)

OUT = output_strings
