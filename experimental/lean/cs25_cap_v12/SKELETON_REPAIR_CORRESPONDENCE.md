# Skeleton Falsity-and-Repair Correspondence (`QuotientRemainder` / `ECFFT` / `InterleavingTransfer` / `AperiodicHankel`)

Status: **conservative** — this packet is a *statement-layer* audit-and-repair of
the remaining `cs25_cap_v12` skeleton files (the README's "main completion
queue"), plus three genuine discharges.  Five skeleton statements were **false
as written** and carry machine-checked negation lemmas; each is repaired to the
paper's statement and (except where discharged) stays honestly sorried.  Three
statements are newly **PROVED**: the repaired `prop_graded_rational_floor`, the
(unchanged-statement) `cor_quantitative_first_grid_floor`, and the new
`cor_first_grid_cap_one` — together with the explicit witness lemma
`hasList_first_grid` these put the paper's unconditional deployed-row
**first-grid cap chain (`c = 1`) end-to-end in Lean**.  Two further statements
receive PLAUSIBLE-graded untied-binder repairs with **no falsity claims**
(`cor_ecfft_macroscopic`, the two `AperiodicHankel` certificates).  Negation
lemmas are **never sorried**; every falsity claim in this packet is a fully
proved Lean theorem.

Base: `3404d21b64c876c6d9b995ad3e29d7120ab27a54` (origin/main at packet time,
the reviewed-PR integration sweep).  None of the four target modules had been
touched by any open PR at packet time.

Source (paper): `tex/cs25_cap_v12.tex` at the same base —
`sec:quotient-remainder` (`w_c` display `:725`–`:733`,
`lem:quotient-remainder-prefix` `:735`, `def:prefix-fiber-certificate` `:806`,
`lem:heaviest-prefix-locator-floor` `:842`, `thm:quotient-remainder-deep-floor`
`:914`, `cor:quantitative-first-grid-floor` `:993`, `cor:augmented-slack-one`
`:1063`–`:1078`, `cor:first-grid-cap` `:1091` with proof consuming `c = 1` at
`:1153`), syndrome conventions (`:1550`–`:1560`, `:2065`–`:2075`),
`lem:regular-exact-agreement-eliminant` `:2112`,
`thm:regular-closed-ball-hankel-packing` `:2135`,
`prop:graded-rational-floor` `:5209`, `cor:ecfft-macroscopic` `:5241`
(band `:5251`), `thm:explicit-head-floor` `:5333` (smoothness `:5334`),
`thm:explicit-pairs` `:5369` (`L₀ :=` at `:5370`).

Source (Lean): `experimental/lean/cs25_cap_v12/cs25_cap_v12/` —
`QuotientRemainder.lean`, `ECFFT.lean`, `InterleavingTransfer.lean`,
`AperiodicHankel.lean` (plus `ECFFT`/`InterleavingTransfer` now import
`QuotientRemainder` for the proved deep floor and the shared constants
pigeonhole).

## Statement map

| Paper statement | Lean declaration | Packet action |
| --- | --- | --- |
| `w_c(s, σ)` prefix weight (`:725`–`:733`) | `RSCap.certWeight` | new def (repair input) |
| `lem:quotient-remainder-prefix` (`:735`) | `RSCap.lem_quotient_remainder_prefix` | **repaired** (weight tied to `certWeight`; pre-repair statement FALSE — `RSCap.lem_quotient_remainder_prefix_false` proved); still sorried |
| `lem:heaviest-prefix-locator-floor` (`:842`) | `RSCap.lem_heaviest_prefix_locator_floor` | **repaired** (heaviest data `(I, H)` existential; pre-repair statement FALSE — `RSCap.lem_heaviest_prefix_locator_floor_false` proved); still sorried |
| `thm:quotient-remainder-deep-floor` (`:914`) | `RSCap.thm_quotient_remainder_deep_floor` | unchanged (already PROVED) |
| `cor:quotient-remainder-trigger` (`:971`) | `RSCap.cor_quotient_remainder_trigger` | unchanged (already PROVED) |
| `cor:augmented-slack-one`, `c = 1` clause (`:1063`–`:1078`) | `RSCap.hasList_first_grid` | new, **PROVED** (explicit `x^{k+1}` witness, `C(n, k+1)` locator codewords) |
| `cor:quantitative-first-grid-floor` (`:993`) | `RSCap.cor_quantitative_first_grid_floor` | statement unchanged, **PROVED** (census 4 → 3 for the file) |
| `cor:first-grid-cap`, `c = 1` clause (`:1091`, consumed at `:1153`) | `RSCap.cor_first_grid_cap_one` | new, **PROVED** (both `ε_ca` and `ε_mca` clauses) |
| `cor:first-grid-cap`, general `c` (`:1091`) | `RSCap.cor_first_grid_cap` | statement audited — **no defect found** (its `hyp` matches the paper exactly, no `\|B\|` division, `:1095`–`:1097`); `c > 1` out of scope, still sorried |
| `prop:rational-floor` (`:4837`) | `RSCap.prop_rational_floor` | audited — `hfB`/`hgB` correctly present, no defect found; still sorried |
| `cor:ecfft-onestep` (`:4863`) | `RSCap.cor_ecfft_onestep` | audited — no defect found; still sorried |
| `prop:graded-rational-floor` (`:5209`) | `RSCap.prop_graded_rational_floor` | **repaired** (deep-band radius; pre-repair statement FALSE — `RSCap.prop_graded_rational_floor_false` proved) and **PROVED** (wrapper over the deep floor; census 4 → 3 for the file) |
| `cor:ecfft-macroscopic` (`:5241`) | `RSCap.cor_ecfft_macroscopic` | **repaired** (`hΔhi : Δ ≤ 1/512` band bound + `hfB`/`hgB` ties), graded PLAUSIBLE, **no falsity claim**; still sorried |
| `lem:inter` CA/MCA (`lem:inter`) | `RSCap.lem_inter_eca`, `RSCap.lem_inter_emca` | unchanged (already PROVED) |
| `thm:explicit-head-floor`(i) (`:5333`) | `RSCap.thm_explicit_head_floor_even` | **repaired** (`hsmooth` restored per `:5334`; pre-repair statement FALSE — `RSCap.thm_explicit_head_floor_even_false` proved); still sorried |
| `thm:explicit-head-floor`(ii) (`:5333`) | `RSCap.thm_explicit_head_floor_odd` | **repaired** (same `hsmooth`), same-class flag, graded PLAUSIBLE, **no falsity claim**; still sorried |
| `thm:explicit-pairs` (`:5369`) | `RSCap.thm_explicit_pairs` | **repaired** (`hL₀ : ⌈(q−n)/K⌉ ≤ L₀` per `:5370`; pre-repair statement FALSE — `RSCap.thm_explicit_pairs_false` proved); still sorried |
| `Syn` twist/syndromes (`:1550`–`:1560`) | `RSCap.synTwist`, `RSCap.rsSyndrome` | new defs (repair input) |
| `lem:regular-exact-agreement-eliminant` (`:2112`) | `RSCap.lem_regular_exact_agreement_eliminant` | **repaired** (`u`/`v` tied to `rsSyndrome dom f/g`), graded PLAUSIBLE, **no falsity claim**; still sorried |
| `thm:regular-closed-ball-hankel-packing` (`:2135`) | `RSCap.thm_regular_closed_ball_hankel_packing` | **repaired** (same syndrome tie), graded PLAUSIBLE; still sorried |
| `thm:scanner-checkable-residual-aperiodic-ledger` | `RSCap.thm_scanner_checkable_residual_aperiodic_ledger` | unchanged (already PROVED; abstract chart predicates, no tie needed) |
| (packet infrastructure) | `RSCap.RSpoly_one_const`, `RSCap.hasList_const_le_card` | new, **PROVED** (constants pigeonhole used by the negation certificates) |

## Falsity findings (all machine-checked; none sorried)

All five defects are **formalization defects, not paper defects** — in each case
the quoted paper line carries the missing constraint.

1. **`lem_quotient_remainder_prefix` (pre-repair): universally quantified
   certificate weight.**  `wₒ` was an implicit binder appearing only in the
   denominator `|B|^{wₒ}`; at `wₒ = 0` the statement demanded a
   pigeonhole-free list of the full count `M_{c,m,s}`.
   Negation `lem_quotient_remainder_prefix_false`: `F = ZMod 17`, `dom` the 16
   units in primitive-root order `3^0, …, 3^15` (squaring is 2-to-1, so
   `DomSmooth` holds by `decide`), `B = ⊤`, `(c, N, K, m, s, A₀, wₒ) =
   (2, 8, 1, 4, 0, 8, 0)`: the bound demands `L ≥ C(8,4) = 70`, but
   `RS[F, D, 1]` is the 17 constants (`hasList_const_le_card`).  Paper fix:
   the denominator is `|B|^{w_c(s,σ)}`, `σ = A₀ − K` (`:752`); repaired with
   `certWeight c s (A₀ − K)` (here `w_2(0,7) = 3`, true floor `⌈70/17³⌉ = 1` —
   consistent).
2. **`lem_heaviest_prefix_locator_floor` (pre-repair): inverted quantifier on
   `H`.**  `H` was universal, constrained only from below by the coarse bound;
   the same `ZMod 17` instance with `H = 70`, `wₒ = 0` satisfies
   `hHbound : 70/1 ≤ 70` while 70 distinct constants do not exist.
   Negation `lem_heaviest_prefix_locator_floor_false`.  Paper fix: `H` is the
   construction's heaviest prefix fiber `H_{c,m,s}^K` (`:806`–`:860`);
   repaired by existentially quantifying certified data `(I, H)` with
   `0 < I ≤ |B|^{w_c}` and `M/I ≤ H` (the paper's chain
   `H ≥ ⌈M/I⌉ ≥ ⌈M/|B|^w⌉` divided through).
3. **`prop_graded_rational_floor` (pre-repair): vacuous radius hypothesis.**
   The only radius constraint was `1 − k/n ≤ 1` (always true) with `hlist` at
   the conclusion radius `δ` itself.  Negation
   `prop_graded_rational_floor_false`: `F = ZMod 2`, `ι = Fin 1`, `f = X`,
   `g = 1`, `(a, e, N, k, H, δ) = (1, 0, 1, 1, 1, 1)` — at `δ = 1` every pair
   is `intClose`, so `ε_ca = 0 < 1/4 = 𝓔_{2,1}(1)`.  Paper fix: the floor is
   stated at the deep radius `1 − am/n`, `am ≥ K` (`:5209`), band-assembled
   below capacity; repaired to a deep-agreement `A > k` list plus the band
   `δ ∈ [1 − A/n, 1 − k/n)` — and then **proved** as a wrapper over
   `thm_quotient_remainder_deep_floor`.
4. **`thm_explicit_head_floor_even` (pre-repair): smoothness dropped.**  The
   paper requires `D` `(φ, c)`-smooth over `B` (`:5334`); the skeleton had no
   fiber hypothesis at all.  Negation `thm_explicit_head_floor_even_false`:
   `F = ZMod 17`, `φ = X²`, `c = 2`, `N = 4`, `dom = (1,4,6,7,2,8,5,3)` — the
   squares `(1,16,2,15,4,13,8,9)` are pairwise distinct (all fibers
   singletons: not 2-smooth) yet antipodally symmetric and nonzero, so every
   stated hypothesis holds at `m = 2`, `K = 1`; the word `φ²|_D` takes each
   value twice, so every constant disagrees on ≥ 6 of 8 points
   (`relDist ≥ 3/4 > 1/2`) and even list size 1 fails (claimed: `C(2,1) = 2`).
   Repaired with `hsmooth : DomSmooth dom (φ.eval ·) c`.
   `thm_explicit_head_floor_odd` has the identical omission; no separate
   counterexample constructed (odd needs `m = 3`, `N ≥ 6`), so it gets the
   same repair with a same-class **PLAUSIBLE** flag and **no falsity claim**.
5. **`thm_explicit_pairs` (pre-repair): family size unconstrained.**  The
   paper fixes `L₀ := ⌈(q−n)/k⌉` (`:5370`); the skeleton left `L₀` free.
   Negation `thm_explicit_pairs_false`: `F = ZMod 7`, `ι = Fin 2`,
   `dom = (0,1)`, `K = 1`, `A = 2`, `L₀ = 1`, `u = P₀ = X`: every pole's value
   set has size `1 < ⌈5/3⌉ = 2`, so the good-pole set is empty while
   `|Ω| = 5`.  Repaired with `hL₀ : ⌈(q−n)/K⌉ ≤ L₀` (the Markov +
   Cauchy–Schwarz bound survives enlarging `L₀`; at `q − n ≤ 2K` the target
   ceiling is ≤ 1 and any nonempty family reaches it).

## PLAUSIBLE-graded repairs (no falsity claims)

* **`cor_ecfft_macroscopic`**: (i) `Δ` was unbounded, so the band admitted
  `δ < 0` where `emcaErr = 0` — a genuine defect, but a machine-checked
  negation needs a satisfiable `(2,1)`-smooth instance of `hyp`
  (disproportionate here); repaired with `hΔhi : Δ ≤ 1/512` (= the paper's
  `2⁻⁹` band, `:5251`).  (ii) `hfB`/`hgB` (present in `prop_rational_floor`
  and `cor_ecfft_onestep`) were missing — the `lem_phi_fiber_ii` untied-binder
  class; restored.  **Residual, documented:** the skeleton's `hyp` is the
  *one-step* binomial, while the paper's macroscopic proof needs the graded
  count at `m = ⌈(k+1+2⁻⁹n)/2⌉` derived from envelope hypotheses
  (`:5241`–`:5245`) that the skeleton never carried; a discharger will likely
  need to swap `hyp` for the graded form.  The repaired statement is *not*
  claimed provable-as-stated.
* **`AperiodicHankel` eliminant/packing**: `u, v : ℕ → F` were free sequences
  never tied to `(f, g)` although the docstrings promised `u = Syn(f)`,
  `v = Syn(g)` and no `Syn` existed in the file.  Repaired by defining the
  paper's twist/syndromes (`synTwist`, `rsSyndrome`, `:1550`–`:1560`) and
  substituting.  A refutation of the untied form (a Hankel-singular line with
  enough bad slopes for an unrelated regular pair) is scriptable but
  disproportionate — **no falsity claim**.

## Scope boundaries

* **`cor_first_grid_cap` for `c > 1` is NOT proved.**  Only the new
  `cor_first_grid_cap_one` (the `c = 1` clause, exactly what the paper's
  deployed-row chain consumes at `:1153`) is proved.  The `c > 1` clause needs
  the multiplicative-coset quotient floor (`cor:augmented-slack-one` at
  `c > 1`), which is not formalized; the general statement stays sorried with
  its docstring pointing at the discharged clause.
* The proved first-grid chain covers `cor:quantitative-first-grid-floor`'s
  `ε_ca` clause exactly as the skeleton stated it (the paper's separate
  `ε_mca` display there is covered at the cap radius through
  `cor_first_grid_cap_one`'s `ε_mca` clause via `eca_le_emca`; the skeleton
  never stated an `ε_mca` clause for the floor itself and none is added).
* `cor:first-grid-grand` (`:1129`, the four deployed-rate rows with numeric
  `k ≥ 127/78/58/47` checks) is **not** formalized; no numeric-row claim is
  made.
* The repaired `lem_quotient_remainder_prefix` /
  `lem_heaviest_prefix_locator_floor` remain **sorried skeletons**: the
  quotient-remainder locator-prefix construction itself is future work; this
  packet only made the targets true-as-stated.
* The repaired `prop_graded_rational_floor` formalizes the paper's
  *conversion* (list → floor on the deep band); the graded `U_z` pigeonhole
  that produces the list (the constructive content of `:5223`–`:5239`) is
  **not** formalized — it enters through the `hlist` hypothesis, exactly as
  the skeleton's abstraction chose.
* Remaining sorries after this packet (12 package-wide, by build warning):
  `Fiber.lean` `lem_fiber_ii` (pre-existing, out of scope);
  `QuotientRemainder.lean` `lem_quotient_remainder_prefix`,
  `lem_heaviest_prefix_locator_floor`, `cor_first_grid_cap`;
  `ECFFT.lean` `prop_rational_floor`, `cor_ecfft_onestep`,
  `cor_ecfft_macroscopic`; `InterleavingTransfer.lean`
  `thm_explicit_head_floor_even`, `thm_explicit_head_floor_odd`,
  `thm_explicit_pairs`; `AperiodicHankel.lean`
  `lem_regular_exact_agreement_eliminant`,
  `thm_regular_closed_ball_hankel_packing`.

## Verification

Pinned toolchain `leanprover/lean4:v4.28.0`, mathlib per the package's own
`lake-manifest.json`.  From `experimental/lean/cs25_cap_v12/`:

```text
lake build
```

* Baseline (pre-edit) build at base `3404d21`: exit 0, package-wide sorry
  census **14** (`declaration uses 'sorry'` warnings): Fiber 1,
  QuotientRemainder 4, InterleavingTransfer 3, AperiodicHankel 2, ECFFT 4.
* Post-packet clean rebuild (package build artifacts removed, all 16 modules
  recompiled): exit 0, census **12** — the two discharges are
  `cor_quantitative_first_grid_floor` and `prop_graded_rational_floor`; the
  five falsity lemmas, `hasList_first_grid`, `cor_first_grid_cap_one`,
  `RSpoly_one_const`, `hasList_const_le_card` all compile sorry-free.
* `#print axioms` on all 14 new/repaired proved declarations
  (`RSpoly_one_const`, `hasList_const_le_card`,
  `lem_quotient_remainder_prefix_false`,
  `lem_heaviest_prefix_locator_floor_false`, `hasList_first_grid`,
  `cor_quantitative_first_grid_floor`, `cor_first_grid_cap_one`,
  `prop_graded_rational_floor`, `prop_graded_rational_floor_false`,
  `thm_explicit_head_floor_even_false`, `thm_explicit_pairs_false`,
  `synTwist`, `rsSyndrome`, `certWeight`): exactly
  `[propext, Classical.choice, Quot.sound]` — no `sorryAx`, no
  `native_decide`, no added axioms.  All finite checks are kernel `decide`
  (the `DomSmooth` instances go through `Finset.filter_congr_decidable` to
  reach a computable `Decidable` instance).
* Tex citations verified against the base blob
  `origin/main:tex/cs25_cap_v12.tex` (line numbers as listed above).
