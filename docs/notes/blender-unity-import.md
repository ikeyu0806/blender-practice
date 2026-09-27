# Blender から Unity へ持ち込むのはいつ、どう学ぶか

## 疑問と結論

**Q. Blender で作ったモデルを Unity に入れて、ゲームで使える？** できる。Unity はモデルファイルを読み込み、シーンに配置できる。Blender の編集用 `.blend` と、Unity に渡すための FBX などは役割が違う。Unity 6.0 のマニュアルはモデル交換に FBX を推奨している。`.blend` の直接インポートも可能だが、その環境に Blender が必要になる。[Unity: モデルのファイル形式](https://docs.unity3d.com/ja/6000.0/Manual/3D-formats.html)

**Q. いつ学ぶ？** このプロジェクトでは、まず Blender で Object と Mesh の違い、複数部品の組み立て、マテリアル、背景の小作品まで学ぶ。その後の [レッスン22](../plan/README.md) を Unity 連携の選択回にする。最初の連携では静的な小作品を使う。人物の骨やアニメーションは、人物を作れるようになってから扱う。

## レッスン01の Unity 例えについて

[レッスン01](../../lessons/01_shared_mesh/README.md) で見える2つの立方体は、Blender 内で1つの Mesh データを共有する2つの Object。Unity の知識はこの仕組みの理解に不要。将来 Unity で同じ形のモデルを2か所に置く場面を考えると、「形状データを使い回し、配置は個別に決める」という発想がつながる。ただし Blender の Object と Unity の GameObject は同じ機能の単位ではないため、名前の対応を丸暗記しない。

## 将来の連携レッスンで確認すること

1. Blender で複数部品を含む小作品を完成させ、寸法・原点・向きを記録する。
2. FBX で書き出し、Unity の Project に入れて Scene に配置する。Unity のモデルインポートではメッシュ、マテリアル、テクスチャなどを確認できる。[Unity: モデルのインポート](https://docs.unity3d.com/ja/6000.0/Manual/ImportingModelFiles.html)
3. Blender と Unity の両方で見た目と寸法を比べ、軸変換、スケール、マテリアルの差を調整する。Unity のインポート設定には軸変換などの項目がある。[Unity: Model タブ](https://docs.unity3d.com/ja/6000.0/Manual/FBXImporter-Model.html)

この文書は学習順序のメモ。実際のエクスポート設定と Unity 操作は、連携レッスンを追加するときに使用バージョンで確認する。
