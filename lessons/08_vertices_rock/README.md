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

頂点番号からFaceが作られること、頂点順を逆にすると法線が反転することを、Face Orientationとログで説明できれば完了。次はロードマップの **09 小シーンの組み立て** で、木箱と岩を同じSceneへ配置する。
