"""Finds intersection of Line and Plane.
Returns Intersection Point if there is any. Otherwise return None.
Works with bound and unbound lines
Source: https://stackoverflow.com/a/18543221
"""

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Line, Plane, XYZ


def line_plane_intersection(line, plane):
    # type: (Line, Plane) -> XYZ | None
    line_orig = line.Origin
    line_dir = line.Direction
    dot_prod = line_dir.DotProduct(plane.Normal)
    intersection = None
    if abs(dot_prod) > 1e-9:
        w = line_orig.Subtract(plane.Origin)
        factor = - plane.Normal.DotProduct(w) / dot_prod
        if not line.IsBound or not (factor < 0 or factor > 1):
            scale = line_dir.Multiply(factor)
            intersection = line_orig.Add(scale)
    return intersection
