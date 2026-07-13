import Mathlib

/-!
# Selector-free direction-distance bounds for all syndrome-line pairs

This module contains only **UNPROVED STATEMENT TARGETS**.  It records the
self-contained generic interfaces for counting every retained `(slope,error)`
pair, including same-slope multiplicity, without a witness selector or a full
punctured affine-coset list.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace DirectionDistanceAllPairs

set_option autoImplicit false

universe u v w

variable {D : Type u} {F : Type v} {W : Type w}
variable [Fintype D] [DecidableEq D]
variable [Field F] [DecidableEq F]
variable [AddCommGroup W] [Module F W]

abbrev SlopeErrorPair (D : Type u) (F : Type v) := F × (D → F)

def wordSupport (z : D → F) : Finset D :=
  Finset.univ.filter fun x => z x ≠ 0

def weight (z : D → F) : ℕ :=
  (wordSupport z).card

def SupportedIn (S : Finset D) (z : D → F) : Prop :=
  ∀ x, x ∉ S → z x = 0

def InSupportImage (H : (D → F) →ₗ[F] W) (e : D → F) (y : W) : Prop :=
  ∃ z : D → F, SupportedIn (wordSupport e) z ∧ H z = y

def wordDifferences {I : Type*} (P : Finset I) (err : I → D → F) :
    Set (D → F) :=
  {z | ∃ p ∈ P, ∃ q ∈ P, z = err p - err q}

def affineDirectionSpan {I : Type*} (P : Finset I) (err : I → D → F) :
    Submodule F (D → F) :=
  Submodule.span F (wordDifferences P err)

def affineRank {I : Type*} (P : Finset I) (err : I → D → F) : ℕ :=
  Module.finrank F (affineDirectionSpan P err)

/-! ## Hosted pair data -/

