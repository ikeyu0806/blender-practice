# 52｜Build：フレームが進むと面が現れる

## このレッスンの目標

木箱の元Meshは6面のまま、フレーム3では評価後の面が少なく、継続時間の終わりでは6面が揃うことを確認する。

前提は [51 Boolean](../51_boolean/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Buildは元Meshの面を消さず、評価結果に含める面をフレームで決める。
- `frame_start`から`frame_duration`の間に、面が順番に現れる。
- タイムラインを動かしても`Object.data`の面数は6のまま。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/52_build/lesson.py
```

`saved: .../output/52_build.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。保存時のフレームは、面が揃った時刻。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/52_build/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Build Collection
└── Prop.Crate Object → Prop.Crate.Mesh（6面）
    └── Build Modifier（frame_start=1, frame_duration=6）
        ├── フレーム3の評価後: 面が少ない
        └── 継続時間終了後の評価後: 6面
```

## 仕組み

Buildは面の出現順を時刻に結びつける。元Meshの面リストはそのままで、Dependency Graphがそのフレームまでに含める面だけを評価結果へ出す。`use_random_order`を切っているので、面インデックスの順に現れる。

フレーム1ではまだ面がほぼ無く、フレーム3では途中、`1 + frame_duration`では6面が揃う。ログはこの2つの評価後面数を出す。保存ファイルを開いたときのカレントフレームは、揃った側。

タイムラインを前後してもEdit Modeの面数は6。変わって見えるのは評価結果だけ。

## Blender画面で観察する

1. `.blend`を開く。下のタイムラインが、面の揃ったフレームにあることを確認する。
2. `Prop.Crate`の **Modifier Properties** で`Appear`のStartとDurationを見る。
3. タイムラインをフレーム1へ戻す。箱が消えるか、面が極端に少ないことを確認する。
4. フレームを終端まで進めて、6面の立方体に戻ることを確認する。
5. ログの途中フレームの面数が、終了フレームより小さいことを照合する。

Modifierメニューの **Apply** は押さない。Applyしたフレームの面だけが元Meshになり、アニメーションは残らない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
FRAME_DURATION = 6.0
```

これを`12.0`にして、実行前に予測する。フレーム3の面は、durationが6のときより少ないか。元Meshは6面のままか。

再実行すると、元Meshは6面のままで、同じフレーム3でも現れている面が少なくなる。確認後は`6.0`へ戻す。

## 完了条件と次へ

元Meshが6面のまま、評価後の面数だけがフレームで変わることを説明できれば完了。次は [53 Decimate](../53_decimate/README.md) で、細かい格子の頂点を評価後だけ減らす。
