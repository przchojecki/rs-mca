---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the positive coordinate order-two branch, every three-loop packet has one exact outside skeleton, one of four guarded common-kernel placements, and one of eight signed seven-edge Vieta systems; each outside label has an exact 22-term generic eliminant and a separately retained degree-drop branch.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R4_COORDINATE_POSITIVE_THREE_LOOP_ATLAS
quantifier: every actual graph-free Q=6,s=6 inner-degree-two component in the positive coordinate order-two orientation whose five common K-fiber edges contain exactly three antipodal orbits
projection_and_unit: exact source-component graph and Vieta interfaces; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: ten common skeleton orbits overall, exactly two three-loop profile rows, one outside skeleton, four guarded degree-six common residuals, eight signed lanes with seven edges each, and exact generic/degree-drop one-edge eliminants
status: PROVED_COMPILER_POSITIVE_THREE_LOOP_SUBCASE_OPEN_ORDER_TWO_TYPE_OPEN_K3_OPEN
impact: REPLACES_THE_POSITIVE_THREE_LOOP_SEARCH_BY_EIGHT_EXACT_SATURATED_POLYNOMIAL_SYSTEMS
falsifier: a positive coordinate three-loop packet outside the printed skeletons or placements, a failed determinant identity, a third sign orbit, a failed square-root-free Vieta equivalence, or an outside edge not covered by the generic and degree-drop eliminants
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r4_coordinate_positive_three_loop_atlas_v1.py --check --tamper-selftest
---

# KoalaBear positive coordinate three-loop atlas

## 0. Verdict

The pinned order-two source-facet packet proves that the coordinate
orientation has exactly the two signed-pair degree profiles

```text
(4,4,2),             (4,3,3).                       (0.1)
```

The pinned coefficient packet puts the positive source form in the exact
shape

```text
H(T,X)=A_2(W)T^2+A_0(W)+XT B_1(W),       W=X^2.     (0.2)
```

This extension compiles the subcase in which the five common `K`-fiber
edge orbits contain exactly three antipodal target edges. The three loops
use both ramified quotient values and the unique root of `B_1`. The two
remaining common edges give one `4 x 4` kernel with one of four explicit
degree-six determinant residuals. The seven outside edges have one exact
graph skeleton and one binary cycle-sign invariant. Thus the complete
three-loop frontier consists of eight exact saturated polynomial systems.

For each outside edge, the product equation has degree at most two in its
quotient label and the squared-sum equation has degree at most four. Their
generic resultant has 22 terms and total coefficient degree six. The
linear degree-drop branch is retained explicitly.

No one of the eight systems is proved empty. This packet does not delete
positive parity, a coordinate orientation, or the order-two type, and it
books no owner or payment.

## 1. Loop ramification and the ten skeletons

Group the six signed target labels into the three pairs fixed by the target
involution. A common antipodal orbit contributes the same target edge at
both source lifts, hence weight two and defect one. Repeating its target
type would give weight at least four and defect at least six, above the
inherited component defect budget three. Therefore every antipodal type
occurs at most once.

At a positive common quotient label `kappa=[u:v]`, the exact homogeneous
sum row is

```text
uv B_1(kappa)+q_kappa A_2(kappa)=0,       A_2(kappa)!=0. (1.1)
```

Both ramified values `uv=0` force loops. At a nonramified loop,
`q_kappa=0`, so `B_1(kappa)=0`. If `B_1=0`, all five common edges would be
loops, forcing a repeated antipodal type. Hence `B_1` is nonzero and has
only one projective root. A three-loop packet consequently uses both
ramified values and that root.

For pair degrees `d_i`, loop indicators `l_i`, and cross multiplicities
`m_ij`, the common graph obeys

```text
2l_i+sum_(j!=i)m_ij=d_i,       sum_i l_i+sum_(i<j)m_ij=5. (1.2)
```

Exact nonnegative enumeration of (1.2), modulo the equal-degree pair swap,
gives 13 labeled records in ten orbits:

```text
(4,4,2):
  (0,0,0;3,1,1), (0,0,1;4,0,0),
  (0,1,0;2,2,0) [orbit 2],
  (1,1,0;1,1,1), (1,1,1;2,0,0);

(4,3,3):
  (0,0,0;2,2,1),
  (0,0,1;3,1,0) [orbit 2],
  (1,0,0;1,1,2),
  (1,0,1;2,0,1) [orbit 2],
  (1,1,1;1,1,0).                                (1.3)
```

