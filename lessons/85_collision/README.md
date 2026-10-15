# 85｜Collision：床が布を突き抜けさせない

## このレッスンの目標

床のCollisionは床の頂点数を変えず、上から落ちる布のワールドZがフレーム12で床付近に揃うことを確認する。布側のClothは、衝突を見せる相手として使う。

前提は [84 Cloth](../84_cloth/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Collisionは、付けたObjectを布や剛体の衝突面にする。形そのものは変形しない。
- `thickness_outer`は表面の外側に足す当たりの厚さ。
- 布が止まるのはCloth側の評価結果で、床の元Meshは平らなまま。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/85_collision/lesson.py
```

`saved: .../output/85_collision.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/85_collision/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Collision Collection
├── Room.Floor Object → 平らな床Mesh
│   └── Collision Modifier（外側の厚さ）
└── Clothing.Cape Object（最初はZ=0.4）
    └── Cloth Modifier
        └── フレーム12の評価後は床のすぐ上
```

## 仕組み

Clothだけでは布は重力で落ち続ける。床ObjectにCollisionを付けると、その表面が布の計算で「ここより下へは進まない」面になる。床の頂点は動かない。ログでは床の評価後頂点数と元の頂点数を比べる。

布はZ=0.4から落ち、12フレーム後のワールドZは0付近に揃う。`thickness_outer`が0.02なので、布は床の数学的な平面より少し上で止まる。厚さを増やすと、空中の高い位置で止まる。

Collisionを床から外すと、同じClothでも床の下へ抜ける。止める役割は布のModifierではなく床側にある。

## Blender画面で観察する

1. `.blend`を開き、床と布を真横から見る。布が床の上にあることを確認する。
2. `Room.Floor`の **Modifier Properties** で`BlockCloth`のOuterが0.02であることを確認する。
3. 床のCollisionの表示を切ってフレームを1から再生すると、布が床を抜ける比較ができる。再生結果はファイルへ自動保存されない。
4. ログの布のワールドZが床付近で、床の頂点数が変わっていないことを照合する。

Modifierメニューの **Apply** は、Collisionには形を焼き込む意味が薄い。床の頂点は元のまま使う。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
THICKNESS_OUTER = 0.02
```

これを`0.2`にして、実行前に予測する。床の頂点数は変わるか。布が止まる高さは上がるか。

再実行すると、床の頂点は同じで、布のワールドZが0.02のときより高くなる。確認後は`0.02`へ戻す。

## 完了条件と次へ

床の形は変わらず、布の評価後が床の上で止まっていることを説明できれば完了。次は [86 Ocean](../86_ocean/README.md) で、小さな面から海面の格子を生成する。
