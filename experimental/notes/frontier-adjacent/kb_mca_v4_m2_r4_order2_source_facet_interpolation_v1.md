---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The coordinate order-two orientation has an exact (J-J,I-I,I-J)=(10,10,4) source-facet census and two K-fiber degree profiles, while the diagonal orientation has an exact whole-fiber 35-by-12 interpolation-kernel compiler.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R4_ORDER_TWO_SOURCE_FACET_AND_DIAGONAL_INTERPOLATION
quantifier: every actual graph-free Q=6,s=6 inner-degree-two component with order-two V4 stabilizer, separated into coordinate and diagonal orientations
projection_and_unit: exact source-facet and endpoint-component interpolation interfaces; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: coordinate census (10,10,4), two exhaustive K-degree profiles, and a 35-by-12 full-support kernel equivalence for diagonal whole-fiber quartics
status: PROVED_INTERFACES_ORDER_TWO_TYPE_OPEN_K3_OPEN
impact: REPLACES_STAR_COUNTING_FOR_THE_COORDINATE_ORIENTATION_AND_VAGUE_SOURCE_LIFT_FOR_THE_DIAGONAL_ORIENTATION
falsifier: an actual coordinate component outside the census/profiles, an actual diagonal component violating whole-fiber transport or the interpolation kernel, or failure of the printed aligned abstract fixture
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.py --check --tamper-selftest
---

# KoalaBear order-two source-facet and interpolation interfaces

## 0. Verdict

After deletion of the full-V4 type, the first open inner-degree-two type is

```text
(m,r,delta)=(2,4,2).
```

Its stabilizer is one of the three order-two subgroups of the endpoint
`V4`. This packet separates the two genuinely different source interfaces.

For a coordinate subgroup, the preserving source lift acts pointwise on the
source `X`-line. It forces an exact component-star census and two degree
profiles, but an aligned defect-zero abstract fixture realizes every current
facet, symmetry, pole-graph, color, and defect constraint. More counting of
those quantities alone cannot delete the orientation.

For the diagonal subgroup, individual stars need not be equivariant.
Multiplying the two quadratic component fibers over one `psi` fiber gives a
split quartic. The twelve quartics satisfy exact diagonal transport and come
from a bidegree-`(4,4)` endpoint component exactly when a concrete
`35 x 12` matrix has a full-support kernel.

Neither interface deletes an order-two subgroup. No owner or payment is
booked; K3 and the KoalaBear row remain open.

## 1. Inherited source facet

Use the notation of Corollaries 9.25 and 9.27 of the pinned equality-wall
source theorem. There are six-sets `I,L`, a five-set

```text
K subset I intersect L,
```

and `eta` is the unique label in `L minus K`. Put `J=I^c`. Over the two
points of every `K` fiber the whole outgoing root set is `J`; over the
`eta` fiber it is `I`. The six fibers indexed by `L^c` are paired
one-exchange facets: each point has five common `I` labels and one exchanged
`J` label. The pole graph between the six noninvariant coordinate labels
and `L^c` is diagonal-free and two-regular.

For a degree-two outgoing component there are two source roots at each of
the 24 coordinate-pole points, and every source row has degree four.

## 2. Coordinate orientation

Assume `<tau x 1>` stabilizes the endpoint component. The preserving source
lift is

```text
(T,X) -> (tau(T),b(X)),
```

so if `bar` is the fixed-point-free permutation of the twelve source
labels, then

```text
star(bx)=bar(star(x)).                                (2.1)
```

The ten points over `K` contribute ten `J-J` stars and 20
`J`-incidences. The two points over `eta` contribute two `I-I` stars.
The remaining twelve stars have type `I-I` or `I-J`. Since all six
`I` labels and all six `J` labels have total degree four, the exact census
is

```text
J-J=10,       I-I=10,       I-J=4.                  (2.2)
```

At most one `J` label can be absent from the `K` fibers: absence consumes
all four of its incidences outside `K`. Equation (2.1) then says at least
five `J` labels map back into `J`. The number of cross-pairs in a
fixed-point-free matching of a six-set is even, so none crosses. Thus

