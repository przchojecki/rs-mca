# Circle-Fiber Correspondence (`CircleCode.lean`, b=0 complete-fiber packet)

Status: **PROVED** for the twin-coset / torus-fiber / Chebyshev-fiber statements
listed below (zero `sorry` in every declaration named in the statement map;
no axioms beyond Lean's standard `propext`, `Classical.choice`, `Quot.sound`
in any of them).  **Update (statement-repair packet, 2026-07-16):**
`RSCap.lem_circle_rs` and `RSCap.lem_stereographic` are now **statement-repaired
and PROVED** (their pre-repair skeleton statements were false as stated; the
machine-checked negations are `RSCap.lem_circle_rs_false` /
`RSCap.lem_stereographic_false` — see the falsity-findings section below).
**Update (Fiber.lean discharge packet, 2026-07-17):** `RSCap.cor_circle_grand`
is now **statement-repaired and PROVED** — `CircleCode.lean` has **zero proof
`sorry`**.  The blocking Fiber.lean route was discharged: `RSCap.lem_phi_fiber_ii`
(statement-repaired: the untied `φ` was **false as stated**, hand-verified
`F₁₆/F₄` counterexample documented in its docstring; repaired with the
value-level tie `hQB` and proved in full) and `RSCap.thm_phi_cap`
(same `hQB` repair, graded PLAUSIBLE there; proved).  `cor_circle_grand` also
received a second statement repair here (`hδlo` cast semantics, see the
falsity-findings section).  `RSCap.lem_fiber_ii` stays honestly sorried (out of
scope: `a ∣ k` never holds for circle rows).  The original b=0 packet formalized
the **smoothness input only** (the content of the pay-per-bit blocker `H5`); no
packet, including this one, claims the M31 circle rows
`cor:circle-deployed(a)/(b)` unblocked (see scope boundaries).

Source (both papers, at repo base `c35a6da31ed0905afcbaaefe4eb0f242572ebb35`):

* `tex/cs25_cap_v12.tex` — twin-coset preamble (`:3908`: size `2M`,
  inversion-closed, no self-inverse element, `χ` exactly two-to-one, `|D| = M`),
  `lem:torus-fibers` (`:3910`), `lem:cheb-fibers` (`:3923`, proof `:3935`–`:3951`
  via the `2a`-point solution set `E_w`), `rem:standard-position` (`:3953`).
* `experimental/rs_mca_thresholds.tex` (submission draft) —
  `def:circle-twin-domain` (`:2791`, cardinality claim `:2809`–`:2813`),
  `lem:cheb-smooth` (`:2873`, compressed proof `:2878`), used by
  `thm:fixed-length-prime-density`(c) (`:3009`) and `cor:circle-32-family`
  (`:3047`) (part (b) instead consumes the `lem:circle-uniformization` lane).  The draft's hypotheses (`a ∣ |H|`, `g^{2a} ∉ H^{(a)}`, all scales
  iff `ord(g) ∤ 2|H|`) are identical to v12's, so one formalization serves both.

## Statement map

