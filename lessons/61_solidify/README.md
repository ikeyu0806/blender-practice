# 61｜Solidify：布の面に評価後だけ厚みを付ける

## このレッスンの目標

マントの元Meshは厚み0の格子のまま、Solidifyの評価後は頂点が2倍になり、Z方向の幅が`CLOTH_THICKNESS`になることを確認する。

前提は [60 Skin](../60_skin/README.md)。服を体と別Meshにする使い方は [26 衣装と部品分割](../26_clothing_parts/README.md)。この回は厚みのパラメータだけを見る。他のレッスンの出力ファイルは必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Solidifyは開いた面、または薄い面に、評価後だけ厚みの表面を足す。
- `thickness`は厚みの長さ、`offset`は元の面を厚みのどこに置くか。
- 元Meshの頂点は片面のままなので、シルエット用の面と布の厚みを別々に調整できる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/61_solidify/lesson.py
```

`saved: .../output/61_solidify.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/61_solidify/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Solidify Collection
└── Clothing.Cape Object → 厚みのない格子Mesh
    └── Solidify Modifier（thickness=0.08, offset=1）
        └── 評価後は頂点2倍、Zの幅が厚みと一致
```

## 仕組み

布を最初から閉じた箱として作ると、柄の面と厚みの側面が同じMeshに混ざる。Solidifyは元の面を表面の片方として残し、評価のときに反対側と側面を足す。

`offset`が1のとき、元の面は厚みの端に残り、法線方向へ`thickness`だけ増える。0なら元の面が厚みの中央、 -1なら逆側へ増える。格子はXY平面なので、増えた厚みはログのZ幅として読める。

頂点が2倍になるのは、反対側の表面用に頂点がコピーされるため。Edit Modeの格子は片面のまま。

## Blender画面で観察する

1. `.blend`を開き、マントを真横から見る。薄い板になっていることを確認する。
2. **Modifier Properties** の`FabricThickness`でThicknessが0.08、Offsetが1であることを確認する。
3. **Show in Viewport** を切ると、厚みのない格子に戻る。
4. ログの評価後頂点が元の2倍、`z span`が0.08付近であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると表裏が元Meshへ入り、片面の格子には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
CLOTH_THICKNESS = 0.08
```

これを`0.2`にして、実行前に予測する。頂点は2倍のままか。Zの幅は0.2に近づくか。

再実行すると、頂点数の倍率は同じで、ログの`z span`が0.2付近になる。確認後は`0.08`へ戻す。

## 完了条件と次へ

片面の元Meshが残り、評価後だけ厚みの分だけ頂点とZ幅が増えることを説明できれば完了。次は [62 Subdivision Surface](../62_subdivision/README.md) で、同じ立方体を滑らかな段へ分割する。
