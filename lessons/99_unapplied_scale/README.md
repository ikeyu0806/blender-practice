# 99｜Scaleを適用しないとBevelの幅が軸で変わる

## このレッスンの目標

同じBevel幅でも、ObjectのScaleだけをXへ伸ばした木箱は、世界座標の面取りがX側だけ広くなる。頂点座標へ同じ倍率を書き込んだ木箱は、XとYの面取りが揃うことを確認する。

前提は [98 BevelとSubdivisionの順番](../98_bevel_subsurf_order/README.md)。ObjectのScaleとMeshの頂点の違いは [02 Transformと親子](../02_parent_transform/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- Bevelの幅は、ObjectのScaleではなく、Meshのローカル座標で計算される。
- ScaleがXだけ2だと、ローカルの0.2mは世界座標のXでは0.4mになる。
- 画面の **Object → Apply → Scale** は、この倍率を頂点座標へ書き込み、Scaleを1に戻す操作である。右の木箱はその結果と同じ状態である。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/99_unapplied_scale/lesson.py
```

`saved: .../output/99_unapplied_scale.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/99_unapplied_scale/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
UnappliedScale Collection
├── Crate.Scaled Object（Scale X = SCALE_X、Meshは一辺2の立方体）
│   └── Bevel width=0.2（ローカル座標）
└── Crate.Applied Object（Scaleは1、頂点のXだけSCALE_X倍）
    └── Bevel width=0.2（ローカル座標）
```

## 仕組み

ModifierはObjectのローカル座標で動く。その結果へ、ObjectのScaleがかかる。左はMeshが一辺2のままなので、Bevelの0.2mはローカルではXもYも同じ幅である。表示するときXだけ2倍になるので、世界座標ではXの面取りが0.4m、Yが0.2mになる。

右は最初から頂点のXを2倍してあり、Scaleは1である。Bevelの0.2mは世界座標でもXとYで0.2mになる。見た目の幅を揃えたいときは、ScaleをMeshへ書いてから面取りする。

ログの`world inset`は、正の角から面取りで内側へ入った世界座標の距離である。

## Blender画面で観察する

1. `.blend`を開き、左の木箱の角を拡大する。X方向の面取りがYより広い。
2. 右の木箱の角は、XとYで同じ幅に切れている。
3. 左を選び、サイドバーの **Item → Scale** のXが2、右のScaleが1であることを確認する。
4. ログの左は`x`が`y`の約2倍、右は`x`と`y`がほぼ同じであることを照合する。

**Apply** は押さない。画面で左に **Object → Apply → Scale** を実行すると右と同じ関係になるが、その操作は`lesson.py`へは戻らない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SCALE_X = 2.0
```

これを`3.0`にして、実行前に予測する。左の世界座標のX面取りは、Yの何倍になるか。右のXとYは揃ったままか。

再実行すると、左のXのinsetはYの約3倍になる。右は頂点側も3倍の細長い箱になり、面取りのXとYは揃ったままである。確認後は`2.0`へ戻す。

## 完了条件と次へ

未適用のScaleが、Bevel幅を軸ごとに引き伸ばすことを説明できれば完了。次は [100 テクスチャの画素数](../100_texture_resolution/README.md) で、同じUVでも画素が少ないと塊に見えることを見る。
