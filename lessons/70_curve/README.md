# 70｜Curve：尾をBezier曲線に沿わせる

## このレッスンの目標

尾の元MeshはZ=0の帯のまま、Curve Modifierの評価後は途中のZが持ち上がることを確認する。曲線は別のCurve Object。

前提は [69 Cast](../69_cast/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Curve Modifierは、Meshの頂点を別のCurve Objectの形へ評価後だけ沿わせる。
- `deform_axis`は、元Meshのどの軸を曲線の長さとみなすか。
- 曲線の制御点を動かすと、尾の元頂点を編集しなくても評価後の曲がりが変わる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/70_curve/lesson.py
```

`saved: .../output/70_curve.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/70_curve/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Curve Collection
├── Tail.Path Object → Bezier Curve（中央が持ち上がる）
└── Monster.Tail Object → Z=0の帯Mesh
    └── Curve Modifier（deform_axis=+X）→ Tail.Path
        └── 評価後のZが正になる
```

## 仕組み

尾やツタをMeshの頂点だけで曲げると、曲がり具合を後から滑らかに直しにくい。Curve Objectに制御点を置き、Mesh側のCurve Modifierがその曲線を参照する。元の帯はX方向に長く、Zは0。`POS_X`は、その長さ方向を曲線に乗せる指定。

曲線の2点目のZが`ARC_HEIGHT`。評価後の尾の最大Zは0より大きくなる。Edit Modeの帯は平らなまま。CurveデータとMeshデータは別のデータブロックで、Modifierが両者を評価時につなぐ。

軸を間違えると、尾の幅方向が曲線に乗り、長さが潰れて見える。まず長さの軸と`deform_axis`を揃える。

## Blender画面で観察する

1. `.blend`を開き、尾と曲線を **View → Frame All** で見る。
2. `Monster.Tail`の **Modifier Properties** でObjectが`Tail.Path`、Deform AxisがXであることを確認する。
3. **Show in Viewport** を切ると、平らな帯に戻る。
4. ログの`source max z`が0、`evaluated max z`が正であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると曲がった頂点が元Meshになり、曲線を動かしても尾は追従しない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
ARC_HEIGHT = 0.8
```

これを`0.3`にして、実行前に予測する。元の帯のZは0のままか。評価後の最大Zは小さくなるか。

再実行すると、元Meshは平らなままで、評価後の最大Zが0.8のときより低くなる。確認後は`0.8`へ戻す。

## 完了条件と次へ

尾の元Meshが平らなまま、評価後の高さだけが曲線に追従することを説明できれば完了。次は [71 Displace](../71_displace/README.md) で、テクスチャの明暗で地面を隆起させる。
