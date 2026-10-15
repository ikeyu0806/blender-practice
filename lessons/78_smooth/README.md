# 78｜Smooth：突き出した頂点を周りへならす

## このレッスンの目標

布の元MeshにはZ=0.5の突起が残ったまま、Smoothの評価後はその最大Zが低くなることを確認する。

前提は [77 Simple Deform](../77_simple_deform/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Smoothは各頂点を、隣の頂点の位置へ評価後だけ近づける。
- `iterations`はならす回数、`factor`は1回で寄せる強さ。
- 元Meshの突起は残るので、回数を減らせば尖りを戻せる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/78_smooth/lesson.py
```

`saved: .../output/78_smooth.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/78_smooth/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Smooth Collection
└── Clothing.Cloth Object → 1頂点だけZ=0.5の格子
    └── Smooth Modifier（factor=1, iterations=10）
        └── 評価後の最大Zが0.5未満
```

## 仕組み

スキャンや押し出しのあとに、1点だけ飛び出した頂点が残ることがある。Smoothはその頂点を隣の平均へ繰り返し近づける。布の意図した折りまで消えるので、全体に強くかける前に回数を見る。

この回は格子の1頂点だけを0.5m上げ、`iterations`を10、`factor`を1にする。ログの評価後の最大Zは0.5より小さい。Edit Modeでは突起が残っている。

頂点グループを指定すると、ならす範囲をそのグループに限れる。この回は布全体。

## Blender画面で観察する

1. `.blend`を開き、布を真横から **View → Frame All** で見る。
2. **Modifier Properties** の`FlattenSpike`でFactorが1、Repeatが10であることを確認する。
3. **Show in Viewport** を切ると、1点の突起が戻る。
4. ログの`evaluated`が`source max z`より小さいことを照合する。

Modifierメニューの **Apply** は押さない。Applyするとならした頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SMOOTH_ITERATIONS = 10
```

これを`2`にして、実行前に予測する。突起は完全には消えず、最大Zは0.5より少し低い程度か。

再実行すると、元の突起は0.5のままで、評価後の最大Zは10回のときより高い。確認後は`10`へ戻す。

## 完了条件と次へ

元の突起が残り、評価後の高さだけがならし回数で下がることを説明できれば完了。次は [79 Corrective Smooth](../79_corrective_smooth/README.md) で、ねじったあとの形を体積を保つように整える。
