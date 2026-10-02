"""22｜Blender → Unity。初期化して観察用ファイルを保存する教材。"""

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

EXPORT_SCALE = 1.0
lesson_scene, assets_collection = tools.start("UnityFBX")
wood_material = tools.material("Surface.Wood", (0.38, 0.18, 0.06))
crate_object = tools.box(
    "Export.Crate", (1, 1, 1), (0, 0, 0.5), assets_collection, wood_material
)
# 地面接触位置に原点を置く。Meshを上へずらし、ObjectのLocationを0にする。
for vertex in crate_object.data.vertices:
    vertex.co.z += 0.5
crate_object.location.z = 0
crate_object.data.update()
tools.uv_smart(crate_object)
# 21の背景と同じ床・壁・小物も含め、1mの箱を寸法確認の基準にする。
tools.room(assets_collection)
tools.prop_set(assets_collection)
source_objects = list(assets_collection.objects)
for source_object in source_objects:
    tools.uv_smart(source_object)
bpy.ops.object.select_all(action="DESELECT")
for source_object in source_objects:
    source_object.select_set(True)
bpy.context.view_layer.objects.active = crate_object
fbx_path = tools.OUTPUT / "22_crate.fbx"
bpy.ops.export_scene.fbx(
    filepath=str(fbx_path),
    use_selection=True,
    object_types={"MESH"},
    global_scale=EXPORT_SCALE,
    apply_unit_scale=True,
    apply_scale_options="FBX_SCALE_ALL",
    axis_forward="-Z",
    axis_up="Y",
    add_leaf_bones=False,
    bake_anim=False,
)
# 同じBlenderへ再取り込みし、Unityへ渡す前に形と寸法を検査する。
# この検査はUnity側のImporterを実行するものではない。
objects_before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=str(fbx_path))
imported_objects = [
    asset_object
    for asset_object in bpy.data.objects
    if asset_object not in objects_before and asset_object.type == "MESH"
]
assert len(imported_objects) == len(source_objects)
imported_object = next(
    candidate_object
    for candidate_object in imported_objects
    if candidate_object.name.startswith("Export.Crate")
)
for candidate_object in imported_objects:
    for old_collection in list(candidate_object.users_collection):
        old_collection.objects.unlink(candidate_object)
    assets_collection.objects.link(candidate_object)
imported_object.name = "Import.Crate"
bpy.context.view_layer.update()
assert max(abs(value - EXPORT_SCALE) for value in imported_object.dimensions) < 1e-4
assert imported_object.data.uv_layers.active is not None


def world_bounds(mesh_objects):
    points = [
        asset_object.matrix_world @ vertex.co
        for asset_object in mesh_objects
        for vertex in asset_object.data.vertices
    ]
    return [min(point[axis] for point in points) for axis in range(3)] + [
        max(point[axis] for point in points) for axis in range(3)
    ]


source_bounds = world_bounds(source_objects)
import_bounds = world_bounds(imported_objects)
assert (
    max(
        abs(actual - expected * EXPORT_SCALE)
        for actual, expected in zip(import_bounds, source_bounds)
    )
    < 1e-4
)
assert all(candidate_object.data.materials for candidate_object in imported_objects)
print("FBX background bounds and material slots: OK")
# Xへ移動するのは検査の後。保存シーンでは左右に元と再取り込みを並べる。
for source_object in source_objects:
    source_object.location.x -= 5
for candidate_object in imported_objects:
    candidate_object.location.x += 5
assert all(
    candidate_object.data.uv_layers.active is not None
    for candidate_object in imported_objects
)
print(
    "FBX round trip dimensions:", tuple(imported_object.dimensions), "path:", fbx_path
)
tools.studio(lesson_scene, span=16, target=(0, 0, 1))
tools.active(imported_object)
tools.finish(lesson_scene, assets_collection, "22_unity_fbx")
