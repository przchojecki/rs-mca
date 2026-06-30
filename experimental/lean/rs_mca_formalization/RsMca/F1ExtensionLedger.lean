import Std

/-!
# F1: stdlib-only core of the σ=1 extension-line MCA counterexample

Target (Paper B `slackMCA_v4`, direction **F1**; experimental note
`experimental/notes/f1/f1_fixed_rate_extension_counterexample.md`,
verifier `experimental/scripts/verify_f1_fixed_rate_extension_counterexample.py`).

Setup of the proved COUNTEREXAMPLE.  `B = F_p`, `F = B[α]` with `α ∉ B`
(e.g. `α² = d`, `d` a nonsquare, so `F = F_{p²}`), `H = B^*`, `n = p-1`,
`a = k+1`, and the genuinely **extension-valued** line over `H`

    u_z(x) = (x^a - z) / (x - α),     z_S = α^a - L_S(α),

where `L_S = ∏_{s∈S}(X - s)` for an `a`-subset `S ⊆ H`.  Fixing an
`(a-2)`-subset `T ⊆ H`, for distinct `x,y ∈ H\T`

    L_{T∪{x,y}}(α) = C_T·(α² - (x+y)·α + x·y),     C_T = ∏_{t∈T}(α-t) ≠ 0.

Two pairs give the **same slope** iff their `L(α)` values agree; cancelling the
nonzero field element `C_T` and reading off the `{1,α}`-independent components,
this happens iff

    x + y = x' + y'   AND   x·y = x'·y'.

So the only arithmetic content of the σ=1 bad-slope injectivity is:

  * **(independence readout)** the slope determines the base-field pair
    `(e₁,e₂) = (x+y, x·y)` — this is exactly `{1,α}` being `B`-independent; and
  * **(Vieta)** the pair `(x+y, x·y)` determines the unordered pair `{x,y}`.

This file PROVES the Vieta core over `Int` (the integral-domain model of `B =
F_p`; the argument uses only integral-domain axioms, so it transfers verbatim to
`F_p`), packages the readout as `slopeCoord`, and records the resulting distinct
bad-slope count `binom(p-a+1,2)` as a stdlib closed form with `decide` anchors at
the note's `p = 5, 7` rows.  Everything is `omega`/`rfl`/`decide` — no mathlib,
no `sorry`/`admit`/`native_decide`.

The full MCA semantics (support-wise badness + same-support noncontainment of the
line `(x^a-z)/(x-α)`, needing Reed--Solomon/field/polynomial infrastructure) is
left as a typed `Prop` bridge `F1ExtensionSigmaOneBridge`, exactly like A6's
`QuotientFloorBridge`.  The note + Python verifier discharge that semantics over
genuine `F_{p²}` at `p = 5,7,11,13`.
-/

namespace RsMca.F1Ext

/-! ### Vieta core: sum and product determine the unordered pair

Over an integral domain, `x+y = x'+y'` and `x·y = x'·y'` force `{x,y} = {x',y'}`.
We model `B = F_p` by `Int`; the proof uses only that there are no zero divisors
(`Int.mul_eq_zero`). -/

/-- The key factorization, mathlib-free: `(x-x')·(x'-y)` expands to
`x'·(x+y-x') - x·y`.  Both sides normalize to `x'·x + x'·y - x'·x' - x·y`
(products held as atoms; `omega` discharges the linear identity). -/
theorem cross_factor (x y x' : Int) :
    (x - x') * (x' - y) = x' * (x + y - x') - x * y := by
  have hL : (x - x') * (x' - y) = x' * x + x' * y - x' * x' - x * y := by
    rw [Int.sub_mul, Int.mul_sub, Int.mul_sub, Int.mul_comm x x']; omega
  have hR : x' * (x + y - x') - x * y = x' * x + x' * y - x' * x' - x * y := by
    rw [Int.mul_sub, Int.mul_add]
  rw [hL, hR]

