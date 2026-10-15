# 46｜UV Warp：2つのEmptyの差でUVをずらす

## このレッスンの目標

布パネルの元UVはすべてのループで`(0.25, 0.25)`のまま、評価後のUVだけが`UV.From`から`UV.To`への移動量だけずれることを確認する。

前提は [45 UV Project](../45_uv_project/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- UV Warpは既存のUVを、2つのObjectの差で評価結果の中だけ変形する。
- 元Meshに保存したUV座標は、Applyするまで変わらない。
- 投影で新しいUVを作るUV Projectとは、すでに入っているUVを動かす点で役割が違う。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/46_uv_warp/lesson.py
```

`saved: .../output/46_uv_warp.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/46_uv_warp/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
UVWarp Collection
├── UV.From Empty（基準位置）
├── UV.To Empty（ずらした位置）
└── Cloth.Panel Object → Cloth.Panel.Mesh
    ├── UVMap（保存値はすべて0.25, 0.25）
    └── UV Warp Modifier → FromとToを参照
        └── 評価後のUVだけが2つの差だけ動く
```

## 仕組み

UV Warpは、`object_from`から`object_to`への移動・回転・拡縮を、指定したUV層の評価結果へ適用する。この回はToをX方向へ1ずらすので、評価後のUが保存値0.25から離れる。

元MeshのUVはループごとに`(0.25, 0.25)`のまま。ログの`stored uv0`と`evaluated uv0`が違う。頂点のXYZは格子のままなので、3Dビューポートの輪郭は変わらず、UV Editor側が変わる。

FromとToを同じ位置に置くと差が無く、評価後のUVは保存値に近づく。骨の名前を指定すれば、ArmatureのBoneの差でUVを動かすこともできる。この回はEmptyだけで観察する。

## Blender画面で観察する

1. `.blend`を開き、布と2つのEmptyを **View → Frame All** で収める。
2. `Cloth.Panel`の **Modifier Properties** で`SlidePattern`のFromとToを確認する。
3. UV Editorで、Modifier表示を切ったときの一点と、有効なときのずれを比べる。
4. ログの保存UVが`(0.25, 0.25)`、評価後のUがそれと違うことを照合する。

Modifierメニューの **Apply** は押さない。**Show in Viewport** を切ると、評価後に見えていたUVのずれが外れる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
TO_LOCATION = (1.0, 0.0, 0.0)
```

これを`(0.0, 1.0, 0.0)`にして、実行前に予測する。ずれるのはUかVか。元MeshのUVは残るか。

再実行すると、保存UVは`(0.25, 0.25)`のままで、評価後はV側が動く。確認後は`(1.0, 0.0, 0.0)`へ戻す。

## 完了条件と次へ

保存されたUVと評価後のUVが違い、その差が2つのEmptyの位置に対応することを説明できれば完了。次は [47 Vertex Weight Edit](../47_vertex_weight_edit/README.md) で、保存済みウェイトを評価後だけ別の値へ変換する。
