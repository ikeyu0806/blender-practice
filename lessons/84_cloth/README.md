# 84｜Cloth：端を固定した布がフレームとともに垂れる

## このレッスンの目標

マントの元Meshは平らなまま、右端のピンは評価後もほぼ動かず、それ以外の頂点はフレーム12で下へ垂れることを確認する。

前提は [83 Wave](../83_wave/README.md)。服の厚みは [61 Solidify](../61_solidify/README.md)。この回はシミュレーションの垂れだけを見る。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Clothは物理演算のModifierで、フレームを進めると頂点の評価後位置が変わる。
- 頂点グループを質量グループに指定すると、ウェイト1の頂点がピンになる。
- 元Meshは平らなままなので、フレームを1へ戻すと垂れる前の状態を比較できる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/84_cloth/lesson.py
```

`saved: .../output/84_cloth.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。保存時のフレームは12。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/84_cloth/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Cloth Collection
└── Clothing.Cape Object → 平らな格子
    ├── Vertex Group Pin（右端が1）
    └── Cloth Modifier（質量グループ=Pin）
        └── フレーム12の評価後は、右以外が下へ垂れる
```

## 仕組み

Waveが数式でZを動かすのに対し、Clothは重力と布のばねでフレームごとに頂点を更新する。`frame_set`で時刻を進めると、その時点までのシミュレーションが評価結果に入る。

`vertex_group_mass`に入れたグループのウェイト1は固定。右端のXが0.8より大きい頂点をピンにし、左側が垂れる。ログの`pin z`はほぼ0、`loose min z`は負。

床が無いので、フレームを伸ばすと布はさらに下へ進む。床で止めるのは次のCollision。

## Blender画面で観察する

1. `.blend`を開く。タイムラインがフレーム12で、布の片側が垂れていることを確認する。
2. **Modifier Properties** の`Drape`で、Pin Groupが`Pin`であることを確認する。
3. フレーム1へ戻すと、垂れる前の平らな評価に近づく。
4. ログのピン側がほぼ0、固定していない側の最小Zが負であることを照合する。

Modifierメニューの **Apply** は押さない。Applyするとそのフレームの垂れた頂点が元Meshになり、再生しても布として計算されない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LAST_FRAME = 12
```

これを`20`にして、実行前に予測する。ピンはほぼ動かないか。垂れた側は12のときより低くなるか。

再実行すると、ピンは残り、固定していない側の最小Zがさらに負になる。確認後は`12`へ戻す。

## 完了条件と次へ

平らな元Meshが残り、ピンした端と垂れた側を評価後で区別できることを説明できれば完了。次は [85 Collision](../85_collision/README.md) で、床が布を受け止めるのを見る。
