# 34｜モンスターの小作品

## 目標と前提

四足・角・尾のある1体を、中立と表情・尾を変えた姿で仕上げる。

前提は [変形と表情](../33_expression_deformation/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/34_monster_project/lesson.py
```

`CHECK OK 34_monster_project`が出たら、Blenderの **File → Open...** で `output/34_monster_project.blend` を開く。ログの関係と数値は `output/34_monster_project.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

30の輪郭、31の部品構造、32の密度と辺の流れ、33の変形を制作上の確認に使う。ここでは低ポリの分割モデルを1体にまとめ、尾と顔だけ動かす。四肢の歩行、翼、体全体のアクションは発展課題として残し、特徴が保たれる局所ポーズを確認する。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. output/34_neutral.pngと34_monster_project.pngを比べ、角・四足・尾の特徴が保たれるか確認する。
2. Timelineの1と24、Front・Right・斜めで、尾の根元と顎の伸びを確認する。
3. Material、UV、部品名、BoneとShape Keyを順に確認し、背景や人物の概念と共通する部分を挙げる。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

自分の変更を角・胴の幅・尾の曲げ角度から1つ選び、2ポーズで破綻がないか見る。全身のアクションへ進む場合は脚にも28の方法で骨とウェイトを足し、接地とバランスを設計する。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

HORN_HEIGHTを0.8へ変更。中立とアクションの両方で角が長くなり、尾と顔のキーは同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

1体の.blendと2ポーズの画像を残し、人物とのシルエットの違いと局所変形を説明する。

次は [再実行可能な生成スクリプト](../35_repeatable_generation/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
