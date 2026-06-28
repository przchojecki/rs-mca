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

## Same-Slope Component Counting Ledger

The component descent gives an explicit summable bound.  For fixed `s`,
write

```text
A_{tau,j}(s) = { T subset H : |T|=j, H_{tau,j}(s)ell_T=0 },
```

and let `A^+_{tau,j}(s)` be the non-isolated vertices in the one-exchange
graph on `A_{tau,j}(s)`.  Define the lower ledgers

```text
S_{tau+1,j-1}(s)
 = { C subset H : |C|=j-1, H_{tau+1,j-1}(s)ell_C=0 },

L_{tau+2,j-2}(s)
 = { R subset H : |R|=j-2, H_{tau+2,j-2}(s)ell_R=0 }.
```

Then

```text
|A^+_{tau,j}(s)| <= (n-j+1) |S_{tau+1,j-1}(s)|.          (NL)
```

Moreover the number of star components is at most
`|S_{tau+1,j-1}(s)|`, and the number of non-star components is at most
`|L_{tau+2,j-2}(s)|`.

Proof: every non-isolated active `T` has an active one-exchange neighbor
`T'`.  Their common `(j-1)`-core `C=T cap T'` lies in
`S_{tau+1,j-1}(s)` by (ED), and `T` contains `C`.  A fixed `(j-1)`-core is
contained in exactly `n-j+1` `j`-complements, proving (NL).

A star component is contained in the full star over its common core `C`; two
components cannot charge the same `C`, since `H_{tau+1,j-1}(s)ell_C=0` makes
all `j`-extensions of `C` active and connected.  Similarly, a non-star
component contains a lower-core witness `R` by (CD).  If
`H_{tau+2,j-2}(s)ell_R=0`, then every two-root extension of `R` is active for
`H_{tau,j}`, and those extensions form a connected Johnson graph.  Hence the
same `R` cannot be charged by two different components.

Thus same-slope support multiplicity is paid by lower Hankel ledgers with only
the local factor `n-j+1` for non-isolated vertices, and branching component
count is paid by the two-row lower-core ledger.

## Isolated Active Locator Criterion

It remains to identify the exact local shape of the vertices not covered by
`A^+_{tau,j}(s)`.  Let `T` be active for `H_{tau,j}(s)` and fix a root
`x in T`.  Put `C=T\{x}`, `L=ell_C`, and

```text
c_i = sum_h L_h s_{i+h}.
```

Since `ell_T=(X-x)L`, activity of `T` gives

```text
c_{i+1}=x c_i,        0<=i<tau.
```

Thus the one-row deeper boundary vector on `C` has the root-marked form

```text
H_{tau+1,j-1}(s)ell_C
  = c_0 (1,x,x^2,...,x^tau).                    (IB)
```

For another extension `C union {y}`, the activity equations are

```text
c_{i+1}=y c_i,        0<=i<tau.
```

If `c_0=0`, then the whole boundary vector in (IB) is zero and every extension
of `C` is active.  If `c_0!=0`, then these equations force `y=x`; no
one-exchange neighbor of `T` occurs through this deletion core.

Consequently, assuming `j<n`, an active locator `T` is isolated in the
one-exchange graph if and only if for every `x in T`,

```text
H_{tau+1,j-1}(s)ell_{T\{x}} != 0.
```

Equivalently, each deletion core carries a nonzero scalar on the Veronese
vector `(1,x,...,x^tau)`.  This turns isolated same-slope support mass into a
root-marked first-boundary residual rather than an unexplained packet.

Let `Iso_{tau,j}(s)` be the isolated active locators and define the
root-marked boundary ledger

```text
B^rm_{tau+1,j-1}(s)
 = { (C,x) : |C|=j-1, x notin C,
             H_{tau+1,j-1}(s)ell_C = c(1,x,...,x^tau), c != 0 }.
```

Then

```text
j |Iso_{tau,j}(s)| <= |B^rm_{tau+1,j-1}(s)|.       (IL)
```

Indeed, every isolated `T` contributes all `j` marked pairs `(T\{x},x)`, and
the map `(T,x) -> (T\{x},x)` is injective.  Thus isolated support mass is
summable once the root-marked first-boundary ledger is controlled.

## First-Boundary Incidence Identity

The root-marked boundary ledger is part of an exact first-boundary
decomposition, not only an upper-bound device.  Let

```text
Z_{tau+1,j-1}(s)
 = { C subset H : |C|=j-1,
     H_{tau+1,j-1}(s)ell_C=0 },

E_{tau+1,j-1}(s)
 = { C subset H : |C|=j-1,
     C union {x}, C union {y} in A_{tau,j}(s)
     for some distinct x,y notin C }.
```

Thus `E_{tau+1,j-1}(s)` is the set of one-row edge cores that actually occur
in the active one-exchange graph.  For `1<=j<n`,

```text
E_{tau+1,j-1}(s) = Z_{tau+1,j-1}(s),
```

and the active deletion incidences satisfy the exact identity

```text
j |A_{tau,j}(s)|
 = (n-j+1) |E_{tau+1,j-1}(s)|
   + |B^rm_{tau+1,j-1}(s)|.                  (FI)
```

Proof: fix a `(j-1)`-core `C`, put `L=ell_C`, and write

```text
c_i = sum_h L_h s_{i+h},        0<=i<=tau.
```

The extension `C union {x}` is active exactly when

```text
c_{i+1}=x c_i,        0<=i<tau.               (AE)
```

If all `c_i` vanish, then every `x notin C` satisfies (AE), giving exactly
`n-j+1` active extensions over `C`.  These are connected by one-exchange
edges through the core `C`, so `C in E_{tau+1,j-1}(s)`.

If the boundary vector is nonzero and `c_0=0`, then (AE) already fails in the
first nonzero step, so no extension over `C` is active.  If `c_0!=0`, then
there is at most one active extension: the root must be
`x=c_1/c_0`, and the remaining equations say exactly that
`H_{tau+1,j-1}(s)ell_C` is the nonzero root-marked vector
`c_0(1,x,...,x^tau)`.  Thus this case contributes one active deletion
incidence precisely for each pair in `B^rm_{tau+1,j-1}(s)`.

Summing over all `(j-1)`-cores counts each active `j`-locator once for each of
its `j` roots, proving (FI).  Conversely, if `C` is an active edge core, two
distinct roots satisfy (AE), forcing the boundary vector to vanish; hence
`E=Z`.  The earlier support ledger follows at once, but (FI) is sharper: it
shows that same-slope active support is exactly split between zero
first-boundary edge cores and nonzero root-marked first-boundary incidences.

