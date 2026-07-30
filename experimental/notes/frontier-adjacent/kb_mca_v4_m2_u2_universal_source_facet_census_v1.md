---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every residual degree-two source component, including the trivial-stabilizer type, has the exact (J-J,I-I,I-J)=(10,10,4) census; component edge coloring cuts the five raw K-fiber profiles to three, every survivor passes the same exact 45-by-12 source-row interpolation gate, its I/J row products split through one squarefree colored quartic, the coordinate orientation descends this to explicit quotient-resultant and five-fiber Vieta-rank equations, endpoint transposition routes the other coordinate subgroup through a fresh source record, and the diagonal endpoint involution must mix I and J in one of five exact crossing-orbit rows, with aligned c=6 impossible, its near-aligned survivor reduced to one reciprocal colored quotient system, the c=2 rows reduced to exact incidence-capacity and square-fiber alternatives, every saturated c=2 square fiber in the source-line branch giving an exact 4/3-dimensional complete-source coefficient cut even at ramification, the entire (2,0,2) diagonal row deleted in both source-subfield branches by the complete-source defect budget, and the saturated (1,1,2) cases reduced to 123 matching-preserving edge orbits, only 12 in the source-line branch, where their colored quartic is the pullback of the explicit two-label quotient Omega=J_1 in the aligned case or Omega={xi,ell} in the near-aligned case, every forced-square survivor obeys one of four explicit odd-part incidence equations, each classified packet reconstructs at most eight source-deck candidate pairs, every reconstructed candidate obeys one prescribed degree-eight J_1-slice resultant identity before the full quotient system, and the 12 negative assignments reduce to 8+4 normalized templates supported only on explicit B or BC factor loci after the apparent A locus is excluded by a fixed internal label.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_U2_UNIVERSAL_SOURCE_FACET_CENSUS
quantifier: every actual graph-free Q=6,s=6,u=2 source component in the residual inner-degree-two order-two or trivial-stabilizer types
projection_and_unit: exact source-facet interface; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: exact universal facet/color/interpolation/resultant interfaces plus coordinate descent to one quotient quadratic, explicit 8/7-dimensional cubic-norm equations, exact 10-by-8 or 10-by-7 K-fiber Vieta gates, transpose transport of the second coordinate subgroup, deletion of the partition-preserving diagonal subcase and aligned c=6, quotient descent of the near-aligned c=6 colored divisor, exact c=2 crossing-degree, square-fiber, fourth-power-product, and exceptional-capacity pins, exact source-line square-fiber coefficient cuts of dimensions 4/3 both off ramification and after the ramified complete-source repair, complete deletion of the diagonal (2,0,2) orbit row, exact saturated (1,1,2) defect packet counts 1560/123 and source-line counts 96/12, exact source-line colored-divisor descent to two complete unramified quotient fibers with Q_J proportional to K_5^2 chi_Omega and chi_Omega Q_I proportional to R_7^2, exclusion of internal-K source ramification, an exact four-case rational odd-part incidence gate for every forced-square survivor, injective internal-star reconstruction to at most eight source-deck pairs per classified packet, the necessary J_1-slice identity Res_T(P_J1,U^2-WV^2) proportional to (W-w)^4 chi_mix^2, and exact negative reconstruction determinants supported on B=0 or BC=0
status: PROVED_FACET_COLOR_INTERPOLATION_RESULTANT_COORDINATE_QUOTIENT_VIETA_RANK_TRANSPOSE_DIAGONAL_MIXING_C6_QUOTIENT_C2_CAPACITY_C2_SOURCE_LINEAR_C2_202_ROW_DEFECT_C2_112_SATURATED_DEFECT_C2_112_SOURCE_QUOTIENT_C2_112_ODD_INCIDENCE_C2_112_RAMIFIED_REPAIR_C2_112_FINITE_RECONSTRUCTION_C2_112_Q_SLICE_C2_112_NEGATIVE_FACTOR_AND_C2_112_ALIGNED_NEGATIVE_EXCLUSION_INTERFACES_TYPES_OPEN_K3_OPEN
impact: GIVES_EXACT_TRIVIAL_SOURCE_INTERFACES_AND_REDUCES_ORDER_TWO_TO_ONE_COORDINATE_ROUTE_PLUS_FOUR_DIAGONAL_MIXING_ROWS_WITH_C6_AT_ONE_QUOTIENT_SYSTEM_THE_202_ROW_EMPTY_AND_SATURATED_112_AT_123_OR_12_EDGE_ORBITS_WITH_ONE_EXPLICIT_SOURCE_LINE_QUOTIENT_QUADRATIC_FOUR_ODD_PART_LABEL_TESTS_NO_RAMIFIED_COEFFICIENT_ESCAPE_AT_MOST_EIGHT_SOURCE_DECK_PAIRS_PER_PACKET_ONE_DEGREE_EIGHT_Q_SLICE_PREFILTER_NEGATIVE_B_OR_BC_FACTOR_LOCI_AND_NO_ALIGNED_NEGATIVE_Q_SLICE_SURVIVOR
falsifier: an actual degree-two component outside the universal source interfaces, a coordinate component whose colored divisor, paired-root resultants, or printed K-fiber Vieta gates fail, failure of endpoint transposition after rebuilding the source record, an actual diagonal component whose endpoint involution preserves I and J, an aligned c=6 component, failure of the near-aligned c=6 quotient identities, a c=2 component violating the printed incidence degrees, square-fiber identities, or exceptional capacity interval, a saturated source-line c=2 square fiber violating the printed coefficient ranks, any actual diagonal (2,0,2) packet, a saturated (1,1,2) packet outside the printed defect census, a saturated source-line (1,1,2) packet whose colored divisor or partial resultants fail (9.17)--(9.18), or one with a ramified internal K orbit, disjoint internal pure stars, zero odd part, failed incidence equation (9.21), ramified root-row orders other than (2,2), noninjective internal U evaluation, more than eight source-deck candidate pairs, failure of the necessary q-slice identity (9.24), or a negative reconstruction outside the factor loci (9.25)
aligned_negative_falsifier: an admissible aligned negative reconstruction satisfying the q-slice identity despite (9.27)
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

