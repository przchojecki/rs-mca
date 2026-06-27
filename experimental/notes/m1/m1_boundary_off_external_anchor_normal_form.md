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

## Corollary 2.1: Explicit Coefficient Ledger For The Anchor Quadrics

For fixed `S` and row indices `alpha<gamma`, write

```text
A = A_u(S),        B = B_u(S),
C = A_v(S),        D = B_v(S).
```

For two row-vectors `P,Q in F^t`, put

```text
W_{alpha,gamma}(P,Q)=P_alpha Q_gamma - P_gamma Q_alpha.
```

Then the external-anchor minor has the exact coefficient expansion

```text
Q_{alpha,gamma,S}(Y)
  = W(A,C)
    - Y ( W(B,C) + W(A,D) )
    + Y^2 W(B,D),                                  (CQ)
```

where `W` means `W_{alpha,gamma}`.

Consequently, the ruled condition for a shadow `S` is equivalent to the
simultaneous vanishing, for every `alpha<gamma`, of the three coefficient
families

```text
W(A_u(S),A_v(S)) = 0,
W(B_u(S),A_v(S)) + W(A_u(S),B_v(S)) = 0,
W(B_u(S),B_v(S)) = 0.                              (Rcoef)
```

In the special case `t=2`, this is a three-scalar test for whether the
external-anchor line over `S` is ruled.

### Proof

The minor is

```text
Q(Y)=W(A-YB,C-YD).
```

Expanding by bilinearity and skew-symmetry of `W` gives (CQ). A polynomial of
degree at most two is identically zero if and only if its three coefficients
vanish, giving (Rcoef). When `t=2` there is only one row pair.

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

## Corollary 4: The Nondegenerate Branch Is A Shadow-Image Problem

Let `A_var` be the active all-domain locator family used in the residual
ledger of `m1_hankel_variable_line_packet_lemma.md`. Define the first boundary
shadow image

```text
Shadow_1(A_var)
  = { S subset D :
      |S|=j-1 and there exists T in A_var with |S cap T|=j-2 }.
```

Let `Shadow_1^quad(A_var)` be the subset of shadows that occur from
nondegenerate boundary targets. Then

```text
|Boundary_off^quad| <= 2 |Shadow_1^quad(A_var)|
                    <= 2 |Shadow_1(A_var)|.          (SH)
```

In particular, if the quotient-aware aperiodic ledger gives

```text
|Shadow_1^quad(A_var)| <= n^B,
```

then the nondegenerate quadratic-anchor part of the one-outside boundary image
is polynomially bounded. Without using any aperiodic structure one has the
crude sanity bound

```text
|Shadow_1(A_var)|
  <= binom(j,2)(n-j)|A_var|.                          (SH0)
```

### Proof

Theorem 1 gives an active all-domain neighbor `T in A_var` for every
one-outside boundary target, so its domain part `S=B cap D` lies in
`Shadow_1(A_var)`. Corollary 2 says that, on a nondegenerate shadow `S`, at
most two external anchors `beta` can satisfy the boundary Hankel gate. This
proves (SH).

For (SH0), fix `T in A_var`. To form a shadow `S` with `|S cap T|=j-2`, choose
the two roots of `T` that are omitted and choose the one new domain point from
`D\T`. This gives at most `binom(j,2)(n-j)` shadows over `T`.

## Corollary 5: Ruled Shadows Have Fixed-Slope Or Row-Cut Form

Fix a ruled shadow `S`.

In the common-kernel branch there is a nonzero pair `(lambda,mu) in F^2` such
that

```text
lambda a_S(beta) + mu b_S(beta) = 0                  (K)
```

for every external anchor `beta`. If `lambda != 0`, every boundary target over
this shadow with `b_S(beta) != 0` has the same finite boundary slope

```text
z = mu/lambda.
```

If `lambda=0`, then `b_S(beta)=0` for the whole external-anchor pencil.

In the common-image branch, let `E_S subset (F^t)^*` be the annihilator of the
common image line. Then for every `eta in E_S` and `w in {u,v}` the shadow
locator `L_S` satisfies the two row-cut equations

```text
eta H_{t,j}(w) ell_S^0 = 0,
eta H_{t,j}(w) ell_S^+ = 0.                          (RC)
```

Equivalently, common-image ruled shadows are split degree-`j-1` locators lying
in the row-cut system cut out by the lower and upper shifted contractions of
the two Hankel windows.

