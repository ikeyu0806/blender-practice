# 24｜顔と髪のブロックアウト

## 目標と前提

頭・顎・鼻・耳と、髪の大きな塊を正面と側面から整える。

前提は [人体の大きな比率](../23_body_proportions/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/24_face_hair/lesson.py
```

`CHECK OK 24_face_hair`が出たら、Blenderの **File → Open...** で `output/24_face_hair.blend` を開く。ログの関係と数値は `output/24_face_hair.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

前方は-Y、上方はZとして作る。正面では横幅と左右の間隔、側面では鼻の突出、額、後頭部、髪の厚みを読む。髪は頭Meshへ書き込まず、4つの独立Objectで大きな輪郭を作る。この回は目や口の細部を増やす前のブロックアウト。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. Frontで頭・顎・左右の髪の幅を確認し、Rightで鼻と前髪の奥行きを見る。
2. OutlinerでFace.とHair.の接頭辞を追い、Cap・Fringe・Sideの4部品を確認する。
3. 髪をOutlinerで一時的に非表示にし、頭の輪郭と髪の輪郭を区別する。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

顎か前髪を1か所だけ変えて別名保存する。正面だけで調整せず、側面と斜めでも頭や鼻へ食い込んでいないか見る。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

NOSE_DEPTHを0.36へ変更。鼻先が-Y方向へ伸び、正面の幅は変わらない。側面のシルエットだけで差を説明する。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

正面と側面で同じモデルの形が成立し、顔と髪が独立したMeshであることを説明する。

次は [関節周辺のトポロジー](../25_joint_topology/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/manual/en/latest/)
