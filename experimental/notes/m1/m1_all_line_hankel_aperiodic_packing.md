# M1 All-Line Hankel Aperiodic Packing Target

## Status

PROVED finite normal form / AUDIT verifier / NOT the final M1 theorem.

This note records the first M1 packet following the maintainer target:

```text
#{z : exists an aperiodic split locator T} <= n^B
```

after tangent/contained and quotient-periodic locator classes are charged.
It uses the Hankel-pencil normal form from `experimental/experiments.tex`.

## Set-Up

Let `F` be a finite field, let `D subset F` have size `n`, and let
`C=RS[F,D,k]`.  Put

```text
r=n-k,        j+t=r,        a=k+t=n-j.
```

For a line `(f,g):D->F^2`, write

```text
u=Syn(f),        v=Syn(g),
```

using the usual RS parity-check syndrome.  For each `j`-point complement
`T subset D`, let

```text
L_T(X)=prod_{x in T}(X-x),
ell_T=(ell_0,...,ell_j)^T
```

be its monic locator vector.  The Hankel-pencil test says that a finite slope
`z` is explained on `S=D\T` if and only if

```text
(H_{t,j}(u)+zH_{t,j}(v)) ell_T = 0.        (1)
```

It is support-wise noncontained on that support if and only if

```text
H_{t,j}(v) ell_T != 0.                      (2)
```

## Charged/Aperiodic Split-Locator Ledger

For fixed `(f,g,t,j)`, define `Bad(T)` to mean that `T` is a split complement
whose locator satisfies (1) for some slope and satisfies (2).  When this holds,
the slope is unique unless the whole vector `H(v)ell_T` vanishes, which is
exactly the contained/tangent-core class removed by (2).

When `D=H` is a cyclic multiplicative subgroup, a split complement `T` is
called whole-fiber quotient-periodic at scale `m|n`, `1<m<n`, if it is a union
of cosets of the subgroup of `H` of size `m`.  Let `QP(T)` mean that this
holds for at least one charged scale.

The finite all-line slope ledger is therefore the disjoint accounting

```text
Bad slopes
  = charged quotient-periodic slope image
    union aperiodic slope image,

AperSlope(f,g;t,j)
  = { z_T : Bad(T) and not QP(T) }.
```

The maintainer target is to prove a polynomial bound for this last image,
uniformly in the line `(f,g)`, after the tangent/contained and
quotient-periodic ledgers have been paid.

## Exactness Lemma

The ledger above is exact for every finite instance.

1. The Hankel-pencil theorem gives equivalence between support-wise line
   incidence and the existence of a split locator satisfying (1).
2. Condition (2) is exactly the noncontainment condition on the same support,
   so contained/tangent-core locators are removed before aperiodicity is
   counted.
3. The quotient-periodic predicate depends only on the support complement and
   the selected quotient scales, so charging it before taking slope images
   cannot create or remove aperiodic locators.
4. Every remaining bad locator contributes the unique slope forced by
   `H(u)ell_T + zH(v)ell_T=0`, and the set of these slopes is precisely
   `AperSlope(f,g;t,j)`.

Thus the residual M1 problem is no longer a question about support-wise MCA
definitions.  It is the slope image of the aperiodic split-locator incidence
inside the Hankel pencil.

## The `t=2` Determinant And Strict-Exchange Profile

In the first nontrivial slack window `t=2`, put

```text
a_T = H_{2,j}(u) ell_T,        b_T = H_{2,j}(v) ell_T  in F^2.
```

Then a split complement contributes a noncontained bad slope if and only if

```text
b_T != 0,        det[a_T b_T] = 0.
```

When this holds, the slope is the unique scalar

```text
z_T = -a_{T,i}/b_{T,i}
```

for any coordinate `i` with `b_{T,i} != 0`.  Thus the residual aperiodic M1
object in this window is the image of a rational slope map on the aperiodic
part of the split-locator determinant locus.

The support-overlap form of the same object is also explicit.  Since
`S=D\T` has size `n-j=k+t`, two supports have strict high overlap
`|S cap S'|>k` exactly when the complements satisfy

```text
|T \ T'| = |T' \ T| < t.
```

For `t=2`, this is the one-exchange graph on complement locators.  After
quotient-periodic locators are charged, the verifier reports the one-exchange
profile of the remaining aperiodic determinant locus: total strict edges,
maximum strict degree, maximum slope-fiber size, and same-slope strict edges.
These are not the final M1 theorem, but they are the finite statistics that a
packing or inverse theorem must eventually control uniformly.

