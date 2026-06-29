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

## Anchored Packets Reconstruct Branch Scalars

The packet label has no hidden multiplicity at a fixed anchor.  Fix the
fixed-root chain `X`, the lower core `R`, and the full branch mode set
`Y=NZ_X(C)` with `C=R union Y`.  If the anchored packet label

```text
(R, Y, (a_y)_{y in Y})
```

is known, then it reconstructs the branch vertex and all outgoing first-row
scalars:

```text
C=R union Y,
c_X(y;C)=a_y prod_{z in Y, z!=y}(y-z).          (AR)
```

Proof: the identity is just the definition of the packet amplitudes in (MP),
`a_y=c_X(y;C)/d_y`, where
`d_y=prod_{z in Y,z!=y}(y-z)`.  Since the roots in `Y` are distinct, all
`d_y` are nonzero.  Thus the anchored packet label recovers both the branch
core `C` and each nonzero scalar cut.

Consequently repeated production of a visible packet label cannot be explained
by local ambiguity at one fixed lower core.  Any remaining multiplicity must
come from different anchors `(X,R)` producing the same label, or from global
relations between those anchors.  This is the next object that must be charged
to quotient-periodic, tangent, or lower-core ledgers.

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

This immediately gives a local endpoint ledger.  Over a finite field `F`, the
number of labeled nonzero `m`-mode sparse packets on `H` is

```text
(|F|-1)^m binom(n,m).                            (LC)
```

Every visible boundary moment sequence has at most `floor(n/m)` such labels
above it by (FB).  Hence the boundary image size lies between

```text
ceil((|F|-1)^m binom(n,m) / floor(n/m))
```

and the labeled count (LC).  In particular, for fixed `m=tau+1` and
`|F|=poly(n)`, the entire boundary sparse-packet endpoint is polynomial-sized.
This does not by itself count how often a terminal deletion tree can produce a
given packet; rather, it says that once terminal branching has been reduced to
visible boundary sparse packets, the packet type itself has only polynomially
many labels and matching-bounded moment fibers.

Combining this with the `2m`-moment recovery theorem gives the local terminal
packet-type ledger.  At row level `tau`, every terminal branch packet has a
visible label in one of the following forms:

1. `2<=m<=tau`: the first `2m` moments are visible, so the mode locator and
   amplitudes are intrinsic to the lower-boundary vector;
2. `m=tau+1`: the boundary endpoint has matching-type fibers of size at most
   `floor(n/m)`, and in the full-domain case its only nontrivial fibers are
   the root-linear complement pairs described below.

Thus, for fixed `tau`, the ambient labeled packet space for all visible
terminal branch packets has size at most

```text
sum_{m=2}^{tau+1} (|F|-1)^m binom(n,m).          (TL)
```

If `|F|=poly(n)`, this is polynomial in `n`.  This is the local packet-type
closure supplied by the terminal sparse-packet analysis: it rules out a new
super-polynomial family of visible sparse packet labels.  The remaining global
M1 work is to control how many times deletion trees can produce these packet
labels, or to charge repeated production to quotient-periodic, tangent, or
lower-core ledgers.

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

## Visible Packet Collisions Are Scalar Collisions

The preceding endpoint analysis turns repeated production into a concrete
scalar-cut problem.  Consider two terminal branch vertices, possibly with
different anchors `(X,R)` and `(X',R')`, producing sparse packets on mode
supports `Y` and `Y'` of the same size `m`.  Write

```text
C=R union Y,        C'=R' union Y',
a_y=c_X(y;C)/d_Y(y),
a'_{y}=c_{X'}(y;C')/d_Y(y),
```

when the support is the same.  If the visible endpoint recovers the support
(`m<=tau`, or the boundary endpoint is support-unique), then a collision of
visible labels is equivalent to

```text
Y=Y',
c_X(y;C)=c_{X'}(y;C')        for every y in Y.       (VC)
```

Indeed the Vandermonde recovery gives the same amplitudes, and the
denominators `d_Y(y)` depend only on the common support.  Conversely (VC)
obviously gives the same packet.

At the maximal boundary `m=tau+1`, there is only one extra collision type:
the disjoint alias already classified above.  Thus any visible collision is
either the same-support scalar equality (VC), or else `Y` and `Y'` are
disjoint and the scalar cuts satisfy the constant-product fit

```text
c_X(y;C) ell_{Y'}(y)=mu        for every y in Y,
```

with the symmetric alias amplitudes on `Y'`.  In the full-domain case
`n=2m`, this exceptional branch is exactly the root-linear scalar condition

```text
c_X(y;C)/(y d_Y(y)) = constant        for every y in Y.
```

Therefore the remaining production problem is not an uncontrolled packet
ambiguity.  It is the problem of bounding same-support scalar-cut collisions
between distinct anchors, plus the already isolated boundary disjoint-alias
ledger.

The verifier now audits this production question directly for visible packet
labels, syndrome by syndrome.  In the largest `F_7^*` audit, all `34560`
visible terminal packet productions have singleton production fibers; the
productive subaudit has all `32400` productive labels singleton as well.  Thus
the current finite data contain no same-syndrome repeated production of an
unanchored visible sparse-packet label.

## Same-Support Collisions Drop to Anchor-Base Kernels

The same-support scalar collision has one more useful normal form.  Collapse
the fixed roots and the lower core into the anchor base

```text
A=X union R,        d=|A|.
```

By the iterated root-difference identity,

```text
H_{tau+m,d}(s) ell_A
 = H_{tau+m,|R|}(Delta_X s) ell_R
 = (sum_{y in Y} a_y y^i)_{0<=i<=tau+m-1}.       (AB)
```

Thus the visible sparse packet is not merely attached to the branch vertex;
it is the direct Hankel image of the collapsed anchor base `A`.

Now suppose two same-size branch packets with the same visible moment sequence
have collapsed anchor bases `A` and `A'` of the same degree `d`.  Then (AB)
gives

```text
H_{tau+m,d}(s)(ell_A-ell_{A'})=0.                (KD)
```

If `A!=A'`, the polynomial `ell_A-ell_{A'}` is nonzero and has degree `<d`,
because the two split locators are monic of degree `d`.  Therefore every
genuine distinct-anchor-base production collision gives a nonzero lower-degree
Hankel-kernel vector.  Equivalently, the split-anchor map

```text
A |-> H_{tau+m,d}(s) ell_A
```

is injective on the relevant split anchors unless the lower polynomial kernel
`ker H_{tau+m,d-1}(s)` contains one of these locator differences.

This is the desired localization: repeated visible production is now either

1. a same collapsed anchor base, hence an ordering/fixed-root split issue
   rather than a new packet image;
2. a distinct-anchor-base collision charged to the lower-degree kernel (KD);
3. at the maximal boundary, the disjoint alias scalar-fit ledger already
   isolated above.

The verifier checks (AB) for every terminal packet.  In the largest `F_7^*`
audit this gives `34560` anchor-base image checks, including all `32400`
productive packets.  Since the visible production fibers are singleton in the
current audit, no nontrivial anchor-base kernel pairs appear there; if they do
appear in a later scan, the verifier checks (KD) directly.

## Anchor-Base Exchange Distance Charges

The lower-degree kernel vector in (KD) has an exchange-distance refinement.
Let two collapsed anchor bases of the same size be

```text
A=I union U,        A'=I union V,
```

where `I=A cap A'`, `|U|=|V|=h`, and `U cap V=empty`.  Then

```text
ell_A-ell_A' = ell_I(ell_U-ell_V),              (ED)
```

and `ell_U-ell_V` has degree `<h` because the degree-`h` leading terms
cancel.  Therefore an exchange-distance `h` production collision gives a
structured lower kernel vector

```text
H_{tau+m,|I|+h}(s) ell_I(ell_U-ell_V)=0,
        deg(ell_U-ell_V)<h.                    (EK)
```

In particular, the one-exchange case `h=1` is completely charged to the
common anchor core:

```text
ell_U-ell_V = v-u != 0,
H_{tau+m,|I|}(s) ell_I=0.                      (OE)
```

Thus an adjacent collapsed-anchor collision cannot be a new packet-producing
mechanism.  It is already a lower-core Hankel-kernel event at the common
anchor base.  Higher exchange distances are similarly bounded-degree
balanced-difference kernel events over the common anchor core; they are the
next natural ledger if singleton production fails in larger scans.

The verifier now records the one-exchange common-core checks around produced
packets.  In the current `t=2` branch audits, all nontrivial collapsed anchor
bases have size at most one, so the one-exchange refinement exhausts possible
distinct-anchor-base collisions in these packets.  In the largest `F_7^*`
case it checks `30240` one-exchange common cores, including all `28080`
productive size-`2` packets, and finds no lower-core kernel hits.  Thus the
current finite packets have neither repeated visible labels nor the adjacent
anchor-base kernel event that would make such a repetition possible at this
anchor-base size.

## Anchor-Base Packets Are Split-Support Certificates

The anchor-base packet identity is reversible.  Let `A` and `Y` be disjoint
domain sets, `m=|Y|`, and suppose

```text
g=H_{tau+m,|A|}(s)ell_A,
g_i=sum_{y in Y} a_y y^i        (0<=i<=tau+m-1),
a_y != 0.
```

Then the total split support `S=A union Y` is active:

```text
H_{tau,|S|}(s)ell_S=0.                          (SS)
```

Moreover every packet mode is a nonzero root-marked boundary of the split
support.  If `d_y=prod_{z in Y,z!=y}(y-z)` and
`c_y=a_y d_y`, then

```text
H_{tau+1,|S|-1}(s)ell_{S\{y}}
  = c_y(1,y,...,y^tau),       c_y != 0.          (SB)
```

Proof: applying `ell_Y` to the sparse moment sequence kills every geometric
mode, giving (SS).  Applying `ell_{Y\{y}}` kills all modes except `y` and
multiplies the remaining one by `d_y`, giving (SB).  The nonzero amplitude
and distinct roots make `c_y` nonzero.

Thus a visible terminal packet can be studied without reference to the
deletion history: it is exactly a split support `A union Y` whose packet modes
are nonzero root-marked exits, together with the sparse moment amplitudes.
The earlier deletion-tree construction proves that terminal branch vertices
produce such split-support certificates; this converse shows that bounding
these certificates is a direct M1 packing target.

The verifier checks (SS) and (SB) for every produced packet.  In the largest
`F_7^*` audit, this gives `34560` split-support checks and `73440`
root-marked split-boundary checks; the productive subaudit contributes
`32400` split supports and `69120` split-boundary checks.

## Root-Marked Split Supports Reconstruct Packets

Conversely, the split-support data reconstructs the packet.  Let `A` and `Y`
be disjoint, `S=A union Y`, and suppose

```text
H_{tau,|S|}(s)ell_S=0,
H_{tau+1,|S|-1}(s)ell_{S\{y}}
  = c_y(1,y,...,y^tau),        c_y != 0
```

for every `y in Y`.  Put

```text
d_y=prod_{z in Y,z!=y}(y-z),        a_y=c_y/d_y.
```

Then the anchor-base vector is exactly the sparse packet

```text
H_{tau+m,|A|}(s)ell_A
  = (sum_{y in Y} a_y y^i)_{0<=i<=tau+m-1}.       (EQ)
```

Proof: applying `ell_{Y\{y}}` to `H(s)ell_A` gives the displayed
root-marked boundary for `S\{y}`.  For each row, these equations form the same
diagonal Lagrange system used in (MP), whose unique solution is the sparse
moment packet with amplitudes `a_y=c_y/d_y`.

Thus the intrinsic object is an equivalence:

```text
sparse anchor-base packet
<-> active split support plus nonzero root-marked selected modes.
```

The verifier checks this roundtrip for every produced packet.  In the largest
`F_7^*` audit, this gives `34560` packet-reconstruction roundtrips, with
`32400` productive roundtrips.

## Total Split Supports Factor Through Marked Exits

The split-support equivalence has a useful fixed-total-support form.  Fix an
active total support `S`; that is,

```text
H_{tau,|S|}(s)ell_S=0.
```

For each `x in S`, write

```text
H_{tau+1,|S|-1}(s)ell_{S\{x}}
  = b_x(S)(1,x,...,x^tau).
```

This scalar is well-defined because `(X-x)ell_{S\{x}}=ell_S`, so the boundary
vector obeys the geometric recurrence with ratio `x`.  Let

```text
M(S)={x in S : b_x(S) != 0}
```

be the marked exits of `S`.

Then the split-support certificates with total support `S` and mode size `m`
are exactly the choices of an `m`-subset `Y subset M(S)`.  For such a choice,
put `A=S\Y` and

```text
d_Y(y)=prod_{z in Y,z!=y}(y-z),        a_y=b_y(S)/d_Y(y).
```

The Lagrange reconstruction gives

```text
H_{tau+m,|A|}(s)ell_A
 = (sum_{y in Y} a_y y^i)_{0<=i<=tau+m-1}.
```

Conversely, every split-support certificate over total support `S=A union Y`
uses only marked exits `Y subset M(S)`, and the amplitudes are forced by the
same formula.  Hence, for fixed `S`, the mode-size `m` certificate fiber has
capacity

```text
binom(|M(S)|,m).                              (MS)
```

This separates two different multiplicities.  Anchor choices inside one
active split support are not arbitrary: they are just choices of marked exits.
The remaining global M1 problem is therefore to bound or classify active
supports with many marked exits, and then to count how many such supports can
occur after quotient-periodic, tangent, and lower-core charges.

The verifier audits this factorization for produced split-support packets and
also reconstructs every marked subset of every produced total support.  In the
largest `F_7^*` audit, `25920` total-support fibers carry `34560` labels, the
maximum fiber size is `3`, and it checks `60480` marked-subset
factorizations.  The productive subaudit has `23760` fibers carrying `32400`
labels, maximum fiber size `3`, and `58320` marked-subset factorizations.  In
both audits the maximum number of marked exits on a produced total support is
`3`.

## Marked Exits Form a Lossless Cube

The preceding fixed-`S` factorization applies simultaneously to all marked
exits.  Let

```text
M=M(S)={x in S : b_x(S) != 0}.
```

For every nonempty `Y subset M`, put `A_Y=S\Y` and

```text
d_Y(y)=prod_{z in Y,z!=y}(y-z),        a_y=b_y(S)/d_Y(y).
```

Then

```text
H_{tau+|Y|,|A_Y|}(s)ell_{A_Y}
 = (sum_{y in Y} a_y y^i)_{0<=i<=tau+|Y|-1}.       (MC)
```

In particular every nonempty face is nonzero: the first `|Y|` rows form an
invertible Vandermonde system on `Y`, and all amplitudes `a_y` are nonzero.
Taking `Y=M` gives one sparse packet over the unmarked core `S\M`; absorbing a
proper subset of `M` gives another nonzero face, while absorbing all of `M`
returns the active equation `H_{tau,|S|}(s)ell_S=0`.

Thus an active total support with `r` marked exits contains a canonical
zero-free `r`-cube of sparse packet faces.  Large marked-exit supports are not
merely many unrelated anchor choices; they are high-dimensional zero-free
frontier cubes.  This is the next natural object for M1: quotient-periodic,
tangent, lower-core, or aperiodic input must bound such cubes or classify the
supports that carry them.

The verifier audits this full marked-exit cube for produced total supports,
including singleton faces that need not appear as terminal branch packets.  In
the largest `F_7^*` audit, it checks `21600` produced total supports and
`133920` nonzero marked-exit faces, with `112320` full marked-exit orderings
and maximum marked count `3`.  The productive subaudit checks `19440`
supports and `127440` nonzero faces, with `108000` orderings and the same
maximum marked count.

## Canonical Unmarked Cores Have Matching-Bounded Fibers

The marked-exit cube gives a canonical anchor for an active total support:

```text
U(S)=S\M(S).
```

Fix an unmarked core `U` and an integer `r`.  Any active total support `S`
with `U(S)=U` and `|M(S)|=r` gives, by the full marked face of (MC), an
`r`-sparse representation of the one fixed vector

```text
g_U=H_{tau+r,|U|}(s)ell_U
```

on the available domain `H\U`, with support `M(S)` and all amplitudes
nonzero.  Conversely, the full marked support is forced by such a
representation together with the requirement that the displayed support is
exactly the nonzero marked-exit set.

Therefore the same sparse-moment uniqueness applies to canonical marked-core
fibers.  If `r<=tau`, the first `2r` moments of `g_U` recover the marked
locator and amplitudes uniquely.  If `r=tau+1`, two different marked supports
over the same unmarked core are disjoint, and the fiber size is at most

```text
floor((n-|U|)/r).                              (UM)
```

Thus repeated large marked-exit supports over one canonical unmarked core are
again only a boundary matching phenomenon.  The remaining global task is to
count the unmarked cores that can carry such cubes, not to control arbitrary
overlapping marked-support clusters over a fixed core.

The verifier audits these canonical marked-core fibers for produced total
supports.  In the largest `F_7^*` audit, `21540` marked-core fibers carry
`21600` full marked supports, with maximum fiber size `2`.  The productive
subaudit has `19380` fibers carrying `19440` full marked supports, again with
maximum fiber size `2`.

## Unmarked Roots Descend as a Zero Cube

The complement of the marked exits is not inert; it is exactly a zero-boundary
descent object.  Let `S` be active and let

```text
U=U(S)=S\M(S).
```

For every `u in U`, the definition of unmarked says

```text
H_{tau+1,|S|-1}(s)ell_{S\{u}}=0.
```

Now fix a nonempty subset `E subset U` and write `P=ell_{S\E}`.  For each
`u in E`,

```text
ell_{S\{u}} = P ell_{E\{u}}.
```

The polynomials `ell_{E\{u}}`, for `u in E`, form a basis of all polynomials
of degree `<|E|`.  Hence the displayed one-deletion zero identities imply

```text
H_{tau+1,|S|-|E|}(s) P Q = 0
        for every Q with deg Q < |E|.
```

Taking `Q=1,X,...,X^{|E|-1}` gives consecutive zero rows, and therefore

```text
H_{tau+|E|,|S|-|E|}(s)ell_{S\E}=0.             (UZ)
```

Thus every active total support splits into two canonical cubes: the marked
exits give nonzero sparse packet faces, while the unmarked roots give zero
descent faces into deeper Hankel ledgers.  This is the structural reason that
unmarked mass should be charged to lower-core/root-slice ledgers rather than
counted as a new packet-producing source.

The verifier audits (UZ) for every nonempty subset of unmarked roots in every
produced total support.  In the largest `F_7^*` audit, it checks `21600`
produced total supports and `4320` unmarked zero faces, with maximum unmarked
count `1`.  The productive subaudit checks `19440` supports and `2160`
unmarked zero faces, again with maximum unmarked count `1`.

## Mixed Marked-Unmarked Faces Are Lossless

The marked and unmarked cubes are compatible.  Let `E subset U(S)` and
`Y subset M(S)` be nonempty.  Put

```text
A_{E,Y}=S\(E union Y),        ell_E(X)=prod_{e in E}(X-e).
```

First delete the unmarked set `E`.  By (UZ), `S\E` is active at row
`tau+|E|`.  For `y in M(S)`, the boundary of `S\E` at `y` is still a nonzero
geometric vector.  Indeed, if

```text
H_{tau+|E|+1,|A_{E,{y}}|}(s)ell_{A_{E,{y}}}
  = c_{E,y}(1,y,...,y^{tau+|E|}),
```

then multiplying by `ell_E` recovers the original marked boundary:

```text
c_{E,y} ell_E(y)=b_y(S).
```

Since `E` is disjoint from `M(S)`, `ell_E(y) != 0`, so

```text
c_{E,y}=b_y(S)/ell_E(y) != 0.
```

Applying the marked-exit reconstruction inside the active support `S\E` gives

```text
H_{tau+|E|+|Y|,|A_{E,Y}|}(s)ell_{A_{E,Y}}
 = (sum_{y in Y}
      b_y(S) y^i / (ell_E(y) prod_{z in Y,z!=y}(y-z)))
     _{0<=i<=tau+|E|+|Y|-1}.                 (MZ)
```

The right side is nonzero by the Vandermonde minor on `Y`.  Thus deleting
unmarked roots shifts the row depth additively and only rescales the marked
packet amplitudes; it does not create a multiplicative loss or destroy marked
faces.  The full split-support object is a two-color cube: unmarked directions
are zero descents, marked directions are nonzero sparse packets, and mixed
faces are the same packets after the exact zero-depth shift.

The verifier audits (MZ) for every produced total support, every nonempty
unmarked subset, and every nonempty marked subset.  In the largest `F_7^*`
audit, it checks `12960` mixed marked-unmarked faces, with maximum deleted
unmarked count `1`.  The productive subaudit checks `6480` mixed faces.

## Unmarked Deletion Preserves the Marked Frontier

The two-color cube has an exact frontier-shift invariant.  Let
`E subset U(S)` and put `S_E=S\E`.  Then `S_E` is active at row
`tau+|E|` by (UZ).  Its marked exits are exactly the original marked exits:

```text
M_{tau+|E|}(S_E)=M(S).
```

Indeed, for `y in M(S)` the mixed-face calculation gives the new boundary
scalar

```text
b^E_y=b_y(S)/ell_E(y) != 0.
```

For a remaining unmarked root `u in U(S)\E`, applying (UZ) to
`E union {u}` gives

```text
H_{tau+|E|+1,|S_E|-1}(s)ell_{S_E\{u}}=0,
```

so `u` stays unmarked.  Thus deleting unmarked roots neither creates new
marked exits nor loses old ones; it only shifts the row depth by `|E|` and
rescales the marked boundary scalars.

This is the local additivity statement needed by the M1 route.  A chain of
unmarked deletions consumes one Hankel row per deleted root, but it does not
restart a new packet problem at each rung.  The nonzero frontier is preserved
exactly until one deliberately deletes marked exits, where the sparse packet
faces above apply.

The verifier audits this shifted marking identity root by root.  In the
largest `F_7^*` audit, it checks `4320` shifted supports and `8640` shifted
boundary roots after unmarked deletions.  The productive subaudit checks
`2160` shifted supports and `4320` shifted boundary roots.

## Two-Color Face Classification

The preceding lemmas combine into one normal form for every face of the
split-support cube.  Let `S` be active, let

```text
M=M(S),        U=U(S)=S\M,
```

and choose arbitrary subsets `E subset U` and `Y subset M`.  Put

```text
A_{E,Y}=S\(E union Y),        ell_E(X)=prod_{e in E}(X-e).
```

Then the face

```text
F_{E,Y}
 = H_{tau+|E|+|Y|,|A_{E,Y}|}(s)ell_{A_{E,Y}}
```

is classified exactly as follows.

If `Y` is empty, then

```text
F_{E,empty}=0.                                (TC0)
```

This is the original active equation when `E` is empty, and it is the
unmarked zero descent (UZ) when `E` is nonempty.

If `Y` is nonempty, then

```text
F_{E,Y}
 = (sum_{y in Y}
      b_y(S)y^i / (ell_E(y) prod_{z in Y,z!=y}(y-z)))
     _{0<=i<=tau+|E|+|Y|-1}.                 (TC1)
```

In particular `F_{E,Y}` is nonzero.  The nonzero assertion follows from the
first `|Y|` rows and the Vandermonde matrix on `Y`, since all displayed
amplitudes are nonzero.

Thus a split support has no hidden internal face type.  Every face is either
a zero descent obtained by deleting only unmarked roots, or a nonzero sparse
packet on the deleted marked roots after an exact additive row shift.  This
is the local object one wants for M1: a deletion path through unmarked roots
does not repeatedly reintroduce a packing problem, and the only packing
frontier is the preserved marked sparse-packet frontier.

The verifier audits the three pieces of this classification directly:
`133920` marked/nonzero faces, `4320` unmarked zero faces, and `12960` mixed
faces in the largest `F_7^*` audit, together with the shifted-frontier root
checks above.

## Canonical Core Closure Criterion

The two-color classification turns the remaining local counting problem into
a canonical-core ledger.  For `1<=m<=tau+1`, let
`Cert_m^{<=tau+1}(s)` be the set of split-support certificates of mode size
`m` whose total active support `S` has at most `tau+1` marked exits.  Thus a
certificate is equivalently a pair `(S,Y)` with

```text
Y subset M(S),        |Y|=m,        |M(S)|<=tau+1,
```

with the amplitudes forced by the marked-exit formula.  For `r>=0`, define
the canonical core ledger

```text
Core_r(s)
 = { U : U=U(S)=S\M(S) for some active S with |M(S)|=r }.
```

Then

```text
|Cert_m^{<=tau+1}(s)|
 <= sum_{r=m}^{tau} binom(r,m) |Core_r(s)|
    + binom(tau+1,m)
      sum_{U in Core_{tau+1}(s)} floor((n-|U|)/(tau+1)).        (CC)
```

Proof: group certificates by the canonical unmarked core `U` and the marked
count `r=|M(S)|`.  For a fixed active support `S`, the fixed-total-support
factorization gives exactly `binom(r,m)` mode-size `m` certificates.  If
`r<=tau`, the canonical marked-core fiber theorem says that a fixed `U`
supports at most one full marked support `S`, because the full marked face is
an `r`-sparse representation visible through `2r` moments.  If `r=tau+1`,
the boundary fiber over `U` is a disjoint matching, hence has size at most
`floor((n-|U|)/(tau+1))`.  Summing these two cases proves (CC).

Consequently, for fixed `tau`, the split-support packet family with marked
frontier size at most `tau+1` is polynomial once the canonical core ledgers
`Core_r(s)` are polynomial.  More explicitly, if
`|Core_r(s)|<=n^B` for all `r<=tau+1`, then (CC) gives

```text
|Cert_m^{<=tau+1}(s)| <= O_tau(n^{B+1}).
```

