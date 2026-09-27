"""レッスン05: 同じ形の球でMaterialの基本値による見え方を比較する。

Base Color、Metallic、Roughnessを1項目ずつ変えた4つのサンプルを作る。
実行後はREADMEの手順でMaterial PreviewとMaterial Propertiesを観察する。
"""

from math import isclose
from pathlib import Path

import bmesh
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
BLEND_PATH = ROOT / "output" / "05_material_basics.blend"

# Baselineに対して1項目だけ変え、どの値が見え方を変えたか比較しやすくする。
MATERIAL_SAMPLES = (
    {
        "object_name": "Sample.Baseline",
        "mesh_name": "Sample.Baseline.Mesh",
        "material_name": "Material.Baseline",
        "location": (-3.0, 0.0, 0.8),
        "base_color": (0.55, 0.06, 0.03, 1.0),
        "metallic": 0.0,
        "roughness": 0.45,
    },
    {
        "object_name": "Sample.ColorBlue",
        "mesh_name": "Sample.ColorBlue.Mesh",
        "material_name": "Material.ColorBlue",
        "location": (-1.0, 0.0, 0.8),
        "base_color": (0.03, 0.15, 0.65, 1.0),
        "metallic": 0.0,
        "roughness": 0.45,
    },
    {
        "object_name": "Sample.RoughnessLow",
        "mesh_name": "Sample.RoughnessLow.Mesh",
        "material_name": "Material.RoughnessLow",
        "location": (1.0, 0.0, 0.8),
        "base_color": (0.55, 0.06, 0.03, 1.0),
        "metallic": 0.0,
        "roughness": 0.08,
    },
    {
        "object_name": "Sample.MetallicHigh",
        "mesh_name": "Sample.MetallicHigh.Mesh",
        "material_name": "Material.MetallicHigh",
        "location": (3.0, 0.0, 0.8),
        "base_color": (0.55, 0.06, 0.03, 1.0),
        "metallic": 1.0,
        "roughness": 0.45,
    },
)


def make_collection(
    collection_name: str,
    lesson_scene: bpy.types.Scene,
) -> bpy.types.Collection:
    """Collectionを作り、現在のSceneに所属させる。"""
    new_collection = bpy.data.collections.new(collection_name)
    lesson_scene.collection.children.link(new_collection)
    return new_collection


def make_sample_mesh(mesh_name: str) -> bpy.types.Mesh:
    """光の反射を観察しやすい、滑らかな球のMeshを作る。"""
    sample_mesh = bpy.data.meshes.new(mesh_name)
    sample_bmesh = bmesh.new()
    bmesh.ops.create_icosphere(sample_bmesh, subdivisions=3, radius=0.8)
    sample_bmesh.to_mesh(sample_mesh)
    sample_bmesh.free()

    # 面を滑らかに表示すると、Roughnessによるハイライトの差を観察しやすい。
    for polygon in sample_mesh.polygons:
        polygon.use_smooth = True
    sample_mesh.update()
    return sample_mesh


def make_material(
    material_name: str,
    base_color: tuple[float, float, float, float],
    metallic: float,
    roughness: float,
) -> bpy.types.Material:
    """Principled BSDFの基本3項目を設定したMaterialを作る。"""
    sample_material = bpy.data.materials.new(material_name)
    sample_material.diffuse_color = base_color

    # Blender 5.2では新規MaterialにPrincipled BSDFが最初から用意されている。
    principled_node = sample_material.node_tree.nodes.get("Principled BSDF")
    if principled_node is None:
        raise RuntimeError(f"Principled BSDFが見つからない: {material_name}")
    principled_node.inputs["Base Color"].default_value = base_color
    principled_node.inputs["Metallic"].default_value = metallic
    principled_node.inputs["Roughness"].default_value = roughness
    return sample_material


def principled_values(
    sample_material: bpy.types.Material,
) -> tuple[tuple[float, float, float, float], float, float]:
    """検査とログ表示のため、Principled BSDFの3項目を読み取る。"""
    principled_node = sample_material.node_tree.nodes.get("Principled BSDF")
    if principled_node is None:
        raise RuntimeError(f"Principled BSDFが見つからない: {sample_material.name}")
    base_color = tuple(principled_node.inputs["Base Color"].default_value)
    metallic = principled_node.inputs["Metallic"].default_value
    roughness = principled_node.inputs["Roughness"].default_value
    return base_color, metallic, roughness


