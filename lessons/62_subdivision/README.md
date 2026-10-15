# 62｜Subdivision Surface：立方体を評価後だけ滑らかに分割する

## このレッスンの目標

体のブロックに見立てた立方体の元Meshは8頂点のまま、Subdivisionの表示段数2で評価後の頂点が増え、角が丸く見えることを確認する。

前提は [57 Multiresolution](../57_multires/README.md) と [61 Solidify](../61_solidify/README.md)。角を丸めるBevelは [07 Modifierの評価](../07_modifier_evaluation/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Subdivision Surfaceは各面を再分割し、評価後の表面を滑らかに近づける。
- `levels`はビューポート、`render_levels`はレンダーで使う段数。
- 元の8頂点を編集すると、滑らかな評価結果の大きな形が追従する。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/62_subdivision/lesson.py
```

`saved: .../output/62_subdivision.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/62_subdivision/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Subdivision Collection
└── Body.Block Object → 8頂点の立方体Mesh
    └── Subdivision Surface Modifier（levels=2）
        └── 評価後の頂点が8より多い、角の丸い形
```

## 仕組み

少ない頂点で大きな形を決め、表示のときだけ滑らかにしたいときにSubdivisionを使う。Catmull-Clark型の分割は、各段で面を四分割し、頂点位置を隣との平均へ寄せる。段数を上げるほど円に近づき、頂点数も増える。

Multiresolutionと違い、このModifierは段ごとの彫刻変位を保持しない。レベルを変えても元Meshは同じ8頂点。Bevelは角だけを面取りし、Subdivisionは面全体を繰り返し分割する。

`levels`を0にすると評価後は元の立方体に戻る。レンダーだけ段数を上げたいときは`render_levels`を別にできる。この回は両方2にして、背景実行の評価と画面が揃うようにする。

## Blender画面で観察する

1. `.blend`を開き、丸みのあるブロックを **View → Frame All** で見る。
2. **Modifier Properties** の`SmoothBody`でLevelsが2であることを確認する。
3. Levelsを0と2で切り替え、立方体と滑らかな形を比べる。
4. Edit Modeの頂点が8個であることを確認する。
5. ログの`source=8`より`evaluated`が大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると分割後の頂点が元Meshになり、8頂点の編集には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
VIEWPORT_LEVELS = 2
```

これを`1`にして、実行前に予測する。元の8頂点は変わるか。評価後の頂点は2のときより減るか。

再実行すると、元Meshは8頂点のままで、評価後の頂点が2段のときより少なく、角の丸みも弱くなる。確認後は`2`へ戻す。

## 完了条件と次へ

元の8頂点が残り、段数に応じて評価後の頂点と丸みが変わることを説明できれば完了。次は [63 Triangulate](../63_triangulate/README.md) で、四角面を評価後だけ三角形にする。同じ段数でも面の並びで結果が変わることは [92](../92_subsurf_topology/README.md)。