Thus this local branch of M1 has a clean closure target: prove that the
canonical unmarked cores are already charged to lower-core, quotient-periodic,
tangent, or aperiodic ledgers.  Any remaining super-polynomial split-support
obstruction must either create too many such canonical cores or produce active
supports with more than `tau+1` marked exits; it cannot come from repeated
internal faces of the same split-support cube.

## Canonical Core Roots Give Simple-Pole Packet Lifts

The canonical core ledger has more structure than the counting statement
above records.  Let `S` be active, let

```text
M=M(S),        U=U(S),        r=|M|>=1,
```

and write

```text
d_M(y)=prod_{z in M, z!=y}(y-z),
        a_y=b_y(S)/d_M(y).
```

The full marked face over the canonical core is

```text
H_{tau+r,|U|}(s)ell_U
 = (sum_{y in M} a_y y^i)_{0<=i<=tau+r-1}.       (CP0)
```

Moreover every unmarked core root `u in U` gives a one-row longer
simple-pole lift of the same packet:

```text
H_{tau+r+1,|U|-1}(s)ell_{U\{u}}
 = (sum_{y in M} a_y y^i/(y-u))_{0<=i<=tau+r}.   (CP1)
```

Proof: (CP0) is the marked-exit cube with `Y=M`.  For (CP1), apply the mixed
marked-unmarked face formula with `E={u}` and `Y=M`.  Since `u` is unmarked,
the row depth increases by one, and since `u` is disjoint from `M`, the
marked amplitudes are rescaled by the nonzero factors `(y-u)^{-1}`.

Thus a canonical unmarked core is not merely a support carrying an
`r`-sparse packet.  Every root of the core imposes a compatible simple-pole
transform of that packet with one extra visible moment.  This gives a sharper
M1 target for the `Core_r(s)` ledgers: after quotient-periodic and tangent
cores are removed, prove that there are only polynomially many supports `U`
for which all of these simultaneous simple-pole packet lifts can hold.

The verifier now checks this directly for every produced total split support.
In the largest `F_7^*` audit, it checks `21600` full canonical-core packets
and `4320` simple-pole lifts; the productive subaudit checks `19440` packets
and `2160` lifts.

## Nonempty Boundary Cores Have Unique Marked Frontiers

The simple-pole lift removes the only matching ambiguity left in the
canonical marked-core fiber theorem, except when the unmarked core is empty.
Assume `r=tau+1` and fix a nonempty canonical unmarked core `U`.  If
`u in U`, then (CP1) gives the fixed vector

```text
V_u=H_{2r,|U|-1}(s)ell_{U\{u}}
```

as an `r`-sparse moment packet on the marked support `M`, with amplitudes
`a_y/(y-u)`.  The displayed window has exactly `2r` moments, and all
amplitudes are nonzero.  Hence the Prony annihilator argument recovers the
marked locator `prod_{y in M}(X-y)` uniquely from `V_u`.

Therefore, for fixed nonempty `U`, there is at most one active support `S`
with `U(S)=U` and `|M(S)|=tau+1`.  Boundary matching fibers can only remain
over the empty core `U=empty`, where no simple-pole lift is available.

Consequently the closure criterion (CC) sharpens as follows.  Let

```text
Core^+_{tau+1}(s)=Core_{tau+1}(s)\{empty},
epsilon_empty=1 if empty in Core_{tau+1}(s), else 0.
```

Then

```text
|Cert_m^{<=tau+1}(s)|
 <= sum_{r=m}^{tau} binom(r,m) |Core_r(s)|
    + binom(tau+1,m)
      ( |Core^+_{tau+1}(s)|
        + epsilon_empty floor(n/(tau+1)) ).       (CC')
```

Thus, once the canonical core ledgers are polynomial, this split-support
branch is `O_tau(n^B+n)` rather than carrying a boundary matching factor over
every core.  The only residual boundary matching is the completely marked
case `S=M(S)`, which is a separate full-marked packet endpoint.

The verifier now enforces this strengthened boundary rule.  In the bundled
audits the largest `F_7^*` case has `21540` marked-core fibers and maximum
fiber size `2`; no nonempty boundary core occurs there, and any future
nonempty boundary core fiber is required to be singleton.

## Moment-Complete Cores Have Unique Marked Frontiers

The same argument is not confined to the boundary `r=tau+1`.  Let `S` be
active, put

```text
M=M(S),        U=U(S),        r=|M|,
```

and fix the canonical unmarked core `U` and the marked count `r`.  If

```text
|U| >= max(0,r-tau),                              (MCU)
```

then there is at most one active support `S` with this core and this marked
count.

The case `r=0` is tautological, since then `S=U`.  Otherwise put
`e=max(0,r-tau)` and choose any `E subset U` of size `e`.  If `r<=tau`,
then `E=empty` and the full marked face (CP0) already gives at least `2r`
visible moments.  If `r>tau`, apply the mixed face formula with this `E` and
`Y=M`:

```text
H_{tau+e+r,|U|-e}(s)ell_{U\E}
 = (sum_{y in M} a_y y^i/ell_E(y))_{0<=i<=tau+e+r-1}.
```

The left hand side is fixed by `U` and `E`.  The right hand side is an
`r`-sparse moment packet with nonzero amplitudes, and
`tau+e+r >= 2r` by the choice of `e`.  Hence the Prony/Vandermonde
annihilator recovers the marked locator `prod_{y in M}(X-y)` uniquely from
that fixed vector.

Consequently any nonunique canonical-core fiber with marked count `r` must be
moment-short:

```text
|U| < r-tau.                                      (MS)
```

Large marked frontiers therefore do not by themselves create a new
same-core packing problem.  Branching over a fixed core can only occur when
the marked excess `r-tau` is larger than the available unmarked zero-depth
shift.  This isolates the remaining large-frontier obstruction to short-core
supports rather than all supports with many marked exits.

The verifier now enforces this uniqueness condition for every produced
canonical-core fiber.  In the largest `F_7^*` audit, it checks `4320`
moment-complete core fibers, all singleton; the productive subaudit checks
`2160`, again all singleton.

## Moment-Short Fibers Are Deficit Packings

The moment-short case still has a rigid form.  Fix a canonical unmarked core
`U` and a marked count `r`, and define the moment deficit

```text
d=r-tau-|U|.
```

If `d<=0`, the preceding theorem gives uniqueness.  Assume `d>0`.  Then any
two distinct active supports `S_1,S_2` with `U(S_i)=U` and `|M(S_i)|=r`
satisfy

```text
|M(S_1) cap M(S_2)| < d.                         (DP0)
```

Consequently every fixed-`U`, fixed-`r` canonical-core fiber has size at most

```text
floor( binom(n-|U|,d) / binom(r,d) ).             (DP1)
```

Proof: delete all unmarked roots, so `E=U`, and put
`L=tau+|U|+r`.  The mixed face formula gives the same fixed length-`L`
sequence for every support in the fiber:

```text
G_U
 = (sum_{y in M(S)} a_y y^i/ell_U(y))_{0<=i<L}.
```

Suppose two marked frontiers `M_1,M_2` in the same fiber have intersection
size `c>=d`.  Subtracting the two displayed sparse representations gives a
zero moment sequence supported on `M_1 union M_2`, whose size is at most
`2r-c`.  Since

```text
2r-c <= 2r-d = tau+|U|+r = L,
```

the first `|M_1 union M_2|` rows form an invertible Vandermonde system.  All
difference coefficients vanish, so the two sparse representations have the
same support and amplitudes.  This contradicts distinctness.  Hence (DP0)
holds.

For (DP1), each marked support contains `binom(r,d)` different `d`-subsets,
and no `d`-subset of `H\U` can occur in two distinct marked frontiers by
(DP0).  There are only `binom(n-|U|,d)` available `d`-subsets.

This theorem unifies the previous special cases.  The moment-complete regime
is `d<=0`.  The boundary matching case is `d=1`, where distinct frontiers are
disjoint and the packing bound becomes `floor((n-|U|)/r)`.  Higher deficits
are not arbitrary same-core clusters; they are bounded packing families with
controlled overlap.

The verifier now checks this deficit-packing rule for every produced
moment-short canonical-core fiber.  In the largest `F_7^*` audit, it checks
`17220` deficit-packing fibers with maximum deficit `1` and maximum fiber
size `2`; the productive subaudit has the same counts.

## Deficit Anchors Reconstruct Moment-Short Fibers

The packing proof has a constructive form.  Keep `U`, `r`, and
`d=r-tau-|U|>0` fixed, and let `W` be a `d`-subset of the marked frontier
`M(S)`.  Then the pair `(U,W)` determines the whole marked frontier `M(S)`.

Indeed, delete all unmarked roots and put `L=tau+|U|+r`.  The mixed face
formula gives the fixed length-`L` moment sequence

```text
G_U
 = (sum_{y in M(S)} a_y y^i/ell_U(y))_{0<=i<L}.
```

Apply the locator `ell_W` to this sequence:

```text
(ell_W G_U)_i
 = sum_{y in M(S)\W} a_y ell_W(y) y^i/ell_U(y),
        0<=i<L-d.
```

The modes in `W` vanish, and every remaining amplitude is nonzero.  Since

```text
|M(S)\W|=r-d=tau+|U|,        L-d=2(r-d),
```

the Prony/Vandermonde annihilator recovers the remaining locator
`prod_{y in M(S)\W}(X-y)` from `(ell_W G_U)`.  Thus `M(S)` is recovered as
`W union (M(S)\W)`.

Equivalently, the map

```text
(S,W),        W subset M(S), |W|=d
    ->        (U(S),W)
```

is injective on fixed-`r` moment-short fibers.  The deficit-packing bound is
just the counting shadow of this reconstruction.  This gives a concrete
object for the remaining M1 short-core ledger: count admissible deficit
anchors `(U,W)`, not repeated marked frontiers over the same core.

The verifier audits this anchor injection directly, in addition to the
pairwise-overlap packing condition.  In the largest `F_7^*` audit, it checks
`51840` deficit-anchor labels, with at most `6` labels in any one fiber; the
productive subaudit has the same counts.

## Deficit Anchors Are Residual Hankel Kernels

The reconstruction can be stated as a concrete Hankel-kernel target.  Given a
deficit anchor `(U,W)` as above, put

```text
q=r-d=tau+|U|.
```

Let

```text
h^{W}_i = (H_{2q,d}(s)ell_W)_i
        = sum_{a=0}^d (ell_W)_a s_{i+a},
        0<=i<2q.
```

Then the residual marked set `R=M(S)\W`, `|R|=q`, has locator `ell_R`
satisfying

```text
H_{q,q}(h^W)ell_R=0.                            (DAK)
```

Moreover the first `2q` entries of `h^W` recover `ell_R` uniquely.  Thus a
deficit anchor does not leave an arbitrary residual search; it leaves a
squarefree degree-`q` locator in the ordinary Hankel kernel of the filtered
sequence `h^W`.

Proof: the formula for `ell_W G_U` in the previous section is exactly the
sequence `h^W`.  Its support is `R`, all amplitudes are nonzero, and it has
`2q` visible moments.  Applying the locator `ell_R` annihilates it for `q`
consecutive rows, giving (DAK).  Conversely, the Prony/Vandermonde recovery
from these `2q` moments gives the unique monic annihilator `ell_R`.

This is the algebraic form of the remaining short-core problem: count pairs
`(U,W)` for which the filtered sequence `h^W` has an admissible squarefree
degree-`tau+|U|` kernel locator disjoint from `U union W`, together with the
unmarked-core conditions on `U`.

The verifier audits this residual-kernel form for every produced deficit
anchor.  In the largest `F_7^*` audit, it checks `51840` filtered kernel
recoveries, with maximum residual size `2`; the productive subaudit has the
same counts.

## Bounded Residual-Kernel Dimension Bounds Deficit Anchors

The filtered-kernel target has an immediate finite-dimensional closure
criterion.  Fix a deficit anchor `(U,W)`, put `q=tau+|U|`, and let `D'` be
the available domain `H\(U union W)`.  Consider the affine space of monic
degree-`q` residual locators

```text
K(U,W)={
  P(X)=p_0+p_1 X+...+p_{q-1}X^{q-1}+X^q :
  H_{q,q}(h^W)P=0
}.
```

Let `b(U,W)` be its direction dimension.  Equivalently, if `M(h^W)` is the
`q x q` moment matrix `(h^W_{i+j})_{0<=i,j<q}`, then

```text
b(U,W)=q-rank M(h^W).
```

The number of squarefree residual supports `R subset D'`, `|R|=q`, whose
locator lies in `K(U,W)` is at most

```text
sum_{i=0}^{b(U,W)} binom(|D'|,i).                (DKB)
```

Proof: view `K(U,W)` as an affine space of dimension `b=b(U,W)`.  For each
root `x in D'`, the condition `P(x)=0` is an affine hyperplane in `K(U,W)`.
If a monic degree-`q` locator `P_R` vanishes on a residual support `R` of
size `q`, then no other monic degree-`q` polynomial can vanish on all of
`R`; hence the hyperplanes indexed by `R` cut `K(U,W)` down to the single
point `P_R`.  Choose a minimal independent subcollection of these
hyperplanes.  It has size at most `b` and determines `P_R`, hence determines
`R` as its zero set in `D'`.  Therefore distinct residual supports inject
into subsets of `D'` of size at most `b`, proving (DKB).

Thus after the deficit-anchor reduction, the only way a fixed anchor can
carry many residual completions is through a high-dimensional filtered
Hankel-kernel direction space.  Bounded direction dimension gives a direct
polynomial residual-fiber bound.

The verifier enumerates these squarefree residual-kernel fibers for every
produced deficit anchor and checks (DKB).  In the largest `F_7^*` audit, it
checks `51840` residual fibers carrying `51840` labels, with maximum fiber
size `1` and maximum direction dimension `0`; the productive subaudit has the
same counts.

## Filtered Residual Kernels Are Divisible Short Kernels

The high-dimensional case in (DKB) is not a new packet object.  It is exactly
a fixed-divisor short Hankel-kernel object in the prefiltered sequence.

Let `E=ell_W` and keep `q=tau+|U|`.  For any polynomial
`Q(X)=sum_{b=0}^q Q_b X^b` of degree at most `q`,

```text
(H_{q,q}(h^W)Q)_i
 = sum_{b=0}^q Q_b h^W_{i+b}
 = sum_{a=0}^d sum_{b=0}^q E_a Q_b s_{i+a+b}
 = (H_{q,q+d}(s)(E Q))_i,        0<=i<q.        (DKI)
```

Consequently the direction space of the affine monic residual kernel is

```text
Dir K(U,W)
 = { Q in F[X]_{<q} : H_{q,q+d}(s)(E Q)=0 }.
```

Thus `b(U,W)>0` is equivalent to the existence of nonzero lower-degree
directions `Q` for which the product `ell_W Q` is killed by the same `q`
Hankel rows.  In other words, the only way a deficit anchor can have a
positive-dimensional residual-kernel fiber is through a short Hankel-kernel
direction with the fixed divisor `ell_W`.

For squarefree residual supports, (DKI) says that a candidate residual locator
`ell_R` is in the filtered kernel if and only if the combined locator
`ell_W ell_R` lies in this divisible short-kernel slice.  This identifies the
remaining high-dimensional residual-anchor obstruction with a fixed-root /
quotient-periodic / aperiodic denominator ledger, rather than with an
unstructured completion multiplicity.

The verifier now checks (DKI) for every squarefree residual candidate tested
in the residual-fiber enumeration.  In the largest `F_7^*` audit, this covers
the same `51840` residual labels as the bounded-dimension audit, with maximum
residual-kernel direction dimension `0`; the productive subaudit has the same
counts.

## Residual Collisions Charge to Root-Slice Directions

The divisible-kernel identity gives a local overlap charge for residual
collisions.  Fix a deficit anchor `(U,W)` and let `R_1,R_2` be two distinct
squarefree residual supports in the same filtered kernel.  Since both
locators are monic of degree `q`,

```text
Q=ell_{R_1}-ell_{R_2}
```

has degree `<q`, is nonzero, and lies in `Dir K(U,W)`.  By (DKI),

```text
H_{q,q+d}(s)(ell_W Q)=0.                         (RCD)
```

If `x in R_1 cap R_2`, then `Q(x)=0`, so `Q=(X-x)Q_x` with
`deg Q_x<q-1`, and therefore

```text
H_{q,q+d-1}(s)(ell_W (X-x) Q_x)=0.               (RCS)
```

Thus any shared residual root in a same-anchor collision is charged to a
one-root slice of the divisible short kernel.  More generally, if
`C subset R_1 cap R_2`, then `ell_C` divides `Q`, and the collision is charged
to the `C`-root slice

```text
H_{q,q+d-1}(s)(ell_W ell_C Q_C)=0,
deg Q_C<q-|C|.
```

This gives a packing form.  For `1<=c<q`, call a `c`-subset
`C subset D'=H\(U union W)` bad if the corresponding `C`-root slice has a
nonzero direction.  Then every good `C` occurs in at most one residual
support in the fixed-anchor fiber.  Consequently, if `Z_c(U,W)` is the set of
bad `c`-subsets and `N=|D'|`, then the residual fiber satisfies

```text
|F(U,W)| binom(q,c)
 <= binom(N,c)-|Z_c(U,W)|
    + |Z_c(U,W)| binom(N-c,q-c).                 (RSP)
```

In particular, if the one-root bad set is empty, residual supports in the
same anchor fiber are pairwise disjoint and `|F(U,W)|<=floor(N/q)`.

This is the local root-slice bridge for the residual-anchor obstruction:
large overlap inside a residual fiber cannot remain invisible.  It either
produces an explicit fixed-root short-kernel direction, or the residual
supports are packing-limited after the bad root slices are charged.

The verifier audits the one-root case.  For each produced deficit anchor with
`q>=2`, it tests every available root `x` for a nonzero direction in the
matrix with columns

```text
H_{q,q+d-1}(s)(ell_W (X-x) X^a),   0<=a<q-1,
```

and checks that any shared root of two residual candidates lies in this bad
set.  In the largest `F_7^*` audit, it checks `51840` anchors and `259200`
one-root residual slices, with `0` bad root-slice labels and maximum bad
root-slice count `0` per anchor; the productive subaudit has the same counts.

## One-Dimensional Residual Kernels Are Root-Slice Packings

The first positive-dimensional residual-kernel case has a sharper structure
than the general hyperplane-arrangement bound.  Suppose `b(U,W)=1`, so the
affine residual kernel is a line

```text
K(U,W)=P_0 + lambda Q,        lambda in F,
```

with a nonzero direction `Q in F[X]_{<q}`.  Let

```text
Z_Q={x in D' : Q(x)=0},     z=|Z_Q|.
```

Because `deg Q<q`, one has `z<=q-1`.  If `R_lambda` and `R_mu` are two
distinct squarefree residual supports in the fiber, then

```text
ell_{R_lambda}-ell_{R_mu}=(lambda-mu)Q.
```

Hence every shared residual root of `R_lambda` and `R_mu` lies in `Z_Q`.
Equivalently, outside `Z_Q` the residual supports are pairwise disjoint.  Since
each residual support has at least `q-z` roots outside `Z_Q`, incidence counting
outside `Z_Q` gives

```text
|F(U,W)| <= floor((|D'|-z)/(q-z)).                  (LKB)
```

For `q>1`, the same direction identifies the one-root bad slices:

```text
Z_Q = {x in D' : H_{q,q+d-1}(s)(ell_W (X-x)Q_x)=0
               for some nonzero deg Q_x<q-1 }.
```

Indeed the root slice has a nonzero direction if and only if the unique
direction `Q` is divisible by `X-x`.  Thus dimension-one residual kernels are
already ordinary root-slice packings; their only overlap reservoir is the
fixed-root set `Z_Q`.

This is stronger than (DKB) at `b=1`: instead of the coarse `1+|D'|` bound, it
gives the disjoint-packing bound after the roots of the single direction
polynomial have been charged.  The verifier now extracts the unique direction
whenever `b(U,W)=1`, checks that its domain roots match the bad one-root slices,
and asserts (LKB).  In the current largest `F_7^*` audit no produced anchor has
`b(U,W)=1`; all produced anchors still have `b(U,W)=0`.

## Direction-MDS Residual Kernels Give b-Packings

The same root-slice mechanism has a higher-dimensional form.  Let

```text
V(U,W)=Dir K(U,W),        b=dim V(U,W),        1<=b<q.
```

For a `b`-subset `C subset D'`, write

```text
ev_C : V(U,W) -> F^C,        Q |-> (Q(x))_{x in C}.
```

Call `C` direction-bad if `ev_C` is not injective, equivalently if some nonzero
`Q in V(U,W)` is divisible by `ell_C`.  Let `Z_b^{dir}(U,W)` be the set of such
bad `b`-subsets.

If two distinct residual supports `R_1,R_2` contain the same `b`-subset `C`,
then

```text
ell_{R_1}-ell_{R_2} in V(U,W)\{0}
```

and this difference vanishes on `C`.  Thus `C in Z_b^{dir}(U,W)`.  Therefore
every good `b`-subset occurs in at most one residual support.  Counting
incidences between residual supports and their `b`-subsets gives

```text
|F(U,W)| binom(q,b)
 <= binom(N,b)-|Z_b^{dir}(U,W)|
    + |Z_b^{dir}(U,W)| binom(N-b,q-b).             (DMB)
```

In particular, if the direction space is MDS on the available domain, meaning
all `b`-root evaluation maps `ev_C` are injective, then

```text
|F(U,W)| <= floor( binom(N,b) / binom(q,b) ).       (DMB-MDS)
```

This is the natural higher-dimensional analogue of the `b=1` root-slice
packing: positive residual dimension is harmless once the bad divisor
incidences of the direction space are charged.  By the divisible-kernel
identity (DKI), the bad `b`-subsets are exactly the `b`-root fixed-divisor
short-kernel slices

```text
H_{q,q+d-b}(s)(ell_W ell_C Q_C)=0,        deg Q_C<q-b.
```

Thus the remaining high-dimensional residual-anchor obstruction is no longer
an arbitrary affine kernel count.  It is a finite rank-defect ledger for the
evaluation matroid of `V(U,W)`, plus the corresponding fixed-root slice charges.

The verifier now extracts a basis for `V(U,W)` whenever `0<b<q`, enumerates
the bad `b`-subsets by the rank of `ev_C`, checks that all shared `b`-subsets of
two residual candidates are bad, and asserts (DMB).  In the current largest
`F_7^*` audit no produced anchor has positive residual direction dimension, so
this audit is installed for future cases but not triggered by the present data.

## Bad Direction Subsets Are Projective Root Shadows

The bad-set term in (DMB) is not an independent object.  It is exactly the
projective root shadow of the residual direction space.  For nonzero
`Q in V(U,W)`, write

```text
Z_{D'}(Q)={x in D' : Q(x)=0}.
```

Then, with `b=dim V(U,W)`,

```text
Z_b^{dir}(U,W)
 =
union_{[Q] in P(V(U,W))}
  {C subset Z_{D'}(Q) : |C|=b}.                    (PRS)
```

Indeed, if `C` is direction-bad, the map `ev_C` is not injective.  Hence there
is a nonzero `Q in V(U,W)` with `Q(x)=0` for every `x in C`, so
`C subset Z_{D'}(Q)`.  Conversely, if `C subset Z_{D'}(Q)` for some nonzero
`Q in V(U,W)`, then `Q` lies in the kernel of `ev_C`, so `C` is bad.  The
condition only depends on the projective class `[Q]`.

Consequently

```text
|Z_b^{dir}(U,W)|
 <=
sum_{[Q] in P(V(U,W))} binom(|Z_{D'}(Q)|,b).       (PRS-bound)
```

In particular, if every nonzero residual direction has fewer than `b`
available roots, then the direction space is MDS on `D'` and (DMB-MDS) applies.
By (DKI), every projective direction is a fixed-divisor short-kernel direction:

```text
H_{q,q+d}(s)(ell_W Q)=0.
```

Thus the higher-dimensional bad-set ledger is a projective fixed-divisor
root-count ledger.  This is the form that can be charged against the fixed-root,
quotient-periodic, and aperiodic pieces of the M1 all-line residue-packing
target.

The verifier now checks (PRS) whenever it audits the `0<b<q` direction-MDS
packing.  The current largest `F_7^*` scan still has no positive-dimensional
produced residual anchors, so the equality check is installed as a future-case
audit rather than triggered by the present data.

## Bad Direction Subsets Are Absorbed Multi-Root Rank Defects

The same bad `b`-subsets also have a direct absorbed-Hankel test.  For
`C subset D'`, `|C|=b`, put

```text
E_C = ell_W ell_C,
h^{W,C}_i = sum_a (E_C)_a s_{i+a}.
```

Let

```text
A_C(U,W)= (h^{W,C}_{i+j})_{0<=i<q, 0<=j<q-b},
```

a `q x (q-b)` matrix.  Then

```text
C in Z_b^{dir}(U,W)
    iff
rank A_C(U,W) < q-b.                            (AMR)
```

Indeed, `C` is direction-bad exactly when there is a nonzero
`Q in Dir K(U,W)` vanishing on every root of `C`.  Since the roots of `C` are
distinct and `deg Q<q`, this is equivalent to `Q=ell_C Q_C` with
`deg Q_C<q-b`.  By (DKI), this is equivalent to

```text
H_{q,q+d-b}(s)(ell_W ell_C Q_C)=0,
```

which is exactly the existence of a nonzero right kernel vector for
`A_C(U,W)`.  The converse is the same implication read backward.

Thus the DMB bad-set term can be computed without first constructing the
evaluation matroid of `Dir K(U,W)`: it is precisely the multi-root absorbed
fixed-divisor rank-defect ledger.  This generalizes the one-root absorbed
matrix below and is the scanner-ready form for fixed-root, quotient-periodic,
and aperiodic charges.