## Fixed-Root Boundary Decomposition

The identity (FI) also holds root by root.  For `x in H`, define

```text
A^x_{tau,j}(s) = { T in A_{tau,j}(s) : x in T },

Z^x_{tau+1,j-1}(s)
 = { C in Z_{tau+1,j-1}(s) : x notin C },

B^x_{tau+1,j-1}(s)
 = { C : (C,x) in B^rm_{tau+1,j-1}(s) }.
```

Then, for every `x in H`,

```text
|A^x_{tau,j}(s)|
 = |Z^x_{tau+1,j-1}(s)| + |B^x_{tau+1,j-1}(s)|.      (FR)
```

Proof: send `T in A^x_{tau,j}(s)` to its deletion core `C=T\{x}`.  The
first-boundary classification over `C` has only three cases.  If the boundary
is zero, then `C in Z^x`.  If the boundary is nonzero, activity of the
extension by `x` forces the nonzero root-marked form with mark `x`, so
`C in B^x`.  These two cases are disjoint and exhaust the active fixed-root
slice.  Conversely, each `C in Z^x` gives the active extension `C union {x}`,
and each `C in B^x` gives exactly the same active extension.  This proves
(FR).

Thus the nonzero root-marked chart is not a separate same-slope branching
object.  It is the fixed-root active slice after the zero first-boundary star
cores have been removed.  Consequently, any global M1 argument that charges
fixed-root/root-slice active slices and zero-boundary edge cores also charges
the root-marked first-boundary residual.

## Fixed-Root Difference Hankel Form

The fixed-root slice has an ordinary Hankel kernel form after taking a
root-difference of the syndrome.  For `x in H`, define

```text
(Delta_x s)_i = s_{i+1} - x s_i.
```

Then multiplication by `(X-x)` gives the exact identity

```text
H_{tau,j}(s)((X-x)L)
 = H_{tau,j-1}(Delta_x s)L.                  (DX)
```

Hence the deletion map `T -> T\{x}` gives a bijection

```text
A^x_{tau,j}(s)
 <-->
K^x_{tau,j-1}(s)
 = { C subset H\{x} : |C|=j-1,
     H_{tau,j-1}(Delta_x s)ell_C=0 }.
```

Under this bijection,

```text
Z^x_{tau+1,j-1}(s)
 = { C in K^x_{tau,j-1}(s) :
     H_{tau+1,j-1}(s)ell_C=0 },

B^x_{tau+1,j-1}(s)
 = K^x_{tau,j-1}(s) \ Z^x_{tau+1,j-1}(s).
```

Proof: if `L=sum_h L_h X^h`, then the `i`th row of the left side of (DX) is

```text
sum_h L_h s_{i+h+1} - x sum_h L_h s_{i+h},
```

which is exactly the `i`th row of `H_{tau,j-1}(Delta_x s)L`.  The bijection
is then just `ell_T=(X-x)ell_C`.  The final two identities are the
first-boundary classification: a fixed-root active core has zero boundary
exactly in the star-core case, and otherwise has the nonzero root-marked
boundary with mark `x`.

Thus the remaining nonzero root-marked chart is a root-slice difference-kernel
problem with a named zero-boundary subkernel removed.  This is the form in
which fixed-root/root-slice, quotient-periodic, or aperiodic-packing bounds
should be applied.

## Iterated Fixed-Root Difference Identity

The fixed-root identity iterates without loss.  For an ordered tuple of
distinct domain roots

```text
X_1=(x_1,...,x_m),
```

write

```text
Delta_{X_1}s = Delta_{x_m} ... Delta_{x_1}s.
```

Then, for any locator `L` with support disjoint from the `x_i`,

```text
H_{tau,j}(s)((X-x_1)...(X-x_m)L)
 = H_{tau,j-m}(Delta_{X_1}s)L.               (IDX)
```

Equivalently, deleting a fixed root chain identifies the active locators
containing all `x_i` with a squarefree support kernel for the iterated
root-difference syndrome:

```text
{ T : {x_1,...,x_m} subset T,
      H_{tau,j}(s)ell_T=0 }
 <->
{ C subset H\{x_1,...,x_m} : |C|=j-m,
      H_{tau,j-m}(Delta_{X_1}s)ell_C=0 }.
```

Proof: the case `m=1` is (DX).  Applying (DX) successively to
`Delta_{x_1}s`, then to `Delta_{x_2}Delta_{x_1}s`, and so on gives (IDX).
The difference operators commute because they are polynomials in the shift
operator, so the ordered notation is only for bookkeeping.

This is the algebraic backbone of the residual ladder above: every time a
fixed root is stripped from a locator, the row count is unchanged, the locator
degree drops by one, and the syndrome is replaced by one more root-difference.
Additive descent can therefore be iterated on root-slice kernels rather than
creating a multiplicative tree of new packet types.

## Recursive First-Boundary Ledger on Fixed-Root Chains

The first-boundary incidence identity is stable under the same fixed-root
deletion.  Let `X_1=(x_1,...,x_m)` be a tuple of distinct roots with `0<=m<j`,
put

```text
d = Delta_{X_1}s,        q=j-m,        H_X=H\{x_1,...,x_m}.
```

Define the fixed-chain active slice

```text
A^{X_1}_{tau,j}(s)
 = { T subset H : {x_1,...,x_m} subset T,
     H_{tau,j}(s)ell_T=0 },
```

and the difference-kernel support family on the remaining domain

```text
K^{X_1}_{tau,q}(s)
 = { C subset H_X : |C|=q, H_{tau,q}(d)ell_C=0 }.
```

For `(q-1)`-cores in `H_X`, let

```text
Z^{X_1}_{tau+1,q-1}(s)
 = { D subset H_X : |D|=q-1,
     H_{tau+1,q-1}(d)ell_D=0 },

B^{X_1,rm}_{tau+1,q-1}(s)
 = { (D,y) : D subset H_X, |D|=q-1, y in H_X\D,
     H_{tau+1,q-1}(d)ell_D=c(1,y,...,y^tau), c!=0 }.
```

Then the fixed-chain deletion map gives a bijection

```text
A^{X_1}_{tau,j}(s) <--> K^{X_1}_{tau,q}(s),
```

and the active deletion incidences inside this rung satisfy

```text
q |K^{X_1}_{tau,q}(s)|
 = (n-j+1) |Z^{X_1}_{tau+1,q-1}(s)|
   + |B^{X_1,rm}_{tau+1,q-1}(s)|.             (RFI)
```

