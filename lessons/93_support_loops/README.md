# 93｜角の近くに支えの辺を置く

## このレッスンの目標

Subdivision Surfaceの段数は同じまま、右の木箱だけ角の近くに辺を書いておく。評価後、右の角が元の角の位置に近く残ることを確認する。

前提は [92 Subdivisionと面の並び](../92_subsurf_topology/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- 支えの辺はMeshに書き込むループで、Bevel Modifierとは別である。
- 角から遠い分割だけだと、Subdivisionは角を大きく内側へ動かす。
- 角のすぐ内側に辺があると、評価後の頂点はその角の近くに残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/93_support_loops/lesson.py
```

`saved: .../output/93_support_loops.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/93_support_loops/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
SupportLoops Collection
├── Crate.Bare Object → 8頂点
│   └── Subdivision Surface levels=2
└── Crate.Held Object → 角の近くにループを書いたMesh
    └── Subdivision Surface levels=2
```

## 仕組み

Subdivisionは、隣の頂点との間隔が広いほど、角を大きく丸める。角のすぐ内側にもう1本辺があると、その区間だけ動きが小さくなり、外側の角は元の座標の近くに残る。家具や機械の縁で「少しだけ尖っている」角は、このループの位置で幅を決める。

この回のループは、Meshの辺を分割して書き込んでいる。ModifierスタックにBevelはない。左は8頂点のまま、右はループの分だけ頂点が増えた状態で、同じSubdivisionを受ける。

ログの`corner distance`は、評価後の頂点のうち、元の角`(1, 1, 1)`に最も近いものまでの距離。左は約0.87まで離れ、右は`LOOP_OFFSET`が0.08のとき約0.07に残る。

## Blender画面で観察する

1. `.blend`を開き、2つの木箱を斜めから **View → Frame All** で見る。
2. 左は角が大きく丸い。右は縁が残っている。
3. 右をEdit Modeにして、角のすぐ内側に辺が2本あることを見る。左の辺にはそれがない。
4. ログの`bare source=8`より`held source`が大きく、右の`corner distance`の方が小さいことを照合する。

Modifierメニューの **Apply** は押さない。ループはすでにMesh側にあり、Subdivisionの結果は評価のたびに計算される。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LOOP_OFFSET = 0.08
```

これを`0.2`にして、実行前に予測する。右の角は元の位置から離れるか。左の8頂点は変わるか。

再実行すると、左は8頂点のまま角が大きく丸い。右の`corner distance`は0.08のときより大きくなるが、左よりは元の角に近い。確認後は`0.08`へ戻す。

## 完了条件と次へ

角の近くの辺が、Subdivision後の角の位置を留めていることを説明できれば完了。次は [94 Edge Crease](../94_edge_crease/README.md) で、頂点を増やさずに角を留める。
