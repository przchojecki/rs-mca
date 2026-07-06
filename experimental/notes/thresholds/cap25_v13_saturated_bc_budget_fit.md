# Saturated line-rays: the rank-one budget fit and the growing-dimension gap

Status: `AUDIT` / `EXACT_ARITHMETIC` / `PROVED-LOCAL(P1,P2 as corollaries of cited lemmas)` /
`MEASURED(toy census)` / `OPEN(the growing-dimension core)`.

**Data:** `experimental/data/certificates/frontier-adjacent/saturated_bc_budget_fit_v1.json`.
**Verifier:** `experimental/scripts/verify_saturated_bc_budget_fit.py` (zero-arg <90s,
`--full` re-enumerates all 45 toy instances, `--tamper-selftest` supported).

**What this is.** The first data/derivation packet on the promoted target
`prob:saturated-bc` (`grande_finale.tex` `\label{prob:saturated-bc}`,
"saturated primitive split-pencil line-ray target"): (i) the **exact margin
identity** showing the maintainer's printed adjacent margins are precisely
`log2 B* - log2 B_B(a_0+1)`, the gap between the deployed budget and the
base-field split-pencil floor; (ii) the **budget-fit** of the two proved
fixed-deficiency Conjecture-F strata (deficiency 1 and 2), exactly quantified
against the growing-deficiency interior cell that is the actual open core;
(iii) the **measured dedup profile** of `prop:line-ray-saturation` on an
exhaustive 45-instance toy census, the first `saturated-bc`-specific data;
and (iv) the **reduction** of the open core to the verbatim missing lemma
`prob:capg-split-pencil-B` (support form) / `prob:capfp-R1` (slope form),
which the raw manuscript itself files under `prob:band`.

**What this is not.** It does **not** prove `prob:saturated-bc`. It does
**not** certify `N_slopes <= B*` for the growing-dimension interior split-pencil
cell -- that cell is exactly where the two available proved bounds miss the
target by `2.07` million and `170` million bits respectively, against a
`22`-bit margin (Sec. 6). It does not move the frontier edge, does not
supersede PR #369 (Latif Kasuli's KB-MCA L4 base-field floor ladder fixture,
open -- cited only, for an independent cross-check of one shared number, Sec.
6), and does not supersede PR #378 (Holm Buar's Lean BC interior census
floor, open, lower-side only). All of `prop:rank-one-distinct-slope-floor`,
`prop:base-field-floor`, `thm:capf-fixeddim`, `thm:bc-proper`, and the toy
census are pre-existing/cited proved statements or fresh exhaustive
measurements. The margin arithmetic itself is the promoted note's OWN
comparison (its L172-176 states `C(n,m) > |B|^w B*` with the printed
next-step bit margins; `L(a)` at its L1783 is the same floor object) --
this packet INDEPENDENTLY REPRODUCES it three ways and adds what is new:
the tie of that margin to the proved ADVERSARIAL floor
(`prop:rank-one-distinct-slope-floor` sits inside the budget by exactly
the margin -- the P1 pin), the fixed-deficiency budget-fit bookkeeping
(P2), the first measured dedup census on the saturated objects, the
dim-W bookkeeping correction, and the verbatim reduction of the open core
to `prob:capg-split-pencil-B` (= `prob:band`) -- not a new proof of
anything in the open core.

Executes laneJ's candidate **[B]** ("L4 is a flatness rung; count slopes,
not supports") and laneM's full analysis of the same target.

---

## 1. Object and dedup identity

For an affine line `U_Z = u + Z v` (`u,v : D -> F`) and a finite slope set
`E subseteq F`, define (`def:line-rays`, `grande_finale.tex` L1555)
```
LineRay_E(u,v;m) = { (z,c) in E x C : s_{z,c} >= m },   s_{z,c} = |{x in D : u(x)+z v(x) = c(x)}|.
```
`prob:saturated-bc` (L1768) bounds the **distinct residual-bad slope count**
```
N_slopes := |{ z in E : exists c, (z,c) in LineRay_E(u,v;a_0+1), z residual-bad }|.
```
"Residual" means: after the quotient/boundary-Q profile (`d1 = w+1`,
`prop:boundary-q`), common-support, tangent (`prop:split-chart-tangent`
L1219), and extension branches have each been paid by first match. So the
active slope set `E` sits in the primitive interior locus
`w+2 <= d1 <= floor((n-K+1)/2)`.

