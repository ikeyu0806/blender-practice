# 06｜Material Slot：1つのMeshで面ごとに色を分ける

## このレッスンの目標

1つの直方体Meshへ2つのMaterialを登録し、側面と上下面で使い分ける。MeshがMaterialを直接たくさん所有するのではなく、**Material slotがMaterialを参照し、各Faceの`material_index`がslot番号を選ぶ**ことを理解する。

先に [05 マテリアルの入口](../05_material_basics/README.md) を終え、Material PropertiesでBase Color、Metallic、Roughnessを確認できる状態を想定する。Mac版の画面操作やショートカットで迷った場合は、[Blender Mac版：最初に迷わないための画面操作](../../docs/notes/blender-mac-controls.md)も参照する。

完了時には、次を自分の言葉で説明できるようにする。

- Material Propertiesの一覧は、Meshが持つ順番付きのMaterial slot。
- Material slotをクリックするだけでは、選択したFaceへの割り当ては変わらない。
- 各Faceは`material_index`で使用するslotを選ぶ。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/06_material_slots/lesson.py
```

`saved: .../output/06_material_slots.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/06_material_slots/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化するため、Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
MaterialSlotsLesson Collection
└── Sample.MaterialSlots Object
    └── Sample.MaterialSlots.Mesh
        ├── material slot[0] ──> Material.Wood
        └── material slot[1] ──> Material.Metal

各Face
└── material_index = 0 または 1
    └── 使用するMaterial slotを選ぶ
```

Rails風の比喩では、`Mesh has_many :material_slots`、`MaterialSlot belongs_to :material`に近い。Materialは別のデータブロックであり、別Meshのslotからも参照できるため、Meshに所有されて一緒に消える子データという意味ではない。

Collection、Object、Mesh、Faceまで含めた関係は、[Rails風ER図で理解するObject・Mesh・Face・Material Slot・Material](../../docs/notes/mesh-material-slots-er.md)で確認できる。

## Material Propertiesで2つのslotを見る

1. `.blend`を開き、Outlinerで`Sample.MaterialSlots`を選ぶ。
2. 3Dビューポート右上の **Material Preview** をクリックする。直方体の側面は茶色、上下面は青い金属色になる。
3. Properties Editorの赤い球アイコン **Material Properties** を開く。
4. 一覧に`Material.Wood`と`Material.Metal`の2行があることを確認する。
5. 各行をクリックし、下のSurface設定が切り替わることを確認する。

ここで行をクリックする操作は、**設定欄で見るMaterialを選んだだけ**。Faceに使うMaterialはまだ変更していない。

## Edit ModeでFaceとslotの対応を見る

ショートカットは、マウスポインターがあるEditorへ作用する。最初に3Dビューポート内を1回クリックする。

1. 3Dビューポート左上の **Object Mode** メニューから **Edit Mode** を選ぶ。`Tab`キーでも切り替えられるが、反応しない場合はメニューを使う。
2. 上部の頂点・辺・面の3アイコンから、右端の塗りつぶされた四角形 **Face Select** を**普通に1回クリック**する。青い背景になればFace Selectは有効。スクリーンショットはすでにこの状態になっている。
3. `Shift`や`Ctrl`は押さない。ツールチップの`Shift-Click`は頂点・辺・面の選択モードを同時に有効にする操作、`Ctrl-Click`は選択要素を広げながらモードを変える操作で、この観察には不要。
4. 右側のProperties Editorで、縦に並んだタブから赤い球の **Material Properties** をクリックする。
5. Material slot一覧の`Material.Metal`を普通に1回クリックする。これはslotを操作対象にしただけで、Faceはまだ選択されない。
6. 3Dビューポート上部の **Select → None** をクリックし、いったんすべてのFaceを非選択にする。ショートカットを使う必要はない。
7. Material Propertiesへ戻り、slot一覧の下にある **Select** をクリックする。`Material.Metal`を使用中の上面がオレンジ色で選択される。下面も選択されているが、現在の角度では箱の裏に隠れている。
8. 違いを見やすくするため、もう一度3Dビューポートの **Select → None** ですべて非選択にする。
9. Material Propertiesで`Material.Wood`を普通に1回クリックし、その下の **Select** をクリックする。今度は木材slotを使用中の側面4枚が選択される。裏側の面は現在の角度では見えない。
10. 観察が終わったら、3Dビューポート左上の **Edit Mode** メニューから **Object Mode**へ戻る。

**Select**は「このslotをすでに使っているFaceを選ぶ」操作。**Assign**は「現在選択中のFaceに、このslot番号を設定する」操作。名前が似ているが向きが逆になる。

### マウスでFaceを1枚選んでAssignする場合

こちらも`Ctrl`クリックは使わない。

1. Edit ModeとFace Selectのまま、3Dビューポートの **Select → None** ですべて非選択にする。
2. 直方体の上面の中央を普通に1回クリックする。上面がオレンジ色になれば選択できている。複数のFaceを追加選択するときだけ`Shift`を押しながらクリックする。
3. Material Propertiesで`Material.Wood`のslotをクリックする。
4. slot一覧の下の **Assign** をクリックする。選択中の上面の`material_index`が`0`になり、上面が木材色へ変わる。
5. 元へ戻すには、上面を選択したまま`Material.Metal`のslotをクリックし、**Assign**をクリックする。

操作の役割を分けると、次の順番になる。

```text
Face Selectアイコンをクリック
└── 面を選べるモードにする

