import Std

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# Frozen M31 quotient data for the signed T8 census

The definitions below independently reconstruct the pinned `c = 2048`,
`(u,v) = (0,1)` quotient domain.  The printed 62-row weight table is not an
assumption: `frozen_weight_table_exact` recomputes it from the norm-one
generator and the Chebyshev T8 map.

All claims are support-selector level only.
-/

namespace M31SignedT8CensusR2.Data

def fieldPrime : Nat := 2 ^ 31 - 1
def monicT2048Scale : Nat := 1073741824

structure Fp2 where
  re : Nat
  im : Nat
  deriving Repr, BEq, DecidableEq

def fp2One : Fp2 := { re := 1, im := 0 }

def fp2Mul (a b : Fp2) : Fp2 :=
  { re := ((a.re * b.re) % fieldPrime + fieldPrime -
      (a.im * b.im) % fieldPrime) % fieldPrime
   , im := ((a.re * b.im) % fieldPrime +
      (a.im * b.re) % fieldPrime) % fieldPrime }

def fp2PowTwo : Nat → Fp2 → Fp2
  | 0, u => u
  | e + 1, u => fp2PowTwo e (fp2Mul u u)

def normOneGenerator : Fp2 :=
  { re := 1717986917, im := 1288490189 }

def quotientBase : Fp2 := fp2PowTwo 19 normOneGenerator
def quotientStep : Fp2 := fp2Mul quotientBase quotientBase

def iterateMul : Nat → Fp2 → Fp2 → List Fp2
  | 0, _, _ => []
  | n + 1, u, step => u :: iterateMul n (fp2Mul u step) step

def quotientUnits : List Fp2 :=
  iterateMul 1024 quotientBase quotientStep

def oddReps : List Nat :=
  (List.range 1024).map fun j => 2 * j + 1

def quotientLabels : List Nat :=
  quotientUnits.map fun u => (monicT2048Scale * u.re) % fieldPrime

def labelOfRep (r : Nat) : Nat :=
  quotientLabels.getD ((r - 1) / 2) 0

def puncturedReps : List Nat :=
  oddReps.filter fun r => !(r == 1) && !(r == 3)

def noDuplicates [BEq α] : List α → Bool
  | [] => true
  | x :: xs => xs.all (fun y => !(y == x)) && noDuplicates xs

def sameSet [BEq α] (xs ys : List α) : Bool :=
  xs.all ys.contains && ys.all xs.contains

def chebyshevDouble (x : Nat) : Nat :=
  (2 * (x % fieldPrime) * (x % fieldPrime) + (fieldPrime - 1)) % fieldPrime

def chebyshevPowTwo : Nat → Nat → Nat
  | 0, x => x % fieldPrime
  | e + 1, x => chebyshevPowTwo e (chebyshevDouble x)

def oddT16Classes : List Nat :=
  (List.range 64).map fun j => 2 * j + 1

def intactT16Classes : List Nat :=
  oddT16Classes.filter fun a => !(a == 1) && !(a == 3)

def expectedIntactT16Classes : List Nat :=
  [
    5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27,
    29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51,
    53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75,
    77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99,
    101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127
  ]

def t16BlockReps (a : Nat) : List Nat :=
  oddReps.filter fun r =>
    (r % 256 == a) || (r % 256 == 256 - a)

def t8BlockReps (a : Nat) : List Nat :=
  oddReps.filter fun r =>
    (r % 512 == a) || (r % 512 == 512 - a)

def t8Rho (a : Nat) : Nat :=
  chebyshevPowTwo 3 ((2 * labelOfRep a) % fieldPrime)

def cubeMod (x : Nat) : Nat :=
  let y := x % fieldPrime
  (((y * y) % fieldPrime) * y) % fieldPrime

def derivedWeightPairs : List (Nat × Nat) :=
  intactT16Classes.map fun a => (t8Rho a, cubeMod (t8Rho a))

def expectedWeightPairs : List (Nat × Nat) :=
  [
    (226571076, 1149036190), (36815260, 729486832), (2133873350, 1973428948), (472916039, 2012089504),
    (224958826, 896497522), (1768947885, 1625686143), (509684486, 526928603), (1397384897, 1521677267),
    (660017901, 1902992880), (1113159341, 932548291), (776881039, 1997032324), (1492095742, 1407234424),
    (2103108137, 382422396), (1202912605, 846614989), (187158958, 1944935532), (1869196184, 1615391951),
    (355239363, 1950354617), (763629963, 274050207), (328267072, 474724636), (1644164930, 1714459144),
    (1195900917, 1866463208), (1716662235, 1166096640), (617361773, 812538654), (578660954, 1091500517),
    (1326503162, 953014655), (653278886, 1572840437), (1894554377, 1215700588), (469386237, 503532193),
    (1398285837, 1401711771), (1336950523, 1403628202), (839591040, 1890734556), (543822408, 1318288908),
    (390715141, 1212437736), (1353673049, 1141084466), (735494074, 2073423450), (1362518885, 1794902836),
    (1995206774, 765313909), (1541513586, 1343659877), (1152650470, 808248146), (528066207, 923716752),
    (820860779, 1480753441), (1662816114, 116727493), (369838865, 159150139), (2110925851, 918902355),
    (1925205788, 628743594), (1916124599, 911316415), (167450866, 732030927), (775814313, 2110406702),
    (752064346, 1745495436), (1664948088, 1990827099), (853979252, 2133750615), (1340846354, 1869478829),
    (749414350, 760513412), (293249438, 1868619032), (1207781610, 236948744), (485600145, 1345482216),
    (952794586, 1846177525), (1064696601, 1147377276), (416817213, 514272233), (914097328, 1457369417),
    (165851886, 395085676), (222141861, 662014336)
  ]

