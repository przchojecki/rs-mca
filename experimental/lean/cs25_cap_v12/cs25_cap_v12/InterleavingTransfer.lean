import cs25_cap_v12.QuotientRemainder
import cs25_cap_v12.ECFFT

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

**Update (head-floor second-round repair packet, 2026-07-19):** the 2026-07-18
`hsmooth` repair of `thm_explicit_head_floor_even` was **insufficient** — two
further defects survived it, each with a machine-checked negation against the
repaired (post-`hsmooth`) statement.  (D1, `thm_explicit_head_floor_even_char2_false`)
the paper's antipodal-partition consequence "so that `Q` is partitioned into `N/2`
antipodal classes `{y, −y}`" (tex `:5334`) was never formalized: `hnegQ` only
encodes `−Q = Q` and is *trivially* satisfied in characteristic `2` (`y = −y`,
witness `j := i`), where the classes are singletons and the `C(N/2, m/2)` count
collapses — `GaloisField 2 3` counterexample.  (D2,
`thm_explicit_head_floor_even_deg_false`) the paper's *integer* arithmetic
`cm ≤ K − 1 + 2c` (tex `:5334`) excludes `K = 0`, but the skeleton's ℕ-truncated
subtraction admits it, and `RS[F, D, 0] = {0}` cannot carry two distinct
codewords — `ZMod 5` counterexample.  Repaired with `h2 : (2 : F) ≠ 0` and
`hK : 1 ≤ K` on the even clause (the odd clause gets `h2` only: `1 ≤ K` is
derivable there from `m ≥ 3`), and **both repaired statements are now proved**,
constructively, via the ECFFT locator expansion `rational_locator_expansion` at
`f = φ²`, `g = 1`.  Both deployed towers have odd characteristic and `K ≥ 1`, so
they satisfy the repaired hypotheses.  Census `3 → 1` in this module;
`thm_explicit_pairs` (statement-repaired 2026-07-18) is untouched and stays
honestly sorried.
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

First-round statement repair (2026-07-18 packet; falsity class, machine-checked
negation `thm_explicit_head_floor_even_false`): the paper opens "Let `D` be
`(φ, c)`-smooth over `B`" (tex `:5334`) — complete fibers of size `c` are what make
the locator `Λ_M` collect `cm` agreement points — but the skeleton carried **no
smoothness hypothesis at all** (`hcN` only fixes the count `n = cN`).  On a
non-smooth domain the fibers are deficient and even the single-codeword list fails;
see the `ZMod 17` counterexample at the negation lemma.  Repaired with
`hsmooth : DomSmooth dom (fun x => φ.eval x) c`, the same `(φ, c)`-smoothness form
used by `lem_phi_fiber_ii` / `cor_circle_grand`.

