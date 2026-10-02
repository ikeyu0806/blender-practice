"""21｜背景の小作品。初期化して観察用ファイルを保存する教材。"""

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

PROP_SPACING = 1.7
lesson_scene, assets_collection = tools.start("EnvironmentProject")
tools.room(assets_collection)
crate_object, rock_object, barrel_object = tools.prop_set(
    assets_collection, PROP_SPACING
)
# 出入口は中央y=-3。小物を中景へ置き、入口からの視線を確保する。
for asset_object in list(assets_collection.objects):
    if asset_object.name.startswith("Prop."):
        asset_object.location.y += 0.8
crate_object["role"] = "storage"
rock_object["role"] = "floor detail"
assert not any(
    abs(asset_object.location.x) < 0.7 and asset_object.location.y < -2
    for asset_object in assets_collection.objects
    if asset_object.name.startswith("Prop.")
)
print("room floors:", 9, "props:", 5, "entrance clearance: OK")
tools.studio(lesson_scene, span=8, target=(0, 0, 1), camera_location=(8, -10, 10))
tools.active(crate_object)
tools.finish(lesson_scene, assets_collection, "21_environment_project", render=True)
