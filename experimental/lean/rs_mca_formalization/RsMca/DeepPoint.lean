import RsMca.Basic

namespace RsMca

/-!
# Forward deep-point bridge: definitions and the arithmetic cores

Formalizes (stdlib-only) the quantitative cores of the X1/L2 forward interleaved
deep-point bridge (`notes/x1/x1_deep_point_interleaved_bridge.md`):

* the deep-image membership predicate (§1-§2);
* the `K_{m,m}` clique-amplification cap arithmetic (§2.6 C):
  `n >= k + m^2 (a-k)`, support size `> a`, interleaved `= m^2`;
* the conditional-budget exponent arithmetic (§2.6 R, §2.8):
  the a-regular exponent (1) is `<=` the worst-case exponent (mu).

Finite-field/combinatorial proofs (the identity itself, the a-regular collapse)
are stated as targets elsewhere; here the `Nat`-arithmetic claims are fully
proved by `omega`/core lemmas.
-/

/-- §1-§2: `z` lies in the deep image of `U` at radius `a` if some codeword `p`
    (carried to a word by `toWord`, evaluated at the deep point by `eval`)
    hits `z` and agrees with `U` on a support that the predicate `bigEnough`
    accepts (intended: `|S| >= a`). -/
def deepImageMem {D F P : Type}
    (code : P -> Prop) (toWord : P -> Word D F) (eval : P -> F)
    (U : Word D F) (bigEnough : List D -> Prop) (z : F) : Prop :=
  exists p, code p /\ eval p = z /\
    exists S, bigEnough S /\ agreesOn U (toWord p) S

/-! ## §2.6 (C): the K_{m,m} clique-amplification cap -/

/-- Domain points used by the grid `K_{m,m}` over-agreement design:
    a shared `k`-set plus `m^2` cells of `a-k` fresh points each. -/
def cliqueGridSize (m a k : Nat) : Nat := k + m * m * (a - k)

/-- Row/column support size of the design: the `k`-set plus one grid line. -/
def cliqueSupportSize (m a k : Nat) : Nat := k + m * (a - k)

/-- The interleaved list the design realizes (the complete bipartite `K_{m,m}`
    has `m^2` edges). -/
def cliqueInterleaved (m : Nat) : Nat := m * m

/-- The cap is exactly `n = k + m^2 (a-k)` (definitional, recorded as a fact). -/
theorem cliqueGridSize_eq (m a k : Nat) :
    cliqueGridSize m a k = k + m * m * (a - k) := rfl

/-- Two-sided over-agreement: for `m >= 2` and reserve `a > k`, every support of
    the design has size strictly greater than `a` (so the rows over-agree). -/
theorem cliqueSupport_over_a (m a k : Nat) (hm : 2 ≤ m) (hak : k < a) :
    a < cliqueSupportSize m a k := by
  have hmul : 2 * (a - k) ≤ m * (a - k) := Nat.mul_le_mul_right (a - k) hm
  unfold cliqueSupportSize
  omega

/-- The amplification `m^2` grows with `m`, so a `K_{m,m}` clique needs ever
    larger `n`; equivalently the realized interleaved list is `m^2`. -/
theorem cliqueInterleaved_eq (m : Nat) : cliqueInterleaved m = m * m := rfl

/-- Monotonicity of the grid size in the arity `m`. -/
theorem cliqueGridSize_mono {m m' : Nat} (a k : Nat) (h : m ≤ m') :
    cliqueGridSize m a k ≤ cliqueGridSize m' a k := by
  unfold cliqueGridSize
  have : m * m ≤ m' * m' := Nat.mul_le_mul h h
  exact Nat.add_le_add_left (Nat.mul_le_mul_right (a - k) this) k

/-! ## §2.6 (R) / §2.8: the conditional-budget exponent arithmetic -/

/-- The interleaved-list exponent. a-regular regime: `1`; worst case: `mu`
    (`Lst(Int) <= Lst(C_+)^mu`, `= Lst(C_+)` when a-regular). -/
