/-!
# Unconditional support-envelope bracket (W45 M2)

Maps to **hard input (e)** lower-reserve / unsafe + **(d)** profile-envelope.

Source labels (frontiers draft — grepped before writing):
- thm:unconditional-support-envelope-bracket L6212
- SB1: L(a), P(a), U(a) formulas
- SB2: P(a−)>B* and U(a+)≤B*
- SB3: a− < a* ≤ a+  (and a*=a+ if adjacent)

Toy (exact nested ceilings):
- n=5, k=1, |B|=2, q=11, |Γ|=11, B*=1
- a−=4, a+=5 (adjacent ⇒ a*=5)
- L(4)=⌈C(5,4)/2^(4-1-1)⌉=⌈5/4⌉=2
- inner=⌈L(q−n)/(q−n+k(L−1))⌉=⌈2·6/(6+1)⌉=⌈12/7⌉=2
- P(4)=⌈(|Γ|/q)·inner⌉=⌈11/11·2⌉=2 > B*=1
- U(5)=min(11,C(5,5))=1 ≤ B*=1

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace ThresholdBracket

-- Hard input (e)/(d): target-aware threshold bracket SB2/SB3.

def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n (k + 1) + binom n k

/-- ⌈num/den⌉ for den > 0. -/
def ceilDiv (num den : Nat) : Nat := (num + den - 1) / den

def pow : Nat → Nat → Nat
  | _, 0 => 1
  | b, e + 1 => b * pow b e

def minNat (x y : Nat) : Nat := if x ≤ y then x else y

/-! ## Toy parameters -/

def n : Nat := 5
def k : Nat := 1
def Bsize : Nat := 2
def q : Nat := 11
def Gamma : Nat := 11
def Bstar : Nat := 1

def aMinus : Nat := 4
def aPlus : Nat := 5

/-! ## L(a) = ⌈ C(n,a) / |B|^(a−k−1) ⌉ -/

def Lof (a : Nat) : Nat :=
  ceilDiv (binom n a) (pow Bsize (a - k - 1))

theorem binom_5_4 : binom 5 4 = 5 := by native_decide
theorem binom_5_5 : binom 5 5 = 1 := by native_decide
theorem pow_B_w4 : pow Bsize (aMinus - k - 1) = 4 := by native_decide
theorem L4_value : Lof aMinus = 2 := by native_decide
theorem L4_exact_ceil : ceilDiv 5 4 = 2 := by native_decide

/-! ## Inner ceiling ⌈ L(q−n) / (q−n + k(L−1)) ⌉ -/

def innerCeil (L : Nat) : Nat :=
  ceilDiv (L * (q - n)) (q - n + k * (L - 1))

theorem inner4_value : innerCeil (Lof aMinus) = 2 := by native_decide
theorem inner4_expanded : ceilDiv (2 * 6) (6 + 1 * 1) = 2 := by native_decide
theorem inner4_frac : 12 / 7 = 1 := by native_decide  -- trunc; ceil is 2

/-! ## P(a) = ⌈ (|Γ|/q) · inner ⌉ -/

def Pof (a : Nat) : Nat :=
  ceilDiv (Gamma * innerCeil (Lof a)) q

theorem P4_value : Pof aMinus = 2 := by native_decide
theorem P4_expanded : ceilDiv (11 * 2) 11 = 2 := by native_decide

/-! ## U(a) = min{|Γ|, C(n,a)} -/

def Uof (a : Nat) : Nat := minNat Gamma (binom n a)

theorem U5_value : Uof aPlus = 1 := by native_decide
theorem U4_value : Uof aMinus = 5 := by native_decide

/-! ## SB2 hyp: P(a−) > B* and U(a+) ≤ B* -/

theorem SB2_unsafe : Pof aMinus > Bstar := by native_decide
theorem SB2_safe : Uof aPlus ≤ Bstar := by native_decide
-- SB2 is the conjunction of SB2_unsafe and SB2_safe above.

/-! ## SB3 conclusion: a− < a* ≤ a+; adjacent ⇒ a* = a+ -/

theorem adjacent : aPlus = aMinus + 1 := by native_decide
/-- On this adjacent bracket, a* = a+ = 5. -/
def aStar : Nat := aPlus
theorem SB3_aStar : aStar = 5 := by native_decide
theorem SB3_lower : aMinus < aStar := by native_decide
theorem SB3_upper : aStar ≤ aPlus := by native_decide

/-! ## L/P at a+ for completeness -/

theorem L5_value : Lof aPlus = 1 := by native_decide
theorem P5_value : Pof aPlus = 1 := by native_decide

/-! ## Dual via `decide` -/

theorem L4_value' : Lof aMinus = 2 := by decide
theorem P4_value' : Pof aMinus = 2 := by decide
theorem U5_value' : Uof aPlus = 1 := by decide
theorem SB2_unsafe' : Pof aMinus > Bstar := by decide
theorem SB2_safe' : Uof aPlus ≤ Bstar := by decide
theorem adjacent' : aPlus = aMinus + 1 := by decide
theorem SB3_aStar' : aStar = 5 := by decide

end ThresholdBracket
