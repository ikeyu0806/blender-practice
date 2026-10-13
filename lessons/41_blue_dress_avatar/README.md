# 41｜青いワンピースのアバター

## 目標と前提

体とは別の開いたMeshで膝下のAラインワンピースを作り、足元をZ=0にして身長約1.64mの女の子を観察する。

前提は [人物の小作品](../29_character_project/README.md)。部品の分け方は [衣装と部品分割](../26_clothing_parts/README.md)、Roughnessは [マテリアルの入口](../05_material_basics/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Faceを理解しておく。この回は他のレッスンの出力ファイルを必要としない。VRoid Studioも、配布済みの完成モデルも使わない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/41_blue_dress_avatar/lesson.py
```

`CHECK OK 41_blue_dress_avatar`が出たら、Blenderの **File → Open...** で `output/41_blue_dress_avatar.blend` を開く。ログの関係と数値は `output/41_blue_dress_avatar.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

この回の女の子は、公開用アバターと同じ設計を単純なMeshで見られるようにしたもの。数値の単位はメートル。Blenderの上方向は+Z。

| 部品 | Object | 形を決めるデータ |
|---|---|---|
| 胴・腕・脚・顔 | `Heroine.Torso` など | 肌のMesh。服を編集しても頂点は動かない |
| ワンピース | `Heroine.Dress` | 別Mesh。裾の高さと半径がAライン |
| 髪 | `Heroine.Hair`、`Heroine.Hair.Back`、`Heroine.Hair.Lock.*` | 頭とは別Mesh。横髪と後ろ髪を下ろす |
| 瞳 | `Heroine.Eye.*` | 小さい黒茶色。ハイライトはさらに別Object |
| サンダル | `Heroine.Sandal.*` | 底面がZ=0。ここが地面との接点 |
| 原点 | `Heroine.Root` | データが空のEmpty。足元に置き、全部品の親 |

ワンピースの筒は上下の蓋を外してある。体の表面を塗り替えるのではなく、布の表面だけを持つ。綿のRoughnessは0.79、肌は0.64、革のサンダルは0.44。布がいちばんマットで、革が少し光る。Base Colorは、この回の観察ライトの下で青・肌・黒・アイボリーが区別できる値にしてある。公開モデルの色係数は、別の色画像へ掛けるための値で、ここの数値とは同じではない。

`Heroine.Root` の親子は、Collectionへの所属でもMeshの共有でもない。親を動かすと全身のTransformが一緒に動く。各部品のMeshはそのまま残る。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 公開しているアバターではどこまでやるか

ゲームに出している青いワンピースの女の子は、このブロックアウトと同じ見た目の判断を、次の順で形にする。

1. **形の正本はVRoid Studio。** 標準の素体に、黒髪ロング、ノースリーブ、淡い青の膝下Aラインワンピース、白いサンダルを組む。身長は約164cm。胸元はV字で、細い肩ひもとフリルは入れない。編集を続けるファイルは `.vroid`。
2. **Blenderへ渡す形はVRM。** VRoidからVRM 1.0で書き出す。人型の骨、表情のShape Key、色の画像がこのファイルに入る。
3. **Blenderでは材質を差し替える。** 読み込み直後の見た目は光に反応しない表示になりやすい。肌を暖かいベージュ、瞳をハイライトの残る黒茶色、ワンピースを粗い綿、サンダルをアイボリーの革として、Principled BSDFへ組み直す。布と革には細かい凹凸の画像を足す。元の `.vroid` と `.vrm` の画像は書き換えない。
4. **原点は足元中央、地面はZ=0。** 身長がおおよそ1.55〜1.75mに収まることを測る。このレッスンの検査は、そのうち1.64mと足元Z=0を単純形状で見る。
5. **渡すファイルはGLB。** 骨と表情の変形は残し、歩行アニメーションはこのモデルには入れない。glTFの上方向は+Y、正面は+Zなので、Blenderの+Zが上・正面が-Yというシーンとは軸の名前が変わる。書き出しと再取り込みの手順は [38](../38_export_roundtrip/README.md)、ブラウザでの表示は [Web公開のメモ](../../docs/notes/blender-web-publish.md)。

このレッスンのMeshは教材用にその場で作ったもので、VRoidの素体・髪型・衣装データは含まない。実モデルがVRoid Studioの標準プリセットを使う場合、それらの権利はpixiv Inc.に残り、利用時は [VRoid Studioガイドライン](https://vroid.com/studio/guidelines) に従う。

## 画面とログで観察する

1. Material Previewで、淡い青のワンピース、黒い髪、アイボリーのサンダルを見分ける。Outlinerで `Heroine.Dress` の目のアイコンを切ると、下から脚と胴が残る。
2. `Heroine.Dress` をEdit Modeにして、裾の輪と胸元の輪を比べる。裾の方が広い。蓋の面はなく、側面は四角面だけになっている。
3. ログの `height_m` が約1.64、`feet_z` が0、`roughness cotton/skin/leather` が `0.79/0.64/0.44` であることを `41_blue_dress_avatar.json` と照合する。Outlinerで `Heroine.Root` を選ぶと、原点が足元にある。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

`Heroine.Root` を横へ移動する。ワンピースだけをEdit Modeで広げた場合と違い、全身が一緒に動く。移動したあとにRootの位置を戻すと、各Meshの頂点は元の場所関係のままになる。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

HEM_RADIUSを0.48へ変更。ワンピースの裾だけが広がり、身長・足元のZ・肌と革のMeshは同じ。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

このブロックアウトには骨、表情のShape Key、布の織り画像、GLB書き出しを入れていない。腕と脚は筒を回して下げているだけで、[28 Armatureとウェイト](../28_armature_weights/README.md) の変形は使わない。公開モデルの骨と表情は、上のVRMの段で既に形へ含まれている。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-13）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

ワンピースを隠しても体が残ること、裾の半径を変えても身長と足元が変わらないこと、綿・肌・革のRoughnessの順を説明する。

ロードマップ本編の次の制作へ進む回ではない。骨を付けるなら [28](../28_armature_weights/README.md)、ファイルを渡すなら [38](../38_export_roundtrip/README.md) へ戻る。用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
