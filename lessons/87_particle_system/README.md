# 87｜Particle System：面から決まった数の粒を出す

## このレッスンの目標

床の元Meshの頂点数はそのままで、Particle Systemの評価後に生きている粒の数が`PARTICLE_COUNT`と一致することを確認する。

前提は [86 Ocean](../86_ocean/README.md)。この回は他のレッスンの出力ファイルを必要としない。種類の並びは [Modifierカタログ](../../docs/notes/modifiers.md)。

完了時には、次を自分の言葉で説明できるようにする。

- Particle System Modifierを足すと、Objectの`particle_systems`に粒の設定が増える。
- `count`は粒の数で、Meshの頂点数ではない。
- 粒の位置はフレームで変わり、元の面の頂点座標とは別に評価される。

## 実行する

プロジェクトのルートで、まず画面なしでシーンを生成する。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python lessons/87_particle_system/lesson.py
```

`saved: .../output/87_particle_system.blend`が出てターミナルに戻ったら、Blenderアプリの **File → Open...** からその`.blend`を開く。すでに開いている別のBlenderウィンドウへ結果は自動表示されない。保存時のフレームは5。

画面付きで実行する場合は次のコマンドも使える。

```bash
/Applications/Blender.app/Contents/MacOS/Blender --python lessons/87_particle_system/lesson.py
```

画面付き起動では、保存後もBlenderが開いたままなのでターミナルはアプリの終了を待つ。スクリプトは実行冒頭で現在のSceneを初期化する。Text Editorから **Run Script** する場合は現在の作業を先に保存する。GUIの変更は`lesson.py`へ同期せず、再実行で同じ出力ファイルが作り直される。手作業の結果を残すなら別名で保存する。[スクリプトと画面の関係](../../docs/notes/script-workflow.md)

## できあがるデータ関係

```text
ParticleSystem Collection
└── Ground.Emitter Object → 床Mesh
    └── Particle System Modifier
        └── particle_systems[0]（count=12、フレーム5で12粒がALIVE）
```

## 仕組み

砂、火の粉、破片の種は、床の頂点を増やすのではなく粒として出す。Modifier stackに`PARTICLE_SYSTEM`が1つあり、詳細な数と寿命は`particle_systems`側の設定データにある。両方は同じ粒の仕組みの、スタック上の姿と設定の姿。

`emit_from`の`FACE`は面の上から出す。`frame_start`と`frame_end`がどちらも1なので、粒はフレーム1で出そろう。フレーム5で評価すると、寿命30の間なので12粒が`ALIVE`。元の床の頂点数は粒の数と一致しない。

次のParticle Instanceは、この粒の位置へ別Meshを置く。Explodeは、同じObjectの面を粒に追従させて割る。

## Blender画面で観察する

1. `.blend`を開く。床の上に粒が見えることを確認する。フレームは5。
2. **Modifier Properties** に`Dust`があることを確認する。
3. Propertiesの粒アイコン **Particle Properties** でNumberが12であることを確認する。
4. ログの`alive=12`と、床の頂点数を照合する。

Modifierメニューの **Apply** は、粒をMesh頂点へ焼き込む操作ではない。粒の数を変えて再実行し、床の面が残ることを見る。

## 変更実験

`lesson.py`の次の値を1つだけ変更する。

```python
PARTICLE_COUNT = 12
```

これを`30`にして、実行前に予測する。床の頂点数は変わるか。生きている粒は30になるか。

再実行すると、床のMeshは同じで、`alive`が30になる。確認後は`12`へ戻す。

## 完了条件と次へ

床のMeshが残り、評価後の生きている粒の数が設定と一致することを説明できれば完了。次は [88 Particle Instance](../88_particle_instance/README.md) で、粒の位置に小石を置く。
