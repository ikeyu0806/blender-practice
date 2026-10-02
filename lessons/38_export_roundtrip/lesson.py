"""38｜書き出しと再取り込み。初期化して観察用ファイルを保存する教材。"""
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

EXPORT_OFFSET = 12.0
lesson_scene, assets_collection=tools.start("ExportRoundtrip")
# 人物・モンスター・背景の3種類を作り、評価した静止Meshへ焼き出して渡す。
character_collection=bpy.data.collections.new("Source.Character")
monster_collection=bpy.data.collections.new("Source.Monster")
environment_collection=bpy.data.collections.new("Source.Environment")
for source_collection in (character_collection,monster_collection,environment_collection):
    lesson_scene.collection.children.link(source_collection)
tools.humanoid(character_collection)
tools.monster(monster_collection)
tools.room(environment_collection)
for source_collection,offset in [(character_collection,(-3,-1,0)),(monster_collection,(3,-1,0)),(environment_collection,(0,5,0))]:
    for source_object in source_collection.objects:
        source_object.location+=Vector(offset)
lesson_scene.frame_set(24)
bpy.context.view_layer.update()
dependency_graph=bpy.context.evaluated_depsgraph_get()
export_objects=[]
for source_collection in (character_collection,monster_collection,environment_collection):
    for source_object in source_collection.objects:
        if source_object.type!="MESH": continue
        evaluated_object=source_object.evaluated_get(dependency_graph)
        export_mesh=bpy.data.meshes.new_from_object(evaluated_object,preserve_all_data_layers=True,depsgraph=dependency_graph)
        export_mesh.name="Export."+source_object.name+".Mesh"
        export_object=bpy.data.objects.new("Export."+source_object.name,export_mesh)
        assets_collection.objects.link(export_object)
        export_object.matrix_world=source_object.matrix_world.copy()
        if not export_mesh.uv_layers:
            tools.uv_smart(export_object)
        export_objects.append(export_object)
# 元のリグや部品はファイルに保持するが、比較画面では非表示。
for source_collection in (character_collection,monster_collection,environment_collection):
    source_collection.hide_viewport=True
    source_collection.hide_render=True
bpy.ops.object.select_all(action="DESELECT")
for export_object in export_objects: export_object.select_set(True)
bpy.context.view_layer.objects.active=export_objects[0]
glb_path=tools.OUTPUT/"38_assets.glb"
bpy.ops.export_scene.gltf(filepath=str(glb_path),export_format="GLB",use_selection=True,
    export_animations=False,export_skins=False,export_morph=False)
objects_before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(glb_path))
imported_objects=[asset_object for asset_object in bpy.data.objects if asset_object not in objects_before and asset_object.type=="MESH"]
assert len(imported_objects)==len(export_objects)

def world_bounds(mesh_objects):
    points=[asset_object.matrix_world@vertex.co for asset_object in mesh_objects for vertex in asset_object.data.vertices]
    return [min(point[axis] for point in points) for axis in range(3)]+[max(point[axis] for point in points) for axis in range(3)]
bpy.context.view_layer.update()
source_bounds=world_bounds(export_objects)
import_bounds=world_bounds(imported_objects)
assert max(abs(a-b) for a,b in zip(source_bounds,import_bounds))<1e-4
assert all(asset_object.data.uv_layers for asset_object in imported_objects)
assert all(asset_object.data.materials for asset_object in imported_objects)
for imported_object in imported_objects:
    # 複雑な階層を持つ取り込みでは、解除前のworld行列を保持してから並べる。
    world_matrix=imported_object.matrix_world.copy()
    imported_object.parent=None
    imported_object.matrix_world=world_matrix
    for old_collection in list(imported_object.users_collection): old_collection.objects.unlink(imported_object)
    assets_collection.objects.link(imported_object)
    imported_object.location.x+=EXPORT_OFFSET
print("GLB round trip: meshes",len(imported_objects),"world bounds equal; UV and Material retained")
tools.studio(lesson_scene,span=23,target=(6,2,1),camera_location=(20,-27,21))
tools.finish(lesson_scene,assets_collection,"38_export_roundtrip")
