"""Groups Lines by connectivity.
Script does not check for duplicated lines. Do it yourself before grouping!
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


def almost_equal(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def are_points_equal(pt1, pt2):
    # type(Point, Point) -> bool
    return all((almost_equal(pt1.X, pt2.X),
               almost_equal(pt1.Y, pt2.Y),
               almost_equal(pt1.Z, pt2.Z)))


def are_lines_connected(line1, line2):
    # type(Curve, Curve) -> bool
    """Checks if lines have common point"""
    p11 = line1.StartPoint
    p12 = line1.EndPoint
    p21 = line2.StartPoint
    p22 = line2.EndPoint
    return any((are_points_equal(p11, p21),
                are_points_equal(p11, p22),
                are_points_equal(p12, p21),
                are_points_equal(p12, p22)))


def get_neighbors(lines_dict):
    # type: (dict) -> list[set[dict.key]]
    """Gets all neighbors for each line
        as list of sets of dictionary keys"""
    all_neighbours = []
    for i, line in lines_dict.items():
        sub_neighbours = {i}
        for j, line in lines_dict.items():
            if j != i and are_lines_connected(lines_dict[i], line):
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


def group_by_connectivity(lines):
    # type: (list[Line]) -> list[list[Line]]
    """Groups lines by their connectivity."""
    lines_dict = {i: v for i, v in enumerate(lines)}
    neighbors = get_neighbors(lines_dict)
    merged = merge_touching_sets(neighbors)
    return [[lines_dict[k] for k in group] for group in merged]


lines = tolist(IN[0])  # type: list[Line]

OUT = group_by_connectivity(lines)
