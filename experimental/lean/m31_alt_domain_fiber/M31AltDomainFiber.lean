import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 flatness-keystone arithmetic certificate

This stdlib-only module certifies the exact integer and degree-gap claims used by
`m31_flatness_keystone_constant_shift_obstruction.md`.

The symbolic polynomial statement—constant-shift blocks of degree `d` hide all
selection-dependent terms below the first `d` nonleading coefficients—is proved
in the note.  This module checks the deployed specialization and the complete
max-versus-average arithmetic.  It does not formalize the finite-field coset
construction, a received word, or the deployed Chebyshev quotient.
-/

namespace M31AltDomainFiber

def fieldPrime : Nat := 2147483647
def domainSize : Nat := 1022
def supportSize : Nat := 479
def prefixDepth : Nat := 32
def blockDegree : Nat := 33
def totalBlocks : Nat := 31
def intactBlocks : Nat := 30
def selectedBlocks : Nat := 14
def coreSize : Nat := 17
def baseDomainSize : Nat := 1024
def punctureCount : Nat := 2
def budget : Nat := 16777215

def fastBinomial (n k : Nat) : Nat :=
  (List.range k).foldl
    (fun value i => value * (n - i) / (i + 1))
    1

def targetCount : Nat := fieldPrime ^ prefixDepth
def totalSupports : Nat := fastBinomial domainSize supportSize
def floorAverage : Nat := totalSupports / targetCount
def averageRemainder : Nat := totalSupports % targetCount
def ceilAverage : Nat := floorAverage + (if averageRemainder = 0 then 0 else 1)
def constantShiftFiberSize : Nat := fastBinomial intactBlocks selectedBlocks

def expectedTargetCount : Nat :=
  41855804344513474996659235398101492226513356497450298740932889847998693318143069882098996132602011303952349637025722282585533160693229396196872386718816372844518146497415885223313922264348563527038409009746582412510577609691239404142296725925022012935690228019787759005225367255740944911962461962241

def expectedTotalSupports : Nat :=
  151271865290567282756670209927671126612573718499984279646030908205795367378645973832177793165136706631573210771619584252500710632400169112681192055348722412206290242750426752087291990702755284787532455089499756167113798752793361036534746315185930511714934550247772523231121741961638844402219522161141316000

def expectedAverageRemainder : Nat :=
  7548778587015219130749919959628379493028775703410749273281236177882372060252956051361373258139744248853801817862284966111208715580527547821932900501597833163649332550399893901282650118721755927357603447484993482512633668572475393014382515879345810719047125207442915642880687636317942661096628835321

theorem parameter_arithmetic :
    baseDomainSize - punctureCount = domainSize ∧
    coreSize + selectedBlocks * blockDegree = supportSize ∧
    prefixDepth + 1 = blockDegree ∧
    totalBlocks * blockDegree + 1 = baseDomainSize := by
  native_decide

theorem degree_gap_exact :
    coreSize + (selectedBlocks - 1) * blockDegree = 446 ∧
    supportSize - prefixDepth = 447 ∧
    446 < 447 := by
  native_decide

theorem family_size_exact :
    constantShiftFiberSize = 145422675 := by
  native_decide

theorem ambient_average_exact :
    targetCount = expectedTargetCount ∧
    totalSupports = expectedTotalSupports ∧
    floorAverage = 3614119 ∧
    averageRemainder = expectedAverageRemainder ∧
    ceilAverage = 3614120 := by
  native_decide

theorem obstruction_margins_exact :
    constantShiftFiberSize - 8 * budget = 11204955 ∧
    constantShiftFiberSize - 40 * ceilAverage = 857875 ∧
    budget - 4 * ceilAverage = 2320735 ∧
    5 * ceilAverage - budget = 1293385 := by
  native_decide

theorem packet_arithmetic :
    constantShiftFiberSize = 145422675 ∧
    ceilAverage = 3614120 ∧
    8 * budget < constantShiftFiberSize ∧
    40 * ceilAverage < constantShiftFiberSize := by
  exact ⟨family_size_exact, ambient_average_exact.2.2.2.2,
    by native_decide, by native_decide⟩

#print axioms parameter_arithmetic
#print axioms degree_gap_exact
#print axioms family_size_exact
#print axioms ambient_average_exact
#print axioms obstruction_margins_exact
#print axioms packet_arithmetic

end M31AltDomainFiber
