"""41｜青いワンピースのアバター。初期化して観察用ファイルを保存する教材。"""

from pathlib import Path
import sys
from math import pi
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

# 公開アバターと同じ設計値。身長はメートル、裾の半径だけを実験で変える。
BODY_HEIGHT = 1.64
HEM_RADIUS = 0.34
HEM_Z = 0.40

lesson_scene, assets_collection = tools.start("BlueDressAvatar")
# 公開モデルの色係数はテクスチャへ掛ける値。ここはテクスチャがないので、
# 観察ライトの下でも肌・青・黒・アイボリーが区別できるBase Colorにする。
skin_material = tools.material("Heroine.Skin", (0.48, 0.30, 0.21), 0.64)
iris_material = tools.material("Heroine.Iris", (0.02, 0.025, 0.03), 0.35)
highlight_material = tools.material("Heroine.EyeHighlight", (0.85, 0.85, 0.85), 0.30)
hair_material = tools.material("Heroine.Hair", (0.012, 0.008, 0.008), 0.9)
hair_material.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.15
# 綿は粗く、革はそれより光る。色だけでなくRoughnessで材質の役割を分ける。
cotton_material = tools.material("Heroine.Cotton", (0.20, 0.38, 0.68), 0.79)
leather_material = tools.material("Heroine.Leather", (0.62, 0.54, 0.40), 0.44)

torso_object = tools.tube(
    "Heroine.Torso",
    [0.84, 1.05, 1.34],
    [0.14, 0.12, 0.17],
    assets_collection,
    skin_material,
    sides=12,
)
neck_object = tools.tube(
    "Heroine.Neck",
    [1.34, 1.46],
    [0.05, 0.045],
    assets_collection,
    skin_material,
)
head_object = tools.sphere(
    "Heroine.Head",
    (0.21, 0.19, 0.22),
    (0, -0.01, BODY_HEIGHT - 0.11),
    assets_collection,
    skin_material,
)
# 髪は頭の頂点を動かさない。横にはみ出す別Meshと、顔の横へ下ろす束で黒を見せる。
hair_object = tools.sphere(
    "Heroine.Hair",
    (0.24, 0.18, 0.12),
    (0, 0.07, 1.57),
    assets_collection,
    hair_material,
)
hair_back_object = tools.tube(
    "Heroine.Hair.Back",
    [0, 0.70],
    [0.11, 0.05],
    assets_collection,
    hair_material,
)
hair_back_object.location = (0, 0.14, 1.52)
hair_back_object.rotation_euler.x = pi
for side in (-1, 1):
    hair_lock_object = tools.tube(
        f"Heroine.Hair.Lock.{side}",
        [0, 0.46],
        [0.035, 0.02],
        assets_collection,
        hair_material,
    )
    hair_lock_object.location = (side * 0.12, 0.02, 1.48)
    hair_lock_object.rotation_euler.x = pi
for side in (-1, 1):
    tools.sphere(
        f"Heroine.Eye.{side}",
        (0.035, 0.022, 0.038),
        (side * 0.045, -0.10, 1.54),
        assets_collection,
        iris_material,
        8,
        4,
    )
    tools.sphere(
        f"Heroine.EyeHighlight.{side}",
        (0.012, 0.008, 0.012),
        (side * 0.058, -0.108, 1.558),
        assets_collection,
        highlight_material,
        8,
        4,
    )
    arm_object = tools.tube(
        f"Heroine.Arm.{side}",
        [0, 0.24, 0.30, 0.52],
        [0.042, 0.036, 0.032, 0.028],
        assets_collection,
        skin_material,
    )
    # 筒は+Zに作る。肩を原点に180度回すと、袖なしの腕が下へ伸びる。
    arm_object.location = (side * 0.23, 0, 1.34)
    arm_object.rotation_euler.x = pi
    leg_object = tools.tube(
        f"Heroine.Leg.{side}",
        [0, 0.38, 0.46, 0.78],
        [0.045, 0.05, 0.055, 0.06],
        assets_collection,
        skin_material,
    )
    leg_object.location = (side * 0.07, 0, 0.84)
    leg_object.rotation_euler.x = pi
    sandal_object = tools.box(
        f"Heroine.Sandal.{side}",
        (0.10, 0.22, 0.03),
        (side * 0.07, 0.02, 0.015),
        assets_collection,
        leather_material,
    )
