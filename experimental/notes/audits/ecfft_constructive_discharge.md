# ECFFT constructive discharge: `prop_rational_floor` + `cor_ecfft_onestep` proved (statements byte-identical)

**Date:** 2026-07-19.
**Scope:** `experimental/lean/cs25_cap_v12/cs25_cap_v12/ECFFT.lean` only (plus this
note, the correspondence file, and the agents log).
**Base:** `999b8f3` (origin/main at lane start).
**Result:** the two remaining audited-no-defect ECFFT sorries are **discharged with
machine-checked proofs**; package sorry census **12 → 10**, ECFFT census **3 → 1**
(only the documented `cor_ecfft_macroscopic` residual remains).  No falsity was
found: both statements are true exactly as the audited skeleton stated them.

## Statement pins

| Item | tex anchor (at `999b8f3`, = `3404d21`) | Lean at `999b8f3` | Lean after packet |
| --- | --- | --- | --- |
| `def:rational-smooth` | `tex/cs25_cap_v12.tex:4833`–`:4835` | `ECFFT.lean:47` (`RationalSmooth`) | unchanged |
| `prop:rational-floor` | `:4837`–`:4849` (proof `:4851`–`:4861`) | `ECFFT.lean:57` (sorried) | `ECFFT.lean:226` (**PROVED**) |
| `cor:ecfft-onestep` | `:4863`–`:4875` (proof `:4877`–`:4883`) | `ECFFT.lean:78` (sorried) | `ECFFT.lean:519` (**PROVED**) |
| `cor:ecfft-macroscopic` | `:5241`–`:5262` | `ECFFT.lean:237` (sorried) | `ECFFT.lean:731` (sorried, untouched) |

Statement byte-identity (gate G5): the extracted statement blocks (`theorem` line
through `:= by`) of both theorems are byte-identical between `999b8f3` and this
packet (`diff` empty, 12 and 14 lines respectively).  Only the `sorry` bodies were
replaced; three helper lemmas were added above `prop_rational_floor`; the module
header and the two theorem docstrings were extended with **marked** update blocks.

## New helper lemmas (all proved; axioms exactly `[propext, Classical.choice, Quot.sound]`)

* `RSCap.eval_mem_of_coeff_mem` (`ECFFT.lean:70`) — a polynomial with all
  coefficients in a subfield `B`, evaluated at a point of `B`, lands in `B`
  (`eval_eq_sum_range` + `Subring.sum_mem`/`mul_mem`/`pow_mem`).  Discharges the
  coefficient-level subfield ties `hfB`/`hgB` into the value-level facts the
  pigeonhole needs (fiber values `ψ(x) = f(x)/g(x) ∈ B` via `Subfield.div_mem`,
  slopes `z = −e₁(A) ∈ B` via `sum_mem`/`neg_mem`).
* `RSCap.rational_locator_expansion` (`ECFFT.lean:84`) — for any `S : Finset F`,
  `∏_{c∈S}(f − c·g) = f^{|S|} − (∑ S)·f^{|S|−1}·g + r_S` with
  `natDegree r_S ≤ a(|S|−2) + 2e` (ℕ-truncated) **and** `r_S = 0` for `|S| ≤ 1`.
  This is the `j ≥ 2` tail of the paper's expansion
  `Λ_A = ∑_j (−1)^j e_j(A) f^{ℓ−j} g^j` (tex `:4852`–`:4856`).  Proof: induction on
  `S`; the strengthened `|S| ≤ 1 → r = 0` clause is load-bearing — in the insert
  step at `|S| = 1` the product `(f − c₀·g)·r` would otherwise only admit the bound
  `a + 2e`, exceeding the required `2e`; and the insert-into-`∅` step is handled
  separately (at `|S| = 0` the ℕ-exponent identity `f·f^{|S|−1} = f^{|S|}` fails,
  rescued only because `e₁(∅) = 0`) — both exactly as the adversarial plan check
  demanded.
* `RSCap.eq_of_eval_eq_of_natDegree_lt` (`ECFFT.lean:182`) — two polynomials of
  `natDegree < n` agreeing on an injective `n`-point domain are equal
  (root-counting on the difference).  Extraction of the inline
  distinct-interpolant argument of `hasList_first_grid` (QuotientRemainder.lean).

