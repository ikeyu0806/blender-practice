# 50｜Array：1つの柱を評価結果の中で繰り返す

## このレッスンの目標

柵の柱1本の元Meshは8頂点のまま、評価後だけ`POST_COUNT`本に増えることを確認する。繰り返しはObjectの複製ではなく、Modifierの評価結果である。

前提は [49 Vertex Weight Proximity](../49_vertex_weight_proximity/README.md)。同じ部品をCollectionで置く方法は [18 反復配置](../18_collection_instances/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Arrayは元Meshを複製せず、評価後の形の中でコピーを並べる。
- `count`は評価後に見える個数。元Meshの`users`は1のまま。
- Relative Offsetの1.0は元の寸法ちょうど。1より大きいと隙間が空く。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/50_array/lesson.py
```

`saved: .../output/50_array.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/50_array/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Array Collection
└── Fence.Post Object → Fence.Post.Mesh（柱1本、8頂点）
    └── Array Modifier（count=4, Xへ1.8倍の間隔）
        └── 評価後は32頂点、柱4本
```

## 仕組み

Arrayは生成系のModifierで、評価のときに形状のコピーを足す。Outlinerに柱Objectが4個できるわけではない。`count`を変えると評価後の本数だけが変わる。

Relative Offsetは、元Meshの寸法を1とした倍率。Xの1.8は、柱の幅の1.8倍ずつ右へ置く。Constant Offsetならメートル単位の固定距離になる。この回は幅に対する倍率の方が、柱を伸ばしても隙間の意味が残るのでRelativeを使う。

頂点をZへ4倍しているのは、立方体を柱の比率にするため。これはMeshの座標変更で、Arrayとは別の操作。ObjectのScaleは1のまま。

## Blender画面で観察する

1. `.blend`を開き、4本の柱を **View → Frame All** で収める。
2. Outlinerでは`Fence.Post`が1個であることを確認する。
3. **Modifier Properties** の`RepeatPosts`でCountが4、Relative OffsetのXが1.8であることを確認する。
4. **Show in Viewport** を切ると柱1本に戻る。元Meshは最初から1本しかない。
5. ログの`source vertices=8`と`evaluated=32`を照合する。

Modifierメニューの **Apply** は押さない。Applyすると、4本分が編集可能な1つのMeshになり、元の1本には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
POST_COUNT = 4
```

これを`6`にして、実行前に予測する。元Meshは8頂点のままか。評価後は48頂点になるか。

再実行すると、保存される柱は1本のままで、評価後の頂点数が48になる。確認後は`4`へ戻す。

## 完了条件と次へ

Objectは1個、元Meshは8頂点、評価後だけ本数倍になっていることを説明できれば完了。次は [51 Boolean](../51_boolean/README.md) で、別の形を使って壁に開口を作る。
