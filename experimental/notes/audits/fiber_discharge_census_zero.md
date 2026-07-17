# Fiber.lean discharge → `cor_circle_grand` → CircleCode census zero

Packet type: repair-and-prove (#822 pattern, lane 19).  Target: the maintainer's
advertised open target — "attack the Fiber.lean skeleton first because it
supplies the list-mass input" (agents-log, 2026-07-16 entries).

Base: `a5750192a2fb4ff7e9f6b2f6bf77fa6652dffda7` (origin/main at packet time;
`Fiber.lean` had exactly one commit ever, `e1635f0`, and `CircleCode.lean` was
last touched by the integrated lane-17 repair packet).

Package: `experimental/lean/cs25_cap_v12` (pinned `leanprover/lean4:v4.28.0`,
mathlib per the package's own `lake-manifest.json`).

## What was done

1. **`RSCap.lem_phi_fiber_ii` (Fiber.lean) — statement-repaired and PROVED**
   (paper `lem:phi-fiber`(ii), tex `:3750`, proof `:3771`–`:3799`).
2. **`RSCap.thm_phi_cap` (Fiber.lean) — statement-repaired and PROVED**
   (paper `thm:phi-cap`, tex `:3809`, `ε_ca` clause).
3. **`RSCap.hasList_fiber_input` (Fiber.lean, new) — PROVED**, the reusable
   `HasList` → `hfiber` translation consumed by both cap theorems.
4. **`RSCap.cor_circle_grand` (CircleCode.lean) — statement-repaired (second
   defect) and PROVED** (paper `cor:circle-grand`, tex `:4015`).  This is the
   census 1 → 0 for `CircleCode.lean`.
5. **`RSCap.lem_fiber_ii` (Fiber.lean) — stays honestly sorried** (out of
   scope; see NON-CLAIMS).
6. Documentation: `CIRCLE_FIBER_CORRESPONDENCE.md` updated (statement map,
   falsity findings 4–5, scope boundaries, census); agents-log entry added.

No `.tex` file was touched.  No files outside
`experimental/lean/cs25_cap_v12/` and this note / the agents-log were touched.

## Statement repairs

### R1 — `lem_phi_fiber_ii`: untied `φ`, FALSE AS STATED (hand-verified)

The skeleton bound `φ : Polynomial F` with **no hypothesis tying `φ` (or its
values on the domain) to `B`**, while the paper's `def:map-smooth` (tex `:3744`)
reads "let `φ ∈ B[X]` have degree `a`".  The `B`-membership of the slopes
`z_A = −e₁(A)`, `A ⊆ Q = φ(D)`, is exactly what makes the pigeonhole run over
`|B|` rather than `|F|`; `hdomB` alone does not give `Q ⊆ B`.

**Counterexample (hand-verified arithmetic; not machine-checked):**
`F = F₁₆`, `B = F₄` (subfield), `t ∈ F₁₆ ∖ F₄`, `φ = X + t`, `a = 1`,
`ι = Fin 4`, `dom` an injective enumeration of `F₄` (fibers of size `1`, so
`DomSmooth` holds trivially), `k = 1`, `N = 4`, `ℓ₂ = ⌊1/1⌋ + 2 = 3 ≤ N − 1`,
`A₂ = 3`.  The conclusion demands `z ∈ F₄` and `L ≥ C(4,3)/4 = 1`, i.e. one
degree-`≤ 1` codeword agreeing with
`u_z(x) = (x+t)³ + z(x+t)²` on `≥ 3` of the `4` points of `F₄`.  In
characteristic 2, `u_z` as a polynomial in `x` is
`x³ + (t+z)x² + t²x + (t³ + zt²)`; subtracting any affine `c` leaves a **monic
cubic with `x²`-coefficient `t + z ∉ F₄`** (as `z ∈ F₄`, `t ∉ F₄`), while a
monic cubic vanishing at three distinct points `r₁, r₂, r₃ ∈ F₄` factors as
`(x−r₁)(x−r₂)(x−r₃)` with `x²`-coefficient `r₁+r₂+r₃ ∈ F₄`.  Contradiction for
every `z ∈ B`; four agreements are impossible (degree 3 ≠ affine on 4 points).
So the stated existential fails.

**Why no Lean negation lemma:** a machine-checked witness needs a concrete
`GF(16)/GF(4)` instance with a `Fintype` subfield and an element outside it;
`decide`-style closure over `GaloisField 2 4` is infeasible at reasonable cost,
and the `F₄/F₂` shrink is impossible: with `a = 1` a `B`-valued injective
domain forces `n ≤ |B| = 2`, while `ℓ₂ ≥ 2` together with `ℓ₂ ≤ N − 1` needs
`n = a·N = N ≥ 3`.
Per the packet's honesty discipline — **never a sorried falsity claim** — the
finding is documented in the docstring and here, and the statement repaired.

**Repair:** `hQB : ∀ i, φ.eval (dom i) ∈ B` — value-level, the minimal
hypothesis making the printed proof sound.  The paper-faithful
coefficient-level alternative (`∀ m, φ.coeff m ∈ B`) implies it given `hdomB`;
the value-level form is what `cor_circle_grand` can discharge from `htorusB`
by `Subfield` power-closure.  `hdomB` is retained (paper setting `D ⊆ B`)
although the proof of the list conclusion consumes only `hQB`; the
unused-variable warning is deliberate and documented in the docstring.

### R2 — `thm_phi_cap`: same untied `φ`, graded PLAUSIBLE

Its conclusion does not mention `z ∈ B`, so the counterexample above does not
directly refute it; but the only known route needs the fiber list of size
`≥ C(N,ℓ₂)/|B|`, and under `(eq:hyp-phi)` a pigeonhole over `F` cannot deliver
it.  No counterexample constructed, so **no falsity claim** — graded PLAUSIBLE.
Same `hQB` repair applied.

### R3 — `cor_circle_grand`: `hδlo` cast semantics, graded PLAUSIBLE
claim-widening

The skeleton's `hδlo : 1 - (a * (k / a + 2) : ℝ) / n ≤ δ` elaborated `k / a`
as **real** division (endpoint `1 − (k+2a)/n`), while its own `hyp` uses
`Nat.choose N (k / a + 2)` with **floor** division (`ℓ₂ = ⌊k/a⌋ + 2`,
`A₂ = a·ℓ₂`) — two different `ℓ₂` semantics in one statement (present since
the original skeleton `e1635f0`; survived the lane-17 `htorusB` repair).  For
circle rows `a ∤ k` always (`k = 2w+1` odd, deployed `a` even; tex `:4010`), so
`A₂ ≤ k + 2a − 1 < k + 2a` and the real-division band starts a sliver strictly
below the paper's certified endpoint `1 − A₂/n_c` (`cor:circle-grand`(b), tex
`:4015`).  The fiber list does not reach those radii, and `emcaErr` is
monotone increasing in `δ`, so the widened claim is not provable by the paper
route.  No falsity witness constructed — **no falsity claim**.
**Repair:** `ℕ`-cast the endpoint, `1 - ((a * (k / a + 2) : ℕ) : ℝ) / n ≤ δ`,
matching the correct `A₂ : ℕ` pattern already used by `thm_phi_cap`'s `hδlo`.

## Proof summary

All-Mathlib; no new axioms; no `native_decide`.

* `lem_phi_fiber_ii` (the packet's real work).  Locator
  `P_A = ∏_{b∈A}(Y − C b)`; Vieta via `Polynomial.prod_X_sub_C_nextCoeff` +
  `nextCoeff_of_natDegree_pos` gives the top two coefficients, so the tail
  `locTail A ℓ₂ := P_A − Y^{ℓ₂} − C(−∑A)·Y^{ℓ₂−1}` has `natDegree ≤ ℓ₂ − 2`
  (coefficient-wise via `natDegree_le_iff_coeff_eq_zero`).  Quotient-domain
  count `|φ(D)| = N` and the `A₂ = a·ℓ₂` agreement count both by
  `Finset.card_eq_sum_card_image` / `card_eq_sum_card_fiberwise` against
  `DomSmooth`.  Codeword degree: `natDegree_comp` + `a·⌊k/a⌋ ≤ k`
  (`Nat.div_mul_le_self`).  Injectivity at fixed slope (`locator_subset_eq`):
  agreement on all `n > k` injective domain points forces equal compositions
  (root-count via `card_roots'`), composition with the nonconstant `φ` is
  injective by the leading-coefficient argument (`leadingCoeff_comp`), and
  equal locators have equal root multisets (`roots_prod_X_sub_C`).  Pigeonhole:
  argmax slope over the image of `A ↦ −∑A` (`Finset.exists_max_image`,
  `card_eq_sum_card_image`, image card `≤ |B|`), fiber packaged into `HasList`
  via `Finset.equivFin`.  ~200 lines plus ~120 lines of private locator algebra.
* `thm_phi_cap`: derived side conditions (`hak` from `hδhi`, `1 ≤ L` from
  `(eq:hyp-phi)`), `hasList_fiber_input`, then the proved
  `universal_cap_of_fiber_list` (MainCap.lean).  The Lean statement models the
  paper's `ε_ca` clause only (as before the packet); the `ε_mca` band and
  `δ*_C` clause are not restated.
* `cor_circle_grand`: `lem_phi_fiber_ii` at `φ = Xᵃ`
  (`natDegree_X_pow`; `hQB` from `pow_mem htorusB`); `hℓ₂N` **derived** from
  `hyp` (the binomial must exceed `|B|(q/k+1) > 1`, and `Nat.choose N ℓ₂ ≥ 2`
  forces `ℓ₂ < N`); `n > 0`, `hak : k < (1−δ)n` (exactly `hδhi`), `1 ≤ L`
  derived; then `hasList_fiber_input` at the repaired `hδlo` and the proved
  `universal_cap_emca_of_fiber_list`.  `thm_phi_cap` is deliberately *not* on
  this route (its `hδhi` is stricter than the corollary's `δ < 1 − ρ` band;
  the emca reduction applies directly).

## Gates

* `lake build` from scratch in a fresh worktree: **exit 0** (8043 jobs),
  baseline before edits also exit 0 (toolchain-first).
* `#print axioms`: `lem_phi_fiber_ii`, `thm_phi_cap`, `hasList_fiber_input`,
  `cor_circle_grand` all report exactly
  `[propext, Classical.choice, Quot.sound]` — **no `sorryAx`** (in particular
  `cor_circle_grand` no longer reports it), no `native_decide`.
* Sorry census by `declaration uses 'sorry'` build warnings:
  * before: package-wide **17** — Fiber 3 (`lem_fiber_ii` L50,
    `lem_phi_fiber_ii` L70, `thm_phi_cap` L91), CircleCode 1
    (`cor_circle_grand` L1289), ECFFT 4, QuotientRemainder 4,
    InterleavingTransfer 3, AperiodicHankel 2.
  * after: package-wide **14** — Fiber 1 (`lem_fiber_ii` only), CircleCode
    **0**, other skeleton files unchanged.
* Source-only: no `.lake`, no `lake-manifest.json`, no toolchain churn.
* Tex citations in docstrings/notes verified against the base blob
  `origin/main:tex/cs25_cap_v12.tex`: `def:map-smooth` `:3744`,
  `lem:phi-fiber` `:3750` (proof `:3771`–`:3799`), `rem:no-divisibility`
  `:3801`, `thm:phi-cap` `:3809`, parity note `:4010`, `cor:circle-grand`
  `:4015`, `lem:fiber` `:664`.

## Self-Red-Team

* **Is `hQB` secretly stronger than the paper?**  No — the paper's
  `φ ∈ B[X]` plus `D ⊆ B` (`hdomB`) implies `φ.eval (dom i) ∈ B` pointwise, so
  the repaired lemma is *weaker-hypothesis-or-equal* relative to the paper's
  setting, and strictly weaker than requiring `φ ∈ B[X]` in Lean.  The
  `cor_circle_grand` discharge (`φ = Xᵃ` on a `B`-valued domain) uses only
  power-closure, matching the paper's instantiation.
* **Is the repaired `hδlo` narrower than the paper's band?**  The paper
  certifies `ε_mca > threshold` on `[1 − A₂/n_c, 1 − ρ_c)` with the *floor*
  `A₂` (`cor:circle-grand`(b)); the repaired Lean band is exactly that.  The
  pre-repair Lean band was strictly wider (started lower), i.e. the repair
  narrows the *claim* to the certified one — claim-widening fixed, no strength
  lost against the paper.
* **Does deriving `hℓ₂N` from `hyp` smuggle in a hypothesis?**  No — it
  *removes* the need for an explicit `ℓ₂ ≤ N − 1` binder in the corollary:
  when `hyp` holds the binomial is `≥ 2`, which forces `ℓ₂ < N`.  If `hyp`
  fails the corollary is vacuous anyway.  The paper's own proof of
  `cor:circle-grand` checks `ℓ₂ ≤ N − 1` from its rate window; the Lean
  statement never claimed that window, so nothing is lost.
* **Could `lem_phi_fiber_ii`'s `L` be zero?**  Yes in principle (tiny `|B|`
  bound `C(N,ℓ₂)/|B| ≤ L` permits `L = 0` when the binomial is small); both
  consumers derive `1 ≤ L` from `(eq:hyp-phi)` before use, and
  `universal_cap_*_of_fiber_list` requires `1 ≤ L` explicitly.  No vacuity in
  the consumers.
* **Unused `hdomB` in `lem_phi_fiber_ii`:** deliberate (paper-setting
  faithfulness; keeping it only weakens the statement).  Documented in the
  docstring; produces one benign linter warning.
* **Line-number drift:** `cor_circle_grand` now sits at a different line than
  L1289; the census above identifies declarations by name, not line.

## NON-CLAIMS

* **`lem_fiber_ii` is NOT proved** — it stays honestly sorried, out of scope:
  not on `cor_circle_grand`'s route (`a ∤ k` always for circle rows, tex
  `:4010`), and not a literal instance of the proved lemma (its `ℓ₂ ≤ N`
  endpoint admits the `ℓ₂ = N` edge case).  A later cheap corollary +
  edge-case treatment is possible but is not claimed here.
* **No M31-row claims beyond what `cor_circle_grand`'s statement gives.**  The
  deployed rows `cor:circle-deployed(a)/(b)` remain blocked in the pay-per-bit
  ledger: the numeric `(eq:hyp-phi)` verification at M31 parameters, the
  concrete standard-position twin coset, and the circle-side transport are not
  formalized.
* **No falsity lemma is formalized** for the pre-repair `lem_phi_fiber_ii`
  statement (hand-verified counterexample only, documented), and **no falsity
  claim at all** is made for the pre-repair `thm_phi_cap` or `cor_circle_grand`
  statements (both graded PLAUSIBLE).
* **No `.tex` edits**; the paper is untouched.
* The Lean `thm_phi_cap` still models only the paper's `ε_ca` clause (as
  before); the `ε_mca` and `δ*_C` clauses of `thm:phi-cap` are not restated.
