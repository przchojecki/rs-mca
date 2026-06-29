# M1 Hankel Variable-Line Packet Lemmas

**Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.

**Agent/model:** Codex.

**Date:** 2026-06-27.

This note extracts local lemmas from the M1 all-line Hankel route.  It does
not prove the all-line M1 theorem.  Its purpose is to make the non-fixed
line-packet branch small enough to state as a clean residual target after the
Hankel-pencil normal form.

The proof status is local: the displayed inequalities are proved under the
Hankel-pencil normal form and the stated non-fixed line-packet hypotheses.
The same-slope root-slice note now verifies the needed slope-injectivity
hypothesis for every surviving fixed-sum or nondegenerate product-Mobius line
packet after fixed-root and full-plane charges.  This note does not prove that
every all-line M1 residue-packing instance reaches these hypotheses, and it
does not bound the remaining active two-exchange codegree or one-outside
target image.

## Setup

Let `D subset F` be a finite evaluation domain and fix a split locator
co-support size `j`.  Work in the Hankel-pencil normal form from
`experimental/experiments.tex`: for received words `f,g`, syndromes `u,v`, and
a `j`-set `T`,

```text
(H(u)+zH(v)) ell_T = 0,        H(v)ell_T != 0
```

is the finite-slope noncontained line-incidence test.

Fix a `(j-2)`-set `R`.  Any two-exchange locator through `R` has the form

```text
T = R union {x,y},
```

and is represented by elementary coordinates

```text
s=x+y,        p=xy.
```

The Hankel vectors on this two-root plane are affine-linear functions of
`(s,p)`.  Consider a proper one-dimensional determinantal component `L` in
this plane, and assume that `L` is not a fixed-root line.  Then `L` is one of
the two involution models

```text
product-Mobius:    (x-c)(y-c)=mu,  mu != 0,
fixed-sum:         x+y=s0.
```

Let `P_L(R)` be the unordered domain-pair packet on `L`:

```text
P_L(R) = { R union {x,iota_L(x)} :
           x,iota_L(x) in D\R, x != iota_L(x) }.
```

Let `d_L=|P_L(R)|`, let `A_L subset P_L(R)` be the aperiodic subpacket after
quotient-periodic locators have been charged, and put `m_L=|A_L|`.  Finally let
`R_L subset A_L` be the active-new subpacket after the already-charged
root-slice, full-plane, and fixed-root line slopes have been removed, and put
`r_L=|R_L|`.

The full-plane charge used here is supplied by
`m1_same_slope_root_slice_lemma.md`: three non-collinear same-slope points in
the elementary two-root plane force the lifted
`H_{t+2,j-2}(u+zv)ell_R=0` Hankel core.  Fixed-root lines are the one-exchange
root slices through `R union {x}`.  The same note classifies every remaining
affine two-root line as fixed-sum or nondegenerate product-Mobius after the
fixed-root case is charged.

## Hankel Discharge of the Variable-Slope Hypothesis

In the original packet lemma, one assumes that the proper line `L` is
variable-slope.  In the `t=2` Hankel residual branch this is no longer an
extra hypothesis.  The non-fixed line-packet collapse in
`m1_same_slope_root_slice_lemma.md` says:

```text
if H_{2,j}(u+zv)ell_{R,s,p}=0 on an entire fixed-sum line
or on an entire nondegenerate product-Mobius line, then
H_{4,j-2}(u+zv)ell_R=0.
```

Thus any non-fixed line packet which is constant at one finite slope has
already been charged to the full-plane Hankel lift.  After fixed-root and
full-plane charges, every surviving fixed-sum or nondegenerate product-Mobius
packet is therefore variable-slope.  Since the restriction of
`H(u)ell_T+zH(v)ell_T` to a line is affine-linear, two distinct active packet
members with the same finite slope would force the whole line to have that
slope.  The collapse rules this out, so the finite-slope map is injective on
every surviving non-fixed line packet.

## Lemma

For every surviving non-fixed line packet as above,

```text
r_L <= 1_{d_L=m_L=r_L=1} + (d_L-m_L) + 2 binom(m_L,2).      (VL)
```

Moreover the `binom(m_L,2)` unordered pairs inside `A_L` inject into the global
different-slope two-exchange edge ledger.

Consequently, after summing over all surviving non-fixed line packets,

```text
sum_L r_L
  <= S_dom + Q_def + 2 E_pkt,
```

where

