"""12｜比率とシルエット。初期化して観察用ファイルを保存する教材。"""

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

HEAD_RATIO = 0.42
lesson_scene, assets_collection = tools.start("Silhouette")
dark_material = tools.material("Surface.Silhouette", (0.035, 0.035, 0.04))
for x, ratio in [(-1.4, 0.28), (1.4, HEAD_RATIO)]:
    tools.box(
        f"Figure.Body.{x}",
        (0.8, 0.4, 1.4),
        (x, 0, 1.2),
        assets_collection,
        dark_material,
    )
    tools.sphere(
        f"Figure.Head.{x}",
        (ratio * 2, 0.5, ratio * 2),
        (x, 0, 2.15),
        assets_collection,
        dark_material,
    )
    for side in (-1, 1):
        tools.box(
            f"Figure.Leg.{x}.{side}",
            (0.22, 0.3, 0.6),
            (x + side * 0.23, 0, 0.3),
            assets_collection,
            dark_material,
        )
# 自作の単純な参照図。画像を外部から取得せず、正面シルエットを比較できる。
reference_image = bpy.data.images.new("Reference.Proportions", width=128, height=128)
pixels = []
for y in range(128):
    for x in range(128):
        head = (x - 64) ** 2 + (y - 100) ** 2 < 14**2
        body = 48 < x < 80 and 40 < y < 87
        legs = (48 < x < 59 or 69 < x < 80) and 12 < y < 40
        tone = 0.05 if head or body or legs else 0.85
        pixels.extend((tone, tone, tone, 1))
reference_image.pixels = pixels
reference_image.filepath_raw = str(tools.OUTPUT / "12_reference.png")
reference_image.file_format = "PNG"
reference_image.save()
reference_image.pack()
print("right head diameter:", HEAD_RATIO * 2, "body height: 1.4")
assert len(assets_collection.objects) == 8
camera_object = tools.studio(
    lesson_scene, span=5, target=(0, 0, 1.4), camera_location=(0, -10, 1.4)
)
camera_object.data.type = "ORTHO"
camera_object.data.ortho_scale = 5.5
tools.finish(lesson_scene, assets_collection, "12_silhouette")
