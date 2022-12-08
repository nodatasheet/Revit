"""Sort Elements naturally by multiple attributes
using Revit's comparison rules.

Sorting is multilevel by the order of supplied attributes."""

import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import NamingUtils


def cmp_to_key_by_attrs(comparer, attrs):
    """Converts a comparer into a key= function
    for multilevel sorting or ordering by supplied attributes.

    Refer to functools.cmp_to_key() and operator.attrgetter().
    """

    class K(object):
        __slots__ = ['_obj']

        def __init__(self, obj, attr):
            self._validate_attr(attr)
            self._obj = self._resolve_attr(obj, attr)

        def _validate_attr(self, attr):
            if not isinstance(attr, str):
                raise TypeError(
                    'Expected string, got {}'.format(type(attr)))

        def _resolve_attr(self, obj, attr):
            for name in attr.split("."):
                obj = getattr(obj, name)
            return obj

        def __lt__(self, other):
            return comparer(self._obj, other._obj) < 0

        def __gt__(self, other):
            return comparer(self._obj, other._obj) > 0

        def __eq__(self, other):
            return comparer(self._obj, other._obj) == 0

        def __le__(self, other):
            return comparer(self._obj, other._obj) <= 0

        def __ge__(self, other):
            return comparer(self._obj, other._obj) >= 0

        def __ne__(self, other):
            return comparer(self._obj, other._obj) != 0

        __hash__ = None

    if not hasattr(attrs, '__iter__'):
        raise TypeError('Attributes must be iterable')

    if len(attrs) == 1:
        def call_k(obj):
            return K(obj, attrs[0])

    else:
        def call_k(obj):
            return tuple(K(obj, attr) for attr in attrs)

    return call_k


def names_comparer(name1, name2):
    """Compares two objects as strings using Revit's comparison rules"""
    return NamingUtils.CompareNames(str(name1), str(name2))


# example:
class TestElement:
    def __init__(self, type, name):
        self.type = type
        self.name = name


elems = [TestElement('b', 10),
         TestElement('b', '3'),
         TestElement('a', '5'),
         TestElement('a', 7)]


# sort elems by type, then by name
sorted_elems = sorted(
    elems,
    key=cmp_to_key_by_attrs(names_comparer, ['type', 'name'])
)

OUT = [[elem.type, elem.name] for elem in sorted_elems]

"""
[a, '5'],
[a, 7],
[b, '3'],
[b, 10]
"""
