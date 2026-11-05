# 再現・計測・公開規約

## 実験ごとに保存するもの

Git commit SHA、設定ファイルとhash、実行コマンド、データ生成seed・split hash、checkpoint hash、開始・終了時刻、終了コード、生記録への参照を保存する。環境はPython/PyTorch、OS、CPU/GPU型番、クロックの固定有無と観測値、threads、batch、文脈長、生成長、dtype、Attention backendを必須とする。

現在は設定ツールのみ。PyYAML 6.0.3、pytest 9.0.2を固定しているが、ビルド環境全体のlockではない。実験環境には別途 `pip freeze` などの記録が必要。PyTorchをまだ必須依存へ加えない。

## 数値・速度の区別

設定検査PASS、構造テストPASS、学習成立、品質非劣性、速度改善を別項目として記録する。CPUでの倍率をGPUへ転記しない。モデル層数を実測時間の代理にしない。

構造確認はFP32・数学SDPA・dropout無効を基準にする。高速backend、GPU、低精度は別条件で照合する。Attention maskの意味、KV追記位置、位置埋め込み、cache dtype、backend切替を実装時の検査項目に含める。量子化は対象外なのでzero-point/量子化ABIは適用外。

品質は同一系列で対比較し、自由生成とteacher forcingを混合しない。時間は方式順を交互化し、全サンプル・全反復を残す。seed間変動と同一環境の計時変動を別々に報告する。構成の不確かさを、単一の標準誤差や正規近似の包含係数で隠さない。

## 公開範囲

`results/` は監査済みの小さな集計、`reports/` は説明、`results/raw/`・`runs/`・`data/`・`outputs/` は既定でGit除外。重みも除外する。公開が必要になった時点で、内容・出典・サイズ・再配布条件を確認して別途決める。

`.env`・秘密鍵・アクセストークンを保存しない。ignore規則は誤混入防止の補助であり、公開前に差分自体を読む。失敗した実験も条件と失敗理由を保存し、成功したseedだけを選別しない。

## CIの範囲

CIは設定とCLIを検査するだけで、学習を実行しない。GitHub Actionsは `contents: read`、PR targetイベントなし、checkout資格情報の永続化なし。checkout/setup-pythonは確認したv6のcommit SHAへ固定する。ローカル検査とGitHub CIの実際の実行状態は別に記録する。
