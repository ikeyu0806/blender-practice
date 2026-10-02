"""31｜非人体の構造。初期化して観察用ファイルを保存する教材。"""

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

HORN_HEIGHT = 0.6
lesson_scene, assets_collection = tools.start("CreatureStructure")
# 四足、長い尾、左右の角を独立部品で配置する。人物の比率をそのまま使わない。
body_object, head_object, tail_object, tail_rig_object = tools.monster(
    assets_collection, horn_height=HORN_HEIGHT
)
assert (
    len(
        [
            asset_object
            for asset_object in assets_collection.objects
            if asset_object.name.startswith("Monster.Leg.")
        ]
    )
    == 4
)
assert tail_object.modifiers["Deform"].object is tail_rig_object
body_object["structure"] = "quadruped; separate horns and tail"
print("legs: 4; horns: 2; tail: separate weighted Mesh")
tools.studio(lesson_scene, span=7, target=(0, 0.5, 1))
tools.active(tail_object)
tools.finish(lesson_scene, assets_collection, "31_creature_structure")
