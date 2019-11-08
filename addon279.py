import bpy 
from bpy.types import Menu, Panel, UIList
from mathutils import Vector
bl_info = {
    "name": "ADA",
    "category": "Object",
}
class rotscale(bpy.types.Operator):
	bl_idname = 'rot.scale'
	bl_label = 'rotscale'
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		bpy.ops.object.select_all(action='DESELECT')
		objects = bpy.context.scene.objects
		for ob in objects:
		    ob.select = True
		    bpy.ops.object.transform_apply(location=False,
        		                            rotation=True, 
                		                    scale=True)
		    ob.select = False
		return {"FINISHED"}

class UvMeasure(bpy.types.Operator):
	bl_idname = 'uv.measure'
	bl_label = 'measureuv'
	bl_option = {"REGISTER", "UNDO"}

	def execute(self,context):
		bpy.ops.mesh.primitive_plane_add()
		x,y,z = bpy.context.active_object.dimensions
		x = 0.15
		y = 0.15
		bpy.context.active_object.dimensions = (x,y,z)
		bpy.ops.rot.scale()
		ob = bpy.context.active_object
		ob.select = True
		bpy.ops.object.mode_set(mode = 'EDIT')
		bpy.ops.uv.unwrap()
		bpy.ops.uv.muv_wsuv_measure()
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.delete()

		objects = bpy.context.scene.objects

		for ob in objects:
			bpy.ops.object.select_all(action='DESELECT')
			ob.select = True
			bpy.context.scene.objects.active = ob
			asd = ob.data
			i = 0
			for verts in range(len(asd.vertices)):
				asd.vertices[i].select = True
				i = i + 1
			bpy.ops.object.mode_set(mode = 'EDIT')
			bpy.ops.uv.muv_wsuv_apply()
			bpy.ops.object.mode_set(mode = 'OBJECT')
		
		return {'FINISHED'}

class select(bpy.types.Operator):
	bl_idname = 'select.face'
	bl_label = 'selectface'
	bl_options= {"REGISTER", "UNDO"}

	def execute(self,context):
		bpy.ops.object.mode_set(mode="EDIT")
		bpy.ops.mesh.select_all(action = 'DESELECT')
		bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
		return {"FINISHED"}

class origo(bpy.types.Operator):
	bl_idname = 'origo.set'
	bl_label = 'origo'
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		objects = bpy.context.selectable_objects

		for ob in objects:
		    bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY', center = 'BOUNDS')
		    ob.hide = True
		    #set all of the mesh's origin to their center of geometry and hide them


		for ob in objects:
		    ob.hide = False
		    ob.select = True
		    #unhide and select the meshes one-by-one

		    local_bbox_center = 0.125 * sum((Vector(b) for b in ob.bound_box), Vector())
		    distancex = local_bbox_center.x - ob.bound_box[3][0]
		    distancey = local_bbox_center.y - ob.bound_box[3][1]
		    distancez = local_bbox_center.x - ob.bound_box[3][2]
		    #calculate the center of the mesh's bounding box
		    #then calculate the distance between the desired corner of the bounding box and it's center

		    globalLocation = ob.location * ob.matrix_world
		    #we calculate the global location of the object (since it's origin is in the center of it's bounding box this would be the global center of the bounding box)

		    v = ob.bound_box
		    ob.location = (0,0,0)
		    bpy.context.scene.cursor_location = v[3]
		    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
		    v=None
		    #put the mesh to the (0,0,0) point in the scene, put a 3d cursor to the desired corner of the bounding box, then set it's origin to the 3d cursor

		    a = (distancex,distancey,distancez)
		    #make a vector out of the distances

		    ob.location = globalLocation - Vector(a)
		    #put the object back to it's original place
		    #we do it like this because and object's location is calculated based on it's origin. So firstly, we set all of the object's origin to it's bounding box's center, and we save it.
		    #After this we calculate the distance in x,y,z coordinates between the center and the desired corner. This will be the offset. Because if I change the object's origin. This new
		    #origin will be at exactly the place where the old origin was. So we have to subtract this offset from the object's old location. And voilá it's done. 


		    ob.hide = True
		    
		for ob in objects:
		    ob.hide = False

		return {"FINISHED"}

class new_panel(Panel):
	bl_space_type =  'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_label = 'upper title'
	bl_context = 'objectmode'
	bl_category = 'ADA'

	def draw(self, context):
		layout = self.layout
		layout.operator('rot.scale', text = 'Rotation and Scale')
		layout.operator('origo.set', text = 'Set Origin')
		layout.operator('select.face', text = 'Select faces')
		layout.operator('uv.measure', text = 'Measure UV')

def register():
	bpy.utils.register_class(new_panel)
	bpy.utils.register_class(rotscale)
	bpy.utils.register_class(origo)
	bpy.utils.register_class(select)
	bpy.utils.register_class(UvMeasure)


def unregister():
	bpy.utils.unregister_class(new_panel)
	bpy.utils.unregister_class(rotscale)
	bpy.utils.unregister_class(origo)
	bpy.utils.unregister_class(select)
	bpy.utils.unregister_class(UvMeasure)

if __name__ == "__main__":
    register()