# 68｜Volume Displace：密度をテクスチャで膨らませる

## このレッスンの目標

同じ岩から作った2つのVolumeのうち、Displaceを付けた側だけ表面の頂点数が変わることを確認する。DisplaceはVolume Objectに付き、Meshの頂点を直接動かさない。

前提は [67 Volume to Mesh](../67_volume_to_mesh/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Volume DisplaceはVolume Objectの密度を、テクスチャの値で押し出す。
- 表面の差は、そのあとのVolume to Meshの評価後頂点として見える。
- 岩の元Meshは両方で同じものを参照している。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/68_volume_displace/lesson.py
```

`saved: .../output/68_volume_displace.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/68_volume_displace/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
VolumeDisplace Collection
├── Rock.Source Object → 立方体Mesh
├── Cloud.Still → Mesh to Volume
│   └── Shell.Still（左）
└── Cloud.Puffed → Mesh to Volume → Volume Displace
    └── Shell.Puffed（右）
```

## 仕組み

MeshのDisplaceは頂点を動かす。Volume Displaceは密度の場をテクスチャで歪める。歪んだ密度をVolume to Meshが読むと、表面の凹凸と頂点数が変わる。

この回は同じ岩からVolumeを2つ作り、右側だけにCloudsテクスチャのDisplaceを付ける。左の表面が基準、右が膨らんだ結果。頂点数が一致しないことで、Displaceが評価に入っていると判断する。岩Objectは1つで、2つのVolumeがそれを参照する。

`strength`を0にすると、右の歪みが弱まり、左の頂点数へ近づく。

## Blender画面で観察する

1. `.blend`を開き、左右の表面を **View → Frame All** で見比べる。
2. `Cloud.Puffed`の **Modifier Properties** で、`FromRock`の下に`Puff`があることを確認する。
3. `Cloud.Still`にはDisplaceが無いことを確認する。
4. ログの`still vertices`と`puffed vertices`が違うことを照合する。

Modifierメニューの **Apply** は押さない。Volume側をApplyすると、その時点の密度がVolumeデータへ入り、テクスチャを差し替えても追従しない。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
PUFF_STRENGTH = 0.4
```

これを`0.8`にして、実行前に予測する。左の頂点数は変わるか。右の表面はより歪むか。

再実行すると、左はDisplace無しのまま、右の頂点数が0.4のときと違う。確認後は`0.4`へ戻す。

## 完了条件と次へ

同じ岩を参照していても、Volume Displaceがある側だけ表面の頂点数が違うことを説明できれば完了。次は [69 Cast](../69_cast/README.md) で、頂点を球の形へ寄せる。
