import Std

/-!
# M1 `(BETA_2)` reduction-skeleton ledger (stdlib-only)

Banks the two genuinely *arithmetic* pillars of the M1 keystone reduction that was
verified theorem-grade by the 2026-06-30 keystone attack (run `w4poxl3ey`): the
chain `M1AperiodicBound → P_e → ||Γ_e^circ||_F → (BETA_2)` was independently
re-derived with no sign error, and the entire content of M1 now rests on the
single analytic import `(BETA_2)`.

Two reduction steps are pure algebra and are PROVED here, stdlib-only:

* **completing-the-square** behind the closed boundary inequality
  `√(M_e^o) ≤ √(P_e^+) + 3(e−1)√p`. Its algebraic heart is: from
  `Y² ≤ c − s² + 2sY` conclude `(Y − s)² ≤ c` (`complete_square`). The final
  √-extraction `(Y−s)² ≤ c ⇒ Y ≤ s + √c` is standard real monotonicity and is
  the one piece needing `Real` (recorded in the doc, not formalized — stdlib has
  no `Real`/`sqrt`).

* **centering**: the quotient-label weight vector `w = (e−1, −1, …, −1) ∈ ℤ^e`
  is centered, `Σ w = 0` (`wList_sum`) — this is exactly why centering kills the
  principal component `ŵ(𝟙)` in `P_e = p·wᵀΓ_e w`; its squared norm is
  `||w||₂² = e(e−1)`.

The lone remaining obligation — the analytic bound `(BETA_2)`, equivalently the
**obstruction floor** "`F_ψ` has no rank-one `φ⁻¹` Kummer subquotient", i.e.
`H²_c(G_m, F_ψ⊗L_φ)=0` — is NOT finite/stdlib-certifiable (it is an `h²_c`-vanishing
fact, provably invisible to every Euler/conductor ledger, which reach `dim H¹≤3`
only by assuming `h²_c=0`). It is recorded as the typed target
`BetaTwoConductorBound`, exactly like A6's `QuotientFloorBridge`. Everything is
`omega`/`rfl`/`decide`; no
`sorry`/`admit`/`native_decide`.
-/

namespace RsMca.BetaTwo

/-! ### Completing-the-square (the boundary-inequality algebra) -/

/-- The algebraic core of the closed boundary inequality, over `Int`: from
`Y*Y ≤ c − s*s + 2*(s*Y)` conclude `(Y − s)² ≤ c`. (With `Y = √(M_e^o)`,
`s = 3(e−1)√p`, `c = P_e^+`, this is the squared form of
`√(M_e^o) ≤ √(P_e^+) + 3(e−1)√p`.) -/
theorem complete_square (Y s c : Int) (h : Y * Y ≤ c - s * s + 2 * (s * Y)) :
    (Y - s) * (Y - s) ≤ c := by
  have expand : (Y - s) * (Y - s) = Y * Y - 2 * (s * Y) + s * s := by
    rw [Int.sub_mul, Int.mul_sub, Int.mul_sub, Int.mul_comm Y s]; omega
  rw [expand]; omega

-- sanity: `Y=5, s=2, c=9` — `(5−2)²=9 ≤ 9`, and `25 ≤ 9−4+2·10=25`.
example : (5 - 2 : Int) * (5 - 2) ≤ 9 := complete_square 5 2 9 (by decide)

/-! ### Centering: the quotient-label weight vector sums to zero -/

/-- The centering weight vector `w = (d, −1, …, −1) ∈ ℤ^{d+1}` (here `d = e−1`, so
length `e`): one entry `e−1` and `e−1` entries `−1`. -/
def wList (d : Nat) : List Int := (d : Int) :: List.replicate d (-1)

theorem replicate_neg_one_sum (d : Nat) :
    (List.replicate d (-1 : Int)).sum = -(d : Int) := by
  induction d with
  | zero => simp
  | succ k ih => rw [List.replicate_succ, List.sum_cons, ih]; omega

/-- **Centering**: `Σ w = 0`. This is why the principal quotient-character
component drops out of `P_e = p·wᵀΓ_e w`, leaving the centered matrix
`Γ_e^circ`. -/
theorem wList_sum (d : Nat) : (wList d).sum = 0 := by
  rw [wList, List.sum_cons, replicate_neg_one_sum]; omega

-- length is `e = d+1`, and the squared norm `||w||₂² = (e−1)² + (e−1) = e(e−1)`,
-- checked at `e = 4` (d = 3): `3² + 3 = 12 = 4·3`.
example : (wList 3).length = 4 := by decide
example : (wList 3).sum = 0 := by decide
example : ((wList 3).map (fun x => x * x)).sum = 12 := by decide
example : (12 : Int) = 4 * 3 := by decide

/-! ### The lone remaining obligation: `(BETA_2)` (typed target / obstruction floor)

`maxAbsG e p` stands for `max` over nonprincipal quotient-character pairs `(ψ,φ)`
of `|G_{ψ,φ}|` (the good β-pushforward trace at quotient order `e`, prime `p`).
`BetaTwoConductorBound` asserts the bounded-conductor estimate `|G| ≤ C_β(e)·p`.
By the verified reduction this single bound yields `||Γ_e^circ||_F = O_e(p)`,
`P_e = O_e(p²)`, `M_e^o = O_e(p²)`, hence the M1 aperiodic local limit. It is the
obstruction floor (no rank-one `φ⁻¹` Kummer subquotient in `F_ψ`); not provable by
the finite/elementary apparatus, left as the typed analytic target. -/
def BetaTwoConductorBound (maxAbsG : Nat → Nat → Nat) (Cbeta : Nat → Nat) : Prop :=
  ∀ e p : Nat, maxAbsG e p ≤ Cbeta e * p

end RsMca.BetaTwo
