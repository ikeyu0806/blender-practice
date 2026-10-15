"""83｜Wave。同じ池の元Meshから、フレームが違うと波の高さが変わる。"""

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

# 波の高さ。速度と合わせて、フレーム間で頂点Zが動く。
WAVE_HEIGHT = 0.3
BLEND_PATH = ROOT / "output" / "83_wave.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("Wave")
    pond_object = tools.grid_object(
        "Pond.Surface", modifiers_collection, x_segments=12, y_segments=12, size=4.0
    )
    wave_modifier = pond_object.modifiers.new("Ripple", "WAVE")
    wave_modifier.height = WAVE_HEIGHT
    wave_modifier.width = 1.0
    wave_modifier.speed = 0.25
    wave_modifier.narrowness = 1.5

    lesson_scene.frame_set(1)
    early = tools.evaluated_snapshot(pond_object)
    lesson_scene.frame_set(20)
    later = tools.evaluated_snapshot(pond_object)
    delta = max(
        (left - right).length for left, right in zip(early.positions, later.positions)
    )

    print("=== 83 wave ===")
    print(f"height={WAVE_HEIGHT} frame delta={delta:.3f} vertices={later.vertex_count}")

    if tools.span([vertex.co.z for vertex in pond_object.data.vertices]) > 1e-6:
        raise RuntimeError("池の元Meshが平らではない")
    if delta < 0.02:
        raise RuntimeError("フレームを進めても波が動いていない")

    tools.save_blend(BLEND_PATH, pond_object)


if __name__ == "__main__":
    main()
