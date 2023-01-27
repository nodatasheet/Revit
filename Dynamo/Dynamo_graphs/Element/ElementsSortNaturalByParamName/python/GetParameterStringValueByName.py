import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


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

    _validate_type(_elem, Element)
    _param = _lookup_param(_elem, _param_name)
    if _param is not None:
        wrapped_param = ParameterWrapper(_param)
        if wrapped_param.value_is_invalid_element_id:
            return None
        custom_format = None
        if wrapped_param._is_measurable:
            doc_unit_opts = \
                doc.GetUnits().GetFormatOptions(wrapped_param.unit_type)
            custom_format = CustomFormatOptions(doc_unit_opts)
            custom_format.strip_symbol()
        return wrapped_param.as_value_string(custom_format)


class ParameterWrapper(object):
    """Revit Parameter wrapper to """
    def __init__(self, parameter):
        # type: (Document, Parameter) -> None
        self._parameter = parameter

    def as_value_string(self, format_options):
        if format_options is not None:
            return self._parameter.AsValueString(format_options)
        return self._parameter.AsValueString()

    @property
    def _is_measurable(self):
        # type: () -> bool
        if self.unit_type is not None:
            if self._revit_ver < 2021:
                return UnitUtils.IsValidUnitType(self.unit_type)
            return UnitUtils.IsMeasurableSpec(self.unit_type)
        return False

    @property
    def unit_type(self):
        # type: () -> UnitType | SpecTypeId
        if self._revit_ver < 2021:
            return self._parameter.Definition.UnitType()
        return self._parameter.Definition.GetDataType()

    @property
    def value_is_invalid_element_id(self):
        # type: () -> bool
        return self._value_is_element_id \
            and self._parameter.AsElementId() == ElementId.InvalidElementId

    @property
    def _value_is_element_id(self):
        # type: () -> bool
        return self._parameter == StorageType.ElementId


class CustomFormatOptions(object):
    _app = DocumentManager.Instance.CurrentUIApplication.Application
    _revit_ver = int(_app.VersionNumber)
    _custom_opts = None

    def __init__(self, format_options):
        # type: (FormatOptions) -> None
        self._custom_opts = format_options

    def strip_symbol(self):
        # type: () -> FormatOptions
        """Gets number format options to show a value without the units."""
        unitless_options = self._set_symbol_type(self._empty_symbol)
        return unitless_options

    def _set_symbol_type(self, symbol_type):
        # type: (ForgeTypeId | UnitSymbolType) -> FormatOptions
        if self._revit_ver < 2021:
            self._custom_opts.UnitSymbol = symbol_type
        else:
            self._custom_opts.SetSymbolTypeId(symbol_type)
        return self._custom_opts

    @property
    def _empty_symbol(self):
        # type: () -> ForgeTypeId | UnitSymbolType
        if self._revit_ver < 2021:
            return UnitSymbolType.UST_NONE
        return ForgeTypeId()


doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application
rvt_ver = ': '.join(('Revit Version', app.SubVersionNumber))

windows = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Windows)\
    .WhereElementIsElementType()\
    .ToElements()

width_param_name = LabelUtils.GetLabelFor(BuiltInParameter.GENERIC_WIDTH)
widths = [get_param_string_value_by_name(w, width_param_name) for w in windows]

print(rvt_ver)
print(widths[:5])
OUT = rvt_ver, widths
