# 91｜Grease Pencil Subdivide：線の点を評価後だけ増やす

## このレッスンの目標

印の線は元の2点のまま、Grease Pencil用のSubdivideが評価後の点を増やすことを確認する。このModifierはMeshの頂点には付かない。

前提は [62 Subdivision Surface](../62_subdivision/README.md)。Mesh用Modifierの一覧は [Modifierカタログ](../../docs/notes/modifiers.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- Grease Pencil ObjectのModifierは、ストロークの点・色・タイミングに働く。
- Subdivideの`level`は、線の途中に点を足す段数。
- 元のストロークの点数は残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/91_grease_pencil_subdiv/lesson.py
```

`saved: .../output/91_grease_pencil_subdiv.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/91_grease_pencil_subdiv/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
GreasePencil Collection
└── Mark.Stroke Object → Grease Pencilデータ
    ├── Layer Line / フレーム1 / ストローク（2点）
    └── Grease Pencil Subdivide Modifier（level=1）
        └── 評価後の点は3以上
```

## 仕組み

42から90まではMesh、Volume、粒に付くModifier。Grease Pencilは線と塗りを持つ別のObjectで、Add Modifierに並ぶ項目もMeshとは別。Subdivideは線の制御点を評価後に増やし、折れ線を滑らかに見せる。

この回の線は`(0, 0, 0)`と`(1, 0, 0.4)`の2点。`level`が1のとき、評価後の点は2より多い。元のストロークを編集すると、増やした点の通る道が変わる。MeshのSubdivision Surfaceとはデータが違い、頂点・辺・面は作らない。

Blender 5.2.2のGrease Pencil向けModifierには、ほかに次がある。手元で1つ動かしたあとは、名前から役割を判別できればよい。

| メニュー上のまとまり | Modifier |
|---|---|
| 見た目 | Hue/Saturation、Tint、Opacity、Texture Mapping |
| 線の形 | Subdivide、Simplify、Length、Envelope、Outline、Multiple Strokes、Dot Dash |
| 繰り返しと時間 | Array、Mirror、Build、Time Offset |
| 変形 | Hook、Noise、Offset、Smooth、Thickness、Lattice、Armature、Shrinkwrap |
| その他 | Vertex Weight Proximity、Vertex Weight Angle、Line Art |

Line Artはシーン内の立体から輪郭線を生成する。人物や背景のMeshを直接変形するModifierではない。

## Blender画面で観察する

1. `.blend`を開き、斜めの線を **View → Frame All** で見る。
2. `Mark.Stroke`の **Modifier Properties** で`SmoothLine`のLevelが1であることを確認する。
3. **Show in Viewport** を切ると、角の残る2点の線に戻る。
4. ログの`source points=2`より`evaluated`が大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると増えた点がストローク本体になる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SUBDIV_LEVEL = 1
```

これを`2`にして、実行前に予測する。元の点は2つのままか。評価後の点はさらに増えるか。

再実行すると、元のストロークは2点のままで、評価後の点が増える。確認後は`1`へ戻す。

## 完了条件と次へ

線の元の点が2つのまま、評価後だけ点が増えることを説明できれば完了。MeshのModifierへ戻るときは [Modifierカタログ](../../docs/notes/modifiers.md)。形・質感・光の差は [モデルの質](../../docs/notes/model-quality.md) と [92](../92_subsurf_topology/README.md) から見る。本編の続きは [08 頂点から作る岩](../08_vertices_rock/README.md)。
