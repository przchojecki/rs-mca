import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat
open scoped Classical
open scoped Pointwise

set_option maxHeartbeats 8000000
set_option maxRecDepth 4000

/-!
# A Pincer, Sparse, and Certificate Picture for the Mutual Correlated Agreement Threshold

This file is a Lean formalization of the definitions and main results of the note
*"A Pincer, Sparse, and Certificate Picture for the Mutual Correlated Agreement
Threshold"* (P. Chojecki, 2026), which studies mutual correlated agreement (MCA)
for Reed–Solomon codes in the parameter box singled out by the Proximity Prize.

## Modelling conventions

* Codewords are functions `ι → F` where `ι` is the (finite) evaluation domain of
  size `n = Fintype.card ι` and `F` is a finite field with `q = Fintype.card F`.
* A code is a Lean `Submodule F (ι → F)` (i.e. an `F`-linear subspace), matching
  "linear code" in the paper.
* All distances are integral, so instead of a real proximity parameter `δ` we use
  the integer radius `r = ⌊δ n⌋` throughout the combinatorial statements; the real
  parameter reappears only in the threshold `δ*` (`dstar`).

## Main results

* `epsCA_le_epsMCA` — Lemma 2.4 (chain): `ε_ca ≤ ε_mca`.
* `one_div_card_le_epsMCA` — Proposition 3.8 (small fields): `ε_mca ≥ 1/q` for a
  proper linear code.
* `dstar_eq_zero_of_small` — Theorem 1.1(1): the threshold is `0` when `q < 2¹²⁸`.
* `deep_epsMCA_le` — Theorem 4.9 (deep regime): `ε_mca ≤ (r+1)/q` below one third
  of the minimum distance.
* `half_epsMCA_le` — Theorem 4.11 (mutual from correlated below half the distance).
* `line_at_most_one_slope` — Lemma 5.1(3).
* `sparsify` — Theorem 5.3: `ε_mca = max(ε_ca, σ_C/q)`.
* `safe_half_distance` — Corollary 4.6 (safe to half the distance, given the
  BCIKS unique-decoding proximity gap as a hypothesis).
* `prefix_floor` — Lemma 3.1 (graded prefix floor), for the identity locator
  `c = 1`: an explicit pigeonhole word carrying a large Reed–Solomon list.

All of the above are proved from first principles (depending only on the standard
axioms `propext`, `Classical.choice`, `Quot.sound`).

`deep_point_conversion` (Theorem 3.2, the deep-point / rational-function
list-to-correlated-agreement conversion) is now also proved from first
principles. Its proof is the full list-decoding argument (the simple-pole
functions `poleF`/`poleG`, a fiber Cauchy–Schwarz inequality `cs_fiber`, the
polynomial root count `eval_eq_count_le`, the CA-badness of the simple-pole
slopes `poles_colFar`/`poles_closeBy`, an averaging step `exists_low_collision`,
and the closing arithmetic `final_algebra`), with the core fiber estimate
isolated as `deep_fiber_bound`. The cap criterion and the binomial-entropy
verification behind `Theorem 1.1(2)–(4)` are not formalized here.
-/

namespace TowardsPrize

variable {ι F : Type*} [Fintype ι] [DecidableEq ι] [Field F] [Fintype F] [DecidableEq F]

/-! ## Section 2. Definitions -/

/-- Hamming weight: the number of nonzero coordinates. -/
noncomputable def wt (c : ι → F) : ℕ := (Finset.univ.filter (fun j => c j ≠ 0)).card

/-- Hamming distance (unnormalised): the number of coordinates where `u` and `v`
differ. The paper's relative distance is this quantity divided by `n`. -/
noncomputable def hd (u v : ι → F) : ℕ := (Finset.univ.filter (fun j => u j ≠ v j)).card

/-- The line word `f₁ + γ f₂`. -/
def combo (f1 f2 : ι → F) (γ : F) : ι → F := fun j => f1 j + γ * f2 j

/-- Column disagreement of a pair `(f₁,f₂)` against `(c₁,c₂)`: the number of
coordinates `j` with `(f₁ j, f₂ j) ≠ (c₁ j, c₂ j)`. -/
noncomputable def cdist (f1 f2 c1 c2 : ι → F) : ℕ :=
  (Finset.univ.filter (fun j => f1 j ≠ c1 j ∨ f2 j ≠ c2 j)).card

/-- `u` is `r`-close to `C`: some codeword agrees with `u` off at most `r`
coordinates. -/
def closeBy (C : Submodule F (ι → F)) (r : ℕ) (u : ι → F) : Prop :=
  ∃ c ∈ C, hd u c ≤ r

/-- The pair `(f₁,f₂)` is `r`-far in columns from `C × C`. -/
def colFar (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) : Prop :=
  ∀ c1 ∈ C, ∀ c2 ∈ C, r < cdist f1 f2 c1 c2

/-- A slope `γ` is `r`-CA-bad for `(f₁,f₂)`: the line word is `r`-close to `C`
while the pair is `r`-far in columns. -/
def CAbad (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) (γ : F) : Prop :=
  closeBy C r (combo f1 f2 γ) ∧ colFar C r f1 f2

/-- A slope `γ` is `r`-MCA-bad for `(f₁,f₂)`: there is a proximity witness for `γ`
(a codeword `c` agreeing with the line word on a set `S` of `≥ n - r` coordinates)
that *fails* to extend to a mutual pair explanation on `S`. -/
def MCAbad (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) (γ : F) : Prop :=
  ∃ c ∈ C, ∃ S : Finset ι, Fintype.card ι - r ≤ S.card ∧
    (∀ j ∈ S, combo f1 f2 γ j = c j) ∧
    ¬ (∃ c1 ∈ C, ∃ c2 ∈ C, (∀ j ∈ S, f1 j = c1 j) ∧ (∀ j ∈ S, f2 j = c2 j))

/-- Number of `r`-CA-bad slopes for a fixed pair. -/
noncomputable def caBadCount (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) : ℕ :=
  (Finset.univ.filter (fun γ => CAbad C r f1 f2 γ)).card

/-- Number of `r`-MCA-bad slopes for a fixed pair. -/
noncomputable def mcaBadCount (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) : ℕ :=
  (Finset.univ.filter (fun γ => MCAbad C r f1 f2 γ)).card

/-- The correlated-agreement error `ε_ca(C, δ)` at integer radius `r = ⌊δ n⌋`. -/
noncomputable def epsCA (C : Submodule F (ι → F)) (r : ℕ) : ℚ :=
  ((Finset.univ.sup (fun p : (ι → F) × (ι → F) => caBadCount C r p.1 p.2) : ℕ) : ℚ)
    / (Fintype.card F : ℚ)

/-- The mutual correlated-agreement error `ε_mca(C, δ)` at integer radius
`r = ⌊δ n⌋`. -/
noncomputable def epsMCA (C : Submodule F (ι → F)) (r : ℕ) : ℚ :=
  ((Finset.univ.sup (fun p : (ι → F) × (ι → F) => mcaBadCount C r p.1 p.2) : ℕ) : ℚ)
    / (Fintype.card F : ℚ)

/-- Support union size of a pair `(ε₁, ε₂)`. -/
noncomputable def suppUnion (e1 e2 : ι → F) : ℕ :=
  (Finset.univ.filter (fun j => e1 j ≠ 0 ∨ e2 j ≠ 0)).card

/-- The sparse mutual layer `σ_C(δ)`: the maximum number of MCA-bad slopes over
pairs whose support union has size at most `r`. -/
noncomputable def sigmaC (C : Submodule F (ι → F)) (r : ℕ) : ℕ :=
  Finset.univ.sup fun p : (ι → F) × (ι → F) =>
    if suppUnion p.1 p.2 ≤ r then mcaBadCount C r p.1 p.2 else 0

/-! ## Basic sup/quotient helpers for the errors -/

/-
Pointwise upper bounds on the MCA count give an upper bound on `ε_mca`.
-/
omit [DecidableEq F] in
theorem epsMCA_le_of_forall {C : Submodule F (ι → F)} {r : ℕ} {B : ℕ}
    (h : ∀ f1 f2 : ι → F, mcaBadCount C r f1 f2 ≤ B) :
    epsMCA C r ≤ (B : ℚ) / (Fintype.card F : ℚ) := by
      exact div_le_div_of_nonneg_right ( Nat.cast_le.mpr <| Finset.sup_le fun p hp => h _ _ ) ( Nat.cast_nonneg _ )

/-
Pointwise upper bounds on the CA count give an upper bound on `ε_ca`.
-/
theorem epsCA_le_of_forall {C : Submodule F (ι → F)} {r : ℕ} {B : ℕ}
    (h : ∀ f1 f2 : ι → F, caBadCount C r f1 f2 ≤ B) :
    epsCA C r ≤ (B : ℚ) / (Fintype.card F : ℚ) := by
      exact div_le_div_of_nonneg_right ( Nat.cast_le.mpr <| Finset.sup_le fun _ _ => h _ _ ) <| Nat.cast_nonneg _

/-! ## Section 2. The comparison chain (Lemma 2.4) -/

/-
**Lemma 2.4 (chain), pointwise.** Every `r`-CA-bad slope is `r`-MCA-bad.
-/
omit [Fintype F] in
theorem CAbad_MCAbad {C : Submodule F (ι → F)} {r : ℕ} {f1 f2 : ι → F} {γ : F}
    (h : CAbad C r f1 f2 γ) : MCAbad C r f1 f2 γ := by
      obtain ⟨c, hc⟩ := h.left;
      refine' ⟨ c, hc.1, Finset.filter ( fun j => combo f1 f2 γ j = c j ) Finset.univ, _, _, _ ⟩ <;> simp_all +decide [ hd ];
      · have := Finset.card_add_card_compl ( Finset.filter ( fun j => combo f1 f2 γ j = c j ) Finset.univ ) ; simp_all +decide ; linarith;
      · intro c1 hc1 c2 hc2 h1
        have h_colFar : r < Finset.card (Finset.univ.filter (fun j => f1 j ≠ c1 j ∨ f2 j ≠ c2 j)) := by
          exact h.2 c1 hc1 c2 hc2;
        contrapose! h_colFar;
        exact le_trans ( Finset.card_le_card fun x hx => by aesop ) hc.2

/-
**Lemma 2.4 (chain).** `ε_ca(C, δ) ≤ ε_mca(C, δ)`.
-/
theorem epsCA_le_epsMCA (C : Submodule F (ι → F)) (r : ℕ) :
    epsCA C r ≤ epsMCA C r := by
      refine' div_le_div_of_nonneg_right _ ( Nat.cast_nonneg _ );
      norm_cast;
      refine' Finset.sup_mono_fun _;
      exact fun p _ => Finset.card_mono fun x hx => Finset.mem_filter.mpr ⟨ Finset.mem_filter.mp hx |>.1, CAbad_MCAbad ( Finset.mem_filter.mp hx |>.2 ) ⟩

/-! ## Section 3. Small fields (Proposition 3.8) -/

