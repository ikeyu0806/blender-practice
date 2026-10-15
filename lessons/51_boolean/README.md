# 51｜Boolean：別Objectの形で壁に開口を作る

## このレッスンの目標

部屋の壁の元Meshは6面の立方体のまま、評価後だけ扉カッターとの差分で面が増えることを確認する。カッターは別Objectで、壁のMeshには吸収されない。

前提は [50 Array](../50_array/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Booleanの`DIFFERENCE`は、評価後の形から別Objectの体積を引く。
- 演算の対象はObject参照で、Meshの共有とは別。
- 壁の元Meshは立方体のままなので、カッターを動かすと開口の位置だけを変えられる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/51_boolean/lesson.py
```

`saved: .../output/51_boolean.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/51_boolean/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Boolean Collection
├── Room.DoorCutter Object → 小さな立方体Mesh
└── Room.Wall Object → 一辺2mの立方体Mesh（8頂点・6面）
    └── Boolean Modifier（DIFFERENCE, solver=MANIFOLD）
        └── 評価後の壁だけに開口ができ、面数が増える
```

## 仕組み

Booleanは2つの体積の足し算、引き算、共通部分を評価後のMeshとして作る。`DIFFERENCE`は壁から扉の箱を引く。`UNION`はくっつけ、`INTERSECT`は重なった部分だけを残す。

参照先は`boolean_modifier.object`。これはCollection所属や親子ではなく、「演算に使う形状はどのObjectの評価結果か」という参照。扉ObjectをX方向へ動かすと、壁の元Meshは動かずに開口だけが移動する。

`MANIFOLD`は閉じた体積向けのソルバ。カッターと壁が面でぴったり重なると、開口が作りにくいことがある。この回は扉を手前へずらして、壁の表面を横切らせている。

ビューポートでは扉の箱も見える。壁のModifierを理解したあとは、扉Objectを非表示にすると開口だけを見やすい。非表示にしても参照は残る。

## Blender画面で観察する

1. `.blend`を開き、壁と手前の小さい箱を **View → Frame All** で収める。
2. `Room.Wall`の **Modifier Properties** でOperationがDifference、Objectが`Room.DoorCutter`であることを確認する。
3. 壁の **Show in Viewport** を切ると、開口のない立方体に戻る。
4. Edit Modeでは壁が6面のままであることを確認する。
5. ログの`source faces=6`より`evaluated faces`が大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると開口が壁の元Meshへ焼き込まれ、扉Objectを動かしても開口は追従しない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
OPERATION = "DIFFERENCE"
```

これを`"UNION"`にして、実行前に予測する。壁の元Meshは6面のままか。評価後は開口ではなく、壁と扉がつながった形になるか。

再実行すると、元Meshは立方体のままで、評価後は2つの箱を足した輪郭になる。確認後は`"DIFFERENCE"`へ戻す。

## 完了条件と次へ

壁の元Meshが立方体のまま、評価後の面だけが増え、演算対象が別Objectであることを説明できれば完了。次は [52 Build](../52_build/README.md) で、面がフレームごとに現れる様子を見る。
