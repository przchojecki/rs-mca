---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every residual degree-two source component, including the trivial-stabilizer type, has the exact (J-J,I-I,I-J)=(10,10,4) census; component edge coloring cuts the five raw K-fiber profiles to three, every survivor passes the same exact 45-by-12 source-row interpolation gate, its I/J row products split through one squarefree colored quartic, the coordinate orientation descends this to explicit quotient-resultant and five-fiber Vieta-rank equations, endpoint transposition routes the other coordinate subgroup through a fresh source record, and the diagonal endpoint involution must mix I and J in one of five exact crossing-orbit rows, with aligned c=6 impossible, its near-aligned survivor reduced to one reciprocal colored quotient system, and the c=2 rows reduced to exact incidence-capacity and square-fiber alternatives.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_U2_UNIVERSAL_SOURCE_FACET_CENSUS
quantifier: every actual graph-free Q=6,s=6,u=2 source component in the residual inner-degree-two order-two or trivial-stabilizer types
projection_and_unit: exact source-facet interface; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: exact universal facet/color/interpolation/resultant interfaces plus coordinate descent to one quotient quadratic, explicit 8/7-dimensional cubic-norm equations, exact 10-by-8 or 10-by-7 K-fiber Vieta gates, transpose transport of the second coordinate subgroup, deletion of the partition-preserving diagonal subcase and aligned c=6, quotient descent of the near-aligned c=6 colored divisor, and exact c=2 crossing-degree, square-fiber, fourth-power-product, and exceptional-capacity pins
status: PROVED_FACET_COLOR_INTERPOLATION_RESULTANT_COORDINATE_QUOTIENT_VIETA_RANK_TRANSPOSE_DIAGONAL_MIXING_C6_QUOTIENT_AND_C2_CAPACITY_INTERFACES_TYPES_OPEN_K3_OPEN
impact: GIVES_EXACT_TRIVIAL_SOURCE_INTERFACES_AND_REDUCES_ORDER_TWO_TO_ONE_COORDINATE_ROUTE_PLUS_FIVE_DIAGONAL_MIXING_ROWS_WITH_C6_AT_ONE_QUOTIENT_SYSTEM_AND_C2_AT_PRINTED_SQUARE_FIBER_ALTERNATIVES
falsifier: an actual degree-two component outside the universal source interfaces, a coordinate component whose colored divisor, paired-root resultants, or printed K-fiber Vieta gates fail, failure of endpoint transposition after rebuilding the source record, an actual diagonal component whose endpoint involution preserves I and J, an aligned c=6 component, failure of the near-aligned c=6 quotient identities, or a c=2 component violating the printed incidence degrees, square-fiber identities, or exceptional capacity interval
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

## 5. Colored partial-resultant split

Let `D_K` be the degree-ten pullback over `K`, put `D_R=B/D_K`, and let
`P_I,P_J` be the source-label sextics on `I,J`. Package the four simple
colored pole roots as the squarefree quartic `C_H`. The product formula for
resultants and the exact source-facet multiplicities give

```text
Res_T(P_J,H) ~ D_K^2 C_H,
C_H Res_T(P_I,H) ~ D_R^2.                          (5.1)
```

For a left pole-graph vertex `j`, its two edge roots form `bZ_j`, so

```text
c_j=deg gcd(C_H,bZ_j).                             (5.2)
```

Thus one four-edge divisor controls both partial resultants and recovers
the surviving profile. This is an exact compiler, not a construction or a
universal resultant failure.

## 6. Coordinate quotient-resultant specialization

In the coordinate orientation, star transport preserves the `I-J`
category. Hence `C_H` is deck invariant and has the form `c(W)` for a
squarefree quotient quadratic selecting two complete right pole-graph
fibers. Since `I,J` are invariant under `T->-T`, write
`P_S(T)=p_S(T^2)`. The positive and negative source forms give

```text
Phi_+=(A_2Y+A_0)^2-WYB_1^2,
Phi_-=W(B_2Y+B_0)^2-YA_1^2,
R_S=Res_Y(p_S,Phi_epsilon).
```

The colored split becomes

```text
R_J~K_5^2c,       cR_I~R_7^2.                     (6.1)
```

This is an explicit univariate system in the existing eight or seven
source coefficients plus a two-fiber choice. Neither parity system is
proved empty.

## 7. Coordinate common-K Vieta-rank gate

The five actual `J-J` stars over the common set `K` can be inserted before
solving the larger norm-factorization system. Write a quotient point as
`kappa=[u:v]`, choose a lift `[r:s]` with `[r^2:s^2]=[u:v]`, and let
`{a,b}` be its unordered `J`-edge. The weighted coordinates

```text
p=ab,       q=r*s*(a+b)
```

are unchanged by `([r:s],a,b)->([-r:s],-a,-b)`. Vieta gives the exact
positive equations

```text
A_0(kappa)=p A_2(kappa),
u*v B_1(kappa)=-q A_2(kappa),
```