There is nevertheless an exact linear consequence in the source-line branch.
Use the coefficient normal form

```text
H(T,X)=U(T,W)+XV(T,W),       G(T,W)=U(T,W)^2-WV(T,W)^2,
W=X^2.                                                        (9.11)
```

Let `w` index one of the forced square fibers in (9.8) or (9.9), and put
`q=P_(J_1)`. If the source fiber over `w` is unramified, its two reduced
stars are `U(T,w)+xV(T,w)` and `U(T,w)-xV(T,w)`, and both are projectively
`q`. Since `x!=0`,

```text
U(T,w) in <q>,       V(T,w) in <q>.                 (9.12)
```

Evaluation of each reciprocal `U` and `V` coefficient vector at
`w notin {0,+1,-1}` is surjective onto the three-dimensional quadratic
space. Each membership condition in (9.12) has rank two. Thus the common
rank-four cut reduces the positive/negative source spaces exactly from
dimensions `8/7` to `4/3`.

Writing `m_ij=u_i v_j-u_j v_i` for the three coefficient minors and
normalizing the reciprocal source-orbit locator as
`chi_w=(W-w)(W-w^(-1))=W^2-sW+1`, the same cut is certified by

```text
m_12= chi_w(AW+B),
m_01=-chi_w(BW+A),
m_02= C chi_w(W-1).                                  (9.13)
```

The ramified orbit `{0,infinity}` is genuinely weaker and must be retained.
There the two source points coincide. At zero only `U(T,0) in <q>` follows
(and at infinity the leading `W^2` coefficient of `U` is used). This is a
rank-two cut with dimensions `6/5`; no condition on the corresponding value
of `V` and no common-minor factor (9.13) follows. Hence an argument that
deduces (9.13) directly from the whole-fiber square without separating
ramification is invalid.

