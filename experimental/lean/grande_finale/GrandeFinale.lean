import Mathlib
import GrandeFinale.DirectionDistanceAllPairs

/-!
# Self-contained core of "Final Inputs for RS-MCA" (`grande_finale.tex`)

This file formalizes the parts of the manuscript that are genuinely self-contained,
theorem-level mathematics: the integer-budget convention, the first-match upper
ledger, the structural comparison and monotonicity of the CA/MCA bad-slope sets,
the Cauchy–Schwarz distinct-value counting kernel underlying the simple-pole
list-to-MCA floor, the collision-averaging selection step, the identity-prefix
pigeonhole, the moment-sandwich inequalities, and the finite numeric certificate
facts (the banked table and the packet inequalities).

The manuscript also contains genuinely open conjectures (Q, BC, SP), asymptotic
`o(1)` statements, and claims that rely on an external certificate verifier over
data packets; those are intentionally *not* formalized here (they are not
self-contained theorems). Where a manuscript result is a coding-theoretic
statement whose proof rests on polynomial machinery, we formalize its
self-contained combinatorial/arithmetic kernel, which carries the reusable
mathematical content.

Each declaration references the `\label{...}` of the manuscript statement it
formalizes.
-/

open scoped BigOperators
open scoped Classical

namespace GrandeFinale

/-! ## The integer budget convention (`lem:integer-budget`) -/

/--
Integer budget convention, non-strict form: for an integer count `B` and a
denominator `Q > 0`, having sampled ratio `B/Q ≤ ε*` is equivalent to the integer
comparison `B ≤ ⌊ε* Q⌋`. (`lem:integer-budget`)
-/
theorem integer_budget_le {Q : ℕ} (hQ : 0 < Q) (B : ℕ) (e : ℚ) :
    (B : ℚ) / (Q : ℚ) ≤ e ↔ (B : ℤ) ≤ ⌊e * (Q : ℚ)⌋ := by
  rw [ Int.le_floor ];
  rw [ div_le_iff₀ ( by positivity ), mul_comm ] ; norm_cast

/--
Integer budget convention, strict form: `ε* < B/Q ↔ ⌊ε* Q⌋ < B`.
(`lem:integer-budget`)
-/
theorem integer_budget_lt {Q : ℕ} (hQ : 0 < Q) (B : ℕ) (e : ℚ) :
    e < (B : ℚ) / (Q : ℚ) ↔ ⌊e * (Q : ℚ)⌋ < (B : ℤ) := by
  rw [ lt_div_iff₀ ( by positivity ), Int.floor_lt ];
  norm_cast

/-! ## The first-match upper ledger (`lem:first-match-ledger`) -/

/--
First-match upper ledger. If the finite set of bad line-parameters is covered
by finitely many cells `E i` with certified caps `(E i).card ≤ U i`, then the
number of bad parameters is at most `∑ U i`. This is the disjoint-cover counting
step behind `lem:first-match-ledger`.
-/
theorem first_match_ledger {α ι : Type*} [DecidableEq α]
    (badset : Finset α) (idx : Finset ι) (E : ι → Finset α) (U : ι → ℕ)
    (hcover : badset ⊆ idx.biUnion E) (hU : ∀ i ∈ idx, (E i).card ≤ U i) :
    badset.card ≤ ∑ i ∈ idx, U i := by
  exact le_trans ( Finset.card_le_card hcover ) ( Finset.card_biUnion_le.trans ( Finset.sum_le_sum hU ) )

/-! ## Support-wise CA and MCA (`def:ca-mca`, `lem:basic-staircase`)

We model a linear code by an arbitrary set `C ⊆ (D → F)` of codewords. A word `h`
is `C`-explained on `S` if some codeword agrees with `h` on all of `S`; a pair is
explained if the two words are simultaneously explained by (possibly different)
codewords on `S`. -/

section CAMCA
variable {F D : Type*} [Field F]

/-- `h` is `C`-explained on `S`: some codeword of `C` agrees with `h` on `S`. -/
def Explained (C : Set (D → F)) (h : D → F) (S : Finset D) : Prop :=
  ∃ c ∈ C, ∀ x ∈ S, c x = h x

