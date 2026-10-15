"""86｜Ocean。4頂点の面を入力に、評価後だけ海面の格子と波を生成する。"""

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

# 生成解像度。大きいほど評価後の頂点が増え、計算も重くなる。
OCEAN_RESOLUTION = 4
BLEND_PATH = ROOT / "output" / "86_ocean.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Ocean")
    sea_object = tools.mesh_from_pydata(
        "Sea.Input",
        modifiers_collection,
        [(-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0)],
        [],
        [(0, 1, 2, 3)],
    )
    ocean_modifier = sea_object.modifiers.new("Waves", "OCEAN")
    ocean_modifier.geometry_mode = "GENERATE"
    ocean_modifier.resolution = OCEAN_RESOLUTION
    ocean_modifier.viewport_resolution = OCEAN_RESOLUTION
    # Blender 5.2では海面の一辺の長さは整数。単位はメートル。
    ocean_modifier.spatial_size = 8
    ocean_modifier.wave_scale = 1.2

    evaluated = tools.evaluated_snapshot(sea_object)
    z_span = tools.span([position.z for position in evaluated.positions])

    print("=== 86 ocean ===")
    print(
        f"resolution={OCEAN_RESOLUTION} source={len(sea_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count} z span={z_span:.3f}"
    )

    if len(sea_object.data.vertices) != 4:
        raise RuntimeError("入力の面が4頂点ではない")
    if evaluated.vertex_count < 50:
        raise RuntimeError("海面の格子が生成されていない")
    if z_span < 0.2:
        raise RuntimeError("生成された海面に高低がない")

    tools.save_blend(BLEND_PATH, sea_object)


if __name__ == "__main__":
    main()
