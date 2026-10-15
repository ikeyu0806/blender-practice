# 07｜Modifierの評価：元Meshと表示結果を分ける

## このレッスンの目標

2つのObjectで1つの立方体Meshを共有し、片方のObjectだけにBevel Modifierを付ける。**保存される元Mesh**と、Modifierを計算した**評価後Mesh**を区別し、見た目が変わっても`Object.data`の元Meshは変わっていないことを確認する。

先に [01 共有Mesh](../01_shared_mesh/README.md)でObjectとMeshの共有を、[06 Material Slot](../06_material_slots/README.md)でMesh内部のFaceを確認しておく。

完了時には、次を自分の言葉で説明できるようにする。

- Modifierは元Meshを直接変更せず、Objectの評価結果へ加工を加える。
- ModifierはこのレッスンではObject側にあり、同じMeshを共有する別Objectへ自動では付かない。
- `object.data`と、Dependency Graphから取得する評価後Meshは別の状態。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/07_modifier_evaluation/lesson.py
```

`saved: .../output/07_modifier_evaluation.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/07_modifier_evaluation/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化するため、Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
ModifierEvaluation Collection
├── Cube.OriginalView Object ──┐
│   └── Modifierなし           │
│                              ├──> Cube.Source.Mesh
└── Cube.BevelView Object ─────┘    元: 8頂点・12辺・6面
    └── Bevel Modifier
        └── 評価後Mesh: 要素数が増えた一時的な結果
```

両Objectの`data`は同じ`Cube.Source.Mesh`。右側だけ丸く見えるのは、`Cube.BevelView`のModifier stackが表示前に計算されるから。Bevel済みの形が、新しい通常のMeshデータブロックとして`bpy.data.meshes`へ追加されるわけではない。

## Blender画面で観察する

1. `.blend`を開き、3Dビューポート内を1回クリックする。
2. 上部の **View → Frame All** を選び、2つの立方体を画面へ収める。
3. 左の`Cube.OriginalView`を選ぶ。角が鋭い立方体であることを確認する。
4. Properties Editorのレンチアイコン **Modifier Properties** を開く。左ObjectにはModifierがない。
5. 右の`Cube.BevelView`を選ぶ。同じ元Meshなのに、角が丸く見える。
6. Modifier Propertiesで`Bevel.NonDestructive`を確認する。Widthは`0.2 m`、Segmentsは`3`。
7. Modifier見出しのモニター形 **Show in Viewport** をクリックして無効にする。右も角張った形へ戻る。
8. もう一度有効にすると丸い形へ戻る。これはModifierの表示を切り替えただけで、元Meshを変更・削除していない。

このレッスンではModifierメニューの **Apply** は押さない。Applyは「評価結果を元に新しい編集可能な形へ確定する」別の操作なので、まず非破壊の状態を観察する。

## WidthとSegmentsでなぜ丸く見える？

はい。Bevelは鋭い1本のEdgeを、幅を持つ複数のFaceへ置き換える。`Width`と`Segments`は別の役割を持ち、組み合わさって丸みを作る。

```text
元の立方体
└── 2枚のFaceが鋭い1本のEdgeで接続

Bevel評価後
└── 鋭いEdgeの周囲を、新しい頂点・辺・Faceの帯へ置き換える
    ├── Width    → 帯をどこまで広げるか
    └── Segments → 帯の断面を何分割するか
```

### Width：丸める範囲の大きさ

このレッスンは既定のWidth Type **Offset**を使う。`Width = 0.2 m`は、元の鋭いEdgeから隣接する各Face上で約`0.2 m`離れた位置までをBevel領域にする設定。値を大きくすると角から離れた場所まで形が削られ、丸みが大きく見える。値を小さくすると、角に細いハイライトが入る程度の小さな面取りになる。

```text
Widthが小さい  → 元の四角い面を多く残す、小さい丸み
Widthが大きい  → 角を広い範囲で置き換える、大きい丸み
```

`Width`を大きくしすぎると、隣のBevel領域とぶつかる。既定では重なりを防ぐClampが働くため、値を増やしても途中から見た目が増えにくくなることがある。このレッスンの一辺は`2 m`で、`0.2 m`は違いを見ながら元の立方体も認識しやすい値。

### Segments：曲線へ近づける分割数

コンピューター上のMeshは、完全な曲線ではなく平らなFaceの集まり。`Segments`はBevel断面を何分割するかを決める。

| Segments | 角の形 | 評価後の要素数 |
|---:|---|---|
| `1` | 平らな斜面1枚。丸みというより面取り | 少ない |
| `2`〜`3` | 複数の斜面で曲線に近づく | 増える |
| `6`以上 | より滑らかな曲線に見える | さらに増える |

`Segments`を増やしても、丸める範囲である`Width`自体は基本的に同じ。**同じ幅の中を細かく分割する**ため、輪郭と反射が滑らかに見える。

このレッスンでは`Width = 0.2`と`Segments = 3`なので、「見える大きさのBevel領域」を「3分割したFace」で近似している。さらに、既定の`Profile = 0.5`が円弧に近い断面を作るため、右Objectが丸みを帯びて見える。

### ANGLEはどのEdgeを丸めるか決める

```python
bevel_modifier.limit_method = "ANGLE"
```

これは、隣り合うFaceの角度がしきい値を超えるEdgeだけをBevel対象にする設定。立方体は各面が90度で接続しているため、12本のEdgeすべてが対象になる。`Width`と`Segments`が丸みの形を決め、`limit_method`が丸めるEdgeを選ぶ。

違いを観察するときは、一度に片方だけ変える。

```text
Widthだけ変更
└── 丸みの占める範囲を比較する

