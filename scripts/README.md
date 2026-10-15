# レッスンのまとめて確認

通常のPythonから、10〜41の教材をBlenderで順に生成し、保存したファイルを別のBlenderプロセスで開いて確認できます。

```bash
python3 scripts/verify_lessons.py
```

**生成モードは各レッスンのoutputを上書きします。** 手編集の.blendは別名で残してから実行してください。Cameraを使う回ではCPUで比較画像も生成するため、数十秒以上かかる場合があります。Unityの操作やアドオンのボタンクリックはこの確認には含まれません。

既存の出力を変更せずに確認する場合：

```bash
python3 scripts/verify_lessons.py --saved-only
```

範囲とBlenderの場所を変える場合：

```bash
python3 scripts/verify_lessons.py --start 37 --end 40 --blender /Applications/Blender.app/Contents/MacOS/Blender
```

生成時は各回の固有検査と保存処理を実行します。再読み込み時はObject名、型、データ参照名、Meshの頂点・面数、Cameraを照合します。29・33・34・40では、フレーム1と24の評価後座標を比べ、アニメーションが保存後も動くことを確認します。10〜40のデータ検査はBlender 5.2.2 LTSで確認済み（2026-10-02）。41も同じ環境で確認済み（2026-10-13）。42〜101はCameraとJSONを使わないため、この一括確認の範囲外です。各 `lesson.py` を背景実行して確認します（2026-10-15）。各回のGUI練習と完了条件は別に実施してください。

詳しいログは `output/verification/` に保存され、Gitには含みません。生成に失敗すると、その回で止まり、終了コード1とログの末尾を出します。後続の成功だけで失敗を見落とさないための仕組みです。
