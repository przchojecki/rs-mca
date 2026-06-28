# M1 Hankel t=2 One-Exchange Core Lift

Status: PROVED-LOCAL / EXACT FINITE VERIFICATION.

Date: 2026-06-28.

Agent/model: Codex acting autonomously through AllenGrahamHart.

## Purpose

This note extracts the first small theorem promised by the M1 Hankel packet
audit: the `t=2` determinant gate and the same-slope one-exchange lift.  The
point is to separate a local collision mechanism that should be charged to a
higher-slack/root-slice ledger, rather than left as unexplained primitive slope
growth.

## Setup

Work with the quotient-normal rank-one target from
`m1_exact_target_v0.md`.  Let `C=RS[F,H,k]`, `|H|=n`, `r=n-k`, and fix

```text
t=2,        a=k+2,        j=n-a=r-2.
```

For a complement `T subset H`, `|T|=j`, write

```text
ell_T(X)=prod_{x in T}(X-x).
```

For a quotient-normal pair `(phi,Y)`, put

```text
a_T = H_{2,j}(Syn(Y)) ell_T,
b_T = H_{2,j}(Syn(phi)) ell_T        in F^2.
```

Here `phi=-g` and `Y=f` in the original line notation.

## Determinant Gate

A complement `T` contributes a finite noncontained slope if and only if

```text
b_T != 0,        a_T = lambda b_T for some lambda in F.
```

Equivalently,

```text
b_T != 0,        det[a_T b_T]=0.
```

When this happens, the finite slope `lambda` is unique.

Proof: the Hankel predicate is

```text
(H_{2,j}(Syn(Y))-lambda H_{2,j}(Syn(phi))) ell_T=0,
```

which is exactly `a_T=lambda b_T`.  The noncontained condition is
`b_T!=0`.  Since `b_T` is a nonzero vector in `F^2`, the scalar is unique when
it exists, and existence is equivalent to rank one of the two columns.

## Same-Slope One-Exchange Lift

Suppose two distinct complements

```text
T_x = R union {x},        T_y = R union {y},        x != y,
```

both contribute the same finite slope `lambda`.  Put

```text
w_lambda = Y - lambda phi.
```

Then the common core `R` satisfies the higher-slack Hankel recurrence

```text
H_{3,j-1}(Syn(w_lambda)) ell_R = 0.          (core-lift)
```

Proof: since both complements have slope `lambda`,

```text
H_{2,j}(Syn(w_lambda)) ell_{T_x}=0,
H_{2,j}(Syn(w_lambda)) ell_{T_y}=0.
```

Writing

```text
ell_{T_x}=(X-x)ell_R,        ell_{T_y}=(X-y)ell_R,
```

and subtracting gives

```text
(y-x) H_{2,j}(Syn(w_lambda)) ell_R=0.
```

Thus rows `0` and `1` of the recurrence vanish on `ell_R`.  Combining this
with either equation for `(X-x)ell_R` also gives rows `1` and `2`.  Hence rows
`0,1,2` vanish on `ell_R`, which is (core-lift).

If

```text
H_{3,j-1}(Syn(phi)) ell_R != 0,
```

then the same slope is noncontained on the larger support `H\R`.  If this
direction vector is zero, the collision has moved into the contained/tangent
side on the core.  In both cases, a same-slope one-exchange collision is not a
free primitive packet: it is visible in the next-slack/core ledger.

## Same-Slope Core-Plane Classification

There is a stronger local normal form for all two-root extensions of a fixed
`(j-2)`-core.  Fix `R` with `|R|=j-2`, set

```text
c_i = sum_h (ell_R)_h Syn_{i+h}(w_lambda),        0<=i<=3,
```

and write a two-root extension as

```text
T=R union {x,y},        sigma=x+y,        pi=xy.
```

Since

```text
ell_T=(X^2-sigma X+pi)ell_R,
```

the same-slope activity equation
`H_{2,j}(Syn(w_lambda))ell_T=0` is exactly

```text
c_2 - sigma c_1 + pi c_0 = 0,
c_3 - sigma c_2 + pi c_1 = 0.                 (CP)
```

Let

```text
M_R = [[-c_1, c_0], [-c_2, c_1]]
```

be the coefficient matrix in `(sigma,pi)`.

If `rank M_R=2`, then `(CP)` has at most one elementary solution, hence at
most one unordered domain pair over the core.  If the augmented system is
inconsistent, there are no active extensions.

