import M31QuotientT16MixingFloor

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 depth-32 T16-completeness counting refutation

This module certifies the deployed class census and the exact integer gates in
the nonconstructive counting refutation of universal depth-32 T16 alignment on
the pinned Mersenne-31 quotient profile.

The mathematical proof in the companion note additionally uses:

* the depth-32 Newton equivalence (`lem:newton-equivalence`);
* the elementary union bound over empty/full intact T16 classes;
* pigeonhole over at most `p^32` prefix targets; and
* the rational constant-intersection rank bound.

Lean checks the finite deployed data and all large arithmetic below.  It does
not extract or print the existential ragged collision, and it does not formalize
the rational rank argument.

The finite domain machinery (`fieldPrime`, `oddT16Classes`, `t16BlockReps`,
`puncturedReps`, `fastBinomial`) is the upstream package
`experimental/lean/m31_quotient_t16_mixing_floor/` (`Witness.lean`).
-/

namespace M31T16RaggedWitness

/--
Pinned-profile constants, replayed as self-contained definitions.  The support
size 479 and the depth-32 prefix target count `p^32` (with `p` the upstream
`fieldPrime = 2^31 - 1`) are the same pinned constants named `supportSize` and
`prefixTargetCount` in the parent capped-rigidity draft; `Support` and
`PrefixTarget` are its representative-list and coefficient-list aliases.
-/
abbrev Support := List Nat
abbrev PrefixTarget := List Nat

def supportSize : Nat := 479
def prefixTargetCount : Nat := M31QuotientT16MixingFloor.Witness.fieldPrime ^ 32

end M31T16RaggedWitness

namespace M31T16RaggedWitness.CountingRefutation

def intactT16Classes : List Nat :=
  M31QuotientT16MixingFloor.Witness.oddT16Classes.filter fun a =>
    !(a == 1) && !(a == 3)

def remainingRepsInT16Class (a : Nat) : List Nat :=
  (M31QuotientT16MixingFloor.Witness.t16BlockReps a).filter fun r =>
    M31QuotientT16MixingFloor.Witness.puncturedReps.contains r

def intactT16ClassCount : Nat := 62
def intactT16ClassSize : Nat := 16
def puncturedClassLabelCount : Nat := 30

def allSupportCount : Nat :=
  M31QuotientT16MixingFloor.Witness.fastBinomial 1022 479

def emptyOneIntactClassCount : Nat :=
  M31QuotientT16MixingFloor.Witness.fastBinomial 1006 479

def fullOneIntactClassCount : Nat :=
  M31QuotientT16MixingFloor.Witness.fastBinomial 1006 463

/--
Union-bound lower count for 479-supports whose occupancy in every intact T16
class lies in `1,...,15`.
-/
def fullyPartialSupportLowerBound : Nat :=
  allSupportCount -
    intactT16ClassCount *
      (emptyOneIntactClassCount + fullOneIntactClassCount)

def deployedPrefixTargetCount : Nat :=
  M31T16RaggedWitness.prefixTargetCount

def ceilDiv (n d : Nat) : Nat :=
  (n + d - 1) / d

def expectedAllSupportCount : Nat :=
  151271865290567282756670209927671126612573718499984279646030908205795367378645973832177793165136706631573210771619584252500710632400169112681192055348722412206290242750426752087291990702755284787532455089499756167113798752793361036534746315185930511714934550247772523231121741961638844402219522161141316000

def expectedEmptyOneIntactClassCount : Nat :=
  5491502670182402772592911288640018159334773997691349463712018016403071837493288092147012319237474774618283907244184087126598499171324600523695369363942992114703682217167074563295890826661863982642100255253368088591305100647724346454664463740408100480157320978753388416119672518170255997843129342476000

def expectedFullOneIntactClassCount : Nat :=
  716427256427630211335271704897132762388629490128321553734874389466340849410645849530571389557169661267970037400687008393614241187049870425850332468225629880117954483223001583025738820807730798080562414236385678330928827548857277843992014410833550894133997607363656099568019883637140120199417314620000

def expectedFullyPartialSupportLowerBound : Nat :=
  150886973635117460711666662582071823255426867483739460042949200876631463792057929927793782975191438676548263027051602244578457442497949895482320221835127957642611301275002567366220049664612169911127650003991391433564620249245172975828229613540553529329728488495433266471149105032726785842900884268401364000

def expectedPrefixTargetCount : Nat :=
  41855804344513474996659235398101492226513356497450298740932889847998693318143069882098996132602011303952349637025722282585533160693229396196872386718816372844518146497415885223313922264348563527038409009746582412510577609691239404142296725925022012935690228019787759005225367255740944911962461962241

def expectedPrefixDivisionRemainder : Nat :=
  21870080910886284861733041597593747658838881436754889184807114470279537660019207823539863398280670446916495924396473369484252231300856102426887572282398832411049098602159335555073649953235545767481348712323309751280784201149329368873428745399391561264631655918914755058429059371488034430004093651557

theorem deployed_t16_partition_census :
    intactT16Classes.length = intactT16ClassCount ∧
    intactT16Classes.all
      (fun a => (remainingRepsInT16Class a).length == intactT16ClassSize) = true ∧
    (remainingRepsInT16Class 1).length = 15 ∧
    (remainingRepsInT16Class 3).length = 15 ∧
    intactT16ClassCount * intactT16ClassSize + puncturedClassLabelCount = 1022 := by
  native_decide

theorem support_count_inputs_exact :
    allSupportCount = expectedAllSupportCount ∧
    emptyOneIntactClassCount = expectedEmptyOneIntactClassCount ∧
    fullOneIntactClassCount = expectedFullOneIntactClassCount := by
  native_decide

theorem fully_partial_lower_bound_exact :
    fullyPartialSupportLowerBound = expectedFullyPartialSupportLowerBound := by
  native_decide

theorem deployed_prefix_target_count_exact :
    deployedPrefixTargetCount = expectedPrefixTargetCount := by
  native_decide

theorem fully_partial_prefix_pigeonhole_arithmetic :
    fullyPartialSupportLowerBound / deployedPrefixTargetCount = 3604923 ∧
    fullyPartialSupportLowerBound % deployedPrefixTargetCount =
      expectedPrefixDivisionRemainder ∧
    ceilDiv fullyPartialSupportLowerBound deployedPrefixTargetCount = 3604924 ∧
    1022 < 3604924 := by
  native_decide

theorem fully_partial_exceeds_constant_intersection_cap :
    1022 * deployedPrefixTargetCount < fullyPartialSupportLowerBound := by
  native_decide

theorem depth_and_rank_boundary_arithmetic :
    M31T16RaggedWitness.supportSize - 32 = 447 ∧
    M31T16RaggedWitness.supportSize - 33 = 446 ∧
    M31T16RaggedWitness.supportSize - 446 = 33 ∧
    33 + 446 * 3604924 = 1607796137 ∧
    puncturedClassLabelCount < 34 := by
  decide

#print axioms deployed_t16_partition_census
#print axioms support_count_inputs_exact
#print axioms fully_partial_lower_bound_exact
#print axioms deployed_prefix_target_count_exact
#print axioms fully_partial_prefix_pigeonhole_arithmetic
#print axioms fully_partial_exceeds_constant_intersection_cap
#print axioms depth_and_rank_boundary_arithmetic

end M31T16RaggedWitness.CountingRefutation
