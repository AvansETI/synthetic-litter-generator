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

# --- Settings ---
# CAMERA_RADIUS = 5.0
# LIGHT_RADIUS = 5.0

# TODO 1. Git toevoegen
# TODO 2. Licht randomisen
# TODO 3. Camera randomisen
# TODO 4. Canvas integreren
# TODO 5. Canvas randomisen

class LitterGeneratorProperties(bpy.types.PropertyGroup):
    # camera_azimuth: bpy.props.FloatProperty(
    #     name="Camera Azimuth",
    #     default=0.0, min=0.0, max=360.0,
    #     update=lambda self, context: update_camera(context)
    # )
    # camera_elevation: bpy.props.FloatProperty(
    #     name="Camera Elevation",
    #     default=45.0, min=0.0, max=90.0,
    #     update=lambda self, context: update_camera(context)
    # )
    # light_azimuth: bpy.props.FloatProperty(
    #     name="Light Azimuth",
    #     default=0.0, min=0.0, max=360.0,
    #     update=lambda self, context: update_light(context)
    # )
    # light_elevation: bpy.props.FloatProperty(
    #     name="Light Elevation",
    #     default=45.0, min=0.0, max=90.0,
    #     update=lambda self, context: update_light(context)
    # )
    image_count: bpy.props.IntProperty(
        name="Amount of Images",
        default=1, min=1, max=100,
        soft_min=1, soft_max=100,
        update=lambda self, context: None
    )

# def update_camera(context):
#     props = context.scene.litter_generator_props
#     az = math.radians(props.camera_azimuth)
#     el = math.radians(props.camera_elevation)
#     x = CAMERA_RADIUS * math.cos(el) * math.cos(az)
#     y = CAMERA_RADIUS * math.cos(el) * math.sin(az)
#     z = CAMERA_RADIUS * math.sin(el)
#     cam = get_or_create_camera()
#     cam.location = (x, y, z)
#     direction = (-x, -y, -z)
#     cam.rotation_euler = direction_to_euler(direction)
#
# def update_light(context):
#     props = context.scene.litter_generator_props
#     az = math.radians(props.light_azimuth)
#     el = math.radians(props.light_elevation)
#     x = LIGHT_RADIUS * math.cos(el) * math.cos(az)
#     y = LIGHT_RADIUS * math.cos(el) * math.sin(az)
#     z = LIGHT_RADIUS * math.sin(el)
#     light = get_or_create_light()
#     light.location = (x, y, z)
#     direction = (-x, -y, -z)
#     light.rotation_euler = direction_to_euler(direction)
#
# def get_or_create_camera():
#     cam = bpy.context.scene.camera
#     if cam is None or cam.type != 'CAMERA':
#         cam_data = bpy.data.cameras.new(name="LitterGenCamera")
#         cam = bpy.data.objects.new("LitterGenCamera", cam_data)
#         bpy.context.collection.objects.link(cam)
#         bpy.context.scene.camera = cam
#     return cam
#
# def get_or_create_light():
#     light_obj = bpy.data.objects.get("LitterGenLight")
#     if light_obj is None or light_obj.type != 'LIGHT':
#         light_data = bpy.data.lights.new(name="LitterGenLight", type='SUN')
#         light_obj = bpy.data.objects.new("LitterGenLight", light_data)
#         bpy.context.collection.objects.link(light_obj)
#     return light_obj

# def direction_to_euler(direction):
#     dx, dy, dz = direction
#     rot_y = math.atan2(dx, dz)
#     rot_x = math.atan2(dy, math.sqrt(dx**2 + dz**2))
#     return (rot_x, 0.0, -rot_y)

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
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "GLB imported but no object was selected")
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

        layout.operator("littergen.import_object", text="Import Litter Object File")
        layout.separator()
        layout.label(text="Amount of images")
        layout.prop(props, "image_count")
        layout.separator()
        layout.operator("littergen.capture_image", text="Create Images")


def randomize_litter_position():
    bpy.data.objects["litter-object"].location = (
        random.randint(0, 3),  # X
        random.randint(0, 3),  # Y
        0
    )
    bpy.data.objects["litter-object"].rotation_quaternion[3] = random.randint(0, 3)


def reset_litter_position():
    bpy.data.objects["litter-object"].location = (0, 0, 0)
    bpy.data.objects["litter-object"].rotation_quaternion[3] = 0


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

            self.render_file(i, scene)

            reset_litter_position()

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
