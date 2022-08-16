"""
Finds Bounding Box Center.
yes.. that simple
"""

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import XYZ, BoundingBoxXYZ


def bbox_center(bbox):
    # type: (BoundingBoxXYZ) -> XYZ
    return (bbox.Min + bbox.Max) / 2
