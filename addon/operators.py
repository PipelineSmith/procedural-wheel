import bpy
import math


def _ensure_tire_material():
    mat = bpy.data.materials.get("_TIRE_M_")
    if mat is None:
        mat = bpy.data.materials.new("_TIRE_M_")
    if not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    principled = nodes.get("Principled BSDF")
    output = nodes.get("Material Output")

    if principled is None:
        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
    if output is None:
        output = nodes.new(type="ShaderNodeOutputMaterial")

    if not any(link.from_node == principled and link.to_node == output for link in links):
        links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    principled.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    principled.inputs["Roughness"].default_value = 0.1

    return mat


class PROCEDURALWHEEL_OT_generate(bpy.types.Operator):
    bl_idname = "procedural_wheel.generate"
    bl_label = "Generate Tire (Revolve Profile)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # ---- parameters you can later expose in UI ----
        major_radius = 0.6   # distance from axis to tire center (meters)
        tire_radius  = 0.18  # tire "thickness" radius (meters)
        steps_view   = 32
        steps_render = 32
        bulge        = tire_radius * 0.35

        # Create a 2-point Bezier curve (half profile), then revolve around Y
        curve_data = bpy.data.curves.new("TireProfileCurve", type="CURVE")
        curve_data.dimensions = "3D"

        spline = curve_data.splines.new(type="BEZIER")
        spline.use_cyclic_u = False
        spline.bezier_points.add(1)

        top = spline.bezier_points[0]
        bot = spline.bezier_points[1]

        top.handle_left_type = "FREE"
        top.handle_right_type = "FREE"
        bot.handle_left_type = "FREE"
        bot.handle_right_type = "FREE"

        top.co = (major_radius, 0.0, tire_radius)
        bot.co = (major_radius, 0.0, -tire_radius)

        top.handle_left = top.co
        bot.handle_right = bot.co
        top.handle_right = (major_radius + bulge, 0.0, tire_radius * 0.5)
        bot.handle_left = (major_radius + bulge, 0.0, -tire_radius * 0.5)

        # Create object in scene
        obj = bpy.data.objects.new("Procedural_Tire", curve_data)
        context.collection.objects.link(obj)

        # Position it where your old cylinder was (cursor), keep your rotation if you like
        obj.location = context.scene.cursor.location

        # Add Screw modifier to revolve the profile 360 degrees
        mod = obj.modifiers.new(name="Revolve", type="SCREW")
        mod.axis = "Y"
        mod.angle = math.tau  # 2*pi
        mod.steps = steps_view
        mod.render_steps = steps_render
        mod.use_merge_vertices = True
        mod.merge_threshold = 0.0005
        mod.screw_offset = 0.0

        # Mirror, solidify, and edge split (manual stack)
        mirror = obj.modifiers.new(name="Mirror", type="MIRROR")
        mirror.use_axis[0] = False
        mirror.use_axis[1] = True
        mirror.use_axis[2] = False

        solidify = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
        solidify.thickness = 0.05

        obj.modifiers.new(name="EdgeSplit", type="EDGE_SPLIT")

        # Optional: add some smoothing on the screw surface
        mod.use_smooth_shade = True

        # Ensure tire material exists and assign it
        mat = _ensure_tire_material()
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(PROCEDURALWHEEL_OT_generate)


def unregister():
    bpy.utils.unregister_class(PROCEDURALWHEEL_OT_generate)
