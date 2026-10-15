"""65｜Wireframe。立方体の面を、評価後だけ辺に沿った細い骨組みへ置き換える。"""

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

# 骨組みの太さ。大きいほど元の面を埋める。
FRAME_THICKNESS = 0.05
BLEND_PATH = ROOT / "output" / "65_wireframe.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Wireframe")
    cage_object = tools.cube_object("Prop.Cage", modifiers_collection, size=1.2)
    wire_modifier = cage_object.modifiers.new("Bars", "WIREFRAME")
    wire_modifier.thickness = FRAME_THICKNESS
    wire_modifier.use_replace = True

    evaluated = tools.evaluated_snapshot(cage_object)

    print("=== 65 wireframe ===")
    print(
        f"thickness={FRAME_THICKNESS} source vertices={len(cage_object.data.vertices)} "
        f"evaluated vertices={evaluated.vertex_count} faces={evaluated.face_count}"
    )

    if len(cage_object.data.vertices) != 8:
        raise RuntimeError("元の立方体が8頂点ではない")
    if evaluated.vertex_count <= 8:
        raise RuntimeError("骨組みの評価後で頂点が増えていない")

    tools.save_blend(BLEND_PATH, cage_object)


if __name__ == "__main__":
    main()
