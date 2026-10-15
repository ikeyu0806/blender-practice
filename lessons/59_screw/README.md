# 59｜Screw：断面を回して器の側面を作る

## このレッスンの目標

壺の断面は3頂点の折線のまま、ScrewがZ軸の周りに回した評価後には側面の面ができることを確認する。

前提は [58 Remesh](../58_remesh/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Screwは断面の辺を、選んだ軸の周りに回して評価後の面を作る。
- `steps`はその回転を何枚の面で近似するか。
- `screw_offset`を0以外にすると、回転しながら軸方向へ進む螺旋になる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/59_screw/lesson.py
```

`saved: .../output/59_screw.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/59_screw/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
Screw Collection
└── Vase.Profile Object → 3頂点・2辺の断面Mesh
    └── Screw Modifier（軸Z、360度、steps=8、offset=0）
        └── 評価後に器の側面
```

## 仕組み

杯、角、柱の断面は、正面から見た折線として作ると修正しやすい。Screwはその折線を軸の周りに配って側面にする。この回の断面は軸から離れたX側にあり、Zへ3点でくびれを持つ。360度回すと一周の器になる。

`steps`が8なら、円周を8分割した側面になる。角ばって見えるのは分割が粗いためで、断面の頂点数とは別。`screw_offset`が0なので、回転しても高さが断面の範囲を超えない。値を入れると、階段の手すりのような螺旋になる。

Edit Modeで断面のXを変えると、器の半径が変わる。評価後の側面を直接編集しているわけではない。

## Blender画面で観察する

1. `.blend`を開き、器を斜め上から **View → Frame All** で見る。
2. **Modifier Properties** の`Lathe`でAxisがZ、Angleが360度、Stepsが8であることを確認する。
3. **Show in Viewport** を切ると、断面の折線だけになる。
4. ログの元頂点が3、評価後の頂点と面がそれより多いことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると側面の頂点が元Meshになり、断面1本の編集には戻せない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
SCREW_STEPS = 8
```

これを`4`にして、実行前に予測する。断面の3頂点は変わるか。側面はより角ばって、評価後の頂点は減るか。

再実行すると、断面は3頂点のままで、評価後の頂点と面が8のときより少なくなる。確認後は`8`へ戻す。

## 完了条件と次へ

断面の3頂点が残り、評価後だけ回転した側面になっていることを説明できれば完了。次は [60 Skin](../60_skin/README.md) で、枝の辺に太さを付けて腕のような体積を作る。
