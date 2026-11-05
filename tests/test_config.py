"""Configuration checks only; these do not verify a Transformer."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def write_config(tmp_path, model):
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump({"model": model}), encoding="utf-8")
    return path


def test_default_protocol():
    from token_mixer.config import load_model_config
    config = load_model_config(ROOT / "configs/minimal.yaml")
    assert config.shared_layers == 2
    assert config.branch_depths == (2, 4, 6)
    assert config.total_depths == (4, 6, 8)
    assert config.hidden_size == 64


def test_more_than_three_branches(tmp_path):
    from token_mixer.config import load_model_config
    config = load_model_config(write_config(tmp_path, {"branch_depths": [1, 2, 4, 6, 8]}))
    assert config.total_depths == (3, 4, 6, 8, 10)


def test_equal_depth_experts_are_allowed(tmp_path):
    from token_mixer.config import load_model_config
    config = load_model_config(write_config(tmp_path, {"branch_depths": [2, 2, 6]}))
    assert config.branch_depths == (2, 2, 6)


@pytest.mark.parametrize("model", [
    {"shared_layers": 0}, {"shared_layers": True}, {"hidden_size": 63},
    {"num_heads": 0}, {"num_heads": 3}, {"branch_depths": []},
    {"branch_depths": [2]}, {"branch_depths": [2, -1, 6]},
    {"branch_depths": [2, True, 6]}, {"branch_depths": "2,4,6"},
    {"branch_depths": [2, 4.0, 6]}, {"ffn_dim": 0},
    {"vocab_size": 1}, {"max_seq_len": -1}, {"unknown_option": 1},
])
def test_rejects_invalid_model_config(tmp_path, model):
    from token_mixer.config import load_model_config
    with pytest.raises(ValueError):
        load_model_config(write_config(tmp_path, model))


@pytest.mark.parametrize("content", ["", "[]", "{}", "model: null", "model: []",
    "model:\n  hidden_size: 64\n  hidden_size: 32\n",
    "model: !!python/object/apply:os.system ['echo unsafe']",
])
def test_rejects_invalid_yaml(tmp_path, content):
    from token_mixer.config import load_model_config
    path = tmp_path / "bad.yaml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        load_model_config(path)


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run([sys.executable, "-m", "token_mixer", *args],
                          cwd=ROOT, env=env, text=True, capture_output=True, check=False)


def test_cli_reports_not_run():
    result = run_cli("--config", "configs/minimal.yaml")
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["configuration_status"] == "MODEL_CONFIG_VALID"
    assert output["experiment_status"] == "NOT_RUN"
    assert output["total_depths"] == [4, 6, 8]


def test_cli_missing_file_is_nonzero_without_traceback():
    result = run_cli("--config", "missing.yaml")
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
