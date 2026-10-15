"""57｜Multiresolution。元の8頂点は残し、細分化レベルをModifier側に積む。"""

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

# Subdivideを繰り返す回数。段を積んだあとに、表示レベルを下げても段自体は残る。
SUBDIVIDE_TIMES = 1
BLEND_PATH = ROOT / "output" / "57_multires.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Multiresolution")
    sculpt_object = tools.cube_object("Monster.Brow", modifiers_collection)
    multires_modifier = sculpt_object.modifiers.new("SculptLevels", "MULTIRES")
    tools.active(sculpt_object)
    for _step in range(SUBDIVIDE_TIMES):
        # 段を1つ追加するOperator。表示レベルの数値だけを上げても、段が無いと細かくならない。
        result = bpy.ops.object.multires_subdivide(modifier=multires_modifier.name)
        if "FINISHED" not in result:
            raise RuntimeError(f"Multiresの細分化に失敗した: {result}")

    evaluated = tools.evaluated_snapshot(sculpt_object)

    print("=== 57 multires ===")
    print(
        f"levels={multires_modifier.levels} total={multires_modifier.total_levels} "
        f"source={len(sculpt_object.data.vertices)} evaluated={evaluated.vertex_count}"
    )

    if len(sculpt_object.data.vertices) != 8:
        raise RuntimeError("元Meshが8頂点のままではない")
    if multires_modifier.total_levels < 1:
        raise RuntimeError("細分化の段が積まれていない")
    if evaluated.vertex_count <= 8:
        raise RuntimeError("表示レベルの評価後で頂点が増えていない")

    tools.save_blend(BLEND_PATH, sculpt_object)


if __name__ == "__main__":
    main()
