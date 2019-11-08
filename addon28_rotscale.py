bl_info = {
    "name" : "RotScale",
    "author" : "Burján Balázs",
    "version" : (1, 0),
    "blender" : (2,80,0),
    "location": "View3D > Object",
    "description" : "Applies the rotation and scale of all objects",
    "warning" : "",
    "wiki_url": "",
    "category": "Object"
}

import bpy
from mathutils import Vector
from bpy.types import AddonPreferences, Operator, Panel, PropertyGroup

class OBJECT_OT_rotscale(Operator):
    bl_label = "RotScale"
    bl_idname = "object.rotscale"
    bl_description = "Applies the rotation and scale of all objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        objects = bpy.context.scene.objects
        for ob in objects:
            bpy.data.objects[ob.name].select_set(True)
            bpy.ops.object.transform_apply(location=False,
                                            rotation=True, 
                                            scale=True)
            bpy.data.objects[ob.name].select_set(False)
        i = 0
        for ob in selected:
            bpy.data.objects[ob.name].select_set(True)

        return {'FINISHED'}

def menu_func(self,context):
    self.layout.operator(OBJECT_OT_rotscale.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_rotscale)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rotscale)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()