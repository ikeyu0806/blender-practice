"""23｜人体の大きな比率。初期化して観察用ファイルを保存する教材。"""

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

HEAD_UNIT = 0.45
lesson_scene, assets_collection = tools.start("BodyProportions")
skin_material = tools.material("Character.Skin", (0.6, 0.35, 0.22))
# デフォルメの6頭身。頭1個の高さを基準に、位置と寸法をまとめて決める。
head_object = tools.sphere(
    "Body.Head",
    (HEAD_UNIT * 0.9, HEAD_UNIT * 0.85, HEAD_UNIT),
    (0, 0, HEAD_UNIT * 5.5),
    assets_collection,
    skin_material,
)
tools.box(
    "Body.Torso",
    (HEAD_UNIT * 1.6, HEAD_UNIT * 0.8, HEAD_UNIT * 1.8),
    (0, 0, HEAD_UNIT * 3.9),
    assets_collection,
    skin_material,
)
tools.box(
    "Body.Pelvis",
    (HEAD_UNIT * 1.5, HEAD_UNIT * 0.85, HEAD_UNIT * 0.7),
    (0, 0, HEAD_UNIT * 2.65),
    assets_collection,
    skin_material,
)
for side in (-1, 1):
    for name, z, height, width, x in [
        ("Thigh", 1.8, 1.0, 0.6, 0.4),
        ("Shin", 0.8, 1.0, 0.45, 0.4),
        ("UpperArm", 4.0, 0.9, 0.4, 1.1),
        ("Forearm", 3.1, 0.9, 0.3, 1.1),
    ]:
        tools.box(
            f"Body.{name}.{side}",
            (HEAD_UNIT * width, HEAD_UNIT * 0.6, HEAD_UNIT * height),
            (side * HEAD_UNIT * x, 0, z * HEAD_UNIT),
            assets_collection,
            skin_material,
        )
    tools.box(
        f"Body.Foot.{side}",
        (HEAD_UNIT * 0.55, HEAD_UNIT, HEAD_UNIT * 0.3),
        (side * HEAD_UNIT * 0.4, -HEAD_UNIT * 0.2, HEAD_UNIT * 0.15),
        assets_collection,
        skin_material,
    )
assert len(assets_collection.objects) == 13
assert abs(head_object.dimensions.z - HEAD_UNIT) < 1e-5
print("head unit:", HEAD_UNIT, "top of head:", HEAD_UNIT * 6)
camera_object = tools.studio(
    lesson_scene,
    span=5,
    target=(0, 0, HEAD_UNIT * 3),
    camera_location=(0, -8, HEAD_UNIT * 3),
)
camera_object.data.type = "ORTHO"
camera_object.data.ortho_scale = 4
tools.active(head_object)
tools.finish(lesson_scene, assets_collection, "23_body_proportions")