Equivalently,

```text
(j-m) |A^{X_1}_{tau,j}(s)|
 = (n-j+1) |Z^{X_1}_{tau+1,j-m-1}(s)|
   + |B^{X_1,rm}_{tau+1,j-m-1}(s)|.
```

Proof: the bijection is (IDX).  Apply the first-boundary identity (FI) to the
ordinary active family `K^{X_1}_{tau,q}(s)` over the smaller domain `H_X` and
the syndrome `d`.  A zero boundary `(q-1)`-core has exactly

```text
|H_X|-(q-1) = (n-m)-(j-m-1) = n-j+1
```

available extensions, giving the same extension factor as the original rung.
The nonzero one-extension case is exactly the root-marked condition in
`B^{X_1,rm}`.  Hence the fixed-root ladder has the same additive
zero-boundary/root-marked split at every rung; it does not acquire a new
multiplicative loss when a root chain has already been stripped.

## Fixed-Root Filtration Incidence Sequence

The count (RFI) comes from an exact set identity.  Keep the notation
`d=Delta_{X_1}s`, `q=j-m`, and `H_X=H\{x_1,...,x_m}`.  Let

```text
I^{X_1}_{tau,q}(s)
 = { (C,y) : C in K^{X_1}_{tau,q}(s), y in C },
```

and send `(C,y)` to `(D,y)` with `D=C\{y}`.  Then (IDX), applied one more
time to the root `y`, identifies this incidence set with the next fixed-root
layer:

```text
I^{X_1}_{tau,q}(s)
 <->
N^{X_1}_{tau,q-1}(s)
 = { (D,y) : y in H_X\D,
     D in K^{X_1 union {y}}_{tau,q-1}(s) }.
```

For each `(q-1)`-core `D`, write

```text
v_D=H_{tau+1,q-1}(d)ell_D.
```

The fiber of `N^{X_1}` above `D` is exactly:

1. all `n-j+1` available roots `y` if `v_D=0`;
2. the single root-marked root `y` if
   `v_D=c(1,y,...,y^tau)` with `c!=0` and `y in H_X\D`;
3. the empty set otherwise.

Therefore there is a disjoint union

```text
I^{X_1}_{tau,q}(s)
 =
{ (D,y) : D in Z^{X_1}_{tau+1,q-1}(s), y in H_X\D }
 disjoint_union
B^{X_1,rm}_{tau+1,q-1}(s).                  (FIS)
```

Proof: for `C=D union {y}`, the equation
`C in K^{X_1}_{tau,q}(s)` is

```text
H_{tau,q}(d)((X-y)ell_D)=0.
```

By the one-root difference identity (DX), this is equivalent to

```text
H_{tau,q-1}(Delta_y d)ell_D=0,
```

which is the next fixed-root condition
`D in K^{X_1 union {y}}_{tau,q-1}(s)`.  The first-boundary vector `v_D`
then classifies the possible `y`: if `v_D=0`, every available root gives an
active extension; if `v_D` is nonzero, the recurrence equations force
`y=v_{D,1}/v_{D,0}` and the remaining coordinates are precisely the
Veronese/root-marked condition; if `v_{D,0}=0` or the Veronese equations fail,
there is no available finite root.  This proves (FIS), and taking cardinalities
gives (RFI).

Thus the root-marked residual at a fixed rung is not a new layer of
unstructured objects: it is the nonzero part of the next fixed-root incidence
sequence, while zero-boundary cores give the whole star fiber.  This is the
set-level form of the additive-loss mechanism.

## First-Zero Stopping Decomposition

Iterating (FIS) gives a finite stopping rule for every ordered deletion path.
Let `X_1` be a fixed root chain and let
`C in K^{X_1}_{tau,q}(s)`.  Choose an ordering

```text
C=(y_1,...,y_q).
```

Set

```text
X_h=X_1 union {y_1,...,y_{h-1}},
C_h=C\{y_1,...,y_{h-1}},
D_h=C_h\{y_h},
d_h=Delta_{X_h}s.
```

Starting with `h=1`, exactly one of the following happens at each stage:

1. `H_{tau+1,|D_h|}(d_h)ell_{D_h}=0`.  The path stops at the
   zero-boundary star over `D_h`.
2. The same boundary vector is nonzero and root-marked by `y_h`.  Then
   `D_h in K^{X_h union {y_h}}_{tau,|D_h|}(s)`, and the path continues to
   the next rung.

If the path never stops, it reaches the terminal bottom condition

```text
H_{tau,0}(Delta_{X_1 union C}s)1=0.            (TERM)
```

Proof: assume the path has not stopped before depth `h`.  Then repeated use
of (FIS) shows that `C_h` lies in the active kernel
`K^{X_h}_{tau,|C_h|}(s)`.  Apply (FIS) to the incidence
`(C_h,y_h)`.  If the deleted boundary core is zero-boundary, the path stops.
Otherwise the same incidence is in the nonzero root-marked part, which is
equivalent to the next fixed-root condition for `D_h`.  This proves the
induction step.  If no zero-boundary stop occurs, after all `q` deletions the
empty locator is active for the iterated difference syndrome, which is (TERM).

Thus every ordered active-support deletion path has a first charged
zero-boundary rung or a bottom terminal difference condition.  The filtration
has finite depth `q`, and nonzero marked steps merely move to the next
fixed-root layer; they do not create a parallel packet family.

## Ordered First-Zero Ledger

The stopping rule gives an ordered counting ledger.  Let
`Path^{X_1}_{tau,q}(s)` be the set of pairs `(C,pi)` where
`C in K^{X_1}_{tau,q}(s)` and `pi` is an ordering of `C`.  Let
`Stop_h^{X_1}` be the subset whose first zero-boundary stop occurs at depth
`h`, and let `Term^{X_1}` be the subset with no zero-boundary stop.  Then

```text
|Path^{X_1}_{tau,q}(s)|
 = sum_{h=1}^q |Stop_h^{X_1}| + |Term^{X_1}|.       (OZ)
```

Moreover every first-zero stop is charged to a one-row deeper zero-boundary
ledger.  If `P=(y_1,...,y_{h-1})` is the prefix before the first stop and
`d_P=Delta_{X_1 union P}s`, the stop core `D` has size `q-h` and satisfies

```text
H_{tau+1,q-h}(d_P)ell_D=0.
```

Thus, after dropping the requirement that the prefix itself was zero-free, one
has the upper ledger

```text
|Stop_h^{X_1}|
 <= (q-h)! (n-j+1)
    sum_P |Z^{X_1 union P}_{tau+1,q-h}(s)|,        (OZL)
```

