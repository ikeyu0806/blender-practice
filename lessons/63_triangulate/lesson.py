"""63｜Triangulate。元の四角面は残し、評価後だけ各面を三角形2枚にする。"""

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

# 四角を割る対角線の選び方。BEAUTYは隣接とのつながりが自然な方を選ぶ。
QUAD_METHOD = "BEAUTY"
BLEND_PATH = ROOT / "output" / "63_triangulate.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("Triangulate")
    crate_object = tools.cube_object("Crate.Quads", modifiers_collection)
    triangulate_modifier = crate_object.modifiers.new("ToTriangles", "TRIANGULATE")
    triangulate_modifier.quad_method = QUAD_METHOD
    triangulate_modifier.ngon_method = "BEAUTY"

    evaluated = tools.evaluated_snapshot(crate_object)

    print("=== 63 triangulate ===")
    print(
        f"quad={QUAD_METHOD} source faces={len(crate_object.data.polygons)} "
        f"evaluated faces={evaluated.face_count} vertices={evaluated.vertex_count}"
    )

    if len(crate_object.data.polygons) != 6:
        raise RuntimeError("元Meshが6面ではない")
    if evaluated.vertex_count != 8:
        raise RuntimeError("三角形化で頂点数が変わった")
    if evaluated.face_count != 12:
        raise RuntimeError("四角6面が三角形12面になっていない")

    tools.save_blend(BLEND_PATH, crate_object)


if __name__ == "__main__":
    main()
