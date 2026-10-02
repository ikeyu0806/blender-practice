# 12｜比率とシルエット

## 目標と前提

正面の輪郭で2体の頭身を比較し、自作参照図から形を分解する。

前提は [法線と面の向き](../11_normals_shading/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/12_silhouette/lesson.py
```

`CHECK OK 12_silhouette`が出たら、Blenderの **File → Open...** で `output/12_silhouette.blend` を開く。ログの関係と数値は `output/12_silhouette.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

細部を増やす前に、頭・胴・脚を単純形状として配置する。Orthographic Cameraでは遠近による大きさの変化がないため、比率を読み取りやすい。参照画像は正解の指定ではなく、大きな形を見つけるための練習用。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. Camera Viewで左右の頭身を比べる。頭の直径以外は同じ寸法。
2. Image Editorの画像一覧でReference.Proportionsを選ぶ。参照を頭・胴・2本の脚へ分解して説明する。
3. View → Viewpoint → FrontとRightで正面と側面を見る。細部なしで印象の違いが伝わるか、縮小して確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、右の胴Objectの寸法を1つだけ変えて、大柄・細身のどちらの印象になるか予測する。画像は外部アセット不要で、output/12_reference.pngとしても保存される。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

HEAD_RATIOを0.55へ変更。右の頭だけ大きくなり、胴と脚は変わらない。遠目でも違いが読めるか観察する。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

正面と側面のどちらからも頭・胴・脚を識別し、比率を選んだ理由を説明する。

次は [UV展開](../13_uv_unwrap/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