More generally, fix an image line `I subset F^t`, let `E=I^perp`, and let
`V_I` be the affine solution space on monic degree-`j-1` locators defined by
(RC) for all `eta in E` and `w in {u,v}`. If the direction space of `V_I`
has dimension at most `j-1-d`, with `0<=d<=j-1`, then the number of `D`-split
shadows in this fixed-image stratum is at most

```text
binom(n,j-1-d).                                      (RCd)
```

### Proof

The common-kernel assertion is just the definition of that ruling applied to
the matrices `[a_S(beta) b_S(beta)]`. If `lambda != 0`, the equation
`a_S(beta)+z b_S(beta)=0` holds with `z=mu/lambda`. If `lambda=0`, then
`mu != 0` and hence `b_S(beta)=0` for all `beta`.

In the common-image branch, every column of every matrix

```text
M_S(beta)=[a_S(beta) b_S(beta)]
```

lies in the fixed image line. Applying any `eta` that kills this line gives

```text
eta a_S(beta)=0,        eta b_S(beta)=0
```

for every `beta`. Since

```text
a_S(beta)=H(u)ell_S^+ - beta H(u)ell_S^0,
b_S(beta)=H(v)ell_S^+ - beta H(v)ell_S^0,
```

the constant and linear coefficients in `beta` vanish separately. This gives
(RC).

For (RCd), write the monic shadow solutions as an affine space `P_0+V`, where
`V` is a vector space of polynomials of degree `<j-1` and
`dim V <= j-1-d`. For every split locator `L_S` in this affine space,
evaluation `V -> F^S` is injective because a nonzero polynomial of degree
`<j-1` cannot vanish on all `j-1` distinct roots of `S`. Hence some
`(j-1-d)`-subset `R subset S` already gives an injective evaluation map on
`V`. Choosing the first such `R` injects the split locators into the
`(j-1-d)`-subsets of `D`, because a fixed `R` determines the unique member of
`P_0+V` vanishing on `R`.

## Corollary 6: Common-Kernel Ruled Shadows Are Fixed-Slope Pencils

Keep a ruled shadow `S` in the common-kernel branch, and write

```text
P_z = H_{t,j}(u) + z H_{t,j}(v).
```

If the common-kernel relation has `lambda != 0`, put `z=mu/lambda`. Then

```text
P_z ell_S^0 = 0,        P_z ell_S^+ = 0.             (FS)
```

Consequently every external-anchor locator over this shadow satisfies

```text
P_z ell_{S,beta}=0        for every beta in F.
```

Thus the finite common-kernel ruled branch is contained in a fixed-slope
two-dimensional kernel slice spanned by `ell_S^0` and `ell_S^+`. It is not a
new moving-anchor branch; any future bound may charge it to the fixed-slope or
root-slice ledger once the corresponding one-outside boundary slice is allowed
in that ledger.

If instead `lambda=0`, then

```text
H_{t,j}(v) ell_S^0 = 0,        H_{t,j}(v) ell_S^+ = 0,
```

so every external-anchor locator over `S` lies in the boundary-contained
pencil for the direction endpoint `g`.

### Proof

The common-kernel relation is

```text
lambda a_S(beta) + mu b_S(beta) = 0
```

for every `beta`. If `lambda != 0`, divide by `lambda` and set
`z=mu/lambda`; then

```text
a_S(beta)+z b_S(beta)=P_z ell_{S,beta}=0
```

for every `beta`. Since `ell_{S,beta}=ell_S^+-beta ell_S^0`, the constant and
linear coefficients in `beta` vanish separately, proving (FS). The displayed
fixed-slope assertion follows by linearity.

If `lambda=0`, then `mu != 0`, so `b_S(beta)=0` for every `beta`. Expanding
`b_S(beta)=H(v)ell_S^+-beta H(v)ell_S^0` and comparing coefficients gives the
boundary-contained alternative.

## Corollary 7: Full Shadow Stars Force Evaluation Row Cuts

Let `m=j-1`, let `alpha in D`, assume `|D\{alpha}| >= m`, and let

```text
h ell_S = 0
```

be a row-cut hyperplane on monic degree-`m` shadow locators. Suppose this
hyperplane contains the whole shadow star through `alpha`:

```text
h ell_{{alpha} union U}=0
        for every U subset D\{alpha}, |U|=m-1.
```

