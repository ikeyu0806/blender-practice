# 89｜Explode：面を粒に追従させて割る

## このレッスンの目標

壺の元Meshは6面のまま、同じObjectの粒のあとにExplodeを置くと、フレーム8の評価後は面が6より多くなることを確認する。

前提は [87 Particle System](../87_particle_system/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Explodeは、同じObjectのParticle Systemより後に置き、面を粒の動きへ分ける。
- `use_edge_cut`は、分かれるときに辺で頂点を切り離す。
- 元の6面は残り、割れて見えるのは評価後。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/89_explode/lesson.py
```

`saved: .../output/89_explode.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。保存時のフレームは8。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/89_explode/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Explode Collection
└── Prop.Pot Object → 6面の立方体Mesh
    ├── Particle System Modifier（8粒）
    └── Explode Modifier（辺で切断）
        └── フレーム8の評価後は面が6より多い
```

## 仕組み

壺を手で面ごとに分離すると、元の立方体を戻せない。Explodeは粒の位置へ面を評価後だけ移動する。スタックの順が重要で、粒より前にExplodeを置くと、追従する粒がまだ無い。

`render_type`を`NONE`にしているのは、粒の点表示より、割れた面を見るため。`use_edge_cut`が有効だと、隣の面と共有していた頂点が分かれ、面が独立して飛める。ログでは元の6面に対して評価後の面が増えている。

フレーム1では割れが小さく、フレームを進めると粒とともに面が離れる。

## Blender画面で観察する

1. `.blend`を開く。フレーム8で、壺の面が離れていることを確認する。
2. **Modifier Properties** で`Shards`が`BreakApart`より上にあることを確認する。
3. フレーム1へ戻し、まだ立方体に近いことを見る。
4. ログの元の面が6、評価後がそれより多いことを照合する。

Modifierメニューの **Apply** は押さない。Applyするとそのフレームの破片が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
OBSERVE_FRAME = 8
```

これを`15`にして、実行前に予測する。元の6面は変わるか。破片は8のときより広がるか。

再実行すると、元Meshは6面のままで、評価後の広がりが進む。確認後は`8`へ戻す。

## 完了条件と次へ

粒のModifierのあとにExplodeがあり、元の6面が残ったまま評価後の面が増えることを説明できれば完了。次は [90 Soft Body](../90_soft_body/README.md) で、柔らかい塊が自重でつぶれるのを見る。
