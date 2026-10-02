"""35｜再実行可能な生成スクリプト。初期化して観察用ファイルを保存する教材。"""

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

ASSET_COUNT = 4
lesson_scene, assets_collection = tools.start("RepeatableGeneration")
keep_object = bpy.data.objects.new("Keep.Unrelated", None)
lesson_scene.collection.objects.link(keep_object)


def generate_assets():
    # 制作ツールは自分の所属先だけを掃除する。Scene全体を消す処理と区別する。
    for generated_object in list(assets_collection.objects):
        generated_mesh = generated_object.data
        bpy.data.objects.remove(generated_object, do_unlink=True)
        if generated_mesh and generated_mesh.users == 0:
            bpy.data.meshes.remove(generated_mesh)
    shared_material = bpy.data.materials.get("Generated.Surface")
    if shared_material is None:
        shared_material = tools.material("Generated.Surface", (0.28, 0.4, 0.25))
    for i in range(ASSET_COUNT):
        tools.box(
            f"Generated.Crate.{i:02}",
            (0.8, 0.8, 0.8),
            (i - 1.5, 0, 0.4),
            assets_collection,
            shared_material,
        )
    bpy.context.view_layer.update()
    return [
        (
            asset_object.name,
            asset_object.data.name,
            tuple(asset_object.location),
            tuple(asset_object.dimensions),
        )
        for asset_object in sorted(
            assets_collection.objects, key=lambda asset_object: asset_object.name
        )
    ]


first_snapshot = generate_assets()
first_mesh_count = len(bpy.data.meshes)
second_snapshot = generate_assets()
assert first_snapshot == second_snapshot
assert len(bpy.data.meshes) == first_mesh_count
assert bpy.data.objects.get("Keep.Unrelated") is keep_object
assert len(assets_collection.objects) == ASSET_COUNT
print(
    "two runs identical:",
    first_snapshot,
    "unrelated object preserved:",
    keep_object.name,
)
tools.studio(lesson_scene, span=6)
tools.finish(lesson_scene, assets_collection, "35_repeatable_generation")