## The formalized proof (as machine-checked)

**`prop_rational_floor`** (paper proof tex `:4851`–`:4861`):

1. *Fibers.* `φ := x ↦ f(x)/g(x)`; `T := image (φ ∘ dom)` has `|T| = N` by the
   `DomSmooth` double count (`card_eq_sum_card_image`, each fiber `= a`,
   `n = a·|T| = a·N`, cancel `a > 0`).  Every value `φ(dom i) ∈ B`
   (`eval_mem_of_coeff_mem`, `div_mem`).
2. *Locator codewords.* For `S ⊆ T`, `|S| = ℓ`, the locator
   `Λ_S = ∏_{c∈S}(f − c·g)` vanishes at every `i` with `φ(dom i) ∈ S` (the factor
   at `c = φ(dom i)` is `f − (f/g)·g = 0`, `g(dom i) ≠ 0`), and conversely a root
   `dom i` of `Λ_S` has `φ(dom i) ∈ S` (`prod_eq_zero_iff` in a field).  With
   `z_S := −∑ S`, the expansion gives `u_{z_S} − Λ_S|_D = (−r_S)|_D` with
   `natDegree r_S ≤ a(ℓ−2) + 2e = k'` (the ℕ-subtraction identity
   `aℓ − 2(a−e) = a(ℓ−2) + 2e` holds under `ℓ ≥ 2`, `e < a`), so the word
   `u_{z_S}` agrees with the codeword `(u_{z_S} − Λ_S|_D) ∈ RS[F, D, k'+1]` on the
   `a·ℓ` fiber points: `relDist ≤ 1 − aℓ/n`.
3. *Fixed-slope injectivity.* At a fixed slope `z`, equal codewords force
   `Λ_S|_D = Λ_{S'}|_D`; since `natDegree Λ_S ≤ aℓ ≤ a(N−1) < n`,
   `eq_of_eval_eq_of_natDegree_lt` gives `Λ_S = Λ_{S'}`, and the root/recovery
   equivalence of step 2 gives `S = S'` (each `c ∈ S` has a witness fiber point).
   Note this route replaces the paper's transcendence argument (tex `:4860`) and
   **does not need coprimality of `f, g`** — consistent with the audited
   skeleton's omission of the paper's coprime hypothesis (deviation flag 1 of the
   tex scout; the omission is benign for this construction).
4. *Pigeonhole.* The `C(N, ℓ)` sets `S ∈ T.powersetCard ℓ` map to slopes
   `z_S ∈ B`; taking the maximal fiber of that map (`exists_max_image`,
   `card_eq_sum_card_image`, image bounded by the `|B|`-element carrier finset)
   gives a slope `z₀ ∈ B` with fiber size `L ≥ C(N, ℓ)/|B|`; enumerating the fiber
   (`Finset.equivFin`) yields the `HasList` witness.

**`cor_ecfft_onestep`** (paper proof tex `:4877`–`:4883`): instantiate at
`(a, e) = (2, 1)`, `ℓ = (k+2)/2` (`2ℓ = k+2` exactly, `k` even), `k' = 2ℓ − 2 = k`;
align `hyp`'s binomial (`n/2 = N`, `(k+2)/2 = ℓ`, omega); derive the trigger
`L ≥ C(N,ℓ)/|B| ≥ q/k + 1 > (q−n)/k` (`|B| > 0`, `n/k > 0`); feed the list at deep
agreement `A = 2ℓ = k + 2 ∈ (k, n]` to the **proved** bridge
`cor_quotient_remainder_trigger` (QuotientRemainder.lean:275 at base; Theorem A at
`η = 1/2` + `ecaFloor_trigger`) at `δ = 1 − k/n − 2/n = 1 − (k+2)/n`, exactly as
`cor_first_grid_cap_one` bridged the `c = 1` list at `A = k + 1`.  The radius glue
is the cast identity `((2ℓ : ℕ) : ℝ) = k + 2` and `1 − (k+2)/n = 1 − k/n − 2/n`;
`hAn : k + 2 ≤ n` comes from `ℓ ≤ N − 1`, `n = 2N`.

## Gates transcript summary

