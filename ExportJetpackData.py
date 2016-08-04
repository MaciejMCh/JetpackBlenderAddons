bl_info = {
    "name": "Export Jetpack Data",
    "category": "All",
}

import bpy
import sys
import json
import os


class ExportJetpackData(bpy.types.Operator):
    """Export Jetpack Data"""
    bl_idname = "jetpack.export_jetpack_data"
    bl_label = "Export Jetpack Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        storagePath = os.path.dirname(bpy.data.filepath) + "/3dAssets/"
        # export scenes
        scenesJsonArray = []
        for scene in bpy.data.scenes:
            sceneJsonObject = {}
            sceneJsonObject['name'] = scene.name
            scenesJsonArray.append(sceneJsonObject)
            objectsJsonArray = []
            sceneJsonObject['renderables'] = objectsJsonArray
            for ob in scene.objects:
                if ob.hide:
                    continue
                if ob.type != 'MESH':
                    continue
                objectJsonObject = {}
                objectJsonObject['type'] = 'regular'
                objectJsonObject['name'] = ob.name
                objectJsonObject['mesh'] = ob.data.name
                objectJsonObject['material'] = ob.active_material.name
                objectJsonObject['transformation'] = {}
                objectJsonObject['transformation']['position'] = [ob.location.x, ob.location.y, ob.location.z]
                objectJsonObject['transformation']['rotation'] = {}
                objectJsonObject['transformation']['rotation']['angle'] = ob.rotation_axis_angle[0]
                objectJsonObject['transformation']['rotation']['x'] = ob.rotation_axis_angle[1]
                objectJsonObject['transformation']['rotation']['y'] = ob.rotation_axis_angle[2]
                objectJsonObject['transformation']['rotation']['z'] = ob.rotation_axis_angle[3]
                objectsJsonArray.append(objectJsonObject)
            with open(storagePath + 'scenes/' + scene.name + '.scene', 'w') as f:
                f.write(json.dumps(sceneJsonObject))
                f.closed

        for mesh in bpy.data.meshes:
            zeroObjectName = mesh.name + "_zero"
            zeroObject = bpy.data.objects.new(zeroObjectName, mesh)
            bpy.context.screen.scene.objects.link(zeroObject)
            bpy.ops.object.select_all(action='DESELECT')
            zeroObject.select = True
            bpy.ops.object.select_pattern(pattern=zeroObjectName, extend=False)
            bpy.ops.export_scene.obj(filepath=storagePath+'meshes/'+mesh.name+'.obj', use_selection=True, axis_forward='Y', axis_up='Z', use_triangles=True, use_uvs=True, use_materials=False)

        materialProperties = ["specular_power", "specular_sharpness", "fresnel_a", "fresnel_b"]
        for material in bpy.data.materials:
            os.system('mkdir ' + storagePath + 'materials/' + material.name)
            materialPropertiesJson = {}
            for key in material.keys():
                for materialProperty in materialProperties:
                    if materialProperty == key:
                        materialPropertiesJson[key] = material[key]
            with open(storagePath + 'materials/' + material.name + '/properties.material', 'w') as f:
                f.write(json.dumps(materialPropertiesJson))
                f.closed
            for textureSlot in material.texture_slots:
                if textureSlot:
                    texture = bpy.data.textures[textureSlot.name]
                    image = bpy.data.images[bpy.data.textures[textureSlot.name].image.name]
                    imageName = 'undefined'
                    if textureSlot == material.texture_slots[0]:
                        imageName = 'diffuse'
                    if textureSlot == material.texture_slots[1]:
                        imageName = 'normal'
                    if textureSlot == material.texture_slots[2]:
                        imageName = 'specular'
                    imageFilePath = storagePath + 'materials/' + material.name + '/' + imageName + '.png'
                    image.save_render(filepath=imageFilePath)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(ExportJetpackData.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ExportJetpackData)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new(ExportJetpackData.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(ExportJetpackData)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()