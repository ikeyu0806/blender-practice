"""39｜操作用アドオン。初期化して観察用ファイルを保存する教材。"""

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

import importlib.util
import zipfile

lesson_scene, assets_collection = tools.start("InspectionAddon")
stone_material = tools.material("Surface.Stone", (0.22, 0.42, 0.5))
crate_object = tools.box(
    "Asset.InspectMe", (1, 1, 1), (0, 0, 0.5), assets_collection, stone_material
)
tools.active(crate_object)
addon_path = Path(source_path).resolve().parent / "addon.py"
addon_spec = importlib.util.spec_from_file_location("lesson39_tools", addon_path)
addon_module = importlib.util.module_from_spec(addon_spec)
addon_spec.loader.exec_module(addon_module)
# 登録→操作→解除→再登録を試し、二重登録の問題も背景実行で見つける。
addon_module.register()
assert bpy.ops.lesson39.inspect() == {"FINISHED"}
assert crate_object["lesson39_face_count"] == 6
addon_module.unregister()
addon_module.register()
assert bpy.ops.lesson39.inspect() == {"FINISHED"}
zip_path = tools.OUTPUT / "39_install_addon.zip"
with zipfile.ZipFile(zip_path, "w") as archive:
    archive.write(addon_path, "lesson39_tools.py")
print("addon register/unregister/register: OK; install ZIP:", zip_path)
tools.studio(lesson_scene, span=4)
tools.finish(lesson_scene, assets_collection, "39_inspection_addon")
