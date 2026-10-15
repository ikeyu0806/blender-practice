# 58｜Remesh：今の形から別の格子を評価後に作る

## このレッスンの目標

石に見立てた立方体の元Meshは8頂点のまま、Voxel Remeshの評価後はそれより何倍も多い規則的な格子になることを確認する。

前提は [57 Multiresolution](../57_multires/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Remeshは元の辺の流れを残さず、評価後に新しい面の並びを作る。
- `VOXEL`は、指定したサイズの升目で表面を作り直す。
- 升目を小さくすると評価後の頂点が増え、元の8頂点は残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/58_remesh/lesson.py
```

`saved: .../output/58_remesh.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/58_remesh/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Remesh Collection
└── Stone.Block Object → 8頂点の立方体Mesh
    └── Remesh Modifier（VOXEL, voxel_size=0.25）
        └── 評価後は升目に沿った多数の頂点
```

## 仕組み

Booleanで面が細長くなったあとや、スカルプトで頂点間隔が偏ったあと、表面を一度そろえたいことがある。Remeshは外側の形を読み、別のトポロジーで評価後Meshを作る。元の辺が肘の曲がりに沿っていた、といった情報は引き継がない。

`VOXEL`の`voxel_size`は升目の一辺。0.25mなら、一辺2mの立方体の表面が複数の升目に分割される。`BLOCKS`はMinecraftのような段差、`SHARP`は角を残しやすい八分木。この回は升目の大きさだけを変えて数を見る。

細かい升目は形に忠実で、頂点も増える。大きい升目は角が丸く、頂点は少ない。

## Blender画面で観察する

1. `.blend`を開き、石を **View → Frame All** で収める。ワイヤー表示で升目の並びを見る。
2. **Modifier Properties** の`VoxelGrid`でModeがVoxel、Voxel Sizeが0.25であることを確認する。
3. **Show in Viewport** を切ると、8頂点の立方体に戻る。
4. ログの`source=8`より`evaluated`が数倍以上大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると升目の頂点が元Meshになり、立方体の6面には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
VOXEL_SIZE = 0.25
```

これを`0.15`にして、実行前に予測する。元の8頂点は変わるか。評価後の頂点は増えるか。

再実行すると、元Meshは8頂点のままで、評価後の頂点が増える。確認後は`0.25`へ戻す。

## 完了条件と次へ

元の立方体が残り、評価後だけ升目の格子になっていることを説明できれば完了。次は [59 Screw](../59_screw/README.md) で、断面の辺を回転させて器を作る。
