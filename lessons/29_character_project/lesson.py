"""29｜人物の小作品。初期化して観察用ファイルを保存する教材。"""
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

HEAD_SIZE = 0.65
lesson_scene, assets_collection=tools.start("CharacterProject")
body_object,head_object,limb_rigs=tools.humanoid(assets_collection,HEAD_SIZE)
# UVをそろえた低ポリの分割人物。4つの局所リグで肘と膝を独立に観察する。
for asset_object in list(assets_collection.objects):
    if asset_object.type=="MESH":
        tools.uv_smart(asset_object)
assert len(limb_rigs)==4
arm_object=bpy.data.objects["Character.Arm.-1"]
lesson_scene.frame_set(1)
neutral_coordinates=tools.evaluated_coordinates(arm_object)
lesson_scene.frame_set(24)
pose_coordinates=tools.evaluated_coordinates(arm_object)
assert max((a-b).length for a,b in zip(neutral_coordinates,pose_coordinates))>0.1
tools.studio(lesson_scene,span=6,target=(0,0,1.8))
lesson_scene.frame_set(1)
lesson_scene.render.filepath=str(tools.OUTPUT/"29_neutral.png")
bpy.ops.render.render(write_still=True)
lesson_scene.frame_set(24)
print("neutral frame: 1; pose frame: 24; limb rigs:",len(limb_rigs))
tools.active(body_object)
tools.finish(lesson_scene,assets_collection,"29_character_project",render=True)
