# 03｜Collection：所属を移しても親子と位置は変わらない

## このレッスンの目標

[01 共有 Mesh](../01_shared_mesh/README.md)では Object と形状、[02 Transform と親子](../02_parent_transform/README.md)では親から受ける位置の影響を見た。今回は **Collection は Object を整理する入れ物**だと確かめる。背景の小作品では「木箱」「岩」「照明」などを Collection ごとにまとめ、種類ごとの表示や選択を管理できる。

実行前に予測する: `Cube.B` を `Props.Right` から `Props.Left` へ移したら、`Cube.B` の親 `Parent.B` とワールド X=3 はどうなるだろう？

完了時には次を説明できるようにする。

- `Collection.objects.link(obj)` は Object の所属先を**追加**する。元の所属を外すには `Collection.objects.unlink(obj)` も必要。
- Collection の変更では `obj.parent`、`obj.location`、`obj.matrix_world.translation` は変わらない。
- 1つの Object が複数の Collection に所属しても、Object と Mesh が複製されたわけではない。

用語は [Blender 用語集](../../docs/glossary.md) の Collection、Parent / Child、Link を参照する。

## 実行する

プロジェクトのルートで、まず画面なしで生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/03_collection/lesson.py
```

`saved: .../output/03_collection.blend` と `Blender quit` が出たら完了。Blender アプリの **File → Open...** から `output/03_collection.blend` を開いて観察する。すでに開いている別の Blender ウィンドウは自動では切り替わらない。

画面付きでスクリプトを実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/03_collection/lesson.py
```

画面付き起動では、スクリプトが保存を終えても、ターミナルは Blender アプリの終了を待つ。この教材は実行冒頭で現在のシーンを初期化する。Blender の Text Editor から **Run Script** する場合、残したい作業は先に別名の `.blend` として保存する。GUI での変更は `lesson.py` へ同期しない。再実行で `output/03_collection.blend` を作り直すので、手作業の結果を残すなら **File → Save As...** で別名にする。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 何が作られるか

```text
Scene
├── Props.Left  ← 最終的に Cube.A と Cube.B が所属
├── Props.Right ← 最終的には空
├── Parent.A    ← Cube.A の親。ワールド X = -2
└── Parent.B    ← Cube.B の親。ワールド X =  2
```

親 Empty 2つと子 Cube 2つの **合計4 Object**。Cube は1つの `SharedCube` Mesh を共有する。`Cube.A` のワールド X は `-1`、`Cube.B` は `3`。Collection を移した後もこの数と位置はそのまま。

Outliner の **View Layer** 表示では、親子が折り畳み表示されるため、Collection の見た目の階層だけで所属を判断しにくい場合がある。まずログの `collections=` を確認する。Blender 画面では `Cube.B` を選択し、**Object Properties → Collections** に表示される所属先も確認する。ビューポートでは2つの立方体が移動していないことを確かめる。

## スクリプトとログを対応させる

| 処理・ログ | 意味 | 観察する結果 |
|---|---|---|
| `bpy.data.collections.new("Props.Left")` | Collection というデータブロックを作る | この時点ではまだ Scene の下にない。 |
| `scene.collection.children.link(left)` | 作った Collection を Scene 内につなぐ | Outliner の Scene Collection の下に現れる。 |
| `collection.objects.link(child)` | 子 Object の所属先を設定する | `users_collection` から直接の所属先を読める。 |
| `child.parent = parent` | Object 間に変形を伝える親子関係を作る | `child.parent` と `matrix_world` に反映される。Collection の所属とは別。 |
| `left.objects.link(cube_b)` → `right.objects.unlink(cube_b)` | 左に追加してから右から外し、「移動」にする | 最終的に `Cube.B` は `Props.Left` にだけ所属。 |

