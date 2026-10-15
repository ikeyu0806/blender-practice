"""52｜Build。同じ元Meshから、フレームによって現れる面の数を変える。"""

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

# このフレーム数をかけて、元Meshの面が順番に評価結果へ現れる。
FRAME_DURATION = 6.0
BLEND_PATH = ROOT / "output" / "52_build.blend"


def face_count_at(crate_object: bpy.types.Object, frame: int) -> int:
    """指定フレームの評価後面数。Buildは時刻で結果が変わる。"""
    bpy.context.scene.frame_set(frame)
    return tools.evaluated_snapshot(crate_object).face_count


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("Build")
    crate_object = tools.cube_object("Prop.Crate", modifiers_collection)
    build_modifier = crate_object.modifiers.new("Appear", "BUILD")
    build_modifier.frame_start = 1.0
    build_modifier.frame_duration = FRAME_DURATION
    build_modifier.use_random_order = False

    early_frame = 3
    done_frame = int(1 + FRAME_DURATION)
    early_faces = face_count_at(crate_object, early_frame)
    done_faces = face_count_at(crate_object, done_frame)
    # 保存して開いたときに、面が揃ったフレームが見えるようにする。
    lesson_scene.frame_set(done_frame)

    print("=== 52 build ===")
    print(f"source faces={len(crate_object.data.polygons)}")
    print(f"frame {early_frame} faces={early_faces}")
    print(f"frame {done_frame} faces={done_faces}")

    if len(crate_object.data.polygons) != 6:
        raise RuntimeError("元Meshの面数が6ではない")
    if early_faces >= done_faces:
        raise RuntimeError("途中フレームの面が、完了フレーム以上になっている")
    if done_faces != 6:
        raise RuntimeError("継続時間の終わりで6面が揃っていない")

    tools.save_blend(BLEND_PATH, crate_object)


if __name__ == "__main__":
    main()