The verifier now checks (AMR) against the evaluation-rank and projective-shadow
descriptions whenever the `0<b<q` direction-MDS audit is triggered.  The current
largest `F_7^*` scan still has no positive-dimensional produced residual
anchors.

## Projective Root Counts Close Bounded Residual Direction

The projective-shadow formula gives a universal bad-set bound.  Since every
nonzero direction `Q in V(U,W)` has `deg Q<q`, it has at most `q-1` roots in
the field, hence at most `min(|D'|,q-1)` roots in the available domain.  Also

```text
|P(V(U,W))| = (|F|^b-1)/(|F|-1).
```

Therefore

```text
|Z_b^{dir}(U,W)|
 <= ((|F|^b-1)/(|F|-1)) binom(min(|D'|,q-1),b).  (PRC)
```

Combining (PRC) with (DMB), and writing

```text
Z_b^max=((|F|^b-1)/(|F|-1)) binom(min(N,q-1),b),
```

gives the explicit fixed-anchor residual-fiber closure

```text
|F(U,W)| binom(q,b)
 <= binom(N,b)-Z_b^{dir}(U,W)
    + |Z_b^{dir}(U,W)| binom(N-b,q-b)
 <= binom(N,b)+Z_b^max binom(N-b,q-b).           (BRC)
```

Thus fixed anchors with bounded residual direction dimension are polynomially
controlled in the polynomial-field window: for fixed `b` and `|F|<=n^A`, the
bad-subset term is `n^{O_{A,b}(1)}`.  The remaining M1 difficulty is not an
unstructured positive-dimensional residual fiber; it is to control how often
such bounded-`b` fixed-divisor kernels occur after quotient-periodic, tangent,
and aperiodic ledgers are charged, and to classify any unbounded-`b` or
persistent family.

This bound is intentionally coarse compared with the direction-MDS case.  Its
role is to turn bounded residual direction into an explicit polynomial
fallback, while sharper work can try to prove MDS behavior or much smaller
root-shadow ledgers for the actual M1 kernels.

The verifier now checks the inequality (PRC) whenever it constructs the
direction-MDS bad-set ledger.  The current largest `F_7^*` scan still has
`b(U,W)=0` for all produced residual anchors.

## Higher Bad Subsets Are Charged to One-Root Slices

There is a sharper envelope when the one-root bad-slice ledger is known.  Let

```text
Z_1(U,W)={x in D' : x is a bad one-root slice}.
```

Equivalently, by the absorbed-anchor rank test below, `x in Z_1(U,W)` iff the
matrix `A_x(U,W)` has rank `<q-1`.  If `C in Z_b^{dir}(U,W)`, then there is a
nonzero direction

```text
Q=ell_C Q_C in Dir K(U,W).
```

For each `x in C`, the same direction is divisible by `X-x`, so the one-root
slice at `x` has a nonzero kernel direction.  Hence

```text
Z_b^{dir}(U,W) subset { C subset Z_1(U,W) : |C|=b }.       (Z1-envelope)
```

In particular, with `z=|Z_1(U,W)|`,

```text
|Z_b^{dir}(U,W)| <= binom(z,b).                         (Z1-bound)
```

Combining this with (DMB) gives the root-slice-charged residual-fiber bound

```text
|F(U,W)| binom(q,b)
 <= binom(N,b)+binom(z,b) binom(N-b,q-b).                (Z1-DMB)
```

If `z<b`, then `Z_b^{dir}(U,W)` is empty and the direction-MDS packing bound
(DMB-MDS) applies.  Thus higher-dimensional residual direction spaces do not
create an independent bad-subset reservoir: their bad `b`-sets are already
contained in the one-root fixed-root ledger.

This is the useful form for M1.  Once quotient-periodic, tangent, fixed-root,
or aperiodic arguments bound the one-root absorbed-rank defects, every bounded
residual direction dimension inherits a packing bound without separately
enumerating the whole projective direction space.

The verifier now checks (Z1-envelope) whenever it constructs the direction-MDS
bad-set ledger.  The current largest `F_7^*` scan still has `Z_1(U,W)=empty`
and `b(U,W)=0` for all produced residual anchors.

## Nonpersistent One-Root Pencils Close Higher Bad Ledgers

The one-root envelope combines with the finite/persistent dichotomy for the
absorbed pencil.  Recall that

```text
A_x(U,W)=B(U,W)-x C(U,W)
```

is a `q x (q-1)` affine pencil.  If it is not persistent, then some maximal
minor is a nonzero polynomial in `x` of degree at most `q-1`.  Hence the
one-root bad set satisfies

```text
|Z_1(U,W)| <= q-1.                               (Z1-finite)
```

By (Z1-bound), every higher bad ledger then satisfies

```text
|Z_b^{dir}(U,W)| <= binom(q-1,b).                (finite-Zb)
```

Substituting this into (DMB) gives the field-size-free fixed-anchor bound

```text
|F(U,W)| binom(q,b)
 <= binom(N,b)+binom(q-1,b) binom(N-b,q-b).       (finite-DMB)
```

Thus the nonpersistent one-root branch closes the entire hierarchy of
direction-MDS bad ledgers.  The only way a higher-dimensional bad-subset
obstruction can avoid this finite bound is for the one-root absorbed pencil to
be persistent.  But the persistent branch already has the moving-kernel
certificate and endpoint/residual-direction containment described below, so it
is not a separate high-dimensional bad-set phenomenon.

This is stronger than the coarse projective root-count fallback in the
polynomial-field window: the bad-subset term is controlled by `q` and `b`, not
by the number of projective residual directions.  Therefore, for the M1
fixed-anchor residual route, the main remaining structural target is the
persistent one-root absorbed pencil after quotient-periodic, tangent, and
aperiodic charges.

The verifier now checks the finite one-root implication.  It detects whether
the absorbed pencil has full column rank at some field value; in that finite
branch it asserts `|Z_1(U,W)|<=q-1` and then checks
`|Z_b^{dir}(U,W)|<=binom(q-1,b)` whenever the direction-MDS bad-set audit is
triggered.  The current largest `F_7^*` scan lies in the finite branch with
`Z_1(U,W)=empty`.

## Persistent One-Root Pencils Are Genuinely Higher-Dimensional

Assume `|F|>q-1`, as in the smooth RS setting where a produced residual
support of size `q` lies in `D' subset F^*`.  If the one-root absorbed pencil
is rank-defective for every `x in F`, then it is genuinely persistent: every
maximal minor has degree at most `q-1`, so a nonzero minor cannot vanish on all
of `F`.

For a produced deficit anchor, such a persistent one-root pencil forces

```text
e(U,W)>0,        b(U,W)>=2.                       (PHD)
```

The endpoint defect `e(U,W)>0` is the moving-kernel endpoint consequence:
persistence gives a nonzero polynomial family `Q_z(X)` with

```text
H_{q,q+d-1}(s)(ell_W (X-z)Q_z(X))=0,
```

and the top coefficient of `Q_z` is a nonzero kernel of the endpoint map
`R -> H_{q,q+d-1}(s)(ell_W R)`.

The endpoint-prefix inclusion gives `e(U,W)<=b(U,W)`, hence `b(U,W)>0`.  It
remains to rule out `b(U,W)=1`.  In that case the residual direction space is
spanned by a single nonzero polynomial `Q` of degree `<q`.  The line-kernel
root-slice theorem identifies the one-root bad set with

```text
Z_Q={x in D' : Q(x)=0},
```

so `|Z_1(U,W)|<=q-1`.  But a genuinely persistent one-root pencil makes every
available root bad, so `Z_1(U,W)=D'`.  Since the anchor is produced, it has a
residual support `R subset D'` with `|R|=q`, hence `|D'|>=q`, a contradiction.
Thus `b(U,W)>=2`.

Consequently, after the finite one-root branch is closed, the only remaining
persistent absorbed obstruction is not a line-kernel phenomenon.  It must
produce a genuinely higher-dimensional fixed-divisor residual direction space.
This sharpens the next M1 target: classify or exclude persistent one-root
moving kernels with `b(U,W)>=2` after quotient-periodic, tangent, and aperiodic
charges.

The verifier checks this when full-field probing certifies persistence
(`|F|>q-1`): certified persistent one-root pencils must have endpoint defect
and residual direction dimension at least two.  The current largest `F_7^*`
scan has no certified persistent produced anchor.

## Higher Residual Direction Is the Persistent One-Root Branch

The converse direction is simpler and completes the local dictionary.  If
`b(U,W)>=2`, then every available root is one-root bad:

```text
Z_1(U,W)=D'.                                      (HRD)
```

Indeed, for any `x in D'`, evaluation at `x` is a linear map

```text
Dir K(U,W) -> F,        Q |-> Q(x).
```

Its domain has dimension at least `2` and its codomain has dimension `1`, so it
has a nonzero kernel.  Thus some nonzero residual direction vanishes at `x`,
which is exactly the one-root bad-slice condition.

For a produced anchor, `D'` contains the produced residual support `R` of size
`q`, so `|D'|>=q`.  If the one-root pencil were nonpersistent, the finite
branch would give `|Z_1(U,W)|<=q-1`, contradicting (HRD).  Hence, when
`|F|>q-1`, a produced anchor satisfies

```text
one-root absorbed pencil is persistent
    iff
b(U,W)>=2.                                       (PEQ)
```

The forward implication is (PHD), and the reverse implication is (HRD) plus the
finite/persistent dichotomy.  Thus the residual-anchor problem has no remaining
gap between the one-root absorbed-pencil language and the residual-direction
language: after the finite one-root branch is closed, the surviving branch is
precisely the higher-dimensional fixed-divisor residual direction space.

The verifier now checks (HRD) whenever `b(U,W)>=2`, and in the usual field-size
range it also checks that such anchors lie in the persistent one-root branch.
The current largest `F_7^*` scan has no positive-dimensional produced residual
anchor.

## Two-Dimensional Residual Directions Are Projective Fibers

The first surviving persistent case after (PHD) is `b(U,W)=2`.  In that case
the bad-pair ledger has a concrete projective-fiber form.  Choose a basis

```text
V(U,W)=span(P,Q),        deg P,deg Q<q.
```

For `x in D'`, put

```text
ev_x=[P(x):Q(x)] in P^1
```

when `(P(x),Q(x))` is nonzero, and put `x in B_0` when `P(x)=Q(x)=0`.
Then the bad pairs are exactly

```text
Z_2^{dir}(U,W)
 =
{ {x,y}: x in B_0 or y in B_0 }
 union
 union_{lambda in P^1}
   { {x,y}: x,y notin B_0, ev_x=ev_y=lambda }.       (PF2)
```

Indeed, a pair `{x,y}` is bad exactly when the two evaluation rows

```text
(P(x),Q(x)),        (P(y),Q(y))
```

have rank `<2`.  This happens if one row is zero, or if both nonzero rows are
projectively equal.  Conversely, either condition gives rank `<2`.

The fibers are ordinary rational-function fibers.  For
`lambda=[a:b] in P^1`, the fiber is cut out by the nonzero polynomial

```text
b P(X)-a Q(X),
```

and has size at most `q-1` in `D'`; the base set `B_0` is contained in the
zero set of the nonzero polynomial `P`, so it also has size at most `q-1`.
Thus the `b=2` persistent residual branch is not a generic rank-defect
matroid.  It is a projective rational-fiber packing problem, with common-root
base points separated from equal-value fibers.

Consequently, if all projective fibers and the base set have bounded size
after quotient-periodic, tangent, fixed-root, and aperiodic charges, then
(DMB) gives the corresponding residual-fiber bound.  In the injective,
base-free case, `Z_2^{dir}(U,W)=empty` and the direction-MDS packing bound
applies.

The verifier now checks (PF2) whenever a produced residual anchor has
`b(U,W)=2`: it compares the bad-pair ledger with the projective evaluation
fibers and checks the elementary degree bound on every fiber and on `B_0`.
The current largest `F_7^*` scan has no such produced anchor.

## Projective Fibers Give Exact Bad-Pair Counts

The `b=2` projective-fiber normal form gives an exact counting ledger.  Let

```text
N=|D'|,        s=|B_0|,
m_lambda=|{x in D'\B_0 : ev_x=lambda}|.
```

Then

```text
|Z_2^{dir}(U,W)|
 =
binom(N,2)-binom(N-s,2)
 + sum_{lambda in P^1} binom(m_lambda,2).        (PF2-count)
```

The first term counts all pairs touching the base locus `B_0`; the sum counts
equal projective-value pairs away from the base.  These two classes are
disjoint and exhaust (PF2).

If every non-base projective fiber has size at most `M`, then

```text
|Z_2^{dir}(U,W)|
 <= binom(N,2)-binom(N-s,2)
    + floor((M-1)(N-s)/2).                       (PF2-envelope)
```

Combining this with (DMB) at `b=2` gives

```text
|F(U,W)| binom(q,2)
 <= binom(N,2)-Z_2^{dir}(U,W)
    + |Z_2^{dir}(U,W)| binom(N-2,q-2).           (PF2-DMB)
```

Thus the `b=2` residual fiber is controlled once the base locus and the
projective evaluation fibers are controlled.  In the base-free injective case
`s=0` and `M=1`, so `Z_2^{dir}(U,W)=empty` and the direction-MDS packing bound
applies.  More generally, bounded fiber size gives only a linear bad-pair
ledger outside the base locus, a sharper target than the coarse projective
root-count fallback.

The verifier now checks (PF2-count) and (PF2-envelope) whenever
`b(U,W)=2`.  The current largest `F_7^*` scan has no positive-dimensional
produced residual anchor.

## Cross-Fiber Good Pairs Give a b=2 Packing Bound

The complement of the bad-pair ledger gives a sharper packing count.  In the
notation of the previous section, call a pair `{x,y}` good if

```text
x,y notin B_0,        ev_x != ev_y.
```

Then the total number of good pairs in `D'` is

```text
G_tot = binom(N-s,2)-sum_lambda binom(m_lambda,2).          (PF2-good)
```

No good pair can lie in two distinct residual supports in the same fixed-anchor
fiber: if two supports shared such a pair, the pair would be a shared
`b=2`-subset and therefore direction-bad by (DMB), contradicting goodness.

For a residual support `R`, let

```text
g(R)=|{{x,y} subset R : x,y notin B_0, ev_x != ev_y}|.
```

Then

```text
sum_{R in F(U,W)} g(R) <= G_tot.                 (PF2-good-pack)
```

In particular, if every residual support in the fixed-anchor fiber has at least
`g_min>0` good pairs, then

```text
|F(U,W)| <= floor(G_tot/g_min).                  (PF2-good-bound)
```

This is often sharper than applying (DMB) with all bad pairs, because the count
uses only cross-fiber pairs that cannot be reused.  It also isolates the only
ways the `b=2` packing can fail to gain this saving: residual supports must
place too many roots in the base locus or inside a small number of projective
fibers.  Those are exactly fixed-root or quotient/aperiodic fiber phenomena.

The verifier now checks the good-pair count, verifies that good pairs are not
shared by two residual candidates, and asserts (PF2-good-bound) whenever
`g_min>0`.  The current largest `F_7^*` scan has no `b(U,W)=2` produced anchor.

## b=2 Good Pairs Have a Concentration Lower Bound

The good-pair count can be lower-bounded from simple occupancy data.  For a
residual support `R`, let

```text
a(R)=|R cap B_0|,
r_lambda(R)=|R cap ev^{-1}(lambda)|,
M(R)=max_lambda r_lambda(R).
```

Then the exact support-level count is

```text
g(R)
 =
binom(q-a(R),2)-sum_lambda binom(r_lambda(R),2).  (PF2-support)
```

Consequently, if every residual support in the fixed-anchor fiber satisfies

```text
a(R)<=A,        M(R)<=M,
```

then, putting `L=q-A`,

```text
g(R)
 >=
binom(L,2)
 - ( floor(L/M) binom(M,2)
     + binom(L mod M,2) ).                       (PF2-conc)
```

The bracket is the largest possible same-fiber pair count among `L` non-base
roots when no projective fiber receives more than `M` of them.  Thus unless a
support concentrates many roots in the base locus or in a single projective
fiber, it contributes many good cross-fiber pairs and is strongly packing
bounded by (PF2-good-bound).

This isolates the next M1 obstruction inside the `b=2` persistent branch:
large residual fibers must create base-heavy or projective-fiber-heavy supports.
Those are fixed-root and quotient/aperiodic concentration phenomena rather
than generic residual-kernel multiplicity.

The verifier now checks (PF2-support) for each residual candidate and checks
the concentration lower bound determined by the largest base occupancy and
largest fiber occupancy seen in the fixed-anchor fiber.  The current largest
`F_7^*` scan has no `b(U,W)=2` produced anchor.

## b=2 Concentration Is a Fixed-Divisor Slice

The concentration alternatives from (PF2-conc) are not new residual
multiplicity.  They are fixed-divisor slice ledgers.

Let `V(U,W)=<P,Q>` and let `B_0` be the common zero locus of `P` and `Q` on
the available roots.  If a residual support contains a subset `C subset B_0`,
then every direction `A in V(U,W)` vanishes on `C`.  Since the domain roots are
distinct, `ell_C` divides every direction `A`, and the DKI identity gives the
fixed-root slice

```text
H_{q,q+d-|C|}(s)(ell_W ell_C A_C)=0.
```

Similarly, if `lambda=[a:b]` is a non-base projective fiber, then

```text
Q_lambda=bP-aQ
```

is a nonzero direction in `V(U,W)` and its zero set contains exactly that
fiber off the base locus.  Any support subset `C` contained in this fiber
therefore satisfies `ell_C | Q_lambda`, and again yields the fixed-divisor slice

```text
H_{q,q+d-|C|}(s)(ell_W ell_C Q_C)=0.
```

Thus the two ways to defeat the cross-fiber good-pair packing bound are already
accounted for by fixed-root, quotient-periodic, or aperiodic slice ledgers.  In
particular, the remaining `b=2` M1 work is not to handle a new kind of
two-dimensional residual kernel, but to bound how often these fixed-divisor
base and projective-fiber slices can occur.

The verifier now checks this dictionary whenever `b(U,W)=2`: every base root is
a zero of the whole residual direction space, and every projective fiber is cut
out by the nonzero direction `bP-aQ`.  The current largest `F_7^*` scan has no
`b(U,W)=2` produced anchor.

## Small b=2 Root-Shadow Height Forces Packing

The previous section turns concentration into a fixed-divisor root-shadow
problem.  There is an exact packing consequence.  In the `b=2` notation, put

```text
h=max(|B_0|, max_lambda |ev^{-1}(lambda)|).
```

Thus `h` is the largest available-root set cut out either by the common base
locus or by one nonzero projective direction `bP-aQ`.  When a residual support
exists, `h>=1`, and every residual support `R` satisfies

```text
a(R)<=h,        r_lambda(R)<=h for all lambda.
```

Substituting `A=M=h` into (PF2-conc) gives a uniform lower bound

```text
g(R) >= gamma_2(q,h),
```

where, with `L=q-h`,

```text
gamma_2(q,h)
 =
binom(L,2)
 - ( floor(L/h) binom(h,2)
     + binom(L mod h,2) ).
```

Therefore, if `gamma_2(q,h)>0`, the cross-fiber packing bound gives

```text
|F(U,W)| <= floor(G_tot/gamma_2(q,h)).            (PF2-height)
```

In particular, `gamma_2(q,h)>0` exactly when `h<q/2`: after removing at most
`h` base-locus roots, the remaining `q-h` roots cannot all fit inside one
projective fiber of capacity `h`, so every residual support contains at least
one good cross-fiber pair.  Hence the only `b=2` residual branch not closed by
good-pair packing must contain a fixed-divisor slice with at least `q/2`
available roots.  The problem has moved from diffuse two-dimensional residual
kernel multiplicity to a large fixed-divisor root-shadow ledger.

The verifier now checks (PF2-height) whenever `b(U,W)=2`, using the same base
locus and projective fibers as the exact bad-pair audit.  The current largest
`F_7^*` scan has no `b(U,W)=2` produced anchor.

## Half-Height b=2 Shadows Are Short Quotient Kernels

The half-height survivor in the preceding section has a sharper algebraic
form.  Let `S` be either the base locus `B_0` or one non-base projective fiber,
and write `h=|S|`.  Suppose `h>=q/2`.

If `S=B_0`, every direction `A in V(U,W)` vanishes on `S`; if
`S=ev^{-1}([a:b])`, the nonzero direction

```text
Q_S=bP-aQ
```

vanishes on `S`.  In both cases there is a nonzero direction `A_S in V(U,W)`
and a quotient polynomial `R_S` such that

```text
A_S = ell_S R_S,        deg R_S < q-h <= q/2.
```

By (DKI), this gives the short quotient Hankel kernel

```text
H_{q,q+d-h}(s)(ell_W ell_S R_S)=0.              (PF2-short)
```

Thus a `b=2` residual branch that survives the root-shadow-height packing
bound is not merely a large-root phenomenon.  It supplies a concrete low-width
quotient kernel, with quotient width at most half of the residual degree.  A
proof that these half-width quotient kernels are absent or charged by the
quotient-periodic, tangent, fixed-root, or aperiodic ledgers would close the
`b=2` persistent branch.

The verifier now checks (PF2-short) whenever `b(U,W)=2` and a base locus or
projective fiber has height at least `q/2`: it divides the relevant residual
direction by the shadow locator, checks the quotient width, reconstructs the
direction, and verifies the resulting Hankel-kernel equation after multiplying
by the fixed anchor.  The current largest `F_7^*` scan has no `b(U,W)=2`
produced anchor.

## Half-Height Base Loci Descend the Whole b=2 Pencil

There is a stronger conclusion in the base-locus half-height case.  If
`h=|B_0|>=q/2`, then every direction in `V(U,W)=<P,Q>` is divisible by
`ell_{B_0}`.  Hence

```text
V(U,W)=ell_{B_0} V',
dim V'=2,
V' subset F[X]_{<q-h},
q-h<=q/2.                                      (PF2-base-desc)
```

Moreover the projective fiber map outside the base locus is unchanged after
division.  For `x notin B_0`,

```text
(P(x),Q(x)) = ell_{B_0}(x) (P'(x),Q'(x)),
ell_{B_0}(x) != 0,
```

so

```text
[P(x):Q(x)] = [P'(x):Q'(x)].
```

Thus a large base locus does not leave a genuinely two-dimensional residual
object at degree `q`.  It descends the entire projective-packing problem to a
two-dimensional quotient pencil of degree `<q-h<=q/2`.  The remaining base
half-height obstruction is therefore a lower-width quotient-pencil problem,
while a non-base half-height fiber remains a single short quotient direction as
in (PF2-short).

The verifier now checks this descent whenever `b(U,W)=2` and `|B_0|>=q/2`: it
divides both basis directions by `ell_{B_0}`, checks that the quotient basis
still has rank two, and verifies that the quotient projective evaluation map
agrees with the original one off `B_0`.  The current largest `F_7^*` scan has
no `b(U,W)=2` produced anchor.

## Zero-Good b=2 Supports Carry Half-Width Certificates

The preceding height reductions can be localized to individual residual
supports.  Let `R` be a residual support in the fixed-anchor fiber, and suppose
its cross-fiber good-pair count is zero:

```text
g(R)=0.
```

Then all non-base roots of `R` lie in a single projective fiber.  Indeed, two
non-base roots in distinct fibers would themselves be a good pair.  Writing

```text
a=|R cap B_0|,        m=max_lambda |R cap ev^{-1}(lambda)|,
```

we have `q=a+m`, hence either `a>=q/2` or `m>=q/2`.

Therefore every residual support not charged by the good-pair packing sum
carries a support-local half-width quotient certificate:

1. If `a>=q/2`, then `C=R cap B_0` is a common root set for the whole direction
   pencil, so `V(U,W)=ell_C V_C` with quotient width `<q-|C|<=q/2`.
2. If `m>=q/2`, then for the unique occupied non-base fiber `lambda`, the
   direction `Q_lambda` satisfies `Q_lambda=ell_C R_C` on
   `C=R cap ev^{-1}(lambda)`, again with `deg R_C<q-|C|<=q/2`.

Thus the `b=2` fixed-anchor fiber splits into a packable part, where
`g(R)>0`, and a certified part, where each uncharged support supplies a
half-width fixed-divisor quotient kernel.  The remaining task is no longer to
control diffuse residual supports; it is to count or charge these explicit
half-width certificates.

The verifier now checks this support-local split whenever `b(U,W)=2`: every
residual candidate with `g(R)=0` must have a base-heavy or fiber-heavy subset
of size at least `q/2`, and the corresponding half-width quotient-kernel
identity is verified directly.  The current largest `F_7^*` scan has no
`b(U,W)=2` produced anchor.

## Zero-Good Envelope Gives a b=2 Fixed-Anchor Closure

The support-local split gives an explicit closure bound for the whole fixed
anchor.  Let

```text
s=|B_0|,        m_lambda=|ev^{-1}(lambda)|.
```

The zero-good support envelope is

```text
Z_0^{env}(U,W)
 =
1_{s>=q} binom(s,q)
 + sum_lambda sum_{r=1}^q binom(m_lambda,r) binom(s,q-r).       (PF2-Z0)
```

This is the exact number of `q`-subsets whose non-base roots lie in at most one
projective fiber: either all `q` roots lie in the base locus, or there is a
unique occupied non-base fiber and `r>=1` roots are chosen from it.  Hence every
zero-good residual support is counted by `Z_0^{env}`.

The positive-good supports are counted by good pairs.  Since no good pair can
occur in two residual supports, choosing one good pair from each support with
`g(R)>0` injects that part of the fiber into the total good-pair set.  Therefore

```text
|F(U,W)| <= G_tot + Z_0^{env}(U,W).              (PF2-Z0-close)
```

