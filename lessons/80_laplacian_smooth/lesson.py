"""80｜Smooth Laplacian。突起を評価後に抑え、布全体の幅は大きく広げない。"""

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

# 1に近いと表面が広がりすぎる。0.2で突起だけを下げる。
LAMBDA_FACTOR = 0.2
BLEND_PATH = ROOT / "output" / "80_laplacian_smooth.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("LaplacianSmooth")
    cloth_object = tools.grid_object(
        "Clothing.Cloth", modifiers_collection, x_segments=4, y_segments=4, size=2.0
    )
    cloth_object.data.vertices[12].co.z = 0.5
    cloth_object.data.update()
    smooth_modifier = cloth_object.modifiers.new("QuietSpike", "LAPLACIANSMOOTH")
    smooth_modifier.lambda_factor = LAMBDA_FACTOR
    smooth_modifier.lambda_border = LAMBDA_FACTOR
    smooth_modifier.iterations = 8

    evaluated = tools.evaluated_snapshot(cloth_object)
    source_max_z = max(vertex.co.z for vertex in cloth_object.data.vertices)
    evaluated_max_z = max(position.z for position in evaluated.positions)

    print("=== 80 laplacian smooth ===")
    print(f"lambda={LAMBDA_FACTOR} source max z={source_max_z:.3f} evaluated={evaluated_max_z:.3f}")

    if evaluated_max_z >= source_max_z:
        raise RuntimeError("突起の評価後が低くなっていない")
    if evaluated.vertex_count != len(cloth_object.data.vertices):
        raise RuntimeError("Smooth Laplacianで頂点数が変わった")

    tools.save_blend(BLEND_PATH, cloth_object)


if __name__ == "__main__":
    main()
