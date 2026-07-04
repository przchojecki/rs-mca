# MCA-vs-CA Sparse-Layer Census Certificate (gap structure)

Status: AUDIT / EXPERIMENTAL.  Computational evidence packet at toy scale, NOT
a theorem.  This directory holds a compact machine-readable extract of an
externally frozen census; the full artifact lives in the external repo (sha256
pinned below).

## Use Rule header (per `experimental/notes/audits/m0_prize_mca_definition_freeze.md`)

```text
object:            structure of the mutual-only layer MCA-bad \ CA-bad past the
                   unique radius: containment shape of thm:mca-from-ca, witness
                   depth, exact-equality window, J-density law
sampler:           finite_affine; finite slopes gamma in {0,...,q_line-1} only;
                   no Mobius/symmetry quotient; no point at infinity
q_gen/q_line:      toy prime rows, q_gen = q_line in {17, 97}; q_chal = null
                   (no soundness division claimed)
agreement/radius:  A = n - r, closed radius r (r = floor(delta*n) convention)
closed-grid:       closed-grid per-row statements only; no supremum claim
ledgers:           none subtracted; NO deployed-row statement; all oracles are
                   exact but exponential (q^k codeword enumeration,
                   C(n, n-r) subset pair lists) — nothing here scales
```

Rows censused:

| row | field | n | k | unique radius | radii censused | oracle |
|---|---|---|---|---|---|---|
| A | F_17 | 8 | 4 | 2 | 2 (control), 3, 4, 5 | exhaustive, all 17 slopes, 176 instances |
| B | F_17 | 8 | 2 | 3 | 3 (control), 4, 5, 6 | exhaustive, all 17 slopes, 86 instances |
| C | F_97 | 16 | 8 | 4 | 5 (= integer Johnson / GS-complete), 6 | engine-driven (GS exact at r=5; r=6 one targeted 28-challenge instance) |

## Headline results

1. **The tangent-containment extension of `thm:mca-from-ca` is FALSE one step
   past the unique radius.**  Verbatim killer: F_17, domain
   `(1,2,4,8,9,13,15,16)`, `k=4`, `r=3`,
   `f1=[0,0,0,0,0,0,2,1]`, `f2=[0,0,0,0,0,1,1,1]` is 3-close to exactly one
   pair (`(0,0)`, tangents `{0,15,16}`) yet **all 17 slopes are MCA-bad**
   (14 non-tangent extras).  At the unique radius `r=2` (control) the same
   pair is pair-far and extras are empty.
2. **Witness-depth invariant.**  All 1293 violating witnesses across the census
   decompose only at joint distance exactly `n-k` (805 at A r=3, 5 at B r=4,
   473 at B r=5, 10 at C r=6): no violating witness admits any structured
   explanation shallower than the generic interpolation floor.
3. **Exact-equality window.**  F_97, n=16, k=8, r=5: extras = radius-r tangent
   union EXACTLY, zero exceptions in either direction, across all 9 censused
   instances.
4. **J-density law.**  With
   `J(n,k,q,r) = sum_{s>=n-r} C(n,s)(q-1)^(n-s) / q^(n-k)`, violation density
   tracks `J` across all censused cells (A r3 `J=2.83` vs `0.577`/slope;
   B r4 `0.20` vs `0.008`; B r5 `2.63` vs `0.472`; C r5 `0.0046` vs `0`;
   C r6 `0.80` vs `~0.43`).  The wall sits at list-decoding CAPACITY
   (`J ~ 1`, i.e. `r -> n-k`), not at the Johnson radius.
5. **`|extras| <= L*r` is dead past the wall** (killer: `17 > L*r = 3`), and
   the `(r+1)`-list repair also fails (B r=4: all 5 violating slopes carry
   witnesses only at depth `n-k = r+2`).

## Distinction from `sigma-c-sparse-census`

