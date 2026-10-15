"""66｜Mesh to Volume。岩のMeshは残し、Volume Objectの評価結果に密度グリッドを作る。

Blender 5.2では、このModifierはMeshではなくVolume Objectに追加する。
参照先のobjectが、体積の元になるMesh Object。
"""

from pathlib import Path
import sys

import bpy

source_path = globals().get("__file__")
if not source_path:
    lesson_text = getattr(bpy.context.space_data, "text", None)
    if not lesson_text or not lesson_text.filepath:
        raise RuntimeError("lesson.pyを保存してから実行してください")
    source_path = bpy.path.abspath(lesson_text.filepath)
LESSON_PATH = Path(source_path).resolve()
ROOT = LESSON_PATH.parents[2]
support_path = LESSON_PATH.parents[1] / "_support"
if str(support_path) not in sys.path:
    sys.path.insert(0, str(support_path))

import modifier_tools as tools

# 升目の一辺。小さいほど密度グリッドは細かく、計算は重くなる。
VOXEL_SIZE = 0.12
BLEND_PATH = ROOT / "output" / "66_mesh_to_volume.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("MeshToVolume")
    rock_object = tools.cube_object("Rock.Source", modifiers_collection, size=1.2)
    volume_data = bpy.data.volumes.new("Cloud.Volume")
    cloud_object = bpy.data.objects.new("Cloud.Density", volume_data)
    modifiers_collection.objects.link(cloud_object)

    volume_modifier = cloud_object.modifiers.new("FromRock", "MESH_TO_VOLUME")
    if volume_modifier is None:
        raise RuntimeError("Volume ObjectへMesh to Volumeを追加できなかった")
    volume_modifier.object = rock_object
    volume_modifier.resolution_mode = "VOXEL_SIZE"
    volume_modifier.voxel_size = VOXEL_SIZE
    volume_modifier.density = 1.0

    bpy.context.view_layer.update()
    dependency_graph = bpy.context.evaluated_depsgraph_get()
    evaluated_cloud = cloud_object.evaluated_get(dependency_graph)
    grid_count = len(evaluated_cloud.data.grids)

    print("=== 66 mesh to volume ===")
    print(
        f"voxel={VOXEL_SIZE} rock vertices={len(rock_object.data.vertices)} "
        f"rock modifiers={len(rock_object.modifiers)} grids={grid_count}"
    )

    if len(rock_object.modifiers) != 0:
        raise RuntimeError("岩Mesh側にModifierが付いている")
    if volume_modifier.object is not rock_object:
        raise RuntimeError("体積の参照先が岩Objectではない")
    if grid_count < 1:
        raise RuntimeError("評価後のVolumeに密度グリッドがない")

    tools.save_blend(BLEND_PATH, cloud_object)


if __name__ == "__main__":
    main()
