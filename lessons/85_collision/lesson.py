"""85｜Collision。床の衝突判定が、落ちてくる布を床の上で止める。

布のClothは、衝突の相手として使う。この回で新しく見るのは床側のCollision。
"""

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

# 床の表面から布を離す厚さ。大きいと布が空中で止まる。
THICKNESS_OUTER = 0.02
LAST_FRAME = 12
BLEND_PATH = ROOT / "output" / "85_collision.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("Collision")
    floor_object = tools.grid_object(
        "Room.Floor", modifiers_collection, x_segments=1, y_segments=1, size=3.0
    )
    collision_modifier = floor_object.modifiers.new("BlockCloth", "COLLISION")
    collision_modifier.settings.thickness_outer = THICKNESS_OUTER
    cape_object = tools.grid_object(
        "Clothing.Cape",
        modifiers_collection,
        x_segments=5,
        y_segments=5,
        size=1.0,
        location=(0.0, 0.0, 0.4),
    )
    cape_object.modifiers.new("Drape", "CLOTH")
    lesson_scene.frame_end = LAST_FRAME
    for frame in range(1, LAST_FRAME + 1):
        lesson_scene.frame_set(frame)

    evaluated = tools.evaluated_snapshot(cape_object)
    world_z = [position.z for position in evaluated.world_positions]
    floor_evaluated = tools.evaluated_snapshot(floor_object)

    print("=== 85 collision ===")
    print(
        f"thickness={THICKNESS_OUTER} cloth world z={min(world_z):.3f}..{max(world_z):.3f} "
        f"floor vertices={floor_evaluated.vertex_count}"
    )

    if floor_evaluated.vertex_count != len(floor_object.data.vertices):
        raise RuntimeError("Collisionが床の頂点を変えた")
    if min(world_z) < -0.05:
        raise RuntimeError("布が床を突き抜けている")
    if max(world_z) > 0.35:
        raise RuntimeError("布が落ちきっていない")

    tools.save_blend(BLEND_PATH, floor_object)


if __name__ == "__main__":
    main()