For the stronger `(a,b,c)=(2,0,2)` row, the ramified alternative is in
fact impossible. If the forced square fiber uses one branch value, its
reciprocal partner uses the other. The two coincident square-root stars are
distinct `J-J` and `I-I` vertices of weight at least two, contributing
defect two. The four labels in `K_0` are then unramified and contribute
eight reduced stars supported on `J_0`. There are only
`binom(4,2)=6` possible `J_0` edges, and balancing eight units over six
vertices gives

```text
sum_(J_0 edges e) binom(weight(e),2) >= 2.
```

Thus the total complete-source defect is at least `2+2=4`, contradicting
the proved budget three. Hence

```text
(2,0,2) source-line row => forced square fiber unramified
                         => coefficient dimensions 4/3.       (9.14)
```

In fact the same budget deletes the entire `(2,0,2)` row. Ramification was
not needed to obtain the first defect cost two: `R_(k_*)=P_(J_1)^2` always
has two identical reduced component stars, and whole-fiber transport gives
a second square on `tau(J_1) subset I`. These are distinct doubled vertices
in every source-subfield branch. The eight `J_0` stars still have the exact
defect floor two. Therefore

```text
(a,b,c)!=(2,0,2)                                    (9.15)
```

for every actual diagonal component. Four rows remain:
`(1,1,2),(1,0,4),(0,1,4),(0,0,6)`. This does not delete the ramified
alternative in `(1,1,2)`.

The saturated `(1,1,2)` cases have an exact one-unit defect ledger. Their
reciprocal square vertices have weight exactly two and consume two defect
units. A third occurrence of either square edge would already raise total
defect to four. The remaining common-`K` stars are therefore

```text
four reduced J_0-J_0 edges,
four reduced J_0-J_1 edges, each J_1 label used twice,
collision_defect(pure)+collision_defect(mixed)<=1. (9.16)
```

The possible `J_0` degree profiles are exactly
`(2,2,4,4),(2,3,3,4),(3,3,3,3)`. Exhausting edge multisets gives `1,560`
labeled packets in `123` orbits under the order-16 relabeling group that
preserves the two `tau` pairs of `J_0` and may swap `J_1`.

In the source-line branch, the four pure edges are a union of two
`tau`-edge orbits. A repeated mixed edge would repeat its transported
`I-J` partner as well and spend two residual defect units, so all four mixed
edges are distinct. Exactly `96` labeled packets in `12` matching-preserving
orbits remain; their transported partners are all four universal `I-J`
stars. These counts are combinatorial admissibility lists, not component
realization or deletion. The exceptional case (9.10) is outside the list.

The source-line list has one common quotient compiler. Put

```text
K_Lc={k in K: tau(k) in L^c},       Omega=tau(K_Lc).
```

There are exactly two labels in `K_Lc`. The four mixed common-`K` stars are
distinct by (9.16), and individual-star equivariance transports them to the
four `I-J` stars. Since the universal census has exactly four such stars,
the transported stars exhaust that category. The two stars over each label
of `K_Lc` transport to the two points in the complete source fiber over its
image in `Omega`. Consequently

```text
|Omega|=2,       C_H(X) ~ chi_Omega(psi(X)).       (9.17)
```

Both fibers over `Omega` are unramified, because `C_H` is squarefree. In
the aligned case `L=I`, `Omega=J_1`. In the near-aligned saturated case
`tau(eta) in K`,

```text
Omega={xi,ell},
```

where `ell` is the other crossing label in `J intersect L^c`. This pair is
not asserted to be a `tau` orbit.

Let `K_5` and `R_7` be the quotient locators on `K` and its seven-label
complement. Substitution of (9.17) into the two universal partial-resultant
identities, followed by faithful descent through the quadratic pullback,
gives

```text
Q_J ~ K_5^2 chi_Omega,       chi_Omega Q_I ~ R_7^2. (9.18)
```

Thus the twelve source-line edge orbits need no arbitrary four-root colored
divisor search: they split into the aligned quotient `chi_Omega=P_(J_1)`
and the near-aligned quotient `chi_Omega=P_{xi,ell}`. Equations
(9.17)--(9.18) do not realize or delete either case.

