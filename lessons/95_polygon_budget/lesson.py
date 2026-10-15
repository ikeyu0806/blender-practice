"""95｜同じ外寸の木箱でも、頂点の密度は見る距離で変える。遠い箱は少ない頂点で足りる。"""

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

# 近くで見せる木箱だけ、辺の分割を増やす。外寸は3つとも同じにする。
NEAR_CUTS = 2
BLEND_PATH = ROOT / "output" / "95_polygon_budget.blend"


def x_span(source_mesh: bpy.types.Mesh) -> float:
    xs = [vertex.co.x for vertex in source_mesh.vertices]
    return max(xs) - min(xs)


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("PolygonBudget")
    distant_object = tools.cube_object("Crate.Distant", quality_collection, location=(-3.2, 0.0, 0.0))
    middle_object = tools.cube_object("Crate.Middle", quality_collection, location=(0.0, 0.0, 0.0))
    near_object = tools.cube_object("Crate.Near", quality_collection, location=(3.2, 0.0, 0.0))
    # 分割はMeshの頂点を増やす。Modifierの評価後ではなく、保存される形そのもの。
    tools.subdivide_mesh(middle_object.data, 1)
    tools.subdivide_mesh(near_object.data, NEAR_CUTS)

    crates = (
        ("distant", distant_object),
        ("middle", middle_object),
        ("near", near_object),
    )
    counts = {label: len(mesh_object.data.vertices) for label, mesh_object in crates}
    spans = {label: x_span(mesh_object.data) for label, mesh_object in crates}

    print("=== 95 polygon budget ===")
    print(
        f"near cuts={NEAR_CUTS} verts distant={counts['distant']} "
        f"middle={counts['middle']} near={counts['near']}"
    )
    print(
        f"x span distant={spans['distant']:.3f} middle={spans['middle']:.3f} "
        f"near={spans['near']:.3f}"
    )

    if not (counts["distant"] < counts["middle"] < counts["near"]):
        raise RuntimeError("近い木箱ほど頂点が多くなっていない")
    if any(abs(span - 2.0) > 0.05 for span in spans.values()):
        raise RuntimeError("密度を変えたのに、木箱の外寸まで変わっている")

    tools.save_blend(BLEND_PATH, near_object)


if __name__ == "__main__":
    main()
