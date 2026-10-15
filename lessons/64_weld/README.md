# 64｜Weld：重なった頂点を評価後だけまとめる

## このレッスンの目標

鎧の板に見立てたMeshは、同じ座標の頂点を2つ持った4頂点のまま、評価後は距離のしきい値以内の頂点がまとまって4未満になることを確認する。

前提は [63 Triangulate](../63_triangulate/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Weldは、`merge_threshold`より近い頂点を評価後に1つへまとめる。
- 元Meshに重なった頂点が残るので、しきい値を変えると結合の範囲を戻せる。
- 離れた頂点を形作るための距離まではまとめない。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/64_weld/lesson.py
```

`saved: .../output/64_weld.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/64_weld/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Weld Collection
└── Armor.Plate Object → 4頂点（うち2つは同じ座標）・2面
    └── Weld Modifier（merge_threshold=0.01）
        └── 評価後の頂点は4未満
```

## 仕組み

Mirrorの中央や、別部品をくっつけた継ぎ目では、見た目は1点でも頂点データが2つあることがある。Weldは距離以内の頂点を評価後に結合し、面の重複も整理する。

この回は原点に同じ座標の頂点を2つ置き、同じ三角形を2枚重ねている。0.01m以内なので評価後は1点にまとまり、面も1枚へ減る。1m離れた反対側の頂点はしきい値の外なので残る。

しきい値を大きくしすぎると、意図して離してあった頂点まで1つになる。継ぎ目の隙間より少し大きい値から試す。

## Blender画面で観察する

1. `.blend`を開き、板を **View → Frame All** で見る。
2. **Modifier Properties** の`MergeSeam`でDistanceが0.01であることを確認する。
3. **Show in Viewport** を切ると、重なった2面の元Meshに戻る。
4. ログの元頂点が4、評価後がそれより少ないことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると結合後の頂点が元Meshになり、重なっていた2点には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
MERGE_DISTANCE = 0.01
```

これを`0.001`にして、実行前に予測する。同じ座標の2点はまだまとまるか。元の4頂点は残るか。

再実行すると、元Meshは4頂点のままで、距離0の2点は0.001以内なので評価後もまとまる。確認後は`0.01`へ戻す。

## 完了条件と次へ

元の4頂点が残り、評価後だけ近い頂点が減っていることを説明できれば完了。次は [65 Wireframe](../65_wireframe/README.md) で、面を骨組みの筒へ置き換える。
