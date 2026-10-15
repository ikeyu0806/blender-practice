"""93｜角の近くに支えの辺を書いてからSubdivisionすると、角が元の位置の近くに残る。"""

from pathlib import Path
import sys

import bmesh
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

# 元の角から、このメートルだけ内側に支えの辺を置く。小さいほど角は鋭く残る。
LOOP_OFFSET = 0.08
BLEND_PATH = ROOT / "output" / "93_support_loops.blend"
CORNER = Vector((1.0, 1.0, 1.0))


def add_support_loops(source_mesh: bpy.types.Mesh, offset: float) -> None:
    """辺のすぐ内側へループを書き込む。Bevel Modifierではなく、Mesh自体の辺を増やす。"""
    source_bmesh = bmesh.new()
    source_bmesh.from_mesh(source_mesh)
    bmesh.ops.bevel(
        source_bmesh,
        geom=list(source_bmesh.edges),
        offset=offset,
        segments=2,
        profile=0.5,
        affect="EDGES",
    )
    source_bmesh.to_mesh(source_mesh)
    source_bmesh.free()
    source_mesh.update()


def nearest_to_corner(positions) -> float:
    return min((position - CORNER).length for position in positions)


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("SupportLoops")
    bare_object = tools.cube_object("Crate.Bare", quality_collection, location=(-1.6, 0.0, 0.0))
    held_object = tools.cube_object("Crate.Held", quality_collection, location=(1.6, 0.0, 0.0))
    add_support_loops(held_object.data, LOOP_OFFSET)
    for mesh_object in (bare_object, held_object):
        subdiv_modifier = mesh_object.modifiers.new("RoundCrate", "SUBSURF")
        subdiv_modifier.levels = 2
        subdiv_modifier.render_levels = 2

    bare_evaluated = tools.evaluated_snapshot(bare_object)
    held_evaluated = tools.evaluated_snapshot(held_object)
    bare_distance = nearest_to_corner(bare_evaluated.positions)
    held_distance = nearest_to_corner(held_evaluated.positions)

    print("=== 93 support loops ===")
    print(
        f"offset={LOOP_OFFSET} bare source={len(bare_object.data.vertices)} "
        f"corner distance={bare_distance:.3f} held source={len(held_object.data.vertices)} "
        f"corner distance={held_distance:.3f}"
    )

    if len(bare_object.data.vertices) != 8:
        raise RuntimeError("支えなしの木箱が8頂点ではない")
    if len(held_object.data.vertices) <= 8:
        raise RuntimeError("支えの辺がMeshに書き込まれていない")
    if bare_distance < 0.6:
        raise RuntimeError("支えなしの角が、元の角の近くに残っている")
    if held_distance > 0.45:
        raise RuntimeError("支えの辺を足しても、角が元の位置から離れている")

    tools.save_blend(BLEND_PATH, held_object)


if __name__ == "__main__":
    main()
