"""81｜Surface Deform。粗い布の1頂点の移動を、細かい布の評価後へ伝える。"""

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

# Bindのあとに、粗い布の1頂点を上げる高さ。
LIFT_Z = 0.4
BLEND_PATH = ROOT / "output" / "81_surface_deform.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("SurfaceDeform")
    driver_object = tools.grid_object(
        "Cloth.Driver", modifiers_collection, x_segments=4, y_segments=4, size=2.0
    )
    detail_object = tools.grid_object(
        "Cloth.Detail", modifiers_collection, x_segments=8, y_segments=8, size=1.6
    )
    deform_modifier = detail_object.modifiers.new("FollowDriver", "SURFACE_DEFORM")
    deform_modifier.target = driver_object
    tools.active(detail_object)
    result = bpy.ops.object.surfacedeform_bind(modifier=deform_modifier.name)
    if "FINISHED" not in result or not deform_modifier.is_bound:
        raise RuntimeError(f"Surface Deformの結合に失敗した: {result}")

    driver_object.data.vertices[0].co.z += LIFT_Z
    driver_object.data.update()
    evaluated = tools.evaluated_snapshot(detail_object)
    max_z = max(position.z for position in evaluated.positions)

    print("=== 81 surface deform ===")
    print(f"bound={deform_modifier.is_bound} detail max z={max_z:.3f}")

    if max(vertex.co.z for vertex in detail_object.data.vertices) > 1e-6:
        raise RuntimeError("細かい布の元Meshが平らではない")
    if max_z < 0.02:
        raise RuntimeError("粗い布の移動が細かい布へ伝わっていない")

    tools.save_blend(BLEND_PATH, detail_object)


if __name__ == "__main__":
    main()