There is also a scalar gate before full interpolation. Let `{z,z^(-1)}` be
the unique internal common-`K` orbit. It cannot be the ramified source
orbit: ramification would make the two stars over `z` equal and the two
stars over `z^(-1)` reciprocal-equal, costing at least two pure-edge
collision units against the one-unit residue in (9.16). Hence

```text
the internal common-K orbit is source-unramified. (9.19)
```

Write its two stars over `z` as edges `e,f` on `J_0`. They are distinct.
If they were disjoint, then on four vertices they would be either the two
fixed `tau` edges or one edge and its `tau` partner; the four-star multiset
`e,f,tau(e),tau(f)` would again cost defect two. Thus `e,f` share exactly
one endpoint `a`, and

```text
U(a,z)=V(a,z)=0.                                  (9.20)
```

Suppose the forced square orbit `w` is unramified and write
`q=P_(J_1)=q_0+q_1T+q_2T^2`. Deck distinction gives `V!=0`. Since
evaluation of the reciprocal three-dimensional `V` space at `w` is an
isomorphism, `V(T,w)~q(T)` pins its projective class. For
`epsilon in {+1,-1}`, set

```text
F=q_0-epsilon*w*q_2,       G=epsilon*q_2-w*q_0,
M=q_1(1-epsilon*w),
N_epsilon(a)=F+Ma+epsilon*G*a^2,
D_epsilon(a)=G+epsilon*Ma+epsilon*F*a^2.
```

Then

```text
V ~ (F+GW)+M(1+epsilon W)T+epsilon(G+FW)T^2,
D_epsilon(a)!=0,       z=-N_epsilon(a)/D_epsilon(a). (9.21)
```

Indeed `V(a,W)=N_epsilon(a)+W D_epsilon(a)`. If both coefficients
vanished, then `V(a,w)=0` and hence `q(a)=0`, contrary to
`a in J_0` and `Root(q)=J_1`. Thus every unramified forced-square record
has only four cheap tests: two signs and two reciprocal `J_0` orbits. This
does not address the forced-ramified branch.

Complete-source multiplicity repairs that last coefficient escape. Orient a
forced-ramified orbit as `W=X^2=0`. The two rows indexed by the projective
roots `r,s` of `q` are the only endpoint rows vanishing at `X=0`. Each row
divides `B/z_i`, so its order is at most two at the double source pole.
Local saturation gives

```text
ord_0 H(r,X)+ord_0 H(s,X)=2 ord_0(B)=4.
```

Thus both orders equal two. In
`H(j,X)=U(j,X^2)+X V(j,X^2)`, vanishing of the linear coefficient gives
`V(r,0)=V(s,0)=0`. Deck distinction excludes `V=0`, and therefore

```text
U(T,0) in <q>,       V(T,0) in <q> minus {0}.       (9.22)
```

The two independent line-membership conditions have total rank four, so
the ramified source dimensions are also `4/3`, not the square-only `6/5`.
After normalizing `V(T,0)=q(T)`, formula (9.21) applies with `w=0`.
Geometric source ramification is retained, but it has no separate
coefficient route.

The internal star pair now removes all remaining continuous coefficient
freedom. Let `S_epsilon(w,q)` be the reciprocal `U` space satisfying
`U(T,w) in <q>`. If `U in S_epsilon(w,q)` vanishes at the internal label
`z`, reciprocity gives

```text
U(T,W)=chi_z(W)R(T),       T^2R(1/T)=epsilon R(T).
```

Since the forced and internal orbits are distinct, `U(T,w) in <q>` would
make `q` an endpoint reciprocal eigenform. This is impossible because
`Root(q)=J_1` and `tau(J_1) subset I`. Therefore evaluation at `z` is
injective:

```text
S_+(w,q) -> Sym^2(T) is a 3 x 3 isomorphism,
S_-(w,q) -> Sym^2(T) is an injective two-plane.     (9.23)
```

For internal edge quadratics `e,f`, the pinned nonzero `V(T,z)` fixes the
relative nonzero scalars in

```text
2xV(T,z)=lambda e(T)-mu f(T),       x^2=z.
```

