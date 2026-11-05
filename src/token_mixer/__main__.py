"""Check the planned model configuration; this is not an experiment runner."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from .config import load_model_config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/minimal.yaml"))
    args = parser.parse_args()
    try:
        config = load_model_config(args.config)
    except (OSError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "configuration_status": "MODEL_CONFIG_VALID",
        "experiment_status": "NOT_RUN",
        "model": asdict(config),
        "total_depths": config.total_depths,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
