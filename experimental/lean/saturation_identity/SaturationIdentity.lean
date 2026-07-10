/-!
# Exact saturation identity instance (W40 M1)

Kernel-checked instance of thm:saturation (grande_finale):

```text
  Cen(U; m) = ∑_c binom(s_c(U), m)
```

where s_c(U) = |{x ∈ D : U(x) = c(x)}| and C = RS[F,D,K].

Explicit toy over F_5 with K=1 (constants only):
- D = {0,1,2,3,4}, n = 5
- U = (0,0,0,1,1)  (values at 0..4)
- Codewords: constants c_a(x) = a for a ∈ F_5
- Agreements: s_{c_0}=3, s_{c_1}=2, s_{c_a}=0 for a∉{0,1}
- m = 2
- RHS = C(3,2)+C(2,2)+0+0+0 = 3+1 = 4
- LHS: m-sets T where U is constant on T
    pairs from {0,1,2}: C(3,2)=3; pair {3,4}: 1 → Cen=4

Disjoint from experimental/lean/saturation_toys (W24 bare binoms).
No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace SaturationIdentity

/-- C(n,2) for Nat. -/
def binom2 (n : Nat) : Nat := (n * (n - 1)) / 2

/-- Recursive binomial (for general m if needed). -/
def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n (k + 1) + binom n k

def n : Nat := 5
def m : Nat := 2
def K : Nat := 1

/-- Domain indices 0..4. -/
def D : List Nat := [0, 1, 2, 3, 4]

/-- Received word U as a function D → F_5 (stored as list of values). -/
def Uvals : List Nat := [0, 0, 0, 1, 1]

def U (x : Nat) : Nat :=
  match x with
  | 0 => 0
  | 1 => 0
  | 2 => 0
  | 3 => 1
  | 4 => 1
  | _ => 0

/-- Constant codeword c_a (independent of domain point). -/
def codeword (a : Nat) (_x : Nat) : Nat := a % 5

/-- Agreement size s_{c_a}(U). -/
def s_c (a : Nat) : Nat :=
  D.foldl (fun acc x => if U x == codeword a x then acc + 1 else acc) 0

/-- RHS of thm:saturation: ∑_a C(s_c(a), m). -/
def censusRHS : Nat :=
  let as : List Nat := [0, 1, 2, 3, 4]
  as.foldl (fun acc a => acc + binom (s_c a) m) 0

/-- All unordered pairs (i,j) with i < j on D. -/
def pairs : List (Nat × Nat) :=
  [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

/-- An m-set {i,j} is explained by a constant iff U i = U j. -/
def explained (p : Nat × Nat) : Bool := U p.1 == U p.2

/-- LHS: Cen(U;2) by enumeration of size-2 supports. -/
def censusLHS : Nat :=
  pairs.foldl (fun acc p => if explained p then acc + 1 else acc) 0

/-! ## Agreement sizes -/

theorem s_c0 : s_c 0 = 3 := by native_decide
theorem s_c1 : s_c 1 = 2 := by native_decide
theorem s_c2 : s_c 2 = 0 := by native_decide
theorem s_c3 : s_c 3 = 0 := by native_decide
theorem s_c4 : s_c 4 = 0 := by native_decide

/-! ## Binomial table -/

theorem binom_3_2 : binom 3 2 = 3 := by native_decide
theorem binom_2_2 : binom 2 2 = 1 := by native_decide
theorem binom_0_2 : binom 0 2 = 0 := by native_decide

/-! ## Main identity Cen = ∑ binom(s_c, m) -/

theorem censusRHS_value : censusRHS = 4 := by native_decide
theorem censusLHS_value : censusLHS = 4 := by native_decide

/-- Exact saturation identity on this instance. -/
theorem saturation_identity_instance : censusLHS = censusRHS := by native_decide

/-- Expanded form: C(3,2)+C(2,2)=4. -/
theorem expanded_rhs : binom 3 2 + binom 2 2 = 4 := by native_decide

/-- Pair count matches C(n,2). -/
theorem n_pairs : pairs.length = binom2 n := by native_decide
theorem n_pairs_value : pairs.length = 10 := by native_decide

/-! ## Dual via `decide` -/

theorem s_c0' : s_c 0 = 3 := by decide
theorem s_c1' : s_c 1 = 2 := by decide
theorem censusRHS_value' : censusRHS = 4 := by decide
theorem censusLHS_value' : censusLHS = 4 := by decide
theorem saturation_identity_instance' : censusLHS = censusRHS := by decide
theorem expanded_rhs' : binom 3 2 + binom 2 2 = 4 := by decide

end SaturationIdentity
