import clr
from System import Enum

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter, LabelUtils


def get_built_in_parameter_label(bip_name):
    # type: (str) -> str
    if Enum.IsDefined(BuiltInParameter, bip_name):
        bip_param = Enum.Parse(BuiltInParameter, bip_name)
        bip_label = LabelUtils.GetLabelFor(bip_param)
        return bip_label
    else:
        return None


# Example:
get_built_in_parameter_label("VIEW_SHOW_GRIDS")  # "Show Grids"
