"""Sort Elements naturally by Parameter Value
using Autodesk.Revit.DB.NamingUtils.CompareNames comparer.

If Element does not have a valid Parameter or its Value is None,
it is ignored from sorting.
"""

import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

try:
    from dynamo import UnwrapElement, IN  # stubs for linter
except Exception:
    pass


def tolist(obj):
    # type: (object) -> list
    if hasattr(obj, '__iter__') and not isinstance(obj, str):
        return obj
    return [obj]


def comparer_to_key(comparer, arg_getter=None):
    """Converts a comparer into a key= function for sorting or ordering.
    Similar to functools.cmp_to_key() but optionally receives an arg_getter()

    Args:
        comparer: a function that compares two arguments and then returns
            a negative value for '<', zero for '==', or a positive for '>'
        arg_getter (optional): a function that extracts the argument
            from supplied object to use in comparer

    Returns:
        key function: a callable that returns a value for sorting or ordering

    Examples:
        >>> # Same as functools.cmp_to_key()
        >>> from Autodesk.Revit.DB.NamingUtils import CompareNames
        >>> sorted(['5', '10', '1'], key=comparer_to_key(CompareNames))
        ['1', '5', '10']
        >>>
        >>> # Using arg_getter()
        >>> from collections import namedtuple
        >>> Num = namedtuple('Num', 'val')
        >>> five = Num('5')
        >>> ten = Num('10')
        >>> one = Num('1')
        >>> sorted([five, ten, one],
        ...        key=comparer_to_key(CompareNames, lambda x: x.val))
        [Num(val='1'), Num(val='5'), Num(val='10')]
    """

    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj):
            self.obj = arg_getter(obj) if arg_getter else obj

        def __lt__(self, other):
            return comparer(self.obj, other.obj) < 0

        def __gt__(self, other):
            return comparer(self.obj, other.obj) > 0

        def __eq__(self, other):
            return comparer(self.obj, other.obj) == 0

        def __le__(self, other):
            return comparer(self._obj, other._obj) <= 0

        def __ge__(self, other):
            return comparer(self._obj, other._obj) >= 0

        def __ne__(self, other):
            return comparer(self._obj, other._obj) != 0

        __hash__ = None
    return K


def get_param_value_or_empty_str(elem, param_name):
    # type: (Element, str) -> int | float | str | ElementId
    validate_type(elem, Element)
    return get_param_value_as_string(elem, param_name) or str()


def get_param_value_as_string(elem, param_name):
    # type: (Element, str) -> int | float | str | ElementId
    param = get_param_by_name(elem, param_name)
    if param is not None:
        return get_value_as_unitless_string(param)


def get_param_by_name(elem, param_name):
    # type: (Element, str) -> Parameter
    instance_param = elem.LookupParameter(param_name)
    if instance_param is not None:
        return instance_param

    elem_type = doc.GetElement(elem.GetTypeId())
    if elem_type is not None:
        return elem_type.LookupParameter(param_name)


def get_param_value_by_name(elem, param_name):
    # type: (Element, str) -> int | float | str | ElementId
    instance_param = elem.LookupParameter(param_name)
    if instance_param is not None:
        return get_value_as_unitless_string(instance_param)
    elem_type = doc.GetElement(elem.GetTypeId())
    if elem_type is not None:
        type_param = elem_type.LookupParameter(param_name)
        if type_param is not None:
            return get_value_as_unitless_string(type_param)


def validate_type(obj, expected_type):
    # type: (object, type) -> None
    """Assures that object is of expected type."""
    if not isinstance(obj, expected_type):
        raise TypeError(
            'Expected <{}>, got <{}>'.format(expected_type.__name__,
                                             type(obj).__name__))


def get_value_as_unitless_string(param):
    # type: (Parameter) -> str
    """Gets Parameter value as it is seen by the user,
    but without the units.
    """
    spec_type = param.Definition.GetDataType()
    if UnitUtils.IsMeasurableSpec(spec_type):
        doc_unit_opts = doc.GetUnits().GetFormatOptions(spec_type)
        custom_opts = FormatOptions(doc_unit_opts)
        empty_symbol = ForgeTypeId()
        custom_opts.SetSymbolTypeId(empty_symbol)
        return param.AsValueString(custom_opts)
    return get_value_as_string(param)


def get_value_as_string(param):
    # type: (Parameter) -> str
    """Gets Parameter value as it is seen by the user."""
    if not value_is_invalid_element_id(param):
        return param.AsValueString()


def value_is_invalid_element_id(param):
    # type: (Parameter) -> bool
    return param.StorageType == StorageType.ElementId \
        and param.AsElementId() == ElementId.InvalidElementId


unsorted_elems = tolist(UnwrapElement(IN[0]))
param_name = IN[1]

doc = DocumentManager.Instance.CurrentDBDocument

sorted_elems = sorted(
    unsorted_elems, key=comparer_to_key(
        NamingUtils.CompareNames,
        lambda x: str(get_param_value_or_empty_str(x, param_name)))
)

sorted_param_vals = [
    get_param_value_by_name(e, param_name) for e in sorted_elems]

OUT = sorted_elems, sorted_param_vals
