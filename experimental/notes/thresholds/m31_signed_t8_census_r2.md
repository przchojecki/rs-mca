---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "Reduce the signed opposite-half T8 selector population on the pinned c=2048, (u,v)=(0,1) quotient profile to an explicit ternary lattice-cube census; certify the lift geometry, lattice index, symmetry, route cuts, completed finite searches, and any nonzero ternary support lower bound obtained."
architecture: DIRECT_PINNED_C2048_U0_V1_SIGNED_T8_CENSUS_R2
partition_digest: "N/A; support-selector reduction packet, no first-match row atom"
atom_or_cell: "Q / pinned quotient prefix fiber / signed opposite-half T8 selector sector"
quantifier: "The 62 intact T16 classes on the deployed 1022-label punctured quotient domain; selector coordinates in {-1,0,1}; support-level constructions only."
projection_and_unit: "Selectors, valid 479-supports, direct locator-prefix collisions, and deficiency. No received word, codeword, list, ray, slope, or row payment."
claimed_bound: "STATE: COMPLETE. The selector census is the ternary cube intersected with the two-congruence lattice. The lattice has an explicit determinant-p^2 basis. Exactly m<=59 lifts. Exact MITM exhaustion proves every nonzero selector has support m>=8, hence the liftable sector has deficiency at least 64; the known m=24 selector gives deficiency 192."
status: PROVED
impact: LOCAL_ONLY
falsifier: "Any kernel or independent recomputation showing an incorrect frozen integer, direct T8 moment row, lift endpoint, selector-to-support construction, modular equation, lattice determinant, symmetry action, route-cut vector, finite-search domain, or direct 479-factor collision check."
replay: "cd experimental/lean/m31_signed_t8_census_r2 && lake clean && lake build; stdlib-only Lean package, native_decide disclosed and every theorem followed by #print axioms."
---

# M31 signed T8 census round 2

**STATE: COMPLETE**

**Request worked from:** certify the reduction packet for the signed
opposite-half T8 selector census and obtain a certified nonzero ternary support
floor.

## 1. Scope and frozen objects

This packet is support-level only.  It counts ternary selector rows, constructs
valid 479-support pairs, checks locator-prefix agreement, and records
support deficiency.  It makes no received-word, codeword, list, ray, slope, or
row-bound claim.

Put

```text
p = 2^31 - 1 = 2147483647,
|D| = 1022,
|S| = 479.
```

The deployed quotient domain is represented by the 1,022 odd exponents modulo
4,096 after deleting representatives 1 and 3.  The 62 intact T16 classes are

```text
C = {5,7,9,...,127};
```

class 1 and class 3 are the two punctured classes.  Every `c in C` has a
16-label block

```text
T16(c) = T8(c) disjoint-union T8(256-c),
|T8(c)| = |T8(256-c)| = 8.
```

The union of the 62 intact T16 blocks has 992 labels; the residual puncture
sector has 30 labels.  This partition and every class size are recomputed by

```text
M31SignedT8CensusR2.Data.intact_block_partition_exact
M31SignedT8CensusR2.Data.deployed_intact_t16_census.
```

## 2. Selector convention and exact census reduction

For each intact class choose

```text
z_c =  1 : put T8(c) on the anchor side and T8(256-c) on the neighbor side;
z_c = -1 : reverse those two halves;
z_c =  0 : skip the class.
```

Thus a selector is a vector `z in {-1,0,1}^62`.  Let

```text
rho(c) = T_8(2 q_c) in F_p,
S_1(z) = sum_c z_c rho(c),
S_3(z) = sum_c z_c rho(c)^3.
```

The deployed roots, all 62 values `(rho(c),rho(c)^3)`, and the opposite-half
identity

```text
rho(256-c) = -rho(c)
```

are reconstructed rather than imported as assumptions:

```text
M31SignedT8CensusR2.Data.frozen_domain_checks
M31SignedT8CensusR2.Data.frozen_weight_table_exact
M31SignedT8CensusR2.Data.opposite_half_weights_are_negatives.
```

