"""レッスン04: 板5枚で木箱を作り、底面中央を Object の原点にする。

実行後は README の手順で Crate.A / Crate.B の Location と接地を比べる。
今回は色や質感を使わず、Mesh 内の頂点座標と Object の Location に集中する。
"""

from math import isclose
from pathlib import Path

import bmesh
import bpy


def lesson_path() -> Path:
    """--python と Blender Text Editor のどちらでも教材の場所を得る。"""
    file_attr = globals().get("__file__")
    if file_attr:
        return Path(file_attr).resolve()
    text = getattr(bpy.context.space_data, "text", None)
    if text and text.filepath:
        return Path(bpy.path.abspath(text.filepath)).resolve()
    raise RuntimeError("lesson.py を保存して Run Script するか、Blender の --python で実行する")


ROOT = lesson_path().parents[2]
BLEND_PATH = ROOT / "output" / "04_crate_origin.blend"

# 変更実験: 0.5 にすると Crate.B だけ地面から 0.5 浮く。
# Mesh の頂点は変更せず、Object の Location だけを変える。
CRATE_B_Z = 0.0


def make_collection(
    collection_name: str,
    lesson_scene: bpy.types.Scene,
) -> bpy.types.Collection:
    """レッスン03と同じく、Collection を作って Scene に所属させる。"""
    new_collection = bpy.data.collections.new(collection_name)
    lesson_scene.collection.children.link(new_collection)
    return new_collection


def add_box(
    target_bmesh: bmesh.types.BMesh,
    center: tuple[float, float, float],
    size: tuple[float, float, float],
) -> None:
    """単位立方体の頂点を拡大・移動し、1枚の厚みのある板にする。"""
    # create_cube の戻り値にある verts は、今作った箱の8頂点だけ。
    # target_bmesh 全体を動かすと、先に配置した板も再度動いてしまう。
    new_vertices = bmesh.ops.create_cube(target_bmesh, size=1.0)["verts"]
    for vertex in new_vertices:
        vertex.co.x = vertex.co.x * size[0] + center[0]
        vertex.co.y = vertex.co.y * size[1] + center[1]
        vertex.co.z = vertex.co.z * size[2] + center[2]


def make_crate_mesh() -> bpy.types.Mesh:
    """底板と4枚の側板を、1つの Mesh データブロックに組み立てる。"""
    crate_mesh = bpy.data.meshes.new("CrateBoards")
    crate_bmesh = bmesh.new()

    # 幅・奥行きは2、高さは1.4、板の厚さは0.12。
    # 底板の下面をローカル Z=0 に合わせる。Object の原点はローカル (0,0,0)
    # なので、この配置により原点が「木箱の底面中央」になる。
    add_box(crate_bmesh, center=(0.0, 0.0, 0.06), size=(2.0, 2.0, 0.12))

    # 側板は底板の上端 Z=0.12 から上端 Z=1.4 まで伸ばす。
    # X 側の2枚は奥行き2、Y 側の2枚は角で重ならないよう幅1.76。
    wall_z = (0.12 + 1.4) / 2
    wall_height = 1.4 - 0.12
    for x in (-0.94, 0.94):
        add_box(crate_bmesh, center=(x, 0.0, wall_z), size=(0.12, 2.0, wall_height))
    for y in (-0.94, 0.94):
        add_box(crate_bmesh, center=(0.0, y, wall_z), size=(1.76, 0.12, wall_height))

    # 5つの箱状の板は別々の閉じた部分だが、保存先は1つの Mesh。
    # Object Mode では木箱全体を1つの Object として移動できる。
    crate_bmesh.to_mesh(crate_mesh)
    crate_bmesh.free()
    crate_mesh.update()
    return crate_mesh


def make_ground_mesh() -> bpy.types.Mesh:
    """上面がワールド Z=0 に来る、薄い地面を作る。"""
    ground_mesh = bpy.data.meshes.new("GroundMesh")
    ground_bmesh = bmesh.new()
    add_box(ground_bmesh, center=(0.0, 0.0, -0.05), size=(8.0, 4.0, 0.1))
    ground_bmesh.to_mesh(ground_mesh)
    ground_bmesh.free()
    ground_mesh.update()
    return ground_mesh


def world_bottom_z(mesh_object: bpy.types.Object) -> float:
    """Mesh 頂点をワールド座標へ変換し、最も低い高さを読む。"""
    # mesh_object.location.z だけでは形状の下面は分からない。
    # matrix_world で Object の移動も反映した頂点位置を調べる。
    return min(
        (mesh_object.matrix_world @ vertex.co).z
        for vertex in mesh_object.data.vertices
    )