With `Cen(U;m)` the size-`m` support-locator census (`def:saturated-rays`
L1490) and the **exact saturation identity**
`Cen(U;m) = sum_c C(s_c(U),m)` (`thm:saturation` L1509),
`prop:line-ray-saturation` (L1565) gives, for every `E`:
```
sum_{z in E} Cen(U_z;m)  =  sum_{(z,c) in LineRay_E} C(s_{z,c},m)          (identity)
N_slopes  <=  |LineRay_E|  <=  sum_{z in E} Cen(U_z;m)                      (two dedup losses)
```
- **loss 1** `|LineRay_E| - N_slopes` = codeword multiplicity per slope
  (forgetting the codeword coordinate). Vanishes iff each bad slope has a
  unique explaining ray.
- **loss 2** `sum Cen - |LineRay_E|` = saturation excess
  `sum_{lineray} (C(s_{z,c},m) - 1)`. Vanishes iff every ray is saturated at
  exactly `m`. By `cor:raw-bc-fails` (L1541) loss 2 can be `C(n-d,m)` for a
  **single** slope and ray: exponentially loose. The raw census
  `sum_z Cen(U_z;m)` is therefore an **audit object**, not the MCA numerator.

### Margins (PART A, exact big-int; recomputed by gate i of the verifier)

`p_KB = 2^31-2^24+1`, `p_M31 = 2^31-1`, `n = 2^21`; L4 = scale-16 quotient
rung, `n=131072, K=65537, m=69753, w=4216` (the `#369` fixture row,
reproduced here from raw conventions, independently of that PR).

| row | w | log2 C(n,a+) | log2 B* | log2 floor B_B(a+) | margin |
|---|---|---|---|---|---|
| KoalaBear MCA | 67471 | 2090873.2798 | 57.9321 | **35.7352** | **22.1969** |
| KoalaBear list | 67471 | 2090873.4657 | 57.9321 | 35.9212 | 22.0109 |
| Mersenne-31 MCA | 67447 | 2090877.7411 | 24.0000 | **20.7411** | **3.2589** |
| Mersenne-31 list | 67447 | 2090877.9270 | 24.0000 | 20.9270 | 3.0730 |
| L4 testbed | 4216 | 130671.4337 | (no B*) | 23.1390 | flatness rung |

`B_B(a+) = C(n,a+)*p^-w` is the **base-field floor**
(`prop:base-field-floor` L1261 / `prop:capg-census-floor`, raw L9728): the
proved lower witness a constructed adversarial `B`-valued pole line realizes.
`B*_KB = floor(p_KB^6/2^128)`, `B*_M31 = floor(p_M31^4/2^100)` (both pinned
directly in `grande_finale.tex`). **Identity confirmed to all 4 printed
decimals, two independent ways** (exact-bigint bit-length truncation and an
independent `math.lgamma`-based recompute, agreeing to `<5e-9`), **and
against `grande_finale.tex`'s own printed table** (the "adjacent agreement /
spare margin" table), which the verifier parses directly from the promoted
TeX source rather than trusting a hardcoded constant. The L4 row's floor
`23.1390` is cross-validated three independent ways in Sec. 6. The L4 row
has no budget confrontation (it is a flatness rung, per laneJ): the correct
L4 object is the per-line **slope** census, not a `B*` comparison.

---

## 2. The flip: from slopes to a point count