* **G1 (baseline):** pre-edit `lake build` from the copied v4.28 cache: fast
  no-op pass, `Build completed successfully (8043 jobs)`; baseline census
  12 sorry warnings (ECFFT at `57`, `78`, `237`).
* **G2 (from-scratch):** `rm -rf .lake/build && lake build` → exit 0,
  `Build completed successfully (8043 jobs)`.
* **G3 (axioms):** `#print axioms` on `prop_rational_floor`, `cor_ecfft_onestep`,
  `eval_mem_of_coeff_mem`, `rational_locator_expansion`,
  `eq_of_eval_eq_of_natDegree_lt` — each exactly
  `[propext, Classical.choice, Quot.sound]`.
* **G4 (census):** package 12 → 10 `declaration uses 'sorry'` warnings; ECFFT
  3 → 1 (`cor_ecfft_macroscopic` only).
* **G5 (byte-identity):** statement extraction diff empty for both theorems.
* **G6 (source-only):** the packet commit touches only `ECFFT.lean`, the
  correspondence file, this note, and `experimental/agents-log.md`.

## Self-Red-Team

* *Is the `HasList` radius exactly the statement's?* Yes — the closeness bound is
  proved in the literal form `1 − (a * ℓ : ℝ)/n` (complement of the `a·ℓ`-point
  fiber set, `Nat.cast_sub` guarded by `aℓ ≤ n` from `ℓ ≤ N − 1`), no rounding.
* *Does the pigeonhole really give the real-division bound?* `C(N,ℓ) ≤ |B|·L` in
  ℕ (max-fiber + image-in-carrier), then one `div_le_iff₀` with `|B| > 0`
  (`⟨0, zero_mem⟩`).  No `⌈·⌉` approximation is involved.
* *Degenerate parameters?* `ℓ ≥ 2` and `ℓ ≤ N − 1` force `N ≥ 3`, `n = aN > 0`;
  `k' < n` since `k' ≤ a(N−3) + 2(a−1) < aN`; the `RSpoly` membership uses
  `degree < k' + 1` via `natDegree ≤ k'`, sound also for the zero polynomial.
* *ℕ-subtraction traps?* All discharged by literal decompositions
  (`ℓ = t + 2`, `N = s + 3`, `m = t + 1`) with products linearized by `ring`
  before `omega`; no `omega` call sees an un-atomized variable product.
* *Instance mismatches (`DecidableEq`/filters)?* All filters/powersets are built
  under `classical` in files that all `open Classical`; `DomSmooth`'s filter and
  ours unify definitionally (verified by the successful `exact hsm i₀`).
* *Does `cor_ecfft_onestep` secretly need more than the skeleton's `hyp`?* No —
  the proof consumes exactly the stated hypotheses; the envelope (`ρ` range,
  `n ≥ 2^12`, `q < 2^256`) is *not* needed because `hyp` already carries the
  binomial count those would imply (conditional-weakening flag 2, unchanged).

## NON-CLAIMS

* **No numeric deployed-row instantiation** is made (no `k ≥ …` row checks, no
  claim about any production parameterization).
* **`cor_ecfft_macroscopic` is untouched** and stays sorried with its documented
  `hyp`-form residual (its `hyp` is the one-step count, not the paper's graded
  count at `m = ⌈(k+1+2⁻⁹n)/2⌉`; see its docstring and the correspondence file).
* **No paper `.tex` was edited**; all tex anchors cite `999b8f3` (= `3404d21` for
  this file).
* **No claim about the graded/macroscopic chain** (`prop:graded-rational-floor`'s
  constructive `U_z` pigeonhole remains unformalized behind its `hlist`
  hypothesis, as before).
* The paper's `ε_mca` band clause, list-challenge clause (`k < 2^128`), and
  odd-`k` variant of `cor:ecfft-onestep` (tex `:4872`–`:4874`) are **not stated**
  by the skeleton and hence **not proved** here (pre-existing deviation flags
  2–3; conclusion here is the `ε_ca` clause at the single first-step radius, as
  audited).
* Coprimality of `f, g` (paper `def:rational-smooth`) remains absent from the
  Lean statements (pre-existing deviation flag 1); this packet *demonstrates* the
  omission is benign for these two results (the proof never uses it), which is a
  strengthening, not a repair.
