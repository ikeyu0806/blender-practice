# BlenderのModifierはどの順番で観察するか

元の疑問は「Blenderに付いているModifierを、種類の抜けが少ない状態で学びたい」。最初に知ることは、**Modifierは元のMeshを直接書き換えず、Objectの評価結果を加工する**こと。その違いは [07 Modifierの評価](../../lessons/07_modifier_evaluation/README.md) で見る。種類ごとの働きは42以降で、1回に1種類ずつ観察する。

Blender 5.2.2 LTS（2026-10-15）のAdd Modifierに出る項目を、このリポジトリのレッスンへ対応させた。メニューはObjectの種類で変わる。Meshを選ぶと編集・生成・変形・物理演算、Grease Pencilを選ぶと線向けの別一覧になる。

## 編集（形を増やさず、データだけ変える）

| Modifier | 観察 |
|---|---|
| Data Transfer | [42](../../lessons/42_data_transfer/README.md) |
| Mesh Cache | 外部の頂点キャッシュファイルが必要。ファイルが無いと評価後の形は元Meshのまま。このカタログではシーンを作らない。 |
| Mesh Sequence Cache | Alembicなどの外部キャッシュが必要。同上。 |
| Normal Edit | [43](../../lessons/43_normal_edit/README.md) |
| Weighted Normal | [44](../../lessons/44_weighted_normal/README.md) |
| UV Project | [45](../../lessons/45_uv_project/README.md) |
| UV Warp | [46](../../lessons/46_uv_warp/README.md) |
| Vertex Weight Edit | [47](../../lessons/47_vertex_weight_edit/README.md) |
| Vertex Weight Mix | [48](../../lessons/48_vertex_weight_mix/README.md) |
| Vertex Weight Proximity | [49](../../lessons/49_vertex_weight_proximity/README.md) |

## 生成（評価後の要素が増える、減る、別の形になる）

| Modifier | 観察 |
|---|---|
| Array | [50](../../lessons/50_array/README.md) |
| Bevel | [07](../../lessons/07_modifier_evaluation/README.md)。角を面取りし、評価後の頂点が増える。 |
| Boolean | [51](../../lessons/51_boolean/README.md) |
| Build | [52](../../lessons/52_build/README.md) |
| Decimate | [53](../../lessons/53_decimate/README.md) |
| Edge Split | [54](../../lessons/54_edge_split/README.md) |
| Geometry Nodes | [36 依存関係と評価結果](../../lessons/36_dependency_evaluation/README.md)。ノードのつながりで加工する。 |
| Mask | [55](../../lessons/55_mask/README.md) |
| Mesh to Volume | [66](../../lessons/66_mesh_to_volume/README.md)。5.2ではVolume Object側に追加する。 |
| Mirror | [56](../../lessons/56_mirror/README.md) |
| Multiresolution | [57](../../lessons/57_multires/README.md) |
| Remesh | [58](../../lessons/58_remesh/README.md) |
| Screw | [59](../../lessons/59_screw/README.md) |
| Skin | [60](../../lessons/60_skin/README.md) |
| Solidify | [61](../../lessons/61_solidify/README.md)。服としての使い方は [26](../../lessons/26_clothing_parts/README.md)。 |
| Subdivision Surface | [62](../../lessons/62_subdivision/README.md) |
| Triangulate | [63](../../lessons/63_triangulate/README.md) |
| Volume to Mesh | [67](../../lessons/67_volume_to_mesh/README.md) |
| Weld | [64](../../lessons/64_weld/README.md) |
| Wireframe | [65](../../lessons/65_wireframe/README.md) |

## 変形（頂点数はほぼそのまま、座標や体積の中身が動く）

| Modifier | 観察 |
|---|---|
| Armature | [28 Armatureとウェイト](../../lessons/28_armature_weights/README.md) |
| Cast | [69](../../lessons/69_cast/README.md) |
| Curve | [70](../../lessons/70_curve/README.md) |
| Displace | [71](../../lessons/71_displace/README.md) |
| Hook | [72](../../lessons/72_hook/README.md) |
| Laplacian Deform | [73](../../lessons/73_laplacian_deform/README.md) |
| Lattice | [74](../../lessons/74_lattice/README.md) |
| Mesh Deform | [75](../../lessons/75_mesh_deform/README.md) |
| Shrinkwrap | [76](../../lessons/76_shrinkwrap/README.md)。投影の制作例は [32](../../lessons/32_sculpt_retopology/README.md)。 |
| Simple Deform | [77](../../lessons/77_simple_deform/README.md) |
| Smooth | [78](../../lessons/78_smooth/README.md) |
| Smooth Corrective | [79](../../lessons/79_corrective_smooth/README.md) |
| Smooth Laplacian | [80](../../lessons/80_laplacian_smooth/README.md) |
| Surface Deform | [81](../../lessons/81_surface_deform/README.md) |
| Warp | [82](../../lessons/82_warp/README.md) |
| Wave | [83](../../lessons/83_wave/README.md) |
| Volume Displace | [68](../../lessons/68_volume_displace/README.md)。Volume Objectに付ける。 |

## 物理演算（フレームを進めると結果が変わる）

| Modifier | 観察 |
|---|---|
| Cloth | [84](../../lessons/84_cloth/README.md) |
| Collision | [85](../../lessons/85_collision/README.md) |
| Dynamic Paint | キャンバスとブラシをベイクし、色や変位のキャッシュを書く。このカタログでは短い背景実行のシーンを作らない。 |
| Explode | [89](../../lessons/89_explode/README.md) |
| Fluid | ドメインのベイクが重く、キャッシュファイルも大きい。役割は液体や煙のシミュレーション。観察用の小さなシーンは作っていない。 |
| Ocean | [86](../../lessons/86_ocean/README.md) |
| Particle Instance | [88](../../lessons/88_particle_instance/README.md) |
| Particle System | [87](../../lessons/87_particle_system/README.md) |
| Soft Body | [90](../../lessons/90_soft_body/README.md) |
| Surface | 古い曲面向けの項目で、Meshの頂点は変えない。このカタログではシーンを作らない。 |

## Grease Pencil

線と塗りのObjectにだけ付く。代表として [91 Grease Pencil Subdivide](../../lessons/91_grease_pencil_subdiv/README.md) で、元の2点が残ったまま評価後の点が増えることを見る。ほかの線向けModifierの名前と役割は、そのレッスンの表にまとめてある。

## 確認のしかた

各レッスンはプロジェクトのルートで、次の形で背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/42_data_transfer/lesson.py
```

`saved:` のパスをBlenderで開く。Applyは押さず、Modifierの表示を切って元のデータが残ることを見る。10〜41の一括確認には、CameraとJSONを使わないこれらの回は含めない。

公式の分類は [Blender Manual: Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html)。