def BasicPairHypotheses (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  y₁ ≠ 0 ∧
    (∀ p ∈ P, H p.2 = y₀ + p.1 • y₁) ∧
    (∀ p ∈ P, weight p.2 ≤ t)

/-- Explicit lifts of both hosted syndromes, with `v` minimum among lifts of `y₁`. -/
def HostedMinimumLift (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) : Prop :=
  H b₀ = y₀ ∧ H v = y₁ ∧
    ∀ z : D → F, H z = y₁ → weight v ≤ weight z

def KernelDistanceAtLeast (H : (D → F) →ₗ[F] W) (d : ℕ) : Prop :=
  ∀ z : D → F, H z = 0 → z ≠ 0 → d ≤ weight z

def PairTransverse (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) : Prop :=
  ∀ p ∈ P,
    ¬ (InSupportImage H p.2 y₀ ∧ InSupportImage H p.2 y₁)

/-! ## Realized puncture words and clusters -/

def outsideCoords (J : Finset D) : Finset D :=
  Finset.univ \ J

def punctureOutside (J : Finset D) (z : D → F) : D → F :=
  fun x => if x ∈ J then 0 else z x

def PunctureInjectiveOnKernel (H : (D → F) →ₗ[F] W)
    (J : Finset D) : Prop :=
  ∀ z : D → F, H z = 0 → punctureOutside J z = 0 → z = 0

def PuncturedKernelDistanceAtLeast (H : (D → F) →ₗ[F] W)
    (J : Finset D) (Δ : ℕ) : Prop :=
  ∀ z : D → F, H z = 0 → z ≠ 0 →
    Δ ≤ weight (punctureOutside J z)

def baseWord (v : D → F) (p : SlopeErrorPair D F) : D → F :=
  p.2 - p.1 • v

def pairPuncture (v : D → F) (p : SlopeErrorPair D F) : D → F :=
  punctureOutside (wordSupport v) (baseWord v p)

/-- The realized set `W_P`, formed by `Finset.image`, not the full affine coset. -/
def realizedWords (P : Finset (SlopeErrorPair D F)) (v : D → F) :
    Finset (D → F) :=
  P.image (pairPuncture v)

def realizedCluster (P : Finset (SlopeErrorPair D F)) (v : D → F)
    (w : D → F) : Finset (SlopeErrorPair D F) :=
  P.filter fun p => pairPuncture v p = w

def puncturedPair (v : D → F) (p : SlopeErrorPair D F) :
    F × (D → F) :=
  (p.1, pairPuncture v p)

def clusterHeight (d t : ℕ) (w : D → F) : ℕ :=
  max 1 (d + weight w - t)

def weightedPunctureBudget (P : Finset (SlopeErrorPair D F))
    (v : D → F) (t : ℕ) : ℕ :=
  ∑ w ∈ realizedWords P v,
    weight v / clusterHeight (weight v) t w

def LowExactHypotheses (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  BasicPairHypotheses H y₀ y₁ P t ∧
    HostedMinimumLift H y₀ y₁ b₀ v ∧
    PairTransverse H y₀ y₁ P ∧
    PunctureInjectiveOnKernel H (wordSupport v)

/-! ## Component targets -/

def ballCodeword (b₀ : D → F) (p : SlopeErrorPair D F) : D → F :=
  b₀ - p.2

/-- **UNPROVED STATEMENT TARGET (all-pair injection).** -/
def allPairInjectionTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  BasicPairHypotheses H y₀ y₁ P t →
    HostedMinimumLift H y₀ y₁ b₀ v →
    Set.InjOn (ballCodeword b₀) (↑P : Set (SlopeErrorPair D F))

/-- **UNPROVED STATEMENT TARGET (punctured-pair injection).** -/
def puncturedPairInjectionTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  LowExactHypotheses H y₀ y₁ b₀ v P t →
    Set.InjOn (puncturedPair v) (↑P : Set (SlopeErrorPair D F))

/-- **UNPROVED STATEMENT TARGET (same-word distinct slopes).** -/
def sameWordDistinctSlopesTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  LowExactHypotheses H y₀ y₁ b₀ v P t →
    ∀ w ∈ realizedWords P v,
      Set.InjOn (fun p : SlopeErrorPair D F => p.1)
        (↑(realizedCluster P v w) : Set (SlopeErrorPair D F))

def ClusterFloorConclusion (P : Finset (SlopeErrorPair D F))
    (v : D → F) (t : ℕ) : Prop :=
  ∀ w ∈ realizedWords P v,
    (realizedCluster P v w).card * clusterHeight (weight v) t w ≤ weight v ∧
    (realizedCluster P v w).card ≤
      weight v / clusterHeight (weight v) t w

/-- **UNPROVED STATEMENT TARGET (realized cluster floor).** -/
def realizedClusterFloorTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  LowExactHypotheses H y₀ y₁ b₀ v P t → ClusterFloorConclusion P v t

def ExactWeightedConclusion (P : Finset (SlopeErrorPair D F))
    (v : D → F) (t : ℕ) : Prop :=
  P.card = ∑ w ∈ realizedWords P v, (realizedCluster P v w).card ∧
    P.card ≤ weightedPunctureBudget P v t

/-- **UNPROVED STATEMENT TARGET (exact selector-free weighted budget).** -/
def exactWeightedBudgetTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  LowExactHypotheses H y₀ y₁ b₀ v P t → ExactWeightedConclusion P v t

def RealizedRankConclusion (P : Finset (SlopeErrorPair D F))
    (v : D → F) : Prop :=
  let Wp := realizedWords P v
  affineRank P (fun p => p.2) ≤ Wp.card ∧
    (P.Nonempty →
      affineRank P (fun p => p.2) ≤ affineRank Wp id + 1 ∧
      affineRank Wp id + 1 ≤ Wp.card)

/-- **UNPROVED STATEMENT TARGET (`sigma ≤ L`, with realized-rank refinement).** -/
def realizedRankTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  LowExactHypotheses H y₀ y₁ b₀ v P t → RealizedRankConclusion P v

/-! ## Subtraction-safe high and low conclusions -/

def highDenominator (N t d : ℕ) : ℕ :=
  (N - t) ^ 2 - N * (N - d)

def highNumerator (N t d : ℕ) : ℕ :=
  N * ((N - t) - (N - d))

def HighPositive (N t d : ℕ) : Prop :=
  N * (N - d) < (N - t) ^ 2

def HighDirectionConclusion (P : Finset (SlopeErrorPair D F))
    (t d : ℕ) : Prop :=
  let N := Fintype.card D
  let den := highDenominator N t d
  let num := highNumerator N t d
  P.card * den ≤ num ∧ P.card ≤ num / den

/-- **UNPROVED STATEMENT TARGET (all-pair high-direction bound).** -/
def pairHighDirectionTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  BasicPairHypotheses H y₀ y₁ P t →
    HostedMinimumLift H y₀ y₁ b₀ v →
    KernelDistanceAtLeast H (weight v) →
    HighPositive (Fintype.card D) t (weight v) →
    HighDirectionConclusion P t (weight v)

def lowDenominator (M ρ Δ : ℕ) : ℕ :=
  (M - ρ) ^ 2 - M * (M - Δ)

def lowNumerator (M ρ Δ : ℕ) : ℕ :=
  M * ((M - ρ) - (M - Δ))

def LowPositive (M ρ Δ : ℕ) : Prop :=
  M * (M - Δ) < (M - ρ) ^ 2

def LowDirectionConclusion (P : Finset (SlopeErrorPair D F))
    (v : D → F) (t Δ : ℕ) : Prop :=
  let Wp := realizedWords P v
  let d := weight v
  let M := (outsideCoords (wordSupport v)).card
  let ρ := min t M
  let den := lowDenominator M ρ Δ
  let num := lowNumerator M ρ Δ
  Wp.card * den ≤ num ∧ Wp.card ≤ num / den ∧
    P.card ≤ d * Wp.card ∧ P.card ≤ d * (num / den)

/-- **UNPROVED STATEMENT TARGET (realized zero-set Johnson inequality).** -/
def realizedZeroSetJohnsonTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F))
    (t Δ : ℕ) : Prop :=
  let M := (outsideCoords (wordSupport v)).card
  let ρ := min t M
  LowExactHypotheses H y₀ y₁ b₀ v P t →
    PuncturedKernelDistanceAtLeast H (wordSupport v) Δ →
    Δ ≤ M → LowPositive M ρ Δ → LowDirectionConclusion P v t Δ

