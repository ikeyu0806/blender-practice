# 88｜Particle Instance：粒の位置に小石を置く

## このレッスンの目標

小石の元Meshは8頂点の立方体1個のまま、床の粒12個の位置に評価後の複製が並び、頂点数が8×12になることを確認する。

前提は [87 Particle System](../87_particle_system/README.md) と [50 Array](../50_array/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Particle Instanceは、別Objectの粒の位置へ、自分のMeshの評価後コピーを置く。
- コピーされるのは評価結果で、小石の元Meshは1個のまま。
- 粒の数を変えると、評価後の頂点数だけが変わる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/88_particle_instance/lesson.py
```

`saved: .../output/88_particle_instance.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/88_particle_instance/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
ParticleInstance Collection
├── Ground.Emitter Object
│   └── Particle System（12粒）
└── Prop.Pebble Object → 8頂点の立方体Mesh
    └── Particle Instance Modifier → Ground.Emitterの粒
        └── 評価後は96頂点
```

## 仕組み

Arrayが等間隔に並べるのに対し、Particle Instanceは粒が飛んだ位置へ並べる。Modifierは小石Object側にあり、`object`が粒を出している床を指す。`particle_system`で、床に複数の粒があるときのどれを使うかを指定する。

元の立方体は8頂点。12粒それぞれに同じ形が評価されるので、評価後は96頂点。小石ObjectはOutlinerに1個のまま。床の粒の設定を変えると、小石の元Meshを編集しなくても並びが変わる。

フレーム5では粒が床から法線方向へ進んでいる。フレーム1に戻すと、小石は放出直後の位置へ集まる。

## Blender画面で観察する

1. `.blend`を開き、散らばった小石を **View → Frame All** で見る。
2. `Prop.Pebble`の **Modifier Properties** で`OnDust`のObjectが`Ground.Emitter`であることを確認する。
3. **Show in Viewport** を切ると、小石1個に戻る。
4. ログの元頂点が8、評価後が96であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると12個分の頂点が1つの元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
PARTICLE_COUNT = 12
```

これを`5`にして、実行前に予測する。小石の元頂点は8のままか。評価後は40頂点になるか。

再実行すると、元の立方体は8頂点のままで、評価後は40頂点になる。確認後は`12`へ戻す。

## 完了条件と次へ

小石Objectが1個、元Meshが8頂点、評価後だけ粒の数倍になっていることを説明できれば完了。次は [89 Explode](../89_explode/README.md) で、同じObjectの面を粒に追従させて割る。
