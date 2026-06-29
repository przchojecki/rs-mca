# p=257 quotient-periodic locator matrix

Exact (no-sampling) `F_257` toy-case database produced by
`experimental/scripts/p257_locator_matrix.py`. It generalizes the single-cell
`p257_locator_certificate.py` (`N=16, rho=1/2, t=1`) to the full feasible matrix
of smooth quotient scales.

`F_257^*` is cyclic of order `256 = 2^8` (257 is the Fermat prime `2^8+1`), so it
has a clean dyadic tower of subgroups `Q_N` of order `N in {2,4,8,16}`. For each
cell `(N, rho, t)` we set `a = 256/N`, `ell = rho*N + t`, `k = (ell-t)*a` and
enumerate **every** `ell`-subset `A` of `Q_N`, building the whole-fiber locator
`prod_{b in A}(X^a - b)` in exact mod-257 arithmetic and recording its slope
`z = -sum(A)` (the restricted sumset over `Q_N`).

## Reproduce

```sh
# regenerate the certificate
python3 experimental/scripts/p257_locator_matrix.py --format json \
  --output experimental/data/certificates/p257-locator-matrix/p257_locator_matrix_certificate.json
# verify reproducibility (exit 0 = byte-identical)
python3 experimental/scripts/p257_locator_matrix.py \
  --check experimental/data/certificates/p257-locator-matrix/p257_locator_matrix_certificate.json
```

Status `PROVED` (exact finite enumeration); 13 feasible cells of 16, all pass.

## What the table shows (obstruction templates)

- **Restricted-sumset coverage grows with the quotient scale.** At the small
  scale `N=8, t=1` only `40` of `257` slopes occur (sparse); at `N=16` the
  restricted sumset is essentially full (`256` slopes at `t=1`, `257` at `t=2`).
  So the "missing slope" obstruction is a *small-scale* phenomenon here.
- **Complementation duality at `N=16, t=2`.** The rate-`1/2` cell (`ell=10`) and
  the rate-`1/4` cell (`ell=6`) have **identical** slope-multiplicity histograms
  and both reach full `257`-coverage. Reason: `10 = 16 - 6`, and the order-16
  subgroup sums to `0` in `F_257`, so `sum(A) = -sum(Q_16 \ A)`; the slope map
  `A -> -sum(A)` therefore sends the `ell`-subsets bijectively (up to negation,
  a bijection of `F_257`) to the `(N-ell)`-subsets, preserving multiplicities.
- **Zero slope appears exactly in the `t=2` (even-`ell`) rows** recorded here:
  the restricted sumset reaches `0` once the slack lets `ell` hit a
  sum-cancelling configuration.
- **Cross-validation.** The `N=16, rho=1/2, t=1` cell reproduces the committed
  `p257_locator_certificate.py` exactly (`11440` subsets, `256` slopes, support
  `144`, no zero slope) — recorded under `summary.cross_check_p257`.

## Scope

This is a **locator / restricted-sum** table, not an MCA bad-slope exhaustion: at
`n = 256` the MCA support enumeration `C(256, support)` is astronomical, so only
the locator object is exhausted. The histograms feed the M1/L1 quotient-periodic
ledger (cf. `notes/m1/m1_quotient_periodic_overlap_profile.md`) and back Paper A
item V2 (`tex/RS_disproof_v3.tex`, `ex:257`).
