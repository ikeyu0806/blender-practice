"""13｜UV展開。初期化して観察用ファイルを保存する教材。"""

from pathlib import Path
import sys
from math import sin, cos, pi, radians
import bmesh
import bpy
from mathutils import Vector

# --pythonと、保存済みText EditorのRun Scriptの両方で教材の場所を解決する。
source_path = globals().get("__file__")
if not source_path:
    lesson_text = getattr(bpy.context.space_data, "text", None)
    if not lesson_text or not lesson_text.filepath:
        raise RuntimeError("lesson.pyを保存してから実行してください")
    source_path = bpy.path.abspath(lesson_text.filepath)
support_path = Path(source_path).resolve().parents[1] / "_support"
if str(support_path) not in sys.path:
    sys.path.insert(0, str(support_path))
import scene_tools as tools

UV_SCALE = 1.0
lesson_scene, assets_collection = tools.start("UVUnwrap")
cloth_material = tools.material("Surface.UV", (0.55, 0.4, 0.18))
crate_object = tools.box(
    "Crate.UV", (1.5, 1, 1), (0, 0, 0.5), assets_collection, cloth_material
)
crate_mesh = crate_object.data
uv_layer = crate_mesh.uv_layers.new(name="UVMap")
# 6面を3列2行に並べる明示的な展開。UVはVertexではなくFaceの角(Loop)にある。
# 共有頂点でもFaceごとのLoopに違うUVを書けるため、継ぎ目を作れる。
for polygon in crate_mesh.polygons:
    column, row = polygon.index % 3, polygon.index // 3
    for loop_index, corner in zip(
        polygon.loop_indices, [(0, 0), (1, 0), (1, 1), (0, 1)]
    ):
        uv_layer.data[loop_index].uv = (
            (column + 0.1 + 0.8 * corner[0]) / 3 * UV_SCALE,
            (row + 0.1 + 0.8 * corner[1]) / 2,
        )
for edge in crate_mesh.edges:
    edge.use_seam = True
checker_image = bpy.data.images.new("UV.Checker", width=256, height=256)
checker_image.generated_type = "COLOR_GRID"
checker_image.pack()
texture_node = cloth_material.node_tree.nodes.new("ShaderNodeTexImage")
texture_node.image = checker_image
cloth_material.node_tree.links.new(
    texture_node.outputs["Color"],
    cloth_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"],
)
cloth_material.node_tree.nodes.active = texture_node
assert len(uv_layer.data) == 24
print("Mesh vertices / UV corners:", len(crate_mesh.vertices), len(uv_layer.data))
tools.active(crate_object)
for polygon in crate_mesh.polygons:
    polygon.select = True
tools.studio(lesson_scene, span=4)
tools.finish(lesson_scene, assets_collection, "13_uv_unwrap")