3DビューポートでFaceをクリック
└── 操作対象の面を選ぶ

Material slotの行をクリック
└── 操作対象のslotを選ぶ

Assignをクリック
└── 選択中のFaceへslot番号を設定する
```

## コードでの対応

### `make_material_slot_mesh()`の読み方

この関数は、ObjectやMaterialではなく、直方体の**Meshデータブロックだけ**を作る。

1. `vertex_coordinates`へ8個の座標を順番に並べる。並び順が`Vertex.index`の`0`〜`7`になる。
2. `FACE_DEFINITIONS`の各要素から、Faceを囲む頂点番号だけを`face_vertex_indices`へ取り出す。Face名とMaterial slot番号は、この時点ではまだ使わない。
3. `bpy.data.meshes.new(mesh_name)`で、中身が空のMeshデータブロックを作る。
4. `from_pydata(vertex_coordinates, [], face_vertex_indices)`で、頂点・辺・面を作る。
5. `update()`で追加した形状データをMesh内部へ反映し、そのMeshを返す。

`from_pydata()`の3引数は次の意味になる。

```text
from_pydata(
    頂点の座標,          # vertex_coordinates
    独立指定する辺,      # []：今回はFaceの輪郭から作られる
    面ごとの頂点番号,    # face_vertex_indices
)
```

この関数を抜けた時点では、MeshはまだSceneに表示されない。`main()`でMaterial slotを追加し、`bpy.data.objects.new()`でMeshを参照するObjectを作り、そのObjectをCollectionへ所属させて初めて画面に現れる。

`FACE_DEFINITIONS`には`(Face名, 頂点番号, Material slot番号)`が入っている。形の生成では頂点番号だけを使い、後の処理で同じ並びを使って各Faceへ`material_index`を設定する。1つの定義を「形を作る処理」と「Materialを割り当てる処理」の両方で使うことで、Faceの順番がずれないようにしている。

Materialをslotへ追加する順番が、そのままslot番号になる。

```python
material_slot_mesh.materials.append(wood_material)   # slot[0]
material_slot_mesh.materials.append(metal_material)  # slot[1]
```

2つのslotを作るのは、**同じMeshの側面と上下面で、別々のMaterialを選べるようにするため**。`make_material()`でMaterialデータブロックを2つ作っただけでは、そのMeshが使用できるMaterial候補にはならない。`materials.append()`でMeshの一覧へ参照を登録する必要がある。

```text
Mesh.materials
├── slot[0] → 既存のwood_materialを参照
└── slot[1] → 既存のmetal_materialを参照
```

`append()`はMaterialのコピーを作る処理ではない。既存のMaterialへの参照を、Meshのslotへ順番に追加する処理。slotが1つしかなければ、すべてのFaceはその1種類しか選べない。slotが2つあるため、各Faceの`material_index`を`0`または`1`にして使い分けられる。

各FaceはMaterialへの直接参照ではなく、整数の`material_index`を持つ。

```python
polygon.material_index = material_index
```

このレッスンでは側面4枚が`0`、上下面が`1`。ログにもFace名、`material_index`、参照先Materialが表示される。

## 変更実験

`lesson.py`の`FACE_DEFINITIONS`で、Topのslot指定だけを変更する。

```python
("Top", (4, 5, 6, 7), METAL_SLOT_INDEX),
```

この行の`METAL_SLOT_INDEX`を`WOOD_SLOT_INDEX`へ変える。実行前に、どのFaceの見た目が変わるか予測してから再実行する。

上面だけが青い金属色から茶色へ変わる。Materialもslotの並びも変更せず、上面の`material_index`だけが`1`から`0`へ変わった結果。

実験後は`METAL_SLOT_INDEX`へ戻す。

## よく混同する点

| 疑問 | 答え |
|---|---|
| MeshがMaterialを`has_many`している？ | `Mesh has_many :material_slots`は近い。slotがMaterialを参照し、Faceがslot番号を選ぶ。 |
| slot一覧でMaterialを選べば見た目も変わる？ | 選択だけでは設定欄の表示対象が変わる。Faceへの変更にはEdit Modeの**Assign**を使う。 |
| 1つのFaceで2つのslotを同時に使える？ | 1つのFaceの`material_index`は1個なので、この方法では1つのslotを選ぶ。Shader内で混ぜる方法は別の仕組み。 |
| ObjectのLocationを変えると割り当ても変わる？ | 変わらない。LocationはObjectのTransform、slotと`material_index`はMesh側のデータ。 |
| Materialを別Meshでも使える？ | 使える。別MeshのMaterial slotから同じMaterialデータブロックを参照できる。 |

## 完了条件と次へ

Material Propertiesで2つのslotを確認し、Edit Modeの**Select**で各slotを使うFaceを見分け、`material_index`との対応を説明できれば完了。次は [07 Modifierの評価](../07_modifier_evaluation/README.md) で、元のMeshと表示結果の違いを調べる。
