# X1 / E5: multiscale resonance evidence

- **Status:** EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `payment_completeness`, `redteam_multiscale`.
- **Fable evidence item:** E5, "Multi-scale resonance".
- **Verifier:** `experimental/scripts/verify_x1_e5_multiscale_resonance_evidence.py`.
- **Artifact:** `experimental/data/certificates/x1-e5-multiscale-resonance/e5_multiscale_resonance_evidence.json`.

## Purpose

This packet runs the E5 red-team question from Fable's evidence plan:

```text
Can phase-locked periodic structure across many dyadic quotient scales create
unpaid alignment mass invisible to the individual per-scale ledgers?
```

The result is evidence only.  It does not prove `payment_completeness`, does not
search arbitrary received words, and does not change any Paper A-D statement.

## Pre-registered model

The model is the linear periodic character model.  Fix a base field `B=F_p`,
a smooth cyclic row `H_n <= B^*`, and a common binomial extension generator
`alpha` of degree `D`.  A periodic `r`-character component at any scale whose
period is divisible by `D` contributes to the `B`-line

```text
B alpha^r.
```

For several dyadic scales at once, the combined slope image is therefore tested
against the deduped union of the active character lines:

```text
rank_B span{alpha^r : r active at some scale}.
```

A fifth-mechanism signal in this model would be

```text
actual combined rank > deduped active-character union rank.
```

The verifier searches:

```text
p = 12289
n in {1024, 2048, 4096}
D = 32
alpha^32 = 11, with X^32 - 11 irreducible over F_12289
scales D, 2D, 4D, ..., n
active characters per scale in {2,3}
all phases for phase-locked same-residue families
all phases for adversarial residue-spread families
512 seeded random trials per row and active-character cap
seed = 20260702
```

## Result

The emitted classification is:

```text
NO_MULTISCALE_HIDDEN_RANK_SIGNAL_IN_PRE_REGISTERED_LINEAR_PERIODIC_MODEL
```

The strongest adversarial configurations do show multiscale accumulation
relative to a single scale: with `D=32`, the pre-registered search reaches
combined rank `24` and an eightfold ratio versus any individual scale, while
each scale uses only two or three active characters.  However, this
accumulation is exactly the deduped union of the character payments.  The
verifier found no hidden rank beyond that union in the pre-registered
phase-locked, adversarial-spread, or seeded-random families.

This supports the current payment-completeness heuristic only in this restricted
linear periodic model: multiscale phase locking can make many scales active, but
the tested slope space remains a union-of-character-lines object rather than a
new unpaid mechanism.

## Interpretation table

| verifier outcome | interpretation |
|---|---|
| `max_hidden_excess_over_deduped_union = 0` | Supports payment completeness in this model; multiscale accumulation is paid by deduped character lines. |
| `max_hidden_excess_over_deduped_union > 0` | Candidate fifth mechanism; minimize the witness and add a new paid-ledger column before using payment completeness. |

The current packet is the first outcome.

## Non-claims

- No proof of `payment_completeness`.
- No arbitrary-word search.
- No nonlinear Hankel chart search.
- No threshold or leaderboard claim.
- No modification to Papers A-D.

## Reproduce

```bash
python3 experimental/scripts/verify_x1_e5_multiscale_resonance_evidence.py --emit
python3 experimental/scripts/verify_x1_e5_multiscale_resonance_evidence.py
```
