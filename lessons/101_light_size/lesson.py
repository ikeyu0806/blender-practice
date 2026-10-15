"""101｜面積の小さいライトは影の境界が鋭く、大きいライトは境界が帯になる。"""

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

# 右のエリアライトの一辺。左は小さいまま、影の境界の違いを見る。
SOFT_SIZE = 4.0
HARD_SIZE = 0.15
LIGHT_ENERGY = 400.0
BLEND_PATH = ROOT / "output" / "101_light_size.blend"


def area_light(light_name: str, quality_collection: bpy.types.Collection, location, size: float):
    """Areaライトは -Z を向く。真上に置くと、下の木箱と地面へ落ちる。"""
    light_data = bpy.data.lights.new(light_name, "AREA")
    light_data.size = size
    light_data.energy = LIGHT_ENERGY
    light_object = bpy.data.objects.new(light_name, light_data)
    quality_collection.objects.link(light_object)
    light_object.location = location
    return light_object


def main() -> None:
    lesson_scene, quality_collection = tools.begin("LightSize")
    world = bpy.data.worlds.new("LightSize.World")
    lesson_scene.world = world
    world.use_nodes = True
    # 環境光を落とすと、2つのAreaライトの影が読みやすい。
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.02
    tools.grid_object(
        "Ground.Shadow",
        quality_collection,
        x_segments=1,
        y_segments=1,
        size=8.0,
        location=(0.0, 0.0, 0.0),
    )
    # 一辺2の立方体は、中心を高さ1に置くと底が地面に接する。
    tools.cube_object("Crate.Hard", quality_collection, location=(-2.4, 0.0, 1.0))
    tools.cube_object("Crate.Soft", quality_collection, location=(2.4, 0.0, 1.0))
    hard_light = area_light("Light.Hard", quality_collection, (-2.4, -1.2, 4.5), HARD_SIZE)
    soft_light = area_light("Light.Soft", quality_collection, (2.4, -1.2, 4.5), SOFT_SIZE)

    print("=== 101 light size ===")
    print(
        f"energy={LIGHT_ENERGY} hard size={hard_light.data.size} "
        f"soft size={soft_light.data.size}"
    )

    if abs(hard_light.data.energy - soft_light.data.energy) > 1e-6:
        raise RuntimeError("2つのライトのEnergyが揃っていない")
    if soft_light.data.size < hard_light.data.size * 5:
        raise RuntimeError("柔らかい影用のライトが、鋭い影用より十分大きくない")

    tools.save_blend(BLEND_PATH, soft_light)


if __name__ == "__main__":
    main()
