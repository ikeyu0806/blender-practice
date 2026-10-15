"""88｜Particle Instance。小石の元Meshは1個のまま、粒の位置に評価後の複製を置く。"""

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

PARTICLE_COUNT = 12
BLEND_PATH = ROOT / "output" / "88_particle_instance.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("ParticleInstance")
    floor_object = tools.grid_object(
        "Ground.Emitter", modifiers_collection, x_segments=1, y_segments=1, size=1.0
    )
    floor_object.modifiers.new("Dust", "PARTICLE_SYSTEM")
    particle_system = floor_object.particle_systems[-1]
    particle_system.settings.count = PARTICLE_COUNT
    particle_system.settings.frame_start = 1
    particle_system.settings.frame_end = 1
    particle_system.settings.lifetime = 30
    particle_system.settings.emit_from = "FACE"
    particle_system.settings.normal_factor = 1.0

    pebble_object = tools.cube_object("Prop.Pebble", modifiers_collection, size=0.1)
    instance_modifier = pebble_object.modifiers.new("OnDust", "PARTICLE_INSTANCE")
    instance_modifier.object = floor_object
    instance_modifier.particle_system = particle_system
    lesson_scene.frame_set(5)

    evaluated = tools.evaluated_snapshot(pebble_object)

    print("=== 88 particle instance ===")
    print(
        f"source vertices={len(pebble_object.data.vertices)} "
        f"evaluated={evaluated.vertex_count} count={PARTICLE_COUNT}"
    )

    if len(pebble_object.data.vertices) != 8:
        raise RuntimeError("小石の元Meshが立方体ではない")
    if evaluated.vertex_count != 8 * PARTICLE_COUNT:
        raise RuntimeError("粒の数だけ小石が評価後に並んでいない")

    tools.save_blend(BLEND_PATH, pebble_object)


if __name__ == "__main__":
    main()
