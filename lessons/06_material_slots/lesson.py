"""レッスン06: 1つのMeshで複数のMaterialをFaceごとに使い分ける。

Material slotとFaceのmaterial_indexの対応を、画面とログで観察できる
立方体を作る。
"""

from pathlib import Path

import bpy


def lesson_path() -> Path:
    """--pythonとBlender Text Editorのどちらでも教材の場所を得る。"""
    file_attr = globals().get("__file__")
    if file_attr:
        return Path(file_attr).resolve()
    text = getattr(bpy.context.space_data, "text", None)
    if text and text.filepath:
        return Path(bpy.path.abspath(text.filepath)).resolve()
    raise RuntimeError("lesson.pyを保存してRun Scriptするか、Blenderの--pythonで実行する")


ROOT = lesson_path().parents[2]
BLEND_PATH = ROOT / "output" / "06_material_slots.blend"

WOOD_SLOT_INDEX = 0
METAL_SLOT_INDEX = 1

# Face名、頂点番号、使用するMaterial slot番号。
# 上下面だけslot[1]、側面4枚はslot[0]を使う。
FACE_DEFINITIONS = (
    ("Bottom", (0, 3, 2, 1), METAL_SLOT_INDEX),
    ("Top", (4, 5, 6, 7), METAL_SLOT_INDEX),
    ("Front", (0, 1, 5, 4), WOOD_SLOT_INDEX),
    ("Right", (1, 2, 6, 5), WOOD_SLOT_INDEX),
    ("Back", (2, 3, 7, 6), WOOD_SLOT_INDEX),
    ("Left", (3, 0, 4, 7), WOOD_SLOT_INDEX),
)


def make_collection(
    collection_name: str,
    lesson_scene: bpy.types.Scene,
) -> bpy.types.Collection:
    """Collectionを作り、現在のSceneに所属させる。"""
    material_slots_collection = bpy.data.collections.new(collection_name)
    lesson_scene.collection.children.link(material_slots_collection)
    return material_slots_collection


def make_material(
    material_name: str,
    base_color: tuple[float, float, float, float],
    metallic: float,
    roughness: float,
) -> bpy.types.Material:
    """観察用のMaterialを作り、Principled BSDFへ値を設定する。"""
    sample_material = bpy.data.materials.new(material_name)
    sample_material.diffuse_color = base_color
    principled_node = sample_material.node_tree.nodes.get("Principled BSDF")
    if principled_node is None:
        raise RuntimeError(f"Principled BSDFが見つからない: {material_name}")
    principled_node.inputs["Base Color"].default_value = base_color
    principled_node.inputs["Metallic"].default_value = metallic
    principled_node.inputs["Roughness"].default_value = roughness
    return sample_material


def make_material_slot_mesh(mesh_name: str) -> bpy.types.Mesh:
    """FaceごとのMaterial割り当てを観察する直方体Meshを作る。"""
    vertices = (
        (-1.4, -1.0, 0.0),
        (1.4, -1.0, 0.0),
        (1.4, 1.0, 0.0),
        (-1.4, 1.0, 0.0),
        (-1.4, -1.0, 1.6),
        (1.4, -1.0, 1.6),
        (1.4, 1.0, 1.6),
        (-1.4, 1.0, 1.6),
    )
    faces = tuple(vertex_indices for _, vertex_indices, _ in FACE_DEFINITIONS)

    material_slot_mesh = bpy.data.meshes.new(mesh_name)
    material_slot_mesh.from_pydata(vertices, [], faces)
    material_slot_mesh.update()
    return material_slot_mesh


# main()の処理の流れ
# ① Sceneを初期化し、観察用Collectionを作る。
# ② 木材用と金属用の2つのMaterialを作る。
# ③ 6枚のFaceを持つMeshを作り、Material slotを2つ追加する。
# ④ 各Faceのmaterial_indexへ、使用するslot番号を設定する。
# ⑤ Meshを参照するObjectを作り、Collectionへ所属させる。
# ⑥ Object・Mesh・slot・Face・Materialの関係をログと検査で確認する。
# ⑦ 完成したSceneをoutput/06_material_slots.blendへ保存する。
def main() -> None:
    # ① Sceneを初期化し、観察用Collectionを作る。
    # Text Editorから実行する場合、現在の未保存作業は消えるので先に保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    material_slots_collection = make_collection("MaterialSlotsLesson", lesson_scene)

    # ② MaterialはMeshと別のデータブロックとして作る。
    wood_material = make_material(
        "Material.Wood",
        base_color=(0.48, 0.12, 0.025, 1.0),
        metallic=0.0,
        roughness=0.55,
    )
    metal_material = make_material(
        "Material.Metal",
        base_color=(0.04, 0.18, 0.45, 1.0),
        metallic=0.8,
        roughness=0.25,
    )

    # ③ 1つのMeshへ、順番を持つMaterial slotを2つ追加する。
    material_slot_mesh = make_material_slot_mesh("Sample.MaterialSlots.Mesh")
    material_slot_mesh.materials.append(wood_material)   # slot[0]
    material_slot_mesh.materials.append(metal_material)  # slot[1]

    # ④ FaceはMaterialそのものではなく、使用するslot番号を記録する。
    for polygon, (_, _, material_index) in zip(
        material_slot_mesh.polygons, FACE_DEFINITIONS
    ):
        polygon.material_index = material_index

    # ⑤ Object.dataからMeshを参照させ、ObjectをCollectionへ所属させる。
    material_slot_object = bpy.data.objects.new(
        "Sample.MaterialSlots", material_slot_mesh
    )
    material_slots_collection.objects.link(material_slot_object)
    bpy.context.view_layer.update()

    # ⑥ 同じ関係をOutliner、Material Properties、ログで照合できるようにする。
    print("=== 06 material slots ===")
    print(
        f"object={material_slot_object.name} -> mesh={material_slot_mesh.name} "
        f"slots={len(material_slot_mesh.materials)}"
    )
    for slot_index, slot_material in enumerate(material_slot_mesh.materials):
        print(f"slot[{slot_index}] -> material={slot_material.name}")

    for polygon, (face_name, _, expected_material_index) in zip(
        material_slot_mesh.polygons, FACE_DEFINITIONS
    ):
        slot_material = material_slot_mesh.materials[polygon.material_index]
        print(
            f"face[{polygon.index}] {face_name}: "
            f"material_index={polygon.material_index} -> {slot_material.name}"
        )
        if polygon.material_index != expected_material_index:
            raise RuntimeError(f"Faceのslot番号が違う: {face_name}")

    if material_slot_object.data is not material_slot_mesh:
        raise RuntimeError("Objectが想定したMeshを参照していない")
    if len(material_slot_mesh.materials) != 2:
        raise RuntimeError("Material slotが2個ではない")
    if material_slot_mesh.materials[WOOD_SLOT_INDEX] is not wood_material:
        raise RuntimeError("slot[0]が木材Materialを参照していない")
    if material_slot_mesh.materials[METAL_SLOT_INDEX] is not metal_material:
        raise RuntimeError("slot[1]が金属Materialを参照していない")

    # ⑦ 観察用の.blendを保存する。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
