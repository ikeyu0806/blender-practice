# 45｜UV Project：Cameraの向きからUVを投影する

## このレッスンの目標

布の旗に見立てた平面の元UVはすべて`(0, 0)`のまま、評価後の`UVMap`だけが上にあるCameraからの投影になることを確認する。

前提は [44 Weighted Normal](../44_weighted_normal/README.md)。UVの考え方は [13 UV展開](../13_uv_unwrap/README.md) も参照できる。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- UV Projectは頂点を動かさず、指定したUV層の評価結果だけを投影で置き換える。
- 投影元はCameraやEmptyなど、別Objectの-Z方向。
- 元Meshに保存されたUVと、評価後のUVは別々に読める。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/45_uv_project/lesson.py
```

`saved: .../output/45_uv_project.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/45_uv_project/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
UVProject Collection
├── Banner.Projector Object → Cameraデータ（Z=3、回転0で真下を見る）
└── Banner.Cloth Object → Banner.Cloth.Mesh
    ├── UVMap（保存値はすべて0, 0）
    └── UV Project Modifier → Projectorを1台参照
        └── 評価後のUVMapだけが投影座標になる
```

## 仕組み

UVは、面の各ループが画像のどこに対応するかを持つ2次元座標。UV Projectは、Projectorに指定したObjectのローカル-Zを投影方向にして、その座標を評価後のUVへ書き込む。Cameraを回転0でZ=3に置くと、旗の真上から見下ろす投影になる。

スクリプトは作った直後の`UVMap`をすべてのループで`(0, 0)`に揃える。これが`Object.data`に保存される値。Modifierを計算したあとのUVは`evaluated_snapshot().uvs`にあり、ログでは`evaluated uv0`が0ではない。頂点数は格子のまま。

`projector_count`を増やすと、複数の方向からの投影を1つのUV層へ重ねられる。この回は旗の真上からの1台だけにする。`scale_x`と`scale_y`は投影結果のUVをどれだけ広げるか。

## Blender画面で観察する

1. `.blend`を開き、旗と上のCameraを **View → Frame All** で収める。
2. `Banner.Cloth`の **Modifier Properties** で`ProjectFromCamera`のUV Mapが`UVMap`、Projectorsが`Banner.Projector`であることを確認する。
3. UV Editorで`UVMap`を開く。Modifierの表示が有効なときの広がりと、無効にしたときの点の集まりを比べる。
4. ログの`stored uv0`が`(0, 0)`、`evaluated uv0`が別の値であることを照合する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、評価で見えていた投影UVが外れる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
PROJECT_SCALE = 1.0
```

これを`2.0`にして、実行前に予測する。元MeshのUVは0のままか。評価後のUVは原点からより離れるか。

再実行すると、保存されたUVは0のままで、評価後の座標の絶対値が大きくなる。確認後は`1.0`へ戻す。

## 完了条件と次へ

元UVが0のまま、評価後のUVだけがCameraからの投影になっていることを説明できれば完了。次は [46 UV Warp](../46_uv_warp/README.md) で、2つのEmptyの差で既存のUVをずらす。
