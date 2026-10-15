# 86｜Ocean：小さな面から海面の格子を生成する

## このレッスンの目標

海の入力Meshは4頂点の1面のまま、Oceanの`GENERATE`が評価後に多数の頂点と波の高低を作ることを確認する。

前提は [83 Wave](../83_wave/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Oceanの`GENERATE`は、入力の面を置き換えて海面の格子を評価後に作る。
- `resolution`は格子の細かさ。ビューポート用とレンダー用を別にできる。
- `DISPLACE`に切り替えると、既存の頂点を波で動かすモードになる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/86_ocean/lesson.py
```

`saved: .../output/86_ocean.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/86_ocean/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Ocean Collection
└── Sea.Input Object → 4頂点・1面
    └── Ocean Modifier（GENERATE, resolution=4）
        └── 評価後は細かい海面とZの高低
```

## 仕組み

Waveが既存の格子を揺するのに対し、Oceanは海面用の頂点を評価のときに作る。入力の4頂点は、Modifierを付けるObjectの受け皿。`geometry_mode`が`GENERATE`のとき、評価後の頂点数は入力と一致しない。

`resolution`の4は、観察用に粗い海。値を上げると頂点が急に増えるので、最初は小さくする。`viewport_resolution`をレンダーより低くすると、画面では軽く、最終画像では細かくできる。この回は両方4。

`wave_scale`は波の大きさ。`spatial_size`は海面が覆う範囲で、Blender 5.2ではメートルの整数である。時間を進めると波の位相が変わる。この回は時刻の既定値で、高低の幅が出ることだけを見る。

## Blender画面で観察する

1. `.blend`を開き、海面を斜めから **View → Frame All** で見る。
2. **Modifier Properties** の`Waves`でGeometryがGenerate、Resolutionが4であることを確認する。
3. **Show in Viewport** を切ると、4頂点の面に戻る。
4. ログの`source=4`、`evaluated`が50以上、`z span`が0.2以上であることを照合する。

Modifierメニューの **Apply** は押さない。Applyするとその瞬間の海面が元Meshになり、解像度を後から変えられない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
OCEAN_RESOLUTION = 4
```

これを`5`にして、実行前に予測する。入力の4頂点は変わるか。評価後の頂点は増えるか。

再実行すると、入力は4頂点のままで、評価後の頂点が増える。確認後は`4`へ戻す。

## 完了条件と次へ

入力が4頂点のまま、評価後だけ海面の格子と高低があることを説明できれば完了。次は [87 Particle System](../87_particle_system/README.md) で、面から粒を出す。
