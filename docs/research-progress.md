# Research progress — container experiments (2026-11-06 to 2026-11-09)

**Status:** Exploratory results produced outside this repository. The GitHub package still contains configuration validation only; the trained models and executable experimental pipelines have **not** been merged into this repository. This document is an audit-oriented summary, not a claim that the CI tests reproduce these results.

## Architecture evolution

1. Shared trunk: two causal Transformer layers, with shared KV memory.
2. Original prototype: independent 2/4/6-layer branches with separate output heads.
3. Shared-upper variant: sequential upper blocks with exits at total depths 4, 6, 8.
4. Recurrent-upper variant: reuse the same two upper layers one, two, or three times, with exits at 4, 6, 8. The upper block reads shared KV; no branch-specific historical KV backfill is required.

The last two are distinct hypotheses: sequential sharing reduces duplicated *paths*; recurrent sharing additionally ties the *weights across depths*. Neither guarantees a better predictor.

## Selected observed results (exploratory)

| Study | Conditions | Observation | Limitation |
| --- | --- | --- | --- |
| Shared KV switching | 3/5 branches, three seeds | 6,426 switches, no greedy mismatch with full-history reference; maximum logit difference ~1.19e-6 | Random/synthetic model; not natural language |
| Numeric sequences | Equal task, 3 seeds, 4/6/8 exits | Independent: 217,056 params; sequential sharing: 131,520; repeated two layers: 74,496. All exits reached 100% on the tested *in-distribution* simple sequences | Unseen step sizes fell near chance; no generalization claim |
| Recurrence stress test | mod-10, 2- and 3-term recurrences | On valid 3-term sequences, 100% was possible, yet perturbing an earlier digit revealed a different, distribution-equivalent update rule | High nominal accuracy does not prove the intended local transition |
| Equal-parameter comparison | Repeated vs low-rank independent, three seeds | Performance rankings reversed across seeds; high-performing models could fail corrupted-history interventions | Low-rank parameterization is a confound |
| Local-transition curriculum | mod-4, 64 local states | Repeated-upper model achieved full-sequence and corrupted-history success in three seeds | All 64 local states were in training |
| mod-6 factorial/curriculum | 216 local states, two curriculum seeds | Repeated-upper model reached ~97.69% and ~96.64% local accuracy after a 2-term-to-3-term curriculum (2,400 updates); direct learning remained substantially lower | Small synthetic tasks; not proof of general rule induction |

**Interpretation:** Weight sharing can reduce stored parameters and retain task performance. Optimization path, task-state coverage and the desired behavior after corrupted prefixes materially affect the result. More parameters and more depth do not automatically improve accuracy. The original adaptive Router has **not** been trained or validated.

## Key failure modes to preserve

- Teacher forcing can report near-perfect later-position accuracy while autoregressive generation fails at the first prediction.
- On valid recurrence sequences, alternative algebraically equivalent rules can produce 100% scores yet respond incorrectly after a token is modified.
- A high maximum Softmax probability is not a calibrated guarantee of correctness.
- Performance and apparent architecture rankings can reverse with random seed.
- The apparent success of a small-state problem may depend on coverage and partial statistical cues.

## Next falsifiable experiment: mod-6 parity decomposition

For uniformly sampled triples of digits 0–5, compare:
- Direct next-digit mod-6 classification.
- Auxiliary mod-2 parity prediction.
- Auxiliary mod-3 residue prediction.
- Joint mod-2/mod-3 heads and deterministic Chinese-remainder reconstruction.

Keep training-state coverage, total updates, trunk/upper architecture, seed set and data splits identical. Account for the extra head parameters. Evaluate held-out triples, free-running four-digit accuracy, intervention correctness, ECE/calibration and latency. Distinguish improved convergence from generalization. Use a pre-registered stopping rule; report FAIL and UNCERTAIN.

## Reproducibility and provenance

Container studies were archived separately in the conversation as:
- `shared_kv_container_experiment_20261106.zip`
- `shared_upper_numeric_experiment_20261106.zip`
- `recurrence_difficulty_study_20261106.zip`
- `matched_depth_followup_20261108.zip`
- `shared_kv_local_transition_experiment_20261108.zip`
- `shared_kv_mod6_factorial_curriculum_20261109.zip`

These are **not** GitHub-hosted artifacts. Their presence in the conversation does not make them available to a fresh clone. Do not treat this document as sufficient independent replication. Reproduction requires importing reviewed source, frozen configs, split manifests, dependency versions, raw metrics and integrity checks. Weights and raw logs remain excluded from the public repository pending review.

Related fields: machine learning / optimization, computer architecture / KV cache, dynamical systems / interventions, algebra / Chinese remainder theorem.
