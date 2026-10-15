# 98｜BevelをSubdivisionの前に置く

## このレッスンの目標

同じ立方体Meshに、BevelとSubdivisionを逆順でかける。Bevelを先に置いた側だけ、評価後の角が外へ残り、頂点も増えることを確認する。

前提は [97 Bumpと実際の凹凸](../97_bump_vs_geometry/README.md)。Bevelの幅は [07 Modifierの評価](../07_modifier_evaluation/README.md)、段数は [62 Subdivision Surface](../62_subdivision/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- Modifierは上から順に評価される。同じ2つでも順番で結果が変わる。
- 鋭い辺を先に面取りしてから分割すると、縁の帯が残る。
- 先に分割して角が浅くなると、角度制限のBevelはその辺を対象にしない。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/98_bevel_subsurf_order/lesson.py
```

`saved: .../output/98_bevel_subsurf_order.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/98_bevel_subsurf_order/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
BevelSubsurfOrder Collection
├── Crate.BevelFirst Object ─┐
│   ├── Bevel（Angle）        ├── Crate.Shared.Mesh（8頂点）
│   └── Subdivision Surface  │
└── Crate.SubsurfFirst Object┘
    ├── Subdivision Surface
    └── Bevel（Angle。浅い辺は対象外）
```

## 仕組み

立方体の隣り合う面は90度で交わる。Angle制限のBevelは、この急な辺を面取りして細い帯を作る。そのあとにSubdivisionをかけると、帯は残り、角は少し丸まる。

逆に先へSubdivisionをかけると、角はすでに丸く、辺の角度は制限より浅くなる。後段のBevelは対象の辺を見つけられず、評価後は分割しただけの形になる。ログでは、先にBevelした側の頂点数が多く、`extent`も元の箱の外側に近い。

光が縁で細く反射して見えるのは、この帯の法線が両側の面の中間を向くためである。帯を作る前に角を丸めてしまうと、その反射の筋ができない。

## Blender画面で観察する

1. `.blend`を開き、2つの木箱を **View → Frame All** で見る。
2. 左は縁に面取りの帯がある。右は角が丸いだけで、帯がない。
3. Modifier Propertiesで、左はBevelが上、右はSubdivisionが上であることを確認する。
4. ログの`source=8`のまま、`bevel-first verts`が`subsurf-first verts`より多く、`extent`も大きいことを照合する。

**Apply** は押さない。順番を画面で入れ替えると見た目は変わるが、`lesson.py`へは戻らない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
BEVEL_WIDTH = 0.15
```

これを`0.08`にして、実行前に予測する。左の帯は狭くなるか。右に帯は現れるか。元の8頂点は変わるか。

再実行すると、元Meshは8頂点のまま。左の帯は狭くなり、右は角度が浅いので面取りされず、頂点数の大小は入れ替わらない。確認後は`0.15`へ戻す。

## 完了条件と次へ

Bevelを分割の前に置くと縁の帯が残り、後に置くと角度制限で省かれることを説明できれば完了。次は [99 未適用のScale](../99_unapplied_scale/README.md) で、同じ幅指定が軸ごとに伸びる理由を見る。
