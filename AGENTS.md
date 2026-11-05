# Repository working rules

- This is a shared-KV, multi-branch research prototype, not an implemented model yet.
- Read README.md, docs/architecture.md and docs/experiment-plan.md first.
- Default: shared 2 layers; independent branches with 2, 4, 6 added layers. Do not hard-code two branches.
- Route BEFORE running branch/head. No per-branch historical KV; shared-trunk caches still exist.
- Do not claim config tests prove KV correctness, quality, speedup or scientific novelty.
- Implement experiment 00 before training. Keep planned and executed work separate.
- Test with `python -m pytest -q`; check configuration with `python -m token_mixer --config configs/minimal.yaml`.
- The current CLI validates the model section only; it does not run experiments.
- Do not upload credentials, raw/private data, checkpoints, or unreviewed legacy results.
- Do not change the license or publish training artifacts without explicit approval.
