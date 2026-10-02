# 29｜人物の小作品

## 目標と前提

デフォルメ人物を1体作り、立ち姿と肘・膝を曲げた姿を残す。

前提は [Armatureとウェイト](../28_armature_weights/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/29_character_project/lesson.py
```

`CHECK OK 29_character_project`が出たら、Blenderの **File → Open...** で `output/29_character_project.blend` を開く。ログの関係と数値は `output/29_character_project.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

体、顔、髪、服、足を別部品で作り、腕と脚だけに局所の2Boneリグを用意する。フレーム1は中立姿勢、24は肘35度・膝25度の比較姿勢。胴・頭・足は独立Objectで、足は脛の骨へ追従する。歩行や全身移動を扱う完成リグではない。曲がるMeshと固定部品を区別して変形の基礎を確かめる。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

骨名のLower/Upperは管のローカルZでの位置を表す。人物では管を上下逆に配置し、Lowerが肩・腰側、Upperが手・足側になる。解剖学的な上腕・前腕の名前ではない。骨名を読み替える発展課題ではVertex Group名も同時に変える。

## 画面とログで観察する

1. output/29_neutral.pngと29_character_project.pngで、腕と脚のシルエットを比べる。
2. Timelineで1と24へ移動し、同じ人物の肘と膝が動くことを見る。正面・側面・斜めから関節の破綻を探す。
3. OutlinerのRig.Arm./Rig.Leg.を選び、各2本の骨と対応するMeshを確認する。ログで4リグと実際の頂点変位を確かめる。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

別名保存し、1つのリグのUpperをPose Modeで回転して自分のポーズを作る。足は脛へ追従するが、頭・胴の全身移動は扱わない。全身の実用リグへ拡張する際は親子・骨への追従・足の接地も設計する。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

HEAD_SIZEを0.8へ変更。頭と髪の横幅が大きくなり、胴と四肢の骨格・キーフレームは変わらない。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

1体の.blendと2ポーズの画像を残し、肘と膝の重みかリングを1か所修正して比較する。

次は [生物のシルエット](../30_creature_silhouette/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
