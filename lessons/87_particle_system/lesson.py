"""87｜Particle System。床の面から、評価後に決まった数の粒が生きている。"""

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

# 放出する粒の数。Meshの頂点数とは別の設定。
PARTICLE_COUNT = 12
BLEND_PATH = ROOT / "output" / "87_particle_system.blend"


def main() -> None:
    lesson_scene, modifiers_collection = tools.begin("ParticleSystem")
    floor_object = tools.grid_object(
        "Ground.Emitter", modifiers_collection, x_segments=1, y_segments=1, size=1.0
    )
    # Modifierを追加すると、Object.particle_systemsにも同じ粒の設定が現れる。
    floor_object.modifiers.new("Dust", "PARTICLE_SYSTEM")
    particle_system = floor_object.particle_systems[-1]
    particle_system.settings.count = PARTICLE_COUNT
    particle_system.settings.frame_start = 1
    particle_system.settings.frame_end = 1
    particle_system.settings.lifetime = 30
    particle_system.settings.emit_from = "FACE"
    particle_system.settings.normal_factor = 1.0
    lesson_scene.frame_set(5)

    bpy.context.view_layer.update()
    dependency_graph = bpy.context.evaluated_depsgraph_get()
    evaluated_object = floor_object.evaluated_get(dependency_graph)
    particles = evaluated_object.particle_systems[0].particles
    alive = sum(1 for particle in particles if particle.alive_state == "ALIVE")

    print("=== 87 particle system ===")
    print(f"count={PARTICLE_COUNT} alive={alive} mesh vertices={len(floor_object.data.vertices)}")

    if alive != PARTICLE_COUNT:
        raise RuntimeError(f"生きている粒の数が設定と違う: {alive}")
    if len(floor_object.modifiers) != 1:
        raise RuntimeError("Particle System Modifierが1つではない")

    tools.save_blend(BLEND_PATH, floor_object)


if __name__ == "__main__":
    main()
