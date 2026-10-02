# 13｜UV展開

## 目標と前提

立方体の6面をUV空間へ並べ、継ぎ目とテクスチャの伸びを調べる。

前提は [比率とシルエット](../12_silhouette/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/13_uv_unwrap/lesson.py
```

`CHECK OK 13_uv_unwrap`が出たら、Blenderの **File → Open...** で `output/13_uv_unwrap.blend` を開く。ログの関係と数値は `output/13_uv_unwrap.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

UVは3Dの頂点位置とは別の2D座標で、Faceの角ごとに記録する。8頂点の箱でもUVの角は24個ある。今回は全辺を継ぎ目として6枚に分ける。各島を同じ大きさへ置くため、横長の面と正方形の面ではチェック柄の比率が異なり、伸びを比較できる。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. UV EditingでCrate.UVを選びEdit Mode・全Face選択。左のUV Editorに3列2行の島が見える。
2. UV Editorの画像一覧からUV.Checkerを選ぶ。右をMaterial Previewにして、横長の面と端面の格子を比べる。
3. 8頂点と24 UV cornersのログを、FaceごとにUVが分かれる仕組みと結びつける。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

箱を別名保存し、1本のSeamを外してからUV → Unwrapを試す。自動Unwrapはスクリプトの6島配置を再現する操作ではない。隣接面がつながると島の形がどう変わるか見る。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

UV_SCALEを0.5へ変更。3D形状は変わらず、横方向のUVの幅だけ半分になる。模様の横の密度がどう変わるか予測する。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

UVの変更がMeshの頂点座標を動かさないことと、継ぎ目を全辺へ置いた理由を説明する。

次は [テクスチャとマテリアル](../14_image_material/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