| Paper statement | Lean declaration |
| --- | --- |
| Twin coset `𝒟 = gH ∪ g⁻¹H` (v12 `:3908`; draft `def:circle-twin-domain`) | `RSCap.twinCoset`, `RSCap.mem_twinCoset`, `RSCap.twinCoset_inv` |
| `𝒟` is inversion-closed with disjoint constituent cosets (`g² ∉ H`) | `RSCap.inv_mem_twinCoset`, `RSCap.twin_coset_sides_disjoint` |
| `𝒟` contains no self-inverse element (v12 `:3908`; the `b = 0` endpoint fact) | `RSCap.twinCoset_no_self_inverse` |
| `χ(u) = χ(v) ⟺ v ∈ {u, u⁻¹}` (v12 `:3898`; asserted in draft `:2878`) | `RSCap.chi_eq_chi_iff`, `RSCap.chi_val_eq_chi_val_iff`, `RSCap.chi_inv` |
| `χ` halves inversion-closed self-inverse-free sets (`\|χ(S)\| = \|S\|/2`) | `RSCap.chi_pair_image_card` |
| `\|χ(𝒟)\| = \|H\|` (v12 `:3908`; **unproved in draft** `def:circle-twin-domain` `:2809`–`:2813`) | `RSCap.twin_coset_chi_card` |
| Chebyshev semiconjugacy `T_a(χ(u)) = χ(uᵃ)` (v12 `:3900`; draft `:2816`–`:2821`) | `RSCap.chebyshev_semiconjugacy` (former `sorry`, now proved) |
| `lem:torus-fibers`, kernel step (`a`-power kernel has card `a`, lies in `H`) | `RSCap.card_pow_eq_one_of_dvd_card`, `RSCap.mem_of_pow_card_eq_one`, `RSCap.mem_of_pow_eq_one_of_dvd` |
| `lem:torus-fibers`(a), `a`-to-one on each coset | `RSCap.coset_pow_fiber_card` |
| `lem:torus-fibers`(a), disjoint branch (`g^{2a} ∉ H^{(a)}` ⟹ cross fibers empty, `𝒟` is `(Xᵃ, a)`-smooth) | `RSCap.coset_pow_fiber_cross_empty`, `RSCap.twin_coset_pow_fiber_card`, `RSCap.lem_torus_fibers` (`DomSmooth` form = `cor_circle_grand`'s `hsmooth` input) |
| `lem:torus-fibers`(b), coincident branch (`g^{2a} ∈ H^{(a)}` ⟹ image cosets coincide) | `RSCap.twin_coset_image_coincident` (coset level only; see scope boundaries) |
| `lem:torus-fibers`, all-scales criterion (`∀ a ∣ M, g^{2a} ∉ H^{(a)} ⟺ ord(g) ∤ 2M`) | `RSCap.twin_coset_all_scales_iff` |
| `lem:cheb-fibers` proof object `E_w` has exactly `2a` elements (v12 `:3935`–`:3951`) | `RSCap.twin_coset_pow_pair_card`, `RSCap.htwin_of_twin_coset` |
| `lem:cheb-fibers` / draft `lem:cheb-smooth`: `D = χ(𝒟)` is `(T_a, a)`-smooth | `RSCap.lem_cheb_fibers` (restated and proved; see statement repair below) |
| `rem:standard-position` (v12 `:3953`) = draft `thm:fixed-length-prime-density`(c) instantiation `H = ⟨g⁴⟩`, `ord(g) = 4n` | `RSCap.standard_position_twin_coset` |
| `lem:circle-rs` (v12 `:3976`, proof `:3988`–`:4008`) — torus uniformization `𝒞_w = t ∘ RS[F, E', 2w+1]` | `RSCap.lem_circle_rs` (**repaired**: `(2 : F) ≠ 0` added; **proved**) |
| Antisymmetric semiconjugacy `u^a − u^{−a} = (u − u⁻¹)U_{a−1}(χ(u))` (inside v12 proof of `lem:circle-rs`, Laurent symmetrization) | `RSCap.chebyshev_antisymm` (proved) |
| `lem:stereographic` (v12 `:5276`, proof `:5289`–`:5303`) — stereographic uniformization `𝒞_w = d ∘ RS[F, T, 2w+1]`, `d = ((1+s²)^{−w})` | `RSCap.lem_stereographic` (**repaired**: `sdom`/`twist` tied to `pt`; **proved**) |
| Negations of the two pre-repair skeleton statements | `RSCap.lem_circle_rs_false`, `RSCap.lem_stereographic_false` (proved) |
| Index bookkeeping for the two uniformizations | `RSCap.sum_range_center`, `RSCap.sum_range_parity` (proved) |
| `cor:circle-grand` (v12 `:4015`) | `RSCap.cor_circle_grand` (**repaired twice** — `htorusB` tie, `hδlo` ℕ-cast — and **PROVED**, 2026-07-17 packet) |
| `lem:phi-fiber`(ii) (v12 `:3750`, proof `:3771`–`:3799`) — consumed at `φ = Xᵃ` | `RSCap.lem_phi_fiber_ii` (Fiber.lean; **repaired** — `hQB` tie, pre-repair statement false — and **PROVED**) |
| `thm:phi-cap` (v12 `:3809`), `ε_ca` clause | `RSCap.thm_phi_cap` (Fiber.lean; **repaired** — `hQB` — and **PROVED**) |
| `HasList` → `hfiber` translation (implicit in the printed proofs) | `RSCap.hasList_fiber_input` (Fiber.lean; proved, reusable) |

## Statement repair (previous skeleton was vacuous)

The previous `lem_cheb_fibers` skeleton assumed, on one index type `ι`, both

* `hdom : Function.Injective dom` with `dom i = χ(torus i)` (so `ι` enumerates
  the `x`-domain and `torus` is a `χ`-section meeting each inverse pair once), and
* `htwin : ∀ i, #{j | torus jᵃ ∈ {torus iᵃ, torus i⁻ᵃ}} = 2a`.

These are jointly unsatisfiable for nonempty `ι`: a `χ`-section meets each
inversion pair of the solution set at most once, so the index-level count is
at most `a + 1 < 2a` for `a ≥ 2`, and exactly `1 < 2` at `a = 1` (`2a` is the
count on the **torus**, v12 `:3935`–`:3951`, not on the `x`-domain index set).
The skeleton statement was therefore provable only vacuously.  The restated `lem_cheb_fibers` takes the paper's actual
hypotheses (twin coset, `a ∣ |H|`, `g² ∉ H`, `g^{2a} ∉ H^{(a)}`, `(2 : F) ≠ 0`,
a `χ`-section covering `χ(𝒟)`), and the former `htwin` is now the **proved**
`RSCap.htwin_of_twin_coset` (phrased on an enumeration of the full twin coset,
where `2a` is correct).  `chebyshev_semiconjugacy` also gained the explicit
hypothesis `(2 : F) ≠ 0`: the unconditioned statement is false in characteristic
two (already at `a = 0`), and both papers have `p` odd throughout.

## Falsity findings and statement repairs (2026-07-16 packet)

Both remaining uniformization skeletons were **false as stated** — with
machine-checked negation lemmas at the Lean-statement level (universe-0
instantiation, which suffices to refute the universe-polymorphic skeletons).
Both defects are **formalization omissions, not paper defects**.

1. **`lem_circle_rs` (pre-repair): missing `(2 : F) ≠ 0`.**  The paper carries
   `p ≡ 3 (mod 4)` globally (`tex/cs25_cap_v12.tex` `sec:circle-geometry`
   preamble `:3888` and `lem:circle-rs` `:3976`), but the skeleton imposed no
   characteristic constraint.  Counterexample (`RSCap.lem_circle_rs_false`):
   `F = ZMod 2`, `ι = Fin 2`, `pt = ![(0,1), (1,0)]`, `i_unit = 1` (indeed
   `1² = −1` in `ZMod 2`), `torus ≡ 1`, `w = 1`.  The circle code contains the
   non-constant word `![0, 1]` (via `f₀ = X`, `f₁ = 0`), while `torus ≡ 1`
   collapses the twisted RS side to the constant words.
   **Repair:** add `h2 : (2 : F) ≠ 0` (`htne` is derivable from
   `hcircle`/`htorus`/`hi` via `u·(x − iy) = x² + y² = 1`, but retained).
   The repaired lemma is **proved in full**: forward by clearing denominators
   into an explicit `Q` of degree `≤ 2w` (`x^k ↦ 2^{−k}u^{w−k}(u²+1)^k`,
   `y·x^k ↦ (2i)⁻¹2^{−k}(u²−1)u^{w−1−k}(u²+1)^k`), reverse by Laurent
   symmetrization of `u^{−w}Q(u)` — symmetric part on the already-proved
   `chebyshev_semiconjugacy`, antisymmetric part on the one new helper
   `chebyshev_antisymm` (`Nat.twoStepInduction`, Mathlib `Chebyshev.U` API).
2. **`lem_stereographic` (pre-repair): `sdom`/`twist` untied.**  The binders
   `sdom, twist : ι → F` had no hypothesis relating them to `pt`
   (`hchar`/`hcircle` constrain only `F`/`pt`).  Counterexample
   (`RSCap.lem_stereographic_false`): `F = ZMod 5`, `ι = Fin 2`,
   `pt = const (1,0)`, `w = 0`, `sdom ≡ 0`, `twist = ![1, 2]` — the left side is
   the constant words, but membership of the constant word `1` on the right
   would force `κ = 1` and `2κ = 1` simultaneously in `ZMod 5`.
   **Repair** (paper anchor `lem:stereographic` `:5276`, twist
   `d := ((1+s(P)²)^{−w})_{P∈E}`): tie `sdom` to the stereographic coordinate via
   the inverse parametrization `x = (1−s²)/(1+s²)`, `y = 2s/(1+s²)` with pole
   exclusion `1 + s² ≠ 0`, and fix the twist to `(1 + s²)^{−w}`; `hcircle`
   becomes derivable and is dropped.  The repaired lemma is **proved in full**
   by the paper's even/odd substitution (`x^j ↦ (1−s²)ʲ(1+s²)^{w−j}`,
   `y·x^j ↦ 2s(1−s²)ʲ(1+s²)^{w−1−j}`; reverse direction by parity-splitting the
   coefficients of `Q`) — no Chebyshev machinery needed.
