# 04｜木箱の組み立て：底面中央を原点にする

## このレッスンの目標

5枚の厚い板を組み合わせた、ふたのない木箱を作る。主題は **Object の原点（Origin）を形状のどこに置くか**。木箱の底面中央を原点にすると、`Location Z=0` で地面に置ける理由を、頂点の高さと画面で確かめる。

先に [01 共有 Mesh](../01_shared_mesh/README.md)、[03 Collection](../03_collection/README.md) を学んでおく。今回の木箱は **5枚の板 = 1つの Mesh = 1つの Object**。板を5つの Object として親 Empty に付ける構成ではない。前回の「複数 Object をまとめて動かす」方法との違いも意識する。

完了時には、次を自分の言葉で説明できるようにする。

- 原点は Object の位置・回転・拡大の基準点で、Mesh の見た目の中心と一致しなくてよい。
- 今回は Mesh の頂点を **ローカル Z=0 より上**に置いたので、木箱 Object の原点は底面中央にある。
- `Crate.A` と `Crate.B` は同じ Mesh を共有するが、Object ごとの `Location` は別々。`Location Z=0` なら両方の底面が地面に接する。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/04_crate_origin/lesson.py
```

`saved: .../output/04_crate_origin.blend` が出てターミナルに戻ったら、Blender アプリの **File → Open...** からその `.blend` を開く。すでに開いている別のBlenderウィンドウには結果が自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/04_crate_origin/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなので、ターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のシーンを初期化するため、Blender の Text Editor から **Run Script** するなら現在の作業を先に保存する。GUI の変更は `lesson.py` に同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## 画面とデータの対応

```text
Scene Collection
├── Crates
│   ├── Crate.A ──┐
│   └── Crate.B ──┴── CrateBoards（共有 Mesh：底板と4枚の側板）
└── Environment
    └── Ground ───── GroundMesh（上面 Z=0 の地面）
