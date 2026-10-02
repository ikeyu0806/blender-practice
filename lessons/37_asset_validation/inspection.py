"""閉じた小物用の検査。importしてもSceneを初期化しない。"""

from pathlib import Path
import bmesh
import bpy


def inspect_asset(
    asset_object: bpy.types.Object, max_dimension: float = 2.0
) -> list[str]:
    # この規則は閉じた小物用。開いた地形・服は別の規則で検査する。
    problems = []
    if not asset_object.name.startswith("Asset."):
        problems.append("name: expected Asset. prefix")
    if any(abs(value - 1) > 1e-5 for value in asset_object.scale):
        problems.append("scale: not applied")
    if max(asset_object.dimensions) > max_dimension + 1e-5:
        problems.append("dimensions: too large")
    asset_mesh = asset_object.data
    if not asset_mesh.uv_layers:
        problems.append("UV: missing")
    if not asset_mesh.materials or any(
        slot_material is None for slot_material in asset_mesh.materials
    ):
        problems.append("material: empty slot")
    for slot_material in asset_mesh.materials:
        if not slot_material:
            continue
        for shader_node in slot_material.node_tree.nodes:
            if shader_node.type == "TEX_IMAGE":
                texture_image = shader_node.image
                if not texture_image or (
                    texture_image.source == "FILE"
                    and not texture_image.packed_file
                    and not Path(bpy.path.abspath(texture_image.filepath)).is_file()
                ):
                    problems.append("image: missing reference")
    inspection_bmesh = bmesh.new()
    inspection_bmesh.from_mesh(asset_mesh)
    if any(face.calc_area() < 1e-10 for face in inspection_bmesh.faces):
        problems.append("face: zero area")
    if any(not edge.is_manifold for edge in inspection_bmesh.edges):
        problems.append("surface: not closed manifold")
    elif (
        any(not edge.is_contiguous for edge in inspection_bmesh.edges)
        or inspection_bmesh.calc_volume(signed=True) < 0
    ):
        problems.append("normals: inconsistent or inward")
    inspection_bmesh.free()
    return problems
