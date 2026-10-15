# 69｜Cast：頂点を球までの距離へ寄せる

## このレッスンの目標

石の元Meshは頂点ごとに原点からの距離が違うまま、Castの評価後は距離のばらつきが元より小さくなることを確認する。

前提は [62 Subdivision Surface](../62_subdivision/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Castは頂点を、球や円柱などの単純な形へ評価後だけ動かす。
- `factor`が1なら目標の形、0なら元の頂点位置。
- 頂点数は変わらず、動くのは評価後の座標。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/69_cast/lesson.py
```

`saved: .../output/69_cast.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/69_cast/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Cast Collection
└── Stone.Mound Object → 中央が盛り上がった格子Mesh
    └── Cast Modifier（SPHERE, factor=1）
        └── 評価後は原点からの距離がほぼ揃う
```

## 仕組み

でこぼこを一度球にまとめたいとき、頂点を手で円周上へ動かすと元の起伏を失う。Castは評価後の座標だけを球へ寄せる。`factor`が1のとき、ログの距離の最大と最小の差は元より小さい。

入力の格子は、中心ほどZが高い。この起伏があるので、元の距離にはばらつきがある。球へ寄せたあとも頂点数は同じで、Edit Modeの起伏は残る。

`CUBOID`や`CYLINDER`に変えると、目標の形が球ではなくなる。この回は球だけを見る。

## Blender画面で観察する

1. `.blend`を開き、石を **View → Frame All** で見る。丸い塊になっていることを確認する。
2. **Modifier Properties** の`ToSphere`でTypeがSphere、Factorが1であることを確認する。
3. **Show in Viewport** を切ると、中央が盛り上がった格子に戻る。
4. ログの`evaluated range`が`source range`より小さいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると球に寄った頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
CAST_FACTOR = 1.0
```

これを`0.5`にして、実行前に予測する。距離のばらつきは0より大きく、元よりは小さいか。

再実行すると、評価後の距離差は元より小さく、1.0のときよりは起伏が残る。確認後は`1.0`へ戻す。

## 完了条件と次へ

頂点数はそのままで、評価後の原点からの距離が揃う方向へ寄ることを説明できれば完了。次は [70 Curve](../70_curve/README.md) で、尾を曲線に沿わせる。
