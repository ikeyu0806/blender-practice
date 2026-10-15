# 48｜Vertex Weight Mix：2つの頂点グループを評価後だけ混ぜる

## このレッスンの目標

`Upper`は0.25、`Lower`は0.75のまま保存し、評価後の`Upper`だけが両者の平均になることを確認する。

前提は [47 Vertex Weight Edit](../47_vertex_weight_edit/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Vertex Weight Mixは、グループBの値を使ってグループAの評価後ウェイトを作る。
- 結果が書かれるのは評価後のAで、AとBの保存値は残る。
- `AVG`は平均、`ADD`は足し算、という演算の種類を`mix_mode`で選ぶ。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/48_vertex_weight_mix/lesson.py
```

`saved: .../output/48_vertex_weight_mix.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/48_vertex_weight_mix/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
VertexWeightMix Collection
└── Arm.Blend Object → Arm.Blend.Mesh
    ├── Vertex Group Upper（保存値0.25）
    ├── Vertex Group Lower（保存値0.75）
    └── Vertex Weight Mix Modifier（A=Upper, B=Lower, mode=AVG）
        └── 評価後のUpperが0.5
```

## 仕組み

骨を2本混ぜたいとき、頂点グループを直接平均して保存すると、元の`Upper`と`Lower`を後から戻せない。Vertex Weight Mixは評価のときだけAを計算し直す。この回の`AVG`では、0.25と0.75の平均で評価後の`Upper`が0.5になる。

`mix_set`の`ALL`は、どちらのグループにも入っていない頂点も含めて計算する。この回は全頂点が両方に入っているので、平均の対象は立方体の8頂点すべて。

Bの保存値はこのModifierでは書き換えない。ログに出るのは、変化が見えるAの保存値と評価後。

## Blender画面で観察する

1. `.blend`を開き、`Arm.Blend`を選ぶ。
2. **Object Data Properties** に`Upper`と`Lower`の2つの頂点グループがあることを確認する。
3. **Modifier Properties** の`BlendBones`で、AがUpper、BがLower、Mix ModeがAverageであることを確認する。
4. ログの`stored Upper=0.250`と`evaluated Upper=0.500`を照合する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、評価後の`Upper`は保存値0.25の見え方に戻る。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
MIX_MODE = "AVG"
```

これを`"ADD"`にして、実行前に予測する。評価後の`Upper`は0.25+0.75で1に近づくか。保存された`Upper`は0.25のままか。

再実行すると、保存値は0.25のままで、評価後の`Upper`は1になる。確認後は`"AVG"`へ戻す。

## 完了条件と次へ

`Upper`の保存値が0.25のまま、評価後だけ`Lower`と演算された値になっていることを説明できれば完了。次は [49 Vertex Weight Proximity](../49_vertex_weight_proximity/README.md) で、別Objectとの距離からウェイトを作る。