It therefore fixes the target
`U(T,z)=(lambda e+mu f)/2`. Equation (9.23) gives one positive source form,
and either rejects the negative sign by one plane equation or gives one
negative form, modulo source-deck conjugation. The five pure multisets have
`2,2,4,2,2` compatible internal assignments, so every classified packet
has at most eight source-deck candidate pairs. The next quotient check is a
finite exact calculation, not a coefficient search.

That quotient check has a smaller necessary first pass. Put

```text
G(T,W)=U(T,W)^2-WV(T,W)^2
```

and let `K_mix={k_1,k_2}` be the two remaining common-`K` labels carrying
the four mixed `J_0-J_1` stars. For either root `r` of `q`, the forced
square makes `G(r,W)` divisible by `(W-w)^2`, including at the repaired
ramified value `w=0`. If `r` occurs `m_(r,i)` times in the two stars over
`k_i`, the unramified product formula gives a zero of order `m_(r,i)`.
These mixed fibers are unramified because the source-line lift transports
them to the unramified complete fibers of the squarefree colored divisor.
Each `r` occurs twice among all four mixed stars, and each mixed fiber has
two `J_1` incidences. Since `deg_W G(r,W)<=4` and `G(r,W)` is nonzero for a
reduced irreducible source component, these roots exhaust its divisor.
Multiplying over the two roots of `q` gives

```text
Res_T(q(T),G(T,W))
  ~ (W-w)^4 ((W-k_1)(W-k_2))^2.                  (9.24)
```

In the aligned branch `(W-k_1)(W-k_2)~tau^*q`; in the near-aligned branch
it is `tau^*chi_Omega`, where `Omega={xi,ell}`. Equation (9.24) is a
necessary `J_1`-slice prefilter, not a sufficient replacement for either
identity in (9.18).

The negative image-plane equation also factors before (9.24). An endpoint
coordinate change commuting with `tau` orients the common internal endpoint
as `2`; write

```text
J_0={2,1/2,b,1/b},       q=(T-c)(T-d).
```

The twelve compatible internal assignments consist of eight fixed-moving
templates `({2,1/2},{2,b})` and four moving-moving templates
`({2,b},{2,1/b})`. Put

```text
E=cdw+4cd-2cw-2c-2dw-2d+4w+1,
A=5cd-4c-4d+5,
B=bcd-2bc-2bd+b+2cd-c-d+2,
C=2bcd-bc-bd+2b+cd-2c-2d+1,
Pi=(c-2)(2c-1)(d-2)(2d-1)(w-1)^5(w+1)^5(cd-1)^2.
```

Direct expansion of the augmented `5 x 5` reconstruction determinant gives

```text
Delta_F=-6 Pi A^2 B / ((2b-1)E^5),
Delta_M= 6 Pi A B C / (((b-1)(b+1))E^5).          (9.25)
```

Here `E` is the nonzero incidence denominator; every factor in `Pi` and the
remaining displayed denominators is nonzero by label distinctness,
fixed-point-freeness, and `tau(J_1) subset I`. The reconstructed internal
label also obeys

```text
z+1=(1+w)A/E.                                      (9.26)
```

The internal orbit and source label are fixed-point-free, so `z!=-1` and
`w!=-1`; hence `A!=0`. Since the coefficient matrix has rank four, negative
candidates exist exactly on `B=0` in the first template and `BC=0` in the
second. These two genuine loci are retained for (9.24); neither `B` nor `C`
is divided out.

The aligned target deletes both retained negative loci. Write

```text
P=cd-2c-2d+1,       Q=2cd-c-d+2,
B=bP+Q,              C=bQ+P=b B(1/b).
```

The moving template is unchanged by `b->1/b`, so its `C=0` locus is the
represented `B=0` locus. On `B=0`, `P!=0`: otherwise `P=Q=0` gives first
`c+d=0` and then `c^2=1`, contrary to fixed-point-free labels. Hence
`b=-Q/P`.

For either template, divide `Res_T(q,U^2-WV^2)` by `(W-w)^4`, make the
residual quartic monic, and subtract the aligned target
`((W-1/c)(W-1/d))^2`. If `m_j` is its `W^j` coefficient, exact
reconstruction gives