Together with the previous section, every term in `Z_0^{env}` is a half-width
fixed-divisor certificate ledger whenever it actually contributes an uncharged
residual support.  Thus the `b=2` residual problem is reduced to the good-pair
packing term plus an explicit half-width zero-good envelope.

The verifier now computes `Z_0^{env}` from the same base locus and projective
fibers, checks that every zero-good residual candidate lies in this envelope,
and asserts (PF2-Z0-close).  The current largest `F_7^*` scan has no
`b(U,W)=2` produced anchor.

## Zero-Good Supports Are Half-Certificate Incidences

The zero-good envelope can be charged to half-width certificates uniformly.
Put

```text
c=ceil(q/2),        N=|D'|,
H_c(U,W)=binom(s,c)+sum_lambda binom(m_lambda,c).
```

Every zero-good `q`-support has all non-base roots in at most one projective
fiber.  If it has `a` roots in the base locus and `m` roots in that occupied
fiber, then `a+m=q`.  Hence `max(a,m)>=c`, so the support contains a
`c`-subset either in `B_0` or in one projective fiber.  Counting incidences
between zero-good supports and such `c`-subsets gives

```text
Z_0^{env}(U,W) <= H_c(U,W) binom(N-c,q-c).       (PF2-half-cert)
```

Combining this with the good-pair injection yields the fixed-anchor closure

```text
|F(U,W)| <= G_tot + H_c(U,W) binom(N-c,q-c).     (PF2-half-cert-close)
```

Each counted `c`-subset is one of the half-width fixed-divisor certificates
from the previous support-local split: either a base-locus certificate shared
by the whole pencil or a single projective-fiber quotient direction.  Thus the
remaining zero-good term is controlled by the number of half-width
fixed-divisor certificate subsets, times the trivial residual completions.

The verifier computes `H_c(U,W)` from the same base locus and projective
fibers, checks that the observed zero-good supports satisfy (PF2-half-cert),
and asserts (PF2-half-cert-close).  The current largest `F_7^*` scan still has
no `b(U,W)=2` produced anchor.

## Half-Certificate Completions Stay in Their Own Shadows

The previous incidence bound used the coarse completion factor
`binom(N-c,q-c)`.  The zero-good structure gives a sharper local version: once
the half-certificate is fixed, its completions cannot range over all of `D'`.

For a base certificate `C subset B_0`, the remaining `q-c` roots must lie in
`B_0\C` together with at most one projective fiber.  Thus one fixed base
certificate has at most

```text
B_c
 =
 binom(s-c,q-c)
 + sum_lambda sum_{r=1}^{q-c}
     binom(m_lambda,r) binom(s-c,q-c-r)
```

zero-good completions.  For a fiber certificate
`C subset ev^{-1}(lambda)`, the remaining roots must lie in
`B_0 union (ev^{-1}(lambda)\C)`, so one fixed certificate in the `lambda`
fiber has at most

```text
F_{c,lambda}
 =
 sum_{r=0}^{q-c}
   binom(m_lambda-c,r) binom(s,q-c-r)
```

zero-good completions.  Since every zero-good support contains either a base
`c`-certificate or a fiber `c`-certificate, the envelope satisfies

```text
Z_0^{env}(U,W)
 <= binom(s,c) B_c
    + sum_lambda binom(m_lambda,c) F_{c,lambda}.  (PF2-local-half-cert)
```

Consequently

```text
|F(U,W)|
 <= G_tot
    + binom(s,c) B_c
    + sum_lambda binom(m_lambda,c) F_{c,lambda}.  (PF2-local-close)
```

This removes the artificial global `N`-completion loss from the zero-good
half-certificate ledger.  Fiber certificates only need a bound for their own
projective root shadow, while base certificates see only the base locus plus
one projective shadow at a time.

The verifier computes the local completion bound, checks that it dominates the
exact zero-good envelope, checks that it is no larger than the coarse global
half-certificate incidence bound, and asserts (PF2-local-close).  The current
largest `F_7^*` scan still has no `b(U,W)=2` produced anchor.

## The Degree Gap Eliminates Zero-Good b=2 Supports

In a genuine `b=2` residual direction space, the preceding zero-good envelope
is actually empty.  The local-shadow form makes the reason visible.

For `lambda=[a:b] in P^1`, put

```text
S_lambda=B_0 union ev^{-1}(lambda).
```

Then `S_lambda` is contained in the zero set on `D'` of the nonzero direction

```text
Q_lambda=bP-aQ.
```

Since `P,Q` are linearly independent directions of degree `<q`, the polynomial
`Q_lambda` is not zero and has degree `<q`.  Hence

```text
|S_lambda| <= q-1.                              (PF2-shadow-gap)
```

The base locus itself is also contained in the zero set of the nonzero
polynomial `P`, so `|B_0|<=q-1`.  Therefore no `q`-element residual support can
lie in the base locus, and no `q`-element support can lie in
`B_0 union ev^{-1}(lambda)` for a single projective fiber.  Equivalently,

```text
Z_0^{env}(U,W)=0.                               (PF2-Z0-vanish)
```

Thus every residual support in a `b=2` fixed-anchor fiber contains at least one
cross-fiber good pair.  The good-pair injection now gives the unconditional
`b=2` fixed-anchor packing bound

```text
|F(U,W)| <= G_tot.                              (PF2-degree-gap-close)
```

This closes the zero-good branch of the `b=2` persistent residual problem.  The
remaining `b=2` work is to sum or charge the good-pair ledger itself in the
global M1 residue-line packing, not to control a separate uncharged
zero-good family.

The verifier rewrites the zero-good envelope as

```text
binom(s,q)+sum_lambda (binom(s+m_lambda,q)-binom(s,q)),
```

checks the shadow gap `s+m_lambda<q` for every projective fiber, asserts
`Z_0^{env}=0`, and verifies the direct closure `|F(U,W)|<=G_tot`.  The current
largest `F_7^*` scan still has no `b(U,W)=2` produced anchor.

## Good Pairs Interpolate the b=2 Residual Locator

The degree-gap closure has a constructive form.  Fix one locator
`L_0 in K(U,W)` as an origin for the affine kernel and write

```text
K(U,W)=L_0+span(P,Q).
```

If `{x,y}` is a good pair, then the matrix

```text
E_{x,y}=
[[P(x),Q(x)],
 [P(y),Q(y)]]
```

has nonzero determinant by definition.  Therefore there is at most one locator
in the affine kernel that vanishes at both `x` and `y`; explicitly it is

```text
L_{x,y}=L_0+alpha P+beta Q,
E_{x,y} [alpha beta]^T = -[L_0(x) L_0(y)]^T.     (PF2-good-interp)
```

If `R` is a residual support containing the good pair `{x,y}`, then its monic
locator is exactly `L_{x,y}`.  Since the degree gap shows that every residual
support contains at least one good pair, the fixed-anchor residual fiber is
not merely bounded by the good-pair ledger; it is contained in the explicit
image of the good-pair interpolation map

```text
{good pairs in D'} -> K(U,W).
```

This gives a canonical reconstruction certificate for every `b=2` residual
support after the zero-good branch has been eliminated.  The remaining global
M1 task can therefore treat the `b=2` branch as an explicit good-pair image
problem.

The verifier checks (PF2-good-interp) for every good pair contained in every
enumerated `b=2` residual candidate: solving the displayed `2 x 2` system
against a fixed origin locator must reconstruct the candidate locator exactly.
The current largest `F_7^*` scan still has no `b(U,W)=2` produced anchor.

## The b=2 Fiber Is the Split Image of Good-Pair Interpolation

The interpolation map gives an exact parametrization after imposing the
ordinary split-locator condition.  For each good pair `e={x,y}`, let
`L_e=L_{x,y}` be the interpolated monic degree-`q` locator from
(PF2-good-interp), and put

```text
Split(e) = { roots of L_e in D' }.
```

Then the fixed-anchor residual fiber is exactly

```text
F(U,W)
 =
{ Split(e) :
  e is a good pair,
  |Split(e)|=q,
  ell_{Split(e)}=L_e }.                          (PF2-good-image)
```

Indeed, if `R in F(U,W)`, the degree-gap lemma gives a good pair
`e subset R`, and (PF2-good-interp) reconstructs `ell_R`, so `R` appears in
the displayed image.  Conversely, if `L_e` splits as the locator of a
`q`-subset of `D'`, then `L_e in K(U,W)` because it is the origin locator plus
a residual direction, so that root set is a residual support in `F(U,W)`.

Thus the `b=2` fixed-anchor problem is no longer a search over all
`q`-subsets.  It is a two-root interpolation problem followed by the single
question of whether the interpolated monic locator splits completely over the
available domain.

The verifier now computes this image over all good pairs, checks that every
split image is an enumerated residual candidate, that every residual candidate
appears in the image, and that the image-pair count agrees with the owned
good-pair incidence count.  The current largest `F_7^*` scan still has no
`b(U,W)=2` produced anchor.

## Good-Pair Image Fibers Are Internal Good-Pair Sets

The split-image parametrization has an exact fiber count.  Let

```text
I = { e good : L_e splits as ell_R for some R subset D', |R|=q }.
```

The map

```text
pi:I -> F(U,W),        pi(e)=roots_{D'}(L_e)
```

is surjective by (PF2-good-image).  Its fiber over `R` is exactly the set of
good pairs contained in `R`:

```text
pi^{-1}(R) = { e subset R : e is good }.         (PF2-good-fibers)
```

One inclusion follows from construction: if `e subset R`, then interpolation
reconstructs `ell_R`, so `pi(e)=R`.  Conversely, if `pi(e)=R`, then `L_e`
vanishes at both roots of `e`, and `roots_{D'}(L_e)=R`, so `e subset R`.
Thus

```text
|I| = sum_{R in F(U,W)} g(R).
```

Equivalently,

```text
|F(U,W)| = sum_{e in I} 1/g(pi(e)).
```

This is the exact weighted form behind the good-pair packing bound.  It
identifies the remaining `b=2` ledger as a split-good-pair image with fiber
weights given by the internal cross-fiber good-pair counts of the split
support.

The verifier counts the good pairs inside every residual candidate, counts the
preimages of each candidate under the split-good-pair image, and checks that
the two counts agree support by support.  The current largest `F_7^*` scan
still has no `b(U,W)=2` produced anchor.

## Good-Pair Images Descend to Two-Root Quotient Locators

The split condition in (PF2-good-image) has a lower-width form.  Since
`L_e` is constructed to vanish at the good pair `e={x,y}`, one has a unique
monic quotient

```text
L_e=ell_e M_e,        deg M_e=q-2.               (PF2-good-quot)
```

Moreover `L_e in K(U,W)`, so after absorbing the good pair into the fixed
anchor, the quotient satisfies the two-root fixed-divisor Hankel identity

```text
H_{q,q+d-2}(s)(ell_W ell_e M_e)=0.              (PF2-good-quot-kernel)
```

Thus `L_e` splits as a residual support if and only if `M_e` splits as a
squarefree degree-`q-2` locator on `D'\e`.  In that case

```text
roots_{D'}(L_e)=e union roots_{D'\e}(M_e).
```

The remaining `b=2` split-image test is therefore a two-root absorbed
quotient-locator test of width `q-2`, not a fresh degree-`q` residual search.
This is the fixed-divisor form of the good-pair endpoint.

The verifier divides every interpolated good-pair locator by `ell_e`, checks
the quotient reconstruction, verifies (PF2-good-quot-kernel), and checks that
splitting of `L_e` is equivalent to splitting of the quotient `M_e` on the
available roots away from `e`.  The current largest `F_7^*` scan still has no
`b(U,W)=2` produced anchor.

## Quotient Roots Are a Three-Row Determinant Gate

The two-root quotient roots have an explicit one-variable gate.  For
`z in D'\e`, the condition `M_e(z)=0` is equivalent to `L_e(z)=0`, because
`ell_e(z) != 0`.  Writing `e={x,y}`, the coefficients of `L_e` are determined
by the two equations `L_e(x)=L_e(y)=0`.  Hence `z` is a quotient root exactly
when the three equations at `x,y,z` are compatible:

```text
Delta_e(z)=
det
[
  L_0(x)  P(x)  Q(x)
  L_0(y)  P(y)  Q(y)
  L_0(z)  P(z)  Q(z)
]
=0.                                                (PF2-det-gate)
```

The `2 x 2` good-pair determinant in the `(P,Q)` columns is nonzero, so this
determinant condition is equivalent to the unique interpolated locator through
`x,y` also vanishing at `z`.

Thus the remaining quotient split test can be read as follows: after choosing
a good pair, the possible remaining roots are exactly the zeros of the
determinant gate `Delta_e` on `D'\e`, and splitting asks whether this gate
selects a squarefree locator of degree `q-2`.

The verifier checks this determinant description for every good pair: the
roots of `Delta_e` away from the pair must agree exactly with the roots of the
two-root quotient locator `M_e`.  The current largest `F_7^*` scan still has
no `b(U,W)=2` produced anchor.

## The Determinant Gate Is the Normalized Interpolated Locator

The determinant gate introduces no new polynomial.  Let

```text
D_e=
det [[P(x),Q(x)],[P(y),Q(y)]] != 0.
```

Expanding `Delta_e(z)` along the third row gives

```text
Delta_e(z)
 =
D_e L_0(z)
 +(Q(x)L_0(y)-L_0(x)Q(y)) P(z)
 +(L_0(x)P(y)-P(x)L_0(y)) Q(z).
```

The two coefficients of `P,Q`, divided by `D_e`, are exactly the interpolation
coefficients `alpha,beta` in (PF2-good-interp).  Hence

```text
Delta_e = D_e L_e.                              (PF2-det-normal)
```

Since `L_e=ell_e M_e`, it follows that

```text
Delta_e/ell_e = D_e M_e.                       (PF2-det-quot)
```

Thus the determinant gate, the interpolated locator, and the two-root quotient
locator are the same object up to the nonzero scalar `D_e` and the forced
factor `ell_e`.  The endpoint may therefore be studied either as a determinant
gate or as the normalized quotient `M_e` without changing the root set.

The verifier checks the coefficient identity (PF2-det-normal) and, after
division by the good-pair locator, the quotient identity (PF2-det-quot) for
every good pair.  The current largest `F_7^*` scan still has no `b(U,W)=2`
produced anchor.

## b=2 Fixed-Anchor Endpoint Theorem

Combining the preceding sections gives the fixed-anchor endpoint for the first
persistent positive-dimensional case.

Let `(U,W)` be a deficit anchor with residual size `q`, available domain `D'`,
and residual direction dimension `b(U,W)=2`.  Choose an origin locator
`L_0 in K(U,W)` and a direction basis `P,Q` for `Dir K(U,W)`.  Let `B_0` be
the common zero locus of `P,Q`, let projective fibers be defined by
`[P(x):Q(x)]`, and let a pair be good when it avoids `B_0` and has distinct
projective values.

Then:

1. The zero-good branch is empty:

```text
Z_0^{env}(U,W)=0.
```

2. Every residual support contains a good pair, and the fixed-anchor residual
fiber is the split image of the good-pair interpolation map:

```text
F(U,W)
 =
{ roots_{D'}(L_e) :
  e good, |roots_{D'}(L_e)|=q, ell_{roots_{D'}(L_e)}=L_e }.
```

3. The image fiber over `R in F(U,W)` is exactly the set of good pairs inside
`R`, so, for the split-good-pair domain `I`,

```text
|I|=sum_{R in F(U,W)} g(R),
|F(U,W)|=sum_{e in I} 1/g(pi(e)).
```

4. For `e={x,y}`, the interpolated locator factors as

```text
L_e=ell_e M_e,
```

where `M_e` is a degree-`q-2` quotient satisfying the absorbed fixed-divisor
Hankel identity.  Equivalently, quotient roots are cut out by the determinant
gate `Delta_e`, and

```text
Delta_e=D_e L_e,        Delta_e/ell_e=D_e M_e,
D_e=det [[P(x),Q(x)],[P(y),Q(y)]] != 0.
```

Consequently the `b=2` fixed-anchor problem is no longer a diffuse residual
`q`-subset problem.  It is a weighted good-pair image, and each image point is
a two-root absorbed quotient-locator/determinant-gate split test of width
`q-2`.  The remaining M1 work in this branch is global: charge these good-pair
determinant gates across anchors using fixed-root, quotient-periodic, tangent,
or aperiodic residue-packing input.

The verifier audits every component of this endpoint theorem in finite scans:
projective fiber normal form, zero-good vanishing, good-pair interpolation,
split-image equality, image-fiber weights, two-root quotient descent, and
determinant normalization.  The current largest `F_7^*` scan still has no
`b(U,W)=2` produced anchor.

## Global b=2 Ledger Reduction

The endpoint theorem converts the local `b=2` branch into a global ledger
target.  Let `A_2` be any family of produced deficit anchors with
`b(U,W)=2`.  For `A=(U,W) in A_2`, write

```text
I_A={ e good for A : Delta_{A,e}/ell_e splits over D'_A\e },
pi_A(e)=roots_{D'_A}(L_{A,e}),
g_A(R)=# good pairs of A contained in R.
```

Then the total residual contribution of all `b=2` anchors in the family is

```text
sum_{A in A_2} |F(A)|
 =
sum_{A in A_2} sum_{e in I_A} 1/g_A(pi_A(e)).   (PF2-global-ledger)
```

Equivalently, the unweighted split-good-pair count satisfies

```text
sum_{A in A_2} |I_A|
 =
sum_{A in A_2} sum_{R in F(A)} g_A(R).
```

Thus the remaining `b=2` task is not to control residual supports after an
anchor has been fixed.  It is to charge the global family of determinant gates

```text
(A,e) -> Delta_{A,e}/ell_e
```

with the reciprocal weight `1/g_A(pi_A(e))` when the gate splits.  Fixed-root,
quotient-periodic, tangent, and aperiodic residue-packing estimates can now be
applied directly to this determinant-gate ledger.

This is the precise handoff from the local fixed-anchor argument to the global
M1 residue-line packing problem.  A future proof can close the `b=2` branch by
showing that the weighted split determinant-gate count in
(PF2-global-ledger) is polynomial after the existing reserve charges.

## Weighted Determinant-Gate Escape Filter

The reciprocal weight in (PF2-global-ledger) is controlled by the same
projective-fiber occupancy that produced the earlier good-pair packing bounds.
For a fixed anchor `A` and residual support `R`, write

```text
a_A(R)=|R cap B_0|,
L_A(R)=q-a_A(R),
m_A(R)=max_lambda |R cap ev^{-1}(lambda)|,
e_A(R)=L_A(R)-m_A(R).
```

Here `L_A(R)` is the number of non-base roots and `e_A(R)` is the number of
non-base roots outside a largest projective fiber.  If
`r_lambda(R)=|R cap ev^{-1}(lambda)|`, then good pairs are exactly cross-fiber
pairs, so

```text
g_A(R)
 = 1/2 ( L_A(R)^2 - sum_lambda r_lambda(R)^2 )
 = sum_{lambda<mu} r_lambda(R) r_mu(R).          (PF2-weight-count)
```

Since `sum_lambda r_lambda(R)^2 <= m_A(R)L_A(R)`, this gives the escape bound

```text
g_A(R) >= L_A(R)e_A(R)/2,
e_A(R) <= 2g_A(R)/L_A(R).                       (PF2-weight-escape)
```

Thus the only split determinant gates carrying a large reciprocal weight are
near a single projective fiber after the base-locus roots are removed.  In
cutoff form, fix integers `A_0<q` and `c>=1`.  Every split support with

```text
a_A(R) <= A_0,        e_A(R) >= c
```

has

```text
1/g_A(R) <= 2/(c(q-A_0)).                       (PF2-generic-weight)
```

Consequently the global weighted determinant-gate ledger decomposes into:

1. a generic part with the explicit reciprocal saving (PF2-generic-weight);
2. base-heavy supports, where `a_A(R)>A_0`;
3. near-fiber supports, where all but fewer than `c` non-base roots lie in one
   projective fiber.

The latter two pieces are exactly fixed-divisor/projective-fiber
residue-line charges: the base locus is the common zero set of the residual
direction space, while each projective fiber is cut out by a nonzero direction
`bP-aQ`.  Thus (PF2-weight-escape) is the promised bridge from the local
weighted determinant gates to the global M1 charging problem: generic gates
pay a denominator, and non-generic gates carry a visible residue-line slice to
charge separately.

The verifier already checks the exact count (PF2-weight-count) for every
residual candidate in its `b(U,W)=2` branch.  It now also checks the
dominant-fiber escape lower bound in (PF2-weight-escape).

## Non-Generic Weighted Gates Have Dominant-Slice Quotients

The exceptional parts in the preceding cutoff decomposition are not merely
large-weight labels.  They carry explicit fixed-divisor certificates.

First suppose a split support `R` is not base-heavy, so `a_A(R)<=A_0`, but is
near one projective fiber, so `e_A(R)<c`.  Let `lambda` be a projective fiber
with largest occupancy and put

```text
C=R cap ev_A^{-1}(lambda).
```

Then

```text
|C| = L_A(R)-e_A(R) >= q-A_0-c+1,
q-|C| <= A_0+c-1.                               (PF2-near-width)
```

If `lambda=[a:b]`, the nonzero direction `Q_lambda=bP-aQ` vanishes on
`ev_A^{-1}(lambda)`, hence on `C`.  Therefore

```text
Q_lambda=ell_C Q'_lambda,
deg Q'_lambda < q-|C| <= A_0+c-1,
H(s)(ell_W ell_C Q'_lambda)=0.                  (PF2-near-quot)
```

Thus the near-fiber exceptional weighted gates are bounded-complement quotient
kernels once `A_0` and `c` are fixed.  They are not a new positive-dimensional
residual family.

The base-heavy exception is also a fixed-divisor charge.  If `a_A(R)>A_0`,
then `R cap B_0` contains an `(A_0+1)`-subset `C_0`, and every direction in
`Dir K(A)` vanishes on `C_0`.  Thus each basis direction has a quotient

```text
P=ell_{C_0}P',        Q=ell_{C_0}Q',
H(s)(ell_W ell_{C_0}P')=
H(s)(ell_W ell_{C_0}Q')=0.                      (PF2-base-quot)
```

For the full dominant base slice `C=R cap B_0`, the quotient width is exactly
`q-|C|`.  Hence base-heavy gates are charged to common-base fixed-divisor
slices, while near-fiber gates are charged to the bounded-complement
projective-fiber quotient in (PF2-near-quot).

The verifier audits the stronger support-local form: for every residual
candidate it chooses the larger of `R cap B_0` and the largest projective-fiber
slice, divides the relevant residual direction(s) by that locator, checks the
quotient reconstruction, and checks that the quotient width equals the
complement size.  The cutoff claims above are immediate consequences.

## Cutoff Ledger Reduction for the b=2 Branch

Combining the weighted ledger, the escape filter, and the dominant-slice
quotient certificates gives a concrete reduction theorem for the whole `b=2`
branch.

Let `A_2` be a family of produced `b=2` anchors.  Fix cutoffs
`A_0<q` and `c>=1`.  For each residual support `R in F(A)`, put it in exactly
one of the following classes:

```text
G_A = { R : a_A(R)<=A_0 and e_A(R)>=c },
B_A = { R : a_A(R)>A_0 },
N_A = { R : a_A(R)<=A_0 and e_A(R)<c }.
```

Let

```text
I_A^G={ e in I_A : pi_A(e) in G_A }.
```

Then (PF2-global-ledger) and (PF2-generic-weight) give

```text
sum_{A in A_2} |F(A)|
 <=
  2/(c(q-A_0)) sum_{A in A_2} |I_A^G|
  + sum_{A in A_2} |B_A|
  + sum_{A in A_2} |N_A|.                       (PF2-cutoff-ledger)
```

Indeed the supports in `G_A` are counted through their good-pair preimages,
each with weight at most `2/(c(q-A_0))`, while the two exceptional support
classes are counted once each.

The two exceptional terms are not opaque.  The `B_A` term is a common-base
fixed-divisor ledger: every `R in B_A` contains an `(A_0+1)`-subset of
`B_0`, and every residual direction descends after this fixed divisor.  The
`N_A` term is a projective-fiber bounded-complement quotient ledger: every
`R in N_A` has a dominant projective-fiber slice `C` with

```text
q-|C| <= A_0+c-1,
```

and the nonzero direction cutting that projective fiber descends to the
quotient kernel (PF2-near-quot).

Thus the local `b=2` branch is closed by any three external polynomial bounds:

1. an unweighted bound for the generic split determinant gates `I_A^G`;
2. a bound for the common-base fixed-divisor ledger `B_A`;
3. a bound for the bounded-complement projective-fiber quotient ledger `N_A`.

This is the current sharp form of the `b=2` M1 target.  It isolates exactly
where the remaining all-line residue-packing input must enter; no further
fixed-anchor residual enumeration is left in this branch.

## Common-Base Ledger Descends by Fixed-Subset Incidence

The first exceptional term in (PF2-cutoff-ledger) has an exact quotient
incidence form.  Fix a `b=2` anchor `A`, an origin locator `L_0`, direction
basis `P,Q`, and let

```text
B_0^*(A)=B_0 cap roots_{D'}(L_0).
```

Only roots in `B_0^*(A)` can occur as base roots of a residual support: if
`R in F(A)` and `x in R cap B_0`, then `P(x)=Q(x)=0` and
`L_R=L_0+alpha P+beta Q` gives `L_0(x)=L_R(x)=0`.

Now fix `d>=1` and a `d`-subset `C subset B_0^*(A)`.  Define the quotient
fiber

```text
F_C(A)={
  R' subset D'\C :
  |R'|=q-d and ell_C ell_{R'} in K(A)
}.
```

