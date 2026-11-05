# 実装ロードマップ

- [x] リポジトリ構成・仕様・モデル設定検査
- [ ] 00: 共有幹、共通KV、任意本数の独立分岐、全履歴参照実装
- [ ] 00: 1,000切替・因果性・非破壊参照・非選択分岐未実行の試験
- [ ] 01: 対応表単位のデータ分割、深い経路学習、開発checkpoint選択
- [ ] 02: 共有部と深い経路の凍結、2/4層分岐のCE＋蒸留
- [ ] 03: Router教師ラベル、校正、確認seed、品質・実時間の対比較
- [ ] 結果の監査・失敗例公開・実験環境の固定

## 次に追加する予定のモジュール（現時点では存在しない）

`shared_transformer.py` は下位層、`shared_kv.py` は共通メモリ所有権、`branches.py` は独立経路、`router.py` は実行前選択、`model.py` は統合APIを担当する。データ生成・計測・学習コードはそれぞれ分離し、空の関数を動作済みと扱わない。

最初の実装単位は**学習なしの実験00**。構造テストが通るまでは学習・Router最適化に着手しない。高性能GPU、巨大データ、外部サービス、認証キーは初期実証の前提にしない。

## 実装Issue

| 順序 | Issue | 前提 |
| --- | --- | --- |
| 00 | [#1 共有KV・切替整合性](https://github.com/Unjuno/adaptive-depth-token-mixer/issues/1) | 学習不要 |
| 01 | [#2 データ分割・深い経路](https://github.com/Unjuno/adaptive-depth-token-mixer/issues/2) | #1 PASS |
| 02 | [#3 浅い・中間分岐](https://github.com/Unjuno/adaptive-depth-token-mixer/issues/3) | #2の品質基準達成 |
| 03 | [#4 Router・品質速度比較](https://github.com/Unjuno/adaptive-depth-token-mixer/issues/4) | #1〜#3完了 |
