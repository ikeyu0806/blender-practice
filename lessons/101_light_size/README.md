# 101｜ライトの面積で影の境界が変わる

## このレッスンの目標

Energyが同じ2つのAreaライトで、一辺が0.15の側は影の境界が鋭く、一辺が4の側は境界が広い帯になることを確認する。

前提は [100 テクスチャの画素数](../100_texture_resolution/README.md)。ライトの役割（Key、Fill、Rim）は [19 照明と色](../19_lighting/README.md)。この回は光源の大きさだけを見る。他のレッスンの出力ファイルは必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- 小さい光源は、物の縁の向こうが急に暗くなる。
- 大きい光源は、明るい側と影の間に勾配の帯ができる。
- Energyを揃えれば、比べているのは明るさの総量ではなく、光源の面積である。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/101_light_size/lesson.py
```

`saved: .../output/101_light_size.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/101_light_size/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
LightSize Collection
├── Ground.Shadow Object（影を受ける板）
├── Crate.Hard Object ← Light.Hard（size=0.15、Energyは右と同じ）
└── Crate.Soft Object ← Light.Soft（size=SOFT_SIZE）
```

Worldの背景は弱くしてある。影の差を、環境光ではなく2つのAreaライトで読む。

## 仕組み

Areaライトは面なので、地面から見ると幅のある光源になる。面が小さいと、木箱の縁を境に光が届くか届かないかが急に分かれる。面が大きいと、縁の近くでは光源の一部だけが木箱に隠れるので、影の境界が帯になる。

Material Previewは、シーンのライトではなくプレビュー用の環境画像で材質を見せることがある。この回の影は、ビューポートを **Rendered** にして見る。Solidのままでは境界の幅は分からない。

初期のゲームに多い鋭い影は、小さい光源や、影をぼかさない描画に近い。大きい光源の柔らかい影は、それだけで形が実在するように見えるが、光源の役割そのものはレッスン19で分ける。

## Blender画面で観察する

1. `.blend`を開き、地面と2つの木箱を **View → Frame All** で収める。
2. ビューポートシェーディングを **Rendered** にする。
3. 左の木箱の影は境界が狭い。右は地面に広い勾配がある。
4. Light Propertiesで両方のEnergyが400、Sizeだけが違うことを確認する。ログの`hard size`と`soft size`と照合する。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SOFT_SIZE = 4.0
```

これを`6.0`にして、実行前に予測する。右のEnergyは変わるか。影の帯は広くなるか。

再実行してRenderedで見ると、Energyは400のまま、右の影の境界がさらに広い。同じEnergyを広い面に配ると右は暗く見えやすい。比べるのは全体の明るさではなく、影の境界の幅である。確認後は`4.0`へ戻す。

## 完了条件と次へ

光源の面積が影の境界の幅を決めることを説明できれば完了。形、質感、光をどの回で見たかは [モデルの質](../../docs/notes/model-quality.md) にまとめてある。
