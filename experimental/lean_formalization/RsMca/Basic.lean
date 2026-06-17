import Std

namespace RsMca

/-!
This file is a deliberately small, stdlib-only formalization seed for the
rs-mca project. It records objects that scripts and later theorem statements
can share without importing finite-field or Reed--Solomon libraries yet.
-/

inductive ProofStatus where
  | proved
  | conditional
  | conjectural
  | experimental
  | audit
  | counterexample
  deriving DecidableEq, Repr

namespace ProofStatus

def isFinal : ProofStatus -> Bool
  | proved => true
  | counterexample => true
  | _ => false

theorem proved_isFinal : ProofStatus.isFinal ProofStatus.proved = true := rfl

theorem audit_not_isFinal : ProofStatus.isFinal ProofStatus.audit = false := rfl

end ProofStatus

abbrev Word (D F : Type) := D -> F

def agreesOn {D F : Type} (u v : Word D F) (S : List D) : Prop :=
  forall x, x ∈ S -> u x = v x

def explainedOn {D F : Type} (code : Word D F -> Prop) (u : Word D F)
    (S : List D) : Prop :=
  exists c, code c /\ agreesOn u c S

def pairExplainedOn {D F : Type} (code : Word D F -> Prop) (f g : Word D F)
    (S : List D) : Prop :=
  exists cf, exists cg, code cf /\ code cg /\ agreesOn f cf S /\
    agreesOn g cg S

def lineWord {D F : Type} (combine : F -> F -> F -> F) (f g : Word D F)
    (z : F) : Word D F :=
  fun x => combine (f x) z (g x)

def mcaBadSupport {D F : Type} (code : Word D F -> Prop)
    (combine : F -> F -> F -> F) (f g : Word D F) (z : F)
    (S : List D) : Prop :=
  explainedOn code (lineWord combine f g z) S /\ ¬ pairExplainedOn code f g S

structure QuotientLocatorParams where
  domainOrder : Nat
  quotientOrder : Nat
  fiberSize : Nat
  rank : Nat
  k : Nat
  ell : Nat
  domain_eq : domainOrder = fiberSize * quotientOrder
  k_eq : k = fiberSize * rank
  ell_eq : ell = rank + 1
  deriving Repr

namespace QuotientLocatorParams

def supportSize (p : QuotientLocatorParams) : Nat :=
  p.k + p.fiberSize

theorem supportSize_eq_fiber_mul_ell (p : QuotientLocatorParams) :
    p.supportSize = p.fiberSize * p.ell := by
  calc
    p.supportSize = p.fiberSize * p.rank + p.fiberSize := by
      simp [supportSize, p.k_eq]
    _ = p.fiberSize * (p.rank + 1) := by
      rw [Nat.mul_add, Nat.mul_one]
    _ = p.fiberSize * p.ell := by
      simp [p.ell_eq]

theorem supportSize_gt_k (p : QuotientLocatorParams) (h : 0 < p.fiberSize) :
    p.k < p.supportSize := by
  unfold supportSize
  exact Nat.lt_add_of_pos_right h

end QuotientLocatorParams

structure ScriptCertificate where
  status : ProofStatus
  theoremOrProblem : String
  inputParameters : List (String × String)
  mathematicalObject : List (String × String)
  result : List (String × String)
  proofCertificate : List (String × String)
  deriving Repr

namespace ScriptCertificate

def isProved (c : ScriptCertificate) : Prop :=
  c.status = ProofStatus.proved

def hasTheoremTag (c : ScriptCertificate) : Prop :=
  c.theoremOrProblem.length > 0

end ScriptCertificate

end RsMca