# ワンピースは体の頂点を動かさない。裾の高さと半径だけでAラインを決める。
dress_object = tools.tube(
    "Heroine.Dress",
    [HEM_Z, 0.70, 1.02, 1.24],
    [HEM_RADIUS, 0.26, 0.15, 0.19],
    assets_collection,
    cotton_material,
    sides=16,
)
dress_bmesh = bmesh.new()
dress_bmesh.from_mesh(dress_object.data)
cap_faces = [face for face in dress_bmesh.faces if len(face.verts) > 4]
bmesh.ops.delete(dress_bmesh, geom=cap_faces, context="FACES_ONLY")
dress_bmesh.to_mesh(dress_object.data)
dress_bmesh.free()
dress_object.data.update()

# 公開GLBの原点は足元中央。Emptyを地面に置き、部品の親にする。
# この親子はCollection所属でも、Meshの共有でもない。
root_object = bpy.data.objects.new("Heroine.Root", None)
assets_collection.objects.link(root_object)
root_object.empty_display_type = "PLAIN_AXES"
root_object.empty_display_size = 0.2
for heroine_object in list(assets_collection.objects):
    if heroine_object is root_object:
        continue
    heroine_object.parent = root_object

bpy.context.view_layer.update()
mesh_objects = [
    heroine_object
    for heroine_object in assets_collection.objects
    if heroine_object.type == "MESH"
]
world_corners = [
    heroine_object.matrix_world @ Vector(corner)
    for heroine_object in mesh_objects
    for corner in heroine_object.bound_box
]
measured_bottom = min(corner.z for corner in world_corners)
measured_top = max(corner.z for corner in world_corners)
measured_height = measured_top - measured_bottom
hem_vertices = [
    vertex
    for vertex in dress_object.data.vertices
    if abs(vertex.co.z - HEM_Z) < 1e-5
]


def roughness_of(surface_material):
    principled_node = surface_material.node_tree.nodes["Principled BSDF"]
    return principled_node.inputs["Roughness"].default_value


cotton_roughness = roughness_of(cotton_material)
skin_roughness = roughness_of(skin_material)
leather_roughness = roughness_of(leather_material)
assert dress_object.data is not torso_object.data
assert all(len(polygon.vertices) == 4 for polygon in dress_object.data.polygons)
assert len(dress_object.data.polygons) == 48
assert hem_vertices
assert all(
    abs((vertex.co.x**2 + vertex.co.y**2) ** 0.5 - HEM_RADIUS) < 1e-4
    for vertex in hem_vertices
)
assert cotton_roughness > skin_roughness > leather_roughness
assert abs(measured_bottom) < 0.001
assert abs(measured_height - BODY_HEIGHT) < 0.03
assert all(
    heroine_object.parent == root_object
    for heroine_object in assets_collection.objects
    if heroine_object is not root_object
)
print(
    f"height_m: {measured_height:.3f}",
    f"feet_z: {measured_bottom:.3f}",
    f"hem_z: {HEM_Z}",
    f"hem_radius: {HEM_RADIUS}",
    f"roughness cotton/skin/leather: {cotton_roughness:.2f}/{skin_roughness:.2f}/{leather_roughness:.2f}",
)
tools.studio(
    lesson_scene,
    span=2.2,
    target=(0, 0, 0.84),
    camera_location=(1.7, -2.15, 1.05),
)
tools.active(dress_object)
tools.finish(lesson_scene, assets_collection, "41_blue_dress_avatar")
