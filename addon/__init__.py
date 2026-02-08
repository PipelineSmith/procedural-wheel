from . import package
from . import dev_reload
from . import ui_panel
from . import operators

bl_info = {
    "name": "Procedural Wheel",
    "version": package.VERSION,
    "blender": (4, 3, 0),
    "category": "Object",
}


def register():
    operators.register()
    ui_panel.register()
    dev_reload.register()

    print("[Procedural Wheel] registered")


def unregister():
    dev_reload.unregister()
    ui_panel.unregister()
    operators.unregister()

    print("[Procedural Wheel] unregistered")