/-
**Proposition 3.8 (small fields).** For every proper linear code
`C ⊊ Fⁿ` and every radius, `ε_mca(C, δ) ≥ 1/q`.
-/
omit [DecidableEq F] in
theorem one_div_card_le_epsMCA {C : Submodule F (ι → F)} (hC : C ≠ ⊤) (r : ℕ) :
    (1 : ℚ) / (Fintype.card F : ℚ) ≤ epsMCA C r := by
      -- Since `C ≠ ⊤`, there is `f2 ∉ C` (from `Submodule.exists_notMem_of_ne_top` or by `ne_top_iff`/`SetLike` reasoning: `¬ (∀ x, x ∈ C)`).
      obtain ⟨f2, hf2⟩ : ∃ f2 : ι → F, f2 ∉ C := by
        simpa [ Submodule.eq_top_iff' ] using hC;
      -- We show `mcaBadCount C r 0 f2 ≥ 1` by showing `0` is MCA-bad.
      have h_mca_bad : MCAbad C r 0 f2 0 := by
        refine' ⟨ 0, C.zero_mem, Finset.univ, _, _, _ ⟩ <;> simp +decide;
        · simp +decide [ combo ];
        · exact fun x hx y hy hxy => not_forall.mp fun h => hf2 <| by convert hy; ext j; simp +decide [ ← h j ] ;
      refine' le_trans _ ( div_le_div_of_nonneg_right ( Nat.cast_le.mpr <| Finset.le_sup <| Finset.mem_univ ( 0, f2 ) ) <| Nat.cast_nonneg _ );
      exact div_le_div_of_nonneg_right ( mod_cast Finset.card_pos.mpr ⟨ 0, Finset.mem_filter.mpr ⟨ Finset.mem_univ _, h_mca_bad ⟩ ⟩ ) ( Nat.cast_nonneg _ )

/-! ## Section 4 (safe side). Deep regime (Theorem 4.9) -/

/-
A word that vanishes off a set `S` has weight at most `|S|`.
-/
omit [DecidableEq ι] [Fintype F] in
theorem wt_le_of_zero_off {d : ι → F} {S : Finset ι} (h : ∀ j ∉ S, d j = 0) :
    wt d ≤ S.card := by
      exact Finset.card_le_card fun x hx => by contrapose! hx; aesop;

/-
A codeword of weight strictly less than the minimum weight is zero.
-/
omit [DecidableEq ι] [Fintype F] in
theorem eq_zero_of_wt_lt {C : Submodule F (ι → F)} {wmin : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) {d : ι → F} (hdC : d ∈ C)
    (hlt : wt d < wmin) : d = 0 := by
      exact Classical.not_not.1 fun h => hlt.not_ge <| hmin d hdC h

/-
Any MCA-bad slope has its line word `r`-close to `C`.
-/
omit [Fintype F] in
theorem MCAbad_imp_closeBy {C : Submodule F (ι → F)} {r : ℕ} {f1 f2 : ι → F} {γ : F}
    (h : MCAbad C r f1 f2 γ) : closeBy C r (combo f1 f2 γ) := by
      obtain ⟨ c, hc, S, hS₁, hS₂, hS₃ ⟩ := h;
      refine' ⟨ c, hc, _ ⟩;
      refine' le_trans ( Finset.card_le_card _ ) _;
      exact Finset.univ \ S; all_goals grind

/-
The number of MCA-bad slopes is at most the number of slopes whose line word
is `r`-close to `C`.
-/
theorem mcaBadCount_le_closeBy (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) :
    mcaBadCount C r f1 f2 ≤
      (Finset.univ.filter (fun γ => closeBy C r (combo f1 f2 γ))).card := by
        refine Finset.card_le_card ?_;
        exact fun γ hγ => by simpa using MCAbad_imp_closeBy ( by simpa using hγ ) ;

/-
Collapse step for the deep regime. If `≥ 3` slopes each have a codeword
explanation of the line word off a set of size `≤ r`, and `3r < wmin`, then there
is a single pair `(ee, dd)` of codewords with `(a-b) • dd = cw a - cw b` and
`(a-b) • ee = a • cw b - b • cw a` for all distinct explaining slopes `a, b`.
-/
omit [Fintype F] in
theorem deep_collapse {C : Submodule F (ι → F)} {wmin r : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) (h3r : 3 * r < wmin)
    {f1 f2 : ι → F} {G : Finset F} {cw : F → ι → F}
    (hcwC : ∀ γ ∈ G, cw γ ∈ C)
    (hcwE : ∀ γ ∈ G, (Finset.univ.filter (fun i => f1 i + γ * f2 i ≠ cw γ i)).card ≤ r)
    (hG3 : 3 ≤ G.card) :
    ∃ dd ∈ C, ∃ ee ∈ C, ∀ a ∈ G, ∀ b ∈ G, a ≠ b →
      (a - b) • dd = cw a - cw b ∧ (a - b) • ee = a • cw b - b • cw a := by
        -- By the properties of the field $F$, we can choose three distinct elements $γ0$, $γ1$, and $γ2$ from $G$.
        obtain ⟨γ0, γ1, γ2, hγ0, hγ1, hγ2, h_distinct⟩ : ∃ γ0 γ1 γ2 : F, γ0 ∈ G ∧ γ1 ∈ G ∧ γ2 ∈ G ∧ γ0 ≠ γ1 ∧ γ0 ≠ γ2 ∧ γ1 ≠ γ2 := by
          rcases Finset.two_lt_card.1 hG3 with ⟨ γ0, hγ0, γ1, hγ1, hne ⟩ ; use γ0, γ1 ; aesop;
        -- Define P and Q as the normalized differences of the codewords.
        set P : F → F → (ι → F) := fun x y => (x - y)⁻¹ • (cw x - cw y)
        set Q : F → F → (ι → F) := fun x y => (x - y)⁻¹ • (x • cw y - y • cw x);
        -- By ATOMIC, we have $P x y = P x z$ and $Q x y = Q x z$ for any distinct $x, y, z \in G$.
        have hPQ_eq : ∀ x y z : F, x ∈ G → y ∈ G → z ∈ G → x ≠ y → x ≠ z → y ≠ z → P x y = P x z ∧ Q x y = Q x z := by
          intros x y z hx hy hz hxy hxz hyz
          have hP : P x y = P x z := by
            have hP : wt (P x y - P x z) < wmin := by
              have hP_zero : ∀ i ∉ (Finset.univ.filter (fun j => f1 j + x * f2 j ≠ cw x j) ∪ Finset.univ.filter (fun j => f1 j + y * f2 j ≠ cw y j) ∪ Finset.univ.filter (fun j => f1 j + z * f2 j ≠ cw z j)), (P x y - P x z) i = 0 := by
                simp +zetaDelta at *;
                grind;
              refine' lt_of_le_of_lt ( wt_le_of_zero_off hP_zero ) _;
              exact lt_of_le_of_lt ( Finset.card_union_le _ _ ) ( lt_of_le_of_lt ( add_le_add ( Finset.card_union_le _ _ ) le_rfl ) ( by linarith [ hcwE x hx, hcwE y hy, hcwE z hz ] ) );
            contrapose! hP;
            exact hmin _ ( Submodule.sub_mem _ ( Submodule.smul_mem _ _ ( Submodule.sub_mem _ ( hcwC _ hx ) ( hcwC _ hy ) ) ) ( Submodule.smul_mem _ _ ( Submodule.sub_mem _ ( hcwC _ hx ) ( hcwC _ hz ) ) ) ) ( sub_ne_zero_of_ne hP )
          have hQ : Q x y = Q x z := by
            have hQ : wt (Q x y - Q x z) ≤ (Finset.univ.filter (fun i => f1 i + x * f2 i ≠ cw x i)).card + (Finset.univ.filter (fun i => f1 i + y * f2 i ≠ cw y i)).card + (Finset.univ.filter (fun i => f1 i + z * f2 i ≠ cw z i)).card := by
              refine' le_trans ( wt_le_of_zero_off _ ) _;
              exact Finset.filter ( fun i => f1 i + x * f2 i ≠ cw x i ) Finset.univ ∪ Finset.filter ( fun i => f1 i + y * f2 i ≠ cw y i ) Finset.univ ∪ Finset.filter ( fun i => f1 i + z * f2 i ≠ cw z i ) Finset.univ;
              · simp +zetaDelta at *;
                grind;
              · exact le_trans ( Finset.card_union_le _ _ ) ( add_le_add ( Finset.card_union_le _ _ ) le_rfl );
            contrapose! hmin;
            refine' ⟨ Q x y - Q x z, _, _, _ ⟩;
            · exact C.sub_mem ( C.smul_mem _ ( C.sub_mem ( C.smul_mem _ ( hcwC _ hy ) ) ( C.smul_mem _ ( hcwC _ hx ) ) ) ) ( C.smul_mem _ ( C.sub_mem ( C.smul_mem _ ( hcwC _ hz ) ) ( C.smul_mem _ ( hcwC _ hx ) ) ) );
            · exact sub_ne_zero_of_ne hmin;
            · linarith [ hcwE x hx, hcwE y hy, hcwE z hz ]
          exact ⟨hP, hQ⟩;
        -- By ATOMIC, we have $P x y = P y x$ and $Q x y = Q y x$ for any distinct $x, y \in G$.
        have hPQ_symm : ∀ x y : F, x ∈ G → y ∈ G → x ≠ y → P x y = P y x ∧ Q x y = Q y x := by
          simp +zetaDelta at *;
          intro x y hx hy hxy; rw [ show x - y = - ( y - x ) by ring, inv_neg ] ; simp +decide [ neg_smul ] ;
          exact ⟨ by rw [ ← smul_neg, neg_sub ], by rw [ ← smul_neg, neg_sub ] ⟩;
        -- By ATOMIC, we have $P x y = P γ0 γ1$ and $Q x y = Q γ0 γ1$ for any distinct $x, y \in G$.
        have hPQ_eq_all : ∀ x y : F, x ∈ G → y ∈ G → x ≠ y → P x y = P γ0 γ1 ∧ Q x y = Q γ0 γ1 := by
          intros x y hx hy hxy
          by_cases hxγ0 : x = γ0 ∨ x = γ1 ∨ x = γ2
          by_cases hyγ0 : y = γ0 ∨ y = γ1 ∨ y = γ2
          generalize_proofs at *; (
          rcases hxγ0 with ( rfl | rfl | rfl ) <;> rcases hyγ0 with ( rfl | rfl | rfl ) <;> simp +decide [ * ] at hxy ⊢;
          · grind +ring;
          · grind +ring;
          · grind +ring;
          · grind);
          · grind +ring;
          · grind +qlia;
        refine' ⟨ P γ0 γ1, _, Q γ0 γ1, _, _ ⟩;
        · exact C.smul_mem _ ( C.sub_mem ( hcwC _ hγ0 ) ( hcwC _ hγ1 ) );
        · exact C.smul_mem _ ( C.sub_mem ( C.smul_mem _ ( hcwC _ hγ1 ) ) ( C.smul_mem _ ( hcwC _ hγ0 ) ) );
        · intro a ha b hb hab; specialize hPQ_eq_all a b ha hb hab; simp_all +decide ;
          exact ⟨ by rw [ ← hPQ_eq_all.1, smul_smul, mul_inv_cancel₀ ( sub_ne_zero_of_ne hab ), one_smul ], by rw [ ← hPQ_eq_all.2, smul_smul, mul_inv_cancel₀ ( sub_ne_zero_of_ne hab ), one_smul ] ⟩

/-
**Theorem 4.9 (deep regime), dichotomy.** For a linear code of minimum weight
`wmin` and radius `r` with `3r ≤ wmin - 1`, every pair either lies within column
distance `r` of a single pair explanation off a set of size `≤ r`, or has at most
`r + 1` slopes whose line word is `r`-close to `C`.
-/
theorem deep_dichotomy {C : Submodule F (ι → F)} {wmin r : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) (h3r : 3 * r ≤ wmin - 1)
    (f1 f2 : ι → F) :
    (∃ c1 ∈ C, ∃ c2 ∈ C, ∃ T : Finset ι, T.card ≤ r ∧
        ∀ j ∉ T, f1 j = c1 j ∧ f2 j = c2 j)
    ∨ ((Finset.univ.filter (fun γ => closeBy C r (combo f1 f2 γ))).card ≤ r + 1) := by
  by_contra! h₂;
  -- From the second failing disjunct: `r + 2 ≤ (Finset.univ.filter (fun γ => closeBy C r (combo f1 f2 γ))).card`.
  obtain ⟨G, hG⟩ : ∃ G : Finset F, G.card = r + 2 ∧ ∀ γ ∈ G, closeBy C r (combo f1 f2 γ) := by
    exact Exists.elim ( Finset.exists_subset_card_eq h₂.2 ) fun G hG => ⟨ G, hG.2, fun γ hγ => Finset.mem_filter.mp ( hG.1 hγ ) |>.2 ⟩;
  -- By `choose!` on `closeBy` (which is `∃ c ∈ C, hd (combo f1 f2 γ) c ≤ r`), obtain `cw : F → ι → F` with, for `γ ∈ G`: `cw γ ∈ C` and `hd (combo f1 f2 γ) (cw γ) ≤ r`.
  obtain ⟨cw, hcwC, hcwE⟩ : ∃ cw : F → ι → F, (∀ γ ∈ G, cw γ ∈ C) ∧ (∀ γ ∈ G, (Finset.univ.filter (fun i => f1 i + γ * f2 i ≠ cw γ i)).card ≤ r) := by
    choose! cw hcwC hcwE using hG.2;
    exact ⟨ cw, hcwC, hcwE ⟩;
  by_cases hr : r = 0;
  · obtain ⟨a, b, hab⟩ : ∃ a b : F, a ≠ b ∧ a ∈ G ∧ b ∈ G := by
      obtain ⟨ a, ha, b, hb, hab ⟩ := Finset.one_lt_card.1 ( by linarith ) ; exact ⟨ a, b, hab, ha, hb ⟩ ;
    -- For every `i`: from `f1 i + a f2 i = cw a i`, `f1 i + b f2 i = cw b i`, solve `f2 i = c2 i` and `f1 i = c1 i` (`field_simp`/`linear_combination`, `a - b ≠ 0`).
    have h_solve : ∀ i, f1 i = ((a * cw b i - b * cw a i) / (a - b)) ∧ f2 i = ((cw a i - cw b i) / (a - b)) := by
      intro i
      have h_eq : f1 i + a * f2 i = cw a i ∧ f1 i + b * f2 i = cw b i := by
        simp_all +decide [ Finset.ext_iff ];
      grind;
    refine' h₂.1 ( fun i => ( a * cw b i - b * cw a i ) / ( a - b ) ) _ ( fun i => ( cw a i - cw b i ) / ( a - b ) ) _ ∅ _ |> fun ⟨ j, hj₁, hj₂ ⟩ => hj₂ ( h_solve j |>.1 ) ( h_solve j |>.2 );
    · convert C.smul_mem ( ( a - b ) ⁻¹ ) ( C.sub_mem ( C.smul_mem a ( hcwC b hab.2.2 ) ) ( C.smul_mem b ( hcwC a hab.2.1 ) ) ) using 1 ; ext i ; simp +decide [ div_eq_inv_mul ];
    · convert C.smul_mem ( ( a - b ) ⁻¹ ) ( C.sub_mem ( hcwC a hab.2.1 ) ( hcwC b hab.2.2 ) ) using 1 ; ext i ; simp +decide [ div_eq_inv_mul ];
    · simp +decide [ hr ];
  · -- Since `r ≥ 1`, we have `G.card = r + 2 ≥ 3`, so apply `deep_collapse hmin (by omega : 3*r < wmin) hcwC hcwE (by omega : 3 ≤ G.card)` to get `dd ∈ C`, `ee ∈ C` with `KEY : ∀ a ∈ G, ∀ b ∈ G, a ≠ b → (a-b) • dd = cw a - cw b ∧ (a-b) • ee = a • cw b - b • cw a`.
    obtain ⟨dd, hddC, ee, heeC, hKEY⟩ : ∃ dd ∈ C, ∃ ee ∈ C, ∀ a ∈ G, ∀ b ∈ G, a ≠ b → (a - b) • dd = cw a - cw b ∧ (a - b) • ee = a • cw b - b • cw a := by
      apply deep_collapse hmin (by omega) hcwC hcwE (by omega);
    -- Define `T := Finset.univ.filter (fun i => f1 i ≠ ee i ∨ f2 i ≠ dd i)`. We show `T.card ≤ r` and that off `T`, `f1 = ee ∧ f2 = dd`, giving the left disjunct (with `c1 := ee`, `c2 := dd`), a contradiction.
    set T := Finset.univ.filter (fun i => f1 i ≠ ee i ∨ f2 i ≠ dd i) with hT_def
    have hT_card : T.card ≤ r := by
      -- Prove that for each `i ∈ T`, there are at least `r + 1` slopes `γ ∈ G` such that `f1 i + γ * f2 i ≠ cw γ i`.
      have hT_slope_count : ∀ i ∈ T, (Finset.univ.filter (fun γ => γ ∈ G ∧ f1 i + γ * f2 i ≠ cw γ i)).card ≥ r + 1 := by
        intro i hi
        by_contra h_contra
        push_neg at h_contra
        have h_slope_count : (Finset.univ.filter (fun γ => γ ∈ G ∧ f1 i + γ * f2 i = cw γ i)).card ≥ 2 := by
          have h_card : (Finset.univ.filter (fun γ => γ ∈ G ∧ f1 i + γ * f2 i = cw γ i)).card + (Finset.univ.filter (fun γ => γ ∈ G ∧ f1 i + γ * f2 i ≠ cw γ i)).card = G.card := by
            rw [ ← Finset.card_union_of_disjoint ];
            · congr with γ ; by_cases h : f1 i + γ * f2 i = cw γ i <;> simp +decide [ h ];
            · exact Finset.disjoint_filter.mpr ( by aesop );
          linarith
        obtain ⟨a, haG, b, hbG, hab⟩ : ∃ a ∈ G, ∃ b ∈ G, a ≠ b ∧ f1 i + a * f2 i = cw a i ∧ f1 i + b * f2 i = cw b i := by
          obtain ⟨ a, ha, b, hb, hab ⟩ := Finset.one_lt_card.mp h_slope_count; use a, by aesop, b, by aesop; ; aesop;
        have h_eq : f2 i = dd i ∧ f1 i = ee i := by
          have := hKEY a haG b hbG hab.1; simp_all +decide [ funext_iff, Finset.ext_iff ] ;
          grind
        simp_all +decide [ Finset.ext_iff ];
      -- Double count: `∑ i ∈ T, (Finset.univ.filter (fun γ => γ ∈ G ∧ f1 i + γ * f2 i ≠ cw γ i)).card ≤ ∑ γ ∈ G, (Finset.univ.filter (fun i => f1 i + γ * f2 i ≠ cw γ i)).card`.
      have hT_double_count : ∑ i ∈ T, (Finset.univ.filter (fun γ => γ ∈ G ∧ f1 i + γ * f2 i ≠ cw γ i)).card ≤ ∑ γ ∈ G, (Finset.univ.filter (fun i => f1 i + γ * f2 i ≠ cw γ i)).card := by
        simp +decide only [Finset.card_filter];
        rw [ Finset.sum_comm ];
        rw [ ← Finset.sum_subset ( Finset.subset_univ G ) ];
        · exact Finset.sum_le_sum fun x hx => Finset.sum_le_sum_of_subset ( Finset.filter_subset _ _ ) |> le_trans <| Finset.sum_le_sum fun y hy => by aesop;
        · simp +contextual;
      have := Finset.sum_le_sum hT_slope_count; simp_all +decide ;
      exact Nat.le_of_lt_succ ( by nlinarith [ show ∑ x ∈ G, Finset.card ( Finset.filter ( fun i => ¬f1 i + x * f2 i = cw x i ) Finset.univ ) ≤ ( r + 2 ) * r by exact le_trans ( Finset.sum_le_sum fun x hx => hcwE x hx ) ( by simp +decide [ hG.1 ] ) ] );
    exact h₂.1 ee heeC dd hddC T hT_card |> fun ⟨ j, hj₁, hj₂ ⟩ => hj₂ ( by aesop ) ( by aesop )

/-
**Theorem 4.11 (half), per pair.** Under `2r ≤ wmin - 1`, every pair has at
most `max (caBadCount) r` MCA-bad slopes.
-/
theorem half_mcaBadCount_le {C : Submodule F (ι → F)} {wmin r : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) (h2r : 2 * r ≤ wmin - 1)
    (f1 f2 : ι → F) : mcaBadCount C r f1 f2 ≤ max (caBadCount C r f1 f2) r := by
      by_cases h_colFar : ∀ c1 ∈ C, ∀ c2 ∈ C, r < cdist f1 f2 c1 c2;
      · refine' le_max_of_le_left ( Finset.card_le_card _ );
        intro γ hγ
        obtain ⟨c, hcC, S, hS_card, hS_eq, hS_not_ext⟩ := (Finset.mem_filter.mp hγ).right
        have h_close : closeBy C r (combo f1 f2 γ) := by
          refine' ⟨ c, hcC, _ ⟩;
          have h_close : (Finset.univ \ S).card ≤ r := by
            grind;
          exact le_trans ( Finset.card_le_card fun x hx => by aesop ) h_close
        exact Finset.mem_filter.mpr ⟨Finset.mem_univ γ, h_close, h_colFar⟩;
      · -- Let `p1 ∈ C`, `p2 ∈ C` with `cdist f1 f2 p1 p2 ≤ r`.
        obtain ⟨p1, hp1C, p2, hp2C, hcdist⟩ : ∃ p1 ∈ C, ∃ p2 ∈ C, cdist f1 f2 p1 p2 ≤ r := by
          aesop;
        -- Let `E := Finset.univ.filter (fun j => f1 j ≠ p1 j ∨ f2 j ≠ p2 j)`, so `E.card = cdist f1 f2 p1 p2 ≤ r`.
        set E := Finset.univ.filter (fun j => f1 j ≠ p1 j ∨ f2 j ≠ p2 j)
        have hE_card : E.card ≤ r := by
          exact hcdist;
        -- Every MCA-bad slope γ is "tangent": ∃ j ∈ E, e1 j + γ * e2 j = 0.
        have h_tangent : ∀ γ, MCAbad C r f1 f2 γ → ∃ j ∈ E, (f1 j - p1 j) + γ * (f2 j - p2 j) = 0 := by
          intro γ hγ
          obtain ⟨c, hcC, S, hS_card, hS_eq, hS_fail⟩ := hγ
          set d := fun j => c j - (p1 j + γ * p2 j)
          have hdC : d ∈ C := by
            exact C.sub_mem hcC ( C.add_mem hp1C ( C.smul_mem γ hp2C ) )
          have hd_zero : ∀ j ∈ S \ E, d j = 0 := by
            simp +zetaDelta at *;
            intro j hj hj1 hj2; specialize hS_eq j hj; simp_all +decide [ combo ] ;
          have hd_card : wt d ≤ wmin - 1 := by
            have hd_card : (Finset.univ.filter (fun j => d j ≠ 0)).card ≤ (Finset.univ \ (S \ E)).card := by
              exact Finset.card_le_card fun x hx => by contrapose! hx; aesop;
            simp_all +decide [ Finset.card_sdiff ];
            exact hd_card.trans ( Nat.sub_le_of_le_add <| by linarith [ Nat.sub_add_cancel <| show ( E ∩ S ).card ≤ S.card from Finset.card_le_card fun x hx => by aesop, show ( E ∩ S ).card ≤ E.card from Finset.card_le_card fun x hx => by aesop ] )
          have hd_zero_all : d = 0 := by
            grind
          have h_tangent : ∀ j ∈ S, (f1 j - p1 j) + γ * (f2 j - p2 j) = 0 := by
            simp_all +decide [ funext_iff, combo ];
            grind +splitImp
          by_contra h_contra
          push_neg at h_contra
          have h_fail : ∃ c1 ∈ C, ∃ c2 ∈ C, (∀ j ∈ S, f1 j = c1 j) ∧ (∀ j ∈ S, f2 j = c2 j) := by
            grind +splitImp
          exact hS_fail h_fail;
        -- The set of MCA-bad slopes is contained in the set of slopes that are tangent to `E`.
        have h_subset : Finset.filter (fun γ => MCAbad C r f1 f2 γ) Finset.univ ⊆ Finset.image (fun j => - (f1 j - p1 j) / (f2 j - p2 j)) E := by
          grind;
        exact le_trans ( Finset.card_le_card h_subset ) ( Finset.card_image_le.trans ( by simpa using hE_card ) ) |> le_trans <| le_max_right _ _

/-- **Theorem 4.9 (deep regime), per pair.** Under the deep hypothesis, every pair
has at most `r + 1` MCA-bad slopes. -/
theorem deep_mcaBadCount_le {C : Submodule F (ι → F)} {wmin r : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) (h3r : 3 * r ≤ wmin - 1)
    (f1 f2 : ι → F) : mcaBadCount C r f1 f2 ≤ r + 1 := by
  have h2r : 2 * r ≤ wmin - 1 := by omega
  refine le_trans (half_mcaBadCount_le hmin h2r f1 f2) (max_le ?_ (by omega))
  by_cases hcf : colFar C r f1 f2
  · refine le_trans ?_ ((deep_dichotomy hmin h3r f1 f2).resolve_left ?_)
    · refine Finset.card_le_card ?_
      intro γ hγ
      exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, (Finset.mem_filter.mp hγ).2.1⟩
    · rintro ⟨c1, hc1, c2, hc2, T, hT, hTagr⟩
      have hcd : cdist f1 f2 c1 c2 ≤ T.card := by
        refine Finset.card_le_card ?_
        intro j hj
        by_contra hjT
        rcases (Finset.mem_filter.mp hj).2 with h | h
        · exact h (hTagr j hjT).1
        · exact h (hTagr j hjT).2
      exact absurd (hcf c1 hc1 c2 hc2) (by omega)
  · have hzero : caBadCount C r f1 f2 = 0 := by
      refine Finset.card_eq_zero.mpr (Finset.filter_eq_empty_iff.mpr ?_)
      intro γ _
      exact fun hCA => hcf hCA.2
    omega

/-
**Theorem 4.9 (deep regime).** `ε_mca(C, δ) ≤ (r+1)/q`.
-/
theorem deep_epsMCA_le {C : Submodule F (ι → F)} {wmin r : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) (h3r : 3 * r ≤ wmin - 1) :
    epsMCA C r ≤ ((r : ℚ) + 1) / (Fintype.card F : ℚ) := by
      have h := epsMCA_le_of_forall (B := r + 1)
        (fun f1 f2 => deep_mcaBadCount_le hmin h3r f1 f2)
      rw [show ((r : ℚ) + 1) = ((r + 1 : ℕ) : ℚ) by push_cast; ring]
      exact h

/-! ## Section 4 (safe side). Mutual from correlated below half the distance (Theorem 4.11) -/


/-
**Theorem 4.11 (mutual from correlated, below half the distance).**
`ε_mca(C, δ) ≤ max(ε_ca(C, δ), r/q)`.
-/
theorem half_epsMCA_le {C : Submodule F (ι → F)} {wmin r : ℕ}
    (hmin : ∀ c ∈ C, c ≠ 0 → wmin ≤ wt c) (h2r : 2 * r ≤ wmin - 1) :
    epsMCA C r ≤ max (epsCA C r) ((r : ℚ) / (Fintype.card F : ℚ)) := by
      have h_le_max : ∀ f1 f2 : ι → F, mcaBadCount C r f1 f2 ≤ max (caBadCount C r f1 f2) r := by
        exact fun f1 f2 => half_mcaBadCount_le hmin h2r f1 f2;
      have h_sup_le_max : (Finset.univ.sup (fun p : (ι → F) × (ι → F) => mcaBadCount C r p.1 p.2)) ≤ max (Finset.univ.sup (fun p : (ι → F) × (ι → F) => caBadCount C r p.1 p.2)) r := by
        refine' Finset.sup_le _;
        exact fun p _ => le_trans ( h_le_max _ _ ) ( max_le_max ( Finset.le_sup ( f := fun p : ( ι → F ) × ( ι → F ) => caBadCount C r p.1 p.2 ) ( Finset.mem_univ p ) ) le_rfl );
      unfold epsMCA epsCA; simp_all +decide ;
      cases' h_sup_le_max with h h;
      · exact Or.inl ( div_le_div_of_nonneg_right ( mod_cast Finset.sup_le fun p hp => h p.1 p.2 ) ( Nat.cast_nonneg _ ) );
      · exact Or.inr ( by gcongr ; exact Finset.sup_le fun p _ => h _ _ )

/-! ## Section 5. Exact sparsification of the mutual layer -/

/-
**Lemma 5.1 (one slope per witness set), clause (3).** If `g₂|_S ∉ C|_S`,
then `(g₁ + γ g₂)|_S ∈ C|_S` for at most one `γ`.
-/
omit [Fintype ι] [DecidableEq ι] [Fintype F] [DecidableEq F] in
theorem line_at_most_one_slope {C : Submodule F (ι → F)} {g1 g2 : ι → F}
    {S : Finset ι} (hg2 : ¬ ∃ c ∈ C, ∀ j ∈ S, g2 j = c j) :
    ∀ γ γ', (∃ c ∈ C, ∀ j ∈ S, combo g1 g2 γ j = c j) →
      (∃ c ∈ C, ∀ j ∈ S, combo g1 g2 γ' j = c j) → γ = γ' := by
        contrapose! hg2; simp_all +decide [ combo ] ;
        obtain ⟨ γ, ⟨ c, hc, hc' ⟩, x, ⟨ d, hd, hd' ⟩, hne ⟩ := hg2; use ( γ - x ) ⁻¹ • ( c - d ) ; simp_all +decide ;
        exact ⟨ C.smul_mem _ ( C.sub_mem hc hd ), fun j hj => by rw [ inv_mul_eq_div, eq_div_iff ( sub_ne_zero_of_ne hne ) ] ; linear_combination hc' j hj - hd' j hj ⟩

/-
**Theorem 5.3 (sparsification of the mutual layer).**
`ε_mca(C, δ) = max(ε_ca(C, δ), σ_C(δ)/q)`.
-/
theorem sparsify (C : Submodule F (ι → F)) (r : ℕ) :
    epsMCA C r = max (epsCA C r) ((sigmaC C r : ℚ) / (Fintype.card F : ℚ)) := by
      -- To prove equality, we show that $Nm = max Nc (sigmaC)$ by showing that $Nm$ is both an upper bound and a lower bound for $max Nc (sigmaC)$.
      have hNm_le : (Finset.univ.sup (fun p : (ι → F) × (ι → F) => mcaBadCount C r p.1 p.2)) ≤ max (Finset.univ.sup (fun p : (ι → F) × (ι → F) => caBadCount C r p.1 p.2)) (sigmaC C r) := by
        refine' Finset.sup_le fun p hp => _;
        by_cases hcolFar : colFar C r p.1 p.2 <;> simp_all +decide [ sigmaC ];
        · refine' Or.inl ( le_trans _ ( Finset.le_sup ( f := fun p : ( ι → F ) × ( ι → F ) => caBadCount C r p.1 p.2 ) ( Finset.mem_univ p ) ) );
          refine' Finset.card_le_card _;
          intro γ hγ; simp_all +decide [ MCAbad, CAbad ] ;
          obtain ⟨ c, hc, S, hS₁, hS₂, hS₃ ⟩ := hγ; use c; simp_all +decide [ hd ] ;
          exact le_trans ( Finset.card_le_card ( show Finset.filter ( fun j => ¬combo p.1 p.2 γ j = c j ) Finset.univ ⊆ Finset.univ \ S from fun x hx => by aesop ) ) ( by simp +decide [ Finset.card_sdiff, * ] ; omega );
        · right;
          obtain ⟨c1, hc1, c2, hc2, hcdist⟩ : ∃ c1 ∈ C, ∃ c2 ∈ C, cdist p.1 p.2 c1 c2 ≤ r := by
            contrapose! hcolFar; aesop;
          refine' le_trans _ ( Finset.le_sup ( f := fun p : ( ι → F ) × ( ι → F ) => if suppUnion p.1 p.2 ≤ r then mcaBadCount C r p.1 p.2 else 0 ) ( Finset.mem_univ ( p.1 - c1, p.2 - c2 ) ) );
          simp +decide [ suppUnion, cdist ] at hcdist ⊢;
          simp_all +decide [ sub_eq_zero ];
          refine' Finset.card_mono _;
          intro γ hγ; simp_all +decide [ MCAbad ] ;
          obtain ⟨ c, hc, S, hS₁, hS₂, hS₃ ⟩ := hγ; use c - ( c1 + γ • c2 ), by
            exact C.sub_mem hc ( C.add_mem hc1 ( C.smul_mem γ hc2 ) ), S, hS₁, by
            simp_all +decide [ combo ];
            intro j hj; linear_combination hS₂ j hj;, by
            intro x hx y hy hxy; specialize hS₃ ( x + c1 ) ( by exact C.add_mem hx hc1 ) ( y + c2 ) ( by exact C.add_mem hy hc2 ) ; simp_all +decide [ sub_eq_iff_eq_add ] ;;
      have hNm_ge : max (Finset.univ.sup (fun p : (ι → F) × (ι → F) => caBadCount C r p.1 p.2)) (sigmaC C r) ≤ Finset.univ.sup (fun p : (ι → F) × (ι → F) => mcaBadCount C r p.1 p.2) := by
        refine' max_le _ _;
        · exact Finset.sup_mono_fun fun p _ => Finset.card_mono fun γ hγ => by exact CAbad_MCAbad ( Finset.mem_filter.mp hγ |>.2 ) |> fun h => Finset.mem_filter.mpr ⟨ Finset.mem_univ _, h ⟩ ;
        · refine' Finset.sup_le fun p hp => _;
          split_ifs <;> [ exact Finset.le_sup ( f := fun p : ( ι → F ) × ( ι → F ) => mcaBadCount C r p.1 p.2 ) hp; exact Nat.zero_le _ ];
      unfold epsMCA epsCA;
      rw [ max_div_div_right ];
      · rw [ le_antisymm hNm_le hNm_ge, Nat.cast_max ];
      · positivity

/-! ## Reed–Solomon codes and the threshold -/

/-- The Reed–Solomon code `RS[F, D, k]`: evaluations at the points `ev` of the
polynomials of degree `< k`. Here `ev : ι → F` lists the evaluation domain. -/
noncomputable def RS (ev : ι → F) (k : ℕ) : Submodule F (ι → F) :=
  (Polynomial.degreeLT F k).map (LinearMap.pi (fun j => Polynomial.leval (ev j)))

omit [Fintype ι] [DecidableEq ι] [Fintype F] [DecidableEq F] in
/-- Membership in the Reed–Solomon code. -/
theorem mem_RS {ev : ι → F} {k : ℕ} {u : ι → F} :
    u ∈ RS ev k ↔ ∃ p : Polynomial F, p.degree < k ∧ ∀ j, u j = p.eval (ev j) := by
  constructor
  · rintro ⟨p, hp, rfl⟩
    exact ⟨p, (Polynomial.mem_degreeLT).1 hp, fun _ => rfl⟩
  · rintro ⟨p, hp, hu⟩
    exact ⟨p, (Polynomial.mem_degreeLT).2 hp, by ext j; exact (hu j).symm⟩

/-- The grand MCA threshold `δ*_C(ε*)`. The membership uses the integer radius
`⌊δ n⌋`, and `sSup ∅ = 0` matches the paper's `sup ∅ := 0`. -/
noncomputable def dstar (C : Submodule F (ι → F)) (ρ : ℝ) (eps : ℚ) : ℝ :=
  sSup {δ : ℝ | 0 < δ ∧ δ < 1 - ρ ∧ epsMCA C ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ eps}

/-! ## Section 6. Proof of Theorem 1.1 — clause (1) -/

/-
**Theorem 1.1(1).** If `q < 2¹²⁸`, then at the grand target `ε* = 2⁻¹²⁸` the
threshold is `δ*_C(2⁻¹²⁸) = 0`, for every proper linear code.
-/
omit [DecidableEq F] in
theorem dstar_eq_zero_of_small (C : Submodule F (ι → F)) (hC : C ≠ ⊤) (ρ : ℝ)
    (hq : (Fintype.card F : ℚ) < 2 ^ 128) :
    dstar C ρ ((2 ^ 128)⁻¹) = 0 := by
      -- Apply the lemma that states the set is empty.
      have h_empty : {δ : ℝ | 0 < δ ∧ δ < 1 - ρ ∧ epsMCA C ⌊δ * (Fintype.card ι : ℝ)⌋₊ ≤ (2 ^ 128 : ℚ)⁻¹} = ∅ := by
        apply Set.eq_empty_of_forall_notMem
        intro δ hδ
        obtain ⟨hδ_pos, hδ_lt, hδ_eps⟩ := hδ
        have h_eps : (1 : ℚ) / (Fintype.card F : ℚ) ≤ epsMCA C ⌊δ * (Fintype.card ι : ℝ)⌋₊ := by
          exact one_div_card_le_epsMCA hC _
        have h_contra : (1 : ℚ) / (Fintype.card F : ℚ) ≤ (2 ^ 128 : ℚ)⁻¹ := by
          exact h_eps.trans hδ_eps
        have h_card : (Fintype.card F : ℚ) ≥ 2 ^ 128 := by
          rw [ inv_eq_one_div, div_le_div_iff₀ ] at h_contra <;> norm_cast at * <;> linarith [ show 0 < Fintype.card F from Fintype.card_pos ] ;
        exact hq.not_ge h_card;
      unfold dstar; aesop;

/-! ## Section 3 (unsafe side)

The graded prefix floor (`prefix_floor`) is proved below for the identity locator
(`c = 1`), which is the case used in `Corollary 3.5 (ordinary locator cap)`. The
deep-point conversion (`deep_point_conversion`) is proved below via the
list-decoding infrastructure developed after `prefix_floor`. -/

/--
**Lemma 3.1 (graded prefix floor)** for the identity locator (`c = 1`). Some
received word `U` carries at least `C(n,m)/q^{m-K}` Reed–Solomon codewords of
`RS[F,D,K]` within Hamming distance `n - m` (i.e. a large list at agreement `m`).
The pigeonhole is over the prefix of elementary-symmetric coefficients of the
degree-`m` locators `∏_{x ∈ M}(X - ev x)`. The general complete-fiber version
(arbitrary locators `φ` of degree `c`) follows the same argument. -/
theorem prefix_floor {ev : ι → F} (hev : Function.Injective ev)
    {K m : ℕ} (hK : 1 ≤ K) (hmK : K ≤ m)
    (hm : m ≤ Fintype.card ι) :
    ∃ U : ι → F,
      Nat.choose (Fintype.card ι) m / (Fintype.card F) ^ (m - K) ≤
        (Finset.univ.filter (fun c => c ∈ RS ev K ∧
          hd U c ≤ Fintype.card ι - m)).card := by
            by_contra! h_contra;
            -- By the pigeonhole principle, there exists a coefficient vector $z$ such that at least $C(n,m)/q^{m−K}$ subsets $M$ satisfy the condition.
            obtain ⟨z, hz⟩ : ∃ z : Fin (m - K) → F, (Finset.univ.filter (fun M : Finset ι => M.card = m ∧ (∀ i : Fin (m - K), ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, (-ev x) = z i))).card ≥ Nat.choose (Fintype.card ι) m / (Fintype.card F) ^ (m - K) := by
              have h_pigeonhole : (Finset.univ.filter (fun M : Finset ι => M.card = m)).card = ∑ z : Fin (m - K) → F, (Finset.univ.filter (fun M : Finset ι => M.card = m ∧ (∀ i : Fin (m - K), ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, (-ev x) = z i))).card := by
                rw [ ← Finset.card_biUnion ];
                · congr with M ; aesop;
                · exact fun x _ y _ hxy => Finset.disjoint_left.mpr fun M hMx hMy => hxy <| funext fun i => by aesop;
              contrapose! h_pigeonhole;
              refine' ne_of_gt ( lt_of_lt_of_le ( Finset.sum_lt_sum_of_nonempty ( Finset.univ_nonempty ) fun z _ => h_pigeonhole z ) _ );
              simp +decide [ Finset.card_univ ];
              exact Nat.mul_div_le _ _;
            -- Let $U$ be the polynomial $X^m + \sum_{j=1}^{m-K} z_j X^{m-j}$ evaluated on $D$.
            set U : ι → F := fun j => Polynomial.eval (ev j) (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)));
            -- For each subset $M$ satisfying the condition, $c_M := U - \Lambda_M|_D$ is the evaluation of a polynomial of degree $\leq K-1$, so $c_M \in RS[F,D,K]$.
            have h_codeword : ∀ M : Finset ι, M.card = m → (∀ i : Fin (m - K), ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, (-ev x) = z i) → (fun j => Polynomial.eval (ev j) (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)) - ∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x)))) ∈ RS ev K := by
              intro M hM hzM
              have h_deg : Polynomial.degree (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)) - ∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x))) < K := by
                have h_deg : Polynomial.degree (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)) - ∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x))) < m := by
                  rw [ Polynomial.degree_lt_iff_coeff_zero ];
                  intro n hn; rcases eq_or_lt_of_le hn with rfl | hn <;> simp_all +decide [ Polynomial.coeff_eq_zero_of_natDegree_lt ] ;
                  · rw [ Finset.prod_congr rfl fun x hx => sub_eq_add_neg _ _ ];
                    rw [ Finset.prod_congr rfl fun x hx => by rw [ ← Polynomial.C_neg ] ];
                    rw [ Finset.prod_X_add_C_coeff ] ; simp +decide [ hM ];
                    · exact Finset.sum_eq_zero fun i hi => if_neg ( Nat.ne_of_gt ( Nat.sub_lt ( by linarith ) ( by linarith ) ) );
                    · linarith;
                  · exact Finset.sum_eq_zero fun i hi => if_neg ( by omega );
                have h_coeff : ∀ i : Fin (m - K), Polynomial.coeff (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)) - ∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x))) (m - (i.val + 1)) = 0 := by
                  intro i
                  have h_coeff : Polynomial.coeff (∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x))) (m - (i.val + 1)) = (-1) ^ (i.val + 1) * ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, ev x := by
                    rw [ Finset.prod_congr rfl fun x hx => sub_eq_add_neg _ _ ];
                    rw [ Finset.prod_congr rfl fun x hx => by rw [ ← Polynomial.C_neg ] ];
                    rw [ Finset.prod_X_add_C_coeff ];
                    · simp +decide [ hM, Nat.sub_sub_self ( show ( i : ℕ ) + 1 ≤ m from by linarith [ Fin.is_lt i, Nat.sub_add_cancel hmK ] ) ];
                      rw [ Finset.mul_sum _ _ _ ] ; exact Finset.sum_congr rfl fun _ _ => by rw [ Finset.prod_congr rfl fun _ _ => neg_eq_neg_one_mul _, Finset.prod_mul_distrib ] ; aesop;
                    · exact hM.symm ▸ Nat.sub_le _ _;
                  have h_coeff : ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, -ev x = (-1) ^ (i.val + 1) * ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, ev x := by
                    rw [ Finset.mul_sum _ _ _ ];
                    exact Finset.sum_congr rfl fun s hs => by rw [ Finset.prod_congr rfl fun _ _ => neg_eq_neg_one_mul _, Finset.prod_mul_distrib ] ; aesop;
                  simp_all +decide [ Polynomial.coeff_X_pow, Finset.sum_ite ];
                  rw [ if_neg ( Nat.ne_of_lt ( Nat.sub_lt ( by linarith ) ( Nat.succ_pos _ ) ) ) ] ; simp +decide [ Finset.sum_filter ] ;
                  rw [ Finset.sum_eq_single i ] <;> simp +contextual [ h_coeff ];
                  exact fun j hj₁ hj₂ => False.elim <| hj₁ <| Fin.ext <| by omega;
                rw [ Polynomial.degree_lt_iff_coeff_zero ] at *;
                intro n hn;
                by_cases hn' : n < m;
                · convert h_coeff ⟨ m - n - 1, _ ⟩ using 1;
                  grind;
                  omega;
                · exact h_deg n ( le_of_not_gt hn' );
              exact mem_RS.mpr ⟨ _, h_deg, fun j => rfl ⟩;
            -- For each subset $M$ satisfying the condition, $U$ agrees with $c_M$ on the $m$ fiber points of $M$, i.e., $hd U c_M \leq n - m$.
            have h_agree : ∀ M : Finset ι, M.card = m → (∀ i : Fin (m - K), ∑ s ∈ M.powersetCard (i.val + 1), ∏ x ∈ s, (-ev x) = z i) → hd U (fun j => Polynomial.eval (ev j) (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)) - ∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x)))) ≤ Fintype.card ι - m := by
              intro M hM hzM
              have h_agree : ∀ j ∈ M, U j = Polynomial.eval (ev j) (Polynomial.X ^ m + ∑ i : Fin (m - K), Polynomial.C (z i) * Polynomial.X ^ (m - (i.val + 1)) - ∏ x ∈ M, (Polynomial.X - Polynomial.C (ev x))) := by
                intro j hj; simp +decide [ U, Finset.prod_eq_prod_diff_singleton_mul hj ] ;
              refine' le_trans ( Finset.card_le_card _ ) _;
              exact Finset.univ \ M;
              · exact fun x hx => Finset.mem_sdiff.mpr ⟨ Finset.mem_univ _, fun hx' => Finset.mem_filter.mp hx |>.2 <| h_agree x hx' ⟩;
              · simp +decide [ Finset.card_sdiff, * ];
            refine' not_lt_of_ge hz ( lt_of_le_of_lt _ ( h_contra U ) );
            refine' le_trans _ ( Finset.card_le_card _ );
            rotate_left;
            exact Finset.image ( fun M : Finset ι => fun j => Polynomial.eval ( ev j ) ( Polynomial.X ^ m + ∑ i : Fin ( m - K ), Polynomial.C ( z i ) * Polynomial.X ^ ( m - ( i.val + 1 ) ) - ∏ x ∈ M, ( Polynomial.X - Polynomial.C ( ev x ) ) ) ) ( Finset.filter ( fun M : Finset ι => M.card = m ∧ ∀ i : Fin ( m - K ), ∑ s ∈ Finset.powersetCard ( i.val + 1 ) M, ∏ x ∈ s, -ev x = z i ) Finset.univ );
            · grind;
            · rw [ Finset.card_image_of_injOn ];
              intro M hM M' hM' h_eq;
              simp_all +decide [ funext_iff, Polynomial.eval_prod ];
              refine' Finset.eq_of_subset_of_card_le ( fun x hx => _ ) _;
              · specialize h_eq x;
                simp_all +decide [ Finset.prod_eq_prod_diff_singleton_mul hx ];
                rw [ eq_comm, Finset.prod_eq_zero_iff ] at h_eq ; simp_all +decide [ sub_eq_iff_eq_add, hev.eq_iff ];
              · linarith

