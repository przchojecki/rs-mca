import cap25_cap_v13_raw_compact.Floor

/-!
# Input BC: the binomial-moment census and its base-field (subfield) floors

This file develops the structural, *provable* content attached to the paper's Residual
Input **BC** (base-field-normalized split-pencil census).  BC itself is an open counting
conjecture (an upper bound on primitive split-pencil cells); it cannot be settled here.
What *can* be settled unconditionally, and is proved in this file, is the matching **lower
obstruction**: the census that BC must bound has an unavoidable `|𝔹|`-scale floor whenever
the evaluation domain lies in a proper subfield.  This is exactly the phenomenon that
forces BC to be *base-field normalized* (`prop:subfield-census-floor` and the discussion of
`prob:BC-expanded` in the paper).

Concretely:

* `RSMCA.census D K m U` — the **`m`-th binomial-moment census**
  `∑_c binom(agr(U,c), m)`, the sum over Reed–Solomon codewords of the number of size-`m`
  supports on which `U` agrees with `c`.  By `prop:lattice-locus-core` this is exactly the
  number of `m`-supports counted in the split-pencil problem.
* `RSMCA.census_ge_listFinset` / `RSMCA.census_ge_list` — the census dominates the plain
  decoding-list size.
* `RSMCA.bc_census_floor` — **the base-field census floor** (interior profiles,
  `prop:subfield-census-floor` (b)): for any level `m' ≥ m` there is a `𝔹`-valued received
  word whose level-`m` census is at least
  `⌊binom(n,m') / |𝔹|^{m'-K}⌋ · binom(m',m)`.
* `RSMCA.bc_boundary_census_floor` — **the boundary case** (`prop:subfield-census-floor`
  (a)), namely `m' = m`, giving census `≥ ⌊binom(n,m) / |𝔹|^{m-K}⌋`.

These are the `M_𝔹(d₁;m)` floors of the paper: a purely challenge-field (`q`-scale) random
model would undercount them, which is precisely why BC must be stated at the base-field
scale.
-/

open Polynomial Finset
open scoped Classical

namespace RSMCA

variable {B F : Type*} [Field B] [Field F] [Algebra B F]
  [Fintype B] [Fintype F] [DecidableEq F] [DecidableEq B]

/-- The Reed–Solomon code as a `Finset` of the finite type `D → F`. -/
noncomputable def RSFinset (D : Finset B) (K : ℕ) : Finset (D → F) :=
  Finset.univ.filter (fun c => c ∈ (RS D K : Set (D → F)))

/-- The decoding list as a `Finset`: codewords agreeing with `U` on `≥ m` positions. -/
noncomputable def listFinset (D : Finset B) (K m : ℕ) (U : D → F) : Finset (D → F) :=
  (RSFinset D K).filter (fun c => m ≤ agreeCard U c)

/-- The **`m`-th binomial-moment census** of `U`:
`∑_c binom(agr(U,c), m)`, the number of pairs `(c, T)` with `c ∈ RS[F,D,K]`, `|T| = m`, and
`c` agreeing with `U` on `T`.  This is the split-pencil census of `prop:lattice-locus-core`
(the `m`-th binomial moment `∑_c binom(agr(U,c), m)` of the agreement profile). -/
noncomputable def census (D : Finset B) (K m : ℕ) (U : D → F) : ℕ :=
  ∑ c ∈ RSFinset D K, (agreeCard U c).choose m

omit [Fintype B] in
/-- `listSet` and `listFinset` describe the same set. -/
lemma listSet_eq_coe_listFinset (D : Finset B) (K m : ℕ) (U : D → F) :
    listSet D K m U = (listFinset D K m U : Set (D → F)) := by
  ext c
  simp only [listSet, listFinset, RSFinset, Finset.coe_filter, Set.mem_setOf_eq,
    Finset.mem_univ, true_and, Finset.mem_filter]

omit [Fintype B] in
/-- The `ncard` of the decoding list equals the `listFinset` cardinality. -/
lemma listSet_ncard_eq (D : Finset B) (K m : ℕ) (U : D → F) :
    (listSet D K m U).ncard = (listFinset D K m U).card := by
  rw [listSet_eq_coe_listFinset, Set.ncard_coe_finset]