## Same-Slope One-Exchange Root Slice

The same-slope part of the strict one-exchange profile has an exact structural
explanation.  Fix `t=2` and a slope `z`, and write

```text
A_z = H_{2,j}(u)+zH_{2,j}(v).
```

Let `R subset D` have size `j-1`, and write

```text
L_R(X)=c_0+c_1X+...+c_{j-1}X^{j-1}.
```

For `x notin R`,

```text
L_{R union {x}}(X) = X L_R(X) - x L_R(X).
```

Thus its locator vector is affine in `x`:

```text
ell_{R union {x}} = s_R - x p_R,
```

where `s_R` is the coefficient vector of `X L_R` and `p_R` is the coefficient
vector of `L_R`, padded to length `j+1`.  If two distinct exchanged roots
`x,y` give the same slope `z`, then

```text
A_z(s_R-xp_R)=0,        A_z(s_R-yp_R)=0.
```

Subtracting gives `A_z p_R=0`, and then also `A_z s_R=0`.  Therefore

```text
A_z ell_{R union {w}}=0        for every w in D\R.
```

So every same-slope strict one-exchange edge lies in a full fixed-slope
root-slice incidence packet.  The only remaining support-wise filter on that
slice is noncontainment, namely whether

```text
H_{2,j}(v) ell_{R union {w}} != 0.
```

This separates two jobs in the M1 proof search: same-slope strict collisions
belong to root-slice/tangent-style ledgers, while the genuinely aperiodic
packing problem is the slope image of determinant-locus packets after these
root slices and the quotient-periodic classes are charged.

## Different-Slope One-Exchange Quadratic Slice

The different-slope part of the one-exchange profile has a complementary
finite-degree constraint.  Keep `t=2` and a fixed `(j-1)`-root core `R`.  With

```text
ell_x = ell_{R union {x}} = s_R-xp_R,
```

the two Hankel vectors

```text
a(x)=H_{2,j}(u)ell_x,        b(x)=H_{2,j}(v)ell_x
```

are affine functions of `x`.  Hence the determinant

```text
Delta_R(x)=det[a(x) b(x)]
```

is a polynomial in `x` of degree at most two.  Therefore a one-root slice has
only two determinant roots unless `Delta_R` is identically zero.  In
particular, a different-slope strict one-exchange edge is either:

1. the whole determinant root set of a nonzero quadratic slice; or
2. part of an exceptional zero-determinant root slice, where every exchanged
   root passes the determinant gate and the slope map along the slice must be
   controlled separately.

The verifier checks this dichotomy on every `(j-1)`-core slice in the finite
audit rows by evaluating `Delta_R` on the ambient prime field.  Thus the
residual `t=2` M1 packing target is further localized: after quotient-periodic
classes and same-slope root slices are charged, different-slope strict edges
can only accumulate through zero-determinant root slices or through many
isolated nonzero quadratic slices.

## Zero-Determinant Slice Slope Dichotomy

The exceptional zero-determinant branch also has an exact local dichotomy.
Assume `Delta_R` vanishes identically on the one-root slice for a fixed core
`R`.  Write

```text
a(x)=a_s-xa_p,        b(x)=b_s-xb_p,
```

where `a_s=H(u)s_R`, `a_p=H(u)p_R`, and similarly for `b`.  If the direction
pencil `span{b_s,b_p}` has rank two in `F^2`, then the identities

```text
det[a_s b_s]=0,
det[a_p b_s]+det[a_s b_p]=0,
det[a_p b_p]=0
```

force `a_s=-z b_s` and `a_p=-z b_p` for a single scalar `z`.  Thus every
noncontained point of the slice has the same slope.

If instead `span{b_s,b_p}` has rank zero, the whole slice is contained and
contributes no noncontained slopes.  The remaining rank-one case is also
constant-slope because the two locator vectors are not arbitrary affine
vectors: for every syndrome `y`,

```text
H_{2,j}(y)s_R=(S_0,S_1),        H_{2,j}(y)p_R=(P_0,S_0).
```

Thus, writing `b_s=(B_0,B_1)` and `b_p=(C,B_0)`, rank one gives
`CB_1=B_0^2`.  The three zero-determinant identities force `a_s` and `a_p` to
lie on the same one-dimensional direction as `b_s` and `b_p`; the displayed
Hankel overlap then forces the two scalar ratios to agree.  The edge cases
`B_0=0` say that one of `b_s,b_p` vanishes, and the same identities force the
matching `a` vector to vanish, again giving a single slope on every
noncontained point.

