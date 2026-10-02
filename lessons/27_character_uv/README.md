# 27｜人物のUVと質感

## 目標と前提

肌・布・金属の領域を1枚のAtlasへ並べ、UVで使う領域を選ぶ。

前提は [衣装と部品分割](../26_clothing_parts/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/27_character_uv/lesson.py
```

`CHECK OK 27_character_uv`が出たら、Blenderの **File → Open...** で `output/27_character_uv.blend` を開く。ログの関係と数値は `output/27_character_uv.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

Atlasは複数の表面の画像を1枚へまとめた配置。この回は左から肌・布・金属の帯を作り、部品のUVを対応する帯へ縮小移動する。同じMaterialでも、UV位置と色・粗さ・金属値の画像が違えば見え方が変わる。部品の境界から5%余白を取り、隣の帯の色を拾いにくくする。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. UV Editingで頭・上着・金具を順に選び、UVがAtlas.Colorの左・中央・右にあることを見る。
2. Shadingで3枚の画像がBase Color、Roughness、Metallicへ接続されることを確認する。
3. Material Previewで肌の柔らかな反射、布の鈍い反射、金具の強い反射を比べる。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

UV Editorで金具の島を肌の帯へ移す。Meshの寸法を変えずに、色・粗さ・金属感がまとめて肌の設定へ変わることを見る。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

CLOTH_ROUGHNESSを0.35へ変更。中央帯の粗さだけが下がり、上着の反射が強くなる。色とUVの場所は同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

3つの部品が同じMaterialで異なる質感になる理由を、UVと画像ノードから説明する。

次は [Armatureとウェイト](../28_armature_weights/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