3. **`cor_circle_grand`: statement-hygiene repair, graded PLAUSIBLE** (no
   counterexample constructed, so **no falsity claim**).  The skeleton took
   `B : Subfield F` and used `Fintype.card B` in `hyp` with no hypothesis tying
   `torus` to `B`; its model `thm_phi_cap` (Fiber.lean) requires a `B`-valued
   domain (`hdomB`), and shrinking `B` weakens `hyp` while the fiber pigeonhole
   needs `B`-valued slopes — so the untied statement is likely unprovable.
   **Repair:** add `htorusB : ∀ i, torus i ∈ B`.  *(2026-07-17 update: the proof
   no longer stays `sorry` — see items 4–5 and the discharge packet above.)*
4. **`lem_phi_fiber_ii` (Fiber.lean, pre-repair): untied `φ`, FALSE AS STATED**
   (hand-verified counterexample, **not machine-checked** — no Lean negation
   lemma, see below).  The skeleton bound `φ : Polynomial F` with nothing tying
   `φ` (or its values on the domain) to `B`; the paper requires `φ ∈ B[X]`
   (`def:map-smooth`, v12 `:3744`), which is what puts `Q = φ(D)` and the slopes
   `z_A = −e₁(A)` inside `B`.  Counterexample: `F = F₁₆`, `B = F₄`,
   `t ∈ F₁₆ ∖ F₄`, `φ = X + t`, `a = 1`, `dom` an enumeration of `F₄`, `k = 1`,
   `N = 4`, `ℓ₂ = 3` — every slope `z ∈ F₄` fails (the received word minus any
   affine codeword is a monic cubic with `X²`-coefficient `t + z ∉ F₄`, but a
   monic cubic vanishing on `3` points of `F₄` has its `X²`-coefficient in `F₄`).
   A machine-checked negation would need a concrete `GF(16)/GF(4)` instance
   (`decide`-infeasible at reasonable cost; the `F₄/F₂` shrink is impossible
   since `a = 1` forces `n ≤ |B|`), so the finding is documented, not formalized
   — **no sorried falsity claim**.  **Repair:** `hQB : ∀ i, φ.eval (dom i) ∈ B`
   (value-level, minimal sufficient; the paper's coefficient-level `φ ∈ B[X]`
   implies it given `hdomB`).  Same repair applied to `thm_phi_cap`, graded
   **PLAUSIBLE** there (its conclusion does not mention `z ∈ B`; no
   counterexample constructed).  Both are now **proved** with the repair.
