# E35 [face 2] — weight-2 abundance vs symmetry-stratum membership

- **Status:** EXPERIMENTAL / toy evidence (sampled census, not exhaustive,
  not a proof).
- **Roadmap link:** wave-5 probe E35, `evidence_plan_codex.md`; prize-DAG
  node `f_weight2_inverse` (FACE-2 CORE: abundant weight-2 words force
  symmetry), feeding `f_sparse_rank_split`.
- **Verifier:** `experimental/scripts/verify_e35_weight2.py`
  (stdlib-only, deterministic seeds, < 1 s; 28/28 families + global
  PASS on 2026-07-03).
- **Predecessors:** E30 (machinery + conventions, dihedral odd-j parity
  refinement), E9 (weight-2 base rates), E25 (dihedral audit).

## Object

E30 conventions: `K = F_17`, `H = mu_16`, `n = 16`; flats are
linear-dim-`d` subspaces of `K[X]_{<=j}`, `d in {3,4,5}`, `j in {3,4,5}`.
Per flat, two EXACT counts of minimal weight-2 dual supports (pairs of
nonzero proportional evaluation columns; zero columns = weight-1 words =
the common-root strip):

```text
w2   raw       sum C(m,2) over projective column classes
w2m  matching  sum floor(m/2)  (max pairwise-DISJOINT supports)
```

Independently, symmetry-stratum membership is tested against every
nontrivial element of Dih_16 (15 rotations `x -> ux`, 16 reflections
`x -> b/x` — all subgroup conjugates), extracting the character data:

```text
MULT       c_{ux} = c_x            (the literal g(X^M) stratum)
MULT-PROJ  c_{ux} = rho c_x, rho = u^e constant   (X^e g(X^M))
DIH        c_{b/x} = c x^k c_x, c^2 b^k = 1: even k = the literal
           X^e g(X^M + b^M X^-M) form (k = -2e); odd k = the odd-j
           anti/reciprocal form lambda_a = -+ a^{-j+2m} lambda_{a^-1}
           (E30 finding 1); both parities = both signs of c
sym_lit = MULT or DIH;   sym_ext = MULT-PROJ or DIH
```

Anomaly detectors for shapes outside the finite ledger (full
proportional matching with non-constant rotation ratio or non-monomial
reflection ratio): **0 hits across all 1452 flats**.

Families (seeds `E35:<family>:<j>:<d>`): 2 full-space calibration rows
(RS[16,4], RS[16,5]); 100 random + 50 `D_j`-span flats per
`(j,d)` grid point; the EXHAUSTIVE in-degree symmetric census at d = 3
(all dim-3 strata: j=4: 17 = 16 b-reciprocal + `{1,X^2,X^4}`; j=5: 50 =
16 odd-k quintic-reciprocal + 32 even-k embedded quartic-reciprocal
`R` and `X*R` + `{1,X^2,X^4}` + `{X,X^3,X^5}`); 75 carriers (sym
sub-flat + random extension, d = 4, 5); 80 near-pencils
(`span{q, qX, ..., v}`, rank-1 clusters, no symmetry, no weight-1); 360
perturbed census members (s = 1, 2, 3 random basis cells bumped).

## (1) Joint distribution (1423 stripped flats): w2m x membership

```text
w2m    nonsym   sym_ext_only   sym_lit
0        923         -            -
1        338         -            -
2         75         -            -
3         12         -            -
7          -         -           31
8          -         2           42
```

The band 4-6 is EMPTY; sub-abundant weight-2 words (w2m <= 3) are all
accidental-twin background at E9/E30 rates (random flats: w2m hist
74/20/4/2 at j4d3), and every flat with w2m >= 4 is symmetric.

## (2) THE ABUNDANCE THRESHOLD

```text
count    stratum list          W*   nonsym max   sym floor   margin
w2m      sym_ext (projective)   4        3           7       3 (robust)
w2 raw   sym_ext (projective)   7        6           7       0 (fragile)
w2m/w2   sym_lit (literal)     --        8           7       FAILS
```

**W\* = 4 disjoint minimal weight-2 supports** (post common-root strip)
forces symmetry-stratum membership in this sample — with a factor-2
gap to the symmetric floor 7. The RAW count separates with zero margin
(near-pencils reach 6 vs floor 7): the inverse theorem's abundance
hypothesis should count DISJOINT supports (matching number), or
equivalently strip rank-1 clusters first, not raw supports.

