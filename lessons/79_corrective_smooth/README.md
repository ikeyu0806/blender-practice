# 79｜Corrective Smooth：ねじった袖の評価後を整える

## このレッスンの目標

1つの袖Meshを2つのObjectが共有し、両方に同じねじりを掛けたうえで、右側だけCorrective Smoothを足すと、評価後の頂点位置が左右でずれることを確認する。

前提は [78 Smooth](../78_smooth/README.md) と [01 共有Mesh](../01_shared_mesh/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Corrective Smoothは、その前の変形で崩れた頂点を、元の形に近づくよう評価後にならす。
- 同じ元Meshでも、ModifierがObject側なので左右の評価結果は別になる。
- 通常のSmoothが突起を消すのに対し、こちらは変形の前後の差を補正する。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/79_corrective_smooth/lesson.py
```

`saved: .../output/79_corrective_smooth.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/79_corrective_smooth/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
CorrectiveSmooth Collection
├── Sleeve.Twisted Object ──┐
│   └── Twistだけ           ├──> Sleeve.Mesh
└── Sleeve.Fixed Object ────┘
    ├── Twist
    └── Corrective Smooth
        └── 評価後の位置が左とずれる
```

## 仕組み

関節を大きく曲げると、内側の頂点が潰れて体積が細くなる。Corrective Smoothは、変形前の形を基準に、潰れた頂点を評価後だけ押し戻す。この回は基準を見るために、Simple Deformのねじりを両方へ同じ設定で置き、右側だけ補正を足す。

元Meshは1つ。左右の差はModifier stackの差。ログの`delta`は、対応する評価後頂点の最大距離。0.05より大きければ、補正が位置を変えている。

`rest_source`の既定`ORCO`は、変形前の座標を基準にする。`BIND`はボタンで記録した形を基準にする。この回はねじりModifierの前の立方体分割を基準にできる`ORCO`のまま。

## Blender画面で観察する

1. `.blend`を開き、左右の袖を **View → Frame All** で見比べる。
2. 右の **Modifier Properties** に`Twist`と`KeepVolume`の順で並んでいることを確認する。
3. 右の`KeepVolume`の表示を切ると、左に近いねじりだけになる。
4. ログの`delta`が0より大きいことを照合する。

Modifierメニューの **Apply** は押さない。補正だけをApplyすると、そのときの頂点が元Meshになり、左の共有Meshも変わる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
FIX_ITERATIONS = 15
```

これを`3`にして、実行前に予測する。左右の差は残るか。元Meshは1つのままか。

再実行すると、共有Meshは1つのままで、`delta`は15のときより小さくなる。確認後は`15`へ戻す。

## 完了条件と次へ

同じ元Meshなのに、補正を足したObjectの評価後だけ位置がずれることを説明できれば完了。次は [80 Smooth Laplacian](../80_laplacian_smooth/README.md) で、形を大きく変えずに突起を抑える。
