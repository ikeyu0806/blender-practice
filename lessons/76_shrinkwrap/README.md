# 76｜Shrinkwrap：布を体の一番近い表面へ貼る

## このレッスンの目標

体の上、Z=2にある平らな布の元MeshはローカルZが0のまま、Shrinkwrapの評価後は体の表面付近までローカルZが下がることを確認する。

前提は [75 Mesh Deform](../75_mesh_deform/README.md)。リトポロジーで高密度の形へ投影する使い方は [32 Sculptとリトポロジー](../32_sculpt_retopology/README.md)。この回は最近傍の表面への貼り付けだけを見る。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Shrinkwrapは、各頂点をtargetの表面へ評価後だけ移動する。
- `NEAREST_SURFACEPOINT`は、一番近い表面上の点へ貼る。
- `offset`は表面から少し浮かせる距離。元Meshの位置はObjectのLocationとして残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/76_shrinkwrap/lesson.py
```

`saved: .../output/76_shrinkwrap.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/76_shrinkwrap/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Shrinkwrap Collection
├── Body.Torso Object → 一辺2mの立方体（表面の目標）
└── Clothing.Patch Object（Location Z=2、元Meshは平ら）
    └── Shrinkwrap Modifier → Body.Torso
        └── 評価後のローカルZが負になり、表面へ貼り付く
```

## 仕組み

服のパターンを体から離して作っておき、表示のときだけ表面へ貼ると、パターンの編集と密着を分けられる。Shrinkwrapの`NEAREST_SURFACEPOINT`は、各頂点から一番近いtarget表面上の点を探す。

布ObjectのLocationはZ=2のまま。評価で読む座標はObjectのローカル座標なので、表面まで下がるとローカルZは負になる。体の上面はワールドZ=1付近で、offset 0.05だけ浮く。ログの`evaluated max local z`が-0.5より小さければ、Z=2の平面にはいない。

`PROJECT`は指定した軸方向へ光線を飛ばす。軸を外すと当たらず、元の位置に残る。この回は最近傍なので、真上からでも側面や上面の近い点へ貼る。

## Blender画面で観察する

1. `.blend`を開き、体と貼り付いた布を **View → Frame All** で見る。
2. `Clothing.Patch`の **Modifier Properties** でTargetが`Body.Torso`、Wrap MethodがNearest Surface Pointであることを確認する。
3. **Show in Viewport** を切ると、布が体の上の平らな位置へ戻る。
4. ログのローカルZが負であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると貼り付いた頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SURFACE_OFFSET = 0.05
```

これを`0.3`にして、実行前に予測する。布は表面からより離れるか。元Meshは平らなままか。

再実行すると、元の格子は平らなままで、評価後は表面から0.3m浮いた位置へ近づく。確認後は`0.05`へ戻す。

## 完了条件と次へ

布の元Meshが平らなまま、評価後だけ体の表面付近へ移動していることを説明できれば完了。次は [77 Simple Deform](../77_simple_deform/README.md) で、板を円弧に曲げる。