def listExponent (aRegular : Bool) (mu : Nat) : Nat :=
  if aRegular then 1 else mu

/-- The a-regular exponent never exceeds the worst-case exponent (for `mu >= 1`).
    This is the §2.6 reduction at the level of exponents. -/
theorem listExponent_areg_le_worst (mu : Nat) (hmu : 1 ≤ mu) :
    listExponent true mu ≤ listExponent false mu := by
  simp [listExponent, hmu]

/-- §2.8: with `|F| < 2^logQ` and target `2^-target`, the interleaved soundness
    term `n^{eB}/q = 2^{e*B*m - logQ}` clears `2^-target` exactly when
    `e*B*m <= logQ - target`. -/
def budgetClears (e B m logQ target : Nat) : Prop :=
  e * B * m + target ≤ logQ

/-- Whatever exponent `e <= mu` clears the budget if the worst case (`mu`) does:
    so an L1 bound clearing the budget at `mu` also clears it a-regularly. -/
theorem budgetClears_mono {e e' B m logQ target : Nat} (he : e ≤ e')
    (h : budgetClears e' B m logQ target) : budgetClears e B m logQ target := by
  unfold budgetClears at *
  have : e * B * m ≤ e' * B * m :=
    Nat.mul_le_mul_right m (Nat.mul_le_mul_right B he)
  omega

/-! ## Statements of the deep-point identity and the a-regular collapse

These record the exact claims proved in the notes by finite-field / set
arguments. Their proofs need polynomial-root and finite-set facts (Mathlib) and
are left as formalization targets; the statements are stdlib-only. -/

/-- The bad-slope set of a line at a radius accepted by `bigEnough`. -/
def badSlopeSet {D F : Type} (code : Word D F -> Prop)
    (combine : F -> F -> F -> F) (f g : Word D F) (bigEnough : List D -> Prop)
    (z : F) : Prop :=
  exists S, bigEnough S /\ mcaBadSupport code combine f g z S

/-- §1-§2 deep-point identity (statement): the MCA-bad slopes of the simple-pole
    line equal the deep image.  Target proof: the per-row division
    `Q = (P - P(alpha))/(X - alpha)` plus the global far condition. -/
def DeepPointIdentity {D F P : Type}
    (code : Word D F -> Prop) (combine : F -> F -> F -> F) (f g : Word D F)
    (pcode : P -> Prop) (toWord : P -> Word D F) (eval : P -> F)
    (U : Word D F) (bigEnough : List D -> Prop) : Prop :=
  forall z, badSlopeSet code combine f g bigEnough z <->
            deepImageMem pcode toWord eval U bigEnough z

/-- §2.3 a-regular collapse (statement): in the a-regular regime the worst-case
    interleaved list equals the base-code list (interleaving exponent 1). -/
def ARegularCollapse (interleavedList baseList : Nat) : Prop :=
  interleavedList = baseList

/-! ## §2 / §2.1: the mu-independent collision bound (arithmetic core) -/

/-- Two distinct interleaved tuples differ in some row, so their simultaneous
    deep-point collision count is at most that row's count, hence at most `k`
    (rows being degree-`<= k`).  Core: a subset/`min` bound. -/
theorem simultaneousCollision_le_k {rowCollision simultaneous k : Nat}
    (hsub : simultaneous ≤ rowCollision) (hrow : rowCollision ≤ k) :
    simultaneous ≤ k :=
  Nat.le_trans hsub hrow

/-- The collision bound is `mu`-independent: the same `k` bounds it for every
    arity, since the simultaneous collision only shrinks as rows are added. -/
theorem collision_bound_mu_independent {k : Nat}
    (simultaneous : Nat -> Nat) (rowCollision : Nat)
    (hmono : forall mu, simultaneous mu ≤ rowCollision) (hrow : rowCollision ≤ k) :
    forall mu, simultaneous mu ≤ k :=
  fun mu => Nat.le_trans (hmono mu) hrow

end RsMca
