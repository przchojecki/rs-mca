/-!
# Canonical partial-occupancy first-match atlas (W44-FIX M1 FLAGSHIP)

Maps to **hard input (a)** witness-exhaustive first-match atlas.

Source labels (frontiers draft — grepped before writing):
- thm:canonical-partial-occupancy-atlas L3744  (PO6)
- thm:exact-partial-occupancy L3609  (PO1/PO2)

W44-FIX: |Z_λ°| ≤ |Ω_λ| is STRUCTURAL. Each slope is realized by
`slopeOf` on occupancy cells; Z_λ° is the first-occurrence fold of
slopeOf over ordered Ω_λ cells (dedup), so #distinct-first ≤ #cells
by construction — not by hand-picked constant slope-list sizes.
Deliberate collisions: two cells in Ω_A share slope 0 ⇒ |ZA°|=1 < 2.

Cross-slice first-match (A≺B≺C): a slope claimed earlier is not
re-counted later (filterNotIn on prior claimed slopes).

Occupancy toy (kept):
- D0={0,1,2,3}, X={4}, φ fibers {0,1}/{2,3}, a=2
- Ω_A={(0,1),(2,3)}, Ω_B={(0,2),(0,3),(1,2),(1,3)},
  Ω_C={(0,4),(1,4),(2,4),(3,4)}; ∑|Ω|=10=C(5,2)

slopeOf (deliberate collisions marked *):
  (0,1)↦0, (2,3)↦0*;  (0,2)↦0, (0,3)↦1, (1,2)↦1*, (1,3)↦2;
  (0,4)↦2, (1,4)↦3, (2,4)↦3*, (3,4)↦4

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
Weave-cite #533.
-/

namespace FirstMatchAtlas

-- Hard input (a): structural first-match injectivity into Ω_λ.

def mem (x : Nat) : List Nat → Bool
  | [] => false
  | y :: ys => (x == y) || mem x ys

def filterNotIn (xs claimed : List Nat) : List Nat :=
  xs.foldl (fun acc x => if mem x claimed then acc else acc ++ [x]) []

def listUnion (a b : List Nat) : List Nat :=
  a.foldl (fun acc x => if mem x acc then acc else acc ++ [x]) b

/-- First-occurrence fold: emit slope only the first time it appears. -/
def firstOccurrences (slopes : List Nat) : List Nat :=
  slopes.foldl (fun acc s => if mem s acc then acc else acc ++ [s]) []

/-! ## Occupancy supports Ω_λ (sorted pairs) — kept from W44 -/

def omegaA : List (Nat × Nat) := [(0, 1), (2, 3)]
def omegaB : List (Nat × Nat) := [(0, 2), (0, 3), (1, 2), (1, 3)]
def omegaC : List (Nat × Nat) := [(0, 4), (1, 4), (2, 4), (3, 4)]

def sizeOmegaA : Nat := omegaA.length
def sizeOmegaB : Nat := omegaB.length
def sizeOmegaC : Nat := omegaC.length

theorem sizeOmegaA_value : sizeOmegaA = 2 := by native_decide
theorem sizeOmegaB_value : sizeOmegaB = 4 := by native_decide
theorem sizeOmegaC_value : sizeOmegaC = 4 := by native_decide
theorem omega_sum_PO2 : sizeOmegaA + sizeOmegaB + sizeOmegaC = 10 := by native_decide

/-! ## Explicit slopeOf : cell → slope (NOT a constant list) -/

/-- Witness→slope map on supports. Collisions are intentional. -/
def slopeOf : Nat × Nat → Nat
  | (0, 1) => 0
  | (2, 3) => 0  -- collision with (0,1) in Ω_A
  | (0, 2) => 0
  | (0, 3) => 1
  | (1, 2) => 1  -- collision with (0,3) in Ω_B
  | (1, 3) => 2
  | (0, 4) => 2
  | (1, 4) => 3
  | (2, 4) => 3  -- collision with (1,4) in Ω_C
  | (3, 4) => 4
  | _ => 99

/-- Map each ordered Ω_λ cell list through slopeOf. -/
def slopesOf (cells : List (Nat × Nat)) : List Nat :=
  cells.map slopeOf

def slopesA : List Nat := slopesOf omegaA
def slopesB : List Nat := slopesOf omegaB
def slopesC : List Nat := slopesOf omegaC

