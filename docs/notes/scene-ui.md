# Blender の Scene は画面のどこで管理する？

## 結論

**Scene を選ぶ・新しく作る場所は、Blender 画面上部の右側にある `Scene` 欄**。レッスン01の画面では、`ViewLayer` 欄の左に表示されている。`Scene` の名前が表示された欄を開くと、現在の `.blend` にある Scene を選べる。新しい Scene を作る操作もこの欄から行う。[Blender Manual: Scene](https://docs.blender.org/manual/en/5.0/scene_layout/scene/introduction.html)

**この欄は保存済みファイルの一覧ではない。** 各 `.blend` ファイルは独自の Scene を持つ。画面タイトルが `Untitled` のままなら、`output/01_shared_mesh.blend` を開いた状態ではない。保存したレッスンの結果を見るには **File → Open...** でその `.blend` ファイルを開く。Scene 欄はファイルを開いた後、そのファイルの中の Scene を切り替えるために使う。

## 似た表示との違い

| 画面の場所 | 役割 |
|---|---|
| **最上部右側の `Scene` 欄** | 現在使う Scene を選ぶ・作る。複数 Scene があるときの切り替え場所。 |
| **File → Open...** | 別の `.blend` ファイルを開く。レッスンの保存結果を見るときはこちら。 |
| **右上の Outliner にある `Scene Collection`** | 現在の Scene に所属する Collection と Object を見る。Scene 自体の切り替え欄ではない。 |
| **右下の Properties の Scene タブ** | 現在の Scene のカメラ、単位、重力などの設定を見る・変える。Scene の一覧ではない。[Blender Manual: Scene Properties](https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html) |
| **上部の `ViewLayer` 欄** | 現在の Scene の View Layer を選ぶ。Scene とは別の単位。 |

## レッスン01のコードとの対応

```python
scene = bpy.data.scenes[0]
scene.collection.objects.link(cube_a)
scene.collection.objects.link(cube_b)
```

`bpy.data.scenes` は `.blend` 内にある Scene の一覧。レッスン01は初期化して Scene が1つの状態なので、`[0]` を使っている。`scene.collection.objects.link(...)` はその Scene の Collection に Object を入れる操作で、画面右上の Outliner に立方体が現れる。複数 Scene を扱うスクリプトでは `[0]` が現在表示中の Scene とは限らない。現在の Scene を知るには `bpy.context.scene` を使う。[Blender Python API: `bpy.data`](https://docs.blender.org/api/5.2/bpy.data.html)・[`bpy.context`](https://docs.blender.org/api/5.2/bpy.context.html)

**確認方法:** 画面最上部の `Scene` 欄を探し、その下に見える Outliner の `Scene Collection` と見比べる。さらに右下で Scene タブを選ぶと、単位や重力などの設定が表示される。それぞれ「切り替え」「中身の一覧」「設定」という別の役割になっている。

関連: [レッスン01](../../lessons/01_shared_mesh/README.md)・[Blender 用語集](../glossary.md)
