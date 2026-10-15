"""42以降のModifierレッスンで繰り返す、初期化と評価結果の読み取り。

各lesson.pyに残すのは、その回のModifierをどう設定し、何と比べるか。
元Meshを読む操作と、Modifier計算後の一時Meshを読む操作はここへまとめる。
"""

from pathlib import Path

import bmesh
import bpy
from mathutils import Vector


class EvaluatedSnapshot:
    """Modifier評価後の一時Meshからコピーした値。一時Mesh自体は保持しない。"""

    def __init__(self) -> None:
        self.vertex_count = 0
        self.edge_count = 0
        self.face_count = 0
        # to_mesh()の座標はObjectのローカル座標。Object.locationは含まれない。
        self.positions: list[Vector] = []
        self.world_positions: list[Vector] = []
        self.corner_normals: list[Vector] = []
        self.weights: dict[str, list[float]] = {}
        self.uvs: dict[str, list[Vector]] = {}


def begin(collection_name: str) -> tuple[bpy.types.Scene, bpy.types.Collection]:
    """未保存のSceneを消し、観察用CollectionをSceneへ所属させる。"""
    # Text Editorから実行すると、開いている未保存の作業も初期化される。
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lesson_scene = bpy.context.scene
    lesson_scene.unit_settings.system = "METRIC"
    lesson_scene.unit_settings.scale_length = 1.0
    modifiers_collection = bpy.data.collections.new(collection_name)
    # Collectionへの所属は、Objectの親子やMeshの共有とは別。
    lesson_scene.collection.children.link(modifiers_collection)
    return lesson_scene, modifiers_collection


