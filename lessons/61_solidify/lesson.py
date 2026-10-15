"""61｜Solidify。布の片面Meshに、評価後だけ厚みを足す。"""

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

# 厚みのメートル。offset=1なので、元の面から法線側へこの分だけ増える。
CLOTH_THICKNESS = 0.08
BLEND_PATH = ROOT / "output" / "61_solidify.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Solidify")
    cape_object = tools.grid_object(
        "Clothing.Cape",
        modifiers_collection,
        x_segments=2,
        y_segments=2,
        size=1.2,
    )
    solidify_modifier = cape_object.modifiers.new("FabricThickness", "SOLIDIFY")
    solidify_modifier.thickness = CLOTH_THICKNESS
    solidify_modifier.offset = 1.0

    evaluated = tools.evaluated_snapshot(cape_object)
    z_values = [position.z for position in evaluated.positions]
    thickness_span = max(z_values) - min(z_values)

    print("=== 61 solidify ===")
    print(
        f"thickness={CLOTH_THICKNESS} source={len(cape_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count} z span={thickness_span:.3f}"
    )

    if evaluated.vertex_count != len(cape_object.data.vertices) * 2:
        raise RuntimeError("厚みで頂点が2倍になっていない")
    if abs(thickness_span - CLOTH_THICKNESS) > 0.02:
        raise RuntimeError(f"評価後の厚みが設定と合わない: {thickness_span}")

    tools.save_blend(BLEND_PATH, cape_object)


if __name__ == "__main__":
    main()