Multiplication by `ell_C` gives a bijection between `F_C(A)` and the residual
supports `R in F(A)` with `C subset R cap B_0`.  Indeed, if such an `R`
contains `C`, then `ell_R=ell_C ell_{R\C}`.  Conversely every
`R' in F_C(A)` gives the split support `C union R'`.
The whole affine pencil descends after `C`: since `C subset B_0^*(A)`,

```text
L_0=ell_C L_{0,C},        P=ell_C P_C,        Q=ell_C Q_C,
```

and the quotient supports are exactly the split locators in

```text
L_{0,C}+span(P_C,Q_C)
```

with fixed divisor `ell_W ell_C`.

Consequently, for `d=A_0+1`,

```text
sum_{C subset B_0^*(A), |C|=d} |F_C(A)|
 =
sum_{R in F(A)} binom(a_A(R),d),                (PF2-base-incidence)
```

and therefore

```text
|B_A| <=
sum_{C subset B_0^*(A), |C|=A_0+1} |F_C(A)|.   (PF2-base-ledger)
```

Thus the common-base exceptional ledger is not a new `b=2` residual object.  It
is an incidence sum of lower-width fixed-divisor quotient fibers.  Any
polynomial bound for these descended fixed-divisor fibers closes the `B_A`
term in (PF2-cutoff-ledger).

The verifier checks the support-local descent used here: whenever a residual
candidate contains base roots, those roots also vanish on the origin locator;
after dividing by their locator, the residual support quotient is the expected
complement locator and each direction basis vector remains in the corresponding
fixed-divisor Hankel kernel.

## Near-Fiber Ledger Descends to Quotient Lines

The second exceptional term in (PF2-cutoff-ledger) has the same fixed-subset
form, but now the descended object is one-dimensional.  Assume
`1<=c<=q-A_0` and put

```text
h=q-A_0-c+1.
```

For `R in N_A`, choose a projective fiber `lambda` of maximal occupancy.  By
definition of `N_A`,

```text
|R cap ev_A^{-1}(lambda)| >= h.
```

Thus every near-fiber support contains an `h`-subset `C` inside a single
non-base projective fiber.  For a projective fiber `lambda=[a:b]`, let
`Q_lambda=bP-aQ`, so `Q_lambda` vanishes on the fiber.  For
`C subset ev_A^{-1}(lambda)`, `|C|=h`, define

```text
F_{lambda,C}(A)={
  R' subset D'\C :
  |R'|=q-h and ell_C ell_{R'} in K(A)
}.
```

Multiplication by `ell_C` identifies `F_{lambda,C}(A)` with the residual
supports containing `C`.  If this fiber is nonempty, choose one locator
`L_C in K(A)` divisible by `ell_C`.  Since evaluation of `span(P,Q)` on a
non-base projective fiber has rank one, the directions vanishing on `C` form
the line `span(Q_lambda)`.  Hence all locators in `K(A)` divisible by `ell_C`
are exactly

```text
L_C + span(Q_lambda),
```

and after division by `ell_C` the quotient supports lie in the affine quotient
line

```text
L_C/ell_C + span(Q_lambda/ell_C)
```

of width

```text
q-h=A_0+c-1.                                    (PF2-near-line-width)
```

Consequently

```text
|N_A| <=
sum_lambda sum_{C subset ev_A^{-1}(lambda), |C|=h}
  |F_{lambda,C}(A)|.                            (PF2-near-ledger)
```

This reduces the near-fiber exceptional term to bounded-width quotient-line
fibers.  Together with (PF2-base-ledger), the only pieces left by
(PF2-cutoff-ledger) are the generic split determinant-gate count and explicit
lower-width quotient ledgers.

The verifier audits the support-local quotient descent for the dominant
projective-fiber slice of every residual candidate: it divides the support
locator by the dominant slice locator, checks that the quotient locator is the
complement support, and checks that the projective-fiber direction descends to
the corresponding fixed-divisor Hankel kernel.

## Constant-Width b=2 Corollary

The cutoff theorem has a useful fixed-width specialization.  Fix an integer
`w` with `0<=w<q`, and set

```text
A_0=0,        c=w+1,        h=q-w.
```

Then every residual support is in one of three classes:

1. `a_A(R)=0` and `e_A(R)>=w+1` (generic);
2. `a_A(R)>0` (base-touching);
3. `a_A(R)=0` and `e_A(R)<=w` (near one projective fiber).

Let

```text
I_A^{gen,w}={ e in I_A : pi_A(e) is generic for this choice }.
```

The cutoff ledger gives

```text
sum_{A in A_2} |F(A)|
 <=
  2/((w+1)q) sum_{A in A_2} |I_A^{gen,w}|
  + sum_{A in A_2} sum_{x in B_0^*(A)} |F_x(A)|
  + sum_{A in A_2} sum_lambda
      sum_{C subset ev_A^{-1}(lambda), |C|=q-w}
        |F_{lambda,C}(A)|.                     (PF2-width-w-ledger)
```

Here `F_x(A)` is the one-root common-base quotient fiber from
(PF2-base-ledger), and `F_{lambda,C}(A)` is the width-`w` quotient-line fiber
from (PF2-near-ledger).  Thus for each fixed `w`, the `b=2` branch is reduced
to:

1. a generic split determinant-gate count with explicit saving
   `2/((w+1)q)`;
2. one-root common-base fixed-divisor fibers;
3. width-`w` projective-fiber quotient-line fibers.

This is often the most convenient form for the global M1 argument: choose `w`
as a small constant to keep all non-generic quotient ledgers bounded-width,
then prove that the saved generic determinant-gate mass is polynomial after
the remaining aperiodic/quotient-periodic charges.

## Exact No-Base Good-Pair Saving

The width-zero case has a sharper elementary weight than the generic cutoff
constant.  Let `R` be a split support for a `b=2` anchor with

```text
a_A(R)=0.
```

Thus all `q` roots of `R` avoid the base locus `B_0`.  The degree-gap lemma
shows that no single non-base projective fiber can contain all roots of `R`:
each fiber is the zero set of a nonzero residual direction of degree `<q`.
Hence the largest projective fiber inside `R` has size at most `q-1`.

Since good pairs are exactly cross-fiber pairs,

```text
g_A(R)=sum_{lambda<mu} r_lambda(R)r_mu(R).
```

If the largest fiber has size `m`, then the pairs from that fiber to its
complement alone give

```text
g_A(R)>=m(q-m)>=q-1,        1<=m<=q-1.          (PF2-nobase-good)
```

The bound is sharp for a `(q-1,1)` fiber split.  Therefore every no-base split
support has reciprocal weight

```text
1/g_A(R) <= 1/(q-1),        q>=2.               (PF2-nobase-weight)
```

This improves the width-zero determinant-gate coefficient from the coarse
escape value `2/q` to the exact no-base value `1/(q-1)`.

The verifier asserts this lower bound for every audited `b=2` no-base
residual candidate in the existing projective-good-pair audit.

## No-Base Escape Profiles Descend to Quotient Lines

The previous bound can be kept profile-by-profile.  For a no-base support
`R`, write

```text
esc_A(R)=q-m_A(R),
```

where `m_A(R)` is the largest projective-fiber occupancy in `R`.  The
degree-gap exclusion gives

```text
1<=esc_A(R)<=q-1.
```

If `esc_A(R)=j`, then the largest projective fiber has size `q-j`, and the
pairs between that fiber and its complement already give

```text
g_A(R)>=j(q-j).                                (PF2-nobase-profile)
```

There is a sharper exact occupancy form.  For `1<=m<=q-1`, write

```text
q=a_m m+r_m,        0<=r_m<m,
Phi_q(m)=1/2 (q^2-a_m m^2-r_m^2).
```

If every projective fiber in `R` has size at most `m`, then

```text
sum_lambda r_lambda(R)^2 <= a_m m^2+r_m^2,
```

because the square sum is maximized by filling as many fibers of size `m` as
possible and one remaining fiber of size `r_m`.  Hence

```text
g_A(R)
 =1/2 (q^2-sum_lambda r_lambda(R)^2)
 >= Phi_q(m).                                  (PF2-nobase-occupancy)
```

Taking `m=m_A(R)=q-esc_A(R)` refines (PF2-nobase-profile); the two bounds
agree in the concentrated range `m>=q/2`, while (PF2-nobase-occupancy) gives
a strictly larger saving for supports with `m<q/2`.

For

```text
F^{nb}(A)={ R in F(A) : R cap B_0=empty },
I_{A,j}^{nb}={ e in I_A^{nb} : esc_A(pi_A(e))=j },
```

the no-base part of the weighted ledger therefore satisfies

```text
|F^{nb}(A)|
 <= sum_{j=1}^{q-1}
      (1/Phi_q(q-j)) |I_{A,j}^{nb}|.          (PF2-nobase-profile-ledger)
```

The dangerous small-escape profiles also have explicit quotient certificates.
Fix an escape cutoff `u` with `1<=u<q`.  If `esc_A(R)=j<u`, choose a dominant
projective fiber `lambda` and put `C=R cap ev_A^{-1}(lambda)`, so
`|C|=q-j`.  For `lambda=[a:b]`, the direction `Q_lambda=bP-aQ` vanishes on
`C`, hence

```text
Q_lambda=ell_C Q'_lambda,        deg Q'_lambda<j,
H(s)(ell_W ell_C Q'_lambda)=0.
```

As in the near-fiber descent, quotienting by `ell_C` puts the remaining roots
in a width-`j` projective-fiber quotient line `F_{lambda,C}(A)`.  Consequently

```text
|F^{nb}(A)|
 <=
  sum_{j=u}^{q-1} (1/Phi_q(q-j)) |I_{A,j}^{nb}|
  + sum_{j=1}^{u-1} sum_lambda
      sum_{C subset ev_A^{-1}(lambda), |C|=q-j}
        |F_{lambda,C}(A)|.                     (PF2-nobase-cutoff)
```

Thus the no-base determinant-gate endpoint is not a single undifferentiated
count.  One may either keep all profiles in the weighted determinant-gate
ledger, or move the small-escape profiles into bounded-width quotient-line
ledgers and leave only the larger-escape determinant gates.

## No-Base Occupancy Cutoff Ledger

The profile form gives a useful one-parameter cutoff.  Fix an integer

```text
0<=w<=q-2.
```

Put the no-base support `R` in the concentrated class if

```text
esc_A(R)<=w,
```

and in the spread class if `esc_A(R)>=w+1`.  Let `I_A^{nb,spread(w)}` be the
good-pair labels in `I_A^{nb}` whose image support is spread.  For a spread
support the largest projective fiber has size at most `q-w-1`; by monotonicity
of the extremal square-sum bound (allowing a larger maximum part can only
increase the maximum possible square sum),

```text
g_A(R)>=Phi_q(q-w-1).
```

The concentrated profiles have the quotient-line certificates from
(PF2-nobase-cutoff) with widths `j<=w`.  Hence

```text
|F^{nb}(A)|
 <=
  (1/Phi_q(q-w-1)) |I_A^{nb,spread(w)}|
  + sum_{j=1}^{w} sum_lambda
      sum_{C subset ev_A^{-1}(lambda), |C|=q-j}
        |F_{lambda,C}(A)|.                    (PF2-nobase-occupancy-cutoff)
```

The case `w=0` is exactly the sharp width-zero no-base coefficient
`1/(q-1)`, since `Phi_q(q-1)=q-1` and there are no concentrated profiles.
Increasing `w` trades bounded-width projective-fiber quotient ledgers for a
stronger determinant-gate saving on the remaining spread supports.  This is the
usable no-base endpoint for the canonical `b=2` peeling tree: after a chosen
bounded-width quotient-line charge, the surviving no-base determinant gates
come with the explicit occupancy coefficient above.

## Width-Zero b=2 Ledger

The fixed-width corollary is especially sharp at `w=0`.  Put

```text
A_0=0,        c=1,        h=q.
```

The near-fiber term is empty.  Indeed, a near-fiber support with `w=0` would
have no base roots and all `q` roots inside a single non-base projective fiber.
But every projective fiber is contained in the zero set of a nonzero residual
direction of degree `<q`; the earlier degree-gap lemma gives

```text
|ev_A^{-1}(lambda)|<q,
```

so such a support cannot exist.

Let

```text
I_A^{nb}={ e in I_A : pi_A(e) cap B_0 = empty }.
```

Then (PF2-width-w-ledger) becomes the two-term bound

```text
sum_{A in A_2} |F(A)|
 <=
  (1/(q-1)) sum_{A in A_2} |I_A^{nb}|
  + sum_{A in A_2} sum_{x in B_0^*(A)} |F_x(A)|.  (PF2-width-zero)
```

Equivalently, after the degree-gap exclusion, the `b=2` branch has only:

1. no-base split determinant gates, paid with the sharp `1/(q-1)` saving;
2. one-root common-base fixed-divisor quotient fibers.

This is a stronger endpoint than the general fixed-width form whenever the
one-root base quotient ledger can be charged globally.  It removes the
projective-fiber quotient-line term completely by using the same degree gap
that eliminated zero-good supports.

## Iterated Common-Base Peeling Recurrence

The one-root common-base term in (PF2-width-zero) can be peeled repeatedly.
Let `S subset B_0^*(A)` and write

```text
L_0=ell_S L_{0,S},        P=ell_S P_S,        Q=ell_S Q_S,
K_S=L_{0,S}+span(P_S,Q_S),
q_S=q-|S|.
```

The split quotient fiber

```text
F_S(A)={
  R' subset D'\S :
  |R'|=q_S and ell_S ell_{R'} in K(A)
}
```

is the residual fiber of the descended fixed-divisor problem with affine
locator space `K_S`.  If `dim span(P_S,Q_S)<2`, then this branch has dropped
to the lower-dimensional residual ledgers already isolated earlier.  If
`dim span(P_S,Q_S)=2`, the width-zero ledger applies to `K_S`:

```text
|F_S(A)|
 <=
  (1/(q_S-1)) |I_S^{nb}|
  + sum_{x in B_0^*(A)\S} |F_{S union {x}}(A)|.   (PF2-base-peel)
```

Here `I_S^{nb}` is the no-base split-good-pair domain for the quotient anchor
`K_S`.  The identity

```text
B_0^*(K_S)=B_0^*(A)\S
```

follows because division by `ell_S` is nonzero on all remaining available
roots.

Summing (PF2-base-peel) over all `s`-subsets `S subset B_0^*(A)` gives the
level recurrence

```text
sum_{|S|=s} |F_S(A)|
 <=
  sum_{|S|=s, dim span(P_S,Q_S)<2} |F_S(A)|
  + sum_{|S|=s, dim span(P_S,Q_S)=2} (1/(q-s-1)) |I_S^{nb}|
  + (s+1) sum_{|T|=s+1} |F_T(A)|.              (PF2-base-level)
```

Thus the common-base ledger is not merely a one-step quotient charge.  It has
a finite peeling tree whose internal `b=2` nodes pay a no-base determinant-gate
term with the sharp `1/(q-s-1)` no-base saving, whose edges add one common-base
root, and whose non-`b=2` nodes fall into lower-dimensional residual ledgers.
Since a `b=2` descended direction space requires `q-s>=2`, the denominator is
defined at every internal `b=2` node, and the tree has depth at most `q-1`.

This gives a precise route for closing the remaining base term in
(PF2-width-zero): prove polynomial bounds for the no-base determinant-gate
terms at every peeled width and for the lower-dimensional terminal ledgers.

## Canonical Base Peeling Removes Multiplicity

The level recurrence (PF2-base-level) is deliberately symmetric, and therefore
overcounts a support by the number of ways to forget its last peeled base root.
For a global bound it is better to choose one deterministic peeling path.

Fix a total order on `B_0^*(A)`.  For each residual support `R`, write its base
roots in increasing order

```text
R cap B_0^*(A)={x_1<...<x_t}.
```

Then `R` determines the unique chain

```text
empty, {x_1}, {x_1,x_2}, ..., {x_1,...,x_t}.
```

For an ordered initial segment `S`, let `F_S^can(A)` be the quotient supports
whose already-peeled base roots are exactly `S` in this sense: the original
support contains `S`, contains no base root smaller than the largest element of
`S` outside `S`, and all remaining base roots are larger than every element of
`S`.  The sets `F_S^can(A)` form a disjoint canonical peeling tree.

At a canonical node `S` with `q_S=q-|S|`, either the quotient direction space
has dimension `<2`, giving a lower-dimensional terminal ledger, or it has
dimension `2`.  In the `b=2` case, the width-zero ledger partitions
`F_S^can(A)` into:

1. no-base quotient supports, paid by the no-base determinant-gate term
   `(1/(q_S-1))|I_S^{nb,can}|`;
2. supports with a next base root `x>max(S)`, which enter the unique child
   `F_{S union {x}}^can(A)`.

Hence there is no branching multiplicity:

```text
|F_S^can(A)|
 <=
  LowerDim_S^can
  + (1/(q_S-1))|I_S^{nb,can}|
  + sum_{x>max(S)} |F_{S union {x}}^can(A)|.    (PF2-canon-peel)
```

For `S=empty`, the last sum ranges over all roots of `B_0^*(A)`.
Iterating over the canonical tree gives the multiplicity-free endpoint

```text
|F(A)|
 <=
  sum_{S in Tree(A)}
    LowerDim_S^can
  + sum_{S in Tree_2(A)}
      (1/(q-|S|-1)) |I_S^{nb,can}|.            (PF2-canon-tree)
```

Here `Tree_2(A)` denotes the canonical nodes whose descended direction space
still has dimension two.  Thus the common-base term is controlled by a
disjoint peeling tree: every original support contributes to exactly one leaf,
and every internal `b=2` payment is a no-base determinant-gate term with the
same sharp no-base saving as in (PF2-width-zero), at the descended width.

This removes the factorial overcount implicit in the symmetric level
recurrence and identifies the remaining `b=2` work as a bound for no-base
determinant gates across canonical peeled anchors, plus lower-dimensional
terminal ledgers.

## Canonical Peeling With Occupancy Cutoffs

The no-base occupancy cutoff can be applied at every internal `b=2` node of
the canonical tree.  For each canonical node `S in Tree_2(A)`, let

```text
q_S=q-|S|,        0<=w_S<=q_S-2.
```

Let `I_S^{nb,spread(w_S),can}` be the no-base good-pair labels in the
canonical node whose image quotient support has escape at least `w_S+1` from
its largest descended projective fiber.  Let `Q_{S,j}^{can}` denote the
canonical concentrated quotient-line ledger at node `S`, obtained by summing
the width-`j` projective-fiber quotient fibers

```text
F_{S,lambda,C}^{can},        |C|=q_S-j,
```

over the descended projective fibers and dominant subsets selected by
(PF2-nobase-occupancy-cutoff).

At node `S`, (PF2-canon-peel) with the no-base occupancy cutoff gives

```text
|F_S^can(A)|
 <= LowerDim_S^can
  + (1/Phi_{q_S}(q_S-w_S-1)) |I_S^{nb,spread(w_S),can}|
  + sum_{j=1}^{w_S} Q_{S,j}^{can}
  + sum_{x>max(S)} |F_{S union {x}}^can(A)|.
```

Because the canonical children are disjoint and every original support follows
one path, iteration over the tree gives the global endpoint

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)}
      (1/Phi_{q_S}(q_S-w_S-1))
        |I_S^{nb,spread(w_S),can}|
  + sum_{S in Tree_2(A)} sum_{j=1}^{w_S} Q_{S,j}^{can}.       (PF2-canon-occ-tree)
```

Thus, after canonical base peeling, no multiplicity or symbolic residual term
remains in the `b=2` branch.  The endpoint is a sum of explicit
lower-dimensional leaves, spread no-base determinant-gate ledgers with
occupancy savings chosen node-by-node, and bounded-width projective-fiber
quotient-line ledgers for the concentrated no-base profiles.

## Quotient-Line Ledgers Are Root-Slice Packings

The bounded-width quotient-line terms in (PF2-canon-occ-tree) are not a new
type of residual object.  Fix one canonical node `S`, one descended projective
fiber `lambda`, and one dominant subset `C` with `|C|=q_S-j`, `j>=1`.
The quotient line has the form

```text
L_{S,C}/ell_C + span(Q'_{S,lambda,C}),        deg Q'_{S,lambda,C}<j,
```

on the remaining canonical domain `D_{S,C}`.  Let

```text
Z_{S,lambda,C}={x in D_{S,C} : Q'_{S,lambda,C}(x)=0},
z_{S,lambda,C}=|Z_{S,lambda,C}|,        N_{S,C}=|D_{S,C}|.
```

Since `Q'_{S,lambda,C}` is nonzero of degree `<j`, one has
`z_{S,lambda,C}<=j-1`.  If two quotient supports `R_1,R_2` in this line are
distinct, then

```text
ell_{R_1}-ell_{R_2}=alpha Q'_{S,lambda,C},        alpha != 0.
```

Thus any common root of `R_1` and `R_2` lies in `Z_{S,lambda,C}`.  Outside
`Z_{S,lambda,C}`, the quotient supports are pairwise disjoint, and every
support contributes at least `j-z_{S,lambda,C}` roots outside this set.
Therefore

```text
|F_{S,lambda,C}^{can}|
 <= floor((N_{S,C}-z_{S,lambda,C})/(j-z_{S,lambda,C})).
                                                        (PF2-quot-line-pack)
```

The roots in `Z_{S,lambda,C}` are exactly the one-root bad slices of the
quotient line, by the same divisible-kernel identity as in the `b=1`
residual-kernel packing.  Consequently every bounded-width quotient-line
ledger in (PF2-canon-occ-tree) is an ordinary root-slice packing ledger.  The
remaining genuinely new `b=2` work is the spread determinant-gate count; the
concentrated quotient-line branch has descended to fixed-width root-slice
packings.

## Explicit Capacity Form of the Canonical b=2 Endpoint

The spread determinant-gate term in (PF2-canon-occ-tree) can be bounded by
ambient good-pair capacity at the same canonical node.  For `S in Tree_2(A)`,
let `D_S^{can}` be the canonical remaining domain, let `B_S` be the descended
base locus, and let `D_{S,lambda}` be the non-base projective fibers.  Put

```text
G_S^{can}
 =
 binom(|D_S^{can}\B_S|,2)
 - sum_lambda binom(|D_{S,lambda}|,2).          (PF2-canon-good-cap)
```

This is the number of ambient cross-fiber good pairs available at node `S`.
Since `I_S^{nb,spread(w_S),can}` is a subset of these good-pair labels,

```text
|I_S^{nb,spread(w_S),can}| <= G_S^{can}.        (PF2-spread-cap)
```

Combining (PF2-canon-occ-tree), (PF2-spread-cap), and
(PF2-quot-line-pack) gives the explicit capacity endpoint

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)}
      G_S^{can}/Phi_{q_S}(q_S-w_S-1)
  + sum_{S in Tree_2(A)} sum_{j=1}^{w_S}
      sum_lambda sum_{C subset D_{S,lambda}, |C|=q_S-j}
        floor((N_{S,C}-z_{S,lambda,C})/(j-z_{S,lambda,C})).
                                                        (PF2-canon-capacity)
```

Here `z_{S,lambda,C}` is the number of remaining-domain roots of the quotient
direction `Q'_{S,lambda,C}`.  The last sum is exactly a fixed-width root-slice
packing ledger.  Thus the canonical `b=2` branch has been reduced to explicit
node capacities, lower-dimensional leaves, and root-slice bad-root counts; no
split determinant-gate set remains as an unexpanded object in this endpoint.

## Optimized Canonical Capacity Choice

The cutoff in (PF2-canon-capacity) is free at each canonical `b=2` node, so it
can be optimized locally.  Define the width-`j` quotient-line packing capacity
at node `S` by

```text
R_{S,j}^{can}
 =
 sum_lambda sum_{C subset D_{S,lambda}, |C|=q_S-j}
   floor((N_{S,C}-z_{S,lambda,C})/(j-z_{S,lambda,C})).
```

For `0<=w<=q_S-2`, put

```text
Cap_S(w)
 =
  G_S^{can}/Phi_{q_S}(q_S-w-1)
  + sum_{j=1}^{w} R_{S,j}^{can}.
```

Since (PF2-canon-capacity) holds for every choice of the node cutoffs, choose
for each node a minimizing cutoff

```text
Cap_S^*=min_{0<=w<=q_S-2} Cap_S(w).
```

Then the whole canonical `b=2` fixed-anchor fiber satisfies

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)} Cap_S^*.              (PF2-canon-opt-cap)
```

This is the sharpest endpoint available from the current occupancy-cutoff
decomposition.  A node with cheap low-width root-slice packings can choose
larger `w` and gain a stronger spread coefficient; a node with expensive
root-slice shadows can choose `w=0` and fall back to the sharp `1/(q_S-1)`
no-base determinant-gate capacity.

## Bad-Root-Free Quotient-Line Majorant

The optimized endpoint can be made independent of the bad-root counts
`z_{S,lambda,C}` at the cost of a coarser but purely height-based bound.  Put

```text
N_S=|D_S^{can}|,
H_{S,j}^{can}=sum_lambda binom(|D_{S,lambda}|,q_S-j).
```

For a width-`j` quotient line, `|C|=q_S-j`, so the remaining quotient domain
has size

```text
N_{S,C}=N_S-q_S+j.
```

Since the quotient direction has degree `<j`, its bad-root count satisfies
`0<=z_{S,lambda,C}<=j-1`.  Therefore, writing `t=j-z_{S,lambda,C}`,

```text
floor((N_{S,C}-z_{S,lambda,C})/(j-z_{S,lambda,C}))
 = floor(1+(N_{S,C}-j)/t)
 <= N_{S,C}-j+1
 = N_S-q_S+1.                                  (PF2-quot-line-unif)
```

Thus

```text
R_{S,j}^{can} <= (N_S-q_S+1) H_{S,j}^{can}.     (PF2-R-unif)
```

Define the height-only capacity

```text
WidehatCap_S(w)
 =
  G_S^{can}/Phi_{q_S}(q_S-w-1)
  + (N_S-q_S+1) sum_{j=1}^{w} H_{S,j}^{can},

