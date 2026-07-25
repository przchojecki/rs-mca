# M31 signed opposite-half T8 census, round 2

**STATE: COMPLETE**

**Request worked from (one line).** Prove the signed opposite-half T8 selector
reduction packet—exact ternary-lattice census, lift geometry, determinant,
symmetry, and SVP route cut—and raise the nonzero ternary support floor by an
exact kernel-checkable certificate, while keeping every claim at support level.

## Abstract

For the 62 intact Mersenne-31 T16 classes, a signed opposite-half T8 selector is
a ternary vector `z in {-1,0,1}^62`.  This paper proves that the complete signed
selector census is the intersection of that ternary cube with the rank-62
congruence lattice

```text
L = {z in Z^62 : Sum z_c rho(c) = 0 and Sum z_c rho(c)^3 = 0 mod p},
p = 2^31-1.
```

The selector support size `m` gives deficiency `e=8m`.  The exact common-core
construction lifts a census row to two valid 479-supports if and only if
`m<=59`; rows of supports 60, 61, and 62 remain census rows but are not
collisions from this construction.  An explicit 62-row integral basis lies in
`L`, has determinant `p^2=4611686014132420609`, and matches the index of `L`.
Global sign is a free `C_2` action away from zero, while exhaustive multiplier
analysis leaves only `+/-1`, both trivial on the 62 class labels.  A certified
lattice vector of squared norm 22 has coefficient `-2`, cutting off ordinary
SVP as a ternary-minimum method.  Finally, an exact meet-in-the-middle census of
9,235,769 signed partial rows excludes all nonzero ternary relations of support
at most seven.  Thus every nonzero selector has `m>=8`, and every liftable one
has deficiency at least 64.  The known `m=24` selector is checked directly and
lifts to a pair of 479-supports whose locator prefixes are obtained by
multiplying all 479 deployed factors; it has deficiency 192.  The remaining
floor question is exactly the support interval `8<=m<=23`.

## 1. Objects and populations

Let

```text
p = 2147483647.
```

The frozen quotient model has 1,024 odd representatives modulo 4,096.
Puncturing representatives `1` and `3` leaves 1,022 usable labels.  The intact
T16 classes are indexed by

```text
C = {5,7,9,...,127},   |C|=62.
```

For each `c in C`, the class has two opposite eight-point halves, denoted
`T8(c)` and `T8(256-c)`.  A selector is

```text
z = (z_c)_{c in C} in {-1,0,1}^62,
```

with `+1` selecting the first half on support A and the opposite half on support
B, `-1` reversing those choices, and `0` skipping the class.  Its support size
is

```text
m(z) = |{c : z_c != 0}|.
```

Two populations must remain distinct throughout:

1. **Census rows:** every ternary vector satisfying the two congruences below.
2. **Lifted support collisions:** census rows with `m<=59`, after adjoining an
   exact common core to form two valid supports of size 479.

In particular, a ternary row of support 60, 61, or 62 is a census row but not a
collision supplied by the common-core lift.

## 2. Main statements

### Theorem A — signed selector census

Let `rho(c)` be the frozen deployed weight `T_8(2q_c) mod p`, computed by three
Chebyshev doublings from the quotient label `q_c`.  A signed opposite-half T8
selector satisfies all direct deployed moment equations through moment 32 if
and only if

```text
Sum_{c in C} z_c rho(c)   = 0 mod p,
Sum_{c in C} z_c rho(c)^3 = 0 mod p.
```

Consequently the complete signed-selector population is exactly

```text
L intersect {-1,0,1}^62,
```

where `L` is the congruence kernel displayed in the abstract.

### Theorem B — deficiency and exact lift range

For every selector,

```text
e(z) = 8m(z).
```

Its two exchange sets have `8m` points each and are disjoint.  A common core
must contain `479-8m` points, while the common complement contains
`1022-16m` points.  Thus the lift exists exactly when

```text
0 <= 479-8m <= 1022-16m,
```

which, on `0<=m<=62`, is equivalent to

```text
m <= 59.
```

The construction is explicit: choose any `479-8m` labels outside both exchange
sets and adjoin that same core to both sides.

### Corollary B.1 — automatic statement change below the witness

Every certified ternary solution with

```text
0 < m < 24
```

automatically lifts and gives a directly verifiable support collision of
deficiency

```text
8m < 192.
```

Such a row would therefore lower the present signed-T8 sector record.

### Theorem C — determinant and explicit basis

The map

```text
Phi : Z^62 -> (Z/pZ)^2,
Phi(z) = (Sum z_c rho(c), Sum z_c rho(c)^3)
```

is surjective.  The two columns for classes 5 and 7 have nonzero determinant

```text
221433382 mod p.
```

Hence `L=ker(Phi)` has index `p^2`.  The package gives 60 explicit pivot
solution pairs `(alpha_j,beta_j)` and the 62 rows

```text
p e_0,
p e_1,
alpha_j e_0 + beta_j e_1 + e_{j+2},  j=0,...,59.
```

Every row lies in `L`.  Their matrix is lower triangular with diagonal
`[p,p,1,...,1]`, so

