# 39｜操作用アドオン

## 目標と前提

選択Meshの情報をボタンで調べる小さなOperatorとPanelを作る。

前提は [書き出しと再取り込み](../38_export_roundtrip/README.md)。既存の01〜09でObject、Mesh、Collection、Transform、Material、Face、Modifierを理解しておく。この回は他のレッスンの出力ファイルを必要としない。

## 実行する

プロジェクトのルートで背景実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python lessons/39_inspection_addon/lesson.py
```

`CHECK OK 39_inspection_addon`が出たら、Blenderの **File → Open...** で `output/39_inspection_addon.blend` を開く。ログの関係と数値は `output/39_inspection_addon.json` にも保存される。`--python-exit-code 1` はスクリプト例外時に失敗を終了コードで知らせる指定。

観察しながら実行する場合は、同じコマンドから `--background` を外せる。保存後もターミナルはBlenderアプリの終了を待つ。現在の未保存のファイルはスクリプトの冒頭で初期化されるので、Text EditorからRun Scriptする前には別名で保存する。

GUI編集はソースへ同期しない。再実行は同じ出力を上書きするため、実験結果は別名で保存する。外部アセットの取得は不要。共通コードは同梱の [_support](../_support/README.md) が必要で、lesson.pyだけを別フォルダへ移動しない。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 仕組みとデータの関係

Operatorは実行処理、Panelはボタンを表示する場所。poll()でMeshが選ばれているときだけ操作可能にし、結果をObjectのCustom Propertiesへ記録する。クラスの登録は実行中のBlenderへ追加する設定で、.blend保存だけでは別の起動へ持ち越されない。

`lesson.py` の冒頭の定数が今回の実験値。`tools.start()`がSceneと所属先Collectionを作り、各Objectの `data` がMeshなどを参照する。最後の `tools.studio()` は観察用のCamera・Light・地面を **Presentation** Collectionへ分ける。この地面は制作対象とは区別して観察する。

**Object Mode**で移動すればObjectのTransformが変わり、**Edit Mode**で頂点を動かせばMeshが変わる。Material Previewは材質を、Solid表示は形を調べるときに使う。今回の操作がどのデータに働くか、コードのコメントと画面を照合する。

## 画面とログで観察する

1. 背景実行ログでregister/unregister/registerと面数6の確認を見る。保存された.blendのCustom Propertiesに結果が残る。
2. GUIでaddon.pyをText Editorへ開きRun Scriptする。3D ViewportのNパネルにLesson39タブが出る。
3. Meshを選んでInspect Selected Meshを押す。選択なしやCamera選択ではボタンが無効になる。

小さく見えるときはObjectを選び **View → Frame Selected**、全体を見たいときは **View → Frame All**。CameraやLightも含めると広い範囲になるので、対象だけを選択して表示する。法線を調べる場合は一般のViewport Overlaysの **Face Orientation**、面番号や面積はEdit Mode専用の **Mesh Edit Mode Overlays**を使う。

## 手で試す

毎起動使う場合はPreferences → Add-onsのメニューからInstall from Diskでoutput/39_install_addon.zipを選び有効にする。配布ZIPはローカル生成のみ。手動で登録した場合の解除はPython Consoleで登録モジュールのunregister()を呼ぶかBlenderを閉じる。実際のクリック操作は手動確認で、背景ではOperator呼出しと登録ライフサイクルを検証済み。

手作業の結果は別名の `.blend` に保存する。スクリプトの結果と見比べ、変えたデータがObject・Mesh・Material・その他のどれかをメモする。

## 値を1つ変える実験

addon.pyの `WARNING_FACE_COUNT = 1000` を4へ変更。6面の木箱でも多い面数の注意が表示される。形状や面数自体は変わらない。

先に「何が変わるか」「何が同じか」を1行ずつ書き、再実行したログと画面で答え合わせする。確認後は元の値へ戻す。期待と違えば、参照するデータと現在のモードを確認する。

## 検査と限界

生成時にはスクリプト内の `assert` と、共通保存処理の空Mesh・面積ゼロの検査を通す。`CHECK OK` はこれらのデータ検査に合格した意味で、芸術的な完成度やすべての手編集の正しさを保証しない。観察・手作業・説明も行って完了とする。

Blender **5.2.2 LTS**で背景実行と保存ファイルの再読み込みを確認（2026-10-02）。Python APIは実環境を基準とし、別バージョンではOperatorの項目名やUI配置が変わる場合がある。

## 完了条件と次へ

GUIでボタンを1回使い、選択条件・処理・表示・登録の役割を説明する。

次は [最終制作](../40_final_project/README.md)へ。 用語は [用語集](../../docs/glossary.md)、全体の到達点は [ロードマップ](../../docs/plan/README.md)へ。

## 理解メモ

- 今回変えたデータ：
- 実験の予測と結果：
- まだ説明できない点：

[公式マニュアル／API](https://docs.blender.org/api/current/bpy.types.Panel.html)
