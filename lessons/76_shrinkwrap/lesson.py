"""76｜Shrinkwrap。体の上に浮いた布を、評価後だけ一番近い表面へ貼り付ける。"""

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

# 表面からこのメートルだけ離して貼る。0だと体と布が同じ位置になる。
SURFACE_OFFSET = 0.05
BLEND_PATH = ROOT / "output" / "76_shrinkwrap.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Shrinkwrap")
    body_object = tools.cube_object("Body.Torso", modifiers_collection, size=2.0)
    cloth_object = tools.grid_object(
        "Clothing.Patch",
        modifiers_collection,
        x_segments=4,
        y_segments=4,
        size=1.2,
        location=(0.0, 0.0, 2.0),
    )
    wrap_modifier = cloth_object.modifiers.new("StickToBody", "SHRINKWRAP")
    wrap_modifier.target = body_object
    wrap_modifier.wrap_method = "NEAREST_SURFACEPOINT"
    wrap_modifier.offset = SURFACE_OFFSET

    evaluated = tools.evaluated_snapshot(cloth_object)
    max_z = max(position.z for position in evaluated.positions)

    print("=== 76 shrinkwrap ===")
    print(f"offset={SURFACE_OFFSET} evaluated max local z={max_z:.3f}")

    if max(vertex.co.z for vertex in cloth_object.data.vertices) > 1e-6:
        raise RuntimeError("布の元Meshが平らではない")
    # ObjectはZ=2にある。評価後のローカルZが負なら、表面まで下がっている。
    if max_z > -0.5:
        raise RuntimeError("布が体の表面まで降りていない")

    tools.save_blend(BLEND_PATH, cloth_object)


if __name__ == "__main__":
    main()
