# 67｜Volume to Mesh：密度から表面のMeshを作る

## このレッスンの目標

殻Objectの元Meshは頂点1つのまま、参照しているVolumeの密度から、評価後に多数の頂点を持つ表面ができることを確認する。

前提は [66 Mesh to Volume](../66_mesh_to_volume/README.md)。この回は66の出力ファイルを使わず、同じ関係をこのスクリプトの中で作り直す。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Volume to MeshはMesh Objectに付け、参照先Volumeの密度の境界面を評価後の表面にする。
- 殻の元Meshは置き場所の受け皿で、表面の頂点は評価後に生成される。
- `threshold`は、どの濃さの升目を内側とみなすか。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/67_volume_to_mesh/lesson.py
```

`saved: .../output/67_volume_to_mesh.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/67_volume_to_mesh/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
VolumeToMesh Collection
├── Rock.Source Object → 立方体Mesh
├── Cloud.Density Object → Volume
│   └── Mesh to Volume → Rock.Source
└── Rock.Shell Object → 頂点1つのMesh
    └── Volume to Mesh → Cloud.Density
        └── 評価後に岩の表面
```

## 仕組み

66で作った密度は、まだ表面の頂点を持たない。Volume to Meshは、密度が`threshold`をまたぐ場所に評価後の面を張る。Modifierが付くのは殻のMesh Objectで、`object`がVolumeを指す。66とは逆向きの参照。

殻の元Meshを頂点1つにしているのは、表面の形が元の頂点から押し出されたものではないと分かるようにするため。ログの`shell source=1`と、数十を超える`evaluated vertices`を見比べる。

岩の立方体、密度のVolume、表面のMeshは3つのObject。どれか1つの参照を外すと、表面だけが消える。

## Blender画面で観察する

1. `.blend`を開き、表面になった岩を **View → Frame All** で見る。
2. `Rock.Shell`の **Modifier Properties** でObjectが`Cloud.Density`、Thresholdが0.1であることを確認する。
3. **Show in Viewport** を切ると、頂点1つの元Meshだけになる。
4. ログの元頂点が1、評価後が50以上であることを照合する。

Modifierメニューの **Apply** は押さない。Applyするとそのときの表面が殻の元Meshになり、Volumeの升目を変えても表面は追従しない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
DENSITY_THRESHOLD = 0.1
```

これを`0.4`にして、実行前に予測する。殻の元頂点は1のままか。評価後の表面は残るか。

再実行すると、元頂点は1のままで、濃い部分だけを内側とみなすので表面の大きさが変わる。確認後は`0.1`へ戻す。

## 完了条件と次へ

殻の元Meshが頂点1つのまま、評価後の表面がVolume由来であることを説明できれば完了。次は [68 Volume Displace](../68_volume_displace/README.md) で、密度をテクスチャで膨らませる。
