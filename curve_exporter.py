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
    "version": (1, 3, 1),
    "blender": (4, 1, 0),
    "location": "File > Export > Export Curve3D (.tres)",
    "description": "Export Bezier curves to Godot 4 Curve3D (.tres) format",
    "warning": "",
    "doc_url": "https://github.com/jbmedlin/blender-godot-curve3d-exporter",
    "category": "Import-Export",
}

def ReadSingleCurve(obj, apply_transform=False, apply_modifiers=False):
	if not obj.data.splines:
		return None

	if apply_modifiers:
		temp_obj = obj.copy()
		temp_obj.data = obj.data.copy()
		bpy.context.collection.objects.link(temp_obj)

		for modifier in list(temp_obj.modifiers):
			try:
				with bpy.context.temp_override(object=temp_obj):
					bpy.ops.object.modifier_apply(modifier=modifier.name)
			except Exception as e:
				print(f"Warning: Could not apply modifier '{modifier.name}' on '{temp_obj.name}': {e}")

		spline = temp_obj.data.splines[0]
		temp_obj_for_cleanup = temp_obj
	else:
		spline = obj.data.splines[0]
		temp_obj_for_cleanup = None

	if spline.type != 'BEZIER':
		if temp_obj_for_cleanup:
			bpy.data.objects.remove(temp_obj_for_cleanup, do_unlink=True)
		return None
	is_cyclic = spline.use_cyclic_u

	if apply_transform:
		curve_data = spline.id_data.copy()

		baked_spline = curve_data.splines[0]

		mat = obj.matrix_world
		for p in baked_spline.bezier_points:
			p.co = mat @ p.co
			p.handle_left = mat @ p.handle_left
			p.handle_right = mat @ p.handle_right

		use_spline = baked_spline
	else:
		use_spline = spline

	array_points = '"points": PackedVector3Array('
	tilt_points = '"tilts": PackedFloat32Array('
	count = 0

	for point in use_spline.bezier_points:
		if count != 0:
				array_points += ','
				tilt_points += ','
		count+=1
		array_points += ( 
				str(point.handle_left.x - point.co.x)+","+
				str(point.handle_left.z - point.co.z)+","+
				str(-(point.handle_left.y - point.co.y))+","+
				str(point.handle_right.x - point.co.x)+","+
				str(point.handle_right.z - point.co.z)+","+
				str(-(point.handle_right.y - point.co.y))+","+
				str(point.co.x)+","+
				str(point.co.z)+","+
				str(-point.co.y)
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

	if temp_obj_for_cleanup:
		bpy.data.objects.remove(temp_obj_for_cleanup, do_unlink=True)

	return final_output

def ReadCurveControls():
	return ReadSingleCurve(bpy.context.active_object)
#		for obj in bpy.context.selected_objects:
#				console_write ("# " + obj.name)
#				console_write(ReadSingleCurve(obj))

def write_curve(context, filepath, apply_transform=False, apply_modifiers=False, obj=None):
	print(f"writing curve to: {filepath}")
	if obj is None:
		obj = bpy.context.active_object

	f = open(filepath, 'w', encoding='utf-8')
	f.write(ReadSingleCurve(obj, apply_transform, apply_modifiers))
	f.close()

	return {'FINISHED'}


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

	apply_transform: BoolProperty(
        name="Apply Object Transform",
        description="Bake location, rotation, and scale into the exported curve data",
        default=True,
    )

	apply_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply all modifiers to the curve before exporting (non-destructive)",
        default=False,
    )

	batch_export: BoolProperty(
		name = "Export All Selected Curves",		
		description = "When enabled, exports every selected Curve object as its own .tres file. (named after the object)",
		default=False,
	)

	directory: StringProperty(
		name = "Export Folder",
		subtype='DIR_PATH',
		default="",
	)

	def invoke(self, context, event):
		obj = context.active_object
		if self.batch_export:
			self.filename_ext = ""
			if not self.directory:
				self.directory = bpy.path.abspath("//")
			return super.invoke(context,event)
		else:
			if obj:
				directory = bpy.path.abspath("//")
				if self.filepath:
					directory = os.path.dirname(self.filepath)

				filename = bpy.path.ensure_ext(obj.name, self.filename_ext)
				self.filepath = os.path.join(directory, filename)
			return super().invoke(context, event)

	def execute(self, context):
		obj = context.active_object
		if self.batch_export:
			exported_count = 0
			folder = bpy.path.abspath(self.directory)

			for obj in context.selected_objects:
				if obj.type != 'CURVE':
					continue

				result = ReadSingleCurve(obj, self.apply_transform, self.apply_modifiers)
				if result is None:
					self.report({'WARNING'}, f"Skipped {obj.name} (not a Bezier curve)")
					continue

				filepath = os.path.join(folder, bpy.path.ensure_ext(obj.name, self.filename_ext))
				write_curve(context, filepath, self.apply_transform, self.apply_modifiers, obj)
				exported_count += 1

			if exported_count > 0:
				self.report({'INFO'},f"Exported {exported_count} curve(s) to {folder}")
				return ({'FINISHED'})
			else:
				self.report({'WARNING'}, "No valid Curve objects selected")
				return {'CANCELLED'}
		else:
			if not obj or obj.type != 'CURVE':
				self.report({'ERROR'}, "Please select a Curve object.")
				return {'CANCELLED'}
			result = ReadSingleCurve(obj)
			if result is None:
				self.report({'ERROR'}, "Only Bezier curves are supported (no NURBS or Poly)")
				return {'CANCELLED'}
			return write_curve(context, self.filepath, self.apply_transform, self.apply_modifiers)


def menu_func_export(self, context):
		self.layout.operator(ExportGodotCurve3D.bl_idname, text="Export Curve3D (.tres)")

def register():
		bpy.utils.register_class(ExportGodotCurve3D)
		bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
		bpy.utils.unregister_class(ExportGodotCurve3D)
		bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
		register()

		bpy.ops.export_curve3d.some_data('INVOKE_DEFAULT')
