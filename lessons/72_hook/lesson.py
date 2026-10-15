"""72｜Hook。蓋の1頂点だけを、Emptyの移動量で評価後に引っ張る。"""

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

# ModifierへEmptyを割り当てたあとで動かす。割り当て時の位置との差が変形になる。
PULL_Z = 1.5
BLEND_PATH = ROOT / "output" / "72_hook.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Hook")
    lid_object = tools.cube_object("Chest.Lid", modifiers_collection, size=1.0)
    top_vertex = max(lid_object.data.vertices, key=lambda vertex: vertex.co.z)
    tools.ensure_weight_group(
        lid_object,
        "Corner",
        lambda vertex: 1.0 if vertex.index == top_vertex.index else 0.0,
    )
    pull_object = tools.empty_object("Lid.Pull", modifiers_collection, (0.0, 0.0, 0.0))
    hook_modifier = lid_object.modifiers.new("PullCorner", "HOOK")
    hook_modifier.object = pull_object
    hook_modifier.vertex_group = "Corner"
    # 割り当て後の移動だけが頂点へ伝わる。最初から高い位置に置くと差が無い。
    pull_object.location.z = PULL_Z

    evaluated = tools.evaluated_snapshot(lid_object)
    moved_z = evaluated.positions[top_vertex.index].z
    stored_z = top_vertex.co.z

    print("=== 72 hook ===")
    print(f"pull={PULL_Z} stored z={stored_z:.3f} evaluated z={moved_z:.3f}")

    if moved_z < stored_z + PULL_Z * 0.5:
        raise RuntimeError("Hookが角を十分に動かしていない")
    if abs(lid_object.data.vertices[top_vertex.index].co.z - stored_z) > 1e-6:
        raise RuntimeError("元Meshの頂点が動いた")

    tools.save_blend(BLEND_PATH, lid_object)


if __name__ == "__main__":
    main()
