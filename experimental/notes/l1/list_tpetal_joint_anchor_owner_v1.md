---
workboard_item: T
row: symbolic smooth RS full-petal source cell at arbitrary t; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: one exact labelled support of total degree h with d<h<=2d+1
B_star: not_applicable
direct_statement: one determinant-coordinate gcd simultaneously recovers common defect roots and common background-agreement roots; all other background roots are affine coordinate equations; every fixed joint owner has an exact packing payment and a dual-domain bounded-tail split-pencil coordinate
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed labelled arbitrary-t monic pair slice with one exact anchor
quantifier: every field and every source partition satisfying the companion primitive remainder theorem
projection_and_unit: determinant coordinates with their split locators, reconstructed numerators, and source-background roots
claimed_bound: exact joint-owner identity, exact owner-containment dimension, binomial-ratio fixed-owner packing, and a two-generator coefficient parameterization of every fixed owner chamber; no owner-aggregate, deployed-row, or endpoint bound
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a common anchor defect or background root missed by the gcd, an extraneous gcd root, a non-anchor background root not represented by the printed affine equation, a fixed-owner family exceeding the binomial ratio, or a candidate violating the owner-cancelled determinant or two-generator coordinate
replay: analytic proof; no computational claim
---

# General t-petal joint anchor owner

## 1. Setup

Use the primitive remainder chart of
`list_tpetal_anchor_pade_chart_v1.md`. Let `(F,W)` be the squarefree split
anchor, let `Bkg` be the source background, and put

```text
R_0={y in Bkg: W(y)=0},       P_0=F L_(R_0).          (1.1)
```

For a coordinate `H`, write `(G_H,B_H)` for its reconstructed pair and

```text
R_H={y in Bkg: B_H(y)=0}.
```

The core, background, and petals are disjoint.

## 2. Joint owner theorem

### Theorem 2.1

One coordinate gcd recovers both anchor-relative owners:

```text
gcd(H,L_(R_0))=gcd(B_H,L_(R_0)),                     (2.1)
gcd(H,P_0)=gcd(G_H,F) gcd(B_H,L_(R_0)).              (2.2)
```

Equivalently, the roots of `(2.2)` are exactly

```text
(Z(G_H) intersect Z(F)) disjoint_union (R_H intersect R_0). (2.3)
```

Every distinct candidate consequently obeys

```text
|Z(G_H) intersect Z(F)|+|R_H intersect R_0|<=e-1.    (2.4)
```

#### Proof

At `y in R_0`, the determinant identity becomes

```text
F(y)B_H(y)=Lambda(y)H(y).
```

Both displayed factors are nonzero on the source background, so
`B_H(y)=0` exactly when `H(y)=0`. Squarefreeness proves `(2.1)`. The
companion anchor-coordinate theorem gives

```text
gcd(H,F)=gcd(G_H,F).
```

Since `F` and `L_(R_0)` are coprime, multiplying the identities proves
`(2.2)--(2.3)`. Finally `H!=0` and `deg H<=e-1` prove `(2.4)`. QED.

## 3. Exact owner strata

Let `Q|P_0` be monic of degree `q<=e-1`. The coordinates whose joint owner
contains `Q` are exactly

```text
H=QK,       deg K<=e-1-q.                             (3.1)
```

This is a linear coordinate space of dimension `e-q`. The exact-owner
stratum is obtained by imposing

```text
gcd(K,P_0/Q)=1.                                       (3.2)
```

Thus defect and background owners are not independent pencils or ledgers;
they are one divisor stratum in the same low-degree coordinate body.

## 4. Remaining background equations

With

```text
Remainder_H=rem_F(-Lambda H W^(-1)),
T_H=(Remainder_H W+Lambda H)/F,                       (4.1)
```

the exact inverse reads `B_H=W+T_H`, and `T_H` is linear in `H`. Hence for
every `y in Bkg\R_0`,

```text
B_H(y)=0 iff T_H(y)=-W(y),                            (4.2)
```

one affine linear equation on the coordinate body.

## 5. Fixed joint-owner packing

For one surviving full-petal cell, write

```text
N=|C|,       b=|Bkg|,       r=2d-t ell=e-1,
u=d-(t-1)ell,       v=max(0,u).                       (5.1)
```

Fix an exact owner `Q=gcd(H,P_0)` of degree `q`. Let `F_Q` be the distinct
exact candidates with this owner. Then

```text
|F_Q| <= floor(
  binom(N+b-q,r-q+1) / binom(d+v-q,r-q+1)
).                                                    (5.2)
```

Indeed, each candidate's combined defect/background marked set has size at
least `d+v`. Two such marked sets meet in at most `r` points by the joint
determinant degree budget. After removing the common `q` owner roots, the
sets have size at least `d+v-q` in an `N+b-q` point universe and meet in at
most `r-q` points. No `(r-q+1)`-subset can occur twice, so double counting
proves `(5.2)`.

