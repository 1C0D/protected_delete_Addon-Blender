import bpy
from bpy.props import BoolProperty

bl_info = {
    "name": "protected_delete_addon",
    "author": "1C0D",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "protect from deleting with a pp in properties panel >object>visibility",
    "category": "Object",
}
    
bpy.types.Object.protected_delete = BoolProperty(
name = 'protected_delete', 
default =False,
description='to apply to several obj from active-> right clic on checkbox > copy to selected',
)

class Delete_Override(bpy.types.Operator):
    """delete unprotected objects"""
    bl_idname = "object.delete_mod"
    bl_label = "Object Delete dd Operator"
    bl_options = {'REGISTER', 'UNDO'} 
    
    @classmethod
    def poll(cls, context):
        return context.mode=='OBJECT'

    def execute(self, context):
    
    
        override = bpy.context.copy()  
        selected=bpy.context.selected_objects
        override['selected_objects'] = [obj for obj in selected if not obj.protected_delete]
        bpy.ops.object.delete(override)
        
        return {'FINISHED'}
    
class Delete_Override_Property_Select_Toggle(bpy.types.Operator):
        bl_idname = "object.del_override_toggle"
        bl_label = "Object Delete Operator"
        bl_options = {'REGISTER', 'UNDO'} 
        bl_description= "to select all propected objects" 
        
        def execute(self, context):        
            
            bpy.ops.object.select_all(action='DESELECT')    
            for obj in bpy.context.scene.objects:
                if obj.protected_delete:
                        obj.select_set(True)
                        context.view_layer.objects.active=obj

            return {'FINISHED'}    
            
def draw_delete_override(self, context):
    layout = self.layout
    layout.use_property_split = True
    flow = layout.grid_flow(row_major=False, columns=0, even_columns=True, even_rows=False, align=False)

    obj = context.object
    col = flow.column()

    col.prop(obj, "protected_delete", text="protected_delete")
    row=layout.row() 
    row.label(text='select all protected_delete')
    row.operator("object.del_override_toggle", text="",icon='ARROW_LEFTRIGHT')

addon_keymaps = []
def register():
    bpy.utils.register_class(Delete_Override_Property_Select_Toggle)
    bpy.types.OBJECT_PT_visibility.append(draw_delete_override) 
    bpy.utils.register_class(Delete_Override)
    
    wm = bpy.context.window_manager   
    
    km = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode')
    kmi = km.keymap_items.new('object.delete_mod', 'DEL', 'PRESS',ctrl=True)
    
    addon_keymaps.append((km, kmi))


def unregister():
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(Delete_Override_Property_Select_Toggle)
    bpy.utils.unregister_class(Delete_Override)
    bpy.types.OBJECT_PT_visibility.remove(draw_delete_override) 


if __name__ == "__main__":
    register()
