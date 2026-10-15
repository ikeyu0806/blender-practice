"""89｜Explode。壺の面を、同じObjectの粒に追従させて評価後にばらす。"""

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

# 破片が見えるフレーム。1に近いと、割れる前に近い。
OBSERVE_FRAME = 8
BLEND_PATH = ROOT / "output" / "89_explode.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("Explode")
    pot_object = tools.cube_object("Prop.Pot", modifiers_collection, size=1.0)
    pot_object.modifiers.new("Shards", "PARTICLE_SYSTEM")
    particle_system = pot_object.particle_systems[-1]
    particle_system.settings.count = 8
    particle_system.settings.frame_start = 1
    particle_system.settings.frame_end = 1
    particle_system.settings.lifetime = 20
    particle_system.settings.normal_factor = 2.0
    particle_system.settings.render_type = "NONE"
    # 粒のModifierより後に置く。面が粒の位置へ分かれる。
    explode_modifier = pot_object.modifiers.new("BreakApart", "EXPLODE")
    explode_modifier.use_edge_cut = True
    lesson_scene.frame_set(OBSERVE_FRAME)

    evaluated = tools.evaluated_snapshot(pot_object)

    print("=== 89 explode ===")
    print(
        f"frame={OBSERVE_FRAME} source faces={len(pot_object.data.polygons)} "
        f"evaluated faces={evaluated.face_count} vertices={evaluated.vertex_count}"
    )

    if len(pot_object.data.polygons) != 6:
        raise RuntimeError("壺の元Meshが6面ではない")
    if evaluated.face_count <= 6:
        raise RuntimeError("評価後の面が割れて増えていない")

    tools.save_blend(BLEND_PATH, pot_object)


if __name__ == "__main__":
    main()