```text
bar(I)=I,       bar(J)=J.                            (2.3)
```

Let `c_j` be the number of `j in J` incidences outside `K`.
The `K`-fiber multiset is `bar`-invariant, so
`c_j=c_bar(j)` and `sum_j c_j=4`. On the three `bar`-pairs the
representative complements are `(2,0,0)` or `(1,1,0)`. Therefore the
`K`-fiber degrees are exactly

```text
(4,4),(4,4),(2,2),       or
(4,4),(3,3),(3,3).                                  (2.4)
```

These conditions do not delete the coordinate orientation. In the allowed
aligned case `L=I`, the certificate prints 24 distinct stars satisfying
all facets, source degree four, the two-regular pole graph, exactly four
component-colored pole edges, (2.1)--(2.4), and defect zero. This is an
abstract route fence, not an algebraic endpoint component.

## 3. Diagonal orientation

Assume `<tau x tau>` stabilizes the endpoint component `Gamma`. Let
`G(T,W)` define `Gamma` and `H(T,X)` define one bidegree-`(2,4)`
source component. The quadratic base change has two distinct components:

```text
G(T,psi(X)) ~ H(T,X) H(T,bX).                       (3.1)
```

Write the degree-two fiber divisor as
`psi^*[alpha_p]=[x_p]+[bx_p]`, allowing `x_p=bx_p` at ramification, and
put

```text
R_p(T)=H(T,x_p)H(T,bx_p).                           (3.2)
```

This is projectively `G(T,alpha_p)`; at ramification it is
`H(T,x_p)^2`. If
`tau(alpha_p)=alpha_bar(p)`, diagonal invariance gives the binary-quartic
identity

```text
[R_bar(p)]=[tau^*R_p].                              (3.3)
```

The pullback notation includes the homogenizing factor of the projective
involution. Equation (3.3) is a whole-`psi`-fiber statement. The
normalization automorphism need not preserve `K(X)`, so it may repartition
the four roots between the two destination stars; no individual-star
version of (2.1) is asserted.

The factors of `R_p` obey the `K`, `eta`, and one-exchange facets from
Section 1. Every source label occurs four times, counted with divisor
multiplicity, hence

```text
product_p R_p(T) ~ A(T)^4.                           (3.4)
```

Write `R_p(T)=sum_(a=0)^4 r_(p,a)T^a` and let `P` be a
`7 x 12` parity-check matrix for degree-at-most-four evaluation at the
twelve `alpha_p`. Form

```text
M_(s,a),p=P_(s,p)r_(p,a),           M in K^(35 x 12). (3.5)
```

There is a biform of bidegree at most `(4,4)` with projective fibers
`[R_p]` if and only if `Mc=0` for some vector `c` with all twelve
coordinates nonzero. Indeed, for each `T` coefficient the vector
`(c_pr_(p,a))_p` must be, and under the parity checks is, the evaluation
of a unique degree-at-most-four polynomial in `W`. This also reconstructs
the unique interpolant for fixed `c`.

A passing interpolant must still be irreducible and divide the actual outer
self-correspondence. Failure of the full-support kernel is already an exact
deletion of the proposed source-facet packet.

## 4. Scope and next action

Proved: the coordinate census, involution preservation, two degree profiles,
the aligned abstract route fence, diagonal whole-fiber transport, the
fourth-power divisor, and the full-support interpolation equivalence.

Not proved: an actual abstract-fixture realization, universal failure of
the coordinate coefficient equations or diagonal kernel, deletion of
`<1 x tau>` or any order-two subgroup, deletion of the type, an owner,
payment, K3, the KoalaBear row, or either Prize problem.

The next exact actions are:

1. impose the source-component coefficient equations on the two coordinate
   profiles;
2. prove universal failure of the diagonal full-support kernel, or
   reconstruct the interpolant and impose the outer factor identity; and
3. transport the coordinate source presentation explicitly before treating
   `<1 x tau>` as equivalent.
