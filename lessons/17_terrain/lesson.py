"""17｜地形と地面。初期化して観察用ファイルを保存する教材。"""

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

HILL_HEIGHT = 1.0
GRID_STEPS = 16
lesson_scene, assets_collection = tools.start("Terrain")
ground_material = tools.material("Surface.Earth", (0.22, 0.32, 0.14))
vertices = []
for j in range(GRID_STEPS + 1):
    y = -4 + 8 * j / GRID_STEPS
    for i in range(GRID_STEPS + 1):
        x = -4 + 8 * i / GRID_STEPS
        # 通路の近くでは高さを抑え、歩く場所と丘を分ける。
        path_factor = min(1, abs(x) / 1.5)
        z = HILL_HEIGHT * path_factor * (0.5 + 0.5 * sin(x * 0.8) * cos(y * 0.6))
        vertices.append((x, y, z))
faces = []
for j in range(GRID_STEPS):
    for i in range(GRID_STEPS):
        a = j * (GRID_STEPS + 1) + i
        faces.append((a, a + 1, a + GRID_STEPS + 2, a + GRID_STEPS + 1))
terrain_object = tools.mesh_object(
    "Terrain.Grid", vertices, faces, assets_collection, ground_material
)
assert all(
    abs(vertex.co.z) < 1e-6
    for vertex in terrain_object.data.vertices
    if abs(vertex.co.x) < 1e-6
)
assert all(polygon.normal.z > 0 for polygon in terrain_object.data.polygons)
print("grid:", len(vertices), "vertices /", len(faces), "faces; path x=0 is flat")
tools.studio(lesson_scene, span=10)
tools.active(terrain_object)
terrain_object.show_wire = True
tools.finish(lesson_scene, assets_collection, "17_terrain")
