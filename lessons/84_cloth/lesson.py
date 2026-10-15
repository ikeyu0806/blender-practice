"""84｜Cloth。端を固定したマントが、フレームを進めると評価後に垂れる。"""

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

# このフレームまでシーンを進める。長いほど垂れが進む。
LAST_FRAME = 12
BLEND_PATH = ROOT / "output" / "84_cloth.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("Cloth")
    cape_object = tools.grid_object(
        "Clothing.Cape", modifiers_collection, x_segments=6, y_segments=6, size=1.0
    )
    tools.ensure_weight_group(
        cape_object,
        "Pin",
        lambda vertex: 1.0 if vertex.co.x > 0.8 else 0.0,
    )
    cloth_modifier = cape_object.modifiers.new("Drape", "CLOTH")
    # 質量用グループのウェイト1が、布シミュレーションでは固定ピンになる。
    cloth_modifier.settings.vertex_group_mass = "Pin"
    lesson_scene.frame_end = LAST_FRAME
    for frame in range(1, LAST_FRAME + 1):
        lesson_scene.frame_set(frame)

    evaluated = tools.evaluated_snapshot(cape_object)
    pinned = [
        evaluated.positions[vertex.index].z
        for vertex in cape_object.data.vertices
        if vertex.co.x > 0.8
    ]
    loose = [
        evaluated.positions[vertex.index].z
        for vertex in cape_object.data.vertices
        if vertex.co.x <= 0.8
    ]

    print("=== 84 cloth ===")
    print(f"frame={LAST_FRAME} pin z={max(abs(z) for z in pinned):.3f} loose min z={min(loose):.3f}")

    if min(loose) > -0.05:
        raise RuntimeError("固定していない側が垂れていない")
    if max(abs(z) for z in pinned) > 0.08:
        raise RuntimeError("ピンした端が動いている")

    tools.save_blend(BLEND_PATH, cape_object)


if __name__ == "__main__":
    main()
