# 83｜Wave：フレームで水面の波を動かす

## このレッスンの目標

池の元Meshは平らなまま、フレーム1とフレーム20で評価後の頂点位置がずれることを確認する。波の高さはModifierの値で、時刻で進む。

前提は [52 Build](../52_build/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Waveは円形の波を評価後の頂点Zへ足し、`speed`でフレームとともに移動する。
- `height`は波の振幅、`width`は波の間隔。
- 元の格子は平らなので、タイムラインを戻すと評価後の波も戻る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/83_wave/lesson.py
```

`saved: .../output/83_wave.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。保存時のフレームは20。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/83_wave/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Wave Collection
└── Pond.Surface Object → 平らな細かい格子
    └── Wave Modifier（height=0.3, speed=0.25）
        ├── フレーム1の評価後
        └── フレーム20の評価後（頂点位置がずれている）
```

## 仕組み

水面を1枚の形として保存すると、波の位置を変えるたびに頂点を打ち直す。Waveは時刻から波の位相を計算し、評価後のZだけを動かす。`speed`が0.25なので、フレーム1と20では山の位置がずれる。ログの`frame delta`はその最大距離。

`height`を0にすると、フレームを進めてもZは動かない。`width`を大きくすると山と山の間隔が広がる。格子が粗いと、波の曲線が角ばる。この回は12分割で、差が出ることだけを見る。

Edit Modeの格子はどのフレームでも平ら。動いて見えるのは評価結果。

## Blender画面で観察する

1. `.blend`を開く。タイムラインがフレーム20にあることを確認する。
2. **Modifier Properties** の`Ripple`でHeightが0.3、Speedが0.25であることを確認する。
3. タイムラインをフレーム1へ戻し、波の位置が変わることを見る。
4. ログの`frame delta`が0.02より大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyするとそのフレームの波が元Meshになり、再生しても進まない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
WAVE_HEIGHT = 0.3
```

これを`0.6`にして、実行前に予測する。元の格子は平らなままか。フレーム間のずれは大きくなるか。

再実行すると、元Meshは平らなままで、`frame delta`が0.3のときより大きくなる。確認後は`0.3`へ戻す。

## 完了条件と次へ

平らな池が残り、フレームを変えると評価後の波の位置が変わることを説明できれば完了。次は [84 Cloth](../84_cloth/README.md) で、端を固定した布がフレームとともに垂れるのを見る。
