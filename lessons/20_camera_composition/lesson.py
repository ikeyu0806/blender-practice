"""20｜カメラと構図。初期化して観察用ファイルを保存する教材。"""

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

FOCAL_LENGTH = 45
lesson_scene, assets_collection = tools.start("CameraComposition")
crate_object, rock_object, barrel_object = tools.prop_set(assets_collection)
stone_material = tools.material("Surface.Background", (0.28, 0.36, 0.39))
tools.box(
    "Composition.Background",
    (5, 0.3, 2.2),
    (0, 3, 1.1),
    assets_collection,
    stone_material,
)
foreground_object = tools.sphere(
    "Composition.Foreground",
    (1, 1, 1),
    (-2, -2, 0.5),
    assets_collection,
    stone_material,
)
camera_object = tools.studio(lesson_scene, span=6, target=(0, 0, 0.8))
# 同じ位置で焦点距離だけを変えると、遠近感ではなく画角と写る範囲が変わる。
for lens in (24, 70):
    camera_object.data.lens = lens
    lesson_scene.render.filepath = str(tools.OUTPUT / f"20_lens_{lens}.png")
    bpy.ops.render.render(write_still=True)
camera_object.data.lens = FOCAL_LENGTH
assert camera_object.location.y < foreground_object.location.y
print(
    "camera lens:", camera_object.data.lens, "location:", tuple(camera_object.location)
)
tools.active(camera_object)
tools.finish(lesson_scene, assets_collection, "20_camera_composition", render=True)
