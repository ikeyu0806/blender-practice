"""16｜モジュラー背景。初期化して観察用ファイルを保存する教材。"""
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

MODULE_SIZE = 2.0
lesson_scene, assets_collection = tools.start("ModularRoom")
lintel_object = tools.room(assets_collection,MODULE_SIZE)
# 接続規則を数値でも確認。床中心の間隔と幅が等しいので継ぎ目に隙間がない。
floor_objects = [asset_object for asset_object in assets_collection.objects if ".Floor." in asset_object.name]
assert len(floor_objects)==9
assert all(abs(asset_object.dimensions.x-MODULE_SIZE)<1e-5 for asset_object in floor_objects)
print("floor tiles:",len(floor_objects),"grid spacing:",MODULE_SIZE,"room width:",3*MODULE_SIZE)
tools.studio(lesson_scene,span=9,target=(0,0,1))
tools.active(lintel_object)
tools.finish(lesson_scene,assets_collection,"16_modular_room")
