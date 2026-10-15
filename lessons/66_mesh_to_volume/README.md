# 66｜Mesh to Volume：Meshから密度の体積を作る

## このレッスンの目標

岩のMesh ObjectにはModifierが無く、8頂点の立方体のままである一方、別のVolume Objectに付けたMesh to Volumeが岩を参照し、評価後のVolumeに密度グリッドができることを確認する。

前提は [65 Wireframe](../65_wireframe/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。Blender 5.2.2で確認する。

完了時には、次を自分の言葉で説明できるようにする。

- Mesh to Volumeは、Blender 5.2ではVolume Object側に追加する。
- Modifierの`object`が、体積の形の元になるMesh Object。
- 岩の頂点は体積へコピーされず、評価後のVolumeが密度グリッドを持つ。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/66_mesh_to_volume/lesson.py
```

`saved: .../output/66_mesh_to_volume.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/66_mesh_to_volume/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
MeshToVolume Collection
├── Rock.Source Object → 立方体Mesh（Modifierなし）
└── Cloud.Density Object → Volumeデータ
    └── Mesh to Volume Modifier → Rock.Sourceを参照
        └── 評価後のVolumeに密度グリッド
```

## 仕組み

Meshは表面の頂点・辺・面。煙、霧、中身の詰まった塊を升目で扱いたいときはVolumeという別のObject Dataを使う。Blender 5.2のMesh to Volumeは、Mesh Objectに足すのではなく、空のVolume Objectに足して、参照先Meshの内側に密度を書く。

`resolution_mode`の`VOXEL_SIZE`は升目の一辺をメートルで決める。`VOXEL_AMOUNT`は一辺の升目数で決める。`density`はその内側の濃さ。ログの`grids`が1以上なら、評価後に密度の入れ物ができている。

ビューポートのVolume表示は、固体のMeshより薄い。Wire表示の岩と、Volumeの雲を同時に見て、データが別Objectであることを確認する。

## Blender画面で観察する

1. `.blend`を開き、岩とVolumeを **View → Frame All** で収める。
2. `Cloud.Density`の **Modifier Properties** で`FromRock`のObjectが`Rock.Source`であることを確認する。
3. `Rock.Source`にはModifierが無いことを確認する。
4. ビューポートをRenderedまたはMaterial Previewにすると、密度の塊が見えやすい。
5. ログの`rock modifiers=0`と`grids`が1以上であることを照合する。

Modifierメニューの **Apply** は押さない。参照を外すと、Volume側の評価結果から岩の形が消える。岩Mesh自体は残る。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
VOXEL_SIZE = 0.12
```

これを`0.25`にして、実行前に予測する。岩の頂点数は変わるか。密度グリッドは残るか。

再実行すると、岩は8頂点のままで、`grids`は1以上のまま、雲の段差は粗くなる。確認後は`0.12`へ戻す。

## 完了条件と次へ

岩ObjectにModifierが無く、Volume Objectの評価後にグリッドがあることを説明できれば完了。次は [67 Volume to Mesh](../67_volume_to_mesh/README.md) で、その密度から再び表面Meshを作る。
