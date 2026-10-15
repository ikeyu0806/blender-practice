"""73｜Laplacian Deform。端を固定したマントを、固定点の移動に合わせて評価後に曲げる。"""

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

# 結合したあとに、+X側の固定点をこの高さだけ上げる。
LIFT_Z = 0.4
BLEND_PATH = ROOT / "output" / "73_laplacian_deform.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("LaplacianDeform")
    cape_object = tools.grid_object(
        "Clothing.Cape", modifiers_collection, x_segments=6, y_segments=2, size=2.0
    )
    tools.ensure_weight_group(
        cape_object,
        "Pins",
        lambda vertex: 1.0 if abs(vertex.co.x) > 0.6 else 0.0,
    )
    deform_modifier = cape_object.modifiers.new("KeepCloth", "LAPLACIANDEFORM")
    deform_modifier.vertex_group = "Pins"
    tools.active(cape_object)
    result = bpy.ops.object.laplaciandeform_bind(modifier=deform_modifier.name)
    if "FINISHED" not in result or not deform_modifier.is_bind:
        raise RuntimeError(f"Laplacian Deformの結合に失敗した: {result}")

    for vertex in cape_object.data.vertices:
        if vertex.co.x > 0.6:
            vertex.co.z += LIFT_Z
    cape_object.data.update()

    evaluated = tools.evaluated_snapshot(cape_object)
    z_values = [position.z for position in evaluated.positions]

    print("=== 73 laplacian deform ===")
    print(f"bound={deform_modifier.is_bind} z={min(z_values):.3f}..{max(z_values):.3f}")

    if max(z_values) < 0.15:
        raise RuntimeError("固定点の移動が表面へ広がっていない")
    if min(z_values) > 0.2:
        raise RuntimeError("反対側の固定点まで持ち上がっている")

    tools.save_blend(BLEND_PATH, cape_object)


if __name__ == "__main__":
    main()