WidehatCap_S^*=min_{0<=w<=q_S-2} WidehatCap_S(w).
```

Then (PF2-canon-opt-cap) gives the bad-root-free endpoint

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)} WidehatCap_S^*.        (PF2-canon-height-cap)
```

This form is weaker than the exact optimized capacity, but it depends only on
canonical node sizes and projective-fiber heights.  It removes the last
one-root bad-slice parameter from the displayed `b=2` capacity bound, which is
useful when one wants a global estimate before proving sharper root-slice
bad-root cancellation.

## Max-Height Corollary for Canonical Nodes

There is an even simpler height-only consequence.  For `S in Tree_2(A)`, put

```text
h_S=max_lambda |D_{S,lambda}|.
```

If `h_S=0`, the no-base term at this node is empty.  Otherwise the degree gap
gives `1<=h_S<=q_S-1`.  Since every no-base quotient support at node `S` has
all projective fibers of size at most `h_S`, the exact occupancy bound gives

```text
g_S(R)>=Phi_{q_S}(h_S)
```

for every no-base support `R` at the node.  Equivalently, in the cutoff
language choose

```text
w_S=q_S-h_S-1.
```

Then `H_{S,j}^{can}=0` for every `j<=w_S`, because a subset of size
`q_S-j>h_S` cannot fit inside one projective fiber.  Hence the height-only
capacity has no concentrated term at this cutoff and

```text
WidehatCap_S^* <= G_S^{can}/Phi_{q_S}(h_S).     (PF2-max-height-node)
```

Combining this with (PF2-canon-height-cap) yields the compact fixed-anchor
bound

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A), h_S>0}
      G_S^{can}/Phi_{q_S}(h_S).                (PF2-canon-height-simple)
```

This is weaker than the optimized cutoff when low-width root-slice packings
are cheap, but it has no cutoff, bad-root, or quotient-line parameters.  The
remaining global `b=2` question is reduced to bounding canonical node
cross-fiber capacities relative to their maximum projective-fiber heights,
together with the explicit lower-dimensional leaves.

## Two-Regime Max-Height Saving

The denominator in (PF2-canon-height-simple) has a simple useful lower bound.
Since every projective-fiber part has size at most `h`, the extremal square
sum satisfies

```text
sum parts^2 <= h q.
```

Therefore

```text
Phi_q(h) >= q(q-h)/2.                           (PF2-Phi-linear)
```

In particular, if `h<=q/2`, then

```text
Phi_q(h) >= q^2/4.
```

If `h>q/2`, the exact formula has only one full `h`-block:

```text
Phi_q(h)=h(q-h).                                (PF2-Phi-half)
```

Thus each canonical node in (PF2-canon-height-simple) falls into one of two
regimes:

```text
h_S<=q_S/2:
  G_S^{can}/Phi_{q_S}(h_S) <= 4 G_S^{can}/q_S^2,

h_S>q_S/2:
  G_S^{can}/Phi_{q_S}(h_S) = G_S^{can}/(h_S(q_S-h_S)).
                                                        (PF2-two-regime)
```

The diffuse-height nodes therefore receive a uniform quadratic saving in the
residual width.  The only max-height nodes not covered by this automatic
`q_S^{-2}` saving are the half-height projective-shadow nodes, precisely the
large fixed-divisor shadows isolated earlier.

## Canonical Half-Height Shadows Are Short Quotient Kernels

The exceptional case in (PF2-two-regime) is still structured.  Fix a canonical
node `S in Tree_2(A)` with `h_S>q_S/2`, and choose a projective fiber
`lambda=[a:b]` such that

```text
C=D_{S,lambda},        |C|=h_S.
```

Define the corresponding projective-shadow direction by

```text
Q_{S,lambda}=bP_S-aQ_S.
```

This direction is nonzero because `span(P_S,Q_S)` has dimension two, and it
vanishes on the whole non-base fiber `C`.  Hence

```text
Q_{S,lambda}=ell_C R_{S,lambda},
deg R_{S,lambda}<q_S-h_S<q_S/2.                (PF2-canon-half-kernel)
```

By the same divisible-kernel identity used in the quotient-line packing
ledger, `R_{S,lambda}` is a fixed-divisor Hankel kernel for the absorbed
canonical anchor `S union C`.  Equivalently, the projective fiber responsible
for the non-diffuse height profile is a short quotient-residue direction of
width `q_S-h_S`.

Thus the two regimes have different remaining tasks.  If `h_S<=q_S/2`, the
node pays the automatic `4G_S^{can}/q_S^2` determinant-gate saving.  If
`h_S>q_S/2`, then

```text
G_S^{can}/Phi_{q_S}(h_S)=G_S^{can}/(h_S(q_S-h_S)),
```

and the complementary factor `q_S-h_S` is exactly the width of the short
quotient kernel in (PF2-canon-half-kernel).  The remaining M1 problem after
the canonical capacity reduction is therefore not an arbitrary large-shadow
case: it is to count these canonical short projective-shadow quotient kernels,
or to charge them to the existing fixed-divisor/root-slice ledgers, across the
base-peeling tree.

## Diffuse-Plus-Short Canonical Endpoint

The preceding half-height interpretation can be built directly into the
canonical endpoint.  At each canonical `b=2` node choose the half-width cutoff

```text
w_S^sh=ceil(q_S/2)-1,        m_S^sh=q_S-w_S^sh-1=floor(q_S/2).
```

Then `m_S^sh<=q_S/2`, so (PF2-Phi-linear) gives

```text
Phi_{q_S}(m_S^sh)>=q_S^2/4.                    (PF2-half-cut-save)
```

All concentrated quotient-line ledgers selected by this cutoff have
`1<=j<=w_S^sh`, hence `j<q_S/2`; they are exactly short
fixed-divisor/root-slice ledgers.  Define

```text
Short_S^{can}=
  sum_{1<=j<q_S/2} R_{S,j}^{can}.
```

Choosing `w_S=w_S^sh` in (PF2-canon-capacity), or equivalently in
(PF2-canon-opt-cap), gives the explicit endpoint

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)} 4G_S^{can}/q_S^2
  + sum_{S in Tree_2(A)} Short_S^{can}.        (PF2-canon-diffuse-short)
```

Thus the canonical `b=2` branch has a clean dichotomy: the spread part is
paid with a uniform quadratic determinant-gate saving, and every
non-diffuse projective-fiber profile has been moved to a short quotient-line
root-slice packing ledger.  In particular, if a node has `h_S>q_S/2` and
`r_S=q_S-h_S`, then `r_S<q_S/2`; the maximal projective fiber
`D_{S,lambda}` is one of the width-`r_S` summands of `Short_S^{can}` with
the certificate (PF2-canon-half-kernel).  No separate half-height exception
remains in this endpoint.

## Short Ledgers Are Half-Height Kernel Tails

The short quotient-line term in (PF2-canon-diffuse-short) has a sharper
normal form.  Fix a canonical `b=2` node `S`, a projective fiber `lambda`, and
write

```text
h_lambda=|D_{S,lambda}|,        r_lambda=q_S-h_lambda.
```

If `h_lambda<=q_S/2`, then this fiber contributes nothing to
`Short_S^{can}`: a short summand has `j<q_S/2`, hence
`|C|=q_S-j>q_S/2`, so no subset `C subset D_{S,lambda}` of that size exists.

Assume now that `h_lambda>q_S/2`.  Let

```text
Q_{S,lambda}=ell_{D_{S,lambda}} R_{S,lambda},
deg R_{S,lambda}<r_lambda.
```

For any short quotient-line summand choose
`C subset D_{S,lambda}` with `|C|=q_S-j`, and put

```text
E=D_{S,lambda}\C,        e=|E|.
```

Then

```text
j=r_lambda+e,        Q'_{S,lambda,C}=Q_{S,lambda}/ell_C
                   =ell_E R_{S,lambda}.       (PF2-short-tail-factor)
```

Thus a short quotient-line certificate is just an `e`-root thickening of the
primitive half-height kernel `R_{S,lambda}`.  Moreover `j<q_S/2` is
equivalent to

```text
0<=e<=floor((q_S-1)/2)-r_lambda.
```

Let

```text
Z_{S,lambda}^{perp}
 =
 {x in D_S^{can}\D_{S,lambda} : R_{S,lambda}(x)=0},
z_{S,lambda}^{perp}=|Z_{S,lambda}^{perp}|.
```

Because `deg R_{S,lambda}<r_lambda`, one has
`z_{S,lambda}^{perp}<=r_lambda-1`.  On the quotient domain `D_{S,C}`, the
zero set of the quotient direction `ell_E R_{S,lambda}` is the disjoint union

```text
E disjoint_union Z_{S,lambda}^{perp}.
```

Consequently the root-slice packing floor for this summand is independent of
the thickening set `E`:

```text
floor((N_{S,C}-z_{S,lambda,C})/(j-z_{S,lambda,C}))
 =
floor((N_S-h_lambda-z_{S,lambda}^{perp})
      /(r_lambda-z_{S,lambda}^{perp})).        (PF2-short-tail-pack)
```

Define the primitive half-height packing factor

```text
B_{S,lambda}^{prim}
 =
floor((N_S-h_lambda-z_{S,lambda}^{perp})
      /(r_lambda-z_{S,lambda}^{perp})).
```

Then the whole short ledger at node `S` satisfies

```text
Short_S^{can}
 <=
 sum_{lambda: h_lambda>q_S/2}
   B_{S,lambda}^{prim}
   sum_{e=0}^{floor((q_S-1)/2)-r_lambda}
      binom(h_lambda,e).                       (PF2-short-primitive-tail)
```

Thus the short side of the canonical M1 endpoint is localized on
half-height projective fibers.  Its only multiplicity is the low-complement
tail of choices `E` inside such a fiber, times the single primitive root-slice
packing factor attached to the half-height kernel `R_{S,lambda}`.

## Primitive Half-Height Packing Is a Surplus Term

The primitive factor in (PF2-short-primitive-tail) has an exact surplus form.
Since `h_lambda=q_S-r_lambda`,

```text
B_{S,lambda}^{prim}
 =
floor((N_S-h_lambda-z_{S,lambda}^{perp})
      /(r_lambda-z_{S,lambda}^{perp}))
 =
1+floor((N_S-q_S)/(r_lambda-z_{S,lambda}^{perp})).
                                                        (PF2-prim-surplus)
```

Here the denominator is positive because
`z_{S,lambda}^{perp}<=r_lambda-1`.  Thus the large half-height fiber itself
does not create a large root-slice packing factor.  After the primitive
half-height kernel and its perpendicular bad roots are fixed, the only source
of additional multiplicity is the canonical node surplus `N_S-q_S`.

In particular, if the primitive kernel has no perpendicular roots on the
remaining canonical domain, then

```text
B_{S,lambda}^{prim}=1+floor((N_S-q_S)/r_lambda).
                                                        (PF2-prim-rootfree)
```

If `z_{S,lambda}^{perp}>0`, each root counted by
`Z_{S,lambda}^{perp}` is a one-root absorbed fixed-divisor slice for the
anchor `S union D_{S,lambda}`.  Peeling those roots reduces the denominator
from `r_lambda` to `r_lambda-z_{S,lambda}^{perp}` and leaves the same surplus
term.  Consequently the unresolved primitive half-height contribution in M1
splits into:

1. root-free primitive kernels, with denominator `r_lambda`;
2. explicit perpendicular fixed-root/root-slice defects, which account for
   every loss in that denominator;
3. the low-complement binomial tail already displayed in
   (PF2-short-primitive-tail).

## Primitive Tail Has a Center-Gap Saving

The low-complement tail in (PF2-short-primitive-tail) is a binomial lower tail
with a visible gap from the center.  Since `q_S=h_lambda+r_lambda`,

```text
floor((q_S-1)/2)-r_lambda
 =
floor((h_lambda-r_lambda-1)/2).
```

Thus, writing

```text
T(h,r)=sum_{e=0}^{floor((h-r-1)/2)} binom(h,e),
```

the primitive-tail term is exactly `T(h_lambda,r_lambda)`.  Put

```text
theta(h,r)=floor((h-r-1)/2)/h < 1/2.
```

The standard binomial-tail estimates give

```text
T(h,r) <= (h+1) 2^{h H_2(theta(h,r))},          (PF2-tail-entropy)
T(h,r) <= 2^h exp(-(r+1)^2/(2h)).               (PF2-tail-gauss)
```

Indeed, the entropy bound is the usual maximal-binomial-coefficient bound for
a lower tail below `h/2`.  For the Gaussian form, if `B` is binomial
`Bin(h,1/2)`, then `T(h,r)=2^h Pr[B<=floor((h-r-1)/2)]`; the cutoff is at
least `(r+1)/2` below the mean `h/2`, and Hoeffding gives the displayed
exponential saving.

Consequently, after the perpendicular fixed-root defects have been charged,
the root-free primitive short branch admits an explicit width cutoff.  Let
`Short_S^{rf}` denote the contribution of primitive half-height fibers with
`z_{S,lambda}^{perp}=0`.  For any integer `R>=1`,

```text
Short_S^{rf}
 <=
 sum_{lambda: h_lambda>q_S/2, r_lambda<R}
   (1+floor((N_S-q_S)/r_lambda)) T(h_lambda,r_lambda)
 +
 sum_{lambda: h_lambda>q_S/2, r_lambda>=R}
   (1+floor((N_S-q_S)/R))
   2^{h_lambda} exp(-R^2/(2h_lambda)).          (PF2-tail-cutoff)
```

Thus wide primitive denominators carry a quantitative center-gap saving in the
number of possible thickenings.  The only root-free primitive short kernels
not helped by this tail estimate are the bounded-width denominators
`r_lambda<R`; those are now isolated as the narrow primitive core of the
half-height M1 obstruction.

## Fixed-Root Charging Removes the Primitive Tail

The tail estimate is useful for uncharged bookkeeping, but the algebraic
status of the tail is sharper.  In the notation of
(PF2-short-tail-factor), the actual quotient-line direction for the summand
indexed by `E` is

```text
Q'_{S,lambda,C}=ell_E R_{S,lambda}.
```

Its bad-root set on the quotient domain is exactly

```text
E disjoint_union Z_{S,lambda}^{perp}.
```

Thus a summand is genuinely root-free only when both

```text
E=empty,        z_{S,lambda}^{perp}=0.
```

Every summand with `E` nonempty is an explicit fixed-root/root-slice
thickening of the primitive direction `R_{S,lambda}`.  Every summand with
`z_{S,lambda}^{perp}>0` has a perpendicular absorbed fixed-root defect.  Hence
after the fixed-root/root-slice ledgers have been charged, the binomial tail
does not remain in the primitive M1 obstruction.  The uncharged root-free
primitive half-height term at node `S` is bounded by

```text
PrimHalf_S^{rf}
 =
 sum_{lambda: h_lambda>q_S/2, z_{S,lambda}^{perp}=0}
   (1+floor((N_S-q_S)/r_lambda)).              (PF2-prim-rf-core)
```

More explicitly, the whole short ledger decomposes as

```text
Short_S^{can}
 <= PrimHalf_S^{rf} + FixedRootTail_S,
```

where

```text
FixedRootTail_S
 =
 sum_{lambda: h_lambda>q_S/2, z_{S,lambda}^{perp}>0}
   B_{S,lambda}^{prim} T(h_lambda,r_lambda)
 + sum_{lambda: h_lambda>q_S/2, z_{S,lambda}^{perp}=0}
   B_{S,lambda}^{prim} (T(h_lambda,r_lambda)-1).
                                                        (PF2-fixed-tail)
```

Each summand of `FixedRootTail_S` carries a displayed nonempty fixed-root set:
either a perpendicular root from `Z_{S,lambda}^{perp}` or an omitted fiber root
from `E`.  Consequently, once those fixed-root/root-slice charges are accepted,
the remaining primitive half-height problem is no longer a binomial-tail
problem.  It is the global count of root-free primitive half-height directions
with weight `1+floor((N_S-q_S)/r_lambda)`.

## Root-Free Primitive Core Is Base-Free and Occupancy-Controlled

The root-free primitive core has no hidden base-locus contribution.  If
`x in B_S`, then `P_S(x)=Q_S(x)=0`, so every projective-shadow direction

```text
Q_{S,lambda}=bP_S-aQ_S
```

vanishes at `x`.  Since `x` is not in any non-base fiber `D_{S,lambda}`, the
factorization `Q_{S,lambda}=ell_{D_{S,lambda}} R_{S,lambda}` gives
`R_{S,lambda}(x)=0`.  Hence

```text
B_S subset Z_{S,lambda}^{perp}
```

for every non-base projective fiber `lambda`.  In particular,
`z_{S,lambda}^{perp}=0` forces `B_S=empty`.  Thus the uncharged root-free
primitive half-height core only occurs at canonical nodes whose descended base
locus has vanished.

At such a base-free node put

```text
u_S=floor((q_S-1)/2),
m_{S,r}^{hh}=#{lambda : |D_{S,lambda}|=q_S-r},        1<=r<=u_S.
```

The half-height fibers are disjoint subsets of `D_S^{can}`, so

```text
sum_{r=1}^{u_S} m_{S,r}^{hh}(q_S-r) <= N_S.    (PF2-hh-occupancy)
```

Combining this with (PF2-prim-rf-core) gives the node-level occupancy bound

```text
PrimHalf_S^{rf}
 <=
 sum_{r=1}^{u_S}
   m_{S,r}^{hh} (1+floor((N_S-q_S)/r)).        (PF2-prim-occupancy)
```

This bound depends only on the projective-fiber height histogram of the
base-free canonical node.  Equivalently, for any cutoff `1<=R<=u_S+1`, if the
bounded-width core `r<R` has been charged separately, then the remaining
root-free primitive core satisfies

```text
PrimHalf_S^{rf}(r>=R)
 <=
 floor(N_S/(floor(q_S/2)+1))
 (1+floor((N_S-q_S)/R)).                       (PF2-prim-occ-cut)
```

The reason is that every half-height fiber has size at least
`floor(q_S/2)+1`, while `r>=R` makes the surplus weight at most
`1+floor((N_S-q_S)/R)`.  Thus after base, fixed-root, and bounded-width
primitive charges, no algebraic multiplicity remains in the half-height
branch beyond this explicit occupancy count.

## Post-Charge Diffuse-Occupancy Endpoint

Combining the preceding reductions gives a useful canonical endpoint with all
charged half-height pieces displayed.  At a canonical `b=2` node `S`, choose a
primitive-width cutoff `R_S>=1`.  Define the bounded-width root-free primitive
core by

```text
BWPrim_S(R_S)
 =
 sum_{lambda: h_lambda>q_S/2,
             z_{S,lambda}^{perp}=0,
             r_lambda<R_S}
   (1+floor((N_S-q_S)/r_lambda)).
```

Define the residual occupancy term by

```text
OccHalf_S(R_S)
 =
 0,                                             if B_S nonempty,

 floor(N_S/(floor(q_S/2)+1))
 (1+floor((N_S-q_S)/R_S)),                      if B_S empty.
```

Then (PF2-fixed-tail) and (PF2-prim-occ-cut) give

```text
Short_S^{can}
 <= FixedRootTail_S + BWPrim_S(R_S) + OccHalf_S(R_S).
                                                        (PF2-short-postcharge)
```

Substituting this into (PF2-canon-diffuse-short) yields the post-charge
canonical endpoint

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)} 4G_S^{can}/q_S^2
  + sum_{S in Tree_2(A)} FixedRootTail_S
  + sum_{S in Tree_2(A)} BWPrim_S(R_S)
  + sum_{S in Tree_2(A)} OccHalf_S(R_S).       (PF2-postcharge-endpoint)
```

Thus the `b=2` M1 branch has been reduced to five explicit ledgers:
lower-dimensional terminal packings, quadratically saved diffuse
determinant-gate capacity, fixed-root/root-slice tails, bounded-width
root-free primitive cores, and a base-free half-height occupancy count.  If
the first four ledgers are charged by the existing lower-dimensional,
fixed-root, bounded-width, and diffuse estimates, the only remaining
unexpanded half-height term is the occupancy count `OccHalf_S(R_S)`, which is
purely combinatorial at each canonical node.

## Histogram-Optimized Post-Charge Core

The occupancy term in (PF2-postcharge-endpoint) can be sharpened by keeping
the half-height height histogram instead of replacing it by the coarsest
fiber-count bound.  For `1<=R<=u_S+1`, define

```text
HOcc_S(R)
 =
 0,                                             if B_S nonempty,

 sum_{r=R}^{u_S}
   m_{S,r}^{hh} (1+floor((N_S-q_S)/r)),         if B_S empty,
```

with the convention that the sum is empty when `R=u_S+1`.  Then the same
partition of root-free primitive directions gives

```text
Short_S^{can}
 <= FixedRootTail_S + BWPrim_S(R) + HOcc_S(R). (PF2-short-hist)
```

Indeed, the root-free primitive directions with `r<R` are counted exactly by
`BWPrim_S(R)`.  The root-free directions with `r>=R` are a subfamily of the
half-height fibers counted by `m_{S,r}^{hh}`, and each has surplus weight
`1+floor((N_S-q_S)/r)`.  If `B_S` is nonempty, the root-free subfamily is
empty by the base-free lemma, so `HOcc_S(R)=0` is valid.

Thus the cutoff can be optimized locally.  Put

```text
PostCore_S^*
 =
 min_{1<=R<=u_S+1} (BWPrim_S(R)+HOcc_S(R)).
```

Substituting the minimizing cutoff into (PF2-short-hist) and then into
(PF2-canon-diffuse-short) gives

```text
|F(A)|
 <=
  sum_{S in Tree(A)} LowerDim_S^can
  + sum_{S in Tree_2(A)} 4G_S^{can}/q_S^2
  + sum_{S in Tree_2(A)} FixedRootTail_S
  + sum_{S in Tree_2(A)} PostCore_S^*.         (PF2-postcharge-opt)
```

The coarser `OccHalf_S(R)` term is recovered from `HOcc_S(R)` by bounding the
number of half-height fibers by `floor(N_S/(floor(q_S/2)+1))` and every wide
surplus denominator by `R`.  The optimized form is therefore the strongest
post-charge endpoint available from the current local analysis: all remaining
uncharged half-height information is encoded in a finite node-local histogram
minimization.

## Surplus-Balanced Primitive Cutoff

The optimized endpoint has a canonical cutoff choice that removes all surplus
weight from the wide side.  If `N_S<q_S`, then the canonical quotient fiber at
node `S` is empty.  Otherwise put

```text
s_S=N_S-q_S,        R_S^{bal}=min(u_S+1,s_S+1).
```

For `R=R_S^{bal}`, the histogram tail in (PF2-short-hist) satisfies

```text
HOcc_S(R_S^{bal})
 <=
 0,                                             if B_S nonempty or s_S>=u_S,

 #{lambda : h_lambda>q_S/2 and r_lambda>=s_S+1},
                                                otherwise.
```

In particular,

```text
HOcc_S(R_S^{bal})
 <= floor(N_S/(floor(q_S/2)+1)).                (PF2-balanced-occ)
```

Indeed, if `s_S>=u_S`, then `R_S^{bal}=u_S+1` and the sum in `HOcc` is empty.
If `s_S<u_S`, then every retained wide denominator has `r>=s_S+1`, so
`1+floor(s_S/r)=1`; only the number of retained half-height fibers remains,
and those fibers are disjoint and each has size at least `floor(q_S/2)+1`.

Thus (PF2-postcharge-opt) has the explicit surplus-balanced specialization

```text
PostCore_S^*
 <= BWPrim_S(R_S^{bal})
    + floor(N_S/(floor(q_S/2)+1)).              (PF2-balanced-core)
```

The bounded-width part now contains only denominators

```text
r_lambda <= min(u_S,s_S).
```

Consequently, after fixed-root tails and primitive denominators of width at
most the node surplus have been charged, the remaining root-free half-height
contribution is at most the bare count of disjoint half-height fibers.  This
removes the surplus factor from the final uncharged occupancy term.

## Bare Half-Height Occupancy Is a Surplus Ledger

The remaining fiber-count term in (PF2-balanced-core) is itself controlled by
node surplus.  Put

```text
h0_S=floor(q_S/2)+1,        s_S=N_S-q_S>=0.
```

Then

```text
floor(N_S/h0_S)
 =
1+floor((s_S+q_S-h0_S)/h0_S)
 =
1+floor((s_S+ceil(q_S/2)-1)/h0_S).             (PF2-bare-occ-exact)
```

In particular,

```text
floor(N_S/h0_S) <= 1+ceil(s_S/h0_S)
                 <= 1+ceil(2s_S/q_S).          (PF2-bare-occ-surplus)
```

Thus, after the surplus-balanced cutoff, the uncharged half-height occupancy
has one baseline slot at a nonempty node, and every additional half-height
fiber consumes at least `h0_S` extra available roots beyond the quotient width
`q_S`.  Combining (PF2-balanced-core) and (PF2-bare-occ-surplus) gives

```text
PostCore_S^*
 <= BWPrim_S(R_S^{bal})
    + 1+ceil((N_S-q_S)/(floor(q_S/2)+1)).       (PF2-balanced-surplus-core)
```

Equivalently, once fixed-root tails and primitive denominators of width at
most the node surplus are charged, the remaining node-local half-height core
is a one-per-node term plus a surplus-over-half-width term.  This is the form
needed for a global canonical-tree charge: no field-size or binomial
multiplicity remains in the uncharged half-height branch.

## Canonical Peeling Debits Surplus Exactly

The surplus term in (PF2-balanced-surplus-core) is not a new multiplicative
loss along the canonical tree.  It has exact bookkeeping under the same
canonical order used for base peeling.

For a nonempty canonical node `S`, write `m(S)=max(S)` and define

```text
b(S)=#{x in B_0^*(A) : x<=m(S)},        skip(S)=b(S)-|S|.
```

Here `<=` denotes the fixed canonical order.  For `S=empty`, set
`b(S)=skip(S)=0`.  Since

```text
Old(S)={x in B_0^*(A)\S : x<m(S)}
```

and every element of `S` is at most `m(S)`, one has

```text
S union Old(S)={x in B_0^*(A) : x<=m(S)}.
```

Thus, with `s_empty=|D'|-q`,