where the sum is over ordered distinct prefixes `P` of length `h-1` disjoint
from `X_1`.

Proof: (OZ) is the disjoint partition by the first time the stopping
algorithm encounters a zero boundary, with `Term` collecting the paths for
which this never happens.  For (OZL), a path in `Stop_h` determines its
zero-free prefix `P`, the stopped root `y_h`, the remaining core `D`, and an
ordering of `D` after the stop.  The stopped core satisfies the displayed
zero-boundary equation by definition.  For fixed `P` and `D`, the stopped
root has at most

```text
|H\setminus(X_1 union P union D)| = n-j+1
```

choices, and the suffix has `(q-h)!` possible orders.  Forgetting the
zero-free prefix condition can only enlarge the right side.  Hence all
nonterminal ordered mass is paid by one-row deeper zero-boundary ledgers; the
only uncharged residual in this filtration is the terminal zero-free flag set.

## Terminal Flags Reduce to Bottom Supports

The terminal zero-free flags are controlled by an unordered bottom support
set.  Define

```text
Bot^{X_1}_{tau,q}(s)
 = { C in K^{X_1}_{tau,q}(s) :
     H_{tau,0}(Delta_{X_1 union C}s)1=0 }.
```

Then the forgetful map `(C,pi) -> C` gives

```text
|Term^{X_1}| <= q! |Bot^{X_1}_{tau,q}(s)|.        (TB)
```

Proof: if `(C,pi)` is terminal, the stopping decomposition reaches (TERM),
so `C` lies in `Bot^{X_1}`.  The condition is independent of the order `pi`,
because the root-difference operators commute.  For a fixed unordered `C`
there are at most `q!` orderings.  This proves (TB).

By (IDX), the bottom condition is equivalent to `C in K^{X_1}_{tau,q}(s)`.
Thus `Bot^{X_1}_{tau,q}(s)=K^{X_1}_{tau,q}(s)`: (TB) is an ordering-forgetting
ledger, not a support-saving estimate.  The genuine terminal residual is the
zero-free condition on the intermediate first-boundary scalars, made explicit
next.

## Terminal Flags Are Zero-Free Scalar Chains

Keep the notation of the stopping decomposition.  If
`C_h=D_h union {y_h}` lies in `K^{X_h}_{tau,|C_h|}(s)`, then

```text
H_{tau+1,|D_h|}(Delta_{X_h}s)ell_{D_h}
 = c_h (1,y_h,...,y_h^tau)                    (SC)
```

for the scalar

```text
c_h = H_{1,|D_h|}(Delta_{X_h}s)ell_{D_h}.
```

An ordered path `(C,(y_1,...,y_q))` is terminal if and only if

```text
c_1 c_2 ... c_q != 0.                         (ZF)
```

Proof: since `C_h` is active for `K^{X_h}`, the one-root deletion equations
force the first-boundary vector to have the root-marked form (SC).  The
stopping algorithm stops exactly when this whole vector is zero.  In the
root-marked form, that is equivalent to `c_h=0`.  Hence the path never stops
if and only if every scalar `c_h` is nonzero.

Consequently the true terminal object is a zero-free flag problem inside the
fixed-root support kernel: the support condition itself is just the ordinary
bottom root-difference equation, while terminality is the nonvanishing of
these explicit scalar cuts along the chosen order.

## Terminal Deletion Tree Recursion

The zero-free flag residual has an exact deletion-tree recursion.  For an
ordered fixed-root list `X` and an active core
`C in K^X_{tau,q}(s)`, define

```text
c_X(y;C) = H_{1,q-1}(Delta_X s)ell_{C\{y}},

NZ_X(C) = { y in C : c_X(y;C) != 0 }.
```

Let `T_X(C)` be the number of terminal ordered deletion flags starting from
`(X,C)`, with `T_X(empty)=1`.  Then

```text
T_X(C) = sum_{y in NZ_X(C)} T_{X,y}(C\{y}).       (DT)
```

Here `X,y` means that the fixed-root list is extended by appending `y`.  Proof:
a terminal flag has a unique first deleted root `y`.  By (ZF), this first step
is allowed exactly when `c_X(y;C)` is nonzero.  In that case the
root-marked identity (SC) says that the child core `C\{y}` lies in
`K^{X,y}_{tau,q-1}(s)`, and the remaining suffix of the flag is precisely a
terminal flag for this child.  The possible first roots are disjoint, giving
(DT).

Thus terminal multiplicity is exactly branching in the nonzero-edge deletion
tree.  If every vertex below `(X,C)` has at most one outgoing nonzero edge,
then `T_X(C)<=1`.  Equivalently, any core carrying two or more terminal
orderings contains a descendant `(X',C')` with

```text
#{ y in C' : H_{1,|C'|-1}(Delta_{X'}s)ell_{C'\{y}} != 0 } >= 2.   (BR)
```

This does not yet bound the terminal residual, but it localizes the remaining
M1 obstruction: after the first-zero ledger removes zero-boundary stops,
all residual multiplicity is concentrated on explicit branching vertices of
first-row scalar cuts inside fixed-root kernels.

## Branch Pairs Have Two-Mode Lower Boundaries

The branching vertices themselves have a lower-core normal form.  Suppose
`C in K^X_{tau,q}(s)` has two distinct nonzero exits `y,z in C`, and put
`R=C\{y,z}`.  Let

```text
g = H_{tau+2,|R|}(Delta_X s)ell_R
  = (g_0,...,g_{tau+1}).
```

Let `c_y=c_X(y;C)` and `c_z=c_X(z;C)` be the two nonzero exit scalars.  Then

```text
g_i = (c_y y^i - c_z z^i)/(y-z),      0<=i<=tau+1.      (TM)
```

Equivalently,

```text
H_{tau+2,|R|}(Delta_X s)ell_R
 =
 (c_y(1,y,...,y^{tau+1})
  - c_z(1,z,...,z^{tau+1}))/(y-z).
```

Proof: deleting `y` leaves the boundary core `R union {z}`, so (SC) gives

```text
g_{i+1}-z g_i = c_y y^i,       0<=i<=tau.
```

Deleting `z` similarly gives

```text
g_{i+1}-y g_i = c_z z^i,       0<=i<=tau.
```

Subtracting gives (TM) for `0<=i<=tau`; substituting the case `i=tau` back
into either boundary equation gives the final coordinate `g_{tau+1}`.

