"""19｜照明と色。初期化して観察用ファイルを保存する教材。"""
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

FILL_ENERGY = 600
lesson_scene, assets_collection = tools.start("Lighting")
crate_object, rock_object, barrel_object = tools.prop_set(assets_collection)
tools.studio(lesson_scene,span=6)
fill_light = bpy.data.lights["Presentation.Fill.Data"]
fill_light.energy = FILL_ENERGY
# 同じMeshとCameraを使い、光だけを変えた2枚を出す。
fill_object=bpy.data.objects["Presentation.Fill"]
rim_object=bpy.data.objects["Presentation.Rim"]
fill_object.hide_render=True
rim_object.hide_render=True
background_node=lesson_scene.world.node_tree.nodes["Background"]
background_node.inputs["Strength"].default_value=0
lesson_scene.render.filepath=str(tools.OUTPUT/"19_key_only.png")
bpy.ops.render.render(write_still=True)
fill_object.hide_render=False
rim_object.hide_render=False
background_node.inputs["Strength"].default_value=0.3
assert fill_light.energy==FILL_ENERGY
print("key / fill / world:",1200,FILL_ENERGY,0.3)
tools.active(crate_object)
tools.finish(lesson_scene,assets_collection,"19_lighting",render=True)
