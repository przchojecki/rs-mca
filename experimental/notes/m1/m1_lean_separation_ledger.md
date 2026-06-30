# M1 Quotient/Aperiodic Separation Ledger — stdlib Lean formalization

**Status: EXPERIMENTAL, compiler-checked.** Pure stdlib Lean 4 (no mathlib), toolchain
`leanprover/lean4:v4.31.0`. Every theorem below is kernel-checked and axiom-clean:
`#print axioms` shows only `propext`/`Quot.sound`/`Classical.choice` (Lean's standard
core) on the proved results, with **no `sorryAx` and no `Lean.ofReduceBool`** (no
`sorry`, no `native_decide`). Builds in ~1s after the one-time toolchain fetch.

## What this is

A machine-checked formalization of the *separable* (structured) half of the M1
residue-line program, distilled from:

* `notes/m1/m1_quotient_periodic_overlap_profile.md` (PROVED) — the quotient-periodic
  and general fiber-occupancy overlap ledger;
* Paper B `tex/slackMCA_v4.tex` — the exact quotient-periodic bad-slope floor
  `A(N',ell')` and the two-term positive bound `emca <= (aperiodic + quotient)/q_gen`;
* `notes/thresholds/f17_32_finite_mca_threshold.tex` — the solved finite row and its
  field-count gate.

The point (per `towards-prize.md`: *"separate quotient-periodic floors from aperiodic
mass"*, with the quotient term kept explicit) is to certify every **structured** family
exactly, so the irreducible **aperiodic** strict-overlap bound is isolated as a single
typed target a future analytic proof must inhabit.

## Files

* `experimental/lean/rs_mca_formalization/RsMca/QuotientOverlap.lean` — the M1 ledger
  (Lane V "V7 quotient-periodic locator").
* `experimental/lean/rs_mca_formalization/RsMca/FiniteThreshold.lean` — the finite-row
  gates (Lane V "V2 agreement/radius staircase", "V3 `7*2^128 > 17^32`").

Both are imported by `RsMca.lean`; `lake build` checks them.

## QuotientOverlap.lean — the structured ledger

Stdlib binomials (`choose` by Pascal recursion, since mathlib's `Nat.choose` is
unavailable): `choose_zero_right`, `choose_one_right`, `choose_eq_zero_of_lt`,
`choose_self`, `choose_symm` (all proved).

**Whole-fiber quotient-periodic family** (overlap-profile §Claim / §M1 Impact):
`qpFamilySize = C(N,L)`, `exchangeCodegree`, `orderedExchangeCount`; and the proved
strict-overlap gating —
* `qpFamily_absent_of_not_dvd` — the family is present at exact size `s` only if `m | s`;
* `not_strictActive_of_t_le_m` — if `t <= m`, no strict high-overlap pair exists;
* `strictSize_iff_le_div` — the active exchange prefix is `h <= (t-1)/m`;
* `firstBand_div_eq_one` — the first band `m < t <= 2m` admits only `h = 1`;
* `exactSupport_dvd_iff_offset`, `maximalDither_kills` — the dither divisibility rule
  (`m | k0 => (m | s <=> m | (t-r))`; maximal dither `t-r = 1` kills every scale `m>=2`);
* `firstExchange_codegree_scaled` — `s(n-s) = m^2 * L(N-L)`.

**General fixed fiber-occupancy class** (overlap-profile §General Fiber-Occupancy):
`occClassSize N m h = multinomial(N;h) * prod_a C(m,a)^{h_a}`, with `occCount`/`occWeight`
the histogram constraints. The key theorem
`occClassSize_wholeFiber : occClassSize N m (wholeFiberHist N L m) = qpFamilySize N L`
holds **for all `N,L,m`** (via `multinomial_two`, the `*_replicate_zero` lemmas, and
`choose_symm`), so the occupancy ledger genuinely GENERALIZES the whole-fiber family.
`decide`-checked instances reproduce the brute-force counts (one-remainder
`occClassSize 3 2 [1,1,1] = 12 = |A_REM|`; partition `3 + 12 = 15 = C(6,2)`).
`OccupancyPartition` records the layer-exhaustion target `sum_h |A_h| = C(Nm,s)`.

**The aperiodic target** (the separation): `layerCodegree s n j = C(s,j)C(n-s,j)` (the
Johnson layer codegree), `qpCodegree` (the whole-fiber contribution), and
`aperiodicResidual := layer - qp`. Proved: `aperiodicResidual_off_grid` — off the
`m`-grid the entire strict-overlap codegree is aperiodic (the quotient floor explains
none of it). `M1AperiodicBound` types the lone remaining obligation
(`exists B, aperiodicResidual <= n^B`), and the capstone `MCANumeratorSplit` records
Paper B's two-term split `numerator <= aper + quotientFloor` with `aper` poly.

**Paper B exact quotient floor**: `quotientFloor n1 ellp` = `A(N',ell')`
(`N' = 2 n1`), `decide`-checked to reproduce Paper B's counts (`= 3280` at `(16,9)`,
`= 21523360` at `(32,17)`); `QuotientFloorHalfClosed` records the rate-`1/2` closed form
`(3^{n1}-1)/2`.

## FiniteThreshold.lean — the solved row `RS[F_17^32, H, 256]`

`field_count_gate : 6*2^128 < 17^32 < 7*2^128` (axiom-FREE `decide`), `field_floor`
(`floor(17^32/2^128) = 6`), `Bfin a = 513 - a` with `Bfin_samples`, and
`safe_iff_agreement_ge_507 : Bfin a * 2^128 <= 17^32 <-> 507 <= a` — the exact
safe/unsafe transition (`r = 5` safe, `r = 6` unsafe).

## Verify

```bash
cd experimental/lean/rs_mca_formalization
lake build                       # ~1s; checks every theorem
# axiom hygiene, e.g.:
echo 'import RsMca.QuotientOverlap
#print axioms RsMca.occClassSize_wholeFiber
#print axioms RsMca.aperiodicResidual_off_grid' > /tmp/ax.lean
lake env lean /tmp/ax.lean       # only propext/Quot.sound; no sorryAx, no ofReduceBool
```

## Scope / non-claims

This certifies the *structured* side and isolates the aperiodic target; it does **not**
prove the M1 local limit. Two pieces are deliberately left as recorded targets because a
clean stdlib encoding is not available (they need finite-set sums / polynomial
coefficient extraction, i.e. mathlib): the general `OccupancyPartition`, the general
`QuotientFloorHalfClosed`, and the per-occupancy exchange-codegree generating function
`H_h(y)` (the `P_{a,b}(y)` transition polynomials). All numeric claims are additionally
brute-force-verified on a finite grid by stdlib Python.
