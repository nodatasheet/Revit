"""Try to remove paint from multiple faces."""

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

surfs = UnwrapElement(IN[0])

was_painted = []
was_not_painted = []
paint_removed = []
failed_to_remove = []
failure_exceptions = []

TransactionManager.Instance.EnsureInTransaction(doc)
for surf in surfs:
    try:
        ref = surf.Tags.LookupTag("RevitFaceReference")
        elem = doc.GetElement(ref)
        face = elem.GetGeometryObjectFromReference(ref)
        if doc.IsPainted(elem.Id, face):
            was_painted.append(face.Id)
            doc.RemovePaint(elem.Id, face)
            if doc.IsPainted(elem.Id, face):
                failed_to_remove.append(face.Id)
            else:
                paint_removed.append(face.Id)
        else:
            was_not_painted.append(face.Id)
    except Exception as err:
        failed_to_remove.append(surf)
        failure_exceptions.append('{},\nElement: {}'.format(err, elem.Name))
TransactionManager.Instance.TransactionTaskDone()

OUT = surfs, was_painted, was_not_painted, paint_removed, failed_to_remove, failure_exceptions