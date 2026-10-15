"""97｜Bumpは法線だけを曲げ、輪郭の頂点は動かない。Displaceは評価後の頂点を動かす。"""

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

# 右の板だけ、この強さで評価後の頂点を法線方向へ動かす。
DISPLACE_STRENGTH = 0.3
BLEND_PATH = ROOT / "output" / "97_bump_vs_geometry.blend"


def add_bump_material(source_mesh: bpy.types.Mesh) -> None:
    """Noiseの明暗をBumpへつなぐ。頂点座標ではなく、光の計算に使う法線を曲げる。"""
    board_material = bpy.data.materials.new("Material.Board")
    board_material.use_nodes = True
    node_tree = board_material.node_tree
    bsdf = node_tree.nodes["Principled BSDF"]
    noise = node_tree.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 5.0
    bump = node_tree.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.8
    bump.inputs["Distance"].default_value = 0.2
    node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    node_tree.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    source_mesh.materials.append(board_material)


def main() -> None:
    _lesson_scene, quality_collection = tools.begin("BumpVsGeometry")
    shaded_object = tools.grid_object(
        "Ground.Shaded",
        quality_collection,
        x_segments=16,
        y_segments=16,
        size=1.5,
        location=(-2.2, 0.0, 0.0),
    )
    # 同じMeshを参照する。マテリアルのBumpは両方に効き、Displaceは右だけ。
    raised_object = tools.link_mesh_object(
        "Ground.Raised",
        shaded_object.data,
        quality_collection,
        location=(2.2, 0.0, 0.0),
    )
    add_bump_material(shaded_object.data)
    clouds_texture = bpy.data.textures.new("Ground.Clouds", "CLOUDS")
    clouds_texture.noise_scale = 0.35
    displace_modifier = raised_object.modifiers.new("Ridges", "DISPLACE")
    displace_modifier.texture = clouds_texture
    displace_modifier.strength = DISPLACE_STRENGTH
    displace_modifier.mid_level = 0.5
    displace_modifier.direction = "NORMAL"

    shaded_evaluated = tools.evaluated_snapshot(shaded_object)
    raised_evaluated = tools.evaluated_snapshot(raised_object)
    shaded_z = tools.span([position.z for position in shaded_evaluated.positions])
    raised_z = tools.span([position.z for position in raised_evaluated.positions])
    source_z = tools.span([vertex.co.z for vertex in shaded_object.data.vertices])

    print("=== 97 bump vs geometry ===")
    print(
        f"strength={DISPLACE_STRENGTH} source z={source_z:.4f} "
        f"bump z={shaded_z:.4f} displace z={raised_z:.4f}"
    )

    if source_z > 1e-6 or shaded_z > 1e-6:
        raise RuntimeError("Bump側の頂点が持ち上がっている")
    if raised_z < 0.02:
        raise RuntimeError("Displace側の輪郭が持ち上がっていない")
    if shaded_object.data != raised_object.data:
        raise RuntimeError("2つの板が同じMeshを参照していない")

    tools.save_blend(BLEND_PATH, raised_object)


if __name__ == "__main__":
    main()
