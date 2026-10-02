# 33｜変形と表情

## 目標と前提

顔はShape Key、尾は骨で変形させ、データの違いを比較する。

前提は [Sculptとリトポロジー](../32_sculpt_retopology/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/33_expression_deformation/lesson.py
```

`CHECK OK 33_expression_deformation`が出たら、Blenderの **File → Open...** で `output/33_expression_deformation.blend` を開く。ログの関係と数値は `output/33_expression_deformation.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

Shape Keyは同じ頂点番号へ別の座標を持ち、Valueで基準と混ぜる。Boneは基準座標へPoseの変換とウェイトを適用する。顔のJawDropは下顎に見立てた前方下側の頂点を下げる練習用で、口腔や歯を持つ完成した口ではない。尾は関節より先を横へ曲げる。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

スクリプトはJawDropの値を明示的に0へ設定してフレーム1のキーを記録し、1へ設定して24のキーを記録する。Blender 5.2.2では追加直後のShape Keyの値が1だったため、初期値に任せると2ポーズが同じになる。名前とキーの存在だけでなく、再読み込み後の頂点座標の差も検証している。

## 画面とログで観察する

1. Timelineの1と24を往復し、顎の輪郭と尾の曲がりを確認する。
2. Monster.HeadのObject Data Properties → Shape KeysでBasisとJawDropを見る。Meshの頂点数は同じ。
3. Rig.TailをPose Modeで開きUpperを選ぶ。顔のShape Keyと尾のBoneが別の場所にあることを確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

Timelineを24へ固定し、Shape KeysのJawDropを0から1へ動かす。アニメーションがある値はフレーム移動でキーの値に戻るので、手作業の値を残すときはキーを更新して別名保存する。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

EXPRESSION_VALUEを0.4へ変更。フレーム24の顎の変形だけ弱くなり、尾のポーズと頂点数は同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

Shape KeyとBoneが同じ結果を作る設定ではないことを、参照と保存場所から説明する。

次は [モンスターの小作品](../34_monster_project/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