```text
m_0=(cd-1)(cd+1)/(c^2 d^2),
cd=-1  =>  m_1-m_3=4(c^2-1)/c=-A.                 (9.27)
```

The first identity and `cd!=1` force `cd=-1`; the second then contradicts
the proved `A!=0`. Thus no aligned negative candidate passes (9.24). This
does not delete the aligned positive sign or either near-aligned sign, whose
target is `tau^*chi_Omega` rather than `tau^*q`.

Provenance: the base argument was first banked as the independently auditable
`prize` node `rate_half_kb_m2_r4_diagonal_facet_mixing_obstruction` at
commit `af28147e`, and the maximally mixed extension at `f45a4d50`; the
minimally mixed refinement is commit
`ac58d21166535a2e6d4c6c9d403c4f753658e344`. The source-line linear cut
and ramification repair are commit
`30c4a8a44f25caf37567b589146f52503bca72dc`; the `(2,0,2)` ramified-defect
exclusion is commit `9d31dd05ad53f079ef41a4cc05cc479e241f768b`. The complete
row deletion is commit `9aea5c6027fc35285f23ffbbf5b55cf1828d23e2`.
The saturated `(1,1,2)` classifier is commit
`7eb3d2d9f8ed13fd44f54e646d0edc90d2748bba`.
The source-line colored quotient compiler is commit
`623eff354b0e844e265ba947cf857d37c1e6b1ae`.
The odd-part incidence gate is commit
`e133e40f6eb2054d9d368a7b3b6208b87df8c564`.
The ramified complete-source repair is commit
`a3054003fe8080940443d641fbefc4aa1fe89c66`.
The internal-star reconstruction is commit
`80045e37cfee303187e1ce8fc6639f4311350c24`.
The `J_1`-slice resultant gate is commit
`0d9990c030978339e15c1d930275e14ffb3be5bd`.
The negative reconstruction factor gate is commit
`eae904eec48f1f09d027bd83ea0d51816b9502a6`.
The fixed-label exclusion of its apparent `A=0` locus is commit
`24b4682367ae289cea3dd24e2fbf56d473f95963`.
The aligned negative q-slice exclusion is commit
`43541fc31451ca5f27bf51b2ba80ddb161feccde`.
The complete proof is reproduced here rather than imported as an opaque
status claim.

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
near-aligned survivor has the quotient system (9.6). The `(2,0,2)` row is
deleted by (9.15). The `(1,1,2)` row has the saturated identity (9.9) apart
from the single orbit alternative (9.10), and its saturated cases have the
exact packet census (9.16). In the source-line branch, every saturated square fiber
has the exact unramified `4/3`-dimensional or ramified `6/5`-dimensional
linear cut (9.12)--(9.13), and its colored divisor and partial resultants
descend to the explicit quotient system (9.17)--(9.18). Its internal
common-`K` orbit is unramified by (9.19); when the forced orbit is also
unramified, it must pass one of the four incidence tests (9.21).
Complete-source multiplicity extends the same `4/3` cut and incidence test
to the forced-ramified branch by (9.22). Internal-star evaluation then
reduces every classified source-line packet to at most eight source-deck
pairs by (9.23). Every reconstructed candidate then obeys the necessary
degree-eight `J_1`-slice identity (9.24), and negative candidates are first
restricted to the factor loci (9.25). In the aligned branch both retained
negative loci are then deleted by (9.27).

Not proved: the aligned positive sign, either near-aligned sign, a
stabilizer action in the trivial branch, realization or
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
Remove `(2,0,2)` by (9.15). For `(1,1,2)`, attack the saturated cases by
applying (9.21), including its repaired ramified instance (9.22), before
combining the aligned and near-aligned instances of
(9.18) with the finite reconstructions from (9.23). In the aligned branch
retain only the positive sign after (9.27). In the near-aligned branch,
restrict negative forms by (9.25) and apply (9.24) with the actual
`tau^*chi_Omega` target before forming either degree-six partial resultant;
route the 123
branch-independent orbits through the split resolvent.
Keep (9.10) and the biquadratic source-cover branch separate.
