import cs25_cap_v12.QuotientRemainder

/-!
# Blueprint: interleaving transfer and explicit witnesses (`lem:inter`, `sec:answers-explicit`)

Skeletons (proofs `sorry`) for two independent parts of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*:

* `lem_inter_eca`, `lem_inter_emca` — **interleaving transfer** (`lem:inter`): for a
  linear code `C`, the `s`-fold interleaved code `C^{≡s}` (here `RSCap.interleave C s`,
  a code over the index type `ι × Fin s`) has CA/MCA error at least that of `C`.  The
  argument is the column-agreement inequality `dist_s(hᐩ, C^{≡s}) ≥ dist(h, C)` with
  equality on diagonal codewords.  (Both proved.)

* `thm_explicit_head_floor_even` / `thm_explicit_head_floor_odd` —
  **explicit head-and-pairs floor** (`thm:explicit-head-floor`): when the quotient
  set `Q = φ(D)` is antipodally symmetric (`−Q = Q`, `0 ∉ Q`), the pigeonhole in the
  fiber lemma is removed: the pure power word `φ^m|_D` (`m` even) resp. the one-head
  word `(φ^m − t·φ^{m−1})|_D` (`m` odd) carries an *explicit* list of
  `C(N/2, m/2)` resp. `C(N/2 − 1, (m−1)/2)` codewords of `RS[F, D, K]`.

* `thm_explicit_pairs` — **explicit certifying pairs up to a pole**
  (`thm:explicit-pairs`): for at least half of the poles `α ∈ F ∖ D`, the explicit
  simple-pole pair `(u/(x−α), −1/(x−α))` has many distinct CA-bad slopes.  Stated here
  in an abstracted counting form.

