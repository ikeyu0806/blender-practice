"""58｜Remesh。立方体の形を保ったまま、評価後の面をボクセルの格子へ作り直す。"""

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

# 小さいほど評価後の格子が細かくなる。元の8頂点は変わらない。
VOXEL_SIZE = 0.25
BLEND_PATH = ROOT / "output" / "58_remesh.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Remesh")
    stone_object = tools.cube_object("Stone.Block", modifiers_collection, size=2.0)
    remesh_modifier = stone_object.modifiers.new("VoxelGrid", "REMESH")
    remesh_modifier.mode = "VOXEL"
    remesh_modifier.voxel_size = VOXEL_SIZE

    evaluated = tools.evaluated_snapshot(stone_object)

    print("=== 58 remesh ===")
    print(
        f"voxel={VOXEL_SIZE} source={len(stone_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count}"
    )

    if len(stone_object.data.vertices) != 8:
        raise RuntimeError("元Meshが8頂点のままではない")
    if evaluated.vertex_count < len(stone_object.data.vertices) * 5:
        raise RuntimeError("ボクセルの格子が十分に作られていない")

    tools.save_blend(BLEND_PATH, stone_object)


if __name__ == "__main__":
    main()
