"""27｜人物のUVと質感。初期化して観察用ファイルを保存する教材。"""

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

CLOTH_ROUGHNESS = 0.88
lesson_scene, assets_collection = tools.start("CharacterUV")
atlas_material = tools.material("Character.Atlas", (0.5, 0.4, 0.3))
color_image = bpy.data.images.new("Atlas.Color", width=96, height=32)
roughness_image = bpy.data.images.new("Atlas.Roughness", width=96, height=32)
metallic_image = bpy.data.images.new("Atlas.Metallic", width=96, height=32)
for texture_image in (roughness_image, metallic_image):
    texture_image.colorspace_settings.name = "Non-Color"
colors = [(0.65, 0.38, 0.23), (0.05, 0.24, 0.38), (0.65, 0.45, 0.12)]
for texture_image, kind in [
    (color_image, "color"),
    (roughness_image, "roughness"),
    (metallic_image, "metallic"),
]:
    pixels = []
    for y in range(32):
        for x in range(96):
            region = x // 32
            values = (
                colors[region]
                if kind == "color"
                else (
                    ([0.55, CLOTH_ROUGHNESS, 0.25][region],) * 3
                    if kind == "roughness"
                    else ((1 if region == 2 else 0),) * 3
                )
            )
            pixels.extend((*values, 1))
    texture_image.pixels = pixels
    texture_image.pack()
    texture_node = atlas_material.node_tree.nodes.new("ShaderNodeTexImage")
    texture_node.image = texture_image
    input_name = {
        "color": "Base Color",
        "roughness": "Roughness",
        "metallic": "Metallic",
    }[kind]
    atlas_material.node_tree.links.new(
        texture_node.outputs["Color"],
        atlas_material.node_tree.nodes["Principled BSDF"].inputs[input_name],
    )
head_object = tools.sphere(
    "Character.SkinPart", (0.65, 0.6, 0.7), (0, 0, 2), assets_collection, atlas_material
)
shirt_object = tools.box(
    "Character.Shirt", (0.85, 0.5, 1), (0, 0, 1.15), assets_collection, atlas_material
)
buckle_object = tools.box(
    "Character.Buckle",
    (0.25, 0.09, 0.18),
    (0, -0.3, 0.9),
    assets_collection,
    atlas_material,
)
for region, asset_object in enumerate((head_object, shirt_object, buckle_object)):
    tools.uv_smart(asset_object)
    # 1枚のAtlasを共有し、部品のUVだけを対応する帯へ移動する。
    for uv_corner in asset_object.data.uv_layers.active.data:
        uv_corner.uv.x = (region + 0.05 + uv_corner.uv.x * 0.9) / 3
    print(
        asset_object.name,
        "UV band:",
        region,
        "material:",
        asset_object.data.materials[0].name,
    )
assert all(
    asset_object.data.materials[0] is atlas_material
    for asset_object in (head_object, shirt_object, buckle_object)
)
tools.studio(lesson_scene, span=4, target=(0, 0, 1.2))
tools.active(shirt_object)
tools.finish(lesson_scene, assets_collection, "27_character_uv")
