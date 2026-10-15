"""68｜Volume Displace。同じ岩の密度を、テクスチャで膨らませてから表面にする。"""

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

# 密度を押し出す強さ。0ならMesh to Volumeの形に近い表面になる。
PUFF_STRENGTH = 0.4
BLEND_PATH = ROOT / "output" / "68_volume_displace.blend"


def cloud_from_rock(rock_object, modifiers_collection, object_name: str):
    """岩を参照するVolume Objectを作る。Displaceは呼び出し側で足す。"""
    volume_data = bpy.data.volumes.new(f"{object_name}.Volume")
    cloud_object = bpy.data.objects.new(object_name, volume_data)
    modifiers_collection.objects.link(cloud_object)
    density_modifier = cloud_object.modifiers.new("FromRock", "MESH_TO_VOLUME")
    density_modifier.object = rock_object
    density_modifier.resolution_mode = "VOXEL_SIZE"
    density_modifier.voxel_size = 0.12
    return cloud_object


def shell_from_cloud(cloud_object, modifiers_collection, object_name: str):
    """Volumeの密度境界面を受け取るMesh Objectを作る。"""
    shell_object = tools.mesh_from_pydata(
        object_name, modifiers_collection, [(0.0, 0.0, 0.0)], [], []
    )
    shell_modifier = shell_object.modifiers.new("Surface", "VOLUME_TO_MESH")
    shell_modifier.object = cloud_object
    shell_modifier.threshold = 0.1
    return shell_object


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("VolumeDisplace")
    rock_object = tools.cube_object("Rock.Source", modifiers_collection, size=1.2)
    still_cloud = cloud_from_rock(rock_object, modifiers_collection, "Cloud.Still")
    puffed_cloud = cloud_from_rock(rock_object, modifiers_collection, "Cloud.Puffed")
    puff_texture = bpy.data.textures.new("Puff.Clouds", "CLOUDS")
    puff_texture.noise_scale = 0.5
    displace_modifier = puffed_cloud.modifiers.new("Puff", "VOLUME_DISPLACE")
    displace_modifier.texture = puff_texture
    displace_modifier.strength = PUFF_STRENGTH

    still_shell = shell_from_cloud(still_cloud, modifiers_collection, "Shell.Still")
    puffed_shell = shell_from_cloud(puffed_cloud, modifiers_collection, "Shell.Puffed")
    still_shell.location = (-1.4, 0.0, 0.0)
    puffed_shell.location = (1.4, 0.0, 0.0)
    still_evaluated = tools.evaluated_snapshot(still_shell)
    puffed_evaluated = tools.evaluated_snapshot(puffed_shell)

    print("=== 68 volume displace ===")
    print(
        f"strength={PUFF_STRENGTH} still vertices={still_evaluated.vertex_count} "
        f"puffed vertices={puffed_evaluated.vertex_count}"
    )

    if still_evaluated.vertex_count < 50 or puffed_evaluated.vertex_count < 50:
        raise RuntimeError("比較用の表面ができていない")
    if still_evaluated.vertex_count == puffed_evaluated.vertex_count:
        raise RuntimeError("Displaceの有無で表面の頂点数が同じ")

    tools.save_blend(BLEND_PATH, puffed_shell)


if __name__ == "__main__":
    main()
