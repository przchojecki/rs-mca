# capg-split-pencil-refutation: the recorded split-pencil census correction fails at interior profiles

**Status: COUNTEREXAMPLE / AUDIT** (base `2b1a7e2`)

## Claim

`prob:capg-split-pencil-B` — the recorded correction of the conceded-false
literal `prob:capfp-split` — fails **verbatim** at interior balanced
profiles, and `prob:capg-active-BC` fails by inheritance (it asks to prove
the same census). Consequently the hypothesis of
`prop:capg-final-active-package` is unsatisfiable as stated: its finite
forms cannot "hold with explicit constants below the margins in
`cor:capg-adjacent-pairs`".

- **Finite deployed form** (the operative one — the problem's own text
  replaces `e^{o(n)}` by exact constants at the `cor:capg-adjacent-pairs`
  values): at the KoalaBear census row `n = 2^21`, `K = 2^20`,
  `m = 1116047`, `w' = 67471`, a single codeword ray at distance `w'+2`
  contributes `C(n-w'-2, m)` (an exact 2,015,083-bit integer) against a
  corrected budget `max(1, M_B(w'+2), C(n,omega) q^{1-w'}) < 2^26` — a
  factor `>= 2^2015057` over budget, vs the +3.3/+22.2-bit margins the
  finite form must meet. (Conservatively including the base-field term
  `C(n,omega) p^{1-w'} ~ 2^66.9` from the mutatis-mutandis models still
  leaves `>= 2^2015015`.)
- **Asymptotic form**: along fixed-rate families with `e = Theta(n)` inside
  the interior range, the excess is `e^{Theta(n)}`, not `e^{o(n)}`.
- **Toy mechanism exhibit** (`F_73`, `q = p` prime so the subfield-floor
  mechanism is vacuous and the codeword-ray mechanism is isolated;
  assumption-free enumeration of all `C(24,9) = 1307504` divisors):
  censuses 15504 / 3877 / 818 at profiles `d1 = 4 / 5 / 6` against literal
  budget `1307504/5329 ~ 245.36` and interior `M_B(5) = 11767536/28398241`,
  `M_B(6) = 47070144/2073071593` (ceiling variants 16, 136 —
  verdict-equivalent). The excess strata are exactly codeword rays; the
  ray-deduplicated counts (1 / 2 / 3) sit far below every budget. A fixed
  `n = 24` cannot refute an `e^{o(n)}` statement; the toy pins the
  mechanism, not the verdict.

## The new ingredient: profile localization

`cor:raw-bc-fails` already prints the ray mechanism (`Cen = C(n-d, m)` from
one codeword) but carries no profile statement, and
`thm:capfr1-near-rational-dichotomy(i)` proves only the `d1 <= w'` branch.
The missing fact, which places the blowup inside the corrected problem's own
range `w'+2 <= d1 <= floor((n-K+1)/2)`:

**Lemma (profile localization).** Let `U : D -> F` be at Hamming distance
exactly `e` from a codeword `c` (`deg c < K`), with error set `E`, and
suppose `2e <= n-K+1`. Then the shifted-Popov profile of
`M_U = {(W,N) : W(x)U(x) = N(x) for all x in D}` satisfies `d1(U) = e`.

*Proof.* (<=) The locator pair `(Lambda_E, Lambda_E c)` lies in `M_U` with
weighted degree `max(e, e + deg c - (K-1)) = e`. (>=) Let `(W,N) in M_U`
be **nonzero** with weighted degree `d`, so `deg W <= d`,
`deg N <= d + K - 1`. Then `N - Wc` vanishes on the `n - e` agreement
points; if `d < n - e - K + 1`, its degree bound `d + K - 1 < n - e`
forces `N = Wc` (and then `W != 0`, else the pair would be zero), whence
`W(U - c) = 0` on `D`, so `W` vanishes on all of `E` and `deg W >= e`,
i.e. `d >= e`. Since `2e <= n-K+1` gives `e <= n - e - K + 1`, any `d < e`
also satisfies `d < n - e - K + 1` — contradiction. QED.

