# 22｜Blender → Unity

## 目標と前提

接地原点と1mの寸法を持つ木箱をFBXへ書き出し、Unityで照合する手順を用意する。

前提は [背景の小作品](../21_environment_project/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/22_unity_fbx/lesson.py
```

`CHECK OK 22_unity_fbx`が出たら、Blenderの **File → Open...** で `output/22_unity_fbx.blend` を開く。ログの関係と数値は `output/22_unity_fbx.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

BlenderはZ上、ここで書き出すFBXはY上・前方-Zの設定。FBXに座標変換を記録し、受け取るImporterも変換を解釈する。変換を何度も手で追加せず、最終的な寸法・軸・原点を実物で照合する。MaterialのノードがすべてUnityへ移るとは限らない。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 左のExport.Crateと右のImport.Crateを比べる。標準値では両方1mで、底面が原点にある。
2. output/22_crate.fbxが生成され、ログのround trip dimensionsが(1,1,1)であることを確認する。
3. UnityプロジェクトのAssetsへFBXをコピーし、ProjectからSceneへ配置する。1mのCubeと大きさを比べ、InspectorのScale、底面のPivot、上向き、Materialを確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

Unity側の確認欄：使用バージョン＿＿、1m Cubeとの比較＿＿、Y上向き＿＿、Pivotが底面＿＿、Material＿＿。この環境にはUnityがないため、FBX生成とBlender再取り込みを検証済み、Unity側は未実行。実際のゲーム用モデルは21などの部品を同じ規則で選択して書き出す。骨とアニメーションはここでは扱わない。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

EXPORT_SCALEを2.0へ変更。Blender再取り込み側の寸法が2mになる。Unityでも1mのCubeと比べ、ImporterのScale Factorを重ねて変更した場合との違いを調べる。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

Blenderの書き出し・再取り込みと、Unityでの寸法・原点・材質チェックを分けて実施する。Unity側は手動確認欄がすべて埋まったら完了。

次は [人体の大きな比率](../23_body_proportions/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.unity3d.com/Manual/ImportingModelFiles.html)
