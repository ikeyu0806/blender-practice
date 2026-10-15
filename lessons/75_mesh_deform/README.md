# 75｜Mesh Deform：粗い檻の変形を中の体へ伝える

## このレッスンの目標

体の元Meshは一辺2mの立方体のまま、それを包む一辺3mの檻をBindしたあと上へ伸ばすと、体の評価後の最大Zが元より高くなることを確認する。

前提は [74 Lattice](../74_lattice/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Mesh Deformは、別Meshを檻にして、その頂点の移動を中の評価後へ伝える。
- 使う前にBindが必要。檻は対象を包む大きさにする。
- 体の元頂点は編集せず、動かすのは檻のMesh。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/75_mesh_deform/lesson.py
```

`saved: .../output/75_mesh_deform.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/75_mesh_deform/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
MeshDeform Collection
├── Body.Cage Object → 一辺3mの立方体Mesh（上側を後から上げる）
└── Body.Core Object → 一辺2mの立方体Mesh
    └── Mesh Deform Modifier（Bind済み）→ Body.Cage
        └── 評価後の最大Zが元より高い
```

## 仕組み

Latticeが規則的な格子なのに対し、Mesh Deformは任意の閉じたMeshを檻にできる。低ポリの檻を直せば、中の細かい体の評価後がまとめて曲がる。

Bindは体Objectをアクティブにして実行する。檻が体より小さいと結合に失敗するか、影響が偏る。この回は檻を3m、体を2mにして包む。Bindのあとで檻の上側頂点のZを1m上げる。体の元の最大Zは1mのままで、評価後はそれより高くなる。

`precision`は結合の精度。高いほど重い。この回は5で、上方向の差が見えることを優先する。

## Blender画面で観察する

1. `.blend`を開き、内側の体と外側の檻を **View → Frame All** で見る。
2. `Body.Core`の **Modifier Properties** で`FollowCage`がBind済みであることを確認する。
3. **Show in Viewport** を切ると、体が元の立方体に戻る。檻の上は伸びたまま。
4. ログの`evaluated`が`source max z`より大きいことを照合する。

Modifierメニューの **Apply** は押さない。Applyすると伸びた体の頂点が元Meshになる。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
LIFT_Z = 1.0
```

これを`0.4`にして、実行前に予測する。体の元の最大Zは変わるか。評価後の増加は小さくなるか。

再実行すると、体の元Meshは立方体のままで、評価後の最大Zの増加が小さくなる。確認後は`1.0`へ戻す。

## 完了条件と次へ

体の元頂点が残り、檻の上側の移動だけが評価後の高さに出ることを説明できれば完了。次は [76 Shrinkwrap](../76_shrinkwrap/README.md) で、布を体の表面へ貼り付ける。
