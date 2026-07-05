# FM1 Exact First-Moment Packet

- **Status:** PROVED / exact finite-slope count.
- **DAG node:** `fm1`.
- **Certificate:** `experimental/data/certificates/fm1/fm1.json`.
- **Verifier:** `python3 experimental/scripts/verify_fm1_packet.py --check experimental/data/certificates/fm1/fm1.json`.

This packet records the exact first-moment formula for aligned supports in the
Hankel/MCA counting frame.

## Claim

Fix a support `R` of size `j`, and write `S = H \ R`. The restriction of the
RS code to `S` has dimension `k`, while

```text
|S| = k + t.
```

Thus the quotient syndrome space has dimension `t`. For a random received pair
`(u,v)`, let `U,V in F^t` be the induced quotient syndromes on `S`.

The support `R` is aligned at a finite slope `z` precisely when

```text
U + z V = 0
```

with `V != 0`. The excluded case `V = 0` is the all-slope/paid-fiber
degeneracy and is not part of this finite-slope first-moment column.

There are `q^t - 1` choices for nonzero `V`. For each nonzero `V`, there are
exactly `q` choices for `U` on the affine line spanned by `V`, namely
`U = -zV` for `z in F`. Among all `q^(2t)` pairs `(U,V)`,

```text
Pr[R aligned at a finite slope]
  = q(q^t - 1) / q^(2t)
  = (1 - q^(-t)) q^(1-t).
```

By linearity of expectation over the `binom(n,j)` supports,

```text
E[#aligned] = binom(n,j) (1 - q^(-t)) q^(1-t).
```

## DAG Use

FM1 feeds the MCA safe-side ledger, spread-regime heuristics, and
integrality/zero-at-crossing bookkeeping. It is a first-moment formula only;
it does not classify the aligned supports.

## Non-Claims

- This packet does not count the all-slope degeneracy `V=0`.
- This packet does not classify aligned supports as paid or unpaid.
- This packet does not prove any higher-moment or concentration bound.
- This packet does not edit Papers A-D.
