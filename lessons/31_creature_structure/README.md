# 31｜非人体の構造

## 目標と前提

四足・角・尾を分割して配置し、人体との構造の違いを作る。

前提は [生物のシルエット](../30_creature_silhouette/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/31_creature_structure/lesson.py
```

`CHECK OK 31_creature_structure`が出たら、Blenderの **File → Open...** で `output/31_creature_structure.blend` を開く。ログの関係と数値は `output/31_creature_structure.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

胴、頭、4本の脚、角、尾は独立Mesh。近接して見えても接続済みの1枚の皮膚ではない。初期設計では部品を分けると形を試しやすく、あとで一体化する場合は重なりや接合面を設計する。尾だけ2Boneの変形を用意し、次の表現の回につなぐ。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 前・横・上から四足、尾の根元、2本の角を確認する。人物との違いを輪郭で説明する。
2. 尾を選んでEdit Modeへ入り、管のリングが胴のMeshと別であることを見る。
3. OutlinerのMonster.Leg.を4個数え、尾のModifierがRig.Tailを参照することを確認する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

尾の根元を移動し、胴との隙間ができることを見る。ObjectのJoinは1Objectにまとめるだけで頂点を自動接続しない。一体化するなら接合部のFaceや頂点を設計する。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

HORN_HEIGHTを0.9へ変更。角だけ長くなり、胴・脚・尾の寸法と骨は変わらない。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

尾・角・追加の脚を独立Meshとして識別し、どこが接続されていないか説明する。

次は [Sculptとリトポロジー](../32_sculpt_retopology/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
