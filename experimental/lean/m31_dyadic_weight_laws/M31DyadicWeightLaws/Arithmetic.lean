/-!
# M31 dyadic collision weight laws — arithmetic shadow

Standard-library-only, kernel-checked arithmetic of the closed constants
asserted in
`experimental/notes/thresholds/m31_dyadic_weight_laws_v1.md`.

This package checks ONLY the exact integer/field-arithmetic identities among the
packet's own claimed constants:

* the base weights `B16 = 8*C(16,8) = 102960` and `B32 = 8*C(32,16) mod p`;
* the seven `T_16` even constants `p_k = 16*2^(29k)*C(k,k/2) mod p` (k=2..14) and
  the fifteen `T_32` even constants `p_k = 32*2^(29k)*C(k,k/2) mod p` (k=2..30);
* the thirty `T_32` class values `p32(a) = (B32 + w(a)) mod p` with the weight
  antisymmetry `w(a) + w(64-a) ≡ 0` and pair sum `p32(a) + p32(64-a) = 2*B32`,
  and the level check `T_32-even(16) = 2*B16`;
* the counts `40 = C(5,2)C(4,1)`, `60 = C(5,2)C(6,1)`, the same-remainder
  neighbour total `10 + 40 + 30 + 4 = 84`, and the cross-remainder census
  `o_192 = 1225 + 8 = 1233` with `49 = 7^2`, `441 = 21^2`, `1225 = 35^2`.

It does NOT formalize the roots-of-unity filter (Lemma B), the Newton argument,
or the censuses; those are proved / computed in the note.  Binomials are computed
by an in-file Pascal recurrence (no Mathlib).  `native_decide` is used
(disclosed) for the identities involving large powers of two; the small
combinatorial facts use `decide`.
-/

namespace M31DyadicWeightLaws

/-- field prime `p = 2^31 - 1`. -/
def p : Nat := 2 ^ 31 - 1

/-- one Pascal row `[C(n,0), …, C(n,n)]`, computed additively (stdlib only). -/
def pascalRow : Nat → List Nat
  | 0 => [1]
  | n + 1 => let r := pascalRow n; List.zipWith (· + ·) (0 :: r) (r ++ [0])

/-- binomial coefficient `C(n, k)` via the Pascal row. -/
def binom (n k : Nat) : Nat := (pascalRow n).getD k 0

/-- base weight `B16 = 8 * C(16,8) = 102960`. -/
theorem base_const_16 : 8 * binom 16 8 = 102960 := by native_decide

/-- base weight `B32 = 8 * C(32,16) mod p`. -/
theorem base_const_32 : (8 * binom 32 16) % p = 513675826 := by native_decide

/-- `2*B32 mod p`, the constant intact-pair `p32` sum. -/
theorem two_base_const_32 : (2 * 513675826) % p = 1027351652 := by native_decide

/-- level check: the `T_32` even constant at `k=16` equals `2*B16` (a `T_32`
class is two `T_16` classes). -/
theorem t32_even16_is_two_B16 : (32 * 2 ^ (29 * 16) * binom 16 8) % p = 2 * 102960 := by
  native_decide

/-- the seven `T_16` even power-sum constants, `(k, p_k)`. -/
def evenTable16 : List (Nat × Nat) :=
  [(2, 2), (4, 805306368), (6, 167772160), (8, 36700160), (10, 8257536),
   (12, 1892352), (14, 439296)]

/-- each `T_16` even `p_k` equals `16 * 2^(29k) * C(k, k/2) mod p`. -/
theorem even_constants_16 :
    evenTable16.all (fun kv =>
      (16 * 2 ^ (29 * kv.1) * binom kv.1 (kv.1 / 2)) % p == kv.2) = true := by
  native_decide

/-- the fifteen `T_32` even power-sum constants, `(k, p_k)`. -/
def evenTable32 : List (Nat × Nat) :=
  [(2, 4), (4, 1610612736), (6, 335544320), (8, 73400320), (10, 16515072),
   (12, 3784704), (14, 878592), (16, 205920), (18, 48620), (20, 536882459),
   (22, 1275071171), (24, 417333908), (26, 1504444574), (28, 554418214),
   (30, 527689737)]

