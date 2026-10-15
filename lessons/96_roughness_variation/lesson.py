"""96｜1つの木箱の中でRoughnessを分ける。全面が同じ値だと、プラスチックのように均一に見える。"""

from pathlib import Path
import sys

import bmesh
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

# 縁の面だけ反射を鋭くする。胴体は広くぼかしたまま。
EDGE_ROUGHNESS = 0.15
BODY_ROUGHNESS = 0.75
BLEND_PATH = ROOT / "output" / "96_roughness_variation.blend"


def add_edge_strip(source_mesh: bpy.types.Mesh) -> None:
    """角に細い面を足す。この面へ、胴体と違うRoughnessを割り当てる。"""
    source_bmesh = bmesh.new()
    source_bmesh.from_mesh(source_mesh)
    bmesh.ops.bevel(
        source_bmesh,
        geom=list(source_bmesh.edges),
        offset=0.06,
        segments=1,
        affect="EDGES",
    )
    source_bmesh.to_mesh(source_mesh)
    source_bmesh.free()
    source_mesh.update()


def principled_material(material_name: str, roughness: float, color: tuple[float, float, float, float]):
    material = bpy.data.materials.new(material_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = 0.0
    return material


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("RoughnessVariation")
    crate_object = tools.cube_object("Crate.Worn", quality_collection)
    crate_mesh = crate_object.data
    add_edge_strip(crate_mesh)
    body_material = principled_material(
        "Material.Body",
        BODY_ROUGHNESS,
        (0.45, 0.28, 0.14, 1.0),
    )
    edge_material = principled_material(
        "Material.Edge",
        EDGE_ROUGHNESS,
        (0.55, 0.42, 0.24, 1.0),
    )
    # Slotの順番がFaceのmaterial_index。0が胴体、1が縁。
    crate_mesh.materials.append(body_material)
    crate_mesh.materials.append(edge_material)
    for polygon in crate_mesh.polygons:
        polygon.material_index = 0 if polygon.area > 1.0 else 1

    body_faces = sum(polygon.material_index == 0 for polygon in crate_mesh.polygons)
    edge_faces = sum(polygon.material_index == 1 for polygon in crate_mesh.polygons)
    print("=== 96 roughness variation ===")
    print(
        f"body roughness={BODY_ROUGHNESS} faces={body_faces} "
        f"edge roughness={EDGE_ROUGHNESS} faces={edge_faces}"
    )

    if body_faces == 0 or edge_faces == 0:
        raise RuntimeError("胴体と縁の両方が同じ木箱に割り当てられていない")
    if abs(BODY_ROUGHNESS - EDGE_ROUGHNESS) < 0.2:
        raise RuntimeError("胴体と縁のRoughnessが分かれていない")

    tools.save_blend(BLEND_PATH, crate_object)


if __name__ == "__main__":
    main()
