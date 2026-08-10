---
workboard_item: T
row: symbolic smooth RS full-petal source cell at arbitrary t; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: one exact labelled support of total degree h with d<h<=2d+1
B_star: not_applicable
direct_statement: one determinant-coordinate gcd simultaneously recovers common defect roots and common background-agreement roots; all other background roots are affine coordinate equations; every fixed joint owner has an exact packing payment
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed labelled arbitrary-t monic pair slice with one exact anchor
quantifier: every field and every source partition satisfying the companion primitive remainder theorem
projection_and_unit: determinant coordinates with their split locators, reconstructed numerators, and source-background roots
claimed_bound: exact joint-owner identity, exact owner-containment dimension, and binomial-ratio fixed-owner packing; no owner-aggregate, deployed-row, or endpoint bound
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a common anchor defect or background root missed by the gcd, an extraneous gcd root, a non-anchor background root not represented by the printed affine equation, or a fixed-owner family exceeding the binomial ratio
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

## 6. Nonclaim

The theorem types the joint owner and all remaining background equations and
pays each fixed owner. It does not aggregate the realized owners, supply
first-match chronology, pay the complete source cell, deploy a row, or move
an endpoint. Summing `(5.2)` over all divisors of `P_0` can still be
exponential.