Then `h` is a scalar multiple of the evaluation row

```text
(1, alpha, alpha^2, ..., alpha^m).
```

Consequently the row-cut hyperplane is exactly

```text
L_S(alpha)=0.
```

For squarefree `D`-split shadow locators, this is precisely the fixed-root
shadow star `alpha in S`. Thus a common-image row-cut packet containing a full
shadow star is not a new boundary obstruction; that full-star part belongs to
the fixed-root/root-slice ledger.

### Proof

Write `S={alpha} union U` and `L_S=(X-alpha)L_U`, where `L_U` is monic of
degree `m-1` and split over `D\{alpha}`. Define a linear functional on
degree-`<=m-1` coefficient vectors by

```text
psi(Q)=h((X-alpha)Q).
```

By hypothesis, `psi(L_U)=0` for every split monic `L_U` with roots in
`D\{alpha}`.

Since `|D\{alpha}| >= m`, choose `Y subset D\{alpha}` of size `m`. The `m`
monic degree-`m-1` polynomials

```text
L_{Y\{y}}(X),        y in Y,
```

are affinely independent in the monic slice: evaluating at the points of `Y`
gives a diagonal matrix with nonzero diagonal entries. Hence their affine span
is the full monic degree-`m-1` slice. Because `psi` vanishes on all of them,
it vanishes on the full monic slice, and therefore on every degree-`<=m-1`
coefficient vector.

Thus `h` annihilates the image of multiplication by `X-alpha`. The cokernel of
that multiplication map is one-dimensional and is generated by evaluation at
`alpha`. In coefficient coordinates this row is
`(1,alpha,...,alpha^m)`.

For a squarefree `D`-split shadow locator, `L_S(alpha)=0` holds exactly when
`alpha in S`.

## Corollary 8: Star-Free Shadow Row Cuts Gain A Slice Factor

Let `m=j-1>=2`, and let

```text
h=(h_0,...,h_m)
```

be a nonzero row cut on monic degree-`m` shadow locators. For `beta in D`,
define the contraction

```text
C_beta(h)=(h_1-beta h_0, h_2-beta h_1, ..., h_m-beta h_{m-1}).
```

On shadows containing `beta`, the row-cut condition is exactly

```text
C_beta(h) ell_U = 0,
```

where

```text
S={beta} union U,        L_S(X)=(X-beta)L_U(X),
```

and `L_U` is a monic degree-`m-1` locator on `D\{beta}`.

Assume `|D\{beta}| >= m` for every `beta in D` and that the row-cut packet
contains no full shadow star. If `N_h` is the number of squarefree `D`-split
monic degree-`m` shadow locators satisfying `h ell_S=0`, then

```text
N_h <= (n/m) binom(n-1,m-2)
     = ((m-1)/m) binom(n,m-1).                       (SF)
```

Thus, after full stars have been moved to the fixed-root/root-slice ledger,
each remaining rank-one row-cut packet improves on the bare one-root-loss
bound `binom(n,m-1)` by the factor `(m-1)/m`.

### Proof

For `S={beta} union U`, write

```text
L_U(X)=q_0+q_1X+...+q_{m-1}X^{m-1}.
```

The coefficient vector of `(X-beta)L_U` is

```text
(-beta q_0, q_0-beta q_1, ..., q_{m-2}-beta q_{m-1}, q_{m-1}).
```

Taking the dot product with `h` gives

```text
h ell_S = C_beta(h) ell_U.
```

If the packet contains no full shadow star, then Corollary 7 implies
`C_beta(h) != 0` for every `beta`. For fixed `beta`, the contracted row cut is
a nonzero affine linear equation on monic degree-`m-1` locators over
`D\{beta}`. Its solution space has direction dimension at most `m-2`, so the
same evaluation-injection argument as in Corollary 5 bounds the number of
split `U` by

```text
binom(n-1,m-2).
```

Counting incidences `(beta,S)` with `beta in S` gives

```text
m N_h <= n binom(n-1,m-2),
```

which is (SF).

## Non-Claims

This note does not prove

```text
|Boundary_off| <= n^B.
```

It also does not prove the all-line M1 theorem, a corrected-reserve MCA bound,
or a prize threshold. It only proves the local external-anchor normal form and
the nondegenerate/ruled split for the boundary target image already isolated in
the variable-line packet lemma.