**Domain side (unconditional, `thm:bc-proper`'s route).** Each residual-bad
`z` is close at a witness support `T_z` (`|T_z|=m`). Slope elimination
(`prop:slope-elimination` L1087 = raw `thm:capfp-slope-elim`(c), L8258): a
**non-common** support carries at most one finite slope `z(T)`. Hence
`N_slopes <= N_MCA-bad(u,v;m) <= #R1(u,v;m) := #{rank-one supports}`, and
`thm:bc-proper` (L1463) bounds `#R1 <= min(C(n,omega), |F|^{r1+r2})`,
`r1+r2 = omega-w+1` at the balanced interior. This is the weak route (Sec.
6).

**The flip: distinct slopes = distinct values of `ev_alpha`.** In the
certifying pole-line normal form (`prop:rank-one-floor` L1290,
`prop:rank-one-distinct-slope-floor` L1313) with `f_alpha = U_z*/(X-alpha)`,
`g_alpha = -1/(X-alpha)`, `alpha in F\B`, each support `S` carries the single
slope `z(S) = zeta_S(alpha) = U_z*(alpha) - l_S(alpha)`, an affine function
of the linear functional `ev_alpha : l_S -> l_S(alpha)`. Two supports collide
iff `alpha` is a root of `l_S - l_S'`; since `S,S'` share the depth-`w`
prefix `z*`, `deg(l_S - l_S') <= K-1` -- **the `K-1` collision cap**.
Averaging over the `q-|B|` extension poles (raw `lem:capfp-pair-descent`
L8209 bounds the image clique) gives, for `N <= (q-|B|)/(K-1)+1` (true at
the frontier: `N ~ 2^35.7 << q/K ~ 2^166`), the pole-line slope count
**pinned to `Theta(B_B(a+))` from both sides** (P1, Sec. 3).

**The quantity that needs a point count.** For a general residual line, the
supports are not confined to one prefix fiber, so `#R1` must itself be
base-field-normalized. Writing the support's locator `W = l_{D\T}` (degree
`omega`) via the split-pencil coefficient space
(`thm:near-rational`(ii) L1129, `prop:capfr1-detrep` raw L7992):
```
W = { A W_1 + B W_2 : deg A <= omega-d1, deg B <= omega-d2 } <= F[X]_{<=omega},   dim W = omega-w+1,
```
`#R1` is **exactly the Conjecture-F incidence count** `|P(W) cap Dloc_omega(D)|`
(raw `sec:capf-m1` L6518, def. at L6670): which matrix = the shifted
weak-Popov determinantal representation of `Lambda_D`
(`prop:capfr1-detrep`); whose rank drop = the split condition at exact
degree `omega`; over which field = **the base field `B`** -- the twisted
columns are `B`-valued on `B`-valued coordinate words
(`lem:capfp-functionals` raw L8246) -- so the incidence variety is defined
over `B` and its point count carries the `|B|^-w` normalization that a
challenge-field-only model cannot see.

---

## 3. Proved partial: rank-one and deficiency-one fit the budget

