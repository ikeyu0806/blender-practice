# 05｜マテリアルの入口：色・金属感・粗さを比べる

## このレッスンの目標

同じ形の球を4個並べ、Principled BSDFの **Base Color、Metallic、Roughness** を1項目ずつ変える。形を作るMesh、Sceneへ置くObject、表面の見え方を決めるMaterialを区別し、Material PreviewとMaterial Propertiesで違いを観察する。

先に [04 木箱の組み立て](../04_crate_origin/README.md) を学び、ObjectとMeshの違いを確認しておく。Mac版の画面操作やKeymapで迷った場合は、[Blender Mac版：最初に迷わないための画面操作](../../docs/notes/blender-mac-controls.md)も参照する。

完了時には、次を自分の言葉で説明できるようにする。

- Materialは表面の見え方を持つデータブロックで、Meshの形やObjectのLocationとは別。
- Base Colorは基本色、Metallicは金属としての反射、Roughnessは反射のぼけ方を主に変える。
- Solid表示ではMaterialの結果が分かりにくく、Material PreviewまたはRendered表示で観察する必要がある。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/05_material_basics/lesson.py
```

`saved: .../output/05_material_basics.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/05_material_basics/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化するため、Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 画面とデータの対応

```text
MaterialSamples Collection
├── Sample.Baseline Object
│   └── Sample.Baseline.Mesh ── Material.Baseline
├── Sample.ColorBlue Object
│   └── Sample.ColorBlue.Mesh ── Material.ColorBlue
├── Sample.RoughnessLow Object
│   └── Sample.RoughnessLow.Mesh ── Material.RoughnessLow
└── Sample.MetallicHigh Object
    └── Sample.MetallicHigh.Mesh ── Material.MetallicHigh
```

このレッスンではMaterialの違いだけを追いやすくするため、4つのObjectはそれぞれ別のMeshと別のMaterialを持つ。レッスン04のような共有Meshではない。

| 左から | Base Color | Metallic | Roughness | Baselineとの差 |
|---|---|---:|---:|---|
| `Sample.Baseline` | 赤 | 0.0 | 0.45 | 比較基準 |
| `Sample.ColorBlue` | 青 | 0.0 | 0.45 | Base Colorだけ変更 |
| `Sample.RoughnessLow` | 赤 | 0.0 | 0.08 | Roughnessだけ変更 |
| `Sample.MetallicHigh` | 赤 | 1.0 | 0.45 | Metallicだけ変更 |

## Material Previewで観察する

1. `.blend`を開いたら、3Dビューポート上部の **View → Frame All** で4個の球を画面へ収める。
2. 3Dビューポート右上にあるViewport Shadingのアイコンへマウスを重ね、ツールチップが **Material Preview** と表示される球のアイコンをクリックする。Solidのままでは色や反射の差を正しく比較しにくい。
3. Outlinerまたは3Dビューポートで`Sample.Baseline`を選ぶ。
4. 右下のProperties Editorで赤い球の **Material Properties** タブを開く。
5. **Surface → Principled BSDF** のBase Color、Metallic、Roughnessを確認する。
6. 残り3個も順番に選び、値と見え方を表と照らし合わせる。

Material Previewはスタジオ用の環境画像から光を受けるため、Roughnessが低い球ではハイライトや周囲の映り込みが比較的くっきり見える。Roughnessが高いほど反射は広くぼける。Metallicを1にした球は、同じBase Colorでも非金属とは異なる反射になる。見る角度や環境画像でも印象は変わるため、「明るい・暗い」だけでなく反射の形を見る。

## Material、Shader、Principled BSDFの関係

MaterialはObject表面の見え方をまとめるデータブロック。このレッスンでは各MeshのMaterial slotへ1つずつ割り当てる。Materialの中ではノードが接続され、Principled BSDFノードが光に対する表面の反応を計算する。

```text
Object ── data ── Mesh ── material slot ── Material
                                              └── Principled BSDF
                                                  ├── Base Color
                                                  ├── Metallic
                                                  └── Roughness
```

- **Base Color:** 表面の基本色。単なる画面上の塗りつぶしではなく、反射計算にも使われる。
- **Metallic:** `0`は非金属、`1`は金属として扱う。この回は差を明確にするため両端を使う。
- **Roughness:** `0`へ近いほど反射が鋭く、`1`へ近いほど広くぼける。

