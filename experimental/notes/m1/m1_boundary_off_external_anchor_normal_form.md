# M1 Boundary-Off External-Anchor Normal Form

**Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.

**Agent/model:** Codex.

**Date:** 2026-06-27.

This note refines the `Boundary_off` residual from
`m1_hankel_variable_line_packet_lemma.md`. It does not prove the all-line M1
polynomial packing theorem. Its purpose is to replace the opaque one-outside
target image by an explicit external-anchor Hankel incidence.

The proof is local. It assumes the Hankel-pencil normal form and the non-fixed
variable-line singleton hypotheses from the variable-line packet note. It does
not bound the number of boundary targets.

## Setup

Let `D subset F` be a finite evaluation domain, `|D|=n`, and work with the
Reed-Solomon code `RS[F,D,k]`. Let `r=n-k`, fix a complement size `j`, and put
`t=r-j`. Assume `t>=2`.

For received line endpoints `f,g:D->F`, write

```text
u = Syn(f),        v = Syn(g).
```

For a degree-`j` locator vector `ell`, the Hankel-pencil incidence is

```text
(H_{t,j}(u)+zH_{t,j}(v)) ell = 0.
```

Equivalently, with

```text
a(ell)=H_{t,j}(u)ell,        b(ell)=H_{t,j}(v)ell,
```

the projective landing gate is

```text
rank [ a(ell)  b(ell) ] <= 1.                         (HG)
```

The finite noncontained slopes are the points of (HG) with `b(ell) != 0`.

Now fix a `(j-1)`-set `S subset D` and an external anchor `beta in F\D`.
Let

```text
L_S(X) = product_{x in S}(X-x).
```

Write `ell_S^0` and `ell_S^+` for the padded degree-`j` locator vectors of
`L_S(X)` and `X L_S(X)`:

```text
ell_S^0 = coeffs of L_S(X) padded with a final 0,
ell_S^+ = coeffs of X L_S(X).
```

The one-outside target

```text
B = S union {beta}
```

has degree-`j` locator vector

```text
ell_{S,beta} = ell_S^+ - beta ell_S^0.                (EA)
```

Define the four Hankel images

```text
A_u(S)=H_{t,j}(u)ell_S^+,
B_u(S)=H_{t,j}(u)ell_S^0,
A_v(S)=H_{t,j}(v)ell_S^+,
B_v(S)=H_{t,j}(v)ell_S^0.
```

Then

```text
a_S(beta)=A_u(S)-beta B_u(S),
b_S(beta)=A_v(S)-beta B_v(S),
M_S(beta)=[ a_S(beta)  b_S(beta) ].
```

## Theorem 1: Boundary-Off Targets Satisfy An External-Anchor Gate

Let `B` be a one-outside boundary target arising from an active
domain-singleton non-fixed variable-line packet in the sense of
`m1_hankel_variable_line_packet_lemma.md`. Write

```text
B = S union {beta},        S subset D,        |S|=j-1,        beta notin D.
```

Then `beta` satisfies the external-anchor Hankel gate

```text
rank M_S(beta) <= 1.                                  (EAG)
```

Equivalently, for every pair of row indices `0<=alpha<gamma<t`,

```text
Q_{alpha,gamma,S}(beta) = 0,                          (Q)
```

where

```text
Q_{alpha,gamma,S}(Y)
 = det [[ a_S(Y)_alpha, b_S(Y)_alpha ],
        [ a_S(Y)_gamma, b_S(Y)_gamma ]].
```

Each `Q_{alpha,gamma,S}(Y)` is a polynomial in `Y` of degree at most two.

Moreover `B` has an active all-domain neighbor: there exists an active
noncontained `D`-split locator `T subset D`, `|T|=j`, such that

```text
|T cap S| = j-2.
```

Thus the `Boundary_off` image is contained in the set of external-anchor
incidences `(S,beta)` satisfying (EAG) and adjacent to the active all-domain
locator family by this one-outside two-exchange relation.

### Proof

The coefficient identity (EA) is just

```text
(X-beta)L_S(X) = X L_S(X) - beta L_S(X).
```

Multiplying by the Hankel windows gives the affine formulas for `a_S(beta)`
and `b_S(beta)`.

A one-outside boundary target in the variable-line packet note is produced by
an off-domain root on the same proper non-fixed determinantal component `L` as
the active domain singleton. By definition of that component, every point on
`L` satisfies the projective Hankel landing gate (HG). Applying this to the
point `B=S union {beta}` gives `rank M_S(beta)<=1`.

The minor equations (Q) are exactly the condition that a `t x 2` matrix has
rank at most one. Since each column of `M_S(Y)` is affine-linear in `Y`, every
minor is quadratic or lower.

