"""
Extend line segment ends to closest curves
*Hereafter line segment called line and endless line called unbound line.
"""

import clr
from itertools import chain
from operator import itemgetter

clr.AddReference("RevitAPI")
clr.AddReference("RevitNodes")
from Autodesk.Revit.DB import *

import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)


def tolist(obj1):
    # type: (list | None ) -> list
    """Convert to list if not list."""
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]


def get_intersection(line_1, curve):
    # type: (Line, Curve) -> Point | list
    """Get intersection of line and curve.
    If no intersection, return empty list
    Orig by Gui Talarico https://github.com/gtalarico
    """
    results = clr.Reference[IntersectionResultArray]()
    result = line_1.Intersect(curve, results)
    if result == SetComparisonResult.Overlap:
        result_indexes = range(0, results.Size)
        intersection = [results.Item[i].XYZPoint for i in result_indexes]
    else:
        intersection = []
        # report = str(result)
    return intersection


line_to_extend_ds = IN[0]
other_lines_ds = tolist(IN[1])

line_to_extend = line_to_extend_ds.ToRevitType()
other_lines = [line.ToRevitType() for line in other_lines_ds]
end1 = line_to_extend.GetEndPoint(0)
line_1_dir = line_to_extend.Direction

unbound_line = Line.CreateUnbound(end1, line_1_dir)
intersections = [get_intersection(unbound_line, line) for line in other_lines]
intersections_flat = list(chain.from_iterable(intersections))

# Make new line by closest intersection points if there is any
if len(intersections_flat) > 0:
    end2 = line_to_extend.GetEndPoint(1)
    points_beh_end1 = []
    points_beh_end2 = []
    for pnt_i in intersections_flat:
        vector_e1i = pnt_i.Subtract(end1)
        vector_e2i = pnt_i.Subtract(end2)
        if line_1_dir.DotProduct(vector_e1i) < 0:
            points_beh_end1.append((pnt_i, end1.DistanceTo(pnt_i)))
        if line_1_dir.DotProduct(vector_e2i) > 0:
            points_beh_end2.append((pnt_i, end2.DistanceTo(pnt_i)))
    if len(points_beh_end1) > 0:
        new_end1 = min(points_beh_end1, key=itemgetter(1))[0]
    else:
        new_end1 = end1
    if len(points_beh_end2) > 0:
        new_end2 = min(points_beh_end2, key=itemgetter(1))[0]
    else:
        new_end2 = end2
    new_line_ds = Line.CreateBound(new_end1, new_end2).ToProtoType()
else:
    new_line_ds = line_to_extend_ds

OUT = new_line_ds
