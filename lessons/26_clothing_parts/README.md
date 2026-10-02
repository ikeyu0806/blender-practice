# 26｜衣装と部品分割

## 目標と前提

体・上着・金具を別々のMeshとして作り、上着へ厚みを付ける。

前提は [関節周辺のトポロジー](../25_joint_topology/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/26_clothing_parts/lesson.py
```

`CHECK OK 26_clothing_parts`が出たら、Blenderの **File → Open...** で `output/26_clothing_parts.blend` を開く。ログの関係と数値は `output/26_clothing_parts.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

薄い服の表面Meshには幾何学的な厚みがない。Solidifyで表示結果へ厚みを足し、元の表面を編集しやすく保つ。今回は開いた筒状のベストで、上下の縁を観察しやすくする。体との隙間、布の厚み、金具の配置は別の問題として調整する。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 上から上着の開いた襟を見る。Object ModeのModifier PropertiesでFabricThicknessを切り替える。
2. OutlinerでClothing.Vestを隠すとCharacter.Bodyが残る。金具も別Objectであることを確認する。
3. Edit Modeの表面16面と、Modifier評価後に増える頂点をログで照合する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、上着の上側リングだけを広げる。襟と体の隙間を見て、厚みを増やす操作との違いを確認する。この教材は袖・縫い目・布シミュレーションの完成モデルではなく部品分割の練習。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

CLOTH_THICKNESSを0.08へ変更。元Meshの16面と体の形は同じで、外向きの厚みが増える。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

体を編集せずに服の厚みを変え、3種類の部品を分けた理由を説明する。

次は [人物のUVと質感](../27_character_uv/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
