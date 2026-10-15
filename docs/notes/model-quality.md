# モデルの質はどこで分かれるか

近い距離でも滑らかに見えるか、頂点の少なさが見えるかは、Modifierを1つ足しただけでは決まらない。Blender 5.2.2で比べると、差は主に次の3つに分かれる。確認日は2026-10-15。

## 最初に知る結論

1. **形の解像度。** 頂点が少ないと、指や箱の角が直線のまま読める。頂点を増やすと、同じ外寸のまま縁や曲がりを足せる。Subdivision Surfaceは、今ある面の並びが整っているときだけ、その形を滑らかに近づける。
2. **表面の質感。** 色が1枚でも、Roughnessが全面で同じだと反射が均一になる。縁と胴体で値を分け、細かい凹凸を法線（Bump）で足し、輪郭まで曲げるところだけ頂点を動かす。
3. **光。** 小さい光源は影の境界が鋭い。大きい光源は境界が帯になる。Key、Fill、Rimの役割は [19 照明と色](../../lessons/19_lighting/README.md)。

レトロな見た目は、頂点を少なくし、面をフラットにシェーディングし、画素の少ない画像を貼り、小さい光源で影を落とすと近づく。滑らかな近景は、整った面に必要なだけ頂点を足し、質感を分け、影の境界に幅を持たせる。

初期の家庭用ゲーム機には、テクスチャが画面上で歪む座標の精度や、頂点が揺れて見える精度もある。それはその機の描画の性質で、BlenderのModifierや画素数を下げただけでは再現されない。この教材で作るのは、頂点・画像・影の粗さである。

## 形

| 見ること | レッスン |
|---|---|
| 同じ外寸で頂点の数だけ変える | [95 ポリゴン予算](../../lessons/95_polygon_budget/README.md) |
| 同じSubdivisionでも、極のある面は外へ残る | [92 面の並び](../../lessons/92_subsurf_topology/README.md) |
| 角の近くの辺で、丸みの幅を留める | [93 支えの辺](../../lessons/93_support_loops/README.md) |
| 頂点を増やさず、辺のCreaseで角を留める | [94 Edge Crease](../../lessons/94_edge_crease/README.md) |
| 面取りを分割の前に置くと、縁の帯が残る | [98 順番](../../lessons/98_bevel_subsurf_order/README.md) |
| Scaleを頂点へ書かないと、面取り幅が軸で伸びる | [99 未適用のScale](../../lessons/99_unapplied_scale/README.md) |
| 面をフラットにすると、頂点を増やさず角張って見える | [11 法線と面の向き](../../lessons/11_normals_shading/README.md) |
| 紙のように薄い面へ厚みを足す | [61 Solidify](../../lessons/61_solidify/README.md) |

Subdivisionの段数そのものは [62](../../lessons/62_subdivision/README.md)。段数を上げる前に、四角面の流れと、残したい角の位置を決める。

角を面取りすると、隣り合う面の中間を向く細い面ができ、光が縁に乗る。幅の意味は [07 Bevel](../../lessons/07_modifier_evaluation/README.md)。同じ部品を並べるのは [50 Array](../../lessons/50_array/README.md)、穴や合体は [51 Boolean](../../lessons/51_boolean/README.md)、経路に沿って曲げるのは [70 Curve](../../lessons/70_curve/README.md)。これらは形を増やす道具で、質感や光の代わりにはならない。

## 表面

| 見ること | レッスン |
|---|---|
| Base Color、Metallic、Roughnessの意味 | [05 マテリアルの入口](../../lessons/05_material_basics/README.md) |
| 1つの物の中でRoughnessを分ける | [96 Roughnessの差](../../lessons/96_roughness_variation/README.md) |
| 画像を色と粗さへつなぐ | [14 テクスチャとマテリアル](../../lessons/14_image_material/README.md) |
| 同じUVで画素数だけ変える | [100 テクスチャの画素数](../../lessons/100_texture_resolution/README.md) |
| 法線だけの凹凸と、頂点が動く凹凸 | [97 Bumpと実際の凹凸](../../lessons/97_bump_vs_geometry/README.md) |

Principled BSDFは、色、金属、粗さを同じシェーダーで扱う。複数の画像に分けるのは、光の当たり方を面の場所ごとに変えるためである。Bumpや法線の画像は輪郭を変えない。シルエットに出る皺や傷は、頂点かDisplaceで作る。

## 光

小さいAreaライトと大きいAreaライトの影は [101 ライトの大きさ](../../lessons/101_light_size/README.md)。ビューポートは **Rendered** で見る。Material Previewはシーンのライトを使わないことがある。

## 確認手順

各回の`lesson.py`を背景実行し、ログの数値と、保存した`.blend`の画面を照合する。92では極のある木箱の`extent`が四角面側より大きい。97ではBump側の`z`が0のまま、Displace側だけ高低がある。99では未適用のScaleの面取りが、世界座標のXだけ広い。
