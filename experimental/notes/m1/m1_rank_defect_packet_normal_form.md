# M1 rank-defect packet normal form

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note extracts the second reviewable local lemma from the broad
same-slope packet in PR #138, following the split requested in
`experimental/notes/triage/pr-triage-2026-06-30.md`.  The root-slice lift is
the `h=1` case.  The present note treats the general `h`-exchange packet:
full affine-rank same-slope packets lift losslessly to higher Hankel cores,
and the residual rank-defect packets have an exact affine-subpacket normal
form with a finite-field moving-fiber count.

## Scope and non-claims

This is local algebra inside the Hankel-pencil normal form.  It does not prove
the all-line M1 aperiodic local limit, does not bound the global residual
slope image, and does not add a leaderboard or threshold row.  It is meant to
separate the same-slope affine-packet ledger from the later different-slope,
Kummer, quotient, and endpoint gates.

Field ledger: the statement is over an arbitrary field `F`.  In an MCA
application `z` is a finite line slope in `q_line`.  No generated-field,
challenge-field, denominator, or radius endpoint convention enters this local
step.  Split-root, distinct-root, domain-root, quotient-periodic,
contained/tangent, and noncontainment filters are external filters; every
count below is a formal coefficient-space ceiling before those filters, so the
filters can only decrease it.

## Setup

Fix a finite-slope Hankel-pencil map

```text
L_z = H_{t,j}(u) + z H_{t,j}(v).
```

Fix `1 <= h <= j` and a `(j-h)`-core locator `ell_R`.  Write a formal monic
`h`-root factor in coefficient coordinates as

```text
P_c(X) = X^h + c_{h-1}X^{h-1} + ... + c_0,
         c=(c_0,...,c_{h-1}) in F^h,
```

and put

```text
ell_{R,c} = P_c(X) ell_R.
```

For the shifted landing vectors

```text
V_m = L_z(X^m ell_R),        0 <= m <= h,
```

the same-slope equation on the `h`-exchange coefficient space is affine-linear:

```text
L_z ell_{R,c}
  = V_h + sum_{m=0}^{h-1} c_m V_m.                (HPKT)
```

## Full affine-rank lift

If `h+1` affinely independent coefficient points
`c^(0),...,c^(h) in F^h` satisfy

```text
L_z ell_{R,c^(i)} = 0        for 0 <= i <= h,
```

then

```text
V_m = 0        for 0 <= m <= h.                    (HLIFT0)
```

Equivalently,

```text
H_{t+h,j-h}(u+zv) ell_R = 0.                       (HLIFT)
```

Proof: append a final coordinate `1` to each `c^(i)`.  Affine independence
means the resulting `(h+1) x (h+1)` matrix is invertible.  Equation `(HPKT)`
therefore gives an invertible linear system for the unknown vectors
`V_0,...,V_{h-1},V_h`, forcing all of them to vanish.  The padded equation
`L_z(X^m ell_R)=0` gives rows `m,...,m+t-1` of `(HLIFT)`, and the row blocks
for `0 <= m <= h` cover exactly rows `0,...,t+h-1`.

Thus full affine-rank same-slope `h`-exchange packets are not residual
aperiodic multiplicity.  They are charged to the lifted `(t+h,j-h)` Hankel
core at the same finite slope.

## Affine-span normal form

Let `C subset F^h` be any set of coefficient points satisfying

```text
L_z ell_{R,c} = 0        for every c in C.
```

Let

```text
A = aff(C) = c_* + W
```

be its affine span, with direction subspace `W subset F^h`.  Then the equations
on `C` are equivalent to

```text
V_h + sum_{m=0}^{h-1} c_{*,m} V_m = 0,            (ASP0)
sum_{m=0}^{h-1} w_m V_m = 0        for every w in W.  (ASPD)
```

Consequently

```text
L_z ell_{R,c} = 0        for every c in A.         (ASPA)
```

Proof: choose points of `C` spanning `A`.  Subtract the equation at `c_*` from
the equations at the spanning points.  This gives `(ASPD)` on a spanning set
of `W`, hence on all of `W`; `(ASP0)` is the equation at `c_*`.  Conversely,
`(ASP0)` and `(ASPD)` give `(ASPA)` by substituting `c=c_*+w`.

Therefore a same-slope packet is a whole formal affine subpacket in elementary
coefficient space.  After the full-rank lift above, every remaining same-slope
`h`-exchange packet lies in a proper affine subspace of `F^h`; these are the
rank-defect packets.

## Fixed-root hyperplanes

Codimension-one rank-defect packets have a useful evaluation test.  Let

```text
H(a,b):        b + sum_{m=0}^{h-1} a_m c_m = 0,
               a=(a_0,...,a_{h-1}) != 0.
```

