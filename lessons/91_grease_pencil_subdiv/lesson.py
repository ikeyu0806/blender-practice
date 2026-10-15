"""91｜Grease Pencil Subdivide。線の元の点は2つのまま、評価後の点だけ増やす。

Grease Pencil ObjectのModifierは、Meshの頂点ではなくストロークの点に働く。
同じAdd Modifierメニューでも、Objectの種類で並ぶ項目が違う。
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

# 細分化の段数。1段で線の途中に点が足され、2段でさらに増える。
SUBDIV_LEVEL = 1
BLEND_PATH = ROOT / "output" / "91_grease_pencil_subdiv.blend"


def stroke_point_count(mark_object: bpy.types.Object, evaluated: bool) -> int:
    """線の点数。evaluatedが真ならModifier計算後のGrease Pencilを読む。"""
    if evaluated:
        bpy.context.view_layer.update()
        dependency_graph = bpy.context.evaluated_depsgraph_get()
        mark_object = mark_object.evaluated_get(dependency_graph)
    drawing = mark_object.data.layers["Line"].frames[0].drawing
    return len(drawing.strokes[0].points)


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("GreasePencil")
    pencil_data = bpy.data.grease_pencils.new("Mark.Pencil")
    mark_object = bpy.data.objects.new("Mark.Stroke", pencil_data)
    modifiers_collection.objects.link(mark_object)
    layer = pencil_data.layers.new("Line")
    frame = layer.frames.new(1)
    frame.drawing.add_strokes([2])
    stroke = frame.drawing.strokes[0]
    stroke.points[0].position = (0.0, 0.0, 0.0)
    stroke.points[1].position = (1.0, 0.0, 0.4)

    subdiv_modifier = mark_object.modifiers.new("SmoothLine", "GREASE_PENCIL_SUBDIV")
    subdiv_modifier.level = SUBDIV_LEVEL
    source_points = stroke_point_count(mark_object, evaluated=False)
    evaluated_points = stroke_point_count(mark_object, evaluated=True)

    print("=== 91 grease pencil subdivide ===")
    print(f"level={SUBDIV_LEVEL} source points={source_points} evaluated={evaluated_points}")

    if mark_object.type != "GREASEPENCIL":
        raise RuntimeError("ObjectがGrease Pencilではない")
    if source_points != 2:
        raise RuntimeError("元の線が2点ではない")
    if evaluated_points <= source_points:
        raise RuntimeError("評価後の点が増えていない")

    tools.save_blend(BLEND_PATH, mark_object)


if __name__ == "__main__":
    main()
