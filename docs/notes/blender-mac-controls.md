# Blender Mac版：最初に迷わないための画面操作

Blender 5.2.2 LTS の macOS 版で、レッスンの `.blend` を観察するときに必要な操作をまとめる。ショートカットが反応しないときは、キーを何度も押す前に **Keymap** と **マウスポインターの位置**を確認する。

## 最初に知るべき結論

Blender には標準の **Blender** Keymap と **Industry Compatible** Keymap があり、同じキーでも動作が違う。

| 操作 | Blender Keymap | Industry Compatible |
|---|---|---|
| 全選択 | `A` | `Control + A` |
| 選択解除 | `Option + A` または `A` を素早く2回 | `Shift + Control + A` |
| 選択物へ表示を寄せる | テンキーの `.` | `F` |
| 全体を画面に収める | `Home` | `A` |
| Edit Modeを切り替える | `Tab` | 画面左上のModeメニュー、または `5` のMode Pie |
| Object Modeへ戻る | `Tab` | 画面左上のModeメニュー、または `4` |
| つながった形状を選ぶ | 対象にマウスを重ねて `L` | 頂点などを1つ選んで `Control + L` |

`A` で全選択されず、代わりにシーン全体が画面へ収まる場合は **Industry Compatible** を使っている可能性が高い。`Tab` もこのKeymapではMode切り替えではなくMenu Searchなので、Object Modeには戻らない。

この教材とBlender公式マニュアルは、特記がなければ標準の **Blender Keymap** を前提にする。初学者には標準へそろえることを推奨する。

## Keymapを確認・変更する

1. Blender上部の **Edit → Preferences...** を開く。
2. 左側で **Keymap** を選ぶ。
3. 画面上部の **Keymap Presets** を確認する。
4. この教材どおりに操作するなら **Blender** を選ぶ。
5. Preferencesを閉じる。通常は設定が自動保存される。

設定を変えたくない場合は、上の表の **Industry Compatible** 側を使う。どちらが優れているというより、説明と実際の設定をそろえることが重要。

## ショートカットはマウスポインターのある領域に効く

Blenderのウィンドウは、役割の違う複数の領域に分かれている。

- **3D Viewport:** モデルが見える大きな3D画面
- **Outliner:** 右上にあるScene Collection、Object、Meshの一覧
- **Properties Editor:** 右下にある各種設定
- **Timeline:** 画面下部にあるフレームの目盛り

多くのショートカットは、**マウスポインターを置いた領域**によって意味が変わる。Outlinerにマウスを置いたまま `A` を押すとOutliner内の項目が対象になり、3D Viewportの頂点は選択されない。モデルを操作するときは、まずマウスポインターを3D Viewportへ移してからキーを押す。

クリックしなくても、マウスポインターを移すだけで対象領域が決まる操作が多い。クリックする場合は、意図せず選択を変えないよう何もない背景部分を使う。

## Modeから戻れないときの確実な復帰方法

ショートカットが分からなくなったら、画面に見えるModeメニューを使う。

1. 3D Viewportの左上を見る。
2. **Edit Mode** など現在のMode名が表示されたプルダウンをクリックする。
3. **Object Mode** を選ぶ。

Modeメニューが使えない場合は、まず `Esc` を押して進行中の移動・回転などをキャンセルする。次にOutlinerで、緑の三角の `CrateBoards` ではなく、オレンジの三角が付いた `Crate.A` の行を選び直す。

## Object ModeとEdit Modeの見分け方

- **Object Mode:** 木箱全体を1つのObjectとして選択・移動する。選択したObjectの外形がオレンジになる。
- **Edit Mode:** Mesh内部の頂点・辺・面を選択・編集する。角の小さな点が頂点、点をつなぐ線が辺、囲まれた領域が面。
- Edit Modeで未選択の頂点は黒、選択した頂点はオレンジ、最後に選んだ頂点は白で表示される。
- 3D Viewport左上にある点・線・四角の3ボタンで、Vertex・Edge・Faceの選択モードを切り替える。

## lesson4の木箱を観察する

ショートカットを避ける場合は、次の画面操作だけで確認できる。

1. Outlinerでオレンジの三角が付いた `Crate.A` の行を選ぶ。
2. 3D Viewport左上の **Object Mode** をクリックし、**Edit Mode** を選ぶ。
3. 3D Viewport上部の **Select → All** で全頂点を選ぶ。
4. **View → Frame Selected** で木箱へ表示を寄せる。
5. **Select → None** で選択を解除する。
6. 左上のVertex Select（点のボタン）が有効な状態で、板の角の頂点を1つクリックする。
7. **Select → Select Linked → Linked** を選ぶ。その板につながる8頂点・12辺・6面だけが選択される。

底板1枚と側板4枚で同じ操作を試すと、`CrateBoards` は1つのMeshだが、その中に連結していない板形状が5つあると確認できる。

## 困ったときの確認順

1. ファイルを保存していない作業中なら、まず別名保存する。
2. `Esc` で途中の操作をキャンセルする。
3. 3D Viewport左上で現在のModeを見る。
4. Modeは左上のプルダウンから戻す。
5. ショートカットを使う前に、マウスポインターを3D Viewportへ置く。
6. `A` や `Tab` の動作が説明と違えば、PreferencesのKeymap Presetを確認する。
7. 分からない操作は、まず3D Viewport上部の **View**、**Select**、**Mesh** メニューから探す。メニューなら操作名と現在使える項目を画面で確認できる。

## 公式資料

- [Blender Manual: Areas](https://docs.blender.org/manual/en/5.2/interface/window_system/areas.html)
- [Blender Manual: Keymap Preferences](https://docs.blender.org/manual/en/5.2/editors/preferences/keymap.html)
- [Blender Manual: Default Keymap](https://docs.blender.org/manual/en/latest/interface/keymap/blender_default.html)
- [Blender Manual: Industry Compatible Keymap](https://docs.blender.org/manual/en/latest/interface/keymap/industry_compatible.html)

関連: [04 木箱の組み立て](../../lessons/04_crate_origin/README.md)、[スクリプトと画面の関係](script-workflow.md)