A branching pair is called productive if both child deletion trees have at
least one terminal completion.  Since two terminal flags with the same start
first diverge at a productive branch pair, any `T_X(C)>1` forces such a pair
somewhere below `(X,C)`.  Thus terminal multiplicity is now reduced one more
step: it is carried by productive two-mode lower-boundary packets (TM), not by
arbitrary branching in the deletion tree.

## Branch Vertices Are Sparse Mode Packets

The two-mode identity is the smallest case of a full branch-packet normal
form.  Let `Y` be any subset of `NZ_X(C)` with `m=|Y|>=2`, and put
`R=C\Y`.  Define

```text
g = H_{tau+m,|R|}(Delta_X s)ell_R.
```

For each `y in Y`, let

```text
d_y = product_{z in Y, z!=y} (y-z),
        a_y = c_X(y;C)/d_y.
```

Then the whole lower-boundary window is the sparse moment packet

```text
g_i = sum_{y in Y} a_y y^i,        0<=i<=tau+m-1.       (MP)
```

In particular, taking `Y=NZ_X(C)` turns every terminal branch vertex into an
explicit `m`-mode lower-boundary packet whose mode coefficients are all
nonzero.

Proof: for fixed `y in Y`, applying the locator of `Y\{y}` to `g` gives the
boundary vector for `C\{y}`.  By (SC) this is

```text
H_{tau+1,|C|-1}(Delta_X s)ell_{C\{y}}
  = c_X(y;C)(1,y,...,y^tau).
```

For each row `i`, the equations over all `y in Y` form a linear system for the
window `(g_i,...,g_{i+m-1})`.  The rows are the coefficient vectors of the
polynomials `prod_{z in Y,z!=y}(X-z)`.  These polynomials are a basis because
their evaluations on `Y` are diagonal with nonzero entries `d_y`.  The
Lagrange packet (MP) satisfies the system, hence by uniqueness it is the
actual window.  Sliding `i` from `0` to `tau` gives all coordinates
`0<=i<=tau+m-1`.

A full branch packet is productive if at least two of its modes lead to
terminal child completions.  The previous productive branch-pair statement is
therefore the two-mode shadow of a stronger fact: terminal multiflag mass is
carried by productive sparse mode packets inside lower fixed-root Hankel
kernels.

## Sparse Packets Have Rank Certificates

When the packet window is long enough, the mode count is detected by a single
Hankel minor.  In the notation of (MP), assume `m<=tau+1` and form

```text
M_Y = (g_{r+s})_{0<=r,s<m}.
```

Then

```text
det M_Y =
  (product_{y in Y} a_y)
  (product_{y<z in Y} (z-y)^2).                 (RC)
```

In particular `det M_Y != 0`, since all exit scalars are nonzero and the
roots in `Y` are distinct.

Proof: write `V=(y^r)_{0<=r<m, y in Y}` and
`A=diag(a_y)`.  The moment formula (MP) gives `M_Y=V A V^T`.  Taking
determinants gives (RC), because `det V` is the Vandermonde product.

Thus a visible terminal branch packet is not merely a formal sparse
representation: it carries a nonzero rank-`m` minor on the lower-boundary
sequence.  For the M1 route this isolates productive terminal multiplicity
inside determinant-nondegenerate sparse moment packets; any remaining bound
can now attack these rank certificates or show they lie in quotient-periodic
or tangent ledgers.

## Sparse Packets Peel Losslessly

The sparse packet also records every intermediate deletion inside the branch
vertex.  Let `E subset Y`, and let `ell_E=prod_{e in E}(X-e)`.  Applying this
locator to the packet (MP) gives

```text
H_{tau+m-|E|, |R|+|E|}(Delta_X s)ell_{R union E}
 =
 sum_{y in Y\E} a_y ell_E(y)(1,y,...,y^{tau+m-|E|-1}).       (PL)
```

Consequently, if `E` is a proper subset of `Y`, the peeled vector is nonzero:
the remaining modes have nonzero coefficients
`a_y ell_E(y)` and the first `|Y\E|` moment rows form an invertible
Vandermonde system.  If `E=Y`, the right side is empty and the peeled vector is
zero; this is exactly the active equation for the original core `C`.

Thus a terminal branch packet has no hidden premature zero-boundary collapse
along its internal mode set.  Every partial mode deletion preserves a
deterministic smaller sparse packet, and only deleting all modes gives the
annihilating locator.  This is the local "lossless frontier shift" promised by
the fixed-root filtration, now visible inside the terminal packet itself.

## Visible Packets Have Unique Minimal Annihilator

With one more visible moment, the packet determines its branch-mode locator.
Assume the packet (MP) is visible through `g_0,...,g_{2m-1}`.  The monic
degree-`m` annihilator

```text
P(X)=X^m+b_{m-1}X^{m-1}+...+b_0
```

is recovered by the nonsingular moment system

```text
sum_{h=0}^{m-1} b_h g_{r+h} = -g_{r+m},       0<=r<m.      (MA)
```

Moreover `P(X)=prod_{y in Y}(X-y)`, and no nonzero polynomial of degree
`<m` annihilates the visible packet.

Proof: the coefficient matrix in (MA) is the rank-certificate matrix `M_Y`,
so (RC) makes the solution unique.  The solution satisfies

```text
0 = sum_{h=0}^m p_h g_{r+h}
  = sum_{y in Y} a_y y^r P(y),       0<=r<m,
```

where `p_m=1`.  Since the Vandermonde matrix on `Y` is invertible and all
`a_y` are nonzero, `P(y)=0` for every `y in Y`.  Thus the monic degree-`m`
polynomial `P` is exactly the branch-mode locator.  The same rank certificate
also rules out a lower-degree annihilator: otherwise the first `m` shifted
moment columns would be linearly dependent.

This converts a visible productive terminal packet into a recoverable object:
its mode set is intrinsic to the lower-boundary moments, not auxiliary
branching data.

## The Boundary Moment Is Genuine

The previous recovery statement is sharp for the available terminal window.
For an `m`-mode branch packet at row level `tau`, the packet formula gives
only

```text
g_0,...,g_{tau+m-1}.
```

Thus every packet with `m<=tau` has the `2m` visible moments needed for (MA),
while a boundary packet with `m=tau+1` has exactly `2m-1` moments: enough for
the rank certificate (RC), but one moment short of intrinsic locator recovery.

This missing moment is not a bookkeeping artifact.  Suppose two `m`-mode
packets on supports `Y` and `Z`, with all amplitudes nonzero, have the same
moments `g_0,...,g_{2m-2}`.  If `Y` and `Z` meet, their difference is a
nonzero measure on at most `2m-1` distinct roots whose first `2m-1` moments
vanish.  The corresponding square Vandermonde matrix is invertible, so this
is impossible.  Hence any ambiguity at the `2m-1` moment boundary must be
between disjoint supports.