/-- The pair `(f₁, f₂)` is `C^{≡2}`-explained on `S`. -/
def ExplainedPair (C : Set (D → F)) (f1 f2 : D → F) (S : Finset D) : Prop :=
  ∃ c1 ∈ C, ∃ c2 ∈ C, (∀ x ∈ S, c1 x = f1 x) ∧ (∀ x ∈ S, c2 x = f2 x)

/-- A finite slope `γ` is MCA-bad at agreement `a` for the pair `(f₁, f₂)`:
there is a support `S` of size at least `a` on which `f₁ + γ f₂` is explained but
the pair is not. (`def:ca-mca`) -/
def MCABad (C : Set (D → F)) (f1 f2 : D → F) (a : ℕ) (γ : F) : Prop :=
  ∃ S : Finset D, a ≤ S.card ∧ Explained C (fun x => f1 x + γ * f2 x) S
    ∧ ¬ ExplainedPair C f1 f2 S

/-- A finite slope `γ` is CA-bad at agreement `a` for the pair `(f₁, f₂)`:
`f₁ + γ f₂` is explained on some support of size at least `a`, while the pair is
not explained on *any* support of size at least `a`. (`def:ca-mca`) -/
def CABad (C : Set (D → F)) (f1 f2 : D → F) (a : ℕ) (γ : F) : Prop :=
  (∃ S : Finset D, a ≤ S.card ∧ Explained C (fun x => f1 x + γ * f2 x) S)
    ∧ (∀ T : Finset D, a ≤ T.card → ¬ ExplainedPair C f1 f2 T)

/--
Comparison: every CA-bad slope is MCA-bad. (First part of `lem:basic-staircase`.)
-/
theorem CABad_imp_MCABad {C : Set (D → F)} {f1 f2 : D → F} {a : ℕ} {γ : F}
    (h : CABad C f1 f2 a γ) : MCABad C f1 f2 a γ := by
  exact ⟨ h.1.choose, h.1.choose_spec.1, h.1.choose_spec.2, h.2 _ h.1.choose_spec.1 ⟩

