"""34｜モンスターの小作品。初期化して観察用ファイルを保存する教材。"""
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

HORN_HEIGHT = 0.6
lesson_scene, assets_collection=tools.start("MonsterProject")
body_object,head_object,tail_object,tail_rig_object=tools.monster(assets_collection,horn_height=HORN_HEIGHT)
for asset_object in list(assets_collection.objects):
    if asset_object.type=="MESH":
        tools.uv_smart(asset_object)
lesson_scene.frame_set(1)
neutral_tail=tools.evaluated_coordinates(tail_object)
tools.studio(lesson_scene,span=7,target=(0,0.5,1),camera_location=(6,-9,6))
lesson_scene.render.filepath=str(tools.OUTPUT/"34_neutral.png")
bpy.ops.render.render(write_still=True)
lesson_scene.frame_set(24)
action_tail=tools.evaluated_coordinates(tail_object)
assert max((a-b).length for a,b in zip(neutral_tail,action_tail))>0.1
assert head_object.data.shape_keys.key_blocks["JawDrop"].value>0.9
print("monster poses: 1 neutral / 24 expression + tail; horns:",HORN_HEIGHT)
tools.active(body_object)
tools.finish(lesson_scene,assets_collection,"34_monster_project",render=True)