Upstream's adjacent lane, `experimental/data/certificates/sigma-c-sparse-census/`,
records **sigma_C VALUES** per row: saturation rows where `sigma_C = q_line`,
via the finite-slope maximal witness sets
`S_z = {i : eps1_i + gamma eps2_i = z_i}`, plus trivial-regime rows
`sigma_C = r` when `2r <= n-k`.  THIS packet instead characterizes the
**STRUCTURE** of the MCA-minus-CA gap: the containment form of
`thm:mca-from-ca` is FALSE past the unique radius, a density form is
supported, all violating witnesses are depth-pinned at exactly `n-k`, and the
density wall sits at capacity (`J`), not Johnson.  I.e. the sigma-c lane
tabulates the value; this lane says WHERE and WHY the mutual layer is nonempty
and HOW it grows — calibrating the sigma_C that `thm:transfer`
(tex/towards-prize.tex:780) needs polynomially bounded.

Conventions are identical (verified against
`experimental/scripts/verify_sigma_c_sparse_census.py`): finite slopes only,
denominator `q_line`, no Mobius quotient; our per-slope MCA-bad semantics (the
engine's `same_set_failures`: some full agreement set of a within-`r` codeword
on which `f1` or `f2` fails to restrict to `C`) is equivalent to the sigma-c
lane's eps2-only check on maximal `S_z` by `lem:line`'s final equivalence
(on any witness set `g1|_S in C|_S` iff `g2|_S in C|_S`).  No row collides
(theirs: n=q-1 style rows at q in {5,7,11,13,17}; ours: F_17 n=8 and F_97
n=16).

Two positioning caveats, stated so the lanes are not conflated:

- `sigma_C` is a MAX over all sparse pairs; our J-density is a per-close-slope
  average over a frozen instance family.  The extremal pair can saturate at
  modest `J` (upstream's `(q,n,k,r)=(11,10,2,5)` row has `J ~ 0.13` yet
  `sigma_C = 11 = q_line`), while our comparable-`J` cells show small typical
  density.  Max and typical coexist; the structural claim (tangent union +
  depth-`(n-k)` witnesses) is per-instance universal in the censused cells,
  the density claim is family-average.
- Toy saturation (`sigma_C = q_line`) does NOT falsify the poly-`sigma_C`
  hypothesis of `thm:transfer`, because `q_line ~ n` at toy scale.  The
  heuristic flood mass per instance, `q*J ~ C(n,r) * q^(1+r-(n-k))`, decays
  in `q` for `r <= n-k-2`; since `n-k >= n(1-sqrt(rho))` at every rate, the
  J-wall sits strictly above the whole band `delta <= 1-sqrt(rho)-eta` of
  `thm:transfer`'s hypothesis.

## Relation to PR #272

PR #272 (conditional BCHKS25 Thm 4.6 / Hab25 Johnson-regime MCA import)
references this census as the toy statement-shape cross-check of Thm 4.6: the
exact-equality window and the capacity-not-Johnson wall are consistent with a
Johnson-radius mutual statement, and pinpoint where (and how) the naive
containment shape fails beyond it.

## Files

- `mca_ca_sparse_layer_census_headline.json` — compact machine-readable
  extract: the killer counterexample verbatim, per-cell violation counts and
  `J` values, the witness-depth summary (1293 witnesses, all at `n-k`), the
  exact-equality window rows, and the sha256 pointer to the full external
  artifact.  It is NOT the full artifact.

## Reproduction

The census and its frozen artifact live in the external repo
`github.com/latifkasuli/mca`, commit `e16dd12`:

```sh
PYTHONPATH=src python3 scripts/mca_ca_sparse_layer_census.py --quick
```

(`--quick` < 2 min: reproduces the killer counterexample with its r=2 control
and the exact-equality window instances; numpy is an optional fast path — the
pure-Python fallback is byte-identical.)  Full frozen artifact:
`runs/mca_ca_sparse_layer_census.json`
(671914 bytes, byte-stable across runs, CI pin
`tests/test_certificates.py::test_mca_ca_sparse_layer_census_quick`):

```text
sha256 = e7c559652692fdf4d62a1c2a5cf1c60f6ab6a9b216300b7ab87315b8254dc98b
```

Writeup: `docs/mca-ca-sparse-layer-census.md` in the same repo.

## NON-CLAIMS

- Toy scale only; no statement for general `(n,k,q)`, no bound past the
  censused radii, no deployed-row statement.
- All oracles are exact but exponential; nothing here scales.
- The `J`-law is a measured correlation across 8 cells, not a proved bound.
- Row C r=6 densities come from one targeted 28-challenge sample (estimates);
  every A/B cell is exhaustive over all 17 slopes.
- No GPU search result; no `q_chal` soundness division.