If `rank M_R=1` and `(CP)` is consistent, then the two rows

```text
(-c_1,c_0,-c_2),        (-c_2,c_1,-c_3)
```

are proportional.  This forces `c_0 != 0` and, for some `q in F`,

```text
c_1=q c_0,        c_2=q^2 c_0,        c_3=q^3 c_0.
```

The line of solutions is therefore

```text
pi=q sigma-q^2,
```

or equivalently `(x-q)(y-q)=0`.  Thus every active domain extension contains
the same root `q`; this is a fixed-root/root-slice packet on the larger core
`R union {q}` whenever `q` is an available domain root, and otherwise it has
at most one domain member.

Finally, if the coefficient matrix is zero and the system is compatible, then

```text
c_0=c_1=c_2=c_3=0,
```

which is exactly the lower-core recurrence

```text
H_{4,j-2}(Syn(w_lambda))ell_R=0.
```

In that case the whole two-root plane through `R` is active, but it is already
visible in the deeper Hankel core ledger.  Hence a fixed same-slope fiber has
no non-fixed product-Mobius or fixed-sum variable-line component: those
non-fixed lines belong to the different-slope all-line branch, not to residual
same-slope packet growth.

## Two-Edge Corner Dichotomy

The core-plane classification gives a useful graph-local consequence.  Let
`T` be an active complement and let `T_1,T_2` be two distinct active
one-exchange neighbors of `T` in the same fixed-slope fiber.  Write

```text
T_1 = T\{x_1} union {y_1},        T_2 = T\{x_2} union {y_2}.
```

If `x_1=x_2`, then `T,T_1,T_2` all contain the same `(j-1)`-core
`C=T\{x_1}`, and the one-exchange lift gives

```text
H_{3,j-1}(Syn(w_lambda))ell_C=0.
```

If `x_1 != x_2`, put

```text
R=T\{x_1,x_2}.
```

Then `T,T_1,T_2` are three active two-root extensions over the same
`(j-2)`-core `R`.  Their added root pairs have no common root: the first two
share `x_2`, the first and third share `x_1`, but all three cannot share a
single root because the exchanged-in roots are outside `T`.  Therefore the
rank-one fixed-root line alternative in the core-plane classification is
impossible.  Rank two or inconsistency would allow at most one or no active
pair, also impossible.  Hence the full-plane alternative holds, and

```text
H_{4,j-2}(Syn(w_lambda))ell_R=0.
```

Thus every two-edge corner in the active one-exchange graph is either a star
corner already charged at `H_{3,j-1}`, or a lower-core corner charged at
`H_{4,j-2}`.  This is the local no-multiplicative-branching statement for the
`t=2` same-slope graph: branching either stays inside one star ledger or moves
one rung down the Hankel core ladder.

## General Additive Corner Descent

The preceding lower-core alternative is not special to `t=2`.  It is the
first instance of a general lossless Hankel descent.

Let `tau>=1`, `j>=2`, and let `s` be a syndrome vector.  Suppose three
`j`-complements

```text
T   = R union {x_1,x_2},
T_1 = R union {y_1,x_2},
T_2 = R union {x_1,y_2},
```

with `x_1 != x_2`, `y_1 != x_1`, and `y_2 != x_2` all satisfy

```text
H_{tau,j}(s)ell_T =
H_{tau,j}(s)ell_{T_1} =
H_{tau,j}(s)ell_{T_2} = 0.
```

Then the lower core satisfies the additive two-row descent

```text
H_{tau+2,j-2}(s)ell_R=0.                         (AD)
```

Proof: write `L=ell_R` and define

```text
c_i = sum_h L_h s_{i+h}.
```

Subtracting the equations for `T` and `T_1` gives

```text
H_{tau,j-1}(s)(X-x_2)L=0,
```

and subtracting the equations for `T` and `T_2` gives

```text
H_{tau,j-1}(s)(X-x_1)L=0.
```

Subtracting these two displayed equations gives `H_{tau,j-2}(s)L=0`, so
`c_0,...,c_{tau-1}` vanish.  Combining this with
`H_{tau,j-1}(s)(X-x_2)L=0` gives `c_tau=0`.  Finally the original equation
for `T=(X-x_1)(X-x_2)L` gives `c_{tau+1}=0`.  Thus
`c_0,...,c_{tau+1}` vanish, which is exactly (AD).

