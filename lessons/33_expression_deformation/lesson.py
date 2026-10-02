"""33｜変形と表情。初期化して観察用ファイルを保存する教材。"""

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

EXPRESSION_VALUE = 1.0
lesson_scene, assets_collection = tools.start("ExpressionDeformation")
body_object, head_object, tail_object, tail_rig_object = tools.monster(
    assets_collection
)
lesson_scene.frame_set(1)
neutral_head = tools.evaluated_coordinates(head_object)
neutral_tail = tools.evaluated_coordinates(tail_object)
lesson_scene.frame_set(24)
mouth_shape_key = head_object.data.shape_keys.key_blocks["JawDrop"]
mouth_shape_key.value = EXPRESSION_VALUE
# 同じフレームのキーも更新し、再読み込み後に値がアニメーションで戻らないようにする。
mouth_shape_key.keyframe_insert("value", frame=24)
expressive_head = tools.evaluated_coordinates(head_object)
bent_tail = tools.evaluated_coordinates(tail_object)
assert len(neutral_head) == len(expressive_head)
assert max((a - b).length for a, b in zip(neutral_tail, bent_tail)) > 0.1
if EXPRESSION_VALUE > 0:
    assert max((a - b).length for a, b in zip(neutral_head, expressive_head)) > 0.01
print(
    "JawDrop:",
    mouth_shape_key.value,
    "head vertices:",
    len(expressive_head),
    "tail bending: OK",
)
tools.studio(lesson_scene, span=7, target=(0, 0.5, 1))
tools.active(head_object)
tools.finish(lesson_scene, assets_collection, "33_expression_deformation")
