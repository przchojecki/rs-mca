# E13 Split-Locator Syzygy Circuit Lemma

- **Status:** PROVED local algebra lemma, with replay against the E13 records.
- **DAG nodes:** `spread_exception_classification`, `spread_regime_bound`.
- **Verifier:** `experimental/scripts/verify_e13_split_locator_syzygy_circuit_lemma.py`.
- **Artifact:**
  `experimental/data/certificates/spread-regime-design-evidence/e13_split_locator_syzygy_circuit_lemma.json`.

## Statement

Let `F` be a field, let `D subset F`, and let
`L_i(X)` be locator polynomials indexed by `i in I`.  Fix slopes
`z_i in F` and a moment length `t`.  For each pair `(i,m)`,
`0 <= m < t`, form the split row

```text
R_{i,m} = coeff( X^m L_i(X), z_i X^m L_i(X) )
```

in the coefficient space of the two polynomials.  A coefficient vector
`c_{i,m}` is a left dependency among the split rows if and only if the two
polynomial identities

```text
sum_{i,m} c_{i,m} X^m L_i(X) = 0,
sum_{i,m} c_{i,m} z_i X^m L_i(X) = 0
```

hold in `F[X]`.

Consequently, if the left-nullspace is one-dimensional, every locator block
has some nonzero coefficient, and deleting any one locator block makes the
remaining split rows independent up to the degree cap, then the rank-loss
configuration is a full-support minimal circuit in the split-locator row
matroid.  No proper subfamily of locator blocks carries the same dependency.

## Proof

The row `R_{i,m}` is, by definition, the concatenation of the coefficient
vectors of `X^m L_i(X)` and `z_i X^m L_i(X)`.  Therefore a linear combination
of the rows vanishes exactly when each half of the concatenated coefficient
vector vanishes.  These two halves are precisely the coefficient vectors of
the two displayed polynomial sums.  This proves the equivalence.

If the nullspace is one-dimensional, every dependency is a scalar multiple of
one generator.  Full locator support says this generator uses every locator
block.  If deleting any one locator block restores the expected degree-cap
rank, then no dependency remains after any such deletion.  Every proper
locator subfamily is contained in a one-block deletion, so no proper subfamily
carries a dependency.  Thus the support is a minimal circuit.

## E13 replay

The companion verifier reads the existing E13 sparse-greedy syzygy artifact
and checks that all `71` stored `n=32` control exceptions satisfy the lemma's
hypotheses:

```text
left nullity = 1,
full locator support,
all one-block deletions independent.
```

It also verifies that the certificate-level totals match the E13 branch
record.

Replay:

```bash
python3 experimental/scripts/verify_e13_split_locator_syzygy_circuit_lemma.py --emit
python3 experimental/scripts/verify_e13_split_locator_syzygy_circuit_lemma.py \
  --check experimental/data/certificates/spread-regime-design-evidence/e13_split_locator_syzygy_circuit_lemma.json
```
