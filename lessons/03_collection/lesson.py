"""レッスン03: Collection の所属と Object の親子関係を区別する。

README の予測課題を読んでから実行する。
Cube.B を右の Collection から左へ移しても、親とワールド位置は変わらない。
"""

from collections.abc import Iterable
from pathlib import Path

import bmesh
import bpy


def lesson_path() -> Path:
    """コマンドライン実行と Blender の Text Editor 実行で、この教材の場所を得る。"""
    file_attr = globals().get("__file__")
    if file_attr:
        return Path(file_attr).resolve()

    text = getattr(bpy.context.space_data, "text", None)
    if text and text.filepath:
        return Path(bpy.path.abspath(text.filepath)).resolve()
    raise RuntimeError("lesson.py を保存して Run Script するか、Blender の --python で実行する")


ROOT = lesson_path().parents[2]
BLEND_PATH = ROOT / "output" / "03_collection.blend"

# 実験用: False にすると、Cube.B を左右両方の Collection に所属させる。
# これを変えても親子と位置は変わらないはず、と予測してから実行する。
MOVE_INSTEAD_OF_LINK = True


def make_collection(name: str, scene: bpy.types.Scene) -> bpy.types.Collection:
    """新しい Collection を作り、シーン内から使えるようにつなぐ。"""
    collection = bpy.data.collections.new(name)
    # 作っただけでは Scene Collection の下に現れない。
    scene.collection.children.link(collection)
    return collection


def make_cube_mesh() -> bpy.types.Mesh:
    """01・02 と同じく、2つの Object から参照する立方体 Mesh を1つ作る。"""
    mesh = bpy.data.meshes.new("SharedCube")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.8)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


def make_parent_and_cube(
    label: str,
    parent_x: float,
    mesh: bpy.types.Mesh,
    scene: bpy.types.Scene,
    collection: bpy.types.Collection,
) -> tuple[bpy.types.Object, bpy.types.Object]:
    """親はシーン直下、子は指定した Collection に置く。"""
    parent = bpy.data.objects.new(f"Parent.{label}", None)
    parent.empty_display_type = "PLAIN_AXES"
    parent.empty_display_size = 0.6
    parent.location = (parent_x, 0.0, 0.0)
    scene.collection.objects.link(parent)

    child = bpy.data.objects.new(f"Cube.{label}", mesh)
    collection.objects.link(child)
    # Collection への所属とは別に、親子は Object の parent プロパティで決まる。
    child.parent = parent
    child.location = (1.0, 0.0, 0.0)
    return parent, child


def xyz(values: Iterable[float]) -> tuple[float, float, float]:
    """ログで見比べやすい3成分の位置へ変換する。"""
    return tuple(round(float(value), 3) for value in values)


def collection_names(obj: bpy.types.Object) -> tuple[str, ...]:
    """Object が直接所属する Collection 名を安定した順で返す。"""
    return tuple(sorted(collection.name for collection in obj.users_collection))


def describe(label: str, obj: bpy.types.Object) -> None:
    """所属・親・ローカル位置・ワールド位置を同じ行で見比べる。"""
    print(
        f"{label}: {obj.name} collections={collection_names(obj)} "
        f"parent={obj.parent.name if obj.parent else None} "
        f"local={xyz(obj.location)} world={xyz(obj.matrix_world.translation)}"
    )


def main() -> None:
    # 毎回同じ状態から作る。GUI の Text Editor で実行する場合、未保存の作業は
    # 消えるため先に別の .blend として保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    left = make_collection("Props.Left", scene)
    right = make_collection("Props.Right", scene)
    mesh = make_cube_mesh()

    parent_a, cube_a = make_parent_and_cube("A", -2.0, mesh, scene, left)
    parent_b, cube_b = make_parent_and_cube("B", 2.0, mesh, scene, right)
    bpy.context.view_layer.update()

    # 移動前の状態を記録する。01・02 と同じ位置と Mesh 共有が出発点。
    before_world = xyz(cube_b.matrix_world.translation)
    before_parent = cube_b.parent
    print("=== 03 Collection ===")
    describe("before", cube_a)
    describe("before", cube_b)

    # Collection.objects.link は所属先を1つ追加するだけ。自動では前の所属を外さない。
    # ここで Cube.B は一時的に左右両方に所属するが、Object は複製されない。
    left.objects.link(cube_b)
    if MOVE_INSTEAD_OF_LINK:
        # 「移動」にしたい場合だけ元の Collection から外す。
        right.objects.unlink(cube_b)
    bpy.context.view_layer.update()
    describe("after ", cube_b)

    expected_collections = ("Props.Left",) if MOVE_INSTEAD_OF_LINK else ("Props.Left", "Props.Right")
    if collection_names(cube_a) != ("Props.Left",) or collection_names(cube_b) != expected_collections:
        raise RuntimeError("Collection の所属が想定と違う")
    if cube_b.parent is not before_parent or cube_b.parent is not parent_b:
        raise RuntimeError("Collection の変更で親子関係が変わった")
    if xyz(cube_b.matrix_world.translation) != before_world:
        raise RuntimeError("Collection の変更でワールド位置が変わった")
    if xyz(cube_a.matrix_world.translation) != (-1.0, 0.0, 0.0) or before_world != (3.0, 0.0, 0.0):
        raise RuntimeError("親子による位置が想定と違う")
    if cube_a.parent is not parent_a or cube_a.data is not cube_b.data or mesh.users != 2:
        raise RuntimeError("前のレッスンの親子または Mesh 共有が維持されていない")
    if len(bpy.data.objects) != 4:
        raise RuntimeError("Collection の変更で Object が増減した")

    # ソース lesson.py と実行結果 .blend は別。再実行すると同じ出力先を作り直す。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
