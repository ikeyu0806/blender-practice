# 53｜Decimate：細かい面を評価後だけ減らす

## このレッスンの目標

地面の元Meshは100頂点以上のまま、Collapseの比率0.2で評価後の頂点が半分未満になることを確認する。

前提は [52 Build](../52_build/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Decimateの`COLLAPSE`は、評価後の頂点を辺の折りたたみで減らす。
- `ratio`は残す割合の目安。1に近いほど元の密度に近い。
- 元Meshの頂点数は減らないので、比率を戻せば評価後の密度も戻る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/53_decimate/lesson.py
```

`saved: .../output/53_decimate.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/53_decimate/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Decimate Collection
└── Ground.Detail Object → 細かい格子Mesh
    └── Decimate Modifier（COLLAPSE, ratio=0.2）
        └── 評価後の頂点だけが半分未満
```

## 仕組み

細かい彫刻やスキャンをそのまま置くと頂点が多すぎることがある。Decimateは評価のときに頂点をまとめる。`COLLAPSE`は短い辺を折りたたみ、`ratio`で残す量の目安を決める。`UNSUBDIV`はSubdivisionの逆、`PLANAR`はほぼ平らな面を結合する。この回は折りたたみだけを見る。

比率0.2でも頂点数が正確に20%になるとは限らない。折りたたみの結果として、ログでは元の半分未満まで減ることを確認する。Edit Modeの格子は元の分割数のまま。

減らしすぎるとシルエットが欠ける。比率は見た目と頂点数の両方で決める。

## Blender画面で観察する

1. `.blend`を開き、地面を **View → Frame All** で収める。
2. **Modifier Properties** の`Reduce`でTypeがCollapse、Ratioが0.2であることを確認する。
3. **Show in Viewport** を切り、細かい格子と間引いた面を往復する。
4. ログの`source`が100以上、`evaluated`がその半分未満であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると間引いた形が元Meshになり、細かい格子には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
KEEP_RATIO = 0.2
```

これを`0.6`にして、実行前に予測する。元の頂点数は変わるか。評価後の頂点は0.2のときより増えるか。

再実行すると、元Meshの頂点数は同じで、評価後は0.2のときより多く残る。確認後は`0.2`へ戻す。

## 完了条件と次へ

元の格子が残ったまま、評価後の頂点だけが比率に応じて減ることを説明できれば完了。次は [54 Edge Split](../54_edge_split/README.md) で、鋭い辺の頂点を評価後だけ分ける。
