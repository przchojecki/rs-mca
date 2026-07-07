# CAP25 v13: the popular-fiber probe confound

Target label: `prob:entropy-inverse-q` (`grande_finale.tex` l.823).

Status:
`EXPERIMENTAL(step-1 dyadic popular-fiber hierarchy at 5 exact rows; the structure verdict -- 0 AP/coset hits in 152 coprime-coordinate tests)` /
`PROVED(lem:probe-confound -- x^j on D=alpha*mu_n is gcd(j,n)-to-1 onto mu_{n/gcd(j,n)}, so a gcd(j,n)>1 probe coordinate is a quotient-scale observable; a one-paragraph corollary of prop:composite-descend + prop:q-orbit-moment + def:coefficient-scale already in the paper)` /
`AUDIT(Brick-2 R_eff(r) monotonicity per row; consistency with PR #384's aggregate-Gamma_r taxonomy)` /
`OPEN(no claim on prob:entropy-inverse-q, on any deployed row, or on skeleton steps 5-6; the null is evidence first-match removal works at toy scale, not evidence for/against the inverse theorem)`.

**Base commit pin:** `upstream/main 53bb5df` ("Add logarithmic moment route to grande finale", 2026-07-07). All line numbers are from that commit's `experimental/grande_finale.tex`.

**Verifier:** `experimental/scripts/verify_popular_fiber_probe_confound.py` (zero-arg, stdlib-only, `<90s`, `--tamper`). Five gates, independent reimplementation (imports no campaign module, reads no campaign JSON): (1) the image-collapse lemma at every probe order; (2) the dyadic hierarchy + exact `Gamma_2/3/4` + the Sec. 4 Brick-2 `R_eff` monotonicity (root-cleared, exact) at rows A, B, C, D; (3) the confound scan (0/152 coprime vs 24/132 gcd>1); (4) row E's `C(6,2)=15` coset-union identity, member-by-member, over the full `C(24,8)=735471` enumeration (plus row E's `Gamma_r` and `R_eff`); (5) the twist-stabilizer formula and the antipodal last-eyes mechanism. Exact `Fraction`/`int` throughout; floats only in human-readable log lines.

**What this is.** The first instantiation of `rem:entropy-inverse-skeleton` (l.861) **step 1** -- "a large `Gamma_r^{prim}` dyadically extracts popular fibers" -- as a per-fiber dyadic hierarchy at five toy rows, extending PR #384's aggregate `Gamma_r` view to the fiber-resolved level; plus one proved lemma that any honest **step-4** instrumentation (small-doubling / AP detection on a probe coordinate) needs. The lemma -- **the probe confound** -- says a probe coordinate `p_j` with `gcd(j,n)>1` is intrinsically low-rank/AP-prone for a structural reason that has nothing to do with the trade population it is meant to measure. With the confound controlled (coprime probe coordinates) the toy-scale null is clean: zero AP/coset hits in 152 tests, and both apparent-structure spikes are mechanically explained as quotient/planted -- exactly the cells `prob:entropy-inverse-q`'s first-match removal excludes.

**What this is not.** Not a claim on `prob:entropy-inverse-q` (stays OPEN). Not evaluated at any deployed `w` (toy rows, `w<=3`). Does not move the frontier edge, alter any margin, or touch skeleton steps 5-6. The null is evidence the **first-match removal is doing its job at toy scale**, not evidence for or against the inverse theorem itself.