The final row in each profile is the unique three-loop orbit.

## 2. Complete outside graph

Normalize the three common loop quotient labels to `0,infinity,1`, with
the first two ramified. An outside loop would have to reuse a ramified
quotient label or give a second nonramified root of `B_1`; neither is
possible.

Let `D,E,F` be the three outside signed target pairs. Let `r_i` count the
two colored edges from the deficient common pairs and let
`m=(m_DE,m_DF,m_EF)` count the five internal outside edges. Degree four
gives

```text
r_D+m_DE+m_DF=4,
r_E+m_DE+m_EF=4,
r_F+m_DF+m_EF=4,
sum r_i=2,                     sum m_ij=5.          (2.1)
```

Modulo `S_3`, (2.1) has only

```text
(r;m)=(0,0,2;3,1,1),          (0,1,1;2,2,1),      (2.2)
```

each with three labeled realizations. The three common loops already spend
the full defect budget three. A multiplicity-three cross pair has only two
signed deck-orbit types and incurs at least two further units of defect.
The first record in (2.2) is therefore impossible. The unique survivor is

```text
r=(0,1,1),                    m=(2,2,1).            (2.3)
```

Thus the colored edges attach to two distinct outside pairs. The uncolored
pair uses both signed cross types with each colored pair; the edge between
the colored pairs retains one free sign.

## 3. Common `4 x 4` kernel

Write the signed loop targets at `W=0,infinity,1` as
`a_0,a_infinity,a_1`. Put

```text
A_2(W)=d_0+d_1W+d_2W^2,            B_1(W)=beta(W-1). (3.1)
```

The three loop product rows force

```text
A_0(W)=-a_0^2d_0
 +[(a_0^2-a_1^2)d_0-a_1^2d_1
   +(a_infinity^2-a_1^2)d_2]W
 -a_infinity^2d_2W^2.                               (3.2)
```

For a remaining common edge with source lift `z`, quotient label `W=z^2`,
target product `p`, and signed target sum `s`, its product and sum rows on
`h=(d_0,d_1,d_2,beta)^T` are

```text
[-a_0^2+(a_0^2-a_1^2)W-p,
 -(a_1^2+p)W,
 (a_infinity^2-a_1^2)W-(a_infinity^2+p)W^2,
 0],

[s,sW,sW^2,z(W-1)].                                (3.3)
```

The two nonloop common edges therefore give an exact `4 x 4` matrix `M`.
Every packet gives an admissible nonzero kernel vector with `beta!=0` and
`A_2` nonzero at all common labels. Conversely, such a kernel reconstructs
all five common Vieta rows.

## 4. Four common placements

Normalize the loop targets to `1,b,c` at `0,infinity,1`, and write the two
nonloop source lifts as `x,y`. Define the common source guard

```text
S=xy(x^2-1)(x^2-y^2)(y^2-1).                       (4.1)
```

The root of `B_1` can carry the low- or high-degree loop role. Modulo the
ramified-value interchange, there are exactly two placements for each
profile. Their determinant factorizations are:

```text
442 root low:
  det M=-S(b^2-1) R_442,L
  R_442,L=(y-x)(b^2-c^2)+bxy(x+y)(c^2-1).

442 root high:
  det M=-S(c^2-1) R_442,H
  R_442,H=(y-x)(b^2-c^2)
    +xy[x(c-1)(b^2+c)+y(c+1)(b^2-c)].

433 root low:
  det M=S(b+1)(c+1) R_433,L
  R_433,L=(y-x)(b^2-c^2)
    +(c-1)xy[b(c+1)x-(b^2+c)y].

433 root high:
  det M=S(b+c)(c+1) R_433,H
  R_433,H=(b-c)[(b+c)y-(bc+1)x]
    +xy(c-1)[(b^2+c)x-b(c+1)y].                    (4.2)
```

Each residual has total degree six. Equation (4.2) is applied only away
from all inherited source and target collision guards. It is a necessary
common-kernel cut, not a claim that every residual point gives an
admissible packet.

