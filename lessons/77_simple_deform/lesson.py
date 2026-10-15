"""77｜Simple Deform。平らな板を、評価後だけZ軸の周りに円弧へ曲げる。"""

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

# 曲げる角度。大きいほど板の端が回り込む。
BEND_ANGLE = radians(90)
BLEND_PATH = ROOT / "output" / "77_simple_deform.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("SimpleDeform")
    plank_object = tools.grid_object(
        "Prop.Plank", modifiers_collection, x_segments=8, y_segments=1, size=2.0
    )
    bend_modifier = plank_object.modifiers.new("BendArc", "SIMPLE_DEFORM")
    bend_modifier.deform_method = "BEND"
    bend_modifier.angle = BEND_ANGLE
    bend_modifier.deform_axis = "Z"

    evaluated = tools.evaluated_snapshot(plank_object)
    source_span = tools.span([vertex.co.x for vertex in plank_object.data.vertices])
    evaluated_span = tools.span([position.x for position in evaluated.positions])

    print("=== 77 simple deform ===")
    print(f"angle={BEND_ANGLE:.3f} source x={source_span:.3f} evaluated x={evaluated_span:.3f}")

    if abs(evaluated_span - source_span) < 0.2:
        raise RuntimeError("曲げで板の幅が変わっていない")

    tools.save_blend(BLEND_PATH, plank_object)


if __name__ == "__main__":
    main()
