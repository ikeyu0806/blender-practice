# 01｜1つの Mesh を2つの Object で共有する

## このレッスンの目標

Blender の「見えている物体」と「形状データ」を分けて説明できるようになる。実行後、次の3点を自分の言葉で言えれば完了。

- `Object` が位置や回転を持ち、`Mesh` が頂点・辺・面を持つ。
- 2つの Object は同じ Mesh を参照できる。片方の Object の位置を変えても、もう片方の位置は変わらない。
- `mesh.users == 2` と `cube_a.data is cube_b.data` は、共有の状態を別の角度から確認している。

前提知識は Python の変数と関数だけ。まず Blender の画面と用語だけで理解できるようにする。

## 実行

プロジェクトのルートで、[lesson.py](lesson.py) を読む。その後、Blender の画面で結果を見る。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/01_shared_mesh/lesson.py
```

画面なしで出力と検証だけ行う場合:

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/01_shared_mesh/lesson.py
```

Blender 内の Text Editor からも、ファイルを開いて **Run Script** で実行できる。スクリプトは最初に現在のシーンを空にする。作業中の `.blend` がある場合は先に保存すること。成功すると `output/01_shared_mesh.blend` を生成する。`output/` は Git 管理しない。

## 何が作られるか

```text
Scene
└── Collection
    ├── Cube.A ──┐
    └── Cube.B ──┴── SharedCube (Mesh は1つ)
```

## Blender の画面とスクリプトを対応させる

| 画面で見えるもの | スクリプトで作るもの | 意味 |
|---|---|---|
| 左の立方体と Outliner の `Cube.A` | `cube_a = bpy.data.objects.new("Cube.A", mesh)` | 形状を表示する1つ目の Object。位置は初期値の `(0, 0, 0)`。 |
| 右の立方体と Outliner の `Cube.B` | `cube_b = bpy.data.objects.new("Cube.B", mesh)` と `cube_b.location = (2, 0, 0)` | 2つ目の Object。同じ形状を参照し、X 方向に2だけ移動。 |
| 各 Object の下に見える緑色の `SharedCube` | `mesh = bpy.data.meshes.new("SharedCube")` と、両 Object に渡した同じ `mesh` | Outliner に名前が2回表示されても、Mesh データは1つ。 |
| 立方体がどちらも画面に見えること | `scene.collection.objects.link(...)` の2行 | 作成した Object をシーンの Collection に入れた結果。 |

画面左の立方体に重なる赤白の照準は **3Dカーソル**。このスクリプトが作った3つ目の物体ではなく、初期位置にある操作用の目印。右下に **Scene** の設定が表示されていても、現在見ているプロパティの種類を示すだけで、Mesh の共有数を表してはいない。

「形は同じ、置き場所は別」を確かめるには、2つの立方体の位置を見比べる。Mesh の共有を確かめるには、Outliner の名前だけでなく、実行ログの `users=2` と `same mesh: True` も見る。

`bpy.data.meshes.new()` は Mesh データブロックを作る。`bmesh` で立方体の頂点・辺・面を組み立て、`bm.to_mesh(mesh)` でその内容を書き込む。この時点では Object もシーン内の表示もない。

`bpy.data.objects.new(name, mesh)` は Mesh を参照する Object を作る。ここで2回とも**同じ `mesh` 変数**を渡している。Object はそれぞれ Transform を持つため、`Cube.B.location` だけを変更できる。Mesh の形状を変更すれば両方の見た目に反映される。

Object を作っただけではシーンに現れない。`scene.collection.objects.link()` でシーンの Collection に所属させて初めて表示対象になる。Collection の所属と Mesh の参照は別の関係である。

最後に共有を検査し、`.blend` に保存する。表示される `vertices=8` は立方体の Mesh の頂点数で、Object が2つあっても Mesh の頂点数は倍にならない。

## 確認してみる

1. 実行ログに `users=2` と `same mesh: True` があることを確認する。
2. Outliner の表示モードを **Blender File** にして、`Object` が2つ、`Mesh` の `SharedCube` が1つあることを見る。Object を選び、両方の Mesh 名が同じことも確認する。
3. `cube_b.location = (2.0, 0.0, 0.0)` を `(3.0, 0.0, 0.0)` に変えて再実行する。変わるのは2つの Object の間隔であり、Mesh の数と `users` は変わらないと予測してから確かめる。
4. さらに確かめたい場合は、`cube_b = bpy.data.objects.new("Cube.B", mesh.copy())` に一時的に変える。共有の検査で停止し、`users` と `same mesh` の結果が変わる。元に戻して再実行する。

失敗した場合は、実行パスがプロジェクトのルートからの相対パスか、Text Editor で開いたファイルが保存済みかを確認する。`output/` への書き込み権限も確認する。

## よく混同する点

| 疑問 | 答え |
|---|---|
| Object が2つなら Mesh も2つ？ | いいえ。同じ Mesh を2つの Object が参照できる。 |
| `location` を変えると共有 Mesh も移動する？ | いいえ。`location` は Object 側の Transform。 |
| Collection に link したら Mesh が複製される？ | いいえ。Collection は Object の所属を決める。 |
| `users` は画面に見える個数？ | いいえ。データブロックへの参照数。今回の構成では Object の数と一致する。 |

## 理解メモ

**Q. Outliner では `SharedCube` が2回表示されるのに、Mesh は本当に1つ？** 2回表示されるのは、各 Object の「参照先」をそれぞれ見せているため。同じ名前の別 Mesh が2つあるという意味ではない。`cube_a.data is cube_b.data` が `True` なので、同じデータブロックを指している。Outliner を **Blender File** 表示に切り替えると、Mesh データブロック側からも確認できる。

**Q. Unity の例えを知らないと理解できない？** 必要ない。この回では「Object = 置き場所を持つもの」「Mesh = 立方体の形のデータ」を区別できればよい。Unity に持ち込む方法は、Blender 内で複数の部品から小作品を作れるようになってから学ぶ。今後の連携の位置づけは [補助ドキュメント](../../docs/notes/blender-unity-import.md) に記録した。

次は [ロードマップ](../../docs/plan/README.md) の **02 Transform と親子**。共有した形状と各 Object の位置を区別できたら、親子による座標の変化へ進む。
