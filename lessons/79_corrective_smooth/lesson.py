"""79｜Corrective Smooth。同じねじりのあと、補正を足した評価後の位置が変わる。"""

from pathlib import Path
import sys
from math import radians

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

# ねじりのあとに寄せる回数。0に近いと、ねじりだけの形に残る。
FIX_ITERATIONS = 15
BLEND_PATH = ROOT / "output" / "79_corrective_smooth.blend"


def add_twist(sleeve_object: bpy.types.Object) -> None:
    """両方の袖に同じSimple Deformを置き、補正の有無だけを比べる。"""
    twist_modifier = sleeve_object.modifiers.new("Twist", "SIMPLE_DEFORM")
    twist_modifier.deform_method = "TWIST"
    twist_modifier.angle = radians(70)
    twist_modifier.deform_axis = "Z"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("CorrectiveSmooth")
    sleeve_mesh = tools.make_cube_mesh("Sleeve.Mesh", 2.0)
    tools.subdivide_mesh(sleeve_mesh, cuts=2)
    twisted_object = tools.link_mesh_object(
        "Sleeve.Twisted", sleeve_mesh, modifiers_collection, (-1.6, 0.0, 0.0)
    )
    fixed_object = tools.link_mesh_object(
        "Sleeve.Fixed", sleeve_mesh, modifiers_collection, (1.6, 0.0, 0.0)
    )
    add_twist(twisted_object)
    add_twist(fixed_object)
    fix_modifier = fixed_object.modifiers.new("KeepVolume", "CORRECTIVE_SMOOTH")
    fix_modifier.factor = 1.0
    fix_modifier.iterations = FIX_ITERATIONS
    fix_modifier.smooth_type = "LENGTH_WEIGHTED"

    twisted = tools.evaluated_snapshot(twisted_object)
    fixed = tools.evaluated_snapshot(fixed_object)
    delta = max(
        (left - right).length
        for left, right in zip(twisted.positions, fixed.positions)
    )

    print("=== 79 corrective smooth ===")
    print(f"iterations={FIX_ITERATIONS} shared vertices={len(sleeve_mesh.vertices)} delta={delta:.3f}")

    if twisted_object.data is not fixed_object.data:
        raise RuntimeError("左右が同じ元Meshを共有していない")
    if delta < 0.05:
        raise RuntimeError("補正で評価後の位置が変わっていない")

    tools.save_blend(BLEND_PATH, fixed_object)


if __name__ == "__main__":
    main()
