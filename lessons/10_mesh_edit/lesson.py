"""10｜メッシュ編集の基本。初期化して観察用ファイルを保存する教材。"""
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

EXTRUDE_HEIGHT = 0.7
lesson_scene, assets_collection = tools.start("MeshEdit")
stone_material = tools.material("Surface.Stone", (0.32,0.42,0.45))
source_object = tools.box("Tower.Before",(1,1,1),(-1,0,0.5),assets_collection,stone_material)
# 元Meshをcopy()するので、右の編集は左には伝わらない。
edited_mesh = source_object.data.copy()
edited_mesh.name = "Tower.After.Mesh"
edited_object = bpy.data.objects.new("Tower.After",edited_mesh)
assets_collection.objects.link(edited_object)
edited_object.location = (1,0,0.5)
edit_bmesh = bmesh.new()
edit_bmesh.from_mesh(edited_mesh)
edit_bmesh.normal_update()
top_face = max(edit_bmesh.faces, key=lambda face: face.calc_center_median().z)
# UIのFace Select→Extrude Regionに対応。新しい頂点だけを移動する。
extrusion = bmesh.ops.extrude_face_region(edit_bmesh,geom=[top_face])
new_vertices = [element for element in extrusion["geom"] if isinstance(element,bmesh.types.BMVert)]
bmesh.ops.translate(edit_bmesh,verts=new_vertices,vec=(0,0,EXTRUDE_HEIGHT))
# 内側に残る元の上面を除き、閉じた表面を保つ。
if top_face.is_valid:
    bmesh.ops.delete(edit_bmesh,geom=[top_face],context="FACES_ONLY")
# 全辺の中点で分割し、側面に連続したリングを追加する。
# Ctrl+Rの1本のLoop Cutとは異なり、このAPI操作は全辺を分割する。
bmesh.ops.subdivide_edges(edit_bmesh,edges=list(edit_bmesh.edges),cuts=1,use_grid_fill=True)
bmesh.ops.recalc_face_normals(edit_bmesh,faces=list(edit_bmesh.faces))
assert all(edge.is_manifold for edge in edit_bmesh.edges)
edit_bmesh.to_mesh(edited_mesh)
edit_bmesh.free()
edited_mesh.update()
assert len(edited_mesh.vertices)>len(source_object.data.vertices)
assert abs(max(vertex.co.z for vertex in edited_mesh.vertices)-0.5-EXTRUDE_HEIGHT)<1e-5
print("before / after vertices:",len(source_object.data.vertices),len(edited_mesh.vertices))
edited_object.show_wire = True
for polygon in edited_mesh.polygons:
    polygon.select = polygon.normal.z > 0.9
tools.active(edited_object)
tools.studio(lesson_scene,span=4)
tools.finish(lesson_scene,assets_collection,"10_mesh_edit")