and the exact negative equations

```text
B_0(kappa)=p B_2(kappa),
A_1(kappa)=-q B_2(kappa).
```

Across five fibers these are homogeneous `10 x 8` and `10 x 7` kernel
gates, with nonzero leading values at every fiber. The positive branch
has the necessary determinant

```text
det[qv^2,quv,qu^2,uv^2,u^2v]=0.
```

The negative branch has

```text
rank[-pv,-pu,v,u]<=3,
det[qv,qu,v^2,uv,u^2]=0.
```

At a ramified source point the negative binary quadratic has only the two
fixed endpoint labels, which are absent from `J`; therefore the negative
branch excludes ramified common-`K` values. The positive equations remain
valid there and were replayed at both quotient branch values. These are
exact packet-deletion gates, not a proof that every coordinate packet
fails.

## 8. Transport of the second coordinate subgroup

The endpoint relation is the symmetric self-correspondence `f(T)=f(W)`.
Axis transposition preserves every actual non-diagonal bidegree-`(4,4)`
component and conjugates the order-two subgroups by

```text
<1 x tau>  <->  <tau x 1>,
<tau x tau> -> <tau x tau>.
```

For a transposed component, rename `T'=W,W'=T` and rerun the degree-two
source reduction on the new second coordinate `W'=psi'(X')`. This gives
fresh data `H',b',I',J',L',K'`. The coordinate source-facet, coefficient,
colored-resultant, and Vieta-rank results apply to that primed record.
They do not assert that `H'` is the formal transpose of the old source
equation or that a packet-specific determinant is unchanged.

Thus the two coordinate subgroups are one existence/deletion route. The
order-two campaign has two independent geometries, coordinate and
diagonal, not three subgroup-specific campaigns. Neither route is closed.

## 9. Diagonal facet-mixing obstruction

Let `tau` now denote the fixed-point-free endpoint deck involution in the
diagonal subgroup `<tau x tau>`; it is not the unrelated canonical matching
also denoted `tau` in the source-facet theorem. Put `J=I^c` and let `xi` be
the unique label in `I minus K`.

The diagonal whole-fiber compiler gives split quartics `R_y` with

```text
[R_tau(y)]=[tau^*R_y].                              (9.1)
```

Every `R_k`, `k in K`, has all four roots in `J`. Suppose `tau(I)=I`.
The fixed-point-free matching on the six-set `I` must pair the odd five-set
`K` to `xi`, so some `k in K` has `tau(k)=xi`. Equation (9.1) transports
four `J` roots to `R_xi`. If `xi in L`, then `L=I` and `xi=eta`, whose
quartic is supported on `I`. Otherwise `xi in L^c`; its two quadratic stars
lie in reduced one-exchange facets, each containing only one `J` label, so
the quartic has at most two `J` roots. Both cases are contradictions. Hence

```text
tau(I)!=I,       tau(J)!=J.                         (9.2)
```

Let `c=|I intersect tau(J)|`. The same number crosses in the other direction,
and the `6-c` noncrossing labels of `I` are internally paired. Thus

```text
c in {2,4,6}.                                      (9.3)
```

If `a` counts involution pairs contained in `K`, and `b` is one exactly when
`tau(xi) in K`, then `6-c=2a+2b`. The exact remaining rows are

```text
(a,b,c)=(2,0,2),(1,1,2),(1,0,4),(0,1,4),(0,0,6). (9.4)
```

There is also a support cut. Set

```text
J_0=J intersect tau(J),       J_1=J intersect tau(I).
```

For `k in K`, transport to `K` forces every root of `R_k` into `J_0`;
transport to `eta` forces every root into `J_1`; and transport to `L^c`
forces at least two roots into `J_1`. This argument uses whole-fiber
transport only, so it applies to both branches of the diagonal
source-subfield dichotomy. It deletes the partition-preserving subcase, not
the five mixing rows or the diagonal orientation.

If `c=6`, then `tau` swaps `I` and `J`. The aligned case `L=I` is impossible:
the `I`-supported `eta` quartic would transport to four `J` roots over an
`L^c` fiber of `J`-capacity two. In the near-aligned case, `eta in J` must
pair into `K`; pairing it with `xi` gives the same capacity contradiction.
Thus

```text
tau(eta) in K,       ell=tau(xi) in J intersect L^c. (9.5)
```

If `z` is the number of `J` roots over `xi`, then the paired quartic over
`ell` has `4-z` such roots. Both one-exchange capacities are two, so
`z=4-z=2`. The remaining four `L^c` quartics are transports of `K` quartics
and are supported on `I`. Therefore exactly the four stars above `xi,ell`
are `I-J`, and the four colored roots are the two complete source fibers
over that `tau` orbit.

Writing their squarefree quotient locator as `chi(W)`, one gets

```text
C_H(X)~chi(psi(X)),       [tau^*chi]=[chi],
Q_J~K_5^2 chi,            chi Q_I~R_7^2.            (9.6)
```

