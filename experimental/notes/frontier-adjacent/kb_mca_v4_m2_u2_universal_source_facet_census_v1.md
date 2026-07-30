---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every residual degree-two source component, including the trivial-stabilizer type, has the exact (J-J,I-I,I-J)=(10,10,4) census; component edge coloring cuts the five raw K-fiber profiles to three, and every survivor passes the same exact 45-by-12 source-row interpolation gate.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_U2_UNIVERSAL_SOURCE_FACET_CENSUS
quantifier: every actual graph-free Q=6,s=6,u=2 source component in the residual inner-degree-two order-two or trivial-stabilizer types
projection_and_unit: exact source-facet interface; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: exact category census (10,10,4), exactly three component-color-compatible K-fiber profiles on the six J labels, and stabilizer-independent 45-by-12 source-row interpolation applicability
status: PROVED_FACET_COLOR_AND_INTERPOLATION_INTERFACES_ORDER_TWO_AND_TRIVIAL_TYPES_OPEN_K3_OPEN
impact: GIVES_THE_FIRST_EXACT_SOURCE_FACET_COLOR_AND_INTERPOLATION_INTERFACE_FOR_THE_TRIVIAL_STABILIZER_TYPE
falsifier: an actual degree-two source component outside the category census or three color-compatible profiles, failure of the shared source-row interpolation equivalence for the trivial-stabilizer branch, or use of coordinate involution pairing there
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_u2_universal_source_facet_census_v1.py --check --tamper-selftest
---

# KoalaBear universal degree-two source-facet census

## 0. Verdict

The order-two coordinate packet derived an exact `(10,10,4)` star census
before using its stabilizer involution. That first part is universal: it
uses only the common-five source facet and quartic source-row degrees.

Consequently the residual trivial-stabilizer type `(r,delta)=(8,1)` is not
source-combinatorially unconstrained. Its ten stars over the five common
`K` fibers first have one of five integer profiles; exact component edge
coloring removes two, leaving three profiles that must next pass the shared
`45 x 12` source-row interpolation gate.

Two raw profiles are deleted here. No surviving profile, component type,
owner, payment, K3 value, or row bound is deleted or booked.

## 1. Universal category census

Use the equality-wall source-facet notation: `I,L` are six-sets,
`J=I^c`, `K subset I intersect L` has size five, and
`eta=L minus K` is one label.

Every source row has degree four. Above the five labels of `K`, the complete
outgoing root set is `J`, so the ten degree-two component slots give ten
`J-J` stars and 20 `J` incidences. The complete `eta` fiber gives two
`I-I` stars and four `I` incidences.

Every remaining slot lies in a one-exchange facet with five `I` labels and
one `J` label. Its component star is `I-I` or `I-J`. If their counts are
`x,y`, then

```text
x+y=12,       2x+y=20,
```

so `x=8,y=4`. Including the `eta` stars gives

```text
J-J=10,       I-I=10,       I-J=4.                  (1.1)
```

This proof does not use a component stabilizer.

## 2. Five raw K-fiber profiles

For `j in J`, let `d_j` be its incidence degree among the ten `J-J` stars
over `K`. The four `I-J` stars supply exactly four `J` incidences outside
`K`, while every `J` source row has total degree four. Hence

```text
0<=d_j<=4,       sum_(j in J)d_j=20,
sum_(j in J)(4-d_j)=4.                              (2.1)
```

The five partitions of four are

```text
4; 3+1; 2+2; 2+1+1; 1+1+1+1.
```

Subtracting these padded deficit rows from four gives, up to permutation,

```text
(0,4,4,4,4,4),
(1,3,4,4,4,4),
(2,2,4,4,4,4),
(2,3,3,4,4,4),
(3,3,3,3,4,4).                                    (2.2)
```

At most one `J` label is absent from `K`. Ramified coordinate fibers retain
two divisor slots, so (1.1)--(2.2) are multiplicity-safe.

The coordinate involution separately narrows (2.2) to its two paired
profiles. No such pairing is transferred to the diagonal or
trivial-stabilizer type.

## 3. Component-color profile cut

Corollary 9.28 colors a pole-graph edge `(j,ell)` by the selected component
exactly when that component contains the exchanged `J` root at the opposite
point of the deck pair. A source-degree-two component colors exactly four
edges. Therefore

```text
c_j=4-d_j=the colored degree of the left vertex j.
```

The pole graph is two-regular on the left, so `0<=c_j<=2`. The only deficit
partitions are `2+2`, `2+1+1`, and `1+1+1+1`, leaving exactly

```text
(2,2,4,4,4,4),
(2,3,3,4,4,4),
(3,3,3,3,4,4).
```

Every `J` label consequently occurs at least twice over `K`. This uses
neither stabilizer symmetry nor the open zero-migration condition.

## 4. Universal source-row gate

The pinned complete-source reduction applies before any stabilizer or conic
invariance argument. Every residual `u=2` outgoing component is represented
by an irreducible bidegree-`(2,4)` source form with twelve nonzero quartic
rows, and their product is proportional to `B^2`.

The parent coefficient packet proves algebraically that twelve proposed
projective quartic rows come from such a bidegree-at-most-`(2,4)` form if
and only if the associated `45 x 12` matrix has a full-support kernel. No
step in that interpolation equivalence uses a component stabilizer.
Therefore the gate applies to all three stabilizer rows

```text
(r,delta)=(2,4), (4,2), (8,1).
```

This is an applicability theorem, not a claim that the matrix always lacks
a full-support kernel.

## 5. Scope and next action

Proved: the universal category census, the five exhaustive raw integer
profiles, the exact three-profile component-color cut, applicability to the
trivial-stabilizer type, and the universal scope of the exact source-row
interpolation gate.

Not proved: a stabilizer action in the trivial branch, realization or
deletion of any of the three surviving profiles, universal failure of the
shared source-row kernel, an owner, payment, K3, the KoalaBear row, or a
Prize result.

For the `(8,1)` type, route all three profiles through the `45 x 12` source
interpolation gate and complete-source defect budget. Retain exact degree,
irreducibility, deck distinction, and outer-factor side conditions.
