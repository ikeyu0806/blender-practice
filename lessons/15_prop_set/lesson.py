"""15｜小物セット。初期化して観察用ファイルを保存する教材。"""

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

SPACING = 1.8
lesson_scene, assets_collection = tools.start("PropSet")
crate_object, rock_object, barrel_object = tools.prop_set(assets_collection, SPACING)
# 全部品をm単位で作り、原点をObjectの中央に統一する。
# 地面との接触は各Objectの高さの半分をLocation.zへ入れて実現する。
for asset_object in assets_collection.objects:
    assert asset_object.scale == Vector((1, 1, 1))
    assert asset_object.name.startswith("Prop.")
    tools.uv_smart(asset_object)
    print(
        asset_object.name,
        "dimensions:",
        tuple(round(value, 3) for value in asset_object.dimensions),
    )
assert len(assets_collection.objects) == 5
assert crate_object.data is not rock_object.data
assert barrel_object.data.materials[0] is crate_object.data.materials[0]
tools.studio(lesson_scene, span=6)
tools.active(crate_object)
tools.finish(lesson_scene, assets_collection, "15_prop_set")
