"""94｜Edge Creaseは頂点を増やさず、Subdivision後も角を元の位置へ留める。"""

from pathlib import Path
import sys

import bpy
from mathutils import Vector

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

# 1で角を留め、0でSubdivisionの丸みに任せる。0.5はその中間。
CREASE = 1.0
BLEND_PATH = ROOT / "output" / "94_edge_crease.blend"
CORNER = Vector((1.0, 1.0, 1.0))


def set_edge_crease(source_mesh: bpy.types.Mesh, crease: float) -> None:
    """辺のcrease_edge属性。頂点座標は動かさない。"""
    crease_attribute = source_mesh.attributes.new("crease_edge", "FLOAT", "EDGE")
    for item in crease_attribute.data:
        item.value = crease


def nearest_to_corner(positions) -> float:
    return min((position - CORNER).length for position in positions)


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("EdgeCrease")
    loose_object = tools.cube_object("Crate.Loose", quality_collection, location=(-1.6, 0.0, 0.0))
    creased_object = tools.cube_object("Crate.Creased", quality_collection, location=(1.6, 0.0, 0.0))
    set_edge_crease(creased_object.data, CREASE)
    for mesh_object in (loose_object, creased_object):
        subdiv_modifier = mesh_object.modifiers.new("RoundCrate", "SUBSURF")
        subdiv_modifier.levels = 2
        subdiv_modifier.render_levels = 2
        # Creaseを評価に使う。切ると右の木箱も左と同じ丸みになる。
        subdiv_modifier.use_creases = True

    loose_evaluated = tools.evaluated_snapshot(loose_object)
    creased_evaluated = tools.evaluated_snapshot(creased_object)
    loose_distance = nearest_to_corner(loose_evaluated.positions)
    creased_distance = nearest_to_corner(creased_evaluated.positions)

    print("=== 94 edge crease ===")
    print(
        f"crease={CREASE} loose verts={len(loose_object.data.vertices)} "
        f"corner distance={loose_distance:.3f} creased verts={len(creased_object.data.vertices)} "
        f"corner distance={creased_distance:.3f}"
    )

    if len(creased_object.data.vertices) != 8:
        raise RuntimeError("Creaseを付けた木箱の頂点数が増えている")
    if creased_distance > loose_distance - 0.4:
        raise RuntimeError("Creaseを付けても、角が支えなしと同じ位置まで丸まっている")

    tools.save_blend(BLEND_PATH, creased_object)


if __name__ == "__main__":
    main()