```text
N_S=|D'|-b(S),        q_S=q-|S|,
s_S=N_S-q_S=s_empty-skip(S).             (PF2-surplus-skip)
```

In particular every active canonical node has `skip(S)<=s_empty`; otherwise
`N_S<q_S` and no quotient support of size `q_S` remains.

If `T=S union {x}` is a canonical child, put

```text
gap_S(x)=#{y in B_0^*(A) : y<x},             if S=empty,
gap_S(x)=#{y in B_0^*(A) : m(S)<y<x},        if S nonempty.
```

Then

```text
skip(T)=skip(S)+gap_S(x),        s_T=s_S-gap_S(x).
                                                        (PF2-surplus-debit)
```

Hence canonical peeling can only decrease node surplus, and it decreases it
by exactly the number of older base roots skipped when the child is chosen.
The surplus-over-half-width term left by (PF2-balanced-surplus-core) is
therefore

```text
ceil((s_empty-skip(S))/(floor((q-|S|)/2)+1))
```

at node `S`: every extra half-height occupancy slot is paid from unused
initial surplus, while skipped canonical base roots debit that reserve
one-for-one.  The remaining global M1 task is consequently separated into a
baseline active-node count and this explicit surplus-debit ledger, rather
than a depth-multiplicative half-height loss.

## Base-Free Half-Height Nodes Have a Skip-Ball Envelope

The preceding surplus debit also bounds the number of places where the
one-per-node half-height baseline can occur.  Let

```text
b_0=|B_0^*(A)|,        s_0=|D'|-q.
```

Assume `s_0>=0`; otherwise `F(A)` is empty.  If `S` is a canonical node with
`B_S=empty`, then either `S=empty` and `b_0=0`, or `S` contains the largest
element of `B_0^*(A)`.

Indeed, if `y in B_0^*(A)` is not in `S union Old(S)`, then `y` remains in
`D_S^{can}`.  Since `P(y)=Q(y)=0` and division by `ell_S` is nonzero at such a
remaining root, one has `P_S(y)=Q_S(y)=0`, so `y in B_S`.  Thus `B_S=empty`
forces

```text
S union Old(S)=B_0^*(A).                       (PF2-basefree-leaf)
```

Consequently a base-free node is a terminal leaf of the canonical base-peeling
tree.  If `b_0>0`, such a node is determined by the subset of the first
`b_0-1` base roots that were skipped before the largest base root was peeled.
For a node with `ell` skipped roots,

```text
skip(S)=ell,        |S|=b_0-ell,
q_S=q-b_0+ell,      s_S=s_0-ell.
```

Activity forces `ell<=s_0`, by (PF2-surplus-skip).  Hence the whole
base-free residual half-height baseline has the explicit envelope

```text
sum_{S in Tree_2(A), B_S=empty}
  (1+ceil(s_S/(floor(q_S/2)+1)))

 <=
 1+ceil(s_0/(floor(q/2)+1)),                         if b_0=0,

 sum_{ell=0}^{min(s_0,b_0-1)}
   binom(b_0-1,ell)
   (1+ceil((s_0-ell)/(floor((q-b_0+ell)/2)+1))),     if b_0>0.
                                                        (PF2-skipball-core)
```

The actual active-node sum may be smaller, since not every subset in the
skip ball need occur and not every such node need remain `b=2`.  The point is
that the uncharged root-free half-height baseline is supported only on a
terminal skip ball of radius `s_0` inside the ordered base locus, rather than
on all depths of the canonical tree.  In fixed-surplus regimes this is a
polynomial-size terminal ledger; in general it isolates the only remaining
combinatorial growth parameter as the number of skipped base roots.

## Fixed-Surplus Half-Height Baseline Is Polynomial

The skip-ball envelope gives a clean polynomial bound in the low-slack regimes
listed in the M1 guide.  Since `B_0^*(A)` is contained in the zero set of a
nonzero degree-`<q` residual direction at a `b=2` root node, one has
`b_0<=q-1`.  Moreover every node counted in `Tree_2(A)` has `q_S>=2`, so

```text
1+ceil((s_0-ell)/(floor(q_S/2)+1))
 <= 1+ceil((s_0-ell)/2)
 <= 1+ceil(s_0/2).
```

Therefore, for `b_0>0`, (PF2-skipball-core) implies

```text
sum_{S in Tree_2(A), B_S=empty}
  (1+ceil(s_S/(floor(q_S/2)+1)))

 <=
 (1+ceil(s_0/2))
 sum_{ell=0}^{min(s_0,b_0-1)} binom(b_0-1,ell)
 <=
 (1+ceil(s_0/2))(s_0+1) q^{s_0}.              (PF2-fixed-surplus-core)
```

For `b_0=0` the same final bound holds from the singleton case in
(PF2-skipball-core), since `1+ceil(s_0/(floor(q/2)+1))` is at most the right
side of (PF2-fixed-surplus-core).  Thus if the initial surplus is bounded by
a fixed constant `sigma`, the entire residual base-free half-height baseline is
`O_sigma(q^sigma)`.  In particular, for fixed slack `t=1,2,3` this part of
the M1 half-height obstruction is polynomial-size after the fixed-root tails,
bounded-width primitive denominators, diffuse determinant gates, and
lower-dimensional terminal leaves have been separated.  The remaining
non-polynomial risk is therefore not a depth compounding of the root-free
half-height baseline, but the still-explicit ledgers outside this terminal
fixed-surplus core.

## Fixed-Surplus Root-Free Half-Height Core Is Polynomial

The same argument also closes the bounded-width primitive part of the
root-free half-height core in fixed-surplus regimes.  At any node,
`BWPrim_S(R)` is zero unless `B_S=empty`, because
`z_{S,lambda}^{perp}=0` forces `B_S=empty`.  Thus the only nodes contributing
to `PostCore_S^*` are the base-free terminal leaves counted by
(PF2-skipball-core).

At such a node put `s_S=N_S-q_S` and `h0_S=floor(q_S/2)+1`.  The fibers
appearing in `BWPrim_S(R_S^{bal})` are disjoint half-height fibers, so their
number is at most `floor(N_S/h0_S)`.  Each primitive factor in
`BWPrim_S(R_S^{bal})` is at most `1+s_S`, since `r_lambda>=1`.  Hence

```text
BWPrim_S(R_S^{bal})
 <= floor(N_S/h0_S)(s_S+1)
 <= (s_S+1)^2.                                 (PF2-bw-fixed-node)
```

where the last inequality is the bare-occupancy estimate
(PF2-bare-occ-surplus).  Combining (PF2-balanced-surplus-core),
(PF2-bw-fixed-node), and the terminal skip-ball parametrization gives the
explicit fixed-surplus envelope

```text
sum_{S in Tree_2(A)} PostCore_S^*
 <=
 (s_0+1)^2 + 1+ceil(s_0/(floor(q/2)+1)),       if b_0=0,

 sum_{ell=0}^{min(s_0,b_0-1)}
   binom(b_0-1,ell)
   ((s_0-ell+1)^2
    + 1+ceil((s_0-ell)/(floor((q-b_0+ell)/2)+1))),
                                                        if b_0>0.
                                                        (PF2-postcore-skipball)
```

In particular, using `q_S>=2` on `Tree_2(A)` and `b_0<=q-1`,

```text
sum_{S in Tree_2(A)} PostCore_S^*
 <=
 ((s_0+1)^2+1+ceil(s_0/2))(s_0+1) q^{s_0}.
                                                        (PF2-postcore-fixed)
```

Therefore the entire root-free half-height post-core in (PF2-postcharge-opt)
is `O_sigma(q^sigma)` whenever the initial surplus `s_0<=sigma` is fixed.
This removes bounded-width primitive denominators and the bare half-height
occupancy baseline as possible super-polynomial sources in the fixed-slack M1
regimes.  What remains outside this root-free post-core is exactly the
already-displayed collection of fixed-root tails, diffuse determinant-gate
capacity, and lower-dimensional terminal ledgers.

## Fixed-Surplus Active Tree and Diffuse Ledgers Are Polynomial

The same skip bookkeeping controls the remaining non-fixed-root terms in the
post-charge endpoint.  Let `Active(A)` be the set of canonical nodes with
`F_S^{can}(A)` nonempty.  Every active node has `N_S>=q_S`, so
(PF2-surplus-skip) gives `skip(S)<=s_0`.

Write the ordered base locus as

```text
B_0^*(A)={x_1<...<x_{b_0}}.
```

A nonempty node with maximum `x_m` and `skip(S)=ell` is determined by the
`ell` skipped roots among `x_1,...,x_{m-1}`.  Therefore

```text
#Active(A)
 <=
 1+sum_{ell=0}^{min(s_0,b_0-1)}
     sum_{m=ell+1}^{b_0} binom(m-1,ell)
 =
 1+sum_{ell=0}^{min(s_0,b_0-1)} binom(b_0,ell+1)
 <=
 sum_{j=0}^{s_0+1} binom(b_0,j)
 <= (s_0+2) q^{s_0+1}.                         (PF2-active-skipball)
```

Thus the whole active canonical tree is polynomial-size in fixed-surplus
regimes, not merely its base-free leaves.

This immediately controls the diffuse determinant-gate capacity in
(PF2-postcharge-opt).  For an active `b=2` node, `q_S>=2`,
`N_S=q_S+s_S`, and `0<=s_S<=s_0`.  Since
`G_S^{can}<=binom(N_S,2)`,

```text
4G_S^{can}/q_S^2
 <= 2(N_S/q_S)^2
 <= 2(1+s_0/2)^2.
```

Consequently

```text
sum_{S in Tree_2(A)} 4G_S^{can}/q_S^2
 <= 2(1+s_0/2)^2 (s_0+2) q^{s_0+1}.          (PF2-diffuse-fixed)
```

The lower-dimensional terminal ledger is also polynomial on the same active
tree.  At a `b=0` terminal leaf the contribution is at most `1`.  At a
`b=1` terminal leaf, the root-slice packing bound gives

```text
|F_S^{can}(A)| <= floor((N_S-z_S)/(q_S-z_S)) <= N_S <= q+s_0,
```

because `z_S<=q_S-1`.  Hence

```text
sum_{S in Tree(A)} LowerDim_S^{can}
 <= (q+s_0)(s_0+2) q^{s_0+1}.                 (PF2-terminal-fixed)
```

Combining (PF2-postcharge-opt), (PF2-postcore-fixed),
(PF2-diffuse-fixed), and (PF2-terminal-fixed) gives the fixed-surplus M1
endpoint

```text
|F(A)|
 <=
 sum_{S in Tree_2(A)} FixedRootTail_S
 + O_sigma(q^{sigma+2}),        whenever s_0<=sigma.   (PF2-fixed-surplus-endpoint)
```

Thus in fixed-slack regimes the canonical `b=2` branch has been reduced to
the explicitly displayed fixed-root/root-slice tail ledger, up to a polynomial
remainder.  There is no remaining super-polynomial source from tree depth,
diffuse determinant gates, lower-dimensional leaves, bounded-width primitive
directions, or the root-free half-height occupancy core.

## Fixed-Root Tail Is an Absorbed One-Root Ledger

The remaining tail ledger in (PF2-fixed-surplus-endpoint) has an exact
one-root absorbed form.  Return to the notation of
(PF2-short-tail-factor).  For a half-height fiber `lambda` and a thickening
set `E subset D_{S,lambda}`, put

```text
C=D_{S,lambda}\E,        e=|E|,        j=r_lambda+e,
B_tail(E)=E disjoint_union Z_{S,lambda}^{perp}.
```

The admissible tail range is

```text
0<=e<=floor((q_S-1)/2)-r_lambda,
```

and the quotient-line direction is

```text
Q'_{S,lambda,E}=ell_E R_{S,lambda},        deg Q'_{S,lambda,E}<j.
```

With this notation, (PF2-fixed-tail) is exactly

```text
FixedRootTail_S
 =
 sum_{lambda:h_lambda>q_S/2}
 sum_{E admissible, B_tail(E) nonempty}
   B_{S,lambda}^{prim}.                       (PF2-tail-expanded)
```

Indeed, if `Z_{S,lambda}^{perp}` is nonempty then all admissible `E` are
non-root-free, giving the factor `T(h_lambda,r_lambda)`.  If it is empty,
only `E=empty` is root-free, giving `T(h_lambda,r_lambda)-1`.

Fix once and for all an order on `D_S^{can}` and let

```text
x(E)=min B_tail(E).
```

Because `x(E)` is a zero of `Q'_{S,lambda,E}`, there is a nonzero polynomial

```text
Q_{S,lambda,E}^{x}=Q'_{S,lambda,E}/(X-x(E)),
        deg Q_{S,lambda,E}^{x}<j-1.
```

The root `x(E)` lies in the quotient domain `D_{S,C}`: it is either an
omitted fiber root in `E` or a perpendicular root outside `D_{S,lambda}`.
By the same divisible-kernel identity used for quotient-line packings,
divisibility of the quotient direction by `X-x(E)` means that
`Q_{S,lambda,E}^{x}` is a direction in the one-root absorbed fixed-divisor
kernel.  Moreover the tail cannot have `j=1`: a nonzero polynomial of degree
`<1` has no root.  Thus every term of (PF2-tail-expanded) supplies an
absorbed one-root fixed-divisor direction of positive residual width `j-1`.

The surplus is unchanged by this absorption.  The quotient domain before the
one-root absorption has size

```text
N_{S,C}=N_S-q_S+j.
```

After fixing `x(E)` the domain size is `N_{S,C}-1` and the quotient width is
`j-1`, so

```text
(N_{S,C}-1)-(j-1)=N_S-q_S=s_S.                (PF2-tail-surplus-preserved)
```

Thus every summand of the remaining fixed-root tail is a canonical one-root
absorbed short-kernel ledger with the same surplus and strictly smaller
quotient width.  Combining this with (PF2-fixed-surplus-endpoint), the
fixed-surplus `b=2` branch is now reduced to polynomial terms plus these
surplus-preserving one-root absorbed fixed-divisor ledgers.  This is the
precise form in which a fixed-root/root-slice theorem or induction on the
absorbed width would close the branch.

## Full Bad-Root Absorption Leaves a Root-Free Primitive Packing

The one-root absorbed form can be iterated inside a single tail summand without
changing the surplus.  With `B_tail(E)` as above, put

```text
z=z_{S,lambda}^{perp},        B=B_tail(E),
Q_{S,lambda,E}^{B}=Q'_{S,lambda,E}/ell_B
                  = R_{S,lambda}/ell_{Z_{S,lambda}^{perp}}.
```

The fully absorbed quotient width and domain size are

```text
j_B=j-|B|=r_lambda-z,
N_B=N_{S,C}-|B|=N_S-h_lambda-z.
```

Thus

```text
N_B-j_B=N_S-q_S=s_S.                           (PF2-full-abs-surplus)
```

Moreover `Q_{S,lambda,E}^{B}` has no roots on the fully absorbed domain.
All roots in the original half-height fiber have been removed by `C union E`,
and all remaining roots of `R_{S,lambda}` outside that fiber are precisely
`Z_{S,lambda}^{perp}`, which have also been absorbed.  Hence the packing
factor in each tail summand is exactly the root-free primitive packing on the
fully absorbed domain:

```text
B_{S,lambda}^{prim}
 =
floor(N_B/j_B)
 =
1+floor(s_S/(r_lambda-z_{S,lambda}^{perp})).
                                                        (PF2-tail-full-abs)
```

Consequently the fixed-root tail has no hidden packing loss after all its
bad roots are absorbed.  It is a sum of root-free primitive lower-width
packings with unchanged surplus, indexed by nonempty absorbed bad-root
certificates `B_tail(E)`.  The remaining tail problem is therefore a
certificate-counting or fixed-root-ledger problem: the individual packing
factor has already descended to the same root-free primitive form that was
bounded above, but now on fully absorbed domains and with the displayed
absorbed certificate multiplicity.

## Collapsed Absorbed Tail Certificates Are Polynomial

Full absorption also removes the dependence of the final kernel on the
thickening subset `E`.  For fixed `S` and `lambda`, every admissible tail
summand collapses to the same absorbed fixed-divisor certificate

```text
A_{S,lambda}^{abs}=S union D_{S,lambda}
                   union Z_{S,lambda}^{perp},
Q_{S,lambda}^{abs}=R_{S,lambda}/ell_{Z_{S,lambda}^{perp}},
w_{S,lambda}^{abs}=r_lambda-z_{S,lambda}^{perp}.
```

The fully absorbed direction `Q_{S,lambda}^{abs}` is root-free on the fully
absorbed domain, and its surplus is `s_S` by (PF2-full-abs-surplus).  Thus the
large binomial family of tail choices `E` does not produce a large family of
distinct lower-width kernels after full absorption; it produces one collapsed
absorbed certificate for the half-height fiber `D_{S,lambda}`.  The remaining
work is to charge or lift the pre-absorption certificate multiplicity inside
that fixed absorbed certificate.

The number of such collapsed certificates is polynomial in fixed-surplus
regimes.  At an active node `S`, the half-height fibers are disjoint subsets
of `D_S^{can}`, each of size at least

```text
h0_S=floor(q_S/2)+1.
```

Therefore

```text
#{lambda : |D_{S,lambda}|>q_S/2}
 <= floor(N_S/h0_S)
 <= 1+ceil(s_S/h0_S)
 <= 1+ceil(s_0/2).                              (PF2-collapsed-per-node)
```

Combining this per-node bound with the active skip-ball count
(PF2-active-skipball) gives

```text
#{collapsed absorbed tail certificates over active Tree_2(A)}
 <= (1+ceil(s_0/2))(s_0+2) q^{s_0+1}.          (PF2-collapsed-tail-fixed)
```

Consequently, in fixed-slack regimes the fixed-root tail has only
polynomially many fully absorbed lower-width certificates.  Any remaining
super-polynomial behavior would have to come from the internal lifting
multiplicity from a collapsed absorbed certificate back to its admissible
tail thickenings, not from the number of absorbed kernels or from their
packing factors.

## Exact Collapsed Tail-Lift Factorization

The residual lifting multiplicity can be isolated exactly.  For a
half-height fiber put

```text
L_{S,lambda}^{tail}
 =
 T(h_lambda,r_lambda),       if z_{S,lambda}^{perp}>0,
 T(h_lambda,r_lambda)-1,     if z_{S,lambda}^{perp}=0.
```

Equivalently, `L_{S,lambda}^{tail}` is the number of admissible thickening
sets `E` for which `B_tail(E)` is nonempty.  Since the primitive packing
factor is independent of `E`, (PF2-tail-expanded) and
(PF2-tail-full-abs) give the exact collapsed factorization

```text
FixedRootTail_S
 =
 sum_{lambda:h_lambda>q_S/2}
   L_{S,lambda}^{tail}
   (1+floor(s_S/(r_lambda-z_{S,lambda}^{perp}))).       (PF2-tail-lift-factor)
```

Thus the fixed-root tail consists of a collapsed absorbed packing factor
times an internal tail-lift multiplicity.  In fixed-surplus regimes the
packing factor is uniformly bounded:

```text
1+floor(s_S/(r_lambda-z_{S,lambda}^{perp})) <= s_0+1,
```

so, with

```text
TailLift(A)=
 sum_{S in active Tree_2(A)}
 sum_{lambda:h_lambda>q_S/2} L_{S,lambda}^{tail},
```

one has

```text
sum_{S in Tree_2(A)} FixedRootTail_S
 <= (s_0+1) TailLift(A).                       (PF2-tail-lift-bound)
```

Combining this with (PF2-fixed-surplus-endpoint) yields the sharpened
fixed-surplus endpoint

```text
|F(A)| <= (sigma+1) TailLift(A) + O_sigma(q^{sigma+2}),
        whenever s_0<=sigma.                  (PF2-tail-lift-endpoint)
```

This is now the exact residual target for the fixed-surplus canonical `b=2`
branch: prove that `TailLift(A)` is polynomial, or classify the collapsed
absorbed certificates for which the low-complement lift multiplicity
`L_{S,lambda}^{tail}` is large.  The previous reductions show that no other
part of this branch can contribute a super-polynomial term.

## Near-Threshold Tail Lifts Are Polynomial

The exact tail-lift factorization has a useful immediate consequence: only
deep half-height fibers can create a large lift multiplicity.  Fix an integer
`d>=0`.  If a half-height fiber satisfies

```text
h_lambda-r_lambda<=2d+2,
```

then

```text
floor((h_lambda-r_lambda-1)/2)<=d,
```

and hence

```text
L_{S,lambda}^{tail}
 <= T(h_lambda,r_lambda)
 <= sum_{e=0}^{d} binom(h_lambda,e)
 <= (d+1) q_S^d.                               (PF2-tail-near-bound)
```

Let `TailLift_{>d}(A)` be the part of `TailLift(A)` supported on collapsed
absorbed certificates with

```text
h_lambda-r_lambda>=2d+3.
```

The collapsed-certificate count (PF2-collapsed-tail-fixed) gives

```text
TailLift(A)
 <= TailLift_{>d}(A)
    +(d+1)(1+ceil(s_0/2))(s_0+2) q^{s_0+d+1}.  (PF2-tail-deep-split)
```

Consequently, for fixed `sigma` and fixed `d`,

```text
|F(A)|
 <= (sigma+1) TailLift_{>d}(A)
    + O_{sigma,d}(q^{sigma+d+1}+q^{sigma+2}),
        whenever s_0<=sigma.                  (PF2-deep-tail-endpoint)
```

Thus the remaining fixed-surplus obstruction is not all tail lifting.  It is
the deep-tail subledger where the dominant projective fiber exceeds its
complement width by an unbounded amount.  If one can prove that these deep
collapsed absorbed certificates are quotient-periodic, tangent/fixed-root
degenerate, or otherwise polynomially liftable, then the fixed-surplus
canonical `b=2` branch closes.

## Entropy-Small Tail Lifts Are Polynomial

The entropy estimate gives a sharper scalar target than a fixed-depth cutoff.
For each half-height certificate put

```text
theta_{S,lambda}=
 floor((h_lambda-r_lambda-1)/2)/h_lambda,
E_{S,lambda}=h_lambda H_2(theta_{S,lambda}).
```

Then (PF2-tail-entropy) says

```text
L_{S,lambda}^{tail} <= (h_lambda+1) 2^{E_{S,lambda}}.
```

Fix a real `B>=0` and let `TailLift_{ent>B}(A)` be the part of `TailLift(A)`
supported on collapsed absorbed certificates with

```text
E_{S,lambda}>B log_2 q.
```

On the complementary entropy-small certificates, `h_lambda<=q` gives

```text
L_{S,lambda}^{tail} <= (q+1) q^B.
```

Using the collapsed-certificate count (PF2-collapsed-tail-fixed),

```text
TailLift(A)
 <= TailLift_{ent>B}(A)
    +(q+1) q^B (1+ceil(s_0/2))(s_0+2) q^{s_0+1}.
                                                        (PF2-tail-entropy-split)
```

Thus, for fixed `sigma` and fixed `B`,

```text
|F(A)|
 <= (sigma+1) TailLift_{ent>B}(A)
    + O_{sigma,B}(q^{sigma+B+2}+q^{sigma+2}),
        whenever s_0<=sigma.                  (PF2-entropy-tail-endpoint)
```

The exact remaining obstruction can therefore be narrowed further: it is not
every deep-tail lift, but only collapsed absorbed certificates whose binomial
tail has entropy exponent larger than a chosen multiple of `log q`.  Any
structural theorem forcing quotient-periodic, tangent/fixed-root, or
aperiodic control on these entropy-large certificates would close the
fixed-surplus canonical `b=2` branch.

## Critical Deep-Entropy Tail Certificates Are the Final Local Target

Combining the fixed-depth and entropy splits gives a single residual subledger.
For fixed `d>=0` and `B>=0`, let `TailLift_{crit(d,B)}(A)` be the part of
`TailLift(A)` supported on collapsed absorbed certificates satisfying both

```text
h_lambda-r_lambda>=2d+3,
E_{S,lambda}>B log_2 q.
```

Every non-critical certificate is either near-threshold, hence covered by
(PF2-tail-deep-split), or entropy-small, hence covered by
(PF2-tail-entropy-split).  Therefore

```text
TailLift(A)
 <= TailLift_{crit(d,B)}(A)
    +O_{s_0,d,B}(q^{s_0+d+1}+q^{s_0+B+2}).    (PF2-critical-tail-split)
```

Combining this with (PF2-tail-lift-endpoint) gives

```text
|F(A)|
 <= (sigma+1) TailLift_{crit(d,B)}(A)
    +O_{sigma,d,B}(q^{sigma+d+1}+q^{sigma+B+2}+q^{sigma+2}),
        whenever s_0<=sigma.                  (PF2-critical-tail-endpoint)
```

Thus, for the fixed-surplus canonical `b=2` branch, every previously exposed
source of growth has been reduced to one explicit local object: collapsed
absorbed tail certificates that are simultaneously deep and entropy-large.
A proof that these critical certificates are quotient-periodic, tangent or
fixed-root degenerate, or aperiodically packable would close this branch up to
the displayed polynomial remainder.

## Critical-Tail Criterion for Fixed-Surplus Closure

