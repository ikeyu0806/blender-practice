# 25｜関節周辺のトポロジー

## 目標と前提

同じ太さの管を、関節付近のリング数を変えて曲げる。

前提は [顔と髪のブロックアウト](../24_face_hair/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/25_joint_topology/lesson.py
```

`CHECK OK 25_joint_topology`が出たら、Blenderの **File → Open...** で `output/25_joint_topology.blend` を開く。ログの関係と数値は `output/25_joint_topology.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

曲がる場所には、向きを変えながら幅を保つための面が必要。左は3リング、右は5リングで、右だけ関節の前後に支えのリングを置く。両方に同じ骨・重みの計算・曲げ角度を使い、頂点の配置の違いを比べる。リングを増やしても、重みが不適切なら自然な変形になるとは限らない。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. Object Modeで左右の曲がった外側と内側を見る。内側の圧縮や外側の伸びを比べる。
2. Edit Modeへ切り替えると基準Meshが見える。左3・右5の断面リングを数える。Modifierの表示切り替えで基準と曲げた形を往復する。
3. ログで頂点数24対40と、曲げによる変位が0より大きいことを確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、右の関節前後のリングを遠ざけて曲げ結果を見る。骨とウェイトは次の28で作るので、ここではModifierが与えられた比較装置として使う。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

BEND_ANGLEを35へ変更。頂点数は同じで曲げる量が減る。変形の違いが小さな角度では見えにくくなることも確認する。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

辺の数だけでなく配置する場所が重要である理由を、左右の関節を示して説明する。

次は [衣装と部品分割](../26_clothing_parts/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
