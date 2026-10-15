"""92｜Subdivision Surfaceは、整った四角面を滑らかにする。極が1個ある面は同じ段数でも外へ残る。"""

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

# 両方の木箱に同じ段数をかける。段数を上げても、極の面だけは外へ残りやすい。
VIEWPORT_LEVELS = 2
BLEND_PATH = ROOT / "output" / "92_subsurf_topology.blend"


def poke_one_face(source_mesh: bpy.types.Mesh) -> None:
    """1面の中央へ頂点を足し、その面を三角形の極にする。Objectの位置は変えない。"""
    source_bmesh = bmesh.new()
    source_bmesh.from_mesh(source_mesh)
    source_bmesh.faces.ensure_lookup_table()
    bmesh.ops.poke(source_bmesh, faces=[source_bmesh.faces[0]])
    source_bmesh.to_mesh(source_mesh)
    source_bmesh.free()
    source_mesh.update()


def max_abs(positions) -> float:
    """評価後の頂点が、原点から軸方向へどれだけ届いているか。"""
    return max(max(abs(position.x), abs(position.y), abs(position.z)) for position in positions)


def add_subsurf(mesh_object: bpy.types.Object) -> None:
    subdiv_modifier = mesh_object.modifiers.new("RoundCrate", "SUBSURF")
    subdiv_modifier.levels = VIEWPORT_LEVELS
    subdiv_modifier.render_levels = VIEWPORT_LEVELS


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("SubsurfTopology")
    even_object = tools.cube_object("Crate.Even", quality_collection, location=(-1.6, 0.0, 0.0))
    pole_object = tools.cube_object("Crate.Pole", quality_collection, location=(1.6, 0.0, 0.0))
    # 右だけ、1面を極にする。Modifierは両方同じ。
    poke_one_face(pole_object.data)
    add_subsurf(even_object)
    add_subsurf(pole_object)

    even_evaluated = tools.evaluated_snapshot(even_object)
    pole_evaluated = tools.evaluated_snapshot(pole_object)
    even_extent = max_abs(even_evaluated.positions)
    pole_extent = max_abs(pole_evaluated.positions)

    print("=== 92 subsurf topology ===")
    print(
        f"levels={VIEWPORT_LEVELS} even source={len(even_object.data.vertices)} "
        f"extent={even_extent:.3f} pole source={len(pole_object.data.vertices)} "
        f"extent={pole_extent:.3f}"
    )

    if len(even_object.data.vertices) != 8:
        raise RuntimeError("四角面だけの木箱が8頂点ではない")
    if len(pole_object.data.vertices) != 9:
        raise RuntimeError("極を足した木箱が9頂点ではない")
    if pole_extent < even_extent + 0.1:
        raise RuntimeError("極のある面が、四角面の木箱より外へ残っていない")

    tools.save_blend(BLEND_PATH, even_object)


if __name__ == "__main__":
    main()
