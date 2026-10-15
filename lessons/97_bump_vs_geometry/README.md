# 97｜Bumpは輪郭を変えず、Displaceは頂点を動かす

## このレッスンの目標

同じ板Meshを2つのObjectが参照する。左はBumpで法線だけを曲げ、右はDisplaceで評価後の頂点が上下することを確認する。

前提は [96 Roughnessの差](../96_roughness_variation/README.md)。Displaceの仕組みは [71 Displace](../71_displace/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- Bumpは光の計算に使う法線を傾け、保存される頂点も評価後の頂点も動かない。
- 真横から見た輪郭（シルエット）は頂点の位置で決まる。Bumpでは板のままである。
- 近づいて見える傷や布目はBumpで足りることが多く、輪郭まで曲がる凹凸は頂点かDisplaceが要る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/97_bump_vs_geometry/lesson.py
```

`saved: .../output/97_bump_vs_geometry.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/97_bump_vs_geometry/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
BumpVsGeometry Collection
├── Ground.Shaded Object ─┐
│                         ├── Ground.Shaded.Mesh → Material.Board（Noise → Bump → Normal）
└── Ground.Raised Object ─┘
    └── Displace Modifier（右だけ。評価後のZが動く）
```

## 仕組み

マテリアルのBumpは、面の明るさの計算に使う法線を画素ごとに傾ける。カメラの外側の線は頂点を結んだ形なので、法線を曲げても板の縁は直線のままである。布の織りや細かい傷を、頂点を何倍にもせずに見せるときに使う。

Displaceは評価後の頂点をテクスチャの明暗で動かす。右の板を真横から見ると、縁が波打つ。左は同じBumpマテリアルでも、`z`の幅は0のままである。2つのObjectは同じMeshを参照しているので、差はModifierの有無にある。

## Blender画面で観察する

1. `.blend`を開き、2枚の板を真横（テンキーの1か、視点を水平に）から見る。
2. 左の縁は直線である。右の縁は上下している。
3. ビューポートを **Material Preview** にすると、左も面の中に明暗がある。それは法線の傾きで、形は平らなまま。
4. ログの`bump z`が0、`displace z`が0.02より大きいことを照合する。

右のModifierの **Show in Viewport** を切ると、右の縁も直線に戻る。 **Apply** は押さない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
DISPLACE_STRENGTH = 0.3
```

これを`0.5`にして、実行前に予測する。左の`bump z`は0のままか。右の高低は増えるか。

再実行すると、左の頂点は平らなまま、右の`displace z`が大きくなる。確認後は`0.3`へ戻す。

## 完了条件と次へ

Bumpが輪郭を変えず、Displaceが評価後の頂点を動かすことを説明できれば完了。次は [98 BevelとSubdivisionの順番](../98_bevel_subsurf_order/README.md) で、面取りをどの段の前に置くかを見る。
