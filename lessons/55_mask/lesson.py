"""55｜Mask。頂点グループのウェイト0の部分を、評価結果から外す。"""

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

# Trueにすると、残す側と外す側が入れ替わる。
INVERT_GROUP = False
BLEND_PATH = ROOT / "output" / "55_mask.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Mask")
    prop_object = tools.cube_object("Prop.Crate", modifiers_collection)
    tools.ensure_weight_group(
        prop_object,
        "KeepUpper",
        lambda vertex: 1.0 if vertex.co.z > 0.0 else 0.0,
    )
    mask_modifier = prop_object.modifiers.new("HideLower", "MASK")
    mask_modifier.vertex_group = "KeepUpper"
    mask_modifier.invert_vertex_group = INVERT_GROUP

    evaluated = tools.evaluated_snapshot(prop_object)
    if evaluated.positions:
        z_values = [position.z for position in evaluated.positions]
        z_span = (min(z_values), max(z_values))
    else:
        z_span = (0.0, 0.0)

    print("=== 55 mask ===")
    print(
        f"invert={INVERT_GROUP} source={len(prop_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count} z={tuple(round(axis, 3) for axis in z_span)}"
    )

    if len(prop_object.data.vertices) != 8:
        raise RuntimeError("元Meshが8頂点ではない")
    if evaluated.vertex_count >= 8:
        raise RuntimeError("ウェイト0の頂点が評価後に残っている")

    tools.save_blend(BLEND_PATH, prop_object)


if __name__ == "__main__":
    main()
