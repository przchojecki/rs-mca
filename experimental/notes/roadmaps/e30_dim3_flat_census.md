# E30 [axis D] — dimension-3 flat census under the enlarged taxonomy

- **Status:** EXPERIMENTAL / toy evidence (sampled census, not exhaustive,
  not a proof).
- **Roadmap link:** wave-4 probe E30, `evidence_plan_codex.md`; RK axis D
  (fixed d -> growing d, face 2's burden), `rigidity_kernel.md`.
- **Verifier:** `experimental/scripts/verify_e30_dim3_flats.py`
  (stdlib-only, deterministic seeds, ~15 s single process;
  17/17 families PASS on 2026-07-03).
- **Predecessors:** E7 (dim-2 pair-generated planes), E9/E10 (codim-1
  Grassmannian censuses), E17 (coset-union prediction), E25 (dihedral audit).

## Object

E7/E9 conventions: `K = F_17`, `H = mu_16 = F_17^*`, `n = 16`;
`D_j` = squarefree monic degree-`j` divisors of `X^16 - 1`; a flat is a
linear-dim-4 subspace `P <= K[X]_{<=j}` (projective dim 3), `j in {3,4,5}`.
For each flat the verifier enumerates the sparse dual words
(`lambda` with `sum_x lambda_x p(x) = 0` for all `p in P`) EXHAUSTIVELY
over supports of size <= 4 (2516 supports x rank checks), counts the
`D_j` points on the flat, and computes the closed-set lattice of the 16
evaluation columns (matroid flats of the rank-<=4 column matroid).

`j = 3` is exact: `Gr(4,4)` is a single flat (the whole space — the
RS[16,4] calibration row). `j = 4, 5` are stratified deterministic
samples; the full `Gr(4,5)`, `Gr(4,6)` are out of light-compute scope.

Enlarged taxonomy (flat label = first hit in priority
(i) > (iv) > (iii) > (ii) > (v) > (vi); all overlaps counted at word level):

```text
(i)   common_root       weight-1 word (common root / tangent point)
(iv)  w2_dihedral       weight-2 word on an inverse pair {a, a^-1} with
                        lambda_a = -a^{2m} lambda_{a^-1}  (dihedral
                        pullback X^e g(X^M + X^-M) shape)
(iii) w2_mult_coset     weight-2 word on {x, cx}, ord(c) <= 8, ratio -1
                        (multiplicative pullback g(X^M) shape)
(ii)  w2_twin_generic   weight-2 word with no ledger shape
(v)   w3/w4_descent     minimal words of weight 3 or 4
(vi)  spread_ge_5       dual distance >= 5
```

Families (seeds `E30:<family>:<j>` in the verifier): (a) 250 random flats
per j; (b) 250 spans of 4 random `D_j` members per j; (c) structured:
60 Hankel-kernel-extended (kernels of the `j-3` Hankel rows of sparse-word
power sums, deterministically restricted/accepted at dim 4), 60 palindromic
carriers (2- or 3-dim sub-flats of the reciprocal space + random extension
— honest label: carriers of palindromic sub-flats, since for j <= 5 the
reciprocal space itself has dim 3 < 4), 60 multiplicative-pullback-adjacent
(`g(X^2)`/`g(X^4)` space + random extension); (d) adversarial: common-divisor
pencils `q * K[X]_{<=3}` (all 16 at j=4; 40 sampled at j=5), 40 spans of
inverse-closed `D_j` members (+1 random `D_j`), 40 coset-structured spans
(`g(X^2)`-divisor spans at j=4; `(X^4-r)(X-a)` spans at j=5).

## Classification table (flats per class per family)

```text
family                 n    root  dihe  coset twin  w3    w4    >=5
j3_full_space          1    -     -     -     -     -     -     1
a_random|j4          250    -     -     -     5     224   21    -
b_dj_span|j4         250    19    1     1     11    206   12    -
c_hankel_ext|j4       60    -     -     -     -     52    8     -
c_palindromic|j4      60    -     10    -     1     26    23    -
c_pullback_adj|j4     60    -     -     21    -     22    17    -
d_common_div_pen|j4   16    16    -     -     -     -     -     -
d_inverse_closed|j4   40    2     7     1     2     19    9     -
d_coset_span|j4       40    -     1     20    -     -     19    -
a_random|j5          250    -     1     -     2     207   40    -
b_dj_span|j5         250    39    -     2     50    151   8     -
c_hankel_ext|j5       60    -     -     3     14    27    16    -
c_palindromic|j5      60    1     -     -     10    48    1     -
c_pullback_adj|j5     60    -     -     11    -     26    23    -
d_common_div_pen|j5   40    40    -     -     -     -     -     -
d_inverse_closed|j5   40    4     -     1     14    20    1     -
d_coset_span|j5       40    -     -     -     -     40    -     -
```

Calibration: the j=3 flat is exactly `spread_ge_5` with all 560 `D_3`
points and closed-set lattice 698 = the uniform-matroid `U(4,16)` count
(MDS-dual row of the RK table, as proved).

## Dihedral frequency: RARE among generic flats, dominant where built in

Weight-2 words at all are rare on generic dim-3 flats (5/250 and 3/250
random flats at j=4/5; null model ~ C(16,2) x 16/(17^4-1) ~ 0.02 words
per flat, matching). Dihedral-class flats among the 500 random flats:
1 (0.2%); among 500 `D_j`-spans: 1. In contrast the reciprocal-structured
families classify dihedral at j=4 exactly where the palindromic sub-flat
survives the random extension (10/60 carriers, 7/40 inverse-closed spans;
the survival rate matches the 1/17-per-pair kill probability of the
extension vector). CAVEAT for frequency reading: for a full-order `a` the
ratio set `{-a^{2m}}` is half of all 16 ratios, so conditional on an
accidental twin landing on an inverse pair, the dihedral shape is hit
~50% of the time by chance; the load-bearing observation is the exact
`-a^{-j}` ratio in the structured families (below), not bare set
membership.

## Fifth-shape watch: one parity refinement, no fifth mechanism

No flat and no word falls outside (i)-(vi) at the coarse level ((ii)/(v)/
(vi) are catch-alls by construction), so the watch tracked structured
supports with off-ledger coefficient shapes. Findings:

1. **Dihedral-odd words (the one recurring near-miss).** 28 inverse-pair
   weight-2 words with ratio `-a^{2m+1}` (odd power), ALL at odd j = 5,
   concentrated in the reciprocal families (13 in `c_palindromic|j5`,
   13 in `d_inverse_closed_span|j5`, 2 accidental in `b_dj_span|j5`).
   Probe: all 26 structured-family occurrences are EXACTLY
   `lambda_a = -+ a^{-5} lambda_{a^-1}` (reciprocal resp. anti-reciprocal
   shape). Explanation: an odd-degree self-reciprocal polynomial is
   forced divisible by `X + 1`, twisting the even dihedral ratio by one
   power of `a`. So clause (iv) as spec'd (`-a^{2m}`) MISSES every
   dihedral-type word at odd j; the refined clause is
   `lambda_a = -+ a^{-j + 2m} lambda_{a^-1}` (sign per reciprocal/
   anti-reciprocal component). Taxonomy-adjacent parity refinement of the
   dihedral ledger — NOT a fifth mechanism, but the clause should be
   restated before RK's clause (i) is written down.
2. Off-ledger inverse-pair words (ratio outside `-<a>` entirely): 4 total
   across ~15k words, only on low-order pairs (e.g. `{2,9}`, ord 8) where
   `-<a>` covers half the ratios; no recurring shape — consistent with the
   accidental-twin background rate.
3. Weight-3/4 words with structured supports occur at (and only at) the
   families that build them in: `d_coset_span|j5` flats each carry exactly
   16 weight-3 words, with all 2240 weight-4 words on coset-union supports
   and 1200 word-counts on inverse-closed supports — the mu_4-coset
   quotient echoing at weights 3-4, consistent with E17's coset-union
   prediction. Generic flats carry ~85 weight-4 words each (the P = 17
   noise floor: each 4-support is singular w.p. ~1/17), overwhelmingly on
   generic supports (structured fractions ~1.5-3%, at the combinatorial
   base rate). Weight-4 abundance at this field size is NOT a rigidity
   signal; the signal is the minimal weight + the structured-support excess.

## D_j points vs profile (count, mean, max per class)

Monotone in the minimal dual weight, uniformly across families — the
axis-D echo of "excess forces membership":

```text
                      j=4 (|D_4| = 1820)      j=5 (|D_5| = 4368)
common_root           mean 455 (pencils=max)  mean 95-364 (pencils 364=max)
w2 (any subclass)     mean ~152-156           mean ~20-85
w3_descent            mean ~107-109           mean ~14-21
w4_descent            mean ~94-104            mean ~8-13
```

Pencils attain exactly `C(15,3) = 455` resp. `C(14,3) = 364` points
(every squarefree monic multiple of q on the flat) — the maximally
`D_j`-rich flats are exactly the paid common-root stratum, per
Conjecture F's dim-3 instance.

## Closed-set lattice vs the fixed-d bound

All sampled lattices lie in `[284, 698]`: max 698 attained only by the
j=3 MDS row (`= 1 + 16 + C(16,2) + C(16,3) + 1`, i.e. ~ n^3/6, far below
the crude `n^{O(d)}` count at d = 4); random dim-3 flats sit at median
394 (j=4) / 429-466 (j=5) — BELOW the generic 698 because the ~107
singular 4-supports merge rank-3 closed sets. Structure only shrinks or
regularizes the lattice: pencils give exactly 577 (j=4) / 471 (j=5)
(= uniform matroid on the 15/14 non-loop columns), `d_coset_span|j5`
gives exactly 422 for every flat. No lattice-size blowup anywhere: the
fixed-d `n^{O(d)}` lattice-bound row of RK looks SLACK at dim 3, not tight.

## Interpretation (axis D)

At dim 3 the enlarged taxonomy absorbs everything sampled: the four
non-catch-all shapes (common-root, dihedral, mult-coset pullback,
plus the weight-3/4 coset-union echoes) appear exactly on the families
that build them, at otherwise null rates; the one genuine discovery is
the odd-j parity twist of the dihedral clause (finding 1). Recommended
DAG actions: (a) restate RK clause (i) dihedral ratio as
`-+ a^{-j+2m}`; (b) record `B_F`-style dim-3 data point: max `D_j` count
= the pencil value `C(n-1-(j-3), 3)`, attained only inside the paid
common-root stratum; (c) no S9 event.

## Limitations

Sampled (1577 flats), not exhaustive; toy scale n = 16 only, where the
1/17 singular-support noise floor makes weight-4 statistics weak;
"palindromic sub-flat" family is carriers (see above); the dihedral
frequency question is answered for THIS sampling frame, not for the
Grassmannian measure.
