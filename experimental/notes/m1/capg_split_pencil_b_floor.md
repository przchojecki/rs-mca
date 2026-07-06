# Base-Field Floor Audit for Split-Pencil-B

## Claim

The current base-field correction in `prop:capg-census-floor` is visible on
small exact rows: direct prefix-fiber enumeration realizes the `M_B(d1)` floor
that `prob:capg-split-pencil-B` includes in the corrected split-pencil model.
On most tested extension rows, the challenge-field-only term is smaller than
this base-field floor.

## Status

EXPERIMENTAL / AUDIT.  This is finite support for the corrected floor term, not
a proof of the full primitive split-pencil upper bound, not a finite adjacent
safe-side certificate, and not a resolution of `prob:band`.

## Pinned Statements

- `prop:capg-census-floor`, `experimental/cap25_cap_v13_raw.tex`, lines
  9727-9776: states the boundary and interior base-field census floors.
- `prob:capg-split-pencil-B`, lines 9841-9865: states the corrected
  base-field-normalized split-pencil model using `M_B(d1)`.
- `rem:capg-subfield-scope`, lines 9873-9890: says these floors identify the
  correct model but do not weaken or prove the remaining program.

## Exact Rows

The checker enumerates all supports at the indicated level, groups them by the
signed locator-prefix map, and compares the heaviest fiber with the exact
`ceil(binomial / p^s)` floor.  Interior profiles multiply the heaviest level
fiber by `binom(m',m)` as in the printed `M_B(d1)` formula.

| row | profile | d1 | floor | observed | q-generic term | q-only below floor |
|---|---|---:|---:|---:|---|---|
| F17 n16 K8 m10 q=p^2 | boundary | 3 | 28 | 32 | 8008/289 | yes |
| F17 n16 K8 m10 q=p^2 | interior | 4 | 11 | 33 | 8008/289 | no |
| F17 n16 K8 m10 q=p^4 | boundary | 3 | 28 | 32 | 8008/83521 | yes |
| F17 n16 K8 m10 q=p^4 | interior | 4 | 11 | 33 | 8008/83521 | yes |
| F17 n16 K6 m9 q=p^4 | boundary | 4 | 3 | 5 | 11440/6975757441 | yes |
| F17 n16 K6 m9 q=p^4 | interior | 5 | 10 | 20 | 11440/6975757441 | yes |
| F97 n16 K8 m10 q=p^2 | boundary | 3 | 1 | 5 | 8008/9409 | no |
| F97 n16 K8 m10 q=p^2 | interior | 4 | 11 | 33 | 8008/9409 | yes |

The oracle row `F7 n6 K3 m4` is included in the certificate and verifies the
same heaviest-fiber calculation on a hand-sized subgroup before the toy rows are
accepted.

## Proof Idea Or Experiment

The generator constructs `mu_n` inside the base field, enumerates every support
of size `m` or `m'`, computes the signed locator-prefix coefficients exactly
modulo `p`, and records the heaviest fiber.  It then compares the resulting
base-field floor with the challenge-field random term appearing in
`prob:capg-split-pencil-B`.

The independent checker uses a different subgroup construction and multiplies
locator polynomials directly to recompute the prefix keys.  It does not import
the generator.

## Ledger Impact

This supports the author's correction that the live split-pencil model must
include base-field floor terms.  It also marks the boundary of the packet: the
full primitive upper bound over arbitrary determinantal representations remains
unproved here.

## Non-Overlap

This does not redo the finite-testability map, the Q/R1 one-step input audit,
prefix-collision ledgers, growing-dimension census, annulus packets, or the
rung-margin audit.  It tests only the live base-field floor term in the current
split-pencil correction.

## Self-Red-Team

An adversarial reviewer could object that realizing a floor term is much weaker
than proving the corrected split-pencil upper bound.  That objection is exactly
why the headline is limited to floor realization: this packet supports the
normalization correction and does not claim control of all primitive
split-pencil cells.

## Reproducibility

```text
py -3.13 experimental/scripts/verify_capg_split_pencil_b_floor.py --emit-defaults --check
py -3.13 experimental/scripts/verify_capg_split_pencil_b_floor_check.py --check
```