```text
|det| = p^2 = 4611686014132420609.
```

The generated sublattice lies in `L` and has the same index, so these rows form
an integral basis of `L`.

### Theorem D — generic symmetry

Global negation `z -> -z` preserves the ternary cube and both equations and has
no nonzero fixed point.  It therefore gives a free `C_2` action on nonzero
selectors.

Among all 4,096 quotient multipliers, exactly

```text
1 and 4095 = -1 mod 4096
```

preserve the puncture set.  Both induce the identity on the canonical T16 class
labels modulo 256.  Thus the puncture-preserving multiplier action on the 62
intact classes is trivial.  In the frozen generic symmetry family generated by
global sign and quotient multipliers, the only nontrivial selector action is
therefore the free sign involution.

### Theorem E — ordinary SVP cannot certify the ternary minimum

There is an explicit vector in `L` with

```text
positive unit classes: {11,13,15,21,25,41,49,51,57,71,77},
negative unit classes: {7,9,27,35,53,61,73},
coefficient -2 at:     {65},
all other entries:     0.
```

It has support 19, squared Euclidean norm 22, and satisfies both congruences,
but it is not ternary.  Therefore an ordinary SVP enumeration can terminate at
a shorter nonternary relation and does not decide the minimum in
`L intersect {-1,0,1}^62` without an additional coefficient-domain
certificate.

### Theorem F — certified ternary floor

There is no nonzero ternary selector in `L` with support at most seven.
Equivalently,

```text
z in L intersect {-1,0,1}^62 and z != 0  ==>  m(z) >= 8.
```

Since all rows with `m<=59` lift, every nonzero liftable signed-T8 selector has

```text
e(z) >= 64.
```

### Proposition G — known upper witness, directly verified

The known selector has 11 positive signs, 13 negative signs, support 24, and
deficiency 192.  It satisfies both lattice equations.  Its two exchange sets
have size 192; adjoining a common core of size 287 gives two distinct supports
of size 479.  Folding every deployed locator factor on both full supports gives

```text
pref_39(A) = pref_39(B),
pref_40(A) != pref_40(B),
|A\B| = |B\A| = 192.
```

Thus the currently certified signed-T8 bracket is

```text
64 <= minimum liftable deficiency <= 192,
```

and the unresolved support range is exactly `8<=m<=23`.

## 3. Reduction mechanism

For `1<=k<=32`, define the direct per-class moment difference

```text
D_k(c) = Sum_{x in T8(c)} x^k - Sum_{y in T8(256-c)} y^k mod p.
```

The package evaluates every one of the `62*32=1984` deployed rows and checks
that

```text
D_k(c) = a_k rho(c) + b_k rho(c)^3 mod p.
```

Odd rows vanish.  Every surviving even row is a linear combination of the two
reduced sums

```text
S_1(z) = Sum z_c rho(c),
S_3(z) = Sum z_c rho(c)^3.
```

Two rows isolate those sums:

```text
k=8:  (a_8,b_8) = (1048576,0),
      1048576 * 2048 = 1 mod p;

k=24: (a_24,b_24) = (366280333,2097152),
      2097152 * 1024 = 1 mod p.
```

If `S_1=S_3=0`, every direct row vanishes by distributivity.  Conversely, the
`k=8` row forces `S_1=0`; after substitution, the `k=24` row forces `S_3=0`.
This gives the equivalence in Theorem A with no solver assumption.

## 4. Exact floor certificate

The meet-in-the-middle certificate uses the pair

```text
key(partial) = (S_1(partial),S_3(partial)).
```

It enumerates exactly:

```text
all signed supports of sizes 0,1,2,3:
  Sum_{j=0}^3 C(62,j)2^j = 310249 rows;

all signed supports of size 4:
  C(62,4)2^4 = 8925520 rows;

total generated rows:
  310249 + 8925520 = 9235769.
```

The certificate checks four exhaustive statements:

1. the only small-side row with key zero is the empty row;
2. all 310,249 small-side keys are distinct;
3. every signed four-support has nonzero key;
4. if the negative of a four-support key occurs on the small side, the unique
   small support carrying it overlaps the four-support.

A relation of support at most three contradicts item 1.  A relation of support
between four and seven can be split into four coordinates and a disjoint
remainder of size at most three.  Their keys would be negatives, contradicting
item 4.  This is an exact exhaustion of all supports 1 through 7—not a random
sample, bound, or solver timeout.

## 5. Kernel-checked evidence

All declarations are in the stdlib-only package

```text
experimental/lean/m31_signed_t8_census_r2/
namespace M31SignedT8CensusR2
Lean v4.31.0
```

The package declares 30 theorems.  Every theorem is proved with
`native_decide`, immediately followed by `#print axioms`, and every printed
axiom census is `[]`.

### Deployed data and direct reduction

```text
Data.deployed_data_exact
Data.deployed_weight_table_exact
Data.direct_moment_table_shape
Data.direct_moment_rows_match_reduced_formula
Data.direct_moment_pivot_gates
Data.pivot_minor_nonzero
Data.explicit_pivot_inverses
```

