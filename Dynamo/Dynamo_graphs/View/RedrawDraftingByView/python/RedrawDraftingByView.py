"""Redraw Drafting View by the given View"""

import os
import clr
import shutil
import tempfile
import traceback
import uuid

clr.AddReference("RevitNodes")
import Revit  # type: ignore
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

from System import Type
from System.Collections.Generic import List

try:
    from dynamo import UnwrapElement, IN  # stubs for linter
except Exception:
    pass

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def export_to_dwg(dir_path, file_name, view, options=DWGExportOptions()):
    # type: (os.path, str, View, DWGExportOptions) -> bool
    """Export view to AutoCAD DWG file."""
    view_id = List[ElementId]()
    view_id.Add(view.Id)
    export_result = doc.Export(dir_path, file_name, view_id, options)
    if export_result is True:
        return export_result
    else:
        raise UserWarning("Could not export DWG ({})".format(view.Title))


def on_dialog_temp_view_mode(sender, event_arg):
    """On dialog: Export with Temporary Hide/Isolate
    Choose: Leave the Temporary Hide/Isolate mode on and export"""
    try:
        really_print = 'TaskDialog_Really_Print_Or_Export_Temp_View_Modes'
        if event_arg.DialogId == really_print:
            event_arg.OverrideResult(1002)
            # 1001 call TaskDialogResult.CommandLink1
            # 1002 call TaskDialogResult.CommandLink2
    except Exception:
        return traceback.format_exc()


def import_dwg(file_path, view):
    # type: (str, View) -> ElementId
    imported_id = clr.Reference[ElementId]()
    options = DWGImportOptions()
    options.ThisViewOnly = True
    imported = doc.Import(file_path, options, view, imported_id)
    if imported is True:
        return imported_id.Value
    else:
        raise UserWarning("Could not import DWG ({})".format(view.Title))


def polyline_to_curve_array(polyline):
    # type: (PolyLine) -> CurveArray
    """Convert PolyLine to CurveArray skipping excessively short curves"""
    points = polyline.GetCoordinates()
    curve_array = CurveArray()
    for i in range(len(points) - 1):
        if points[i].DistanceTo(points[i + 1]) > app.ShortCurveTolerance:
            line = Line.CreateBound(points[i], points[i + 1])
            curve_array.Append(line)
    return curve_array


def set_line_style(curve, line_style):
    # type: (DetailCurve, GraphicsStyle) -> None
    curve.LineStyle = line_style


def has_short_curve(curve_loop):
    # type: (CurveLoop) -> bool
    return any(c.Length < app.ShortCurveTolerance for c in curve_loop)


source_view = UnwrapElement(IN[0])  # type: View
filled_region_type = UnwrapElement(IN[1])  # type: FilledRegionType
line_style = UnwrapElement(IN[2])  # type: GraphicsStyle
dest_view = UnwrapElement(IN[3])  # type: View

source_view_id = source_view.Id

uiapp.DialogBoxShowing += on_dialog_temp_view_mode

try:
    TransactionManager.Instance.EnsureInTransaction(doc)
    sub_transaction = SubTransaction(doc)
    sub_transaction.Start()

    source_view.HideCategoryTemporary(
        ElementId(BuiltInCategory.OST_Dimensions))

    if source_view.ViewType == ViewType.ThreeD:
        view_to_export = ViewSheet.Create(doc, ElementId(-1))
        view_copy = source_view.Duplicate(ViewDuplicateOption.WithDetailing)
        Viewport.Create(doc, view_to_export.Id, view_copy, XYZ(0, 0, 0))
    else:
        view_to_export = source_view

    # Prepare temp path
    temp_dir = tempfile.mkdtemp()
    temp_file_name = str(uuid.uuid4()) + ".dwg"
    temp_file_path = os.path.join(temp_dir, temp_file_name)

    # Setup DWG Export Options
    dwg_export_options = DWGExportOptions()
    dwg_export_options.MergedViews = True
    dwg_export_options.Colors = ExportColorMode.TrueColorPerView
    dwg_export_options.PreserveCoincidentLines = False

    export_to_dwg(temp_dir, temp_file_name, view_to_export, dwg_export_options)

    sub_transaction.RollBack()
    sub_transaction.Start()

    drafting_view = dest_view
    all_in_view = FilteredElementCollector(doc, drafting_view.Id).ToElements()

    to_delete = []
    for elem in all_in_view:
        if hasattr(elem, 'Name') and elem.Name == "ExtentElem":
            pass
        else:
            to_delete.append(elem.Id)
    doc.Delete(List[ElementId](to_delete))

    imported_dwg_id = import_dwg(temp_file_path, drafting_view)

    impoted_dwg = doc.GetElement(imported_dwg_id)
    geom_options = Options()
    geom_options.View = drafting_view
    geom_elems = impoted_dwg.get_Geometry(geom_options)

    CURVELIKE_GEOMETRY = (Arc, Curve, Ellipse, Line, NurbSpline, HermiteSpline)
    det_curves = []
    det_curve_arrays = []
    det_fill_regions = []
    skipped_geometry = []  # for testing

    for geom_elem in geom_elems:
        if isinstance(geom_elem, GeometryInstance):
            geom_objects = geom_elem.GetInstanceGeometry()
            for geom_obj in geom_objects:
                if isinstance(geom_obj, CURVELIKE_GEOMETRY):
                    if geom_obj.Length > app.ShortCurveTolerance:
                        det_curve = doc.Create.NewDetailCurve(
                            drafting_view,
                            geom_obj)
                        set_line_style(det_curve, line_style)
                        det_curves.append(det_curve)
                elif isinstance(geom_obj, PolyLine):
                    curve_array = polyline_to_curve_array(geom_obj)
                    if not curve_array.IsEmpty:
                        # After removing excessively short curves
                        det_curve_array = doc.Create.NewDetailCurveArray(
                            drafting_view,
                            curve_array)
                        [set_line_style(c, line_style) for c in det_curve_array]
                        det_curve_arrays.append(det_curve_array)
                elif isinstance(geom_obj, Solid):
                    # Imported fill patterns represented as flat solids
                    faces = geom_obj.Faces
                    for face in faces:
                        face_edges = face.GetEdgesAsCurveLoops()
                        if not any(has_short_curve(loop) for loop in face_edges):
                            try:
                                fill_region = FilledRegion.Create(
                                    doc,
                                    filled_region_type.Id,
                                    drafting_view.Id,
                                    face_edges)
                                fill_region.SetLineStyleId(line_style.Id)
                                det_fill_regions.append(fill_region)
                            except Exception:
                                pass

    drafting_view.Scale = source_view.Scale
    doc.Delete(imported_dwg_id)
    shutil.rmtree(temp_dir, True)

    sub_transaction.Commit()
    TransactionManager.Instance.TransactionTaskDone()
    result = drafting_view, [det_curves, det_curve_arrays, det_fill_regions]

except Exception:
    shutil.rmtree(temp_dir, True)
    result = traceback.format_exc()
    sub_transaction.RollBack()
    TransactionManager.Instance.TransactionTaskDone()

uiapp.DialogBoxShowing -= on_dialog_temp_view_mode

OUT = result
