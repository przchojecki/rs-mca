/-!
# Integer staircase / identity-profile scale (W42 M1)

Maps to **hard input (d)** complete profile-envelope comparison
(the identity staircase scale is the profile numerator budget).

Source label (frontiers draft):
`def:integer-staircase-detail` (L6667):
  At agreement a = K+w, the identity profile has scale
    barN_1 = binom(n,a) · |B|^(-w).
  It is a safe numerator budget only after the full profile envelope
  is e^{o(n)} barN_1 (envelope hypothesis not claimed here).

Explicit toy:
- n=8, K=3, w=2 ⇒ a = K+w = 5
- |B|=2 ⇒ barN_1 = C(8,5) / 2^2 = 56 / 4 = 14
- Exact division: C(8,5) = 14 · 4
- Second step w=1, a=4: barN_1 = C(8,4)/2 = 70/2 = 35

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Weave-cite grande_finale Frontier/SP named tree (citation only).
-/

namespace IntegerStaircase

-- Hard input (d): profile-envelope / identity staircase scale.

def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n (k + 1) + binom n k

def pow : Nat → Nat → Nat
  | _, 0 => 1
  | b, n + 1 => b * pow b n

/-! ## def:integer-staircase-detail instance -/

def n : Nat := 8
def K : Nat := 3
def w : Nat := 2
def a : Nat := K + w
def Bsize : Nat := 2

/-- Identity-profile scale barN_1 = binom(n,a) / |B|^w. -/
def barN1 : Nat := binom n a / pow Bsize w

theorem a_eq_K_plus_w : a = K + w := by native_decide
theorem a_value : a = 5 := by native_decide
theorem binom_8_5 : binom 8 5 = 56 := by native_decide
theorem pow_B_w : pow Bsize w = 4 := by native_decide
theorem barN1_value : barN1 = 14 := by native_decide

/-- Exact identity-scale division (definitional form). -/
theorem barN1_exact : binom n a = barN1 * pow Bsize w := by native_decide
theorem barN1_pos : barN1 > 0 := by native_decide

/-- Second step: w=1, a=K+1=4, barN_1 = C(8,4)/2 = 70/2 = 35. -/
def w2 : Nat := 1
def a2 : Nat := K + w2
def barN1_w1 : Nat := binom n a2 / pow Bsize w2

theorem a2_value : a2 = 4 := by native_decide
theorem barN1_w1_value : barN1_w1 = 35 := by native_decide
theorem barN1_w1_exact : binom n a2 = barN1_w1 * pow Bsize w2 := by native_decide

/-! ## Dual via `decide` -/

theorem a_eq_K_plus_w' : a = K + w := by decide
theorem barN1_value' : barN1 = 14 := by decide
theorem barN1_exact' : binom n a = barN1 * pow Bsize w := by decide
theorem barN1_w1_value' : barN1_w1 = 35 := by decide

end IntegerStaircase
