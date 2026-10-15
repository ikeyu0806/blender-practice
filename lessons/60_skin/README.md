# 60｜Skin：枝の辺に太さを付けて体積にする

## このレッスンの目標

腕に見立てた3頂点の折線は元Meshのまま、Skinの半径から評価後に面を持つ体積になることを確認する。

前提は [59 Screw](../59_screw/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Skinは辺だけのMeshに、頂点ごとの半径で断面を付けて評価後の体積を作る。
- 半径はModifier追加後にできるSkin頂点データへ書く。
- 根元の頂点には`use_root`を付け、枝の起点を決める。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/60_skin/lesson.py
```

`saved: .../output/60_skin.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/60_skin/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Skin Collection
└── Arm.Branch Object → 3頂点・2辺の折線Mesh
    ├── Skin頂点データ（半径と、先頭頂点のroot）
    └── Skin Modifier
        └── 評価後は面を持つ体積
```

## 仕組み

関節の位置だけを先に打ち、太さは後から決めたいときにSkinを使う。入力は面ではなく辺。各頂点の`radius`が、その位置の断面の半径になる。XとYで楕円にできるが、この回は両方0.12で円に近い断面にする。

Skin頂点レイヤーは、Skin ModifierをObjectへ追加したときにMeshへ作られる。Modifierより先に半径を書こうとしても、保存場所がまだ無い。ルート頂点は枝分かれの起点で、この回は肩側の1点をrootにする。

評価後の面は、半径と辺のつながりから生成される。元の3頂点をEdit Modeで動かすと、体積の中心線が追従する。

## Blender画面で観察する

1. `.blend`を開き、腕の体積を **View → Frame All** で見る。
2. **Modifier Properties** に`LimbVolume`があることを確認する。
3. **Show in Viewport** を切ると、中心の折線だけになる。
4. Edit Modeで頂点が3つであることを確認する。
5. ログの元頂点が3、評価後に面があることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると体積の頂点が元Meshになり、中心線3点の編集には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SKIN_RADIUS = 0.12
```

これを`0.28`にして、実行前に予測する。元の3頂点は変わるか。評価後の太さは増えるか。

再実行すると、折線は3頂点のままで、断面が太く見える。確認後は`0.12`へ戻す。

## 完了条件と次へ

元の折線が3頂点のまま、評価後だけ半径のある体積になっていることを説明できれば完了。次は [61 Solidify](../61_solidify/README.md) で、布の面に厚みを付ける。
