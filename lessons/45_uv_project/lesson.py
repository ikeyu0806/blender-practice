"""45｜UV Project。Cameraの位置から、評価後のUVだけを投影する。

元Meshに保存したUVは(0, 0)のまま。評価後のUV層だけが投影結果になる。
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

# 投影の拡大率。大きくすると評価後のUVが原点から離れる。
PROJECT_SCALE = 1.0
BLEND_PATH = ROOT / "output" / "45_uv_project.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("UVProject")
    banner_object = tools.grid_object(
        "Banner.Cloth", modifiers_collection, x_segments=2, y_segments=2, size=2.0
    )
    # 新しいUV層の初期値は0。ここが保存される元UV。
    uv_layer = banner_object.data.uv_layers.new(name="UVMap")
    # 新規UV層はループによって初期値が揃わないので、観察の基準を0で揃える。
    for loop_uv in uv_layer.data:
        loop_uv.uv = (0.0, 0.0)
    camera_data = bpy.data.cameras.new("Banner.Projector.Camera")
    projector_object = bpy.data.objects.new("Banner.Projector", camera_data)
    # Cameraのローカル-Zが投影方向。回転0なら真下を向く。
    modifiers_collection.objects.link(projector_object)
    projector_object.location = (0.0, 0.0, 3.0)

    project_modifier = banner_object.modifiers.new("ProjectFromCamera", "UV_PROJECT")
    project_modifier.uv_layer = "UVMap"
    project_modifier.projector_count = 1
    project_modifier.projectors[0].object = projector_object
    project_modifier.scale_x = PROJECT_SCALE
    project_modifier.scale_y = PROJECT_SCALE

    evaluated = tools.evaluated_snapshot(banner_object)
    stored_uvs = [loop.uv.copy() for loop in banner_object.data.uv_layers["UVMap"].data]
    projected_uvs = evaluated.uvs["UVMap"]

    print("=== 45 uv project ===")
    print(f"stored uv0={tuple(round(axis, 3) for axis in stored_uvs[0])}")
    print(f"evaluated uv0={tuple(round(axis, 3) for axis in projected_uvs[0])}")

    if any(uv.length > 1e-6 for uv in stored_uvs):
        raise RuntimeError("元MeshのUVが0のままではない")
    if all((left - right).length < 1e-5 for left, right in zip(projected_uvs, stored_uvs)):
        raise RuntimeError("評価後のUVが投影されていない")
    if evaluated.vertex_count != len(banner_object.data.vertices):
        raise RuntimeError("UV Projectで頂点数が変わった")

    tools.save_blend(BLEND_PATH, banner_object)


if __name__ == "__main__":
    main()