5. **`cor_circle_grand` (pre-repair, second defect): `hδlo` cast semantics,
   graded PLAUSIBLE claim-widening** (no falsity claim).  The skeleton's
   `hδlo : 1 - (a * (k / a + 2) : ℝ) / n ≤ δ` elaborated `k / a` as **real**
   division (endpoint `1 − (k+2a)/n`), while `hyp` uses `Nat.choose N (k/a + 2)`
   with **floor** division — two different `ℓ₂` semantics in one statement.
   Here `a ∤ k` always (`k = 2w+1` odd, deployed `a` even, v12 `:4010`), so
   `A₂ = a(⌊k/a⌋ + 2) ≤ k + 2a − 1 < k + 2a` and the real-division band starts
   strictly below the paper's certified endpoint `1 − A₂/n_c`
   (v12 `cor:circle-grand`(b) `:4015`); the fiber list does not reach those
   radii and `emcaErr` is monotone in `δ`, so the widened claim is not provable
   by the paper route.  **Repair:** `ℕ`-cast the endpoint,
   `hδlo : 1 - ((a * (k / a + 2) : ℕ) : ℝ) / n ≤ δ`, matching `thm_phi_cap`'s
   (correct) `A₂ : ℕ` pattern.  With both repairs the corollary is **proved**.

## Scope boundaries

