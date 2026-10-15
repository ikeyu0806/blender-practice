# 74｜Lattice：格子点で箱の評価後の形を歪める

## このレッスンの目標

箱の元Meshは一辺2mの立方体のまま、それを包むLatticeの上側の点をXへ動かすと、評価後のX幅だけが広がることを確認する。

前提は [73 Laplacian Deform](../73_laplacian_deform/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Latticeは、少数の格子点の位置で、中にあるMeshの評価後座標を曲げる。
- Lattice ModifierはMesh Object側にあり、参照先はLattice Object。
- 格子が対象を包んでいないと、頂点はほとんど動かない。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/74_lattice/lesson.py
```

`saved: .../output/74_lattice.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/74_lattice/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Lattice Collection
├── Crate.Cage Object → Latticeデータ（2×2×2、Scaleは2）
└── Crate.Body Object → 8頂点の立方体Mesh
    └── Lattice Modifier → Crate.Cage
        └── 評価後のX幅が元より広い
```

## 仕組み

箱の頂点を1つずつ動かすと、後から「上だけ右へ」を戻しにくい。Latticeは箱とは別のObjectで、U・V・W方向の点を動かすと、その中のMesh頂点が評価後に補間される。

既定のLatticeは1m程度の範囲なので、一辺2mの箱を包むようObjectのScaleを2にしている。ScaleはLattice ObjectのTransformで、箱Meshの頂点座標ではない。上側（ローカルZが正）の格子点だけXを足すので、箱の上側が横へ広がり、ログのX幅が増える。

同じLatticeを複数のMeshから参照すると、1つの格子で服と体を一緒に曲げられる。この回は箱1つ。

## Blender画面で観察する

1. `.blend`を開き、箱と周りの格子を **View → Frame All** で見る。
2. `Crate.Body`の **Modifier Properties** でObjectが`Crate.Cage`であることを確認する。
3. **Show in Viewport** を切ると、幅が揃った立方体に戻る。
4. ログの`evaluated x`が`source x`より大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると歪んだ頂点が箱の元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SHIFT_X = 0.4
```

これを`0.15`にして、実行前に予測する。箱の元のX幅は変わるか。評価後の広がりは小さくなるか。

再実行すると、元の立方体の幅は同じで、評価後のX幅の増加が小さくなる。確認後は`0.4`へ戻す。

## 完了条件と次へ

箱の8頂点が残り、Latticeの点の移動だけが評価後の幅に出ることを説明できれば完了。次は [75 Mesh Deform](../75_mesh_deform/README.md) で、別の粗いMeshを檻にして変形する。
