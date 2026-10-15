# 56｜Mirror：右半分から左半分を評価後に作る

## このレッスンの目標

胴体の元MeshはXが0以上の8頂点だけなのに、評価後は原点の左側にも頂点ができ、左右が1つの形になることを確認する。

前提は [55 Mask](../55_mask/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- MirrorはObjectの原点を通る軸の反対側を、評価後だけ作る。
- 元Meshを左にもコピーしているわけではなく、編集するのは右半分だけでよい。
- `use_mirror_merge`は、鏡の面上で重なる頂点を1つにまとめる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/56_mirror/lesson.py
```

`saved: .../output/56_mirror.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/56_mirror/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Mirror Collection
└── Body.RightHalf Object → X≥0の半身Mesh（8頂点）
    └── Mirror Modifier（X軸、中央を結合）
        └── 評価後はXが負の側にも広がり、中央の頂点は共有される
```

## 仕組み

人物や左右対称の小物は、片方だけを編集して反対側を評価で作れる。鏡の位置はObjectの原点を通るローカル軸。この回はX軸なので、原点より右の頂点が左へ映る。半身のXを0より小さく作ってしまうと、鏡像と重なって二重になる。

中央の4頂点はX=0上にある。`use_mirror_merge`が有効だと、元の頂点と鏡像の頂点が同じ位置で1つにまとまり、胴の中心が割れない。無効だと中央が二重になり、評価後の頂点数が増える。

Edit Modeで右の側面を動かすと、左も同じ量だけ追従する。追従しているのは評価結果で、元Meshに左の頂点は無い。

## Blender画面で観察する

1. `.blend`を開き、左右のある胴を **View → Frame All** で収める。正面から見て左右が揃っていることを確認する。
2. **Modifier Properties** の`LeftSide`でAxisのXだけが有効、Mergeが有効であることを確認する。
3. **Show in Viewport** を切ると右半分だけになる。
4. Edit Modeで頂点を選び、Xが負の頂点が元Meshに無いことを確認する。
5. ログの`min x source`が0、`evaluated`が負であることを照合する。

Modifierメニューの **Apply** は押さない。Applyすると左側の頂点が元Meshへ入り、以後は左右を別々に編集することになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
MERGE_CENTER = True
```

これを`False`にして、実行前に予測する。左側はまだできるか。評価後の頂点数は、結合しているときより増えるか。

再実行すると、左側は残り、中央をまとめない分だけ評価後の頂点が増える。確認後は`True`へ戻す。

## 完了条件と次へ

元MeshのXが0以上だけで、評価後に左側ができていることを説明できれば完了。次は [57 Multiresolution](../57_multires/README.md) で、細分化の段数を元Meshと別に持つ。
