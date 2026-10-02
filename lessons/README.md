# レッスン一覧

| 番号 | テーマ | 状態 |
|---|---|---|
| [01](01_shared_mesh/README.md) | 共有 Mesh | 実装済み |
| [02](02_parent_transform/README.md) | Transform と親子 | 実装済み |
| [03](03_collection/README.md) | Collection の所属 | 実装済み |
| [04](04_crate_origin/README.md) | 木箱の組み立てと原点 | 実装済み |
| [05](05_material_basics/README.md) | マテリアルの入口 | 実装済み |
| [06](06_material_slots/README.md) | Material SlotとFaceの割り当て | 実装済み |
| [07](07_modifier_evaluation/README.md) | Modifierの評価 | 実装済み |
| [08](08_vertices_rock/README.md) | 頂点から作る岩とFaceの向き | 実装済み |
| [09](09_face_inspection/README.md) | Face情報の閲覧と編集 | 実装済み |
| [10](10_mesh_edit/README.md) | メッシュ編集の基本 | 実装済み |
| [11](11_normals_shading/README.md) | 法線と面の向き | 実装済み |
| [12](12_silhouette/README.md) | 比率とシルエット | 実装済み |

これからのテーマと順番は [ロードマップ](../docs/plan/README.md) を参照してください。

## フォルダとファイル

```text
lessons/
  01_shared_mesh/
    README.md     # 目的、解説、実行、観察、実験、よくある疑問
    lesson.py     # コメント付きの実行可能な教材
  02_parent_transform/
    README.md
    lesson.py
  03_collection/
    README.md
    lesson.py
  04_crate_origin/
    README.md
    lesson.py
  05_material_basics/
    README.md
    lesson.py
  06_material_slots/
    README.md
    lesson.py
  07_modifier_evaluation/
    README.md
    lesson.py
  08_vertices_rock/
    README.md
    lesson.py
  09_face_inspection/
    README.md
    lesson.py
```

新しいレッスンは `NN_short_topic/` のように番号付きフォルダを作り、少なくとも `README.md` と `lesson.py` を一緒に追加します。生成物は `output/` に保存し、Git には含めません。画像・入力ファイルが必要な回は、その用途と入手・作成方法を README に書きます。

スクリプトには、操作の**理由**、重要な Blender の概念、画面やログで見える結果、失敗しやすい点を説明するコメントを付けます。README には学習目標、前提、実行方法、仕組みの解説、観察手順、変更実験、完了条件を入れます。コードの各行を README で言い換えるだけにはしません。

各スクリプトは、単独で実行して予測可能なシーンを作り、観察結果をログに出すことを基本にします。既存の `.blend` を初期化する場合は README に明記します。依存する外部アセットがある場合は同じフォルダに置くか、取得手順を記します。レッスン間の共通コードを先に増やさず、同じ処理が繰り返されて必要になったら切り出します。

普段は各 README の `--background --python` コマンドでシーンを生成し、保存された `.blend` を Blender アプリで開いて観察します。画面での編集は `lesson.py` へ自動で反映されません。詳しくは [スクリプトと画面の関係](../docs/notes/script-workflow.md) を参照してください。

質問の回答は、レッスン固有ならその `README.md` の「理解メモ」へ、複数回に共通するなら [docs/notes](../docs/notes/README.md) へ残します。