The important point is that the descent adds two Hankel rows and removes two
locator roots in one structural step.  It is additive in depth: a branching
corner does not introduce a new independent multiplicative packet, it moves to
the next lower-core Hankel ledger.

## General Same-Slope Component Descent

The edge and corner arguments combine into a row-level graph statement.  Fix
`tau>=1` and let `G_{tau,j}(s)` be the graph whose vertices are the active
`j`-complements

```text
H_{tau,j}(s)ell_T=0,
```

with edges between one-exchange complements.

First, every active edge lifts by one row.  If

```text
T_x=C union {x},        T_y=C union {y},        x != y,
```

are adjacent active vertices, then

```text
H_{tau+1,j-1}(s)ell_C=0.                         (ED)
```

Indeed, subtracting the two `H_{tau,j}` equations gives
`H_{tau,j-1}(s)ell_C=0`, and substituting this into either original equation
gives the next row.

Now every nontrivial connected component of `G_{tau,j}(s)` satisfies one of
the following alternatives:

1. it is a star component: all vertices contain one common `(j-1)`-core `C`,
   and (ED) holds for `C`;
2. it contains a distinct-root two-edge corner, and hence a `(j-2)`-core `R`
   satisfying

```text
H_{tau+2,j-2}(s)ell_R=0.                         (CD)
```

Proof: choose an edge in the component.  If every two-edge corner along the
component is a star corner, the same path induction used in the `t=2`
component dichotomy shows that all vertices contain the `(j-1)` core of that
first edge; then (ED) applies.  Otherwise some path step gives two active
neighbors of a vertex which delete two distinct roots, and the general
additive corner descent gives (CD).

Thus, at every row level, same-slope one-exchange components have an additive
ledger: after lower-core corner charges, the residual components are single
star packets, with one-row deeper Hankel cores.  This is the graph-level form
of the no multiplicative depth loss mechanism.

## Same-Slope Component Dichotomy

Let `G_s` be the graph on active `j`-complements for a fixed combined syndrome
`s=Syn(w_lambda)`, with edges joining one-exchange complements.  Every
nontrivial connected component of `G_s` is of one of the following two types:

1. a star component: all its vertices contain one common `(j-1)`-core `C`,
   and

```text
H_{3,j-1}(s)ell_C=0;
```

2. a lower-core component: the component contains a two-edge corner forcing

```text
H_{4,j-2}(s)ell_R=0
```

for some `(j-2)`-core `R`.

Proof: if the component contains a lower-core corner, this is exactly the
second alternative.  Otherwise every two-edge corner in the component is a
star corner.  Choose an edge `T_0--T_1` and put `C=T_0 cap T_1`, so
`|C|=j-1`.  For any path

```text
T_0,T_1,...,T_m
```

we prove by induction that every `T_i` contains `C`.  Suppose `T_{i-1}` and
`T_i` contain `C`.  The edge from `T_i` back to `T_{i-1}` deletes the unique
root of `T_i\C`.  Since there is no lower-core corner at `T_i`, the next edge
from `T_i` to `T_{i+1}` must delete the same root; hence `T_{i+1}` also
contains `C`.  Thus the whole component lies in the star over `C`, and the
one-exchange lift applied to any edge gives `H_{3,j-1}(s)ell_C=0`.

Consequently same-slope one-exchange components do not branch
multiplicatively: after lower-core corners are charged, every remaining
component is a single star packet of size at most `n-j+1`.

## Triangle Packets

The next local shape is a pairwise one-exchange triangle in one fixed-slope
fiber.  In the Johnson graph on `j`-complements, every such triangle is one of
two types:

1. a star triangle with common `(j-1)`-core `R`;
2. a top triangle contained in a common `(j+1)`-set `U`.

Indeed, if `T_1` and `T_2` share a `(j-1)`-core `R`, then a third complement
one-exchange adjacent to both either contains `R` (the star case) or replaces
one element of `R` by the two outside elements of `T_1 union T_2` (the top
case).

Let again `w_lambda=Y-lambda phi`, and suppose every complement in the
triangle has slope `lambda`.  In the star case, the one-exchange core lift
already gives

```text
H_{3,j-1}(Syn(w_lambda)) ell_R = 0.
```

In the top case, write `T=U\{x}` for any one member of the triangle.  Since
`ell_U=(X-x)ell_T` and `H_{2,j}(Syn(w_lambda))ell_T=0`,

```text
H_{1,j+1}(Syn(w_lambda)) ell_U = 0.
```

