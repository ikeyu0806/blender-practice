# 90｜Soft Body：柔らかい塊が自重で下がる

## このレッスンの目標

ゼリーの元Meshの最小Zはそのままで、Goalを切ったSoft Bodyをフレーム8まで進めると、評価後の最小Zが元より低くなることを確認する。

前提は [84 Cloth](../84_cloth/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Soft Bodyは、頂点をばねでつなぎ、フレームごとに重力で動かす。
- `use_goal`を切ると、頂点が元の位置へ戻ろうとしないので自重が見える。
- 頂点を分割しておかないと、立方体の角だけではつぶれ方が粗い。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/90_soft_body/lesson.py
```

`saved: .../output/90_soft_body.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。保存時のフレームは8。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/90_soft_body/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
SoftBody Collection
└── Prop.Jelly Object（Location Z=1、分割済みの立方体Mesh）
    └── Soft Body Modifier（use_goal=False）
        └── フレーム8の評価後は、元より低い頂点がある
```

## 仕組み

Clothが布の面向けなのに対し、Soft Bodyは体積のある塊の頂点をばねで結ぶ。`use_goal`が有効だと、各頂点が元の座標へ戻ろうとして、落下が小さい。この回はGoalを切り、自重で下がる様子を見る。

入力の立方体は辺を2回分割して、角だけでなく面の内側も動けるようにする。ObjectのLocationはZ=1だが、ログが比べるのはMeshのローカルZ。評価後の最小値が元の最小値より小さければ、形が下へ伸びている。

床のCollisionを足すと、84と85と同じように落下を止められる。この回は床を置かず、下方向の差だけを見る。

## Blender画面で観察する

1. `.blend`を開く。フレーム8で、ゼリーが下へ伸びていることを確認する。
2. **Modifier Properties** の`Squish`を開き、Goalが無効であることを確認する。
3. フレーム1へ戻すと、分割した立方体に近い形へ戻る。
4. ログの`evaluated`が`source min z`より小さいことを照合する。

Modifierメニューの **Apply** は押さない。Applyするとそのフレームのつぶれが元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LAST_FRAME = 8
```

これを`14`にして、実行前に予測する。元の最小Zは変わるか。評価後はさらに低くなるか。

再実行すると、元Meshの最小Zは同じで、評価後の最小Zがさらに小さくなる。確認後は`8`へ戻す。

## 完了条件と次へ

元の最小Zが残り、フレームを進めた評価後だけがより低いことを説明できれば完了。次は [91 Grease Pencil Subdivide](../91_grease_pencil_subdiv/README.md) で、Meshではなくストロークに付くModifierを1つ見る。
