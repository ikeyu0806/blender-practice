# Blender 用語集

このプロジェクトのレッスンで出会う言葉を、**Blender の画面で何を見るか**と結びつけて説明する。最初から全部覚える必要はない。まず「[Object と Mesh](#最初に区別する-object-と-mesh)」を読み、レッスンで出てきた語をここで引く。画面の英語表記を併記している。

## 最初に区別する Object と Mesh

```text
Scene（作業する場面）
└── Collection（Object をまとめる）
    ├── Cube.A（Object：位置などを持つ）──┐
    └── Cube.B（Object：別の位置を持つ）──┴── SharedCube（Mesh：立方体の形）
```

[レッスン01](../lessons/01_shared_mesh/README.md)では、**Object が2つ、Mesh が1つ**。`Cube.B` を動かしても `Cube.A` は動かない。同じ Mesh の頂点を編集すると、両方の立方体の形が変わる。画面で2回表示される `SharedCube` は、2つの Object が同じデータを参照していることを示す。

| 用語 | 意味 | レッスン01での例・見方 |
|---|---|---|
| **Object（オブジェクト）** | シーンに置く単位。位置・回転・拡大率を持ち、Mesh などのデータを参照する。形状を持たない Empty も Object。 | Outliner の `Cube.A` と `Cube.B`。 |
| **Mesh（メッシュ）** | 頂点・辺・面からなる形状データ。複数の Object から共有できる。 | 緑色のアイコンの `SharedCube`。データブロックは1つ。 |
| **Object Data（オブジェクトデータ）** | Object が参照する種類別のデータ。Mesh Object なら Mesh、Camera Object なら Camera データ。 | `cube_a.data` は `SharedCube` Mesh。 |
| **Data-Block（データブロック）** | `.blend` 内で名前と種類を持ち、参照・再利用できるデータの単位。Object、Mesh、Material、Scene なども該当する。 | `Cube.A` と `SharedCube` は別種のデータブロック。 |
| **Users（ユーザー数）** | そのデータブロックを参照しているデータの数。画面に見える物体数と常に同じとは限らない。 | `SharedCube` の `mesh.users == 2`。 |

## 画面・ファイル・シーン

| 用語 | 意味 | どこで見る・使うか |
|---|---|---|
| **`.blend` ファイル** | Blender の作業データを保存するファイル。Object や Mesh、Scene などを含む。 | `output/01_shared_mesh.blend`。 |
| **Scene（シーン）** | Object の配置、カメラ、レンダー設定などを含む作業のまとまり。1つの `.blend` に複数の Scene を持てる。 | Outliner の一番上付近の `Scene`。 |
| **Collection（コレクション）** | Object をまとめ、表示や整理を行う入れ物。所属させても親子の位置関係は生まれない。 | Outliner の `Scene Collection`。 |
| **Outliner（アウトライナー）** | Scene の Object やデータの関係を一覧で見る画面。表示モードによって見えるものが変わる。 | スクリーンショットの右上。`Blender File` 表示ならデータブロック側からも確認できる。 |
| **3D Viewport（3Dビューポート）** | モデルを見て、選択・移動・編集するメインの3D画面。 | 2つの立方体が見える領域。 |
| **Properties Editor（プロパティエディター）** | 選んだタブに応じて Scene、Object、Mesh、Material などの設定を表示する画面。 | スクリーンショット右下は Scene 設定のタブ。 |
| **Workspace（ワークスペース）** | Modeling、Shading、Scripting など、作業に合わせた画面配置。データそのものとは別。 | 画面上部のタブ。 |
| **Object Mode（オブジェクトモード）** | Object 全体を選択・変形するモード。 | 立方体全体を移動する。 |
| **Edit Mode（編集モード）** | 選んだ Object の Mesh など、内部の形状を編集するモード。 | 頂点を動かして立方体の形を変える。共有 Mesh なら両 Object の見た目に反映される。 |

## 位置・向き・親子

| 用語 | 意味 | 例・混同しやすい点 |
|---|---|---|
| **Transform（トランスフォーム）** | Object の Location、Rotation、Scale の組。 | 同じ Mesh でも `Cube.A` と `Cube.B` は別の Transform を持つ。 |
| **Location（位置）** | Object の基準点がどこにあるかを表す値。親がある場合は親との関係にも注意する。 | `cube_b.location = (2, 0, 0)`。 |
| **Rotation（回転）** | Object の向き。Python で角度を扱うときは API が期待する単位を確認する。 | 木箱を斜めに置く。 |
| **Scale（拡大率）** | Object の各軸方向の倍率。Mesh の頂点そのものを変えた値とは別。 | `Scale = (2, 1, 1)` なら X 方向に2倍。 |
| **Origin（原点）** | Object の位置・回転・拡大の基準になる点。見えている形の中心と必ず一致するわけではない。 | 木箱を地面に置きやすいよう、底面に設定することがある。 |
| **3D Cursor（3Dカーソル）** | 3D空間に置く操作用の目印。新しい Object の配置やピボットなどに使う。Object の Origin とは別。 | レッスン01の左の立方体付近にある赤白の照準。 |
| **Pivot Point（ピボットポイント）** | 変形操作の中心として使う位置の設定。Origin や 3D Cursor などを選べる。 | 「回転の中心が想定と違う」ときに確認する。 |
| **Global / World（グローバル／ワールド）** | シーン全体を基準にした座標・軸。 | 画面の赤・緑・青の軸は X・Y・Z。 |
| **Local（ローカル）** | Object 自身や親などを基準にした座標・軸。何に対するローカルかを確認する。 | 親を回すと、子の見える位置が変わる。 |
| **Parent / Child（親／子）** | 親の変形が子に影響する関係。Collection に入れる操作とは別。 | [予定レッスン02](plan/README.md)で学ぶ。 |
| **`matrix_world`** | Object のワールド空間での変換を表す行列。親子関係を反映した位置や向きを調べるときに使う。 | `location` だけでは分からない親子込みの結果を見る。 |

## 形を作る・直す

| 用語 | 意味 | 例 |
|---|---|---|
| **Vertex（頂点）** | Mesh を形作る点。 | 立方体の角。 |
| **Edge（辺）** | 2つの頂点をつなぐ線。 | 立方体の稜線。 |
| **Face / Polygon（面／ポリゴン）** | 頂点と辺で囲まれた面。 | 立方体の6つの外面。 |
| **Topology（トポロジー）** | 頂点・辺・面のつながり方。曲げやすさや編集のしやすさに関係する。 | 人物の肘の周囲の辺の流れ。 |
| **Normal（法線）** | 面や頂点の向きを表す方向。光の当たり方や表裏の判断に使う。 | 岩の一部が暗く見えるときに確認する。 |
| **Primitive（プリミティブ）** | 立方体、球、円柱など、基本形状。 | 木箱の板を立方体から作る。 |
| **Extrude（押し出し）** | 選択した頂点・辺・面から新しい形状を伸ばす操作。 | 面を押し出して取っ手を作る。 |
| **Bevel（ベベル）** | 角や辺に幅を付け、鋭い角を丸める操作・Modifier。 | 木箱の縁を少し丸める。 |
| **Modifier（モディファイア）** | 元の形状を直接編集せず、表示・評価結果に加工を加える仕組み。必要に応じて適用できる。 | Bevel で角を丸める。 |
| **Evaluated Mesh（評価後メッシュ）** | Modifier などを計算した後に得られる形状。元の Mesh とは頂点数が違うことがある。 | Bevel の前後を比較する。 |
| **Sculpt（スカルプト）** | 粘土を扱うようにブラシで形を作る方法。 | モンスターの筋肉や角の形を作る。 |
| **Retopology（リトポロジー）** | 既存の形を参考に、扱いやすい辺・面の構成へ作り直すこと。 | 高密度に造形したモンスターを動かしやすい Mesh にする。 |
| **Geometry Nodes（ジオメトリノード）** | ノードのつながりで形状の生成・加工を組み立てる仕組み。 | 背景の石を規則に従って繰り返し配置する。 |

## 色・質感・画像

| 用語 | 意味 | 例 |
|---|---|---|
| **Material（マテリアル）** | 表面の色や光への反応など、見た目を決める設定。Mesh の形そのものではない。 | 金属の剣と木の柄を見分ける。 |
| **Shader（シェーダー）** | 光を受けた表面をどう表示・描画するかを計算する仕組み。 | Material のノードで設定する。 |
| **Principled BSDF** | 多くの質感をまとめて設定できる標準的なシェーダーノード。 | Base Color、Metallic、Roughness を調整する。 |
| **Texture（テクスチャ）** | 色・凹凸・粗さなどの変化に使う画像やデータ。 | 木目の画像を箱に貼る。 |
| **UV Map（UVマップ）** | Mesh の表面のどこが2D画像のどこに対応するかを記録する座標。 | 箱を展開して木目画像を割り当てる。 |
| **Seam（シーム）** | UV 展開で表面を切り開く位置として印を付けた辺。 | 箱の目立ちにくい裏側を切り目にする。 |
| **Render（レンダー）** | Camera・Light・Material などから最終画像や映像を計算すること。3D Viewport の表示と一致するとは限らない。 | 背景小作品を1枚の画像にする。 |
| **Camera（カメラ）** | レンダー時の視点を決める Object とその設定。 | 背景の構図を決める。 |
| **Light（ライト）** | シーンを照らす Object とその設定。 | 人物の輪郭を見やすくする。 |

## 人物・モンスターを動かす

| 用語 | 意味 | 例 |
|---|---|---|
| **Armature（アーマチュア）** | Bone をまとめた骨格データと、それをシーンに置く Object。 | 人物の体を動かすための骨格。 |
| **Bone（ボーン）** | Armature を構成する骨。変形用・操作用など役割がある。 | 肘を曲げるための上腕・前腕の骨。 |
| **Rigging（リギング）** | モデルを動かすための骨、制御、変形設定を組む作業。 | 腕を自然に曲げられるようにする。 |
| **Weight（ウェイト）** | 骨などの影響が各頂点へどれだけ及ぶかを表す値。 | 前腕の骨が肘周辺の頂点をどの程度動かすか。 |
| **Vertex Group（頂点グループ）** | 頂点とウェイトを名前付きで管理する仕組み。骨による変形や Modifier の範囲指定に使う。 | `forearm` に影響される頂点を管理。 |
| **Shape Key（シェイプキー）** | 同じ Mesh の別の形を記録し、混ぜて変形する仕組み。 | 口を開く、眉を上げる。 |
| **Keyframe（キーフレーム）** | 特定時刻の値を記録し、途中の動きを作るための印。 | 1フレーム目と20フレーム目の腕の角度。 |

## Python とファイルのやり取り

`bpy` と `bmesh` は Python 標準ライブラリではなく Blender が提供する。レッスンを通常の `python3` で直接動かすと、通常はこれらを読み込めない。Blender の `--python` または Text Editor の **Run Script** から実行する。`pathlib` は標準ライブラリで、Blender 内の Python からも利用できる。[Blender Python API の概要](https://docs.blender.org/api/5.2/info_overview.html)・[Python の `pathlib`](https://docs.python.org/3/library/pathlib.html)

| 用語 | 意味 | レッスンでの例 |
|---|---|---|
| **`pathlib`** | Python 標準ライブラリ。ファイルやフォルダのパスを扱う。 | `from pathlib import Path`。 |
| **`bpy`** | Blender が提供する Python モジュール。Scene や Object などのデータ・操作へアクセスする。 | `import bpy`。 |
| **`bpy.data`（データ API）** | `.blend` 内の Scene、Object、Mesh などへ直接アクセスする入口。 | `bpy.data.meshes.new("SharedCube")`。 |
| **`bpy.ops`（オペレーター）** | Blender の操作を Python から呼ぶ入口。選択状態やモードなどの Context を必要とする操作がある。 | `bpy.ops.wm.save_as_mainfile(...)`。 |
| **Context（コンテキスト）** | 今どの Scene・Object・エリア・モードなどで操作しているかという状態。 | UI では動く操作が背景実行で失敗するときに確認する。 |
| **`bmesh`** | Blender が提供する Python モジュール。Mesh の頂点・辺・面を組み立てたり編集したりする。 | `bmesh.ops.create_cube(...)`。 |
| **Link（リンク）** | データ同士の参照を結ぶこと。対象によって意味が異なる。 | `scene.collection.objects.link(cube_a)` は Object を Collection に所属させる。Mesh を複製する操作ではない。 |
| **Export / Import（書き出し／読み込み）** | 別形式へ変換して渡す／別形式のデータを取り込むこと。`.blend` を保存する操作とは区別する。 | 将来の Unity 連携では FBX を使う予定。 |

## よく混同する組み合わせ

- **Object と Mesh:** Object は配置と参照を持つ。Mesh は形を持つ。同じ Mesh を複数の Object が使える。
- **Collection と Parent:** Collection は整理・表示のまとまり。Parent は変形が伝わる親子関係。
- **Origin と 3D Cursor:** Origin は各 Object の基準点。3D Cursor は操作用に置く独立した目印。
- **Object Mode と Edit Mode:** 前者は Object 全体、後者は形状の中身を主に扱う。
- **保存と書き出し:** `.blend` 保存は編集を続けるため。FBX などの書き出しは他のアプリへ渡すため。

## 公式資料

- [Blender Manual: Object と Object Data](https://docs.blender.org/manual/en/latest/scene_layout/object/introduction.html)
- [Blender Manual: Collection](https://docs.blender.org/manual/en/latest/scene_layout/collections/introduction.html)
- [Blender Manual: Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html)
- [Blender Python API: `bpy.data`](https://docs.blender.org/api/current/bpy.data.html)
- [Blender Python API: `bmesh`](https://docs.blender.org/api/current/bmesh.html)

用語が新しく出てきたら、関連レッスンの具体例とともにこの用語集を更新する。細かい操作手順は各レッスンの README に置く。