The reductions above can be packaged as a single closure criterion.  Fix
constants `sigma,d,B`.  Suppose that for every fixed-anchor canonical `b=2`
problem with initial surplus `s_0<=sigma`, the critical deep-entropy lift
ledger satisfies a polynomial bound

```text
TailLift_{crit(d,B)}(A) <= C_{sigma,d,B} q^{K_{sigma,d,B}},
```

or more generally is charged to quotient-periodic, tangent, fixed-root, or
aperiodic ledgers already known to be polynomial in the same window.  Then
(PF2-critical-tail-endpoint) gives

```text
|F(A)| <= C'_{sigma,d,B} q^{K'_{sigma,d,B}}.
                                                        (PF2-critical-closure)
```

Thus the fixed-surplus canonical `b=2` M1 branch has been reduced to a single
paper-ready target: prove polynomial control of the critical collapsed
absorbed certificates.  All other terms in the branch have already been
converted into lower-dimensional leaves, diffuse determinant-gate capacity,
root-free half-height post-core, polynomially many collapsed absorbed
certificates, or polynomial tail-lift regimes.

Equivalently, a counterexample to this fixed-surplus route must now exhibit a
family of collapsed absorbed certificates with bounded initial surplus,
unbounded depth `h_lambda-r_lambda`, entropy exponent above `B log_2 q`, and
super-polynomial lift multiplicity that is not quotient-periodic, tangent,
fixed-root, or aperiodically packable.  This is the current sharp local target
left by the canonical half-height analysis.

## Critical Tail Has a Single-Level One-Root Witness

The critical ledger can be localized one step further.  Fix a collapsed
absorbed certificate `(S,lambda)`, and put

```text
h=h_lambda,        r=r_lambda,
a=floor((h-r-1)/2),        Z=Z_{S,lambda}^{perp}.
```

For `0<=e<=a`, let

```text
Theta_e(S,lambda)
 = { E subset D_{S,lambda} : |E|=e and B_tail(E) nonempty }.
```

For a root `x in D_{S,lambda} union Z`, define the one-root tail slice

```text
Theta_e(S,lambda;x)
 = { E in Theta_e(S,lambda) : x in B_tail(E) },
M_{S,lambda}=max_{e,x} #Theta_e(S,lambda;x).
```

Each pair `(E,x)` with `x in B_tail(E)` is exactly one of the one-root absorbed
fixed-divisor directions from (PF2-tail-surplus-preserved), with the same node
surplus.  The tail multiplicity cannot be spread invisibly across tail levels
and roots.  For a fixed level `e`, if `Z` is nonempty then every root of `Z`
belongs to every member of `Theta_e`, so

```text
#Theta_e(S,lambda) <= M_{S,lambda}.
```

If `Z` is empty then `e=0` contributes nothing and, for `e>=1`, incidence
counting gives

```text
e #Theta_e(S,lambda)
 = sum_{x in D_{S,lambda}} #Theta_e(S,lambda;x)
 <= h M_{S,lambda}.
```

Since `h<=q_S`, summing over the at most `a+1<=q_S` levels gives

```text
L_{S,lambda}^{tail} <= q_S^2 M_{S,lambda}.      (PF2-tail-root-witness)
```

Thus the critical tail is controlled by the one-root critical tail-slice
ledger

```text
RootTail_{crit(d,B)}(A)
 =
 sum_{(S,lambda) critical} M_{S,lambda},
```

via

```text
TailLift_{crit(d,B)}(A)
 <= q^2 RootTail_{crit(d,B)}(A).                (PF2-root-tail-reduction)
```

Consequently polynomial control of these one-root tail slices is sufficient
for the fixed-surplus closure criterion above, with only a harmless `q^2`
loss.  A counterexample cannot merely distribute small lift counts over many
levels; after the polynomial bound on collapsed certificates, it must create
large fixed-level bad-root slices.

Entropy-large certificates also force such a slice quantitatively.  The
standard type bound gives

```text
binom(h,a) >= 2^{h H_2(a/h)}/(h+1).
```

If `(S,lambda)` is entropy-large, so
`h H_2(a/h)>B log_2 q`, then

```text
binom(h,a) > q^B/(q+1).
```

For a critical certificate one has `a>=1`, so the top tail level `e=a` is
nonempty even in the root-free case `Z=empty`.  If `Z` is nonempty, any
perpendicular root lies in all `binom(h,a)` top-level thickenings.  If
`Z=empty`, incidence over the `h` fiber roots gives a fiber root lying in at
least `(a/h)binom(h,a)` top-level thickenings.  Hence in all cases

```text
M_{S,lambda} >= q^B/(q+1)^2.                   (PF2-entropy-root-witness)
```

This is the promised counterexample-first form of the critical tail target:
an entropy-large collapsed certificate is already visible as a large
single-level one-root absorbed slice.  The remaining proof problem is to show
that such high-multiplicity one-root slices are quotient-periodic,
tangent/fixed-root degenerate, or aperiodically packable; finding a primitive
family of them would be a genuine obstruction to the present M1 route.

## Canonical Terminal Leaves Are Explicit Residual Packings

The lower-dimensional term in (PF2-canon-tree) is not a new primitive.  At a
canonical node `S`, put

```text
V_S=span(P_S,Q_S),        b_S=dim V_S,        q_S=q-|S|.
```

Let the base-root order be the one used in the canonical peeling tree.  Define

```text
Old(S)={x in B_0^*(A)\S : x<max(S)}
```

with `Old(empty)=empty`, and set

```text
D_S^{can}=D'\(S union Old(S)),        N_S=|D_S^{can}|.
```

Every quotient support counted by `F_S^can(A)` lies in `D_S^{can}`: the roots
of `S` have already been divided out, and older unpeeled base roots are
forbidden by the canonical rule.

If `b_S=0`, the quotient affine space consists of a single polynomial
`L_{0,S}`.  Since a squarefree support locator determines its support, this
leaf contributes at most one quotient support:

```text
|F_S^can(A)|<=1.                         (PF2-canon-b0)
```

If `b_S=1` and `q_S>0`, choose a nonzero direction `Q_S^*` spanning `V_S` and
write

```text
Z_S={x in D_S^{can} : Q_S^*(x)=0},        z_S=|Z_S|.
```

For two distinct quotient supports `R_1,R_2 in F_S^can(A)`,

```text
ell_{R_1}-ell_{R_2}=lambda Q_S^*
```

for some nonzero scalar `lambda`.  Hence any common root of `R_1` and `R_2`
lies in `Z_S`.  Outside `Z_S`, the quotient supports are pairwise disjoint.
Because `deg Q_S^*<q_S`, one has `z_S<=q_S-1`, so every quotient support has at
least `q_S-z_S` roots outside `Z_S`.  Incidence counting on
`D_S^{can}\Z_S` gives

```text
|F_S^can(A)| <= floor((N_S-z_S)/(q_S-z_S)).       (PF2-canon-b1)
```

Moreover `Z_S` is exactly the bad one-root slice set of the descended
fixed-divisor problem, restricted to the canonical admissible domain, by the
same divisible-kernel identity used in (LKB).  Thus the terminal term in the
canonical tree is explicit:

```text
LowerDim_S^can <=
  1,                                           if b_S=0,
  floor((N_S-z_S)/(q_S-z_S)),                  if b_S=1.
```

Consequently the `b=2` peeling tree has no hidden lower-dimensional reservoir.
The only residual payments are singleton zero-direction leaves, ordinary
one-dimensional root-slice packings, and the no-base determinant-gate terms at
canonical `b=2` nodes.

## Bad Root Slices Are Absorbed-Anchor Rank Defects

The preceding bad-root condition has an equivalent absorbed-anchor form.  Fix
`x in D'=H\(U union W)` and put

```text
E_x=ell_W (X-x),
h^{W,x}_i=sum_{a=0}^{d+1} (E_x)_a s_{i+a}.
```

For every polynomial `Q_x` with `deg Q_x<q-1`,

```text
(H_{q,q-1}(h^{W,x})Q_x)_i
 = (H_{q,q+d-1}(s)(ell_W (X-x)Q_x))_i,
        0<=i<q.                                  (ART)
```

Thus `x` is a bad one-root slice for the fixed anchor `(U,W)` if and only if
the rectangular absorbed-anchor matrix

```text
A_x(U,W)=(h^{W,x}_{i+j})_{0<=i<q, 0<=j<q-1}
```

fails to have full column rank `q-1`.

Consequently, a full-column-rank statement for all absorbed roots
`x in D'` is exactly the no-overlap input needed by the previous section.  If
all matrices `A_x(U,W)` have rank `q-1`, then residual completions over the
fixed anchor are pairwise disjoint and the residual fiber is bounded by
`floor(|D'|/q)`.  If some `A_x` drops rank, the obstruction has already moved
to a concrete one-extra-row absorbed-anchor kernel, which is a fixed-root
short-kernel ledger.

The verifier now checks (ART) directly while computing the one-root
root-slice ranks.  In the largest `F_7^*` audit, all `259200` absorbed-anchor
matrices tested have full column rank; the productive subaudit has the same
counts.

## Absorbed-Rank Defects Give a Residual-Fiber Closure Bound

The absorbed-rank formulation gives a direct fixed-anchor closure criterion.
Let

```text
F(U,W) = { R subset D' : |R|=q and ell_R in K(U,W) },
N      = |D'|,
Z_1(U,W)= { x in D' : rank A_x(U,W) < q-1 },
z      = |Z_1(U,W)|.
```

Then, for `q>=2`,

```text
|F(U,W)|
 <= floor( ((N-z) + z binom(N-1,q-1)) / q ).     (ARC)
```

Proof: count incidences `(R,x)` with `R in F(U,W)` and `x in R`.  There are
`q |F(U,W)|` such incidences.  If `x notin Z_1(U,W)`, the previous section
shows that `x` cannot lie in two distinct residual supports, so all good roots
contribute at most `N-z` incidences.  If `x in Z_1(U,W)`, use only the trivial
bound that `x` lies in at most `binom(N-1,q-1)` squarefree `q`-subsets of
`D'`.  Dividing by `q` gives (ARC).

Thus the residual-anchor problem is now split into two explicit pieces:
packing over full-rank absorbed roots, and a weighted count of absorbed-rank
defect roots.  If `z=0`, (ARC) reduces to the disjoint packing bound
`floor(N/q)`.  If `z` is small after quotient-periodic and fixed-root charges,
then residual completions remain polynomially controlled.

The verifier asserts (ARC) for every produced deficit anchor with `q>=2`.
In the largest `F_7^*` audit, it checks the same `51840` residual fibers and
`259200` absorbed-root tests; all have `z=0`, so the audited bound is the
full-rank disjoint-packing case.  The productive subaudit has the same counts.

## Absorbed-Rank Defects Are Finite or Persistent

For a fixed deficit anchor `(U,W)`, the absorbed matrix is an affine pencil in
the absorbed root.  Indeed, with `E=ell_W`,

```text
h^{W,x}_i = h^W_{i+1} - x h^W_i,
```
and hence

```text
A_x(U,W) = B(U,W) - x C(U,W)
```

is a `q x (q-1)` matrix pencil whose entries are affine functions of `x`.
The bad-root condition `rank A_x(U,W)<q-1` is the simultaneous vanishing of
all `(q-1) x (q-1)` minors of this pencil.  Each such minor is a polynomial in
`x` of degree at most `q-1`.

Therefore exactly one of the following holds.

1. Some maximal minor is not the zero polynomial.  Then

```text
|Z_1(U,W)| <= q-1.                               (AFP)
```

2. Every maximal minor vanishes identically.  Equivalently, the pencil
`A_x(U,W)` has rank `<q-1` over the rational function field `F(x)`.  This is
a persistent absorbed-rank defect.

Combining (AFP) with (ARC), every nonpersistent fixed anchor satisfies

```text
|F(U,W)|
 <= floor( ((N-(q-1)) + (q-1) binom(N-1,q-1)) / q ).
```

Thus the remaining residual-anchor obstruction has a sharper form: either
each anchor has only `q-1` bad absorbed roots and is polynomially
packing-bounded, or the anchor carries a persistent low-rank affine Hankel
pencil.  The latter is now the named object to classify or charge to
quotient-periodic, fixed-root, tangent, or aperiodic ledgers.

The current verifier data land in the finite branch with room to spare: in
the largest `F_7^*` audit, every produced anchor has `|Z_1(U,W)|=0`, hence no
persistent absorbed-rank candidate is seen.

## Persistent Absorbed Defects Have Moving-Kernel Certificates

The persistent branch above is certificate-form.  Write the absorbed parameter
as `z` and the locator variable as `X`.  A persistent absorbed-rank defect for
`(U,W)` is equivalent to the existence of a nonzero polynomial family

```text
Q_z(X)=sum_{a=0}^{q-2} Q_a(z) X^a in F[z][X],
deg_X Q_z < q-1,
```

such that

```text
H_{q,q+d-1}(s)(ell_W (X-z) Q_z(X)) = 0          (MKC)
```

as an identity in `F[z]^q`.  Moreover `Q_z` may be chosen with

```text
max_a deg_z Q_a <= q-2.
```

Proof: the persistent condition is `rank A_z(U,W)<q-1` over `F(z)`, where
`A_z` is the `q x (q-1)` absorbed Hankel pencil.  Hence its right kernel over
`F(z)` is nonzero.  Clearing denominators gives a nonzero vector
`(Q_0(z),...,Q_{q-2}(z)) in F[z]^{q-1}` killed by `A_z`, which is exactly
(MKC) by (ART).  Conversely, any nonzero `Q_z` satisfying (MKC) gives a
nonzero right-kernel vector over `F(z)`, so the pencil has rank `<q-1`
persistently.  For the degree bound, choose a full-rank `r x r` minor over
`F(z)` with `r=rank A_z<=q-2`; the standard cofactor construction gives a
kernel vector whose entries are `r x r` minors of an affine matrix, hence have
`z`-degree at most `r<=q-2`.

Thus the residual-anchor branch now has a finite certificate target: either
there are at most `q-1` bad absorbed roots, or one can exhibit a bounded-degree
moving denominator `Q_z(X)` satisfying the explicit Hankel identity (MKC).
The next M1 task is to classify such moving kernels as quotient-periodic,
fixed-root/tangent, or genuinely aperiodic; a proof that no primitive
aperiodic moving kernel survives after the known charges would close this
residual branch.

## Moving-Kernel Coefficients Force Endpoint Kernels

The moving-kernel certificate has immediate endpoint consequences.  Write

```text
Q_z(X)=sum_{m=0}^D z^m R_m(X),
```

with `R_0` and `R_D` nonzero after removing any common power of `z`.  Expanding
(MKC) in powers of `z` gives the coefficient ladder

```text
H_{q,q+d-1}(s)(ell_W X R_0)=0,
H_{q,q+d-1}(s)(ell_W (X R_m - R_{m-1}))=0, 1<=m<=D,
H_{q,q+d-1}(s)(ell_W R_D)=0.
```

In particular, every persistent absorbed-rank defect supplies a nonzero
endpoint kernel `R_D` for the map

```text
R |-> H_{q,q+d-1}(s)(ell_W R),        deg R < q-1.
```

Consequently a fixed deficit anchor whose endpoint matrix

```text
E(U,W) = ( H_{q,q+d-1}(s)(ell_W X^a) )_{0<=a<q-1}
```

has full column rank cannot carry a persistent absorbed-rank defect.  The
bottom coefficient gives the parallel shifted endpoint condition
`H_{q,q+d-1}(s)(ell_W X R_0)=0`, so any remaining primitive moving-kernel
obstruction must pass through both endpoints of this ladder, not merely through
one singular absorbed value.

The verifier now audits the unshifted endpoint rank for every produced deficit
anchor with `q>=2`.  The largest `F_7^*` audit checks `51840` such endpoint
matrices and finds no endpoint-rank defects.

## Endpoint Defects Are Residual-Direction Defects

The endpoint obstruction is contained in the residual-kernel obstruction already
isolated above.  Let

```text
M(U,W)=(h^W_{i+a})_{0<=i<q, 0<=a<q}
```

be the square residual moment matrix, and let `E(U,W)` be the endpoint matrix
from the previous section.  Then `E(U,W)` is the first `q-1` columns of
`M(U,W)`.  Therefore, if

```text
b(U,W)=q-rank M(U,W),
e(U,W)=(q-1)-rank E(U,W),
```

then

```text
e(U,W) <= b(U,W).                                  (ERD)
```

Equivalently, every endpoint kernel `R` with `deg R<q-1` lies in

```text
Dir K(U,W)
 = { Q in F[X]_{<q} : H_{q,q+d}(s)(ell_W Q)=0 }.
```

Combining this with the moving-kernel coefficient ladder gives a useful
collapse:

```text
persistent absorbed-rank defect  =>  b(U,W)>0.
```

Thus persistent absorbed pencils do not create a second independent residual
branch.  After the positive-dimensional fixed-divisor residual kernels
`Dir K(U,W)` are charged to fixed-root, quotient-periodic, tangent, or aperiodic
ledgers, the persistent absorbed branch is charged as well.  In particular, if
`b(U,W)<=B`, the fixed-anchor residual fiber remains bounded by

```text
sum_{i=0}^B binom(|D'|,i)
```

whether or not the absorbed pencil is persistent.

The verifier now asserts the endpoint-prefix identity and the inequality
`e(U,W)<=b(U,W)` on the same endpoint-rank audit.  In the largest `F_7^*` run,
the checked anchors have `e(U,W)=b(U,W)=0`.

## Deficit-Weighted Core Closure Criterion

The preceding local packing theorem removes the artificial cutoff
`|M(S)|<=tau+1` from the earlier closure criterion.  For `m>=1`, let
`Cert_m(s)` be the set of all split-support certificates of mode size `m`:

```text
Cert_m(s)
 = { (S,Y) : S active, Y subset M(S), |Y|=m }.
```

For `U in Core_r(s)`, define

```text
d(U,r)=max(0,r-tau-|U|),
P(U,r)=floor( binom(n-|U|,d(U,r)) / binom(r,d(U,r)) ).
```

Then every `m` satisfies the all-frontier closure bound

```text
|Cert_m(s)|
 <= sum_{r>=m} binom(r,m)
      sum_{U in Core_r(s)} P(U,r).                 (DWCC)
```

Proof: group certificates by the canonical unmarked core `U` and marked
count `r`.  For a fixed active support `S` with `|M(S)|=r`, the marked-exit
factorization gives exactly `binom(r,m)` mode-size `m` certificates.  For
fixed `U` and `r`, the moment-complete theorem gives one support when
`d(U,r)=0`, and the deficit-packing theorem gives at most `P(U,r)` supports
when `d(U,r)>0`.  Multiplying by `binom(r,m)` and summing over all core
ledgers proves (DWCC).

The sharpened boundary criterion (CC') is the special case `r<=tau+1`:
for `r<=tau` all cores have `d=0`; for `r=tau+1` every nonempty core has
`d=0`, while the empty core has `d=1` and contributes
`floor(n/(tau+1))`.  Thus the same formula now covers large marked
frontiers without adding a new uncontrolled multiplicity term.

Consequently the remaining M1 split-support task can be phrased as a
deficit-weighted core ledger problem.  For fixed `m`, it is enough to prove a
polynomial bound for the weighted sum

```text
sum_{r>=m} binom(r,m) sum_{U in Core_r(s)} P(U,r),
```

after quotient-periodic, tangent, and known endpoint ledgers are charged.  In
particular, if the inner weighted core ledgers are bounded uniformly by
`n^B`, then (DWCC) gives `|Cert_m(s)|=O_m(n^{B+m+1})`.  Any surviving
super-polynomial obstruction must create too many weighted canonical cores;
it cannot be hidden in repeated marked frontiers over one core.

## Empty-Core Endpoint Is The Boundary Moment Map

It remains to identify the empty-core boundary exception left by the
nonempty-core theorem.
Put `r=tau+1` and `U=empty`.  Then an active support `S` with
`M(S)=S` and `|S|=r` is exactly a nonzero `r`-sparse representation of the
fixed boundary moment vector

```text
g=(s_0,s_1,...,s_{2r-2}).
```

More explicitly, if `S` is full-marked, then

```text
g_i=sum_{y in S} a_y y^i,        0<=i<=2r-2,
        a_y=b_y(S)/prod_{z in S, z!=y}(y-z).       (EC)
```

Conversely, if a set `Y subset H`, `|Y|=r`, and nonzero amplitudes `a_y`
satisfy (EC) with `S` replaced by `Y`, then `Y` is active at row `tau` and
all roots of `Y` are marked.  Indeed, applying `ell_Y` to the sparse moment
sequence gives the `tau=r-1` active zero rows, and applying
`ell_{Y\{y}}` leaves the nonzero geometric boundary

```text
a_y prod_{z in Y, z!=y}(y-z) (1,y,...,y^tau).
```

Therefore the only boundary ambiguity left by the canonical-core closure is
precisely the boundary moment fiber already classified earlier.  Distinct
supports in one fiber are disjoint, so every empty-core boundary fiber has
size at most `floor(n/r)`.  In the full-domain root-of-unity case `n=2r`,
the only nontrivial fibers are the root-linear complement pairs

```text
(Y, (nu y)_{y in Y})  <->  (H\Y, (-nu z)_{z in H\Y}).
```

Thus the refined canonical-core closure has no residual overlapping boundary
cluster: nonempty cores are support-unique, and the empty core is the known
matching/root-linear endpoint.

The verifier records this endpoint separately.  In the largest `F_7^*` audit
there are `17220` produced empty-core boundary fibers carrying `17280`
labels, maximum fiber size `2`, with `60` produced complement-pair checks.
In the full-domain case `n=6=2r`, all nontrivial produced pairs are
root-linear complements; the audit records `480` root-linear produced labels.

## Fixed Anchors Have Matching-Bounded Fibers

Fix the collapsed anchor base `A` and the mode size `m`.  Then

```text
g_A=H_{tau+m,|A|}(s)ell_A
```

is fixed.  By the equivalence above, split-support certificates over this
anchor are exactly nonzero `m`-sparse representations of `g_A` on the
available domain `H\A`.

If `m<=tau`, the first `2m` moments of `g_A` are visible, so the usual Prony
annihilator argument recovers the mode locator and the amplitudes uniquely.
Thus a fixed anchor has at most one `m`-mode split-support certificate below
the boundary.

At the maximal boundary `m=tau+1`, only `2m-1` moments are visible.  Still,
two different `m`-supports in the same fixed-anchor fiber cannot meet: their
difference would be a nonzero measure on at most `2m-1` roots with vanishing
first `2m-1` moments, contradicting the square Vandermonde determinant.  Once
the support is fixed, amplitudes are recovered from the first `m` moments.
Therefore every fixed-anchor boundary fiber has size at most

```text
floor((n-|A|)/m).                              (AF)
```

This improves the earlier global boundary matching bound by removing the
anchor roots from the available domain.  Consequently repeated production at
one fixed anchor is either impossible below the boundary or is a matching-type
boundary alias; it is not a new overlapping support cluster.

The verifier audits the fixed-anchor fibers of the produced split-support
certificates.  In the largest `F_7^*` audit, it sees `34500` fixed-anchor
fibers carrying `34560` labels, with maximum fiber size `2`; the productive
subaudit sees `32340` fibers carrying `32400` labels, again with maximum
fiber size `2`.

## Partial Mode Absorption Is Lossless

The split-support certificate is stable when packet modes are absorbed into
the anchor.  With `A`, `Y`, and `a_y` as above, let `E subset Y` and put

```text
A_E=A union E,        Y_E=Y\E,        ell_E(X)=prod_{e in E}(X-e).
```

Then

```text
H_{tau+m-|E|,|A_E|}(s)ell_{A_E}
 = (sum_{y in Y_E} a_y ell_E(y) y^i)_{0<=i<=tau+m-|E|-1}.      (PA)
```

If `E` is a proper subset of `Y`, the right side is nonzero because the
remaining amplitudes `a_y ell_E(y)` are nonzero.  If `E=Y`, the right side is
zero and (PA) is exactly the active support equation for `A union Y`.

Proof: multiply the sparse moment sequence by `ell_E`.  Each absorbed mode in
`E` is killed, and each remaining mode `y` is multiplied by the nonzero scalar
`ell_E(y)`.  The available row window loses exactly `|E|` rows.

Thus the split-support packet has no hidden intermediate collapse: every
proper partial absorption remains a smaller nonzero sparse packet, and full
absorption is precisely the active split-support relation.  This gives an
inductive object for M1: one may move packet modes into the anchor one subset
at a time without leaving the split-support packet category.

The verifier checks (PA) for every nonempty subset of modes of every produced
packet.  In the largest `F_7^*` audit this gives `120960` partial-absorption
checks, of which `86400` are proper nonzero absorptions.  The productive
subaudit contributes `114480` absorptions, of which `82080` are proper.

## Split-Support Packets Contain Zero-Free Mode Cubes

Partial absorption gives an ordered form.  For any ordering

```text
(y_1,...,y_m)
```

of the mode set `Y`, absorb the prefix
`E_h={y_1,...,y_{h-1}}` before deleting `y_h`.  By (PA), the current boundary
scalar is

```text
a_{y_h} ell_{E_h}(y_h)
 prod_{z in Y\E_h, z!=y_h}(y_h-z),
```

which is nonzero.  Hence every ordering of `Y` is a zero-free mode flag inside
the collapsed split-support chart `(A,Y)`.  The packet contributes exactly
`m!` intrinsic ordered mode flags.

This is not a new deletion-tree multiplicity claim for the original core,
because the collapsed anchor `A` already contains the lower core.  It is the
right intrinsic statement for the split-support certificate: its mode cube has
all proper vertices nonzero, and the only zero vertex is the full absorption
`A union Y`.

The verifier now records this intrinsic ordered count.  In the largest
`F_7^*` audit, the split-support packets contain `86400` zero-free ordered
mode flags, with `82080` coming from productive packets.

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