/-! ### Infrastructure for the deep-point conversion (Theorem 3.2)

The following definitions and lemmas develop the Reed–Solomon list-decoding
argument behind Theorem 3.2: the simple-pole functions `poleF`/`poleG`, the
fiber Cauchy–Schwarz inequality, the polynomial root count, the CA-badness of
the simple-pole slopes, an averaging step, and a final arithmetic lemma. -/

/-- The simple-pole numerator function `f_α(x) = U(x)/(x-α)` on the domain. -/
noncomputable def poleF (U ev : ι → F) (α : F) : ι → F := fun j => U j * (ev j - α)⁻¹

/-- The simple-pole function `g_α(x) = -1/(x-α)` on the domain. -/
noncomputable def poleG (ev : ι → F) (α : F) : ι → F := fun j => -(ev j - α)⁻¹

/-
**Fiber Cauchy–Schwarz.** For a finite set `S` and a coloring `f`, the square
of `|S|` is at most the number of colors used times the number of monochromatic
ordered pairs. This is the combinatorial core of the fiber count.
-/
theorem cs_fiber {α₀ γ₀ : Type*} [DecidableEq α₀] [DecidableEq γ₀]
    (S : Finset α₀) (f : α₀ → γ₀) :
    S.card ^ 2 ≤ (S.image f).card *
      ((S ×ˢ S).filter (fun p => f p.1 = f p.2)).card := by
        refine' le_trans _ ( Nat.mul_le_mul_left _ ( Finset.card_le_card _ ) );
        any_goals exact Finset.biUnion ( Finset.image f S ) fun x => Finset.product ( Finset.filter ( fun y => f y = x ) S ) ( Finset.filter ( fun y => f y = x ) S );
        · rw [ sq, Finset.card_biUnion ];
          · simp +decide [ ← sq, Finset.card_product ];
            have h_cauchy_schwarz : ∀ (s : Finset γ₀) (g : γ₀ → ℕ), (∑ x ∈ s, g x) ^ 2 ≤ s.card * ∑ x ∈ s, g x ^ 2 := by
              intros s g; have := Finset.sum_le_sum fun x (hx : x ∈ s) => pow_two_nonneg ( g x - ( ∑ y ∈ s, g y ) / s.card : ℝ ) ; simp_all +decide [ sub_sq, Finset.sum_add_distrib, Finset.mul_sum _ _ _ ] ;
              by_cases hs : s = ∅ <;> simp_all +decide [ ← Finset.mul_sum _ _ _, ← Finset.sum_mul ];
              rw [ ← @Nat.cast_le ℝ ] ; push_cast ; nlinarith [ mul_div_cancel₀ ( ∑ x ∈ s, ( g x : ℝ ) ) ( Nat.cast_ne_zero.mpr <| Finset.card_ne_zero_of_mem <| Classical.choose_spec <| Finset.nonempty_of_ne_empty hs ) ];
            convert h_cauchy_schwarz ( Finset.image f S ) ( fun x => Finset.card ( Finset.filter ( fun y => f y = x ) S ) ) using 1;
            rw [ Finset.card_eq_sum_ones, Finset.sum_image' ] ; aesop;
          · exact fun x hx y hy hxy => Finset.disjoint_left.mpr fun z => by aesop;
        · intro p hp
          aesop

/-
The bad-slope count of any pair is at most `ε_ca · q`.
-/
theorem caBadCount_le_epsCA (C : Submodule F (ι → F)) (r : ℕ) (f1 f2 : ι → F) :
    (caBadCount C r f1 f2 : ℚ) ≤ epsCA C r * (Fintype.card F : ℚ) := by
      unfold epsCA;
      rw [ div_mul_cancel₀ _ ( Nat.cast_ne_zero.mpr Fintype.card_ne_zero ) ];
      exact_mod_cast Finset.le_sup ( f := fun p : ( ι → F ) × ( ι → F ) => caBadCount C r p.1 p.2 ) ( Finset.mem_univ ( f1, f2 ) )

/-
Two distinct polynomials of degree `≤ k` agree on at most `k` points of any
finite set.
-/
omit [Fintype F] in
theorem eval_eq_count_le {k : ℕ} {P Q : Polynomial F} (hPQ : P ≠ Q)
    (hP : P.degree ≤ (k : ℕ)) (hQ : Q.degree ≤ (k : ℕ)) (s : Finset F) :
    (s.filter (fun a => P.eval a = Q.eval a)).card ≤ k := by
      -- Let $Z$ be the set of elements in $s$ where $P$ and $Q$ agree.
      set Z := s.filter (fun a => P.eval a = Q.eval a) with hZ;
      -- Since $P$ and $Q$ are distinct polynomials of degree at most $k$, their difference $D = P - Q$ is a non-zero polynomial of degree at most $k$.
      have hD_nonzero : P - Q ≠ 0 := by
        exact sub_ne_zero_of_ne hPQ
      have hD_deg : (P - Q).degree ≤ k := by
        exact le_trans ( Polynomial.degree_sub_le _ _ ) ( max_le hP hQ );
      exact le_trans ( Finset.card_le_card ( show Z ⊆ ( P - Q |> Polynomial.roots |> Multiset.toFinset ) from fun x hx => by aesop ) ) ( le_trans ( Multiset.toFinset_card_le _ ) ( by exact le_trans ( Polynomial.card_roots' _ ) ( Polynomial.natDegree_le_of_degree_le hD_deg ) ) )

/-
**Column-farness of the simple-pole pair.** For `α ∉ D`, the pair
`(f_α, g_α)` is `r`-far in columns from `RS[F,D,k] × RS[F,D,k]`, because `g_α`
agrees with any degree-`<k` codeword on at most `k` points.
-/
omit [Fintype F] in
theorem poles_colFar {ev : ι → F} (hev : Function.Injective ev) {k r : ℕ}
    (hr : r ≤ Fintype.card ι - k - 1) (hn : k < Fintype.card ι)
    {α : F} (hα : ∀ j, ev j ≠ α) (U : ι → F) :
    colFar (RS ev k) r (poleF U ev α) (poleG ev α) := by
      intro c1 hc1 c2 hc2
      have h_bound : (Finset.univ.filter (fun j => poleG ev α j ≠ c2 j)).card ≥ Fintype.card ι - k := by
        -- By definition of $c2$, there exists a polynomial $G$ of degree less than $k$ such that $c2 j = G.eval (ev j)$ for all $j$.
        obtain ⟨G, hG_deg, hG_eval⟩ : ∃ G : Polynomial F, G.degree < k ∧ ∀ j, c2 j = G.eval (ev j) := by
          rw [ mem_RS ] at hc2 ; tauto;
        -- Consider the polynomial $H(x) = (x - \alpha)G(x) + 1$.
        set H : Polynomial F := (Polynomial.X - Polynomial.C α) * G + 1;
        -- Since $H$ is a polynomial of degree at most $k$, it has at most $k$ roots.
        have hH_roots : (Finset.univ.filter (fun j => H.eval (ev j) = 0)).card ≤ k := by
          have hH_roots : (Finset.image ev (Finset.univ.filter (fun j => H.eval (ev j) = 0))).card ≤ k := by
            have hH_roots : (Finset.image ev (Finset.univ.filter (fun j => H.eval (ev j) = 0))) ⊆ H.roots.toFinset := by
              simp +decide [ Finset.subset_iff ];
              exact fun j hj => ⟨ by exact ne_of_apply_ne ( Polynomial.eval α ) ( by aesop ), hj ⟩;
            refine' le_trans ( Finset.card_le_card hH_roots ) _;
            refine' le_trans ( Multiset.toFinset_card_le _ ) ( le_trans ( Polynomial.card_roots' _ ) _ );
            by_cases hG : G = 0 <;> simp_all +decide;
            · aesop;
            · rw [ Polynomial.natDegree_add_eq_left_of_natDegree_lt ] <;> rw [ Polynomial.natDegree_mul' ] <;> simp +decide [ Polynomial.natDegree_sub_eq_left_of_natDegree_lt, hG ];
              rw [ Polynomial.degree_eq_natDegree hG ] at hG_deg ; norm_cast at hG_deg ; linarith;
          rwa [ Finset.card_image_of_injective _ hev ] at hH_roots;
        simp +zetaDelta at *;
        rw [ show ( Finset.univ.filter fun j => ¬poleG ev α j = c2 j ) = Finset.univ \ Finset.filter ( fun j => ( ev j - α ) * Polynomial.eval ( ev j ) G + 1 = 0 ) Finset.univ from ?_ ];
        · grind;
        · grind +locals;
      exact lt_of_lt_of_le ( by omega ) ( h_bound.trans ( Finset.card_mono fun x hx => by aesop ) )

/-
**Closeness of the simple-pole line word.** If `U` agrees off `≤ r`
coordinates with the evaluation of a polynomial `P` of degree `< k+1`, then the
line word at slope `P(α)` is `r`-close to `RS[F,D,k]` (the witness codeword is the
evaluation of `(P - P(α))/(X-α)`, of degree `< k`).
-/
omit [DecidableEq ι] [Fintype F] in
theorem poles_closeBy {ev : ι → F} {k r : ℕ} (hk : 1 ≤ k)
    {α : F} (hα : ∀ j, ev j ≠ α) {P : Polynomial F} (hP : P.degree < k + 1)
    (U : ι → F) (hagree : hd U (fun j => P.eval (ev j)) ≤ r) :
    closeBy (RS ev k) r (combo (poleF U ev α) (poleG ev α) (P.eval α)) := by
      -- Set c := fun j => Q.eval (ev j). By `mem_RS`, c ∈ RS ev k (witness Q, degree < k).
      obtain ⟨Q, hQ⟩ : ∃ Q : Polynomial F, Q.degree < k ∧ ∀ j, (P.eval (ev j) - P.eval α) = (ev j - α) * Q.eval (ev j) := by
        obtain ⟨Q, hQ⟩ : ∃ Q : Polynomial F, P = Polynomial.C (P.eval α) + (Polynomial.X - Polynomial.C α) * Q := by
          exact ⟨ ( P - Polynomial.C ( P.eval α ) ) /ₘ ( Polynomial.X - Polynomial.C α ), by rw [ Polynomial.mul_divByMonic_eq_iff_isRoot.mpr ( by simp +decide ), add_sub_cancel ] ⟩;
        refine' ⟨ Q, _, _ ⟩;
        · contrapose! hP;
          rw [ hQ, Polynomial.degree_add_eq_right_of_degree_lt ] <;> norm_num [ Polynomial.degree_sub_eq_left_of_degree_lt, hP ];
          · rw [ add_comm ] ; gcongr;
          · exact lt_of_le_of_lt ( Polynomial.degree_C_le ) ( by rw [ Polynomial.degree_eq_natDegree ( by rintro rfl; simp_all +singlePass ) ] at *; norm_cast at *; linarith );
        · intro j; replace hQ := congr_arg ( Polynomial.eval ( ev j ) ) hQ; norm_num at hQ; linear_combination hQ;
      refine' ⟨ fun j => Q.eval ( ev j ), _, _ ⟩ <;> simp_all +decide [ RS ];
      · exact ⟨ Q, Polynomial.mem_degreeLT.mpr hQ.1, rfl ⟩;
      · refine' le_trans _ hagree;
        refine' Finset.card_le_card _;
        grind +locals

/-
**Averaging step.** If for every pair of distinct elements the value maps
agree on at most `k` points of `Ω`, then some `b ∈ Ω` has few monochromatic
ordered off-diagonal pairs.
-/
omit [Field F] [Fintype F] in
theorem exists_low_collision {β₀ : Type*} {δ₀ : Type*} [DecidableEq δ₀]
    (Ω : Finset β₀) (hΩ : Ω.Nonempty) (S : Finset δ₀) (k : ℕ) (g : β₀ → δ₀ → F)
    (hcol : ∀ c ∈ S, ∀ c' ∈ S, c ≠ c' →
      (Ω.filter (fun b => g b c = g b c')).card ≤ k) :
    ∃ b ∈ Ω,
      ((S ×ˢ S).filter (fun p => p.1 ≠ p.2 ∧ g b p.1 = g b p.2)).card * Ω.card
        ≤ k * (S.card * (S.card - 1)) := by
          -- By Fubini's theorem, we can interchange the order of summation.
          have h_fubini : ∑ b ∈ Ω, (Finset.filter (fun p => p.1 ≠ p.2 ∧ g b p.1 = g b p.2) (S ×ˢ S)).card = ∑ p ∈ Finset.filter (fun p => p.1 ≠ p.2) (S ×ˢ S), (Finset.filter (fun b => g b p.1 = g b p.2) Ω).card := by
            simp +decide only [Finset.card_filter];
            rw [ Finset.sum_comm, Finset.sum_filter ];
            exact Finset.sum_congr rfl fun x hx => by split_ifs <;> simp +decide [ * ] ;
          -- By hypothesis, for each pair $(c, c')$ with $c \neq c'$, the number of $b \in \Omega$ such that $g(b, c) = g(b, c')$ is at most $k$.
          have h_bound : ∑ p ∈ Finset.filter (fun p => p.1 ≠ p.2) (S ×ˢ S), (Finset.filter (fun b => g b p.1 = g b p.2) Ω).card ≤ k * (S.card * (S.card - 1)) := by
            refine' le_trans ( Finset.sum_le_sum fun p hp => hcol _ _ _ _ ( Finset.mem_filter.mp hp |>.2 ) ) _;
            · aesop;
            · grind;
            · rw [ show Finset.filter ( fun p : δ₀ × δ₀ => ¬p.1 = p.2 ) ( S ×ˢ S ) = Finset.offDiag S by ext; aesop ] ; simp +decide [ Finset.offDiag_card ] ;
              grind +splitImp;
          contrapose! h_bound;
          rw [ ← h_fubini ];
          refine' lt_of_mul_lt_mul_right _ ( Nat.zero_le Ω.card );
          simpa [ mul_assoc, mul_comm, mul_left_comm, Finset.mul_sum _ _ _ ] using Finset.sum_lt_sum_of_nonempty hΩ h_bound

/-
**Final arithmetic.** The closing inequality of the deep-point conversion.
With `E = ε_ca · q`, `W = q - n`, and the fiber bound `L² ≤ E(L + kL(L-1)/W)`
together with `E·k ≤ η·W`, one gets `L ≤ E/(1-η)`.
-/
theorem final_algebra {L : ℚ} (hL : 0 ≤ L) {W E η : ℚ} {k : ℕ}
    (hW : 0 < W) (hE : 0 ≤ E) (hη0 : 0 < η) (hη1 : η < 1) (hk : 1 ≤ k)
    (hEk : E * (k : ℚ) ≤ η * W)
    (hmain : L ^ 2 ≤ E * (L + (k : ℚ) * L * (L - 1) / W)) :
    L ≤ E / (1 - η) := by
      rw [ le_div_iff₀ ( by linarith ) ];
      field_simp at hmain;
      by_cases hL_pos : 0 < L;
      · nlinarith [ mul_le_mul_of_nonneg_left hEk hL_pos.le, mul_pos hL_pos hW, mul_pos hL_pos hη0, mul_pos hW hη0, mul_le_mul_of_nonneg_left ( show ( k : ℚ ) ≥ 1 by norm_cast ) hL_pos.le, mul_le_mul_of_nonneg_left ( show ( k : ℚ ) ≥ 1 by norm_cast ) hW.le, mul_le_mul_of_nonneg_left ( show ( k : ℚ ) ≥ 1 by norm_cast ) hη0.le ];
      · nlinarith

/-
**Fiber bound (heart of Theorem 3.2).** The Cauchy–Schwarz fiber count for
the list `L = |Lst(RS[F,D,k+1], δ, U)|`: with `E = ε_ca·q` and `W = q - n`,
`L² ≤ E·(L + k·L·(L-1)/W)`. This is the core list-decoding estimate.
-/
theorem deep_fiber_bound {ev : ι → F} (hev : Function.Injective ev) {k r : ℕ}
    (hk : 1 ≤ k) (hn : k < Fintype.card ι) (hqn : Fintype.card ι < Fintype.card F)
    (hr : r ≤ Fintype.card ι - k - 1) (U : ι → F) :
    ((Finset.univ.filter (fun c => c ∈ RS ev (k + 1) ∧ hd U c ≤ r)).card : ℚ) ^ 2
      ≤ (epsCA (RS ev k) r * (Fintype.card F : ℚ)) *
          (((Finset.univ.filter (fun c => c ∈ RS ev (k + 1) ∧ hd U c ≤ r)).card : ℚ)
            + (k : ℚ)
              * ((Finset.univ.filter (fun c => c ∈ RS ev (k + 1) ∧ hd U c ≤ r)).card : ℚ)
              * (((Finset.univ.filter (fun c => c ∈ RS ev (k + 1) ∧ hd U c ≤ r)).card : ℚ) - 1)
              / ((Fintype.card F : ℚ) - (Fintype.card ι : ℚ))) := by
                by_contra h_contra;
                -- Let's define the set Lst and its cardinality L.
                set Lst := Finset.univ.filter (fun c : ι → F => c ∈ RS ev (k + 1) ∧ hd U c ≤ r)
                set L := (Lst.card : ℚ);
                -- Let's define the polynomial Pc and the function g.
                set Pc : (ι → F) → Polynomial F := fun c => if h : c ∈ RS ev (k + 1) then (mem_RS.mp h).choose else 0
                set g : F → (ι → F) → F := fun a c => (Pc c).eval a;
                -- By `exists_low_collision`, we get an α in Ω with a bounded number of monochromatic off-diagonal pairs (col).
                obtain ⟨α, hαmem, hcolb⟩ : ∃ α ∈ Finset.univ \ Finset.image ev Finset.univ, ((Lst ×ˢ Lst).filter (fun p => p.1 ≠ p.2 ∧ g α p.1 = g α p.2)).card * (Finset.card (Finset.univ \ Finset.image ev Finset.univ) : ℚ) ≤ k * (Lst.card * (Lst.card - 1) : ℚ) := by
                  have hcol : ∀ c ∈ Lst, ∀ c' ∈ Lst, c ≠ c' → (Finset.filter (fun a => g a c = g a c') (Finset.univ \ Finset.image ev Finset.univ)).card ≤ k := by
                    intro c hc c' hc' hne
                    have hPc : (Pc c).degree < k + 1 ∧ ∀ j, c j = (Pc c).eval (ev j) := by
                      grind
                    have hPc' : (Pc c').degree < k + 1 ∧ ∀ j, c' j = (Pc c').eval (ev j) := by
                      grind +suggestions
                    have hPc_ne : Pc c ≠ Pc c' := by
                      exact fun h => hne <| funext fun j => by rw [ hPc.2 j, hPc'.2 j, h ] ;
                    have h_root_count : (Finset.filter (fun a => (Pc c).eval a = (Pc c').eval a) (Finset.univ \ Finset.image ev Finset.univ)).card ≤ (Pc c - Pc c').roots.toFinset.card := by
                      refine Finset.card_le_card ?_;
                      simp +contextual [ Finset.subset_iff, sub_eq_zero ];
                      exact fun x hx hx' => hPc_ne;
                    refine' le_trans h_root_count ( le_trans ( Multiset.toFinset_card_le _ ) ( le_trans ( Polynomial.card_roots' _ ) _ ) );
                    have h_deg : Polynomial.degree (Pc c - Pc c') < k + 1 := by
                      exact lt_of_le_of_lt ( Polynomial.degree_sub_le _ _ ) ( max_lt hPc.1 hPc'.1 );
                    exact Nat.le_of_lt_succ ( by rw [ Polynomial.degree_eq_natDegree ( sub_ne_zero.mpr hPc_ne ) ] at h_deg; exact_mod_cast h_deg );
                  have := exists_low_collision ( Finset.univ \ Finset.image ev Finset.univ ) ?_ Lst k g hcol;
                  · rcases this with ⟨ α, hα₁, hα₂ ⟩ ; use α; norm_cast; simp_all +decide [ Finset.card_sdiff, Finset.card_image_of_injective _ hev ] ;
                    lia;
                  · refine' Finset.card_pos.mp _;
                    simp +decide [ Finset.card_sdiff, Finset.card_image_of_injective _ hev, hqn ];
                -- By `cs_fiber`, we have L^2 ≤ (Lst.image (g α)).card * (L + col).
                have hcs : L^2 ≤ (Lst.image (g α)).card * (L + ((Lst ×ˢ Lst).filter (fun p => p.1 ≠ p.2 ∧ g α p.1 = g α p.2)).card : ℚ) := by
                  have hcs : Lst.card ^ 2 ≤ (Lst.image (g α)).card * ((Lst ×ˢ Lst).filter (fun p => g α p.1 = g α p.2)).card := by
                    convert cs_fiber Lst ( g α ) using 1;
                  rw [ show ( Finset.filter ( fun p : ( ι → F ) × ( ι → F ) => g α p.1 = g α p.2 ) ( Lst ×ˢ Lst ) ) = Finset.diag Lst ∪ Finset.filter ( fun p : ( ι → F ) × ( ι → F ) => p.1 ≠ p.2 ∧ g α p.1 = g α p.2 ) ( Lst ×ˢ Lst ) from ?_, Finset.card_union_of_disjoint ] at hcs;
                  · norm_num +zetaDelta at *;
                    exact_mod_cast hcs;
                  · simp +contextual [ Finset.disjoint_left ];
                  · grind;
                -- By `caBadCount_le_epsCA`, we have (Lst.image (g α)).card ≤ epsCA (RS ev k) r * (Fintype.card F).
                have hcard : (Lst.image (g α)).card ≤ epsCA (RS ev k) r * (Fintype.card F : ℚ) := by
                  have hcard : ∀ c ∈ Lst, CAbad (RS ev k) r (poleF U ev α) (poleG ev α) (g α c) := by
                    intro c hc
                    have hPc : (Pc c).degree < k + 1 ∧ ∀ j, c j = (Pc c).eval (ev j) := by
                      grind +splitImp;
                    have hcloseBy : closeBy (RS ev k) r (combo (poleF U ev α) (poleG ev α) (g α c)) := by
                      apply poles_closeBy hk (fun j => by
                        exact fun h => Finset.mem_sdiff.mp hαmem |>.2 ( Finset.mem_image.mpr ⟨ j, Finset.mem_univ _, h ⟩ )) hPc.left U (by
                      convert Finset.mem_filter.mp hc |>.2.2 using 1;
                      exact congr_arg Finset.card ( Finset.filter_congr fun _ _ => by simp +decide [ ← hPc.2 ] ));
                    exact ⟨ hcloseBy, poles_colFar hev hr hn ( fun j => by simpa using Finset.mem_sdiff.mp hαmem |>.2 |> fun h => by simpa using fun h' => h <| Finset.mem_image.mpr ⟨ j, Finset.mem_univ _, h' ⟩ ) U ⟩;
                  have hcard : (Lst.image (g α)).card ≤ (Finset.univ.filter (fun γ => CAbad (RS ev k) r (poleF U ev α) (poleG ev α) γ)).card := by
                    exact Finset.card_le_card fun x hx => by obtain ⟨ c, hc, rfl ⟩ := Finset.mem_image.mp hx; exact Finset.mem_filter.mpr ⟨ Finset.mem_univ _, hcard c hc ⟩ ;
                  refine' le_trans ( Nat.cast_le.mpr hcard ) _;
                  convert caBadCount_le_epsCA ( RS ev k ) r ( poleF U ev α ) ( poleG ev α ) using 1;
                refine' h_contra ( hcs.trans _ );
                gcongr;
                · exact le_trans ( Nat.cast_nonneg _ ) hcard;
                · rw [ le_div_iff₀ ] <;> norm_num [ Finset.card_sdiff, Finset.card_image_of_injective _ hev ] at *;
                  · convert hcolb using 1 ; rw [ Nat.cast_sub hqn.le ];
                    ring!;
                  · exact hqn

/-
**Theorem 3.2 (deep-point conversion).** If the CA error is at most
`η · (1/k)(1 - n/q)`, then every received word has a bounded list in `RS[F,D,k+1]`.
-/
theorem deep_point_conversion {ev : ι → F} (hev : Function.Injective ev) {k r : ℕ}
    (hk : 1 ≤ k) (hn : k < Fintype.card ι) (hqn : Fintype.card ι < Fintype.card F)
    (hr : r ≤ Fintype.card ι - k - 1) (η : ℚ) (hη0 : 0 < η) (hη1 : η < 1)
    (hca : epsCA (RS ev k) r ≤
      η * (1 / (k : ℚ)) * (1 - (Fintype.card ι : ℚ) / (Fintype.card F : ℚ)))
    (U : ι → F) :
    ((Finset.univ.filter (fun c => c ∈ RS ev (k + 1) ∧ hd U c ≤ r)).card : ℚ)
      ≤ (Fintype.card F : ℚ) * epsCA (RS ev k) r / (1 - η) := by
        convert final_algebra _ _ _ _ _ _ _ _ using 1;
        any_goals exact k;
        exact Nat.cast_nonneg _;
        exact ( Fintype.card F : ℚ ) - ( Fintype.card ι : ℚ );
        any_goals linarith;
        · exact sub_pos_of_lt ( Nat.cast_lt.mpr hqn );
        · exact mul_nonneg ( Nat.cast_nonneg _ ) ( div_nonneg ( Nat.cast_nonneg _ ) ( Nat.cast_nonneg _ ) );
        · convert mul_le_mul_of_nonneg_left hca ( show ( 0 : ℚ ) ≤ ( Fintype.card F : ℚ ) * k by positivity ) using 1 ; ring;
          field_simp;
        · convert deep_fiber_bound hev hk hn hqn hr U using 1;
          ring

/-
**Corollary 4.6 (safe to half the distance, modulo one import).** Under the
unique-decoding proximity gap of BCIKS (here supplied as the hypothesis `hca`),
MCA holds up to half the minimum distance with the same error `n/q`.
-/
theorem safe_half_distance {ev : ι → F} {k r : ℕ}
    (hmin : ∀ c ∈ RS ev k, c ≠ 0 → (Fintype.card ι - k + 1) ≤ wt c)
    (h2r : 2 * r ≤ Fintype.card ι - k)
    (hca : epsCA (RS ev k) r ≤ (Fintype.card ι : ℚ) / (Fintype.card F : ℚ)) :
    epsMCA (RS ev k) r ≤ (Fintype.card ι : ℚ) / (Fintype.card F : ℚ) := by
      -- Apply `half_epsMCA_le` with `wmin := Fintype.card ι - k + 1`.
      have h_half : epsMCA (RS ev k) r ≤ max (epsCA (RS ev k) r) ((r : ℚ) / (Fintype.card F : ℚ)) := by
        apply_rules [ half_epsMCA_le ];
      refine' h_half.trans ( max_le hca _ );
      gcongr ; omega

/-! ## Finite certificate anchors

These anchors record small, verifier-backed numerical rows now used by the
experimental certificate ledger.  They deliberately check only finite arithmetic
printed by the certificates; the exhaustive Reed-Solomon semantics remain in the
Python verifiers listed in `CERTIFICATION_MAP.md`.
-/

namespace FiniteAnchors

structure SigmaCRow where
  q : ℕ
  n : ℕ
  k : ℕ
  r : ℕ
  sigma : ℕ
deriving DecidableEq, Repr

structure EmcaRow where
  q : ℕ
  n : ℕ
  k : ℕ
  r : ℕ
  eca : ℕ
  sigma : ℕ
  emca : ℕ
deriving DecidableEq, Repr

def sigma_q763_r2 : SigmaCRow :=
  { q := 7, n := 6, k := 3, r := 2, sigma := 7 }

def sigma_q541_r2 : SigmaCRow :=
  { q := 5, n := 4, k := 1, r := 2, sigma := 3 }

theorem sigma_q763_r2_value : sigma_q763_r2.sigma = 7 := by decide

theorem sigma_q541_r2_value : sigma_q541_r2.sigma = 3 := by decide

def emca_q763_r0 : EmcaRow :=
  { q := 7, n := 6, k := 3, r := 0, eca := 1, sigma := 0, emca := 1 }

def emca_q763_r1 : EmcaRow :=
  { q := 7, n := 6, k := 3, r := 1, eca := 2, sigma := 1, emca := 2 }

def emca_q763_r2 : EmcaRow :=
  { q := 7, n := 6, k := 3, r := 2, eca := 7, sigma := 7, emca := 7 }

theorem emca_q763_sparsify_r0 :
    max emca_q763_r0.eca emca_q763_r0.sigma = emca_q763_r0.emca := by decide

theorem emca_q763_sparsify_r1 :
    max emca_q763_r1.eca emca_q763_r1.sigma = emca_q763_r1.emca := by decide

theorem emca_q763_sparsify_r2 :
    max emca_q763_r2.eca emca_q763_r2.sigma = emca_q763_r2.emca := by decide

theorem identity_prefix_floor_q17_n16_k8 :
    Nat.choose 16 9 = 11440 := by decide

end FiniteAnchors

end TowardsPrize
