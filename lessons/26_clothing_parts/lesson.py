"""26｜衣装と部品分割。初期化して観察用ファイルを保存する教材。"""

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

CLOTH_THICKNESS = 0.04
lesson_scene, assets_collection = tools.start("ClothingParts")
skin_material = tools.material("Surface.Skin", (0.64, 0.36, 0.2))
cloth_material = tools.material("Surface.Cloth", (0.06, 0.24, 0.36))
metal_material = tools.material("Surface.Buckle", (0.45, 0.33, 0.08), 0.25, 0.8)
body_object = tools.tube(
    "Character.Body", [0, 1.2], [0.45, 0.35], assets_collection, skin_material
)
body_object.location.z = 0.6
# 衣装は上下が開いた別Mesh。体を消さずに、隙間と厚みを独立して調整する。
shirt_object = tools.tube(
    "Clothing.Vest",
    [0, 0.6, 1.2],
    [0.51, 0.48, 0.41],
    assets_collection,
    cloth_material,
)
shirt_object.location.z = 0.6
shirt_bmesh = bmesh.new()
shirt_bmesh.from_mesh(shirt_object.data)
cap_faces = [face for face in shirt_bmesh.faces if len(face.verts) > 4]
bmesh.ops.delete(shirt_bmesh, geom=cap_faces, context="FACES_ONLY")
shirt_bmesh.to_mesh(shirt_object.data)
shirt_bmesh.free()
shirt_object.data.update()
solidify_modifier = shirt_object.modifiers.new("FabricThickness", "SOLIDIFY")
solidify_modifier.thickness = CLOTH_THICKNESS
solidify_modifier.offset = 1
buckle_object = tools.box(
    "Accessory.Buckle",
    (0.24, 0.08, 0.18),
    (0, -0.53, 0.9),
    assets_collection,
    metal_material,
)
assert shirt_object.data is not body_object.data
assert len(shirt_object.data.polygons) == 16
assert len(tools.evaluated_coordinates(shirt_object)) > len(shirt_object.data.vertices)
print(
    "cloth source faces:",
    16,
    "thickness:",
    CLOTH_THICKNESS,
    "body/shirt/buckle: separate Mesh",
)
tools.studio(lesson_scene, span=4, target=(0, 0, 1))
tools.active(shirt_object)
tools.finish(lesson_scene, assets_collection, "26_clothing_parts")
