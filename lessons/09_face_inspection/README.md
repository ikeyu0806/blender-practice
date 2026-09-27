# 09｜Face情報を閲覧・編集する

## このレッスンの目標

Blender 5.2.2 LTSでFaceを1枚選び、Face番号、構成頂点、面積、中心、法線、Material slot番号を画面とPythonログで照合する。Faceには直接割り当てる値と、頂点から自動計算される値があることを区別する。

先に[08 頂点から作る岩](../08_vertices_rock/README.md)を終え、Vertex、Edge、Face、法線の関係を確認しておく。Mac版のMode切り替えやショートカットで迷った場合は、[Blender Mac版の画面操作](../../docs/notes/blender-mac-controls.md)も参照する。

完了時には、次を自分の言葉で説明できるようにする。

- 一般のViewport Overlaysと、Mesh Edit Mode専用Overlaysは別のポップオーバー。
- `index`と`vertices`はFaceの識別・構造、`center`、`area`、`normal`は頂点から計算される値。
- `material_index`はFaceへ明示的に割り当てるMaterial slot番号。
- Faceの全情報を1つのProperties画面で編集するのではなく、目的に応じてEdit Mode、Overlay、Material Propertiesを使い分ける。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/09_face_inspection/lesson.py
```

`saved: .../output/09_face_inspection.blend`が出てターミナルへ戻ったら、Blenderアプリの **File → Open...**からその`.blend`を開く。別のBlenderウィンドウへ結果が自動反映されるわけではない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/09_face_inspection/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化するため、Text Editorから **Run Script**する場合は現在の作業を先に保存する。GUIで変更した形は`lesson.py`へ自動同期されず、再実行すると同じ出力ファイルを作り直す。手作業を残す場合は別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
FaceInspection Collection
└── FaceSample Object
    └── FaceSample.Mesh
        ├── 8 Vertices
        ├── 12 Edges
        ├── 6 Faces
        ├── material slot[0] → Material.FaceBase
        └── material slot[1] → Material.FaceHighlight

Face 5: Top
├── vertices = (4, 5, 6, 7)
└── material_index = 1
```

出力ファイルは、上面のFace 5を選択した **Edit Mode / Face Select**の状態で保存される。上面だけをオレンジ色のMaterialにして、どのFaceを観察しているか見分けやすくしている。

## Blender 5.2.2でFace情報を表示する

Blender 4.0以降、共通のOverlayとMode固有のOverlayは別ポップオーバーになっている。Blender 5.2.2の3Dビューポート右上は、次の順番で並ぶ。

```text
… Gizmos ▼  一般Viewport Overlays ▼  Mesh Edit Mode Overlays ▼  X-Ray  表示モード
                      │                         │
                      └ Face Orientation       └ Face番号・面積・法線
```

一般Viewport Overlaysは青い丸のアイコン。開くと`Guides`、`Text`、`Objects`、`Geometry`などが表示される。ここをスクロールしてもMesh Edit Mode項目は出ない。

Face情報を表示する正しい手順は次のとおり。

1. `.blend`を開き、3Dビューポート左上が **Edit Mode**になっていることを確認する。
2. `Edit Mode`の右にある3つの選択アイコンで、右端の **Face Select**が青いことを確認する。
3. 上面が小さければ **View → Frame Selected**を選ぶ。
4. 右上の青い一般Viewport Overlaysの、さらに1つ右を見る。
5. 「4頂点を線で結んだ四角形」のような **Mesh Edit Mode Overlays**アイコンまたは横の下向き矢印をクリックする。
6. タイトルが **Mesh Edit Mode**なら正しいパネル。**Indices**と **Center**をオンにする。
7. **Measurement**を展開し、**Face Area**をオンにする。
8. **Normals**を展開し、右端の **Face Normals**をオンにする。必要なら **Size**を調整する。

このレッスンのスクリプトは、これらのOverlayをあらかじめオンにして保存する。ただし「どこで切り替えるか」を覚えるため、一度オフにして同じ手順で戻してみる。

| 見たい情報 | 画面上の場所 | 意味 |
|---|---|---|
| `Face.index` | Mesh Edit Mode Overlays → Indices | Mesh内で何番目のFaceか。0始まり。 |
| Face中心 | Mesh Edit Mode Overlays → Center | Face中央の点。 |
| `area` | Mesh Edit Mode Overlays → Measurement → Face Area | 現在の頂点位置から計算した面積。 |
| `normal` | Mesh Edit Mode Overlays → Normals → Face Normals | Faceの表が向く方向。 |
| 表・裏 | 一般Viewport Overlays → Geometry → Face Orientation | 表を青、裏を赤で確認する。 |
| `material_index` | Material Properties | Faceが使うMaterial slot番号。 |

