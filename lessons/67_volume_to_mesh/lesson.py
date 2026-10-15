"""67｜Volume to Mesh。密度Volumeから、評価後の表面Meshを作る。

殻Objectの元Meshは頂点1つの目印。表面の頂点は評価後だけに現れる。
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

# この密度以上の升目を、表面Meshの内側とみなす。
DENSITY_THRESHOLD = 0.1
BLEND_PATH = ROOT / "output" / "67_volume_to_mesh.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("VolumeToMesh")
    rock_object = tools.cube_object("Rock.Source", modifiers_collection, size=1.2)
    volume_data = bpy.data.volumes.new("Cloud.Volume")
    cloud_object = bpy.data.objects.new("Cloud.Density", volume_data)
    modifiers_collection.objects.link(cloud_object)
    density_modifier = cloud_object.modifiers.new("FromRock", "MESH_TO_VOLUME")
    density_modifier.object = rock_object
    density_modifier.resolution_mode = "VOXEL_SIZE"
    density_modifier.voxel_size = 0.12

    # 表面を受け取るMeshは、体積とは別Object。元の頂点は評価の入力に使わない。
    shell_object = tools.mesh_from_pydata(
        "Rock.Shell", modifiers_collection, [(0.0, 0.0, 0.0)], [], []
    )
    shell_modifier = shell_object.modifiers.new("Surface", "VOLUME_TO_MESH")
    shell_modifier.object = cloud_object
    shell_modifier.threshold = DENSITY_THRESHOLD
    shell_modifier.grid_name = "density"

    evaluated = tools.evaluated_snapshot(shell_object)

    print("=== 67 volume to mesh ===")
    print(
        f"threshold={DENSITY_THRESHOLD} shell source={len(shell_object.data.vertices)} "
        f"evaluated vertices={evaluated.vertex_count} faces={evaluated.face_count}"
    )

    if len(shell_object.data.vertices) != 1:
        raise RuntimeError("殻の元Meshが頂点1つではない")
    if evaluated.vertex_count < 50:
        raise RuntimeError("密度から表面が作られていない")

    tools.save_blend(BLEND_PATH, shell_object)


if __name__ == "__main__":
    main()
