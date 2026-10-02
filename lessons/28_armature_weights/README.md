# 28｜Armatureとウェイト

## 目標と前提

2本の骨と同名のVertex Groupで、肘の重みを混ぜて曲げる。

前提は [人物のUVと質感](../27_character_uv/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/28_armature_weights/lesson.py
```

`CHECK OK 28_armature_weights`が出たら、Blenderの **File → Open...** で `output/28_armature_weights.blend` を開く。ログの関係と数値は `output/28_armature_weights.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

ArmatureデータのEdit Boneは基準骨格、ObjectのPose Boneはポーズを持つ。Mesh ObjectのArmature Modifierが骨格Objectを参照し、Boneと同名のVertex Groupを使って変形する。Objectの親子だけではこの重み付き変形は作れない。関節の前後0.25mの範囲で2本の重みを混ぜ、頂点ごとの合計を1に保つ。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. Rig.Armを選びPose Modeへ。Upperだけを選択し回転すると上半分が曲がる。Edit Modeの骨は基準姿勢であることを確認する。
2. Arm.Skinnedを選びObject Data PropertiesのVertex Groupsを見る。LowerとUpperがBone名と一致する。
3. Edit Modeでz=1のリングの頂点を1つ選び、Vertex WeightsとログのLower=0.5、Upper=0.5を照合する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

Weight PaintでUpperの重みを観察する。塗る前に別名保存し、関節の頂点をUpper=1へ寄せて変形の境目を見る。Auto Normalizeを使うか、Lowerも含めて合計1を保つ。全身リグやIKへ進む前にこの2本で関係を確かめる。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

BEND_ANGLEを75へ変更。基準MeshとBoneの位置は同じで、Pose Boneによる曲げ量が増える。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

Armature参照、Bone名、Vertex Group、重み合計の4条件から変形を説明する。

次は [人物の小作品](../29_character_project/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html)
