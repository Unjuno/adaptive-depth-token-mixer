# Adaptive-Depth Token Mixer

共有KV型・多分岐Transformerの最小実証リポジトリ。
共有2層の上に独立した追加2・4・6層の経路を置き、同じ履歴メモリを読みながらトークン単位で経路を選ぶ構想を検証する。3分岐は既定例であり、分岐数は固定しない。

**現在は研究用の初期構成です。モデル・学習・高速化実験は未実装／未実施です。**
設定検査やCIの成功は、共有KV方式の成立・生成品質・高速化の証拠ではありません。

## 現在の状態

| 項目 | 状態 |
| --- | --- |
| 実験仕様・ディレクトリ構成 | 整備済み |
| モデル設定の読み込み・検査 | 実装済み |
| 00: 共有KVと切替の整合性 | 未実装 |
| 01: 深い分岐の学習 | 未実装 |
| 02: 浅い・中間分岐の学習 | 未実装 |
| 03: Routerと実測速度の評価 | 未実装 |

## 最初に動かすもの

Python 3.11以上を使用。CI対象は3.11・3.13。以下は**リポジトリ直下**で実行する。

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
python -m pytest -q
python -m token_mixer --config configs/minimal.yaml
```

最後のコマンドは `MODEL_CONFIG_VALID` と `experiment_status: NOT_RUN` を出力する。
現時点ではYAMLの `model` 節だけを意味検査する。他の節は今後の実験設定であり、学習器での検査は未実装。
この初期版のインストール・CIにはPyTorchやGPUは不要。

## 確定した設計

| 処理順 | 役割 |
| --- | --- |
| 埋め込み・共有Transformer 2層 | 全トークンで実行し、共通の文脈状態と分岐共通KVを更新 |
| Mixer / Router | 共有表現から、実行する分岐を先に1つ選ぶ |
| 選択した分岐のみ | 独自QueryとFFNで共有KVを参照。既定の追加深さは2・4・6層 |
| 分岐専用Head・Softmax・トークン選択 | 次トークンを決め、次の共有層更新へ渡す |

分岐側は通常の独立Self-Attentionではなく、共有KVを読むCross-Attention型を予定する。
分岐専用の過去KVは持たない。共有下位2層自身のKVと、分岐共通KVは区別して管理する。
推論時に全分岐のSoftmaxまで計算してから選ぶ方式ではない。

## 構成

```text
configs/                 実験条件（既定値: minimal.yaml）
src/token_mixer/         Pythonパッケージ。現在は設定検査のみ
experiments/             実験00〜03の実装予定と実行契約
tests/                  設定・CLI検査（モデル試験とは別）
docs/                    アーキテクチャ・実験計画・再現手順
results/                 監査済み集計結果の置き場。現在は結果なし
reports/                 実行・検証レポート
.github/                 CI、実験Issue、PRテンプレート
```

## 読む順序

[アーキテクチャ](docs/architecture.md) → [最小実験計画](docs/experiment-plan.md) → [実装順序](docs/roadmap.md) → [再現・計測規約](docs/reproducibility.md)。
開発時は [CONTRIBUTING.md](CONTRIBUTING.md) と [AGENTS.md](AGENTS.md) を参照。

## 公開範囲

認証情報、非公開データ、重み、生ログはコミットしない。過去の独立KV分岐実験のZIPや性能数値も、この共有KV型の成果としては転載しない。
公開用の結果は条件・生記録への参照・失敗例を添えて別途レビューする。

**ライセンス: 未設定。** 初期整理ではMITなどを自動付与していない。