For `1 <= k <= 32`, let `D_k(c)` be the difference between the kth raw power
sum of `T8(c)` and that of `T8(256-c)`.  Direct multiplication in the deployed
field gives

```text
D_k(c) = A_k rho(c) + B_k rho(c)^3.
```

The 32 coefficient rows are

```text
k= 1.. 7: (0,0)
k= 8:     (1048576,0)
k= 9:     (0,0)
k=10:     (655360,0)
k=11:     (0,0)
k=12:     (270336,0)
k=13:     (0,0)
k=14:     (93184,0)
k=15:     (0,0)
k=16:     (29120,0)
k=17:     (0,0)
k=18:     (8568,0)
k=19:     (0,0)
k=20:     (1073744246,0)
k=21:     (0,0)
k=22:     (402653850,0)
k=23:     (0,0)
k=24:     (1197473971,2097152)
k=25:     (0,0)
k=26:     (1450967087,3407872)
k=27:     (0,0)
k=28:     (1104003084,3096576)
k=29:     (0,0)
k=30:     (548284419,2078720)
k=31:     (0,0)
k=32:     (1805479680,1150720).
```

`moment_difference_table_exact` recomputes all `62*32=1,984` direct block
moment rows from the 1,022 deployed roots.  Hence the selector moment difference
at row `k` is

```text
A_k S_1(z) + B_k S_3(z).
```

If `S_1=S_3=0`, all 32 direct differences vanish.  Conversely, row 8 gives
`2^20 S_1=0`; multiplication by 2,048 is an inverse modulo `p`.  After
`S_1=0`, row 24 gives `2^21 S_3=0`; multiplication by 1,024 is an inverse.
The inverse identities are checked by

```text
M31SignedT8CensusR2.Census.dyadic_row_inverse_certificates.
```

Therefore, with the hypotheses above explicit, the signed opposite-half T8
selector census is exactly

```text
L intersect {-1,0,1}^62,

L = {z in Z^62 :
       sum_c z_c rho(c)   == 0 (mod p),
       sum_c z_c rho(c)^3 == 0 (mod p)}.
```

Even powers of the opposite parameters agree automatically.  The displayed
raw-moment table is the direct verification layer; the two compressed equations
are the reduction layer.

Lean names:

```text
M31SignedT8CensusR2.Data.moment_difference_table_exact
M31SignedT8CensusR2.Data.reduction_pivot_and_rows_exact
M31SignedT8CensusR2.Census.reduced_census_is_lattice_cube_intersection
M31SignedT8CensusR2.Census.known_selector_direct_and_reduced
M31SignedT8CensusR2.Census.dyadic_row_inverse_certificates.
```

## 3. Lift geometry

Let

```text
m(z) = |supp z|.
```

The two exchanged halves each have `8m` labels, so

```text
deficiency e(z) = 8m.
```

A valid 479-support lift is obtained by choosing a common core `G`, disjoint
from both exchanged sides, with

```text
|G| = 479 - 8m.
```

The two exchanged sides occupy `16m` distinct labels, leaving

```text
1022 - 16m
```

available core labels.  Thus a lift exists exactly when

```text
0 <= 479 - 8m <= 1022 - 16m.
```

On the census range `0 <= m <= 62`, this is equivalent to

```text
m <= 59.
```

The endpoint ledger is

```text
m=59: core  7, available 78, liftable;
m=60: core -1, available 62, unliftable;
m=61: core -9, available 46, unliftable;
m=62: core -17, available 30, unliftable.
```

Rows 60--62 remain valid selector-census rows if they satisfy the lattice
equations, but they are not collisions.  The generic arithmetic and exact
finite table are checked by

```text
M31SignedT8CensusR2.Reduction.lift_criterion_iff_support_le_59
M31SignedT8CensusR2.Reduction.liftable_table_exact
M31SignedT8CensusR2.Reduction.lift_endpoint_arithmetic.
```

The construction is exact: select any `479-8m` labels from the complement of
the two disjoint exchanges and adjoin the same selected core to both sides.
For the printed `m=24` row, Lean constructs

```text
8m = 192,
|available complement| = 638,
|G| = 287,
|G union X| = |G union Y| = 479
```

