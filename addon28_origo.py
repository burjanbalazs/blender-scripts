bl_info = {
    "name" : "Origo",
    "author" : "Burján Balázs",
    "version" : (1, 0),
    "blender" : (2,80,0),
    "location": "View3D > Object",
    "description" : "Sets the object's origin to the lower left back corner of the mesh",
    "warning" : "",
    "wiki_url": "",
    "category": "Object"
}

import bpy
from mathutils import Vector
from bpy.types import AddonPreferences, Operator, Panel, PropertyGroup

class OBJECT_OT_origo(Operator):
    bl_label = "Origo"
    bl_idname = "object.origo"
    bl_description = "Sets the object's origin to the lower left back corner of the mesh"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.scene.objects
        for ob in objects:
            bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY', center = 'BOUNDS')
            bpy.data.objects[ob.name].hide_viewport = True
        for ob in objects:
            bpy.data.objects[ob.name].hide_viewport = False
            bpy.data.objects[ob.name].select_set(True)
            local_bbox_center = 0.125 * sum((Vector(b) for b in ob.bound_box), Vector())
            distancex = local_bbox_center.x - ob.bound_box[3][0]
            distancey = local_bbox_center.y - ob.bound_box[3][1]
            distancez = local_bbox_center.z - ob.bound_box[3][2]
            globalLocation = ob.location @ ob.matrix_world
            v = ob.bound_box
            ob.location = (0,0,0)
            bpy.context.scene.cursor.location = v[3]
            bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
            v=None
            a = (distancex,distancey,distancez)
            ob.location = globalLocation - Vector(a)
            bpy.data.objects[ob.name].hide_viewport = True
        for ob in objects:
            bpy.data.objects[ob.name].hide_viewport = False

        return {'FINISHED'}

def menu_func(self,context):
    self.layout.operator(OBJECT_OT_origo.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_origo)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_origo)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()