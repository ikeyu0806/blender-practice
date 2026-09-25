# blender-toolkit の進め方

Blender をスクリプトで操作する toolkit のスクリプト集として始める。動くことより、Outliner に何が増えたかを言葉にできることを目標にする。

Unity でいう GameObject の組み立てを、Blender ではデータブロックとして作り直す。見た目の立方体を出すことより、どのデータが共有され、どの階層が位置を決めるかを毎回確認する。

対象バージョンは Blender 4.4.1（`/Applications/Blender.app`）。コマンド名 `blender` は PATH に無いので、実行時はアプリ内のバイナリを直接呼ぶ。

## 理解の軸

Blender のファイルは、メッシュやマテリアルなどのデータブロックの集まりである。オブジェクトはその入れ物である。

| Unity | Blender | スクリプトで触るもの |
|---|---|---|
| Mesh アセット | Mesh データブロック | `bpy.data.meshes` |
| GameObject + Transform + MeshFilter | Object | `bpy.data.objects` |
| 空の GameObject を親にした階層 | 親子（parent） | `obj.parent`、`matrix_world` |
| Hierarchy の整理用フォルダ | Collection | `bpy.data.collections` |
| Prefab を2つ置いてメッシュを共有 | 1つの Mesh を複数 Object が参照 | `mesh.users` |
| URP Lit | Principled BSDF | マテリアルのノード |
| コンポーネントを足して後から Bake | Modifier | 元メッシュと評価後メッシュ |

Unity では Hierarchy が「見た目の整理」と「Transform の親子」を同時に担う。Blender ではこれが分かれている。Collection に入れても位置関係は変わらない。位置を決めるのは parent である。ゲーム用の原点（地面に置くピボット）は、Object の origin として別に扱う。

座標系は Blender が Z-up、1 unit = 1 m。Python の回転はラジアン。glTF で書き出すと Y-up に変換される。Unity に持っていく前に、位置・向き・サイズを実測してこの変換を確認する。

UI の「立方体を追加」は内部ではオペレーター（`bpy.ops`）である。オペレーターは選択中のオブジェクトやモードに依存する。レッスンの本体はデータ API（`bpy.data` と `bmesh`）に置く。オペレーターは、UI のあの操作がどのデータブロックを作っていたかを一度見るときに使う。

## リポジトリの形

アドオンにはまだしない。アドオンは登録処理が前に出て、データの動きが見えにくくなる。単体スクリプトで、関数にすると何が残るかが分かってから、ボタンにする。

```text
blender-toolkit/
  toolkit/          # 再利用する関数。scene, mesh, material, inspect
  lessons/          # 1ファイル1概念。実行すると output に .blend を書く
  output/           # 生成物。git 管理しない
  docs/plan/        # この方針
```

`toolkit/` に関数を移すのは、同じ操作を2回書いたときだけにする。先にライブラリを作ると、何を隠したか分からなくなる。

## レッスンの型

各レッスンは次の型にする。

1. ファイル先頭に「今日分かること」と、Unity でいうと何かを書く
2. シーンを空にしてから作り直す（再実行で差分が読める）
3. 最後にデータブロックの木を print する
4. `.blend` を保存する

学習中の実行は GUI 付きにする。結果を Outliner で見られる。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/01_shared_mesh.py
```

同じスクリプトを `--background` で走らせると、画面なしで `.blend` だけ作れる。toolkit の確認用である。Blender 内では Scripting ワークスペースの Text Editor で Run Script しても同じ結果になる。

## 進める順番

各段階でプロップを1つ作り、そのプロップで1つの概念だけを見る。

1. **共有メッシュ** (`lessons/01_shared_mesh.py`)
   立方体の Mesh を1つ作り、Object を2つから参照する。片方だけ動かす。`mesh.users` が 2 になることを print する。Unity の共有メッシュと同じで、見た目が2つでもデータは1つである。

2. **Transform と親子**
   Empty を親にして、子の location がローカルだと確認する。`matrix_world` を print して、ワールド座標は親子の積だと確認する。

3. **Collection**
   同じ親子を、Collection の所属だけ変える。位置は変わらないことを見る。整理と階層が別だと体感する。

4. **木箱**
   板を Transform で組む。origin を底面の中央に置く。Unity に置いたとき地面に埋まるかどうかは、ほぼここで決まる。

5. **マテリアル**
   Principled BSDF の Base Color / Metallic / Roughness だけ触る。Roughness は Unity の Smoothness と向きが逆である。数値を変えてビューポートで比較する。

6. **Modifier**
   木箱に Bevel を足し、元の頂点数と評価後の頂点数を両方 print する。Modifier は元の Mesh を書き換えない。書き出す直前に Apply する、という判断がここである。

7. **頂点から作る**
   低ポリの岩を、頂点・辺・面の配列から作る。プリミティブを並べる段階と、メッシュそのものを編集する段階の境目である。

8. **glTF で Unity に置く**
   スケールを適用し、原点を確認し、書き出して Unity で位置・向き・サイズを見る。Blender だけで完結させず、ゲーム側の結果で理解を閉じる。

## 毎回の見方

スクリプトを走らせたあと、Outliner の表示を Blender File に切り替える。Scene の外に Mesh や Material がいるのが見える。Object を選んで、使っている Mesh 名と `users` を確認する。数値を1つだけ変えて、変わるものと変わらないものを予測してから再実行する。予測が外れた箇所がその回の理解になる。

## 最初の実装

最初に書くのは `lessons/01_shared_mesh.py` である。Mesh を1つ、Object を2つ、print で利用者数、保存まで。ここが分かると、その後の木箱も岩も「Object に Mesh を付けている」と同じ操作の延長になる。