**P1 (the adversary's floor is inside the budget; the extremal class is
pinned).** `prop:rank-one-distinct-slope-floor` (L1313) proves a lower
bound: the constructed non-`B`-rational pole line realizes
`>= N - C(N,2)(K-1)/(q-|B|)` distinct MCA-bad slopes with
`N = ceil(C(n,a+)|B|^-w) = B_B(a+)`; at the frontier
`N ~ 2^35.7 << (q-|B|)/(K-1) ~ 2^166`, so the count is `>= B_B(a+)(1-o(1))`.
The trivial image-<=-domain bound gives, for this constructed family,
`N_slopes <= N`, so the extremal class is **two-sidedly pinned at
`B_B(a+)`**. By the margin identity (Sec. 1), `B_B(a+) = B* * 2^-Delta`,
`Delta in {22.1969, 22.0109, 3.2589, 3.0730} > 0`: **the adversary's own
proved lower witness sits inside the budget by exactly the printed margin.**
This is not automatic: a challenge-field-only model
`C(n,m)*q^-(w-1)` (`prob:capfp-R1`'s uncorrected form, raw L8278) places it
`~10.45` million bits *lower* (falsely "safe"); a base-field-blind reading
of `thm:capf-fixeddim` places the growing-deficiency cell `~2` million bits
*higher* (Sec. 6). P1 fixes the **target constant** for a general upper
bound; it is **not itself** a general upper bound (`cite`:
`prop:rank-one-distinct-slope-floor`, `prop:rank-one-floor`,
`prop:base-field-floor`).

**P2 (fixed-deficiency charts fit, via proved Conjecture-F).** For a chart
of fixed deficiency `d`, slope elimination makes the count a
fixed-dimension Conjecture-F incidence `|P(W) cap Dloc_omega(D)|`,
`dim P(W) = d`:

| deficiency `d` | proved bound | KoalaBear-MCA (`B*=2^57.93`) | Mersenne-31-MCA (`B*=2^24.00`) |
|---|---|---|---|
| 1 | `floor(n/omega)` (`lem:capf-dim1`, raw L6696) | `2` fits | `2` fits |
| 2 | `C(n,2)/(omega-1)` (`thm:capf-dim2`, raw L6719) | `2^21.10` fits | `2^21.10` fits |
| `d` fixed | `C(n,d)` (`thm:capf-fixeddim`, raw L6735) | fits iff `d<=2` | fits iff `d<=1` |
| **`omega-w` (interior BC)** | `C(n,omega-w)` (only proved bound) | **`2^2072017.7` does not fit** | **`2^2072035.6` does not fit** |

Deficiency `<=2` is provably budget-fitting at both rows (the tangent /
bounded-SPI paid strata: `prop:split-chart-tangent` L1219, raw
`thm:capf-spi` L6859). **BC proper is the growing-deficiency residual**
`d = omega-w`, `dim W = d+1 = 913634` (KoalaBear) / `913682` (Mersenne-31)
(Sec. 6 has a provenance note on this number).

**P3 (the margin *is* the floor gap).** `margin = log2 B* - log2 B_B(a+)`
exactly, to 4 decimals, at all four rows (Sec. 1). The safe side needs
**only** `R_BC <= 2^Delta`; a challenge-field-only model
(`= 2^-10.45M` per line) is `~10.45M` bits below the true floor and would
falsely certify safety -- exactly the failure mode `prop:base-field-floor`
(L1261) warns against.

P1 fixes the target constant; P2 is proved-and-fits at fixed deficiency
`<=2`; only the interior `d1 >= w+2` growing-deficiency class (Sec. 6) is
open.

---

## 4. First `saturated-bc` data: the toy census (PART B, exhaustive)

Exhaustive line-ray census over `F_{p^2} >= B=F_p >= D`, all `q` slopes,
three line families (`random_base`, `pole` [adversarial, extension-valued],
`random_ext`) across five `(p,K,m)` configurations x 3 seeds = **45
instances**. Independently re-enumerated by the verifier's gate iii (a
different interpolation algorithm from the packaging input, Sec. 7).

**M1 -- `thm:saturation` is exact.** `Cen(U;m) = sum_c C(s_c,m)` **and** the
fiber over each ray equals `C(s_c,m)`: **verified on all 45 instances, zero
failures.** A direct computational check of the identity underlying
`prob:saturated-bc`.

**M2 -- the two dedup losses are strict and structured.** Representative
row (`p=13, K=5, m=7, w=2`, base-field floor `M_B=11`):

| line family | N_slopes | (base / ext) | \|LineRay\| | sum Cen | loss1 | loss2 | max `C(s,m)` | codewords/slope |
|---|---|---|---|---|---|---|---|---|
| random **B**-valued | 13 | (13 / 0) | 91 | 119 | 78 | 28 | 8 | mean **7.0** |
| **pole** (extension, adversarial) | **71** | **(7 / 64)** | 79 | 135 | 8 | 56 | 8 | mean 1.11 |
| random **F**-valued | 10 | (0 / 10) | 10 | 10 | 0 | 0 | 1 | 1.0 |

Empirical laws (stable across `p=7,11,13`, all seeds):
- **loss 1** (line-ray -> slope, codeword multiplicity) is large for
  `B`-valued lines (mean 7 codewords/slope at `p=13`), small for pole/ext
  lines.
- **loss 2** (census -> line-ray, saturation excess) is large whenever a
  high-agreement codeword exists -- pole lines hit `C(s,m)` up to
  **120** (`C(10,7)`), the `cor:raw-bc-fails` mechanism in miniature.
