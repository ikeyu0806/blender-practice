# 32｜Sculptとリトポロジー

## 目標と前提

高密度の造形を参考に、少ない頂点で表面を追うMeshを用意する。

前提は [非人体の構造](../31_creature_structure/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/32_sculpt_retopology/lesson.py
```

`CHECK OK 32_sculpt_retopology`が出たら、Blenderの **File → Open...** で `output/32_sculpt_retopology.blend` を開く。ログの関係と数値は `output/32_sculpt_retopology.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

高密度球へ数式の凹凸を加え、低密度の別MeshをShrinkwrapで投影する。これはリトポロジーの入口の比較で、必要な辺の流れを自動設計するものではない。少ない頂点へ投影すると細かな凹凸は失われる。保存前に投影を適用し、左右に離して比較できる状態へする。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 左Sculpt.Highと右Retopo.Lowを比べる。右はWireを重ねて、少ない面で大きな形を残すことを見る。
2. Edit Modeで右の四角面の流れと、左の密度を比較する。ログで頂点数の差を確認する。
3. 別名保存した左をSculpt Modeで開き、Drawブラシで少し盛る。ブラシ操作はPythonの数式変更とは別の手作業。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、高密度Meshを中央へ戻して、新しいPlaneから4頂点・1Faceの低密度パッチを作る。Face Snappingで表面へ合わせ、辺を押し出して隣のQuadを足す。Shrinkwrapを補助に使い、関節へ必要なループは自分で設計する。投影だけで実用リトポロジーが完成するわけではない。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

BULGEを0.22へ変更。高密度側の凹凸が増え、低密度側が追えない細部がはっきりする。低密度側の頂点数は同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

Sculptで形を作ることと、Retopologyで辺のつながりを設計することを区別する。

次は [変形と表情](../33_expression_deformation/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html)