**Update (skeleton falsity-and-repair packet, 2026-07-18):**
`thm_explicit_head_floor_even` was **false as stated** (the `(φ, c)`-smoothness
hypothesis of the paper was dropped; machine-checked negation
`thm_explicit_head_floor_even_false` over `ZMod 17`) and `thm_explicit_pairs` was
**false as stated** (the paper's size `L₀ = ⌈(q−n)/k⌉` was left a free binder;
machine-checked negation `thm_explicit_pairs_false` over `ZMod 7`).  Both are
statement-repaired below and stay honestly sorried;
`thm_explicit_head_floor_odd` carries the identical smoothness omission (same-class
flag, PLAUSIBLE — no separate counterexample constructed) and receives the same
repair.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
**`lem:inter` (CA form).**  For a linear code `C` and interleaving arity `s ≥ 1`,
the correlated-agreement error of the interleaved code `C^{≡s}` is at least that of
`C`:  `ε_ca(C, δ) ≤ ε_ca(C^{≡s}, δ)`.
-/
theorem lem_inter_eca (C : Set (ι → F)) {s : ℕ} (hs : 1 ≤ s) (δ : ℝ) :
    ecaErr C δ δ ≤ ecaErr (interleave C s) δ δ := by
  refine' Finset.sup'_le _ _ _;
  intro p hp;
  refine' le_trans _ ( Finset.le_sup' _ _ );
  convert prob_mono _;
  rotate_left;
  exact ( fun x => p.1 x.1, fun x => p.2 x.1 );
  · simp +decide;
  · intro γ hγ;
    constructor;
    · obtain ⟨ c, hc₁, hc₂ ⟩ := hγ.1;
      refine' ⟨ fun i => c i.1, _, _ ⟩ <;> simp_all +decide [ interleave ];
      convert hc₂ using 1;
      unfold relDist;
      unfold numDiff; simp +decide [ Fintype.card_prod ] ;
      rw [ show ( Finset.univ.filter fun i : ι × Fin s => ¬p.1 i.1 + γ * p.2 i.1 = c i.1 ) = Finset.univ.filter ( fun i : ι => ¬p.1 i + γ * p.2 i = c i ) ×ˢ Finset.univ from ?_, Finset.card_product ] ; simp +decide [ div_eq_mul_inv, mul_assoc, mul_comm, mul_left_comm, ne_of_gt ( zero_lt_one.trans_le hs ) ];
      ext ⟨ i, j ⟩ ; simp +decide [ Finset.mem_product ] ;
    · rintro ⟨ c1, hc1, c2, hc2, h ⟩;
      -- By definition of `relDist2`, we know that
      have h_relDist2 : (Finset.univ.filter (fun i : ι × Fin s => p.1 i.1 ≠ c1 i ∨ p.2 i.1 ≠ c2 i)).card ≤ δ * (Fintype.card ι * s) := by
        unfold relDist2 at h;
        rw [ div_le_iff₀ ] at h <;> norm_cast at * ; aesop;
        cases isEmpty_or_nonempty ι <;> simp_all +decide;
        · exact hγ.2 ⟨ p.1, by
            convert hγ.1.choose_spec.1, p.2, by
            convert hγ.1.choose_spec.1, by
            unfold relDist2; aesop; ⟩;
        · exact ⟨ Fintype.card_pos, hs ⟩;
      -- By definition of `relDist2`, we know that there exists some `t : Fin s` such that
      obtain ⟨t, ht⟩ : ∃ t : Fin s, (Finset.univ.filter (fun i : ι => p.1 i ≠ c1 (i, t) ∨ p.2 i ≠ c2 (i, t))).card ≤ δ * (Fintype.card ι) := by
        have h_relDist2 : ∑ t : Fin s, (Finset.univ.filter (fun i : ι => p.1 i ≠ c1 (i, t) ∨ p.2 i ≠ c2 (i, t))).card ≤ δ * (Fintype.card ι * s) := by
          convert h_relDist2 using 1;
          simp +decide only [Finset.card_filter];
          rw [ Finset.sum_comm ];
          rw [ ← Finset.sum_product' ];
          rfl;
        contrapose! h_relDist2;
        simpa [ mul_assoc, mul_comm, mul_left_comm, Finset.mul_sum _ _ _ ] using Finset.sum_lt_sum_of_nonempty ⟨ ⟨ 0, hs ⟩, Finset.mem_univ _ ⟩ fun t ht => h_relDist2 t;
      refine' hγ.2 ⟨ fun i => c1 ( i, t ), _, fun i => c2 ( i, t ), _, _ ⟩;
      · exact hc1 t;
      · exact hc2 t;
      · refine' div_le_of_le_mul₀ _ _ _ <;> norm_cast;
        · exact Nat.zero_le _;
        · exact le_of_not_gt fun h => by nlinarith [ show ( Fintype.card ι : ℝ ) > 0 by exact Nat.cast_pos.mpr ( Fintype.card_pos_iff.mpr ⟨ Classical.choose ( Finset.card_pos.mp ( show 0 < Finset.card ( Finset.univ : Finset ι ) from Finset.card_pos.mpr ⟨ Classical.choose ( Finset.card_pos.mp ( show 0 < Finset.card ( Finset.univ : Finset ι ) from by
                                                                                                                                                                                                                                                                                                        exact absurd ‹δ < 0› ( not_lt_of_ge ( le_trans ( by exact div_nonneg ( Nat.cast_nonneg _ ) ( Nat.cast_nonneg _ ) ) ‹relDist2 ( fun x => p.1 x.1 ) ( fun x => p.2 x.1 ) c1 c2 ≤ δ› ) ) ) ), Finset.mem_univ _ ⟩ ) ) ⟩ ) ] ;

/-
**`lem:inter` (MCA form).**  Likewise `ε_mca(C, δ) ≤ ε_mca(C^{≡s}, δ)`.
-/
theorem lem_inter_emca (C : Set (ι → F)) {s : ℕ} (hs : 1 ≤ s) (δ : ℝ) :
    emcaErr C δ ≤ emcaErr (interleave C s) δ := by
  by_contra h_contra;
  obtain ⟨p, hp⟩ : ∃ p : (ι → F) × (ι → F), prob (fun γ => mcaBad C δ p.1 p.2 γ) > emcaErr (interleave C s) δ := by
    contrapose! h_contra;
    exact Finset.sup'_le _ _ fun p _ => h_contra p;
  refine' hp.not_ge ( le_trans _ ( Finset.le_sup' _ _ ) );
  convert prob_mono _;
  rotate_left;
  exact ⟨ fun x => p.1 x.1, fun x => p.2 x.1 ⟩;
  · grind +qlia;
  · rintro γ ⟨ S, hS₁, ⟨ c, hc₁, hc₂ ⟩, hc₃ ⟩;
    refine' ⟨ S ×ˢ Finset.univ, _, _, _ ⟩ <;> simp_all +decide [ Finset.card_product ];
    · nlinarith;
    · exact ⟨ fun p => c p.1, fun t => hc₁, fun a b ha => rfl ⟩;
    · intro x hx y hy;
      contrapose! hc₃;
      exact ⟨ fun i => x ( i, ⟨ 0, hs ⟩ ), hx ⟨ 0, hs ⟩, fun i => y ( i, ⟨ 0, hs ⟩ ), hy ⟨ 0, hs ⟩, fun i hi => hc₃ i hi ⟨ 0, hs ⟩ ⟩

