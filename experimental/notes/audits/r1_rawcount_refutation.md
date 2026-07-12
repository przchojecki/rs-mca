# r1-rawcount-refutation: the raw R1 support-count model fails; the repair is the slope/ray-deduplicated LineRay count

**Status: COUNTEREXAMPLE / AUDIT** (base `36de5bf`)

| item | value |
| --- | --- |
| refuted object | `prob:capfp-R1` at the raw (with-multiplicity) rank-one support count, including the corrected mutatis-mutandis model of `prob:capg-split-pencil-B` |
| mechanism | planted near-codeword-slope line: ONE slope, ONE codeword ray, `C(n-w'-2, m)` supports |
| deployed margin | `#R1 >= 2^2015082.59` vs corrected model `2^35.92`: factor `>= 2^2015046` (exact bit-length fact) |
| sibling `prob:capfr1-rank-one-census` | REFUTED-WITH-AMBIGUITY-FOOTNOTE ("all paid cells" is not a closed printed list) |
| repair | record R1 on the slope/ray-deduplicated `|LineRay|` count; the pole-line floors survive verbatim under that reading |
| certificate | `experimental/data/certificates/r1-rawcount-refutation/r1_rawcount_refutation.json` |

**Use Rule.** Downstream material must not cite `prob:capfp-R1` (or the
corrected R1 model in `prob:capg-split-pencil-B`'s mutatis-mutandis clause)
as a plausible per-line bound on the raw rank-one *support* count: that
object equals the with-multiplicity LineRay census and blows up by
`e^{Theta(n)}` on planted lines.  Cite the slope-count / ray-deduplicated
form instead.  This packet cleans up the R1 waypoint; it is **not** a final
frontier theorem, and it does not touch `thm:capfp-slope-elim`(c) --- the
inequality `N_MCA-bad <= #R1` remains true (it just stops being useful at
the raw reading).

## Claim

`prob:capfp-R1` --- "Prove, for every line at band agreements,
`#R1(u,v;m) <= e^{o(n)} max(1, C(n,m) q^{-(w-1)})`, with the finite form
fitting under the deployed budget at `a_0+1`" --- fails **verbatim**, and it
still fails after the recorded correction (the mutatis-mutandis clause of
`prob:capg-split-pencil-B`: model
`max(1, C(n,m) p^{-w'}, C(n,m) q^{-(w'-1)})` per line, "the middle term
achieved by the non-B-rational pole lines of `prop:capg-census-floor`(c)").

- **Finite deployed form** (the operative one --- the problem's own text
  demands a finite form under the deployed budget): at the KoalaBear census
  row `n = 2^21`, `K = 2^20`, `m = 1116047`, `w' = m-K = 67471`,
  `omega = 981105`, `p = 2^31-2^24+1`, `q = p^6`, a planted line with one
  near-codeword slope at distance `e = w'+2 = 67473` has
  `#R1 >= C(n-w'-2, m)`, an exact 2,015,083-bit integer
  (`log2 ~ 2015082.59`).  The corrected model's binding middle term is
  `ceil(C(n,m) p^{-w'}) = 65065153468 ~ 2^35.92`; the `q`-term is `< 1`
  (bit-length proof: `q^{w'-1} >= 2^{185(w'-1)} = 2^12481950 > C(n,m)`).
  Over-model factor `>= 2^2015046` (floor-division bit-length fact; display
  `2^2015046.67`).  Against the literal `q`-scale model
  `max(1, ~2^-10453966) = 1` the factor is `>= 2^2015082`.
- **Asymptotic form**: along fixed-rate families with `e = Theta(n)` the
  excess is `e^{Theta(n)}`, not `e^{o(n)}`.
- **Toy mechanism exhibit** (`F_73`, `q = p` prime so the subfield/pole-line
  mechanism is vacuous and the one-slope mechanism is isolated;
  assumption-free scan of all `C(24,15) = C(24,9) = 1307504` supports per
  line): planted lines at `e = 4/5/6` have `#R1 = 15709/4115/1116` against
  the per-line model `1307504/5329 ~ 245.36` --- **FAILS** --- while the
  random control line has `#R1 = 218` --- **HOLDS**.  The failure is the
  plant, not a trivially wrong model.  The planted slope carries
  `15505/3877/818 >= C(n-e, m) = 15504/3876/816` supports; common supports
  are zero on every line.  A fixed `n = 24` cannot refute an `e^{o(n)}`
  statement; the toy pins the mechanism, not the verdict.

## The verbatim anchors and the exclusion sweep

`thm:capfp-slope-elim` defines rank-one supports (`alpha(T), beta(T)`
proportional, not both zero, `beta(T) != 0`) and part (c) proves
`N_MCA-bad(u,v;m) <= #R1(u,v;m)` by injecting slopes into supports ---
nothing caps how many supports one slope contributes.  `prob:capfp-R1`'s
quantifier is bare: "for every line at band agreements"; there is **no
profile clause** (unlike `prob:capg-split-pencil-B`'s interior clause) and
no exclusion that touches the plant:

- "first match" / "first-match" / "strip": zero hits in the entire source.
- Tangent in this lane means COMMON support (`alpha = beta = 0`, removed by
  slope-elim(b)); the planted line has zero common supports (verified at
  toy; forced generically at deployed scale by the freedom count below).
- The printed paid-cell list (tangent, quotient, extension-pole,
  common-GCD, quotient-pullback, fixed-dimensional, sunflower, SPI ---
  `sec:capfr1-programme` preamble) contains no near-codeword-slope cell;
  sunflower/planted cells are LIST-side and scope `prob:capfp-A`, not R1.
- "Primitive" in every printed sense (non-quotient-periodic, not a
  pullback, no member proportional to a B-rational datum ---
  `rem:capg-subfield-scope`(iii)): the planted line is primitive under all
  of them; generic `v` kills B-rationality outright.
- Band membership: deployed `m/n ~ 0.532` sits inside the `m > n/2` band.

## The construction and the freedom count

Pick a codeword `c0` and an error `eta` of weight `e = w'+2` with
challenge-field values; set `U := c0 + eta`, pick `z0 != 0`, and put
`u := U - z0 v`.  For every slope `z != z0` (including infinity) the word
`u + zv = U + (z-z0)v` is uniform in `v`, so by the first moment
`Pr_v[cen(u+zv;m) > 0] <= C(n,m) q^{-w'}`; the union over all `q` slopes is
`<= 2 C(n,m) q^{-(w'-1)} < 1` (deployed: certified as the bit-length fact
`C(n,m).bits + 1 <= 185 (w'-1)`).  Hence `v` **exists deterministically**
with every other slope census-empty, no common supports (a common support
would put `v`'s own census, the infinity slope, above zero), and the line
challenge-field-primitive.  Then every `m`-subset of the agreement set of
`(U, c0)` is a rank-one support of slope `z0`, and

```
#R1(u,v;m) = sum_c C(agr(U,c), m) >= C(n-w'-2, m).
```

**Why `e = w'+2` exactly:** `e <= w'` is priced by the near-rational branch
(`thm:capfp-dichotomy`(i) + `cor:capfp-line`); `e = w'+1` is the boundary
profile delegated to (Q) (`rem:capg-boundary-offbyone`); `e = w'+2` is
interior and unpriced.  By profile localization (the #518 lemma: a word at
distance exactly `e` from a codeword with `2e <= n-K+1` has shifted-Popov
profile `d1 = e`; deployed `2e = 134946 <= n-K+1 = 1048577`), the planted
word sits at `d1 = w'+2`, outside every priced convention.  Verified at
every planted toy word (`d1 = e` for `e = 4, 5, 6`) by two disjoint routes.

## Mechanism novelty: the opposite of the pole-line floor

Upstream's own refutation of the literal R1 model (the subfield concession
of `sec:capg-subfield` and `prop:capg-census-floor`(c)) is
**many-slopes-one-support-each**: each fiber member of the pole line
carries its own slope at agreement exactly `m`.  The corrected middle term
`C(n,m) p^{-w'}` was calibrated to that floor.  The plant is the
**opposite** configuration --- one slope, one codeword ray, `C(n-w'-2, m)`
supports at agreement `n-w'-2` --- and no term in either model prices it.
It is the same census-saturation insight as the #518/#666 packets (the
paper's own "m-th binomial moment" prose at `prop:capfp-lattice`(c)),
propagated to the per-line object.

Two clauses of `rem:capg-subfield-scope` are directly contradicted:

- (ii) "the corrected R1 model is tight at the floors": tight at THEIR
  pole-line floors, blind to ours --- the planted line exceeds the
  corrected model by `2^2015046`.
- (iii) "for genuinely challenge-field-primitive representations ... the
  original q-scale models remain the plausible targets": the planted line
  is primitive in the printed sense and has `#R1 >= 2^2015082.59` against
  `max(1, 2^-10453965.87) = 1`.

## The identity: R1 IS the with-multiplicity LineRay census

Both routes verify, at every slope of every toy line,

```
mult(z) = sum_{c in List(u+zv; m)} C(agr(u+zv, c), m),   hence
#R1(u,v;m) = sum_z sum_c C(agr(U_z, c), m)     (zero common supports).
```

So the raw R1 count is exactly the with-multiplicity LineRay census: every
`(slope, codeword-ray)` pair is counted `C(agr, m)` times.  The blowup is
pure multiplicity, not new slopes: the planted toy lines hit 72/69/70
slopes and 206/210/211 line-rays (vs 68 slopes / 218 line-rays for the
control) while the raw counts blow up to 15709/4115/1116 vs 218.

## Sibling grading: `prob:capfr1-rank-one-census`

Graded **REFUTED-WITH-AMBIGUITY-FOOTNOTE**.  Its guard is "After all paid
cells and common supports have been removed"; "all paid cells" is not a
closed printed list inside the statement.  On the printed paid-cell list
(no near-codeword-slope cell) the sibling fails with the same margins; an
unprinted reading that pays the plant would have to introduce a new cell
--- which is exactly the repair below, not the current text.

## What is NOT affected, and the repair direction

`lem:capfp-functionals`, `thm:capfp-slope-elim` (including part (c)),
`thm:capfp-dichotomy`, and every unconditional reduction are untouched
(`rem:capg-subfield-scope`(i) stands).  The pole-line floors of
`prop:capg-census-floor` are untouched --- they are the opposite mechanism
and they are floors, not models.

**Repair direction (not claimed as a theorem):** record R1 on the
slope/ray-deduplicated `|LineRay_E|` count.  The ray-collapse theorem of
the split-pencil lane (PR #666;
`experimental/notes/thresholds/split_pencil_ray_collapse.md` once
integrated) proves dedup census = list count per slope; under the
deduplicated reading upstream's own pole-line floors survive verbatim
(their supports each carry distinct slopes), and at the toy the
deduplicated per-line counts (206/210/211 planted, 218 control) sit
**below** the corrected model `245.36` at every line, including the planted
ones.  The deduplicated restatement is the object the slope-count lane
already demands, so the R1 waypoint collapses into that lane rather than
standing as an independent raw-count problem.

## Dual routes

Generator (`verify_r1_rawcount_refutation.py`): toy --- full `C(24,9)`
support scan classifying common/beta-zero/rank-one(z)/rank-two via the
`w = 3` interpolation functionals; every slope multiplicity cross-checked
against the independent interpolation-route list census of `U_z`; planted
profiles `d1 = e` via shifted-weak-Popov reduction verified from its
defining properties (membership, `det = unit * Lambda_D`,
`gcd(W_1,W_2) = 1`, `d1+d2 = n-K+1`, distinct pivots); deployed ---
Legendre floor-sum exponents + product-tree exact binomials, all verdicts
bit-length/floor-division integer facts; frozen line menu (words, planted
codeword coefficients, error positions, `z0`) in the certificate.

Independent checker (`verify_r1_rawcount_refutation_check.py`, no generator
import): toy --- **no rank-one scan**; every finite slope of every line is
censused by GRS duality (power-sum functionals), hits grouped by
interpolated codeword with per-ray saturation `count = C(agr, m)`, stored
multiplicities verified as list censuses, absent slopes verified empty;
common/beta-zero recomputed as `|hits(u) cap hits(v)|` and
`|hits(v)| - common`; `d1 = e` by direct rank tests plus locator
construction; deployed --- Kummer carry-count exponents + smallest-first
heap merging, lgamma cross-estimates; statement pins re-scanned with fresh
line hashes.

Deployed cross-validation: the same pipeline reproduces the paper's own
printed floors at its orientation row `(K, m) = (k, 1116046)`:
boundary `2^67.0958` (paper prints "67.1"), first interior `M_B`
`2^56.0111` (paper prints "56.0").

## Self-Red-Team

- *"A toy at n = 24 can't refute e^{o(n)}."*  Correct, and not claimed:
  the refutation is the finite deployed form (the problem's own text
  demands one at `a_0+1`) plus the `e^{Theta(n)}` family; the toy pins the
  mechanism only.
- *"Maybe the intended reading of R1 already deduplicates by slope."*  The
  printed object is `#{rank-one supports}` --- a support count; the proof
  of slope-elim(c) injects slopes INTO supports, and the paper's own floor
  derivation (`prop:capg-census-floor`(c)) counts fiber members, i.e.
  supports.  The deduplicated reading is exactly the repair direction, and
  it is not the printed statement.
- *"Maybe the paid cells exclude near-codeword lines."*  The printed cell
  list has no such cell (checked cell by cell); tangent in this lane means
  common support, and the plant has none.  For the capfr1 sibling, whose
  guard is open-ended, we grade with an explicit ambiguity footnote
  instead of claiming an unambiguous refutation.
- *"Doesn't the corrected model's middle term price this?"*  The middle
  term `C(n,m) p^{-w'} ~ 2^35.92` was calibrated to the pole-line floor
  (many slopes, agreement exactly `m`).  The plant sits at agreement
  `n-w'-2` with `C(n-w'-2, m) ~ 2^2015082.59` supports on one slope ---
  off by two million bits.
- *"Maybe v with the required hygiene doesn't exist."*  The union bound
  over all `q` slopes is certified below 1 as an exact bit-length fact;
  existence is deterministic, not heuristic.  At the toy the hygiene
  deliberately fails (`q = 73` is too small) and the extra slopes are
  reported and cross-checked --- they only add to `#R1`.
- *"Is the planted word maybe in a priced profile branch?"*  `d1 = e =
  w'+2` by profile localization (`2e <= n-K+1` holds with room), verified
  at toy by two disjoint routes; `e <= w'` and `e = w'+1` are exactly the
  priced/delegated branches, which is why the plant sits at `w'+2`.

## NON-CLAIMS

- No defect in `lem:capfp-functionals`, `thm:capfp-slope-elim`,
  `thm:capfp-dichotomy`, or any unconditional reduction.
- No defect in the pole-line floors of `prop:capg-census-floor`; under the
  slope/ray-deduplicated reading those floors survive verbatim.
- No refutation of the slope-count / `|LineRay_E|` (deduplicated) form of
  R1 --- that is the repair direction and the toy evidence supports it.
- No unambiguous refutation of `prob:capfr1-rank-one-census` (ambiguity
  footnote above).
- No claim against the frontier statements, `prob:capfp-A`, or the
  list-side sunflower cells.
- Not a frontier theorem: this packet cleans up the R1 waypoint.

## Reproducibility

```
python3 experimental/scripts/verify_r1_rawcount_refutation.py --emit-defaults   # ~2.5 min
python3 experimental/scripts/verify_r1_rawcount_refutation.py --check           # ~2.5 min
python3 experimental/scripts/verify_r1_rawcount_refutation_check.py --check     # ~2.5 min
```

stdlib only, deterministic (seed 20260712; the full line menu --- words,
planted codeword coefficients, error positions, `z0` --- is frozen in the
certificate), byte-stable regeneration, no timing or machine data in any
frozen output.  Certificate:
`experimental/data/certificates/r1-rawcount-refutation/r1_rawcount_refutation.json`.

## Provenance

Base `36de5bf` (`experimental/cap25_cap_v13_raw.tex`, 10083 lines); all
eight statement pins are line-hashed in the certificate and re-scanned by
the checker.  Design lineage: the #518 packet (codeword-ray refutation of
`prob:capg-split-pencil-B` at interior profiles) supplies the ray mechanism
and the profile-localization lemma; the #666 lane supplies the ray-collapse
(dedup = list) repair target; this packet propagates the mechanism to the
per-line rank-one object `#R1` of `prob:capfp-R1`.
