# 63｜Triangulate：四角面を評価後だけ三角形にする

## このレッスンの目標

木箱の元Meshは四角6面・8頂点のまま、評価後は同じ8頂点で三角形12面になることを確認する。

前提は [62 Subdivision Surface](../62_subdivision/README.md)。書き出し時の三角形化は [38 書き出しと再取り込み](../38_export_roundtrip/README.md) でも触れる。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Triangulateは頂点を増やさず、四角以上の面を評価後だけ三角形に分ける。
- 四角1枚は三角形2枚になるので、立方体の6面は12面になる。
- `quad_method`は、四角のどちらに対角線を引くかを決める。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/63_triangulate/lesson.py
```

`saved: .../output/63_triangulate.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/63_triangulate/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Triangulate Collection
└── Crate.Quads Object → 8頂点・四角6面のMesh
    └── Triangulate Modifier（quad_method=BEAUTY）
        └── 評価後は8頂点・三角形12面
```

## 仕組み

ゲームや一部の書き出し先は、面を三角形として受け取る。編集中は四角のままループを追い、評価や書き出しの直前で三角形にすると、辺の流れを崩さずに渡せる。

Triangulateは各四角に対角線を1本足す。頂点は増えない。`BEAUTY`は隣の面とのつながりがきれいに見える対角線、`FIXED`は頂点番号で決まる対角線、`FIXED_ALTERNATE`は隣同士で向きを交互にする。この回の立方体はどの方法でも12面になる。違いは対角線の方向。

五角以上は`ngon_method`で割る。この回の入力は四角だけなので、結果の面数は`quad_method`を変えても12のまま。

## Blender画面で観察する

1. `.blend`を開き、木箱のワイヤーを表示する。各面に対角線があることを確認する。
2. **Modifier Properties** の`ToTriangles`でQuad Methodを確認する。
3. **Show in Viewport** を切ると、対角線のない四角6面に戻る。
4. ログの頂点が8のまま、面が6から12になることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると三角形が元Meshになり、四角のループ編集には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
QUAD_METHOD = "BEAUTY"
```

これを`"FIXED"`にして、実行前に予測する。頂点数と面数は8と12のままか。対角線の向きは変わるか。

再実行すると、ログの頂点8・面12は同じで、ワイヤー上の対角線の入り方が変わる。確認後は`"BEAUTY"`へ戻す。

## 完了条件と次へ

頂点は8のまま、評価後の面だけが12になることを説明できれば完了。次は [64 Weld](../64_weld/README.md) で、重なった頂点を評価後だけ1つにまとめる。
