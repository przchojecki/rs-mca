import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: quotient-profile floors with remainder supports (`sec:quotient-remainder`)

Skeletons (proofs `sorry`) for the quotient-remainder / heaviest-prefix floor results of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

These floors extend the fiber lemma below the multiplicative grid: given a divisor
`c ∣ n` (with quotient order `N = n/c`) and an agreement value `A₀ = mc + s`, a
prefix-selected received word carries a list whose size is the *quotient-remainder
count* `M_{c,m,s} = C(N, m)·C(n − mc, s)` divided by a certificate weight
`|B|^{w_c(s, A₀−K)}`.

**Update (skeleton falsity-and-repair packet, 2026-07-18):** the two prefix-floor
skeletons were **false as stated** — the certificate weight `wₒ` was universally
quantified (so `wₒ = 0` demanded a pigeonhole-free list of the full count), and the
heaviest-prefix count `H` was likewise a universally quantified input instead of the
construction's output.  Machine-checked negations over `ZMod 17` are
`lem_quotient_remainder_prefix_false` / `lem_heaviest_prefix_locator_floor_false`;
the repaired statements below tie the weight to the paper's `w_c(s, σ)`
(`RSCap.certWeight`) and existentially quantify the heaviest-prefix data.  The same
packet **discharges** `cor_quantitative_first_grid_floor` (via the explicit
`x^{k+1}` witness list `RSCap.hasList_first_grid`, the `c = 1` clause of
`cor:augmented-slack-one`) and proves the `c = 1` clause of the first-grid cap as
`RSCap.cor_first_grid_cap_one`; the general `cor_first_grid_cap` (with the `c > 1`
smooth-coset route) stays honestly sorried.

Formalized here:

* `qrCount` — the count `M_{c,m,s} = C(N, m)·C(n − mc, s)`.
* `certWeight` — the paper's prefix weight `w_c(s, σ)`.
* `lem_quotient_remainder_prefix` — `lem:quotient-remainder-prefix`: the list-mass floor
  `|Lst(RS[F,D,K], 1 − A₀/n, U)| ≥ ⌈M_{c,m,s}/|B|^{w_c(s,A₀−K)}⌉` (statement-repaired).
* `lem_heaviest_prefix_locator_floor` — `lem:heaviest-prefix-locator-floor`: the sharper
  heaviest-prefix count `H_{c,m,s}^K`, dominating the coarse certificate bound
  (statement-repaired; `I`/`H` abstract the prefix-image size and heaviest fiber).
* `thm_quotient_remainder_deep_floor` — `thm:quotient-remainder-deep-floor`: the
  resulting deep-band error floor `ε_ca(C, δ) ≥ 𝓔_{q,k}(L)` (proved).
* `cor_quotient_remainder_trigger` — `cor:quotient-remainder-trigger` (proved).
* `hasList_first_grid` — the explicit `x^{k+1}` witness list of
  `cor:augmented-slack-one` at `c = 1` (proved).
* `cor_quantitative_first_grid_floor` — `cor:quantitative-first-grid-floor`: the
  unconditional first-grid floor `ε_ca(C, δ) ≥ 𝓔_{q,k}(C(n, k+1))` for any `n`-point
  domain (proved).
* `cor_first_grid_cap_one` — `cor:first-grid-cap`, `c = 1` clause, both `ε_ca` and
  `ε_mca` (proved).
* `cor_first_grid_cap` — `cor:first-grid-cap`, general `c` (skeleton; the `c > 1`
  clause needs the multiplicative-coset fiber route and stays sorried).
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The quotient-remainder count `M_{c,m,s} = C(N, m)·C(n − mc, s)`. -/
def qrCount (N n c m s : ℕ) : ℕ := Nat.choose N m * Nat.choose (n - m * c) s

/-- The paper's prefix weight `w_c(s, σ) = #{h : 1 ≤ h ≤ σ, h mod c ∈ {0, 1, …, s}}`
(`sec:quotient-remainder`, display before `lem:quotient-remainder-prefix`,
tex `:720`–`:733`; there `w_c(0, σ) = ⌊σ/c⌋` for full-fiber supports).  This is the
certificate weight of the quotient-remainder locator-prefix construction: the number
of high-degree prefix slots that the pigeonhole must pay for. -/
def certWeight (c s σ : ℕ) : ℕ :=
  ((Finset.Icc 1 σ).filter (fun h => h % c ≤ s)).card

omit [Fintype ι] [Fintype F] in
/-- A codeword of `RSpoly dom 1` (degree `< 1`) is a constant word.  Used by the
statement-falsity certificates below, which refute skeletons by counting the
constants. -/
theorem RSpoly_one_const (dom : ι → F) {c : ι → F}
    (hc : c ∈ RSpoly dom 1) (i j : ι) : c i = c j := by
  obtain ⟨Q, hQ, hev⟩ := hc
  have hQC : Q = Polynomial.C (Q.coeff 0) :=
    Polynomial.eq_C_of_degree_le_zero (by
      exact_mod_cast Nat.WithBot.lt_one_iff_le_zero.mp hQ)
  rw [hev i, hev j, hQC, Polynomial.eval_C, Polynomial.eval_C]

