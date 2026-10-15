# 42｜Data Transfer：別Meshの頂点グループを評価結果へ写す

## このレッスンの目標

左の立方体に保存した`ClothPin`ウェイトを、右の立方体の評価結果だけへ写す。右の元Meshに入っているウェイトは0のままであることを確認する。

前提は [07 Modifierの評価](../07_modifier_evaluation/README.md)。元Meshと評価結果の違い、ModifierがObject側にあることを先に確認する。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Data Transferは形を増やさず、頂点グループなどのデータをObjectの評価結果へ写す。
- 写し先にも、同じ名前の頂点グループが先に要る。
- `TOPOLOGY`は頂点番号で対応するので、2つの立方体の位置が違っても写せる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/42_data_transfer/lesson.py
```

`saved: .../output/42_data_transfer.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/42_data_transfer/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
DataTransfer Collection
├── Weight.Source Object → Weight.Source.Mesh
│   └── Vertex Group ClothPin（上が1、下が0.1）
└── Weight.Dest Object → Weight.Dest.Mesh
    ├── Vertex Group ClothPin（保存値はすべて0）
    └── Data Transfer Modifier → Source Objectを参照
        └── 評価後のClothPinだけ、Sourceの上下が写る
```

## 仕組み

Data Transferは、生成系のModifierのように頂点を増やさない。別Objectから、頂点グループ、UV、法線などのデータを評価結果へ渡す。この回が渡すのは頂点グループ`ClothPin`だけ。

対応のさせ方は`vert_mapping`。`TOPOLOGY`は「0番は0番」という頂点番号の対応なので、同じ立方体を2つ作り、位置だけずらしても写せる。形が違うMeshへ写すときは`NEAREST`のように位置で探す方法を選ぶ。

`mix_factor`は、写し先に元からある値と、写してきた値をどれだけ混ぜるか。1なら評価結果はSource側の値になる。Destの`Object.data`に保存された0は、Applyするまで残る。ログの`dest stored`と`dest evaluated`を見比べる。

## Blender画面で観察する

1. `.blend`を開き、**View → Frame All** で左右の立方体を収める。
2. `Weight.Dest`を選び、Propertiesの緑の逆三角 **Object Data Properties** で`ClothPin`を見る。
3. 同じObjectのレンチアイコン **Modifier Properties** で`CopyPin`のSourceが`Weight.Source`であることを確認する。
4. ターミナルログの`dest stored`がすべて0、`dest evaluated`に1と0.1が混ざることを照合する。
5. Weight Paintへ切り替えると、評価後のウェイトが見える。Edit Modeの元Mesh側は0のままに見える操作と混同しないよう、ログの2行を基準にする。

Modifierメニューの **Apply** は押さない。見出しのモニター形 **Show in Viewport** を切ると評価前の形へ戻り、元データは残る。このModifierは形を変えないので、見た目の輪郭は左右とも立方体のまま。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
MIX_FACTOR = 1.0
```

これを`0.5`にして、実行前に予測する。Destの元Meshは0のままか。評価後の最大値は1より小さくなるか。

再実行すると、保存されたウェイトは0のままで、評価後はSourceの値と0の中間に近づく。確認後は`1.0`へ戻す。

## 完了条件と次へ

Destの元ウェイトが0のまま、評価後だけSourceの上下が写っていることをログで説明できれば完了。次は [43 Normal Edit](../43_normal_edit/README.md) で、頂点は動かさず法線の向きだけを変える。
