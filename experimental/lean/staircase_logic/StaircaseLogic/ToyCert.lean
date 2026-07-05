import StaircaseLogic.Staircase

namespace StaircaseLogic

/-!
# Decide-certificates: the M1 `A406/A407` adjacent threshold toy

Stdlib-only (no mathlib) instantiation of the abstract staircase layer
(`Staircase.lean`) on the small integers of the committed M1 residual-design
threshold row:

* note: `experimental/notes/m1/m1_a407_a408_residual_design_threshold_v1.md`.

That packet proves, for `C = RS[F_p, H, 256]` with `n = 512`, the exact
finite-slope support-wise numerators (moving-root tangent floor
`LD_sw(C,A) = n - A + 1`)

```text
LD_sw(C, 406) = 107,   LD_sw(C, 407) = 106,   LD_sw(C, 408) = 105,
```

against the `2^-128`-scaled budget

```text
B_* = floor((p-1) / 2^128) = 106,   p = 27168 * 2^120 + 1.
```

The packet's Python verifier owns the *huge-integer* facts (primality of `p` by
Lucas witness `11`, and `floor((p-1)/2^128) = 106`, `106*2^128 < p < 107*2^128`).
This module consumes only the resulting *small* integers `107/106/105` and the
budget `106`, so every certificate is a kernel `decide` on tiny numerals — no
huge integers, no `native_decide`, no mathlib.

The toy uses the minimal `3`-point agreement window `I = [406, 408]` around the
committed adjacent pair.  The abstract theorems of `Staircase.lean` carry the
generality; here they are *instantiated* and the point facts discharged by
`decide`.

`#print axioms` at the foot: every certificate is within `{propext, Quot.sound}`.
-/

open Staircase

/-- The M1 tangent numerator `N(a) = n - a + 1 = 513 - a` at `n = 512`
(`LD_sw(C,a)` in the committed high-agreement/tangent range).  It reproduces the
packet's `107 / 106 / 105` at `a = 406 / 407 / 408` and is globally antitone. -/
def toyN (a : Nat) : Nat := 513 - a

/-- The committed M1 `A406/A407` staircase as an instance of the abstract
`Staircase`.  Interval `I = [406, 408]`, block `n = 512`, budget `B_* = 106`. -/
def toyStair : Staircase where
  N := toyN
  B := 106
  n := 512
  amin := 406
  amax := 408
  hI := by decide
  hn := by decide
  antitone := by intro a a' _ hle _; unfold toyN; omega

/-! ## Point certificates (kernel `decide`) -/

/-- The abstract numerator reproduces the packet's exact `LD_sw` values. -/
theorem toyN_values :
    toyStair.N 406 = 107 ∧ toyStair.N 407 = 106 ∧ toyStair.N 408 = 105 := by decide

/-- Agreement `406` is unsafe (`N = 107 > 106 = B_*`) — the lower certificate
`L(a0) > B_*` of the one-step pair. -/
theorem toy_unsafe_406 : toyStair.Unsafe 406 := by decide

/-- Agreement `407` is safe (`N = 106 ≤ 106 = B_*`) — the upper certificate
`U(a0+1) ≤ B_*` of the one-step pair. -/
theorem toy_safe_407 : toyStair.safe 407 := by decide

/-- Agreement `408` is safe (`N = 105 ≤ 106`), consistent with antitonicity. -/
theorem toy_safe_408 : toyStair.safe 408 := by decide

/-! ## One-step localization: `a_* = 407` -/

/-- **One-step certificate on the toy** (`prop:onestep`).  The adjacent pair
`N 406 = 107 > 106` and `N 407 = 106 ≤ 106` pins the first safe agreement to
`a_* = 407 = 406 + 1`, by the abstract `oneStep_isFirstSafe`. -/
theorem toy_isFirstSafe : toyStair.IsFirstSafe 407 :=
  toyStair.oneStep_isFirstSafe 406 (by decide) (by decide) toy_unsafe_406 toy_safe_407

/-! ## Endpoint / supremum on the toy (`cor:v13-endpoint`) -/

/-- Endpoint arithmetic (`cor:v13-endpoint`), by `decide`: the largest safe
closed integer radius is `r_safe = n - a_* = 105` (grid `105/512`, safe), the
supremum numerator is `106` (fraction `106/512 = 53/256`, not attained), and the
agreement `n - supNum = 406` at that radius has `N = 107 > B_*` (unsafe). -/
theorem toy_endpoint_arith :
    toyStair.rSafe 407 = 105
      ∧ toyStair.supNum 407 = 106
      ∧ toyStair.N (toyStair.n - toyStair.supNum 407) = 107
      ∧ 106 * 256 = 53 * 512 := by decide

/-- The abstract endpoint characterization (`cor:v13-endpoint`, all four parts)
*instantiated* on the toy from `toy_isFirstSafe`. -/
theorem toy_endpoint_supremum :
    toyStair.safe (toyStair.n - toyStair.rSafe 407)
      ∧ toyStair.supNum 407 = toyStair.rSafe 407 + 1
      ∧ toyStair.Unsafe (toyStair.n - toyStair.supNum 407)
      ∧ (∀ a, toyStair.amin ≤ a → a ≤ toyStair.amax → toyStair.safe a →
          toyStair.n - a < toyStair.supNum 407) :=
  toyStair.endpoint_supremum toy_isFirstSafe (by decide)

/-! ## Computable first-safe search, and witness-vs-lemma consistency -/

/-- The computable first-match scan returns `a_* = 407` (kernel `decide`). -/
theorem toy_firstSafe_eval : toyStair.firstSafe = 407 := by decide

/-- **Witness-vs-lemma consistency closure.**  The computable search value
(`firstSafe = 407`) agrees with the abstractly-proven first-safe point
(`IsFirstSafe 407`).  Both equal `a0 + 1 = 407`. -/
theorem toy_consistency :
    toyStair.firstSafe = 407 ∧ toyStair.IsFirstSafe 407 :=
  ⟨toy_firstSafe_eval, toy_isFirstSafe⟩

/-! ## Typed bridge to the packet's finite-slope numerators -/

/-- Typed bridge (`CERTIFICATION_MAP` convention): the abstract numerator and
budget consumed by this toy are exactly the packet's finite-slope support-wise
`LD_sw` values and the `2^-128`-scaled `B_*`.  The huge-integer primality/floor
facts behind `B_* = 106` are the Python verifier's; Lean consumes the small
integers. -/
def M1ThresholdBridge (LDsw : Nat → Nat) (Bstar : Nat) : Prop :=
  LDsw 406 = 107 ∧ LDsw 407 = 106 ∧ LDsw 408 = 105 ∧ Bstar = 106

/-- The toy's numerator/budget satisfy the packet bridge (kernel `decide`). -/
theorem toy_matches_bridge : M1ThresholdBridge toyStair.N toyStair.B := by
  unfold M1ThresholdBridge; decide

/-! ## Axiom audit -/

#print axioms toyN_values
#print axioms toy_unsafe_406
#print axioms toy_safe_407
#print axioms toy_isFirstSafe
#print axioms toy_endpoint_arith
#print axioms toy_endpoint_supremum
#print axioms toy_firstSafe_eval
#print axioms toy_consistency
#print axioms toy_matches_bridge

end StaircaseLogic
