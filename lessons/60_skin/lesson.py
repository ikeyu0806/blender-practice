"""60｜Skin。枝の辺に頂点ごとの半径を与え、評価後に腕のような体積を作る。"""

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

# 各頂点の断面半径。Modifierを追加したあとのSkin頂点データへ書く。
SKIN_RADIUS = 0.12
BLEND_PATH = ROOT / "output" / "60_skin.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Skin")
    branch_object = tools.mesh_from_pydata(
        "Arm.Branch",
        modifiers_collection,
        [(0.0, 0.0, 0.0), (0.0, 0.0, 0.8), (0.45, 0.0, 1.15)],
        [(0, 1), (1, 2)],
        [],
    )
    skin_modifier = branch_object.modifiers.new("LimbVolume", "SKIN")
    # Skin頂点レイヤーはModifierを足したときにMeshへ作られる。先に半径は書けない。
    skin_layer = branch_object.data.skin_vertices[0]
    for skin_vertex in skin_layer.data:
        skin_vertex.radius = (SKIN_RADIUS, SKIN_RADIUS)
    skin_layer.data[0].use_root = True

    evaluated = tools.evaluated_snapshot(branch_object)

    print("=== 60 skin ===")
    print(
        f"radius={SKIN_RADIUS} source vertices={len(branch_object.data.vertices)} "
        f"evaluated vertices={evaluated.vertex_count} faces={evaluated.face_count}"
    )

    if len(branch_object.data.vertices) != 3:
        raise RuntimeError("枝の元頂点が3ではない")
    if evaluated.face_count < 4:
        raise RuntimeError("半径から体積の面が作られていない")

    tools.save_blend(BLEND_PATH, branch_object)


if __name__ == "__main__":
    main()
