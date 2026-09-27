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


def make_collection(name: str, scene: bpy.types.Scene) -> bpy.types.Collection:
    """レッスン03と同じく、Collection を作って Scene に所属させる。"""
    collection = bpy.data.collections.new(name)
    scene.collection.children.link(collection)
    return collection


def add_box(
    bm: bmesh.types.BMesh,
    center: tuple[float, float, float],
    size: tuple[float, float, float],
) -> None:
    """単位立方体の頂点を拡大・移動し、1枚の厚みのある板にする。"""
    # create_cube の戻り値にある verts は、今作った箱の8頂点だけ。
    # bm 全体の頂点を動かすと、先に配置した板も再度動いてしまう。
    new_vertices = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    for vertex in new_vertices:
        vertex.co.x = vertex.co.x * size[0] + center[0]
        vertex.co.y = vertex.co.y * size[1] + center[1]
        vertex.co.z = vertex.co.z * size[2] + center[2]


def make_crate_mesh() -> bpy.types.Mesh:
    """底板と4枚の側板を、1つの Mesh データブロックに組み立てる。"""
    mesh = bpy.data.meshes.new("CrateBoards")
    bm = bmesh.new()

    # 幅・奥行きは2、高さは1.4、板の厚さは0.12。
    # 底板の下面をローカル Z=0 に合わせる。Object の原点はローカル (0,0,0)
    # なので、この配置により原点が「木箱の底面中央」になる。
    add_box(bm, center=(0.0, 0.0, 0.06), size=(2.0, 2.0, 0.12))

    # 側板は底板の上端 Z=0.12 から上端 Z=1.4 まで伸ばす。
    # X 側の2枚は奥行き2、Y 側の2枚は角で重ならないよう幅1.76。
    wall_z = (0.12 + 1.4) / 2
    wall_height = 1.4 - 0.12
    for x in (-0.94, 0.94):
        add_box(bm, center=(x, 0.0, wall_z), size=(0.12, 2.0, wall_height))
    for y in (-0.94, 0.94):
        add_box(bm, center=(0.0, y, wall_z), size=(1.76, 0.12, wall_height))

    # 5つの箱状の板は別々の閉じた部分だが、保存先は1つの Mesh。
    # Object Mode では木箱全体を1つの Object として移動できる。
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return mesh


def make_ground_mesh() -> bpy.types.Mesh:
    """上面がワールド Z=0 に来る、薄い地面を作る。"""
    mesh = bpy.data.meshes.new("GroundMesh")
    bm = bmesh.new()
    add_box(bm, center=(0.0, 0.0, -0.05), size=(8.0, 4.0, 0.1))
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return mesh


def bottom_z(obj: bpy.types.Object) -> float:
    """Mesh 頂点をワールド座標へ変換し、最も低い高さを読む。"""
    # obj.location.z だけでは形状の下面は分からない。
    # matrix_world で Object の移動も反映した頂点位置を調べる。
    return min((obj.matrix_world @ vertex.co).z for vertex in obj.data.vertices)


def main() -> None:
    # 再実行で同じシーンを作る。Text Editor から実行する場合は、現在の
    # 未保存の作業が消えるので、先に別の .blend に保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    crates = make_collection("Crates", scene)
    environment = make_collection("Environment", scene)

    # objects.new() は Object データブロックを作るだけで、まだ Scene には出ない。
    # 第2引数の Mesh を Object.data として参照させる。
    ground = bpy.data.objects.new("Ground", make_ground_mesh())
    # Collection へ link して、初めてこの Scene の構成要素として表示される。
    environment.objects.link(ground)
    crate_mesh = make_crate_mesh()

    # objects.new(name, object_data) の第2引数に同じ crate_mesh を渡す。
    # これが「2つの Object が1つの Meshを共有する」関係を作る。
    # この時点では Object データブロックを作っただけで、Scene にはまだ出ない。
    crate_a = bpy.data.objects.new("Crate.A", crate_mesh)
    crate_b = bpy.data.objects.new("Crate.B", crate_mesh)

    # ここでの link は Object 同士をつなぐ操作ではない。
    # 各 Object を Crates Collection に所属させ、Scene から見えるようにする。
    crates.objects.link(crate_a)
    crates.objects.link(crate_b)

    # Location は Mesh ではなく各 Object が持つ。そのため、同じ形を共有しても
    # Crate.A と Crate.B を別々の場所に置ける。
    crate_a.location = (-1.5, 0.0, 0.0)
    crate_b.location = (1.5, 0.0, CRATE_B_Z)

    # 変更した配置を依存関係グラフへ反映し、matrix_world を最新にする。
    bpy.context.view_layer.update()

    print("=== 04 crate origin ===")
    print(f"mesh local bottom={min(vertex.co.z for vertex in crate_mesh.vertices):.3f}")
    for crate in (crate_a, crate_b):
        print(
            f"{crate.name} origin_z={crate.matrix_world.translation.z:.3f} "
            f"bottom_z={bottom_z(crate):.3f} collection={crate.users_collection[0].name}"
        )
    print(f"ground top_z={max(vertex.co.z for vertex in ground.data.vertices):.3f}")

    # 原点と Mesh の底面が一致しているか、保存前に確かめる。
    if len(crate_mesh.vertices) != 40 or len(crate_mesh.polygons) != 30:
        raise RuntimeError("5枚の板（各8頂点・6面）が作られていない")
    if not isclose(min(vertex.co.z for vertex in crate_mesh.vertices), 0.0, abs_tol=1e-6):
        raise RuntimeError("木箱のローカル底面が原点 Z=0 にない")
    if crate_a.data is not crate_b.data or crate_mesh.users != 2:
        raise RuntimeError("2つの木箱が Mesh を共有していない")
    for crate in (crate_a, crate_b):
        if not isclose(bottom_z(crate), crate.location.z, abs_tol=1e-6):
            raise RuntimeError(f"原点と底面の高さが違う: {crate.name}")
    if not isclose(max(vertex.co.z for vertex in ground.data.vertices), 0.0, abs_tol=1e-6):
        raise RuntimeError("地面の上面が Z=0 にない")

    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