### Lift arithmetic

```text
Reduction.lift_table_exact
Reduction.lift_criterion_exact
Reduction.auto_lift_below_known_witness
Reduction.known_witness_arithmetic
Reduction.deficiency_is_eight_times_support
```

### Lattice, determinant, symmetry, and route cut

```text
Lattice.known_selector_lattice_equations
Lattice.known_selector_signs_and_support
Lattice.basis_satisfies_lattice_equations
Lattice.determinant_p2_explicit_basis
Lattice.puncture_preserving_multipliers_are_trivial_on_classes
Lattice.c2_sign_involution_is_free_off_zero
Lattice.norm22_nonternary_route_cut
```

### Direct support collision

```text
Collision.known_exchange_sets_exact
Collision.known_supports_exact
Collision.direct_locator_collision_exact
```

### Census packaging

```text
Census.reduced_census_is_lattice_cube_intersection
Census.known_selector_direct_and_reduced
Census.known_selector_is_census_row_and_lifts
```

### Exact partial census

```text
TernaryFloor.partial_search_counts_exact
TernaryFloor.small_nonzero_partials_have_no_zero_key
TernaryFloor.small_partial_keys_are_injective
TernaryFloor.all_four_partials_safe
TernaryFloor.split_sizes_cover_support_through_seven
```

The direct collision theorem computes locator prefixes from the complete
479-element support lists.  Compressed moment equations are not used as the
final verification layer.

## 6. Formalization boundary

The finite numerical content is kernel evaluated: deployed blocks and weights,
all 1,984 direct moment rows, pivot gates, every explicit basis row, the
triangular determinant, all multipliers, the norm-22 vector, all 9,235,769
partial rows, and the complete 479-factor witness check.

Two short mathematical assembly steps are printed in this paper rather than
encoded as abstract library theorems:

1. finite-sum distributivity turns the checked per-class direct-moment table
   into the arbitrary-selector equations of Theorem A; and
2. equality of lattice indices turns the checked determinant-`p^2` generating
   set into a basis of `ker(Phi)`.

Likewise, the support-seven exclusion follows from the checked key/overlap
predicates and the elementary `4+(0..3)` split written in Section 4.  These are
not numerical hypotheses or solver outputs.  No `sorry`, `admit`, custom axiom,
unsafe declaration, Mathlib dependency, Python verifier, or search script is
part of the packet.

## 7. Routes killed and evidence against a stronger conclusion

The following round-1 routes are documented failures only; none is promoted to
a theorem.

- **MILP / SMT.** No run emitted a proof object, complete infeasibility
  certificate, or exact replay log.  Obstruction: a solver status without an
  exported certificate is not kernel-checkable evidence.
- **Subset sum through six terms per side.** This covers at most 12 nonzero
  coordinates.  Obstruction: it does not close the full interval below the
  support-24 witness.
- **Single weight-16 slice.** This fixes one Newton stratum.  Obstruction: other
  signed support patterns and strata remain unexamined.
- **Local replacement.** No monotone invariant or completeness argument was
  found.  Obstruction: local irreducibility does not imply a global support
  floor.
- **Ordinary lattice reduction / SVP.** The certified squared-norm-22 relation
  contains `-2`.  Obstruction: Euclidean shortness does not enforce ternarity.

The present result does **not** prove that support 24 is minimal.  The exact
search stops at support seven, leaving supports 8 through 23 open.  It also does
not claim anything about codewords, list sizes, row bounds, rays, slopes, or
selector sectors outside the frozen signed opposite-half T8 population.

## 8. Natural next step

The immediate target is any certified increment beyond `m>=8`.  Two mechanisms
look structurally compatible with the present certificate:

1. enlarge the exact complement side while retaining enough support data to
   certify disjointness; or
2. derive an algebraic or modular exclusion for one or more support bands, then
   enumerate only the surviving bands.

Every increment to `m>=m_0` raises the liftable-sector deficiency floor to
`8m_0`.  Reaching `m>=24` would make the known support-24 row extremal and close
the signed-T8 sector minimum at deficiency 192.

## 9. Provenance and references

### This packet

- Lean package:
  `experimental/lean/m31_signed_t8_census_r2/`
- Reduction dossier:
  `experimental/notes/thresholds/m31_signed_t8_census_r2.md`

### Predecessor and upstream sources consulted

- Predecessor packet: PR 1087.
- Integrated selector-spectrum note:
  `experimental/notes/thresholds/m31_selector_spectrum_generator_v1.md`.
- Exact Newton reduction label: `lem:newton-equivalence`.
- Frozen witness namespace:
  `M31CappedRigidity.M31T16CompletenessS1.RaggedWitness`, including
  `explicit_ragged_collision`.
- Frozen deployed quotient source namespace:
  `M31QuotientT16MixingFloor.Witness`.
- Upstream snapshot read for this round:
  `przchojecki/rs-mca@b13de8113a03f06b6fc22bbd2f289a8abcdf7e95`.

These references supply the frozen deployed labels and predecessor witness;
every numerical claim newly made in this paper is re-derived and certified in
the round-2 package named above.
