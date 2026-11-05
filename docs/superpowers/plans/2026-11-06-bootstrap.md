# Repository Bootstrap Implementation Plan

> For agentic workers: use superpowers:executing-plans to execute task by task.

**Goal:** 合意済みの共有KV・多分岐実験を、未実施の状態を明示した再現可能な研究リポジトリに整理する。
**Architecture:** 文書・設定・Pythonパッケージ・実験・検査・結果を分離する。今回はモデル、学習器、性能測定は実装しない。
**Tech Stack:** Python 3.11–3.13、setuptools、PyYAML、pytest、GitHub Actions。
**Spec:** `docs/experiment-plan.md`（会話で合意した実験計画を保存）。

## Global Constraints
- 共有2層、独立した追加2/4/6層の3分岐を既定値とする。分岐数は設定化する。
- Routerは分岐計算前。分岐専用の履歴KVは持たない。
- 実験00–03はNOT_IMPLEMENTED。設定検査を実験PASSと呼ばない。
- 秘密情報・重み・過去の未監査成果物を公開しない。ライセンスは未選択のままにする。
- 空の公開リポジトリの初期整理。既存コミットが生じていたら再読込し、上書きしない。

## Review Focus
- 分岐数が2本へ固定されていないか。
- 設定キーの誤記、負の層数、head数の不整合を拒否するか。
- 検査出力が学習・速度の成功を暗示しないか。
- READMEのコマンドとリンクが存在するか。
- 学習・校正・最終テストの独立性と、CPU結果の限界が記載されているか。

## Task 1: Configuration and package
- [x] tests/test_config.py に既定構成、多分岐、型・範囲・未知キーの失敗テストを書く。
- [x] `python -m pytest` を実行し、機能未実装による失敗を確認する。
- [x] src/token_mixer/config.py の `load_model_config(path)` と設定検査CLIを実装する。
- [x] 全テストを通し、設定検査がNOT_RUNを返すことを確認する。

## Task 2: Research organization
- [x] README、アーキテクチャ、実験計画、再現手順、実装順序を保存する。
- [x] experiments/results/reportsの役割と非公開ファイル規則を記載する。
- [x] CI、Issue/PRテンプレート、貢献手順を追加する。

## Task 3: Verify and publish
- [x] 全テスト、インストール、CLI、内部リンク、秘密情報混入を検査する。
- [x] 自己レビューを記録する（独立レビューではない）。
- [x] GitHubへ初期構成を追加し、リモートtreeとローカルtreeの一致を検証する。
- [x] CIの実際の状態を確認し、未完了なら未確認と報告する。
