# 80｜Smooth Laplacian：形を保ったまま突起を抑える

## このレッスンの目標

布の元MeshにZ=0.5の突起が残ったまま、Smooth Laplacianの評価後はその高さが下がり、頂点数は変わらないことを確認する。

前提は [78 Smooth](../78_smooth/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Smooth Laplacianは、隣との関係を保ちながら細かい凹凸を評価後にならす。
- `lambda_factor`が大きいと、ならすだけでなく表面が広がりやすい。
- 頂点数は元Meshと同じ。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/80_laplacian_smooth/lesson.py
```

`saved: .../output/80_laplacian_smooth.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/80_laplacian_smooth/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
LaplacianSmooth Collection
└── Clothing.Cloth Object → 1頂点がZ=0.5の格子
    └── Smooth Laplacian Modifier（lambda=0.2, iterations=8）
        └── 評価後の最大Zが0.5未満、頂点数は同じ
```

## 仕組み

Smoothが頂点を隣の位置へ直接寄せるのに対し、Smooth Laplacianは表面の曲がり方を少しずつならす。スキャンのノイズのように、全体の輪郭は残して細かい突起だけを下げたいときに使う。

`lambda_factor`を1に近づけると、突起だけでなく布の幅まで広がりやすい。この回は0.2にして、最大Zが下がることと、頂点数が同じであることを見る。`lambda_border`はフチの頂点への強さ。内側と同じ0.2にする。

元の突起はEdit Modeに残る。回数を増やすと、さらに低くなる。

## Blender画面で観察する

1. `.blend`を開き、布を真横から見る。
2. **Modifier Properties** の`QuietSpike`でLambda Factorが0.2、Repeatが8であることを確認する。
3. **Show in Viewport** を切ると、0.5の突起が戻る。
4. ログの評価後の最大Zが元より小さいことを照合する。

Modifierメニューの **Apply** は押さない。Applyするとならした頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LAMBDA_FACTOR = 0.2
```

これを`0.05`にして、実行前に予測する。突起は残りの高さが0.2のときより高いか。頂点数は同じか。

再実行すると、頂点数は同じで、評価後の最大Zは0.2のときほど下がらない。確認後は`0.2`へ戻す。

## 完了条件と次へ

頂点数は同じで、評価後の突起だけが低くなることを説明できれば完了。次は [81 Surface Deform](../81_surface_deform/README.md) で、粗い布の動きを細かい布へ伝える。