Equivalently, if two distinct exchanged roots `x,y` have the same slope `z`,
then the same subtraction argument as above gives

```text
(H_{2,j}(u)+zH_{2,j}(v))p_R=0,
(H_{2,j}(u)+zH_{2,j}(v))s_R=0.
```

Consequently every noncontained member of that zero-determinant slice has the
same slope `z`.  Thus zero-determinant one-root slices split into:

1. constant-slope root-slice packets, already handled by the same-slope
   root-slice ledger; or
2. contained/tangent slices, which contribute no noncontained aperiodic slope.

The verifier certifies this split by checking the three determinant
coefficients of `Delta_R`, computing the direction-pencil rank, and then
checking that every noncontained zero-determinant slice is constant-slope.

## Root-Slice Peeling Corollary

For `t=2`, the fixed-slope one-exchange graph can be peeled exactly.  For each
same-slope strict edge, include the full fixed-slope root slice supplied by the
root-slice lemma, and remove every aperiodic locator lying in one of these
packets.  The remaining aperiodic locator family has no same-slope
one-exchange edge.

Indeed, any same-slope one-exchange edge in the residual family would generate
one of the root slices used in the peeling step, so both of its endpoints would
have been removed.  Thus repeated-slope high-overlap structure is completely
charged to constant root-slice packets; the residual slope fibers are
one-exchange independent and must be controlled by a different mechanism.

## Verifier

The companion verifier

```bash
python3 experimental/scripts/verify_m1_all_line_hankel_aperiodic.py
```

enumerates small cyclic-domain cases.  For each case it:

- computes syndromes and Hankel windows for a deterministic family of all-line
  words;
- enumerates all split complements `T`;
- applies the projective slope gate for `t=2`;
- cross-checks every bad slope by direct RS interpolation on `D\T`;
- labels whole-fiber quotient-periodic complements at the selected scales;
- reports the aperiodic slope image after charged locators are removed;
- in the `t=2` rows, verifies the determinant gate and reports the strict
  one-exchange profile of the aperiodic locator family;
- checks that every same-slope strict one-exchange edge extends to the full
  fixed-slope root slice predicted by the lemma above;
- verifies that different-slope strict edges obey the quadratic root-slice
  dichotomy above;
- verifies that every zero-determinant slice is constant-slope or contained
  via the direction-pencil rank and Hankel overlap, and that constant zero
  slices account for all same-slope strict edges;
- peels root-slice members and checks that the residual aperiodic family has
  no same-slope one-exchange edges;
- runs one deterministic arbitrary-line probe which hits the rank-one
  zero-determinant branch and verifies that it is classified by the same
  constant/contained zero-slice ledger.

The default audit currently checks three cyclic-domain parameter rows, twelve
deterministic polynomial-family line samples, and one deterministic arbitrary
line probe.  The largest observed residual aperiodic slope image in this smoke
packet has size `17`, after direct interpolation checks on every reported
support-wise bad slope.

In the polynomial-family full-domain `F_17`, `j=4`, `t=2` row, the residual
aperiodic locus has maximum slope fiber `16`, strict one-exchange degree `15`,
and `190` strict one-exchange pairs.  Of these strict edges, `78` are
same-slope edges, and the verifier certifies that they are exactly the
repeated pairs inside one constant-slope rank-two zero-determinant slice with
`13` aperiodic members.  The remaining `112` different-slope strict edges lie
on `112` nonzero quadratic slices; there are no zero-determinant
different-slope edge slices in this audit row.  After peeling the root-slice
members, the residual family has `86` aperiodic locators, all `16` residual
slopes still occur, the maximum residual slope fiber drops to `9`, and the
residual same-slope one-exchange edge count is `0`.

The arbitrary `F_17`, `j=4`, `t=2` rank-one probe has `176` aperiodic locators,
all `17` slopes, and `16` zero-determinant slices.  Four of those zero slices
have rank-one direction pencil; the verifier classifies all zero slices in the
probe as constant-slope.  These are exactly the profile quantities a packing
proof must shrink or explain structurally.

This is an audit/verifier for the M1 target, not a proof of the desired
polynomial all-line bound.  Its purpose is to make future counterexample-first
work precise: a claimed obstruction should now say whether its split locators
are contained/tangent, quotient-periodic, or genuinely aperiodic in this
Hankel-pencil ledger.
