"""レッスン08: 頂点座標とFaceの頂点順から低ポリ岩を作る。

正しい岩と、1枚だけFaceの頂点順を反転した岩を並べる。
Face Orientationと法線の向きを画面・ログの両方で観察する。
"""

from pathlib import Path

import bpy
from mathutils import Vector


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
BLEND_PATH = ROOT / "output" / "08_vertices_rock.blend"

# 並び順がVertex.indexになる。0〜3が底、4〜7が中段、8が頂点。
ROCK_VERTEX_COORDINATES = (
    (-1.2, -0.9, 0.0),  # 0: 底・前左
    (1.0, -0.8, 0.0),   # 1: 底・前右
    (1.2, 0.7, 0.0),    # 2: 底・奥右
    (-0.8, 1.0, 0.0),   # 3: 底・奥左
    (-0.9, -0.6, 0.8),  # 4: 中段・前左
    (0.7, -0.7, 1.0),   # 5: 中段・前右
    (0.9, 0.5, 0.9),    # 6: 中段・奥右
    (-0.6, 0.7, 1.1),   # 7: 中段・奥左
    (0.0, 0.0, 1.55),   # 8: 岩の頂点
)

# 頂点番号を外側から見て反時計回りに並べると、Faceの法線は外向きになる。
# Face名はログと検査用で、from_pydata()へ渡すのは頂点番号だけ。
ROCK_FACE_DEFINITIONS = (
    ("Bottom", (0, 3, 2, 1)),
    ("Lower.Front", (0, 1, 5, 4)),
    ("Lower.Right", (1, 2, 6, 5)),
    ("Lower.Back", (2, 3, 7, 6)),
    ("Lower.Left", (3, 0, 4, 7)),
    ("Upper.Front", (4, 5, 8)),
    ("Upper.Right", (5, 6, 8)),
    ("Upper.Back", (6, 7, 8)),
    ("Upper.Left", (7, 4, 8)),
)

# 右の比較用Meshでは、このFaceだけ頂点順を逆転させる。
FLIPPED_FACE_NAME = "Upper.Front"


def make_collection(
    collection_name: str,
    lesson_scene: bpy.types.Scene,
) -> bpy.types.Collection:
    """Collectionを作り、現在のSceneに所属させる。"""
    rocks_collection = bpy.data.collections.new(collection_name)
    lesson_scene.collection.children.link(rocks_collection)
    return rocks_collection


def make_rock_mesh(
    mesh_name: str,
    flipped_face_name: str | None = None,
) -> bpy.types.Mesh:
    """頂点座標とFace定義から、低ポリ岩のMeshを作る。"""
    face_vertex_indices: list[tuple[int, ...]] = []

    for face_name, outward_vertex_indices in ROCK_FACE_DEFINITIONS:
        if face_name == flipped_face_name:
            # 同じ頂点を逆順で結ぶと形と位置は同じまま、法線だけが反転する。
            face_vertex_indices.append(tuple(reversed(outward_vertex_indices)))
        else:
            face_vertex_indices.append(outward_vertex_indices)

    rock_mesh = bpy.data.meshes.new(mesh_name)
    # EdgeはFaceの輪郭から作られるため、第2引数は空のリストにする。
    rock_mesh.from_pydata(ROCK_VERTEX_COORDINATES, [], face_vertex_indices)
    rock_mesh.update()
    return rock_mesh


def mesh_counts(target_mesh: bpy.types.Mesh) -> tuple[int, int, int]:
    """Meshの頂点数、辺数、面数を同じ順番で返す。"""
    return (
        len(target_mesh.vertices),
        len(target_mesh.edges),
        len(target_mesh.polygons),
    )


def face_orientation_scores(target_mesh: bpy.types.Mesh) -> tuple[float, ...]:
    """各Face法線が岩の中心から外を向くほど正になる値を返す。"""
    rock_center = sum(
        (vertex.co for vertex in target_mesh.vertices),
        Vector((0.0, 0.0, 0.0)),
    ) / len(target_mesh.vertices)

    # Face中心へ向かうベクトルと法線の内積を取る。
    # 正: 外向き、負: 岩の中心側を向いた裏返しFace。
    return tuple(
        (polygon.center - rock_center).dot(polygon.normal)
        for polygon in target_mesh.polygons
    )