Conversely, the boundary ambiguity exists in general.  For any `2m` distinct
roots `W`, the `(2m-1) x 2m` Vandermonde matrix of moments
`0,...,2m-2` has a one-dimensional kernel.  No kernel coordinate can vanish,
since any `2m-1` columns form an invertible square Vandermonde matrix.  If
`W=Y disjoint_union Z` with `|Y|=|Z|=m`, this kernel relation gives nonzero
amplitudes on `Y` and on `Z` which produce identical first `2m-1` moments.
The next moment separates them, because the full `2m x 2m` Vandermonde matrix
is invertible.

More explicitly, put

```text
P_W(X)=prod_{w in W}(X-w),        omega_w=1/P_W'(w).
```

The unique relation is

```text
sum_{w in W} omega_w w^i=0,        0<=i<=2m-2.
```

Thus a packet on `Y` with amplitudes `a_y` has a disjoint `Z`-alias through
`W=Y disjoint_union Z` if and only if there is a scalar `mu != 0` such that

```text
a_y = mu omega_y        for every y in Y.
```

Then the alias amplitudes on `Z` are `-mu omega_z`.  This follows from the
one-dimensionality of the Vandermonde kernel, and gives a concrete
branch-amplitude test for the boundary obstruction.

For terminal branch packets this has an even more useful scalar-cut form.  In
(MP),

```text
a_y = c_X(y;C) / d_Y(y),
d_Y(y)=prod_{u in Y, u!=y} (y-u).
```

If `Z` is disjoint from `Y` and `ell_Z(X)=prod_{z in Z}(X-z)`, then

```text
P_{Y union Z}'(y)=d_Y(y) ell_Z(y).
```

Therefore the disjoint `Z`-alias condition is equivalent to

```text
c_X(y;C) ell_Z(y) = mu        for every y in Y.        (SF)
```

In words: a boundary alias is exactly a constant-product fit of the first-row
exit scalars against a candidate disjoint locator.  This cancels the internal
Vandermonde denominators of the true branch packet and leaves only the scalar
cuts produced by the deletion tree.  Thus the boundary endpoint is no longer a
generic Prony ambiguity; it is a finite squarefree-locator interpolation
problem for the explicit scalars `c_X(y;C)`.

The same Vandermonde argument gives a general fiber bound without assuming
`|H|=2m`.  Fix any domain `H` of size `n`, and consider the boundary moment
map

```text
Psi(Y,(a_y)) = (sum_{y in Y} a_y y^i)_{0<=i<=2m-2},
        |Y|=m,        a_y in F^*.
```

Inside any fiber of `Psi`, the supports are pairwise disjoint.  Indeed, two
different supports in the same fiber cannot meet, by the square Vandermonde
argument above; and once a support is fixed, its amplitudes are uniquely
recovered from the first `m` moments.  Hence every boundary fiber has size at
most

```text
floor(n/m).                                      (FB)
```

Equivalently, even before one classifies the disjoint aliases, the
`2m-1`-moment endpoint has only matching-type support ambiguity.  There is no
overlapping cluster or multiplicative support packet hidden at the boundary.

There is a particularly simple full-domain boundary specialization.  Suppose
the available mode universe is the whole root-of-unity domain

```text
H={x:x^n=1},        n=2m,
```

and `Z=H\Y`.  Then `P_H'(y)=n y^{-1}`, so the kernel weights are
`omega_y=y/n`.  The complementary alias exists if and only if

```text
a_y/y = constant        for every y in Y.       (RL)
```

Equivalently, the true packet amplitudes are root-linear:
`a_y=nu y` on `Y`, and the complementary alias has amplitudes `-nu z` on
`H\Y`.  Thus, in the full-domain boundary case, the remaining endpoint is not
even an arbitrary scalar-fit problem; it is exactly the root-linear amplitude
locus.

This gives a complete support-identifiability dichotomy in the full-domain
boundary case.  The first `2m-1` moments of an `m`-mode packet on `H` either:

1. determine the support `Y` uniquely among all domain `m`-sets; or
2. the amplitudes are root-linear, `a_y=nu y`, and the only other domain
   `m`-set giving the same visible moments is the complement `H\Y`, with
   amplitudes `-nu z`.

Indeed, any second support must be disjoint by the square Vandermonde
argument above.  Since `|H|=2m`, a disjoint `m`-support is necessarily
`H\Y`; the kernel-weight computation then gives exactly (RL).  Conversely
(RL) gives the complementary alias.  Once the support is unique, the
amplitudes are recovered from the first `m` moments by the square Vandermonde
matrix on that support.

Consequently the aliased endpoint is polynomial-sized for fixed `m`.  As
labeled packets `(Y,(a_y))`, the full-domain root-linear alias locus is

```text
{ (Y,nu) : Y subset H, |Y|=m, nu in F^*,
           a_y=nu y for y in Y },
```

so it has cardinality

```text
(|F|-1) binom(n,m).                              (AL)
```

The visible moment sequence identifies the unordered pair
`{(Y,nu),(H\Y,-nu)}`, so the number of distinct visible aliased sequences is

```text
(|F|-1) binom(n,m)/2
```

when `m>=1`.  This count is independent of arbitrary `m`-tuples of
amplitudes: the alias condition cuts the amplitude freedom from `(F^*)^m` down
to one scalar.  Thus, for fixed slack `m=tau+1`, the actual ambiguous
full-domain endpoint is already a polynomial ledger in the polynomial-field
window.

Equivalently, the full-domain boundary moment map has an exact fiber count.
Let

```text
Psi(Y,(a_y)) = (sum_{y in Y} a_y y^i)_{0<=i<=2m-2},
```

with `Y subset H`, `|Y|=m`, and all `a_y in F^*`.  Then every fiber of `Psi`
has size one except the root-linear complement pairs

```text
(Y, (nu y)_{y in Y})  <-->  (H\Y, (-nu z)_{z in H\Y}).
```

Therefore

```text
|im Psi|
 =
 ((|F|-1)^m - (|F|-1)) binom(n,m)
 + ((|F|-1) binom(n,m))/2.                    (BI)
```

In particular, for fixed `m` and `|F|=poly(n)`, the whole full-domain
boundary endpoint is polynomial-sized, not merely its aliased sublocus.  This
is the exact local closure available at the `2m-1` moment boundary: the
non-root-linear part is support-recoverable, and the root-linear part is a
half-sized complement-pair ledger.