## (3) Falsifier hunt: two ledger corrections, no S9

1. **The literal stratum list is FALSIFIED by the twisted pullback.**
   `{X, X^3, X^5}` (j = 5) carries 8 disjoint weight-2 supports on the
   `{x,-x}` pairs with lambda-ratio +1, and is in NO `g(X^M)` and NO
   dihedral stratum (its reflection ratio test fails for every b).
   It IS `X e(X^2)`-shaped: the multiplicative clause of
   `f_weight2_inverse` must be stated projectively, `X^e g(X^M)`, like
   the dihedral clause already is. (Same class as E30's ratio-caveat:
   these words are `w2_coset_generic_ratio` there, invisible to clause
   (iii).) With the projective restatement, membership is restored.
2. **Rank-1 clusters (near-pencils) break RAW abundance.**
   `span{q, qX, v}` with `deg q = 4` has one column class of size 4:
   C(4,2) = 6 raw supports, matching only 2, no symmetry, no weight-1
   word — and these occur in the wild (7 of the `b_djspan|j5d3` flats
   reach w2m = 3, one shows the same `(4,)` class profile). Raw-count
   abundance at 6 sits one below the symmetric floor by luck of the
   field size; the matching count demotes them to the background band.
3. **No abundant asymmetric flat.** No stripped flat with w2m >= 4 is
   outside every (projectively stated) stratum; no non-character ratio
   matching exists anywhere in the sample. `f_weight2_inverse`
   survives as restated; conclusion space stays finite.

Odd-j structural fact (strip interaction): every maximal
quintic-reciprocal stratum (odd k = 11) carries a FORCED weight-1 word
— for odd k the two reflection fixed points `x0, -x0` have ratio
product `(c x0^k)(c(-x0)^k) = -1`, so exactly one is a forced zero
column. Post-strip, odd-j symmetric abundance lives entirely in the
even-k embedded strata and the pullbacks; the odd-k strata sit behind
the strip (consistent with E30 finding 1's `X+1` divisibility).

## (4) Near-symmetric collapse: all-or-nothing

Perturbing s random basis cells of a d = 3 symmetric flat
(60 trials per (j, s); "sym" = perturbation landed inside the stratum):

```text
           still-sym    nonsym w2m distribution        nonsym max
j=4 s=1      11/60      0:28  1:16  2:5                    2
j=4 s=2       5/60      0:33  1:19  2:3                    2
j=4 s=3       1/60      0:33  1:24  2:2                    2
j=5 s=1       6/60      0:37  1:15  2:2                    2
j=5 s=2       0/60      0:33  1:23  2:3  3:1               3
j=5 s=3       1/60      0:36  1:18  2:4  3:1               3
```

One generic cell already collapses w2m from 7-8 to <= 2: surviving
pairs are the <= 2 root-pairs of the perturbation's anti-symmetric
part, so there is NO gradual degradation band — the 4-6 gap in the
joint table is structural, not sampling luck. The inverse theorem's
stability constant is maximal at this scale: any flat even one
generic vector away from a stratum is already at background abundance.

## Interpretation (DAG actions)

(a) Restate `f_weight2_inverse`'s conclusion strata projectively:
`X^e g(X^M)` and the `(b, k, c)`-dihedral family with `c^2 b^k = 1`
(both parities, both k-parities) — the literal list is falsified by
finding 1. (b) State the abundance hypothesis as >= W* pairwise-
DISJOINT minimal weight-2 supports (or strip rank-1 clusters alongside
the tangent strip): raw counting has zero margin by finding 2.
(c) Toy calibration for the constant: W* = 4 = half the symmetric
floor at n = 16. (d) No S9 event.

## Limitations

Sampled (1452 flats), single toy scale n = 16, so "poly(n) abundance"
is calibrated only as a floor-vs-background gap (7-8 vs 3); for
j <= 5 all in-degree symmetry strata have dim 3, so stratum
CONTAINMENT is only exercised at d = 3 (d >= 4 columns are pure
falsifier hunts — all clean); perturbations are basis-cell bumps, not
a metric on the Grassmannian; the symmetric census is exhaustive for
dim-3 strata but the sampling frame, as in E30, is not the
Grassmannian measure.