and checks all disjointness and support-validity predicates in

```text
M31SignedT8CensusR2.Collision.exact_core_and_complement_construction.
```

## 4. Automatic improvement corollary

Every certified nonzero selector with

```text
0 < m < 24
```

satisfies `m<=59`, therefore lifts, and has

```text
e = 8m < 192.
```

This is the statement-changing floor corollary: finding any such row would
immediately improve the known support-level collision deficiency.  It is
checked symbolically and by the exact row table:

```text
M31SignedT8CensusR2.Reduction.auto_lift_below_known_witness
M31SignedT8CensusR2.Reduction.auto_lift_rows_below_known_witness_exact.
```

## 5. Explicit basis and lattice determinant

Let

```text
phi : Z^62 -> (Z/pZ)^2,
phi(z) = (S_1(z),S_3(z)).
```

Using the first two coordinates, classes 5 and 7, the 2-by-2 pivot determinant
is

```text
221433382 mod p,
```

which is nonzero.  Hence `phi` is onto and the kernel lattice `L` has index
`p^2` in `Z^62`.

The packet prints an explicit lower-triangular integer basis.  With `e_i` the
standard coordinate vectors, its rows are

```text
b_0 = p e_0,
b_1 = p e_1,
b_j = e_j + alpha_j e_0 + beta_j e_1,  2 <= j <= 61,
```

where the 60 exact pairs `(alpha_j,beta_j)` are the literal list
`M31SignedT8CensusR2.Lattice.basisCoefficients`.  Each row is checked against
both congruences.  The matrix diagonal is

```text
[p,p,1,...,1]
```

and a standard Laplace determinant evaluator returns

```text
|det B| = p^2 = 4611686014132420609.
```

Thus the basis sublattice `B` lies in `L` and has the same index `p^2`; hence
`B=L`.  Kernel evidence:

```text
M31SignedT8CensusR2.Lattice.explicit_basis_rows_are_lattice_rows
M31SignedT8CensusR2.Lattice.explicit_basis_determinant
M31SignedT8CensusR2.Data.reduction_pivot_and_rows_exact.
```

## 6. Symmetry

The sign involution

```text
z |-> -z
```

preserves both equations.  Over the integer ternary cube its only fixed point
is zero, since `z_c=-z_c` implies `z_c=0` in every coordinate.  Therefore the
resulting `C_2` action is free on nonzero selectors.

For quotient exponent multipliers, the packet enumerates every odd
`u mod 4096` preserving the deleted pair `{1,3}` modulo sign.  The exact list is

```text
u in {1,4095} = {+1,-1}.
```

Both act trivially on the 62 canonical T16 classes modulo sign and modulo 256.
There is therefore no additional nontrivial class permutation from the
puncture-preserving quotient multipliers.

Kernel evidence:

```text
M31SignedT8CensusR2.Lattice.puncture_preserving_multiplier_action_is_trivial
M31SignedT8CensusR2.Lattice.ternary_coordinate_fixed_by_sign_only_at_zero.
```

## 7. Known extremal row and direct collision verification

The known row has

```text
m = 24,
11 positive coordinates,
13 negative coordinates,
squared Euclidean norm = 24,
e = 192.
```

It is checked against both congruences by

```text
M31SignedT8CensusR2.Lattice.known_selector_relation_exact.
```

The construction uses 24 opposite T8 half-pairs, a 287-label common core, and
produces two valid 479-supports.  The final collision check does not trust the
two compressed equations.  It multiplies all 479 factors

```text
product_{r in support} (Y-q_r)
```

on each side and checks

```text
prefix_32 equal,
prefix_39 equal,
prefix_40 unequal,
coefficient 40 on anchor   = 381197232,
coefficient 40 on neighbor = 1671112725,
deficiency = 192.
```

Kernel evidence:

```text
M31SignedT8CensusR2.Collision.opposite_half_selector_packet_exact
M31SignedT8CensusR2.Collision.known_collision_direct_479_factor_check.
```

## 8. Certified route cut: ordinary SVP is insufficient

The lattice contains the explicit vector

