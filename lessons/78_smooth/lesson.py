"""78｜Smooth。1頂点だけ持ち上げた布を、評価後に周りへならす。"""

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

# ならす繰り返し。多いほど突起が周りの高さへ近づく。
SMOOTH_ITERATIONS = 10
BLEND_PATH = ROOT / "output" / "78_smooth.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Smooth")
    cloth_object = tools.grid_object(
        "Clothing.Cloth", modifiers_collection, x_segments=4, y_segments=4, size=2.0
    )
    cloth_object.data.vertices[12].co.z = 0.5
    cloth_object.data.update()
    smooth_modifier = cloth_object.modifiers.new("FlattenSpike", "SMOOTH")
    smooth_modifier.factor = 1.0
    smooth_modifier.iterations = SMOOTH_ITERATIONS

    evaluated = tools.evaluated_snapshot(cloth_object)
    source_max_z = max(vertex.co.z for vertex in cloth_object.data.vertices)
    evaluated_max_z = max(position.z for position in evaluated.positions)

    print("=== 78 smooth ===")
    print(f"iterations={SMOOTH_ITERATIONS} source max z={source_max_z:.3f} evaluated={evaluated_max_z:.3f}")

    if source_max_z < 0.4:
        raise RuntimeError("元Meshの突起が無い")
    if evaluated_max_z >= source_max_z:
        raise RuntimeError("評価後の突起が低くなっていない")

    tools.save_blend(BLEND_PATH, cloth_object)


if __name__ == "__main__":
    main()
