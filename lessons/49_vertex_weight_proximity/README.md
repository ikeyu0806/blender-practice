# 49｜Vertex Weight Proximity：距離から評価後のウェイトを作る

## このレッスンの目標

胸に見立てた立方体の`NearHorn`は保存値0のまま、頭上の小さな角に近い上側の頂点だけ、評価後のウェイトが高くなることを確認する。

前提は [48 Vertex Weight Mix](../48_vertex_weight_mix/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Vertex Weight Proximityは、targetとの距離を評価後の頂点グループへ書く。
- `GEOMETRY`は頂点ごとに表面までの距離を使う。`OBJECT`はObject原点までの距離を全頂点で共有する。
- 既定のフォールオフは遠い頂点ほどウェイト1に近づく。近くを重くするには Invert Falloff をオンにする。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/49_vertex_weight_proximity/lesson.py
```

`saved: .../output/49_vertex_weight_proximity.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/49_vertex_weight_proximity/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
VertexWeightProximity Collection
├── Prop.Horn Object（胸の上にある小さな立方体）
└── Body.Chest Object → Body.Chest.Mesh
    ├── Vertex Group NearHorn（保存値はすべて0）
    └── Vertex Weight Proximity Modifier → Prop.Hornを参照
        └── 評価後は上の頂点ほどウェイトが大きい
```

## 仕組み

距離で影響範囲を作りたいとき、手でウェイトを塗る代わりにtargetの位置から計算できる。Blender 5.2の既定では、`min_dist`でウェイト0、`max_dist`でウェイト1になり、それより遠い頂点は1に張り付く。この回は Invert Falloff をオンにし、角に近い側が重くなる向きへ反転する。反転後は`min_dist`が1、`max_dist`が0になる。

`GEOMETRY`は角の表面までの距離を頂点ごとに測る。胸の上側は角に近く、下側は`max_dist`の1.5mに近くなるので、ログの`top`が`bottom`より大きい。`OBJECT`にすると、胸Objectから角Objectの原点までの距離が1つだけ計算され、全頂点が同じウェイトになる。

頂点グループに頂点を先に入れておかないと、評価後のウェイトを頂点番号へ対応づけられない。保存値は0のまま。

## Blender画面で観察する

1. `.blend`を開き、胸と上の小さな角を **View → Frame All** で収める。
2. `Body.Chest`の **Modifier Properties** で`NearHorn`のTargetが`Prop.Horn`、Proximity ModeがGeometry、Invert Falloffがオンであることを確認する。
3. Weight Paintで、上側が下側より濃いことを見る。
4. ログの`stored=0.000`と、`top`が`bottom`より大きいことを照合する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、距離で付いた色が外れ、保存値0に戻る。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
MAX_DISTANCE = 1.5
```

これを`3.0`にして、実行前に予測する。下側のウェイトは0のままか、それとも値を持つか。保存値は0のままか。

再実行すると、保存値は0のままで、下側の評価後ウェイトも0より大きくなる。角から下までの距離が3m以内に入るため。確認後は`1.5`へ戻す。

## 完了条件と次へ

保存ウェイトが0のまま、評価後は角に近い頂点ほど重いことを説明できれば完了。次は [50 Array](../50_array/README.md) で、同じ柱を評価結果の中で繰り返す。
