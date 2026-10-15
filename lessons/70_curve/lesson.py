"""70｜Curve。平らな尾の頂点を、Bezier曲線の評価後の形へ沿わせる。"""

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

# 曲線の途中を持ち上げる高さ。尾の評価後のZはこの値に近づく。
ARC_HEIGHT = 0.8
BLEND_PATH = ROOT / "output" / "70_curve.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Curve")
    vertices = []
    for index in range(8):
        vertices.append((index * 0.25, -0.05, 0.0))
        vertices.append((index * 0.25, 0.05, 0.0))
    faces = [(index * 2, index * 2 + 1, index * 2 + 3, index * 2 + 2) for index in range(7)]
    tail_object = tools.mesh_from_pydata(
        "Monster.Tail", modifiers_collection, vertices, [], faces
    )
    curve_data = bpy.data.curves.new("Tail.Path", "CURVE")
    curve_data.dimensions = "3D"
    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(2)
    for point, coordinate in zip(
        spline.bezier_points,
        [(0.0, 0.0, 0.0), (1.0, 0.0, ARC_HEIGHT), (2.0, 0.0, 0.0)],
    ):
        point.co = coordinate
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    path_object = bpy.data.objects.new("Tail.Path", curve_data)
    modifiers_collection.objects.link(path_object)

    curve_modifier = tail_object.modifiers.new("FollowPath", "CURVE")
    curve_modifier.object = path_object
    # 尾の長さ方向は元Meshの+X。曲線もその軸に沿って変形する。
    curve_modifier.deform_axis = "POS_X"

    evaluated = tools.evaluated_snapshot(tail_object)
    source_max_z = max(vertex.co.z for vertex in tail_object.data.vertices)
    evaluated_max_z = max(position.z for position in evaluated.positions)

    print("=== 70 curve ===")
    print(f"arc={ARC_HEIGHT} source max z={source_max_z:.3f} evaluated max z={evaluated_max_z:.3f}")

    if source_max_z > 1e-6:
        raise RuntimeError("尾の元Meshが平らではない")
    if evaluated_max_z < 0.2:
        raise RuntimeError("評価後の尾が曲線の高さへ乗っていない")

    tools.save_blend(BLEND_PATH, tail_object)


if __name__ == "__main__":
    main()
