# CAP25 v13 raw: the moment constant Gamma_r on the removed prefix object -- benign growth, an exact order floor, and why removal does not help

Status: `PROVED-LOCAL(Brick 1: unconditional order floor; Brick 2: monotone certificate)` /
`MEASURED(Gamma_r curves raw-vs-removed, 5 rows, r=2..8, exact Fraction arithmetic)` /
`AUDIT(the removal-does-not-help finding; the Poisson closed-form model)` /
`OPEN(dense-bulk law persistence at the deployed w = prob:row-sharp-q itself)`.

**Data:** `experimental/data/certificates/frontier-adjacent/gammar_order_floor_v1.json`.
**Verifier:** `experimental/scripts/verify_gammar_order_floor.py` (zero-arg `<90s`,
`--full` re-enumerates additional rows/widths, `--tamper-selftest` supported).

**What this is.** The first `Gamma_r` data (the fixed-moment collision hierarchy of
`grande_finale.tex \label{prop:moment-sandwich}` / raw `\label{prob:capfp-gamma}`) measured
on the paid quotient/planted-pruned prefix object, raw vs twist-primitive ("removed"),
across five toy rows spanning the dense, Poisson-boundary, and over-saturated regimes,
`r=2..8`, exact `Fraction` arithmetic throughout. Reproduces `rem:capfp-gamma-measured` and
`rem:capff1-calibration`'s calibration values to all printed digits and extends both to
`r=8` and to the raw-vs-removed split (novel). Proves two one-line but exact structural
bricks: **(1)** an unconditional order floor `r >= ceil(w log2|B| / Delta)`, forced purely
by `Gamma_r >= 1`, that independently reproduces PR #366's own shipped moment-route numbers
(`94196` at the KB-MCA row, `5886` at L4) to the digit and upgrades them from
Gamma_r-assumed-trivial estimates to unconditional proved floors; **(2)** a monotone
certificate `R_eff(r) := Gamma_r^{1/(r-1)} -> R` pinning the exact order at which the moment
method can close, `r_min(R)`, finite iff `R < 2^Delta`. Finds that quotient/planted removal
does **not** tame the moment constants where the deployed frontier actually lives (the
dense bulk, `lambda >> 100`): it shaves `<0.08` bit off `R` and `<0.04` bit off `Gamma_8`
there, because the bulk collision mass is provably primitive (exact ledger: the
quotient/removable off-diagonal is `<=6%` of `Gamma_2` at every measured depth).
Independently recomputes the frontier's mean-fiber placement (`lambda=2^{35.7}` at KB-MCA)
from raw constants, cross-checked to 4 decimals against Lane M's concurrent, independently
derived value.

