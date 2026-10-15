# 81｜Surface Deform：粗い布の動きを細かい布へ伝える

## このレッスンの目標

細かい布の元Meshは平らなまま、Bindした粗い布の1頂点を上げると、細かい布の評価後にZが正の頂点が現れることを確認する。

前提は [75 Mesh Deform](../75_mesh_deform/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Surface Deformは、別の表面に貼り付けた関係をBindし、その表面の変形を評価後へ伝える。
- 動かすのはtargetのMeshで、詳細側の元頂点は平らなまま。
- 詳細側がtargetの範囲を大きくはみ出すと、結合や追従が不安定になる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/81_surface_deform/lesson.py
```

`saved: .../output/81_surface_deform.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/81_surface_deform/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
SurfaceDeform Collection
├── Cloth.Driver Object → 粗い格子（1頂点を後から上げる）
└── Cloth.Detail Object → 細かい平らな格子
    └── Surface Deform Modifier（Bind済み）→ Cloth.Driver
        └── 評価後の最大Zが正
```

## 仕組み

シミュレーションや手付けは頂点の少ない布で行い、見た目の布は細かくしておきたいことがある。Surface Deformは、細かい側を粗い表面へBindし、粗い側の頂点移動を補間して評価後へ書く。

この回は細かい布を一辺1.6m、粗い布を2mにして、細かい側が粗い側の内側に収まるようにする。Bindは細かいObjectをアクティブにして行う。そのあと粗い側の頂点0のZを0.4上げる。細かい元MeshのZは0のままで、評価後の最大Zは正になる。

Mesh Deformが体積を包む檻なのに対し、Surface Deformは表面同士の対応。布やデカールを別の表面の変形へ載せるときに使う。

## Blender画面で観察する

1. `.blend`を開き、持ち上がった角を **View → Frame All** で見る。
2. `Cloth.Detail`の **Modifier Properties** で`FollowDriver`がBind済みであることを確認する。
3. **Show in Viewport** を切ると、細かい布は平らに戻る。粗い布の1点は上がったまま。
4. ログの`detail max z`が正であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると追従した頂点が細かい布の元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LIFT_Z = 0.4
```

これを`0.15`にして、実行前に予測する。細かい布の元Meshは平らなままか。評価後の最大Zは小さくなるか。

再実行すると、元の格子は平らなままで、評価後の最大Zが0.4のときより低くなる。確認後は`0.4`へ戻す。

## 完了条件と次へ

細かい布の元Meshが平らなまま、粗い布の1頂点の移動が評価後に出ることを説明できれば完了。次は [82 Warp](../82_warp/README.md) で、2つのEmptyの間で布を引っ張る。
