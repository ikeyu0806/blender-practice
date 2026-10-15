# 77｜Simple Deform：板を円弧に曲げる

## このレッスンの目標

板の元Meshは平らな格子のまま、Simple DeformのBendが評価後のX幅を変えることを確認する。曲げる角度はModifier側の値。

前提は [76 Shrinkwrap](../76_shrinkwrap/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Simple Deformは、曲げ、ねじり、先細り、伸縮を1つのModifierで切り替える。
- `BEND`の`angle`は円弧の角度、`deform_axis`は曲げるときの軸。
- 原点の位置が曲がりの中心になる。元の頂点座標は残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/77_simple_deform/lesson.py
```

`saved: .../output/77_simple_deform.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/77_simple_deform/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
SimpleDeform Collection
└── Prop.Plank Object → 細長い格子Mesh
    └── Simple Deform Modifier（BEND, 90度, 軸Z）
        └── 評価後のX幅が元の直線と違う
```

## 仕組み

角、板、帯を円弧にしたいとき、曲線を別Objectで用意する前に、角度だけで試せる。`BEND`は指定軸の周りに頂点を円弧へ並べる。この回の板はXY平面に長く、軸Zなので上から見て弧を描く。

90度では端が回り、直線のときのX幅と評価後のX幅がずれる。ログはその差が0.2より大きいことを確認する。`TWIST`は軸の周りにねじり、`TAPER`は先を細くし、`STRETCH`は軸方向へ伸縮する。方法を変えても元Meshは同じ格子。

原点が板の中央にあるので、弧は中央を基準に左右へ開く。原点を端へ移すと、曲がりの中心も端になる。

## Blender画面で観察する

1. `.blend`を開き、上から板の弧を **View → Frame All** で見る。
2. **Modifier Properties** の`BendArc`でMethodがBend、Angleが90度であることを確認する。
3. **Show in Viewport** を切ると、まっすぐな板に戻る。
4. ログの`source x`と`evaluated x`が違うことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると弧の頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
BEND_ANGLE = radians(90)
```

これを`radians(45)`にして、実行前に予測する。弧は緩くなるか。元の格子は平らなままか。

再実行すると、元Meshは平らなままで、評価後のX幅の変化が90度のときより小さくなる。確認後は`radians(90)`へ戻す。

## 完了条件と次へ

平らな板が残り、評価後の幅だけが曲げ角度で変わることを説明できれば完了。次は [78 Smooth](../78_smooth/README.md) で、突き出した頂点を周りへならす。
