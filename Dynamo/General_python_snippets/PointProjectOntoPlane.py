"""Project a 3D point orthogonally onto a Plane.
Starting Revit 2018.1 can use Plane.Project() method instead."""

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import XYZ, Plane, Point


def point_project_onto_plane(point, plane):
    # type: (XYZ, Plane) -> Point
    normal = plane.Normal
    vec_to_orig = point - plane.Origin
    signed_dist = normal.DotProduct(vec_to_orig)
    return point - (normal * signed_dist)
