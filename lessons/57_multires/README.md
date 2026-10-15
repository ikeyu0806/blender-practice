# 57｜Multiresolution：細かい段を元の8頂点と別に持つ

## このレッスンの目標

眉に見立てた立方体の元Meshは8頂点のまま、Multiresolutionで1段細分化した評価後は頂点が増えることを確認する。段はModifier側に積む。

前提は [56 Mirror](../56_mirror/README.md)。高密度の造形から辺を作り直す流れは [32 Sculptとリトポロジー](../32_sculpt_retopology/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Multiresolutionは、Subdivisionに似た細分化を段としてModifierに保存する。
- 表示レベルを上げる前に、Subdivideで段を追加する。
- 元Meshの頂点数は8のままで、細かい頂点は評価後に現れる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/57_multires/lesson.py
```

`saved: .../output/57_multires.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/57_multires/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Multiresolution Collection
└── Monster.Brow Object → 8頂点の立方体Mesh
    └── Multiresolution Modifier（total levels ≥ 1）
        └── 評価後の頂点が8より多い
```

## 仕組み

Sculptで角や眉の稜線を足したいとき、最初から元Meshを細かく割ると、大きな形を直しにくい。Multiresolutionは細かい段をModifierに持ち、表示レベルを下げれば荒い立方体の編集に戻れる。

`multires_subdivide`は段を1つ追加するOperatorで、アクティブなObjectが必要。Levelsの数値だけを大きくしても、積んだ段より細かくはならない。ログの`total`が積んだ段、`levels`が表示に使っている段。

次のSubdivision Surfaceは段を後から捨てやすい平滑化で、Multiresolutionは段ごとの変位を保持できる点が違う。この回は変位を彫る前の、段を積んだ状態を見る。

## Blender画面で観察する

1. `.blend`を開き、`Monster.Brow`を **View → Frame All** で収める。角が立方体より滑らかになっていることを確認する。
2. **Modifier Properties** の`SculptLevels`でLevelと、積んである段数を見る。
3. Levelを0にすると、評価結果が元の立方体に近づく。段の削除とは別の操作。
4. Edit Modeでは頂点が8個であることを確認する。
5. ログの`source=8`と、それより大きい`evaluated`を照合する。

Modifierメニューの **Apply** は押さない。Applyすると表示レベルの頂点が元Meshになり、レベル0の8頂点には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SUBDIVIDE_TIMES = 1
```

これを`2`にして、実行前に予測する。元Meshは8頂点のままか。評価後の頂点は1段のときより増えるか。

再実行すると、元Meshは8頂点のままで、`total`が2になり評価後の頂点が増える。確認後は`1`へ戻す。

## 完了条件と次へ

元の8頂点が残り、細分化の段を積んだ評価後だけ頂点が増えることを説明できれば完了。次は [58 Remesh](../58_remesh/README.md) で、今の形から別の格子を作り直す。
