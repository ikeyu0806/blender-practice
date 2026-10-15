"""62｜Subdivision Surface。元の8頂点は残し、評価後だけ滑らかな分割を足す。"""

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

# ビューポートで計算する分割段数。1段でも頂点は増え、2段でさらに滑らかになる。
VIEWPORT_LEVELS = 2
BLEND_PATH = ROOT / "output" / "62_subdivision.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Subdivision")
    body_object = tools.cube_object("Body.Block", modifiers_collection)
    subdiv_modifier = body_object.modifiers.new("SmoothBody", "SUBSURF")
    subdiv_modifier.levels = VIEWPORT_LEVELS
    subdiv_modifier.render_levels = VIEWPORT_LEVELS

    evaluated = tools.evaluated_snapshot(body_object)

    print("=== 62 subdivision ===")
    print(
        f"levels={VIEWPORT_LEVELS} source={len(body_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count}"
    )

    if len(body_object.data.vertices) != 8:
        raise RuntimeError("元Meshが8頂点のままではない")
    if evaluated.vertex_count <= 8:
        raise RuntimeError("分割の評価後で頂点が増えていない")

    tools.save_blend(BLEND_PATH, body_object)


if __name__ == "__main__":
    main()
