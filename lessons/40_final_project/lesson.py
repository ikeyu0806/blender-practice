"""40｜最終制作。初期化して観察用ファイルを保存する教材。"""
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

CHARACTER_X = -1.8
lesson_scene, assets_collection=tools.start("FinalProject")
# 各カテゴリの所有Collectionを分け、形とリグの依存関係を保ったまま配置する。
character_collection=bpy.data.collections.new("Final.Character")
monster_collection=bpy.data.collections.new("Final.Monster")
environment_collection=bpy.data.collections.new("Final.Environment")
for category_collection in (character_collection,monster_collection,environment_collection):
    assets_collection.children.link(category_collection)
body_object,head_object,limb_rigs=tools.humanoid(character_collection)
monster_body,monster_head,tail_object,tail_rig_object=tools.monster(monster_collection)
tools.room(environment_collection)
for category_collection,offset in [(character_collection,(CHARACTER_X,-1.2,0)),(monster_collection,(1.1,0.2,0))]:
    # MeshとRigを同じoffsetで動かす。片方だけ移動すると変形の基準がずれる。
    for asset_object in category_collection.objects:
        asset_object.location+=Vector(offset)
for asset_object in assets_collection.all_objects:
    if asset_object.type=="MESH":
        tools.uv_smart(asset_object)
        assert all(abs(value-1)<1e-5 for value in asset_object.scale)
        assert asset_object.data.materials
lesson_scene.frame_set(1)
neutral_arm=tools.evaluated_coordinates(bpy.data.objects["Character.Arm.-1"])
neutral_tail=tools.evaluated_coordinates(tail_object)
lesson_scene.frame_set(24)
pose_arm=tools.evaluated_coordinates(bpy.data.objects["Character.Arm.-1"])
pose_tail=tools.evaluated_coordinates(tail_object)
assert max((a-b).length for a,b in zip(neutral_arm,pose_arm))>0.1
assert max((a-b).length for a,b in zip(neutral_tail,pose_tail))>0.1
print("final categories:",[category_collection.name for category_collection in assets_collection.children])
print("validation: scale=1, UV, material, arm and tail deformation OK")
tools.studio(lesson_scene,span=9,target=(0,0,1.3),camera_location=(8,-11,11))
tools.active(body_object)
tools.finish(lesson_scene,assets_collection,"40_final_project",render=True)
