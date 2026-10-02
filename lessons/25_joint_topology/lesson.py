"""25｜関節周辺のトポロジー。初期化して観察用ファイルを保存する教材。"""

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

BEND_ANGLE = 65
lesson_scene, assets_collection = tools.start("JointTopology")
skin_material = tools.material("Surface.Limb", (0.6, 0.32, 0.18))
for name, x, heights in [
    ("Sparse", -1, [0, 1, 2]),
    ("Supported", 1, [0, 0.75, 1, 1.25, 2]),
]:
    limb_object = tools.tube(
        "Limb." + name, heights, [0.2] * len(heights), assets_collection, skin_material
    )
    limb_object.location.x = x
    # 曲げる装置をあらかじめ用意。骨とウェイトそのものは28で詳しく学ぶ。
    rig_object = tools.two_bone_rig(
        "Rig." + name, limb_object, 1, assets_collection, BEND_ANGLE
    )
    limb_object.show_wire = True
    source_coordinates = [vertex.co.copy() for vertex in limb_object.data.vertices]
    bent_coordinates = tools.evaluated_coordinates(limb_object)
    displacement = max(
        (a - b).length for a, b in zip(source_coordinates, bent_coordinates)
    )
    assert displacement > 0.1
    print(
        name,
        "rings:",
        len(heights),
        "vertices:",
        len(source_coordinates),
        "max bend displacement:",
        round(displacement, 3),
    )
assert len(bpy.data.objects["Limb.Supported"].data.vertices) > len(
    bpy.data.objects["Limb.Sparse"].data.vertices
)
tools.studio(lesson_scene, span=5, target=(0, 0, 1))
tools.active(bpy.data.objects["Limb.Supported"])
tools.finish(lesson_scene, assets_collection, "25_joint_topology")
