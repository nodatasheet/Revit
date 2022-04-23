"""

https://github.com/DynamoDS/Dynamo/wiki/Python-0.6.3-to-0.7.x-Migration"""

import clr


""" Collections """
from System.Collections.Generic import List


""" Document and Application """

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# End Transaction
TransactionManager.Instance.TransactionTaskDone()


""" Elements unwrap/wrap """
# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
# Import ToDSType(bool) extension method
clr.ImportExtensions(Revit.Elements)
# Import ToProtoType(), ToRevitType() geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)


# Unwrap from Dynamo to Revit

# Elements
DynamoElement = UnwrapElement(IN[0])

# Geometry
    Point.ToRevitType()  # XYZ
    Vector.ToRevitType()  # XYZ
    Plane.ToPlane()  # Plane
    List<Point>.ToXyzs()  # List<XYZ>
    Curve.ToRevitType()  # Curve
    PolyCurve.ToRevitType()  # CurveLoop
    Surface.ToRevitType()  # IList<GeometryObject>
    Solid.ToRevitType()  # IList<GeometryObject>
    Mesh.ToRevitType()  # IList<GeometryObject>
    CoordinateSystem.ToTransform()  # Transform
    CoordinateSystem.ToRevitBoundingBox()  # BoundingBoxXYZ
    BoundingBox.ToRevitType()  # BoundingBoxXYZ


# Wrap from Revit to Dynamo

# Elements
    Element.ToDSType(True)  # Not created in script, mark as Revit-owned
    Element.ToDSType(False)  # Created in script, mark as non-Revit-owned
# Geometry
    XYZ.ToPoint()  # Point
    XYZ.ToVector()  # Vector
    Point.ToProtoType()  # Point
    List<XYZ>.ToPoints()  # List<Point>
    UV.ToProtoType()  # UV
    Curve.ToProtoType()  # Curve
    CurveArray.ToProtoType()  # PolyCurve
    PolyLine.ToProtoType()  # PolyCurve
    Plane.ToPlane()  # Plane
    Solid.ToProtoType()  # Solid
    Mesh.ToProtoType()  # Mesh
    IEnumerable<Mesh>.ToProtoType()  # Mesh[]
    Face.ToProtoType()  # IEnumerable<Surface>
    Transform.ToCoordinateSystem()  # CoordinateSystem
    BoundingBoxXYZ.ToProtoType()  # BoundingBox
