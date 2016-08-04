bl_info = {
    "name": "Setup Jetpack Data",
    "category": "All",
}

import bpy


class SetupJetpackData(bpy.types.Operator):
    """Setup Jetpack Data"""
    bl_idname = "jetpack.setup_jetpack_data"
    bl_label = "Setup Jetpack Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
    	renderableTypesEnum = [
    	("UNDEFINED", "Undefined", "", 0),
    	("REGULAR", "Regular", "", 1),
    	("REFLECTIVE_SURFACE", "Reflective Surface", "", 2)
    	]

    	bpy.types.Object.renderableType = bpy.props.EnumProperty(items=renderableTypesEnum, name="Renderable Type")
    	for ob in bpy.data.objects:
    		ob.rotation_mode = 'AXIS_ANGLE'
    		if ob.renderableType == 'UNDEFINED':
    			ob.renderableType = 'REGULAR'

    	bpy.types.Material.specular_power = bpy.props.FloatProperty(name="Specular Power")
    	bpy.types.Material.specular_sharpness = bpy.props.FloatProperty(name="Specular Sharpness")
    	bpy.types.Material.fresnel_a = bpy.props.FloatProperty(name="Fresnel A")
    	bpy.types.Material.fresnel_b = bpy.props.FloatProperty(name="Fresnel B")
    	for material in bpy.data.materials:
    		if material.specular_power == 0.0:
    			material.specular_power = -1.0
    		if material.specular_sharpness == 0.0:
    			material.specular_sharpness = -1.0
    		if material.fresnel_a == 0.0:
    			material.fresnel_a = -1.0
    		if material.fresnel_b == 0.0:
    			material.fresnel_b = -1.0
    	return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SetupJetpackData.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(SetupJetpackData)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new(SetupJetpackData.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(SetupJetpackData)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()