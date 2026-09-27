---
name: blender-python-style
description: Blender教材のPythonコードを作成・編集・レビューするときに、Object、Mesh、Collectionなどの型とデータ関係が変数名から分かるように整える。一般的なPythonだけのコードには使わない。
---

# Blender Python コーディングガイド

このプロジェクトは初学者がBlenderのデータ構造を学ぶ教材なので、短さよりも **画面の用語とコードの対応が読めること**を優先する。

## データ型を変数名に出す

永続的なBlenderデータブロックや、複数の型が同時に登場する処理では、役割名の後ろに種類を付ける。

| Blenderの型 | 命名例 |
|---|---|
| `bpy.types.Object` | `crate_a_object`, `ground_object`, `mesh_object` |
| `bpy.types.Mesh` | `crate_mesh`, `ground_mesh` |
| `bpy.types.Collection` | `crates_collection`, `environment_collection` |
| `bpy.types.Material` | `wood_material` |
| `bpy.types.Scene` | `lesson_scene` |
| `bmesh.types.BMesh` | `crate_bmesh`, `target_bmesh` |

- `crate`、`crates`、`data`、`item`、`obj`のように、型や役割を読み直さないと分からない名前を主要な変数へ使わない。
- `mesh`や`collection`だけの名前は、型が自明な数行の小さな生成関数でも、同じ関数に別種のデータが登場するなら具体名へ置き換える。
- 複数のObjectが同じMeshを参照する場合、`crate_a_object`と`crate_b_object`のようにObject側だけを区別し、共有側は`crate_mesh`のように単数で表す。
- Pythonの一時的な数値、座標、ループカウンターに無理に型接尾辞を付けない。

## 関係をコード上で分離する

次の操作を同じ意味の「リンク」として説明しない。

- `bpy.data.objects.new(name, mesh)` はObjectを作り、`Object.data`にMeshを参照させる。
- `collection.objects.link(object)` はObjectをCollectionへ所属させる。
- `object.location`はObjectのTransformを変更する。Meshの頂点座標は変更しない。
- 親子関係は`object.parent`であり、Collection所属やMesh共有とは別。

これらが近接するコードでは、何を作り、どの画面で確認できるかをコメントする。コメントは処理の言い換えだけにせず、混同しやすい別の関係ではないことも必要な範囲で示す。

## 編集時の確認

1. 関連するlessonのREADMEと用語集を読み、画面で使っている名前とコードをそろえる。
2. 同じ変数名がログ、検査、READMEのコード例にも出ていないか検索する。
3. 名前変更だけで動作を変えない。差分で意図しないロジック変更がないことを確認する。
4. 利用可能なBlenderでlessonを背景実行し、データ関係、ログ、保存結果が維持されることを確認する。
