# 共通のシーン準備

10〜40では、初期化・単純形状・配置・保存を繰り返すため、その部分を `scene_tools.py` にまとめています。各 `lesson.py` は他のレッスンを実行せずに動きますが、このリポジトリの `_support/` が必要です。フォルダ全体を保持してください。Pythonの標準実行ではなく、Blenderの `--python` で動かします。

学習対象のBMesh編集、UV、画像ノード、Modifier、検査、書き出し、UIは各回のスクリプトに置きます。制作回は既習内容を組み合わせるため、`prop_set()`、`room()`、`humanoid()`、`monster()`も使います。これらの内部を読んで、部品の寸法・リング・ウェイトを変えられます。

- `start()`：現在のファイルを初期化し、SceneにCollectionを所属させる。
- `box()/sphere()/cone()/tube()`：Meshに寸法を作り込み、ObjectのScaleは1に保つ。
- `material()`：MaterialとPrincipled BSDFを作る。Material共有はMesh共有とは別。
- `active()/uv_smart()`：UI Operatorに必要な選択とモードをそろえる。
- `evaluated_coordinates()`：Modifier評価後の一時Meshを読み、必ず解放する。
- `studio()`：観察用Camera・Light・地面を別Collectionに作る。
- `finish()`：空Mesh・面積ゼロのFaceを検査し、`.blend`とデータ関係の`.json`を保存する。検査は制作規則をすべて保証するものではなく、各回固有の検査と画面観察も必要。

人物は学習用の分割モデルです。腕・脚はそれぞれ2本の骨、胴や足は独立したObjectで、全身の実用リグ、IK、歩行アニメーションではありません。モンスターは尾の2本の骨と顔のShape Keyを持ちます。先に変形を局所的に理解するための構成です。

生成物はすべてGit管理外の `output/`。レンダーする回はCPUのCycles・16サンプル・640×480で、画像の仕上げ品質よりも形と構図の観察を優先します。