## 5. Eight signed outside lanes

Name the uncolored outside pair `d` and the colored pairs `e,f`. For profile
`442`, the two colored attachments come from its deficient pair. For
profile `433`, one comes from each deficient pair. Target-sign gauge puts
the seven edges in the exact form

```text
colored:  a e, a' f;
internal: de,-de, df,-df, sigma ef,       sigma in {+1,-1}. (5.1)
```

The three raw signs on the two colored edges and the single `ef` edge have
eight assignments. Flipping the representatives of `e` and `f` gives
orbits of size four; their only invariant is the product `sigma`. The four
common placements in (4.2) therefore give exactly eight signed lanes and
56 edge records.

For signed target representatives `r,t`, edge product `p`, and squared sum

```text
s^2=r^2+t^2+2p,                                    (5.2)
```

put `D=A_2`, `E=A_0`. The square-root-free equations for one outside
quotient label `w` are

```text
P_p(w)=E(w)-pD(w)=0,
Q_p,s(w)=beta^2 w(w-1)^2-s^2D(w)^2=0.              (5.3)
```

Under

```text
beta D(w) w(w-1)(w-x^2)(w-y^2)!=0,                 (5.4)
```

(5.3) is equivalent to the original product row and one of the two source
lifts of the sum row. A full lane must additionally saturate by every
`w_i-w_j` and every signed-target square-collision factor. The resultant
of one pair in (5.3) is only a necessary scalar cut before these
saturations.

## 6. One-edge eliminant

Write

```text
P(w)=Aw^2+Bw+C,
Q(w)=q_4w^4+q_3w^3+q_2w^2+q_1w+q_0.               (6.1)
```

The coefficients from (3.2) and (5.3) are

```text
A=-(a_infinity^2+p)d_2,
B=(a_0^2-a_1^2)d_0-a_1^2d_1
  +(a_infinity^2-a_1^2)d_2-pd_1,
C=-(a_0^2+p)d_0,                                   (6.2)

(q_0,...,q_4)=
(-s^2d_0^2,
 beta^2-2s^2d_0d_1,
 -2beta^2-s^2(d_1^2+2d_0d_2),
 beta^2-2s^2d_1d_2,
 -s^2d_2^2).                                       (6.3)
```

On the generic branch `A!=0`, define

```text
R_1=q_4(-B^3+2ABC)+q_3A(B^2-AC)-q_2A^2B+q_1A^3,
R_0=q_4(-B^2C+AC^2)+q_3ABC-q_2A^2C+q_0A^3.        (6.4)
```

Polynomial division of `A^3Q` by `P` gives remainder `R_1w+R_0`, and

```text
A^3 Res_w(P,Q)=A R_0^2-B R_0R_1+C R_1^2.          (6.5)
```

The resultant in (6.5) has 22 terms and total degree six in
`A,B,C,q_0,...,q_4`.

The degree drop is genuine. Since `d_2!=0`, `A=0` exactly when
`p=-a_infinity^2`. If `B!=0`, the unique product root is `w=-C/B`, and the
exact cleared sum cut is

```text
L=q_4C^4-q_3C^3B+q_2C^2B^2-q_1CB^3+q_0B^4=0.     (6.6)
```

If also `B=0`, then `C!=0` under the loop-target collision guards, so the
constant product equation has no root. Thus (6.5) and (6.6) exhaust every
outside edge without dividing away the repeated-product branch.

## 7. Scope and next action

Proved: the loop nonrepetition and ramification gate; the exact ten-orbit
common skeleton census; the unique complete outside graph in the
three-loop subcase; the four common placement determinants; the two sign
orbits and eight signed Vieta lanes; the square-root-free edge equivalence;
and the generic and degree-drop one-edge eliminants.

Not proved: emptiness of any saturated lane, simultaneous compatibility of
the seven outside labels, the remaining source-facet or outer-factor
conditions, deletion of positive parity or another orientation, an owner,
payment, K3, the KoalaBear row, or a Prize result.

The next exact task is one parametric saturation calculation per lane,
retaining the guards in (5.4), all label-separation factors, and all target
collisions. A bare product of the seven scalar resultants cannot close a
lane. Any survivor must then be reconstructed through the full common
kernel and tested against the remaining source-facet and outer-component
identities.
