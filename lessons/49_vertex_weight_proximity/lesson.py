"""49｜Vertex Weight Proximity。角までの距離で、評価後のウェイトを頂点ごとに変える。"""

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

# この距離より遠い頂点の評価後ウェイトは0へ近づく。
MAX_DISTANCE = 1.5
BLEND_PATH = ROOT / "output" / "49_vertex_weight_proximity.blend"


def main() -> None:
    _lesson_scene, modifiers_collection = tools.begin("VertexWeightProximity")
    body_object = tools.cube_object("Body.Chest", modifiers_collection, size=2.0)
    # グループに頂点を入れておかないと、評価後のウェイト配列が頂点に対応しない。
    tools.ensure_weight_group(body_object, "NearHorn", lambda _vertex: 0.0)
    horn_object = tools.cube_object(
        "Prop.Horn",
        modifiers_collection,
        size=0.3,
        location=(0.0, 0.0, 1.3),
    )
    proximity_modifier = body_object.modifiers.new("NearHorn", "VERTEX_WEIGHT_PROXIMITY")
    proximity_modifier.vertex_group = "NearHorn"
    proximity_modifier.target = horn_object
    # GEOMETRYは頂点ごとの距離。OBJECTはObject原点までの距離を全頂点で共有する。
    proximity_modifier.proximity_mode = "GEOMETRY"
    proximity_modifier.proximity_geometry = {"VERTEX", "EDGE", "FACE"}
    proximity_modifier.min_dist = 0.0
    proximity_modifier.max_dist = MAX_DISTANCE
    # 既定のフォールオフは遠い頂点ほど1に近づく。角の近くを重くするため反転する。
    proximity_modifier.invert_falloff = True

    evaluated = tools.evaluated_snapshot(body_object)
    stored = tools.source_weights(body_object, "NearHorn")
    weights = evaluated.weights["NearHorn"]
    top = [weights[vertex.index] for vertex in body_object.data.vertices if vertex.co.z > 0]
    bottom = [weights[vertex.index] for vertex in body_object.data.vertices if vertex.co.z < 0]

    print("=== 49 vertex weight proximity ===")
    print(f"stored={stored[0]:.3f} top={sum(top)/len(top):.3f} bottom={sum(bottom)/len(bottom):.3f}")

    if any(weight != 0.0 for weight in stored):
        raise RuntimeError("元MeshのNearHornが0のままではない")
    if sum(top) / len(top) <= sum(bottom) / len(bottom):
        raise RuntimeError("角に近い上側のウェイトが下側以下になっている")

    tools.save_blend(BLEND_PATH, body_object)


if __name__ == "__main__":
    main()
