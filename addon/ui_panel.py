import bpy


class PROCEDURALWHEEL_PT_main(bpy.types.Panel):
    bl_label = "Procedural Wheel"
    bl_idname = "PROCEDURALWHEEL_PT_main"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Procedural"   # ← tab name

    def draw(self, context):
        layout = self.layout

        layout.label(text="Wheel Tools")
        layout.operator("procedural_wheel.generate", icon="MESH_CYLINDER")


def register():
    bpy.utils.register_class(PROCEDURALWHEEL_PT_main)


def unregister():
    bpy.utils.unregister_class(PROCEDURALWHEEL_PT_main)
