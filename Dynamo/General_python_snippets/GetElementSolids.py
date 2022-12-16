"""Retrieve Solids from the list of Elements"""

import clr

try:
    from dynamo import UnwrapElement, IN  # stubs for linter
except Exception:
    pass

clr.AddReference("RevitNodes")
import Revit  # type: ignore
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *


def validate_type(obj, expected_type):
    if isinstance(obj, expected_type):
        return True
    else:
        raise TypeError(
            'Expected <{}>, got <{}>'.format(expected_type.__name__,
                                             type(elem).__name__))


def get_element_solids(elem, geom_options):
    # type: (Element, Options) -> list[Solid]
    """Attempts to retrieve all Solids from the Element
    with the given Geometry Options
    """
    solids = []
    geom_elems = elem.get_Geometry(geom_options)
    for geom_elem in geom_elems:
        if isinstance(geom_elem, Solid):
            solids.append(geom_elem)
        elif isinstance(geom_elem, GeometryInstance):
            geom_objects = geom_elem.GetInstanceGeometry()
            for geom_obj in geom_objects:
                if isinstance(geom_obj, Solid):
                    solids.append(geom_obj)
    return solids


elems = UnwrapElement(IN[0])  # type: list[Element]

doc = DocumentManager.Instance.CurrentDBDocument  # type: Document
active_view = doc.ActiveView

geom_options = Options()
geom_options.View = active_view

all_solids = []
for elem in elems:
    validate_type(elem, Element)
    elem_solids = get_element_solids(elem, geom_options)
    all_solids.append(rvt_solid.ToProtoType() for rvt_solid in elem_solids)

OUT = all_solids