# main()の処理の流れ
# ① Sceneを初期化し、MaterialSamples Collectionを作る。
# ② 比較用のMaterial、Mesh、Objectを4組作る。
# ③ Objectを横一列に配置し、Materialを各Meshへ割り当てる。
# ④ Object・Mesh・Materialの関係とPrincipled BSDFの値をログへ表示する。
# ⑤ サンプル数、データの独立、設定値が設計どおりか検査する。
# ⑥ 完成したSceneをoutput/05_material_basics.blendへ保存する。
def main() -> None:
    # ① Sceneを初期化し、観察用Collectionを作る。
    # Text Editorから実行する場合、現在の未保存作業は消えるので先に保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    samples_collection = make_collection("MaterialSamples", lesson_scene)

    sample_objects: list[bpy.types.Object] = []
    sample_materials: list[bpy.types.Material] = []

    # ②〜③ 定義ごとにMaterial、Mesh、Objectを作って配置・所属させる。
    for sample_settings in MATERIAL_SAMPLES:
        sample_material = make_material(
            material_name=sample_settings["material_name"],
            base_color=sample_settings["base_color"],
            metallic=sample_settings["metallic"],
            roughness=sample_settings["roughness"],
        )
        sample_mesh = make_sample_mesh(sample_settings["mesh_name"])

        # Material slotはMesh側にあり、このサンプルでは各Meshに1個だけ割り当てる。
        sample_mesh.materials.append(sample_material)

        # objects.new()でObjectがMeshを参照し、CollectionへのlinkでSceneに現れる。
        sample_object = bpy.data.objects.new(sample_settings["object_name"], sample_mesh)
        samples_collection.objects.link(sample_object)
        sample_object.location = sample_settings["location"]
        sample_objects.append(sample_object)
        sample_materials.append(sample_material)

    bpy.context.view_layer.update()

    # ④ 画面で見るObject・Mesh・Materialと、シェーダー値をログでも対応させる。
    print("=== 05 material basics ===")
    for sample_object, sample_material in zip(sample_objects, sample_materials):
        base_color, metallic, roughness = principled_values(sample_material)
        rgb = tuple(round(component, 2) for component in base_color[:3])
        print(
            f"{sample_object.name}: mesh={sample_object.data.name} "
            f"material={sample_material.name} base_color={rgb} "
            f"metallic={metallic:.2f} roughness={roughness:.2f}"
        )

    # ⑤ 4サンプルが別々のMeshとMaterialを持ち、指定値が保存されることを検査する。
    if len(sample_objects) != 4 or len(sample_materials) != 4:
        raise RuntimeError("比較用サンプルが4個作られていない")
    if len({sample_object.data for sample_object in sample_objects}) != 4:
        raise RuntimeError("各Objectが独立したMeshを持っていない")
    if len(set(sample_materials)) != 4:
        raise RuntimeError("各サンプルが独立したMaterialを持っていない")

    for sample_settings, sample_object, sample_material in zip(
        MATERIAL_SAMPLES, sample_objects, sample_materials
    ):
        if sample_object.data.materials[0] is not sample_material:
            raise RuntimeError(f"Material割り当てが違う: {sample_object.name}")
        base_color, metallic, roughness = principled_values(sample_material)
        if any(
            not isclose(actual, expected, abs_tol=1e-6)
            for actual, expected in zip(base_color, sample_settings["base_color"])
        ):
            raise RuntimeError(f"Base Colorが違う: {sample_material.name}")
        if not isclose(metallic, sample_settings["metallic"], abs_tol=1e-6):
            raise RuntimeError(f"Metallicが違う: {sample_material.name}")
        if not isclose(roughness, sample_settings["roughness"], abs_tol=1e-6):
            raise RuntimeError(f"Roughnessが違う: {sample_material.name}")

    # ⑥ 観察用の.blendを保存する。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
