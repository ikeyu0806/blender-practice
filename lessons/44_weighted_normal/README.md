# 44｜Weighted Normal：大きい面の向きを共有頂点へ残す

## このレッスンの目標

細長い木箱の頂点を動かさず、評価後のコーナー法線が隣り合う面の面積で混ざることを確認する。広い面の向きが、角のシェーディングに残りやすくなる。

前提は [43 Normal Edit](../43_normal_edit/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Weighted Normalは頂点座標を変えず、カスタム法線の混ぜ方だけを変える。
- `FACE_AREA`は、面積の大きい面の法線を共有頂点で強く残す。
- `weight`を上げるほど、その偏りが強くなる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/44_weighted_normal/lesson.py
```

`saved: .../output/44_weighted_normal.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/44_weighted_normal/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
WeightedNormal Collection
└── Crate.Side Object → Crate.Side.Mesh（8頂点の細長い箱）
    └── Weighted Normal Modifier（mode=FACE_AREA, weight=50）
        └── 評価後のコーナー法線が、広い面と狭い面の間で混ざる
```

## 仕組み

1つの頂点は複数の面に共有される。スムーズに見せるとき、その頂点の法線は隣り合う面の法線を混ぜた方向になる。均等に混ぜると、広い面と狭い面が同じ強さで角の陰影に出る。

Weighted Normalの`FACE_AREA`は、面積が大きい面の法線をより強く残す。木箱の広い側面と、細い端面では面積が違うので、角のカスタム法線は軸の1方向だけには揃わない。ログの`mixed corners`は、2つ以上の成分が0.2より大きい法線の数。

`keep_sharp`を有効にすると、鋭い辺として印が付いた箇所は混ぜない。この回はオフにして、箱の角全体の混ざりを見る。頂点数は8のまま。

## Blender画面で観察する

1. `.blend`を開き、`Crate.Side`を **View → Frame All** で収める。
2. **Modifier Properties** で`WideFace`のModeがFace Area、Weightが50であることを確認する。
3. ビューポートをスムーズ表示にし、広い面と端面の境でハイライトがどちらへ傾くかを見る。
4. オーバーレイの法線表示で、角の法線が面の真ん中の法線と違うことを確認する。
5. ログの頂点数が8のまま、`mixed corners`が1以上であることを照合する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、カスタム法線の偏りが外れる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
FACE_WEIGHT = 50
```

これを`10`にして、実行前に予測する。頂点数は変わるか。混ざったコーナー法線は残るか。

再実行すると、頂点は8つのままで、Weightが小さい分だけ広い面への偏りが弱くなる。ログの例の成分を、50のときと比べる。確認後は`50`へ戻す。

## 完了条件と次へ

頂点数が元Meshと同じで、コーナー法線が複数の軸成分を持つことを説明できれば完了。次は [45 UV Project](../45_uv_project/README.md) で、別Objectの向きからUVを投影する。
