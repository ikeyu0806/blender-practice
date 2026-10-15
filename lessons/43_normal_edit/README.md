# 43｜Normal Edit：頂点を動かさず法線の向きだけ変える

## このレッスンの目標

看板に見立てた立方体の頂点座標はそのままに、評価後のループ法線だけをEmptyの方向へ向ける。面の法線と、シェーディングに使うカスタム法線が別であることを確認する。

前提は [07 Modifierの評価](../07_modifier_evaluation/README.md) と [42 Data Transfer](../42_data_transfer/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Normal Editは頂点を動かさず、評価後の法線だけを書き換える。
- `DIRECTIONAL`は、targetに置いたObjectの方向へ法線を向ける。
- 面法線と、各ループのカスタム法線は別の値として読める。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/43_normal_edit/lesson.py
```

`saved: .../output/43_normal_edit.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/43_normal_edit/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
NormalEdit Collection
├── Sign.Aim Empty（Meshなし。法線が向く位置）
└── Sign.Board Object → Sign.Board.Mesh（8頂点のまま）
    └── Normal Edit Modifier → Sign.Aimを参照
        └── 評価後のコーナー法線だけがAim方向へ寄る
```

## 仕組み

法線は面や頂点がどちらの表を向くかを表す方向で、座標そのものではない。Normal Editの`DIRECTIONAL`は、targetのObjectがある方向へ、評価後の法線をコピーする。この回のtargetは座標`(0, -2, 2)`のEmptyなので、法線は-Yかつ+Zの成分を持つ。

`Object.data.polygons[].normal`は面の幾何学的な法線で、立方体では軸に沿ったまま。シェーディングが参照するコーナー法線は評価後Meshの`corner_normals`にあり、こちらがEmptyの方を向く。頂点数は8のまま。ログの2つの法線を見比べる。

`RADIAL`は1点から放射する向き、`mix_factor`は元の法線と新しい法線の混ぜ具合。この回は`COPY`と`1.0`で、評価後をtarget方向へ置き換える。

## Blender画面で観察する

1. `.blend`を開き、`Sign.Board`と矢印の`Sign.Aim`が見える位置へ **View → Frame All** する。
2. `Sign.Board`の **Modifier Properties** で`AimNormals`のModeがDirectional、Targetが`Sign.Aim`であることを確認する。
3. ビューポートオーバーレイの **Normals** を有効にし、面法線と頂点法線の向きの差を見る。
4. ログの`face normal`が軸に沿い、`corner normal`がYとZの両方を持つことを照合する。
5. Edit Modeへ入ると元の立方体の頂点位置のままであることを確認する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、カスタム法線の向きが元の面の向きへ戻る。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
AIM = (0.0, -2.0, 2.0)
```

これを`(0.0, 2.0, 0.5)`にして、実行前に予測する。頂点数は変わるか。コーナー法線のY成分の符号はどう変わるか。

再実行すると、頂点は8つのままで、コーナー法線のY成分が正の側へ寄る。確認後は`(0.0, -2.0, 2.0)`へ戻す。

## 完了条件と次へ

頂点座標が元Meshと同じで、コーナー法線だけがEmptyの方向を向いていることを説明できれば完了。次は [44 Weighted Normal](../44_weighted_normal/README.md) で、面の面積を使って法線の混ざり方を変える。
