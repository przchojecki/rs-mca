# L1 Petal Fixed-Excess Compiler

## Status

PROVED-COMPILER, citing
`experimental/notes/l1/l1_full_list_quotient_proof_program.md` Lemma 16
(`Cofactor-Budgeted Full-Petal Layers`).

This note packages the roadmap node `petal_fixed_excess`: fixed cofactor-excess
full-petal layers are already polynomially controlled. The package records the
exact layer bounds for excess `0 <= e <= 6`, where `d = ell + e`, and the
growth consequence at the L1 lower cutoff.

It does not close the mixed-petal sunflower amplification problem.

## Setting

Use the background-free full-petal notation of the L1 proof program. There are
`M` planted petals, each of size `ell`, and a non-planted listed codeword has
core defect

```text
d = ell + e.
```

Here `e = d - ell` is the cofactor excess. The fixed-excess node concerns
bounded `e`; the replayable certificate now records the first seven layers
`e <= 6`, matching the E16 petal-growth table request.

## Bound

Lemma 16 gives, for every fixed `E >= 0`, the total number of non-planted
listed codewords whose touched petals are all full and whose defect satisfies

```text
ell <= d <= ell + E
```

as at most

```text
binom(M,2) q + 2^M sum_{e=1}^E q^(e+1).
```

Equivalently, the per-layer compiler is

```text
e = 0:      binom(M,2) q,
e >= 1:    2^M q^(e+1).
```

The `e=0` term is the minimal-defect two-petal layer; the `e>=1` terms use the
full-petal cofactor injection over each touched-petal set.

## Consequence

At the L1 lower cutoff, the number of petals satisfies `M = O(log n)`. If also
`q <= n^Q` for a fixed `Q`, then for every fixed `E`,

```text
2^M q^(E+1) <= n^(O(1)).
```

Thus fixed-excess full-petal extras cannot be the asymptotic obstruction. Any
full-petal counterexample must force `e = d - ell` to grow with `n`, exactly as
the proof-program note indicates.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_fixed_excess_compiler.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_fixed_excess_compiler.py \
  --check experimental/data/certificates/l1-petal-fixed-excess/l1_petal_fixed_excess_compiler.json
```

The verifier is stdlib-only and records exact integer tables for `e <= 6`.