The pair `(d1, d2) = (e, n-K+1-e)` is balanced on the whole range, so the
representation is a legitimate `prop:capfr1-detrep` instance at **every**
interior profile: choosing `e = d1` plants the ray blowup at any prescribed
`d1`. `M_B(d1)` prices the pigeonhole witnesses at agreement `m' = K-1+d1`
(each contributing `C(m', m)`), but the near-codeword ray sits at agreement
`n - e`, contributing `C(n-e, m)` — a stratum no term in the corrected
budget models. The count is a raw `(A,B)` point count (monic normalization
kills only scalars; distinct supports in a ray have distinct root sets,
hence distinct monic `AW_1 + BW_2`), so the ray is counted with full
multiplicity — consistent with the paper's own census identity
`prop:capfr1-lattice-census(c)`. The lemma is verified exhaustively at
every planted-error toy row (`d1 = e` for `e = 4, 5, 6`) by two disjoint
routes.

## What is NOT affected, and the repair direction

`thm:saturation`, `cor:raw-bc-fails`, and every slope-count
(ray-deduplicated) object are untouched — the first two are ingredients
here. `prob:saturated-bc` explicitly demands "slope, not raw-support"
bounds and demotes the raw census to "an audit object"; its margin identity
is unaffected. The finding is precisely that the split-pencil corrections
were recorded on the with-multiplicity object — the trap
`cor:raw-bc-fails` names, resurfacing inside the corrected problems' own
interior range.

Repair direction (not claimed as a theorem): restate the missing lemma on
the ray-deduplicated count `|Ray(U;m)|` (at the toy: 1/2/3 vs 245.36). That
deduplicated statement is exactly the object `prob:saturated-bc` already
demands, so the split-pencil lane collapses into the saturated-BC lane
rather than standing as an independent route to
`prob:capfr1-normalized-band`.

## Dual routes

Generator (`verify_capg_split_pencil_refutation.py`): toy — full divisor
enumeration + shifted-weak-Popov basis of `M_U` (verified from its defining
properties: membership, `det = unit * Lambda_D`, `gcd(W_1,W_2) = 1`,
`d1+d2 = n-K+1`, distinct pivots) + cap-space parity membership + per-ray
saturation identity `Cen = sum_c C(agr, m)` + ray collinearity; deployed —
Legendre floor-sum exponents + product-tree exact binomials, all verdicts
bit-length/floor-division integer facts.

Independent checker (`verify_capg_split_pencil_refutation_check.py`, no
generator import): toy — GRS duality on complements (power-sum functionals
`sum_k lambda_k T_{j+1+k} = 0`; no Popov basis, no cap space), ray
decomposition by direct interpolation, `d1 = e` by direct rank tests plus
locator construction; deployed — Kummer carry-count exponents +
smallest-first heap merging, lgamma cross-estimates; statement pins
re-scanned with fresh line hashes.

## Self-Red-Team

- *"A toy at n = 24 can't refute e^{o(n)}."* Correct, and not claimed: the
  refutation is the finite deployed form (the problem's own text replaces
  `e^{o(n)}` by exact constants at the `cor:capg-adjacent-pairs` values)
  plus the `e^{Theta(n)}` family; the toy pins the mechanism only.
- *"Isn't the raw count a strawman — maybe the problem means slopes?"* The
  statement counts `(A,B)` pairs under monic normalization, which kills
  only scalars; the paper's own census identity
  (`prop:capfr1-lattice-census(c)`) and floor derivation
  (`prop:capg-census-floor`) use the same with-multiplicity reading. The
  slope reading is exactly the repair direction, and it is
  `prob:saturated-bc`, not this problem.
- *"Maybe `M_B` was transcribed with a ceiling that changes the verdict."*
  Both variants are evaluated at toy and deployed scale; verdicts agree.
- *"Maybe `d1 = e` only holds generically."* It is a theorem
  (unconditional, five lines, above), verified exhaustively at the toy by
  two disjoint routes; no genericity enters the deployed claim.

## Reproducibility

```
python3 experimental/scripts/verify_capg_split_pencil_refutation.py --emit-defaults   # ~7 s
python3 experimental/scripts/verify_capg_split_pencil_refutation.py --check           # ~7 s
python3 experimental/scripts/verify_capg_split_pencil_refutation_check.py             # ~17 s
```

stdlib only, deterministic (seed 20260710; toy words and error data are
frozen in the certificate), byte-stable regeneration, no timing in any
frozen output. Certificate:
`experimental/data/certificates/capg-split-pencil-refutation/capg_split_pencil_refutation.json`.