```text
S_dom = #{ L : d_L=m_L=r_L=1 },
Q_def = sum_L(d_L-m_L),
E_pkt = image size of injected different-slope packet edges.
```

Thus the non-fixed line-packet branch is reduced to true active domain
singletons, quotient defects, and different-slope packet-edge energy.  The
remaining M1 singleton work is the separate task of charging `S_dom` to
escape/target-image structure.

## Proof

First, the slope map is injective on every surviving non-fixed line packet by
the Hankel discharge above.  Equivalently, the original variable-slope
hypothesis of the packet lemma has been replaced here by the full-plane
charge: a repeated finite slope on two distinct active packet members would
make the whole affine line constant-slope and hence already lifted to
`H_{4,j-2}(u+zv)ell_R=0`.

Second, the non-fixed line models are involutions on roots.  In the
product-Mobius case the partner is

```text
iota_L(x)=c+mu/(x-c),
```

away from the pole `x=c`; in the fixed-sum case it is

```text
iota_L(x)=s0-x.
```

Two distinct unordered domain pairs in the same involution packet are disjoint:
if they shared one root, applying the involution would give the same partner
and hence the same unordered pair.  Therefore two distinct packet locators
`T_1,T_2` have intersection exactly `R`; they differ by two deleted and two
inserted roots, so `{T_1,T_2}` is a strict two-exchange edge.  By slope
injectivity this edge is different-slope.

The edge charge is globally injective.  A charged edge key is the unordered
pair `{T_1,T_2}`.  Its intersection recovers the core `R`, and the two
elementary points `(x_1+y_1,x_1y_1)` and `(x_2+y_2,x_2y_2)` determine the
unique affine line `L` in the two-root plane.  Hence no other non-fixed
line packet can charge the same edge key.

It remains only to prove the numerical inequality.  If `m_L=0`, then `r_L=0`.
If `m_L=1`, then `r_L<=1`; the right side of (VL) is `1` in the true active
domain-singleton case `d_L=m_L=r_L=1`, and at least `d_L-m_L>=1` otherwise
whenever `r_L=1`.  If `m_L>=2`, then `d_L-m_L>=0` and

```text
r_L <= m_L <= 2 binom(m_L,2).
```

This proves (VL).  Summing (VL) over all surviving non-fixed line packets `L`
and using the injected packet-edge image gives the displayed global bound.

## Active Domain-Singleton Escape/Target Lemma

The remaining term in the packet lemma is

```text
S_dom = #{ L : d_L=m_L=r_L=1 }.
```

This section gives a purely combinatorial reduction for that term.  Restrict
to an active domain-singleton packet `L`, and let

```text
T_a = R union {x_a,iota_L(x_a)}
```

be its unique active noncontained domain locator.  Put `n=|D|`,
`A=D\R`, and `|R|=j-2`.  For the line model define

```text
tau_L = 3  for product-Mobius lines,
tau_L = 1  for fixed-sum lines.
```

Let `C_L` be the number of contained domain pairs on `L`, namely unordered
pairs `{x,iota_L(x)}` with both roots in `A`, distinct, and

```text
H(v) ell_{R union {x,iota_L(x)}} = 0.
```

Let `O_L` be the number of off-domain roots `x in A` with
`iota_L(x) notin D`.  Define the free escape mass

```text
free_L = 2 C_L + O_L.
```

Then every active domain-singleton packet satisfies

```text
free_L >= lambda_L := max(0, n-j-|R|-tau_L).          (SE)
```

Equivalently, in the two-exchange normalization `|R|=j-2`,

```text
lambda_L =
  max(0,n-2j-1)   for product-Mobius singleton lines,
  max(0,n-2j+1)   for fixed-sum singleton lines.
```

Now let `Target_cb` be the set of contained/tangent targets

```text
T_c = R union {x,iota_L(x)}
```

arising from contained domain pairs on active domain-singleton packets.  Let
`Target_off` be the set of one-outside boundary targets

```text
B = R union {x,iota_L(x)},      x in D\R, iota_L(x) notin D,
```

arising from off-domain roots on active domain-singleton packets.  Then

```text
sum_{L in S_dom} lambda_L
  <= 2 binom(j,2) binom(n-j,2) |Target_cb|
     + (j-1) binom(n-j+1,2) |Target_off|.            (ST)
```

Consequently

```text
S_dom
  <= Z_0
     + 2 binom(j,2) binom(n-j,2) |Target_cb|
     + (j-1) binom(n-j+1,2) |Target_off|,            (SS)
```

