"""レッスン01: 1つの Mesh を2つの Object で共有する。

実行方法と観察課題は同じフォルダの README.md を参照する。
このファイルを読むときは「データを作る → シーンにつなぐ → 関係を調べる」
という順番に注目する。Unity なら1つの Mesh アセットを2つの
GameObject が参照する状態に近い。
"""

from pathlib import Path

import bmesh
import bpy


def lesson_path() -> Path:
    """実行中のレッスンファイルの場所を返す。"""
    # コマンドラインの --python なら __file__ が使える。
    file_attr = globals().get("__file__")
    if file_attr:
        return Path(file_attr).resolve()

    # Text Editor の Run Script では、開いているテキストの保存先を使う。
    # 未保存のテキストには場所がないため、README に従って先に保存する。
    space = bpy.context.space_data
    text = getattr(space, "text", None)
    if text and text.filepath:
        return Path(bpy.path.abspath(text.filepath)).resolve()
    raise RuntimeError(
        "スクリプトの場所が分からない。"
        "ターミナルから --python で実行するか、Text Editor でこのファイルを開いてから実行する。"
    )


# lesson.py → 01_shared_mesh/ → lessons/ → プロジェクト直下。
# レッスンをサブフォルダに入れたので parents[2] まで戻る。
ROOT = lesson_path().parents[2]
OUTPUT = ROOT / "output"
BLEND_PATH = OUTPUT / "01_shared_mesh.blend"


def main() -> None:
    # 再実行するたびに同じ結果を作る。開いている未保存の作業は消えるので、
    # 実行前に別の .blend を保存しておく。シーン全体の初期化には operator を使う。
    # 以降は選択状態・編集モードに左右されにくいデータ API を使う。
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Mesh は頂点・辺・面を持つデータブロック。ここではまだ画面に現れない。
    mesh = bpy.data.meshes.new("SharedCube")
    # bmesh は編集中の形状を組み立てる一時的な入れ物。
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # 完成した形状を Blender の Mesh に書き込み、一時データを解放する。
    bm.to_mesh(mesh)
    bm.free()

    # Object は位置などの Transform と参照先データを持つ。
    # 2つ目の Object に同じ mesh を渡すのが、このレッスンの中心。
    # mesh.copy() を渡すと別 Mesh になり、共有ではなくなる。
    cube_a = bpy.data.objects.new("Cube.A", mesh)
    cube_b = bpy.data.objects.new("Cube.B", mesh)
    # Object ごとに Transform は独立。Mesh を共有していても別の位置に置ける。
    # 親がないので、この段階の location はワールド座標と一致する。
    cube_b.location = (2.0, 0.0, 0.0)

    # bpy.data.objects.new() は Object を作るだけ。シーンに表示するには
    # Collection へ link する必要がある。この link は Mesh の共有とは別。
    scene = bpy.data.scenes[0]
    scene.collection.objects.link(cube_a)
    scene.collection.objects.link(cube_b)

    print_report(mesh, cube_a, cube_b)

    # users は「この Mesh を参照するデータブロック数」。今回は2つの Object。
    # is は名前や形状の一致ではなく、同一の Mesh インスタンスかを調べる。
    if mesh.users != 2 or cube_a.data is not cube_b.data:
        raise SystemExit(
            f"共有になっていない: users={mesh.users} same={cube_a.data is cube_b.data}"
        )

    # 生成物はソースから分離する。output/ は Git 管理の対象外。
    OUTPUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


def print_report(mesh: bpy.types.Mesh, cube_a: bpy.types.Object, cube_b: bpy.types.Object) -> None:
    """Outliner で見えるデータの関係を数値でも確かめる。"""
    print("=== 01 shared mesh ===")
    print(f"Mesh '{mesh.name}' vertices={len(mesh.vertices)} users={mesh.users}")
    for obj in (cube_a, cube_b):
        loc = tuple(round(v, 3) for v in obj.location)
        print(f"  Object '{obj.name}' location={loc} mesh='{obj.data.name}'")
    print(f"same mesh: {cube_a.data is cube_b.data}")


if __name__ == "__main__":
    main()
