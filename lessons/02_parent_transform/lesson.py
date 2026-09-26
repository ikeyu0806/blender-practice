"""レッスン02: 親の位置によって子のワールド位置が変わる。

同じフォルダの README.md に、画面での観察方法と変更実験を書く。
前回の Mesh 共有を再利用しつつ、今回は Transform と親子に注目する。
"""

from collections.abc import Iterable
from pathlib import Path

import bmesh
import bpy


def lesson_path() -> Path:
    """Blender の --python と Text Editor の両方でソースの場所を得る。"""
    file_attr = globals().get("__file__")
    if file_attr:
        return Path(file_attr).resolve()

    text = getattr(bpy.context.space_data, "text", None)
    if text and text.filepath:
        return Path(bpy.path.abspath(text.filepath)).resolve()
    raise RuntimeError("lesson.py を保存してから Run Script するか、Blender の --python で実行する")


# lesson.py → 02_parent_transform/ → lessons/ → プロジェクト直下。
ROOT = lesson_path().parents[2]
BLEND_PATH = ROOT / "output" / "02_parent_transform.blend"


def make_cube_mesh() -> bpy.types.Mesh:
    """前回と同じ形の Mesh を1つ作る。今回の主題は形ではなく配置。"""
    mesh = bpy.data.meshes.new("SharedCube")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.8)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


def make_parent_and_child(
    label: str, parent_x: float, mesh: bpy.types.Mesh, scene: bpy.types.Scene
) -> tuple[bpy.types.Object, bpy.types.Object]:
    """親 Empty と子 Cube を作り、子のローカル X を1に固定する。"""
    # Empty は形状データを持たない Object。親として Transform だけを使う。
    parent = bpy.data.objects.new(f"Parent.{label}", None)
    parent.empty_display_type = "PLAIN_AXES"
    parent.empty_display_size = 0.6
    parent.location = (parent_x, 0.0, 0.0)
    scene.collection.objects.link(parent)

    # 子は前回と同じ Mesh を参照する。Object 自体は親ごとに別々。
    child = bpy.data.objects.new(f"Cube.{label}", mesh)
    scene.collection.objects.link(child)

    # 親を先に設定し、その後に location を入れる。
    # この例では Parent Inverse が初期値のままなので、子の location は
    # 親の原点から見た位置として読める。両方の子を同じ (1, 0, 0) にする。
    child.parent = parent
    child.location = (1.0, 0.0, 0.0)
    return parent, child


def xyz(values: Iterable[float]) -> tuple[float, float, float]:
    """ログで読みやすいよう、3成分を小数3桁に丸める。"""
    return tuple(round(float(value), 3) for value in values)


def main() -> None:
    # 毎回同じ結果にするため現在の .blend を初期化する。
    # 未保存の作業は消えるので、GUI で実行する前に別途保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mesh = make_cube_mesh()

    parent_a, child_a = make_parent_and_child("A", -2.0, mesh, scene)
    parent_b, child_b = make_parent_and_child("B", 2.0, mesh, scene)

    # 親子の変更を評価してから matrix_world を読む。
    # location は子のローカル位置、matrix_world.translation は最終的な位置。
    bpy.context.view_layer.update()
    print("=== 02 parent transform ===")
    for parent, child in ((parent_a, child_a), (parent_b, child_b)):
        print(
            f"{parent.name} world={xyz(parent.matrix_world.translation)} -> "
            f"{child.name} local={xyz(child.location)} "
            f"world={xyz(child.matrix_world.translation)}"
        )

    # 回転・拡大・Parent Inverse の補正がない今回の例では、
    # 子の world X = 親の world X + 子の local X になる。
    for parent, child in ((parent_a, child_a), (parent_b, child_b)):
        if child.parent is not parent or xyz(child.location) != (1.0, 0.0, 0.0):
            raise RuntimeError(f"親子またはローカル位置が想定と違う: {child.name}")
        expected_world = xyz(parent.matrix_world.translation + child.location)
        if xyz(child.matrix_world.translation) != expected_world:
            raise RuntimeError(f"ワールド位置が想定と違う: {child.name}")
    if xyz(child_a.matrix_world.translation) == xyz(child_b.matrix_world.translation):
        raise RuntimeError("親が違うのに子が同じワールド位置になっている")
    if child_a.data is not child_b.data or mesh.users != 2:
        raise RuntimeError("前回の共有 Mesh が維持されていない")

    # lesson.py は教材、output/*.blend は実行結果として分ける。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
