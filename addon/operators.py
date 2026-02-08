import bpy
import math


class PROCEDURALWHEEL_OT_generate(bpy.types.Operator):
    bl_idname = "procedural_wheel.generate"
    bl_label = "Generate Tire (Revolve Profile)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # ---- parameters you can later expose in UI ----
        major_radius = 0.6   # distance from axis to tire center (meters)
        tire_radius  = 0.18  # tire "thickness" radius (meters)
        steps_view   = 64
        steps_render = 128

        # Create a 2D curve (profile) in local XZ plane, then revolve around Y
        curve_data = bpy.data.curves.new("TireProfileCurve", type="CURVE")
        curve_data.dimensions = "2D"
        curve_data.fill_mode = "BOTH"  # gives the profile a filled face (helps make it solid-ish)

        spline = curve_data.splines.new(type="POLY")
        spline.use_cyclic_u = True

        # Simple rounded-ish tire profile as a loop.
        # Profile is offset by major_radius so it revolves around origin (axis at (0,0,0)).
        # Points are (x, y, z, w). Keep y = 0 because it's a 2D profile plane.
        pts = [
            (major_radius - 0.02, 0.0,  tire_radius * 0.85, 1.0),
            (major_radius + 0.06, 0.0,  tire_radius * 0.65, 1.0),
            (major_radius + 0.10, 0.0,  tire_radius * 0.20, 1.0),
            (major_radius + 0.10, 0.0, -tire_radius * 0.20, 1.0),
            (major_radius + 0.06, 0.0, -tire_radius * 0.65, 1.0),
            (major_radius - 0.02, 0.0, -tire_radius * 0.85, 1.0),
            (major_radius - 0.08, 0.0, -tire_radius * 0.35, 1.0),
            (major_radius - 0.08, 0.0,  tire_radius * 0.35, 1.0),
        ]

        spline.points.add(len(pts) - 1)
        for i, p in enumerate(pts):
            spline.points[i].co = p

        # Create object in scene
        obj = bpy.data.objects.new("Procedural_Tire", curve_data)
        context.collection.objects.link(obj)

        # Position it where your old cylinder was (cursor), keep your rotation if you like
        obj.location = context.scene.cursor.location
        obj.rotation_euler = (0.0, 1.0, 0.0)  # keep your existing rotation setup

        # Add Screw modifier to revolve the profile 360 degrees
        mod = obj.modifiers.new(name="Revolve", type="SCREW")
        mod.axis = "Y"
        mod.angle = math.tau  # 2*pi
        mod.steps = steps_view
        mod.render_steps = steps_render
        mod.use_merge_vertices = True
        mod.merge_threshold = 0.0005

        # Optional: add some smoothing
        mod.use_smooth_shade = True

        return {"FINISHED"}


def register():
    bpy.utils.register_class(PROCEDURALWHEEL_OT_generate)


def unregister():
    bpy.utils.unregister_class(PROCEDURALWHEEL_OT_generate)