* `cor_circle_grand` is now proved for the **uniformized RS code** on an
  abstract `B`-valued smooth domain, exactly as stated: the corollary's `hyp`,
  `hsmooth`, and `htorusB` remain *hypotheses*.  The Lean statement models the
  paper's `ε_mca` clause on the uniformized side only; the transport back to
  the bivariate circle code `𝒞_w` through `lem_circle_rs`/`lem_diag-invariance`
  and the paper's `ε_ca` band/`δ*` clauses of `cor:circle-grand` are not
  restated as separate Lean theorems.
* `lem_fiber_ii` (Fiber.lean) stays honestly sorried: it is not on
  `cor_circle_grand`'s route (`a ∤ k` always for circle rows) and is not a
  literal instance of the proved `lem_phi_fiber_ii` (its `ℓ₂ ≤ N` endpoint
  admits the `ℓ₂ = N` edge that the divisibility-free statement excludes).
* **No M31 unblocking claim.** The pay-per-bit ledger
  (`experimental/notes/audits/pay_per_bit_86bit_conditional_rows.md`) marks
  `cor:circle-deployed(a)/(b)` **blocked** on `H5` (map-smooth vs multiplicative
  coset).  The b=0 packet machine-checked the smoothness content behind `H5`,
  the 2026-07-16 packet added the proved uniformizations, and this packet proves
  the generic `cor_circle_grand`; but the deployed rows additionally need the
  numeric instantiation (the entropy verification of `(eq:hyp-phi)` at M31
  parameters, the concrete standard-position twin coset, and the circle-side
  transport), none of which is formalized.  No claim is made about the M31 rows
  beyond what `cor_circle_grand`'s statement itself gives.
* `lem:torus-fibers`(b)'s `(Xᵃ, 2a)` fiber **count** in the coincident case is
  not formalized (only the coset-coincidence dichotomy); `lem:cheb-fibers`'s
  image-domain statement `T_a(D) = χ(𝒟^{(a)})` and the dyadic tower packaging
  are not formalized as standalone declarations.
* The norm-one torus `𝕌 = ker(N_{F_{p²}/F_p})` is not constructed; twin cosets
  live in `Fˣ` for an abstract finite field `F`, with cyclicity of finite-field
  unit groups the only global input — matching v12's "over any field containing
  `F_{p²}`" phrasing.  No statement about primes, densities, or specific
  deployed parameters (e.g. M31) is made in Lean.

## Verification

Pinned toolchain `leanprover/lean4:v4.28.0`, mathlib tag `v4.28.0` (this
package's own pin).  From `experimental/lean/cs25_cap_v12/`:

```text
lake build
```

builds the package with `sorry` warnings only in the intended skeletons
(after the 2026-07-17 Fiber-discharge packet, `CircleCode.lean`: **none**;
`Fiber.lean`: `lem_fiber_ii` only; plus the pre-existing skeleton files
`QuotientRemainder`, `InterleavingTransfer`, `AperiodicHankel`, `ECFFT`).
`#print axioms` on every declaration in the statement map (b=0 packet: 25
declarations, 28 including the auxiliary lemmas `pow_card_subgroup_eq_one`,
`twin_coset_pow_eq_card_left`, `twin_coset_pow_eq_card_right`; statement-repair
packet: `lem_circle_rs`, `lem_stereographic`, `chebyshev_antisymm`,
`lem_circle_rs_false`, `lem_stereographic_false`, `sum_range_center`,
`sum_range_parity`; Fiber-discharge packet: `lem_phi_fiber_ii`, `thm_phi_cap`,
`hasList_fiber_input`, `cor_circle_grand`) reports no axioms beyond
`[propext, Classical.choice, Quot.sound]` (several use a proper subset) —
no `sorryAx`, no `native_decide`, no added axioms.  Package `sorry` census by
`declaration uses 'sorry'` build warnings: b=0 packet `CircleCode` 5 → 3
(package-wide 21 → 19); statement-repair packet `CircleCode` 3 → 1
(package-wide 19 → 17); Fiber-discharge packet `CircleCode` 1 → **0** and
`Fiber` 3 → 1 (package-wide 17 → **14**), the `Fiber` survivor being
`lem_fiber_ii` (out of scope, documented in its docstring).  Raw `grep -c sorry`
after the discharge packet: `CircleCode.lean` 2, both doc-text mentions, zero
proof sorries; `Fiber.lean` 3, of which exactly 1 is the `lem_fiber_ii` proof.