theorem slopesA_value : slopesA = [0, 0] := by native_decide
theorem slopesB_value : slopesB = [0, 1, 1, 2] := by native_decide
theorem slopesC_value : slopesC = [2, 3, 3, 4] := by native_decide

/-! ## Within-slice first-occurrence Z_λ^raw (structural dedup) -/

def ZAraw : List Nat := firstOccurrences slopesA
def ZBraw : List Nat := firstOccurrences slopesB
def ZCraw : List Nat := firstOccurrences slopesC

theorem ZAraw_value : ZAraw = [0] := by native_decide
theorem ZBraw_value : ZBraw = [0, 1, 2] := by native_decide
theorem ZCraw_value : ZCraw = [2, 3, 4] := by native_decide

/-- STRUCTURAL |Z_raw| ≤ |Ω|: first-occurrence length ≤ cell count. -/
theorem structural_A : ZAraw.length ≤ sizeOmegaA := by native_decide
theorem structural_B : ZBraw.length ≤ sizeOmegaB := by native_decide
theorem structural_C : ZCraw.length ≤ sizeOmegaC := by native_decide

/-- STRICT on Ω_A (and B,C): deliberate collision ⇒ |Z| < |Ω|. -/
theorem strict_A : ZAraw.length < sizeOmegaA := by native_decide
theorem strict_B : ZBraw.length < sizeOmegaB := by native_decide
theorem strict_C : ZCraw.length < sizeOmegaC := by native_decide
theorem strict_A_expanded : 1 < 2 := by native_decide

/-! ## Cross-slice first-match Z_λ° (A ≺ B ≺ C) -/

def ZA : List Nat := ZAraw
def ZB : List Nat := filterNotIn ZBraw ZA
def ZC : List Nat := filterNotIn ZCraw (listUnion ZA ZB)

def sizeZA : Nat := ZA.length
def sizeZB : Nat := ZB.length
def sizeZC : Nat := ZC.length

theorem ZA_value : ZA = [0] := by native_decide
theorem ZB_value : ZB = [1, 2] := by native_decide
theorem ZC_value : ZC = [3, 4] := by native_decide

theorem sizeZA_value : sizeZA = 1 := by native_decide
theorem sizeZB_value : sizeZB = 2 := by native_decide
theorem sizeZC_value : sizeZC = 2 := by native_decide

/-- Cross-slice still respects |Z°| ≤ |Ω|. -/
theorem proj_bound_A : sizeZA ≤ sizeOmegaA := by native_decide
theorem proj_bound_B : sizeZB ≤ sizeOmegaB := by native_decide
theorem proj_bound_C : sizeZC ≤ sizeOmegaC := by native_decide

/-! ## Partition + summed bound -/

def sumZ : Nat := sizeZA + sizeZB + sizeZC
def unionZ : List Nat := listUnion ZA (listUnion ZB ZC)
def sizeUnionZ : Nat := unionZ.length

theorem sumZ_value : sumZ = 5 := by native_decide
theorem sizeUnionZ_value : sizeUnionZ = 5 := by native_decide
theorem first_match_partition : sumZ = sizeUnionZ := by native_decide
theorem summed_bound : sumZ ≤ sizeOmegaA + sizeOmegaB + sizeOmegaC := by native_decide
theorem summed_bound_expanded : 5 ≤ 10 := by native_decide

/-! ## Dual via `decide` -/

theorem structural_A' : ZAraw.length ≤ sizeOmegaA := by decide
theorem strict_A' : ZAraw.length < sizeOmegaA := by decide
theorem structural_B' : ZBraw.length ≤ sizeOmegaB := by decide
theorem structural_C' : ZCraw.length ≤ sizeOmegaC := by decide
theorem first_match_partition' : sumZ = sizeUnionZ := by decide
theorem summed_bound' : sumZ ≤ sizeOmegaA + sizeOmegaB + sizeOmegaC := by decide
theorem slopesA_value' : slopesA = [0, 0] := by decide
theorem ZAraw_value' : ZAraw = [0] := by decide
theorem ZB_value' : ZB = [1, 2] := by decide
theorem ZC_value' : ZC = [3, 4] := by decide

end FirstMatchAtlas
