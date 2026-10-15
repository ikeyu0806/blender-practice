"""54｜Edge Split。面の数は6のまま、鋭い辺で評価後の頂点だけを複製する。"""

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

# 隣り合う面の角度がこの値より大きい辺で、評価後の頂点を分ける。
SPLIT_ANGLE = radians(30)
BLEND_PATH = ROOT / "output" / "54_edge_split.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("EdgeSplit")
    crate_object = tools.cube_object("Crate.HardEdge", modifiers_collection)
    split_modifier = crate_object.modifiers.new("SplitSharp", "EDGE_SPLIT")
    split_modifier.use_edge_angle = True
    split_modifier.split_angle = SPLIT_ANGLE

    evaluated = tools.evaluated_snapshot(crate_object)

    print("=== 54 edge split ===")
    print(
        f"angle={SPLIT_ANGLE:.3f} source vertices={len(crate_object.data.vertices)} "
        f"evaluated vertices={evaluated.vertex_count} faces={evaluated.face_count}"
    )

    if evaluated.face_count != 6:
        raise RuntimeError("面数が6のままではない")
    if evaluated.vertex_count <= len(crate_object.data.vertices):
        raise RuntimeError("鋭い辺で評価後の頂点が増えていない")

    tools.save_blend(BLEND_PATH, crate_object)


if __name__ == "__main__":
    main()
