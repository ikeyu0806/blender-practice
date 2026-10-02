"""18｜反復配置。初期化して観察用ファイルを保存する教材。"""
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

INSTANCE_COUNT = 5
lesson_scene, assets_collection = tools.start("CollectionInstances")
# 元のCollectionはSceneへ直接所属させない。Instance経由で表示する。
source_collection=bpy.data.collections.new("Source.Pillar")
stone_material=tools.material("Surface.Stone",(0.4,0.46,0.5))
pillar_object=tools.box("Source.Pillar.Body",(0.5,0.5,2),(0,0,1),source_collection,stone_material)
for i in range(INSTANCE_COUNT):
    instance_object=bpy.data.objects.new(f"Instance.Pillar.{i:02}",None)
    assets_collection.objects.link(instance_object)
    instance_object.instance_type="COLLECTION"
    instance_object.instance_collection=source_collection
    instance_object.location=(i*1.4-(INSTANCE_COUNT-1)*0.7,0,0)
# finish()は直接Meshも検査するので、比較用に独立した基台を置く。
tools.box("Display.Base",(INSTANCE_COUNT*1.4,0.9,0.12),(0,0,-0.06),assets_collection,stone_material)
assert sum(asset_object.instance_collection is source_collection for asset_object in assets_collection.objects)==INSTANCE_COUNT
assert pillar_object.data.users==1
print("instances:",INSTANCE_COUNT,"source mesh users:",pillar_object.data.users)
tools.studio(lesson_scene,span=8)
tools.active(bpy.data.objects["Instance.Pillar.00"])
tools.finish(lesson_scene,assets_collection,"18_collection_instances")