- the census overcounts the true slope object by **~2-9x already at `n=13`**
  (`119` vs `13`; `135` vs `71`); at frontier depth this multiplier becomes
  the exponential saturation gap `prob:saturated-bc` must not pay.
- **adversarial = extension-valued.** Pole lines maximize `N_slopes` and
  make the bad slopes predominantly extension-valued -- **64 of 71** at
  `p=13` -- the exact `prop:rank-one-distinct-slope-floor` signature.
  Generic `F`-valued lines are clean: `loss1=loss2=0`, one support per
  slope.
- **pre-asymptotic caveat (honest).** At these toy sizes `q=p^2` is small,
  so the collision term `C(N,2)(K-1)/(q-b)` is **not** negligible, and the
  pole line's `N_slopes` (71) *exceeds* the base-field floor `M_B` (11) --
  the complement of Sec. 2's frontier pin (`N <= (q-|B|)/(K-1)+1` fails at
  this toy scale). At the deployed rows `q=p^6 >> N*K`, so the pin holds
  and `N_slopes ~ M_B(a+)`. **The toy shows the mechanism, not the frontier
  constant.**

---

## 5. The missing lemma, verbatim

The exact statement the program lacks -- the analogue of what would pin RC
for BC -- is `prob:capg-split-pencil-B` (raw L9842), **support-census
form**:

> Let `(W_1,N_1,W_2,N_2)` be a determinantal representation of `Lambda_D`
> (`prop:capfr1-detrep`) with interior balanced profile
> `w+2 <= d1 <= floor((n-K+1)/2)`. Prove
> ```
> #{ (A,B): deg A <= omega-d1, deg B <= omega-d2, A W_1+B W_2 | Lambda_D, deg(A W_1+B W_2)=omega }
>        <=  e^{o(n)} * max( 1,  M_B(d1),  C(n,omega) q^{1-w} ),
> ```
> counting monic normalizations, with `M_B(d1) = C(K-1+d1,m)*C(n,K-1+d1)*p^{-(d1-1)}`
> the subfield floor of `prop:capg-census-floor`, achieved there.