def link_mesh_object(
    object_name: str,
    source_mesh: bpy.types.Mesh,
    modifiers_collection: bpy.types.Collection,
    location: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    """Meshを参照するObjectを作り、Collectionへ入れる。Meshの頂点は動かさない。"""
    mesh_object = bpy.data.objects.new(object_name, source_mesh)
    modifiers_collection.objects.link(mesh_object)
    mesh_object.location = location
    return mesh_object


def make_cube_mesh(mesh_name: str, size: float = 2.0) -> bpy.types.Mesh:
    """中心が原点の立方体Meshを作る。sizeは一辺の長さ。"""
    cube_mesh = bpy.data.meshes.new(mesh_name)
    cube_bmesh = bmesh.new()
    bmesh.ops.create_cube(cube_bmesh, size=size)
    cube_bmesh.to_mesh(cube_mesh)
    cube_bmesh.free()
    cube_mesh.update()
    return cube_mesh


def cube_object(
    object_name: str,
    modifiers_collection: bpy.types.Collection,
    size: float = 2.0,
    location: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    """立方体Meshと、それを参照するObjectを作る。"""
    cube_mesh = make_cube_mesh(f"{object_name}.Mesh", size)
    return link_mesh_object(object_name, cube_mesh, modifiers_collection, location)


def grid_object(
    object_name: str,
    modifiers_collection: bpy.types.Collection,
    x_segments: int,
    y_segments: int,
    size: float,
    location: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    """XY平面の格子Meshを作る。頂点を増やすModifierの入力に使う。"""
    grid_mesh = bpy.data.meshes.new(f"{object_name}.Mesh")
    grid_bmesh = bmesh.new()
    bmesh.ops.create_grid(
        grid_bmesh,
        x_segments=x_segments,
        y_segments=y_segments,
        size=size,
    )
    grid_bmesh.to_mesh(grid_mesh)
    grid_bmesh.free()
    grid_mesh.update()
    return link_mesh_object(object_name, grid_mesh, modifiers_collection, location)


def mesh_from_pydata(
    object_name: str,
    modifiers_collection: bpy.types.Collection,
    vertices: list[tuple[float, float, float]],
    edges: list[tuple[int, int]],
    faces: list[tuple[int, ...]],
    location: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    """頂点・辺・面を直接定義したMesh Objectを作る。"""
    source_mesh = bpy.data.meshes.new(f"{object_name}.Mesh")
    source_mesh.from_pydata(vertices, edges, faces)
    source_mesh.update()
    return link_mesh_object(object_name, source_mesh, modifiers_collection, location)


def empty_object(
    object_name: str,
    modifiers_collection: bpy.types.Collection,
    location: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    """形状を持たないEmpty。Modifierの目標位置として使う。"""
    empty = bpy.data.objects.new(object_name, None)
    empty.empty_display_type = "ARROWS"
    empty.empty_display_size = 0.3
    modifiers_collection.objects.link(empty)
    empty.location = location
    return empty


def active(target_object: bpy.types.Object) -> None:
    """Operatorが必要とするアクティブObjectを指定する。"""
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    target_object.select_set(True)
    bpy.context.view_layer.objects.active = target_object


def subdivide_mesh(source_mesh: bpy.types.Mesh, cuts: int) -> None:
    """既存Meshの辺を分割して頂点を増やす。ObjectのTransformは変えない。"""
    source_bmesh = bmesh.new()
    source_bmesh.from_mesh(source_mesh)
    bmesh.ops.subdivide_edges(
        source_bmesh,
        edges=list(source_bmesh.edges),
        cuts=cuts,
    )
    source_bmesh.to_mesh(source_mesh)
    source_bmesh.free()
    source_mesh.update()


def ensure_weight_group(
    mesh_object: bpy.types.Object,
    group_name: str,
    weight_for_vertex,
) -> bpy.types.VertexGroup:
    """全頂点を頂点グループへ入れ、元Mesh側のウェイトを記録する。"""
    vertex_group = mesh_object.vertex_groups.new(name=group_name)
    for vertex in mesh_object.data.vertices:
        vertex_group.add([vertex.index], float(weight_for_vertex(vertex)), "REPLACE")
    return vertex_group


def evaluated_snapshot(source_object: bpy.types.Object) -> EvaluatedSnapshot:
    """元Meshではなく、Modifier計算後の一時Meshから数と座標をコピーする。"""
    # Object.dataは保存される元データ。evaluated_get()はDependency Graph側。
    bpy.context.view_layer.update()
    dependency_graph = bpy.context.evaluated_depsgraph_get()
    evaluated_object = source_object.evaluated_get(dependency_graph)
    evaluated_mesh = evaluated_object.to_mesh()
    snapshot = EvaluatedSnapshot()
    try:
        snapshot.vertex_count = len(evaluated_mesh.vertices)
        snapshot.edge_count = len(evaluated_mesh.edges)
        snapshot.face_count = len(evaluated_mesh.polygons)
        snapshot.positions = [vertex.co.copy() for vertex in evaluated_mesh.vertices]
        snapshot.world_positions = [
            source_object.matrix_world @ position for position in snapshot.positions
        ]
        snapshot.corner_normals = [
            Vector(corner_normal.vector)
            for corner_normal in evaluated_mesh.corner_normals
        ]
        group_names = {
            group.index: group.name for group in evaluated_object.vertex_groups
        }
        for group_name in group_names.values():
            snapshot.weights[group_name] = [0.0] * snapshot.vertex_count
        for vertex in evaluated_mesh.vertices:
            for element in vertex.groups:
                group_name = group_names.get(element.group)
                if group_name is not None:
                    snapshot.weights[group_name][vertex.index] = element.weight
        for uv_layer in evaluated_mesh.uv_layers:
            snapshot.uvs[uv_layer.name] = [
                Vector(loop_uv.uv) for loop_uv in uv_layer.data
            ]
        return snapshot
    finally:
        # 一時Meshは数をコピーしたあと解放する。保存されるデータブロックではない。
        evaluated_object.to_mesh_clear()


def source_weights(source_object: bpy.types.Object, group_name: str) -> list[float]:
    """Object.dataに保存されている頂点グループのウェイト。評価後とは別に読む。"""
    vertex_group = source_object.vertex_groups[group_name]
    weights = []
    for vertex in source_object.data.vertices:
        weight = 0.0
        for element in vertex.groups:
            if element.group == vertex_group.index:
                weight = element.weight
        weights.append(weight)
    return weights


def span(values: list[float]) -> float:
    """座標成分の最大と最小の差。空なら0。"""
    if not values:
        return 0.0
    return max(values) - min(values)


def save_blend(blend_path: Path, active_object: bpy.types.Object) -> None:
    """開いたときにModifier Propertiesを見られるObjectを選んで保存する。"""
    active(active_object)
    blend_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"saved: {blend_path}")