The five rows (task-fixed; `char B = p > w` at each, so `prop:newton`'s power-sum reading is valid):

| row | `p` | `n` | `m` | `w` | `gcd(m,n)` | `C(n,m)` | `|B|^w` | max fiber | `R = |B|^w max mu` |
|---|---|---|---|---|---|---|---|---|---|
| A | 97 | 16 | 6 | 2 | 2 | 8008 | 9409 | 5 | `47045/8008 ~ 5.875` |
| B | 97 | 16 | 7 | 2 | 1 | 11440 | 9409 | 6 | `28227/5720 ~ 4.935` |
| C | 113 | 16 | 6 | 2 | 2 | 8008 | 12769 | 5 | `63845/8008 ~ 7.973` |
| D | 31 | 10 | 5 | 2 | 5 | 252 | 961 | 2 | `961/126 ~ 7.627` |
| E | 193 | 24 | 8 | 3 | 8 | 735471 | 7189057 | 15 | `35945285/245157 ~ 146.62` |

---

## 1. [EXPERIMENTAL] The dyadic popular-fiber hierarchy (step 1, fiber-resolved)

For each row, bucket every prefix value `z` by the dyadic level `k` of its normalized ratio
`R(z) = |B|^w |Fib_w(z)|/C(n,m)`: level `k` iff `2^k <= R(z) < 2^{k+1}`, with a below-average
bucket for `R(z)<1`. This is step 1's "dyadically extracts popular fibers" made explicit; PR
#384 measured the aggregate `Gamma_r` over all `z`, this resolves the mass by level.

| row | level `k` | ratio `[2^k,2^{k+1})` | `#z` | mass (subsets) | mass frac |
|---|---|---|---|---|---|
| A | 0 | `[1,2)` | 2504 | 2504 | 0.3127 |
| A | 1 | `[2,4)` | 1968 | 4432 | 0.5534 |
| A | 2 | `[4,8)` | 256 | 1072 | 0.1339 |
| B | 0 | `[1,2)` | 1312 | 2624 | 0.2294 |
| B | 1 | `[2,4)` | 1400 | 4640 | 0.4056 |
| B | 2 | `[4,8)` | 240 | 1248 | 0.1091 |
| B | below | `<1` | 2928 | 2928 | 0.2559 |
| C | 0 | `[1,2)` | 4168 | 4168 | 0.5205 |
| C | 1 | `[2,4)` | 1504 | 3008 | 0.3756 |
| C | 2 | `[4,8)` | 256 | 832 | 0.1039 |
| D | 1 | `[2,4)` | 210 | 210 | 0.8333 |
| D | 2 | `[4,8)` | 21 | 42 | 0.1667 |
| E | 3 | `[8,16)` | 618816 | 618816 | 0.8414 |
| E | 4 | `[16,32)` | 51392 | 109848 | 0.1494 |
| E | 5 | `[32,64)` | 1632 | 6708 | 0.0091 |
| E | 6 | `[64,128)` | 12 | 84 | 0.0001 |
| E | 7 | `[128,256)` | **1** | **15** | 0.0000 |

Masses (plus the below-average bucket) reconstruct `C(n,m)` exactly on every row (gate 2/4).
Observed vs empty prefixes: A `4728/4681`, B `5880/3529`, C `5928/6841`, D `231/730`,
E `671853/6517204`.

Two rows carry a single dramatic spike. **Row E level `k=7` is one fiber of mass 15** -- the
unique dominant fiber, at ratio `~146.6` above random (`R_max`). It is the `C(6,2)=15`
coset-union quotient object of Sec. 3. Rows A-C are dense/Poisson-boundary (max ratio `<8`,
no isolated spike); row D (`gcd(m,n)=5`) is over-saturated, every fiber `<=2`.

**Exact `Gamma_r`** (`prop:moment-sandwich`, `Gamma_r = |B|^{w(r-1)} sum_z mu(z)^r`), recomputed
as reduced `Fraction`s (gate 2 for rows A-D, gate 4 for E):

| row | `Gamma_2` | `Gamma_3` | `Gamma_4` |
|---|---|---|---|
| A | `20445757/8016008` | `74276066759/9170313152` | `15564081912098365/514051074048512` |
| B | `17867691/8179600` | `563665932127/93574624000` | `1876685927105037/97317608960000` |
| C | `20698549/8016008` | `527132118113/64192192064` | `1496923310125871/46731915822592` |
| D | `961/216` | `923521/42336` | `11537547853/96018048` |
| E | `236512786243/20033984883` | `22179510594169659101/132609734062964037` | `101867143731616647125106617/32510204573674074418809` |

---

## 2. [PROVED] The probe confound

**Setup.** `D = alpha H subseteq B^x`, `H` cyclic of order `n`, `char B nmid n`
(`def:coefficient-scale`'s standing hypothesis; on these rows `D = mu_n`, `alpha=1`). The depth-`w`
prefix `Phi_w` buckets `m`-subsets by their first `w` power sums (equivalently top `w` locator
coefficients, `prop:newton`). "Instrumenting past the bucketing depth" means probing a coordinate
`j > w`: the **probe coordinate** of a support `S subseteq D` is `p_j(S) = sum_{x in S} x^j`.
Step-4 evaluates additive-structure statistics (small doubling, AP tests) on `p_j`-differences of
trades. The skeleton fixes `j = w+1` and `j = w+2` (the first two coordinates not pinned to `z`).

**Lemma `lem:probe-confound`.** Fix a probe order `j >= 1` and put `c = gcd(j,n)`.

**(a) Image collapse.** The power map `phi_j : D -> B^x`, `x |-> x^j`, has image
`phi_j(D) = alpha^j mu_{n/c}`, a coset of the order-`(n/c)` subgroup, and is exactly `c`-to-1
onto that image. So `x^j` takes exactly `n/c` distinct values on `D`, each attained `c` times.

**(b) Coordinate factorization.** For any `S subseteq D`, `p_j(S)` depends on `S` only through the
pushforward multiset `phi_j(S) = <x^j : x in S>`, which is supported on the `(n/c)`-element set
`alpha^j mu_{n/c}`. Writing `M_y = #{x in S : x^j = y}`, `p_j(S) = sum_{y in alpha^j mu_{n/c}} M_y y`.
Hence for a trade `(S,T)` the probe-difference
`p_j(S) - p_j(T) = sum_y (M_y^S - M_y^T) y` lies in the sumset arithmetic of a **single
multiplicative coset of order `n/c`** -- an object governed by `n/c`, not by `n` or `p`.

**(c) Twist / composite reading.** The pure prefix direction supported at coordinate `j` (i.e. `z`
with `A(z) = {j}`) has twist stabilizer `s(z) = gcd(n,j) = c` (`prop:q-orbit-moment` l.923) -- the
same `gcd(n, .)`. Under `prop:composite-descend` (l.969) with the monomial probe `g(x) = x^j`
(its `h = X`, `e = j`, `S = D`, `N = n`), the probe "contributes through the image coset `S_e` with
power-map multiplicity `c`; when `c>1` it is a quotient-scale object rather than primitive mass" --
verbatim. And `lem:coeff-scale` (l.1112) pins the supports on which the probe is quotient-locked:
`S` is a union of `x |-> x^c` fibers iff `c | s(L_S)`, where `s(L_S) = gcd(n,e,{r : lambda_r != 0})`
is `def:coefficient-scale` (l.1100) -- the `mu_c`-invariant supports of the row-E mechanism (Sec. 3).

**Proof.** (a) Write `x = alpha zeta`, `zeta in mu_n`. Then `x^j = alpha^j zeta^j`; the
`j`-power endomorphism of the cyclic group `mu_n` has image the subgroup of order `n/gcd(j,n) = n/c`
and is `gcd(j,n) = c`-to-1 onto it (elementary cyclic-group fact; `X^n - alpha^n` squarefree since
`c | n` and `char B nmid n`). This is the `S = D`, `e = j`, `N = n` case of
`prop:composite-descend`'s displayed factorization. (b) Immediate from `x^j in alpha^j mu_{n/c}`.
(c) `s(z) = gcd(n, A(z)) = gcd(n, j)` by `prop:q-orbit-moment`'s definition; `prop:composite-descend`
is the displayed identity at `h = X`, `e = j`; `lem:coeff-scale`'s equivalence
`c | s(L_S) <=> S` a union of `x |-> x^c` fibers is quoted directly. `[]`

**Consequence (stated carefully).** A step-4 instrument evaluated on a probe coordinate with
`c = gcd(j,n) > 1` measures sums drawn from the `(n/c)`-element coset `alpha^j mu_{n/c}`. Its output
is intrinsically low-rank / AP-prone: the probe values form the sumset of `<= n/c` roots of unity, an
exact arithmetic progression already at `n/c = 2` (there `p_j(S) = alpha^j (a-b)` with `a+b = |S|`,
so the values are `alpha^j {|S|, |S|-2, ..., -|S|}`, common difference `2 alpha^j`), and empirically
sitting near the Cauchy-Davenport floor at the `n/c in {4,5}` seen here (Sec. 3) -- regardless of
whether the underlying primitive trade population carries structure. **Therefore step-4
instrumentation must use coprime probe orders `gcd(j,n) = 1`** (full image `alpha^j mu_n = D`), or
explicitly divide out the quotient image before applying an inverse-theorem statistic. This is the
coordinate-past-the-bucketing-depth extension of the twist-stabilizer formula
`s(z) = gcd(n, {j : z_j != 0})`: the same `gcd(n, .)` that shortens a prefix-direction's twist orbit
collapses that coordinate's probe image.

*(A related but distinct member-level effect -- a `mu_2`-invariant support kills every odd probe
coordinate, even a coprime one -- is the row-E antipodal mechanism of Sec. 3/5; that is `c | s(L_S)`
at the support, not `gcd(j,n) > 1` at the coordinate.)*

This is a lemma about the **instrument**, not the object. It is why the measured structure in Sec. 3
lands where it does.

---

## 3. [EXPERIMENTAL] The structure verdict, confound controlled

Operationalize step 5's conclusion -- "contained in a proper generalized arithmetic progression or
coset progression" -- by the exact Vosper/Cauchy-Davenport equality on the distinct residues
`P subseteq B` of a probe coordinate's primitive-trade values: `P` is an AP/coset progression iff
`|P + P| = 2|P| - 1` (the additive floor; needs `|P| >= 4` to be nontrivial). Scan every fiber of
size `>= 5` (`>= 6` at row E), primitive trades only (coefficient scale `s(S,T) = 1`,
`cor:primitive-coeff-exclusion`), both probe coordinates `j = w+1` and `j = w+2`, and split hits by
`gcd(j,n)` (gate 3):

| row | `j = w+1` | `gcd(j,n)` | exact-AP | `j = w+2` | `gcd(j,n)` | exact-AP |
|---|---|---|---|---|---|---|
| A | 3 | 1 (coprime) | **0/24** | 4 | 4 | **9/19 (47%)** |
| B | 3 | 1 (coprime) | **0/128** | 4 | 4 | 15/105 (14%) |
| C | 3 | 1 (coprime) | -- | 4 | 4 | 0/4 |
| D | 3 | 1 (coprime) | -- | 4 | 2 | -- |
| E | 4 | 4 | 0/4 | 5 | 1 (coprime) | -- |

(`--` = no fiber offers a size-`>=4` support at that coordinate.) **Aggregate: 0 exact-AP hits in 152
coprime-coordinate tests; 24 in 132 gcd>1-coordinate tests.** All AP/coset structure is confined to
the `gcd(j,n) > 1` probe coordinate, up to 47% in-fiber (row A, `j=4`) versus 0% at every coprime
coordinate -- exactly `lem:probe-confound`. The `j = 4` collapse in rows A/C is the image
`mu_{16/4} = mu_4` (four values); row D's `j = 4` image is `mu_5`.

Both dramatic apparent-structure instances are mechanically explained, and both are quotient/planted
-- the cells `prob:entropy-inverse-q` excises by first-match removal:

- **Row E's dominant fiber (the `C(6,2)=15` coset-union object).** The unique level-7 fiber is the
  **null prefix** `z = (0,0,0)`, size 15. `mu_4 = {1,81,112,192} subseteq mu_24` (sum `= 0 mod 193`)
  has six cosets in `D`, each of size 4; the `C(6,2) = 15` pairwise unions each have prefix `(0,0,0)`
  (any `mu_4`-coset kills `p_1, p_2, p_3`), and the actual null fiber equals **exactly these 15
  member-by-member** (gate 4). Every member is `mu_4`-invariant, i.e. quotient scale 4
  (`lem:coeff-scale`). All 14 trades from any base are non-primitive, so this fiber contributes
  **zero primitive trades** and is removed wholesale by first-match removal. Its apparent structure --
  the probe `p_5` is identically 0 across the fiber -- is `mu_4` killing every non-multiple-of-4
  power sum, a `prop:composite-descend` effect, not a primitive AP. The object is predicted by the
  twist-stabilizer formula: `A(z) = varnothing => s(z) = n = 24`, a maximally twist-degenerate,
  orbit-size-1 fiber.

- **Rows A/B's `j=4` AP excess.** The 24 hits are the `lem:probe-confound` image `mu_4`; each hit is a
  four- or five-term AP inside `alpha^4 mu_4`, not a property of the trades. Under the clean coprime
  coordinate `j = 3` (full image `mu_16`) the same fibers give 0/152.

**Small-sample calibration.** A null model (4000 IID-uniform draws from `Z/pZ` per size) pins the
looser flags a raw scan throws at coprime coordinates as noise: the observed coprime near-floor
`ratio_to_cd_min = 1.29` at `|P| = 4` sits *below* the null median (`1.43`), and the coprime
coincidence `2.50` at `n = 4` equals the null maximum. The exact-AP criterion (`|P+P| = 2|P|-1`)
removes them all and returns 0 at every coprime coordinate.

**Last-eyes caveat (Sec. 5).** The campaign's raw boolean `any_structure_in_primitive_only` is `True`
on four rows, but never from a coprime AP: it fires from (i) the `gcd>1` confound itself, (ii) `n=4`
noise, and (iii) a subtler **member-level** quotient effect that the trade-scale primitivity flag
misses -- see Sec. 5. Under the within-fiber exact-AP criterion, coprime coordinates are clean.

---

## 4. [AUDIT] Brick-2 monotonicity and consistency with PR #384

PR #384's Brick 2 is the certificate `R_eff(r) := Gamma_r^{1/(r-1)} -> R`, non-decreasing in `r`,
pinning the order at which the moment route can close. Verified per row from the exact `Gamma_r` of
Sec. 1, machine-checked as exact root-cleared inequalities (`Gamma_2^2 <= Gamma_3`,
`Gamma_3^3 <= Gamma_4^2`, `Gamma_4 <= R^3`; gate 2 for A-D, gate 4 for E) so no float enters the
verdict (values `Gamma_r^{1/(r-1)}`, `R = R_max`, below, are display-only):

| row | `R_eff(2)` | `R_eff(3)` | `R_eff(4)` | `R` | monotone `<= R` |
|---|---|---|---|---|---|
| A | 2.551 | 2.846 | 3.117 | 5.875 | yes |
| B | 2.184 | 2.454 | 2.682 | 4.935 | yes |
| C | 2.582 | 2.866 | 3.176 | 7.973 | yes |
| D | 4.449 | 4.671 | 4.935 | 7.627 | yes |
| E | 11.806 | 12.933 | 14.633 | 146.62 | yes |

`R_eff(2) <= R_eff(3) <= R_eff(4) <= R` on every row, consistent with Brick 2. The taxonomy matches
PR #384: the dense/Poisson rows A-C have a slowly-rising `R_eff` (the mass is spread, high moment
order needed), while over-saturated D and spiked E start high. Row E's `R_eff` is far below its `R`
at `r <= 4` precisely because the spike is a single fiber of mass 15 -- a low moment order barely
sees it, so the aggregate-`Gamma_r` route (PR #384) and the fiber-resolved view (Sec. 1) agree that
the dominant object here is caught only at high `r`, and it is quotient anyway.

---

## 5. Open problems, non-claims, and the last-eyes finding

- **No claim on `prob:entropy-inverse-q`.** It stays OPEN. This note neither proves nor refutes it and
  does not move the asymptotic-Q frontier.
- **Toy scale only.** Five rows, `w <= 3`, `n <= 24`. No claim about any deployed row or any `w` near
  the frontier. `lem:probe-confound` is scale-free (it is a `gcd` fact), but the **null** is toy.
- **The null is evidence about the instrument, not the theorem.** Zero coprime AP hits is evidence
  that first-match removal excludes the structured cells at toy scale -- the excess, where it exists,
  is quotient/planted (row E fiber, `gcd>1` coordinates). It is *not* evidence for or against the
  inverse theorem's structured alternative at scale.
- **Steps 5-6 untouched.** No contact with the Green-Ruzsa/PFR structuralization or the
  slice-derivative push-back.
- **Last-eyes finding (a caveat the JSONs carry that the campaign's one-line summary compresses).**
  The campaign's `falsifier_verdict.any_structure_in_primitive_only` is `True` on rows A, B, C, E.
  Read literally this looks like primitive structure survives; it does not. Classifying every
  primitive-only flag by coordinate shows exactly one is an exact AP, and it is at a `gcd>1`
  coordinate (row B, `j=4`). The coprime flags are of two kinds, neither a coset progression:
  (i) `n=4` small-sample noise (coincidence `2.50` = the null `n=4` maximum), and
  (ii) **member-level quotient structure that trade-scale primitivity misses.** At row E's fibers
  `z = (0, even, 0)` (`A(z) = {2}`, twist stabilizer `s(z) = gcd(24,2) = 2`, generated by `x |-> -x`),
  exactly **5 of 7 members are antipodal** (`M = -M`). Only the forward direction is a theorem: an
  antipodal support is a union of `{x,-x} = x mu_2` pairs, a `mu_2`-quotient object, so
  `M = -M => ` every odd power sum vanishes, in particular `p_5(M) = 0`. The converse is **not**
  general -- `p_5 = 0` is a single linear condition (e.g. `S = {1,9,49,181} subseteq mu_24` in
  `F_193` has `p_5(S) = 0` but `S != -S`, `p_1 = 47`, `p_3 = 79`). On **these 7 measured members**,
  though, *antipodal `<=>` `p_5(M) = 0`* holds member-by-member (gate 5) -- an empirical coincidence
  of this small fiber, where `p_1 = p_3 = 0` is already forced. So the coprime probe `p_5` collapses to a near-singleton -- a
  *coincidence*, `|P| = 2`, never registering as an AP (`|P| >= 4` required) -- driven by the
  **members** being quotient, even though the connecting **trades** are flagged primitive
  (`s(S,T) = 1`). The trade-scale first-match filter of `def:primitive-logmoment` is a statement about
  `S, T`; it does not by itself remove a base/member with a hidden `mu_2` (antipodal) symmetry. This
  is a real instrumentation subtlety worth carrying into any step-4 attempt: **primitivity must be
  read at the level of the object the statistic sees.** Under the clean within-fiber exact-AP
  criterion the coprime coordinates are 0 regardless, so the headline null stands; the caveat sharpens
  *why* first-match removal must be applied to the right object. (One further raw flag, row C's pooled
  coincidence `2.14` at coprime `j = 3`, is a cross-fiber pooling artifact -- all five top fibers have
  `s(z) = 1`, no within-fiber structure -- marginally above the IID null and not a coset progression.)

---

## 6. Weave (refs re-grepped at base `53bb5df`)

- **PR #396** (`thresholds-entropy-inverse-trade-reconciliation`, holmbuar, **OPEN** -- the parent).
  Pins the step-1/step-2 dictionary (`lem:trade-is-shift-pair`: the skeleton's "signed trade" = a
  depth-`w` shift pair; step 1's "popular fiber" = the `Fib_w(z)` histogram) and flags that
  **only steps 4-6 lack an in-repo object.** This packet is the first *measurement* on step 1's
  popular-fiber excess and the first proved lemma for a step-4 instrument. The confound coordinate is
  `j = w+1, w+2`, exactly PR #396's "moment-curve column" index shifted past the bucketing depth `w`;
  restate self-containedly here (Sec. 2 needs nothing from #396 but the framing).
- **PR #384** (aggregate `Gamma_r` / moment route, integrated). Brick 1 (order floor
  `r >= ceil(w log2|B|/Delta)`) and Brick 2 (`R_eff(r) = Gamma_r^{1/(r-1)} -> R`, monotone). Sec. 1
  resolves that PR's aggregate `Gamma_r` by dyadic level per fiber; Sec. 4 re-verifies Brick 2 on the
  same five rows. Same moment kernel (`prop:moment-sandwich`), no verdict changed.
- **PR #380** (composite Q-prefix multiplicity, integrated). "Composite Q-prefix multiplicity must be
  read with quotient scale `c = gcd(e,N)`." `lem:probe-confound` is the single-coordinate probe
  instance of exactly this `c = gcd(.)` rule, now at the instrumentation coordinate rather than the
  prefix direction.
- **T1/T2/T4 concurrent** (sibling entropy-inverse lanes) -- no file contact; shared skeleton labels
  only.
- **PR #397** (`rowsharp-q-prefix-atom-reductions`, avdeevvadim, OPEN) and **PR #398** (`b2` dual /
  character-sum package, scottdhughes, OPEN), both opened shortly before this packet. Courtesy check,
  no object contact. #397 is the row-sharp Q-prefix atom wall for the **deployed** KB-MCA `a=1116048`
  row as a certificate-target reduction: its "Newton/power-sum equivalence" is `prop:newton` at the
  deployed frontier and its "top-seam marked incidence" is a deployed-row object -- this packet is
  toy-scale (`n<=24`, `w<=3`) and its probe lemma names no certificate target. #398 is the **dual**
  (character-sum) attack on `conj:Q`, with a Lean `powersum_rigidity` package certifying
  `prop:prefix-rigidity` and `b2_sp_*` shift-pair scripts; it shares the power-sum / odd-moment theme
  but at the deployed subgroup and via the dual route, with no file or object contact with the
  toy-scale probe-confound lemma. No competitor-PR contact.
- **Manuscript objects used:** `prop:newton` (l.551), `prop:moment-sandwich` (l.705),
  `def:primitive-logmoment` (l.752), `prob:entropy-inverse-q` (l.823), `rem:entropy-inverse-skeleton`
  (l.861), `prop:twist-orbit` (l.869), `prop:q-orbit-moment` (l.923), `prop:composite-descend` (l.969),
  `def:coefficient-scale` (l.1100), `lem:coeff-scale` (l.1112), `thm:coeff-quotient-extract` (l.1130),
  `cor:primitive-coeff-exclusion` (l.1151). All cited, none modified.
