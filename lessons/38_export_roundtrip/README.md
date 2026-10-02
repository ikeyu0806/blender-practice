# 38｜書き出しと再取り込み

## 目標と前提

人物・モンスター・背景をGLBへ渡し、再取り込み後の寸法・UV・Materialを検証する。

前提は [アセット検査](../37_asset_validation/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/38_export_roundtrip/lesson.py
```

`CHECK OK 38_export_roundtrip`が出たら、Blenderの **File → Open...** で `output/38_export_roundtrip.blend` を開く。ログの関係と数値は `output/38_export_roundtrip.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

用途はWebなどで静止モデルを見せるための交換。フレーム24のModifierとShape Keyを評価し、独立した静止Meshへ焼き出してから書き出す。元のリグは.blendに保持し、GLBには骨とアニメーションを含めない。再取り込みでFaceが三角形化されても、ワールド境界とUV・Materialが保持されるか確認する。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 左右に並ぶ元の静止Meshと再取り込みMeshを見比べる。右の配置移動は検査後に行っている。
2. ログのworld bounds equalと、output/38_assets.glbの生成を確認する。人物・モンスター・部屋が含まれる。
3. 取り込んだMeshをEdit Modeで見て面数の変化を調べる。三角形化で面数が増えても寸法が同じなら、それだけで失敗とはしない。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

任意のglTF対応ビューアへ38_assets.glbを開き、材質と向きを確認する。これはファイル作成までで公開は行わない。アニメーションを書き出す発展課題では、骨・Shape Key・Actionの対応を別途検証する。[Web公開メモ](../../docs/notes/blender-web-publish.md)。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

EXPORT_OFFSETを15へ変更。再取り込みの比較位置だけ離れ、GLBの中身と境界検査は同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

3種類のモデルの寸法、UV、Materialを確認し、静止Meshの焼き出しで編集用リグが失われる範囲を説明する。

次は [操作用アドオン](../39_inspection_addon/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)