/-- **`thm:explicit-head-floor`(i) — pure power word, `m` even**
(tex `:5333`–`:5351`; statement-repaired).

Let `dom` be `(φ, c)`-smooth over `B` with `N = n/c` even, and suppose the quotient
`Q = φ(D)` is antipodally symmetric with `0 ∉ Q`.  For even `m` with `2 ≤ m ≤ N − 2`
and `c·m ≤ K − 1 + 2c`, the explicit *pure power word* `u = φ^m|_D` carries a list of
at least `C(N/2, m/2)` distinct codewords of `RS[F, D, K]` at radius `1 − cm/n`, with
no pigeonhole and no subfield division.

Statement repair (this packet; falsity class, machine-checked negation
`thm_explicit_head_floor_even_false`): the paper opens "Let `D` be
`(φ, c)`-smooth over `B`" (tex `:5334`) — complete fibers of size `c` are what make
the locator `Λ_M` collect `cm` agreement points — but the skeleton carried **no
smoothness hypothesis at all** (`hcN` only fixes the count `n = cN`).  On a
non-smooth domain the fibers are deficient and even the single-codeword list fails;
see the `ZMod 17` counterexample at the negation lemma.  Repaired with
`hsmooth : DomSmooth dom (fun x => φ.eval x) c`, the same `(φ, c)`-smoothness form
used by `lem_phi_fiber_ii` / `cor_circle_grand`.  A formalization omission, not a
paper defect. -/
theorem thm_explicit_head_floor_even (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {c N K m : ℕ}
    (hc : 0 < c) (hφdeg : φ.natDegree = c) (hcN : c * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) c) (hNeven : Even N)
    (hnegQ : ∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i))
    (h0 : ∀ i, φ.eval (dom i) ≠ 0)
    (hm_even : Even m) (hm_lo : 2 ≤ m) (hm_hi : m ≤ N - 2)
    (hmK : c * m ≤ K - 1 + 2 * c) :
    HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
      (fun i => (φ.eval (dom i)) ^ m) (Nat.choose (N / 2) (m / 2)) := by
  sorry

/-- The `GF(17)` counterexample instance below needs the primality fact as a closed
instance term (a local `haveI` would put a free variable into the `decide` goals). -/
private instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩

private instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩

