# 37｜アセット検査

## 目標と前提

正しい小物と意図的な不良モデルを検査し、問題の場所を一覧にする。

前提は [依存関係と評価結果](../36_dependency_evaluation/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/37_asset_validation/lesson.py
```

`CHECK OK 37_asset_validation`が出たら、Blenderの **File → Open...** で `output/37_asset_validation.blend` を開く。ログの関係と数値は `output/37_asset_validation.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

検査は用途を先に決める。この回は閉じた小物用に、接頭辞・Scale・最大寸法・UV・Material・画像参照・面積・閉じた辺・面の向きの整合を確認する。開いた地形や服に同じ閉面規則を使うと誤検出する。問題を集めて報告し、検出した後に人が修正する。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 左Asset.Goodと右WrongNameの見た目を比較する。右はScale.z=2で、1面だけ法線が反転しUVもない。
2. ログとoutput/37_inspection.jsonで、右のname・scale・UV・normalsの4項目を確認する。
3. 右をEdit ModeのFace Orientationで見て、反転面を特定する。Custom Propertiesのinspectionにも結果が残る。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、右をAsset.Fixedへ改名、Object → Apply → Scale、Edit ModeでRecalculate Outside、UV → Smart UV Projectを行う。検査関数へ修正後Objectを渡し、問題が消えるか確認する。GUI修正後の再検査は関数だけを呼び、全スクリプトの初期化は避ける。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

MAX_DIMENSIONを1.5へ変更。右の高さ2mが追加の寸法違反になり、左の1mモデルは合格のまま。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

検査で発見した問題を画面から示し、閉じた小物と開いた表面で規則を変える理由を説明する。

次は [書き出しと再取り込み](../38_export_roundtrip/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
