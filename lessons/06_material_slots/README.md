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
2. 上部の頂点・辺・面の3アイコンから、右端の **Face Select** をクリックする。
3. Material Propertiesで`Material.Metal`のslotを選ぶ。
4. slot一覧の下に出る **Select** をクリックする。上面と下面が選択される。
5. `Material.Wood`のslotを選び、同じく **Select** をクリックする。側面4枚も選択される。
6. 3Dビューポート左上の **Edit Mode** メニューから **Object Mode**へ戻る。

**Select**は「このslotをすでに使っているFaceを選ぶ」操作。**Assign**は「現在選択中のFaceに、このslot番号を設定する」操作。名前が似ているが向きが逆になる。

## コードでの対応

Materialをslotへ追加する順番が、そのままslot番号になる。

```python
material_slot_mesh.materials.append(wood_material)   # slot[0]
material_slot_mesh.materials.append(metal_material)  # slot[1]
```

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

Material Propertiesで2つのslotを確認し、Edit Modeの**Select**で各slotを使うFaceを見分け、`material_index`との対応を説明できれば完了。次はロードマップの **Modifierの評価** で、元のMeshと表示結果の違いを調べる。