Then `H(a,b)` is exactly the hyperplane of monic `h`-root factors containing a
fixed finite root `alpha` if and only if there is a scalar `lambda != 0` such
that

```text
a_m = lambda alpha^m        for 0 <= m < h,
b   = lambda alpha^h.                                (FROOT)
```

Indeed, `P_c(alpha)=0` is

```text
alpha^h + sum_{m=0}^{h-1} alpha^m c_m = 0,
```

and multiplying this equation by `lambda` gives `(FROOT)`.  Conversely,
`(FROOT)` is just the same evaluation equation.  Hyperplanes of this form are
not new rank-defect residual packets: every split locator in them has the
fixed root `alpha` and is charged to the lower exchange ledger through the
enlarged core `R union {alpha}`.

## Moving-fiber dimension drop

Fix `1 <= r <= h` and a monic `(h-r)`-root factor

```text
Q(X)=X^{h-r}+e_{h-r-1}X^{h-r-1}+...+e_0,
```

with `e_{h-r}=1` and `e_i=0` outside `0 <= i <= h-r`.  Let

```text
B_a(X)=X^r+a_{r-1}X^{r-1}+...+a_0,        a in F^r,
P_a(X)=B_a(X)Q(X)
      =X^h+c_{h-1}(a)X^{h-1}+...+c_0(a).
```

The coefficient map `a |-> c(a)` is the affine embedding

```text
c_m(a) = e_{m-r} + sum_{i=0}^{r-1} a_i e_{m-i},
         0 <= m < h.                               (RFIB)
```

Its direction vectors

```text
d_i = (e_{m-i})_{0 <= m < h},        0 <= i < r,    (RDIR)
```

are linearly independent: a relation among the `d_i` would make
`(sum_i a_i X^i)Q(X)=0`, hence `sum_i a_i X^i=0`.

Let `A=c_*+W` be any affine rank-defect packet.  The intersection of `A` with
the moving `r`-root fiber over `Q` is the preimage of `A` under the affine
embedding `(RFIB)`, hence an affine subspace of `F^r`.  If this preimage has
full affine rank `r`, equivalently if it contains `r+1` affinely independent
parameter points, then every direction `d_i` lies in `W`, and the whole moving
`r`-root fiber lies in `A`.  Otherwise the intersection has affine rank at
most `r-1`.

In the killed same-slope Hankel setting, the full-fiber case is charged to the
full elementary-packet lift with moving size `r`, namely to the lifted
`(t+r,j-r)` Hankel core on `ell_R Q`.  Therefore, after full moving `r`-root
fibers have been charged, residual affine rank-defect packets meet every fixed
moving `r`-root fiber only in lower-dimensional affine subpackets.

## Finite-field count and residual exchange degree

Over a finite field `F` with `|F|=Q_F`, the dimension drop gives the formal
fiber count

```text
# { a in F^r : coeff(B_a Q) in A } <= Q_F^{r-1}.    (RCOUNT)
```

whenever the full moving `r`-root fiber over `Q` has not been charged.  The
split-root, distinct-root, domain-root, quotient, tangent, and noncontainment
filters can only shrink this count.

Equivalently, inside one residual affine rank-defect `h`-exchange packet, let
`G_r^res` be the graph on remaining formal `h`-root locators where two
vertices are adjacent when they share exactly `h-r` moving roots.  For a fixed
residual locator there are `binom(h,r)` choices of the shared `(h-r)` factor,
and each uncharged moving fiber contributes at most `Q_F^{r-1}-1` other
formal parameters.  Hence

```text
Delta(G_r^res) <= binom(h,r)(Q_F^{r-1}-1).          (RDEG)
```

In particular, `r=1` leaves no residual one-exchange edges inside an uncharged
affine rank-defect packet, while `r=2` gives the formal line-packet ceiling
`binom(h,2)(Q_F-1)`.

## Residual use in M1

This local theorem supplies the rank-defect filtration requested by the June
30 triage.  Same-slope multiplicity has three explicit destinations:

```text
full affine-rank packet       -> lifted (t+h,j-h) Hankel core,
fixed-root hyperplane packet  -> lower exchange/root-slice ledger,
residual rank-defect packet   -> moving-fiber count and exchange-degree bound.
```

The remaining global M1 work is still to sum these local ledgers after quotient
floors, contained/tangent branches, noncontainment, different-slope codegrees,
and the aperiodic local-limit estimates are all accounted for.

## Verification

The companion verifier checks the affine-span identities, full-rank linear
system, Hankel row lift, fixed-root hyperplane criterion, moving-fiber affine
embedding, and finite-field fiber count over sampled prime fields:

```sh
python3 experimental/scripts/verify_m1_rank_defect_packet_normal_form.py
```
