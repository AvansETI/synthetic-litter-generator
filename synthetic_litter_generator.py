import math

bl_info = {
    "name": "Synthetic Litter Data Generator",
    "author": "Bjorn Jaeken",
    "version": (0, 1),
    "blender": (4, 4, 3),
    "location": "View3D > Sidebar > LitterGen",
    "description": "Generate synthetic litter data by importing a litter object",
    "category": "3D View",
}

import os
import random
import bpy

class LitterGeneratorProperties(bpy.types.PropertyGroup):
    image_count: bpy.props.IntProperty(
        name="Amount of Images",
        default=1, min=1, max=100,
        soft_min=1, soft_max=100,
        update=lambda self, context: None
    )

class EnvironmentResetter(bpy.types.Operator):
    bl_idname = "littergen.reset_environment"
    bl_label = "Reset the environment"
    bl_description = "Resets the environment to camera and light elements"

    def execute(self, context):
        camera = context.scene.camera
        for obj in list(bpy.data.objects):
            if obj == camera:
                continue
            bpy.data.objects.remove(obj, do_unlink=True)

        light_data = bpy.data.lights.new(name="Sun", type='SUN')
        light_obj = bpy.data.objects.new(name="Sun", object_data=light_data)
        context.collection.objects.link(light_obj)

        light_obj.location = (0, 3, 10)
        camera.location = (7, -7, 5)

        self.report({'INFO'}, "Environment reset: all objects except camera removed, and sun light added")
        return {'FINISHED'}

class LitterObjectImporter(bpy.types.Operator):
    bl_idname = "littergen.import_object"
    bl_label = "Import GLB Object"
    bl_description = "Import a 3D model in GLB format (with textures)"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        if not self.filepath.lower().endswith('.glb'):
            self.report({'ERROR'}, "Only .glb files are supported")
            return {'CANCELLED'}

        bpy.ops.import_scene.gltf(
            filepath=self.filepath,
            filter_glob="*.glb;*.gltf",
            import_pack_images=True
        )

        imported_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects else None

        if imported_obj:
            imported_obj.name = "litter-object"
            self.report({'INFO'}, "GLB file imported and renamed to 'litter-object'")

            litter_obj = bpy.data.objects.get("litter-object")
            litter_obj.location = (0, 0, 0.250)

            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "GLB imported but no object was selected")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class LitterCanvastImporter(bpy.types.Operator):
    bl_idname = "littergen.import_canvas_object"
    bl_label = "Import GLB Object"
    bl_description = "Import a 3D canvas in GLB format (with textures)"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        if not self.filepath.lower().endswith('.glb'):
            self.report({'ERROR'}, "Only .glb files are supported")
            return {'CANCELLED'}

        bpy.ops.import_scene.gltf(
            filepath=self.filepath,
            filter_glob="*.glb;*.gltf",
            import_pack_images=True
        )

        imported_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects else None

        if imported_obj:
            imported_obj.name = "canvas-object"
            self.report({'INFO'}, "GLB file imported and renamed to 'canvas-object'")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "GLB imported but no canvas object was selected")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class SyntheticLitterPanel(bpy.types.Panel):
    bl_label = "Synthetic Litter Data Generator"
    bl_idname = "SyntheticLitterPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LitterGen'

    def draw(self, context):
        layout = self.layout
        props = context.scene.litter_generator_props

        layout.operator("littergen.reset_environment", text="Reset environment")
        layout.separator()
        layout.operator("littergen.import_canvas_object", text="Import Canvas Object File")
        layout.separator()
        layout.operator("littergen.import_object", text="Import Litter Object File")
        layout.separator()
        layout.label(text="Amount of images")
        layout.prop(props, "image_count")
        layout.separator()
        layout.operator("littergen.capture_image", text="Create Images")

def randomize_camera():
    camera = bpy.context.scene.camera
    target = bpy.data.objects.get("litter-object")

    if not camera or not target:
        return

    radius = random.uniform(5, 30)
    azimuth = random.uniform(0, 2 * math.pi)
    elevation = random.uniform(math.radians(15), math.radians(45))

    x = radius * math.cos(azimuth) * math.cos(elevation)
    y = radius * math.sin(azimuth) * math.cos(elevation)
    z = radius * math.sin(elevation)

    camera.location = (x, y, z)

    direction = target.location - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

def randomize_litter_position():
    bpy.data.objects["litter-object"].location = (
        random.randint(0, 3),  # X
        random.randint(0, 3),  # Y
        0.250
    )
    bpy.data.objects["litter-object"].rotation_quaternion[3] = random.randint(0, 3)

def randomize_light():
    sun = bpy.data.objects.get("Sun")
    if not sun or sun.type != 'LIGHT' or sun.data.type != 'SUN':
        return

    sun.data.energy = random.uniform(1.0, 10.0)
    sun.data.angle = random.uniform(0.1, math.radians(45))
    sun.location = (
        random.uniform(-10, 10),
        random.uniform(-10, 10),
        random.uniform(10, 50)
    )

def reset_litter_position():
    bpy.data.objects["litter-object"].location = (0, 0, 0.250)
    bpy.data.objects["litter-object"].rotation_quaternion[3] = 0

def reset_light():
    sun = bpy.data.objects.get("Sun")
    if not sun or sun.type != 'LIGHT' or sun.data.type != 'SUN':
        return

    sun.location = (0, 3, 10)
    sun.data.energy = 5.0
    sun.data.angle = math.radians(15)

def reset_camera(camera):
    camera.location = (7, -7, 5)
    camera.rotation_euler = (math.radians(60), 0, 0)

class SyntheticLitterDataGenerator(bpy.types.Operator):
    bl_idname = "littergen.capture_image"
    bl_label = "Capture Image"
    bl_description = "Render current camera view and save to Desktop"

    def execute(self, context):
        scene = context.scene
        camera = scene.camera

        if camera is None:
            self.report({'ERROR'}, "No camera found in the scene")
            return {'CANCELLED'}

        props = context.scene.litter_generator_props
        image_count = props.image_count

        for i in range(image_count):
            randomize_litter_position()
            randomize_camera()
            randomize_light()

            self.render_file(i, scene)

            reset_light()
            reset_litter_position()
            reset_camera(camera)

        return {'FINISHED'}

    def render_file(self, i, scene):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop/litter_images")
        output_path = os.path.join(desktop, f"{i + 1}_littergen_render.png")
        prev_filepath = scene.render.filepath
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = output_path
        bpy.ops.render.render(write_still=True)
        scene.render.filepath = prev_filepath
        self.report({'INFO'}, f"Image saved to {output_path}")

classes = (
    LitterGeneratorProperties,
    EnvironmentResetter,
    LitterCanvastImporter,
    LitterObjectImporter,
    SyntheticLitterPanel,
    SyntheticLitterDataGenerator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.litter_generator_props = bpy.props.PointerProperty(type=LitterGeneratorProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.litter_generator_props

if __name__ == "__main__":
    register()