omit [Fintype B] in
/-- **The census dominates the decoding-list size** (as a `Finset`). Each listed codeword
agrees on `≥ m` positions, hence contributes at least `binom(m,m) = 1` support. -/
lemma census_ge_listFinset (D : Finset B) (K m : ℕ) (U : D → F) :
    (listFinset D K m U).card ≤ census D K m U := by
  have h1 : (listFinset D K m U).card = ∑ _c ∈ listFinset D K m U, 1 := by
    rw [Finset.sum_const, smul_eq_mul, mul_one]
  rw [h1, census]
  calc ∑ _c ∈ listFinset D K m U, 1
      ≤ ∑ c ∈ listFinset D K m U, (agreeCard U c).choose m := by
        apply Finset.sum_le_sum
        intro c hc
        rw [listFinset, Finset.mem_filter] at hc
        exact Nat.choose_pos hc.2
    _ ≤ ∑ c ∈ RSFinset D K, (agreeCard U c).choose m :=
        Finset.sum_le_sum_of_subset (Finset.filter_subset _ _)

omit [Fintype B] in
/-- **The census dominates the decoding-list size** (as an `ncard`). -/
lemma census_ge_list (D : Finset B) (K m : ℕ) (U : D → F) :
    (listSet D K m U).ncard ≤ census D K m U := by
  rw [listSet_ncard_eq]; exact census_ge_listFinset D K m U

/-- **Base-field census floor (interior profiles).** For `K ≤ m ≤ m' ≤ n = |D|`, there is a
`𝔹`-valued received word whose level-`m` binomial-moment census is at least
`⌊binom(n,m') / |𝔹|^{m'-K}⌋ · binom(m',m)`.

This is `prop:subfield-census-floor` (b): the interior split-pencil profile at first shifted
degree `d₁ = m' - K + 1` carries a base-field floor `M_𝔹(d₁;m)`.  A purely `q`-scale random
model would undercount it, which is why BC must be base-field normalized. -/
theorem bc_census_floor (D : Finset B) (K m m' : ℕ) (hKm' : K ≤ m')
    (hm'n : m' ≤ D.card) :
    ∃ Ub : D → B,
      ((D.card).choose m' / (Fintype.card B) ^ (m' - K)) * (m'.choose m)
        ≤ census D K m (fun x => algebraMap B F (Ub x)) := by
  obtain ⟨Ub, hUb⟩ := identity_floor (F := F) D K m' hKm' hm'n
  refine ⟨Ub, ?_⟩
  set U : D → F := (fun x => algebraMap B F (Ub x)) with hU
  -- the list at level `m'`, as a Finset
  have hfloor : (D.card).choose m' / (Fintype.card B) ^ (m' - K)
      ≤ (listFinset D K m' U).card := by
    rw [← listSet_ncard_eq]; exact hUb
  -- census at level `m`, restricted to the level-`m'` list, using `binom(agr,m) ≥ binom(m',m)`
  calc ((D.card).choose m' / (Fintype.card B) ^ (m' - K)) * (m'.choose m)
      ≤ (listFinset D K m' U).card * (m'.choose m) := by
        exact Nat.mul_le_mul_right _ hfloor
    _ = ∑ _c ∈ listFinset D K m' U, (m'.choose m) := by
        rw [Finset.sum_const, smul_eq_mul]
    _ ≤ ∑ c ∈ listFinset D K m' U, (agreeCard U c).choose m := by
        apply Finset.sum_le_sum
        intro c hc
        rw [listFinset, Finset.mem_filter] at hc
        exact Nat.choose_le_choose m hc.2
    _ ≤ ∑ c ∈ RSFinset D K, (agreeCard U c).choose m :=
        Finset.sum_le_sum_of_subset (Finset.filter_subset _ _)
    _ = census D K m U := rfl