/-- A decoding list of `RSpoly dom 1` (a code with at most `|F|` words — the
constants) has size at most `|F|`.  This is the pigeonhole that refutes the
pre-repair prefix-floor skeletons. -/
theorem hasList_const_le_card [Nonempty ι] (dom : ι → F) {δ : ℝ} {U : ι → F} {L : ℕ}
    (h : HasList (RSpoly dom 1) δ U L) : L ≤ Fintype.card F := by
  obtain ⟨P, hmem, hinj, -⟩ := h
  obtain ⟨i₀⟩ := ‹Nonempty ι›
  have hval : Function.Injective (fun t : Fin L => P t i₀) := by
    intro a b hab
    refine hinj (funext fun x => ?_)
    rw [RSpoly_one_const dom (hmem a) x i₀, RSpoly_one_const dom (hmem b) x i₀]
    exact hab
  simpa using Fintype.card_le_of_injective _ hval

/-- **`lem:quotient-remainder-prefix` — quotient-remainder prefix floor**
(tex `:734`–`:755`; statement-repaired).

Let `B ⊆ F`, let `dom` be an injective `B`-valued multiplicative coset domain of order
`n`, let `K < n`, `c ∣ n`, `N = n/c`, and `A₀ = mc + s` with `0 ≤ s < c`, `0 ≤ m ≤ N`,
`A₀ ≥ K` (and `mc + s ≤ n` if `s > 0`).  Then there is a `B`-valued received word `U`
carrying a list of at least `⌈M_{c,m,s}/|B|^{w_c(s,A₀−K)}⌉` distinct codewords of
`RS[F, D, K]` at radius `1 − A₀/n`.

Statement repair (this packet; falsity class, machine-checked negation
`lem_quotient_remainder_prefix_false`): the previous skeleton universally quantified
the certificate weight `wₒ`, so the instance `wₒ = 0` demanded a list of the **full**
count `M_{c,m,s}` with no pigeonhole loss — refuted over `GF(17)` where
`M_{2,4,0} = C(8,4) = 70` exceeds the `17` codewords of `RS[F, D, 1]`.  The paper
fixes the weight to `w_c(s, A₀−K)` (`lem:quotient-remainder-prefix`, tex `:752`:
denominator `|B|^{w_c(s,σ)}`, `σ = A₀ − K`); the defect was a formalization
quantifier inversion, not a paper defect.  Repaired with `wₒ := certWeight c s (A₀ − K)`. -/
theorem lem_quotient_remainder_prefix (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {c N K m s A₀ : ℕ} (hc : 0 < c) (hcn : c ∣ Fintype.card ι)
    (hN : c * N = Fintype.card ι) (hsmooth : DomSmooth dom (fun x => x ^ c) c)
    (hK : K < Fintype.card ι) (hs : s < c) (hm : m ≤ N)
    (hA₀ : A₀ = m * c + s) (hA₀K : K ≤ A₀) (hA₀n : A₀ ≤ Fintype.card ι) :
    ∃ (U : ι → F) (_ : ∀ i, U i ∈ B) (L : ℕ),
      (qrCount N (Fintype.card ι) c m s : ℝ)
          / (Fintype.card B : ℝ) ^ certWeight c s (A₀ - K) ≤ (L : ℝ) ∧
      HasList (RSpoly dom K) (1 - (A₀ : ℝ) / Fintype.card ι) U L := by
  sorry

/-- The `GF(17)` counterexample instances below need the primality fact as a closed
instance term (a local `haveI` would put a free variable into the `decide` goals). -/
private instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩

/-- **The previous `lem_quotient_remainder_prefix` skeleton statement was false.**
The certificate weight `wₒ` was an implicit universally quantified binder appearing
only in the denominator `|B|^{wₒ}`; at `wₒ = 0` the skeleton demanded a received word
carrying `M_{c,m,s}` distinct codewords with no pigeonhole loss.  Counterexample:
`F = ZMod 17`, `dom` the 16 units enumerated by powers of the primitive root `3`
(so squaring is `2`-to-`1` and `DomSmooth` holds), `B = ⊤`, `c = 2`, `N = 8`,
`K = 1`, `m = 4`, `s = 0`, `A₀ = 8`, `wₒ = 0`: the bound demands `L ≥ C(8,4) = 70`,
but `RS[F, D, 1]` is the constants, of which there are only `17`.  The paper is not
affected: `lem:quotient-remainder-prefix` (tex `:752`) fixes the denominator to
`|B|^{w_c(s,σ)}` with `σ = A₀ − K` (here `w_2(0,7) = 3`, giving the true floor
`⌈70/17³⌉ = 1`), so the defect was a formalization quantifier inversion.  Stated
over `Type` (universe 0), which suffices to refute the universe-polymorphic
skeleton. -/
theorem lem_quotient_remainder_prefix_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (B : Subfield F) [Fintype B], (∀ i, dom i ∈ B) →
        ∀ (c N K m s A₀ wₒ : ℕ), 0 < c → c ∣ Fintype.card ι →
          c * N = Fintype.card ι → DomSmooth dom (fun x => x ^ c) c →
          K < Fintype.card ι → s < c → m ≤ N →
          A₀ = m * c + s → K ≤ A₀ → A₀ ≤ Fintype.card ι →
          ∃ (U : ι → F) (_ : ∀ i, U i ∈ B) (L : ℕ),
            (qrCount N (Fintype.card ι) c m s : ℝ) / (Fintype.card B : ℝ) ^ wₒ ≤ (L : ℝ) ∧
            HasList (RSpoly dom K) (1 - (A₀ : ℝ) / Fintype.card ι) U L := by
  intro h
  have key := h (Fin 16) (ZMod 17)
    ![1, 3, 9, 10, 13, 5, 15, 11, 16, 14, 8, 7, 4, 12, 2, 6] (by decide)
    ⊤ (fun _ => Subfield.mem_top _) 2 8 1 4 0 8 0
    (by norm_num) (by decide) (by decide)
    (by unfold DomSmooth; intro i; rw [Finset.filter_congr_decidable]; revert i; decide)
    (by decide) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by decide)
  obtain ⟨U, -, L, hL, hHas⟩ := key
  have hq70 : qrCount 8 (Fintype.card (Fin 16)) 2 4 0 = 70 := by decide
  rw [hq70, pow_zero, div_one] at hL
  have hL70 : 70 ≤ L := by exact_mod_cast hL
  have hle := hasList_const_le_card _ hHas
  rw [ZMod.card] at hle
  omega