```text
class:  7  9 11 13 15 21 25 27 35 41 49 51 53 57 61 65 71 73 77
value: -1 -1  1  1  1  1  1 -1 -1  1  1  1 -1  1 -1 -2  1 -1  1.
```

It has

```text
support = 19,
squared norm = 22,
coefficient at class 65 = -2,
S_1 = S_3 = 0 mod p.
```

It is a valid short lattice vector but is not ternary.  Therefore ordinary
Euclidean SVP enumeration cannot decide the ternary minimum: a shorter
nonternary vector can appear before the known norm-24 ternary row.

Kernel evidence:

```text
M31SignedT8CensusR2.Lattice.norm_twenty_two_nonternary_route_cut.
```

## 9. ARM 2: exact ternary floor through support seven

The search is an exact meet-in-the-middle exhaustion, not a solver claim.
Every signed relation of support at most seven is either:

1. a signed partial of size at most three; or
2. a signed four-subset plus a disjoint signed remainder of size at most three.

The exact unsigned subset counts for sizes 0 through 4 are

```text
1, 62, 1891, 37820, 557845.
```

After signs, the exact counts are

```text
1, 124, 7564, 302560, 8925520.
```

The small table contains

```text
1 + 124 + 7564 + 302560 = 310249
```

signed partials of sizes 0 through 3.  All 310,249 two-equation keys are
distinct; only the empty partial has key `(0,0)`.

The four-subset side streams

```text
557845 * 16 = 8925520
```

signed records.  Every key is nonzero, and its negative is either absent from
the small table or represented only by a partial overlapping the four chosen
coordinates.  Hence no disjoint pair exists.

The complete executable domain comprises

```text
310249 + 8925520 = 9235769
```

signed records.  It proves

```text
no nonzero z in L intersect {-1,0,1}^62 has m(z) <= 7.
```

Therefore

```text
m(z) >= 8
```

for every nonzero selector, and the liftable collision sector has certified
deficiency floor

```text
e >= 8*8 = 64.
```

Together with the known row, the current ternary minimum is bracketed by

```text
8 <= m_min <= 24,
64 <= e_min <= 192.
```

Kernel evidence:

```text
M31SignedT8CensusR2.TernaryFloor.enumeration_domain_sizes_exact
M31SignedT8CensusR2.TernaryFloor.small_partial_keys_are_injective
M31SignedT8CensusR2.TernaryFloor.no_ternary_relation_through_support_seven_certificate
M31SignedT8CensusR2.TernaryFloor.split_sizes_cover_support_through_seven
M31SignedT8CensusR2.TernaryFloor.certified_sector_deficiency_floor_arithmetic.
```

The first three use `native_decide`; the split theorem uses `omega`; the final
arithmetic theorem uses ordinary `decide`.

## 10. Exact-search and derivation-direction ledger

