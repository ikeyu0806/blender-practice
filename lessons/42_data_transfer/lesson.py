"""42｜Data Transfer。別Objectの頂点グループを評価結果へ写す。

Destの元Meshに入っているウェイトは0のまま、評価後だけSourceの上下の差が写る。
"""

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

# 1はSourceのウェイトをDestの評価結果へそのまま使う。
# 0.5にすると、Destに保存された0とSourceの値の中間になる。
MIX_FACTOR = 1.0
BLEND_PATH = ROOT / "output" / "42_data_transfer.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("DataTransfer")
    # 2つの立方体は別Mesh。位置が違っても、頂点番号は同じ立方体の構成を持つ。
    source_object = tools.cube_object(
        "Weight.Source", modifiers_collection, location=(-1.6, 0.0, 0.0)
    )
    dest_object = tools.cube_object(
        "Weight.Dest", modifiers_collection, location=(1.6, 0.0, 0.0)
    )
    # 衣装の固定ピンに見立て、上半分だけ重いウェイトにする。
    tools.ensure_weight_group(
        source_object,
        "ClothPin",
        lambda vertex: 1.0 if vertex.co.z > 0.0 else 0.1,
    )
    # Dest側にも同じ名前のグループが要る。空のグループだと評価結果へ対応づけられない。
    tools.ensure_weight_group(dest_object, "ClothPin", lambda _vertex: 0.0)

    # ModifierはDest Objectに付く。SourceのMeshを複製したり、Destの元Meshを書き換えたりしない。
    transfer_modifier = dest_object.modifiers.new("CopyPin", "DATA_TRANSFER")
    transfer_modifier.object = source_object
    transfer_modifier.use_vert_data = True
    transfer_modifier.data_types_verts = {"VGROUP_WEIGHTS"}
    transfer_modifier.vert_mapping = "TOPOLOGY"
    transfer_modifier.mix_factor = MIX_FACTOR

    dest_evaluated = tools.evaluated_snapshot(dest_object)
    dest_stored = tools.source_weights(dest_object, "ClothPin")
    copied = dest_evaluated.weights["ClothPin"]

    print("=== 42 data transfer ===")
    print("dest stored   ", [round(weight, 2) for weight in dest_stored])
    print("dest evaluated", [round(weight, 2) for weight in copied])

    if any(weight != 0.0 for weight in dest_stored):
        raise RuntimeError("Destの元Meshウェイトが0のままではない")
    if max(copied) <= 0.4 or min(copied) >= 0.3:
        raise RuntimeError(f"評価後がSourceの上下を写していない: {copied}")
    if dest_evaluated.vertex_count != len(dest_object.data.vertices):
        raise RuntimeError("Data Transferで頂点数が変わった")

    tools.save_blend(BLEND_PATH, dest_object)


if __name__ == "__main__":
    main()
