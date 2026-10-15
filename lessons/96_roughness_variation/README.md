# 96｜1つの物の中でRoughnessを分ける

## このレッスンの目標

1つの木箱に、胴体と縁で違うRoughnessのMaterialを割り当てる。全面が1つの値ではないことを確認する。

前提は [95 ポリゴン予算](../95_polygon_budget/README.md)。Roughnessそのものは [05 マテリアルの入口](../05_material_basics/README.md)、面への割り当ては [06 Material Slot](../06_material_slots/README.md)。この回は他のレッスンの出力ファイルを必要としない。

完了時には、次を自分の言葉で説明できるようにする。

- 全面が同じRoughnessだと、プラスチックのように均一な反射になる。
- 縁だけ値を下げると、擦れた角や別の仕上げとして読める。
- 色を変えなくても、Roughnessの差だけで面の役割が分かれる。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/96_roughness_variation/lesson.py
```

`saved: .../output/96_roughness_variation.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/96_roughness_variation/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
RoughnessVariation Collection
└── Crate.Worn Object → Crate.Worn.Mesh
    ├── Material Slot 0 → Material.Body（Roughness 0.75）
    └── Material Slot 1 → Material.Edge（Roughness 0.15）
```

## 仕組み

Principled BSDFのRoughnessは、反射が点に集まるか、広くぼけるかを決める。レッスン05は球を並べて値の意味を見た。この回は1つの木箱の中で、広い面と角の細い面に別の値を置く。角の面はMeshに書き込んだ細い帯で、Bevel Modifierの評価結果ではない。

面積が1より大きい面を胴体、それ以下を縁にしている。ログの`faces`が両方とも1以上なら、1つのMeshに2つのRoughnessがある。

## Blender画面で観察する

1. `.blend`を開き、木箱を **View → Frame Selected** で収める。
2. ビューポートを **Material Preview** にする。縁の帯は反射が鋭く、広い面はぼやけて見える。
3. Material Propertiesで`Material.Body`のRoughnessが0.75、`Material.Edge`が0.15であることを確認する。
4. ログの`body faces`と`edge faces`がどちらも1以上であることを照合する。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
EDGE_ROUGHNESS = 0.15
```

これを`0.05`にして、実行前に予測する。縁の面の数は変わるか。胴体の0.75は変わるか。

再実行すると、面の数と胴体の値はそのままで、縁のRoughnessだけが下がる。確認後は`0.15`へ戻す。

## 完了条件と次へ

1つの物の中のRoughnessの差が、均一なプラスチックとの違いになることを説明できれば完了。次は [97 Bumpと実際の凹凸](../97_bump_vs_geometry/README.md) で、法線だけの凹凸と頂点の移動を分ける。
