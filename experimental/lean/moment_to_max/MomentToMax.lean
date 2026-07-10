/-!
# Q-to-SP moment-to-max transfer (W42 M2)

Maps to **hard input (b)** image-scale MI+MA (max-fiber → second-moment
scale needed by SP / image-scale payment).

Source label (frontiers draft):
`lem:q-to-sp-detail` (L6659):
  If max_z N(z) ≤ κ · N̄, then M^{-1} ∑_z N(z)² ≤ κ · N̄.
  Proof form used: ∑ N² ≤ κ · N̄ · M.

Complementary to #551 (lem:largest-fiber-log-detail q=2 upper
∑N² ≤ maxN·M) and #548 (∑Q² identity): here the transfer is through
the normalized max κ = maxN / N̄.

Explicit toy:
- Fiber sizes N = [6, 3, 3]
- M = ∑N = 12, L = 3, N̄ = M/L = 4
- maxN = 6, take κ = 2 (hypothesis: 6 ≤ 2·4)
- Conclusion: ∑N² = 36+9+9 = 54 ≤ κ·N̄·M = 2·4·12 = 96

Tight case: N=[8], M=8, N̄=8, κ=1 ⇒ ∑N²=64 = κ·N̄·M.

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Weave-cite grande_finale/QEntropyInverse + #548/#551.
-/

namespace MomentToMax

-- Hard input (b): image-scale MI+MA / max-to-SP transfer.

def sumList (xs : List Nat) : Nat :=
  xs.foldl (fun acc x => acc + x) 0

def sumSq (xs : List Nat) : Nat :=
  xs.foldl (fun acc x => acc + x * x) 0

def maxList : List Nat → Nat
  | [] => 0
  | x :: xs => Nat.max x (maxList xs)

/-! ## Primary toy: N=[6,3,3], κ=2, N̄=4 -/

def N : List Nat := [6, 3, 3]
def Mtot : Nat := sumList N
def L : Nat := N.length
def barN : Nat := Mtot / L
def maxN : Nat := maxList N
def kappa : Nat := 2
def sumN2 : Nat := sumSq N

theorem Mtot_value : Mtot = 12 := by native_decide
theorem L_value : L = 3 := by native_decide
theorem barN_value : barN = 4 := by native_decide
theorem barN_exact : Mtot = barN * L := by native_decide
theorem maxN_value : maxN = 6 := by native_decide
theorem sumN2_value : sumN2 = 54 := by native_decide

/-- Hypothesis of lem:q-to-sp-detail: max N ≤ κ · N̄. -/
theorem hyp_max_le_kappa_barN : maxN ≤ kappa * barN := by native_decide
theorem hyp_expanded : 6 ≤ 2 * 4 := by native_decide

/-- Conclusion (cleared denominator): ∑ N² ≤ κ · N̄ · M. -/
theorem q_to_sp_conclusion : sumN2 ≤ kappa * barN * Mtot := by native_decide
theorem q_to_sp_expanded : 54 ≤ 2 * 4 * 12 := by native_decide

/-- Normalized form: ∑N² · L ≤ κ · M · M  when N̄=M/L
    i.e. ∑N² ≤ κ · M² / L, cleared: ∑N² * L ≤ κ * M². -/
theorem q_to_sp_cleared : sumN2 * L ≤ kappa * Mtot * Mtot := by native_decide
theorem q_to_sp_cleared_expanded : 54 * 3 ≤ 2 * 12 * 12 := by native_decide

/-! ## Tight single-fiber case: κ=1, equality -/

def N1 : List Nat := [8]
def M1 : Nat := sumList N1
def barN1 : Nat := M1 / N1.length
def maxN1 : Nat := maxList N1
def kappa1 : Nat := 1
def sumN2_1 : Nat := sumSq N1

theorem tight_hyp : maxN1 ≤ kappa1 * barN1 := by native_decide
theorem tight_concl : sumN2_1 ≤ kappa1 * barN1 * M1 := by native_decide
theorem tight_eq : sumN2_1 = kappa1 * barN1 * M1 := by native_decide

/-! ## Distinct from bare max·M bound (#551 form) -/

/-- #551-style bound still holds: ∑N² ≤ maxN · M. -/
theorem bare_max_bound : sumN2 ≤ maxN * Mtot := by native_decide

/-- κ·N̄ can be strictly larger than maxN when κ is a loose upper. -/
def kappaLoose : Nat := 3
theorem loose_hyp : maxN ≤ kappaLoose * barN := by native_decide
theorem loose_concl : sumN2 ≤ kappaLoose * barN * Mtot := by native_decide
theorem kappa_bar_vs_max : kappa * barN ≥ maxN := by native_decide

/-! ## Dual via `decide` -/

theorem hyp_max_le_kappa_barN' : maxN ≤ kappa * barN := by decide
theorem q_to_sp_conclusion' : sumN2 ≤ kappa * barN * Mtot := by decide
theorem q_to_sp_cleared' : sumN2 * L ≤ kappa * Mtot * Mtot := by decide
theorem tight_eq' : sumN2_1 = kappa1 * barN1 * M1 := by decide
theorem bare_max_bound' : sumN2 ≤ maxN * Mtot := by decide

end MomentToMax
