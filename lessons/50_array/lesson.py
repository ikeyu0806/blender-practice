"""50｜Array。1本の柱Meshを、評価結果の中で等間隔に繰り返す。"""

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

# 元Meshは1本。評価後の本数はこの値になる。
POST_COUNT = 4
BLEND_PATH = ROOT / "output" / "50_array.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Array")
    post_object = tools.cube_object(
        "Fence.Post", modifiers_collection, size=0.3, location=(0.0, 0.0, 0.8)
    )
    # 高さをMesh側で伸ばす。Object.scaleは1のままにして、本数の検査を分かりやすくする。
    for vertex in post_object.data.vertices:
        vertex.co.z *= 4.0
    post_object.data.update()

    array_modifier = post_object.modifiers.new("RepeatPosts", "ARRAY")
    array_modifier.count = POST_COUNT
    array_modifier.use_relative_offset = True
    # 1.0だと隣と接する。1.8で柱の間に隙間ができる。
    array_modifier.relative_offset_displace[0] = 1.8

    evaluated = tools.evaluated_snapshot(post_object)
    source_count = len(post_object.data.vertices)

    print("=== 50 array ===")
    print(f"source vertices={source_count} evaluated={evaluated.vertex_count} count={POST_COUNT}")

    if evaluated.vertex_count != source_count * POST_COUNT:
        raise RuntimeError("評価後の頂点数が、柱の本数倍になっていない")
    if source_count != 8:
        raise RuntimeError("元の柱が8頂点の立方体ではない")

    tools.save_blend(BLEND_PATH, post_object)


if __name__ == "__main__":
    main()
