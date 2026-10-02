# 08｜頂点から作る岩：Faceの頂点順と法線

## このレッスンの目標

9個の頂点座標と9枚のFaceを自分で定義し、低ポリ岩を作る。同じ頂点を使っても、Faceを囲む頂点番号の順番を逆にすると法線が反転することを、正しい岩と1面だけ裏返した岩で比較する。

先に [06 Material Slot](../06_material_slots/README.md)でFaceがMeshの表面単位であることを、[07 Modifierの評価](../07_modifier_evaluation/README.md)で元Meshと表示結果を確認しておく。

完了時には、次を自分の言葉で説明できるようにする。

- 頂点座標の並び順が`Vertex.index`になり、Faceは頂点番号の組で作られる。
- Faceの頂点順は形だけでなく、表裏と法線方向を決める。
- Face Orientationの青は表、赤は裏を示す。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/08_vertices_rock/lesson.py
```

`saved: .../output/08_vertices_rock.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/08_vertices_rock/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化するため、Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
VertexRocks Collection
├── Rock.Correct Object
│   └── Rock.Correct.Mesh
│       └── 9頂点・16辺・9面、すべて外向き
└── Rock.FlippedFace Object
    └── Rock.FlippedFace.Mesh
        └── 同じ要素数、Upper.Frontだけ内向き
```

2つは別々のMesh。形と要素数は同じだが、右の`Upper.Front`だけFaceの頂点順が逆になっている。

## 頂点からFaceができるまで

座標を並べた順番が、そのまま頂点番号になる。

```python
ROCK_VERTEX_COORDINATES = (
    (-1.2, -0.9, 0.0),  # Vertex 0
    (1.0, -0.8, 0.0),   # Vertex 1
    # ...
    (0.0, 0.0, 1.55),   # Vertex 8
)
```

Faceは「どの頂点を、どの順番で結ぶか」で定義する。

```python
("Upper.Front", (4, 5, 8))
```

このFaceはVertex 4、5、8を順番に結ぶ三角形。`from_pydata()`へはFace名を渡さず、`(4, 5, 8)`だけを渡す。

```python
rock_mesh.from_pydata(ROCK_VERTEX_COORDINATES, [], face_vertex_indices)
```

第2引数のEdge一覧は空。Faceの輪郭から必要なEdgeが作られるため、結果は9頂点・16辺・9面になる。

## 頂点順でなぜ表裏が変わる？

同じ3頂点でも、たどる順番を逆にすると法線方向が逆になる。

```text
外向き: (4, 5, 8)  → Upper.Frontの表が岩の外側
内向き: (8, 5, 4)  → 同じ位置・同じ形だが、表が岩の内側
```

MeshのFaceは厚みを持つ板ではなく、表と裏を持つ面。法線は「表が向いている方向」を表す。光の計算、Backface Culling、書き出したモデルの表示などで向きが重要になる。

この教材では、外側からFaceを見たときに頂点番号が反時計回りになるよう並べる。右の比較用Meshだけ、`reversed()`で`Upper.Front`の順番を逆転する。

## Mac画面でFaceごとの情報を見る

スクリーンショットはすでに **Edit Mode**だが、`Edit Mode`の右に並ぶ3つの選択アイコンでは、左端の **Vertex Select**が青くなっている。Faceを調べるときは、右端の塗りつぶされた四角形アイコン **Face Select**を普通にクリックする。`control`や`command`は押さなくてよい。

また、右下に表示されている緑の三角形タブは **Object Data Properties**で、Mesh全体の設定を見る場所。Face 0、Face 1……という個別レコードの一覧は、ここには表示されない。Faceごとの情報は、3Dビューポートの **Mesh Edit Mode Overlays**へ表示する。

1. 岩が小さい場合は、現在のように岩全体がオレンジ色の状態で **View → Frame Selected**を選び、画面へ大きく表示する。
2. `Edit Mode`の右にある3アイコンのうち、右端の **Face Select**をクリックする。
3. 上部の **Select → None**を選び、いったん全選択を解除する。
4. 調べたいFaceの中央を普通にクリックする。選択したFaceがオレンジ色になる。
5. 3Dビューポート右上で、青い丸の **Viewport Overlays**を見つける。その右側の下向き矢印を開くと、`Guides`、`Text`、`Objects`、`Geometry`などを含む一般Overlayが出る。**Face Orientation**はここにある。
6. Face番号・面積・法線を見る場合は一般Overlayを閉じ、さらに1つ右隣にある「4頂点を線で結んだ四角形」のような **Mesh Edit Mode Overlays**アイコンと下向き矢印をクリックする。
7. タイトルが **Mesh Edit Mode**のポップオーバーで、**Indices**をオンにする。**Measurement**を展開して **Face Area**、**Normals**を展開して **Face Normals**をオンにする。

```text
3Dビューポート右上（Blender 5.2.2）
…  Gizmos ▼  一般Viewport Overlays ▼  Mesh Edit Mode Overlays ▼  X-Ray  表示モード
                    │                         │
                    └ Face Orientation       └ Indices・Face Area・Face Normals