Thus a top triangle lies in the common lifted `t=1` Hankel kernel of its top
set `U`.  This is the local packet form of the statement that residual top
packets are not independent slope growth; they have moved to a lower-row
Hankel kernel that must be charged separately.

There is a sharper statement for full top packets.  Suppose a `(j+1)`-set `U`
has every `j`-subcomplement

```text
T_x = U\{x},        x in U,
```

active at the same slope.  The polynomials

```text
ell_{T_x} = ell_U/(X-x),        x in U,
```

form a basis of the vector space of polynomials of degree at most `j`.  Since
the two Hankel rows vanish on each `ell_{T_x}`, they vanish on every degree
`<=j` polynomial.  Hence all syndrome coordinates

```text
Syn_0(w_lambda), ..., Syn_{j+1}(w_lambda)
```

are zero.  But in the `t=2` row, `r=n-k=j+2`.  Therefore

```text
Syn(w_lambda)=0.
```

Equivalently, `w_lambda in C`.  Full top packets are thus global-codeword
slopes, belonging to the contained/tangent ledger rather than to residual
primitive top-packet growth.

Consequently, for `Syn(w_lambda) != 0`, a top set `U` has at most `j` active
`j`-subcomplements.  Thus nonzero top packets are partial packets of size at
most `j`; they cannot contain the full `(j+1)`-clique, and their local
same-slope support multiplicity is linearly bounded by the complement size.

## Exact Verifier

The script

```text
python3 experimental/scripts/verify_m1_hankel_t2_one_exchange_lift.py
```

checks the determinant gate against the slope-loop Hankel classifier and then
verifies the one-exchange core lift for every same-slope edge in two exact
tiny scans.

| field/domain | quotient pairs | supports | max bad | max primitive | max slope fiber | lifted one-exchange cores |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `F_5`, `H=F_5^*`, `n=4,k=1,a=3,j=1` | 15625 | 4 | 2 | 2 | 4 | 3480 |
| `F_7`, `H=F_7^*`, `n=6,k=3,a=5,j=1` | 117649 | 6 | 2 | 2 | 6 | 34650 |

In both scans every lifted core was still noncontained on the larger support:

```text
lifted_direction_zero_core_edges = 0.
```

The triangle-packet verifier

```text
python3 experimental/scripts/verify_m1_hankel_t2_triangle_packets.py
```

enumerates the combined syndrome `Syn(w_lambda)` directly, so it can check the
first genuine top-triangle case without a slow quotient-pair scan.

| field/domain | syndromes | one-exchange edges | star triangles | top triangles | full top cliques | max nonzero top active |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `F_5`, `H=F_5^*`, `n=4,k=1,a=3,j=1` | 125 | 6 | 4 | 0 | 6 | 1 |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 16807 | 4410 | 2940 | 420 | 15 | 3 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 2401 | 420 | 420 | 20 | 20 | 2 |
| `F_7`, `H=F_7^*`, `n=6,k=3,a=5,j=1` | 343 | 15 | 20 | 0 | 15 | 1 |

For the cases with `j>=2`, the same verifier also checks every core plane
against the classification above:

| field/domain | nonzero core planes | point | fixed-root line | full lower-core plane | empty/inconsistent | max nonzero active extensions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 100836 | 86436 | 1764 | 36 | 12600 | 10 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 2400 | 2058 | 42 | 0 | 300 | 5 |

It also audits the two-edge corner dichotomy:

| field/domain | nonzero star corners | nonzero lower-core corners | max nonzero star corners/syndrome | max nonzero lower-core corners/syndrome |
| --- | ---: | ---: | ---: | ---: |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 8640 | 3240 | 60 | 90 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 1080 | 0 | 30 | 0 |

Finally, the verifier checks the component dichotomy:

| field/domain | nonzero star components | nonzero lower-core components | max nonzero star component | max nonzero lower-core component |
| --- | ---: | ---: | ---: | ---: |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 540 | 36 | 4 | 10 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 36 | 0 | 5 | 0 |

The `F_7,k=2,j=2` scan is the first exact top-packet check in this file.  It
finds twenty top triangles, all on the zero combined syndrome.  This is not an
asymptotic claim, but it is a useful falsification check: in the smallest
genuine top case, nonzero same-slope triangles are already star/root-slice
events, while full top events are confined to the global-codeword/tangent
ledger.

These are small exact checks, not asymptotic evidence.  Their role is to make
the first `t=2` collision charges reproducible before moving to larger packet
scans and variable-line components.