/-- each `T_32` even `p_k` equals `32 * 2^(29k) * C(k, k/2) mod p`. -/
theorem even_constants_32 :
    evenTable32.all (fun kv =>
      (32 * 2 ^ (29 * kv.1) * binom kv.1 (kv.1 / 2)) % p == kv.2) = true := by
  native_decide

/-- the fourteen intact antisymmetric `T_32` pairs, as
`(a, 8*eta_a, p32(a), 64-a, 8*eta_{64-a}, p32(64-a))`. -/
def pairTable : List (Nat × Nat × Nat × Nat × Nat × Nat) :=
  [(5, 1590749127, 2104424953, 59, 556734520, 1070410346),
   (7, 99910478, 613586304, 57, 2047573169, 413765348),
   (9, 526221414, 1039897240, 55, 1621262233, 2134938059),
   (11, 232480480, 746156306, 53, 1915003167, 281195346),
   (13, 2114958684, 481150863, 51, 32524963, 546200789),
   (15, 1251605585, 1765281411, 49, 895878062, 1409553888),
   (17, 998021454, 1511697280, 47, 1149462193, 1663138019),
   (19, 114309104, 627984930, 45, 2033174543, 399366722),
   (21, 1508662977, 2022338803, 43, 638820670, 1152496496),
   (23, 1676708738, 42900917, 41, 470774909, 984450735),
   (25, 2054273900, 420466079, 39, 93209747, 606885573),
   (27, 996335, 514672161, 37, 2146487312, 512679491),
   (29, 1052145471, 1565821297, 35, 1095338176, 1609014002),
   (31, 830574365, 1344250191, 33, 1316909282, 1830585108)]

/-- for every intact pair: closed form `p32 = (B32 + 8*eta) mod p` on both members,
weight antisymmetry `8*eta_a + 8*eta_{64-a} ≡ 0`, and pair sum `= 2*B32`. -/
theorem pair_relations :
    pairTable.all (fun r =>
      ((513675826 + r.2.1) % p == r.2.2.1) &&
      ((513675826 + r.2.2.2.2.1) % p == r.2.2.2.2.2) &&
      ((r.2.1 + r.2.2.2.2.1) % p == 0) &&
      ((r.2.2.1 + r.2.2.2.2.2) % p == 1027351652)) = true := by
  native_decide

/-- the two singleton `T_32` classes (their `T_64` partners 1,3 are punctured). -/
theorem singleton_61 : (513675826 + 156859168) % p = 670534994 := by native_decide

theorem singleton_63 : (513675826 + 892336617) % p = 1406012443 := by native_decide

/-- deployed masked count `s_224 = C(5,2) * C(4,1) = 40`. -/
theorem deployed_count : binom 5 2 * binom 4 1 = 40 := by decide

/-- naive all-pairs-available count `C(5,2) * C(6,1) = 60` (the counterfactual). -/
theorem naive_count : binom 5 2 * binom 6 1 = 60 := by decide

/-- same-remainder neighbour total across the spectrum `10 + 40 + 30 + 4 = 84`. -/
theorem spectrum_sum : 10 + 40 + 30 + 4 = 84 := by decide

/-- cross-remainder o-census levels are perfect squares of `C(7,1),C(7,2),C(7,3)`. -/
theorem o64_is_square : binom 7 1 ^ 2 = 49 := by decide
theorem o128_is_square : binom 7 2 ^ 2 = 441 := by decide
theorem o192_whole_t64_is_square : binom 7 3 ^ 2 = 1225 := by decide

/-- `o_192 = 1225 whole-T_64 + 8 mixed = 1233` (the integrated rooted degree). -/
theorem o192_total : binom 7 3 ^ 2 + 8 = 1233 := by decide

/- Axiom census: the `native_decide` theorems carry a theorem-local
native-decision axiom; the `decide` facts are kernel-only. -/
#print axioms base_const_16
#print axioms base_const_32
#print axioms two_base_const_32
#print axioms t32_even16_is_two_B16
#print axioms even_constants_16
#print axioms even_constants_32
#print axioms pair_relations
#print axioms singleton_61
#print axioms singleton_63
#print axioms deployed_count
#print axioms naive_count
#print axioms spectrum_sum
#print axioms o64_is_square
#print axioms o128_is_square
#print axioms o192_whole_t64_is_square
#print axioms o192_total

end M31DyadicWeightLaws
