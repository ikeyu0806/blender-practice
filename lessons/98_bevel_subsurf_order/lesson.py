"""98｜BevelをSubdivisionの前に置くと角の帯が残る。後に置くと、丸めたあとの浅い角には面取りが付かない。"""

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

# 面取りの幅。順番を入れ替えても、この値は両方で同じにする。
BEVEL_WIDTH = 0.15
BLEND_PATH = ROOT / "output" / "98_bevel_subsurf_order.blend"


def add_bevel(mesh_object: bpy.types.Object) -> None:
    bevel_modifier = mesh_object.modifiers.new("EdgeBand", "BEVEL")
    bevel_modifier.width = BEVEL_WIDTH
    bevel_modifier.segments = 2
    # 角度が急な辺だけ面取りする。Subdivisionのあとは辺が浅くなり、対象から外れる。
    bevel_modifier.limit_method = "ANGLE"


def add_subsurf(mesh_object: bpy.types.Object) -> None:
    subdiv_modifier = mesh_object.modifiers.new("RoundCrate", "SUBSURF")
    subdiv_modifier.levels = 2
    subdiv_modifier.render_levels = 2


def max_abs(positions) -> float:
    return max(max(abs(position.x), abs(position.y), abs(position.z)) for position in positions)


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("BevelSubsurfOrder")
    crate_mesh = tools.make_cube_mesh("Crate.Shared.Mesh")
    bevel_first_object = tools.link_mesh_object(
        "Crate.BevelFirst",
        crate_mesh,
        quality_collection,
        location=(-1.6, 0.0, 0.0),
    )
    subsurf_first_object = tools.link_mesh_object(
        "Crate.SubsurfFirst",
        crate_mesh,
        quality_collection,
        location=(1.6, 0.0, 0.0),
    )
    add_bevel(bevel_first_object)
    add_subsurf(bevel_first_object)
    add_subsurf(subsurf_first_object)
    add_bevel(subsurf_first_object)

    bevel_first = tools.evaluated_snapshot(bevel_first_object)
    subsurf_first = tools.evaluated_snapshot(subsurf_first_object)
    bevel_extent = max_abs(bevel_first.positions)
    subsurf_extent = max_abs(subsurf_first.positions)

    print("=== 98 bevel subsurf order ===")
    print(
        f"width={BEVEL_WIDTH} source={len(crate_mesh.vertices)} "
        f"bevel-first verts={bevel_first.vertex_count} extent={bevel_extent:.3f} "
        f"subsurf-first verts={subsurf_first.vertex_count} extent={subsurf_extent:.3f}"
    )

    if len(crate_mesh.vertices) != 8:
        raise RuntimeError("共有している元Meshが8頂点ではない")
    if bevel_first.vertex_count <= subsurf_first.vertex_count:
        raise RuntimeError("Bevelを先にしても、評価後の頂点が後置きより増えていない")
    if bevel_extent < subsurf_extent + 0.08:
        raise RuntimeError("Bevelを先にしても、角が後置きより外へ残っていない")

    tools.save_blend(BLEND_PATH, bevel_first_object)


if __name__ == "__main__":
    main()