where `Z_0` is the number of active domain-singleton packets with
`lambda_L=0`.  If `S_prod` and `S_sum` denote the active singleton counts in
the product-Mobius and fixed-sum models, then

```text
Z_0 <= 1_{n<=2j+1} S_prod + 1_{n<=2j-1} S_sum.       (SZ)
```

In particular `Z_0=0` throughout the range `n>2j+1`.

### Proof

The involution on `L` partitions the available roots `A=D\R`.  Since
`L` is a domain singleton, exactly two roots of `A` form the unique active
noncontained domain pair.  Every other root lies in one of four escape
buckets:

```text
contained domain pairs,
core-hit roots with iota_L(x) in R,
off-domain roots with iota_L(x) notin D,
fixed or pole roots.
```

Thus the total escape-root mass is `|A|-2=n-j`.  The core-hit bucket has size
at most `|R|`, because the involution is injective away from its pole.  The
fixed/pole bucket has size at most `tau_L`: a product-Mobius map has one pole
and at most two fixed roots, while a fixed-sum map has no pole and at most one
fixed root.  Removing these two algebraic buckets leaves the free escape mass,
which proves (SE).

Contained domain escape is pair-valued, so it contributes `2 C_L` roots.  Each
contained pair gives a strict boundary edge from the active locator `T_a` to
the contained target `T_c`.  For a fixed contained target `T_c`, every active
all-domain neighbor is obtained by deleting two roots of `T_c` and inserting
two roots from `D\T_c`.  Hence the number of such edges over a fixed `T_c` is
at most

```text
binom(j,2) binom(n-j,2).
```

Therefore the total contained-pair contribution is at most

```text
2 binom(j,2) binom(n-j,2) |Target_cb|.
```

Similarly, each off-domain root gives a one-outside boundary target `B` and a
strict boundary edge from `T_a` to `B`.  For fixed `B`, an all-domain active
neighbor must delete the outside point and one of the `j-1` domain roots of
`B`, then insert two roots from the `n-j+1` domain roots outside `B cap D`.
Thus the number of off-domain edges over fixed `B` is at most

```text
(j-1) binom(n-j+1,2).
```

This proves (ST).  Finally, each active singleton with `lambda_L>0` contributes
one unit to the left side of (ST), while the `lambda_L=0` singletons are
exactly the exceptional term `Z_0`.  This proves (SS).  The displayed
formula (SZ) follows by substituting the two explicit values of `lambda_L`.

## Residual Ledger Corollary

The previous two lemmas can be stated in the same language as the existing
M1 support-overlap and quotient ledgers.  Let `A_var` be the active aperiodic
locator family contributed by surviving non-fixed line packets after the
root-slice, full-plane, and fixed-root line charges have been removed.  Define
the different-slope two-exchange codegree subledger

```text
E_2^neq(A_var)
  = #{ {T,T'} subset A_var :
       |T cap T'|=j-2 and z_T != z_T' }.
```

Let `Boundary_off` be the one-outside target image from the singleton lemma,
and let `Tangent_cb` be its contained/tangent target image.  Then

```text
sum_L r_L
  <= Q_def + 2 E_2^neq(A_var) + Z_0
     + 2 binom(j,2) binom(n-j,2) |Tangent_cb|
     + (j-1) binom(n-j+1,2) |Boundary_off|.         (RL)
```

In particular, if the quotient-defect and contained/tangent ledgers have
already been budgeted, the uncharged non-fixed line-packet branch is reduced
to three named objects:

```text
different-slope active two-exchange codegree,
one-outside boundary target image,
short-range zero-lower singletons.
```

The zero-lower term is absent in the range `n>2j+1`.

### Proof

The packet lemma injects every packet pair into the global different-slope
two-exchange edge image.  Since both endpoints are active aperiodic locators
in the family `A_var`, this image is a subset of `E_2^neq(A_var)`.  Hence
`E_pkt <= E_2^neq(A_var)`.  Substitute this inequality and the singleton
bound (SS) into the summed packet bound

```text
sum_L r_L <= S_dom + Q_def + 2 E_pkt.
```

The final sentence is exactly (SZ).

## High-Agreement Zero-Lower Elimination

Write the agreement as `a=n-j`.  The zero-lower term in (RL) is not a live
obstruction in the high-agreement half of the parameter space.  More precisely,

```text
Z_0 = 0        whenever        a > (n+1)/2.          (HA0)
```

Equivalently, product-Mobius zero-lower singletons can occur only when
`a <= (n+1)/2`, and fixed-sum zero-lower singletons can occur only when
`a <= (n-1)/2`.

