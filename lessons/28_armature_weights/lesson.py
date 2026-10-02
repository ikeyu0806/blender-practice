"""28｜Armatureとウェイト。初期化して観察用ファイルを保存する教材。"""
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

BEND_ANGLE = 50
lesson_scene, assets_collection=tools.start("ArmatureWeights")
skin_material=tools.material("Surface.Limb",(0.65,0.34,0.17))
limb_object=tools.tube("Arm.Skinned",[0,0.75,0.9,1,1.1,1.25,2],[0.2]*7,assets_collection,skin_material)
# ヘルパー内部のEdit ModeでLower/UpperのBoneを作り、同名Vertex Groupを割り当てる。
rig_object=tools.two_bone_rig("Rig.Arm",limb_object,1,assets_collection)
rest_coordinates=tools.evaluated_coordinates(limb_object)
upper_pose_bone=rig_object.pose.bones["Upper"]
upper_pose_bone.rotation_euler.x=radians(BEND_ANGLE)
bent_coordinates=tools.evaluated_coordinates(limb_object)
assert max((a-b).length for a,b in zip(rest_coordinates,bent_coordinates))>0.1
assert limb_object.modifiers["Deform"].object is rig_object
for vertex in limb_object.data.vertices:
    total=sum(group.weight for group in vertex.groups)
    assert abs(total-1)<1e-6
    if abs(vertex.co.z-1)<1e-5:
        print("joint vertex",vertex.index,"weights:",[(limb_object.vertex_groups[group.group].name,round(group.weight,2)) for group in vertex.groups])
print("bones:",list(rig_object.data.bones.keys()),"pose angle:",BEND_ANGLE)
tools.studio(lesson_scene,span=4,target=(0,0,1))
tools.active(rig_object)
tools.finish(lesson_scene,assets_collection,"28_armature_weights")
