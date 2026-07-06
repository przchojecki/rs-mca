# Finite Reachability Map for `prob:band`

## Claim

A fixed-parameter exact-integer census of split-locator incidence or random-pair
occupancy sits in a layer already controlled by the v13 fixed-parameter
theorems. Such a census is still useful as a reproducibility and scope check,
but it does not reach the growing-dimensional, worst-case aperiodic content
named by `prob:band` and `rem:v13-conjf-open`.

This note states the following method-boundary observation in a fileable form:
fixed-dimensional and fixed-row packets confirm proved bounds; the residual
open layer is the growing-dimensional regime.

## Status

EXPERIMENTAL / SCOPE-MAP. This is not a proof of the aperiodic band conjecture,
not a claim of undecidability, and not a claim about all possible methods. It
maps the reach of the fixed-parameter finite-census method only.

## Pinned Statements

- `thm:v13-fixeddim`: if `W <= K[X]_{\le j}` has vector-space dimension
  `d+1`, `0 <= d <= j`, and is gcd-trivial on `H`, then
  `|PP(W) cap Dloc_j(H)| <= binom(|H|, d)`. With common root set `C0`, the
  bound refines to `binom(|H|-|C0|, d)`. Its common-root refinement invokes
  `lem:v13-gcd`; the surrounding fixed-stratum reductions also name
  `lem:v13-quot-pullback`, `lem:v13-dim1`, and `thm:v13-dim2`.
- `thm:v13-dim2`: under hyperplane concurrency, projective planes satisfy
  `|PP(W) cap Dloc_j(H)| <= binom(|H|,2)/(j-1)`, and the denominator improves
  to `binom(j,2)` when the evaluation lines are pairwise distinct. The
  hyperplane formulation is `lem:v13-concurrency`.
- `thm:v13-first-moment`: for random independent words,
  `E N_A = binom(n,j) (1-q^{-t}) q^{1-t}`.
- `thm:v13-second-moment`: `E N_A^2` is the ordered-overlap sum over
  `c=max(0,2j-n),...,j` with `h(c)=max(0,t-j+c)` and the displayed
  probability `P_h`.
- `rem:v13-conjf-open`: the primitive Conjecture-F core is
  dimension-growing; common-root, quotient-periodic, dimension-one,
  projective-plane, and every fixed-dimensional stratum are paid by the cited
  reductions, while the growing-dimensional incidence theorem needed for the
  aperiodic band remains open.
- `prob:band`: in the open band
  `k + 2n/N < a < n - floor((n-k)/3)`, bound the number of MCA-bad finite
  slopes whose witness supports are aperiodic by a polynomial independent of
  `q`; the TeX states this as a two-outcome open problem.

## Finite Check

`experimental/scripts/verify_finite_reachability_map.py` exhausts the listed
fixed rows and emits
`experimental/data/certificates/finite-reachability-map/finite_reachability_map.json`.
`experimental/scripts/verify_finite_reachability_map_check.py` independently
recomputes the counts and confirms the cited labels exist in the current TeX.

| Row | Object | Census value | Proved bound | Result |
| --- | --- | ---: | ---: | --- |
| `F17_mu16_j4_d1` | fixed-dimensional locator incidence | 2 | 16 | PASS |
| `F17_mu16_j4_d2` | fixed-dimensional locator incidence | 15 | 120 | PASS |
| `F17_mu16_j4_d3` | fixed-dimensional locator incidence | 153 | 560 | PASS |
| `F97_mu16_j5_d4` | fixed-dimensional locator incidence | 390 | 1820 | PASS |
| `F13_mu12_j4_d2` | fixed-dimensional locator incidence | 10 | 66 | PASS |
| `F17_mu16_j5_d2_common_root_refinement` | common-root refinement | 24 | 91 | PASS |

The small random-pair moment rows also match the proved formulas exactly:

| Row | Exact `E N_A` | Exact `E N_A^2` | Result |
| --- | ---: | ---: | --- |
| `F5_mu4_j2_t1` | `24/5` | `24` | PASS |
| `F5_mu4_j2_t2` | `144/125` | `43056/15625` | PASS |

## Boundary

Finitely decidable layer: for fixed `n,j,d,t` or a fixed common-root datum, the
incidence or moment quantity is finite and exactly enumerable. In the rows
above, the enumerated values respect `thm:v13-fixeddim`, the common-root
refinement, `thm:v13-dim2`, and the exact moment formulas. A d=3 or d=4 census
of this kind is therefore in the same layer: it checks a fixed parameter
instance already covered by a proved statement.

Asymptotically open layer: `rem:v13-conjf-open` identifies the remaining
Conjecture-F core as dimension-growing, and `prob:band` asks for a worst-case
aperiodic slope bound polynomial in `n` and independent of `q` throughout the
open agreement band. That is not tested by holding the dimension and row size
fixed and enumerating the resulting finite set.

Collapse statement for this method: a fixed-parameter finite census can confirm
the cited proved bounds or catch an implementation mismatch in its own row. It
does not touch the growing-dimensional open layer unless the object itself is
changed to that regime.

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_finite_reachability_map.py --emit-defaults
py -3.13 experimental/scripts/verify_finite_reachability_map.py --check experimental/data/certificates/finite-reachability-map/finite_reachability_map.json
py -3.13 experimental/scripts/verify_finite_reachability_map_check.py --check experimental/data/certificates/finite-reachability-map/finite_reachability_map.json
```

The certificate carries `claim_boundaries`, `evidence_type=FULL_FINITE_CENSUS`,
and the required degeneracy-detector fields. Its top-level scope field is
marked novel because the contribution is the method boundary, not a new
fixed-d incidence theorem.

## Self-Check

An adversarial reading could say this packet merely confirms known theorems.
That is correct for the finite rows, and the note treats that as the point: the
claimable contribution is the explicit scope boundary, not any new bound inside
the fixed-dimensional layer.
