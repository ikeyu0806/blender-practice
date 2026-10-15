# 92｜Subdivisionは整った面を滑らかにする

## このレッスンの目標

同じ段数のSubdivision Surfaceを、四角面だけの木箱と、1面に極がある木箱へかける。極のある側だけ、評価後の表面が外へ残ることを確認する。

前提は [62 Subdivision Surface](../62_subdivision/README.md)。この回は他のレッスンの出力ファイルを必要としない。質の全体像は [モデルの質](../../docs/notes/model-quality.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Subdivisionは段数を上げるボタンではなく、今ある面の並びを滑らかに近づける。
- 四角面が揃った立方体は、角が内側へ丸まる。
- 1面の中央に頂点が集まる極は、同じ段数でもその位置が外へ残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/92_subsurf_topology/lesson.py
```

`saved: .../output/92_subsurf_topology.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/92_subsurf_topology/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
SubsurfTopology Collection
├── Crate.Even Object → 8頂点の立方体
│   └── Subdivision Surface（levelsは両方同じ）
└── Crate.Pole Object → 9頂点。1面の中央に極がある
    └── Subdivision Surface（Evenと同じ段数）
```

## 仕組み

Catmull-Clarkの分割は、隣り合う面の並びから新しい位置を決める。四角面が箱の形に沿っていると、角は内側へ寄って丸くなる。1つの面へ頂点を集めると、その点は周囲の面と違う流れになる。段数を上げても、その点は元の面の位置へ残り、箱の一面が膨らんで見える。

ログの`extent`は、評価後の頂点が軸方向へどれだけ原点から離れているか。一辺2の立方体は、分割前は1.0まで届く。四角面だけを2段にすると約0.84まで内側へ寄る。極のある箱は1.0の近くに頂点が残る。

## Blender画面で観察する

1. `.blend`を開き、2つの木箱を **View → Frame All** で並べて見る。
2. 左`Crate.Even`は角が丸い。右`Crate.Pole`は一面だけ角張ったまま、または膨らんでいる。
3. 右をEdit Modeにすると、1面の中央に頂点がある。左にはそれがない。
4. ログの`even source=8`、`pole source=9`、極側の`extent`が四角面側より0.1以上大きいことを照合する。

Modifierメニューの **Apply** は押さない。段数は評価の設定で、元の9頂点と8頂点は残っている。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
VIEWPORT_LEVELS = 2
```

これを`1`にして、実行前に予測する。極の面は段数を下げると四角面側と同じ外形になるか。元の頂点数は変わるか。

再実行すると、元の頂点は8と9のまま。段数が1でも、極側の`extent`は四角面側より大きい。確認後は`2`へ戻す。

## 完了条件と次へ

同じSubdivisionでも、面の並びが悪いと角や面が残ることを説明できれば完了。次は [93 支えの辺](../93_support_loops/README.md) で、残したい角の近くにループを足す。