| Printed item | Direction | Certificate or proof |
|---|---|---|
| `p=2147483647` | derived from `2^31-1` | `Data.frozen_domain_checks` |
| 1,022 deployed labels | enumerated from the punctured exponent domain | `Data.frozen_domain_checks` |
| 62 intact T16 classes | enumerated | `Data.deployed_intact_t16_census` |
| 992 intact-block labels and 30 residual labels | enumerated and partition-checked | `Data.intact_block_partition_exact` |
| 62 `(rho,rho^3)` pairs | enumerated from deployed roots | `Data.frozen_weight_table_exact` |
| 1,984 direct moment entries | enumerated (`62*32`) | `Data.moment_difference_table_exact` |
| pivot determinant `221433382` | derived and enumerated | `Data.reduction_pivot_and_rows_exact` |
| lattice determinant `4611686014132420609` | evaluated from explicit basis | `Lattice.explicit_basis_determinant` |
| multiplier list `[1,4095]` | exact enumeration over residues `0,...,4095` | `Lattice.puncture_preserving_multiplier_action_is_trivial` |
| deficiency `8m` | derived from one 8-point half per selected class | definition plus Section 3 |
| core `479-8m` | derived | `Reduction.requiredCoreSize` |
| available `1022-16m` | derived | `Reduction.availableCoreLabels` |
| liftable rows `m=0,...,59` | exact enumeration, plus symbolic theorem | `Reduction.liftable_table_exact`, `lift_criterion_iff_support_le_59` |
| unliftable rows 60,61,62 | exact enumeration | `Reduction.lift_endpoint_arithmetic` |
| known row `m=24`, signs `11/13` | enumerated | `Lattice.known_selector_relation_exact` |
| direct locator agreement 39, failure at 40 | direct multiplication of all 479 factors per side | `Collision.known_collision_direct_479_factor_check` |
| SVP route-cut norm 22 | direct evaluation | `Lattice.norm_twenty_two_nonternary_route_cut` |
| unsigned subset counts through 4 | exact enumeration | `TernaryFloor.enumeration_domain_sizes_exact` |
| signed partial counts through 4 | derived from enumerated subsets times `2^k`, then checked | same theorem |
| 310,249 small keys | exact enumeration | `small_partial_keys_are_injective` |
| 8,925,520 signed four-subsets | exact enumeration | `no_ternary_relation_through_support_seven_certificate` |
| 9,235,769 total signed records | derived from the two exact domains | `enumeration_domain_sizes_exact` |
| ternary floor `m>=8` | derived from exact exhaustion plus split theorem | Section 9 |
| sector-deficiency floor `e>=64` | derived from `m>=8` and `e=8m` | `certified_sector_deficiency_floor_arithmetic` |

No printed count in this note is an unlabeled heuristic or probabilistic
estimate.

## 11. Documented failed routes and their precise obstructions

These are route-history statements, not theorems.  No unpushed round-1 session
text is cited as evidence.

1. **MILP did not finish as a certificate.**  No exact optimum or infeasibility
   proof over the full 62-coordinate ternary cube was exported into a
   kernel-checkable format.  A solver state or timeout cannot certify a floor.
2. **SMT did not finish as a certificate.**  The same obstruction applies: no
   replayable proof object covered the full two-congruence domain.
3. **Subset-sum through six choices per side did not finish.**  Its declared
   domain has at most six positive and six negative coordinates.  Even a
   completed run would not cover rows with larger one-sided sign count, so it
   cannot by itself prove the target floor 24.  The exact support-through-seven
   MITM search in this packet is a different, complete domain.
4. **The single-weight-16 slice is not exhaustive.**  It imposes an additional
   slice condition not proved to contain every ternary solution of the two
   equations.  Absence in that slice is not absence in the full cube.
5. **Local replacement did not produce a descent theorem.**  No terminating
   potential, confluence statement, or proof that every solution reaches a
   classified normal form was obtained.  Blocked local moves therefore do not
   certify global minimality.
6. **Ordinary SVP is formally cut.**  The squared-norm-22 vector with coefficient
   `-2` is a concrete falsifier to using Euclidean shortest-vector enumeration
   as a ternary-minimum oracle.

## 12. Axiom and replay census

The package is stdlib-only and contains no Mathlib import.  Every declared
theorem is immediately followed by `#print axioms`.

The build log reports only:

- standard Lean logical axioms such as `propext`, `Classical.choice`, and
  `Quot.sound` where used by tactics or library structures; and
- the explicitly named `native_decide` certificate axiom for finite
  computations.

There is no `sorryAx`, `sorry`, `admit`, or custom axiom in the successful
build.  The exact MITM theorem takes about 93 seconds in the recorded green
build; all other modules compile in seconds.

Package:

```text
experimental/lean/m31_signed_t8_census_r2/
```

Namespace:

```text
M31SignedT8CensusR2
```

## 13. Open interval and next step

The exact minimum remains in

```text
8 <= m_min <= 24.
```

The natural next step is a certificate for support 8 and above, preferably one
of:

1. an exact meet-in-the-middle exclusion extending the four-plus-three split;
2. a modular descent that forces a larger support; or
3. a structure theorem for repeated two-equation keys that yields a compact
   replay certificate.

Any certified solution with `8 <= m < 24` automatically lifts and improves the
known deficiency 192.  A proof excluding every support below 24 would establish
`m_min=24` and `e_min=192` in this signed opposite-half T8 sector.