/-- **`lem:heaviest-prefix-locator-floor` — heaviest-prefix locator floor**
(tex `:841`–`:860`; statement-repaired).

Under the hypotheses of `lem_quotient_remainder_prefix`, the construction produces a
`B`-valued received word whose list is at least the heaviest-prefix count
`H = H_{c,m,s}^K`: there is a prefix-image size `I = I_{c,m,s}^K` with
`0 < I ≤ |B|^{w_c(s,A₀−K)}` and `H ≥ M_{c,m,s}/I`, and the word carries a list of
`H` distinct codewords (`def:prefix-fiber-certificate`, tex `:806`–`:838`:
`H ≥ ⌈M/I⌉ ≥ ⌈M/|B|^{w}⌉`).  The abstract pair `(I, H)` stands for the prefix-image
size and the heaviest prefix fiber; the chain of inequalities of the paper's
statement is recovered by dividing.

Statement repair (this packet; falsity class, machine-checked negation
`lem_heaviest_prefix_locator_floor_false`): the previous skeleton universally
quantified `H` subject only to the *lower* bound `M/|B|^{wₒ} ≤ H` (with `wₒ` also
universal), i.e. the constraint was inverted — any huge `H` above the coarse bound
was demanded as a list size.  The paper's `H` is the **output** heaviest-fiber count
(tex `:841`–`:860`); the repaired statement existentially quantifies the certified
pair `(I, H)`. -/
theorem lem_heaviest_prefix_locator_floor (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {c N K m s A₀ : ℕ} (hc : 0 < c) (hcn : c ∣ Fintype.card ι)
    (hN : c * N = Fintype.card ι) (hsmooth : DomSmooth dom (fun x => x ^ c) c)
    (hK : K < Fintype.card ι) (hs : s < c) (hm : m ≤ N)
    (hA₀ : A₀ = m * c + s) (hA₀K : K ≤ A₀) (hA₀n : A₀ ≤ Fintype.card ι) :
    ∃ (U : ι → F) (_ : ∀ i, U i ∈ B) (I H : ℕ),
      0 < I ∧ I ≤ Fintype.card B ^ certWeight c s (A₀ - K) ∧
      (qrCount N (Fintype.card ι) c m s : ℝ) / (I : ℝ) ≤ (H : ℝ) ∧
      HasList (RSpoly dom K) (1 - (A₀ : ℝ) / Fintype.card ι) U H := by
  sorry

/-- **The previous `lem_heaviest_prefix_locator_floor` skeleton statement was
false.**  `H` was a universally quantified binder constrained only from *below*
(`hHbound : M_{c,m,s}/|B|^{wₒ} ≤ H`, with `wₒ` also universal), yet the conclusion
demanded a decoding list of size `H`.  Counterexample: the same `ZMod 17` instance
as `lem_quotient_remainder_prefix_false` with `wₒ = 0` and `H = 70`
(`hHbound : 70/1 ≤ 70` holds), while `RS[F, D, 1]` has only `17` codewords.  The
paper's `H_{c,m,s}^K` is the heaviest prefix fiber produced by the construction
(tex `:806`–`:860`), not an arbitrary number above the coarse bound; the defect was
a formalization quantifier inversion, not a paper defect. -/
theorem lem_heaviest_prefix_locator_floor_false :
    ¬ ∀ (ι F : Type) [Fintype ι] [Field F] [Fintype F]
        (dom : ι → F), Function.Injective dom →
        ∀ (B : Subfield F) [Fintype B], (∀ i, dom i ∈ B) →
        ∀ (c N K m s A₀ H wₒ : ℕ), 0 < c → c ∣ Fintype.card ι →
          c * N = Fintype.card ι → DomSmooth dom (fun x => x ^ c) c →
          K < Fintype.card ι → s < c → m ≤ N →
          A₀ = m * c + s → K ≤ A₀ → A₀ ≤ Fintype.card ι →
          (qrCount N (Fintype.card ι) c m s : ℝ) / (Fintype.card B : ℝ) ^ wₒ ≤ (H : ℝ) →
          ∃ (U : ι → F) (_ : ∀ i, U i ∈ B),
            HasList (RSpoly dom K) (1 - (A₀ : ℝ) / Fintype.card ι) U H := by
  intro h
  have hq70 : qrCount 8 (Fintype.card (Fin 16)) 2 4 0 = 70 := by decide
  have key := h (Fin 16) (ZMod 17)
    ![1, 3, 9, 10, 13, 5, 15, 11, 16, 14, 8, 7, 4, 12, 2, 6] (by decide)
    ⊤ (fun _ => Subfield.mem_top _) 2 8 1 4 0 8 70 0
    (by norm_num) (by decide) (by decide)
    (by unfold DomSmooth; intro i; rw [Finset.filter_congr_decidable]; revert i; decide)
    (by decide) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by decide)
    (by rw [hq70, pow_zero, div_one])
  obtain ⟨U, -, hHas⟩ := key
  have hle := hasList_const_le_card _ hHas
  rw [ZMod.card] at hle
  omega