For the `t=2` terminal audit this says exactly what the data show:
mode-size-`2` packets are locator-recoverable, while mode-size-`3` packets are
maximal-window boundary packets.  Therefore a proof of M1 cannot use rank
visibility alone to identify these boundary modes in complete generality; it
must either obtain one more moment from additional structure, charge possible
disjoint aliases, or exploit the special branch-amplitude constraints to bound
the boundary packet family directly.  The verifier now searches for
equal-size aliases in the `F_7^*`, mode-size-`3` boundary packets and checks
that any such alias would have to be disjoint, as the Vandermonde argument
predicts.  In the largest current audit, only `120` of the `4320` boundary
packets admit such an alias; the other `4200` are support-identifiable among
domain `3`-sets despite lacking the formal Prony recovery moment.  The same
audit checks (SF) directly: the constant-product scalar fits have exactly the
same `4200/120` histogram as the moment aliases.  Since this audit is also a
full-domain boundary case with `n=6=2m`, the root-linear test (RL) has the
same histogram: the `120` aliased packets are precisely the root-linear
amplitude packets.  The remaining `4200` boundary packets are support-unique.
The root-linear packets occupy all `binom(6,3)=20` supports with `6=|F|-1`
scalar multiples per support, exactly as (AL) predicts.  Thus the visible
full-domain endpoint has `4200+120/2=4260` distinct boundary moment sequences,
matching (BI).  The same audit checks the general matching-fiber bound (FB):
the boundary fiber-size histogram is `4200` fibers of size `1` and `120`
labeled packets lying in fibers of size `2`, with maximum fiber size `2`.

## Root-Marked Slice Is One Row

The zero-boundary subkernel in the fixed-root difference form is cut out by a
single additional Hankel row.  With the notation above,

```text
Z^x_{tau+1,j-1}(s)
 = { C in K^x_{tau,j-1}(s) : H_{1,j-1}(s)ell_C=0 },

B^x_{tau+1,j-1}(s)
 = { C in K^x_{tau,j-1}(s) : H_{1,j-1}(s)ell_C!=0 }.
```

Proof: membership in `K^x_{tau,j-1}(s)` is the recurrence

```text
c_{i+1}=x c_i,        0<=i<tau,
```

for the first-boundary coordinates
`c_i=sum_h (ell_C)_h s_{i+h}`.  Hence the whole boundary vector
`(c_0,...,c_tau)` vanishes if and only if its first coordinate `c_0` vanishes.
But `c_0=H_{1,j-1}(s)ell_C`.  Therefore the root-marked part is exactly the
complement of this single row inside the fixed-root difference kernel.

This is the rank-testable local target left by the same-slope packet
reduction: for each fixed root `x`, bound the squarefree support solutions of
`H_{tau,j-1}(Delta_x s)` not lying in the first-row subkernel
`H_{1,j-1}(s)`.

## Root-Marked Edge Descent

The one-row residual has the same additive one-exchange behavior.  Fix
`x in H` and suppose `j>=2`.  Let

```text
C_y = R union {y},        C_z = R union {z},        y != z,
```

be two distinct cores in `B^x_{tau+1,j-1}(s)`.  Then their common
`(j-2)`-core satisfies

```text
H_{tau+1,j-2}(Delta_x s)ell_R=0.              (RME)
```

Proof: by the fixed-root difference form, both `C_y` and `C_z` lie in the
active locator family for `H_{tau,j-1}(Delta_x s)`.  Applying the same
one-exchange subtraction as before to

```text
ell_{C_y}=(X-y)ell_R,        ell_{C_z}=(X-z)ell_R
```

gives `H_{tau+1,j-2}(Delta_x s)ell_R=0`.

Consequently, if `(B^x)^+` denotes the non-isolated vertices in the
one-exchange graph on `B^x_{tau+1,j-1}(s)` and

```text
E^x_{tau+1,j-2}(s)
 = { R subset H\{x} : |R|=j-2,
     R union {y}, R union {z} in B^x_{tau+1,j-1}(s)
     for some distinct y,z notin R union {x} },
```

then

```text
|(B^x)^+| <= (n-j+1) |E^x_{tau+1,j-2}(s)|,
```

and every `R in E^x_{tau+1,j-2}(s)` lies in the lower root-difference kernel
cut out by (RME).  Thus branching inside the root-marked residual is not a new
primitive source: it descends one row in the root-difference Hankel ladder.
Only isolated vertices of the one-row residual remain after these lower-core
charges.

## Isolated Vertices of the One-Row Residual

The isolated vertices left after (RME) again have an exact marked-boundary
criterion.  Assume `2<=j<=n-2`.  Let `C in B^x_{tau+1,j-1}(s)` and, for
`y in C`, put `R=C\{y}` and `d=Delta_x s`.  Write

```text
a_i = sum_h (ell_R)_h d_{i+h}.
```

Since `C=R union {y}` lies in the fixed-root difference kernel,

```text
a_{i+1}=y a_i,        0<=i<tau.
```

Then `C` is isolated in the one-exchange graph on `B^x_{tau+1,j-1}(s)` if and
only if, for every `y in C`,

```text
H_{tau+1,j-2}(Delta_x s)ell_{C\{y}} != 0.        (RI)
```

Proof: if the lower boundary vector above is nonzero, the equations
`a_{i+1}=z a_i` force any active extension through `R` to have `z=y`, so no
one-exchange neighbor of `C` occurs through `R`.  If the lower boundary vector
is zero, then every extension `R union {z}` lies in the root-difference kernel.
Inside this kernel the residual condition is the nonvanishing of the linear
row

```text
H_{1,j-1}(s)ell_{R union {z}}.
```

This row is not identically zero on available `z`, because it is nonzero at
`z=y`.  Since `j<=n-2`, there is an alternate available extension with this
row still nonzero.  Hence `C` has a residual neighbor through `R`.  This proves
(RI).

Define the second marked-boundary residual

```text
B^{x,2}_{tau+1,j-2}(s)
 = { (R,y) : R subset H\{x,y}, |R|=j-2,
     H_{tau+1,j-2}(Delta_x s)ell_R
       = a(1,y,...,y^tau), a!=0,
     R union {y} in B^x_{tau+1,j-1}(s) }.
```

If `Iso(B^x)` is the set of isolated vertices in the one-row residual graph,
then

```text
(j-1) |Iso(B^x)| <= |B^{x,2}_{tau+1,j-2}(s)|.
```

