# 73｜Laplacian Deform：固定点の間の布のつながりを保って曲げる

## このレッスンの目標

マントの左右の端を固定して結合したあと、右の固定点だけを上げると、評価後の表面は右が高く左は低いままであることを確認する。

前提は [72 Hook](../72_hook/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Laplacian Deformは、頂点グループの固定点を動かしたとき、周りの面のつながりを評価後に保とうとする。
- 使う前にBindが必要。BindしていないModifierは変形しない。
- 固定点以外の頂点は、隣との関係から評価後の位置が決まる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/73_laplacian_deform/lesson.py
```

`saved: .../output/73_laplacian_deform.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/73_laplacian_deform/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
LaplacianDeform Collection
└── Clothing.Cape Object → 格子Mesh
    ├── Vertex Group Pins（左右の端）
    └── Laplacian Deform Modifier（Bind済み）
        └── 右を上げた評価後は、右が高く左は低い
```

## 仕組み

布の端だけを持って中間を自然に垂らしたいとき、端の頂点だけを動かすと中間が伸びきることがある。Laplacian DeformはBindした時点の隣同士の関係を記憶し、固定点の新しい位置に合わせて残りの頂点を評価する。

固定点は頂点グループ`Pins`。左右の端を1、中央を0にする。BindはアクティブObjectに対するOperatorで、成功すると`is_bind`が真になる。そのあとで右端の元頂点のZを上げる。評価後の最大Zは上がり、最小Zは左端付近に残る。

Bind前に頂点を動かすと、その形が基準になる。順序は「グループを作る、Bindする、固定点を動かす」。

## Blender画面で観察する

1. `.blend`を開き、右が持ち上がったマントを **View → Frame All** で見る。
2. **Modifier Properties** の`KeepCloth`がBind済みで、Vertex Groupが`Pins`であることを確認する。
3. **Show in Viewport** を切ると、右端だけが持ち上がった元の格子になる。
4. ログのZ範囲が、低い側と高い側の両方を含むことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると評価後の頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LIFT_Z = 0.4
```

これを`0.15`にして、実行前に予測する。Bindは成功したままか。評価後の最大Zは小さくなるか。

再実行すると、右端の持ち上がりが小さくなり、左は低い側に残る。確認後は`0.4`へ戻す。

## 完了条件と次へ

Bind済みで、右の固定点の移動が表面の評価後に広がり、左は低く残ることを説明できれば完了。次は [74 Lattice](../74_lattice/README.md) で、格子の点を動かして箱を歪める。
