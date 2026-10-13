# 40｜最終制作

## 目標と前提

人物・モンスター・背景を1つのSceneで見せ、再現と検査の手順を残す。

前提は [操作用アドオン](../39_inspection_addon/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/40_final_project/lesson.py
```

`CHECK OK 40_final_project`が出たら、Blenderの **File → Open...** で `output/40_final_project.blend` を開く。ログの関係と数値は `output/40_final_project.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

最終制作は既習内容の統合。各カテゴリを別Collectionへ入れ、人物のMeshと局所Rig、モンスターのMeshと尾Rigを同じ距離だけ動かして配置する。背景は規格部品を使い、UV・Material・Scaleと実際の変形を検査する。1から24へ切り替えれば両キャラクターのポーズを比較できる。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. output/40_final_project.pngで人物、モンスター、入口のある部屋が1枚に見えることを確認する。
2. OutlinerのFinal.Character・Final.Monster・Final.Environmentを順に隠し、カテゴリとPresentationの違いを見る。
3. Timelineの1と24で肘・膝・顎・尾を観察する。ログと40_final_project.jsonで寸法・名前・参照を確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

自分の作品として人物かモンスターの比率・色を1つ変え、入口からの視線と2ポーズを確認する。交換ファイルは38の静止Mesh焼き出し手順で作る。完成した自作版では、37の検査規則を用途へ合わせ、修正した値と検査結果を制作メモへ残す。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

CHARACTER_Xを-1.3へ変更。人物のMeshとRigが一緒に動き、人物の位置だけがモンスターへ近づく。光・部屋・モンスターの配置は同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

3種類の.blendと画像を残し、生成→検査→画像→交換形式の手順を自分の言葉で再実行する。

この回でロードマップの制作を終え、自分の題材へ置き換えて反復する。公開アバターと同じ設計を単純形状で見るなら [41 青いワンピースのアバター](../41_blue_dress_avatar/README.md)。用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
