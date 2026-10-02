"""24｜顔と髪のブロックアウト。初期化して観察用ファイルを保存する教材。"""
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

NOSE_DEPTH = 0.24
lesson_scene, assets_collection=tools.start("FaceHair")
skin_material=tools.material("Face.Skin",(0.67,0.4,0.25))
hair_material=tools.material("Face.Hair",(0.045,0.025,0.015))
head_object=tools.sphere("Face.Head",(1,0.8,1.35),(0,0,1.4),assets_collection,skin_material)
tools.box("Face.Jaw",(0.62,0.57,0.35),(0,-0.04,0.89),assets_collection,skin_material)
tools.box("Face.Nose",(0.16,NOSE_DEPTH,0.28),(0,-0.4-NOSE_DEPTH/2,1.35),assets_collection,skin_material)
for side in (-1,1):
    tools.sphere(f"Face.Ear.{side}",(0.16,0.23,0.35),(side*0.51,0,1.4),assets_collection,skin_material)
    tools.box(f"Hair.Side.{side}",(0.15,0.78,0.8),(side*0.48,0.07,1.61),assets_collection,hair_material)
tools.sphere("Hair.Cap",(1.09,0.89,0.65),(0,0.05,1.97),assets_collection,hair_material)
tools.box("Hair.Fringe",(0.82,0.18,0.22),(0,-0.37,1.83),assets_collection,hair_material)
assert head_object.data is not bpy.data.objects["Hair.Cap"].data
print("nose forward tip y:",-0.4-NOSE_DEPTH,"hair objects:",4)
tools.studio(lesson_scene,span=4,target=(0,0,1.4))
tools.active(head_object)
tools.finish(lesson_scene,assets_collection,"24_face_hair")
