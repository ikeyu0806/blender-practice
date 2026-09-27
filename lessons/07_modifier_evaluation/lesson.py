"""レッスン07: 元のMeshとModifier評価後のMeshを比較する。

2つのObjectが同じ立方体Meshを共有し、片方のObjectだけにBevel Modifierを
追加する。元Meshを変更せずに、評価後の頂点・辺・面が増えることを観察する。
"""

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
BLEND_PATH = ROOT / "output" / "07_modifier_evaluation.blend"

# Widthは元の鋭いEdgeから、Bevelで置き換える範囲の広さ。
# Segmentsはその範囲の断面を何分割して曲線へ近づけるか。
BEVEL_WIDTH = 0.2
BEVEL_SEGMENTS = 3


def make_collection(
    collection_name: str,
    lesson_scene: bpy.types.Scene,
) -> bpy.types.Collection:
    """Collectionを作り、現在のSceneに所属させる。"""
    modifier_collection = bpy.data.collections.new(collection_name)
    lesson_scene.collection.children.link(modifier_collection)
    return modifier_collection


def make_source_cube_mesh(mesh_name: str) -> bpy.types.Mesh:
    """Modifier適用前の、8頂点・12辺・6面の立方体Meshを作る。"""
    source_mesh = bpy.data.meshes.new(mesh_name)
    source_bmesh = bmesh.new()
    bmesh.ops.create_cube(source_bmesh, size=2.0)
    source_bmesh.to_mesh(source_mesh)
    source_bmesh.free()
    source_mesh.update()
    return source_mesh


def mesh_counts(target_mesh: bpy.types.Mesh) -> tuple[int, int, int]:
    """Meshの頂点数、辺数、面数を同じ順番で返す。"""
    return (
        len(target_mesh.vertices),
        len(target_mesh.edges),
        len(target_mesh.polygons),
    )


def evaluated_mesh_counts(
    source_object: bpy.types.Object,
    dependency_graph: bpy.types.Depsgraph,
) -> tuple[int, int, int]:
    """ObjectへModifierを反映した一時Meshの頂点・辺・面数を返す。"""
    # Object.dataは元Meshを返す。evaluated_get()はModifierなどを計算した
    # Dependency Graph側のObjectを返すため、両者を混同しない。
    evaluated_object = source_object.evaluated_get(dependency_graph)
    evaluated_mesh = evaluated_object.to_mesh()
    try:
        # to_mesh()の結果は評価結果を読むための一時Mesh。
        # 数だけ通常のPythonタプルへコピーしてから解放する。
        return mesh_counts(evaluated_mesh)
    finally:
        # 一時Meshを使い終わったことをBlenderへ伝える。
        evaluated_object.to_mesh_clear()