**What this is not.** Does not evaluate `Gamma_r` at any deployed `w` (astronomically out
of reach -- toy rows only, `w<=4`). Does not prove or refute `prob:row-sharp-q`. Does not
move the frontier edge `(1116047,1116048)`. Does not alter any verdict, integer, or ladder
margin of PR #366 -- upgrades its route-cut moment orders to unconditional floors, touches
nothing else of that PR. Does not touch `prob:saturated-bc` (Lane M's concurrent target)
beyond citing the shared moment-kernel object (`thm:q-implies-sp`).

---

## 1. The object -- `Gamma_r` in house notation

### 1.1 The prefix-fiber distribution and `Gamma_r`

Domain `D subseteq B`, `|D|=n`, base field `B`, `|B|=p`. For an `m`-subset `M subseteq D`,
the depth-`w` prefix is `Phi_{m,w}(M) = (e_1(M),...,e_w(M)) in B^w`, the top `w`
coefficients of the locator `l_M(X) = prod_{x in M}(X-x)`; equivalently (Newton, `w<char B`)
the power-sum prefix `(p_1(M),...,p_w(M))`, `p_j = sum_{x in M} x^j` (raw
`\label{subsec:capfr1-Q-kernel}`, section header, `cap25_cap_v13_raw.tex` L7661). Fiber
`N_w(z) = |Phi^{-1}(z)|`, probability `mu(z) = N_w(z) / C(n,m)`. Then
(`\label{prop:moment-sandwich}`, `grande_finale.tex` L692, defining formula at L695 -- this
is the SAME object as raw `\label{prob:capfp-gamma}`, `cap25_cap_v13_raw.tex` L8135,
defining formula at L8138; **note the raw label is `prob:capfp-gamma`, a `\begin{remark}`
environment, not `prop:capfp-gamma`** -- see Sec 9):

```text
Gamma_r = |B|^{w(r-1)} * sum_z mu(z)^r,   r >= 2.
```

House reading: `Gamma_r = |B|^{w(r-1)} * C(n,m)^{-r} * sum_z N_w(z)^r`, and `sum_z N_w(z)^r`
counts ordered `r`-tuples of `m`-subsets sharing a common prefix. Proved in-manuscript:
`Gamma_r=1` iff the prefix distribution is uniform over all `|B|^w` prefixes; `Gamma_r>=1`
always (power means, distribution-free); `Gamma_2 = sum_tau |mu-hat(tau)|^2` (Parseval); and
`Gamma_r^{1/r}` increases to

```text
R = |B|^w * max_z mu(z)    (the max-to-mean fiber ratio; the L^infinity target of Q).
```

`R` is the "normalized maximum-fiber ratio" of `\label{thm:moment-q}`
(`grande_finale.tex` L708); the finite adjacent problem `\label{prob:row-sharp-q}`
(`grande_finale.tex` L1754) asks `R <= 2^Delta`, `Delta in {22.1969, 22.0109, 3.2589,
3.0730}` bits (KB-MCA, KB-list, M31-MCA, M31-list; `grande_finale.tex` L183-186, table
reproduced again at L1662-1665).

### 1.2 The moment criterion and the moment kernel

`thm:moment-q` requires, for a finite proof of `R <= 2^Delta`:

```text
log2 Gamma_r + w log2|B| <= r * Delta.            (MC)
```

The `Gamma_r` hierarchy is tied to a `B`-rational linear code by `\label{prop:capfp-kernel}`
(`cap25_cap_v13_raw.tex` L8173) -- the moment kernel

```text
K_w(D) = { f: D -> B : sum_{x in D} f(x) x^j = 0, 1 <= j <= w },
```

dimension `n-w`, minimum Hamming weight `>= w+1`. Fiber collisions correspond to
`{0,+-1}`-valued words of `K_w`: `f = 1_M - 1_{M'}` for distinct `M,M'` in one fiber. The
exact second-moment ledger (`\label{prop:capfr1-collision-ledger}`,
`cap25_cap_v13_raw.tex` L7696; restated as `prop:capfp-kernel`(c), L8173-8192):

```text
sum_z N_w(z)^2 = C(n,m) + sum_{ell>=delta} C(n-2 ell, m-ell) * T_w(ell),   delta = ceil((w+1)/2),
```

`T_w(ell)` the number of ordered disjoint `ell`-subset pairs with equal power sums through
`w` -- equivalently `{0,+-1}`-words of `K_w` with `ell` entries of each sign. `Gamma_2` is a
weighted balanced-ternary weight enumerator of `K_w`.

### 1.3 Removal -- the twist-primitive split (house definition)

The paid "quotient/planted" stratum (raw `\label{prob:capfp-A}`,
`cap25_cap_v13_raw.tex` L8147) is the twist-periodic mass. The twist group `H` (order `n`)
acts on `B^w` by `(z_j) -> (zeta^j z_j)` (`\label{prop:twist-orbit}`,
`grande_finale.tex` L743); fibers are constant on orbits. A prefix value `z` has twist
stabilizer `s(z) = gcd(n, {j : z_j != 0})` (`\label{prop:q-orbit-moment}`,
`grande_finale.tex` L797); `z` is PRIMITIVE iff `s(z)=1`, quotient/periodic iff `s(z)>1`
(`z=0` has `s=n`, the fully-periodic/planted fiber). We split
`Gamma_r = (primitive part) + (periodic part)` and take the primitive part as the "removed"
object -- i.e. what survives after the paid quotient/planted strata are stripped.

---

## 2. Measured curves -- raw vs removed (first data)

Five rows, `D = mu_n subset F_p` or `F_p^x`, exhaustive fiber histogram (rows 1-3) or
subset-size DP (row 4, `(257,64,34)`, since `C(64,34) ~ 2^60` is too large to enumerate),
exact `Fraction` arithmetic throughout, float only in the final `log2` reports. Validated
against `rem:capfp-gamma-measured` (raw L8228, printed table at L8231-8237):
`(17,16,8)`: `Gamma_2 = 1.000000 / 1.001539 / 1.137687` at `w=1/2/3`; `(41,20,10)`:
`1.000001 / 1.004136 / 1.502534` -- both match to all printed digits. Kernel ledger
`matches_hist=True` at every `w` tested. Independently re-derived bit-for-bit in this
packaging session (own reimplementation, not imported from `laneN_compute.py`) against
`laneN_outputs.json` -- see the companion verifier's gate ii.

### 2.A Growth of `log2 Gamma_r` in `r`, and the regime it lives in

| row | `w` | `lambda` (mean fiber) | `log2 Gamma_2` | `log2 Gamma_8` | regime |
|---|---|---|---|---|---|
| (257,64,34) | 1 | `6.3e15` | 0.00000 | **0.0000** | ultra-dense |
| (97,24,12) | 1 | `2.8e4` | 0.00000 | 0.0000 | dense |
| (41,20,10) | 2 | 110 | 0.00596 | 0.166 | dense |
| **(97,24,12)** | **2** | **287** | **0.00193** | **0.0550** | **dense (headline)** |
| (17,16,8) | 3 | 2.62 | 0.186 | 3.72 | Poisson |
| (41,20,10) | 4 | 0.065 | 4.04 | 31.9 | over-sat |

`log2 Gamma_r` is flat (`<0.17`) whenever `lambda >~ 100`, and `=0` (i.e. `Gamma_r=1`) to
machine precision at ultra-density (`lambda ~ 2^{45}`-scale). The log-log slope of
`log2 Gamma_r` vs `r` is `~2.4` in the dense/Poisson rows (Bell-number-like, polynomial in
`r`), dropping to `~1.4` when over-saturated. **The deployed frontier
(`lambda=2^{35.7}` at KB-MCA, independently recomputed in Sec 6) is squarely dense: its toy
proxies give `Gamma_r == 1`.**

### 2.B Monotone certificate `R_eff(r) := Gamma_r^{1/(r-1)} -> R` (PROVED; all 14 measured rows monotone)

| row | `w` | `R_eff(2)` | `R_eff(4)` | `R_eff(8)` | `R` (true `L^infinity`) |
|---|---|---|---|---|---|
| (97,24,12) | 2 | 1.00134 | 1.00269 | 1.00546 | **1.22477** |
| (41,20,10) | 3 | 1.50253 | 1.80347 | 2.27679 | **4.10342** |

At any feasible order (`r<=8`) the certificate sees only `R_eff(r) << R`; it reaches the
true `R` only as `r -> infinity`, since the max fiber (measure `|B|^{-w}`) dominates
`Gamma_r` only at `r ~ w log2|B| / log2 R`. This is why the moment order must be enormous
even though `Gamma_r` itself is benign (Sec 3-4 below).

### 2.C Removal effect in the dense bulk (the mandate's core question)

| row | `w` | `lambda` | `dR` (bits) | `d Gamma_8` (bits) |
|---|---|---|---|---|
| (257,64,34) | 2 | `2.5e13` | 0.000 | 0.006 |
| **(97,24,12)** | **2** | **287** | **0.080** | **0.0165** |
| (41,20,10) | 2 | 110 | 0.000 | 0.038 |
| (17,16,8) | 3 | 2.62 | 0.485 | 0.634 |
| (41,20,10) | 4 | 0.065 | 1.585 | 0.887 |

In the dense bulk (the frontier's regime), quotient/planted removal shaves `<0.08` bit off
`R` and `<0.04` bit off `Gamma_8` -- negligible; the constants are already `~1` and need no
taming. Removal bites (up to `1.6` bits) only at the Poisson/over-saturated boundary, and
even there inconsistently (`dR=0` at `(41,20,10)` `w=2`, where the heaviest fiber is itself
already primitive). **First-match quotient/planted removal is not the lever that tames the
moment constants at the frontier.**

### 2.D Why removal can't help: the collision mass is primitive (exact ledger)

`Gamma_2 = 1/lambda [diag] + prim_off + quot_off`, exact, `(17,16,8)`:

| `w` | `Gamma_2` | diag | prim_off | quot_off | quot fraction |
|---|---|---|---|---|---|
| 1 | 1.000000 | 0.00132 | 0.98999 | 0.00868 | 0.9% |
| 2 | 1.001539 | 0.02246 | 0.97532 | 0.00377 | 0.4% |
| 3 | 1.137687 | 0.38174 | 0.69194 | 0.06401 | 5.6% |
| 4 | 6.732633 | 6.48959 | 0.24204 | 0.00101 | 0.015% |

The quotient (removable) off-diagonal is `<=6%` of `Gamma_2` at every measured `w`; the
primitive/aperiodic part carries the mass (`\label{prop:gamma2-ledger}`,
`grande_finale.tex` L1071, made numerical here). SP/BC-style removal leaves the Q-moment
essentially unchanged.

---

## 3. Brick 1 -- the exact unconditional order floor (PROOF)

**Statement.** Because `Gamma_r >= 1` for all `r` (`prop:moment-sandwich` / raw
`prob:capfp-gamma`, a power-mean fact true for *any* distribution), the finite criterion
(MC) forces

```text
r >= r0 := ceil( w log2|B| / Delta )
```

unconditionally, achieved iff `Gamma_r=1` (perfect prefix flatness) at that order, and
lowerable by no removal, cancellation, or twist-orbit argument, since `Gamma_r >= 1` uses
nothing about the distribution.

**Proof.** Set `log2 Gamma_r = 0` (its infimum, by `Gamma_r>=1`) in (MC):
`w log2|B| <= r Delta`, i.e. `r >= w log2|B| / Delta`; `r` an integer forces the ceiling.
One line, no new machinery; strengthens `\label{rem:finite-moment-order}`
(`grande_finale.tex` L739) and `prob:row-sharp-q` (L1754).

**The exact floors**, computed from the exact integer field size
(`P_KB = 2^31-2^24+1 = 2130706433`, `P_M31 = 2^31-1 = 2147483647`) and the 4-decimal `Delta`
printed in `grande_finale.tex`'s own adjacent-margin table:

| row | `w` | `Delta` (bits) | `r0` |
|---|---|---|---|
| KB-MCA | 67471 | 22.1969 | **94196** |
| KB-list | 67471 | 22.0109 | 94992 |
| M31-MCA | 67447 | 3.2589 | **641584** |
| M31-list | 67447 | 3.0730 | 680397 |
| L4-rung | 4216 | 22.1969 | **5886** |

**This independently reproduces PR #366's own shipped moment-route numbers to the digit**
(`kb_mca_conjq_route_margins_v1.json`, `moment_route`: `r_at_bar=94196` at `L_0`/KB-MCA,
`r_at_bar=5886` at `L_4`) -- and upgrades both from route-cut estimates computed "at the
optimistic case `log2(Gamma_r)~0`" to **proved unconditional lower bounds**, since Brick 1
shows `log2 Gamma_r >= 0` always, not merely optimistically. No removal, quotient routing,
or twist-orbit cancellation can lower these floors: `Gamma_r>=1` is distribution-free.

*A note on a small, fully explained variant.* `laneN_analysis.md`'s own prose gives
`94200`, `94996`, `680396`, `5889` for four of these five rows (M31-MCA's `641584` is
unanimous), computed via `w log2|B| / Delta` with `log2|B|` hardcoded to 2 decimals
(`30.99` KoalaBear, `31.00` Mersenne-31) in `laneN_compute.py`'s deployed-rows table. The
`94200/94996/5889` vs `94196/94992/5886` gap (`-4,-4,-3`) is fully explained by that
2-decimal rounding of `log2(p_KB)` (`30.99` vs the exact `30.98868468744926` -- a
`~0.0013%` relative difference, amplified by `w~67471` or `w~4216`); Mersenne-31 is
essentially unaffected (`log2(p_M31) = 30.999999999328193` rounds to `31.00` with negligible
error). Separately, the printed `680396` for M31-list is itself off by one against its own
underlying raw value `680396.0299...`: `ceil` of that is `680397`, not `680396` -- a
rounding/truncation slip in the prose (not in `laneN_outputs.json`'s stored float, which is
correct). This note ships `94196 / 94992 / 641584 / 680397 / 5886` throughout, since these
(a) use genuinely exact arithmetic from raw constants and (b) independently match PR #366's
own shipped values to the digit. See the JSON's `found_vs_claimed_corrections` for the
full account.

---

## 4. Brick 2 -- the monotone certificate (PROOF)

**Statement.** `r -> R_eff(r) := Gamma_r^{1/(r-1)}` is non-decreasing and increases to
`R = |B|^w max_z mu(z)` as `r -> infinity` (`ell^p`-norm monotonicity). Combined with the
proved upper bound `Gamma_r <= R^{r-1}` (raw `\label{prop:capfp-anchors}`,
`cap25_cap_v13_raw.tex` L8157, bound printed at L8160), this pins the exact minimal order at
which (MC) *can* hold given the true `R`:

```text
r_min(R) = ceil( (w log2|B| - log2 R) / (Delta - log2 R) ),   finite iff R < 2^Delta,
```

`-> r0` (Brick 1) as `R -> 1`, `-> infinity` as `R` approaches `2^Delta` from below. So the
moment method certifies `R<=2^Delta` at order `r_min(R)` **iff Q is true**; it is not a
route around Q but a high-moment certificate *for* it. Monotonicity was verified on all 14
measured `(row,w)` pairs of Sec 2 (100% pass: every one of `F17x_16_8` `w=1..4`,
`mu20_F41_10` `w=1..4`, `mu24_F97_12` `w=1..4`, `mu64_F257_34` `w=1..2` is non-decreasing
across `r=2..8`), re-verified live on a subset by the companion verifier (gate iii), which
also checks the formula's finiteness-iff-`R<2^Delta` branch directly on synthetic `R`
values.

**The `R`-insensitivity table** (KB-MCA, `w=67471`, `Delta=22.1969`, exact-integer method):

| `R` | `log2 R` | `r_min` |
|---|---|---|
| `2^0` (`=1`, Brick 1 floor) | 0.000 | 94196 |
| `2^0.001` | 0.001 | 94200 |
| `2^0.01` | 0.01 | 94238 |
| `2^0.1` | 0.1 | 94622 |
| `2^1` (full doubling) | 1.0 | **98639** |

Doubling `R` (`log2 R`: `0 -> 1`) inflates KB-MCA's order from `94196` to `98639` -- a
**4.72% increase**. The same pattern holds at the other rows (exact-integer method):
M31-MCA (`w=67447`, `Delta=3.2589`) goes `641584 -> 643559 -> 661894 -> 925609` across the
same `R` menu; L4-rung (`w=4216`, `Delta=22.1969`) goes `5886 -> 5889 -> 5913 -> 6164`.
`r_min` is near-insensitive to `R` across three orders of magnitude: the moment order is
robustly `~ w log2|B| / Delta` regardless of the measured, benign (`~1`) value of
`Gamma_r`/`R` in the dense bulk.

---

## 5. The regime law -- a Poisson closed-form model (heuristic brick, labeled)

Modeling the `|B|^w` fibers as `N(z) ~ Poisson(lambda)`, `lambda = C(n,m)|B|^{-w}`:

```text
Gamma_r ~= E_{N~Poi(lambda)}[(N/lambda)^r] = B_r(lambda) / lambda^r,   B_r = Bell/Touchard polynomial.
```

Matched by the data: `lambda >> 1` (dense/frontier) gives `Gamma_r -> 1` (matching the
`=1.000000`-to-machine-precision ultra-dense measurement); `lambda=O(1)` (Poisson boundary)
gives `log2 Gamma_r ~ r log r` (Bell growth, matching the measured log-log slope `~2.4`);
`lambda<1` (over-saturated) gives `Gamma_r ~ lambda^{1-r}` (matching measured slopes
`3-5.6`). The model's constant is measurably off by `10-40%` at the boundary (real tail
heavier; proper-subgroup rows are heavier than Poisson, while the full-multiplicative-group
row is sub-Poisson/flatter by twist-orbit symmetry, `prop:twist-orbit`) -- labeled
heuristic, not a theorem. **Since the deployed rows use the full, maximally symmetric group
structure and land at `lambda` between `2^{20.7}` and `2^{35.9}` (Sec 6), the model
predicts `Gamma_r=1+o(1)` at every accessible `r` -- i.e. the entire difficulty is Brick 1's
order floor, not `Gamma_r` growth.**

---

## 6. Extrapolation -- EXPERIMENTAL (label loudly), and an independent cross-check of `lambda`

`laneN_analysis.md` asserts, in prose, that the deployed KB-MCA row sits at
`lambda=2^{35.7}` -- a claim about the *deployed* row, outside the toy data's reach, and not
accompanied by a JSON computation. This packaging session independently recomputed it from
the same raw constants `verify_conjq_rung_routes_dead.py` uses (`N=2^21`, `K=2^20`,
`M_SAFE=1116048`, `W_SAFE=67471`), via `log2(lambda) = log2 C(n,m) - w log2(p)`
(`math.lgamma`, no huge exact integers needed):

| row | `n` | `m` | `w` | `log2 lambda` |
|---|---|---|---|---|
| KB-MCA | `2^21` | 1116048 | 67471 | **35.7352** |
| KB-list | `2^21` | 1116047 | 67471 | 35.9212 |
| M31-MCA | `2^21` | 1116024 | 67447 | 20.7411 |
| M31-list | `2^21` | 1116023 | 67447 | 20.9270 |
| L4-rung (scale-16) | `2^17` | 69753 | 4216 | 23.1390 |

`35.7352` matches Lane N's `2^{35.7}` claim to the printed digit. It **also** independently
matches Lane M's concurrent, uncommitted in-flight cross-check
(`saturated_bc_budget_fit_v1.json`, `margins_table[0].log2_floor = 35.7352`, derived via a
completely different route -- the `prob:saturated-bc` margin identity
`margin = log2(B*) - log2(C(n,a+)*p^-w)`, not the Q-moment formalism at all) to 4 decimals,
on every one of the 5 rows. This is a three-way, two-lane cross-validation (Lane N's prose
claim, Lane M's independently derived JSON value, and this packaging session's own
from-scratch recompute) that the deployed frontier really does sit deep in the measured
dense-bulk regime (`log2 lambda` between `20.7` and `35.9`, i.e. `lambda` between `~1.7e6`
and `~1e11`) where the toy data shows `Gamma_r = 1+o(1)`.

**The moment-order extrapolation** (`r_min(R)` at the deployed rows and L4; `R=1` column =
Brick 1's floor; all entries recomputed by the exact-integer method of Sec 3-4, so the table
is internally consistent -- see Sec 3's "small, fully explained variant" paragraph for why
this differs slightly from `laneN_analysis.md`'s own rounded-log2B numbers):

| row | `w log2|B|` | `R=1` (Brick 1) | `R=2^0.01` | `R=2^0.1` | `R=2^1` |
|---|---|---|---|---|---|
| KB-MCA | 2090837.5 | 94196 | 94238 | 94622 | 98639 |
| M31-MCA | 2090857 | 641584 | 643559 | 661894 | 925609 |
| L4-rung | 130648.3 | 5886 | 5889 | 5913 | 6164 |

**What the toys cannot reach.** The dense-bulk law `lambda >> 1 => Gamma_r ~= 1` is measured
only at `w<=4` (ultra-dense only to `w=2`). Its persistence to the deployed `w=67471` (or
`67447`, or `4216`) is the unmeasured extrapolation, and is **exactly the open
`prob:row-sharp-q` flatness** -- the moment reformulation does not escape it. Status:
**EXPERIMENTAL**; supports "route not killed by moment growth", does **not** support "route
closes" (that needs deployed-`w` flatness, i.e. Q itself).

---

## 7. Verdict

**Alive as a certificate format; non-circumventing; the obstruction is an exact order
floor, not `Gamma_r` growth.**

- **Not dead by moment growth.** The feared scenario (`Gamma_r` exponential/factorial in
  `r`, so even `r~10^5` is insufficient) is measured **FALSE** at the frontier's regime:
  `Gamma_r` grows that way only at mean fiber `lambda=O(1)` (Poisson) or `<1`
  (over-saturated); the deployed `lambda` (`2^{20.7}` to `2^{35.9}` across the four rows,
  Sec 6) gives `Gamma_r=1+o(1)` (Poisson model + ultra-dense toy measurement).
- **Not a shortcut.** By Brick 1 the order is `>=94196` (KB-MCA) / `>=641584` (M31-MCA) /
  `>=5886` (L4) **unconditionally**, and by Brick 2 it closes **iff `R<2^Delta`** = Q
  itself. Removal does not lower it (Sec 2.C-2.D).
- **Net.** The moment route converts the finite-adjacent problem into "evaluate one
  balanced-ternary weight enumerator of `K_67471(D)` at order `r~94000` and check
  `Gamma_r <= 2^{r Delta - w log2|B|}`" -- a well-posed finite computation, benign in its
  constant, but of astronomical order and content-equivalent to the flatness it would need
  to prove. This packet's contribution is the first data pricing this exactly, and the
  proved order floor.

---

## 8. Honest scope

- The measured `Gamma_r` data (Sec 2) covers only toy rows at `w<=4`; the ultra-dense
  exhibit reaches `w=2`. **No deployed-`w` `Gamma_r` value is computed or computable here.**
- The dense-bulk law `lambda>>1 => Gamma_r=1+o(1)` is a measured pattern at those toy scales
  plus a heuristic (Poisson) explanation (Sec 5); its persistence to the deployed rows
  (`w=67471/67447/4216`) is **not measured** and **is** `prob:row-sharp-q` itself --
  extrapolation across this gap is labeled EXPERIMENTAL throughout (Sec 6) and is not
  claimed as evidence beyond "not obviously false."
- Brick 1 and Brick 2 (Sec 3-4) are exact and unconditional, but they are one-line
  consequences of already-proved facts (`Gamma_r>=1`; `Gamma_r<=R^{r-1}`); they resolve
  nothing about the true value of `R`, only the *order* a moment proof would need.
- The frontier `lambda` cross-check (Sec 6) independently confirms a *placement* claim
  (which regime the deployed rows sit in), not a `Gamma_r` measurement at those rows.

---

## 9. Non-claims

This note does **not** prove any of the following:

```text
prob:row-sharp-q (grande_finale.tex \label{prob:row-sharp-q}),
Gamma_r at any deployed w (67471, 67447, or any full-scale row),
that the frontier edge (1116047,1116048) moves in either direction,
prob:saturated-bc, or anything about Lane M's concurrent object beyond the shared
  moment-kernel citation (thm:q-implies-sp).
```

It does not alter any verdict, integer, ladder shape, or margin of PR #366
(`kb_mca_conjq_route_margins_v1.json` / `cap25_v13_qfin_rung_routes_dead.md`) -- it upgrades
that PR's two moment-route numbers (`94196`, `5886`) from estimates computed "at the
optimistic case `log2(Gamma_r)~0`" to proved unconditional floors, and touches nothing else
of that PR's content. It does not modify, import from, or depend on `laneN_compute.py`,
`laneN_fit.py`, or `laneN_outputs.json` (independent reimplementation throughout; Sec 3
documents one small, fully explained numerical variance against `laneN_analysis.md`'s own
prose, not against its underlying stored data, which this note's own recompute matches
bit-for-bit).

**A label note.** The raw manuscript's `Gamma_r` definition is labeled `prob:capfp-gamma`
(`cap25_cap_v13_raw.tex` L8135, a `\begin{remark}` environment) -- not `prop:capfp-gamma`.
This note and its JSON use the verbatim label throughout; see the JSON's `cross_refs` for
every label's exact environment type and line.

The Poisson closed-form (Sec 5) is a heuristic curve-fit, not a theorem.

---

## 10. Verifier contract

`experimental/scripts/verify_gammar_order_floor.py` is zero-arg, stdlib-only,
deterministic, and supports `--full` / `--tamper-selftest`. Five gates:

- **gate i** -- Brick-1 floor arithmetic: recomputes `w`, `|B|` (exact integer field size),
  and `Delta` (the 4-decimal audited constant) for five rows from raw constants, and
  `r0 = ceil(w log2|B| / Delta)` via exact `ceil` arithmetic; cross-checks the KB-MCA and L4
  values against PR #366's own shipped numbers (`94196`, `5886`, embedded as literals with
  a provenance comment, since this verifier does not read another PR's branch/worktree).
- **gate ii** -- live exact `Gamma_r` recomputation (`Fraction`, independent
  reimplementation, not imported from `laneN_compute.py`): by default, `F17x_16_8`
  (`w=1..4`), `mu24_F97_12` (`w=2`, the dense-bulk exhibit, `log2 Gamma_8=0.0550<0.17`), and
  `mu64_F257_34` (`w=1`, the ultra-dense exhibit, `Gamma_r=1` to machine precision);
  `--full` adds `mu20_F41_10` (all `w`), `mu24_F97_12` (`w=1,3,4`), and `mu64_F257_34`
  (`w=2`, the DP-heavy row, `~50s` alone).
- **gate iii** -- Brick-2 monotonicity: checks `R_eff(r)` is non-decreasing on every row
  computed by gate ii, checks the `r_min(R)` formula's finiteness-iff-`R<2^Delta` branch on
  synthetic `R` values (above and below `2^Delta`), and reproduces the `4.72%`
  R-insensitivity figure at KB-MCA.
- **gate iv** -- balanced-ternary kernel ledger: recomputes the exact `Gamma_2` ledger
  (`prop:capfr1-collision-ledger`) on `F17x_16_8` `w=2` (`--full`: all `w`), checks
  `matches_hist` and the `T_w`/`T_w^prim` censuses against the shipped JSON.
- **gate v** -- removal comparison: recomputes raw-vs-primitive `R` and `Gamma_8` on
  `mu24_F97_12` `w=2` live, checks the dense-bulk shave is `<0.04` bit (measured `~0.0165`).

Hidden self-test: `python3 verify_gammar_order_floor.py --tamper-selftest` corrupts one
guarded value per gate and confirms the gate then reports a mismatch (CAUGHT). Expected
zero-arg runtime: well under `90s` (dominated by `mu24_F97_12`'s exhaustive enumeration,
single digit to low double-digit seconds); `--full` runtime: a couple of minutes (dominated
by `mu64_F257_34` `w=2`'s DP, `~50s`, and the full `mu24_F97_12` `w=1..4` sweep).

---

## Refs

- `experimental/grande_finale.tex` -- `\label{prop:moment-sandwich}` (L692),
  `\label{thm:moment-q}` (L708), `\label{rem:finite-moment-order}` (L739),
  `\label{prop:mode-null-false}` (L759), `\label{prop:twist-orbit}` (L743),
  `\label{prop:q-orbit-moment}` (L797), `\label{prop:gamma2-ledger}` (L1071),
  `\label{thm:coeff-quotient-extract}` (L1002), `\label{thm:q-implies-sp}` (L1587),
  `\label{prob:row-sharp-q}` (L1754), `\label{prob:saturated-bc}` (L1768), the
  adjacent-margin table (L183-186, L1662-1665).
- `experimental/cap25_cap_v13_raw.tex` -- `\label{prob:capfp-gamma}` (L8135),
  `\label{prob:capfp-A}` (L8147), `\label{prop:capfp-anchors}` (L8157),
  `\label{prop:capfp-kernel}` (L8173), `\label{subsec:capfr1-Q-kernel}` (L7661),
  `\label{prop:capfr1-collision-ledger}` (L7696), `\label{rem:capff1-calibration}` (L7118),
  `\label{rem:capfp-gamma-measured}` (L8228), `\label{prob:capfp-R1}` (L8278).
- PR #366 (Holm Buar, OPEN, `v13-raw-conjq-rung-routes-dead`) --
  `experimental/notes/thresholds/cap25_v13_qfin_rung_routes_dead.md`,
  `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_route_margins_v1.json` --
  the moment-route numbers this packet upgrades to proved floors.
- PR #368 (`L1: bounded-excess structure (C' localized)`) and PR #364
  (`L1: m*(19)<=9 -- vacancy band refuted at p=571`) -- L1 track, disjoint object, cited for
  completeness, no dependence in either direction.
- Lane M's concurrent, same-session, in-flight work (branch
  `thresholds-saturated-bc-budget-fit`, uncommitted at packaging time) --
  `experimental/notes/thresholds/cap25_v13_saturated_bc_budget_fit.md`,
  `experimental/data/certificates/frontier-adjacent/saturated_bc_budget_fit_v1.json` -- the
  joint-closer object on `prob:saturated-bc` (`thm:q-implies-sp` makes SP/BC a sub-sum of
  this packet's off-diagonal); its `margins_table` independently cross-validates this
  packet's frontier `lambda` values (Sec 6) to 4 decimals.
- `experimental/data/certificates/frontier-adjacent/gammar_order_floor_v1.json` -- this
  note's data.
- `experimental/scripts/verify_gammar_order_floor.py` -- this note's verifier.
