# M1 Width-One Fixed-Root Closure

**Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-29.

This note extracts a compact width-one consequence from the M1 Hankel-pencil
route.  It does not prove the all-line M1 theorem.  Its purpose is to isolate
the first low-width critical-tail obstruction and show that, in fixed surplus,
that obstruction reduces to the already exposed one-root fixed-divisor
root-slice ledger.

## Setup

Work at a base-free canonical `b=2` node in the Hankel-pencil normal form.  Let

```text
V=span(P,Q) subset F[X]_{<q},        D=D^{can},        |D|=q+s,
```

where `s` is the node surplus.  For a nonzero direction `A in V`, put

```text
Z(A)={x in D : A(x)=0}.
```

A root-free width-one certificate is a direction `A` with the maximal possible
root shadow

```text
|Z(A)|=q-1.
```

Write `Z=Z(A)` and `O=D\Z`.  Then `|O|=s+1`, and the degree gap forces

```text
A=c ell_Z,        c != 0.                         (W1-shadow)
```

Equivalently, width-one certificates are exactly co-small projective fibers in
the descended two-dimensional pencil.

## Bounded-Complement Rank Test

The maximal-shadow condition can be tested on the bounded complement.  For

```text
O subset D,        |O|=s+1,
```

put

```text
L_O=ell_{D\O}.
```

Then `O` supports a width-one certificate if and only if

```text
L_O in V.                                            (W1-rank-test)
```

Indeed, if `L_O in V`, then `L_O` has exactly the root set `D\O` on `D`,
which has size `q-1`, so it gives a width-one maximal shadow.  Conversely,
every width-one direction satisfies (W1-shadow), hence is proportional to
`L_O` for `O=D\Z(A)`.

Equivalently, after choosing any coefficient basis of `F[X]_{<q}`, the rows
`P,Q,L_O` have rank at most two.  Thus all `3 x 3` coefficient minors vanish.
In fixed surplus this is a polynomial family of tests over the active tree:

```text
sum_{S in Active(A_0)} binom(|D_S^{can}|,s_S+1)
 <= (s_0+2) Q^{s_0+1} binom(Q+s_0,s_0+1),      (W1-test-count)
```

using the active-node bound and `|D_S^{can}|<=Q+s_0`, `s_S<=s_0`.  A passing
test may still carry a large co-small flag cube, but the possible complements
are now a bounded-complement algebraic search problem rather than an
unstructured family of projective directions.

## Near-Constant Pencil

Choose `B in V` independent of `A`.  Since the node is base-free, `B(x)!=0`
for every `x in Z`; otherwise both basis directions would vanish at `x`.
Thus the projective evaluation map is constant on the large fiber:

```text
[A(x):B(x)]=[0:1]        for every x in Z.        (W1-constant)
```

For `y in O`, one has `A(y)!=0`, so `[A(y):B(y)]!=[0:1]`.  Hence all
nonconstant projective information is confined to the bounded complement `O`.
In particular the good-pair capacity at this node splits as

```text
G^{can}=(q-1)(s+1)+G_O,        0<=G_O<=binom(s+1,2).  (W1-good)
```

Pairs inside `Z` are bad, every cross pair `Z x O` is good, and the only
undetermined contribution is inside `O`.

## Lossless Descent

Let `P_m subset Z` have size `m`.  In the fixed-root slice obtained by
absorbing `P_m`, the divided direction is

```text
A^{P_m}=A/ell_{P_m}=c ell_{Z\P_m}.              (W1-desc-dir)
```

The descended canonical domain is

```text
D\P_m=(Z\P_m) disjoint union O,
```

so

```text
q^{P_m}=q-m,        |Z\P_m|=q^{P_m}-1,        r^{P_m}=1.  (W1-desc)
```

Thus every rung of a width-one flag is again a width-one maximal shadow with
the same bounded complement `O`.  The operation deletes roots from one fixed
large fiber; it does not create a fresh moving-denominator problem.

## First-Root Injection

Let

```text
a=floor((q-2)/2),        R1Flag(A)=sum_{e=1}^a binom(q-1,e).
```

If `a=0`, the flag count is empty.  Otherwise order `Z` by the ambient root
order and put

```text
Z_{>x}={y in Z : y>x}.
```

The canonical first-root partition gives the exact identity

```text
R1Flag(A)
 =
 sum_{x in Z} sum_{f=0}^{a-1} binom(|Z_{>x}|,f).      (W1-first-root)
```

Indeed, a nonempty flag `E subset Z`, `|E|<=a`, has a unique first root
`x=min(E)` and a remainder `F=E\{x} subset Z_{>x}` with `|F|<=a-1`.