/-- **The previous `thm_explicit_head_floor_even` skeleton statement was false.**
It dropped the paper's `(φ, c)`-smoothness hypothesis (tex `:5334`), keeping only
the count `c·N = n`.  Counterexample: `F = ZMod 17`, `φ = X²`, `c = 2`, `N = 4`,
`dom = (1, 4, 6, 7, 2, 8, 5, 3)` — the values `φ(D) = (1, 16, 2, 15, 4, 13, 8, 9)`
are pairwise distinct (every `φ`-fiber inside `D` is a *singleton*, so `D` is not
`2`-smooth) yet antipodally symmetric and nonzero, so all stated hypotheses hold
with `m = 2`, `K = 1` (`hmK : 4 ≤ 0 + 4`).  The word `u = φ²|_D` takes each of its
four values exactly twice, so every constant codeword of `RS[F, D, 1]` disagrees
with `u` on at least `6` of the `8` points — relative distance `3/4 > 1/2` — and
even a list of size `1` at radius `1 − 4/8` is unreachable, let alone the claimed
`C(2,1) = 2`.  With complete fibers (the repair) each value would be taken `c·1 = 2`
… `cm = 4` times on a fiber union and the paper's argument runs.  Stated over
`Type` (universe 0), which suffices to refute the universe-polymorphic skeleton. -/
theorem thm_explicit_head_floor_even_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (φ : Polynomial F) (c N K m : ℕ),
          0 < c → φ.natDegree = c → c * N = Fintype.card ι → Even N →
          (∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i)) →
          (∀ i, φ.eval (dom i) ≠ 0) →
          Even m → 2 ≤ m → m ≤ N - 2 →
          c * m ≤ K - 1 + 2 * c →
          HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
            (fun i => (φ.eval (dom i)) ^ m) (Nat.choose (N / 2) (m / 2)) := by
  intro h
  have key := h (Fin 8) (ZMod 17) ![1, 4, 6, 7, 2, 8, 5, 3] (by decide)
    (Polynomial.X ^ 2) 2 4 1 2
    (by norm_num) (Polynomial.natDegree_X_pow 2) (by decide) (by decide)
    (by simp only [Polynomial.eval_pow, Polynomial.eval_X]; decide)
    (by simp only [Polynomial.eval_pow, Polynomial.eval_X]; decide)
    (by decide) (by norm_num) (by decide) (by norm_num)
  rw [show Nat.choose (4 / 2) (2 / 2) = 2 from rfl] at key
  obtain ⟨P, hmem, hinj, hclose⟩ := key
  have hconst := fun x => RSpoly_one_const _ (hmem 0) x 0
  -- the word takes each of its four values exactly twice, so no constant is close
  have hgap : ∀ b : ZMod 17, 4 <
      (Finset.univ.filter
        (fun i : Fin 8 => ((![1, 4, 6, 7, 2, 8, 5, 3] : Fin 8 → ZMod 17) i ^ 2) ^ 2 ≠ b)).card := by
    decide
  have hcl := hclose 0
  rw [relDist] at hcl
  have hnum : (numDiff (fun i => ((Polynomial.X ^ 2 : Polynomial (ZMod 17)).eval
      ((![1, 4, 6, 7, 2, 8, 5, 3] : Fin 8 → ZMod 17) i)) ^ 2) (P 0) : ℝ) ≤ 4 := by
    have hrad : (1 : ℝ) - (((2 : ℕ) : ℝ) * ((2 : ℕ) : ℝ)) / (Fintype.card (Fin 8) : ℝ)
        = 1 / 2 := by
      norm_num [Fintype.card_fin]
    rw [div_le_iff₀ (by norm_num [Fintype.card_fin] : (0 : ℝ) < (Fintype.card (Fin 8) : ℝ))] at hcl
    calc (numDiff _ (P 0) : ℝ)
        ≤ (1 - (((2 : ℕ) : ℝ) * ((2 : ℕ) : ℝ)) / (Fintype.card (Fin 8) : ℝ))
            * (Fintype.card (Fin 8) : ℝ) := hcl
      _ = 4 := by rw [hrad]; norm_num [Fintype.card_fin]
  have hnum' : numDiff (fun i => ((Polynomial.X ^ 2 : Polynomial (ZMod 17)).eval
      ((![1, 4, 6, 7, 2, 8, 5, 3] : Fin 8 → ZMod 17) i)) ^ 2) (P 0) ≤ 4 := by
    exact_mod_cast hnum
  unfold numDiff at hnum'
  -- the decidable constant-disagreement set injects into the numDiff set
  refine absurd (le_trans (Finset.card_le_card ?_) hnum') (not_le.mpr (hgap (P 0 0)))
  intro i hi
  simp only [Finset.mem_filter, Finset.mem_univ, true_and,
    Polynomial.eval_pow, Polynomial.eval_X] at hi ⊢
  rw [hconst i]
  exact hi

/-- **`thm:explicit-head-floor`(ii) — one-head word, `m` odd**
(tex `:5333`–`:5351`; statement-repaired, same-class flag, PLAUSIBLE).

Under the same antipodal hypotheses, for odd `m` and every `t ∈ Q` the explicit
*one-head word* `u = (φ^m − t·φ^{m−1})|_D` carries a list of at least
`C(N/2 − 1, (m−1)/2)` distinct codewords of `RS[F, D, K]` at radius `1 − cm/n`.

Statement repair (this packet): the identical `(φ, c)`-smoothness omission as
`thm_explicit_head_floor_even` (the paper's tex `:5334` hypothesis covers both
clauses).  No separate counterexample was constructed for the odd clause (the even
one needs only `m = 2`; an odd instance needs `m = 3`, hence `N ≥ 6` — same defect
class, larger instance), so per the packet's honesty discipline this is a
same-class **PLAUSIBLE** flag, not a falsity claim.  Same `hsmooth` repair
applied. -/
theorem thm_explicit_head_floor_odd (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {c N K m : ℕ} (t : F)
    (hc : 0 < c) (hφdeg : φ.natDegree = c) (hcN : c * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) c) (hNeven : Even N)
    (hnegQ : ∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i))
    (h0 : ∀ i, φ.eval (dom i) ≠ 0) (ht : ∃ i, φ.eval (dom i) = t)
    (hm_odd : Odd m) (hm_lo : 2 ≤ m) (hm_hi : m ≤ N - 2)
    (hmK : c * m ≤ K - 1 + 2 * c) :
    HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
      (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1))
      (Nat.choose (N / 2 - 1) ((m - 1) / 2)) := by
  sorry

