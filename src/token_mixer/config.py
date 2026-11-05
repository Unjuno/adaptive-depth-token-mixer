"""Validate the model section only; no model execution or training occurs."""
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import yaml


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loading without silently accepting duplicate keys."""


def _unique_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode) -> dict:
    loader.flatten_mapping(node)
    result: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"Duplicate configuration key: {key!r}")
        result[key] = loader.construct_object(value_node)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


@dataclass(frozen=True)
class ModelConfig:
    shared_layers: int = 2
    branch_depths: tuple[int, ...] = (2, 4, 6)
    hidden_size: int = 64
    num_heads: int = 4
    ffn_dim: int = 128
    vocab_size: int = 64
    max_seq_len: int = 64

    def __post_init__(self) -> None:
        for name in ("shared_layers", "hidden_size", "num_heads", "ffn_dim",
                     "vocab_size", "max_seq_len"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.vocab_size < 2:
            raise ValueError("vocab_size must be at least 2")
        if self.hidden_size % self.num_heads:
            raise ValueError("hidden_size must be divisible by num_heads")
        if not isinstance(self.branch_depths, tuple) or len(self.branch_depths) < 2:
            raise ValueError("branch_depths must contain at least two depths")
        if any(type(depth) is not int or depth <= 0 for depth in self.branch_depths):
            raise ValueError("All branch depths must be positive integers")

    @property
    def total_depths(self) -> tuple[int, ...]:
        """Return planned shared-plus-branch layer counts, not measured costs."""
        return tuple(self.shared_layers + depth for depth in self.branch_depths)


def load_model_config(path: str | Path) -> ModelConfig:
    """Read safe YAML and validate its model section; other sections are metadata."""
    try:
        document: Any = yaml.load(Path(path).read_text(encoding="utf-8"),
                                  Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, TypeError) as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("model"), dict):
        raise ValueError("Configuration requires a 'model' mapping")
    values = dict(document["model"])
    allowed = {field.name for field in fields(ModelConfig)}
    unknown = set(values) - allowed
    if unknown:
        raise ValueError(f"Unknown model keys: {sorted(map(str, unknown))}")
    if "branch_depths" in values:
        if not isinstance(values["branch_depths"], list):
            raise ValueError("branch_depths must be a YAML list")
        values["branch_depths"] = tuple(values["branch_depths"])
    return ModelConfig(**values)