```

ビューポートに、ふたのない木箱が左右に1個ずつ、薄い地面の上に見える。Outliner では `Crates` と `Environment` の Collection を分けている。Collection は整理と表示のためで、木箱の原点や位置を決めてはいない。

`Crate.A` を選択し、**Object Properties → Transform → Location** を見ると `X=-1.5, Z=0`。`Crate.B` は `X=1.5, Z=0`。どちらも Object の原点が底面中央なので、木箱の底が地面上面の Z=0 に接する。選択した Object の原点はビューポートの小さな点として確認できる。見づらければ木箱を選択してテンキーの `.` で選択物に寄るか、ビューポートの **View → Frame Selected** を使う。

`Crate.A` を **Edit Mode** にして、底板と側板が頂点・辺・面として1つの Mesh に入っていることを見る。5枚の板はつながった一枚の表面ではなく、箱状の部分が5つ入った練習用形状。細かい接合や角の仕上げは後のレッスンで扱う。`Crate.A` と `Crate.B` は同じ Mesh を使うので、Edit Mode での形状変更は両方に反映される。一方、Object Mode の Location はそれぞれ独立している。

## 原点と「形の位置」はどう違うか

`Object.location` は **Object の原点をどこに置くか**を表す。Mesh の各頂点は、その原点を基準にした**ローカル座標**を持つ。Object に親がなく回転も拡大もない今回の例では、頂点のワールド位置は「Object の Location + 頂点のローカル位置」として読める。

| 対象 | 比べる面のローカル Z | Object の Location Z | 比べる面のワールド Z |
|---|---:|---:|---:|
| `Crate.A` | 0 | 0 | 0 |
| `Crate.B` | 0 | 0 | 0 |
| `Ground` の上面 | 0 | 0 | 0 |

木箱の底板は中心 Z=0.06、厚さ0.12。下面は `0.06 - 0.12/2 = 0`。側板は底板の上面 Z=0.12 から木箱の上端 Z=1.4 まで伸びる。これで、Mesh の最下点と Object の原点が同じ高さになる。地面は上面を Z=0 にした別 Mesh。

ここで **原点を後から移動したわけではない**。スクリプトは最初から原点 `(0, 0, 0)` を基準に板の頂点を配置している。Blender画面で既存モデルの原点を直すなら **Object → Set Origin** などを使えるが、この回は「形状をどの座標で作るか」に集中する。[Blender Manual: Object Origin](https://docs.blender.org/manual/en/5.2/scene_layout/object/origin.html)

## スクリプトの流れ

1. レッスン03と同じ方法で `Crates` と `Environment` の Collection を作る。
2. `add_box()` は単位立方体の8頂点を拡大・移動し、厚みのある板を1枚作る。すでに置いた板の頂点は動かさない。
3. `make_crate_mesh()` で底板1枚と側板4枚を **同じ BMesh** に作り、1つの `CrateBoards` Mesh に書き込む。
4. `Crate.A` と `Crate.B` の2つの Object に同じ Mesh を渡し、左右の位置を別々に設定する。地面の Object は `Environment` に入れる。
5. ログで Mesh の最下点、各 Object の原点と底面、地面の上面を比べる。さらに板5枚分の40頂点・30面と Mesh の共有を検査して `.blend` に保存する。

ログの `mesh local bottom=0.000` は形状の底、`origin_z=0.000` は Object の基準点、`bottom_z=0.000` は配置後の底の高さ。3つが同じなので地面に接する。

## 変更実験

1. [lesson.py](lesson.py) の `CRATE_B_Z = 0.0` を **`0.5`** に変える。実行前に `Crate.B` の `origin_z` と `bottom_z`、`Crate.A` の `bottom_z` を予測する。
2. 再実行する。`Crate.B` の原点と底は両方 Z=0.5 になり、地面から0.5浮く。`Crate.A` は Z=0 のまま。2つの Object はまだ同じ Mesh を共有している。
3. `CRATE_B_Z = 0.0` に戻して再実行し、両方が地面に接することを確かめる。

## よく混同する点

| 疑問 | 答え |
|---|---|
| 板が5枚なら Object も5つ？ | 今回は1つの Mesh に5つの箱状の部分を作り、木箱1個につき Object は1つ。 |
| 原点は形の中心に自動で置かれる？ | Object の原点と Mesh 頂点の配置は別。今回は底面中央を原点にする座標で頂点を作った。 |
| Collection に入れると底面の位置がそろう？ | そろわない。原点と頂点のローカル座標、各 Object の Location で決まる。 |
| 木箱2個は同じ Location を持つ？ | いいえ。共有するのは Mesh。`Crate.A` は X=-1.5、`Crate.B` は X=1.5。 |
| 木箱1個を動かすのに Empty は必要？ | 今回は木箱全体が1つの Object なので、その Object を動かせばよい。板を別 Object に分けた構成なら、親 Empty が便利。 |

## 理解メモ：5枚の板と Mesh は画面のどこで確認する？

今回の構造は「5つの Mesh」ではなく、**5枚の板形状が1つの Mesh データに入っている**。スクリーンショットでは、右上の Outliner で `Crate.A` または `Crate.B` の左にある開閉用の三角を開くと、その下に緑の三角アイコン付きで表示される `CrateBoards` が Mesh データ。`Crate.A` と `Crate.B` の両方の下に同じ名前が見えるのは、2つの Object が同じ Mesh を参照しているから。

5枚の中身は次の手順で確認できる。

1. ビューポートまたは Outliner で `Crate.A` を選ぶ。
2. `Tab` キーで **Edit Mode** に入る。1つの Object の編集なのに、底板1枚と側板4枚の頂点・辺・面を編集できる。
3. 何も選択していない状態で、マウスポインターを板1枚の上に置いて `L`（Select Linked）を押す。その板だけが選ばれる。板ごとにこれを試すと、1つの Mesh の中に連結していない部分が5つあると分かる。
4. 頂点・面の総数も見たい場合は、ビューポート右上の **Viewport Overlays**（重なった丸のアイコン）を開き、**Text Info → Statistics** を有効にする。この教材では5枚合計で40頂点・30面。

右下の Properties Editor では、`Crate.A` を選択して縦タブの**緑の三角（Object Data Properties）**を押すと、現在参照している Mesh の各種設定を確認できる。ただし「連結していない板が5つ」という個数はここには直接表示されないため、Edit Mode の `L` で形状のまとまりを見るのが分かりやすい。

## 完了条件と次へ

画面で木箱が2個とも地面に接することを見て、`Location Z=0` で接地する理由を **Mesh のローカル底面 Z=0** から説明できれば完了。次は [05 マテリアルの入口](../../docs/plan/README.md)。同じ木箱の形でも、色や粗さで見え方がどう変わるか調べる。