def powMod (x k : Nat) : Nat :=
  (List.range k).foldl (fun total _ => (total * (x % fieldPrime)) % fieldPrime) 1

def sumMod (xs : List Nat) : Nat :=
  xs.foldl (fun total x => (total + x) % fieldPrime) 0

def blockMoment (a k : Nat) : Nat :=
  sumMod ((t8BlockReps a).map fun r => powMod (labelOfRep r) k)

def t8DifferenceMoment (a k : Nat) : Nat :=
  (blockMoment a k + fieldPrime - blockMoment (256 - a) k) % fieldPrime

/-- Coefficients `(A_k,B_k)` in `D_k(c)=A_k rho(c)+B_k rho(c)^3`. -/
def momentCoefficientTable : List (Nat × Nat) :=
  [
    (0, 0), (0, 0), (0, 0), (0, 0),
    (0, 0), (0, 0), (0, 0), (1048576, 0),
    (0, 0), (655360, 0), (0, 0), (270336, 0),
    (0, 0), (93184, 0), (0, 0), (29120, 0),
    (0, 0), (8568, 0), (0, 0), (1073744246, 0),
    (0, 0), (402653850, 0), (0, 0), (1197473971, 2097152),
    (0, 0), (1450967087, 3407872), (0, 0), (1104003084, 3096576),
    (0, 0), (548284419, 2078720), (0, 0), (1805479680, 1150720)
  ]

def predictedDifferenceMoment (a k : Nat) : Nat :=
  let coeff := momentCoefficientTable.getD (k - 1) (0, 0)
  (coeff.1 * t8Rho a + coeff.2 * cubeMod (t8Rho a)) % fieldPrime

def pivotDeterminant : Nat :=
  let r5 := t8Rho 5
  let r7 := t8Rho 7
  (r5 * cubeMod r7 + fieldPrime - r7 * cubeMod r5) % fieldPrime

def intactBlockReps : List Nat :=
  intactT16Classes.flatMap t16BlockReps

def residualPunctureReps : List Nat :=
  puncturedReps.filter fun r => !(intactBlockReps.contains r)

theorem intact_block_partition_exact :
    intactBlockReps.length = 992 ∧
    noDuplicates intactBlockReps = true ∧
    intactBlockReps.all puncturedReps.contains = true ∧
    residualPunctureReps.length = 30 ∧
    noDuplicates residualPunctureReps = true ∧
    sameSet puncturedReps (intactBlockReps ++ residualPunctureReps) = true := by
  native_decide

theorem deployed_intact_t16_census :
    intactT16Classes = expectedIntactT16Classes ∧
    intactT16Classes.length = 62 ∧
    intactT16Classes.all (fun a => (t16BlockReps a).length == 16) = true ∧
    intactT16Classes.all (fun a => (t8BlockReps a).length == 8) = true ∧
    intactT16Classes.all (fun a => (t8BlockReps (256 - a)).length == 8) = true ∧
    intactT16Classes.all (fun a =>
      noDuplicates (t8BlockReps a ++ t8BlockReps (256 - a)) &&
      sameSet (t16BlockReps a) (t8BlockReps a ++ t8BlockReps (256 - a))) = true := by
  native_decide

theorem frozen_domain_checks :
    fieldPrime = 2147483647 ∧
    puncturedReps.length = 1022 ∧
    noDuplicates quotientLabels = true ∧
    noDuplicates puncturedReps = true ∧
    (2 * monicT2048Scale) % fieldPrime = 1 := by
  native_decide

theorem frozen_weight_table_exact :
    derivedWeightPairs = expectedWeightPairs := by
  native_decide

theorem opposite_half_weights_are_negatives :
    intactT16Classes.all (fun a =>
      (t8Rho a + t8Rho (256 - a)) % fieldPrime == 0) = true := by
  native_decide

/--
Directly recomputes all `62 * 32` T8-half moment differences from the deployed
roots and checks the two-column reduction table.
-/
theorem moment_difference_table_exact :
    (List.range 32).all (fun j =>
      intactT16Classes.all (fun a =>
        t8DifferenceMoment a (j + 1) == predictedDifferenceMoment a (j + 1))) = true := by
  native_decide

theorem reduction_pivot_and_rows_exact :
    pivotDeterminant = 221433382 ∧
    pivotDeterminant ≠ 0 ∧
    momentCoefficientTable.getD 7 (0, 0) = (1048576, 0) ∧
    momentCoefficientTable.getD 23 (0, 0) = (1197473971, 2097152) ∧
    1048576 ≠ 0 ∧
    2097152 ≠ 0 := by
  native_decide

#print axioms intact_block_partition_exact
#print axioms deployed_intact_t16_census
#print axioms frozen_domain_checks
#print axioms frozen_weight_table_exact
#print axioms opposite_half_weights_are_negatives
#print axioms moment_difference_table_exact
#print axioms reduction_pivot_and_rows_exact

end M31SignedT8CensusR2.Data
