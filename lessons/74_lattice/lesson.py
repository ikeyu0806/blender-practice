"""74｜Lattice。箱を包む格子点を動かし、評価後の箱の幅だけを広げる。"""

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

# 格子の上側の点をXへずらす量。箱の上側の評価後幅が広がる。
SHIFT_X = 0.4
BLEND_PATH = ROOT / "output" / "74_lattice.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Lattice")
    crate_object = tools.cube_object("Crate.Body", modifiers_collection, size=2.0)
    lattice_data = bpy.data.lattices.new("Crate.Cage")
    lattice_data.points_u = 2
    lattice_data.points_v = 2
    lattice_data.points_w = 2
    cage_object = bpy.data.objects.new("Crate.Cage", lattice_data)
    modifiers_collection.objects.link(cage_object)
    # 既定のLatticeは1m立方。箱の一辺2mを包むためにObjectのScaleを広げる。
    cage_object.scale = (2.0, 2.0, 2.0)
    lattice_modifier = crate_object.modifiers.new("CageWarp", "LATTICE")
    lattice_modifier.object = cage_object
    for point in lattice_data.points:
        if point.co_deform.z > 0.0:
            point.co_deform.x += SHIFT_X

    evaluated = tools.evaluated_snapshot(crate_object)
    source_span = tools.span([vertex.co.x for vertex in crate_object.data.vertices])
    evaluated_span = tools.span([position.x for position in evaluated.positions])

    print("=== 74 lattice ===")
    print(f"shift={SHIFT_X} source x={source_span:.3f} evaluated x={evaluated_span:.3f}")

    if len(crate_object.data.vertices) != 8:
        raise RuntimeError("箱の元頂点が8ではない")
    if evaluated_span <= source_span + 0.15:
        raise RuntimeError("格子点の移動が箱の評価後へ広がっていない")

    tools.save_blend(BLEND_PATH, crate_object)


if __name__ == "__main__":
    main()
