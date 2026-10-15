"""82｜Warp。2つのEmptyの差で、布の一部を評価後に持ち上げる。"""

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

# FromからToへの移動が、半径内の頂点へかかる強さの基準になる。
WARP_STRENGTH = 1.0
BLEND_PATH = ROOT / "output" / "82_warp.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Warp")
    banner_object = tools.grid_object(
        "Banner.Cloth", modifiers_collection, x_segments=6, y_segments=6, size=2.0
    )
    from_object = tools.empty_object("Warp.From", modifiers_collection, (0.0, -0.2, 0.0))
    to_object = tools.empty_object("Warp.To", modifiers_collection, (0.0, 0.8, 0.6))
    warp_modifier = banner_object.modifiers.new("PullBanner", "WARP")
    warp_modifier.object_from = from_object
    warp_modifier.object_to = to_object
    warp_modifier.strength = WARP_STRENGTH
    warp_modifier.falloff_radius = 1.5
    warp_modifier.falloff_type = "SMOOTH"

    evaluated = tools.evaluated_snapshot(banner_object)
    z_span = tools.span([position.z for position in evaluated.positions])

    print("=== 82 warp ===")
    print(f"strength={WARP_STRENGTH} evaluated z span={z_span:.3f}")

    if tools.span([vertex.co.z for vertex in banner_object.data.vertices]) > 1e-6:
        raise RuntimeError("旗の元Meshが平らではない")
    if z_span < 0.05:
        raise RuntimeError("2つのEmptyの差が旗へ出ていない")

    tools.save_blend(BLEND_PATH, banner_object)


if __name__ == "__main__":
    main()
