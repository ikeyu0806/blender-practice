"""別プロセスで保存結果を開き、データとポーズを検証する。生成はしない。"""

from pathlib import Path
import json
import sys

import bpy

support_path = Path(__file__).resolve().parent
sys.path.insert(0, str(support_path))
import scene_tools as tools

for argument in sys.argv[sys.argv.index("--") + 1 :]:
    blend_path = Path(argument).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    lesson_scene = bpy.context.scene
    report = json.loads(blend_path.with_suffix(".json").read_text())
    assert lesson_scene.camera is not None, blend_path.name
    for record in report["objects"]:
        asset_object = bpy.data.objects[record["name"]]
        assert asset_object.type == record["type"]
        if record["vertices"] is not None:
            assert len(asset_object.data.vertices) == record["vertices"]
            assert len(asset_object.data.polygons) == record["faces"]
        if record["data"]:
            assert asset_object.data.name == record["data"]
    number = int(blend_path.name[:2])
    if number in (29, 33, 34, 40):
        target_names = []
        if number in (29, 40):
            target_names.append("Character.Arm.-1")
        if number in (33, 34, 40):
            target_names.extend(("Monster.Head", "Monster.Tail"))
        saved_frame = lesson_scene.frame_current
        lesson_scene.frame_set(1)
        neutral_coordinates = {
            name: tools.evaluated_coordinates(bpy.data.objects[name])
            for name in target_names
        }
        lesson_scene.frame_set(24)
        for name in target_names:
            posed_coordinates = tools.evaluated_coordinates(bpy.data.objects[name])
            assert len(neutral_coordinates[name]) == len(posed_coordinates)
            assert (
                max(
                    (a - b).length
                    for a, b in zip(neutral_coordinates[name], posed_coordinates)
                )
                > 0.01
            ), name
        lesson_scene.frame_set(saved_frame)
    print(f"REOPEN OK {blend_path.stem}", flush=True)
