# 100｜画素数を落とすと板目が塊になる

## このレッスンの目標

頂点とUVの置き方が同じ2つの木箱で、貼る画像の一辺だけが8と64で違うことを確認する。少ない画素の板目は階段状に見える。

前提は [99 未適用のScale](../99_unapplied_scale/README.md)。画像をマテリアルへつなぐ手順は [14 テクスチャとマテリアル](../14_image_material/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- UVは、面のどの位置が画像のどこを読むかという座標である。画素数ではない。
- 同じUVでも、画像が8×8だと4本の板目が数画素の塊になる。
- 64×64は同じ4本でも境界が細かく、近くで見ても段が目立ちにくい。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/100_texture_resolution/lesson.py
```

`saved: .../output/100_texture_resolution.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/100_texture_resolution/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
TextureResolution Collection
├── Crate.Coarse Object → 8頂点、UVMap
│   └── Material.Coarse → Texture.Coarse（LOW_SIZE × LOW_SIZE）
└── Crate.Fine Object → 8頂点、同じ置き方のUVMap
    └── Material.Fine → Texture.Fine（64 × 64）
```

## 仕組み

画像はUVの0から1を、持っている画素数で分ける。4本の板目を8画素で塗ると、1本が約2画素になり、境界は斜めでも階段になる。64画素なら1本が約16画素あり、同じUVを読んでも境界が細い。レトロな見た目は、この画素数の少なさで作れる。形の角張りの方は [95 ポリゴン予算](../95_polygon_budget/README.md) と [11 法線と面の向き](../11_normals_shading/README.md) のフラットシェーディングである。

初期の家庭用ゲーム機には、テクスチャが画面上で歪む座標の精度もある。それはその機の描画の性質で、Blenderの画素数を下げただけでは再現されない。この回で見るのは、画像が粗いことによる塊である。

画像は`.blend`へPackしてある。外部ファイルは要らない。

## Blender画面で観察する

1. `.blend`を開き、ビューポートを **Material Preview** にする。
2. 左の板目は大きな色の塊、右は細い縞に見える。木箱の頂点の角張りは両方同じである。
3. Image Editorで`Texture.Coarse`と`Texture.Fine`を切り替え、画素の大きさを見る。
4. ログの`coarse image`が`LOW_SIZE`、`fine image=64`、頂点数が同じであることを照合する。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LOW_SIZE = 8
```

これを`16`にして、実行前に予測する。左の頂点数は変わるか。板目の塊は8のときより細かくなるか。

再実行すると、頂点は8のまま、左の画像だけ16×16になる。右の64よりは粗い。確認後は`8`へ戻す。

## 完了条件と次へ

同じUVでも画素数で板目の粗さが変わることを説明できれば完了。次は [101 ライトの大きさ](../101_light_size/README.md) で、影の境界の鋭さを光源の面積で変える。