```

Blender 4.0以降、モード固有のOverlay設定は一般Viewport Overlaysとは別ポップオーバーへ移動した。Blender 5.2.2で`Guides`、`Text`、`Objects`、`Geometry`、`Viewer Node`、`Motion Tracking`だけが表示されるのは正常で、その一般パネルをスクロールしてもMesh Edit Modeは現れない。

また、Blender 4.4以降は **Indices**が常時表示されるようになり、**Developer Extrasは不要**。古いBlender向けの解説では、一般Overlay内を探す手順やDeveloper Extrasを有効にする手順が書かれていることがあるため注意する。

この違いは、[Blender 4.0のViewport変更](https://developer.blender.org/docs/release_notes/4.0/viewport/#overlays)と[Blender 4.4のUI変更](https://developer.blender.org/docs/release_notes/4.4/user_interface/)にも記載されている。このレッスンでは、実際に使っている **Blender 5.2.2 LTS**の画面を基準にする。

Mesh Edit Mode Overlaysアイコンが見えない場合は、3Dビューポート上端の **View → Area → Toggle Maximize Area**で表示領域を広げる。元へ戻すときは **View → Area → Restore Area**を選ぶ。この専用アイコンはMeshのEdit Mode中だけ表示される。

分割画面のスクリーンショット右下にある検索欄横の下向き矢印は、Properties Editorの **Options**であり、Viewport Overlaysではない。Viewport Overlaysは必ず、岩が表示されている3Dビューポートの上端にある。

**control + space**は同じ操作のショートカットだが、カーソル位置やキーマップによって反応しない場合がある。迷ったときは上記のメニュー操作を使う。もう1つの方法は、3Dビューポートと右側領域の境界線を右へドラッグして、3Dビューポート自体を広げること。

| 知りたい情報 | 開くポップオーバー | 有効にする項目 | 画面での見え方 |
|---|---|---|---|
| Faceの中心 | Mesh Edit Mode Overlays | **Center** | 各Faceの中央に点が出る。Face Select時だけ表示される。 |
| Face番号 | Mesh Edit Mode Overlays | **Indices** | 選択したFaceに`0`、`1`……の番号が出る。 |
| 面積 | Mesh Edit Mode Overlays → Measurement | **Face Area** | 選択したFaceに面積が数値表示される。 |
| 表が向く方向 | Mesh Edit Mode Overlays → Normals | **Face Normals** | Face中央から法線方向へ短い線が出る。見づらければ **Size**を大きくする。 |
| 表・裏 | 一般Viewport Overlays → Geometry | **Face Orientation** | 表側が青、裏側が赤になる。 |

Indicesは選択中の要素だけに表示される。Face SelectならFace番号、Vertex Selectなら頂点番号を確認できる。

このレッスンの`Upper.Front`は **Face 5**。左の`Rock.Correct`で正面上側の三角形を選び、Indicesに`5`、Face Orientationで外側が青、Face Normalsが岩の外側を向くことを照合する。右の`Rock.FlippedFace`でもFace番号は`5`だが、同じ三角形の外側が赤く、法線は内側を向く。

```text
Properties（右下）    = Mesh全体の設定
一般Viewport Overlays = Face Orientationなど共通表示
Mesh Edit Mode Overlay = 選択したFaceの番号・面積・法線など
```

Faceを構成する頂点番号の組まで確認したい場合は、Face Selectで対象を選んでからVertex Selectへ切り替えると、そのFaceの角にある頂点が選択されたままになる。そこで **Indices**を有効にすると、`Upper.Front`では左の岩が`4`、`5`、`8`で構成されていることを画面上で確認できる。

## Face情報はどこで閲覧・編集する？

Blenderには、Faceをデータベースの1レコードのように選び、全フィールドを1つのフォームで閲覧・編集する画面はない。Faceの値には、直接変更する値と、頂点から自動計算される値が混在するため、目的ごとに画面や操作を使い分ける。

```text
Mesh
└── Face 5 Upper.Front
    ├── vertices = (4, 5, 8)  ← どの頂点を結ぶか
    ├── center                ← 頂点位置から自動計算
    ├── area                  ← 頂点位置から自動計算
    ├── normal                ← 頂点位置と並び順から自動計算
    └── material_index        ← Material slotの割り当て番号
