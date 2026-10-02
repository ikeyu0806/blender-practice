"""30｜生物のシルエット。初期化して観察用ファイルを保存する教材。"""
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

HORN_HEIGHT = 0.7
lesson_scene, assets_collection=tools.start("CreatureSilhouette")
dark_material=tools.material("Monster.Silhouette",(0.035,0.04,0.035))
for name,x,width,height in [("Tank",-2,1.5,1.0),("Scout",0,0.65,1.8),("Guardian",2,1.1,1.3)]:
    tools.sphere("Concept.Body."+name,(width,0.7,height),(x,0,height/2+0.3),assets_collection,dark_material)
    tools.sphere("Concept.Head."+name,(width*0.6,0.6,0.5),(x,-0.1,height+0.45),assets_collection,dark_material)
    for side in (-1,1):
        tools.cone(f"Concept.Horn.{name}.{side}",0.13,0,HORN_HEIGHT,(x+side*width*0.25,0,height+0.7+HORN_HEIGHT/2),assets_collection,dark_material)
        tools.box(f"Concept.Leg.{name}.{side}",(0.2,0.3,0.4),(x+side*width*0.25,0,0.2),assets_collection,dark_material)
assert len(assets_collection.objects)==18
print("concepts: Tank / Scout / Guardian; horn height:",HORN_HEIGHT)
camera_object=tools.studio(lesson_scene,span=7,target=(0,0,1.5),camera_location=(0,-12,1.5))
camera_object.data.type="ORTHO"
camera_object.data.ortho_scale=7
tools.finish(lesson_scene,assets_collection,"30_creature_silhouette")
