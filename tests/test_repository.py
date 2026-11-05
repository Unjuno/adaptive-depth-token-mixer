"""Repository hygiene checks, not numerical or model-quality tests."""
from pathlib import Path
import re
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_internal_markdown_links_resolve():
    files = list(ROOT.glob("*.md"))
    for folder in ("docs", "experiments", "results", "reports"):
        files.extend((ROOT / folder).rglob("*.md"))
    for path in files:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            assert (path.parent / target.split("#", 1)[0]).exists(), (path, target)


@pytest.mark.parametrize("path", [".env", ".env.local", "private.key", "checkpoint.pt",
    "checkpoint.safetensors", "data/private.json", "results/raw/log.jsonl",
    "runs/seed11/log.jsonl"])
def test_sensitive_and_large_paths_are_ignored(path):
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    assert result.returncode == 0


def test_audited_result_summaries_are_not_blanket_ignored():
    result = subprocess.run(["git", "check-ignore", "-q", "results/summary.json"],
                            cwd=ROOT, check=False)
    assert result.returncode == 1


def test_ci_is_read_only_and_actions_are_pinned():
    document = yaml.load((ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"),
                         Loader=yaml.BaseLoader)
    assert document["permissions"] == {"contents": "read"}
    assert "pull_request_target" not in document["on"]
    steps = document["jobs"]["checks"]["steps"]
    for step in steps:
        if "uses" in step:
            assert re.fullmatch(r"[\w-]+/[\w-]+@[0-9a-f]{40}", step["uses"])
    assert steps[0]["with"]["persist-credentials"] == "false"