```

| 目的 | 閲覧する場所 | 編集方法 |
|---|---|---|
| Face番号・面積・法線 | 3DビューポートのMesh Edit Mode Overlays | 面積や法線は直接数値入力せず、頂点を動かすと再計算される。 |
| Faceの形・位置 | Edit ModeでFaceを選択 | `G`で移動、`R`で回転、`S`で拡大縮小、`E`で押し出す。実際にはFaceを構成する頂点が動く。 |
| Faceの表裏 | Face OrientationまたはFace Normals | **Mesh → Normals → Flip**で反転、**Recalculate Outside**で外向きに再計算する。 |
| 使用Material | Material PropertiesのMaterial slot | Faceを選択し、slotを選んで **Assign**する。 |
| Face属性を表形式で一覧 | エリアを **Spreadsheet Editor**へ変更し、MeshのFace Domainを選ぶ | Spreadsheetは確認用。編集はEdit Modeの各操作や **Mesh → Set Attribute**などで行う。 |

したがって、このレッスンで最初に確認するなら、Face Selectで1面を選び、Mesh Edit Mode Overlaysの **Indices**、**Face Area**、**Face Normals**をオンにするのが最短。全Faceを表として比較したくなった段階でSpreadsheet Editorを使う。

## Face Orientationで確認する

1. `.blend`を開き、3Dビューポート内を1回クリックする。
2. 上部の **View → Frame All** を選び、2つの岩を画面へ収める。
3. 3Dビューポート右上の、重なった円の **Viewport Overlays**の右にある下向き矢印をクリックする。
4. 表示された項目の **Face Orientation**へチェックを入れる。
5. 左の`Rock.Correct`は、外側がすべて青く表示されることを確認する。
6. 右の`Rock.FlippedFace`は、正面上側の三角形`Upper.Front`だけ赤く表示される。見えない場合は中ボタンドラッグで少し回転する。

```text
青 = Faceの表側
赤 = Faceの裏側
```

色はMaterialではなく、法線確認用のViewport Overlay。Face Orientationをオフにすれば通常表示へ戻る。

## ログで法線方向を確認する

スクリプトは岩の中心から各Face中心へ向かうベクトルと、Face法線の内積を計算する。

```text
score > 0  → 法線は岩の外向き
score < 0  → 法線は岩の中心側を向く
```

左は9面すべて`OUT`。右は`Upper.Front`だけ`IN`になり、その他は`OUT`になる。Face Orientationの色とログを照合する。

## 画面で裏向きFaceを直す

1. 右の`Rock.FlippedFace`を選ぶ。
2. 3Dビューポート左上のモードメニューから **Edit Mode**を選ぶ。
3. 上部の頂点・辺・面アイコンから **Face Select**を選ぶ。
4. Face Orientationで赤い`Upper.Front`を普通にクリックする。
5. 3Dビューポート上部の **Mesh → Normals → Flip**を選ぶ。
6. 赤かったFaceが青に変わることを確認する。
7. モードメニューから **Object Mode**へ戻る。

このGUI修正は`lesson.py`へ自動反映されない。スクリプトを再実行すると、比較のために再び1面が裏向きの状態で作り直される。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
FLIPPED_FACE_NAME = "Upper.Front"
```

`"Upper.Right"`へ変更し、どのFaceが赤くなるか予測してから再実行する。形と要素数は変わらず、右の岩で裏向きになるFaceだけが正面上側から右上側へ移る。確認後は`"Upper.Front"`へ戻す。

## よく混同する点

| 疑問 | 答え |
|---|---|
| 頂点順を逆にすると頂点の位置も変わる？ | 変わらない。同じ頂点を結ぶため形と位置は同じで、Faceの表裏だけが変わる。 |
| Edgeを定義していないのに、なぜ16辺ある？ | `from_pydata()`がFaceの輪郭に必要なEdgeを作るため。 |
| Face Orientationの青と赤はMaterial？ | 違う。法線方向を確認するViewport Overlay。 |
| Normalを反転するとObjectの向きやLocationも変わる？ | 変わらない。Faceの表裏と光の計算方向が変わる。 |
| 右の岩だけ形が壊れて見えないのはなぜ？ | Solid表示では裏面も見えるため。Face OrientationやBackface Cullingで問題を発見できる。 |

## 完了条件と次へ

頂点番号からFaceが作られること、頂点順を逆にすると法線が反転することを、Face Orientationとログで説明できれば完了。次は [09 Face情報の閲覧と編集](../09_face_inspection/README.md) で、面積・法線・Material Slotの閲覧と編集を整理する。木箱と岩を同じSceneへ置く制作は [15 小物セット](../15_prop_set/README.md)で扱う。
