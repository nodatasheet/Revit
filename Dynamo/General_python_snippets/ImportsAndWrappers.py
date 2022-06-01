"""
Describe Imports and Conversions in Python code for Dynamo.
https://github.com/DynamoDS/Dynamo/wiki/Python-0.6.3-to-0.7.x-Migration"""

import clr


""" Collections """
from System.Collections.Generic import List


""" Document and Application """
clr.AddReference("RevitServices")
# Import DocumentManager 
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


""" Transaction Manager """
# Import DocumentManager and TransactionManager
from RevitServices.Transactions import TransactionManager

# TransactionManager is a layer around the regular Revit.DB.Transaction.
# It is preferable to use TransactionManager in Dynamo
# instead of regular transaction.
# To rollback your changes use regular transaction as a subtransaction
# inside the TransactionManager.
# More explanation:
# https://forum.dynamobim.com/t/transactionmanager-vs-transaction/7305/2
# Naming Transaction in TransactionManager is not supported.
# https://forum.dynamobim.com/t/name-a-transaction/23990/15

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# End Transaction - Preferable
TransactionManager.Instance.TransactionTaskDone()
# Force Close Transaction - If above doesn't work
TransactionManager.ForceCloseTransaction()

# Transaction with rollback
TransactionManager.Instance.EnsureInTransaction(doc)
sub_transaction = SubTransaction(doc)
sub_transaction.Start()
# some code here
if 'result is ok':
    sub_transaction.Commit()
else:
    sub_transaction.RollBack()
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


# Unwrap (from Dynamo to Revit)

#   Elements
    DynamoElement = UnwrapElement(IN[0])

#   Geometry
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


# Wrap (from Revit to Dynamo)

#   Elements
    Element.ToDSType(True)  # Not created in script, mark as Revit-owned
    Element.ToDSType(False)  # Created in script, mark as non-Revit-owned

#   Geometry
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