# main()の処理の流れ
# ① Sceneを初期化し、観察用Collectionを作る。
# ② Modifier適用前の立方体Meshを1つ作る。
# ③ 2つのObjectから、同じ元Meshを参照させる。
# ④ 右側のObjectだけへBevel Modifierを追加する。
# ⑤ 元Meshと、2つのObjectの評価後Meshの要素数を比較する。
# ⑥ Mesh共有、Modifierの所属、評価結果が設計どおりか検査する。
# ⑦ 完成したSceneをoutput/07_modifier_evaluation.blendへ保存する。
def main() -> None:
    # ① Sceneを初期化し、観察用Collectionを作る。
    # Text Editorから実行する場合、現在の未保存作業は消えるので先に保存する。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    modifier_collection = make_collection("ModifierEvaluation", lesson_scene)

    # ② 保存される元Meshは1つだけ。Modifier評価後の形はここへ書き込まれない。
    source_cube_mesh = make_source_cube_mesh("Cube.Source.Mesh")

    # ③ Objectは別々なのでLocationとModifierを独立して持てるが、
    # Object.dataは両方とも同じsource_cube_meshを参照する。
    original_view_object = bpy.data.objects.new(
        "Cube.OriginalView", source_cube_mesh
    )
    bevel_view_object = bpy.data.objects.new("Cube.BevelView", source_cube_mesh)
    modifier_collection.objects.link(original_view_object)
    modifier_collection.objects.link(bevel_view_object)
    original_view_object.location = (-1.4, 0.0, 0.0)
    bevel_view_object.location = (1.4, 0.0, 0.0)

    # ④ ModifierはMeshではなくObjectのmodifier stackへ追加する。
    # そのため、共有Meshを使う左Objectは角張ったまま、右Objectだけが丸くなる。
    bevel_modifier = bevel_view_object.modifiers.new(
        name="Bevel.NonDestructive",
        type="BEVEL",
    )
    # Widthを大きくするほど、元の角から離れた位置まで削られて丸みが大きくなる。
    bevel_modifier.width = BEVEL_WIDTH

    # Segments=1は平らな斜面1枚の面取り。2以上にすると断面が分割され、
    # デフォルトのProfile=0.5の曲線へ近づく。値を増やすほど滑らかになるが、
    # 評価後Meshの頂点・辺・面も増える。
    bevel_modifier.segments = BEVEL_SEGMENTS

    # ANGLEは、隣り合うFaceの角度がしきい値を超えるEdgeだけを対象にする。
    # 立方体の12本のEdgeは90度なので、すべてBevelの対象になる。
    bevel_modifier.limit_method = "ANGLE"

    # Dependency Graphへ直前の変更を反映してから評価後Objectを取得する。
    bpy.context.view_layer.update()
    dependency_graph = bpy.context.evaluated_depsgraph_get()

    # ⑤ object.dataの元Meshと、Modifier計算後の一時Meshを別々に数える。
    source_counts = mesh_counts(source_cube_mesh)
    original_evaluated_counts = evaluated_mesh_counts(
        original_view_object, dependency_graph
    )
    bevel_evaluated_counts = evaluated_mesh_counts(bevel_view_object, dependency_graph)

    print("=== 07 modifier evaluation ===")
    print(
        f"source mesh={source_cube_mesh.name} users={source_cube_mesh.users} "
        f"vertices={source_counts[0]} edges={source_counts[1]} "
        f"faces={source_counts[2]}"
    )
    print(
        f"{original_view_object.name}: modifiers={len(original_view_object.modifiers)} "
        f"evaluated={original_evaluated_counts}"
    )
    print(
        f"{bevel_view_object.name}: modifiers={len(bevel_view_object.modifiers)} "
        f"evaluated={bevel_evaluated_counts}"
    )

    # ⑥ 元Meshは共有されたまま8頂点・12辺・6面で、左の評価結果も同じ。
    if original_view_object.data is not source_cube_mesh:
        raise RuntimeError("左Objectが元Meshを参照していない")
    if bevel_view_object.data is not source_cube_mesh:
        raise RuntimeError("右Objectが元Meshを参照していない")
    if source_cube_mesh.users != 2:
        raise RuntimeError(f"元Meshのusersが2ではない: {source_cube_mesh.users}")
    if source_counts != (8, 12, 6):
        raise RuntimeError(f"元Meshの要素数が違う: {source_counts}")
    if original_evaluated_counts != source_counts:
        raise RuntimeError("ModifierなしObjectの評価結果が元Meshと違う")
    if len(original_view_object.modifiers) != 0:
        raise RuntimeError("左Objectへ想定外のModifierが付いている")
    if len(bevel_view_object.modifiers) != 1:
        raise RuntimeError("右ObjectのModifier数が1ではない")
    if not all(
        evaluated_count > source_count
        for evaluated_count, source_count in zip(bevel_evaluated_counts, source_counts)
    ):
        raise RuntimeError(
            f"Bevel評価後の要素数が増えていない: {bevel_evaluated_counts}"
        )

    # Blenderで開いたとき、右ObjectのModifier Propertiesを確認しやすくする。
    bevel_view_object.select_set(True)
    bpy.context.view_layer.objects.active = bevel_view_object

    # ⑦ 保存されるのは元Mesh、2つのObject、右ObjectのModifier設定。
    # evaluated_mesh_counts()で読んだ一時Meshはデータブロックとして保存しない。
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"saved: {BLEND_PATH}")


if __name__ == "__main__":
    main()
