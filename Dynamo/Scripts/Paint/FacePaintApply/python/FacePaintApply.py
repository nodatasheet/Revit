"""Try to apply paint to multiple faces."""

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
mat = UnwrapElement(IN[1])
override = IN[2]

paint_applied = []
paint_ignored = []
failed_to_apply = []
failure_exceptions = []

TransactionManager.Instance.EnsureInTransaction(doc)
for surf in surfs:
    try:
        ref = surf.Tags.LookupTag("RevitFaceReference")
        elem = doc.GetElement(ref)
        face = elem.GetGeometryObjectFromReference(ref)
        if not override and doc.IsPainted(elem.Id, face):
            paint_ignored.append(surf)
        else:
            doc.Paint(elem.Id, face, mat.Id)
            if doc.IsPainted(elem.Id, face):
                paint_applied.append(surf)
            else:
                failed_to_apply.append(surf)
    except Exception as err:
        failed_to_apply.append(surf)
        failure_exceptions.append('{},\nElement: {}'.format(err, elem.Name))
TransactionManager.Instance.TransactionTaskDone()

OUT = surfs, paint_applied, paint_ignored, failed_to_apply, failure_exceptions