/--
Monotonicity of the bad-slope sets in the agreement threshold: an MCA-bad
slope at agreement `a` is MCA-bad at every lower agreement `a' ≤ a`.
(Second part of `lem:basic-staircase`.)
-/
theorem MCABad_antitone {C : Set (D → F)} {f1 f2 : D → F} {γ : F} {a a' : ℕ}
    (haa : a' ≤ a) (h : MCABad C f1 f2 a γ) : MCABad C f1 f2 a' γ := by
  exact ⟨ h.choose, le_trans haa h.choose_spec.1, h.choose_spec.2.1, h.choose_spec.2.2 ⟩

end CAMCA

section Numerators
variable {F D : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D]

/-- The MCA staircase numerator: the maximum over received lines of the number of
MCA-bad finite slopes at agreement `a`. (`def:staircase`, MCA track.) -/
noncomputable def B_MCA (C : Set (D → F)) (a : ℕ) : ℕ :=
  Finset.univ.sup (fun p : (D → F) × (D → F) =>
    (Finset.univ.filter (fun γ : F => MCABad C p.1 p.2 a γ)).card)

/-- The CA staircase numerator. (`def:staircase`, CA track.) -/
noncomputable def B_CA (C : Set (D → F)) (a : ℕ) : ℕ :=
  Finset.univ.sup (fun p : (D → F) × (D → F) =>
    (Finset.univ.filter (fun γ : F => CABad C p.1 p.2 a γ)).card)

omit [DecidableEq F] in
/--
The numerator comparison `B_CA ≤ B_MCA`. (`lem:basic-staircase`.)
-/
theorem B_CA_le_B_MCA (C : Set (D → F)) (a : ℕ) : B_CA C a ≤ B_MCA C a := by
  refine' Finset.sup_le _;
  intro p hp;
  refine' le_trans _ ( Finset.le_sup hp );
  exact Finset.card_le_card fun x hx => by simpa using CABad_imp_MCABad ( Finset.mem_filter.mp hx |>.2 ) ;

/-- The normalized MCA error `ε_mca(C, 1 - a/n) = B_MCA(a)/|F|`. (`def:ca-mca`.) -/
noncomputable def emca (C : Set (D → F)) (a : ℕ) : ℝ := (B_MCA C a : ℝ) / (Fintype.card F)

/-- The normalized CA error `ε_ca(C, 1 - a/n) = B_CA(a)/|F|`. (`def:ca-mca`.) -/
noncomputable def eca (C : Set (D → F)) (a : ℕ) : ℝ := (B_CA C a : ℝ) / (Fintype.card F)

omit [DecidableEq F] in
/--
`ε_ca ≤ ε_mca`. (`lem:basic-staircase`.)
-/
theorem eca_le_emca (C : Set (D → F)) (a : ℕ) : eca C a ≤ emca C a := by
  exact div_le_div_of_nonneg_right ( Nat.cast_le.mpr ( GrandeFinale.B_CA_le_B_MCA C a ) ) ( Nat.cast_nonneg _ )

end Numerators

/-! ## The Cauchy–Schwarz distinct-value kernel

This is the arithmetic heart of the quantitative simple-pole list-to-MCA floor
(`thm:simple-pole-list-floor`) and the fiber-to-slope conversion
(`thm:fiber-to-slope`): from `L` values with multiplicities whose collision
budget is controlled, the number `M` of distinct values is large. -/

/--
Cauchy–Schwarz distinct-value floor. Let a finite family carry multiplicities
`m : ι → ℕ` on `s` (with `s.card = M`), total `∑ m = L ≥ 1`, and second-moment
budget `d · ∑ m² ≤ d·L + k·L·(L-1)` (with `d = q - n > 0`). Then
`L·d ≤ M·(d + k(L-1))`, i.e. `M ≥ L·d / (d + k(L-1))`.
-/
theorem distinct_value_floor {ι : Type*} (s : Finset ι) (m : ι → ℕ)
    (L k d M : ℕ) (hL : 0 < L)
    (hsum : ∑ i ∈ s, m i = L) (hcard : s.card = M)
    (hsq : d * ∑ i ∈ s, (m i) ^ 2 ≤ d * L + k * L * (L - 1)) :
    L * d ≤ M * (d + k * (L - 1)) := by
  -- By Cauchy-Schwarz inequality, we have $(∑ i ∈ s, m i)^2 ≤ |s| * ∑ i ∈ s, m i^2$.
  have h_cauchy_schwarz : (∑ i ∈ s, m i)^2 ≤ s.card * ∑ i ∈ s, (m i)^2 := by
    have h_cauchy_schwarz : ∀ (u v : ι → ℝ), (∑ i ∈ s, u i * v i)^2 ≤ (∑ i ∈ s, u i^2) * (∑ i ∈ s, v i^2) := by
      exact fun u v => Finset.sum_mul_sq_le_sq_mul_sq s u v
    simpa [ ← @Nat.cast_le ℝ ] using h_cauchy_schwarz ( fun _ => 1 ) ( fun i => m i );
  rw [ hsum, hcard ] at h_cauchy_schwarz;
  nlinarith [ Nat.sub_add_cancel hL ]

/--
Nat ceiling helper: if `N ≤ M·Dv` with `Dv > 0`, then `⌈N/Dv⌉ = (N+Dv-1)/Dv ≤ M`.
Combined with `distinct_value_floor`, this yields the manuscript ceiling
`M ≥ ⌈L(q-n)/(q-n+k(L-1))⌉`.
-/
theorem nat_ceil_div_le {N Dv M : ℕ} (hD : 0 < Dv) (h : N ≤ M * Dv) :
    (N + Dv - 1) / Dv ≤ M := by
  exact Nat.le_of_lt_succ ( Nat.div_lt_of_lt_mul <| by rw [ tsub_lt_iff_left ] <;> linarith )

/-! ## Collision-averaging selection (`thm:fiber-to-slope`, `thm:simple-pole-list-floor`)

The pole `α` with few colliding value-pairs is chosen by an averaging argument:
some element of a nonempty finite set attains at most the mean. -/

/--
Averaging (min ≤ mean): some element of a nonempty finite set has value at most
the average, i.e. `s.card · f a ≤ ∑ f`. This selects the pole `α` with few
collisions in the fiber-to-slope conversion.
-/
theorem exists_le_average {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (f : ι → ℕ) :
    ∃ a ∈ s, s.card * f a ≤ ∑ i ∈ s, f i := by
  obtain ⟨a, ha, hle⟩ := Finset.exists_min_image s f hs;
  exact ⟨ a, ha, by simpa using Finset.sum_le_sum hle ⟩

/-! ## Identity-prefix witness pigeonhole (`prop:prefix-witness`) -/

/--
Identity-prefix pigeonhole (max ≥ mean form). If `f` maps `s` into a nonempty
`t`, some fiber has `s.card ≤ t.card · (fiber card)`, i.e. some prefix value has a
fiber of size at least `⌈s.card / t.card⌉`. This is the final counting sentence of
`prop:prefix-witness` (with `s` the `m`-subsets, `t` the `|B|^w` prefix values).
-/
theorem prefix_witness_maxfiber {α β : Type*} [DecidableEq β] {s : Finset α}
    {t : Finset β} {f : α → β} (hf : ∀ a ∈ s, f a ∈ t) (ht : t.Nonempty) :
    ∃ y ∈ t, s.card ≤ t.card * ({x ∈ s | f x = y}).card := by
  have h_pigeonhole : s.card = ∑ y ∈ t, (s.filter (fun x => f x = y)).card := by
    simp +decide only [Finset.card_eq_sum_ones, Finset.sum_fiberwise_of_maps_to hf];
  obtain ⟨y, hy⟩ : ∃ y ∈ t, ∀ z ∈ t, (s.filter (fun x => f x = z)).card ≤ (s.filter (fun x => f x = y)).card := by
    exact Finset.exists_max_image _ _ ht;
  exact ⟨ y, hy.1, h_pigeonhole.symm ▸ le_trans ( Finset.sum_le_sum hy.2 ) ( by simp +decide ) ⟩

/-! ## The moment sandwich (`prop:moment-sandwich`, `thm:moment-q`) -/

/--
Upper moment bound: for a probability weight `μ` on `s` (`∑ μ = 1`, `μ ≥ 0`)
with maximum at most `mx` and `r ≥ 1`, one has `∑ μ^r ≤ mx^(r-1)`. This is the
lower half of `prop:moment-sandwich` (`Γ_r ≤ R^{r-1}`).
-/
theorem moment_upper {ι : Type*} (s : Finset ι) (μ : ι → ℝ)
    (hμ : ∀ i ∈ s, 0 ≤ μ i) (hsum : ∑ i ∈ s, μ i = 1)
    (r : ℕ) (hr : 1 ≤ r) (mx : ℝ) (hmx : ∀ i ∈ s, μ i ≤ mx) :
    ∑ i ∈ s, (μ i) ^ r ≤ mx ^ (r - 1) := by
  have h_max : ∑ i ∈ s, (μ i) ^ r ≤ ∑ i ∈ s, (mx ^ (r - 1)) * (μ i) := by
    exact Finset.sum_le_sum fun i hi => by rw [ show μ i ^ r = ( μ i ^ ( r - 1 ) ) * μ i by rw [ ← pow_succ, Nat.sub_add_cancel hr ] ] ; exact mul_le_mul_of_nonneg_right ( pow_le_pow_left₀ ( hμ i hi ) ( hmx i hi ) _ ) ( hμ i hi ) ;
  simp_all +decide [ ← Finset.mul_sum _ _ _ ]

/--
Lower moment bound: the `r`-th power of any single (in particular the maximal)
weight is at most `∑ μ^r`. This is the upper half of `prop:moment-sandwich`
(`R ≤ (∑ μ^r)^{1/r}` after taking `r`-th roots) and the engine of the finite Q
moment route (`thm:moment-q`).
-/
theorem moment_lower {ι : Type*} (s : Finset ι) (μ : ι → ℝ)
    (hμ : ∀ i ∈ s, 0 ≤ μ i) (i0 : ι) (hi0 : i0 ∈ s) (r : ℕ) :
    (μ i0) ^ r ≤ ∑ i ∈ s, (μ i) ^ r := by
  exact Finset.single_le_sum ( fun i _ => pow_nonneg ( hμ i ‹_› ) r ) hi0

/--
Finite moment criterion for Q (`thm:moment-q`). With `μ` a probability weight,
`R = base^w · mx` the normalized maximum-fiber ratio, `mx = μ i0` the maximal
weight, and `Γ_r = base^{w(r-1)} · ∑ μ^r`, one has `R^r ≤ base^w · Γ_r`; taking
`r`-th roots gives `R ≤ (base^w Γ_r)^{1/r}`, the finite adjacent Q bound.
-/
theorem moment_q_finite {ι : Type*} (s : Finset ι) (μ : ι → ℝ)
    (hμ : ∀ i ∈ s, 0 ≤ μ i) (i0 : ι) (hi0 : i0 ∈ s)
    (r w : ℕ) (hr : 1 ≤ r) (base : ℝ) (hbase : 0 ≤ base) :
    (base ^ w * μ i0) ^ r ≤ base ^ w * (base ^ (w * (r - 1)) * ∑ i ∈ s, (μ i) ^ r) := by
  rw [ mul_pow ];
  rw [ ← mul_assoc, ← pow_add, show w + w * ( r - 1 ) = w * r by nlinarith [ Nat.sub_add_cancel hr ] ];
  exact mul_le_mul ( by rw [ ← pow_mul ] ) ( Finset.single_le_sum ( fun i _ => pow_nonneg ( hμ i ‹_› ) r ) hi0 ) ( pow_nonneg ( hμ i0 hi0 ) r ) ( by positivity )

/-! ## Finite numeric certificate facts (`\S`"What Is Already Banked", `prop:finite-packet-consequences`)

The base primes and the exact challenge budgets, together with the packet-recorded
list/MCA numerators, verified by direct integer computation. The astronomically
large binomial derivations that *produce* the packet `M`-values are not re-derived
here; we verify the integer comparisons that the packets assert. -/

namespace Certificates

/-- The KoalaBear base prime `p_KB = 2^31 - 2^24 + 1`. -/
def pKB : ℕ := 2130706433

/-- The Mersenne-31 base prime `p_M31 = 2^31 - 1`. -/
def pM31 : ℕ := 2147483647

theorem pKB_eq : pKB = 2 ^ 31 - 2 ^ 24 + 1 := by norm_num [pKB]
theorem pM31_eq : pM31 = 2 ^ 31 - 1 := by norm_num [pM31]

/-- The KoalaBear challenge budget `B*_KB = ⌊p_KB^6 / 2^128⌋`. -/
def BstarKB : ℕ := pKB ^ 6 / 2 ^ 128

/-- The Mersenne-31 challenge budget `B*_M31 = ⌊p_M31^4 / 2^100⌋`. -/
def BstarM31 : ℕ := pM31 ^ 4 / 2 ^ 100

theorem BstarKB_eq : BstarKB = 274980728111395087 := by native_decide
theorem BstarM31_eq : BstarM31 = 16777215 := by native_decide

/-- Packet MCA lower numerators (`prop:finite-packet-consequences`, `rem:finite-artifacts`). -/
def M_KB_a0 : ℕ := 138634741058327852652
def M_KB_a0p : ℕ := 57198030366
def M_M31_a0 : ℕ := 4281388998575706
def M_M31_a0p : ℕ := 1752700

/-- KoalaBear MCA: the active agreement `a₀` is unsafe: `B*_KB < M(a₀)`. -/
theorem KB_unsafe : BstarKB < M_KB_a0 := by native_decide

/-- KoalaBear MCA: the same lower route fails at the adjacent agreement: `M(a₀+1) ≤ B*_KB`. -/
theorem KB_adjacent_lower_fails : M_KB_a0p ≤ BstarKB := by native_decide

/-- Mersenne-31 MCA: the active agreement `a₀` is unsafe: `B*_M31 < M(a₀)`. -/
theorem M31_unsafe : BstarM31 < M_M31_a0 := by native_decide

/-- Mersenne-31 MCA: the same lower route fails at the adjacent agreement. -/
theorem M31_adjacent_lower_fails : M_M31_a0p ≤ BstarM31 := by native_decide

/-- The Mersenne-31 MCA `c = 2048` dyadic quotient watch item is below budget
(`prop:rung-veto`): its exact mass `12769758 < B*_M31 = 16777215`. -/
theorem M31_watch : 12769758 < BstarM31 := by native_decide

end Certificates

end GrandeFinale