/-- **UNPROVED STATEMENT TARGET (complete all-pair low-direction wrapper).** -/
def pairLowDirectionTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ v : D → F) (P : Finset (SlopeErrorPair D F))
    (t Δ : ℕ) : Prop :=
  let M := (outsideCoords (wordSupport v)).card
  let ρ := min t M
  LowExactHypotheses H y₀ y₁ b₀ v P t →
    PuncturedKernelDistanceAtLeast H (wordSupport v) Δ →
    Δ ≤ M → LowPositive M ρ Δ →
    ExactWeightedConclusion P v t ∧ RealizedRankConclusion P v ∧
      LowDirectionConclusion P v t Δ

/-! ## Direct LineRay transfer targets -/

def lineRayError (u vLine : D → F) (p : SlopeErrorPair D F) : D → F :=
  u + p.1 • vLine - p.2

def lineRayPairMap (u vLine : D → F) (p : SlopeErrorPair D F) :
    SlopeErrorPair D F :=
  (p.1, lineRayError u vLine p)

def lineRaySyndromePairs (u vLine : D → F)
    (P : Finset (SlopeErrorPair D F)) : Finset (SlopeErrorPair D F) :=
  P.image (lineRayPairMap u vLine)

def BasicLineRayHypotheses (H : (D → F) →ₗ[F] W) (u vLine : D → F)
    (P : Finset (SlopeErrorPair D F)) (t : ℕ) : Prop :=
  H vLine ≠ 0 ∧ (∀ p ∈ P, H p.2 = 0) ∧
    (∀ p ∈ P, weight (lineRayError u vLine p) ≤ t)

def LineRayTransverse (H : (D → F) →ₗ[F] W) (u vLine : D → F)
    (P : Finset (SlopeErrorPair D F)) : Prop :=
  ∀ p ∈ P,
    ¬ (InSupportImage H (lineRayError u vLine p) (H u) ∧
      InSupportImage H (lineRayError u vLine p) (H vLine))

/-- **UNPROVED STATEMENT TARGET (LineRay pair-map injection).** -/
def lineRayPairInjectionTarget (u vLine : D → F)
    (P : Finset (SlopeErrorPair D F)) : Prop :=
  Set.InjOn (lineRayPairMap u vLine) (↑P : Set (SlopeErrorPair D F))

def LineRayHighConclusion (u vLine : D → F)
    (P : Finset (SlopeErrorPair D F)) (t d : ℕ) : Prop :=
  let Q := lineRaySyndromePairs u vLine P
  Q.card = P.card ∧ HighDirectionConclusion Q t d

/-- **UNPROVED STATEMENT TARGET (direct LineRay high transfer).** -/
def lineRayHighDirectionTarget (H : (D → F) →ₗ[F] W)
    (u vLine vMin : D → F) (P : Finset (SlopeErrorPair D F))
    (t : ℕ) : Prop :=
  BasicLineRayHypotheses H u vLine P t →
    HostedMinimumLift H (H u) (H vLine) u vMin →
    KernelDistanceAtLeast H (weight vMin) →
    HighPositive (Fintype.card D) t (weight vMin) →
    LineRayHighConclusion u vLine P t (weight vMin)

def LineRayLowConclusion (u vLine : D → F)
    (P : Finset (SlopeErrorPair D F)) (vMin : D → F)
    (t Δ : ℕ) : Prop :=
  let Q := lineRaySyndromePairs u vLine P
  Q.card = P.card ∧ ExactWeightedConclusion Q vMin t ∧
    RealizedRankConclusion Q vMin ∧ LowDirectionConclusion Q vMin t Δ

/-- **UNPROVED STATEMENT TARGET (direct LineRay low transfer).** -/
def lineRayLowDirectionTarget (H : (D → F) →ₗ[F] W)
    (u vLine vMin : D → F) (P : Finset (SlopeErrorPair D F))
    (t Δ : ℕ) : Prop :=
  let M := (outsideCoords (wordSupport vMin)).card
  let ρ := min t M
  BasicLineRayHypotheses H u vLine P t → LineRayTransverse H u vLine P →
    HostedMinimumLift H (H u) (H vLine) u vMin →
    PunctureInjectiveOnKernel H (wordSupport vMin) →
    PuncturedKernelDistanceAtLeast H (wordSupport vMin) Δ →
    Δ ≤ M → LowPositive M ρ Δ →
    LineRayLowConclusion u vLine P vMin t Δ

end DirectionDistanceAllPairs
end GrandeFinale