/-
**`thm:quotient-remainder-deep-floor` — deep-band quotient-remainder error floor.**

If a `B`-valued received word carries a list of `L ≥ 1` distinct degree-`< k+1`
codewords at agreement `A ∈ {k+1, …, n}` (deep), then the correlated-agreement error of
`C = RS[F, D, k]` is bounded below by the deep-list floor `𝓔_{q,k}(L)` at every radius
`δ ∈ [1 − A/n, 1 − k/n)`.  This is `thm:quotient-remainder-deep-floor` in the form that
combines the prefix floors above with Theorem A.
-/
theorem thm_quotient_remainder_deep_floor (dom : ι → F) (hdom : Function.Injective dom)
    {k A L : ℕ} (hk : 0 < k) (hL : 1 ≤ L) (hAlo : k < A) (hAn : A ≤ Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (U : ι → F) (hlist : HasList (RSpoly dom (k + 1)) (1 - (A : ℝ) / Fintype.card ι) U L)
    (δ : ℝ) (hδlo : 1 - (A : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k L ≤ ecaErr (RSpoly dom k) δ δ := by
  obtain ⟨ P, hP₁, hP₂, hP₃ ⟩ := hlist;
  -- For each `i`, membership `P i ∈ RSpoly dom (k+1)` gives (by `Classical.choice`) a polynomial `Q i : Polynomial F` with `(Q i).degree < ((k+1 : ℕ) : WithBot ℕ)` and `∀ x, P i x = (Q i).eval (dom x)`; hence `(Q i).degree ≤ (k : WithBot ℕ)` (since `degree < k+1` means `degree ≤ k`).
  obtain ⟨Q, hQ⟩ : ∃ Q : Fin L → Polynomial F, (∀ i, (Q i).degree ≤ (k : WithBot ℕ)) ∧ (∀ i x, P i x = (Q i).eval (dom x)) := by
    choose Q hQ₁ hQ₂ using hP₁;
    refine' ⟨ Q, _, _ ⟩ <;> simp_all +decide [ Polynomial.degree_le_iff_coeff_zero ];
    exact fun i m hm => Polynomial.coeff_eq_zero_of_degree_lt <| lt_of_lt_of_le ( hQ₁ i ) <| WithBot.coe_le_coe.mpr hm;
  apply RSCap.ecaFloor_le_ecaErr_deep_list hL dom hdom δ U Q;
  · exact hQ.1;
  · intro i j hij h; have := @hP₂ i j; simp_all +decide [ funext_iff ] ;
  · intro i
    specialize hP₃ i
    simp [relDist] at hP₃;
    rw [ div_le_iff₀ ( Nat.cast_pos.mpr <| Fintype.card_pos_iff.mpr ⟨ Classical.choose <| Finset.card_pos.mp <| show 0 < Fintype.card ι from by linarith ⟩ ) ] at hP₃;
    convert hP₃.trans ( mul_le_mul_of_nonneg_right hδlo <| Nat.cast_nonneg _ ) using 1;
    exact congr_arg _ ( congr_arg _ ( by ext; simp +decide [ hQ.2 i ] ; tauto ) );
  · nlinarith [ show ( k : ℝ ) + 1 ≤ A by norm_cast, show ( A : ℝ ) ≤ Fintype.card ι by norm_cast, div_mul_cancel₀ ( A : ℝ ) ( show ( Fintype.card ι : ℝ ) ≠ 0 by norm_cast; linarith ), div_mul_cancel₀ ( k : ℝ ) ( show ( Fintype.card ι : ℝ ) ≠ 0 by norm_cast; linarith ) ];
  · exact_mod_cast hq

/-
**`cor:quotient-remainder-trigger` — trigger for the quotient-remainder floor.**

If the quotient-remainder list size exceeds `(q − n)/k`, then the correlated-agreement
error of `C = RS[F, D, k]` exceeds the half-inverse-dimension threshold throughout the
deep band `δ ∈ [1 − A/n, 1 − k/n)`.
-/
theorem cor_quotient_remainder_trigger (dom : ι → F) (hdom : Function.Injective dom)
    {k A L : ℕ} (hk : 0 < k) (hAlo : k < A) (hAn : A ≤ Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (U : ι → F) (hlist : HasList (RSpoly dom (k + 1)) (1 - (A : ℝ) / Fintype.card ι) U L)
    (htrig : ((Fintype.card F : ℝ) - Fintype.card ι) / k < L)
    (δ : ℝ) (hδlo : 1 - (A : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k) δ δ := by
  refine' lt_of_lt_of_le _ ( RSCap.thm_quotient_remainder_deep_floor dom hdom hk _ hAlo hAn hq U hlist δ hδlo hδhi );
  · convert RSCap.ecaFloor_trigger _ _ _ _ |>.2 htrig using 1;
    · field_simp;
    · exact Nat.cast_pos.mpr ( Fintype.card_pos );
    · exact_mod_cast hq;
    · positivity;
    · exact lt_of_le_of_lt ( div_nonneg ( sub_nonneg.2 hq.le ) ( Nat.cast_nonneg _ ) ) htrig;
  · exact Nat.one_le_iff_ne_zero.mpr ( by rintro rfl; norm_num at htrig; exact absurd htrig ( by exact not_lt_of_ge ( div_nonneg ( sub_nonneg.mpr hq.le ) ( Nat.cast_nonneg _ ) ) ) )

omit [Fintype F] in
/-- **`cor:augmented-slack-one`, `c = 1` clause (tex `:1063`–`:1078`) — the universal
first-grid list.**  On any injective `n`-point domain, the explicit monomial word
`u = x^{k+1}|_D` carries `C(n, k+1)` distinct codewords of `RS[F, D, k+1]` at radius
`1 − (k+1)/n`: for each `(k+1)`-subset `S ⊆ D`, the codeword `c_S = u − Λ_S|_D`
(with `Λ_S = ∏_{s∈S}(X − s)` the monic locator) has degree `≤ k` and agrees with `u`
on `S`; distinct `S` give distinct `c_S` because the difference of two monic
degree-`(k+1)` locators has degree `≤ k < n` yet would vanish on all of `D`.  No
smoothness and no subfield structure is used ("the `c=1` statement in fact holds for
any set `D ⊆ B` of `n` distinct points", tex `:1076`–`:1078`). -/
theorem hasList_first_grid (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hkn : k < Fintype.card ι) :
    HasList (RSpoly dom (k + 1)) (1 - ((k + 1 : ℕ) : ℝ) / Fintype.card ι)
      (fun i => dom i ^ (k + 1)) (Nat.choose (Fintype.card ι) (k + 1)) := by
  classical
  have hn0 : 0 < Fintype.card ι := lt_of_le_of_lt (Nat.zero_le _) hkn
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hk1n : k + 1 ≤ Fintype.card ι := hkn
  -- the family of (k+1)-subsets and its enumeration
  have hcard : (Finset.univ.powersetCard (k + 1) : Finset (Finset ι)).card
      = Nat.choose (Fintype.card ι) (k + 1) := by
    rw [Finset.card_powersetCard, Finset.card_univ]
  let E : Fin (Nat.choose (Fintype.card ι) (k + 1))
      ≃ (Finset.univ.powersetCard (k + 1) : Finset (Finset ι)) :=
    (finCongr hcard.symm).trans (Finset.univ.powersetCard (k + 1)).equivFin.symm
  -- locators and codewords
  let Λ : Finset ι → Polynomial F := fun S => ∏ s ∈ S, (Polynomial.X - Polynomial.C (dom s))
  have hΛmonic : ∀ S : Finset ι, (Λ S).Monic := fun S =>
    Polynomial.monic_prod_of_monic _ _ (fun s _ => Polynomial.monic_X_sub_C (dom s))
  have hΛdeg : ∀ S : Finset ι, S.card = k + 1 → (Λ S).natDegree = k + 1 := by
    intro S hS
    have hne : ∀ s ∈ S, (Polynomial.X - Polynomial.C (dom s)) ≠ 0 :=
      fun s _ => Polynomial.X_sub_C_ne_zero (dom s)
    rw [show Λ S = ∏ s ∈ S, (Polynomial.X - Polynomial.C (dom s)) from rfl,
      Polynomial.natDegree_prod _ _ hne]
    simp [hS]
  have hΛzero : ∀ (S : Finset ι) (i : ι), i ∈ S → (Λ S).eval (dom i) = 0 := by
    intro S i hi
    rw [show Λ S = ∏ s ∈ S, (Polynomial.X - Polynomial.C (dom s)) from rfl,
      Polynomial.eval_prod]
    exact Finset.prod_eq_zero hi (by simp)
  let cw : Finset ι → (ι → F) := fun S i => dom i ^ (k + 1) - (Λ S).eval (dom i)
  -- membership: the difference of two monic degree-(k+1) polynomials has degree ≤ k
  have hcwmem : ∀ S : Finset ι, S.card = k + 1 → cw S ∈ RSpoly dom (k + 1) := by
    intro S hS
    refine ⟨Polynomial.X ^ (k + 1) - Λ S, ?_, fun i => by simp [cw]⟩
    have hd : (Polynomial.X ^ (k + 1) : Polynomial F).degree = (Λ S).degree := by
      rw [Polynomial.degree_X_pow, Polynomial.degree_eq_natDegree (hΛmonic S).ne_zero,
        hΛdeg S hS]
    have hlc : (Polynomial.X ^ (k + 1) : Polynomial F).leadingCoeff
        = (Λ S).leadingCoeff := by
      rw [(Polynomial.monic_X_pow (k + 1)).leadingCoeff, (hΛmonic S).leadingCoeff]
    have hlt := Polynomial.degree_sub_lt hd
      (pow_ne_zero _ Polynomial.X_ne_zero) hlc
    rwa [Polynomial.degree_X_pow] at hlt
  -- closeness: agreement on the k+1 points of S
  have hclose : ∀ S : Finset ι, S.card = k + 1 →
      relDist (fun i => dom i ^ (k + 1)) (cw S)
        ≤ 1 - ((k + 1 : ℕ) : ℝ) / Fintype.card ι := by
    intro S hS
    have hsub : Finset.univ.filter (fun i => dom i ^ (k + 1) ≠ cw S i) ⊆ Sᶜ := by
      intro i hi
      rw [Finset.mem_filter] at hi
      rw [Finset.mem_compl]
      intro hiS
      exact hi.2 (by simp [cw, hΛzero S i hiS])
    have hnum : numDiff (fun i => dom i ^ (k + 1)) (cw S) ≤ Fintype.card ι - (k + 1) := by
      calc numDiff (fun i => dom i ^ (k + 1)) (cw S) ≤ Sᶜ.card :=
            Finset.card_le_card hsub
        _ = Fintype.card ι - (k + 1) := by rw [Finset.card_compl, hS]
    rw [relDist, div_le_iff₀ hnR]
    calc (numDiff (fun i => dom i ^ (k + 1)) (cw S) : ℝ)
        ≤ ((Fintype.card ι - (k + 1) : ℕ) : ℝ) := by exact_mod_cast hnum
      _ = (Fintype.card ι : ℝ) - ((k + 1 : ℕ) : ℝ) := by
          rw [Nat.cast_sub hk1n]
      _ = (1 - ((k + 1 : ℕ) : ℝ) / Fintype.card ι) * Fintype.card ι := by
          field_simp
  -- injectivity: equal codewords force equal locators, hence equal subsets
  have hcwinj : ∀ S S' : Finset ι, S.card = k + 1 → S'.card = k + 1 →
      cw S = cw S' → S = S' := by
    intro S S' hS hS' hEq
    have heval : ∀ i, (Λ S).eval (dom i) = (Λ S').eval (dom i) := by
      intro i
      have h := congrFun hEq i
      simp only [cw] at h
      exact sub_right_inj.mp h
    have hzero : Λ S - Λ S' = 0 := by
      by_contra hne
      have hd : (Λ S).degree = (Λ S').degree := by
        rw [Polynomial.degree_eq_natDegree (hΛmonic S).ne_zero,
          Polynomial.degree_eq_natDegree (hΛmonic S').ne_zero, hΛdeg S hS, hΛdeg S' hS']
      have hdlt := Polynomial.degree_sub_lt hd (hΛmonic S).ne_zero
        (by rw [(hΛmonic S).leadingCoeff, (hΛmonic S').leadingCoeff])
      rw [Polynomial.degree_eq_natDegree (hΛmonic S).ne_zero, hΛdeg S hS] at hdlt
      have hnd : (Λ S - Λ S').natDegree < k + 1 :=
        (Polynomial.natDegree_lt_iff_degree_lt hne).mpr hdlt
      have hsubroots : Finset.univ.image dom ⊆ (Λ S - Λ S').roots.toFinset := by
        intro x hx
        obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hx
        rw [Multiset.mem_toFinset, Polynomial.mem_roots hne]
        simp [Polynomial.IsRoot, heval i]
      have hn_le : Fintype.card ι ≤ (Λ S - Λ S').natDegree := by
        calc Fintype.card ι = (Finset.univ.image dom).card := by
              rw [Finset.card_image_of_injective _ hdom, Finset.card_univ]
          _ ≤ (Λ S - Λ S').roots.toFinset.card := Finset.card_le_card hsubroots
          _ ≤ Multiset.card (Λ S - Λ S').roots := Multiset.toFinset_card_le _
          _ ≤ (Λ S - Λ S').natDegree := Polynomial.card_roots' _
      omega
    have hΛeq : Λ S = Λ S' := sub_eq_zero.mp hzero
    have hprod : ∀ T : Finset ι,
        ∏ b ∈ T.image dom, (Polynomial.X - Polynomial.C b) = Λ T := fun T =>
      Finset.prod_image (fun x _ y _ hxy => hdom hxy)
    have hval : (S.image dom).val = (S'.image dom).val := by
      rw [← Polynomial.roots_prod_X_sub_C (S.image dom),
        ← Polynomial.roots_prod_X_sub_C (S'.image dom), hprod S, hprod S', hΛeq]
    have himg : S.image dom = S'.image dom := Finset.val_injective hval
    have hmem_iff : ∀ (T : Finset ι) (i : ι), i ∈ T ↔ dom i ∈ T.image dom := by
      intro T i
      constructor
      · exact Finset.mem_image_of_mem _
      · intro hmem
        obtain ⟨j, hj, hji⟩ := Finset.mem_image.mp hmem
        rwa [← hdom hji]
    ext i
    rw [hmem_iff S i, hmem_iff S' i, himg]
  -- assemble the list
  have hEcard : ∀ j, ((E j : Finset ι)).card = k + 1 := fun j =>
    (Finset.mem_powersetCard.mp (E j).2).2
  refine ⟨fun j => cw (E j), fun j => hcwmem _ (hEcard j), ?_, fun j => hclose _ (hEcard j)⟩
  intro j j' hjj'
  have hSS : (E j : Finset ι) = (E j' : Finset ι) :=
    hcwinj _ _ (hEcard j) (hEcard j') hjj'
  exact E.injective (Subtype.ext hSS)

/-- **`cor:quantitative-first-grid-floor` — unconditional first-grid floor**
(tex `:992`–`:1020`; **proved**, this packet).

For any Reed–Solomon code `C = RS[F, D, k]` on an `n`-point domain (no smoothness),
the correlated-agreement error is at least the deep-list floor `𝓔_{q,k}(C(n, k+1))`
across the first grid band `δ ∈ [1 − (k+1)/n, 1 − k/n)`.  The witness is the explicit
monomial word `x^{k+1}|_D` with its `C(n, k+1)` locator codewords
(`hasList_first_grid`), fed to the proved deep floor
`thm_quotient_remainder_deep_floor` at `A = k + 1`. -/
theorem cor_quantitative_first_grid_floor (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hk : 0 < k) (hkn : k < Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (δ : ℝ) (hδlo : 1 - (k + 1 : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k (Nat.choose (Fintype.card ι) (k + 1))
      ≤ ecaErr (RSpoly dom k) δ δ := by
  have hcast : ((k + 1 : ℕ) : ℝ) = (k : ℝ) + 1 := by push_cast; ring
  refine thm_quotient_remainder_deep_floor dom hdom hk
    (Nat.choose_pos (by omega : k + 1 ≤ Fintype.card ι))
    (by omega : k < k + 1) (by omega : k + 1 ≤ Fintype.card ι) hq
    (fun i => dom i ^ (k + 1)) (hasList_first_grid dom hdom hkn) δ ?_ hδhi
  rw [hcast]
  exact hδlo

/-- **`cor:first-grid-cap`, `c = 1` clause (tex `:1090`–`:1127`; **proved**, this
packet).**  For `C = RS[F, D, k]` on any injective `n`-point domain with `q > n`
and `C(n, k+1) ≥ q/k + 1`, both `ε_ca` and `ε_mca` at the first closed grid point
below capacity, `δ = 1 − (k+1)/n`, exceed the half-inverse-dimension threshold.
No smoothness is needed ("for `c = 1` ... no smoothness is needed", tex `:1093`).
The route: `hasList_first_grid` gives the `C(n,k+1)` list at agreement `k + 1`;
`cor_quotient_remainder_trigger` converts (`C(n,k+1) ≥ q/k + 1 > (q−n)/k`) into the
`ε_ca` bound; the `ε_mca` clause follows from the proved `eca_le_emca`
(`fact:chain`: every CA-bad slope is MCA-bad).  The general-`c` statement is
`cor_first_grid_cap` below (still a skeleton for `c > 1`). -/
theorem cor_first_grid_cap_one (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hk : 0 < k) (hkn : k < Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card F : ℝ) / k + 1 ≤ (Nat.choose (Fintype.card ι) (k + 1) : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
        < ecaErr (RSpoly dom k)
            (1 - (k + 1 : ℝ) / Fintype.card ι) (1 - (k + 1 : ℝ) / Fintype.card ι)
      ∧ (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
        < emcaErr (RSpoly dom k) (1 - (k + 1 : ℝ) / Fintype.card ι) := by
  have hkR : (0 : ℝ) < k := by exact_mod_cast hk
  have hn0 : 0 < Fintype.card ι := lt_of_le_of_lt (Nat.zero_le _) hkn
  have hnR : (0 : ℝ) < Fintype.card ι := by exact_mod_cast hn0
  have hcast : ((k + 1 : ℕ) : ℝ) = (k : ℝ) + 1 := by push_cast; ring
  have htrig : ((Fintype.card F : ℝ) - Fintype.card ι) / k
      < (Nat.choose (Fintype.card ι) (k + 1) : ℝ) := by
    have h1 : ((Fintype.card F : ℝ) - Fintype.card ι) / k
        < (Fintype.card F : ℝ) / k + 1 := by
      rw [sub_div]
      have h2 : 0 < (Fintype.card ι : ℝ) / k := div_pos hnR hkR
      linarith
    linarith
  have hδhi : 1 - ((k + 1 : ℕ) : ℝ) / Fintype.card ι
      < 1 - (k : ℝ) / Fintype.card ι := by
    have hlt : (k : ℝ) < ((k + 1 : ℕ) : ℝ) := by exact_mod_cast Nat.lt_succ_self k
    have hstep : (k : ℝ) / Fintype.card ι < ((k + 1 : ℕ) : ℝ) / Fintype.card ι := by
      rw [div_lt_div_iff₀ hnR hnR]
      nlinarith
    linarith
  have hca := cor_quotient_remainder_trigger dom hdom hk
    (by omega : k < k + 1) (by omega : k + 1 ≤ Fintype.card ι) hq
    (fun i => dom i ^ (k + 1)) (hasList_first_grid dom hdom hkn) htrig
    (1 - ((k + 1 : ℕ) : ℝ) / Fintype.card ι) le_rfl hδhi
  rw [hcast] at hca
  refine ⟨hca, lt_of_lt_of_le hca ?_⟩
  simpa [ecaErrDiag] using eca_le_emca (RSpoly dom k) (1 - ((k : ℝ) + 1) / Fintype.card ι)

/-- **`cor:first-grid-cap` — first-grid cap, general divisor scale `c`**
(tex `:1090`–`:1127`).

Let `c ∣ gcd(n, k)`; if `c > 1` assume `D` is a multiplicative coset, and if
`C(n/c, k/c + 1) ≥ q/k + 1`, then both `ε_ca` and `ε_mca` of `C = RS[F, D, k]` at the
grid radius `1 − (k+c)/n` exceed the half-inverse-dimension threshold.  For `c = 1` this
is the first closed grid point below capacity and needs no smoothness.

Status (skeleton falsity-and-repair packet, 2026-07-18): the statement matches the
paper (the `hyp` binomial has **no** `|B|` division, exactly as tex `:1095`–`:1097`) —
no defect found, so no statement repair.  The `c = 1` instance is fully discharged by
the proved `cor_first_grid_cap_one` above (at `c = 1`, `N = n` and the radius is
`1 − (k+1)/n`).  The general `c > 1` clause routes through the augmented slack-one
quotient floor (`cor:augmented-slack-one` at `c > 1`, tex `:1063`), whose
multiplicative-coset fiber machinery is not yet formalized; it stays honestly
sorried and is out of scope for this packet. -/
theorem cor_first_grid_cap (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {c N k : ℕ} (hk : 0 < k) (hkn : k < Fintype.card ι)
    (hc : 0 < c) (hcnk : c ∣ Nat.gcd (Fintype.card ι) k)
    (hN : c * N = Fintype.card ι) (hsmooth : DomSmooth dom (fun x => x ^ c) c)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card F : ℝ) / k + 1 ≤ (Nat.choose N (k / c + 1) : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
        < ecaErr (RSpoly dom k)
            (1 - (k + c : ℝ) / Fintype.card ι) (1 - (k + c : ℝ) / Fintype.card ι)
      ∧ (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
        < emcaErr (RSpoly dom k) (1 - (k + c : ℝ) / Fintype.card ι) := by
  sorry

end RSCap
