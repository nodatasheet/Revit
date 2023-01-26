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


def get_param_string_value_by_name(_elem, _param_name):
    # type: (Element, str) -> str
    """Gets Element's parameter string value by the given parameter name.

    Returned value is the same as it is seen by the user,
    but without the units.
    """

    def _validate_type(obj, expected_type):
        # type: (object, type) -> None
        """Assures that object is of expected type."""
        if not isinstance(obj, expected_type):
            raise TypeError(
                'Expected <{}>, got <{}>'.format(expected_type.__name__,
                                                 type(obj).__name__))

    def _lookup_param(_elem, _param_name):
        # type: (Element, str) -> Parameter
        """Gets Element's instance or type parameter by the given name."""
        instance_param = _elem.LookupParameter(_param_name)
        if instance_param is not None:
            return instance_param
        elem_type = doc.GetElement(_elem.GetTypeId())
        if elem_type is not None:
            return elem_type.LookupParameter(_param_name)

    def _get_value_as_unitless_string(_param):
        # type: (Parameter) -> str
        """Gets value as it is seen by the user, but without the units."""
        unitless_format_opts = _get_unitless_format_opts(_param)
        if unitless_format_opts is not None:
            return _param.AsValueString(unitless_format_opts)
        return _get_value_as_string(_param)

    def _get_unitless_format_opts(_param):
        # type: (Parameter) -> FormatOptions
        """Gets number format options to show value without the units."""

        def _get_unit_type(_param, revit_ver):
            # type: (Parameter, int) -> UnitType | SpecTypeId
            if revit_ver < 2021:
                return _param.Definition.UnitType()
            return _param.Definition.GetDataType()

        def _is_measurable(unit_type, revit_ver):
            # type: (Parameter) -> bool
            if revit_ver < 2021:
                return UnitUtils.IsValidUnitType(unit_type)
            return UnitUtils.IsMeasurableSpec(unit_type)

        def _get_empty_symbol(revit_ver):
            # type: (int) -> UnitSymbolType | ForgeTypeId
            if revit_ver < 2021:
                return UnitSymbolType.UST_NONE
            return ForgeTypeId()

        def _set_symbol_type(format_opts, symbol_type, revit_ver):
            # type: (FormatOptions, UnitSymbolType | ForgeTypeId, int) -> FormatOptions
            if revit_ver < 2021:
                format_opts.UnitSymbol = symbol_type
            else:
                format_opts.SetSymbolTypeId(symbol_type)
            return format_opts

        revit_ver = int(app.VersionNumber)
        unit_type = _get_unit_type(_param, revit_ver)

        if _is_measurable(unit_type, revit_ver):
            doc_unit_opts = doc.GetUnits().GetFormatOptions(unit_type)
            custom_opts = FormatOptions(doc_unit_opts)
            empty_symbol = _get_empty_symbol(revit_ver)
            return _set_symbol_type(custom_opts, empty_symbol, revit_ver)

    def _get_value_as_string(_param):
        # type: (Parameter) -> str
        """Gets value as it is seen by the user."""
        if not _value_is_invalid_element_id(_param):
            return _param.AsValueString()

    def _value_is_invalid_element_id(_param):
        # type: (Parameter) -> bool
        return _param.StorageType == StorageType.ElementId \
            and _param.AsElementId() == ElementId.InvalidElementId

    _validate_type(_elem, Element)
    _param = _lookup_param(_elem, _param_name)
    if _param is not None:
        return _get_value_as_unitless_string(_param)


unsorted_elems = tolist(UnwrapElement(IN[0]))
param_name = IN[1]

doc = DocumentManager.Instance.CurrentDBDocument  # type: Document
app = DocumentManager.Instance.CurrentUIApplication.Application

sorted_elems = sorted(
    unsorted_elems, key=comparer_to_key(
        NamingUtils.CompareNames,
        lambda e: get_param_string_value_by_name(e, param_name) or str())
)

sorted_param_vals = [
    get_param_string_value_by_name(e, param_name) for e in sorted_elems]

OUT = sorted_elems, sorted_param_vals
