"""44｜Weighted Normal。大きい面の法線が、共有頂点のカスタム法線へ強く残る。"""

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

# 大きいほど、面積の大きい面の法線が共有頂点へ強く残る。
FACE_WEIGHT = 50
BLEND_PATH = ROOT / "output" / "44_weighted_normal.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("WeightedNormal")
    # 細長い箱。広い面と狭い面が隣り合うので、面積による重みの差が見える。
    crate_object = tools.mesh_from_pydata(
        "Crate.Side",
        modifiers_collection,
        [
            (-1.2, -0.3, -0.8),
            (1.2, -0.3, -0.8),
            (1.2, 0.3, -0.8),
            (-1.2, 0.3, -0.8),
            (-1.2, -0.3, 0.8),
            (1.2, -0.3, 0.8),
            (1.2, 0.3, 0.8),
            (-1.2, 0.3, 0.8),
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
    weighted_modifier = crate_object.modifiers.new("WideFace", "WEIGHTED_NORMAL")
    weighted_modifier.mode = "FACE_AREA"
    weighted_modifier.weight = FACE_WEIGHT
    weighted_modifier.keep_sharp = False

    evaluated = tools.evaluated_snapshot(crate_object)
    source_count = len(crate_object.data.vertices)
    # 軸にぴったり沿う法線は、どれか1成分だけが1に近い。混ざると複数成分が残る。
    mixed = [
        normal
        for normal in evaluated.corner_normals
        if sum(abs(axis) > 0.2 for axis in normal) >= 2
    ]

    print("=== 44 weighted normal ===")
    print(f"vertices={source_count} corners={len(evaluated.corner_normals)}")
    print(f"mixed corners={len(mixed)} weight={FACE_WEIGHT}")
    if mixed:
        print(f"example={tuple(round(axis, 3) for axis in mixed[0])}")

    if evaluated.vertex_count != source_count:
        raise RuntimeError("Weighted Normalで頂点数が変わった")
    if not mixed:
        raise RuntimeError("面積で混ざったコーナー法線がない")

    tools.save_blend(BLEND_PATH, crate_object)


if __name__ == "__main__":
    main()
