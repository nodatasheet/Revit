#Reset Material Properties to default

import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

def tolist(obj1):
    # type: (list | None ) -> list
    """Convert to list if not list."""
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
rev_ver=int(app.VersionNumber)

state = IN[0]
materials = UnwrapElement(tolist(IN[1]))

if state is True:

    TransactionManager.Instance.EnsureInTransaction(doc)

    for m in materials:
        if rev_ver < 2019:
            m.UseRenderAppearanceForShading = False
            m.Color = Autodesk.Revit.DB.Color.InvalidColorValue
            m.SurfacePatternId = surfaceForegroundPattern.Id
            m.SurfacePatternColor = Autodesk.Revit.DB.Color.InvalidColorValue
            m.SurfacePatternId = ElementId.InvalidElementId
            m.SurfacePatternColor = Autodesk.Revit.DB.Color.InvalidColorValue
            m.CutPatternId = ElementId.InvalidElementId
            m.CutPatternColor = Autodesk.Revit.DB.Color.InvalidColorValue
            m.CutPatternId = ElementId.InvalidElementId
            m.CutPatternColor = Autodesk.Revit.DB.Color.InvalidColorValue

        else:
            m.UseRenderAppearanceForShading = False
            m.Color = Autodesk.Revit.DB.Color.InvalidColorValue
            m.SurfaceForegroundPatternId = ElementId.InvalidElementId
            m.SurfaceForegroundPatternColor = Autodesk.Revit.DB.Color.InvalidColorValue
            m.SurfaceBackgroundPatternId = ElementId.InvalidElementId
            m.SurfaceBackgroundPatternColor = Autodesk.Revit.DB.Color.InvalidColorValue
            m.CutForegroundPatternId = ElementId.InvalidElementId
            m.CutForegroundPatternColor = Autodesk.Revit.DB.Color.InvalidColorValue
            m.CutBackgroundPatternId = ElementId.InvalidElementId
            m.CutBackgroundPatternColor = Autodesk.Revit.DB.Color.InvalidColorValue

    TransactionManager.Instance.TransactionTaskDone()

else:
    IN[1] = []  # empty list if state is false

OUT = IN[1]
