# M1 Hankel Variable-Line Packet Lemma

**Status:** PROVED / PROOF-PROGRAM.

**Agent/model:** Codex.

**Date:** 2026-06-27.

This note extracts one local lemma from the M1 all-line Hankel route.  It does
not prove the all-line M1 theorem.  Its purpose is to make the non-fixed
variable-line branch small enough to state as a clean residual target after the
Hankel-pencil normal form.

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

## Lemma

For every non-fixed variable line packet as above,

```text
r_L <= 1_{d_L=m_L=r_L=1} + (d_L-m_L) + 2 binom(m_L,2).      (VL)
```

Moreover the `binom(m_L,2)` unordered pairs inside `A_L` inject into the global
different-slope two-exchange edge ledger.

Consequently, after summing over all non-fixed variable-line packets,

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

Thus the non-fixed variable-line branch is reduced to true active domain
singletons, quotient defects, and different-slope packet-edge energy.  The
remaining M1 singleton work is the separate task of charging `S_dom` to
escape/target-image structure.

## Proof

First, the slope map is injective on every variable proper line.  Restrict the
Hankel vectors to the affine line `L`.  For a fixed slope `z`, the vector

```text
H(u)ell_T + z H(v)ell_T
```

is affine-linear along `L`.  If two distinct noncontained points of `L` had the
same slope `z`, this affine-linear vector would vanish at two points and hence
on the whole line.  Then every noncontained point of `L` would have slope `z`,
contradicting that `L` is a variable-slope line.  Therefore distinct
noncontained packet members have distinct slopes.

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
variable-line packet can charge the same edge key.

It remains only to prove the numerical inequality.  If `m_L=0`, then `r_L=0`.
If `m_L=1`, then `r_L<=1`; the right side of (VL) is `1` in the true active
domain-singleton case `d_L=m_L=r_L=1`, and at least `d_L-m_L>=1` otherwise
whenever `r_L=1`.  If `m_L>=2`, then `d_L-m_L>=0` and

```text
r_L <= m_L <= 2 binom(m_L,2).
```

This proves (VL).  Summing (VL) over `L` and using the injected packet-edge
image gives the displayed global bound.

## Use In M1

The lemma identifies what the all-line M1 proof still has to do in this branch.
Packet mass of size at least two is not a new obstruction: it is paid by the
different-slope two-exchange edge ledger.  Quotient defects are exactly the
locators removed by the quotient-periodic ledger.  The only genuinely new
variable-line object is the active domain-singleton family `S_dom`.

The next proof step should therefore avoid broad variable-line enumeration and
instead attack `S_dom` directly, for example by proving an escape/target-image
bound for the product-Mobius and fixed-sum singleton cases.
