namespace L1Threshold

/-!
# QF.10 fiber double-count: an injective-packing counting bound

Stdlib-only (no mathlib) formalization of the **counting skeleton** of the
fiber-side scoped Conjecture F (roadmap QF.10):

* note : `experimental/notes/m1/conjecture_f_fiber_scoped.md` (PR #225, Theorem A).

## The gate this file certifies

For a prefix length `sigma` and reserve `d = j - sigma`, the prefix fiber
`E_p = { S in binom(H,j) : Phi_sigma(S) = p }` obeys (note Theorem A)

    #E_p  <=  binom(n, d) / binom(j, d).

The mechanism (note §3, the shortened-RS MDS / dual-distance argument) is: any
two members `S, S'` of one fiber have locators differing by a polynomial of
degree `<= d - 1`, so they cannot agree on `d` common points — hence **each
`d`-subset of `H` lies in at most one member** of `E_p`. Double-counting the
`d`-subsets: each of the `#E_p` members contains exactly `binom(j,d)` of them and
they are used disjointly, so `#E_p * binom(j,d) <= binom(n,d)`.

This file machine-checks that combinatorial skeleton in a stdlib `List` model of
"finite types" (Lean core has no `Finset`/`Fintype`):

* `double_count` : the injective-packing inequality `#members * b <= T` from
  "each of the `#members` blocks holds `b` distinct tokens, all tokens are
  globally distinct (`Nodup`), and every token lies in a universe of size `T`"
  — the `<= 1 owner` hypothesis of QF.10, via a `Nat`-list pigeonhole;
* `fiber_card_bound` : the division step `E * b <= T  ==>  E <= T / b`;
* `fiber_double_count` / `fiber_bound` : the two combined at `b = binom(j,d)`,
  `T = binom(n,d)`, giving `#E_p <= binom(n,d)/binom(j,d)` verbatim.

The finite-field / MDS content ("each `d`-subset has `<= 1` owner") is the note's
§3 Singleton input; it is recorded as the typed target `SingletonOwnerBound` and
enters here only as the `Nodup` hypothesis on the pooled token list.

No `sorry`, no `native_decide`, no mathlib; `#print axioms` at the foot.
-/

/-! ## Local binomial coefficient (Pascal recursion; `Nat.choose` is mathlib-only) -/

/-- Binomial coefficient by Pascal's recursion (stdlib-only). -/
def choose : Nat → Nat → Nat
  | _,    0    => 1
  | 0,    _+1  => 0
  | n+1, k+1 => choose n k + choose n (k+1)

@[simp] theorem choose_zero_right (n : Nat) : choose n 0 = 1 := by cases n <;> rfl

/-- In range the binomial is positive: `k <= n ==> 0 < choose n k`. -/
theorem choose_pos : ∀ {n k : Nat}, k ≤ n → 0 < choose n k := by
  intro n
  induction n with
  | zero => intro k h; cases k with | zero => decide | succ j => omega
  | succ m ih =>
    intro k h
    cases k with
    | zero => simp
    | succ j =>
      have hjm : j ≤ m := by omega
      have := ih hjm
      simp only [choose]; omega

/-! ## `Nat`-list pigeonhole -/

/-- Pigeonhole: a `Nodup` list of naturals all `< n` has length `<= n`.
    (Core has no `Finset`; this is the counting primitive behind `double_count`.) -/
theorem nodup_lt_length : ∀ (n : Nat) (l : List Nat),
    l.Nodup → (∀ x ∈ l, x < n) → l.length ≤ n := by
  intro n
  induction n with
  | zero =>
    intro l _ hb
    cases l with
    | nil => simp
    | cons a t => exact absurd (hb a (by simp)) (by omega)
  | succ m ih =>
    intro l hnd hb
    by_cases hm : m ∈ l
    · have hnd' : (l.erase m).Nodup := hnd.erase m
      have hb' : ∀ x ∈ l.erase m, x < m := by
        intro x hx
        have h2 := hnd.mem_erase_iff.mp hx
        have := hb x h2.2; omega
      have hlen : (l.erase m).length = l.length - 1 := List.length_erase_of_mem hm
      have hpos : 0 < l.length := List.length_pos_of_mem hm
      have := ih (l.erase m) hnd' hb'; omega
    · have hb' : ∀ x ∈ l, x < m := by
        intro x hx
        have := hb x hx
        have hne : x ≠ m := fun h => hm (h ▸ hx)
        omega
      exact Nat.le_succ_of_le (ih l hnd hb')

/-- When every block has the same length `b`, the pooled (flattened) token list
    has length `#blocks * b`. -/
theorem flatten_length_const (b : Nat) :
    ∀ (blocks : List (List Nat)), (∀ blk ∈ blocks, blk.length = b) →
      blocks.flatten.length = blocks.length * b := by
  intro blocks
  induction blocks with
  | nil => simp
  | cons hd tl ih =>
    intro hall
    have hhd : hd.length = b := hall hd (List.mem_cons.mpr (Or.inl rfl))
    have htl : ∀ blk ∈ tl, blk.length = b := fun blk hb => hall blk (List.mem_cons.mpr (Or.inr hb))
    simp only [List.flatten_cons, List.length_append, hhd, ih htl, List.length_cons,
               Nat.add_mul, Nat.one_mul]
    omega

/-! ## The double-count -/

/-- **Injective-packing double-count.** Model the fiber `E_p` as `blocks`, one
    per member; block `i` lists the `b = binom(j,d)` distinct `d`-subset "tokens"
    that member `i` contains, each token an index `< T = binom(n,d)`. The QF.10
    "each `d`-subset lies in `<= 1` member" hypothesis is exactly that the pooled
    token list `blocks.flatten` is `Nodup`. Then `#members * b <= T`. -/
theorem double_count {blocks : List (List Nat)} {b T : Nat}
    (hconst : ∀ blk ∈ blocks, blk.length = b)
    (hnodup : blocks.flatten.Nodup)
    (hbound : ∀ x ∈ blocks.flatten, x < T) :
    blocks.length * b ≤ T := by
  have hlen := flatten_length_const b blocks hconst
  have hpig := nodup_lt_length T blocks.flatten hnodup hbound
  omega

/-! ## The division step and the QF.10 fiber bound -/

/-- `E * b <= T` and `0 < b` give the sharp quotient bound `E <= T / b`. -/
theorem fiber_card_bound {E b T : Nat} (hb : 0 < b) (h : E * b ≤ T) : E ≤ T / b :=
  (Nat.le_div_iff_mul_le hb).mpr h

/-- **QF.10 Theorem A (fiber bound), skeleton.** With `b = binom(j,d)`,
    `T = binom(n,d)`, the block/token model gives `#E_p <= binom(n,d)/binom(j,d)`
    directly from the `<= 1 owner` (`Nodup`) hypothesis and `d <= j`. -/
theorem fiber_bound {blocks : List (List Nat)} {n j d : Nat} (hdj : d ≤ j)
    (hconst : ∀ blk ∈ blocks, blk.length = choose j d)
    (hnodup : blocks.flatten.Nodup)
    (hbound : ∀ x ∈ blocks.flatten, x < choose n d) :
    blocks.length ≤ choose n d / choose j d :=
  fiber_card_bound (choose_pos hdj) (double_count hconst hnodup hbound)

/-! ## Sanity certificates (kernel `decide`, axiom-free) -/

/-- The local `choose` reproduces the standard values used by QF.10's ratio
    `binom(n,d)/binom(j,d)`, e.g. the reserve-`2` shape `binom(6,2)/binom(4,2)`. -/
theorem choose_values :
    choose 6 2 = 15 ∧ choose 4 2 = 6 ∧ choose 6 2 / choose 4 2 = 2 := by decide

/-- A concrete packing instance: three members, each holding `b = 2` distinct
    tokens drawn `Nodup` from a size-`6` universe, do fit (`3 * 2 = 6 <= 6`). -/
theorem double_count_example :
    ([[0, 1], [2, 3], [4, 5]] : List (List Nat)).length * 2 ≤ 6 := by
  apply double_count (b := 2) (T := 6) <;> decide

/-! ## Typed target — the MDS / dual-distance input NOT proved here

The `<= 1 owner` property (note §3) is the shortened-RS Singleton statement: the
difference code `ev_H(V) = RS_H[n,d]` is MDS, so its dual has minimum distance
`d + 1` and no `d` points of `H` carry a dependence — hence two fiber members
cannot share `d` common points. This needs Reed–Solomon / finite-field
machinery and is outside the stdlib scope; it enters `double_count` /
`fiber_bound` as the `Nodup` hypothesis on the pooled `d`-subset tokens. -/

/-- Interface `Prop`: the `<= 1 owner` hypothesis QF.10 supplies over `F` and this
    file consumes as `blocks.flatten.Nodup`. Recorded as a typed target. -/
def SingletonOwnerBound (blocks : List (List Nat)) : Prop := blocks.flatten.Nodup

/-! ## Axiom audit -/

#print axioms double_count
#print axioms fiber_bound
#print axioms choose_values

end L1Threshold