Blender 4.4以降、Indicesの表示にDeveloper Extrasは不要。古い解説の手順と混同しない。[Blender 4.0のOverlay変更](https://developer.blender.org/docs/release_notes/4.0/viewport/#overlays)、[Blender 4.4のIndices変更](https://developer.blender.org/docs/release_notes/4.4/user_interface/)

## Faceの値は直接編集できる？

Faceをデータベースの1行のように考えると、値の性質は次のように分かれる。

```text
Mesh
└── Face 5
    ├── index = 5                 読み取り・識別用
    ├── vertices = (4, 5, 6, 7)  Topologyで決まる
    ├── center                    頂点位置から自動計算
    ├── area                      頂点位置から自動計算
    ├── normal                    頂点位置と並び順から自動計算
    └── material_index = 1        Material slotを明示的に割り当てる
```

`area = 5.0`のように面積だけを直接入力するのではない。Faceを構成する頂点を移動・拡大縮小すると、その結果として中心、面積、法線が再計算される。

| 編集したいもの | 操作 |
|---|---|
| Faceの位置 | Faceを選択して`G`。構成頂点が一緒に移動する。 |
| Faceの面積 | Faceを選択して`S`。頂点間の距離が変わり、面積が再計算される。 |
| 新しい側面を作る | Faceを選択して`E`で押し出す。新しい頂点・辺・Faceができる。 |
| Faceの表裏 | **Mesh → Normals → Flip**。頂点順と法線方向が反転する。 |
| 使用Material | Material Propertiesでslotを選び、**Assign**する。`material_index`が変わる。 |

## Pythonログと画面を照合する

スクリプトは全Faceについて次を出力する。

```text
face[5] Top: vertices=(4, 5, 6, 7) center=(...) area=... normal=(...) material_index=1
```

画面に出したFace番号・面積・法線と、ログの`face[5]`を比べる。

- `index`と`vertices`はFaceの並びとTopologyを示す。
- `center`、`area`、`normal`は現在の頂点座標からBlenderが計算する。
- `material_index=1`は、2番目のMaterial slotを使うという意味。

全Faceを表形式で比較したい場合は、いずれかのエリア左上にあるEditor Typeを **Spreadsheet**へ変更し、Meshの **Face Domain**を選ぶ。Spreadsheetは属性の一覧確認に向くが、形の編集は3DビューポートのEdit Modeで行う。

## 変更実験

まず画面上でTop Faceの面積を変更する。

1. Top Faceだけが選択された状態で、変更前の **Face Area**を読む。
2. 3Dビューポートへマウスポインターを置き、`S`を押す。
3. `1.2`と入力して`Enter`を押す。マウスホイールは使わない。
4. Top Faceが広がり、Face Areaが増えることを確認する。
5. Face番号は`5`、`material_index`は`1`のままであることを説明する。

元へ戻す場合は、保存せずにファイルを開き直すか、スクリプトを再実行する。

次に`lesson.py`の値を1つだけ変更する。

```python
TOP_REAR_HEIGHT = 1.8
```

`2.4`へ変更し、再実行前にどのFaceの面積と法線が変わるか予測する。奥側のVertex 6、7が高くなるため、Top、Back、Left、Rightの計算値が変わる。FrontとBottomは同じ頂点位置を使うため変わらない。確認後は`1.8`へ戻す。

## よく混同する点

| 疑問 | 答え |
|---|---|
| 一般Viewport OverlaysをスクロールすればMesh Edit Modeが出る？ | 出ない。Blender 5.2.2では右隣の別ポップオーバー。 |
| IndicesにはDeveloper Extrasが必要？ | Blender 4.4以降は不要。 |
| Face Areaを直接入力して形を変える？ | 面積は計算値。頂点またはFaceを移動・拡大縮小する。 |
| FaceのLocationはどこ？ | Face単独のObject Transformはない。構成頂点の座標がFaceの位置を決める。 |
| Face番号は永続ID？ | Topologyの追加・削除・並べ替えで変わり得る。教材内で照合するための番号として使う。 |
| Properties EditorにFace一覧がないのはなぜ？ | Propertiesは主にObjectやMesh全体の設定。Faceごとの形状情報はEdit Mode、Overlay、Spreadsheetで確認する。 |

## 完了条件と次へ

Face 5を選び、画面とログで`index`、`vertices`、`area`、`normal`、`material_index`を対応づけられれば完了。さらに「面積と法線は頂点からの計算値、Material slot番号はFaceへ割り当てる値」と説明できることを確認する。

次はPhase Aの小作品として、木箱と岩を同じSceneへ置き、これまで学んだObject、Mesh、Collection、Material、Modifier、Faceの関係をまとめて確認する。
