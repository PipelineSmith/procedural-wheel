# addon/dev_reload.py
import bpy
import importlib
import sys

# This module name must match the folder name Blender imports:
# %APPDATA%\...\addons\procedural_wheel\__init__.py
ADDON_MODULE = "procedural_wheel"


def _reload_package(package_name: str):
    """Reload all modules under this add-on package."""
    names = [name for name in sys.modules.keys()
             if name == package_name or name.startswith(package_name + ".")]

    # Reload deeper modules first, then the package
    for name in sorted(names, key=len, reverse=True):
        importlib.reload(sys.modules[name])


class PROCEDURALWHEEL_OT_reload(bpy.types.Operator):
    bl_idname = "procedural_wheel.reload"
    bl_label = "Reload Procedural Wheel"
    bl_options = {"REGISTER"}

    def execute(self, context):
        # Disable (unregisters) if enabled
        try:
            bpy.ops.preferences.addon_disable(module=ADDON_MODULE)
        except Exception:
            pass

        # Reload python modules
        _reload_package(ADDON_MODULE)

        # Enable (registers) again
        try:
            bpy.ops.preferences.addon_enable(module=ADDON_MODULE)
        except Exception as e:
            self.report({"ERROR"}, f"Enable failed: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, "Procedural Wheel reloaded")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(PROCEDURALWHEEL_OT_reload)


def unregister():
    bpy.utils.unregister_class(PROCEDURALWHEEL_OT_reload)
