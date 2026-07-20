import AsymptoticSpine.UniformClosedLedger

namespace AsymptoticSpine

/-!
# Certified semantic atlas ownership

This module separates semantic first-match owners from witness-local refinements.
The distinction is forced by the singleton-planted C3 regression: an arbitrary
factor of one support locator cannot by itself create an earlier C3 owner.

A semantic owner must carry a row-derived certificate from a fixed catalogue.
Witness-local facts may refine or help pay an already-owned cell, but do not
alter first-match ownership.  The resulting line package composes certified C3
profiles with a deletion-aware later ledger while preserving the existing
`sup_line sum_profile` compiler boundary.
-/

/-- Provenance of an admissible row-derived planted certificate.  These labels
record the permitted semantic mechanisms; constructing a label is not itself a
mathematical proof that a concrete row has the certificate. -/
inductive PlantedCertificateKind where
  | gcd
  | resultant
  | ramification
  | quotient
  | otherCanonical
  deriving DecidableEq, Repr

/-- A certified planted profile eligible to create a semantic C3 first-match
owner.  `certificateId` indexes a fixed row-level catalogue; `assignedSlopes`
is already post-deletion and directly paid at its own natural scale. -/
structure CertifiedC3Profile (compilerLoss : Nat) where
  certificateId : Nat
  certificateKind : PlantedCertificateKind
  assignedSlopes : List Nat
  assignedSlopes_nodup : assignedSlopes.Nodup
  naturalScale : Nat
  paid : assignedSlopes.length ≤ compilerLoss * naturalScale

namespace CertifiedC3Profile

/-- Install a certified C3 owner into the existing closed-ledger payment type. -/
def payment {compilerLoss : Nat} (profile : CertifiedC3Profile compilerLoss) :
    ProfilePayment compilerLoss :=
  ProfilePayment.ofDirect .c3 profile.assignedSlopes profile.naturalScale
    compilerLoss profile.assignedSlopes_nodup profile.paid

@[simp] theorem payment_owner {compilerLoss : Nat}
    (profile : CertifiedC3Profile compilerLoss) :
    profile.payment.owner = .c3 := rfl

@[simp] theorem payment_assignedSlopes {compilerLoss : Nat}
    (profile : CertifiedC3Profile compilerLoss) :
    profile.payment.assignedSlopes = profile.assignedSlopes := rfl

end CertifiedC3Profile

/-- Witness-local support information.  This may be used inside a selected
profile, but deliberately contains no constructor producing a semantic owner. -/
structure WitnessLocalRefinement where
  witnessId : Nat
  factorId : Nat
  factorDividesWitnessLocator : Prop

/-- A typed semantic atlas slice: certified C3 owners first, followed by a later
already-closed ledger (for example C4--C9 after deletion by the C3 slope image).
The cross-disjointness field is the exact ownership obligation between the two
slices. -/
structure CertifiedC3ThenLater
    (compilerLoss c3Cap laterCap : Nat) where
  badCount : Nat
  c3Profiles : List (CertifiedC3Profile compilerLoss)
  laterProfiles : List (ProfilePayment compilerLoss)
  c3CountControl : c3Profiles.length ≤ c3Cap
  laterCountControl : laterProfiles.length ≤ laterCap
  ownership :
    ((c3Profiles.map (fun p => p.assignedSlopes)) ++
      (laterProfiles.map (fun p => p.assignedSlopes))).flatten.Nodup
  exhaustive :
    badCount ≤
      (((c3Profiles.map (fun p => p.assignedSlopes)) ++
        (laterProfiles.map (fun p => p.assignedSlopes))).flatten).length

namespace CertifiedC3ThenLater

/-- The actual payment list, with certified C3 owners before all later owners. -/
def profiles {compilerLoss c3Cap laterCap : Nat}
    (atlas : CertifiedC3ThenLater compilerLoss c3Cap laterCap) :
    List (ProfilePayment compilerLoss) :=
  atlas.c3Profiles.map CertifiedC3Profile.payment ++ atlas.laterProfiles