Finally, if the singleton packet has core `R` and active locator

```text
T = R union {x_a,iota_L(x_a)},
```

while the off-domain root is `x` with `iota_L(x)=beta notin D`, then

```text
S = R union {x}.
```

The active domain pair and the off-domain pair are distinct packet points, so
`T cap S = R` and `|R|=j-2`. This proves the stated active-neighbor
certificate.

## Corollary 2: Nondegenerate Quadratic-Anchor Branch

Fix `S subset D`, `|S|=j-1`. If at least one polynomial
`Q_{alpha,gamma,S}` is not identically zero, then there are at most two
external anchors `beta in F` satisfying (EAG) for this `S`.

Consequently, any domain shadow `S` that supports three distinct external
anchors is forced into the degenerate branch where all minors
`Q_{alpha,gamma,S}` vanish identically.

### Proof

A nonzero polynomial of degree at most two over a field has at most two roots.
All external anchors satisfying (EAG) are common roots of the minors, so they
are roots of any one nonzero minor.

## Corollary 3: The Degenerate Branch Is Ruled

Fix `S subset D`, `|S|=j-1`, and suppose every minor
`Q_{alpha,gamma,S}` vanishes identically. Put

```text
M_0=[ A_u(S)  A_v(S) ],        M_1=[ B_u(S)  B_v(S) ].
```

Then every matrix in the linear span

```text
W_S = span{M_0,M_1} subset Mat_{t x 2}(F)
```

has rank at most one.

If `dim W_S=2`, exactly one of the following ruled alternatives holds after
discarding zero matrices:

```text
common-image branch:
  all nonzero matrices in W_S have image contained in one fixed line in F^t;

common-kernel branch:
  all nonzero matrices in W_S have kernel containing one fixed line in F^2.
```

If `dim W_S<=1`, the same statement is read in the evident one-dimensional
sense.

### Proof

The identities `Q_{alpha,gamma,S}(Y)=0` say that every matrix

```text
M_0 - Y M_1
```

has rank at most one as a polynomial identity in `Y`. Equivalently, every
homogeneous combination `lambda M_0 + mu M_1` has rank at most one, so `W_S`
is a linear subspace of the rank-one cone.

Assume `dim W_S=2` and choose a nonzero `M in W_S`. After row and column basis
changes, write

```text
M = [[1,0],
     [0,0],
     ...
     [0,0]].
```

Let

```text
N = (n_{i,c})
```

be a second generator of `W_S`. The `2 x 2` minor of `M+sN` using rows `1,i`
with `i>1` and both columns has coefficient of `s`

```text
n_{i,2}.
```

Hence `n_{i,2}=0` for every `i>1`. The coefficient of `s^2` in the same minor
then gives

```text
n_{1,2} n_{i,1}=0        for every i>1.
```

If `n_{1,2}=0`, then both generators kill the second coordinate vector, so
there is a common kernel line. If `n_{1,2} != 0`, then `n_{i,1}=0` for every
`i>1`, so both generators have image contained in the first coordinate line.
This is the common-image branch.

## Consequence For The M1 Boundary Residual

The one-outside target image from the variable-line packet lemma now has a
canonical split by domain shadow `S=B cap D`:

```text
Boundary_off = Boundary_off^quad union Boundary_off^ruled.
```

A target lies in `Boundary_off^quad` when at least one quadratic minor for its
shadow `S` is nonzero, and in `Boundary_off^ruled` when all those minors vanish
identically.

For `Boundary_off^quad`, each fixed domain shadow `S=B cap D` admits at most
two external anchors. Thus the remaining work in this branch is to bound the
number of adjacent domain shadows `S` that occur next to active all-domain
locators.

For `Boundary_off^ruled`, the obstruction is not a large arbitrary
one-variable root set. It is a ruled rank-one Hankel artifact:

```text
common-kernel ruled branch:
  a fixed projective slope kills the whole external-anchor pencil;

common-image ruled branch:
  all boundary Hankel images lie in one fixed line in F^t.
```

This is a sharper target than the original opaque `Boundary_off` term. A
future closure of the non-fixed variable-line branch can now try to prove that
the ruled branch is charged by the existing fixed-slope/root-slice,
contained/tangent, quotient-periodic, or active-codegree ledgers, and that the
nondegenerate quadratic branch has polynomially many adjacent domain shadows.

## Non-Claims

This note does not prove

```text
|Boundary_off| <= n^B.
```

It also does not prove the all-line M1 theorem, a corrected-reserve MCA bound,
or a prize threshold. It only proves the local external-anchor normal form and
the nondegenerate/ruled split for the boundary target image already isolated in
the variable-line packet lemma.
