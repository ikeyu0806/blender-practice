"""レッスン09: Faceの情報をBlender 5.2.2の画面とPythonで観察する。

1つの傾いた直方体Meshを作り、上面を選択したEdit Modeの状態で保存する。
Face番号、構成頂点、面積、中心、法線、Material slot番号を照合する。
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
BLEND_PATH = ROOT / "output" / "09_face_inspection.blend"

# 奥側を高くすると、上面と側面の面積・法線が頂点位置から再計算される。
TOP_FRONT_HEIGHT = 1.0
TOP_REAR_HEIGHT = 1.8

BASE_MATERIAL_SLOT_INDEX = 0
HIGHLIGHT_MATERIAL_SLOT_INDEX = 1
TOP_FACE_INDEX = 5

# 並び順がVertex.indexになる。0〜3が底、4〜7が傾いた上部。
FACE_SAMPLE_VERTEX_COORDINATES = (
    (-1.5, -1.0, 0.0),  # Vertex 0: 底・前左
    (1.5, -1.0, 0.0),   # Vertex 1: 底・前右
    (1.5, 1.0, 0.0),    # Vertex 2: 底・奥右
    (-1.5, 1.0, 0.0),   # Vertex 3: 底・奥左
    (-1.0, -1.0, TOP_FRONT_HEIGHT),  # Vertex 4: 上・前左
    (1.0, -1.0, TOP_FRONT_HEIGHT),   # Vertex 5: 上・前右
    (1.0, 1.0, TOP_REAR_HEIGHT),     # Vertex 6: 上・奥右
    (-1.0, 1.0, TOP_REAR_HEIGHT),    # Vertex 7: 上・奥左
)

# (教材内のFace名, Faceを囲む頂点番号, 使用するMaterial slot番号)
# この並び順がMesh.polygonsのindex 0〜5になる。
FACE_SAMPLE_DEFINITIONS = (
    ("Bottom", (0, 3, 2, 1), BASE_MATERIAL_SLOT_INDEX),
    ("Front", (0, 1, 5, 4), BASE_MATERIAL_SLOT_INDEX),
    ("Right", (1, 2, 6, 5), BASE_MATERIAL_SLOT_INDEX),
    ("Back", (2, 3, 7, 6), BASE_MATERIAL_SLOT_INDEX),
    ("Left", (3, 0, 4, 7), BASE_MATERIAL_SLOT_INDEX),
    ("Top", (4, 5, 6, 7), HIGHLIGHT_MATERIAL_SLOT_INDEX),
)


def make_collection(
    collection_name: str,
    lesson_scene: bpy.types.Scene,
) -> bpy.types.Collection:
    """観察用Collectionを作り、現在のSceneへ所属させる。"""
    face_inspection_collection = bpy.data.collections.new(collection_name)
    lesson_scene.collection.children.link(face_inspection_collection)
    return face_inspection_collection


def make_material(
    material_name: str,
    base_color: tuple[float, float, float, float],
) -> bpy.types.Material:
    """ViewportとPrincipled BSDFで同じ色を使うMaterialを作る。"""
    face_material = bpy.data.materials.new(material_name)
    face_material.diffuse_color = base_color

    principled_node = face_material.node_tree.nodes.get("Principled BSDF")
    if principled_node is None:
        raise RuntimeError(f"{material_name}にPrincipled BSDFがない")
    principled_node.inputs["Base Color"].default_value = base_color
    principled_node.inputs["Roughness"].default_value = 0.65
    return face_material


def make_face_sample_mesh(
    mesh_name: str,
    base_material: bpy.types.Material,
    highlight_material: bpy.types.Material,
) -> bpy.types.Mesh:
    """Faceごとに面積と法線が異なる観察用Meshを作る。"""
    face_vertex_indices = tuple(
        vertex_indices
        for _, vertex_indices, _ in FACE_SAMPLE_DEFINITIONS
    )

    face_sample_mesh = bpy.data.meshes.new(mesh_name)
    face_sample_mesh.from_pydata(
        FACE_SAMPLE_VERTEX_COORDINATES,
        [],
        face_vertex_indices,
    )
    face_sample_mesh.materials.append(base_material)
    face_sample_mesh.materials.append(highlight_material)

    # FaceはMaterialを直接参照せず、Mesh.materials内のslot番号を持つ。
    for polygon, (_, _, material_slot_index) in zip(
        face_sample_mesh.polygons,
        FACE_SAMPLE_DEFINITIONS,
    ):
        polygon.material_index = material_slot_index

    face_sample_mesh.update()
    return face_sample_mesh


def configure_viewport_overlays() -> None:
    """保存後にFace番号・面積・法線をすぐ観察できる表示設定にする。"""
    for lesson_screen in bpy.data.screens:
        for editor_area in lesson_screen.areas:
            if editor_area.type != "VIEW_3D":
                continue

            viewport_space = editor_area.spaces.active
            viewport_overlay = viewport_space.overlay
            viewport_overlay.show_overlays = True
            viewport_overlay.show_face_center = True
            viewport_overlay.show_extra_indices = True
            viewport_overlay.show_extra_face_area = True
            viewport_overlay.show_face_normals = True
            viewport_overlay.normals_length = 0.35

            # Solid表示でもMaterial slotの違いが色で分かるようにする。
            viewport_space.shading.type = "SOLID"
            viewport_space.shading.color_type = "MATERIAL"


def print_face_information(face_sample_mesh: bpy.types.Mesh) -> None:
    """画面Overlayと照合するFace情報をログへ表示する。"""
    print("=== 09 face inspection ===")
    for polygon, (face_name, _, _) in zip(
        face_sample_mesh.polygons,
        FACE_SAMPLE_DEFINITIONS,
    ):
        print(
            f"face[{polygon.index}] {face_name}: "
            f"vertices={tuple(polygon.vertices)} "
            f"center={tuple(round(value, 3) for value in polygon.center)} "
            f"area={polygon.area:.3f} "
            f"normal={tuple(round(value, 3) for value in polygon.normal)} "
            f"material_index={polygon.material_index}"
        )


# main()の処理の流れ
# ① Sceneを初期化し、Face観察用Collectionを作る。
# ② ベース色と選択Face強調色のMaterialを作る。
# ③ 8頂点・6面から傾いた直方体Meshを作り、2つのslotを追加する。
# ④ Meshを参照するObjectを作り、Collectionへ所属させる。
# ⑤ Face番号・構成頂点・中心・面積・法線・slot番号をログへ表示する。
# ⑥ データ関係とTop Faceの番号・Material割り当てを検査する。
# ⑦ Top Faceを選択したEdit ModeとOverlay設定を保存する。
def main() -> None:
    # ① 現在のSceneを初期化するため、Text Editor実行前には作業を保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    face_inspection_collection = make_collection("FaceInspection", lesson_scene)

    # ② Materialは独立データ。次の手順でMeshのslotから参照する。
    base_material = make_material(
        "Material.FaceBase",
        (0.22, 0.32, 0.42, 1.0),
    )
    highlight_material = make_material(
        "Material.FaceHighlight",
        (0.95, 0.32, 0.08, 1.0),
    )

    # ③ Faceのindex・verticesは定義順から決まり、center・area・normalは
    # 頂点座標と頂点順からBlenderが計算する。material_indexは明示的に設定する。
    face_sample_mesh = make_face_sample_mesh(
        "FaceSample.Mesh",
        base_material,
        highlight_material,
    )

    # ④ MeshだけではSceneに表示されない。ObjectがMeshを参照し、
    # Collectionへ所属することで、Outlinerと3Dビューポートに現れる。
    face_sample_object = bpy.data.objects.new(
        "FaceSample",
        face_sample_mesh,
    )
    face_inspection_collection.objects.link(face_sample_object)
    face_sample_object.show_wire = True
    face_sample_object.show_all_edges = True
    bpy.context.view_layer.update()

    # ⑤ PythonではMesh.polygonsを順番に読み、UIでは同じ値をOverlayで見る。
    print_face_information(face_sample_mesh)

    # ⑥ 形状とデータ関係が教材の想定からずれていないか確認する。
    element_counts = (
        len(face_sample_mesh.vertices),
        len(face_sample_mesh.edges),
        len(face_sample_mesh.polygons),
    )
    if element_counts != (8, 12, 6):
        raise RuntimeError(f"要素数が想定と違う: {element_counts}")
    if face_sample_object.data is not face_sample_mesh:
        raise RuntimeError("FaceSample Objectが観察用Meshを参照していない")
    if len(face_sample_mesh.materials) != 2:
        raise RuntimeError("Material slot数が2ではない")

    top_polygon = face_sample_mesh.polygons[TOP_FACE_INDEX]
    if tuple(top_polygon.vertices) != (4, 5, 6, 7):
        raise RuntimeError(f"Top Faceの構成頂点が違う: {top_polygon.vertices[:]}")
    if top_polygon.material_index != HIGHLIGHT_MATERIAL_SLOT_INDEX:
        raise RuntimeError(
            f"Top Faceのmaterial_indexが違う: {top_polygon.material_index}"
        )

    # ⑦ 開いた直後にFace 5を観察できるよう、Face SelectとEdit Modeを保存する。
    for polygon in face_sample_mesh.polygons:
        polygon.select = polygon.index == TOP_FACE_INDEX

    face_sample_object.select_set(True)
    bpy.context.view_layer.objects.active = face_sample_object
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    configure_viewport_overlays()
    bpy.ops.object.mode_set(mode="EDIT")

    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
