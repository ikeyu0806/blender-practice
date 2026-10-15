# 72｜Hook：1つの角をEmptyで引っ張る

## このレッスンの目標

蓋の元Meshの頂点は動かさず、頂点グループ`Corner`に入った1頂点だけが、Emptyを割り当てたあとの移動量で評価後に持ち上がることを確認する。

前提は [71 Displace](../71_displace/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Hookは、頂点グループで選んだ頂点を別Objectの変形に追従させる。
- 追従するのは、HookへObjectを割り当てた時点からの移動の差。
- 元Meshの座標は残るので、Emptyを戻せば評価後の角も戻る。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/72_hook/lesson.py
```

`saved: .../output/72_hook.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/72_hook/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Hook Collection
├── Lid.Pull Empty（割り当て後にZ=1.5）
└── Chest.Lid Object → 立方体Mesh
    ├── Vertex Group Corner（頂点1つだけ1）
    └── Hook Modifier → Lid.Pull
        └── 評価後のその頂点だけが持ち上がる
```

## 仕組み

一部の頂点だけを制御用のEmptyへ預けたいときにHookを使う。頂点グループのウェイト1の頂点が追従し、0の頂点は元の位置に残る。

Emptyを最初から高い位置に置いてからModifierへ渡すと、その位置が基準になり、見た目は動かない。スクリプトは原点で割り当ててから`PULL_Z`だけ上げる。ログの評価後Zは、保存された頂点Zより大きい。

親子関係でObject全体を動かすのとは違い、HookはMeshの一部の評価後座標だけを動かす。ObjectのLocationは蓋の基準位置のまま。

## Blender画面で観察する

1. `.blend`を開き、持ち上がった角とEmptyを **View → Frame All** で見る。
2. **Modifier Properties** の`PullCorner`でObjectが`Lid.Pull`、Vertex Groupが`Corner`であることを確認する。
3. **Show in Viewport** を切ると、角が立方体の位置へ戻る。
4. ログの`evaluated z`が`stored z`より大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると引っ張った位置が元Meshの頂点になる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
PULL_Z = 1.5
```

これを`0.4`にして、実行前に予測する。元の頂点Zは変わるか。評価後の持ち上がりは小さくなるか。

再実行すると、元Meshの頂点は同じで、評価後のZの増加が小さくなる。確認後は`1.5`へ戻す。

## 完了条件と次へ

元の頂点座標が残り、評価後の1頂点だけがEmptyの移動に追従することを説明できれば完了。次は [73 Laplacian Deform](../73_laplacian_deform/README.md) で、固定した点の間の表面を保ったまま曲げる。
