"""100｜同じUVでも、画像の画素数が少ないと板目が塊になって見える。"""

from pathlib import Path
import sys

import bpy

source_path = globals().get("__file__")
if not source_path:
    lesson_text = getattr(bpy.context.space_data, "text", None)
    if not lesson_text or not lesson_text.filepath:
        raise RuntimeError("lesson.pyを保存してから実行してください")
    source_path = bpy.path.abspath(lesson_text.filepath)
LESSON_PATH = Path(source_path).resolve()
ROOT = LESSON_PATH.parents[2]
support_path = LESSON_PATH.parents[1] / "_support"
if str(support_path) not in sys.path:
    sys.path.insert(0, str(support_path))

import modifier_tools as tools

# 左の板目画像の一辺。右は細かい画素のまま比べる。
LOW_SIZE = 8
HIGH_SIZE = 64
BLEND_PATH = ROOT / "output" / "100_texture_resolution.blend"


def write_box_uv(source_mesh: bpy.types.Mesh) -> None:
    """面の法線を見て、縦横の座標を0から1のUVへ置く。画像の解像度とは別の情報。"""
    uv_layer = source_mesh.uv_layers.new(name="UVMap")
    for polygon in source_mesh.polygons:
        normal = polygon.normal
        if abs(normal.z) >= 0.5:
            axis_u, axis_v = 0, 1
        elif abs(normal.x) >= 0.5:
            axis_u, axis_v = 1, 2
        else:
            axis_u, axis_v = 0, 2
        for loop_index in polygon.loop_indices:
            vertex = source_mesh.vertices[source_mesh.loops[loop_index].vertex_index]
            uv_layer.data[loop_index].uv = (
                vertex.co[axis_u] * 0.5 + 0.5,
                vertex.co[axis_v] * 0.5 + 0.5,
            )


def striped_image(image_name: str, size: int) -> bpy.types.Image:
    """同じ4本の板目を、指定した画素数で塗る。少ない画素ほど境界が階段になる。"""
    image = bpy.data.images.new(image_name, size, size)
    pixels = [0.0] * (size * size * 4)
    dark = (0.40, 0.24, 0.10, 1.0)
    light = (0.72, 0.52, 0.28, 1.0)
    for y in range(size):
        band = (y * 4) // size
        color = dark if band % 2 == 0 else light
        for x in range(size):
            start = (y * size + x) * 4
            pixels[start:start + 4] = color
    image.pixels.foreach_set(pixels)
    image.pack()
    return image


def textured_material(material_name: str, image: bpy.types.Image) -> bpy.types.Material:
    material = bpy.data.materials.new(material_name)
    material.use_nodes = True
    node_tree = material.node_tree
    bsdf = node_tree.nodes["Principled BSDF"]
    image_node = node_tree.nodes.new("ShaderNodeTexImage")
    image_node.image = image
    node_tree.links.new(image_node.outputs["Color"], bsdf.inputs["Base Color"])
    return material


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("TextureResolution")
    coarse_object = tools.cube_object("Crate.Coarse", quality_collection, location=(-1.6, 0.0, 0.0))
    fine_object = tools.cube_object("Crate.Fine", quality_collection, location=(1.6, 0.0, 0.0))
    write_box_uv(coarse_object.data)
    write_box_uv(fine_object.data)
    coarse_image = striped_image("Texture.Coarse", LOW_SIZE)
    fine_image = striped_image("Texture.Fine", HIGH_SIZE)
    coarse_object.data.materials.append(textured_material("Material.Coarse", coarse_image))
    fine_object.data.materials.append(textured_material("Material.Fine", fine_image))

    print("=== 100 texture resolution ===")
    print(
        f"coarse image={coarse_image.size[0]} fine image={fine_image.size[0]} "
        f"verts={len(coarse_object.data.vertices)}/{len(fine_object.data.vertices)}"
    )

    if coarse_image.size[0] != LOW_SIZE or fine_image.size[0] != HIGH_SIZE:
        raise RuntimeError("画像の画素数が指定と違う")
    if coarse_image.size[0] >= fine_image.size[0]:
        raise RuntimeError("粗い画像の方が画素が多い")
    if len(coarse_object.data.vertices) != len(fine_object.data.vertices):
        raise RuntimeError("画素だけを変える比較なのに、頂点数まで違っている")

    tools.save_blend(BLEND_PATH, coarse_object)


if __name__ == "__main__":
    main()