実行ログでは `before: Cube.B collections=('Props.Right',) parent=Parent.B local=(1.0, 0.0, 0.0) world=(3.0, 0.0, 0.0)` が、移動後には `after : Cube.B collections=('Props.Left',) parent=Parent.B local=(1.0, 0.0, 0.0) world=(3.0, 0.0, 0.0)` になる。**変わった欄は `collections` だけ**。親子は「位置への影響」、Collection は「整理・表示の単位」という違いがここに現れる。[Blender公式の Outliner 操作説明](https://docs.blender.org/manual/en/5.2/editors/outliner/usage.html)でも、Collection への Move / Link と Object への Parenting は別の操作として説明されている。

## 変更実験

1. `lesson.py` の `MOVE_INSTEAD_OF_LINK = True` を `False` に変える。実行前に、`Cube.B` の所属先、親、ワールド X、Object 数を予測する。
2. 再実行し、ログの `after` を見る。`Cube.B` の所属は `('Props.Left', 'Props.Right')` の **2つ**になる。親 `Parent.B`、ワールド X=3、Object 数4は変わらない。`link` だけでは「移動」ではなく「追加」だと分かる。
3. `True` に戻して再実行する。最終結果が `Props.Left` だけに戻ることを確かめる。

## よく混同する点

| 疑問 | 答え |
|---|---|
| 同じ Object が2つの Collection にあれば2個に増えた？ | 増えていない。1つの Object に所属先が2つある。ログでは Object 数4のまま。 |
| Collection を変えると親も変わる？ | 変わらない。親は `obj.parent` に記録されている。 |
| Collection は Object を動かすための親？ | 違う。位置を伝えるのは Object の親子。Collection は整理と表示の単位。 |
| `link` だけで元の Collection から移動する？ | 移動しない。元から外すには `unlink` が必要。 |

## 理解メモ

**Q. `make_parent_and_cube()` は、できた Cube に親子関係も付けている？** はい。この関数は **親用の Empty Object と、子用の Cube Object を1つずつ新規作成**する。`bpy.data.objects.new(f"Cube.{label}", mesh)` で Cube Object を作り、`collection.objects.link(child)` で指定の Collection に所属させる。その後の `child.parent = parent` で、Cube Object が親 Empty を参照するように設定する。`child.location = (1, 0, 0)` は、その親を基準にした子の位置を入れる。最後の `return parent, child` は作った2つの Object を呼び出し元へ返す。

たとえば `make_parent_and_cube("B", 2.0, mesh, scene, right)` なら、`Parent.B` の X は `2`、`Cube.B` のローカル X は `1`、結果のワールド X は `3`。`Cube.B` は最初 `Props.Right` に所属する。`mesh` は Cube の**形状データ**、`parent` は Cube の**親 Object**、`collection` は Cube の**所属先**で、それぞれ別の参照である。後で `Cube.B` を `Props.Left` に移しても、`child.parent` は `Parent.B` のまま。

**Q. Collection に入れた Object の Location をまとめて操作できる？** Collection 自体には Object のような `location` がない。`Props.Left` にある2つの Cube をCollectionの所属設定だけでまとめて移動することはできず、親にした Empty を動かすか、対象の Object を複数選択して一緒に移動する。複数選択して `G` で移動すると、それぞれの Object の位置が変わる。親 Empty を動かすと、子の相対配置を保ったまま全体を移動・回転・拡大できる。今回の `Cube.A` と `Cube.B` は**別々の親**を持つので、`Parent.A` だけを動かせば `Cube.A` だけが動く。

背景を作るときの使い分けを、木箱の例で考える。

| したいこと | 使う仕組み | 例 |
|---|---|---|
| 作業中に種類ごとに表示・非表示を切り替え、誤選択も避ける | Collection | `Crates`、`Rocks`、`Lighting` を分け、岩を作る間は木箱や照明を隠す。必要なら選択も制限する。 |
| 木箱を構成する板と金具を、形を崩さず1個の木箱として動かす | 親 Empty | `Crate.Root` を板と金具の親にし、この Empty の Transform を動かす。 |
| 今選んだ複数の岩を同じ距離だけ動かす | 複数 Object の選択 | 対象を選択して Object Mode で `G`。動くのは選択された Object。 |
| 同じ木箱セットを何度も配置する | Collection Instance | 木箱部品を入れた Collection のインスタンスを置き、そのインスタンス Object を動かす。これは後の反復配置の回で詳しく扱う。 |

つまり `Crates` Collection は「木箱を見つけて管理するためのまとまり」、`Crate.Root` Empty は「木箱を動かすための基準点」として併用できる。1つの Object が複数の Collection に所属する場合、片方のCollectionの表示設定だけでは隠れないこともあるため、どこに所属しているか確認する。[Blender Manual: Collections](https://docs.blender.org/manual/en/5.2/scene_layout/collections/collections.html) は整理・表示・レンダー管理を、[Parenting Objects](https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/parent.html) は親から子への Transform の伝達を説明している。

## 完了条件と次へ

ログで `Cube.B` の `collections` だけが変わったことを指し示し、なぜ親と位置が変わらなかったか説明できれば完了。次は [04 木箱の組み立て](../../docs/plan/README.md)。部品を Collection で整理しつつ、地面に置きやすい Object の原点を考える。
