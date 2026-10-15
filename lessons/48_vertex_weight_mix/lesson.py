"""48｜Vertex Weight Mix。2つの頂点グループを、評価後のグループAだけへ混ぜる。"""

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

# AVGはAとBの平均を、評価後のAへ書く。ADDは足し算。
MIX_MODE = "AVG"
BLEND_PATH = ROOT / "output" / "48_vertex_weight_mix.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("VertexWeightMix")
    arm_object = tools.cube_object("Arm.Blend", modifiers_collection)
    tools.ensure_weight_group(arm_object, "Upper", lambda _vertex: 0.25)
    tools.ensure_weight_group(arm_object, "Lower", lambda _vertex: 0.75)
    mix_modifier = arm_object.modifiers.new("BlendBones", "VERTEX_WEIGHT_MIX")
    mix_modifier.vertex_group_a = "Upper"
    mix_modifier.vertex_group_b = "Lower"
    mix_modifier.mix_mode = MIX_MODE
    # ALLは、グループに入っていない頂点も既定値で計算に含める。
    mix_modifier.mix_set = "ALL"

    evaluated = tools.evaluated_snapshot(arm_object)
    stored_upper = tools.source_weights(arm_object, "Upper")
    mixed_upper = evaluated.weights["Upper"]

    print("=== 48 vertex weight mix ===")
    print(f"mode={MIX_MODE} stored Upper={stored_upper[0]:.3f}")
    print(f"evaluated Upper={mixed_upper[0]:.3f}")

    if any(abs(weight - 0.25) > 1e-5 for weight in stored_upper):
        raise RuntimeError("Upperの元ウェイトが0.25のままではない")
    if any(abs(weight - 0.25) < 1e-4 for weight in mixed_upper):
        raise RuntimeError("評価後のUpperがLowerと混ざっていない")

    tools.save_blend(BLEND_PATH, arm_object)


if __name__ == "__main__":
    main()
