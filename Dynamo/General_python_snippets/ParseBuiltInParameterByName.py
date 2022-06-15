import clr
from System import Enum

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter


def parse_built_in_param(bip_name):
    # type: (str) -> Enum
    if Enum.IsDefined(BuiltInParameter, bip_name):
        return Enum.Parse(BuiltInParameter, bip_name)
    else:
        return None


# Example:
parse_built_in_param("VIEW_SHOW_GRIDS")  # BuiltInParameter.VIEW_SHOW_GRIDS