Since `a=k+t`, this includes every positive-slack row with `k>=n/2` and
`t>=1`.  In particular, the rate-half positive-slack M1 window has no
zero-lower singleton residual.

Consequently, in the range `a>(n+1)/2`,

```text
sum_L r_L
  <= Q_def + 2 E_2^neq(A_var)
     + 2 binom(j,2) binom(n-j,2) |Tangent_cb|
     + (j-1) binom(n-j+1,2) |Boundary_off|.         (RL-HA)
```

If the quotient-defect and contained/tangent ledgers have already been paid,
the non-fixed line-packet branch in this range has only two residual objects:

```text
active different-slope two-exchange codegree,
one-outside boundary target image.
```

### Proof

The singleton lemma gives

```text
Z_0 <= 1_{n<=2j+1} S_prod + 1_{n<=2j-1} S_sum.
```

Substituting `j=n-a`, the product-Mobius indicator is nonzero only if

```text
n <= 2(n-a)+1,        equivalently        a <= (n+1)/2,
```

and the fixed-sum indicator is nonzero only if

```text
n <= 2(n-a)-1,        equivalently        a <= (n-1)/2.
```

Both indicators therefore vanish when `a>(n+1)/2`.  Substituting `Z_0=0` into
(RL) gives (RL-HA).  Finally, if `k>=n/2` and `t>=1`, then

```text
a=k+t >= n/2+1 > (n+1)/2,
```

so the positive-slack rate-half assertion follows.

## Rate-Half Line-Packet Closure Criterion

The previous corollary turns the rate-half positive-slack non-fixed
line-packet problem into two explicit residual estimates.  Suppose `k>=n/2`,
`t>=1`, and the
quotient-defect and contained/tangent target ledgers satisfy

```text
Q_def <= n^B_Q,        |Tangent_cb| <= n^B_T.
```

Suppose also that the two live residual objects satisfy

```text
E_2^neq(A_var) <= n^B_E,        |Boundary_off| <= n^B_O.
```

Then the non-fixed line-packet active-new contribution obeys

```text
sum_L r_L
  <= n^B_Q + 2 n^B_E + n^(B_T+4) + n^(B_O+3).       (PC)
```

In particular, once quotient defects and contained/tangent targets have already
been paid by their own ledgers, polynomial bounds for the active
different-slope two-exchange codegree and the one-outside boundary target
image imply a polynomial bound for the whole non-fixed line-packet branch.
No zero-lower singleton term remains in this rate-half positive-slack range.

### Proof

In the rate-half positive-slack range the high-agreement corollary gives
`Z_0=0`, so (RL-HA) applies.  Since `0<=j<=n`,

```text
2 binom(j,2) binom(n-j,2) <= n^4,
(j-1) binom(n-j+1,2) <= n^3.
```

Substituting these two crude polynomial bounds and the four displayed
hypotheses into (RL-HA) proves (PC).

## Use In M1

The lemma identifies what the all-line M1 proof still has to do in this branch.
Packet mass of size at least two is not a new obstruction: it is paid by the
different-slope two-exchange edge ledger.  Quotient defects are exactly the
locators removed by the quotient-periodic ledger.  The only genuinely new
line-packet object after the first lemma is the active domain-singleton
family `S_dom`.

The singleton escape/target lemma reduces that family further, and the
residual-ledger corollary puts the result into the same support-overlap
language as the existing M1 average-collinearity ledger:

```text
sum_L r_L
  <= Q_def + 2 E_2^neq(A_var) + Z_0
     + 2 binom(j,2) binom(n-j,2) |Tangent_cb|
     + (j-1) binom(n-j+1,2) |Boundary_off|.
```

Thus the non-fixed line-packet branch has been reduced to quotient defects,
active different-slope two-exchange codegree, charged contained/tangent
targets, one-outside boundary targets, and the short-range zero-lower class.
The high-agreement corollary removes the zero-lower class whenever
`a>(n+1)/2`, hence throughout the positive-slack rate-half window
`k>=n/2`, `t>=1`.  In that range, after quotient and contained/tangent charges,
the next M1 step is exactly to bound the active codegree and one-outside target
image inside the quotient-aware residue-line ledger.  The closure criterion
makes the exponent bookkeeping explicit: any polynomial estimates for those
two live residual objects close the non-fixed line-packet branch up to a
fixed `n^3`/`n^4` bookkeeping loss.