def print_face_orientations(
    rock_label: str,
    target_mesh: bpy.types.Mesh,
    orientation_scores: tuple[float, ...],
) -> None:
    """Face名、頂点番号、外向き判定をログへ表示する。"""
    print(f"{rock_label}:")
    for polygon, (face_name, _), score in zip(
        target_mesh.polygons,
        ROCK_FACE_DEFINITIONS,
        orientation_scores,
    ):
        # ROCK_FACE_DEFINITIONSの元値ではなく、このMeshへ実際に保存された順番を出す。
        actual_vertex_indices = tuple(polygon.vertices)
        direction = "OUT" if score > 0 else "IN"
        print(
            f"  face[{polygon.index}] {face_name}: "
            f"vertices={actual_vertex_indices} normal={direction} score={score:.3f}"
        )


# main()の処理の流れ
# ① Sceneを初期化し、観察用Collectionを作る。
# ② 9頂点と9面から、全Faceが外向きの岩Meshを作る。
# ③ 1面だけ頂点順を逆にした比較用の岩Meshを作る。
# ④ 2つのMeshを参照するObjectを作り、左右へ配置する。
# ⑤ 頂点・辺・面の数と、各Faceの法線方向をログへ表示する。
# ⑥ 左は全Faceが外向き、右は指定した1面だけ内向きか検査する。
# ⑦ 完成したSceneをoutput/08_vertices_rock.blendへ保存する。
def main() -> None:
    # ① Sceneを初期化し、観察用Collectionを作る。
    # Text Editorから実行する場合、現在の未保存作業は消えるので先に保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    rocks_collection = make_collection("VertexRocks", lesson_scene)

    # ② 左は、ROCK_FACE_DEFINITIONSの頂点順をそのまま使う正しいMesh。
    correct_rock_mesh = make_rock_mesh("Rock.Correct.Mesh")

    # ③ 右はUpper.Frontだけ頂点順を逆転し、意図的に裏向きFaceを作る。
    flipped_rock_mesh = make_rock_mesh(
        "Rock.FlippedFace.Mesh",
        flipped_face_name=FLIPPED_FACE_NAME,
    )

    # ④ Objectを作って初めてMeshがSceneに現れる。2つのMeshは別データ。
    correct_rock_object = bpy.data.objects.new("Rock.Correct", correct_rock_mesh)
    flipped_rock_object = bpy.data.objects.new(
        "Rock.FlippedFace", flipped_rock_mesh
    )
    rocks_collection.objects.link(correct_rock_object)
    rocks_collection.objects.link(flipped_rock_object)
    correct_rock_object.location = (-1.6, 0.0, 0.0)
    flipped_rock_object.location = (1.6, 0.0, 0.0)

    # Solid表示でもTopologyを追いやすいよう、すべてのEdgeを重ねて表示する。
    correct_rock_object.show_wire = True
    correct_rock_object.show_all_edges = True
    flipped_rock_object.show_wire = True
    flipped_rock_object.show_all_edges = True
    bpy.context.view_layer.update()

    # ⑤ Faceの位置と法線から、外向きか内向きかを数値でも確認する。
    correct_scores = face_orientation_scores(correct_rock_mesh)
    flipped_scores = face_orientation_scores(flipped_rock_mesh)

    print("=== 08 vertices rock ===")
    print(f"correct counts={mesh_counts(correct_rock_mesh)}")
    print_face_orientations("Rock.Correct", correct_rock_mesh, correct_scores)
    print(f"flipped counts={mesh_counts(flipped_rock_mesh)}")
    print_face_orientations("Rock.FlippedFace", flipped_rock_mesh, flipped_scores)

    # ⑥ どちらも同じ要素数。違いは1枚のFaceの頂点順と法線方向だけ。
    expected_counts = (9, 16, 9)
    if mesh_counts(correct_rock_mesh) != expected_counts:
        raise RuntimeError(f"正しい岩の要素数が違う: {mesh_counts(correct_rock_mesh)}")
    if mesh_counts(flipped_rock_mesh) != expected_counts:
        raise RuntimeError(
            f"比較用の岩の要素数が違う: {mesh_counts(flipped_rock_mesh)}"
        )

    inward_correct_faces = [
        ROCK_FACE_DEFINITIONS[index][0]
        for index, score in enumerate(correct_scores)
        if score <= 0
    ]
    inward_flipped_faces = [
        ROCK_FACE_DEFINITIONS[index][0]
        for index, score in enumerate(flipped_scores)
        if score <= 0
    ]
    if inward_correct_faces:
        raise RuntimeError(f"正しい岩に内向きFaceがある: {inward_correct_faces}")
    if inward_flipped_faces != [FLIPPED_FACE_NAME]:
        raise RuntimeError(
            f"比較用の裏向きFaceが想定と違う: {inward_flipped_faces}"
        )

    # Blenderで開いたとき、比較用の右Objectを見つけやすくする。
    flipped_rock_object.select_set(True)
    bpy.context.view_layer.objects.active = flipped_rock_object

    # ⑦ 2つのObjectと2つのMeshを保存する。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
