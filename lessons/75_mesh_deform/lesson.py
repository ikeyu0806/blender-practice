"""75｜Mesh Deform。体を包む粗い檻の頂点を動かし、評価後の体を一緒に伸ばす。"""

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

# 檻の上側頂点を上げる量。Bindのあとに動かす。
LIFT_Z = 1.0
BLEND_PATH = ROOT / "output" / "75_mesh_deform.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("MeshDeform")
    body_object = tools.cube_object("Body.Core", modifiers_collection, size=2.0)
    cage_object = tools.cube_object("Body.Cage", modifiers_collection, size=3.0)
    deform_modifier = body_object.modifiers.new("FollowCage", "MESH_DEFORM")
    deform_modifier.object = cage_object
    deform_modifier.precision = 5
    tools.active(body_object)
    result = bpy.ops.object.meshdeform_bind(modifier=deform_modifier.name)
    if "FINISHED" not in result or not deform_modifier.is_bound:
        raise RuntimeError(f"Mesh Deformの結合に失敗した: {result}")

    for vertex in cage_object.data.vertices:
        if vertex.co.z > 0.0:
            vertex.co.z += LIFT_Z
    cage_object.data.update()

    evaluated = tools.evaluated_snapshot(body_object)
    source_max_z = max(vertex.co.z for vertex in body_object.data.vertices)
    evaluated_max_z = max(position.z for position in evaluated.positions)

    print("=== 75 mesh deform ===")
    print(f"bound={deform_modifier.is_bound} source max z={source_max_z:.3f} evaluated={evaluated_max_z:.3f}")

    if evaluated_max_z <= source_max_z + 0.2:
        raise RuntimeError("檻の変形が体の評価後へ伝わっていない")

    tools.save_blend(BLEND_PATH, body_object)


if __name__ == "__main__":
    main()
