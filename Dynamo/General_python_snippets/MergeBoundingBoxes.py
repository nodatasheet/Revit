"""
Merge multiple Bounding Boxes into a single Bounding Box.
kudos to Pavel Altynnikov https://github.com/PavelAltynnikov
"""

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import XYZ, BoundingBoxXYZ


def merge_bounding_boxes(bboxes):
    # type: (list) -> BoundingBoxXYZ
    """Merges multiple bounding boxes"""
    merged_bb = BoundingBoxXYZ()
    merged_bb.Min = XYZ(
        min(bboxes, key=lambda bb: bb.Min.X).Min.X,
        min(bboxes, key=lambda bb: bb.Min.Y).Min.Y,
        min(bboxes, key=lambda bb: bb.Min.Z).Min.Z
    )
    merged_bb.Max = XYZ(
        max(bboxes, key=lambda bb: bb.Max.X).Max.X,
        max(bboxes, key=lambda bb: bb.Max.Y).Max.Y,
        max(bboxes, key=lambda bb: bb.Max.Z).Max.Z
    )
    return merged_bb
