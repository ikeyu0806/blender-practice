# 71｜Displace：テクスチャの明暗で地面を隆起させる

## このレッスンの目標

地面の元MeshはZの幅が0のまま、CloudsテクスチャのDisplaceで評価後のZに高低ができることを確認する。

前提は [70 Curve](../70_curve/README.md)。Volume側のDisplaceは [68 Volume Displace](../68_volume_displace/README.md)。この回は頂点を動かすMesh用。他のレッスンの出力ファイルは必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Displaceはテクスチャの値で、評価後の頂点を法線方向などへ動かす。
- `mid_level`の0.5は、テクスチャの灰色を動かさない基準にする。
- 頂点が少ない格子では起伏が粗く、分割を増やしてからDisplaceする。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/71_displace/lesson.py
```

`saved: .../output/71_displace.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/71_displace/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Displace Collection
└── Ground.Plain Object → Z=0の格子Mesh
    └── Displace Modifier → Cloudsテクスチャ
        └── 評価後のZ幅が正
```

## 仕組み

手で頂点を上げると、その形が元Meshに保存される。Displaceはテクスチャの明るい部分を`strength`だけ押し、暗い部分を引く。`mid_level`が0.5なので、0.5の灰色は基準面に残る。方向`NORMAL`は各頂点の法線方向で、平らな格子ではほぼZ。

テクスチャはMeshとは別のデータブロック。`noise_scale`を変えると起伏の粗さが変わる。頂点数が少ないと、テクスチャの細かい模様は頂点の間で表現できない。この回は8分割の格子で、高低の差が出ることだけを見る。

元MeshのZ幅は0。ログの`evaluated`が0.02より大きければ、評価後に起伏がある。

## Blender画面で観察する

1. `.blend`を開き、地面を斜めから **View → Frame All** で見る。
2. **Modifier Properties** の`Bumps`でTextureが`Ground.Clouds`、Strengthが0.3であることを確認する。
3. **Show in Viewport** を切ると、平らな格子に戻る。
4. ログの`source z span`が0、`evaluated`がそれより大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると隆起した頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
DISPLACE_STRENGTH = 0.3
```

これを`0.8`にして、実行前に予測する。元のZ幅は0のままか。評価後のZ幅は大きくなるか。

再実行すると、元Meshは平らなままで、評価後の高低差が増える。確認後は`0.3`へ戻す。

## 完了条件と次へ

平らな元Meshが残り、評価後の高低だけがテクスチャ由来であることを説明できれば完了。次は [72 Hook](../72_hook/README.md) で、1つの角だけをEmptyで引っ張る。