Its **slope refinement** -- the exact object of `prob:saturated-bc` -- is
`prob:capfp-R1` (raw L8278) with the corrected base-field model (raw
L9860-9861, inside `prob:capg-split-pencil-B`'s own remark):

> For every residual line at band agreement `m`,
> ```
> N_slopes <= #R1(u,v;m) <= e^{o(n)} * max( 1,  C(n,m) p^{-w},  C(n,m) q^{-(w-1)} ),
> ```
> the middle term achieved by the **non-`B`-rational pole lines** of
> `prop:capg-census-floor`(c).

For a **finite adjacent proof** (`thm:finite` L1720), the required instance
is:

> **(BC-fin)** `R_BC <= 2^Delta` with `Delta = 22.1969` (KB-MCA) /
> `3.2589` (M31-MCA), i.e. `N_slopes <= 2^Delta * B_B(a+) <= B*` after the
> first-match ledger subtracts the already-paid cells.

The missing mathematical content is the **base-field normalization of a
growing-dimensional Conjecture-F incidence**: extract the `|B|^-w` factor
from the `B`-valued moment-kernel arithmetic (`prop:capfp-kernel` raw
L8173), not from the projective dimension. `thm:capf-fixeddim` gives the
dimension part `C(n,omega-w)`; the arithmetic part is `prob:band`
(`rem:capf-conjf-open`, raw **L6758** -- see the provenance note below) --
unsettled.

---

## 6. Gap ledger, tractability verdict, and the L4 cross-check

**Proved reach:** the rank-one/pole class (P1) and deficiency-one/two (P2)
-- the boundary and tangent-adjacent charts -- fit the budget. These are the
classes where the Conjecture-F incidence is a projective point/line/plane
(fixed dimension 0-2), so `lem:capf-dim1`/`thm:capf-dim2`/image-<=-domain
suffice.

**Open core:** the interior primitive profiles `w+2 <= d1 <= floor((n-K+1)/2)`,
where the Conjecture-F subspace has **growing** dimension
`dim W = omega-w+1`. The gap, quantified exactly (PART A, and re-derived
independently by the verifier's gate ii):

| upper bound | KoalaBear-MCA value | misses floor by | Mersenne-31-MCA value | misses floor by |
|---|---|---|---|---|
| target `R_BC * B_B(a+)` needed | `2^{35.7+Delta}` | -- (the goal) | `2^{20.7+Delta}` | -- (the goal) |
| `thm:capf-fixeddim` `C(n,omega-w)` | `2^2072017.7` | **2.07 x 10^6 bits** | `2^2072035.6` | **2.07 x 10^6 bits** |
| `thm:bc-proper` `q^{omega-w+1}` | `2^169873895.7` | **1.70 x 10^8 bits** | `2^113296568.0` | **1.13 x 10^8 bits** |

Against a **22-bit** margin (KoalaBear) / **3-bit** margin (Mersenne-31),
the two proved bounds are `~10^5x`-`~10^7x` too weak in the exponent.
Neither bound extracts the `|B|^-w` factor; that factor is the entire
content and lives in the `B`-rational moment kernel
(`prop:capfp-kernel`), tying BC to Q on the same `{0,+-1}`-configuration
count `Gamma_r`. **Tractability by direct point count: LOW** -- this is the
growing-dimensional primitive incidence problem the manuscript itself files
under `prob:band` (`rem:capf-conjf-open`, raw L6758). Weil/character sums do
not obviously help here: unlike `prob:row-sharp-q`, the incidence is a
*divisor locus*, not a character sum, and the depth to control is the full
`w` (`=67471`), not a reduced one.

**Where a proof could plausibly come from (ranked; all
`SPECULATIVE/ROUTE-ASSESSMENT`, none a claim):**
1. **Base-field-normalized fixed-dim induction on `Gamma_r`.**
   `prop:capfp-kernel`(c) (raw L8173) makes `Gamma_2` a balanced-ternary
   weight enumerator of the order-`w` moment kernel `K_w`;
   `rem:capfp-gamma-measured` (raw L8228) measures `Gamma_r = 1+o(1)` in the
   dense bulk. If `Gamma_r = e^{o(n)}` persists to `r ~ 10^5`
   (`prob:capfp-gamma`, raw L8135), the split-pencil census inherits the
   `|B|^-w` normalization by the moment method. **This is the one object
   that would close both Q and BC.**
2. **Stability/inverse theorem** (`rem:capfp-band-obstruction`(iii), raw
   L8220): a heavy interior fiber forces a quotient-stabilizer / common-block
   structure already paid by `thm:coeff-quotient-extract` (L1002) + the
   capf ledger. Needs a growing-dimension Conjecture-F inverse theorem, not
   in hand.
3. **`cor:capfp-packing`** (raw L8194) already shaves `~213500` bits off the
   trivial `C(n,m)` fiber bound by rigidity alone -- a proved down-payment,
   still `~1.877` million bits above target. The residual is exactly the
   aperiodic core.

### L4 floor: a three-route cross-check

The L4 testbed row's base-field floor (`log2 = 23.1390`, Sec. 1) is
confirmed by **three independent computational routes**, agreeing to six
decimal places (`23.139009...`):

1. this packet's own recompute, `log2(C(n,m) p^-w)` directly (PART A /
   verifier gate iv);
2. the already-integrated `kb_mca_conjq_rung_audit_v1.json`, rung `j=4`
   (`log2_quotient_avg_a_j = 23.139009074`) -- computed via the **quotient-
   average pigeonhole route** of the `conj:Q` rung audit, an entirely
   different derivation from (1);
3. PR #369 (Latif Kasuli, open), `verify_bc_l4_base_floor_ladder.py`'s
   printed `base_field_floor_log2_approx = 23.139009` at `d1=4217`
   (`prop:capg-census-floor`'s direct route) -- confirmed via `gh pr diff
   369` during packaging of this note; this packet does **not** fetch or
   depend on #369's (unmerged) files at verify-time, it only records the
   cross-check narratively.

This is a strong three-route numerical cross-validation of one exact
rational; it is not, and is not claimed to be, progress on
`prob:saturated-bc` itself.

### Provenance note: two corrections found while cross-checking laneM_analysis.md

While verifying every cited number against the raw manuscript, two items in
the Lane M working analysis (the base text this note was built from) did
not check out, and are corrected here rather than silently propagated:

1. **`dim W` at the current adjacent pair.** `laneM_analysis.md` Sec. 2.3/3
   quotes raw `prob:capfp-balanced` (L8386) verbatim as printing
   `"913642 at the KoalaBear adjacent pair, 913686 at Mersenne-31"` for
   `dim W = omega-w+1`. Recomputing `omega-w+1` at the **current, active**
   moved adjacent pair (`a+ = 1116048` KB-MCA / `1116024` M31-MCA, per
   `rem:packet-convention`) gives **913634 / 913682** instead -- matching
   `omega-w` from PART A (`913633`/`913681`) plus one, and matching
   independently via a second `lgamma`-based recompute. No integer `m`
   within a few units of either current `a_0`/`a+` reproduces 913642/913686
   under either `K` convention; the raw citation appears to be a leftover
   from a historical (pre-move) adjacent-pair numbering elsewhere in the
   same v13 raw manuscript -- precisely the phenomenon `rem:packet-convention`
   documents for other tables in the same packet family. This note uses
   **913634 / 913682** throughout (Sec. 3, Sec. 6), not 913642/913686.
2. **A line-number self-citation.** `laneM_analysis.md` Sec. 6 cites
   `rem:capf-conjf-open` at "raw L8225". The label's actual line is raw
   **L6758** (confirmed directly, and consistent with that same document's
   own Sec. 2/3 citations of the identical label). Raw L8225 falls inside a
   *different* remark, `rem:capfp-band-obstruction` (which starts at
   L8220). This note cites `rem:capf-conjf-open` at L6758 only.

Neither correction changes any conclusion; both are recorded in the shipped
JSON's `found_vs_claimed_corrections` block for the record.

---

## Non-claims

- No upper bound on the growing-dimension interior split-pencil cell
  (`d1 >= w+2`) is proved or claimed here.
- `prob:saturated-bc` is **not** solved, and `N_slopes <= B*` (or
  `U(a_0+1) <= B*`) is **not** certified.
- The toy census (Sec. 4) is mechanism-scale and pre-asymptotic (`q=p^2`
  small enough that the frontier pin's own hypothesis fails at toy scale,
  Sec. 4/M2); it demonstrates the dedup mechanism, not the frontier
  constant.
- The moment-kernel route (Sec. 6, item 1) is a `SPECULATIVE /
  ROUTE-ASSESSMENT`, not a proof sketch and not a claim of progress.
- Nothing here supersedes PR #369 (Latif Kasuli's L4 base-field floor
  ladder fixture, open) or PR #378 (Holm Buar's Lean BC interior census
  floor, open, lower side only); both are cited, neither is duplicated.

## Weave

- **laneJ dossier lineage.** Executes laneJ's candidate **[B]**: "L4 is a
  flatness rung; count slopes, not supports" -- Sec. 1's L4 row and Sec. 2's
  domain-side reduction are exactly this move, applied to the promoted
  `prob:saturated-bc` object.
- **#369** (Latif Kasuli, open, KB-MCA L4 base-field floor ladder fixture):
  cited only, for the independent L4 floor cross-check (Sec. 6); not
  duplicated, and this packet reproduces the row's raw conventions
  (`K=65537, m=69753, w=4216`) from scratch rather than depending on that
  PR's (unmerged) files.
- **#378** (Holm Buar, open, Lean BC interior census floor): the sibling
  **lower**-side result (`bc_census_floor_pigeonhole`, non-vacuous pigeonhole
  ceiling `M_B(d1)` in Lean). This note's object is the missing **upper**
  side that #378 explicitly states remains open. Consistent, not competing.
- **Concurrent same-session ship** (branch `thresholds-gammar-order-floor`,
  note `experimental/notes/thresholds/cap25_v13_gammar_order_floor.md`):
  first Gamma_r measurements + a proved unconditional moment-order floor on
  the SAME joint object this note's route-1 assessment names. Concurrent by
  path, cite-not-duplicate; neither depends on the other.
- **Repo-reference discipline.** All `grande_finale.tex` labels are
  `upstream/main` `e749e9e`; all raw labels are `cap25_cap_v13_raw.tex` v13,
  the same commit. Every label cited in this note was checked to exist at
  that commit before citation (see the packaging report); the two
  discrepancies found are recorded above, not silently fixed.

---

## Verifier contract

`experimental/scripts/verify_saturated_bc_budget_fit.py` is zero-arg,
stdlib-only, deterministic, and supports `--full` and `--tamper-selftest`.
Four gates:

- **gate i** -- margin identity: recomputes `B*` and `B_B(a+)` from raw
  constants (exact big-int; one expensive `math.comb` plus three
  near-free exact-ratio-derived siblings) and checks all four margins
  against the promoted note's printed values to `>=4` decimals, cross-checked
  against `grande_finale.tex`'s own printed table (parsed directly from the
  TeX) and against an independent `math.lgamma`-based recompute.
- **gate ii** -- P2 arithmetic (deficiency 1 and 2, both budgets) and the
  growing-deficiency miss (`thm:capf-fixeddim`, `thm:bc-proper`), including
  `dim W = 913634`/`913682` (see the provenance note above).
- **gate iii** -- toy census replay: by default, live re-enumerates 39 of
  the 45 instances (both `p=7` and `p=11` configurations in full, plus the
  `p=13` seed-0 headline witness across all three line families), checking
  the remaining 6 against pinned values; `--full` re-enumerates all 45.
  Every live instance re-verifies `thm:saturation`'s exact identity via a
  different algorithm (the `S_r` functional criterion of
  `lem:capfp-functionals`, not Newton divided differences).
- **gate iv** -- the L4 floor three-route cross-check (Sec. 6).

Expected runtime under 90s zero-arg (`--full` adds ~25-30s). A nonzero exit
code means a genuine arithmetic mismatch in this packet, not a judgment
about `prob:saturated-bc` itself.

## Refs

- `experimental/grande_finale.tex` -- `prob:saturated-bc`, `def:line-rays`,
  `prop:line-ray-saturation`, `thm:saturation`, `def:saturated-rays`,
  `cor:raw-bc-fails`, `thm:bc-proper`, `prop:base-field-floor`,
  `prop:rank-one-floor`, `prop:rank-one-distinct-slope-floor`,
  `prop:slope-elimination`, `thm:near-rational`, `prop:split-chart-tangent`,
  `thm:finite`.
- `experimental/cap25_cap_v13_raw.tex` -- `lem:capf-dim1`, `thm:capf-dim2`,
  `thm:capf-fixeddim`, `rem:capf-conjf-open`, `prop:capfr1-detrep`,
  `cor:capfp-packing`, `lem:capfp-pair-descent`, `rem:capfp-band-obstruction`,
  `rem:capfp-gamma-measured`, `prop:capfp-kernel`, `lem:capfp-functionals`,
  `thm:capfp-slope-elim`, `prob:capfp-R1`, `prob:capg-split-pencil-B`,
  `prop:capg-census-floor`, `prob:band`, `sec:capf-m1`.
- PR #369 (Latif Kasuli, open) -- KB-MCA L4 base-field floor ladder; cited
  for the L4 cross-check only (Sec. 6).
- PR #378 (Holm Buar, open) -- Lean BC interior census floor, lower side;
  sibling, not duplicated (Weave).
- `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_rung_audit_v1.json`
  -- already-integrated rung audit; rung `j=4` is the second L4 cross-check
  route (Sec. 6).
- `experimental/data/certificates/frontier-adjacent/saturated_bc_budget_fit_v1.json`
  -- this packet's data (margins table, P1/P2 ledger, toy census summary,
  the pinned open-lemma block, the L4 cross-check, and the
  `found_vs_claimed_corrections` record).
- `experimental/scripts/verify_saturated_bc_budget_fit.py` -- this packet's
  verifier (see Verifier contract above).
