"""14｜テクスチャとマテリアル。初期化して観察用ファイルを保存する教材。"""
from pathlib import Path
import sys
from math import sin, cos, pi, radians
import bmesh
import bpy
from mathutils import Vector

# --pythonと、保存済みText EditorのRun Scriptの両方で教材の場所を解決する。
source_path = globals().get("__file__")
if not source_path:
    lesson_text = getattr(bpy.context.space_data, "text", None)
    if not lesson_text or not lesson_text.filepath:
        raise RuntimeError("lesson.pyを保存してから実行してください")
    source_path = bpy.path.abspath(lesson_text.filepath)
support_path = Path(source_path).resolve().parents[1] / "_support"
if str(support_path) not in sys.path:
    sys.path.insert(0, str(support_path))
import scene_tools as tools

ROUGHNESS_HIGH = 0.9
lesson_scene, assets_collection = tools.start("ImageMaterial")
wood_material = tools.material("Surface.PaintedWood",(0.4,0.2,0.1))
color_image = bpy.data.images.new("Texture.Color",width=64,height=64)
roughness_image = bpy.data.images.new("Texture.Roughness",width=64,height=64)
roughness_image.colorspace_settings.name = "Non-Color"
color_pixels, roughness_pixels = [], []
for y in range(64):
    for x in range(64):
        stripe = (x//8)%2
        color_pixels.extend((0.45+0.2*stripe,0.18+0.08*stripe,0.05,1))
        roughness = 0.12 if stripe else ROUGHNESS_HIGH
        roughness_pixels.extend((roughness,roughness,roughness,1))
for texture_image, pixels in [(color_image,color_pixels),(roughness_image,roughness_pixels)]:
    texture_image.pixels = pixels
    texture_image.pack()  # 外部画像への参照切れを避け、.blendだけで持ち運べるようにする。
color_node = wood_material.node_tree.nodes.new("ShaderNodeTexImage")
roughness_node = wood_material.node_tree.nodes.new("ShaderNodeTexImage")
color_node.image, roughness_node.image = color_image, roughness_image
principled_node = wood_material.node_tree.nodes["Principled BSDF"]
wood_material.node_tree.links.new(color_node.outputs["Color"],principled_node.inputs["Base Color"])
wood_material.node_tree.links.new(roughness_node.outputs["Color"],principled_node.inputs["Roughness"])
crate_object = tools.box("Crate.Textured",(1.5,1,1),(0,0,0.5),assets_collection,wood_material)
tools.uv_smart(crate_object)
assert roughness_image.colorspace_settings.name=="Non-Color"
assert color_image.packed_file and roughness_image.packed_file
print("color / roughness:",color_image.colorspace_settings.name,roughness_image.colorspace_settings.name)
tools.studio(lesson_scene,span=4)
tools.active(crate_object)
tools.finish(lesson_scene,assets_collection,"14_image_material")