Here `Q_I,Q_J` are the descended partial resultants. The quadratic `chi` is
in the positive `tau`-eigenspace and is reciprocal when `tau(W)=1/W`.
This descent follows from the universal divisor identities, not from an
individual-star lift, so it applies to both diagonal source-subfield
branches. It deletes aligned `c=6`; the near-aligned quotient system remains
open.

The two minimally mixed rows also have an exact capacity ledger. Let `d_j`
be the incidence degree of `j in J` among the ten common-`K` component
stars. The universal color cut gives

```text
2 <= d_j <= 4,                sum_(j in J) d_j = 20. (9.7)
```

For `(a,b,c)=(2,0,2)`, put `K_0=K intersect tau(K)` and let `k_*` be
the remaining label of `K`. The four quartics indexed by `K_0` are supported
on the four-label set `J_0`; their sixteen roots saturate its capacity.
Consequently

```text
d_j=4 (j in J_0),             d_j=2 (j in J_1),
R_(k_*)~P_(J_1)^2,            product_(k in K_0) R_k~P_(J_0)^4. (9.8)
```

The square follows because each of the two reduced quadratic stars in
`R_(k_*)` is supported on the same two-label set `J_1`.

For `(a,b,c)=(1,1,2)`, suppose either `L=I` or `tau(eta) in K`. The
quartic indexed by `tau(eta)` contributes four `J_1` roots, and the two
common-`K` quartics transported to `L^c` contribute at least two each.
This saturates the capacity eight of `J_1`, giving

```text
d_j=4 (j in J_1),             R_(tau(eta))~P_(J_1)^2. (9.9)
```

Every common-`K` quartic transported to `L^c` then has exactly two `J_1`
roots. The sole unsaturated case has

```text
L!=I,       eta,tau(eta) in J_0,
6 <= sum_(j in J_1) d_j <= 8.                       (9.10)
```

Indeed, its three common-`K` labels with non-`K` destinations all transport
to `L^c`, giving the lower bound six; (9.7) gives the upper bound eight.
These are divisor and capacity consequences, not a deletion of either
`c=2` row. In particular, a reciprocal square fiber alone is not a
contradiction.

Provenance: the base argument was first banked as the independently auditable
`prize` node `rate_half_kb_m2_r4_diagonal_facet_mixing_obstruction` at
commit `af28147e`, and the maximally mixed extension at `f45a4d50`; the
minimally mixed refinement is commit
`ac58d21166535a2e6d4c6c9d403c4f753658e344`. The complete proof is
reproduced here rather than imported as an opaque status claim.

## 10. Scope and next action

Proved: the universal category census, the five exhaustive raw integer
profiles, the exact three-profile component-color cut, applicability to the
trivial-stabilizer type, and the universal scope of the exact source-row
interpolation gate and colored partial-resultant split. In the coordinate
branch, the quotient-resultant and common-`K` Vieta-rank systems are exact,
including the negative ramified-fiber exclusion. Endpoint transposition
routes the second coordinate subgroup through a freshly rebuilt coordinate
source record. In the diagonal branch, partition preservation is impossible;
the endpoint involution has one of the five crossing rows (9.4), with the
printed common-`K` support cuts. Aligned `c=6` is impossible, and its
near-aligned survivor has the quotient system (9.6). The `(2,0,2)` row has
the exact degree profile and square/fourth-power identities (9.8). The
`(1,1,2)` row has the saturated identity (9.9) apart from the single orbit
alternative (9.10).

Not proved: a stabilizer action in the trivial branch, realization or
deletion of any of the three surviving profiles, universal failure of the
shared source-row kernel, an owner, payment, K3, the KoalaBear row, or a
Prize result.

For the `(8,1)` type, classify squarefree four-edge divisors `C_H` and route
their two partial-resultant identities through the `45 x 12` source
interpolation gate and complete-source defect budget. Retain exact degree,
irreducibility, deck distinction, and outer-factor side conditions.

For the coordinate type, apply the small Vieta determinants and full
five-fiber kernel before solving `(6.1)` separately in the positive and
negative parity spaces. Preserve the ramified-fiber distinction before
generic endpoint reconstruction. Apply the same program to `<1 x tau>`
only after transposition and reconstruction of its primed source record;
continue the diagonal subgroup as the other independent geometry route.
Split that route by (9.4), starting with `c=2`, and combine the transported
root supports with the reciprocal norm or split-resolvent branch gate. Do
not import the coordinate branch's `I,J` invariance or colored quotient
descent outside the proved near-aligned `c=6` row. For that row, attack the
single reciprocal quadratic system (9.6), not arbitrary four-edge divisors.
For `c=2`, substitute the forced square fiber (9.8) into the source norm or
split-resolvent equation and combine the resulting coefficient minors with
the four-fiber fourth-power product. Keep (9.10) as a separate branch.
