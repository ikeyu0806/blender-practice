"""46｜UV Warp。2つのEmptyの位置の差で、評価後のUVを平行移動する。"""

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

# FromからToへの移動が、評価後のUVのずれになる。
TO_LOCATION = (1.0, 0.0, 0.0)
BLEND_PATH = ROOT / "output" / "46_uv_warp.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("UVWarp")
    cloth_object = tools.grid_object(
        "Cloth.Panel", modifiers_collection, x_segments=2, y_segments=2, size=2.0
    )
    uv_layer = cloth_object.data.uv_layers.new(name="UVMap")
    for loop_uv in uv_layer.data:
        loop_uv.uv = (0.25, 0.25)
    from_object = tools.empty_object("UV.From", modifiers_collection, (0.0, 0.0, 0.0))
    to_object = tools.empty_object("UV.To", modifiers_collection, TO_LOCATION)

    warp_modifier = cloth_object.modifiers.new("SlidePattern", "UV_WARP")
    warp_modifier.uv_layer = "UVMap"
    warp_modifier.object_from = from_object
    warp_modifier.object_to = to_object

    evaluated = tools.evaluated_snapshot(cloth_object)
    stored = [loop.uv.copy() for loop in cloth_object.data.uv_layers["UVMap"].data]
    warped = evaluated.uvs["UVMap"]

    print("=== 46 uv warp ===")
    print(f"stored uv0={tuple(round(axis, 3) for axis in stored[0])}")
    print(f"evaluated uv0={tuple(round(axis, 3) for axis in warped[0])}")

    if any(abs(uv.x - 0.25) > 1e-5 or abs(uv.y - 0.25) > 1e-5 for uv in stored):
        raise RuntimeError("元MeshのUVが0.25のままではない")
    if all((left - right).length < 1e-5 for left, right in zip(warped, stored)):
        raise RuntimeError("評価後のUVがFromとToの差で動いていない")

    tools.save_blend(BLEND_PATH, cloth_object)


if __name__ == "__main__":
    main()
