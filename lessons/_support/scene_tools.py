"""10–40で繰り返す配置・保存だけをまとめる。学習対象の処理は各lesson.pyへ。"""

from pathlib import Path
from math import cos, sin, pi
import json

import bmesh
import bpy
from mathutils import Vector, Quaternion

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"


def start(title: str):
    """未保存のシーンを消して、所属先Collectionを作る。"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    lesson_scene.unit_settings.system = "METRIC"
    lesson_scene.unit_settings.scale_length = 1.0
    assets_collection = bpy.data.collections.new(title)
    lesson_scene.collection.children.link(assets_collection)
    OUTPUT.mkdir(exist_ok=True)
    return lesson_scene, assets_collection


def material(name, color, roughness=0.65, metallic=0.0):
    surface_material = bpy.data.materials.new(name)
    surface_material.diffuse_color = (*color[:3], 1.0)
    principled_node = surface_material.node_tree.nodes.get("Principled BSDF")
    principled_node.inputs["Base Color"].default_value = surface_material.diffuse_color
    principled_node.inputs["Roughness"].default_value = roughness
    principled_node.inputs["Metallic"].default_value = metallic
    return surface_material


def mesh_object(name, vertices, faces, assets_collection, surface_material=None):
    asset_mesh = bpy.data.meshes.new(name + ".Mesh")
    asset_mesh.from_pydata(vertices, [], faces)
    asset_mesh.update()
    # Meshを参照するObjectを作る操作と、Collectionへの所属は別。
    asset_object = bpy.data.objects.new(name, asset_mesh)
    assets_collection.objects.link(asset_object)
    if surface_material:
        asset_mesh.materials.append(surface_material)
    return asset_object


def box(name, size, location, assets_collection, surface_material=None):
    x, y, z = (value / 2 for value in size)
    asset_object = mesh_object(
        name,
        [
            (-x, -y, -z),
            (x, -y, -z),
            (x, y, -z),
            (-x, y, -z),
            (-x, -y, z),
            (x, -y, z),
            (x, y, z),
            (-x, y, z),
        ],
        [
            (0, 3, 2, 1),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
            (4, 5, 6, 7),
        ],
        assets_collection,
        surface_material,
    )
    # 寸法はMesh内で決める。Object.scaleは(1,1,1)のままなので検査しやすい。
    asset_object.location = location
    return asset_object


def sphere(
    name, size, location, assets_collection, surface_material=None, segments=16, rings=8
):
    asset_bmesh = bmesh.new()
    bmesh.ops.create_uvsphere(
        asset_bmesh, u_segments=segments, v_segments=rings, radius=1
    )
    for vertex in asset_bmesh.verts:
        vertex.co.x *= size[0] / 2
        vertex.co.y *= size[1] / 2
        vertex.co.z *= size[2] / 2
    asset_mesh = bpy.data.meshes.new(name + ".Mesh")
    asset_bmesh.to_mesh(asset_mesh)
    asset_bmesh.free()
    asset_object = bpy.data.objects.new(name, asset_mesh)
    assets_collection.objects.link(asset_object)
    asset_object.location = location
    if surface_material:
        asset_mesh.materials.append(surface_material)
    return asset_object


def cone(
    name, radius1, radius2, depth, location, assets_collection, surface_material=None
):
    asset_bmesh = bmesh.new()
    bmesh.ops.create_cone(
        asset_bmesh,
        cap_ends=True,
        cap_tris=False,
        segments=12,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
    )
    asset_mesh = bpy.data.meshes.new(name + ".Mesh")
    asset_bmesh.to_mesh(asset_mesh)
    asset_bmesh.free()
    asset_object = bpy.data.objects.new(name, asset_mesh)
    assets_collection.objects.link(asset_object)
    asset_object.location = location
    if surface_material:
        asset_mesh.materials.append(surface_material)
    return asset_object


def active(target_object):
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    target_object.select_set(True)
    bpy.context.view_layer.objects.active = target_object


def evaluated_coordinates(target_object):
    bpy.context.view_layer.update()
    dependency_graph = bpy.context.evaluated_depsgraph_get()
    evaluated_object = target_object.evaluated_get(dependency_graph)
    evaluated_mesh = evaluated_object.to_mesh()
    try:
        return [vertex.co.copy() for vertex in evaluated_mesh.vertices]
    finally:
        # 評価結果は一時データ。参照を残さず座標だけコピーして解放する。
        evaluated_object.to_mesh_clear()


def tube(name, ring_heights, radii, assets_collection, surface_material, sides=8):
    vertices = [
        (radius * cos(2 * pi * i / sides), radius * sin(2 * pi * i / sides), height)
        for height, radius in zip(ring_heights, radii)
        for i in range(sides)
    ]
    faces = [tuple(reversed(range(sides)))]
    for ring in range(len(ring_heights) - 1):
        for i in range(sides):
            a = ring * sides + i
            b = ring * sides + (i + 1) % sides
            faces.append((a, b, b + sides, a + sides))
    faces.append(tuple((len(ring_heights) - 1) * sides + i for i in range(sides)))
    return mesh_object(name, vertices, faces, assets_collection, surface_material)


def two_bone_rig(name, target_object, joint_height, assets_collection, bend_degrees=0):
    """Z方向の管を2本の骨で曲げる。25/28用、重みは関節周辺で混ぜる。"""
    from math import radians

    rig_armature = bpy.data.armatures.new(name + ".Armature")
    rig_object = bpy.data.objects.new(name, rig_armature)
    assets_collection.objects.link(rig_object)
    rig_object.location = target_object.location
    active(rig_object)
    bpy.ops.object.mode_set(mode="EDIT")
    bottom = min(vertex.co.z for vertex in target_object.data.vertices)
    top = max(vertex.co.z for vertex in target_object.data.vertices)
    lower_bone = rig_armature.edit_bones.new("Lower")
    lower_bone.head, lower_bone.tail = (0, 0, bottom), (0, 0, joint_height)
    upper_bone = rig_armature.edit_bones.new("Upper")
    upper_bone.head, upper_bone.tail = lower_bone.tail, (0, 0, top)
    upper_bone.parent = lower_bone
    upper_bone.use_connect = True
    bpy.ops.object.mode_set(mode="OBJECT")
    lower_group = target_object.vertex_groups.new(name="Lower")
    upper_group = target_object.vertex_groups.new(name="Upper")
    for vertex in target_object.data.vertices:
        upper_weight = min(1, max(0, (vertex.co.z - joint_height + 0.25) / 0.5))
        lower_group.add([vertex.index], 1 - upper_weight, "REPLACE")
        upper_group.add([vertex.index], upper_weight, "REPLACE")
    armature_modifier = target_object.modifiers.new("Deform", "ARMATURE")
    armature_modifier.object = rig_object
    armature_modifier.use_deform_preserve_volume = True
    rig_object.show_in_front = True
    upper_pose_bone = rig_object.pose.bones["Upper"]
    upper_pose_bone.rotation_mode = "XYZ"
    upper_pose_bone.rotation_euler.x = radians(bend_degrees)
    return rig_object


def uv_smart(target_object):
    # UIのSmart UV Projectは選択とモードに依存するため、その前提をそろえる。
    active(target_object)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=0.03)
    bpy.ops.object.mode_set(mode="OBJECT")
    assert target_object.data.uv_layers.active is not None


def prop_set(assets_collection, spacing=1.8):
    wood_material = material("Surface.Wood", (0.34, 0.16, 0.06))
    stone_material = material("Surface.Stone", (0.28, 0.34, 0.40))
    metal_material = material("Surface.Metal", (0.20, 0.23, 0.25), 0.3, 0.8)
    crate_object = box(
        "Prop.Crate", (1, 1, 1), (-spacing, 0, 0.5), assets_collection, wood_material
    )
    bevel_modifier = crate_object.modifiers.new("EdgeWear", "BEVEL")
    bevel_modifier.width, bevel_modifier.segments = 0.05, 2
    rock_object = sphere(
        "Prop.Rock",
        (1.2, 0.8, 0.7),
        (0, 0, 0.35),
        assets_collection,
        stone_material,
        8,
        4,
    )
    for vertex in rock_object.data.vertices:
        vertex.co.x += 0.06 * sin(vertex.co.z * 10 + vertex.co.y * 4)
    barrel_object = cone(
        "Prop.Barrel",
        0.45,
        0.45,
        1.1,
        (spacing, 0, 0.55),
        assets_collection,
        wood_material,
    )
    for height in (0.2, 0.9):
        cone(
            f"Prop.BarrelBand.{height}",
            0.47,
            0.47,
            0.08,
            (spacing, 0, height),
            assets_collection,
            metal_material,
        )
    return crate_object, rock_object, barrel_object


def room(assets_collection, unit=2.0):
    wall_material = material("Surface.Plaster", (0.44, 0.52, 0.50))
    floor_material = material("Surface.Floor", (0.23, 0.17, 0.11))
    for x in (-unit, 0, unit):
        for y in (-unit, 0, unit):
            box(
                f"Room.Floor.{x}.{y}",
                (unit, unit, 0.15),
                (x, y, -0.075),
                assets_collection,
                floor_material,
            )
    # 前面は左右の壁と上部の梁に分け、中央に入口を残す。
    for x in (-unit, unit):
        box(
            f"Room.EntrySide.{x}",
            (unit, 0.2, 2.8),
            (x, -1.5 * unit, 1.4),
            assets_collection,
            wall_material,
        )
    box(
        "Room.Lintel",
        (unit, 0.2, 0.6),
        (0, -1.5 * unit, 2.5),
        assets_collection,
        wall_material,
    )
    for x in (-unit, 0, unit):
        box(
            f"Room.Back.{x}",
            (unit, 0.2, 2.8),
            (x, 1.5 * unit, 1.4),
            assets_collection,
            wall_material,
        )
    for y in (-unit, 0, unit):
        box(
            f"Room.Side.{y}",
            (0.2, unit, 2.8),
            (-1.5 * unit, y, 1.4),
            assets_collection,
            wall_material,
        )
    return bpy.data.objects["Room.Lintel"]


def humanoid(assets_collection, head_size=0.65, posed=False):
    """制作回用のデフォルメ人物。胴は剛体、四肢はリングとウェイトで変形。"""
    from math import radians

    skin_material = material("Character.Skin", (0.65, 0.36, 0.21))
    cloth_material = material("Character.Cloth", (0.08, 0.28, 0.43))
    hair_material = material("Character.Hair", (0.055, 0.028, 0.018))
    body_object = box(
        "Character.Torso",
        (0.9, 0.48, 0.95),
        (0, 0, 2.35),
        assets_collection,
        cloth_material,
    )
    box(
        "Character.Pelvis",
        (0.8, 0.5, 0.4),
        (0, 0, 1.72),
        assets_collection,
        cloth_material,
    )
    head_object = sphere(
        "Character.Head",
        (head_size, 0.60, head_size),
        (0, 0, 3.2),
        assets_collection,
        skin_material,
    )
    sphere(
        "Character.Hair",
        (head_size * 1.06, 0.64, 0.45),
        (0, 0.03, 3.43),
        assets_collection,
        hair_material,
    )
    for side in (-1, 1):
        sphere(
            f"Character.Eye.{side}",
            (0.07, 0.05, 0.08),
            (side * 0.14, -0.29, 3.24),
            assets_collection,
            hair_material,
            8,
            4,
        )
    limb_rig_objects = []
    for side in (-1, 1):
        arm_object = tube(
            f"Character.Arm.{side}",
            [0, 0.4, 0.5, 0.6, 1.0],
            [0.13] * 5,
            assets_collection,
            skin_material,
        )
        arm_object.location = (side * 0.68, 0, 2.6)
        arm_object.rotation_euler.x = pi
        arm_rig_object = two_bone_rig(
            f"Rig.Arm.{side}", arm_object, 0.5, assets_collection
        )
        arm_rig_object.rotation_euler.x = pi
        leg_object = tube(
            f"Character.Leg.{side}",
            [0, 0.65, 0.75, 0.85, 1.45],
            [0.16] * 5,
            assets_collection,
            cloth_material,
        )
        leg_object.location = (side * 0.23, 0, 1.65)
        leg_object.rotation_euler.x = pi
        leg_rig_object = two_bone_rig(
            f"Rig.Leg.{side}", leg_object, 0.75, assets_collection
        )
        leg_rig_object.rotation_euler.x = pi
        foot_object = box(
            f"Character.Foot.{side}",
            (0.36, 0.6, 0.2),
            (side * 0.23, -0.15, 0.1),
            assets_collection,
            hair_material,
        )
        # 足はUpper（膝より先の骨）へ100%割り当て、脛と一緒に追従させる。
        foot_group = foot_object.vertex_groups.new(name="Upper")
        foot_group.add(list(range(len(foot_object.data.vertices))), 1, "REPLACE")
        foot_modifier = foot_object.modifiers.new("FollowShin", "ARMATURE")
        foot_modifier.object = leg_rig_object
        limb_rig_objects.extend([arm_rig_object, leg_rig_object])
    # キーフレーム1で中立姿勢、24で肩と腰を固定して肘と膝を曲げる。
    for rig_object in limb_rig_objects:
        upper_pose_bone = rig_object.pose.bones["Upper"]
        upper_pose_bone.keyframe_insert("rotation_euler", frame=1)
        upper_pose_bone.rotation_euler.x = radians(
            -35 if ".Arm." in rig_object.name else 25
        )
        upper_pose_bone.keyframe_insert("rotation_euler", frame=24)
    bpy.context.scene.frame_end = 24
    bpy.context.scene.frame_set(24 if posed else 1)
    return body_object, head_object, limb_rig_objects


def monster(assets_collection, posed=False, horn_height=0.6):
    from math import radians

    body_material = material("Monster.Scales", (0.13, 0.32, 0.16))
    horn_material = material("Monster.Horn", (0.72, 0.62, 0.38))
    eye_material = material("Monster.Eye", (0.90, 0.38, 0.04), 0.25)
    body_object = sphere(
        "Monster.Body", (1.8, 2.0, 1.4), (0, 0, 1.0), assets_collection, body_material
    )
    head_object = sphere(
        "Monster.Head",
        (1.2, 1.0, 0.9),
        (0, -1.0, 1.6),
        assets_collection,
        body_material,
    )
    for side in (-1, 1):
        cone(
            f"Monster.Horn.{side}",
            0.18,
            0,
            horn_height,
            (side * 0.35, -0.8, 2.0 + horn_height / 2),
            assets_collection,
            horn_material,
        )
        sphere(
            f"Monster.Eye.{side}",
            (0.15, 0.12, 0.15),
            (side * 0.35, -1.43, 1.75),
            assets_collection,
            eye_material,
            8,
            4,
        )
        for y in (-0.55, 0.65):
            cone(
                f"Monster.Leg.{side}.{y}",
                0.2,
                0.25,
                0.6,
                (side * 0.68, y, 0.3),
                assets_collection,
                body_material,
            )
    tail_object = tube(
        "Monster.Tail",
        [0, 0.8, 1.0, 1.2, 2.1],
        [0.3, 0.23, 0.2, 0.17, 0.02],
        assets_collection,
        body_material,
    )
    tail_object.location = (0, 0.75, 1.0)
    tail_object.rotation_euler.x = -pi / 2
    tail_rig_object = two_bone_rig("Rig.Tail", tail_object, 1.0, assets_collection)
    tail_rig_object.rotation_euler = tail_object.rotation_euler
    # Shape Keyは同じ頂点番号に別座標を持つ。頂点数は増やさない。
    head_object.shape_key_add(name="Basis")
    mouth_shape_key = head_object.shape_key_add(name="JawDrop")
    for point in mouth_shape_key.data:
        if point.co.y < 0 and point.co.z < 0:
            point.co.z -= 0.25 * (-point.co.y / 0.5)
    mouth_shape_key.value = 0
    mouth_shape_key.keyframe_insert("value", frame=1)
    mouth_shape_key.value = 1
    mouth_shape_key.keyframe_insert("value", frame=24)
    upper_pose_bone = tail_rig_object.pose.bones["Upper"]
    upper_pose_bone.keyframe_insert("rotation_euler", frame=1)
    upper_pose_bone.rotation_euler.y = radians(40)
    upper_pose_bone.keyframe_insert("rotation_euler", frame=24)
    bpy.context.scene.frame_end = 24
    bpy.context.scene.frame_set(24 if posed else 1)
    return body_object, head_object, tail_object, tail_rig_object


def studio(lesson_scene, span=6, target=(0, 0, 1), camera_location=None):
    presentation_collection = bpy.data.collections.new("Presentation")
    lesson_scene.collection.children.link(presentation_collection)
    ground_material = material("Presentation.Ground", (0.055, 0.065, 0.08))
    box(
        "Presentation.Ground",
        (span * 4, span * 4, 0.1),
        (0, 0, -0.16),
        presentation_collection,
        ground_material,
    )
    camera_data = bpy.data.cameras.new("Presentation.Camera.Data")
    camera_object = bpy.data.objects.new("Presentation.Camera", camera_data)
    presentation_collection.objects.link(camera_object)
    camera_object.location = camera_location or (span * 0.8, -span * 1.4, span * 0.95)
    camera_object.rotation_euler = (
        (Vector(target) - camera_object.location).to_track_quat("-Z", "Y").to_euler()
    )
    camera_data.lens = 45
    camera_data.clip_end = 500
    lesson_scene.camera = camera_object
    for name, location, energy, size in [
        ("Key", (span / 2, -span / 2, span), 1200, 4),
        ("Fill", (-span, -span / 3, span / 2), 600, 5),
        ("Rim", (0, span, span), 1000, 3),
    ]:
        light_data = bpy.data.lights.new("Presentation." + name + ".Data", "AREA")
        light_data.energy, light_data.shape, light_data.size = energy, "DISK", size
        light_object = bpy.data.objects.new("Presentation." + name, light_data)
        presentation_collection.objects.link(light_object)
        light_object.location = location
        light_object.rotation_euler = (
            (Vector(target) - light_object.location).to_track_quat("-Z", "Y").to_euler()
        )
    lesson_scene.world = bpy.data.worlds.new("Presentation.World")
    lesson_scene.world.use_nodes = True
    lesson_scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        0.15,
        0.18,
        0.24,
        1,
    )
    lesson_scene.world.node_tree.nodes["Background"].inputs[
        "Strength"
    ].default_value = 0.3
    lesson_scene.render.engine = "CYCLES"
    lesson_scene.cycles.device = "CPU"
    lesson_scene.cycles.samples = 16
    lesson_scene.render.resolution_x, lesson_scene.render.resolution_y = 640, 480
    lesson_scene.render.resolution_percentage = 100
    for lesson_screen in bpy.data.screens:
        for editor_area in lesson_screen.areas:
            if editor_area.type == "VIEW_3D":
                viewport_space = editor_area.spaces.active
                viewport_space.shading.color_type = "MATERIAL"
                viewport_space.region_3d.view_distance = span * 1.8
                viewport_space.region_3d.view_location = target
                viewport_space.region_3d.view_rotation = (
                    camera_object.rotation_euler.to_quaternion()
                )
    return camera_object


def finish(lesson_scene, assets_collection, slug, render=False):
    """保存前に空の教材でないことを確認し、関係をJSONにも残す。"""
    bpy.context.view_layer.update()
    mesh_objects = [
        asset_object
        for asset_object in assets_collection.all_objects
        if asset_object.type == "MESH"
    ]
    assert mesh_objects, "観察するMeshがない"
    for asset_object in mesh_objects:
        assert (
            asset_object.data.vertices and asset_object.data.polygons
        ), asset_object.name
        assert all(
            polygon.area > 1e-10 for polygon in asset_object.data.polygons
        ), asset_object.name
    report = {
        "lesson": slug,
        "blender": bpy.app.version_string,
        "frame": lesson_scene.frame_current,
        "objects": [
            {
                "name": asset_object.name,
                "type": asset_object.type,
                "data": asset_object.data.name if asset_object.data else None,
                "dimensions": list(asset_object.dimensions),
                "vertices": (
                    len(asset_object.data.vertices)
                    if asset_object.type == "MESH"
                    else None
                ),
                "faces": (
                    len(asset_object.data.polygons)
                    if asset_object.type == "MESH"
                    else None
                ),
            }
            for asset_object in assets_collection.all_objects
        ],
    }
    blend_path = OUTPUT / (slug + ".blend")
    (OUTPUT / (slug + ".json")).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lesson_scene.render.filepath = str(OUTPUT / (slug + ".png"))
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    assert blend_path.is_file() and blend_path.stat().st_size > 1000
    print(f"CHECK OK {slug}: meshes={len(mesh_objects)} saved={blend_path}")
    if render:
        bpy.ops.render.render(write_still=True)
        assert (OUTPUT / (slug + ".png")).is_file()
