"""共有メッシュ

今日分かること:
    Object は Mesh を参照する入れ物である。
    Mesh は1つ、Object は2つ作れる。見た目が2つでもデータは1つ。
    mesh.users は、その Mesh を参照しているデータブロックの数。

Unity でいうと:
    同じ Mesh アセットを参照する GameObject を2つ置いた状態。

実行（GUI で結果を見る）:
    /Applications/Blender.app/Contents/MacOS/Blender --python lessons/01_shared_mesh.py

実行（保存だけ確認する）:
    /Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/01_shared_mesh.py
"""

from pathlib import Path

import bmesh
import bpy


def lesson_path() -> Path:
    """ターミナルの --python でも、Text Editor の Run Script でも場所が取れる。"""
    file_attr = globals().get("__file__")
    if file_attr:
        return Path(file_attr).resolve()
    space = bpy.context.space_data
    text = getattr(space, "text", None)
    if text and text.filepath:
        return Path(bpy.path.abspath(text.filepath)).resolve()
    raise RuntimeError(
        "スクリプトの場所が分からない。"
        "ターミナルから --python で実行するか、Text Editor でこのファイルを開いてから実行する。"
    )


ROOT = lesson_path().parent.parent
OUTPUT = ROOT / "output"
BLEND_PATH = OUTPUT / "01_shared_mesh.blend"


def main() -> None:
    # ファイルを空にする操作だけオペレーターを使う。
    # 以降の作成はデータ API。選択やモードに依存しない。
    bpy.ops.wm.read_factory_settings(use_empty=True)

    mesh = bpy.data.meshes.new("SharedCube")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    cube_a = bpy.data.objects.new("Cube.A", mesh)
    cube_b = bpy.data.objects.new("Cube.B", mesh)
    # 親はまだいないので、location はこの時点ではワールド座標と同じ。
    cube_b.location = (2.0, 0.0, 0.0)

    scene = bpy.data.scenes[0]
    scene.collection.objects.link(cube_a)
    scene.collection.objects.link(cube_b)

    print_report(mesh, cube_a, cube_b)

    if mesh.users != 2 or cube_a.data is not cube_b.data:
        raise SystemExit(
            f"共有になっていない: users={mesh.users} same={cube_a.data is cube_b.data}"
        )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


def print_report(mesh: bpy.types.Mesh, cube_a: bpy.types.Object, cube_b: bpy.types.Object) -> None:
    print("=== 01 shared mesh ===")
    print(f"Mesh '{mesh.name}' vertices={len(mesh.vertices)} users={mesh.users}")
    for obj in (cube_a, cube_b):
        loc = tuple(round(v, 3) for v in obj.location)
        print(f"  Object '{obj.name}' location={loc} mesh='{obj.data.name}'")
    print(f"same mesh: {cube_a.data is cube_b.data}")


if __name__ == "__main__":
    main()
