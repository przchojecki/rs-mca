# Circle-Fiber Correspondence (`CircleCode.lean`, b=0 complete-fiber packet)

Status: **PROVED** for the twin-coset / torus-fiber / Chebyshev-fiber statements
listed below (zero `sorry` in every declaration named in the statement map;
no axioms beyond Lean's standard `propext`, `Classical.choice`, `Quot.sound`
in any of them).  **NOT PROVED** (unchanged `sorry` skeletons): `RSCap.lem_circle_rs`,
`RSCap.cor_circle_grand`, `RSCap.lem_stereographic`.  This packet formalizes the
**smoothness input only** (the content of the pay-per-bit blocker `H5`); it does
**not** claim the M31 circle rows `cor:circle-deployed(a)/(b)` unblocked.

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

## Scope boundaries

* `lem_circle_rs`, `cor_circle_grand`, `lem_stereographic` remain `sorry`
  skeletons, unchanged in content (only `cor_circle_grand`'s docstring notes
  that its `hsmooth` input is now constructible via `lem_torus_fibers`).
* **No M31 unblocking claim.** The pay-per-bit ledger
  (`experimental/notes/audits/pay_per_bit_86bit_conditional_rows.md`) marks
  `cor:circle-deployed(a)/(b)` **blocked** on `H5` (map-smooth vs multiplicative
  coset).  This packet machine-checks the smoothness content behind `H5`
  (`(T_a, a)`-smoothness of twin-coset `x`-domains), but the rows' certifying
  route (`thm:phi-cap` / `cor:circle-grand` / `lem:circle-rs`) is not formalized
  here; the rows stay blocked.
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
(`CircleCode.lean`: `lem_circle_rs`, `cor_circle_grand`, `lem_stereographic`;
plus the pre-existing skeleton files).  `#print axioms` on every declaration in
the statement map (25 declarations; 28 including the auxiliary lemmas
`pow_card_subgroup_eq_one`, `twin_coset_pow_eq_card_left`,
`twin_coset_pow_eq_card_right`) reports no axioms beyond
`[propext, Classical.choice, Quot.sound]` (several use a proper subset) —
no `sorryAx`, no `native_decide`, no added axioms.  Package `sorry` census by
`declaration uses 'sorry'` build warnings: `CircleCode` 5 → 3, every other
module unchanged (package-wide 21 → 19).  Raw `grep -c sorry` on
`CircleCode.lean`: 6 → 5, of which 2 are doc-text mentions (`Proved here
(no `sorry`)` / `Still skeletons`), 3 are the listed proofs.
