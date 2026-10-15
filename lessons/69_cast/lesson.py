"""69｜Cast。でこぼこした石の頂点を、評価後だけ原点から等距離の球へ寄せる。"""

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

# 1で目標の球へ完全に寄せる。0.5なら元の形と球の中間。
CAST_FACTOR = 1.0
BLEND_PATH = ROOT / "output" / "69_cast.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Cast")
    stone_object = tools.grid_object(
        "Stone.Mound", modifiers_collection, x_segments=8, y_segments=8, size=2.0
    )
    for vertex in stone_object.data.vertices:
        vertex.co.z = 0.15 * (1.0 - (vertex.co.x ** 2 + vertex.co.y ** 2))
    stone_object.data.update()
    source_lengths = [vertex.co.length for vertex in stone_object.data.vertices]

    cast_modifier = stone_object.modifiers.new("ToSphere", "CAST")
    cast_modifier.cast_type = "SPHERE"
    cast_modifier.factor = CAST_FACTOR

    evaluated = tools.evaluated_snapshot(stone_object)
    evaluated_lengths = [position.length for position in evaluated.positions]
    source_range = max(source_lengths) - min(source_lengths)
    evaluated_range = max(evaluated_lengths) - min(evaluated_lengths)

    print("=== 69 cast ===")
    print(f"factor={CAST_FACTOR} source range={source_range:.3f} evaluated range={evaluated_range:.3f}")

    if source_range < 0.05:
        raise RuntimeError("元の頂点がすでに球に近い")
    if evaluated_range >= source_range:
        raise RuntimeError("評価後が球へ寄っていない")

    tools.save_blend(BLEND_PATH, stone_object)


if __name__ == "__main__":
    main()