/-- **Vieta determination** (unordered form): equal sum and equal product force
the unordered pair to coincide. -/
theorem pair_det (x y x' y' : Int)
    (hs : x + y = x' + y') (hp : x * y = x' * y') :
    (x = x' ∧ y = y') ∨ (x = y' ∧ y = x') := by
  have hy' : y' = x + y - x' := by omega
  have key : (x - x') * (x' - y) = 0 := by
    have hp' : x' * (x + y - x') = x * y := by rw [← hy']; exact hp.symm
    rw [cross_factor, hp', Int.sub_self]
  rcases Int.mul_eq_zero.mp key with hxx' | hx'y
  · left; constructor <;> omega
  · right; constructor <;> omega

/-- **Vieta determination** (ordered/canonical form): on strictly increasing
representatives the swap branch is impossible, so the pair is rigid.  This is the
form used for counting distinct bad slopes. -/
theorem pair_det_lt (x y x' y' : Int)
    (hxy : x < y) (hxy' : x' < y')
    (hs : x + y = x' + y') (hp : x * y = x' * y') :
    x = x' ∧ y = y' := by
  rcases pair_det x y x' y' hs hp with h | h
  · exact h
  · -- x = y', y = x'  ⇒  y' = x < y = x', contradicting x' < y'
    obtain ⟨hx_eq, hy_eq⟩ := h
    omega

/-! ### Independence readout

The slope of the σ=1 line through `T∪{x,y}` records exactly the base-field pair
`(e₁,e₂) = (x+y, x·y)`.  Encoding `F = B ⊕ B·α` as `Int × Int` (so `{1,α}`
independence is componentwise equality of pairs), the readout map is: -/

/-- Base-field readout of the σ=1 slope: `(x+y, x·y)`. -/
def slopeCoord (x y : Int) : Int × Int := (x + y, x * y)

/-- Distinct ordered pairs have distinct slope readouts — the σ=1 bad-slope
injectivity, reduced to its Vieta core. -/
theorem slopeCoord_inj_lt {x y x' y' : Int}
    (hxy : x < y) (hxy' : x' < y')
    (h : slopeCoord x y = slopeCoord x' y') :
    x = x' ∧ y = y' := by
  have hs : x + y = x' + y' := congrArg Prod.fst h
  have hp : x * y = x' * y' := congrArg Prod.snd h
  exact pair_det_lt x y x' y' hxy hxy' hs hp

/-! ### Distinct bad-slope count

The injective readout sends the `binom(|H\T|,2)` unordered pairs of `H\T` to
distinct slopes.  With `D = H = F_p^*`, `|H\T| = (p-1)-(a-2) = p-a+1`, so the
line has at least `binom(p-a+1,2)` distinct bad slopes and

    emca(C_F, 1-a/n) ≥ binom(p-a+1, 2) / |F|.

We record the count closed form `binom(m,2) = m(m-1)/2` and the note's published
rows; the link to `emca` is the typed bridge below. -/

/-- `binom(m,2) = m(m-1)/2` (the number of unordered pairs of an `m`-set). -/
def binom2 (m : Nat) : Nat := m * (m - 1) / 2

/-- Distinct σ=1 bad-slope lower bound for `D = H = F_p^*` at agreement `a`:
`binom(p-a+1, 2)`. -/
def sigmaOneBadSlopeBound (p a : Nat) : Nat := binom2 (p - a + 1)

-- Note row `p=5`, rate `1/2`: `k=2`, `a=3`, bound `binom(3,2)=3`.
example : sigmaOneBadSlopeBound 5 3 = 3 := by decide
-- Note row `p=7`, rate `1/2`: `k=3`, `a=4`, bound `binom(4,2)=6`.
example : sigmaOneBadSlopeBound 7 4 = 6 := by decide
-- Note rows `p=11,13`, rate `1/2`.
example : sigmaOneBadSlopeBound 11 6 = 15 := by decide
example : sigmaOneBadSlopeBound 13 7 = 21 := by decide

-- Triangular recurrence `binom2 (m+1) = binom2 m + m`, checked concretely.
example : binom2 4 = binom2 3 + 3 := by decide
example : binom2 7 = binom2 6 + 6 := by decide

/-! ### Genuine `F_{p²}` anchor at `p = 5`

To check the readout is faithful to the *actual* field (not just the `Int`
model), we evaluate the σ=1 slopes over `F_25 = F_5[α]`, `α² = 2` (`2` is a
nonsquare mod `5`).  Encode `c₀ + c₁α` as `(c₀, c₁) : Fin5 × Fin5`. -/

abbrev GF5 := Fin 5
/-- Element of `F_25` as `(lo, hi) = lo + hi·α`, `α² = 2`. -/
abbrev GF25 := GF5 × GF5

/-- Multiplication in `F_25` with `α² = 2`: `(a+bα)(c+dα) = (ac+2bd)+(ad+bc)α`. -/
def mul25 (u v : GF25) : GF25 :=
  (u.1 * v.1 + 2 * (u.2 * v.2), u.1 * v.2 + u.2 * v.1)

/-- Evaluate the σ=1 slope readout `(x+y) , (x·y)` of a base pair, embedded into
`F_25` as the coefficient pair `(α² - (x+y)α + xy)` data — here just the
base-field coordinates `(x·y, -(x+y))` ∈ `F_5 × F_5`. -/
def slopeCoord25 (x y : GF5) : GF25 := (x * y, -(x + y))

-- The three σ=1 pairs of `H\T` for `p=5, a=3` (T a singleton, |H\T|=3) read off
-- to three DISTINCT `F_25` coordinates — the finite witness of `slopeCoord_inj_lt`.
example :
    let s12 := slopeCoord25 1 2
    let s13 := slopeCoord25 1 3
    let s23 := slopeCoord25 2 3
    s12 ≠ s13 ∧ s12 ≠ s23 ∧ s13 ≠ s23 := by decide

-- `mul25` really squares `α = (0,1)` to `2 = (2,0)`.
example : mul25 (0, 1) (0, 1) = (2, 0) := by decide

/-! ### Typed bridge to full MCA semantics (unproved target)

`F1ExtensionSigmaOneBridge` packages the remaining, non-stdlib obligation: that
each distinct readout above is a genuine **support-wise MCA-bad, non-contained**
slope of the extension line `(x^a - z)/(x - α)` for `C_F = RS[F,H,k]`.  Proving it
(over real `F`, with polynomial/RS infrastructure) together with
`slopeCoord_inj_lt` yields `emca(C_F, 1-a/n) ≥ binom(p-a+1,2)/|F|`.  It is left
unproved here and discharged numerically by the F1 Python verifier. -/

/-- Predicate stand-in: `isBadNoncontained p a z` asserts `z` is a support-wise
MCA-bad, same-support-non-contained slope of the σ=1 extension line at
`(p, a)`.  (Opaque here; defined by the RS semantics in the note.) -/
def F1ExtensionSigmaOneBridge
    (isBadNoncontained : Nat → Nat → (GF5 → GF5 → Prop)) : Prop :=
  ∀ p a : Nat, ∀ x y : GF5, isBadNoncontained p a x y

end RsMca.F1Ext
