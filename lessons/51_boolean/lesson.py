"""51｜Boolean。壁の元Meshは残し、評価後だけ扉の形をくり抜く。"""

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

# DIFFERENCEは壁から扉の体積を引く。UNIONは結合、INTERSECTは共通部分。
OPERATION = "DIFFERENCE"
BLEND_PATH = ROOT / "output" / "51_boolean.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Boolean")
    wall_object = tools.cube_object("Room.Wall", modifiers_collection, size=2.0)
    # 壁の手前下にめり込む箱。これが扉の開口になる。
    door_object = tools.cube_object(
        "Room.DoorCutter",
        modifiers_collection,
        size=0.8,
        location=(0.0, -0.7, -0.5),
    )
    boolean_modifier = wall_object.modifiers.new("DoorOpening", "BOOLEAN")
    boolean_modifier.operation = OPERATION
    boolean_modifier.operand_type = "OBJECT"
    boolean_modifier.object = door_object
    boolean_modifier.solver = "MANIFOLD"

    evaluated = tools.evaluated_snapshot(wall_object)
    source_faces = len(wall_object.data.polygons)

    print("=== 51 boolean ===")
    print(
        f"operation={OPERATION} source faces={source_faces} "
        f"evaluated faces={evaluated.face_count} vertices={evaluated.vertex_count}"
    )

    if wall_object.data is door_object.data:
        raise RuntimeError("壁と扉カッターがMeshを共有している")
    if len(wall_object.data.vertices) != 8:
        raise RuntimeError("壁の元Meshが立方体のままではない")
    if evaluated.face_count <= source_faces:
        raise RuntimeError("開口の評価後で面が増えていない")

    tools.save_blend(BLEND_PATH, wall_object)


if __name__ == "__main__":
    main()
