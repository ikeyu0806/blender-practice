"""43｜Normal Edit。頂点は動かさず、評価後の法線だけをEmptyの方向へ向ける。"""

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

# Directionalは、targetのEmptyがある方向へ法線を寄せる。
AIM = (0.0, -2.0, 2.0)
BLEND_PATH = ROOT / "output" / "43_normal_edit.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("NormalEdit")
    sign_object = tools.cube_object("Sign.Board", modifiers_collection)
    # EmptyはMeshを持たない。法線が向く目標の位置だけを持つ。
    aim_object = tools.empty_object("Sign.Aim", modifiers_collection, AIM)

    normal_modifier = sign_object.modifiers.new("AimNormals", "NORMAL_EDIT")
    normal_modifier.mode = "DIRECTIONAL"
    normal_modifier.target = aim_object
    normal_modifier.mix_mode = "COPY"
    normal_modifier.mix_factor = 1.0

    evaluated = tools.evaluated_snapshot(sign_object)
    source_positions = [vertex.co.copy() for vertex in sign_object.data.vertices]
    face_normal = sign_object.data.polygons[0].normal
    corner_normal = evaluated.corner_normals[0]

    print("=== 43 normal edit ===")
    print(f"face normal={tuple(round(axis, 3) for axis in face_normal)}")
    print(f"corner normal={tuple(round(axis, 3) for axis in corner_normal)}")
    print(f"vertices unchanged={evaluated.vertex_count}")

    if evaluated.vertex_count != len(source_positions):
        raise RuntimeError("Normal Editで頂点数が変わった")
    if any((left - right).length > 1e-6 for left, right in zip(evaluated.positions, source_positions)):
        raise RuntimeError("Normal Editが頂点座標を動かした")
    # 面法線は軸に沿い、カスタム法線はEmptyの方（-Yかつ+Z）へ寄る。
    if abs(corner_normal.y) < 0.2 or corner_normal.z < 0.4:
        raise RuntimeError(f"法線がAimの方向へ寄っていない: {corner_normal}")

    tools.save_blend(BLEND_PATH, sign_object)


if __name__ == "__main__":
    main()
