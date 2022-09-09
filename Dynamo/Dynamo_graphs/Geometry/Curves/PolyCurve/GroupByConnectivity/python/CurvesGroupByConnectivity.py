"""Groups Curves by connectivity.
Script does not check for duplicated curves. Do it yourself before grouping!
"""

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *


def tolist(obj1):
    # type: (list | None ) -> list
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]


def almost_equal(a, b, abs_tol=0.0):
    if connection_tolerance:  # gotta use it as global
        rel_tol = connection_tolerance
    else:
        rel_tol = 1e-09
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def are_points_equal(pt1, pt2):
    # type(Point, Point) -> bool
    return all((almost_equal(pt1.X, pt2.X),
               almost_equal(pt1.Y, pt2.Y),
               almost_equal(pt1.Z, pt2.Z)))


def are_curves_connected(curve1, curve2):
    # type(Curve, Curve) -> bool
    """Checks if lines have common point"""
    p11 = curve1.StartPoint
    p12 = curve1.EndPoint
    p21 = curve2.StartPoint
    p22 = curve2.EndPoint
    return any((are_points_equal(p11, p21),
                are_points_equal(p11, p22),
                are_points_equal(p12, p21),
                are_points_equal(p12, p22)))


def get_neighbors(curves_dict):
    # type: (dict) -> list[set[dict.key]]
    """Gets all neighbors for each line
        as list of sets of dictionary keys"""
    all_neighbours = []
    for i in curves_dict.keys():
        sub_neighbours = {i}
        for j in curves_dict.keys():
            if j != i and are_curves_connected(curves_dict[i], curves_dict[j]):
                sub_neighbours.add(j)
        all_neighbours.append(sub_neighbours)
    return all_neighbours


def merge_touching_sets(sets):
    # type: (list[set]) -> list[set]
    """Merges sets with common elements.
        Source: https://stackoverflow.com/a/9400562
    """
    new_group = []
    while len(new_group) != len(sets):
        new_group, sets = sets, []
        for set1 in new_group:
            for set2 in sets:
                if not set1.isdisjoint(set2):
                    set2.update(set1)
                    break
            else:
                sets.append(set1)
    return sets


def group_by_connectivity(curves):
    # type: (list[Curve]) -> list[list[Curve]]
    """Groups curves by their connectivity."""
    curves_dict = {i: v for i, v in enumerate(curves)}
    neighbors = get_neighbors(curves_dict)
    merged = merge_touching_sets(neighbors)
    return [[curves_dict[k] for k in group] for group in merged]


curves = tolist(IN[0])  # type: list[Curve]
connection_tolerance = IN[1]  # type: float

OUT = group_by_connectivity(curves)
