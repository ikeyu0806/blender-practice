# 35｜再実行可能な生成スクリプト

## 目標と前提

自分が生成したObjectだけを置き換え、2回走らせても同じ結果にする。

前提は [モンスターの小作品](../34_monster_project/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/35_repeatable_generation/lesson.py
```

`CHECK OK 35_repeatable_generation`が出たら、Blenderの **File → Open...** で `output/35_repeatable_generation.blend` を開く。ログの関係と数値は `output/35_repeatable_generation.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

冪等な生成では、命名だけでなく個数、寸法、位置、使わないデータの増殖も確認する。start()は教材を用意するために1回初期化し、その後のgenerate_assets()は専用Collectionだけを掃除する。消したObjectのMeshはusers=0なら解放し、Materialは名前で再利用する。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. OutlinerでGenerated.Crate.00〜03と、消さずに残したKeep.Unrelatedを確認する。
2. ログのtwo runs identicalを読み、名前・Mesh名・位置・寸法のスナップショットが等しいことを見る。
3. Blender File表示でMeshやMaterialに.001の余分な複製が増えていないことを確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

Scriptingでgenerate_assets()の削除対象を読み、SceneのすべてのObjectを消す実装との差を説明する。この教材の入口start()は初期化するので、手作業のSceneへ組み込むときはgenerate_assets()の所有範囲の考え方を取り出す。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

ASSET_COUNTを6へ変更。生成数が6へ変わるが、1回目と2回目の結果は同じでKeep.Unrelatedが残る。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

生成処理を2回呼び、個数・命名・形・無関係Objectの保存を検査する。

次は [依存関係と評価結果](../36_dependency_evaluation/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
