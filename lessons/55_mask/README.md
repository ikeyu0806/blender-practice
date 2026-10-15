# 55｜Mask：頂点グループで評価後の表示範囲を切る

## このレッスンの目標

木箱の元Meshは8頂点のまま、`KeepUpper`のウェイトが0の下半分が評価後から外れ、頂点数が8未満になることを確認する。

前提は [49 Vertex Weight Proximity](../49_vertex_weight_proximity/README.md) と [54 Edge Split](../54_edge_split/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Maskは頂点を削除せず、ウェイトがしきい値未満の部分を評価結果から外す。
- 残す範囲は頂点グループの名前で決まる。
- `invert_vertex_group`を有効にすると、残る側と外れる側が入れ替わる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/55_mask/lesson.py
```

`saved: .../output/55_mask.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/55_mask/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Mask Collection
└── Prop.Crate Object → 8頂点の立方体Mesh
    ├── Vertex Group KeepUpper（上は1、下は0）
    └── Mask Modifier
        └── 評価後は上側の頂点だけ
```

## 仕組み

Maskは生成というより、評価結果に含める頂点を選ぶ。ウェイト0の頂点と、それだけに支えられていた面は評価後のMeshから外れる。Edit Modeでは8頂点が残っているので、グループの値を変えれば隠していた側を戻せる。

この回はZが正の頂点を1、負の頂点を0にしている。立方体の上の面だけが評価後に残る。ログの`z`は残った頂点のローカルZの範囲。反転すると下側の範囲になる。

Armatureをtargetにすると、骨の選択で表示を切ることもできる。この回は頂点グループだけを使う。

## Blender画面で観察する

1. `.blend`を開き、残った上の面を **View → Frame All** で収める。
2. **Modifier Properties** の`HideLower`でVertex Groupが`KeepUpper`であることを確認する。
3. **Show in Viewport** を切ると、下半分を含む立方体に戻る。
4. Edit Modeで頂点が8個あることを確認する。
5. ログの`evaluated`が8未満で、`z`が正の側であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると外れていた頂点が元Meshから無くなり、下半分を戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
INVERT_GROUP = False
```

これを`True`にして、実行前に予測する。元Meshは8頂点のままか。評価後に残るZは負の側か。

再実行すると、元Meshは8頂点のままで、ログの`z`が負の範囲になる。確認後は`False`へ戻す。

## 完了条件と次へ

元の8頂点が残り、評価後だけウェイト0の側が外れることを説明できれば完了。次は [56 Mirror](../56_mirror/README.md) で、体の右半分から左半分を評価後に作る。
