"""32｜Sculptとリトポロジー。初期化して観察用ファイルを保存する教材。"""

from pathlib import Path
import sys
from math import sin, cos, pi, radians
import bmesh
import bpy
from mathutils import Vector

# --pythonと、保存済みText EditorのRun Scriptの両方で教材の場所を解決する。
source_path = globals().get("__file__")
if not source_path:
    lesson_text = getattr(bpy.context.space_data, "text", None)
    if not lesson_text or not lesson_text.filepath:
        raise RuntimeError("lesson.pyを保存してから実行してください")
    source_path = bpy.path.abspath(lesson_text.filepath)
support_path = Path(source_path).resolve().parents[1] / "_support"
if str(support_path) not in sys.path:
    sys.path.insert(0, str(support_path))
import scene_tools as tools

BULGE = 0.14
lesson_scene, assets_collection = tools.start("SculptRetopology")
clay_material = tools.material("Surface.Clay", (0.37, 0.22, 0.13))
high_object = tools.sphere(
    "Sculpt.High", (2, 1.6, 2), (0, 0, 1.2), assets_collection, clay_material, 64, 32
)
# ブラシで盛ったような高密度の例を再現可能な数式で用意する。
# これは自動Sculptや自動Retopologyではなく、手作業の開始形状。
for vertex in high_object.data.vertices:
    scale = 1 + BULGE * sin(vertex.co.x * 5) * cos(vertex.co.z * 4)
    vertex.co *= scale
high_object.data.update()
low_object = tools.sphere(
    "Retopo.Low", (2.3, 1.9, 2.3), (0, 0, 1.2), assets_collection, clay_material, 12, 8
)
shrinkwrap_modifier = low_object.modifiers.new("ProjectToSculpt", "SHRINKWRAP")
shrinkwrap_modifier.target = high_object
shrinkwrap_modifier.wrap_method = "NEAREST_SURFACEPOINT"
shrinkwrap_modifier.offset = 0.01
projected_coordinates = tools.evaluated_coordinates(low_object)
assert len(low_object.data.vertices) < len(high_object.data.vertices) / 5
assert (
    max(
        (vertex.co - coordinates).length
        for vertex, coordinates in zip(low_object.data.vertices, projected_coordinates)
    )
    > 0.02
)
print(
    "high / low vertices:",
    len(high_object.data.vertices),
    len(low_object.data.vertices),
)
# 投影をMeshへ確定してから左右へ並べる。投影前のMeshはoutput JSONではなく
# 元のlesson.pyのsphere定義に残る。適用後も高密度の元モデルは保持する。
tools.active(low_object)
bpy.ops.object.modifier_apply(modifier=shrinkwrap_modifier.name)
high_object.location.x = -1.4
low_object.location.x = 1.4
low_object.show_wire = True
tools.studio(lesson_scene, span=7, target=(0, 0, 1.2))
tools.active(low_object)
tools.finish(lesson_scene, assets_collection, "32_sculpt_retopology")
