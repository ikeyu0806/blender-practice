"""37｜アセット検査。初期化して観察用ファイルを保存する教材。"""

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

MAX_DIMENSION = 2.0
lesson_scene, assets_collection = tools.start("AssetValidation")
stone_material = tools.material("Surface.Stone", (0.25, 0.4, 0.45))
good_object = tools.box(
    "Asset.Good", (1, 1, 1), (-1.2, 0, 0.5), assets_collection, stone_material
)
bad_object = tools.box(
    "WrongName", (1, 1, 1), (1.2, 0, 1), assets_collection, stone_material
)
tools.uv_smart(good_object)
bad_object.scale.z = 2
bad_bmesh = bmesh.new()
bad_bmesh.from_mesh(bad_object.data)
bad_bmesh.faces.ensure_lookup_table()
bmesh.ops.reverse_faces(bad_bmesh, faces=[bad_bmesh.faces[0]])
bad_bmesh.to_mesh(bad_object.data)
bad_bmesh.free()
bad_object.data.update()

# 検査だけを手編集後にも呼べるように、初期化しないモジュールへ分ける。
sys.path.insert(0, str(Path(source_path).resolve().parent))
from inspection import inspect_asset

bpy.context.view_layer.update()
good_problems = inspect_asset(good_object, MAX_DIMENSION)
bad_problems = inspect_asset(bad_object, MAX_DIMENSION)
assert good_problems == []
assert any("name:" in problem for problem in bad_problems)
assert any("scale:" in problem for problem in bad_problems)
assert any("UV:" in problem for problem in bad_problems)
assert any("normals:" in problem for problem in bad_problems)
for asset_object, problems in [
    (good_object, good_problems),
    (bad_object, bad_problems),
]:
    asset_object["inspection"] = "PASS" if not problems else " / ".join(problems)
    print(asset_object.name, "PASS" if not problems else problems)
import json

(tools.OUTPUT / "37_inspection.json").write_text(
    json.dumps(
        {good_object.name: good_problems, bad_object.name: bad_problems}, indent=2
    )
)
tools.studio(lesson_scene, span=5)
tools.active(bad_object)
tools.finish(lesson_scene, assets_collection, "37_asset_validation")
