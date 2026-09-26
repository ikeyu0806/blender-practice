# 02｜Transform と親子：local と world を比べる

## このレッスンの目標

**子の `location` が同じでも、親の位置が違えば画面上の位置が変わる**ことを、Outliner・ビューポート・ログで確かめる。[01 共有 Mesh](../01_shared_mesh/README.md) で Object と Mesh の違いを見た後に取り組む。

完了したら、次を説明できる状態を目指す。

- `Parent.A` と `Parent.B` は形状のない **Empty Object**。子をまとめて動かすための基準点になる。
- `Cube.A` と `Cube.B` の `location` は両方 `(1, 0, 0)` だが、親の位置が違うため **ワールド位置は `(-1, 0, 0)` と `(3, 0, 0)`**。
- Outliner で子が親の下に見えることと、`child.parent` が親を指すことは同じ関係を表す。Collection への所属とは別。

用語に迷ったら [Blender 用語集](../../docs/glossary.md) の Transform、Local、Global / World、Parent / Child を参照する。

## 実行する

プロジェクトのルートから、画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/02_parent_transform/lesson.py
```

ログに `saved:` が出れば `output/02_parent_transform.blend` に保存済みで、ターミナルへ戻る。結果を見るときは Blender アプリの **File → Open...** からこの `.blend` を開く。画面付きで起動して実行する場合はこちら。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/02_parent_transform/lesson.py
```

画面付き起動では、スクリプトが終わっても **Blender を閉じるまでターミナルは待機**する。画面で Location を編集しても `lesson.py` は変わらない。再実行で同じ出力ファイルを作り直すため、画面での変更を残す場合は別名で保存する。詳しくは [スクリプトと画面の関係](../../docs/notes/script-workflow.md) を参照する。

Blender の Text Editor で保存済みの `lesson.py` を開き、**Run Script** してもよい。スクリプトは最初に今の作業を初期化するため、残したい `.blend` は先に保存する。すでに別の Blender ウィンドウを開いている場合は自動で切り替わらない。

## 画面と数値の対応

```text
Scene Collection
├── Parent.A  Empty / world X = -2
│   └── Cube.A  Mesh Object / local X = 1 / world X = -1
└── Parent.B  Empty / world X = 2
    └── Cube.B  Mesh Object / local X = 1 / world X = 3
```

Outliner では `Cube.A` と `Cube.B` が各 `Parent` の下に入る。ビューポートでは、Empty は小さな軸の印、子は立方体として見える。子 Object を選んで Object Properties の **Transform → Location** を見ると、どちらも X が `1`。それでも2つの立方体は離れている。親の位置が加わった最終結果をログの `world=` で確認する。

| 親 | 親のワールド X | 子のローカル X | 子のワールド X |
|---|---:|---:|---:|
| `Parent.A` → `Cube.A` | -2 | 1 | -1 |
| `Parent.B` → `Cube.B` | 2 | 1 | 3 |

この回は回転・拡大を使わず、親子の補正行列も初期値なので、**子のワールド位置 = 親のワールド位置 + 子のローカル位置**と考えられる。一般の親子関係では回転や拡大も影響するため、単純な足し算ではなく行列の合成になる。`child.matrix_world.translation` はその合成後のワールド位置を読む方法。

## スクリプトの流れ

1. 前回と同じく `bmesh` で立方体の Mesh を1つ作る。今回は形を変えず、配置の違いに集中する。
2. `bpy.data.objects.new(..., None)` で形状を持たない Empty Object を2つ作り、X を `-2` と `2` に設定する。
3. 各子 Cube を作って `child.parent = parent` と設定し、**その後**に `child.location = (1, 0, 0)` を入れる。両 Cube は同じ Mesh を使うが、親と Transform は別々。
4. `bpy.context.view_layer.update()` で親子の変更を評価してから、`child.location` と `child.matrix_world.translation` をログに出す。
5. 関係と位置を検査し、`.blend` を保存する。

GUI で `Ctrl+P` を使って親子付けすると、「変形を維持」や Parent Inverse の設定によって、子の Location と見える位置の関係がこの例と異なる場合がある。このレッスンでは **親を先に指定し、補正を入れずにローカル位置を設定**して、基本の関係だけを見る。[Blender Manual: Parenting Objects](https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/parent.html)

## 変更実験

`main()` 内の `make_parent_and_child("B", 2.0, mesh, scene)` の `2.0` を **`4.0`** に変える。実行前に、`Cube.B` の local X と world X、`Cube.A` の world X を予測する。再実行すると、`Cube.B` の local X は `1` のまま、world X は `5` になる。`Cube.A` は `-1` のまま。実験後は `2.0` に戻す。

## よく混同する点

| 疑問 | 答え |
|---|---|
| Empty は「何もない」ので移動できない？ | 形状はないが Object と Transform はある。子の位置を決められる。 |
| 子の `location` が同じなら同じ場所に見える？ | 親が違えばワールド位置は変わる。 |
| Parent の下に見えるのは Collection の階層？ | 違う。親子の階層で、親の Transform が子に伝わる。 |
| Mesh が共有だから子も一緒に動く？ | 違う。位置を決めるのは各 Object とその親。Mesh 共有は形状の共有。 |

次は [ロードマップの03 Collection](../../docs/plan/README.md)。同じ Object の所属 Collection だけを変え、親子の変形とは別の仕組みだと確認する。
