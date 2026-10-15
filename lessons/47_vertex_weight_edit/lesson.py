"""47｜Vertex Weight Edit。保存されたウェイトを、評価後だけ別の曲線で変換する。"""

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

# ROOTは小さいウェイトを持ち上げる。SHARPは逆に小さい値をさらに小さくする。
FALLOFF = "ROOT"
STORED_WEIGHT = 0.2
BLEND_PATH = ROOT / "output" / "47_vertex_weight_edit.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("VertexWeightEdit")
    arm_object = tools.cube_object("Arm.Upper", modifiers_collection)
    tools.ensure_weight_group(
        arm_object, "Forearm", lambda _vertex: STORED_WEIGHT
    )
    edit_modifier = arm_object.modifiers.new("RemapForearm", "VERTEX_WEIGHT_EDIT")
    edit_modifier.vertex_group = "Forearm"
    edit_modifier.falloff_type = FALLOFF

    evaluated = tools.evaluated_snapshot(arm_object)
    stored = tools.source_weights(arm_object, "Forearm")
    remapped = evaluated.weights["Forearm"]

    print("=== 47 vertex weight edit ===")
    print(f"falloff={FALLOFF} stored={stored[0]:.3f} evaluated={remapped[0]:.3f}")

    if any(abs(weight - STORED_WEIGHT) > 1e-5 for weight in stored):
        raise RuntimeError("元Meshのウェイトが変わった")
    if any(abs(weight - stored[index]) < 1e-4 for index, weight in enumerate(remapped)):
        raise RuntimeError("評価後ウェイトが保存値から変換されていない")

    tools.save_blend(BLEND_PATH, arm_object)


if __name__ == "__main__":
    main()
