"""99｜ObjectのScaleをMeshへ焼かずにBevelすると、世界座標では軸ごとに面取り幅が変わる。"""

from pathlib import Path
import sys

import bpy
from mathutils import Vector

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

# 未適用の木箱は、この倍率をObject.scaleにだけ持たせる。右は同じ倍率を頂点座標へ書き込む。
SCALE_X = 2.0
BEVEL_WIDTH = 0.2
BLEND_PATH = ROOT / "output" / "99_unapplied_scale.blend"


def add_bevel(mesh_object: bpy.types.Object) -> None:
    bevel_modifier = mesh_object.modifiers.new("EdgeBand", "BEVEL")
    bevel_modifier.width = BEVEL_WIDTH
    bevel_modifier.segments = 1
    bevel_modifier.limit_method = "NONE"


def corner_insets(mesh_object: bpy.types.Object, local_corner: Vector) -> tuple[float, float]:
    """正の角から、面取りで内側へ入った世界座標の幅。XとYを別々に返す。"""
    evaluated = tools.evaluated_snapshot(mesh_object)
    world_corner = mesh_object.matrix_world @ local_corner
    deltas = []
    for position in evaluated.world_positions:
        delta = world_corner - position
        if delta.x >= -0.02 and delta.y >= -0.02 and delta.z >= -0.02 and delta.length < 1.2:
            deltas.append(delta)
    if len(deltas) < 3:
        raise RuntimeError(f"{mesh_object.name}の角に面取り頂点が見つからない")
    return max(delta.x for delta in deltas), max(delta.y for delta in deltas)


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("UnappliedScale")
    scaled_object = tools.cube_object("Crate.Scaled", quality_collection, location=(0.0, 0.0, 0.0))
    # ScaleはObjectの変形。Meshの頂点は一辺2の立方体のまま。
    scaled_object.scale = (SCALE_X, 1.0, 1.0)
    applied_mesh = tools.make_cube_mesh("Crate.Applied.Mesh")
    for vertex in applied_mesh.vertices:
        vertex.co.x *= SCALE_X
    applied_mesh.update()
    applied_object = tools.link_mesh_object(
        "Crate.Applied",
        applied_mesh,
        quality_collection,
        location=(8.0, 0.0, 0.0),
    )
    add_bevel(scaled_object)
    add_bevel(applied_object)

    scaled_dx, scaled_dy = corner_insets(scaled_object, Vector((1.0, 1.0, 1.0)))
    applied_dx, applied_dy = corner_insets(applied_object, Vector((SCALE_X, 1.0, 1.0)))

    print("=== 99 unapplied scale ===")
    print(
        f"scale x={SCALE_X} bevel={BEVEL_WIDTH} "
        f"scaled world inset x={scaled_dx:.3f} y={scaled_dy:.3f} "
        f"applied world inset x={applied_dx:.3f} y={applied_dy:.3f}"
    )

    if abs(scaled_object.scale.x - SCALE_X) > 1e-6:
        raise RuntimeError("左の木箱のScaleが実験値ではない")
    if any(abs(component - 1.0) > 1e-6 for component in applied_object.scale):
        raise RuntimeError("右の木箱のScaleが1ではない")
    if scaled_dx < scaled_dy * 1.5:
        raise RuntimeError("未適用のScaleで、Xの面取りがYより広がっていない")
    if abs(applied_dx - applied_dy) > 0.05:
        raise RuntimeError("頂点へ焼き込んだ木箱の面取りが、XとYで揃っていない")

    tools.save_blend(BLEND_PATH, scaled_object)


if __name__ == "__main__":
    main()