# main() の処理の流れ
# ① Scene を初期化し、Crates と Environment の Collection を作る。
# ② 地面の Mesh と Object を作り、Environment Collection に所属させる。
# ③ 木箱の共有 Mesh と2つの Object を作り、Crates Collection に所属させる。
# ④ 2つの木箱 Object に別々の Location を設定し、配置の計算を更新する。
# ⑤ 原点、底面、Collection、地面の高さをログへ表示する。
# ⑥ 頂点・面の数、接地、Mesh共有などが設計どおりか検査する。
# ⑦ 完成した Scene を output/04_crate_origin.blend に保存する。
def main() -> None:
    # ① Sceneを初期化し、2つのCollectionを作る。
    # 再実行で同じSceneを作る。Text Editorから実行する場合は、現在の
    # 未保存の作業が消えるので、先に別の.blendへ保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    crates_collection = make_collection("Crates", lesson_scene)
    environment_collection = make_collection("Environment", lesson_scene)

    # ② 地面のMeshとObjectを作り、Environment Collectionへ所属させる。
    # objects.new() は Object データブロックを作るだけで、まだ Scene には出ない。
    # 第2引数の Mesh を Object.data として参照させる。
    ground_object = bpy.data.objects.new("Ground", make_ground_mesh())
    # Collection へ link して、初めてこの Scene の構成要素として表示される。
    environment_collection.objects.link(ground_object)

    # ③ 共有する木箱Meshと2つのObjectを作り、Crates Collectionへ所属させる。
    crate_mesh = make_crate_mesh()

    # objects.new(name, object_data) の第2引数に同じ crate_mesh を渡す。
    # これが「2つの Object が1つの Meshを共有する」関係を作る。
    # この時点では Object データブロックを作っただけで、Scene にはまだ出ない。
    crate_a_object = bpy.data.objects.new("Crate.A", crate_mesh)
    crate_b_object = bpy.data.objects.new("Crate.B", crate_mesh)

    # ここでの link は Object 同士をつなぐ操作ではない。
    # 各 Object を Crates Collection に所属させ、Scene から見えるようにする。
    crates_collection.objects.link(crate_a_object)
    crates_collection.objects.link(crate_b_object)

    # ④ 木箱ObjectごとにLocationを設定し、配置の計算を更新する。
    # Location は Mesh ではなく各 Object が持つ。そのため、同じ形を共有しても
    # Crate.A と Crate.B を別々の場所に置ける。
    crate_a_object.location = (-1.5, 0.0, 0.0)
    crate_b_object.location = (1.5, 0.0, CRATE_B_Z)

    # 変更した配置を依存関係グラフへ反映し、matrix_world を最新にする。
    bpy.context.view_layer.update()

    # ⑤ 原点、底面、Collection、地面の高さをログへ表示する。
    print("=== 04 crate origin ===")
    print(f"mesh local bottom={min(vertex.co.z for vertex in crate_mesh.vertices):.3f}")
    for crate_object in (crate_a_object, crate_b_object):
        print(
            f"{crate_object.name} origin_z={crate_object.matrix_world.translation.z:.3f} "
            f"bottom_z={world_bottom_z(crate_object):.3f} "
            f"collection={crate_object.users_collection[0].name}"
        )
    print(
        f"ground top_z={max(vertex.co.z for vertex in ground_object.data.vertices):.3f}"
    )

    # ⑥ 頂点・面の数、接地、Mesh共有などが設計どおりか検査する。
    # 原点と Mesh の底面が一致しているか、保存前に確かめる。
    if len(crate_mesh.vertices) != 40 or len(crate_mesh.polygons) != 30:
        raise RuntimeError("5枚の板（各8頂点・6面）が作られていない")
    if not isclose(min(vertex.co.z for vertex in crate_mesh.vertices), 0.0, abs_tol=1e-6):
        raise RuntimeError("木箱のローカル底面が原点 Z=0 にない")
    if crate_a_object.data is not crate_b_object.data or crate_mesh.users != 2:
        raise RuntimeError("2つの木箱が Mesh を共有していない")
    for crate_object in (crate_a_object, crate_b_object):
        if not isclose(
            world_bottom_z(crate_object), crate_object.location.z, abs_tol=1e-6
        ):
            raise RuntimeError(f"原点と底面の高さが違う: {crate_object.name}")
    if not isclose(
        max(vertex.co.z for vertex in ground_object.data.vertices), 0.0, abs_tol=1e-6
    ):
        raise RuntimeError("地面の上面が Z=0 にない")

    # ⑦ 完成したSceneを.blendへ保存する。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
