"""90｜Soft Body。目標位置へ戻す力を切ると、塊がフレームとともに自重で下がる。"""

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

LAST_FRAME = 8
BLEND_PATH = ROOT / "output" / "90_soft_body.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("SoftBody")
    jelly_object = tools.cube_object("Prop.Jelly", modifiers_collection, size=1.0)
    tools.subdivide_mesh(jelly_object.data, cuts=2)
    jelly_object.location.z = 1.0
    soft_modifier = jelly_object.modifiers.new("Squish", "SOFT_BODY")
    # Goalが有効だと頂点が元の位置へ戻ろうとして、自重の垂れが見えにくい。
    soft_modifier.settings.use_goal = False
    source_min_z = min(vertex.co.z for vertex in jelly_object.data.vertices)
    lesson_scene.frame_end = LAST_FRAME
    for frame in range(1, LAST_FRAME + 1):
        lesson_scene.frame_set(frame)

    evaluated = tools.evaluated_snapshot(jelly_object)
    evaluated_min_z = min(position.z for position in evaluated.positions)

    print("=== 90 soft body ===")
    print(f"frame={LAST_FRAME} source min z={source_min_z:.3f} evaluated={evaluated_min_z:.3f}")

    if evaluated_min_z >= source_min_z:
        raise RuntimeError("自重で評価後が下がっていない")

    tools.save_blend(BLEND_PATH, jelly_object)


if __name__ == "__main__":
    main()
