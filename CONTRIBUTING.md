# 開発手順

1. [実験計画](docs/experiment-plan.md)と[実装順序](docs/roadmap.md)を読む。
2. 変更は目的を絞ったbranchで行い、失敗するテストを先に用意する。
3. `python -m pip install -e '.[dev]'` と `python -m pytest -q` を実行する。
4. `python -m token_mixer --config configs/minimal.yaml` でモデル設定を確認する。
5. PRに変更理由、実行したコマンド、実測結果、未検証事項を記載する。

設定・checkpoint・データ分割を最終テストに合わせて調整しない。protocol変更は版を上げ、旧条件の結果を残す。重み・秘密情報・過去実験の未監査成果物を追加しない。ライセンスの新規付与や変更は所有者の明示決定を必要とする。