/-- **Base-field census floor (boundary profile).** The special case `m' = m` of
`bc_census_floor`: there is a `𝔹`-valued received word whose `m`-th binomial-moment census
is at least `⌊binom(n,m) / |𝔹|^{m-K}⌋`.

This is `prop:subfield-census-floor` (a): the heaviest identity-prefix witness has census at
least `⌈binom(n,m) · |𝔹|^{-w}⌉` (here the honest integer floor `⌊·⌋`, `w = m - K`). -/
theorem bc_boundary_census_floor (D : Finset B) (K m : ℕ) (hKm : K ≤ m) (hmn : m ≤ D.card) :
    ∃ Ub : D → B,
      (D.card).choose m / (Fintype.card B) ^ (m - K)
        ≤ census D K m (fun x => algebraMap B F (Ub x)) := by
  obtain ⟨Ub, hUb⟩ := bc_census_floor (F := F) D K m m hKm hmn
  refine ⟨Ub, ?_⟩
  simpa [Nat.choose_self] using hUb

/-- **Interior base-field census floor — pigeonhole (`⌈·⌉ ≥ 1`) form.** For `K ≤ m' ≤ n = |D|`
there is a `𝔹`-valued received word whose level-`m` binomial-moment census is at least
`binom(m', m)`.

This is the *non-vacuous* strengthening of `bc_census_floor` on the interior side.  The floor
in `bc_census_floor` is `⌊binom(n,m') / |𝔹|^{m'-K}⌋ · binom(m',m)`, and Lean's `Nat` division is
a genuine floor: in the interior *below-one* regime `binom(n,m') < |𝔹|^{m'-K}` (which already
holds at the first interior profile `d₁ = w + 2`, since `m' - K = d₁ - 1`) that floor collapses
to `0`, so `bc_census_floor` degenerates to `0 ≤ census`.  The paper's floor `M_𝔹(d₁;m)` is the
*ceiling* `⌈binom(n,m') / |𝔹|^{m'-K}⌉ · binom(m',m)`, and `⌈binom(n,m') / |𝔹|^{m'-K}⌉ ≥ 1`
whenever `binom(n,m') ≥ 1` (i.e. `m' ≤ n`); its non-trivial content in the below-one regime is
exactly `binom(m',m) ≤ census`.  This theorem supplies that content by an elementary
max-fiber `≥ 1` pigeonhole: a single `m'`-subset `M ⊆ D` (which exists because `m' ≤ n`) sits in
the prefix fiber of its own locator prefix `pre K m' M`, producing one degree-`< K` codeword
(`code_mem_RS`) that agrees with the associated identity-prefix witness on all of `M`
(`code_agrees`), hence on `≥ m'` positions, contributing `binom(m',m)` size-`m` supports to the
census.  This is `prop:subfield-census-floor` (b) in its ceiling form. -/
theorem bc_census_floor_pigeonhole (D : Finset B) (K m m' : ℕ) (hKm' : K ≤ m')
    (hm'n : m' ≤ D.card) :
    ∃ Ub : D → B,
      m'.choose m ≤ census D K m (fun x => algebraMap B F (Ub x)) := by
  have hpos : 0 < (D.powersetCard m').card := by
    rw [Finset.card_powersetCard]; exact Nat.choose_pos hm'n
  obtain ⟨M, hMmem⟩ := Finset.card_pos.mp hpos
  set z : Fin (m' - K) → B := pre K m' M with hz
  have hMfib : M ∈ fiber D K m' z := Finset.mem_filter.mpr ⟨hMmem, hz.symm⟩
  refine ⟨fun x => (Pz K m' z).eval (x : B), ?_⟩
  show m'.choose m ≤ census D K m (recv (F := F) D K m' z)
  have hc_agree : m' ≤ agreeCard (recv (F := F) D K m' z) (code (F := F) D K m' z M) :=
    code_agrees (F := F) D z hMfib
  have hc0_mem : code (F := F) D K m' z M ∈ RSFinset D K :=
    Finset.mem_filter.mpr ⟨Finset.mem_univ _, code_mem_RS (F := F) hKm' D z hMfib⟩
  calc m'.choose m
      ≤ (agreeCard (recv (F := F) D K m' z) (code (F := F) D K m' z M)).choose m :=
        Nat.choose_le_choose m hc_agree
    _ ≤ ∑ c ∈ RSFinset D K, (agreeCard (recv (F := F) D K m' z) c).choose m :=
        Finset.single_le_sum (f := fun c => (agreeCard (recv (F := F) D K m' z) c).choose m)
          (fun c _ => Nat.zero_le _) hc0_mem
    _ = census D K m (recv (F := F) D K m' z) := rfl

/-- **Interior base-field census floor — explicit ceiling form (below-one regime).** In the
interior below-one regime `binom(n,m') ≤ |𝔹|^{m'-K}` (with `K ≤ m' ≤ n`), the ceiling
`⌈binom(n,m') / |𝔹|^{m'-K}⌉`, written as the `Nat` ceil-division
`(binom(n,m') + |𝔹|^{m'-K} - 1) / |𝔹|^{m'-K}`, equals `1`, so the paper's floor
`⌈binom(n,m') / |𝔹|^{m'-K}⌉ · binom(m',m)` is `binom(m',m)` and is attained by a `𝔹`-valued
received word.  This makes the match to the manuscript's ceiling semantics
(`prop:base-field-floor`, `M_𝔹(d₁)`) syntactic in Lean, and is non-vacuous exactly where the
`⌊·⌋` form of `bc_census_floor` reads `0`. -/
theorem bc_census_floor_ceil_below_one (D : Finset B) (K m m' : ℕ) (hKm' : K ≤ m')
    (hm'n : m' ≤ D.card)
    (hbelow : (D.card).choose m' ≤ (Fintype.card B) ^ (m' - K)) :
    ∃ Ub : D → B,
      (((D.card).choose m' + (Fintype.card B) ^ (m' - K) - 1) / (Fintype.card B) ^ (m' - K))
          * (m'.choose m)
        ≤ census D K m (fun x => algebraMap B F (Ub x)) := by
  obtain ⟨Ub, hUb⟩ := bc_census_floor_pigeonhole (F := F) D K m m' hKm' hm'n
  refine ⟨Ub, ?_⟩
  have ha : 0 < (D.card).choose m' := Nat.choose_pos hm'n
  have hbpos : 0 < (Fintype.card B) ^ (m' - K) := by omega
  have hceil : ((D.card).choose m' + (Fintype.card B) ^ (m' - K) - 1)
      / (Fintype.card B) ^ (m' - K) = 1 := by
    have hsplit : (D.card).choose m' + (Fintype.card B) ^ (m' - K) - 1
        = ((D.card).choose m' - 1) + (Fintype.card B) ^ (m' - K) := by omega
    have hlt : (D.card).choose m' - 1 < (Fintype.card B) ^ (m' - K) := by omega
    rw [hsplit, Nat.add_div_right _ hbpos, Nat.div_eq_of_lt hlt]
  rw [hceil, one_mul]
  exact hUb

/-- **Boundary base-field census floor — positivity (`⌈·⌉ ≥ 1`) form.** The `m' = m` case of
`bc_census_floor_pigeonhole`: for `K ≤ m ≤ n = |D|` there is a `𝔹`-valued received word whose
`m`-th binomial-moment census is at least `1`.  This is the non-vacuous strengthening of
`bc_boundary_census_floor`, whose `⌊binom(n,m) / |𝔹|^{m-K}⌋` form collapses to `0` in the
below-one regime; here `binom(m,m) = 1 ≤ census`, i.e. the decoding list is nonempty
(`prop:subfield-census-floor` (a), ceiling form). -/
theorem bc_boundary_census_floor_pos (D : Finset B) (K m : ℕ) (hKm : K ≤ m)
    (hmn : m ≤ D.card) :
    ∃ Ub : D → B, 1 ≤ census D K m (fun x => algebraMap B F (Ub x)) := by
  obtain ⟨Ub, hUb⟩ := bc_census_floor_pigeonhole (F := F) D K m m hKm hmn
  exact ⟨Ub, by simpa [Nat.choose_self] using hUb⟩

end RSMCA