/-- **`thm:explicit-pairs` — explicit certifying pairs, up to the choice of a pole**
(tex `:5369`–`:5399`; statement-repaired).

Given an explicit list of `L₀` distinct polynomials `P : Fin L₀ → F[X]` of degree
`≤ K` all agreeing with a pure power word `u` on at least `A` points of `D` (deep:
`A > K`), with the paper's family size `L₀ ≥ ⌈(q − n)/K⌉`, the explicit simple-pole
pairs `f_α(x) = u(x)/(x − α)`, `g_α(x) = −1/(x − α)` (`α ∈ Ω := F ∖ range dom`)
satisfy: for at least half of the `α ∈ Ω`, the set of distinct CA-bad slopes
`{P_M(α)}` of the pair `(f_α, g_α)` at radius `δ = 1 − A/n` has size at least
`⌈(q − n)/(3K)⌉`.

Here `caBad (RSpoly dom (K+1)) δ δ f_α g_α (P i).eval α` is the paper's CA-badness of
the slope `P_M(α)`.

Statement repair (this packet; falsity class, machine-checked negation
`thm_explicit_pairs_false`): the paper *fixes* `L₀ := ⌈(q−n)/k⌉` (tex `:5370`), and
its Markov + Cauchy–Schwarz count needs the family that large; the skeleton left
`L₀` a free binder, so tiny families (even `L₀ = 1`, whose one-element value set can
never reach `⌈(q−n)/(3K)⌉ ≥ 2`) refuted the count.  Repaired with the lower bound
`hL₀ : ⌈(q − n)/K⌉ ≤ L₀` (the paper's exact choice satisfies it, and the bound
`L₀/(1 + 2K(L₀−1)/(q−n)) ≥ (q−n)/(3K)` survives enlarging `L₀`).  A formalization
omission, not a paper defect. -/
theorem thm_explicit_pairs (dom : ι → F) (hdom : Function.Injective dom)
    {K L₀ A : ℕ} (hdeep : K < A) (hAn : A ≤ Fintype.card ι)
    (hL₀ : ⌈((Fintype.card F : ℝ) - Fintype.card ι) / K⌉ ≤ (L₀ : ℤ))
    (u : Polynomial F) (P : Fin L₀ → Polynomial F)
    (hPdeg : ∀ i, (P i).degree ≤ (K : WithBot ℕ)) (hPinj : Function.Injective P)
    (hagree : ∀ i, A ≤ (Finset.univ.filter (fun x => (P i).eval (dom x) = u.eval (dom x))).card) :
    let Ω : Finset F := Finset.univ.filter (fun α => α ∉ Set.range dom)
    (Ω.filter (fun α =>
        ⌈(Fintype.card F - Fintype.card ι : ℝ) / (3 * K)⌉ ≤
          ((Finset.univ.image (fun i => (P i).eval α)).card : ℤ))).card
      * 2 ≥ Ω.card := by
  sorry

