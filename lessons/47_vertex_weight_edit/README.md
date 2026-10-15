# 47｜Vertex Weight Edit：保存したウェイトを評価後だけ変換する

## このレッスンの目標

腕に見立てた立方体の`Forearm`ウェイトはすべての頂点で0.2のまま、評価後だけ`ROOT`の変換で別の値になることを確認する。

前提は [42 Data Transfer](../42_data_transfer/README.md)。頂点グループの基本は [28 Armatureとウェイト](../28_armature_weights/README.md) でも使う。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Vertex Weight Editは頂点を動かさず、指定した頂点グループの評価後ウェイトを変換する。
- `falloff_type`は、保存された0〜1の値を別の0〜1へ読み替える曲線の種類。
- 元Meshに保存されたウェイトは、後続のModifierやWeight Paintの評価前の値として残る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/47_vertex_weight_edit/lesson.py
```

`saved: .../output/47_vertex_weight_edit.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/47_vertex_weight_edit/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
VertexWeightEdit Collection
└── Arm.Upper Object → Arm.Upper.Mesh
    ├── Vertex Group Forearm（保存値はすべて0.2）
    └── Vertex Weight Edit Modifier（falloff=ROOT）
        └── 評価後のForearmだけが0.2より大きい
```

## 仕組み

頂点グループのウェイトは、各頂点に保存された0〜1の数。Vertex Weight Editはその数を、選んだフォールオフで別の数へ読み替える。`LINEAR`はほぼそのまま、`ROOT`は小さい値を持ち上げ、`SHARP`は小さい値をさらに小さくする。

この回は全頂点を0.2で保存し、`ROOT`で評価する。ログの`stored`は0.2、`evaluated`はそれより大きい。立方体の形と頂点数は変わらない。後にMaskやArmatureを積むと、この評価後の値がそちらの入力になる。

`use_add`はしきい値を超えた頂点をグループへ加え、`use_remove`はしきい値未満を外す。この回は既に全員が入っているグループの値だけを変換する。

## Blender画面で観察する

1. `.blend`を開き、`Arm.Upper`を選ぶ。
2. **Modifier Properties** で`RemapForearm`のVertex Groupが`Forearm`、Falloff TypeがRootであることを確認する。
3. Weight Paintで、Modifierの表示を切ったときの赤さ（0.2）と、有効なときの濃さを比べる。
4. ログの`stored=0.200`と、それより大きい`evaluated`を照合する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、評価後の変換が外れ、保存値0.2の見え方に戻る。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
FALLOFF = "ROOT"
```

これを`"SHARP"`にして、実行前に予測する。保存値は0.2のままか。評価後は0.2より小さくなるか。

再実行すると、元Meshは0.2のままで、評価後は0.2より小さい値になる。確認後は`"ROOT"`へ戻す。

## 完了条件と次へ

保存ウェイトと評価後ウェイトが違い、フォールオフの種類で評価後の大小が変わることを説明できれば完了。次は [48 Vertex Weight Mix](../48_vertex_weight_mix/README.md) で、2つのグループを混ぜる。