Second-round statement repair (this packet; falsity class **twice over**,
machine-checked negations `thm_explicit_head_floor_even_char2_false` and
`thm_explicit_head_floor_even_deg_false`): the first-round packet claimed its
`ZMod 17` instance "isolates the dropped hypothesis exactly" — it did not.  Two
defects survived the `hsmooth` repair.  (D1) the paper's clause "so that `Q` is
partitioned into `N/2` antipodal classes `{y, −y}`" (tex `:5334`) is a *consequence*
of `−Q = Q`, `0 ∉ Q` only in characteristic `≠ 2`; the skeleton's `hnegQ` encodes
`−Q = Q` alone, which is trivially true in characteristic `2` (`j := i`), where the
classes are singletons and both the pairing count and the proof's `e₁`-vanishing
fail.  Repaired with `h2 : (2 : F) ≠ 0`.  (D2) the paper's `cm ≤ K − 1 + 2c`
(tex `:5334`) is integer arithmetic and, at `m = 2`, forces `K ≥ 1`; the skeleton's
ℕ-truncated `K - 1` admits `K = 0`, whose code `RS[F, D, 0] = {0}` cannot carry the
claimed two codewords.  Repaired with `hK : 1 ≤ K`.  Both are formalization
omissions, not paper defects (both deployed towers are odd-characteristic with
`K ≥ 1`).  **Now proved**: the locator `Λ_T = ∏_{r∈T}(φ² − r)` over `(m/2)`-subsets
`T` of the square set `Qsq = {y² : y ∈ Q}` (`|Qsq| = N/2` — squaring is exactly
`2`-to-`1` on `Q` by `h2`) expands as `φ^m + s` with `deg s ≤ c(m−2) ≤ K−1` by
`rational_locator_expansion` at `f = φ²`, `g = 1`, collects the `cm` points of the
`m/2` antipodal fiber pairs, and `T` is recovered from the root set. -/
theorem thm_explicit_head_floor_even (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {c N K m : ℕ}
    (hc : 0 < c) (hφdeg : φ.natDegree = c) (hcN : c * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) c) (hNeven : Even N)
    (h2 : (2 : F) ≠ 0) (hK : 1 ≤ K)
    (hnegQ : ∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i))
    (h0 : ∀ i, φ.eval (dom i) ≠ 0)
    (hm_even : Even m) (hm_lo : 2 ≤ m) (hm_hi : m ≤ N - 2)
    (hmK : c * m ≤ K - 1 + 2 * c) :
    HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
      (fun i => (φ.eval (dom i)) ^ m) (Nat.choose (N / 2) (m / 2)) := by
  classical
  -- numerology
  have hmN : m ≤ N := by omega
  have hn0 : 0 < Fintype.card ι := by
    rw [← hcN]; exact Nat.mul_pos hc (by omega)
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hcmn : c * m ≤ Fintype.card ι := by
    rw [← hcN]; exact Nat.mul_le_mul_left c hmN
  have h2m : 2 * (m / 2) = m := Nat.mul_div_cancel' hm_even.two_dvd
  have hf2deg : (φ ^ 2).natDegree = 2 * c := by
    rw [Polynomial.natDegree_pow, hφdeg]
  -- the smoothness hypothesis, beta-reduced
  have hsm : ∀ i, (Finset.univ.filter (fun j => φ.eval (dom j) = φ.eval (dom i))).card = c :=
    hsmooth
  -- the value set Q = φ(D): complete fibers of size c, |Q| = N
  set Q : Finset F := Finset.univ.image (fun i => φ.eval (dom i)) with hQdef
  have hfiber : ∀ y ∈ Q, (Finset.univ.filter (fun i => φ.eval (dom i) = y)).card = c := by
    intro y hy
    obtain ⟨i₀, -, rfl⟩ := Finset.mem_image.mp hy
    exact hsm i₀
  have hQcard : Q.card = N := by
    have hcount : Fintype.card ι
        = ∑ y ∈ Q, (Finset.univ.filter (fun i => φ.eval (dom i) = y)).card := by
      rw [← Finset.card_univ]
      exact Finset.card_eq_sum_card_image (fun i => φ.eval (dom i)) Finset.univ
    rw [Finset.sum_congr rfl hfiber, Finset.sum_const, smul_eq_mul] at hcount
    have h1 : c * Q.card = c * N := by rw [Nat.mul_comm c Q.card]; omega
    exact Nat.eq_of_mul_eq_mul_left hc h1
  -- Q is antipodally closed, and y ≠ −y on Q (this is where h2 enters)
  have hQneg : ∀ y ∈ Q, -y ∈ Q := by
    intro y hy
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hy
    obtain ⟨j, hj⟩ := hnegQ i
    exact Finset.mem_image.mpr ⟨j, Finset.mem_univ _, hj⟩
  have hQne : ∀ y ∈ Q, y ≠ -y := by
    intro y hy hcon
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hy
    have h2y : (2 : F) * φ.eval (dom i) = 0 := by linear_combination hcon
    rcases mul_eq_zero.mp h2y with hcase | hcase
    · exact h2 hcase
    · exact h0 i hcase
  -- the square set Qsq: squaring is exactly 2-to-1 on Q, so |Qsq| = N/2
  set Qsq : Finset F := Q.image (fun y => y ^ 2) with hQsqdef
  have hQsqcard2 : 2 * Qsq.card = N := by
    have hcount : Q.card = ∑ r ∈ Qsq, (Q.filter (fun y => y ^ 2 = r)).card :=
      Finset.card_eq_sum_card_image (fun y => y ^ 2) Q
    have hinner : ∀ r ∈ Qsq, (Q.filter (fun y => y ^ 2 = r)).card = 2 := by
      intro r hr
      obtain ⟨y₀, hy₀Q, rfl⟩ := Finset.mem_image.mp hr
      have hpair : Q.filter (fun y => y ^ 2 = y₀ ^ 2) = {y₀, -y₀} := by
        ext y
        simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
        constructor
        · rintro ⟨hyQ, hyy⟩
          have hfac : (y - y₀) * (y + y₀) = 0 := by linear_combination hyy
          rcases mul_eq_zero.mp hfac with hcase | hcase
          · exact Or.inl (sub_eq_zero.mp hcase)
          · exact Or.inr (by linear_combination hcase)
        · rintro (rfl | rfl)
          · exact ⟨hy₀Q, rfl⟩
          · exact ⟨hQneg _ hy₀Q, neg_sq y₀⟩
      rw [hpair, Finset.card_insert_of_notMem
        (fun hmem => hQne _ hy₀Q (Finset.mem_singleton.mp hmem)), Finset.card_singleton]
    rw [Finset.sum_congr rfl hinner, Finset.sum_const, smul_eq_mul, hQcard] at hcount
    omega
  have hQsqcard : Qsq.card = N / 2 := by omega
  -- every square value is attained on the domain
  have hwit : ∀ r ∈ Qsq, ∃ i₀, (φ.eval (dom i₀)) ^ 2 = r := by
    intro r hr
    obtain ⟨y₀, hy₀Q, hy₀r⟩ := Finset.mem_image.mp hr
    obtain ⟨i₀, -, hi₀⟩ := Finset.mem_image.mp hy₀Q
    exact ⟨i₀, by rw [hi₀, hy₀r]⟩
  -- locator evaluation: vanishing on the T-fibers, and recovery of T
  have hvanish : ∀ (T : Finset F) (i : ι), (φ.eval (dom i)) ^ 2 ∈ T →
      (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i) = 0 := by
    intro T i hi
    rw [Polynomial.eval_prod]
    refine Finset.prod_eq_zero hi ?_
    simp only [Polynomial.eval_sub, Polynomial.eval_pow, Polynomial.eval_C]
    exact sub_self _
  have hrecover : ∀ (T : Finset F) (i : ι),
      (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i) = 0 → (φ.eval (dom i)) ^ 2 ∈ T := by
    intro T i hzero
    rw [Polynomial.eval_prod, Finset.prod_eq_zero_iff] at hzero
    obtain ⟨r, hrT, hr⟩ := hzero
    simp only [Polynomial.eval_sub, Polynomial.eval_pow, Polynomial.eval_C] at hr
    rw [sub_eq_zero] at hr
    rwa [hr]
  -- degree budget: c(m−2) ≤ K−1 (genuine, since the paper's bound is integer
  -- arithmetic; the products are abstracted for omega)
  have hdegK : c * (m - 2) ≤ K - 1 := by
    have hsub : c * (m - 2) + 2 * c = c * m := by
      obtain ⟨u, rfl⟩ : ∃ u, m = u + 2 := ⟨m - 2, by omega⟩
      rw [Nat.add_sub_cancel]
      ring
    revert hmK hsub
    generalize c * m = A
    generalize c * (m - 2) = B
    intro hmK hsub
    omega
  -- membership: each T-locator produces a codeword of RS[F, D, K]
  have hkey : ∀ T : Finset F, T.card = m / 2 →
      (fun i => (φ.eval (dom i)) ^ m - (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ∈ RSpoly dom K := by
    intro T hTc
    obtain ⟨hdeg, -⟩ := rational_locator_expansion (φ ^ 2) 1 (a := 2 * c) (e := 0)
      (by omega) hf2deg Polynomial.natDegree_one T
    simp only [mul_one, Nat.mul_zero, Nat.add_zero] at hdeg
    rw [hTc] at hdeg
    refine ⟨(φ ^ 2) ^ (m / 2) - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r), ?_, ?_⟩
    · have hrw : (φ ^ 2) ^ (m / 2) - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)
          = Polynomial.C (∑ r ∈ T, r) * (φ ^ 2) ^ (m / 2 - 1)
            - ((∏ r ∈ T, (φ ^ 2 - Polynomial.C r)) - (φ ^ 2) ^ (m / 2)
              + Polynomial.C (∑ r ∈ T, r) * (φ ^ 2) ^ (m / 2 - 1)) := by
        ring
      have hb1 : (Polynomial.C (∑ r ∈ T, r) * (φ ^ 2) ^ (m / 2 - 1)).natDegree
          ≤ c * (m - 2) := by
        refine le_trans Polynomial.natDegree_mul_le ?_
        rw [Polynomial.natDegree_C, Nat.zero_add]
        refine le_trans Polynomial.natDegree_pow_le ?_
        rw [hf2deg]
        have harith : 2 * (m / 2 - 1) ≤ m - 2 := by omega
        calc (m / 2 - 1) * (2 * c) = (2 * (m / 2 - 1)) * c := by ring
          _ ≤ (m - 2) * c := Nat.mul_le_mul_right c harith
          _ = c * (m - 2) := Nat.mul_comm _ _
      have hb2 : ((∏ r ∈ T, (φ ^ 2 - Polynomial.C r)) - (φ ^ 2) ^ (m / 2)
          + Polynomial.C (∑ r ∈ T, r) * (φ ^ 2) ^ (m / 2 - 1)).natDegree
          ≤ c * (m - 2) := by
        refine le_trans hdeg ?_
        have harith : 2 * (m / 2 - 2) ≤ m - 2 := by omega
        calc 2 * c * (m / 2 - 2) = (2 * (m / 2 - 2)) * c := by ring
          _ ≤ (m - 2) * c := Nat.mul_le_mul_right c harith
          _ = c * (m - 2) := Nat.mul_comm _ _
      have hQnat : ((φ ^ 2) ^ (m / 2) - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree
          ≤ K - 1 := by
        rw [hrw]
        exact le_trans (le_trans (Polynomial.natDegree_sub_le _ _) (max_le hb1 hb2)) hdegK
      have hKlt : K - 1 < K := by omega
      exact lt_of_le_of_lt
        (Polynomial.degree_le_natDegree.trans (WithBot.coe_le_coe.mpr hQnat))
        (WithBot.coe_lt_coe.mpr hKlt)
    · intro i
      simp only [Polynomial.eval_sub, Polynomial.eval_pow, ← pow_mul, h2m]
  -- closeness: agreement on the cm fiber points of the m/2 antipodal pairs of T
  have hclose : ∀ T : Finset F, T ⊆ Qsq → T.card = m / 2 →
      relDist (fun i => (φ.eval (dom i)) ^ m)
        (fun i => (φ.eval (dom i)) ^ m - (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ≤ 1 - (c * m : ℝ) / Fintype.card ι := by
    intro T hTQ hTc
    have hfibcard : (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).card
        = c * m := by
      have hinner : ∀ r ∈ T,
          ((Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).filter
            (fun i => (φ.eval (dom i)) ^ 2 = r)).card = 2 * c := by
        intro r hr
        have heqf : (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).filter
            (fun i => (φ.eval (dom i)) ^ 2 = r)
            = Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 = r) := by
          ext i
          simp only [Finset.mem_filter, Finset.mem_univ, true_and]
          exact ⟨fun hcase => hcase.2, fun hcase => ⟨by rw [hcase]; exact hr, hcase⟩⟩
        rw [heqf]
        obtain ⟨y₀, hy₀Q, rfl⟩ := Finset.mem_image.mp (hTQ hr)
        have hdisj : Disjoint (Finset.univ.filter (fun i => φ.eval (dom i) = y₀))
            (Finset.univ.filter (fun i => φ.eval (dom i) = -y₀)) := by
          refine Finset.disjoint_left.mpr ?_
          intro i hi hi'
          simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi hi'
          exact hQne y₀ hy₀Q (hi.symm.trans hi')
        have hsplit : Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 = y₀ ^ 2)
            = (Finset.univ.filter (fun i => φ.eval (dom i) = y₀))
              ∪ (Finset.univ.filter (fun i => φ.eval (dom i) = -y₀)) := by
          ext i
          simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_union]
          constructor
          · intro hcase
            have hfac : (φ.eval (dom i) - y₀) * (φ.eval (dom i) + y₀) = 0 := by
              linear_combination hcase
            rcases mul_eq_zero.mp hfac with hc1 | hc1
            · exact Or.inl (sub_eq_zero.mp hc1)
            · exact Or.inr (by linear_combination hc1)
          · rintro (hcase | hcase)
            · rw [hcase]
            · rw [hcase]; exact neg_sq y₀
        rw [hsplit, Finset.card_union_of_disjoint hdisj,
          hfiber y₀ hy₀Q, hfiber (-y₀) (hQneg y₀ hy₀Q)]
        omega
      calc (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).card
          = ∑ r ∈ T, ((Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).filter
              (fun i => (φ.eval (dom i)) ^ 2 = r)).card :=
            Finset.card_eq_sum_card_fiberwise (fun i hi => (Finset.mem_filter.mp hi).2)
        _ = ∑ _r ∈ T, 2 * c := Finset.sum_congr rfl hinner
        _ = T.card * (2 * c) := by rw [Finset.sum_const, smul_eq_mul]
        _ = c * m := by
            rw [hTc]
            calc (m / 2) * (2 * c) = (2 * (m / 2)) * c := by ring
              _ = m * c := by rw [h2m]
              _ = c * m := Nat.mul_comm _ _
    have hsubd : Finset.univ.filter (fun i =>
          (φ.eval (dom i)) ^ m
            ≠ (φ.eval (dom i)) ^ m - (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ⊆ (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T))ᶜ := by
      intro i hi
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi
      simp only [Finset.mem_compl, Finset.mem_filter, Finset.mem_univ, true_and]
      intro hiT
      exact hi (by rw [hvanish T i hiT]; ring)
    have hnum : numDiff (fun i => (φ.eval (dom i)) ^ m)
        (fun i => (φ.eval (dom i)) ^ m - (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ≤ Fintype.card ι - c * m := by
      calc numDiff _ _
          ≤ ((Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T))ᶜ).card :=
            Finset.card_le_card hsubd
        _ = Fintype.card ι - c * m := by rw [Finset.card_compl, hfibcard]
    rw [relDist, div_le_iff₀ hnR]
    calc (numDiff _ _ : ℝ) ≤ ((Fintype.card ι - c * m : ℕ) : ℝ) := by exact_mod_cast hnum
      _ = (Fintype.card ι : ℝ) - ((c * m : ℕ) : ℝ) := by rw [Nat.cast_sub hcmn]
      _ = (1 - (c * m : ℝ) / Fintype.card ι) * Fintype.card ι := by
          push_cast
          field_simp
  -- locator degrees stay below n = |D|, so equal words force equal locators
  have hΛdeg : ∀ T : Finset F, T.card = m / 2 →
      (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree < Fintype.card ι := by
    intro T hTc
    have hterm : ∀ r ∈ T, (φ ^ 2 - Polynomial.C r).natDegree ≤ 2 * c := by
      intro r _
      refine le_trans (Polynomial.natDegree_sub_le _ _) (max_le (le_of_eq hf2deg) ?_)
      rw [Polynomial.natDegree_C]
      omega
    calc (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree
        ≤ ∑ r ∈ T, (φ ^ 2 - Polynomial.C r).natDegree := Polynomial.natDegree_prod_le _ _
      _ ≤ T.card • (2 * c) := Finset.sum_le_card_nsmul _ _ _ hterm
      _ = (m / 2) * (2 * c) := by rw [smul_eq_mul, hTc]
      _ = (2 * (m / 2)) * c := by ring
      _ = m * c := by rw [h2m]
      _ < N * c := mul_lt_mul_of_pos_right (by omega) hc
      _ = c * N := Nat.mul_comm _ _
      _ = Fintype.card ι := hcN
  -- assembly: enumerate all (m/2)-subsets of Qsq — the count is exact
  set 𝒯 : Finset (Finset F) := Qsq.powersetCard (m / 2) with h𝒯def
  have h𝒯card : 𝒯.card = Nat.choose (N / 2) (m / 2) := by
    rw [h𝒯def, Finset.card_powersetCard, hQsqcard]
  have hmemT : ∀ T ∈ 𝒯, T ⊆ Qsq ∧ T.card = m / 2 := by
    intro T hT
    rw [h𝒯def, Finset.mem_powersetCard] at hT
    exact hT
  set E := 𝒯.equivFinOfCardEq h𝒯card with hEdef
  refine ⟨fun j => (fun i =>
      (φ.eval (dom i)) ^ m
        - (∏ r ∈ ((E.symm j : Finset F)), (φ ^ 2 - Polynomial.C r)).eval (dom i)),
    ?_, ?_, ?_⟩
  · intro j
    exact hkey _ (hmemT _ (E.symm j).2).2
  · intro j j' hjj'
    obtain ⟨hTQ, hTc⟩ := hmemT _ (E.symm j).2
    obtain ⟨hT'Q, hT'c⟩ := hmemT _ (E.symm j').2
    have heq : ∀ i,
        (∏ r ∈ ((E.symm j : Finset F)), (φ ^ 2 - Polynomial.C r)).eval (dom i)
          = (∏ r ∈ ((E.symm j' : Finset F)), (φ ^ 2 - Polynomial.C r)).eval (dom i) := by
      intro i
      have hpt := congrFun hjj' i
      dsimp only at hpt
      exact sub_right_inj.mp hpt
    have hΛeq := eq_of_eval_eq_of_natDegree_lt dom hdom (hΛdeg _ hTc) (hΛdeg _ hT'c) heq
    have hsub : (E.symm j : Finset F) ⊆ (E.symm j' : Finset F) := by
      intro r hrT
      obtain ⟨i₀, hi₀⟩ := hwit r (hTQ hrT)
      have hz : (∏ r' ∈ ((E.symm j : Finset F)),
          (φ ^ 2 - Polynomial.C r')).eval (dom i₀) = 0 :=
        hvanish _ i₀ (by rw [hi₀]; exact hrT)
      rw [hΛeq] at hz
      have hrec := hrecover _ i₀ hz
      rwa [hi₀] at hrec
    have hTeq : (E.symm j : Finset F) = (E.symm j' : Finset F) :=
      Finset.eq_of_subset_of_card_le hsub (by rw [hT'c, hTc])
    exact E.symm.injective (Subtype.ext hTeq)
  · intro j
    obtain ⟨hTQ, hTc⟩ := hmemT _ (E.symm j).2
    exact hclose _ hTQ hTc

/-- The `GF(17)` counterexample instance below needs the primality fact as a closed
instance term (a local `haveI` would put a free variable into the `decide` goals). -/
private instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩

private instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩

private instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩

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

/-- **The first-round (`hsmooth`-repaired) `thm_explicit_head_floor_even` statement
was still false in characteristic `2`.**  The paper's "so that `Q` is partitioned
into `N/2` antipodal classes `{y, −y}`" (tex `:5334`) is a consequence of `−Q = Q`,
`0 ∉ Q` only when `char F ≠ 2`; the skeleton encoded `−Q = Q` alone (`hnegQ`),
which any characteristic-`2` domain satisfies trivially with `j := i`.
Counterexample: `F = GaloisField 2 3` (`GF(8)`), `φ = X`, `c = 1`, `N = 4`, `m = 2`,
`K = 1`, `dom` any four distinct nonzero elements (the `7 ≥ 4` units provide an
embedding; no explicit coordinates are needed, and none are available — `GaloisField`
does not compute, so this proof is `decide`-free on the field).  All repaired
hypotheses hold — `dom` is tautologically `(X, 1)`-smooth and `hnegQ` is trivial —
but squaring is *injective* in characteristic `2` (Frobenius), so the word
`u = φ²|_D` takes `4` distinct values, any constant codeword of `RS[F, D, 1]`
agrees with it on at most `1` of the `4` points, and no codeword lies within the
claimed radius `1 − 2/4 = 1/2` (which allows at most `2` disagreements) — even a
list of size `1` is unreachable, let alone `C(2, 1) = 2`.  This negation targets
the *current* on-main statement (with `hsmooth`), superseding the first-round
packet's claim that its `ZMod 17` instance "isolates the dropped hypothesis
exactly."  Note the instance has `K = 1`, so the `hK`-repair of the second negation
below is independently necessary.  Stated over `Type` (universe 0), which suffices
to refute the universe-polymorphic skeleton. -/
theorem thm_explicit_head_floor_even_char2_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (φ : Polynomial F) (c N K m : ℕ),
          0 < c → φ.natDegree = c → c * N = Fintype.card ι →
          DomSmooth dom (fun x => φ.eval x) c → Even N →
          (∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i)) →
          (∀ i, φ.eval (dom i) ≠ 0) →
          Even m → 2 ≤ m → m ≤ N - 2 →
          c * m ≤ K - 1 + 2 * c →
          HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
            (fun i => (φ.eval (dom i)) ^ m) (Nat.choose (N / 2) (m / 2)) := by
  intro h
  haveI : Fintype (GaloisField 2 3) := Fintype.ofFinite _
  haveI : DecidableEq (GaloisField 2 3) := Classical.decEq _
  -- |GF(8)| = 8, so the unit group has 7 ≥ 4 elements: embed Fin 4 into it
  have hcardF : Fintype.card (GaloisField 2 3) = 8 := by
    have hn := GaloisField.card 2 3 (by norm_num)
    rw [Nat.card_eq_fintype_card] at hn
    norm_num at hn
    exact hn
  have hcardU : Fintype.card (GaloisField 2 3)ˣ = 7 := by
    rw [Fintype.card_units, hcardF]
  obtain ⟨e⟩ : Nonempty (Fin 4 ↪ (GaloisField 2 3)ˣ) :=
    Function.Embedding.nonempty_of_card_le (by rw [Fintype.card_fin, hcardU]; norm_num)
  set dom : Fin 4 → GaloisField 2 3 := fun i => ((e i : (GaloisField 2 3)ˣ) : GaloisField 2 3)
    with hdomdef
  have hdom : Function.Injective dom := fun i j hij => e.injective (Units.ext hij)
  have h0 : ∀ i, (Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i) ≠ 0 := by
    intro i
    rw [Polynomial.eval_X]
    exact Units.ne_zero (e i)
  have hsmooth : DomSmooth dom
      (fun x => (Polynomial.X : Polynomial (GaloisField 2 3)).eval x) 1 := by
    intro i
    rw [Finset.card_eq_one]
    refine ⟨i, ?_⟩
    ext j
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Polynomial.eval_X,
      Finset.mem_singleton]
    exact ⟨fun hj => hdom hj, fun hj => by rw [hj]⟩
  have hnegQ : ∀ i, ∃ j, (Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom j)
      = - (Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i) :=
    fun i => ⟨i, by rw [Polynomial.eval_X, CharTwo.neg_eq]⟩
  have key := h (Fin 4) (GaloisField 2 3) dom hdom Polynomial.X 1 4 1 2
    (by norm_num) Polynomial.natDegree_X (by decide) hsmooth (by decide)
    hnegQ h0 (by decide) (by norm_num) (by norm_num) (by norm_num)
  rw [show Nat.choose (4 / 2) (2 / 2) = 2 from rfl] at key
  obtain ⟨P, hmem, hinj, hclose⟩ := key
  have hconst := fun x => RSpoly_one_const _ (hmem 0) x 0
  -- the radius allows at most 2 disagreements out of 4 …
  have hcl := hclose 0
  rw [relDist, div_le_iff₀
    (by norm_num [Fintype.card_fin] : (0 : ℝ) < (Fintype.card (Fin 4) : ℝ))] at hcl
  have hnum : numDiff
      (fun i => ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2)
      (P 0) ≤ 2 := by
    have hcast : (numDiff
        (fun i => ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2)
        (P 0) : ℝ) ≤ 2 := le_trans hcl (by norm_num [Fintype.card_fin])
    exact_mod_cast hcast
  -- … but char-2 squaring is injective, so the constant z := P 0 0 is hit at most once
  have hagree : (Finset.univ.filter (fun i : Fin 4 =>
      ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2 = P 0 0)).card
      ≤ 1 := by
    refine Finset.card_le_one.mpr ?_
    intro i hi j hj
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Polynomial.eval_X] at hi hj
    refine hdom (CharTwo.sq_injective ?_)
    show dom i ^ 2 = dom j ^ 2
    rw [hi, hj]
  -- so at least 3 of the 4 points disagree with the constant word P 0
  have hsplit := Finset.card_filter_add_card_filter_not
    (s := (Finset.univ : Finset (Fin 4)))
    (fun i => ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2 = P 0 0)
  rw [Finset.card_univ, Fintype.card_fin] at hsplit
  have hge3 : 3 ≤ (Finset.univ.filter (fun i : Fin 4 =>
      ¬ ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2 = P 0 0)).card := by
    omega
  -- the constant-disagreement set injects into the numDiff disagreement set
  have hle : (Finset.univ.filter (fun i : Fin 4 =>
      ¬ ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2 = P 0 0)).card
      ≤ numDiff (fun i => ((Polynomial.X : Polynomial (GaloisField 2 3)).eval (dom i)) ^ 2)
        (P 0) := by
    unfold numDiff
    refine Finset.card_le_card ?_
    intro i hi
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi ⊢
    rw [hconst i]
    exact hi
  have hcontra : (3 : ℕ) ≤ 2 := le_trans hge3 (le_trans hle hnum)
  omega

/-- **The first-round (`hsmooth`-repaired) `thm_explicit_head_floor_even` statement
was also false at `K = 0`, independently of the characteristic.**  The paper's
`cm ≤ K − 1 + 2c` (tex `:5334`) is integer arithmetic: at `c = 1`, `m = 2` it reads
`2 ≤ K + 1`, forcing `K ≥ 1`.  The skeleton's ℕ-truncated subtraction turns it into
`2 ≤ (0 − 1) + 2 = 2` at `K = 0` — satisfied — while `RS[F, D, 0]` demands
`degree < 0`, i.e. the zero polynomial, so the code is `{0}` and cannot carry the
claimed `C(2, 1) = 2` *distinct* codewords.  Counterexample: `F = ZMod 5`
(characteristic `5 ≠ 2`, so the `h2`-repair of the previous negation is
independently necessary), `dom = (1, 2, 3, 4)`, `φ = X`, `c = 1`, `N = 4`, `m = 2`,
`K = 0`; the evaluated hypotheses are checked by `decide`/`norm_num` (`hsmooth` is
tautological at `c = 1` for injective `dom`, proved by the singleton-fiber lemma
route), and injectivity of the list map fails on the two forced-equal zero words —
no agreement analysis is needed at all.  Stated over `Type` (universe 0), which
suffices to refute the universe-polymorphic skeleton. -/
theorem thm_explicit_head_floor_even_deg_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (φ : Polynomial F) (c N K m : ℕ),
          0 < c → φ.natDegree = c → c * N = Fintype.card ι →
          DomSmooth dom (fun x => φ.eval x) c → Even N →
          (∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i)) →
          (∀ i, φ.eval (dom i) ≠ 0) →
          Even m → 2 ≤ m → m ≤ N - 2 →
          c * m ≤ K - 1 + 2 * c →
          HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
            (fun i => (φ.eval (dom i)) ^ m) (Nat.choose (N / 2) (m / 2)) := by
  intro h
  have hdom : Function.Injective (![1, 2, 3, 4] : Fin 4 → ZMod 5) := by decide
  have hsmooth : DomSmooth (![1, 2, 3, 4] : Fin 4 → ZMod 5)
      (fun x => (Polynomial.X : Polynomial (ZMod 5)).eval x) 1 := by
    intro i
    rw [Finset.card_eq_one]
    refine ⟨i, ?_⟩
    ext j
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Polynomial.eval_X,
      Finset.mem_singleton]
    exact ⟨fun hj => hdom hj, fun hj => by rw [hj]⟩
  have key := h (Fin 4) (ZMod 5) ![1, 2, 3, 4] hdom Polynomial.X 1 4 0 2
    (by norm_num) Polynomial.natDegree_X (by decide) hsmooth (by decide)
    (by simp only [Polynomial.eval_X]; decide)
    (by simp only [Polynomial.eval_X]; decide)
    (by decide) (by norm_num) (by norm_num) (by decide)
  rw [show Nat.choose (4 / 2) (2 / 2) = 2 from rfl] at key
  obtain ⟨P, hmem, hinj, -⟩ := key
  -- RS[F, D, 0] contains only the zero word: degree < 0 forces the zero polynomial
  have hzero : ∀ w ∈ RSpoly (![1, 2, 3, 4] : Fin 4 → ZMod 5) 0, ∀ i, w i = 0 := by
    rintro w ⟨Q, hQdeg, hQeval⟩ i
    have hQ0 : Q = 0 := by
      rw [← Polynomial.degree_eq_bot, ← Nat.WithBot.lt_zero_iff]
      exact_mod_cast hQdeg
    rw [hQeval i, hQ0, Polynomial.eval_zero]
  have h01 : P 0 = P 1 := by
    funext i
    rw [hzero _ (hmem 0) i, hzero _ (hmem 1) i]
  exact absurd (hinj h01) (by decide)

/-- **`thm:explicit-head-floor`(ii) — one-head word, `m` odd**
(tex `:5333`–`:5351`; statement-repaired, same-class flag, PLAUSIBLE).

Under the same antipodal hypotheses, for odd `m` and every `t ∈ Q` the explicit
*one-head word* `u = (φ^m − t·φ^{m−1})|_D` carries a list of at least
`C(N/2 − 1, (m−1)/2)` distinct codewords of `RS[F, D, K]` at radius `1 − cm/n`.

First-round statement repair (2026-07-18 packet): the identical `(φ, c)`-smoothness
omission as `thm_explicit_head_floor_even` (the paper's tex `:5334` hypothesis
covers both clauses).  No separate counterexample was constructed for the odd
clause (the even one needs only `m = 2`; an odd instance needs `m = 3`, hence
`N ≥ 6` — same defect class, larger instance), so per the packet's honesty
discipline this was a same-class **PLAUSIBLE** flag, not a falsity claim.  Same
`hsmooth` repair applied.

Second-round statement repair (this packet): the characteristic-`2` gap of
`thm_explicit_head_floor_even_char2_false` (the paper's antipodal-partition clause,
tex `:5334`, covers both clauses) propagates here by the same same-class discipline:
`h2 : (2 : F) ≠ 0` is added as a same-class **PLAUSIBLE** flag — no separate odd
counterexample was constructed (a characteristic-`2` odd instance needs `m = 3`,
`N ≥ 6` over a `GaloisField`, which does not `decide`).  The `K`-truncation repair
is *not* needed here: for odd `m` the constraint `cm ≤ K − 1 + 2c` with `m ≥ 3`
already forces `K ≥ 1` even under ℕ-truncation (at `K = 0` it reads
`3c ≤ cm ≤ 2c`, contradicting `c ≥ 1`), and the proof derives it.  **Now proved**,
by the even clause's argument shifted by one head factor: the locator
`Λ_T = (φ − t)·∏_{r∈T}(φ² − r)` over `((m−1)/2)`-subsets `T` of
`Qsq ∖ {t²}` expands as `φ^m − t·φ^{m−1} + s` with `deg s ≤ c(m−2) ≤ K−1`, collects
the `c` points of the `t`-fiber (disjoint from the pair fibers since `t² ∉ T`) plus
the `c(m−1)` points of the `(m−1)/2` antipodal pairs, and `T` is recovered from the
root set — the `(φ − t)` factor cannot fire on a pair witness since its square is
not `t²`. -/
theorem thm_explicit_head_floor_odd (dom : ι → F) (hdom : Function.Injective dom)
    (φ : Polynomial F) {c N K m : ℕ} (t : F)
    (hc : 0 < c) (hφdeg : φ.natDegree = c) (hcN : c * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) c) (hNeven : Even N)
    (h2 : (2 : F) ≠ 0)
    (hnegQ : ∀ i, ∃ j, φ.eval (dom j) = - φ.eval (dom i))
    (h0 : ∀ i, φ.eval (dom i) ≠ 0) (ht : ∃ i, φ.eval (dom i) = t)
    (hm_odd : Odd m) (hm_lo : 2 ≤ m) (hm_hi : m ≤ N - 2)
    (hmK : c * m ≤ K - 1 + 2 * c) :
    HasList (RSpoly dom K) (1 - (c * m : ℝ) / Fintype.card ι)
      (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1))
      (Nat.choose (N / 2 - 1) ((m - 1) / 2)) := by
  classical
  obtain ⟨k, hmk⟩ := hm_odd
  -- numerology; K ≥ 1 is derivable for odd m (m ≥ 3 gives 3c ≤ cm ≤ K−1+2c)
  have hk1 : 1 ≤ k := by omega
  have hk2 : (m - 1) / 2 = k := by omega
  have hmN : m ≤ N := by omega
  have hn0 : 0 < Fintype.card ι := by
    rw [← hcN]; exact Nat.mul_pos hc (by omega)
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hcmn : c * m ≤ Fintype.card ι := by
    rw [← hcN]; exact Nat.mul_le_mul_left c hmN
  have hf2deg : (φ ^ 2).natDegree = 2 * c := by
    rw [Polynomial.natDegree_pow, hφdeg]
  have hφCdeg : (φ - Polynomial.C t).natDegree ≤ c := by
    refine le_trans (Polynomial.natDegree_sub_le _ _) (max_le (le_of_eq hφdeg) ?_)
    rw [Polynomial.natDegree_C]
    omega
  have h3c : 3 * c ≤ c * m := by
    have h3m : 3 ≤ m := by omega
    calc 3 * c = c * 3 := Nat.mul_comm _ _
      _ ≤ c * m := Nat.mul_le_mul_left c h3m
  have hK : 1 ≤ K := by
    rcases Nat.eq_zero_or_pos K with hK0 | hKpos
    · subst hK0
      revert hmK h3c
      generalize c * m = A
      intro hmK h3c
      omega
    · exact hKpos
  have hdegK : c * (m - 2) ≤ K - 1 := by
    have hsub : c * (m - 2) + 2 * c = c * m := by
      obtain ⟨u, rfl⟩ : ∃ u, m = u + 2 := ⟨m - 2, by omega⟩
      rw [Nat.add_sub_cancel]
      ring
    revert hmK hsub
    generalize c * m = A
    generalize c * (m - 2) = B
    intro hmK hsub
    omega
  -- the smoothness hypothesis, beta-reduced
  have hsm : ∀ i, (Finset.univ.filter (fun j => φ.eval (dom j) = φ.eval (dom i))).card = c :=
    hsmooth
  -- the value set Q = φ(D): complete fibers of size c, |Q| = N
  set Q : Finset F := Finset.univ.image (fun i => φ.eval (dom i)) with hQdef
  have hfiber : ∀ y ∈ Q, (Finset.univ.filter (fun i => φ.eval (dom i) = y)).card = c := by
    intro y hy
    obtain ⟨i₀, -, rfl⟩ := Finset.mem_image.mp hy
    exact hsm i₀
  have hQcard : Q.card = N := by
    have hcount : Fintype.card ι
        = ∑ y ∈ Q, (Finset.univ.filter (fun i => φ.eval (dom i) = y)).card := by
      rw [← Finset.card_univ]
      exact Finset.card_eq_sum_card_image (fun i => φ.eval (dom i)) Finset.univ
    rw [Finset.sum_congr rfl hfiber, Finset.sum_const, smul_eq_mul] at hcount
    have h1 : c * Q.card = c * N := by rw [Nat.mul_comm c Q.card]; omega
    exact Nat.eq_of_mul_eq_mul_left hc h1
  have hQneg : ∀ y ∈ Q, -y ∈ Q := by
    intro y hy
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hy
    obtain ⟨j, hj⟩ := hnegQ i
    exact Finset.mem_image.mpr ⟨j, Finset.mem_univ _, hj⟩
  have hQne : ∀ y ∈ Q, y ≠ -y := by
    intro y hy hcon
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hy
    have h2y : (2 : F) * φ.eval (dom i) = 0 := by linear_combination hcon
    rcases mul_eq_zero.mp h2y with hcase | hcase
    · exact h2 hcase
    · exact h0 i hcase
  -- the square set Qsq with |Qsq| = N/2, and the head class t² ∈ Qsq
  set Qsq : Finset F := Q.image (fun y => y ^ 2) with hQsqdef
  have hQsqcard2 : 2 * Qsq.card = N := by
    have hcount : Q.card = ∑ r ∈ Qsq, (Q.filter (fun y => y ^ 2 = r)).card :=
      Finset.card_eq_sum_card_image (fun y => y ^ 2) Q
    have hinner : ∀ r ∈ Qsq, (Q.filter (fun y => y ^ 2 = r)).card = 2 := by
      intro r hr
      obtain ⟨y₀, hy₀Q, rfl⟩ := Finset.mem_image.mp hr
      have hpair : Q.filter (fun y => y ^ 2 = y₀ ^ 2) = {y₀, -y₀} := by
        ext y
        simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
        constructor
        · rintro ⟨hyQ, hyy⟩
          have hfac : (y - y₀) * (y + y₀) = 0 := by linear_combination hyy
          rcases mul_eq_zero.mp hfac with hcase | hcase
          · exact Or.inl (sub_eq_zero.mp hcase)
          · exact Or.inr (by linear_combination hcase)
        · rintro (rfl | rfl)
          · exact ⟨hy₀Q, rfl⟩
          · exact ⟨hQneg _ hy₀Q, neg_sq y₀⟩
      rw [hpair, Finset.card_insert_of_notMem
        (fun hmem => hQne _ hy₀Q (Finset.mem_singleton.mp hmem)), Finset.card_singleton]
    rw [Finset.sum_congr rfl hinner, Finset.sum_const, smul_eq_mul, hQcard] at hcount
    omega
  have hQsqcard : Qsq.card = N / 2 := by omega
  obtain ⟨it, hit⟩ := ht
  have htQ : t ∈ Q := Finset.mem_image.mpr ⟨it, Finset.mem_univ _, hit⟩
  have ht2Qsq : t ^ 2 ∈ Qsq := Finset.mem_image.mpr ⟨t, htQ, rfl⟩
  have hQsqecard : (Qsq.erase (t ^ 2)).card = N / 2 - 1 := by
    rw [Finset.card_erase_of_mem ht2Qsq, hQsqcard]
  have hwit : ∀ r ∈ Qsq, ∃ i₀, (φ.eval (dom i₀)) ^ 2 = r := by
    intro r hr
    obtain ⟨y₀, hy₀Q, hy₀r⟩ := Finset.mem_image.mp hr
    obtain ⟨i₀, -, hi₀⟩ := Finset.mem_image.mp hy₀Q
    exact ⟨i₀, by rw [hi₀, hy₀r]⟩
  have hvanish : ∀ (T : Finset F) (i : ι), (φ.eval (dom i)) ^ 2 ∈ T →
      (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i) = 0 := by
    intro T i hi
    rw [Polynomial.eval_prod]
    refine Finset.prod_eq_zero hi ?_
    simp only [Polynomial.eval_sub, Polynomial.eval_pow, Polynomial.eval_C]
    exact sub_self _
  have hrecover : ∀ (T : Finset F) (i : ι),
      (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i) = 0 → (φ.eval (dom i)) ^ 2 ∈ T := by
    intro T i hzero
    rw [Polynomial.eval_prod, Finset.prod_eq_zero_iff] at hzero
    obtain ⟨r, hrT, hr⟩ := hzero
    simp only [Polynomial.eval_sub, Polynomial.eval_pow, Polynomial.eval_C] at hr
    rw [sub_eq_zero] at hr
    rwa [hr]
  -- membership: each one-head locator produces a codeword of RS[F, D, K]
  have hkey : ∀ T : Finset F, T.card = k →
      (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1)
        - ((φ - Polynomial.C t) * ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ∈ RSpoly dom K := by
    intro T hTc
    obtain ⟨hdeg, -⟩ := rational_locator_expansion (φ ^ 2) 1 (a := 2 * c) (e := 0)
      (by omega) hf2deg Polynomial.natDegree_one T
    simp only [mul_one, Nat.mul_zero, Nat.add_zero] at hdeg
    rw [hTc] at hdeg
    refine ⟨(φ - Polynomial.C t) * ((φ ^ 2) ^ k - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)),
      ?_, ?_⟩
    · have hinner : ((φ ^ 2) ^ k - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree
          ≤ 2 * c * (k - 1) := by
        have hrw : (φ ^ 2) ^ k - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)
            = Polynomial.C (∑ r ∈ T, r) * (φ ^ 2) ^ (k - 1)
              - ((∏ r ∈ T, (φ ^ 2 - Polynomial.C r)) - (φ ^ 2) ^ k
                + Polynomial.C (∑ r ∈ T, r) * (φ ^ 2) ^ (k - 1)) := by
          ring
        rw [hrw]
        refine le_trans (Polynomial.natDegree_sub_le _ _) (max_le ?_ ?_)
        · refine le_trans Polynomial.natDegree_mul_le ?_
          rw [Polynomial.natDegree_C, Nat.zero_add]
          refine le_trans Polynomial.natDegree_pow_le ?_
          rw [hf2deg]
          exact le_of_eq (by ring)
        · exact le_trans hdeg (Nat.mul_le_mul_left (2 * c) (by omega))
      have hQnat : ((φ - Polynomial.C t)
          * ((φ ^ 2) ^ k - ∏ r ∈ T, (φ ^ 2 - Polynomial.C r))).natDegree ≤ K - 1 := by
        refine le_trans Polynomial.natDegree_mul_le ?_
        refine le_trans (Nat.add_le_add hφCdeg hinner) ?_
        refine le_trans ?_ hdegK
        have hm2 : m - 2 = 2 * (k - 1) + 1 := by omega
        rw [hm2]
        obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
        rw [Nat.add_sub_cancel]
        exact le_of_eq (by ring)
      have hKlt : K - 1 < K := by omega
      exact lt_of_le_of_lt
        (Polynomial.degree_le_natDegree.trans (WithBot.coe_le_coe.mpr hQnat))
        (WithBot.coe_lt_coe.mpr hKlt)
    · intro i
      have hm1 : m - 1 = 2 * k := by omega
      simp only [Polynomial.eval_mul, Polynomial.eval_sub, Polynomial.eval_pow,
        Polynomial.eval_C]
      rw [hm1, hmk]
      ring
  -- closeness: the t-fiber (c points) plus the T-pair fibers (2c each) give cm
  have hclose : ∀ T : Finset F, T ⊆ Qsq.erase (t ^ 2) → T.card = k →
      relDist (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1))
        (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1)
          - ((φ - Polynomial.C t) * ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ≤ 1 - (c * m : ℝ) / Fintype.card ι := by
    intro T hTE hTc
    have hTQsq : T ⊆ Qsq := fun r hr => Finset.mem_of_mem_erase (hTE hr)
    have hfibT : (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).card
        = k * (2 * c) := by
      have hinner : ∀ r ∈ T,
          ((Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).filter
            (fun i => (φ.eval (dom i)) ^ 2 = r)).card = 2 * c := by
        intro r hr
        have heqf : (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).filter
            (fun i => (φ.eval (dom i)) ^ 2 = r)
            = Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 = r) := by
          ext i
          simp only [Finset.mem_filter, Finset.mem_univ, true_and]
          exact ⟨fun hcase => hcase.2, fun hcase => ⟨by rw [hcase]; exact hr, hcase⟩⟩
        rw [heqf]
        obtain ⟨y₀, hy₀Q, rfl⟩ := Finset.mem_image.mp (hTQsq hr)
        have hdisj : Disjoint (Finset.univ.filter (fun i => φ.eval (dom i) = y₀))
            (Finset.univ.filter (fun i => φ.eval (dom i) = -y₀)) := by
          refine Finset.disjoint_left.mpr ?_
          intro i hi hi'
          simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi hi'
          exact hQne y₀ hy₀Q (hi.symm.trans hi')
        have hsplit : Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 = y₀ ^ 2)
            = (Finset.univ.filter (fun i => φ.eval (dom i) = y₀))
              ∪ (Finset.univ.filter (fun i => φ.eval (dom i) = -y₀)) := by
          ext i
          simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_union]
          constructor
          · intro hcase
            have hfac : (φ.eval (dom i) - y₀) * (φ.eval (dom i) + y₀) = 0 := by
              linear_combination hcase
            rcases mul_eq_zero.mp hfac with hc1 | hc1
            · exact Or.inl (sub_eq_zero.mp hc1)
            · exact Or.inr (by linear_combination hc1)
          · rintro (hcase | hcase)
            · rw [hcase]
            · rw [hcase]; exact neg_sq y₀
        rw [hsplit, Finset.card_union_of_disjoint hdisj,
          hfiber y₀ hy₀Q, hfiber (-y₀) (hQneg y₀ hy₀Q)]
        omega
      calc (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).card
          = ∑ r ∈ T, ((Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)).filter
              (fun i => (φ.eval (dom i)) ^ 2 = r)).card :=
            Finset.card_eq_sum_card_fiberwise (fun i hi => (Finset.mem_filter.mp hi).2)
        _ = ∑ _r ∈ T, 2 * c := Finset.sum_congr rfl hinner
        _ = T.card * (2 * c) := by rw [Finset.sum_const, smul_eq_mul]
        _ = k * (2 * c) := by rw [hTc]
    have hdisjtT : Disjoint (Finset.univ.filter (fun i => φ.eval (dom i) = t))
        (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)) := by
      refine Finset.disjoint_left.mpr ?_
      intro i hi hi'
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi hi'
      rw [hi] at hi'
      exact (Finset.mem_erase.mp (hTE hi')).1 rfl
    have hfibcard : (Finset.univ.filter (fun i => φ.eval (dom i) = t
        ∨ (φ.eval (dom i)) ^ 2 ∈ T)).card = c * m := by
      have hsplit : Finset.univ.filter (fun i => φ.eval (dom i) = t
            ∨ (φ.eval (dom i)) ^ 2 ∈ T)
          = (Finset.univ.filter (fun i => φ.eval (dom i) = t))
            ∪ (Finset.univ.filter (fun i => (φ.eval (dom i)) ^ 2 ∈ T)) := by
        ext i
        simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_union]
      rw [hsplit, Finset.card_union_of_disjoint hdisjtT, hfiber t htQ, hfibT]
      calc c + k * (2 * c) = c * (2 * k + 1) := by ring
        _ = c * m := by rw [← hmk]
    have hvanishU : ∀ i, (φ.eval (dom i) = t ∨ (φ.eval (dom i)) ^ 2 ∈ T) →
        ((φ - Polynomial.C t) * ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i) = 0 := by
      intro i hi
      rw [Polynomial.eval_mul]
      rcases hi with hi | hi
      · rw [Polynomial.eval_sub, Polynomial.eval_C, hi, sub_self, zero_mul]
      · rw [hvanish T i hi, mul_zero]
    have hsubd : Finset.univ.filter (fun i =>
          (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1)
            ≠ (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1)
              - ((φ - Polynomial.C t) * ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ⊆ (Finset.univ.filter (fun i => φ.eval (dom i) = t
            ∨ (φ.eval (dom i)) ^ 2 ∈ T))ᶜ := by
      intro i hi
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hi
      simp only [Finset.mem_compl, Finset.mem_filter, Finset.mem_univ, true_and]
      intro hiT
      exact hi (by rw [hvanishU i hiT]; ring)
    have hnum : numDiff
        (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1))
        (fun i => (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1)
          - ((φ - Polynomial.C t) * ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).eval (dom i))
        ≤ Fintype.card ι - c * m := by
      calc numDiff _ _
          ≤ ((Finset.univ.filter (fun i => φ.eval (dom i) = t
              ∨ (φ.eval (dom i)) ^ 2 ∈ T))ᶜ).card :=
            Finset.card_le_card hsubd
        _ = Fintype.card ι - c * m := by rw [Finset.card_compl, hfibcard]
    rw [relDist, div_le_iff₀ hnR]
    calc (numDiff _ _ : ℝ) ≤ ((Fintype.card ι - c * m : ℕ) : ℝ) := by exact_mod_cast hnum
      _ = (Fintype.card ι : ℝ) - ((c * m : ℕ) : ℝ) := by rw [Nat.cast_sub hcmn]
      _ = (1 - (c * m : ℝ) / Fintype.card ι) * Fintype.card ι := by
          push_cast
          field_simp
  -- locator degrees stay below n
  have hΛdeg : ∀ T : Finset F, T.card = k →
      ((φ - Polynomial.C t) * ∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree
        < Fintype.card ι := by
    intro T hTc
    have hterm : ∀ r ∈ T, (φ ^ 2 - Polynomial.C r).natDegree ≤ 2 * c := by
      intro r _
      refine le_trans (Polynomial.natDegree_sub_le _ _) (max_le (le_of_eq hf2deg) ?_)
      rw [Polynomial.natDegree_C]
      omega
    have hprod : (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree ≤ k * (2 * c) := by
      calc (∏ r ∈ T, (φ ^ 2 - Polynomial.C r)).natDegree
          ≤ ∑ r ∈ T, (φ ^ 2 - Polynomial.C r).natDegree := Polynomial.natDegree_prod_le _ _
        _ ≤ T.card • (2 * c) := Finset.sum_le_card_nsmul _ _ _ hterm
        _ = k * (2 * c) := by rw [smul_eq_mul, hTc]
    refine lt_of_le_of_lt
      (le_trans Polynomial.natDegree_mul_le (Nat.add_le_add hφCdeg hprod)) ?_
    have heq : c + k * (2 * c) = c * m := by
      calc c + k * (2 * c) = c * (2 * k + 1) := by ring
        _ = c * m := by rw [← hmk]
    rw [heq, ← hcN]
    exact mul_lt_mul_of_pos_left (by omega) hc
  -- assembly: enumerate all k-subsets of Qsq ∖ {t²} — the count is exact
  set 𝒯 : Finset (Finset F) := (Qsq.erase (t ^ 2)).powersetCard k with h𝒯def
  have h𝒯card : 𝒯.card = Nat.choose (N / 2 - 1) ((m - 1) / 2) := by
    rw [h𝒯def, Finset.card_powersetCard, hQsqecard, hk2]
  have hmemT : ∀ T ∈ 𝒯, T ⊆ Qsq.erase (t ^ 2) ∧ T.card = k := by
    intro T hT
    rw [h𝒯def, Finset.mem_powersetCard] at hT
    exact hT
  set E := 𝒯.equivFinOfCardEq h𝒯card with hEdef
  refine ⟨fun j => (fun i =>
      (φ.eval (dom i)) ^ m - t * (φ.eval (dom i)) ^ (m - 1)
        - ((φ - Polynomial.C t)
            * ∏ r ∈ ((E.symm j : Finset F)), (φ ^ 2 - Polynomial.C r)).eval (dom i)),
    ?_, ?_, ?_⟩
  · intro j
    exact hkey _ (hmemT _ (E.symm j).2).2
  · intro j j' hjj'
    obtain ⟨hTE, hTc⟩ := hmemT _ (E.symm j).2
    obtain ⟨hT'E, hT'c⟩ := hmemT _ (E.symm j').2
    have heq : ∀ i,
        ((φ - Polynomial.C t)
            * ∏ r ∈ ((E.symm j : Finset F)), (φ ^ 2 - Polynomial.C r)).eval (dom i)
          = ((φ - Polynomial.C t)
              * ∏ r ∈ ((E.symm j' : Finset F)), (φ ^ 2 - Polynomial.C r)).eval (dom i) := by
      intro i
      have hpt := congrFun hjj' i
      dsimp only at hpt
      exact sub_right_inj.mp hpt
    have hΛeq := eq_of_eval_eq_of_natDegree_lt dom hdom (hΛdeg _ hTc) (hΛdeg _ hT'c) heq
    have hsub : (E.symm j : Finset F) ⊆ (E.symm j' : Finset F) := by
      intro r hrT
      obtain ⟨hrne, hrQsq⟩ := Finset.mem_erase.mp (hTE hrT)
      obtain ⟨i₀, hi₀⟩ := hwit r hrQsq
      have hz : ((φ - Polynomial.C t)
          * ∏ r' ∈ ((E.symm j : Finset F)), (φ ^ 2 - Polynomial.C r')).eval (dom i₀)
          = 0 := by
        rw [Polynomial.eval_mul, hvanish _ i₀ (by rw [hi₀]; exact hrT), mul_zero]
      rw [hΛeq, Polynomial.eval_mul, mul_eq_zero] at hz
      rcases hz with hz | hz
      · exfalso
        rw [Polynomial.eval_sub, Polynomial.eval_C, sub_eq_zero] at hz
        exact hrne (by rw [← hi₀, hz])
      · have hrec := hrecover _ i₀ hz
        rwa [hi₀] at hrec
    have hTeq : (E.symm j : Finset F) = (E.symm j' : Finset F) :=
      Finset.eq_of_subset_of_card_le hsub (by rw [hT'c, hTc])
    exact E.symm.injective (Subtype.ext hTeq)
  · intro j
    obtain ⟨hTE, hTc⟩ := hmemT _ (E.symm j).2
    exact hclose _ hTE hTc

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
