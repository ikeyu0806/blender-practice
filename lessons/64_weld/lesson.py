"""64｜Weld。同じ位置に重なった頂点を、評価後だけ1つにまとめる。"""

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

# この距離より近い頂点を、評価後に1つへまとめる。
MERGE_DISTANCE = 0.01
BLEND_PATH = ROOT / "output" / "64_weld.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Weld")
    # 0番と1番は同じ座標。面は2枚あるように見えるが、評価後は1頂点へまとまる。
    plate_object = tools.mesh_from_pydata(
        "Armor.Plate",
        modifiers_collection,
        [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)],
        [],
        [(0, 2, 3), (1, 2, 3)],
    )
    weld_modifier = plate_object.modifiers.new("MergeSeam", "WELD")
    weld_modifier.merge_threshold = MERGE_DISTANCE

    evaluated = tools.evaluated_snapshot(plate_object)

    print("=== 64 weld ===")
    print(
        f"distance={MERGE_DISTANCE} source vertices={len(plate_object.data.vertices)} "
        f"faces={len(plate_object.data.polygons)} evaluated vertices={evaluated.vertex_count} "
        f"faces={evaluated.face_count}"
    )

    if len(plate_object.data.vertices) != 4:
        raise RuntimeError("元の重なり頂点が残っていない")
    if evaluated.vertex_count >= 4:
        raise RuntimeError("近い頂点が評価後にまとまっていない")

    tools.save_blend(BLEND_PATH, plate_object)


if __name__ == "__main__":
    main()
