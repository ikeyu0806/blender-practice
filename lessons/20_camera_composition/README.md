# 20｜カメラと構図

## 目標と前提

前景・中景・背景を配置し、Cameraの焦点距離と位置の違いを理解する。

前提は [照明と色](../19_lighting/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/20_camera_composition/lesson.py
```

`CHECK OK 20_camera_composition`が出たら、Blenderの **File → Open...** で `output/20_camera_composition.blend` を開く。ログの関係と数値は `output/20_camera_composition.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

同じCamera位置で焦点距離を変えると画角が変わる。遠近の大小関係を変えるのは視点の位置。短い焦点距離で近づく操作と、遠くから長い焦点距離で同じ被写体サイズにする操作は結果が異なる。前景の岩、中景の小物、背景の壁で奥行きを読む。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. output/20_lens_24.pngと20_lens_70.pngを比べ、70mmでは写る範囲が狭くなることを見る。
2. View → Cameras → Active Cameraで画面の枠を確認。Camera Data PropertiesのLensと、NパネルのCamera位置を確認する。
3. output/20_camera_composition.pngで前景・中景・背景を指し、物の重なり方が奥行きを伝えることを説明する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、Cameraを被写体へ近づけてから焦点距離を短くし、中景の箱が同じ大きさになるよう調整する。前景と背景の相対的な大きさが変わることを観察する。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

FOCAL_LENGTHを55へ変更。Camera位置は固定で、画面に写る範囲が狭くなる。比較用24/70mm画像は変わらない。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

焦点距離とCamera位置を別のデータとして説明し、見せたい小物が枠に収まる構図を作る。

次は [背景の小作品](../21_environment_project/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
