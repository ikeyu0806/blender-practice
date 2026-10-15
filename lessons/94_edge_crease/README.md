# 94｜Edge Creaseで頂点を増やさず角を留める

## このレッスンの目標

両方とも8頂点の木箱に同じSubdivisionをかける。右の辺だけCreaseを1にし、評価後の角が元の位置に残ることを確認する。

前提は [93 支えの辺](../93_support_loops/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- Creaseは辺の属性で、Meshの頂点数は増えない。
- Subdivisionの`use_creases`がオンのとき、その値が評価後の角の位置に使われる。
- 支えの辺はループを足す方法、Creaseは同じ頂点のまま角の鋭さを残す方法である。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/94_edge_crease/lesson.py
```

`saved: .../output/94_edge_crease.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/94_edge_crease/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
EdgeCrease Collection
├── Crate.Loose Object → 8頂点、Creaseなし
│   └── Subdivision Surface（use_creases）
└── Crate.Creased Object → 8頂点、全辺のcrease_edge
    └── Subdivision Surface（use_creases）
```

## 仕組み

Blender 5.2では、辺の折れはMeshの`crease_edge`属性に入る。0はSubdivisionの丸みに任せ、1はその辺を元の角へ留める。頂点を足さないので、ゲーム用に頂点予算を抑えたい角や、あとから鋭さを数値で戻したい縁に向く。支えの辺は形としてループが残るので、ハイライトの幅を辺の位置で決めたいときに使う。

ログの`corner distance`は、評価後で元の角`(1, 1, 1)`に最も近い頂点までの距離。Creaseが1のとき、この距離はほぼ0になる。Creaseがない左は、92と同じように角が内側へ寄る。

## Blender画面で観察する

1. `.blend`を開き、2つの木箱を **View → Frame All** で見る。
2. 左は丸く、右は立方体の角が残っている。
3. 右をEdit Modeで辺を選び、サイドバーの **Item → Edge Crease** が1であることを確認する。Mean Creaseでも読める。
4. ログの両方の`verts=8`と、右の`corner distance`が左より小さいことを照合する。

Modifierの **Use Creases** を切ると、右も左と同じ丸みになる。 **Apply** は押さない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
CREASE = 1.0
```

これを`0.5`にして、実行前に予測する。右の頂点数は8のままか。角は1のときより内側へ寄るか。

再実行すると、頂点は8のまま。`corner distance`は1のときより大きくなるが、Creaseなしの左よりは元の角に近い。確認後は`1.0`へ戻す。

## 完了条件と次へ

Creaseが頂点を増やさずに角を留め、支えの辺とは別の手段であることを説明できれば完了。次は [95 ポリゴン予算](../95_polygon_budget/README.md) で、同じ外寸を頂点の数だけ変える。