Indeed, every isolated residual core contributes its `j-1` nonzero deletion
boundaries, and the map `(C,y) -> (C\{y},y)` is injective.  Thus the residual
one-row slice has the same local split as the original same-slope support:
non-isolated mass descends to lower root-difference cores, while isolated mass
is a second marked-boundary object.

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

The same run checks the component ledger inequalities:

| field/domain | max nonzero edge cores | max nonzero lower-core witnesses | max nonisolated slack | max non-star component slack |
| --- | ---: | ---: | ---: | ---: |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 5 | 1 | 10 | 0 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 1 | 0 | 0 | 0 |

It also checks the isolated active locator criterion:

| field/domain | max nonzero isolated active locators | deletion zero-counts seen |
| --- | ---: | --- |
| `F_5`, `H=F_5^*`, `n=4,k=1,a=3,j=1` | 1 | `0,1` |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 2 | `0,1,2,3` |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 1 | `0,1,2` |
| `F_7`, `H=F_7^*`, `n=6,k=3,a=5,j=1` | 1 | `0,1` |

The marked-boundary ledger is also checked:

| field/domain | max nonzero marked boundaries | max marked-boundary slack |
| --- | ---: | ---: |
| `F_5`, `H=F_5^*`, `n=4,k=1,a=3,j=1` | 1 | 0 |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 10 | 10 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 5 | 5 |
| `F_7`, `H=F_7^*`, `n=6,k=3,a=5,j=1` | 1 | 0 |

The first-boundary incidence identity (FI) is checked in the same scan.  In
particular, the zero first-boundary cores coincide exactly with the active
edge cores:

| field/domain | max nonzero zero-boundary cores | max nonzero fixed-root active | residual lower cores | isolated residual | second boundaries | incidence defect | rootwise defect | root-difference defect | single-row defect |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `F_5`, `H=F_5^*`, `n=4,k=1,a=3,j=1` | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| `F_7`, `H=F_7^*`, `n=6,k=1,a=3,j=3` | 5 | 10 | 5 | 6 | 12 | 0 | 0 | 0 | 0 |
| `F_7`, `H=F_7^*`, `n=6,k=2,a=4,j=2` | 1 | 5 | 1 | 2 | 2 | 0 | 0 | 0 | 0 |
| `F_7`, `H=F_7^*`, `n=6,k=3,a=5,j=1` | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

The same run checks the iterated fixed-root identity (IDX) with zero defects;
the largest listed case, `F_7`, `k=1`, `j=3`, performs `2352980` direct
locator-versus-iterated-difference row checks up to chain length `3`.
It also checks the recursive fixed-chain boundary identity (RFI) with zero
defects; the same largest case performs `352947` rung identities up to chain
length `2`, with maximum nonzero rung counts `10` active cores, `5` zero
boundary cores, and `4` root-marked boundaries.
The verifier additionally checks the set-level fixed-root filtration identity
(FIS) behind this count; in the same largest case it checks `61740` incidence
pairs, with maximum nonzero fixed-rung incidence fiber count `20` and zero
defects.
Finally, it audits the induced first-zero stopping decomposition for ordered
fixed-root deletion paths.  In the largest listed case it checks `102900`
ordered paths with zero defects: `14700` stop first at depth `1`, `10080` at
depth `2`, `4320` at depth `3`, and `73800` reach the terminal bottom
difference condition.  Among nonzero syndromes the largest path count is
`150`, with at most `30` terminal paths.
The same audit verifies the ordered path partition (OZ): in the largest case
the `102900` paths split as `29100` first-zero stops and `73800` terminal
paths, with zero partition defect.  Among nonzero syndromes the maximum
first-zero stop count is `140`.
It also audits the terminal bottom-support reduction (TB): in the largest
case the `73800` terminal paths reduce to `37080` local bottom-support
instances with total factorial capacity `73800`, maximum nonzero local bottom
support count `2`, and zero slack.
The same audit checks the zero-free scalar-chain criterion (ZF); the largest
case checks `174600` nonzero scalar steps, with maximum nonzero per-syndrome
step count `66`.
It also checks the deletion-tree recursion (DT) against the explicit path
enumeration.  In the largest listed case it audits `48020` active starting
cores with zero recursion defects; it finds `34560` branching vertices and
`19440` multiflag starting cores in the audited local trees.  Among nonzero
syndromes the maximum terminal-tree count is `6`, the maximum number of
branching vertices in one such tree is `4`, and at most `2` starting cores in
one audit have more than one terminal ordering.
The same audit verifies the branch-pair two-mode identity (TM).  In the
largest case it checks `43200` branch pairs with zero defects, of which
`41040` are productive branch pairs.  Among nonzero syndromes the maximum
number of branch pairs in one terminal tree is `6`, and all six can be
productive.
It also verifies the full branch-packet identity (MP).  In the largest case
it checks `34560` branch mode packets with zero defects: `30240` have mode
size `2` and `4320` have mode size `3`.  Of these, `32400` are productive
mode packets.  Among nonzero syndromes the maximum mode size is `3`, and one
terminal tree contains at most `4` mode packets, all of which can be
productive.
The rank-certificate formula (RC) is checked on the same packets.  In the
largest case all `34560` mode packets have enough visible moments for the
nonzero determinant check; the rank sizes are again `30240` of size `2` and
`4320` of size `3`, and all `32400` productive packets pass the determinant
certificate.
The lossless peeling identity (PL) is also checked on every nonempty subset of
each branch mode set.  In the largest case this gives `120960` peeling checks:
`73440` peel one mode, `43200` peel two modes, and `4320` peel all three
modes.  The productive branch packets account for `114480` of these checks.
The minimal-annihilator recovery (MA) is checked whenever `2m` moments are
visible.  In the largest case this recovers the locator for all `30240`
mode-size-`2` packets, including all `28080` productive size-`2` packets; the
mode-size-`3` packets need one additional moment beyond the current `t=2`
window.  The boundary alias search checks all `4320` size-`3` packets:
`4200` have no equal-size visible alias, while `120` have one disjoint alias
with the kernel-weight amplitude profile above.

The `F_7,k=2,j=2` scan is the first exact top-packet check in this file.  It
finds twenty top triangles, all on the zero combined syndrome.  This is not an
asymptotic claim, but it is a useful falsification check: in the smallest
genuine top case, nonzero same-slope triangles are already star/root-slice
events, while full top events are confined to the global-codeword/tangent
ledger.

These are small exact checks, not asymptotic evidence.  Their role is to make
the first `t=2` collision charges reproducible before moving to larger packet
scans and variable-line components.
