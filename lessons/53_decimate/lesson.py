"""53｜Decimate。細かい地面の元の頂点数は残し、評価後だけ間引く。"""

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

# 1は元の密度のまま。0.2は評価後の頂点をおおよそ2割まで崩してまとめる。
KEEP_RATIO = 0.2
BLEND_PATH = ROOT / "output" / "53_decimate.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Decimate")
    ground_object = tools.grid_object(
        "Ground.Detail",
        modifiers_collection,
        x_segments=10,
        y_segments=10,
        size=2.0,
    )
    decimate_modifier = ground_object.modifiers.new("Reduce", "DECIMATE")
    decimate_modifier.decimate_type = "COLLAPSE"
    decimate_modifier.ratio = KEEP_RATIO

    evaluated = tools.evaluated_snapshot(ground_object)
    source_count = len(ground_object.data.vertices)

    print("=== 53 decimate ===")
    print(f"ratio={KEEP_RATIO} source={source_count} evaluated={evaluated.vertex_count}")

    if evaluated.vertex_count >= source_count * 0.5:
        raise RuntimeError("評価後の頂点が半分未満まで減っていない")
    if source_count < 100:
        raise RuntimeError("元の地面が細かくない")

    tools.save_blend(BLEND_PATH, ground_object)


if __name__ == "__main__":
    main()
