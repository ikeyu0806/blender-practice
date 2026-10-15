"""59｜Screw。断面の折線をZ軸の周りに回し、評価後に器の側面を作る。"""

from pathlib import Path
import sys
from math import radians

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

# 360度をこの段数で近似する。多いほど側面が滑らかで、評価後の頂点も増える。
SCREW_STEPS = 8
BLEND_PATH = ROOT / "output" / "59_screw.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Screw")
    # 軸から離れたXZ上の折線。これを断面として回す。
    profile_object = tools.mesh_from_pydata(
        "Vase.Profile",
        modifiers_collection,
        [(0.25, 0.0, 0.0), (0.45, 0.0, 0.35), (0.18, 0.0, 0.8)],
        [(0, 1), (1, 2)],
        [],
    )
    screw_modifier = profile_object.modifiers.new("Lathe", "SCREW")
    screw_modifier.axis = "Z"
    screw_modifier.angle = radians(360)
    screw_modifier.steps = SCREW_STEPS
    screw_modifier.screw_offset = 0.0

    evaluated = tools.evaluated_snapshot(profile_object)

    print("=== 59 screw ===")
    print(
        f"steps={SCREW_STEPS} source vertices={len(profile_object.data.vertices)} "
        f"evaluated vertices={evaluated.vertex_count} faces={evaluated.face_count}"
    )

    if len(profile_object.data.vertices) != 3:
        raise RuntimeError("断面の元頂点が3ではない")
    if evaluated.vertex_count <= SCREW_STEPS:
        raise RuntimeError("回転後の頂点が段数より多くなっていない")
    if evaluated.face_count < SCREW_STEPS:
        raise RuntimeError("器の側面になる面が足りない")

    tools.save_blend(BLEND_PATH, profile_object)


if __name__ == "__main__":
    main()