/-- **The previous `thm_explicit_pairs` skeleton statement was false.**  The paper
fixes the family size `L₀ := ⌈(q−n)/k⌉` (tex `:5370`); the skeleton left `L₀` free
with no lower bound, while the conclusion still demanded `⌈(q−n)/(3K)⌉` distinct
values.  Counterexample: `F = ZMod 7`, `ι = Fin 2`, `dom = (0, 1)`, `K = 1`,
`A = 2`, `L₀ = 1`, `u = P₀ = X` (full agreement on both points): for every pole
`α ∈ Ω = {2, …, 6}` the value set `{P₀(α)}` has size `1 < ⌈5/3⌉ = 2`, so the good
set is empty while `|Ω| = 5 > 0`.  A formalization omission, not a paper defect.
Stated over `Type` (universe 0), which suffices to refute the universe-polymorphic
skeleton. -/
theorem thm_explicit_pairs_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (K L₀ A : ℕ), K < A → A ≤ Fintype.card ι →
        ∀ (u : Polynomial F) (P : Fin L₀ → Polynomial F),
          (∀ i, (P i).degree ≤ (K : WithBot ℕ)) → Function.Injective P →
          (∀ i, A ≤ (Finset.univ.filter (fun x => (P i).eval (dom x) = u.eval (dom x))).card) →
          let Ω : Finset F := Finset.univ.filter (fun α => α ∉ Set.range dom)
          (Ω.filter (fun α =>
              ⌈(Fintype.card F - Fintype.card ι : ℝ) / (3 * K)⌉ ≤
                ((Finset.univ.image (fun i => (P i).eval α)).card : ℤ))).card
            * 2 ≥ Ω.card := by
  intro h
  have key := h (Fin 2) (ZMod 7) ![0, 1] (by decide) 1 1 2
    (by norm_num) (by decide) Polynomial.X (fun _ => Polynomial.X)
    (fun _ => Polynomial.degree_X_le) (fun a b _ => Subsingleton.elim a b)
    (fun i => by simp)
  simp only [ge_iff_le] at key
  -- the good-pole filter is empty: a one-element family has value sets of size 1 < ⌈5/3⌉ = 2
  have hceil : ⌈((Fintype.card (ZMod 7) : ℝ) - (Fintype.card (Fin 2) : ℝ))
      / (3 * ((1 : ℕ) : ℝ))⌉ = (2 : ℤ) := by
    rw [ZMod.card, Fintype.card_fin, Int.ceil_eq_iff]
    norm_num
  refine absurd key (not_le.mpr ?_)
  refine lt_of_le_of_lt (Nat.mul_le_mul (Nat.le_of_eq
    (Finset.card_eq_zero.mpr (Finset.filter_eq_empty_iff.mpr fun α _ => ?_))) le_rfl) ?_
  -- every value set of a one-element family has size 1 < ⌈5/3⌉ = 2
  · rw [hceil]
    intro hcon
    -- the classical `DecidableEq` instance below is the one baked into the skeleton
    -- statement (elaborated over an abstract field), so the terms line up
    have h1 : ((@Finset.image (Fin 1) (ZMod 7) (fun a b => propDecidable (a = b))
        (fun i => Polynomial.eval α ((fun _ : Fin 1 => (Polynomial.X : Polynomial (ZMod 7))) i))
        Finset.univ).card : ℤ) ≤ 1 := by
      exact_mod_cast le_trans
        (@Finset.card_image_le _ _ _ _ (fun a b => propDecidable (a = b))) (by simp)
    exact absurd (le_trans hcon h1) (by norm_num)
  -- but Ω is nonempty: 3 is not in the domain
  · simp only [Nat.zero_mul]
    refine Finset.card_pos.mpr ⟨3, ?_⟩
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    rintro ⟨i, hi⟩
    fin_cases i <;> exact absurd hi (by decide)

end RSCap
