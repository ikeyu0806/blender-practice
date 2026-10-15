"""56｜Mirror。体の右半分の元Meshから、評価後だけ左半分を作る。"""

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

# 原点をまたぐX軸で左右を作る。中央の頂点は結合して1つの胴にする。
MERGE_CENTER = True
BLEND_PATH = ROOT / "output" / "56_mirror.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Mirror")
    # Xが0以上だけの半身。原点の平面が鏡になる。
    body_object = tools.mesh_from_pydata(
        "Body.RightHalf",
        modifiers_collection,
        [
            (0.0, -0.45, 0.0),
            (0.35, -0.45, 0.0),
            (0.35, 0.45, 0.0),
            (0.0, 0.45, 0.0),
            (0.0, -0.45, 1.4),
            (0.35, -0.45, 1.4),
            (0.35, 0.45, 1.4),
            (0.0, 0.45, 1.4),
        ],
        [],
        [
            (0, 1, 2, 3),
            (4, 7, 6, 5),
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (3, 7, 4, 0),
        ],
    )
    mirror_modifier = body_object.modifiers.new("LeftSide", "MIRROR")
    mirror_modifier.use_axis[0] = True
    mirror_modifier.use_axis[1] = False
    mirror_modifier.use_axis[2] = False
    mirror_modifier.use_mirror_merge = MERGE_CENTER

    evaluated = tools.evaluated_snapshot(body_object)
    source_min_x = min(vertex.co.x for vertex in body_object.data.vertices)
    evaluated_min_x = min(position.x for position in evaluated.positions)

    print("=== 56 mirror ===")
    print(
        f"merge={MERGE_CENTER} source vertices={len(body_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count} min x source={source_min_x:.3f} "
        f"evaluated={evaluated_min_x:.3f}"
    )

    if source_min_x < -1e-6:
        raise RuntimeError("元Meshが右半分だけになっていない")
    if evaluated_min_x >= -0.1:
        raise RuntimeError("評価後に左側が作られていない")
    if evaluated.vertex_count <= len(body_object.data.vertices):
        raise RuntimeError("鏡像で頂点が増えていない")

    tools.save_blend(BLEND_PATH, body_object)


if __name__ == "__main__":
    main()
