# 82｜Warp：2つのEmptyの差で布を引っ張る

## このレッスンの目標

旗の元Meshは平らなまま、`Warp.From`から`Warp.To`への差が評価後のZ幅になることを確認する。影響はFromを中心とした半径の中。

前提は [72 Hook](../72_hook/README.md)。UVをずらす同名の操作は [46 UV Warp](../46_uv_warp/README.md)。この回は頂点座標を動かす。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Warpは、2つのObjectの位置の差を、半径内の頂点の評価後座標へ加える。
- `falloff_radius`の外では影響が弱まる。
- `strength`は差をどれだけ頂点へ伝えるか。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/82_warp/lesson.py
```

`saved: .../output/82_warp.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/82_warp/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Warp Collection
├── Warp.From Empty
├── Warp.To Empty（Fromより+Yかつ+Z）
└── Banner.Cloth Object → 平らな格子
    └── Warp Modifier（radius=1.5, strength=1）
        └── 評価後のZ幅が正
```

## 仕組み

Hookが選んだ頂点だけを追従させるのに対し、WarpはFromの周囲にある頂点へ、FromからToへの移動をぼかして加える。旗の中央付近が持ち上がり、端は半径の外なので残りやすい。

ToはFromに対してYとZの両方へずれている。平らな格子の評価後にZ幅が出れば、その差が頂点へ伝わっている。`falloff_type`の`SMOOTH`は半径の端で急に切らない。

元MeshのZ幅は0。Emptyを動かすと、旗の元頂点を編集せずに引っ張り位置を変えられる。

## Blender画面で観察する

1. `.blend`を開き、旗と2つのEmptyを **View → Frame All** で見る。
2. **Modifier Properties** の`PullBanner`でFrom、To、Radiusが1.5であることを確認する。
3. **Show in Viewport** を切ると、平らな旗に戻る。
4. ログの`evaluated z span`が正であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると引っ張った頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
WARP_STRENGTH = 1.0
```

これを`0.4`にして、実行前に予測する。元の旗は平らなままか。評価後のZ幅は小さくなるか。

再実行すると、元Meshは平らなままで、Z幅が1.0のときより小さくなる。確認後は`1.0`へ戻す。

## 完了条件と次へ

平らな旗が残り、2つのEmptyの差だけが評価後の高低になることを説明できれば完了。次は [83 Wave](../83_wave/README.md) で、フレームによって波の位置が変わるのを見る。
