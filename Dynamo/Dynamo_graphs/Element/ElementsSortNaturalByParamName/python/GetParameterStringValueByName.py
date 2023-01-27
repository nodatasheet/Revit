try:
    # assuming we're in RPS or pyRevit
    import clr

    clr.AddReference("RevitAPI")
    from Autodesk.Revit.DB import *

    app = __revit__.Application
    doc = __revit__.ActiveUIDocument.Document

except NameError:
    # ok, I guess, we're in Dynamo then =)
    import clr

    clr.AddReference("RevitAPI")
    from Autodesk.Revit.DB import *

    clr.AddReference("RevitServices")
    from RevitServices.Persistence import DocumentManager

    doc = DocumentManager.Instance.CurrentDBDocument
    app = DocumentManager.Instance.CurrentUIApplication.Application


def get_param_str_value_by_name(_elem, _param_name):
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

        if not wrapped_param.value_is_invalid_element_id:
            return wrapped_param.as_value_string(None)

        if wrapped_param._is_measurable:
            doc_unit_opts = \
                doc.GetUnits().GetFormatOptions(wrapped_param.unit_type)
            custom_format_opts = CustomFormatOptions(doc_unit_opts)
            custom_format_opts.strip_symbol()
            custom_format = custom_format_opts.format_options
            return wrapped_param.as_value_string(custom_format)


class ParameterWrapper(object):
    """Revit Parameter wrapper for cross-version usage"""
    _app = app
    _revit_ver = int(_app.VersionNumber)

    def __init__(self, parameter):
        # type: (Parameter) -> None
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
        # type: () -> SpecTypeId | UnitType
        if self._revit_ver < 2021:
            return self._parameter.Definition.UnitType()
        return self._parameter.Definition.GetDataType()

    @property
    def value_is_invalid_element_id(self):
        """Checks whether parameter value the invalid ElementId."""
        # type: () -> bool
        return self._parameter == StorageType.ElementId \
            and self._parameter.AsElementId() == ElementId.InvalidElementId


class CustomFormatOptions(object):
    """Revit FormatOptions wrapper for cross-version usage"""
    _app = app
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
        # type: (ForgeTypeId | UnitSymbolType) -> None
        if self._revit_ver < 2021:
            self._custom_opts.UnitSymbol = symbol_type
        else:
            self._custom_opts.SetSymbolTypeId(symbol_type)

    @property
    def format_options(self):
        # type: () -> FormatOptions
        return self._custom_opts

    @property
    def _empty_symbol(self):
        # type: () -> ForgeTypeId | UnitSymbolType
        if self._revit_ver < 2021:
            return UnitSymbolType.UST_NONE
        return ForgeTypeId()


rvt_ver = ': '.join(('Revit Version', app.SubVersionNumber))

win_types = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Windows)\
    .WhereElementIsElementType()\
    .ToElements()

width_param_name = LabelUtils.GetLabelFor(BuiltInParameter.GENERIC_WIDTH)
widths = [
    get_param_str_value_by_name(wt, width_param_name) for wt in win_types]

print(rvt_ver)
print(widths[:5])

OUT = rvt_ver, widths[:5]
