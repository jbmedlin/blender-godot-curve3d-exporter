import bpy	
import os
from bpy import context
import builtins as __builtin__
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

bl_info = {
    "name": "Godot Curve3D Exporter",
    "author": "jbmedlin",
    "version": (1, 0, 0),
    "blender": (4, 1, 0),
    "location": "File > Export > Export Curve3D (.tres)",
    "description": "Export Bezier curves to Godot 4 Curve3D (.tres) format",
    "warning": "",
    "doc_url": "https://github.com/jbmedlin/blender-godot-curve3d-exporter",
    "category": "Import-Export",
}

def ReadSingleCurve(obj):
	if not obj.data.splines:
		return None

	spline = obj.data.splines[0]

	if spline.type != 'BEZIER':
		return None
	is_cyclic = spline.use_cyclic_u
	array_points = '"points": PackedVector3Array('
	tilt_points = '"tilts": PackedFloat32Array('
	count = 0
	for point in spline.bezier_points:
		if count != 0:
				array_points += ','
				tilt_points += ','
		count+=1
		array_points += ( 
				str(point.handle_left.x - point.co.x)+","+
				str(point.handle_left.z - point.co.z)+","+
				str(point.handle_left.y - point.co.y)+","+
				str(point.handle_right.x - point.co.x)+","+
				str(point.handle_right.z - point.co.z)+","+
				str(point.handle_right.y - point.co.y)+","+
				str(point.co.x)+","+
				str(point.co.z)+","+
				str(point.co.y)
				)
		tilt_points += str(point.tilt)
	array_points += '),'
	tilt_points += ')'
	final_output = ''
	final_output += '[gd_resource type="Curve3D" format=3]\n'
	final_output += '\n'
	final_output += '[resource]\n'
	if is_cyclic:
		final_output += 'closed = true\n'
	final_output += '_data = {\n'
	final_output += array_points + '\n'
	final_output += tilt_points + '\n'
	final_output += '}\n'
	final_output += "point_count = " + str(count)
	return final_output

def ReadCurveControls():
	return ReadSingleCurve(bpy.context.active_object)
#		for obj in bpy.context.selected_objects:
#				console_write ("# " + obj.name)
#				console_write(ReadSingleCurve(obj))

def write_curve(context, filepath):
	print("running write_some_data...")
	f = open(filepath, 'w', encoding='utf-8')
	f.write(ReadCurveControls())
	f.close()

	return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.


class ExportGodotCurve3D(Operator, ExportHelper):
	"""This appears in the tooltip of the operator and in the generated docs"""
	bl_idname = "export_godot.curve3d"	
	bl_label = "Export Curve3D"

	filename_ext = ".tres"

	filter_glob: StringProperty(
			default="*.tres",
			options={'HIDDEN'},
			maxlen=255,	
			)

	def invoke(self, context, event):
		obj = context.active_object
		if obj:
			directory = bpy.path.abspath("//")
			if self.filepath:
				directory = os.path.dirname(self.filepath)

			filename = bpy.path.ensure_ext(obj.name, self.filename_ext)
			self.filepath = os.path.join(directory, filename)
		return super().invoke(context, event)

	def execute(self, context):
		obj = context.active_object
		if not obj or obj.type != 'CURVE':
			self.report({'ERROR'}, "Please select a Curve object.")
			return {'CANCELLED'}
		result = ReadSingleCurve(obj)
		if result is None:
			self.report({'ERROR'}, "Only Bezier curves are supported (no NURBS or Poly)")
			return {'CANCELLED'}
		return write_curve(context, self.filepath)


def menu_func_export(self, context):
		self.layout.operator(ExportGodotCurve3D.bl_idname, text="Export Curve3D (.tres)")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
		bpy.utils.register_class(ExportGodotCurve3D)
		bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
		bpy.utils.unregister_class(ExportGodotCurve3D)
		bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
		register()

		bpy.ops.export_curve3d.some_data('INVOKE_DEFAULT')
