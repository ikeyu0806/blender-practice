"""36｜依存関係と評価結果。初期化して観察用ファイルを保存する教材。"""
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

X_SCALE = 1.4
lesson_scene, assets_collection=tools.start("DependencyEvaluation")
stone_material=tools.material("Surface.Stone",(0.25,0.43,0.48))
source_object=tools.box("Asset.Source",(1,1,1),(-1.2,0,0.5),assets_collection,stone_material)
evaluated_view_object=bpy.data.objects.new("Asset.Evaluated",source_object.data)
assets_collection.objects.link(evaluated_view_object)
evaluated_view_object.location=(1.2,0,0.5)
# Geometry Nodesの入出力とTransformノードを接続する。
geometry_node_group=bpy.data.node_groups.new("Geometry.ScaleThenBevel","GeometryNodeTree")
geometry_node_group.interface.new_socket(name="Geometry",in_out="INPUT",socket_type="NodeSocketGeometry")
geometry_node_group.interface.new_socket(name="Geometry",in_out="OUTPUT",socket_type="NodeSocketGeometry")
input_node=geometry_node_group.nodes.new("NodeGroupInput")
transform_node=geometry_node_group.nodes.new("GeometryNodeTransform")
output_node=geometry_node_group.nodes.new("NodeGroupOutput")
input_node.location=(-250,0)
output_node.location=(250,0)
transform_node.inputs["Scale"].default_value=(X_SCALE,1,1)
geometry_node_group.links.new(input_node.outputs["Geometry"],transform_node.inputs["Geometry"])
geometry_node_group.links.new(transform_node.outputs["Geometry"],output_node.inputs["Geometry"])
nodes_modifier=evaluated_view_object.modifiers.new("01.GeometryScale","NODES")
nodes_modifier.node_group=geometry_node_group
bevel_modifier=evaluated_view_object.modifiers.new("02.Bevel","BEVEL")
bevel_modifier.width,bevel_modifier.segments=0.08,2
coordinates=tools.evaluated_coordinates(evaluated_view_object)
evaluated_width=max(co.x for co in coordinates)-min(co.x for co in coordinates)
assert len(source_object.data.vertices)==8
assert len(coordinates)>8
assert abs(evaluated_width-X_SCALE)<1e-5
assert evaluated_view_object.data is source_object.data
print("source vertices:",8,"evaluated vertices:",len(coordinates),"evaluated width:",round(evaluated_width,3))
tools.studio(lesson_scene,span=5)
tools.active(evaluated_view_object)
tools.finish(lesson_scene,assets_collection,"36_dependency_evaluation")
