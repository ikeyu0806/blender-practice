"""71｜Displace。平らな地面の評価後だけ、雲テクスチャの明暗でZを動かす。"""

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

# テクスチャの0.5を基準に、このメートルだけ法線方向へ動かす。
DISPLACE_STRENGTH = 0.3
BLEND_PATH = ROOT / "output" / "71_displace.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Displace")
    ground_object = tools.grid_object(
        "Ground.Plain", modifiers_collection, x_segments=8, y_segments=8, size=2.0
    )
    bump_texture = bpy.data.textures.new("Ground.Clouds", "CLOUDS")
    bump_texture.noise_scale = 0.4
    displace_modifier = ground_object.modifiers.new("Bumps", "DISPLACE")
    displace_modifier.texture = bump_texture
    displace_modifier.strength = DISPLACE_STRENGTH
    displace_modifier.mid_level = 0.5
    displace_modifier.direction = "NORMAL"

    evaluated = tools.evaluated_snapshot(ground_object)
    source_z = tools.span([vertex.co.z for vertex in ground_object.data.vertices])
    evaluated_z = tools.span([position.z for position in evaluated.positions])

    print("=== 71 displace ===")
    print(f"strength={DISPLACE_STRENGTH} source z span={source_z:.4f} evaluated={evaluated_z:.4f}")

    if source_z > 1e-6:
        raise RuntimeError("地面の元Meshが平らではない")
    if evaluated_z < 0.02:
        raise RuntimeError("テクスチャで評価後の高低ができていない")

    tools.save_blend(BLEND_PATH, ground_object)


if __name__ == "__main__":
    main()