Segmentsだけ変更
└── 同じ範囲で、曲線の滑らかさと要素数を比較する
```

## Outlinerで共有Meshを確認する

Outlinerで2つのObjectを展開すると、どちらの下にも緑色の三角アイコン付き`Cube.Source.Mesh`が見える。同じ名前が表示されるのは、コピーが2個あるのではなく、2つのObjectが同じMeshデータブロックを参照しているから。

一方、Bevelは右ObjectのModifier Propertiesにだけ存在する。

```text
共有されるもの
└── Cube.Source.Meshの頂点・辺・面

Objectごとに独立するもの
├── Location
└── Modifier stack
```

## 元Meshと評価後Meshをコードで分ける

元Meshは`Object.data`から取得する。

```python
source_cube_mesh = bevel_view_object.data
```

Modifierを計算した結果はDependency Graphから取得する。

```python
dependency_graph = bpy.context.evaluated_depsgraph_get()
evaluated_object = bevel_view_object.evaluated_get(dependency_graph)
evaluated_mesh = evaluated_object.to_mesh()
```

`evaluated_mesh`は評価結果を読むための一時Mesh。使い終わったら解放する。

```python
evaluated_object.to_mesh_clear()
```

スクリプトは、元Mesh、ModifierなしObjectの評価結果、Bevel付きObjectの評価結果について、それぞれ頂点・辺・面の数をログへ表示する。

Blender 5.2.2 LTS、`BEVEL_SEGMENTS = 3`では次の結果になる。

```text
元Mesh                         (8頂点, 12辺, 6面)
Cube.OriginalViewの評価後     (8頂点, 12辺, 6面)
Cube.BevelViewの評価後        (96頂点, 192辺, 98面)
```

右Objectの評価後だけ要素数が増えても、`Cube.Source.Mesh`そのものは`(8, 12, 6)`のまま。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
BEVEL_SEGMENTS = 3
```

これを`1`にして、実行前に次を予測する。

- 元Meshの`8頂点・12辺・6面`は変わるか。
- 右Objectの丸みはどう変わるか。
- 評価後Meshの頂点・辺・面は増えるか、減るか。

再実行すると、元Meshの数は変わらず、右Objectの角は少ない面で切り落とした形になり、評価後Meshの要素数はSegmentsが`3`のときより減る。確認後は`3`へ戻す。

## よく混同する点

| 疑問 | 答え |
|---|---|
| 右Objectが丸いなら、共有Meshも丸くなった？ | なっていない。`object.data`は8頂点・12辺・6面のまま。右Objectの評価結果だけが丸い。 |
| 同じMeshならModifierも共有される？ | このレッスンのModifierはObject側にあるため共有されない。右Objectだけが持つ。 |
| Show in Viewportを切るとModifierが削除される？ | 削除されない。ビューポートで評価結果を表示するか切り替えるだけ。 |
| 評価後MeshはOutlinerに新しいMeshとして保存される？ | 保存されない。Dependency Graphが計算した一時的な結果として読む。 |
| `to_mesh_clear()`を呼ばないと？ | `to_mesh()`で取得した一時Meshを使い終わったことをBlenderへ伝えられない。読み終えたら必ず解放する。 |

## 完了条件と次へ

2つのObjectが同じ元Meshを参照していること、右ObjectだけがBevel Modifierを持つこと、評価後だけ要素数が増えることを画面とログで確認できれば完了。次は [08 頂点から作る岩](../08_vertices_rock/README.md) で、頂点・辺・面を自分で定義する。Modifierの種類ごとの働きは [カタログ](../../docs/notes/modifiers.md) の42以降で、1種類ずつ観察できる。
