"""
Selects elements filtered by built in category from linked document.
Shown example for pipes category.
"""

import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit import DB, UI, Exceptions

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = uiapp.ActiveUIDocument


class PickFromLinkByCatIdFilter(UI.Selection.ISelectionFilter):
    def __init__(self, built_in_cat_id):
        # type: (DB.ElementId) -> None
        self._bic_id = built_in_cat_id

    def AllowElement(self, element):
        # type: (DB.Element) -> bool
        return True

    def AllowReference(self, reference, position):
        # type: (DB.Reference, DB.XYZ) -> bool
        active_doc = doc
        referenced_elem = active_doc.GetElement(reference)

        if not isinstance(referenced_elem, DB.RevitLinkInstance):
            return False

        link_doc = referenced_elem.GetLinkDocument()
        linked_elem = link_doc.GetElement(reference.LinkedElementId)

        return self._allow_by_cat_id(linked_elem, self._bic_id)

    def _allow_by_cat_id(self, element, cat_id):
        # type: (DB.Element, DB.ElementId) -> bool
        try:
            if element.Category.Id == cat_id:
                return True
        except Exception:
            pass
        return False


def pick_elems_from_link_by_cat(built_in_category, message='Select Elements'):
    # type: (DB.BuiltInCategory, str) -> list[DB.Element]

    bic_id = DB.ElementId(built_in_category)
    pick_filter = PickFromLinkByCatIdFilter(bic_id)
    picked_elems = []

    try:
        picked_references = uidoc.Selection.PickObjects(
            UI.Selection.ObjectType.LinkedElement,
            pick_filter,
            message
        )  # type: list[DB.Reference]

    except Exceptions.OperationCanceledException:
        return []

    for picked_ref in picked_references:
        link_instance = doc.GetElement(picked_ref.ElementId)  # type: DB.RevitLinkInstance
        linked_doc = link_instance.GetLinkDocument()
        linked_elem = linked_doc.GetElement(picked_ref.LinkedElementId)
        picked_elems.append(linked_elem)

    return picked_elems


# example for pipes
picked_pipes = pick_elems_from_link_by_cat(
    built_in_category=DB.BuiltInCategory.OST_PipeCurves,
    message='Select pipes from link document and press "Finish"'
)

OUT = picked_pipes