/-- The typed atlas compiles to the existing line-local ledger without changing
its arithmetic compiler or summation order. -/
def line {compilerLoss c3Cap laterCap : Nat}
    (atlas : CertifiedC3ThenLater compilerLoss c3Cap laterCap) :
    ClosedLineLedger compilerLoss (c3Cap + laterCap) where
  badCount := atlas.badCount
  profiles := atlas.profiles
  firstMatchOwnership := by
    unfold profiles
    rw [List.map_append, List.map_map]
    exact atlas.ownership
  atlasExhaustive := by
    unfold profiles
    rw [List.map_append, List.map_map]
    exact atlas.exhaustive
  profileCountControl := by
    unfold profiles
    rw [List.length_append, List.length_map]
    exact Nat.add_le_add atlas.c3CountControl atlas.laterCountControl

/-- Tightening semantic ownership is conservative: once the certified atlas
fields are proved, the existing closed-ledger compiler applies unchanged. -/
theorem bad_le_loss_mul_naturalTotal
    {compilerLoss c3Cap laterCap : Nat}
    (atlas : CertifiedC3ThenLater compilerLoss c3Cap laterCap) :
    atlas.badCount ≤ compilerLoss * atlas.line.naturalTotal :=
  atlas.line.bad_le_loss_mul_naturalTotal

/-- A finite row wrapper preserving `sup_line sum_profile`. -/
def ledger {compilerLoss c3Cap laterCap envelope : Nat}
    (atlases : List (CertifiedC3ThenLater compilerLoss c3Cap laterCap))
    (hUnif : ∀ atlas ∈ atlases, atlas.line.naturalTotal ≤ envelope) :
    UniformClosedLedger compilerLoss (c3Cap + laterCap) envelope where
  lines := atlases.map line
  windowUniformity := by
    intro current hcurrent
    rcases List.mem_map.mp hcurrent with ⟨atlas, hatlas, rfl⟩
    exact hUnif atlas hatlas

/-- The certified semantic atlas reaches the same row compiler theorem, with
all profile sums still taken inside each received line. -/
theorem ledger_compiles
    {compilerLoss c3Cap laterCap envelope : Nat}
    (atlases : List (CertifiedC3ThenLater compilerLoss c3Cap laterCap))
    (hUnif : ∀ atlas ∈ atlases, atlas.line.naturalTotal ≤ envelope) :
    (ledger atlases hUnif).rowBad ≤ compilerLoss * envelope :=
  (ledger atlases hUnif).compile

end CertifiedC3ThenLater

/-- Executable ownership fixture: one certified C3 slope is followed by two C7
slopes.  A witness-local singleton refinement exists as data but cannot become
an owner without constructing a `CertifiedC3Profile`. -/
def certifiedOwnershipFixtureC3 : CertifiedC3Profile 3 where
  certificateId := 7
  certificateKind := .resultant
  assignedSlopes := [10]
  assignedSlopes_nodup := by decide
  naturalScale := 1
  paid := by decide

def certifiedOwnershipFixtureC7 : ProfilePayment 3 :=
  ProfilePayment.ofDirect .c7 [11, 12] 1 3 (by decide) (by decide)

def certifiedOwnershipFixture : CertifiedC3ThenLater 3 1 1 where
  badCount := 3
  c3Profiles := [certifiedOwnershipFixtureC3]
  laterProfiles := [certifiedOwnershipFixtureC7]
  c3CountControl := by decide
  laterCountControl := by decide
  ownership := by decide
  exhaustive := by decide

example : certifiedOwnershipFixture.line.badCount ≤
    3 * certifiedOwnershipFixture.line.naturalTotal := by
  exact certifiedOwnershipFixture.bad_le_loss_mul_naturalTotal

#print axioms CertifiedC3ThenLater.bad_le_loss_mul_naturalTotal
#print axioms CertifiedC3ThenLater.ledger_compiles

end AsymptoticSpine
