# 65｜Wireframe：面を辺に沿った骨組みへ置き換える

## このレッスンの目標

檻に見立てた立方体の元Meshは8頂点・6面のまま、Wireframeの評価後は辺に沿った細い枠になり、頂点が増えることを確認する。

前提は [64 Weld](../64_weld/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Wireframeは各面の内側を空け、辺に沿った厚みのある枠を評価後に作る。
- `thickness`は枠の太さ。
- `use_replace`が有効だと、元の面の内側は評価後に残らない。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/65_wireframe/lesson.py
```

`saved: .../output/65_wireframe.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/65_wireframe/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Wireframe Collection
└── Prop.Cage Object → 8頂点の立方体Mesh
    └── Wireframe Modifier（thickness=0.05, replace）
        └── 評価後は辺に沿った枠で、頂点が8より多い
```

## 仕組み

檻、窓枠、金網のように、面の真ん中を空けたいとき、面を削除して辺だけ残すと太さが無い。Wireframeは辺の周囲に厚みのある面を評価後に作る。`use_replace`が有効なので、立方体の6面そのものは評価後に残らず、枠だけが見える。

太さを上げると枠が太くなり、上げすぎると隣の枠とくっついて穴が消える。この回の0.05mは、一辺1.2mの立方体で穴が残る太さ。

Edit Modeは元の立方体。穴の形を変えたいときは、元の辺の位置を変える。

## Blender画面で観察する

1. `.blend`を開き、檻の穴が見える角度で **View → Frame All** する。
2. **Modifier Properties** の`Bars`でThicknessが0.05であることを確認する。
3. **Show in Viewport** を切ると、中身の詰まった立方体に戻る。
4. ログの元頂点が8、評価後がそれより多いことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると枠の頂点が元Meshになり、6面の立方体には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
FRAME_THICKNESS = 0.05
```

これを`0.15`にして、実行前に予測する。元の8頂点は変わるか。枠は太くなり、評価後の頂点は8より多いままか。

再実行すると、元Meshは8頂点のままで、枠が太く見える。確認後は`0.05`へ戻す。

## 完了条件と次へ

元の立方体が残り、評価後だけ辺に沿った枠になっていることを説明できれば完了。次は [66 Mesh to Volume](../66_mesh_to_volume/README.md) で、Meshから体積データを作る。
