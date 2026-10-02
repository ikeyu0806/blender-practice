"""11｜法線と面の向き。初期化して観察用ファイルを保存する教材。"""

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

SMOOTH_SIDE = True
lesson_scene, assets_collection = tools.start("NormalsShading")
stone_material = tools.material("Surface.Stone", (0.3, 0.5, 0.55))
flat_object = tools.cone(
    "Pillar.Flat", 0.6, 0.6, 1.8, (-1, 0, 0.9), assets_collection, stone_material
)
smooth_object = tools.cone(
    "Pillar.SmoothSides", 0.6, 0.6, 1.8, (1, 0, 0.9), assets_collection, stone_material
)
# 法線の表裏と、隣接面の陰影を補間する設定は別。
# 水平な蓋はflatに残すことで、縁を丸い面のように見せない。
for polygon in smooth_object.data.polygons:
    polygon.use_smooth = SMOOTH_SIDE and abs(polygon.normal.z) < 0.5
assert len(flat_object.data.vertices) == len(smooth_object.data.vertices)
assert all(
    polygon.normal.dot(polygon.center) > 0 for polygon in smooth_object.data.polygons
)
print(
    "smooth faces:", sum(polygon.use_smooth for polygon in smooth_object.data.polygons)
)
print(
    "flat and smooth vertices:",
    len(flat_object.data.vertices),
    len(smooth_object.data.vertices),
)
tools.active(smooth_object)
tools.studio(lesson_scene, span=4)
tools.finish(lesson_scene, assets_collection, "11_normals_shading")