The denominator is always defined. If `u>=0`, then `d+v-r=ell`. If `u<0`,
then `d+v-r=t ell-d>=ell-b>=1` by the list threshold. In particular, for
`q=r-c`,

```text
|F_Q|<=n^(c+1).                                       (5.3)
```

Every bounded co-deficiency chamber is therefore polynomial per fixed
joint owner.

## 6. Dual-domain bounded-tail split-pencil reduction

Fix one distinct exact candidate and abbreviate `(G_H,B_H)` to `(G,B)`. Put

```text
D=gcd(F,G),       E=gcd(B,L_(R_0)),
Q=gcd(H,P_0)=D E,       q=deg Q,       c=r-q.         (6.1)
```

The factors `D,E` have roots in the disjoint core and background. Since
`D|F,G` and `E|W,B`, define

```text
A=F/D,       C=G/D,       U=W/E,       V=B/E,
K=H/(D E).                                             (6.2)
```

### Theorem 6.1

The reduced rows satisfy

```text
A V-C U=Lambda K,       K!=0,       deg K<=c,         (6.3)
gcd(A,C)=gcd(A,U)=gcd(C,V)=1.                         (6.4)
```

The locator entries `A,C` are monic squarefree and split on the core. For
every touched petal,

```text
E U == c_i D A (mod L_i),
E V == c_i D C (mod L_i),                             (6.5)
```

or, equivalently, after inverting the core/background factors modulo the
petal locator,

```text
U == c_i D E^(-1) A (mod L_i),
V == c_i D E^(-1) C (mod L_i).                        (6.6)
```

#### Proof

The joint-owner identity gives `Q=DE` and hence `H=DEK`. Substitution in
`F B-G W=Lambda H` gives

```text
D E(A V-C U)=D E Lambda K.
```

Cancellation proves `(6.3)`, including `deg K<=r-q`; `K` is nonzero because
the candidate differs from the anchor. Exactness of `D=gcd(F,G)` gives
`gcd(A,C)=1`. Original primitivity gives the other two gcd identities.
Substitution in the anchor and candidate petal congruences proves
`(6.5)`. Core, background, and petals are disjoint, so `D,E` are units
modulo every `L_i`, proving `(6.6)`. QED.

### Theorem 6.2

Fix one exact owner chamber `Q`, and within it fix one reference member
`(C_0,V_0,K_0)`. Every other member has a unique polynomial `T` satisfying

```text
K_0 C-K C_0=A T,       K_0 V-K V_0=U T,
deg K<=c,               deg T<=c.                    (6.7)
```

Thus the chamber injects into bounded-degree coefficient pairs `(K,T)` in
one two-generator rational pencil. At top ownership `q=r`, all coefficients
in `(6.7)` are scalars and monicity gives

```text
(C,V)=lambda(C_0,V_0)+(1-lambda)(A,U),                (6.8)
```

where `lambda=K/K_0` is nonzero and differs from `1` for a member other than
the reference. The top chamber is therefore an ordinary affine pencil of
primitive core-split locators, coupled through `(6.3)` to a nonzero scalar
determinantal representation of the touched-petal locator.

#### Proof

For fixed `Q`, the factors `D,E` and hence the anchor row `(A,U)` are fixed.
Multiply `(6.3)` by `K_0`, subtract `K` times the reference equation, and
obtain

```text
A(K_0 V-K V_0)=U(K_0 C-K C_0).                       (6.9)
```

Since `gcd(A,U)=1`, a unique `T` gives `(6.7)`. If
`a=deg A=deg C=deg C_0`, then the numerator in the first equation has degree
at most `a+c`, proving `deg T<=c`. When `c=0`, comparison of leading
coefficients gives `T/K_0=1-K/K_0`, which is `(6.8)`. QED.

### Relation to the active split-pencil problem

The algebra in `(6.3)` and `(6.7)` is the same primitive two-generator
algebra isolated by `prop:capfr1-detrep` and targeted by
`prob:capfr1-split-pencil`. The domains are not the same: here the natural
determinant parent is the touched-petal locator `Lambda`, while the varying
locators `C` split on the disjoint core. In the active upstream problem the
varying locator divides the same evaluation-domain locator represented by
the determinant. Consequently Theorems 6.1--6.2 are a dual-domain analogue,
not a proof or direct specialization of the base-field-normalized interior
census.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit
`8d0d19b8860143ad1a33aeee467a18f07e37baf4`, node
`l1_fpc5_tpetal_joint_owner_split_pencil`.

## 7. Nonclaim

The theorem types the joint owner and all remaining background equations and
pays each fixed owner. The new reduction neither counts the dual-domain
pencils nor supplies a converse from arbitrary coefficient pairs to guarded
FPC5 candidates. It does not aggregate the realized owners, supply
first-match chronology, pay the complete source cell, deploy a row, or move
an endpoint. Summing `(5.2)` over all divisors of `P_0` can still be
exponential.
