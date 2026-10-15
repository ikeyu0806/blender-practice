# 54｜Edge Split：鋭い辺で評価後の頂点を分ける

## このレッスンの目標

木箱の面数は6のまま、90度の辺がしきい値より鋭いので、評価後の頂点だけが増えることを確認する。輪郭の寸法は立方体のまま。

前提は [53 Decimate](../53_decimate/README.md)。面の向きとスムーズ表示は [11 法線と面の向き](../11_normals_shading/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Edge Splitは、選んだ辺の両側で評価後の頂点を別々にする。
- 面の枚数は増えず、共有されていた頂点が辺ごとに分かれる。
- 角度のしきい値より緩い辺は、頂点を共有したままになる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/54_edge_split/lesson.py
```

`saved: .../output/54_edge_split.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/54_edge_split/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
EdgeSplit Collection
└── Crate.HardEdge Object → 8頂点・6面の立方体Mesh
    └── Edge Split Modifier（角度30度より鋭い辺）
        └── 評価後は面6のまま、頂点が8より多い
```

## 仕組み

スムーズ表示は、共有頂点の法線を混ぜて角を丸く見せる。木箱の角を鋭く残したいとき、その辺の両側で頂点を分け、法線が混ざらないようにできる。Edge Splitはその分割を評価後だけ行う。

立方体の隣り合う面は90度。しきい値が30度なら、12本の辺すべてが対象になり、各角の頂点が面ごとに分かれて頂点数が増える。面はまだ6枚。輪郭を見ても立方体のままなので、増えているのは内部の頂点の共有関係。

しきい値を180度まで上げると、90度の辺は「鋭くない」側になり、頂点は8のままに近づく。

## Blender画面で観察する

1. `.blend`を開き、木箱を正面から見る。
2. **Modifier Properties** の`SplitSharp`でEdge Angleが有効であることを確認する。
3. オーバーレイの **Wireframe** を有効にし、Modifierの表示を切ったときの頂点の共有と、有効なときの分割を比べる。
4. ログの面数が6のまま、評価後の頂点が8より多いことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると分かれた頂点が元Meshになり、スムーズに戻すには頂点を溶接し直す。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SPLIT_ANGLE = radians(30)
```

これを`radians(120)`にして、実行前に予測する。90度の辺はまだ分割されるか。面数は6のままか。

再実行すると、面数は6のままで、120度未満の90度の辺はまだ分かれ、評価後の頂点は8より多い。`radians(180)`にすると分割が外れるので、まずは120度で比べる。確認後は`radians(30)`へ戻す。

## 完了条件と次へ

面数は6のまま、評価後の頂点だけが鋭い辺で増えることを説明できれば完了。次は [55 Mask](../55_mask/README.md) で、頂点グループに入っていない部分を評価後から外す。