テクスチャ画像やUVはまだ使わない。まず1色と数値だけでMaterialの役割を分離して観察する。

## 理解メモ：MeshからMaterialは`has_many`？

Rails風に表すなら、`Mesh has_many :material_slots`はかなり近い。ただし、MeshがMaterialそのものを所有するのではなく、**順番付きのMaterial slotがMaterialデータブロックを参照する**。

```text
Mesh
├── material_slots[0] ──参照──> Material.A
└── material_slots[1] ──参照──> Material.B

Meshの各Face
└── material_index = 0 または 1
    └── どのMaterial slotを使うかを選ぶ
```

関係をRails風に分解すると、次のイメージになる。

- `Mesh has_many :material_slots`
- `MaterialSlot belongs_to :material`
- 1つのMaterialは複数のMeshのslotから再利用できる

そのため、MeshとMaterial全体の関係は、slotを間に置いた**多対多に近い**。ただしこれは理解のためのたとえであり、Blender内部にRailsの関連があるわけではない。

このレッスンの`sample_mesh.materials.append(sample_material)`は、MeshへMaterial slotを1つ追加し、そのslotからMaterialを参照させている。Faceは最初のslotを使うため、`material_index`は`0`になる。

スクリーンショットの`Sample.MetallicHigh.Mesh`には、教材が作った`Material.MetallicHigh`に加えて、`Material`という2つ目のslotが増えている。下の一覧で`Material`を選択しても、**設定欄で表示するMaterialを切り替えただけ**で、Faceへの割り当ては自動では変わらない。教材のMetallic値を確認するには、一覧の`Material.MetallicHigh`を選ぶ。そこではMetallicが`1.0`、Roughnessが`0.45`になっている。

教材を元の状態へ戻す場合は、追加した`Material`のslotを選んでMaterial slotの削除ボタンを押すか、レッスンのスクリプトを再実行して出力を作り直す。

## スクリプトの流れ

1. Sceneを初期化し、`MaterialSamples` Collectionを作る。
2. `MATERIAL_SAMPLES`に、Object名、Mesh名、Material名、位置、3つの比較値を定義する。
3. `make_material()`でMaterialとPrincipled BSDFの値を作る。
4. `make_sample_mesh()`で反射を見やすい球Meshを作り、Material slotへMaterialを追加する。
5. Objectを作ってCollectionへ所属させ、横一列に配置する。
6. Object・Mesh・Material名と設定値をログへ出し、関係と数値を検査して`.blend`を保存する。

## 変更実験

`MATERIAL_SAMPLES`内の`Sample.RoughnessLow`だけを変更する。

```python
"roughness": 0.08,
```

これを`0.8`に変える前に、ハイライトや映り込みがどう変わるか予測する。スクリプトを再実行し、Material PreviewでBaselineと比較する。確認後は`0.08`へ戻す。

変更するのはRoughnessだけ。Base ColorとMetallicを同時に変えると、どの値が結果の原因か判断しにくくなる。

## よく混同する点

| 疑問 | 答え |
|---|---|
| Base Colorを変えるとMeshの形も変わる？ | 変わらない。Materialの見え方だけが変わる。 |
| ObjectのLocationを変えるとMaterialも変わる？ | Material値は変わらない。ただし環境光を受ける角度や位置で見え方が変化する場合はある。 |
| Solid表示で赤や青が見えないのは設定失敗？ | Material Previewへ切り替えて確認する。Solid表示はMaterialのシェーダー結果を観察する表示ではない。 |
| Metallicを1にすれば必ず銀色になる？ | ならない。Base Colorが金属の反射色に影響する。この教材の金属サンプルは赤い金属として見える。 |
| Roughnessが低いほど明るくなる？ | 単純な明るさではなく、主に反射が鋭くなる。環境や見る角度で明暗は変わる。 |
| Material slotを選べば、そのMaterialがFaceへ割り当てられる？ | 選択だけでは設定欄の表示対象が変わる。複数slotを使い分ける場合は、Edit ModeでFaceを選び、使うslotを選んで**Assign**する。 |

## 完了条件と次へ

4サンプルについて、どの値だけがBaselineと違うかをMaterial Propertiesで確認し、Object、Mesh、Materialの役割を説明できれば完了。次は [06 Material Slot](../06_material_slots/README.md)で、1つのMeshに複数のMaterialを登録し、Faceごとに使い分ける。
