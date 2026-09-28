# Blender レッスンのログはどこで見る？

## 結論

このプロジェクトで「ログ」と呼ぶ `print()` の文字列は、**Blender を起動したターミナル**に表示される。保存した `.blend` を Blender アプリで開くだけでは、以前の `print()` 出力は画面に再表示されない。

たとえばプロジェクトのルートで次を実行する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/04_crate_origin/lesson.py
```

実行した**同じターミナルの画面**を上にスクロールすると、次のような行が見つかる。

```text
=== 04 crate origin ===
mesh local bottom=0.000
Crate.A origin_z=0.000 bottom_z=0.000 collection=Crates
Crate.B origin_z=0.000 bottom_z=0.000 collection=Crates
ground top_z=0.000
saved: .../output/04_crate_origin.blend
```

`--background` はBlenderの画面を出さずに実行し、終了後にターミナルへ戻る。`--background` を外して画面付きで起動しても、**ターミナルから起動した場合は出力先はそのターミナル**。画面付き起動ではBlenderを閉じるまでターミナルが待機するが、`saved:` が出ていれば保存処理は終わっている。

## Blender アプリ内で見えるものとの違い

| 場所 | 主に見えるもの | この教材の `print()` ログ |
|---|---|---|
| 起動に使った macOS のターミナル | `print()`、実行エラー、Blender の起動・終了メッセージ | **ここで見る** |
| Blender の **Info Editor** | 実行した操作、報告、警告など | 通常の `print()` 出力を探す場所ではない |
| Blender の **Python Console** | `>>>` に自分で入力したPythonと、その実行結果 | 別の `lesson.py` の実行履歴を表示する窓ではない |
| Blender の **Text Editor** | `lesson.py` のソースコード | 出力先ではない |

Blender をDockやFinderから開いて **Text Editor → Run Script** した場合、`print()` をすぐ見られるターミナルがないことがある。レッスンのログを確実に見たいときは、上のように**ターミナルからBlenderを起動して実行**する。画面の操作履歴だけを見たい場合は、Blenderのエリア左上にあるエディター種類のボタンから **Info Editor** を選ぶ。

Blender公式資料も、スクリプトの `print()` と詳細なエラーを確認する場所として、Blenderを起動した[ターミナル](https://docs.blender.org/api/5.2/info_tips_and_tricks.html)を案内している。macOSでは[アプリ内の実行ファイルをターミナルから起動](https://docs.blender.org/manual/en/5.2/advanced/command_line/launch/macos.html)できる。Info Editor の役割は[操作・報告の履歴](https://docs.blender.org/manual/en/5.2/editors/info_editor.html)。

関連: [スクリプトと画面の関係](script-workflow.md)、[04 木箱の組み立て](../../lessons/04_crate_origin/README.md)
