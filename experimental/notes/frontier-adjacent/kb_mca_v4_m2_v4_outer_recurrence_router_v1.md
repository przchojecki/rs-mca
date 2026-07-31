---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: For the three residual inner-degree-2 transverse types, delta is exactly the V4 setwise stabilizer order of the actual component; every outer degree-30 map decomposes and all destinations are empty or recurrent to degree 2. Coordinate-stabilized rows obey an equivariant source-star normal form with no weight-three defect.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_V4_OUTER_RECURRENCE_ROUTER
quantifier: every actual inner-degree-2 transverse terminal in the imported three-type frontier
projection_and_unit: exact geometric stabilizer, recurrence, and source-star router; not deletion or a carrier/data/slope payment
claimed_bound: no primitive outer case remains; the live m2 frontier is split into exact V4 stabilizer regimes and the full-V4 row loses its weight-three source defect
status: PROVED_M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY
impact: NARROWS_THE_COMPLETE_M2_TRANSVERSE_FRONTIER_WITHOUT_DELETING_A_TYPE
falsifier: a mismatch between delta and V4 stabilizer order, a primitive degree-30 subdegree 2,4,8, a missing factor destination, or a coordinate-stabilized source row violating the paired-locator or defect-parity conclusions
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_v4_outer_recurrence_router_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-2 V4 outer-recurrence router

## 0. Verdict

The three residual rows are exactly

```text
(r,delta)=(2,4): full V4 stabilizer;
(r,delta)=(4,2): one of three order-two stabilizers;
(r,delta)=(8,1): trivial stabilizer.
```

There is no primitive outer degree-30 case. Every outer decomposition is
empty or returns to inner degree two. This is a classified recurrence, not
an `m=2` deletion or payment.

## 1. Deck stabilizers

Let `tau` be the unique deck involution of the separable quadratic inner
map `h`. Then `h x h` is the generically free Galois quotient by

```text
V4=<tau x 1,1 x tau>.
```

For the actual irreducible component `Gamma`, put
`C=(h x h)(Gamma)` and `S=Stab_V4(Gamma)`. The components over the generic
point of `C` form one V4 orbit, and the normalization of `C` is
`Gamma/S`. Therefore

```text
delta=deg(Gamma->C)=|S|.
```

Combining this with `delta*r=8` gives the three printed regimes, including
all three orientations of the order-two row.

## 2. Outer recurrence

An indecomposable outer degree-30 map would have primitive monodromy with
subdegree `r`. The complete pinned `PRIMGRP[30]` entry is

```text
group          order          subdegrees
PSL(2,29)      12180             1,29
PGL(2,29)      24360             1,29
A30             30!/2            1,29
S30             30!              1,29.
```

Thus the outer map has a proper right factor. The complete destination
ledger is

```text
outer factor d       2    3    5    6    10   15
endpoint inner 2d    4    6    10   12   20   30.
```

The imported m3 frontier certificate binds the `m=4,6,12,30` closures and
routers. The exact m10 Scott router handles `m=10`, and the primitive-route
profile excludes `m=20`. Every surviving destination therefore returns to
`m=2`. Re-entering the same degree-two decomposition is not a contradiction.

Catalogue completeness is pinned to PrimGrp commit
`5612e113d50ac23a7d10945383936e20440b4e14`. The exact 344-byte entry has
SHA-256
`1a923cc8f4428ec22864109cdc60d0c87326e8939cc1d72d217d22df2a4b8da0`.
The replay reconstructs the PSL and PGL projective-line actions over
`F_29` without GAP.

## 3. Coordinate-stabilized source normal form

Let `H_0` be the actual bidegree-`(2,4)` source component, let `b` be the
deck involution of the quadratic source map `psi(X)=W`, and use the proved
birational map `H_0->Gamma`. The other base-change component is `bH_0`.

Assume `tau x 1` stabilizes `Gamma`; this holds throughout `(r,delta)=(2,4)`
and in one orientation of `(4,2)`. The lift with `X` fixed cannot preserve
`H_0`: invariance under `tau` would place its binary-quadratic coefficient
image in a projective eigenspace line (or a point), already excluded before
the residual birational-quartic branch. It therefore exchanges `H_0` and
`bH_0`, and the preserving lift is

```text
(T,X)->(tau(T),b(X)).
```

The six unramified quadratic source fibers pair the labels by
`i->bar(i)`. With `q_i=H(alpha_i,X)`, complete-source saturation gives

```text
div(q_i) <= div(B/(z_i z_bar(i))),
star(bx)=tau(star(x)).
```

The fixed star vertices are exactly the six matching pairs. Their weights
are even, while nonfixed vertices occur in equal involution pairs. The
imported defect budget is at most three, so a fixed occupied vertex has
weight two and a nonfixed weight-three vertex would cost at least six.
Hence the former weight-three defect type is absent. If `d` is the number
of double vertices and `e` the number of fixed matching vertices, then

```text
0<=e<=d<=3,       e=d mod 2.
```

## 4. Scope

The three `m=2` rows remain live. The order-two row is not assigned a
preferred orientation, and the source refinement is asserted only when
`tau x 1` belongs to the stabilizer. No parameter-to-carrier transport,
received-data or explaining-polynomial descent, slope owner, payment,
`u=2`, K3, endpoint, or KoalaBear-row close is claimed.
