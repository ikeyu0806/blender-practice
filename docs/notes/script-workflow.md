# `lesson.py` と Blender の画面は同期する？

## 結論

`lesson.py` はシーンを**作る手順**、`output/*.blend` は実行してできた**結果のファイル**です。Blender の画面で Object の Location などを変えても、Python のソースは書き換わりません。画面での変更は現在開いている `.blend` のデータにだけ反映され、保存するとその `.blend` に記録されます。

## 普段の実行手順

プロジェクトのルートで、たとえばレッスン01を次のように実行します。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/01_shared_mesh/lesson.py
```

1. `Blender` は `/Applications/Blender.app` の中にある Blender の実行ファイルです。macOS のデスクトップそのものを起動するコマンドではありません。
2. `--background` は Blender の画面を出さずに実行します。`--python` は指定したスクリプトを Blender 内の Python で実行します。
3. スクリプトが `output/01_shared_mesh.blend` を保存したら Blender のプロセスも終了し、ターミナルの入力待ちに戻ります。
4. 結果を観察するときは、Blender アプリの **File → Open...** から `output/01_shared_mesh.blend` を開きます。すでに開いていた別のウィンドウは、自動では新しい結果に切り替わりません。

`--background` を付けずに `Blender --python ...` と実行すると、Blender は画面付きで起動します。スクリプトが保存まで終わってもアプリは開いたままで、ターミナルは**Blender の終了**を待ちます。これは Python が変更を監視・同期している状態ではありません。

## 画面で試した変更を残すには

- 画面で動かして試した結果を残したい場合は、**File → Save As...** で別名の `.blend` に保存します。`lesson.py` を再実行すると、この教材はシーンを最初から作り直して同じ `output/XX.blend` に保存するため、その出力ファイルへ保存した手作業の変更は上書きされ得ます。
- 毎回同じ配置を再現したい場合は、GUI で変えた値を参考に `lesson.py` の該当する値を自分で編集し、背景実行して出力を作り直します。GUI からソースへの自動反映はありません。
- Blender の **Text Editor → Run Script** でも実行できますが、この教材のスクリプトは最初に開いているシーンを初期化します。今の作業を残すなら、実行前に別の `.blend` として保存します。

たとえばレッスン01では、`Cube.B` を GUI で X=3 に動かして保存しても、ソースの `cube_b.location = (2.0, 0.0, 0.0)` はそのままです。ソースを変更しないまま再実行すると、生成される `Cube.B` は再び X=2 になります。

関連: [01 共有 Mesh](../../lessons/01_shared_mesh/README.md)、[02 Transform と親子](../../lessons/02_parent_transform/README.md)