Each summand is a one-root fixed-divisor slice.  After exposing `x`, the
divided direction is

```text
A^x=A/(X-x)=c ell_{Z\{x}},
q^x=q-1,        r^x=1,        s^x=s,        O^x=O.   (W1-one-root)
```

For a remainder `F subset Z_{>x}`, the descendant is

```text
A^{x,F}=A/ell_{{x} union F}
       =c ell_{Z\({x} union F)}.                     (W1-slice-dir)
```

This is exactly the same descendant as the original flag `E={x} union F`,
with the first root exposed as a fixed divisor.  Therefore the whole width-one
cube embeds into the disjoint union of one-root absorbed fixed-divisor
root-slice families, preserving surplus and the bounded complement.

## Large Cubes Have Large One-Root Witnesses

The first-root partition also gives a counterexample-first form: a large
width-one cube cannot be hidden by spreading thinly across many roots.  Put

```text
M_x=# { F subset Z_{>x} : |F|<=a-1 }.
```

Then (W1-first-root) gives

```text
max_{x in Z} M_x >= R1Flag(A)/(q-1).            (W1-root-witness)
```

When `a>=1`, equivalently `q>=4`, `R1Flag(A)>=binom(q-1,a)`.  The
central-binomial lower bound gives

```text
max_{x in Z} M_x >= 2^{q-1}/(2q^2).             (W1-root-witness-exp)
```

Indeed, with `n=q-1`, the level `a=floor((q-2)/2)=floor((n-1)/2)` is central
or one step below central, so `binom(n,a)>=2^n/(2(n+1))`; dividing by
`q-1<=q` gives the displayed bound.

Thus any fixed-surplus counterexample with `q` larger than a constant multiple
of `log Q` already produces a super-polynomial one-root absorbed slice.  The
remaining obstruction is therefore visible at a single fixed root; it is not a
depth-multiplicative or many-root averaging phenomenon.

## Polynomial One-Root Slices Force Logarithmic Width

The preceding witness bound gives an explicit logarithmic-width criterion.
Suppose that, after the quotient-periodic, tangent, fixed-root, and aperiodic
charges under consideration, every first-root slice of the width-one cube is
bounded by

```text
M_x <= C Q^K
```

for constants `C,K` independent of the initial quotient width `Q`.  Then every
uncharged width-one certificate with `q>=4` satisfies

```text
2^{q-1}/(2q^2) <= C Q^K,
```

hence

```text
q <= K log_2 Q + 2 log_2 q + log_2(2C)+1.       (W1-log-width)
```

For fixed `C,K`, this forces `q=O_{C,K}(log Q)`.  Equivalently, any
fixed-surplus width-one family with `q/log Q -> infinity` must create
super-polynomial one-root fixed-divisor slices after the standard charges.  So
large-width counterexamples to the width-one closure criterion are exactly
large one-root slice counterexamples; the width-one cube has no additional
reservoir of growth once those slices are polynomially controlled.

## Fixed-Surplus Closure Criterion

Now sum over active canonical nodes with initial surplus `s_0<=sigma`.  Let
`WO_1(A_0)` denote the total root-free width-one flag contribution that remains
after quotient-periodic, tangent, fixed-root, and aperiodic charges have
removed the already-accounted cases.

Small quotient-width nodes are polynomial by size alone.  If

```text
q_S<=s_S+2,
```

then `q_S<=sigma+2`, so the local width-one cube is `O_sigma(1)`.  The active
canonical tree has size

```text
#Active(A_0) <= (s_0+2) Q^{s_0+1},
```

where `Q` is the initial quotient width.  Hence all small-`q_S` nodes
contribute `O_sigma(Q^{sigma+1})`.

For large nodes, `q_S>s_S+2`, there is at most one width-one maximal shadow at
the node: two distinct projective fibers of size `q_S-1` would be disjoint and
would force

```text
2(q_S-1)<=q_S+s_S,
```

contradicting `q_S>s_S+2`.

On this large-node range, the first-root injection charges the whole
width-one cube to the one-root fixed-divisor ledger.  Consequently

```text
WO_1(A_0)
 <= FixedRootOneRoot_{r1}(A_0)+O_sigma(Q^{sigma+1}).  (W1-global)
```

Thus, in fixed surplus, the width-one critical-tail branch is closed once the
corresponding one-root fixed-root/root-slice ledger is polynomial.  The
remaining target is not another width-one packing problem; it is to prove or
import the fixed-surplus bound for `FixedRootOneRoot_{r1}` after the standard
quotient-periodic, tangent, fixed-root, and aperiodic charges.
