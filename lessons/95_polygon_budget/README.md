# 95｜見る距離で頂点の数を変える

## このレッスンの目標

外寸が同じ3つの木箱で、頂点の数だけが違うことを確認する。遠い箱は8頂点、近い箱は辺を分割した密なMeshである。

前提は [94 Edge Crease](../94_edge_crease/README.md)。シルエットの読み方は [12 比率とシルエット](../12_silhouette/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- 画面の中で小さく見える物は、外寸が合っていれば頂点が少なくても形が読める。
- 近くで縁や面の曲がりを見せる物は、同じ外寸のまま頂点を増やす。
- 頂点を増やすことと、外寸を変えることは別である。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/95_polygon_budget/lesson.py
```

`saved: .../output/95_polygon_budget.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/95_polygon_budget/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
PolygonBudget Collection
├── Crate.Distant Object → 8頂点。外寸は一辺2
├── Crate.Middle Object → 辺を1回分割。外寸は一辺2
└── Crate.Near Object → 辺をNEAR_CUTS回分割。外寸は一辺2
```

## 仕組み

レトロなゲームの人物は、画面に対して頂点が少なかった。指が角張って見えるのは、その距離でも頂点を足す余裕がなかったためである。現代の近景は、同じ身長のまま頂点を増やし、関節や服の縁を曲げる。遠くの背景用の木箱に、近景と同じ密度は要らない。

この3つはModifierの評価後ではなく、保存されるMeshの頂点数が違う。分割しても角の頂点は`±1`に残るので、X方向の幅は2のままである。ログの`verts`が増えても`x span`は2の近くに留まる。

## Blender画面で観察する

1. `.blend`を開き、3つの木箱を **View → Frame All** で見る。外形の幅は揃っている。
2. 左からEdit Modeで頂点を表示し、右ほど面が細かいことを見る。
3. カメラを引いたつもりで小さく見て、3つの差が外形より弱くなることを確認する。近づくと右の分割が読める。
4. ログの`verts`が distant < middle < near で、`x span`がどれも約2であることを照合する。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
NEAR_CUTS = 2
```

これを`3`にして、実行前に予測する。右の外寸は変わるか。頂点数は増えるか。

再実行すると、3つの`x span`は約2のまま、右の頂点だけが増える。確認後は`2`へ戻す。

## 完了条件と次へ

同じ外寸でも、見る距離に合わせて頂点数を変えることを説明できれば完了。次は [96 Roughnessの差](../96_roughness_variation/README.md) で、1つの木箱の中の反射を分ける。
