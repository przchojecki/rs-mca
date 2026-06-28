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

## Corollary 9: Polynomial-Field Closure Criterion

Let `q=|F|`. After fixed-root/root-slice full shadow stars from Corollary 7
have been charged, let `Boundary_off^red` be the remaining one-outside
boundary target set covered by Theorem 1.

Let the following reduced shadow ledgers be the corresponding branch images
(with overlaps allowed, or with any admissible branch assignment for shadows
that satisfy more than one ruled description):

```text
Sh_quad = nondegenerate quadratic-anchor shadows,
Sh_ker  = finite common-kernel fixed-slope ruled shadows,
Sh_cont = boundary-contained endpoint ruled shadows,
Sh_img  = common-image row-cut shadows after full stars are removed.
```

Then

```text
|Boundary_off^red|
  <= 2 |Sh_quad| + q ( |Sh_ker| + |Sh_cont| + |Sh_img| ).          (BC)
```

Consequently, in a polynomial-field window `q <= n^B_F`, polynomial bounds

```text
|Sh_quad| <= n^B_Q,      |Sh_ker| <= n^B_K,
|Sh_cont| <= n^B_C,      |Sh_img| <= n^B_I
```

imply the polynomial boundary-off bound

```text
|Boundary_off^red|
  <= 2 n^B_Q + n^(B_F+B_K) + n^(B_F+B_C) + n^(B_F+B_I).
```

Thus the boundary-off problem is reduced, in the polynomial-field regime, to
polynomial shadow-image estimates for the four ledgers above, together with
the already separated fixed-root/full-star charges.

### Proof

For a nondegenerate shadow, Corollary 2 gives at most two external anchors
`beta`. This contributes `2 |Sh_quad|`.

For a ruled shadow, the whole external-anchor pencil may satisfy the Hankel
gate. Without a sharper branch-specific estimate, the only uniform
multiplicity bound over a fixed shadow is the field-size bound `q`, since
`beta` ranges over `F\D`. Corollaries 5 and 6 classify every ruled shadow into
the finite common-kernel fixed-slope branch, the boundary-contained endpoint
branch, or the common-image row-cut branch. Corollary 7 moves full shadow
stars in the common-image row-cut branch to the fixed-root/root-slice ledger;
the remaining common-image shadows are, by definition, counted in `Sh_img`.
Summing these shadow multiplicities gives (BC).

The displayed polynomial estimate is (BC) with `q <= n^B_F` and the four
shadow-ledger hypotheses substituted.

## Corollary 10: Common-Image Row-Rank Certificate

Let `m=j-1`. Fix a projective image line `I subset F^t`, put
`E=I^perp`, and choose any basis of `E`. For `w in {u,v}` and
`sigma in {0,+}`, let

```text
L_S -> eta H_{t,j}(w) ell_S^sigma
```

run over the lower and upper shifted common-image row cuts from Corollary 5,
with `eta` in the chosen basis of `E`. These affine equations act on the
monic degree-`m` shadow-locator slice

```text
L(X)=X^m+c_{m-1}X^{m-1}+...+c_0.
```

Let `A_I` be their affine solution space, let `V_I` be its direction space,
and put

```text
d_I = dim V_I.
```

Equivalently, if `rk_I` is the rank of the homogeneous row-cut matrix on the
`m` lower coefficients, then

```text
d_I <= m-rk_I.
```

Let `Sh_img(I)` be any set of squarefree `D`-split shadows assigned to this
fixed image-line row-cut system after full shadow stars have already been
charged to the fixed-root/root-slice ledger. Then

```text
|Sh_img(I)| <= binom(n,d_I).                         (IR)
```

Consequently, for any set `P_img` of projective image lines supporting the
reduced common-image branch,

```text
|Sh_img| <= sum_{I in P_img} binom(n,d_I).           (IRsum)
```

In particular, if `d_I <= B_I` for every uncharged image line in `P_img`, then

```text
|Sh_img| <= |P_img| n^B_I,
```

and the common-image contribution to Corollary 9 is at most

```text
q |P_img| n^B_I.
```

Since `|P_img| <= (q^t-1)/(q-1)`, this branch is polynomial in the
bounded-slack polynomial-field window once the uncharged image-line row-cut
systems all have bounded direction dimension. Thus the remaining obstruction
in the common-image ruled branch is exactly the low-rank image-line locus.

### Proof

The equations defining a fixed image line `I` are affine linear equations on
the monic degree-`m` coefficient slice. Their solution set, if nonempty, is an
affine space `P_0+V_I` with direction dimension `d_I`.

Let `L_S` be a squarefree `D`-split locator in `P_0+V_I`. The evaluation map

```text
V_I -> F^S
```

is injective: a nonzero element of `V_I` has degree `<m`, and hence cannot
vanish at all `m` distinct points of `S`. Therefore some `d_I`-subset
`R subset S` already gives an injective evaluation map `V_I -> F^R`; choose
the first such `R` in a fixed ordering of `D`.

This choice injects `Sh_img(I)` into the `d_I`-subsets of `D`. Indeed, if two
locators in `P_0+V_I` vanish on the same chosen `R`, their difference lies in
`V_I` and vanishes on `R`, so it is zero by injectivity. This proves (IR).
Summing over image lines gives (IRsum), and the displayed polynomial
consequences are immediate.

## Corollary 11: Fixed-Slope And Contained Row-Rank Certificates

Let `m=j-1`. For a finite slope `z in F`, put

```text
P_z = H_{t,j}(u)+zH_{t,j}(v).
```

Consider the affine row-cut system on monic degree-`m` shadow locators

```text
P_z ell_S^0 = 0,        P_z ell_S^+ = 0.             (KR_z)
```

Let `A_z` be its affine solution space, let `V_z` be its direction space, and
put

```text
d_z = dim V_z.
```

Let `Sh_ker(z)` be any set of finite common-kernel ruled shadows assigned to
the slope `z`. Then

```text
|Sh_ker(z)| <= binom(n,d_z).                         (KR)
```

The endpoint contained branch has the same form with

```text
P_infty = H_{t,j}(v),
P_infty ell_S^0 = 0,        P_infty ell_S^+ = 0.
```

If `A_infty` is the corresponding affine solution space with direction
dimension `d_infty`, and `Sh_cont` is the boundary-contained endpoint shadow
ledger, then

```text
|Sh_cont| <= binom(n,d_infty).                       (CR)
```

Consequently, for any set `Z_ker` of finite slopes supporting the reduced
common-kernel branch,

```text
|Sh_ker| <= sum_{z in Z_ker} binom(n,d_z).           (KRsum)
```

Together with Corollary 10, every ruled shadow ledger in Corollary 9 is now a
row-rank ledger:

```text
|Boundary_off^ruled,red|
  <= q ( sum_{z in Z_ker} binom(n,d_z)
         + binom(n,d_infty)
         + sum_{I in P_img} binom(n,d_I) ).          (RR)
```

Thus, in the polynomial-field window, the ruled boundary-off branch is reduced
to controlling the direction dimensions of explicit Hankel row-cut systems for
finite slopes, the endpoint direction, and projective image lines.

### Proof

Corollary 6 puts every finite common-kernel shadow assigned to `z` inside the
solution set of (KR_z), and puts the endpoint contained branch inside the
displayed `P_infty` solution set. These are affine linear systems on the monic
degree-`m` coefficient slice.

The same evaluation-injection argument used in Corollary 10 applies verbatim.
If `P_0+V_z` is nonempty and `L_S in P_0+V_z` is squarefree and `D`-split, then
evaluation `V_z -> F^S` is injective because every nonzero element of `V_z`
has degree `<m`. Choosing the first `d_z`-subset of `S` on which evaluation is
injective gives an injection from `Sh_ker(z)` to the `d_z`-subsets of `D`.
This proves (KR). The endpoint proof gives (CR), summing over finite slopes
gives (KRsum), and substituting these bounds plus Corollary 10 into Corollary
9 gives (RR).

## Corollary 12: Finite-Slope Low-Rank Dichotomy

Keep the finite-slope row-cut matrix from Corollary 11.  Let

```text
R_z : F^m -> F^{2t}
```

be the homogeneous matrix on the lower coefficients of a monic degree-`m`
shadow locator, so that

```text
d_z = dim ker R_z.
```

The entries of `R_z` are affine-linear functions of `z`.  Fix an integer
`b` with `0<=b<m`, and define the low-rank finite-slope locus

```text
Z_{>b} = { z in F : d_z > b }.
```

Then one of the following alternatives holds.

```text
finite-exception alternative:
  |Z_{>b}| <= m-b;

persistent low-rank alternative:
  d_z > b for every z in F.
```

More precisely, if some `(m-b) x (m-b)` minor of `R_z` is not the zero
polynomial in `z`, then the finite-exception alternative holds.  If every
such minor vanishes identically, then the persistent low-rank alternative
holds.

In particular, for `b=0`, either there are at most `m` finite slopes with a
nontrivial shift-pair direction kernel, or every finite slope has one.

### Proof

Since `d_z=dim ker R_z`, the condition `d_z>b` is equivalent to

```text
rank R_z < m-b.
```

This is equivalent to the vanishing at `z` of every `(m-b) x (m-b)` minor of
`R_z`.  Each such minor is a polynomial in `z` of degree at most `m-b`, because
the entries of `R_z` are affine-linear in `z`.

If at least one of these minors is a nonzero polynomial, then every
`z in Z_{>b}` is a root of that polynomial, so `|Z_{>b}| <= m-b`.  If all of
the minors vanish identically, then `rank R_z < m-b` for every `z`, hence
`d_z>b` for every `z`.

## Corollary 13: Bounded-Rank Finite-Slope Closure After Exceptional Charges

Fix `b<m`, and suppose the finite-exception alternative of Corollary 12 holds:

```text
Z_{>b} = { z in F : d_z > b },        |Z_{>b}| <= m-b.
```

Split the finite common-kernel shadow ledger as

```text
Sh_ker = Sh_ker^{<=b} union Sh_ker^{>b},
```

where `Sh_ker^{<=b}` contains the shadows assigned to slopes with `d_z<=b`,
and `Sh_ker^{>b}` contains the shadows assigned to the exceptional slopes
`Z_{>b}`. Then

```text
|Sh_ker^{<=b}| <= q binom(n,b).                     (BK)
```

Consequently, the bounded-rank finite common-kernel targets contribute at most

```text
q^2 binom(n,b)                                      (BKT)
```

to the reduced boundary-off target count.

In particular, if `q<=n^B_F` and `b` is bounded independently of `n`, then the
bounded-rank finite common-kernel residual is polynomial:

```text
|Boundary_off,ker^{<=b}| <= n^(2B_F+b).
```

Thus, away from the persistent low-rank alternative, the only finite-slope
common-kernel shadows not closed by a bounded-rank estimate are the at most
`m-b` exceptional fixed slopes. These are precisely the pieces that must be
charged to the fixed-slope/root-slice ledger rather than left inside the
aperiodic boundary-off residual.

### Proof

For each finite slope with `d_z<=b`, Corollary 11 gives

```text
|Sh_ker(z)| <= binom(n,d_z) <= binom(n,b).
```

There are at most `q` finite slopes, proving (BK).  Corollary 9 then allows at
most `q` external anchors over each shadow, giving (BKT).  The displayed
polynomial bound follows from `q<=n^B_F` and `binom(n,b)<=n^b`.

The remaining finite slopes have `d_z>b`, hence lie in `Z_{>b}`; by the
finite-exception alternative there are at most `m-b` of them.  No smallness
claim is made for their split-shadow count here.  The conclusion is only that
they have been isolated as a finite fixed-slope charge.

## Corollary 14: Persistent Low-Rank Has Polynomial Kernel Certificates

Keep the notation of Corollary 12, and let `K=F(z)`.  Suppose the finite-slope
row-cut pencil is identically persistent at threshold `b`, meaning that every
`(m-b) x (m-b)` minor of `R_z` vanishes as a polynomial in `F[z]`.  Then

```text
dim_K ker(R_z:K^m -> K^{2t}) >= b+1.
```

Equivalently, there exist `b+1` vectors

```text
Q_0(z),...,Q_b(z) in F[z]^m
```

that are linearly independent over `K` and satisfy

```text
R_z Q_i(z)=0        for 0<=i<=b.                    (PK)
```

Writing

```text
Q_i(z,X)=sum_{a=0}^{m-1} Q_{i,a}(z) X^a,
```

the certificate equations are exactly

```text
(H_{t,j}(u)+zH_{t,j}(v)) ell_{Q_i(z)}^0 = 0,
(H_{t,j}(u)+zH_{t,j}(v)) ell_{Q_i(z)}^+ = 0         (MK)
```

as identities in `F[z]^t`.  Conversely, the existence of `b+1`
`K`-independent polynomial vectors satisfying (PK) forces every
`(m-b) x (m-b)` minor of `R_z` to vanish identically.

Thus the persistent finite-slope obstruction is equivalent to a finite
polynomial-kernel certificate: a moving degree-`<m` polynomial direction, or
`b+1` independent such directions at threshold `b`, whose lower and upper
Hankel shifts are killed by the whole pencil.

### Proof

Over the rational function field `K=F(z)`, the vanishing of every
`(m-b) x (m-b)` minor is equivalent to

```text
rank_K R_z < m-b.
```

Since the domain has dimension `m`, this is equivalent to

```text
dim_K ker R_z >= b+1.
```

Choose `b+1` independent kernel vectors over `K`.  Multiplying each by a
nonzero common denominator turns it into a vector in `F[z]^m` without changing
`K`-linear independence, proving (PK).

The rows of `R_z` are precisely the homogeneous lower-coefficient equations
for the two shifted conditions

```text
P_z ell_Q^0=0,        P_z ell_Q^+=0,
```

with `P_z=H_{t,j}(u)+zH_{t,j}(v)`.  Substituting the polynomial coefficient
vector `Q_i(z)` gives (MK).

Conversely, if `b+1` `K`-independent vectors satisfy (PK), then
`dim_K ker R_z>=b+1`, so `rank_K R_z<m-b`.  Hence all `(m-b) x (m-b)` minors
are zero in `K`, and therefore vanish as polynomials in `F[z]`.

## Corollary 15: Persistent Finite-Slope Low Rank Forces Endpoint Low Rank

Write

```text
R_z = R_u + z R_v,
```

where `R_u` is the homogeneous row-cut matrix for the shifted pair

```text
H_{t,j}(u) ell_Q^0 = 0,        H_{t,j}(u) ell_Q^+ = 0,
```

and `R_v` is the endpoint matrix for

```text
H_{t,j}(v) ell_Q^0 = 0,        H_{t,j}(v) ell_Q^+ = 0.
```

Let

```text
d_0 = dim ker R_u,        d_infty = dim ker R_v.
```

If the finite-slope row-cut pencil is identically persistent at threshold
`b`, then

```text
d_0 > b,        d_infty > b.                         (EP)
```

Equivalently, if either endpoint row-cut system has direction dimension at
most `b`, then the persistent low-rank alternative in Corollary 12 is
impossible.  In that case the finite-exception alternative holds, so the
bounded-rank closure of Corollary 13 applies after charging the at most
`m-b` exceptional fixed slopes.

At the level of the polynomial-kernel certificate, every nonzero moving kernel

```text
Q(z)=q_0+q_1z+...+q_Dz^D
```

can be divided by a power of `z` so that `q_0 != 0`, and then its coefficients
satisfy the endpoint ladder

```text
R_u q_0 = 0,
R_u q_i + R_v q_{i-1} = 0        for 1<=i<=D,
R_v q_D = 0.                                         (EL)
```

Thus a persistent moving kernel necessarily starts in the `u`-endpoint kernel
and ends in the `v`-endpoint kernel.

### Proof

Put `r=m-b`.  Persistent low rank at threshold `b` says that every `r x r`
minor of the affine pencil `R_u+zR_v` vanishes identically as a polynomial in
`z`.  The constant coefficient of such a minor is the corresponding `r x r`
minor of `R_u`, while the coefficient of `z^r` is the corresponding
`r x r` minor of `R_v`.  Hence every `r x r` minor of both endpoint matrices
vanishes, so

```text
rank R_u < r,        rank R_v < r.
```

Since the domain dimension is `m`, this is exactly `d_0>b` and `d_infty>b`.
The contrapositive and the appeal to Corollary 13 are immediate.

For the ladder, substitute `Q(z)=sum_i q_i z^i` into

```text
(R_u+zR_v)Q(z)=0
```

and compare coefficients of powers of `z`.  If the first nonzero coefficient
of `Q` occurs at degree `s>0`, divide by `z^s` in the polynomial ring before
applying the comparison.  This gives (EL).

## Corollary 16: Common-Image Low-Rank Is A Projective Determinantal Locus

Let `m=j-1`.  For a nonzero vector `y in F^t`, let `I=[y]` be the projective
image line it spans.  Define the homogeneous common-image matrix

```text
C_y : F^m -> (wedge^2 F^t)^4
```

by

```text
Q |-> ( y wedge H_{t,j}(u) ell_Q^0,
        y wedge H_{t,j}(u) ell_Q^+,
        y wedge H_{t,j}(v) ell_Q^0,
        y wedge H_{t,j}(v) ell_Q^+ ).
```

Then

```text
ker C_y = V_I,        d_I = dim ker C_y.             (CI)
```

In particular, for `0<=b<m`, the low-rank image-line locus

```text
P_img,>b = { [y] in P^{t-1}(F) : d_[y] > b }
```

is cut out by the `(m-b) x (m-b)` minors of any matrix for `C_y`.  These
minors are homogeneous polynomials of degree `m-b` in the coordinates of `y`.

If at least one such minor is not the zero polynomial, then

```text
|P_img,>b| <= ((m-b) q^(t-1))/(q-1).                (PI)
```

If every such minor vanishes identically, then over
`K=F(y_0,...,y_{t-1})` there are `b+1` independent moving-image directions

```text
Q_0(y),...,Q_b(y) in K^m
```

such that, after clearing denominators,

```text
y wedge H_{t,j}(u) ell_{Q_i(y)}^0 = 0,
y wedge H_{t,j}(u) ell_{Q_i(y)}^+ = 0,
y wedge H_{t,j}(v) ell_{Q_i(y)}^0 = 0,
y wedge H_{t,j}(v) ell_{Q_i(y)}^+ = 0              (PIC)
```

as polynomial identities.  Conversely, `b+1` independent moving-image
directions satisfying these identities force all `(m-b) x (m-b)` minors of
`C_y` to vanish identically.

Consequently, after charging the projective low-rank image-line locus
`P_img,>b`, the bounded-rank common-image shadow ledger satisfies

```text
|Sh_img^{<=b}| <= ((q^t-1)/(q-1)) binom(n,b),
```

and its boundary-off target contribution is at most

```text
q ((q^t-1)/(q-1)) binom(n,b).                       (CIB)
```

For bounded slack `t`, bounded `b`, and polynomial field size `q<=n^B_F`, this
bounded-rank common-image residual is polynomial.  The only remaining
common-image obstruction is the explicitly determinantal projective low-rank
locus, or the identically persistent moving-image certificate (PIC).

### Proof

A vector `Q` lies in the direction space for the image line `I=[y]` exactly
when each of the four Hankel images

```text
H(u)ell_Q^0, H(u)ell_Q^+, H(v)ell_Q^0, H(v)ell_Q^+
```

lies in `I`.  This is equivalent to the vanishing of its wedge with `y`, which
proves (CI).  Scaling `y` scales every row of `C_y` uniformly and does not
change the kernel, so the condition is projective.

The entries of `C_y` are homogeneous linear forms in the coordinates of `y`.
The condition `d_[y]>b` is equivalent to

```text
rank C_y < m-b,
```

and hence to the vanishing of all `(m-b) x (m-b)` minors.  Those minors are
homogeneous of degree `m-b`.

If one of these minors is a nonzero homogeneous polynomial `P(y)` of degree
`m-b`, the affine Schwartz-Zippel bound gives at most `(m-b)q^(t-1)` zeros in
`F^t`.  Dividing nonzero zeros into projective lines gives (PI).

If all minors vanish identically, then over the rational function field
`K=F(y_0,...,y_{t-1})` the rank of `C_y` is `<m-b`, so the kernel dimension is
at least `b+1`.  Choose `b+1` independent kernel vectors over `K` and clear
denominators to obtain polynomial vectors satisfying (PIC).  The converse is
the same rank-nullity argument over `K`.

Finally, for all image lines outside `P_img,>b`, Corollary 10 gives at most
`binom(n,b)` split shadows per line.  There are `(q^t-1)/(q-1)` projective
image lines in `F^t`; multiplying and then using the external-anchor factor
`q` from Corollary 9 proves (CIB).

## Corollary 17: Ruled Boundary-Off Closure After Low-Rank Charges

Fix `0<=b<m`.  Work in the reduced boundary-off target set after the
fixed-root/full-star charges from Corollary 9.  Suppose the following
exceptional pieces are charged to their own ledgers:

```text
E_slope = finite common-kernel slopes with d_z>b,
E_img   = projective common-image lines with d_I>b.
```

Assume also that the endpoint-contained row-cut system has

```text
d_infty <= b.
```

Then the uncharged ruled boundary-off targets satisfy

```text
|Boundary_off^{ruled,red,<=b}|
 <= q^2 binom(n,b)
    + q binom(n,b)
    + q ((q^t-1)/(q-1)) binom(n,b).                 (RBC)
```

Equivalently,

```text
|Boundary_off^{ruled,red,<=b}|
 <= ( q^2 + q + q ((q^t-1)/(q-1)) ) binom(n,b).
```

In particular, for bounded slack `t`, bounded rank threshold `b`, and
polynomial field size `q<=n^B_F`, the uncharged bounded-rank ruled branch is
polynomially bounded.

If the finite-slope persistent alternative is absent, Corollary 12 gives

```text
|E_slope| <= m-b.
```

If it is present, Corollaries 14 and 15 replace it by the explicit moving
kernel/endpoint-low-rank certificate.  If the common-image projective
persistent alternative is absent, Corollary 16 gives the hypersurface bound

```text
|E_img| <= ((m-b) q^(t-1))/(q-1).
```

Thus the ruled boundary-off branch has been reduced to:

```text
bounded-rank polynomial residual
+ exceptional fixed-slope charges
+ exceptional projective image-line charges
+ explicit persistent moving-kernel certificates.
```

### Proof

The finite common-kernel slopes outside `E_slope` have `d_z<=b`.  Corollary 13
gives their boundary-off target contribution at most

```text
q^2 binom(n,b).
```

The endpoint-contained branch has `d_infty<=b` by hypothesis.  Corollary 11
gives at most `binom(n,b)` endpoint shadows, and Corollary 9 contributes at
most `q` anchors over each shadow, giving

```text
q binom(n,b).
```

The common-image lines outside `E_img` have `d_I<=b`.  Corollary 16 gives their
target contribution at most

```text
q ((q^t-1)/(q-1)) binom(n,b).
```

Adding the three ruled contributions proves (RBC).  The final claims are just
the exceptional-locus alternatives already proved in Corollaries 12, 14, 15,
and 16.

## Corollary 17.1: Root-Free Row-Rank Ledgers Gain A Slice Factor

Let `m=j-1`, and let

```text
A = P_0 + V
```

be an affine solution space of monic degree-`m` shadow locators inside any one
of the row-rank ledgers from Corollaries 10 and 11.  Put `d=dim V`, and let
`Sh(A)` be a set of squarefree `D`-split shadow locators assigned to this
stratum.

For `alpha in D`, write

```text
ev_alpha : V -> F,        Q |-> Q(alpha).
```

Assume `d>=1` and that the common-root part of the stratum has already been
charged to the fixed-root/root-slice ledger, in the following precise sense:
whenever some assigned locator in `Sh(A)` vanishes at `alpha`, the functional
`ev_alpha` is nonzero on `V`.  Then

```text
|Sh(A)| <= (n/m) binom(n-1,d-1)
        = (d/m) binom(n,d).                         (RF)
```

If `d=0`, the previous row-rank bound gives the conservative estimate

```text
|Sh(A)| <= 1.
```

Consequently the ruled row-rank target ledger from Corollary 11 can be
sharpened, after common-root charges, to

```text
|Boundary_off^{ruled,red,rootfree}|
 <= q ( sum_{z in Z_ker} Phi_m(d_z)
        + Phi_m(d_infty)
        + sum_{I in P_img} Phi_m(d_I) ),             (RFR)
```

where

```text
Phi_m(0)=1,        Phi_m(d)=(d/m) binom(n,d) for d>=1.
```

In particular, in the bounded-rank range `d_z,d_infty,d_I<=b` with
`1<=b<=n/2`, the uncharged root-free ruled residual satisfies

```text
|Boundary_off^{ruled,red,rootfree,<=b}|
 <= ( q^2 + q + q ((q^t-1)/(q-1)) )
    (b/m) binom(n,b).                                (RFR_b)
```

Thus the bounded-rank ruled branch carries a genuine root-slice saving after
the common-root pieces have been removed.  For `b<m`, this is sharper than the
bare `binom(n,b)` row-rank estimate used in Corollary 17.

### Proof

For a fixed `alpha in D`, let `Sh_alpha(A)` be the assigned split locators in
`Sh(A)` that vanish at `alpha`.  If this set is empty, there is nothing to
count.  Otherwise the hypothesis says that `ev_alpha` is nonzero on `V`, so
the locators in `A` that vanish at `alpha` form an affine subspace whose
direction space is

```text
W_alpha = ker(ev_alpha:V->F),
```

with `dim W_alpha=d-1`.

Fix `L_S in Sh_alpha(A)`.  Since every `Q in W_alpha` has degree `<m` and
vanishes at `alpha`, the evaluation map

```text
W_alpha -> F^{S\{alpha}}
```

is injective: a nonzero `Q` cannot vanish on `alpha` and on all `m-1` other
roots of `S`.  Therefore some `(d-1)`-subset `R subset S\{alpha}` gives an
injective evaluation map on `W_alpha`; choose the first such `R` in a fixed
ordering of `D`.

This choice injects `Sh_alpha(A)` into the `(d-1)`-subsets of `D\{alpha}`.
Indeed, if two locators in the same affine slice vanish on `alpha` and on the
same chosen `R`, their difference lies in `W_alpha` and vanishes on `R`, so it
is zero.  Hence

```text
|Sh_alpha(A)| <= binom(n-1,d-1).
```

Counting incidences `(alpha,S)` with `alpha in S` gives

```text
m |Sh(A)| = sum_{alpha in D} |Sh_alpha(A)|
          <= n binom(n-1,d-1),
```

which proves (RF).  The case `d=0` is the old row-rank injection bound
`binom(n,0)=1`.

Apply (RF) separately to every finite-slope, endpoint, and projective
image-line row-rank stratum in Corollary 11.  The extra factor `q` in (RFR) is
the external-anchor multiplicity from Corollary 9.  Finally, if
`1<=d<=b<=n/2`, then

```text
Phi_m(d)=(d/m)binom(n,d) <= (b/m)binom(n,b),
```

because `d binom(n,d)` is increasing for `d<=n/2`.  Substituting this bound
into (RFR), and using at most `q` finite slopes and `(q^t-1)/(q-1)`
projective image lines, proves (RFR_b).

## Corollary 18: Popular Nondegenerate Shadows Are Low-Exchange Ledgers

Let `A` be any family of `j`-subsets of `D`.  Define the boundary-shadow
degree

```text
deg_A(S)=#{ T in A : |S cap T|=j-2 },
        |S|=j-1.
```

For `h>=1`, let

```text
E_h(A)=#{ {T,T'} subset A : T != T' and |T\T'|=|T'\T|=h }
```

be the unordered exchange profile of `A`.  Then

```text
sum_{|S|=j-1} binom(deg_A(S),2)
 <= N_1 E_1(A) + N_2 E_2(A) + N_3 E_3(A),          (PS)
```

where, with the convention that invalid binomial coefficients are zero,

```text
N_1 = (j-1) binom(n-j-1,1) + binom(j-1,2),
N_2 = binom(n-j-2,1) + 4(j-2),
N_3 = 9.
```

No exchange level `h>=4` can share such a boundary shadow.

Now take `A=A_var`, the active all-domain family from Corollary 4, and let
`Iso_quad` be the nondegenerate quadratic-anchor shadows with `deg_A(S)=1`.
Then

```text
|Boundary_off^quad|
 <= 2 |Iso_quad|
    + 2 ( N_1 E_1(A_var) + N_2 E_2(A_var) + N_3 E_3(A_var) ).      (NQ)
```

Thus the nondegenerate quadratic-anchor branch is reduced to a unique-neighbor
shadow ledger plus the first three active exchange profiles.  In the M1
variable-line program, those exchange profiles are the same kind of
low-exchange active-codegree objects already isolated by the packet lemma.

### Proof

Fix distinct `T,T' in A` and put

```text
h=|T\T'|=|T'\T|,        I=T cap T',
A_0=T\T',               B_0=T'\T,
O=D\(T union T').
```

Then `|I|=j-h`, `|A_0|=|B_0|=h`, and `|O|=n-j-h`.  Count the `(j-1)`-sets `S`
with

```text
|S cap T|=|S cap T'|=j-2.
```

Write

```text
x=|S cap I|,        a=|S cap A_0|,
b=|S cap B_0|,      o=|S cap O|.
```

The two intersection equations give

```text
x+a=j-2,        x+b=j-2,
```

so `a=b=r`.  Since `|S|=j-1`,

```text
j-1 = x+a+b+o = j-2+r+o,
```

and hence `r+o=1`.  There are only two cases.

If `r=0` and `o=1`, then `x=j-2`; this contributes

```text
binom(j-h,j-2)(n-j-h)
```

common boundary shadows.  This term is nonzero only for `h<=2`.

If `r=1` and `o=0`, then `x=j-3`; this contributes

```text
binom(j-h,j-3) h^2
```

common boundary shadows.  This term is nonzero only for `h<=3`.

Therefore a pair at exchange level `h` has at most

```text
N_h = binom(j-h,j-2)(n-j-h) + binom(j-h,j-3) h^2
```

common boundary shadows, and `N_h=0` for `h>=4`.  Substituting `h=1,2,3` gives
the displayed values of `N_1,N_2,N_3`.  Summing over unordered active pairs
proves (PS).

A nondegenerate boundary target has at most two external anchors over its
shadow by Corollary 2.  Split its shadow according to whether `deg_A(S)=1` or
`deg_A(S)>=2`.  The first class contributes at most `2|Iso_quad|`.  The second
has cardinality at most

```text
sum_S binom(deg_A(S),2),
```

and (PS) gives the claimed exchange-ledger bound.

## Corollary 19: Unique-Neighbor Shadows Are Not Controlled By Low Exchange

Let `A` be a family of `j`-subsets of `D` with

```text
E_1(A)=E_2(A)=E_3(A)=0.
```

Equivalently, every two distinct members of `A` have exchange distance at
least `4`.  Then every first boundary shadow of `A` is unique:

```text
deg_A(S) <= 1        for every |S|=j-1.
```

Consequently the first boundary-shadow image has the exact size

```text
|Shadow_1(A)|
  = |A| binom(j,2)(n-j),                             (US)
```

where

```text
Shadow_1(A)
  = { S subset D :
      |S|=j-1 and there exists T in A with |S cap T|=j-2 }.
```

Thus the unique-neighbor shadow ledger in Corollary 18 is genuinely necessary:
it cannot be bounded using only the first three exchange profiles.  Any closure
of the nondegenerate boundary branch must use additional structure, such as
the Hankel anchor equations, quotient/aperiodic restrictions, or a separate
bound on the number of isolated active locators.

### Proof

If a shadow `S` had two distinct active neighbors `T,T' in A`, then
Corollary 18's pair count shows that `T` and `T'` must have exchange distance
at most `3`.  This contradicts the assumption `E_1=E_2=E_3=0`.  Hence every
shadow has degree at most one.

For each fixed `T in A`, a first boundary shadow adjacent to `T` is obtained by
deleting two points of `T` and adding one point of `D\T`.  This gives exactly

```text
binom(j,2)(n-j)
```

shadows over `T`.  Since no shadow is shared by two members of `A`, summing
over `T` proves (US).

## Lemma 19.1: Quadratic Cofactor Interpolation

Let `E` be a set of at least `r+2` distinct field elements.  Let `G` be a
polynomial of degree at most two on the affine space of monic degree-`r`
locators

```text
Q(X)=X^r+q_{r-1}X^{r-1}+...+q_0.
```

If

```text
G(Q_U)=0        for every U subset E with |U|=r,
```

where

```text
Q_U(X)=prod_{x in U}(X-x),
```

then `G` is identically zero.

Equivalently, for any fixed `(r+2)`-set

```text
E_0={e_1,...,e_{r+2}},
```

the `binom(r+2,2)` cofactors

```text
Q_{ab}(X)=prod_{x in E_0\{e_a,e_b}}(X-x),
        1<=a<b<=r+2,
```

are unisolvent for quadratic polynomials on the monic degree-`r` coefficient
slice.

### Proof

It is enough to prove the second statement, since any `E` of size at least
`r+2` contains such an `E_0`.  The vector space of degree-`<=2` polynomials in
the `r` lower coefficients has dimension

```text
1+r+binom(r+1,2)=binom(r+2,2),
```

the same as the number of cofactors.

Use the standard monomial basis

```text
1, q_i, q_i q_j        (0<=i<=j<r)
```

and form the square evaluation matrix on the cofactors `Q_{ab}`.  The
quadratic cofactor Vandermonde determinant is

```text
det M(E_0) = +/- prod_{1<=a<b<=r+2} (e_a-e_b)^r.     (CV)
```

Indeed, writing the coefficients of `Q_{ab}` as the elementary symmetric
functions of `E_0\{e_a,e_b}` turns `M(E_0)` into the usual second symmetric
power of the cofactor/Vandermonde evaluation matrix; elementary column
operations give (CV).  Since the elements of `E_0` are distinct, the
determinant is nonzero.  Hence evaluation on these cofactors is an isomorphism
on quadratic polynomials, proving the lemma.

## Corollary 20: Full Anchor Stars Are Fixed-Root Factors

Let `m=j-1`, fix an external anchor `beta in F\D`, and fix a row pair
`rho=(alpha_0,gamma_0)` with `0<=alpha_0<gamma_0<t`.  For a monic degree-`m`
locator `L`, put

```text
ell_{L,beta} = coeffs of (X-beta)L(X),
```

and let

```text
P_{rho,beta}(L)
```

be the corresponding row-pair minor of

```text
[ H_{t,j}(u) ell_{L,beta}   H_{t,j}(v) ell_{L,beta} ].
```

Thus `P_{rho,beta}` is a polynomial of degree at most two on the affine space
of monic degree-`m` locators.

Fix `alpha in D`, and assume

```text
|D\{alpha}| >= m+1.                                  (FS0)
```

If

```text
P_{rho,beta}(L_S)=0
    for every S subset D with |S|=m and alpha in S,  (FS1)
```

then `P_{rho,beta}` vanishes on the whole affine hyperplane

```text
L(alpha)=0.
```

Equivalently, as a polynomial on the monic degree-`m` coefficient slice,
`P_{rho,beta}` is divisible by the evaluation functional

```text
Ev_alpha(L)=L(alpha).
```

Consequently, if all external-anchor minors for a fixed `beta` vanish on the
full shadow star through `alpha`, then that full-star part of the anchor gate
is a fixed-root algebraic slice.  After fixed-root/root-slice charges have
been removed, no uncharged anchor-minor zero set may contain a full domain
root star.

### Proof

The entries of each Hankel column are linear in the coefficients of
`ell_{L,beta}`, and `ell_{L,beta}` is affine-linear in the lower coefficients
of the monic locator `L`.  Hence every row-pair minor
`P_{rho,beta}` has degree at most two in the coefficient coordinates of `L`.

Write

```text
L(X)=(X-alpha)Q(X),
```

where `Q` is monic of degree `r=m-1`, and define

```text
G(Q)=P_{rho,beta}((X-alpha)Q).
```

This is a degree-`<=2` polynomial on the monic degree-`r` coefficient slice.
The assumption (FS1) says that `G(Q_U)=0` for every

```text
Q_U(X)=prod_{x in U}(X-x),        U subset D\{alpha}, |U|=r.
```

Since `|D\{alpha}|>=r+2`, Lemma 19.1 forces `G` to be identically zero.
Therefore `P_{rho,beta}` vanishes on every monic degree-`m` locator divisible
by `X-alpha`, which is exactly the hyperplane `L(alpha)=0`.

A polynomial on an affine space that vanishes on the hyperplane cut out by the
linear functional `Ev_alpha` belongs to the principal ideal generated by
`Ev_alpha`.  This proves the divisibility assertion.  Applying the same
argument to every row-pair minor gives the fixed-root statement for the full
anchor gate.

## Corollary 21: Repeated Full Anchor Stars Force Exact Root Factors

Keep the notation and size hypothesis of Corollary 20.  Let
`P=P_{rho,beta}` be one fixed row-pair anchor minor, and suppose that `P`
vanishes on the full shadow stars through distinct roots

```text
alpha_1,...,alpha_s in D.
```

Then `P` is divisible by

```text
Ev_{alpha_1}(L) ... Ev_{alpha_s}(L).
```

Consequently:

```text
s=1:
  P has the fixed-root factor L(alpha_1);

s=2:
  P is either zero or has the exact form
  c L(alpha_1)L(alpha_2);

s>=3:
  P is identically zero.
```

Thus a nonzero nondegenerate anchor minor can carry at most two full domain
root stars.  Any third full star forces that minor into the identically
vanishing side of the anchor-minor ledger.

### Proof

Corollary 20 gives divisibility by `Ev_{alpha_i}` for every full star
`alpha_i`.  These evaluation functionals are pairwise nonproportional on the
monic degree-`m` coefficient slice whenever the roots are distinct: for
example, a monic locator can vanish at one of the two roots but not the other.
Hence the linear factors `Ev_{alpha_i}` are pairwise coprime in the affine
coordinate ring.  Their product divides `P`.

Since `P` has degree at most two, the displayed alternatives follow
immediately.  For `s=2`, the quotient has degree at most zero, so it is a
constant.  For `s>=3`, a nonzero product of three distinct linear factors
cannot divide a degree-`<=2` polynomial, so `P=0`.

## Corollary 22: Core-Line Free Anchor Zeros Have One More Slice Saving

Keep `m=j-1`, fix an external anchor `beta`, and fix one row-pair anchor minor

```text
P=P_{rho,beta}
```

as in Corollary 20.  For an `(m-1)`-set `R subset D`, define the core-line
restriction

```text
p_R(Y)=P(L_{R,Y}),        L_{R,Y}(X)=(X-Y)L_R(X),
```

more explicitly,

```text
p_R(x)=P(L_{R union {x}})        for x in D\R.
```

Here `p_R` is a polynomial in the added root `x` of degree at most two.  Let

```text
Core(P)={ R subset D : |R|=m-1 and p_R is identically zero }.
```

After the full core-lines `R in Core(P)` have been charged to their own
ledger, the remaining `D`-split zeros of `P` satisfy

```text
|{ S subset D : |S|=m, P(L_S)=0,
                 no (m-1)-subset of S lies in Core(P) }|
 <= (2/m) binom(n,m-1).                              (CL)
```

Thus a fixed nonzero anchor minor has only a one-root-loss zero set after both
fixed-root full stars and identically vanishing core-lines have been removed.
The residual obstruction is no longer a full `m`-shadow family for that minor;
it is the explicitly named core-line degeneracy plus the bounded two-roots-per
core remainder.

### Proof

For fixed `R`, the locator

```text
L_{R union {x}}(X)=(X-x)L_R(X)
```

depends affine-linearly on `x` in coefficient coordinates.  Since `P` has
degree at most two in those coordinates, `p_R(x)` has degree at most two.

If `R notin Core(P)`, then `p_R` is a nonzero degree-`<=2` polynomial, so it
has at most two roots in `D\R`.  Count incidences

```text
(R,S) with R subset S, |R|=m-1, |S|=m, P(L_S)=0,
```

among zeros `S` with no core in `Core(P)`.  Each such `S` has exactly `m`
cores `R=S\{x}`, and every one of them is outside `Core(P)`.  Each
nondegenerate core contributes at most two extensions.  Therefore

```text
m |Z_rem| <= 2 binom(n,m-1),
```

which proves (CL).

## Corollary 23: Core-Line Degeneracy Has A Lower Anchor-Coefficient Ledger

Keep the notation of Corollary 22.  For a fixed `(m-1)`-core `R`, write

```text
L_R(X)=prod_{alpha in R}(X-alpha).
```

The one-root extension with external anchor `beta` is

```text
(X-beta)(X-Y)L_R(X)
 = (X-beta)X L_R(X) - Y (X-beta)L_R(X).
```

Let

```text
A = H(u) coeffs((X-beta)X L_R),
B = H(u) coeffs((X-beta)L_R),
C = H(v) coeffs((X-beta)X L_R),
D = H(v) coeffs((X-beta)L_R),
```

with the usual zero padding into the boundary locator window.  Then every
row-pair restriction from Corollary 22 has the explicit quadratic form

```text
p_R(Y)
 = W(A,C) - Y( W(B,C)+W(A,D) ) + Y^2 W(B,D).          (CoreCoeff)
```

Consequently

```text
R in Core(P_{rho,beta})
```

if and only if the three lower-dimensional Hankel-wedge coefficients

```text
W(A,C),      W(B,C)+W(A,D),      W(B,D)
```

vanish for that row pair.  Thus the full core-line obstruction left by
Corollary 22 is not an unstructured zero-set condition: it is exactly a
three-coefficient anchor ledger on the `(m-1)`-core locator `L_R`.

### Proof

The displayed identity for `(X-beta)(X-Y)L_R` says that the boundary locator
along the core-line is `M_1 - Y M_0`, where

```text
M_1=(X-beta)X L_R,       M_0=(X-beta)L_R.
```

Applying the two Hankel maps gives `A-YB` and `C-YD`.  Expanding the row-pair
wedge bilinearly gives

```text
W(A-YB,C-YD)
 = W(A,C) - Y( W(B,C)+W(A,D) ) + Y^2 W(B,D),
```

which is `(CoreCoeff)`.  Since `p_R` has degree at most two in `Y`, it is
identically zero exactly when the three displayed coefficients vanish.

## Corollary 24: Full Core-Lines Are Lower Ruled Pencils

Fix an `(m-1)`-core `R` and an external anchor `beta`.  Put

```text
M_1=(X-beta)X L_R,        M_0=(X-beta)L_R,
A=H(u)M_1,               B=H(u)M_0,
C=H(v)M_1,               D=H(v)M_0.
```

Suppose the whole external-anchor gate vanishes identically on the core-line,
meaning

```text
rank [ A-YB   C-YD ] <= 1
```

as a polynomial identity in `Y`, or equivalently

```text
(A-YB) wedge (C-YD) = 0 in Lambda^2(F^t)[Y].       (FullCore)
```

Then at least one of the following lower ruled alternatives holds.

```text
u-endpoint:
  A=B=0.

v-endpoint:
  C=D=0.

common image:
  span{A,B,C,D} has dimension <= 1.

fixed projective kernel:
  span{A,B} has dimension 2 and there is lambda in F with
  C=lambda A and D=lambda B.
```

In the last case the same projective column-kernel line kills both lower
anchor shifts `M_1` and `M_0`:

```text
(-lambda) H(u)M_i + H(v)M_i = 0,      i=0,1,
```

with the evident endpoint interpretation when `lambda=0`.  Thus a full
core-line gate is already a lower-dimensional ruled pencil: it is an endpoint
containment, a fixed image line, or a fixed projective slope for the two
core-shift locators.

### Proof

Let `U=span{A,B}`.

If `dim U=0`, then `A=B=0`, giving the `u`-endpoint alternative.

If `dim U=1`, write `A=a_1 e` and `B=a_0 e` with `e!=0`.  Then

```text
A-YB=(a_1-Ya_0)e.
```

Since the scalar polynomial `a_1-Ya_0` is nonzero, (FullCore) and the fact
that `F[Y]` is a domain imply

```text
e wedge (C-YD)=0.
```

Hence `C,D in F e`, so the common-image alternative holds.

It remains to handle `dim U=2`.  Expanding (FullCore) coefficient by
coefficient gives

```text
A wedge C = 0,
A wedge D + B wedge C = 0,
B wedge D = 0.
```

Since `A` and `B` are independent, the first and third equations force
`C in F A` and `D in F B`.  Write

```text
C=aA,        D=dB.
```

The middle equation then becomes

```text
(d-a) A wedge B = 0,
```

so `d=a`.  Therefore `C=aA` and `D=aB`, which is the fixed projective-kernel
alternative with `lambda=a`.  These cases exhaust the possibilities.

## Corollary 25: Full-Gate Core-Line Reduction

Fix an external anchor `beta`.  For an `(m-1)`-core `R`, let

```text
M_R(Y) = [ A-YB   C-YD ]
```

be the lower core-line matrix from Corollary 24.  Define the full-gate
core-line ledger

```text
FullCoreGate(beta)
 = { R subset D : |R|=m-1 and rank M_R(Y)<=1 identically in Y }.
```

Then the actual rank-one anchor gate has the core-line bound

```text
|{ S subset D : |S|=m, rank M_S(beta)<=1,
                 no (m-1)-subset of S lies in FullCoreGate(beta) }|
 <= (2/m) binom(n,m-1).                              (FGCL)
```

Thus, for each fixed external anchor, the star-free boundary-off gate splits
into

```text
full core-line gates, classified by Corollary 24,
+ a one-root-loss residual of size at most (2/m) binom(n,m-1).
```

In particular, the common zero set of all row-pair minors has no larger
core-line residual than a single nonzero quadratic minor: if a core-line is
not identically rank one, one of its minors cuts the line to at most two
extensions.

### Proof

Fix `R notin FullCoreGate(beta)`.  Then not all `2 x 2` minors of `M_R(Y)`
vanish identically as polynomials in `Y`.  Choose one nonzero minor
`p_R(Y)`.  By Corollary 23, it has degree at most two.  Every extension
`S=R union {x}` satisfying the full rank-one gate is a zero of this particular
nonzero quadratic, hence there are at most two such `x in D\R`.

Now count incidences

```text
(R,S) with R subset S, |R|=m-1, |S|=m,
rank M_S(beta)<=1,
```

among the displayed shadows `S` having no core in `FullCoreGate(beta)`.  Each
such `S` has exactly `m` cores, all outside `FullCoreGate(beta)`, and each
core has at most two rank-one extensions.  Therefore

```text
m |Z_rem(beta)| <= 2 binom(n,m-1),
```

which proves (FGCL).

## Corollary 26: Full Core-Line Ledgers Have Row-Rank Certificates

Keep the fixed external anchor `beta`, and put `c=m-1`.  For a monic
degree-`c` core locator `L_R`, write

```text
M_0=(X-beta)L_R,        M_1=(X-beta)X L_R.
```

The full core-line alternatives from Corollary 24 are contained in the
following affine row-cut systems on the monic degree-`c` coefficient slice.

```text
u-endpoint:
  H(u)M_0=0,        H(u)M_1=0.

v-endpoint:
  H(v)M_0=0,        H(v)M_1=0.

finite fixed kernel lambda in F:
  (H(v)-lambda H(u))M_0=0,
  (H(v)-lambda H(u))M_1=0.

common image line I=[y] in P(F^t):
  y wedge H(u)M_i=0 and y wedge H(v)M_i=0,     i=0,1.
```

Let the direction dimensions of these affine systems be

```text
e_u(beta),  e_v(beta),  e_lambda(beta),  e_I(beta),
```

omitting an empty system from the count.  If full core-lines are assigned
arbitrarily to one of the alternatives supplied by Corollary 24, then

```text
|FullCoreGate(beta)|
 <= binom(n,e_u(beta)) + binom(n,e_v(beta))
    + sum_{lambda in F} binom(n,e_lambda(beta))
    + sum_{I in P(F^t)} binom(n,e_I(beta)).          (FCRR)
```

In particular, if every uncharged lower system has direction dimension at most
`b`, then

```text
|FullCoreGate(beta)|
 <= ( 2 + q + (q^t-1)/(q-1) ) binom(n,b).            (FCB)
```

The corresponding full-core boundary shadows for this fixed `beta` are bounded
by the extra extension factor

```text
(n-m+1) |FullCoreGate(beta)| <= n |FullCoreGate(beta)|.
```

Thus Corollary 25 plus (FCRR) reduces the fixed-anchor full rank-one gate to a
one-root-loss residual and explicit lower endpoint, projective-image, and
fixed-kernel row-rank ledgers on degree-`m-1` core locators.

### Proof

Corollary 24 puts every full core-line into one of the displayed alternatives:
endpoint containment, common image, or fixed projective kernel.  Each
displayed alternative is an affine linear system in the lower coefficients of
the monic degree-`c` locator `L_R`, because multiplication by `(X-beta)` and
by `X` are linear operations after the leading coefficient of `L_R` is fixed.

Consider one such nonempty affine solution space `P_0+V`, and put
`e=dim V`.  For every squarefree `D`-split core locator `L_R` in this affine
space, the evaluation map

```text
V -> F^R
```

is injective: a nonzero element of `V` is represented by a polynomial of
degree `<c`, and therefore cannot vanish at all `c` distinct roots of `R`.
Choose the first `e`-subset of `R` on which evaluation is injective.  As in
Corollaries 10 and 11, this choice injects the split core locators in
`P_0+V` into the `e`-subsets of `D`, giving at most `binom(n,e)` such cores.

Applying this bound to the two endpoint systems, every finite fixed-kernel
slope `lambda`, and every projective image line `I` proves (FCRR).  The
bounded-dimension estimate (FCB) follows from
`|F|=q` and `|P(F^t)|=(q^t-1)/(q-1)`.  Finally, a fixed `(m-1)`-core has at
most `n-(m-1)=n-m+1` extensions to an `m`-shadow, proving the displayed
shadow bound.

## Corollary 27: Lower Fixed-Kernel Slopes Have The Same Low-Rank Dichotomy

Keep `beta` fixed and put `c=m-1`.  Assume `c>=1`.  For each finite lower
fixed-kernel slope `lambda in F`, let

```text
R_lambda^core(beta): F^c -> F^{2t}
```

be the homogeneous row-cut matrix on the lower coefficients of a monic
degree-`c` core locator `L_R` for the system

```text
(H(v)-lambda H(u))(X-beta)L_R = 0,
(H(v)-lambda H(u))(X-beta)X L_R = 0.                (CoreKer_lambda)
```

Let

```text
e_lambda(beta)=dim ker R_lambda^core(beta).
```

Fix `0<=b<c`, and define

```text
Z_core,>b(beta)={ lambda in F : e_lambda(beta)>b }.
```

Then one of the following alternatives holds.

```text
finite-exception alternative:
  |Z_core,>b(beta)| <= c-b;

persistent lower-kernel alternative:
  e_lambda(beta)>b for every lambda in F.
```

More precisely, if some `(c-b) x (c-b)` minor of `R_lambda^core(beta)` is not
the zero polynomial in `lambda`, then the finite-exception alternative holds.
If every such minor vanishes identically, then the lower fixed-kernel
obstruction is persistent for this `beta`.

Consequently, outside the exceptional slopes `Z_core,>b(beta)`, the fixed-kernel
part of `FullCoreGate(beta)` contributes at most

```text
q binom(n,b)
```

split cores, and at most

```text
q (n-m+1) binom(n,b)
```

boundary shadows for this fixed anchor.  The exceptional slopes are now a
finite fixed-slope charge unless the persistent lower-kernel alternative
occurs.

### Proof

Multiplication by `(X-beta)` and by `X` are fixed linear maps in the lower
coefficients of the monic degree-`c` locator.  Therefore the homogeneous
direction matrix for (CoreKer_lambda) has entries affine-linear in `lambda`.
The condition `e_lambda(beta)>b` is equivalent to

```text
rank R_lambda^core(beta) < c-b,
```

which is equivalent to the vanishing of all `(c-b) x (c-b)` minors.  Each such
minor is a polynomial in `lambda` of degree at most `c-b`.

If one of those minors is nonzero, it has at most `c-b` roots, proving the
finite-exception alternative.  If every such minor is identically zero, then
the rank is `<c-b` for every `lambda`, hence `e_lambda(beta)>b` for every
`lambda`.

For every non-exceptional slope, Corollary 26 gives at most `binom(n,b)` split
cores.  There are at most `q` finite slopes.  Finally, each split core extends
to at most `n-m+1` degree-`m` shadows, giving the displayed shadow bound.

## Corollary 28: Persistent Lower Fixed-Kernel Rank Forces Endpoint Low Rank

Keep the notation of Corollary 27, and write

```text
R_lambda^core(beta)=R_v^core(beta)-lambda R_u^core(beta),
```

where `R_u^core(beta)` and `R_v^core(beta)` are the endpoint row-cut matrices
for

```text
H(u)M_0=H(u)M_1=0,        H(v)M_0=H(v)M_1=0,
```

with `M_0=(X-beta)L_R` and `M_1=(X-beta)X L_R`.  Put

```text
e_u(beta)=dim ker R_u^core(beta),
e_v(beta)=dim ker R_v^core(beta).
```

If the lower fixed-kernel pencil is persistent at threshold `b`, meaning every
`(c-b) x (c-b)` minor of `R_lambda^core(beta)` vanishes identically in
`lambda`, then

```text
e_u(beta)>b,        e_v(beta)>b.                    (LowerEP)
```

Equivalently, if either lower endpoint system has direction dimension at most
`b`, the persistent lower-kernel alternative in Corollary 27 is impossible for
this `beta`; only the finite-exception alternative can occur.

The persistent alternative is also certificate-form.  Over `K=F(lambda)`,
there are `b+1` independent moving core directions

```text
Q_0(lambda),...,Q_b(lambda) in F[lambda]^c
```

satisfying

```text
(H(v)-lambda H(u))(X-beta)Q_i(lambda,X)=0,
(H(v)-lambda H(u))(X-beta)X Q_i(lambda,X)=0         (LowerMK)
```

as polynomial identities.  Conversely, `b+1` `K`-independent moving core
directions satisfying (LowerMK) force the persistent lower-kernel alternative.

For a single moving kernel

```text
Q(lambda)=q_0+q_1 lambda+...+q_D lambda^D
```

with `q_0!=0`, the coefficient ladder is

```text
R_v^core q_0 = 0,
R_v^core q_i - R_u^core q_{i-1} = 0       for 1<=i<=D,
R_u^core q_D = 0.                                      (LowerEL)
```

Thus a persistent lower moving kernel starts in the `v`-endpoint core kernel
and ends in the `u`-endpoint core kernel.

### Proof

Put `r=c-b`.  Persistent low rank says every `r x r` minor of
`R_v^core-lambda R_u^core` is the zero polynomial in `lambda`.  The constant
coefficient of such a minor is the corresponding `r x r` minor of
`R_v^core`, while the coefficient of `lambda^r` is, up to sign, the
corresponding `r x r` minor of `R_u^core`.  Hence every `r x r` minor of both
endpoint matrices vanishes, so both endpoint ranks are `<r`.  Since the
domain dimension is `c`, this is exactly `e_u(beta)>b` and `e_v(beta)>b`.

Over `K=F(lambda)`, the same persistent minor vanishing is equivalent to

```text
rank_K R_lambda^core(beta) < c-b,
```

and therefore to `dim_K ker R_lambda^core(beta)>=b+1`.  Choosing `b+1`
independent kernel vectors over `K` and clearing denominators gives the
polynomial moving core directions.  These are exactly the two displayed
Hankel equations (LowerMK).  The converse is rank-nullity over `K`.

Finally substitute `Q(lambda)=sum_i q_i lambda^i` into

```text
(R_v^core-lambda R_u^core)Q(lambda)=0
```

and compare powers of `lambda`.  If the first nonzero coefficient has positive
degree, divide by the corresponding power of `lambda` first.  This gives
(LowerEL).

## Corollary 29: Lower Common-Image Lines Are Projective-Determinantal

Keep `beta` fixed and put `c=m-1`.  For a nonzero vector `y in F^t`, let
`I=[y]` be the projective image line.  Define the lower common-image direction
map

```text
C_y^core(beta): F^c -> Lambda^2(F^t)^4
```

by sending a degree-`<c` direction `Q` to

```text
( y wedge H(u)(X-beta)Q,
  y wedge H(u)(X-beta)XQ,
  y wedge H(v)(X-beta)Q,
  y wedge H(v)(X-beta)XQ ).
```

Let

```text
e_I(beta)=dim ker C_y^core(beta).
```

This is the direction dimension of the lower common-image row-cut system from
Corollary 26 for the image line `I`.  For `0<=b<c`, the projective low-rank
line locus

```text
P_core,img,>b(beta)={ [y] in P^{t-1}(F) : e_[y](beta)>b }
```

is cut out by the `(c-b) x (c-b)` minors of any matrix for `C_y^core(beta)`.
These minors are homogeneous polynomials of degree `c-b` in the coordinates of
`y`.

If at least one such minor is not the zero polynomial, then

```text
|P_core,img,>b(beta)| <= ((c-b) q^(t-1))/(q-1).      (LowerPI)
```

Outside this projective low-rank locus, the lower common-image part of
`FullCoreGate(beta)` contributes at most

```text
((q^t-1)/(q-1)) binom(n,b)
```

split cores, and hence at most

```text
(n-m+1) ((q^t-1)/(q-1)) binom(n,b)
```

degree-`m` boundary shadows for this fixed anchor.

If every `(c-b) x (c-b)` minor vanishes identically, then over
`K=F(y_0,...,y_{t-1})` there are `b+1` independent moving-image core
directions

```text
Q_0(y),...,Q_b(y) in K^c
```

which, after clearing denominators, satisfy

```text
y wedge H(u)(X-beta)Q_i(y)=0,
y wedge H(u)(X-beta)XQ_i(y)=0,
y wedge H(v)(X-beta)Q_i(y)=0,
y wedge H(v)(X-beta)XQ_i(y)=0.                     (LowerPIC)
```

Conversely, `b+1` independent moving-image core directions satisfying
(LowerPIC) force all `(c-b) x (c-b)` minors of `C_y^core(beta)` to vanish
identically.

### Proof

A direction `Q` lies in the lower common-image direction space for `I=[y]`
exactly when each of the four lower Hankel images

```text
H(u)(X-beta)Q, H(u)(X-beta)XQ,
H(v)(X-beta)Q, H(v)(X-beta)XQ
```

lies in the line `I`.  This is equivalent to the vanishing of its wedge with
`y`, proving the identification with `ker C_y^core(beta)`.

The entries of `C_y^core(beta)` are homogeneous linear forms in the coordinates
of `y`, and scaling `y` does not change the kernel.  The condition
`e_[y](beta)>b` is equivalent to

```text
rank C_y^core(beta) < c-b,
```

and hence to the vanishing of all `(c-b) x (c-b)` minors.  Those minors are
homogeneous of degree `c-b`.

If one such minor is a nonzero homogeneous polynomial of degree `c-b`, the
affine Schwartz-Zippel bound gives at most `(c-b)q^(t-1)` zeros in `F^t`.
Dividing nonzero zeros into projective lines gives (LowerPI).

For image lines outside `P_core,img,>b(beta)`, Corollary 26 gives at most
`binom(n,b)` split cores per line.  There are `(q^t-1)/(q-1)` projective
lines in `F^t`, and each core extends to at most `n-m+1` degree-`m` shadows.

If all minors vanish identically, then over the rational function field
`K=F(y_0,...,y_{t-1})` the rank of `C_y^core(beta)` is `<c-b`, so the kernel
dimension is at least `b+1`.  Choose `b+1` independent kernel vectors over
`K` and clear denominators to get (LowerPIC).  The converse is rank-nullity
over `K`.

## Corollary 30: Fixed-Anchor Full-Core Closure After Lower Rank Charges

Fix an external anchor `beta`, put `c=m-1`, and choose `0<=b<c`.  Assign each
full core-line in `FullCoreGate(beta)` to one of the lower alternatives from
Corollary 24:

```text
u-endpoint, v-endpoint, finite fixed kernel, or projective common image.
```

Let `ChargedCore(beta)` be the set of assigned full cores lying in one of the
following exceptional lower ledgers:

```text
endpoint systems with e_u(beta)>b or e_v(beta)>b;
finite fixed-kernel slopes lambda with e_lambda(beta)>b;
projective image lines I with e_I(beta)>b;
persistent moving-kernel or moving-image certificate ledgers.
```

Assume every uncharged lower endpoint system has direction dimension at most
`b`.  Then the uncharged fixed-anchor full rank-one shadows

```text
Z_beta^{<=b}
 = { S subset D : |S|=m, rank M_S(beta)<=1,
                  no (m-1)-core of S lies in ChargedCore(beta) }
```

satisfy

```text
|Z_beta^{<=b}|
 <= (2/m) binom(n,m-1)
    + (n-m+1) ( 2 + q + (q^t-1)/(q-1) ) binom(n,b).  (FAC)
```

If both lower endpoint dimensions are at most `b`, then Corollary 28 rules out
the persistent lower fixed-kernel alternative, and Corollary 27 gives

```text
|{lambda : e_lambda(beta)>b}| <= c-b
```

for the finite fixed-kernel exceptional slopes.  If the lower common-image
minors are not all identically zero, Corollary 29 gives

```text
|{I : e_I(beta)>b}| <= ((c-b) q^(t-1))/(q-1)
```

for the projective image-line exceptional locus.  Thus, after these explicitly
named lower exceptional ledgers are charged, the fixed-anchor full gate is
reduced to the one-root-loss residual from Corollary 25 plus bounded-rank
lower row-cut ledgers.

### Proof

Split the shadows in `Z_beta^{<=b}` into two classes.

First, suppose no `(m-1)`-core of `S` lies in `FullCoreGate(beta)`.  Corollary
25 bounds these shadows by

```text
(2/m) binom(n,m-1).
```

Second, suppose `S` has at least one core in `FullCoreGate(beta)`.  Since
`S` has no core in `ChargedCore(beta)`, each assigned full core that we count
lies in a lower row-cut system of direction dimension at most `b`.  Corollary
26 bounds the number of such uncharged full cores by

```text
( 2 + q + (q^t-1)/(q-1) ) binom(n,b),
```

and each core extends to at most `n-m+1` shadows.  Adding the two classes gives
(FAC).

The final assertions are just Corollaries 28, 27, and 29 applied to the lower
fixed-kernel and lower common-image exceptional sets.

## Corollary 30.1: Lower Root-Free Full-Core Ledgers Gain A Slice Factor

Keep `beta` fixed and put `c=m-1`.  Let

```text
A=P_0+V
```

be an affine solution space of monic degree-`c` core locators inside any one of
the lower full-core row-rank ledgers from Corollary 26.  Put `e=dim V`, and
let `Core(A)` be a set of squarefree `D`-split core locators assigned to this
stratum.

For `alpha in D`, write

```text
ev_alpha:V -> F,        Q |-> Q(alpha).
```

Assume `e>=1` and that the common-root part of the lower stratum has already
been charged to the fixed-root/root-slice ledger, in the following precise
sense: whenever some assigned core in `Core(A)` vanishes at `alpha`, the
functional `ev_alpha` is nonzero on `V`.  Then

```text
|Core(A)| <= (n/c) binom(n-1,e-1)
          = (e/c) binom(n,e).                       (LowerRF)
```

If `e=0`, the row-rank injection bound gives the conservative estimate

```text
|Core(A)| <= 1.
```

Define

```text
Psi_c(0)=1,        Psi_c(e)=(e/c) binom(n,e) for e>=1.
```

After common-root charges, Corollary 26 sharpens to

```text
|FullCoreGate^{rootfree}(beta)|
 <= Psi_c(e_u(beta)) + Psi_c(e_v(beta))
    + sum_{lambda in F} Psi_c(e_lambda(beta))
    + sum_{I in P(F^t)} Psi_c(e_I(beta)).           (LowerFCRF)
```

Consequently, in the bounded-rank range `1<=b<=n/2`, if every uncharged lower
system has direction dimension at most `b`, then

```text
|FullCoreGate^{rootfree,<=b}(beta)|
 <= ( 2 + q + (q^t-1)/(q-1) ) (b/c) binom(n,b),
```

and the fixed-anchor closure of Corollary 30 improves to

```text
|Z_beta^{rootfree,<=b}|
 <= (2/m) binom(n,m-1)
    + (n-m+1) ( 2 + q + (q^t-1)/(q-1) )
      (b/c) binom(n,b).                             (FAC_RF)
```

Thus, once common-root lower core pieces are charged, the bounded-rank
full-core term carries a genuine root-slice saving.  The one-root-loss
residual from Corollary 25 is unchanged.

### Proof

For fixed `alpha in D`, let `Core_alpha(A)` be the assigned split cores in
`Core(A)` that vanish at `alpha`.  If this set is empty there is nothing to
count.  Otherwise the hypothesis says `ev_alpha` is nonzero on `V`, so the
cores in `A` that vanish at `alpha` form an affine subspace whose direction
space is

```text
W_alpha=ker(ev_alpha:V->F),
```

with `dim W_alpha=e-1`.

Fix `L_R in Core_alpha(A)`.  Since every `Q in W_alpha` has degree `<c` and
vanishes at `alpha`, the evaluation map

```text
W_alpha -> F^{R\{alpha}}
```

is injective: a nonzero `Q` cannot vanish on `alpha` and on all `c-1` other
roots of `R`.  Choose the first `(e-1)`-subset of `R\{alpha}` on which
evaluation is injective.  This injects `Core_alpha(A)` into the
`(e-1)`-subsets of `D\{alpha}`, so

```text
|Core_alpha(A)| <= binom(n-1,e-1).
```

Counting incidences `(alpha,R)` with `alpha in R` gives

```text
c |Core(A)| = sum_{alpha in D} |Core_alpha(A)|
             <= n binom(n-1,e-1),
```

which proves (LowerRF).  The case `e=0` is the old row-rank injection bound.

Apply (LowerRF) to each lower endpoint, finite fixed-kernel, and projective
image-line stratum from Corollary 26 to get (LowerFCRF).  If
`1<=e<=b<=n/2`, then `Psi_c(e)<= (b/c)binom(n,b)` because
`e binom(n,e)` is increasing for `e<=n/2`.  Summing over two endpoints, at
most `q` finite slopes, and `(q^t-1)/(q-1)` projective image lines gives the
bounded-rank estimate.  Multiplying by the extension factor `n-m+1` and adding
the unchanged Corollary 25 residual gives (FAC_RF).

## Corollary 31: Lower Endpoint Bad Anchors Have A Finite-Exception Dichotomy

Fix `w in {u,v}` and put `c=m-1`.  For each anchor `beta in F`, let

```text
R_w^core(beta): F^c -> F^{2t}
```

be the homogeneous direction matrix on degree-`<c` core directions for the
lower endpoint system

```text
H(w)(X-beta)Q = 0,
H(w)(X-beta)XQ = 0.                                (End_beta)
```

Let

```text
e_w(beta)=dim ker R_w^core(beta).
```

Fix `0<=b<c`, and define the bad-anchor endpoint locus

```text
B_{w,>b}={ beta in F : e_w(beta)>b }.
```

Then one of the following alternatives holds.

```text
finite-anchor alternative:
  |B_{w,>b}| <= c-b;

persistent endpoint-anchor alternative:
  e_w(beta)>b for every beta in F.
```

More precisely, write

```text
R_w^core(beta)=R_{w,+}^core - beta R_{w,0}^core,
```

where `R_{w,0}^core` is the direction matrix for

```text
H(w)Q=0,        H(w)XQ=0,
```

and `R_{w,+}^core` is the direction matrix for

```text
H(w)XQ=0,       H(w)X^2Q=0.
```

If some `(c-b) x (c-b)` minor of `R_w^core(beta)` is not the zero polynomial
in `beta`, then the finite-anchor alternative holds.  If every such minor
vanishes identically, then the persistent endpoint-anchor alternative holds;
in that case

```text
dim ker R_{w,0}^core > b,        dim ker R_{w,+}^core > b.   (EndCoeff)
```

The persistent alternative is also certificate-form.  Over `K=F(beta)`, there
are `b+1` independent moving endpoint-core directions

```text
Q_0(beta),...,Q_b(beta) in F[beta]^c
```

satisfying

```text
H(w)(X-beta)Q_i(beta,X)=0,
H(w)(X-beta)XQ_i(beta,X)=0.                         (EndMK)
```

Conversely, `b+1` `K`-independent moving directions satisfying (EndMK) force
the persistent endpoint-anchor alternative.

Thus, unless the endpoint-anchor pencil is persistently low-rank, each
endpoint contributes at most `c-b` anchors to the charged endpoint part of
Corollary 30.

### Proof

The identities

```text
(X-beta)Q = XQ - beta Q,
(X-beta)XQ = X^2Q - beta XQ
```

show that the endpoint direction matrix has the displayed affine form in
`beta`.  The condition `e_w(beta)>b` is equivalent to

```text
rank R_w^core(beta) < c-b,
```

and hence to the vanishing at `beta` of all `(c-b) x (c-b)` minors.  Each such
minor is a polynomial of degree at most `c-b`.

If one minor is nonzero, it has at most `c-b` roots, proving the
finite-anchor alternative.  If every such minor is the zero polynomial, then
the rank is `<c-b` for every `beta`, proving persistence.  The constant and
top-degree coefficients of all `(c-b) x (c-b)` minors are, up to sign, the
corresponding minors of `R_{w,+}^core` and `R_{w,0}^core`, so both coefficient
endpoint matrices have rank `<c-b`.  This proves (EndCoeff).

Over `K=F(beta)`, persistent minor vanishing is equivalent to
`dim_K ker R_w^core(beta)>=b+1`.  Choosing `b+1` independent kernel vectors and
clearing denominators gives the polynomial moving endpoint-core directions.
These are exactly (EndMK).  The converse is rank-nullity over `K`.

## Corollary 32: Lower Fixed-Kernel Bad Anchor-Slope Pairs Are Determinantal

Put `c=m-1` and fix `0<=b<c`.  For an anchor `beta in F` and a finite lower
fixed-kernel slope `lambda in F`, let

```text
R_{beta,lambda}^core: F^c -> F^{2t}
```

be the homogeneous direction matrix on degree-`<c` core directions for

```text
(H(v)-lambda H(u))(X-beta)Q = 0,
(H(v)-lambda H(u))(X-beta)XQ = 0.                    (CoreKer_pair)
```

Let

```text
e(beta,lambda)=dim ker R_{beta,lambda}^core
```

and define the bad anchor-slope locus

```text
B_{ker,>b}={ (beta,lambda) in F^2 : e(beta,lambda)>b }.
```

Then `B_{ker,>b}` is cut out by the `(c-b) x (c-b)` minors of
`R_{beta,lambda}^core`.  Each entry of this matrix has bidegree at most `(1,1)`
in `(beta,lambda)`, and each such minor has total degree at most `2(c-b)`.
Consequently one of the following alternatives holds.

```text
finite pair-locus alternative:
  |B_{ker,>b}| <= 2(c-b) q;

two-parameter persistent lower-kernel alternative:
  e(beta,lambda)>b for every (beta,lambda) in F^2.
```

More precisely, the finite pair-locus alternative holds whenever at least one
`(c-b) x (c-b)` minor is not the zero polynomial in `F[beta,lambda]`.  If every
such minor vanishes identically, then over `K=F(beta,lambda)` there are `b+1`
independent moving core directions

```text
Q_0(beta,lambda),...,Q_b(beta,lambda) in F[beta,lambda]^c
```

satisfying

```text
(H(v)-lambda H(u))(X-beta)Q_i(beta,lambda,X)=0,
(H(v)-lambda H(u))(X-beta)XQ_i(beta,lambda,X)=0.      (PairMK)
```

Conversely, `b+1` `K`-independent moving directions satisfying (PairMK) force
the two-parameter persistent alternative.

Thus, after charging the bad pair locus `B_{ker,>b}`, the uncharged finite
fixed-kernel full-core ledger over all anchors and finite slopes contributes at
most

```text
q^2 binom(n,b)
```

split cores, and at most

```text
q^2 (n-m+1) binom(n,b)
```

boundary shadows before the lower root-free refinement.  After common-root
lower core pieces have been charged and `1<=b<=n/2`, the same term improves to

```text
q^2 (b/c) binom(n,b)
```

split cores.

### Proof

Expanding the two equations in (CoreKer_pair) gives

```text
(H(v)-lambda H(u))(X-beta)Q
 = H(v)XQ - beta H(v)Q - lambda H(u)XQ + beta lambda H(u)Q,

(H(v)-lambda H(u))(X-beta)XQ
 = H(v)X^2Q - beta H(v)XQ
   - lambda H(u)X^2Q + beta lambda H(u)XQ.
```

Therefore every entry of the direction matrix is bilinear in
`(beta,lambda)`, with bidegree at most `(1,1)` and total degree at most `2`.
The condition `e(beta,lambda)>b` is equivalent to

```text
rank R_{beta,lambda}^core < c-b,
```

and hence to the vanishing of all `(c-b) x (c-b)` minors.  These minors have
total degree at most `2(c-b)`.

If one minor is a nonzero polynomial, the common bad locus is contained in the
zero set of that one polynomial.  The elementary two-variable finite-field
Schwartz-Zippel bound gives at most `2(c-b)q` zeros in `F^2`, proving the finite
pair-locus alternative.  If every minor vanishes identically, then the rank over
`K=F(beta,lambda)` is `<c-b`, so the kernel over `K` has dimension at least
`b+1`.  Choosing independent kernel vectors and clearing denominators gives
(PairMK).  The converse is rank-nullity over `K`.

Outside the charged bad pair locus, each fixed pair `(beta,lambda)` has
direction dimension at most `b`, so Corollary 26 gives at most `binom(n,b)`
split cores for that pair.  There are at most `q^2` anchor-slope pairs.  Each
core extends to at most `n-m+1` boundary shadows.  The root-free improvement is
Corollary 30.1 applied to each good pair.

## Corollary 33: Lower Common-Image Bad Anchor-Line Incidence Is Determinantal

Put `c=m-1` and fix `0<=b<c`.  For an anchor `beta in F` and a projective image
line `I=[y] in P(F^t)`, let

```text
C_{beta,y}^core: F^c -> Lambda^2(F^t)^4
```

be the homogeneous direction map

```text
Q |-> ( y wedge H(u)(X-beta)Q,
        y wedge H(u)(X-beta)XQ,
        y wedge H(v)(X-beta)Q,
        y wedge H(v)(X-beta)XQ ).
```

Let

```text
e(beta,[y])=dim ker C_{beta,y}^core
```

and define the bad anchor-image incidence

```text
B_img,>b={ (beta,[y]) in F x P(F^t) : e(beta,[y])>b }.
```

Then `B_img,>b` is cut out by the `(c-b) x (c-b)` minors of
`C_{beta,y}^core`.  Each entry of this matrix has degree at most one in `beta`
and is homogeneous linear in `y`.  Hence each such minor has beta-degree at most
`c-b`, is homogeneous of degree `c-b` in `y`, and has total degree at most
`2(c-b)`.

Consequently one of the following alternatives holds.

```text
finite anchor-image incidence alternative:
  |B_img,>b| <= (2(c-b) q^t)/(q-1);

persistent anchor-image alternative:
  e(beta,[y])>b for every beta in F and every [y] in P(F^t).
```

More precisely, the finite incidence alternative holds whenever at least one
`(c-b) x (c-b)` minor is not the zero polynomial in `F[beta,y_0,...,y_{t-1}]`.
If every such minor vanishes identically, then over
`K=F(beta,y_0,...,y_{t-1})` there are `b+1` independent moving image-core
directions

```text
Q_0(beta,y),...,Q_b(beta,y) in F[beta,y]^c
```

satisfying, after clearing denominators,

```text
y wedge H(u)(X-beta)Q_i(beta,y,X)=0,
y wedge H(u)(X-beta)XQ_i(beta,y,X)=0,
y wedge H(v)(X-beta)Q_i(beta,y,X)=0,
y wedge H(v)(X-beta)XQ_i(beta,y,X)=0.                (PairPIC)
```

Conversely, `b+1` `K`-independent moving directions satisfying (PairPIC) force
the persistent anchor-image alternative.

Thus, after charging the bad incidence `B_img,>b`, the uncharged lower
common-image full-core ledger over all anchors and projective image lines
contributes at most

```text
q ((q^t-1)/(q-1)) binom(n,b)
```

split cores, and at most

```text
q (n-m+1) ((q^t-1)/(q-1)) binom(n,b)
```

boundary shadows before the lower root-free refinement.  After common-root
lower core pieces have been charged and `1<=b<=n/2`, the same split-core term
improves to

```text
q ((q^t-1)/(q-1)) (b/c) binom(n,b).
```

### Proof

For fixed `Q`, each vector

```text
H(w)(X-beta)Q,        H(w)(X-beta)XQ
```

is affine-linear in `beta`.  Wedging with `y` makes every coordinate of
`C_{beta,y}^core` homogeneous linear in `y` and degree at most one in `beta`.
Thus an `r x r` minor, with `r=c-b`, has beta-degree at most `r`, homogeneous
`y`-degree `r`, and total degree at most `2r`.

The condition `e(beta,[y])>b` is equivalent to

```text
rank C_{beta,y}^core < c-b,
```

and hence to the vanishing of all `r x r` minors.  If one such minor `P` is not
the zero polynomial, then the bad incidence is contained in the projectivization
in `y` of the affine zero set of `P(beta,y)`.  The affine Schwartz-Zippel bound
in the `t+1` variables `(beta,y)` gives at most `2r q^t` affine zeros.  Since
`P` is homogeneous in `y`, every projective bad pair has `q-1` nonzero affine
representatives.  Therefore

```text
|B_img,>b| <= (2r q^t)/(q-1).
```

If every `r x r` minor vanishes identically, then the rank over
`K=F(beta,y_0,...,y_{t-1})` is `<r`, so the kernel dimension is at least `b+1`.
Choosing independent kernel vectors and clearing denominators gives (PairPIC).
The converse is rank-nullity over `K`.

Outside the charged bad incidence, each anchor-image pair has direction
dimension at most `b`, so Corollary 26 gives at most `binom(n,b)` split cores
for that pair.  There are `q((q^t-1)/(q-1))` such pairs, and each core extends
to at most `n-m+1` boundary shadows.  The root-free improvement is Corollary
30.1 applied pairwise.

## Corollary 34: All-Anchor Full-Gate Closure After Global Lower Charges

Put `c=m-1`, choose `1<=b<c`, and assume `b<=n/2`.  For each anchor `beta`,
assign every full core-line in `FullCoreGate(beta)` to one of the four lower
alternatives from Corollary 24.  Charge the following global lower ledgers:

```text
endpoint-bad anchors:
  beta with e_u(beta)>b or e_v(beta)>b;

fixed-kernel bad pairs:
  (beta,lambda) in B_{ker,>b};

common-image bad incidences:
  (beta,[y]) in B_img,>b;

persistent moving endpoint, fixed-kernel, or common-image certificate ledgers;
common-root lower core pieces from Corollary 30.1.
```

Let `Z_all^{rf,<=b}` be the remaining root-free all-anchor full-gate incidence:

```text
Z_all^{rf,<=b}
 = { (beta,S) : beta in F, S subset D, |S|=m, rank M_S(beta)<=1,
                no (m-1)-core of S is assigned to a charged lower ledger }.
```

Then

```text
|Z_all^{rf,<=b}|
 <= q (2/m) binom(n,m-1)
    + q (n-m+1) ( 2 + q + (q^t-1)/(q-1) )
      (b/c) binom(n,b).                              (AllFAC_RF)
```

Let `Z_all^{<=b}` be the analogous all-anchor incidence before the common-root
lower core pieces are charged.  Without the root-free common-root charge,
`Z_all^{<=b}` satisfies the same bound with the second term replaced by

```text
q (n-m+1) ( 2 + q + (q^t-1)/(q-1) ) binom(n,b).      (AllFAC)
```

Moreover, outside the corresponding persistent alternatives, the charged
low-rank parameter loci have the explicit sizes

```text
|{ endpoint-bad anchors }| <= 2(c-b),
|B_{ker,>b}|              <= 2(c-b)q,
|B_img,>b|                <= (2(c-b)q^t)/(q-1).      (GlobalCharges)
```

Consequently the number of anchors `beta` supporting an uncharged root-free
full-gate shadow is also bounded by the right hand side of (AllFAC_RF).  In any
parameter regime where this incidence bound is polynomial, the full-core
component of the all-anchor boundary-off problem is reduced to the explicitly
listed global charges plus the Corollary 25 one-root-loss residual.

### Proof

After the endpoint-bad anchors are charged, every uncharged anchor has

```text
e_u(beta)<=b,        e_v(beta)<=b.
```

After the fixed-kernel bad pairs and common-image bad incidences are charged,
every uncharged lower fixed-kernel pair and every uncharged lower common-image
pair has direction dimension at most `b`.  The persistent alternatives have
also been moved to their own certificate ledgers.  Thus, for each fixed
uncharged anchor `beta`, the hypotheses of Corollary 30 hold for the non-root
free statement, and the hypotheses of Corollary 30.1 hold after common-root
lower core pieces have been charged.

Applying Corollary 30.1 to each anchor gives

```text
|Z_beta^{rootfree,<=b}|
 <= (2/m) binom(n,m-1)
    + (n-m+1) ( 2 + q + (q^t-1)/(q-1) )
      (b/c) binom(n,b).
```

There are at most `q` anchors, so summing this inequality over anchors gives
(AllFAC_RF).  The same summation applied to Corollary 30 gives (AllFAC).

The three displayed charge sizes are exactly Corollaries 31, 32, and 33, with
the two endpoint anchor sets union-bounded.  Finally, projecting an incidence
set `(beta,S)` to its anchor coordinate cannot increase cardinality, so the
same bound controls the uncharged anchor projection.

## Corollary 35: Full-Core Anchor Multiplicity Collapses Unless Globally Full

Fix an `(m-1)`-core `R subset D`.  For anchor and extension variables
`beta,Y`, put

```text
N_R(beta,Y) = [ H(u)(X-beta)(X-Y)L_R    H(v)(X-beta)(X-Y)L_R ].
```

Define the globally full core-line ledger

```text
GlobalFullCore
 = { R : rank N_R(beta,Y) <= 1 identically in F[beta,Y] }.
```

For fixed `R`, let

```text
A_R={ beta in F : R in FullCoreGate(beta) }.
```

If `R notin GlobalFullCore`, then

```text
|A_R| <= 2.                                           (CoreAnchor)
```

Consequently, after the globally full core-lines have been charged, the
all-anchor full-core shadow incidence

```text
I_full^nonglobal
 = { (beta,S) : beta in F, S subset D, |S|=m,
                S contains a core R in FullCoreGate(beta)
                with R notin GlobalFullCore }
```

satisfies

```text
|I_full^nonglobal| <= 2 (n-m+1) binom(n,m-1).          (NGFull)
```

Combining this with the Corollary 25 residual gives the direct all-anchor bound
after globally full core-lines are charged:

```text
|{ (beta,S) : rank M_S(beta)<=1,
                no (m-1)-core of S lies in GlobalFullCore }|
 <= ( (2q)/m + 2(n-m+1) ) binom(n,m-1).               (DirectAllCore)
```

Thus the full-core part of the all-anchor gate has no field-size multiplicity
except through the explicit one-root-loss residual and the globally full
two-variable core-line obstruction.

### Proof

For fixed `R`, write

```text
(X-beta)(X-Y)L_R
 = X^2 L_R - (beta+Y)X L_R + beta Y L_R.
```

Thus both Hankel images in `N_R(beta,Y)` have bidegree at most `(1,1)` in
`(beta,Y)`.  For any row-pair minor `P_R(beta,Y)`, the coefficients of
`P_R(beta,Y)` as a polynomial in `Y` have degree at most two in `beta`; this is
the same coefficient ledger as Corollary 23, now with the anchor dependence
left visible.

The condition `R in FullCoreGate(beta)` says that every row-pair minor
`P_R(beta,Y)` vanishes identically as a polynomial in `Y`.  Equivalently, all
of its `Y`-coefficients vanish at that value of `beta`.

If `R notin GlobalFullCore`, some `Y`-coefficient of some row-pair minor is a
nonzero polynomial in `beta` of degree at most two.  Every `beta in A_R` is a
root of this one nonzero polynomial, so `|A_R|<=2`.

For (NGFull), each non-global core has at most two full-core anchors and, for
each such anchor, at most `n-m+1` extensions to a degree-`m` shadow.  There are
`binom(n,m-1)` split cores.  Finally, for any anchor and shadow with no globally
full core, either no core of the shadow lies in `FullCoreGate(beta)`, which is
counted by the Corollary 25 residual, or at least one non-global full core is
present, which is counted by (NGFull).  Summing the residual over the at most
`q` anchors gives (DirectAllCore).

## Corollary 36: Globally Full Cores Are Three-Shift Ruled Pencils

Keep the notation of Corollary 35 and put

```text
U_i=H(u)X^i L_R,        V_i=H(v)X^i L_R,        i=0,1,2.
```

If `R in GlobalFullCore`, then at least one of the following global alternatives
holds.

```text
u three-shift endpoint:
  U_0=U_1=U_2=0;

v three-shift endpoint:
  V_0=V_1=V_2=0;

global common image:
  dim span{U_i,V_i : i=0,1,2} <= 1;

global fixed kernel:
  there is lambda in F such that V_i=lambda U_i for i=0,1,2.
```

Thus globally full core-lines are not a new unstructured obstruction: they are
three-shift versions of the endpoint, common-image, and fixed-kernel ruled
ledgers.

For a monic degree-`c=m-1` core locator, let the corresponding affine row-rank
systems have direction dimensions

```text
g_u, g_v, g_lambda, g_I
```

for the two endpoints, finite slopes `lambda in F`, and projective image lines
`I in P(F^t)`.  Assign each globally full split core to any one alternative it
satisfies.  Then

```text
|GlobalFullCore|
 <= binom(n,g_u)+binom(n,g_v)
    + sum_{lambda in F} binom(n,g_lambda)
    + sum_{I in P(F^t)} binom(n,g_I).                 (GFC_RR)
```

In particular, if all uncharged three-shift global systems have direction
dimension at most `b`, then

```text
|GlobalFullCore^{<=b}|
 <= ( 2 + q + (q^t-1)/(q-1) ) binom(n,b).             (GFC_B)
```

After common-root global core pieces have been charged, the same root-free
replacement as Corollary 30.1 applies to each positive-dimensional stratum:
`binom(n,e)` can be replaced by `(e/c)binom(n,e)`.

Consequently, under the bounded-rank hypothesis above, the uncharged all-anchor
rank-one incidence is bounded by

```text
|{ (beta,S) : rank M_S(beta)<=1,
                no (m-1)-core of S lies in a charged high-dimensional
                global three-shift ledger }|
 <= ( (2q)/m + 2(n-m+1) ) binom(n,m-1)
    + q(n-m+1) ( 2 + q + (q^t-1)/(q-1) ) binom(n,b),
```

after the high-dimensional global three-shift ledgers are charged.  In the
root-free charged version, the final `binom(n,b)` term gains the factor `b/c`
for `1<=b<=n/2`.

### Proof

Write

```text
U(beta,Y)=U_2-(beta+Y)U_1+beta Y U_0,
V(beta,Y)=V_2-(beta+Y)V_1+beta Y V_0.
```

Since `R in GlobalFullCore`, we have

```text
U(beta,Y) wedge V(beta,Y)=0
```

as a polynomial identity.  Put `s=beta+Y` and `p=beta Y`.  The subring
`F[s,p]` injects into `F[beta,Y]`, so equivalently

```text
(U_2-sU_1+pU_0) wedge (V_2-sV_1+pV_0)=0              (GFC)
```

in `Lambda^2(F^t)[s,p]`.

Let `W=span{U_0,U_1,U_2}`.  If `dim W=0`, the `u` endpoint alternative holds.
If `dim W=1`, then `U_2-sU_1+pU_0=f(s,p)e` for a nonzero vector `e` and a
nonzero polynomial `f`.  Since the polynomial ring is a domain, (GFC) implies
`e wedge (V_2-sV_1+pV_0)=0`, so all `V_i` lie in the same line `F e`; this is
the global common-image alternative.

It remains to consider `dim W>=2`.  Over the fraction field `F(s,p)`, (GFC)
says that `V(beta,Y)=mu(s,p)U(beta,Y)` for some rational function `mu`.  Choose
two linear functionals `phi,psi` on `F^t` for which the affine-linear
polynomials `phi(U)` and `psi(U)` are nonproportional and `phi(U)` is
nonconstant.  They are therefore coprime in `F[s,p]`.  From

```text
phi(V) psi(U) = psi(V) phi(U)
```

we get that `phi(U)` divides `phi(V)`.  Both are affine-linear, so
`phi(V)=lambda phi(U)` for some constant `lambda in F`.  Then
`V-lambda U` is still pointwise collinear with `U`, and its `phi`-coordinate is
zero.  Over the fraction field, `V-lambda U=nu(s,p)U`; applying `phi` gives
`0=nu(s,p)phi(U)`.  Since `phi(U)` is nonzero, `nu=0`, so `V=lambda U`.  Hence
`V_i=lambda U_i` for `i=0,1,2`, proving the fixed-kernel alternative.  The
`v` endpoint is the subcase `lambda=0` in this branch, and is listed separately
because it has its own row-rank ledger.

The row-rank bounds are the same evaluation-injection argument used in
Corollary 26.  Each endpoint, fixed-kernel slope, or image line imposes an
affine system on monic degree-`c` core locators with the displayed direction
dimension; split cores in such a stratum inject into `g`-subsets of `D`, giving
`binom(n,g)`.  Summing over the two endpoints, `q` finite slopes, and
`(q^t-1)/(q-1)` image lines proves (GFC_RR) and (GFC_B).

The root-free replacement is exactly the incidence proof of Corollary 30.1
applied to these three-shift affine strata.  Finally, add the non-global
all-anchor bound (DirectAllCore) from Corollary 35 to the contribution of
globally full cores, which is at most

```text
q(n-m+1)|GlobalFullCore^{<=b}|.
```

This gives the displayed all-anchor incidence bound.

## Corollary 37: Three-Shift Global Ledgers Have Determinantal Charges

Put `c=m-1` and fix `0<=b<c`.  For a finite slope `lambda in F`, let

```text
G_lambda: F^c -> F^{3t}
```

be the homogeneous direction matrix for the three-shift fixed-kernel system

```text
(H(v)-lambda H(u)) X^i Q = 0,        i=0,1,2,
```

and put

```text
g_lambda=dim ker G_lambda.
```

Then the bad slope set

```text
E_{G,>b}={ lambda in F : g_lambda>b }
```

has the following dichotomy.

```text
finite global-slope alternative:
  |E_{G,>b}| <= c-b;

persistent global-slope alternative:
  g_lambda>b for every lambda in F.
```

More precisely, if some `(c-b) x (c-b)` minor of `G_lambda` is not the zero
polynomial in `lambda`, the finite alternative holds.  If every such minor
vanishes identically, then the endpoint three-shift systems

```text
H(u)X^i Q=0,        H(v)X^i Q=0,        i=0,1,2,
```

both have direction dimension `>b`, and there are `b+1` independent moving
three-shift kernels over `F(lambda)`.  For a single nonzero moving kernel

```text
Q(lambda)=q_0+q_1 lambda+...+q_D lambda^D,
```

after dividing by the first nonzero power of `lambda` if necessary, its
coefficients satisfy the endpoint ladder

```text
G_v q_0 = 0,
G_v q_i - G_u q_{i-1} = 0        for 1<=i<=D,
G_u q_D = 0.                                           (GEL)
```

Thus a persistent three-shift moving kernel starts in the `v` endpoint
three-shift kernel and ends in the `u` endpoint three-shift kernel.

Similarly, for a projective image line `I=[y] in P(F^t)`, let

```text
C_y^G: F^c -> Lambda^2(F^t)^6
```

be the direction map

```text
Q |-> ( y wedge H(u)X^i Q, y wedge H(v)X^i Q )_{i=0,1,2},
```

and put `g_I=dim ker C_y^G`.  The bad image-line locus

```text
P_{G,img,>b}={ [y] in P(F^t) : g_[y]>b }
```

is cut out by homogeneous `(c-b) x (c-b)` minors of degree `c-b` in `y`.  If at
least one such minor is nonzero, then

```text
|P_{G,img,>b}| <= ((c-b) q^(t-1))/(q-1).              (GPI)
```

If all such minors vanish identically, there are `b+1` independent moving
three-shift image directions over `F(y_0,...,y_{t-1})`.

Consequently, after charging endpoint systems with direction dimension `>b`,
the finite bad slopes `E_{G,>b}`, the projective bad image-line locus
`P_{G,img,>b}`, and the persistent moving-certificate alternatives, the
globally full core ledger from Corollary 36 contributes at most

```text
( 2 + q + (q^t-1)/(q-1) ) binom(n,b)
```

split cores, with the root-free `b/c` improvement after common-root global core
pieces are charged.

### Proof

The matrix `G_lambda` has the affine form

```text
G_lambda=G_v-lambda G_u,
```

where `G_w` is the direction matrix for the endpoint equations
`H(w)X^iQ=0`, `i=0,1,2`.  Thus `g_lambda>b` is equivalent to
`rank G_lambda<c-b`, i.e. to vanishing of all `(c-b) x (c-b)` minors.  These
minors have degree at most `c-b` in `lambda`.

If one minor is nonzero, it has at most `c-b` roots.  If every minor vanishes
identically, the constant and top-degree coefficients show that all
`(c-b) x (c-b)` minors of both `G_v` and `G_u` vanish, so both endpoint kernels
have dimension `>b`.  Over `F(lambda)`, persistent minor vanishing is equivalent
to kernel dimension at least `b+1`; clearing denominators gives the moving
three-shift kernels.

Substituting `Q(lambda)=sum_i q_i lambda^i` into

```text
(G_v-lambda G_u)Q(lambda)=0
```

and comparing powers of `lambda` gives (GEL).  If the first nonzero coefficient
of `Q` occurs at positive degree, divide by the corresponding power of
`lambda` before comparing coefficients.

For the image-line statement, the entries of `C_y^G` are homogeneous linear
forms in `y`.  Hence its `(c-b) x (c-b)` minors are homogeneous of degree
`c-b`, and the same projective Schwartz-Zippel count as in Corollaries 16 and
29 gives (GPI) when one minor is nonzero.  If all minors vanish identically,
rank-nullity over `F(y_0,...,y_{t-1})` gives `b+1` moving image directions, and
the converse is immediate.

The final bounded-rank count is exactly Corollary 36 after the endpoint,
finite-slope, image-line, and moving-certificate bad global ledgers have been
charged.  The root-free replacement is the Corollary 30.1 incidence argument
applied to these three-shift strata.

## Corollary 38: Three-Shift Endpoint Ledgers Are Exact Frontier Shifts

Put `c=m-1`.  For any syndrome vector `w`, the three-shift endpoint system on
degree-`<c` core directions

```text
H_{t,j}(w)X^i Q = 0,        i=0,1,2,                  (ThreeShift_w)
```

is exactly the single deeper Hankel system

```text
H_{t+2,c-1}(w) Q = 0.                                (FrontierShift)
```

Consequently the endpoint direction matrices `G_u,G_v` from Corollary 37 are
ordinary Hankel windows:

```text
G_u = H_{t+2,c-1}(u),        G_v = H_{t+2,c-1}(v),
```

and the three-shift fixed-kernel pencil is the deeper Hankel pencil

```text
G_lambda = H_{t+2,c-1}(v-lambda u).
```

Thus the endpoint and fixed-kernel global full-core charges do not create a new
type of row-rank condition.  They are precisely the original Hankel-pencil
kernel condition shifted from `(t,j)` to `(t+2,c-1)=(t+2,j-2)`.

In particular, if a lower-depth theory supplies a rank bound for
`H_{t+2,c-1}(w)` on degree-`<c` locators, then the endpoint and fixed-kernel
charges in Corollaries 36 and 37 consume that bound without any additional
square-root or one-root loss.

### Proof

Write

```text
Q(X)=q_0+q_1X+...+q_{c-1}X^{c-1}.
```

The `a`-th row of `H_{t,j}(w)X^i Q` is

```text
sum_{h=0}^{c-1} w_{a+i+h} q_h,        0<=a<t,  i=0,1,2.
```

For fixed `i`, these are the deeper Hankel rows with indices

```text
i, i+1, ..., i+t-1.
```

As `i` runs through `0,1,2`, the union of these intervals is exactly

```text
0,1,...,t+1.
```

These are precisely the rows of `H_{t+2,c-1}(w)Q`.  Hence the three shifted
systems and the deeper Hankel system impose the same equations on `Q`.

The identities for `G_u`, `G_v`, and `G_lambda` follow by applying the same
calculation to `w=u`, `w=v`, and `w=v-lambda u`.

## Corollary 38.1: Consecutive Shift Frontiers Iterate Losslessly

Let `r>=0` and let `Q` range over degree-`<c` directions.  For any syndrome
vector `w`, the consecutive `(r+1)`-shift system

```text
H_{t,c+r-1}(w)X^iQ=0,        0<=i<=r,                (Shift_r)
```

is exactly the single deeper Hankel system

```text
H_{t+r,c-1}(w)Q=0.                                  (Frontier_r)
```

Equivalently, a stack of consecutive shift-frontier endpoint equations adds
`r` Hankel rows and removes `r` locator degrees, but introduces no further
algebraic loss.  Thus any lower-depth rank, injectivity, or endpoint charge
bound for `H_{t+r,c-1}(w)` is consumed once by the whole consecutive-shift
stack, not once per shift.

The same identity holds for fixed-kernel pencils:

```text
H_{t,c+r-1}(v-lambda u)X^iQ=0,        0<=i<=r,
```

is equivalent to

```text
H_{t+r,c-1}(v-lambda u)Q=0.
```

### Proof

Write `Q(X)=sum_{h=0}^{c-1}q_hX^h`.  The `a`-th row of
`H_{t,c+r-1}(w)X^iQ` is

```text
sum_{h=0}^{c-1} w_{a+i+h}q_h,        0<=a<t.
```

For fixed `i`, these are exactly the deeper Hankel rows with indices

```text
i, i+1, ..., i+t-1.
```

As `i` ranges from `0` to `r`, the union of these consecutive row intervals is

```text
0,1,...,t+r-1,
```

which is precisely the row set of `H_{t+r,c-1}(w)Q`.  Hence the stacked
shift system and the deeper Hankel system impose the same equations.  Applying
the identity to `w=v-lambda u` gives the fixed-kernel pencil statement.

## Corollary 38.2: Consecutive Fixed-Kernel Charges Have No Extra Slope Loss

Keep `0<=b<c`, let `r>=0`, and put

```text
G_u^(r)=H_{t+r,c-1}(u),        G_v^(r)=H_{t+r,c-1}(v).
```

For a finite slope `lambda`, let

```text
G_lambda^(r)=G_v^(r)-lambda G_u^(r)
            =H_{t+r,c-1}(v-lambda u),
```

and write

```text
g_lambda^(r)=dim ker G_lambda^(r).
```

The bad finite-slope set

```text
E_{r,>b}={ lambda in F : g_lambda^(r)>b }
```

has the following dichotomy.

```text
finite consecutive-slope alternative:
  |E_{r,>b}| <= c-b;

persistent consecutive-slope alternative:
  g_lambda^(r)>b for every lambda.
```

More precisely, if some `(c-b) x (c-b)` minor of `G_lambda^(r)` is not the
zero polynomial in `lambda`, the finite alternative holds.  If every such
minor vanishes identically, then both deeper endpoint maps have direction
dimension `>b`:

```text
dim ker G_u^(r)>b,        dim ker G_v^(r)>b.
```

In the persistent case there are `b+1` independent moving kernels over
`F(lambda)`.  For a single nonzero moving kernel

```text
Q(lambda)=q_0+q_1 lambda+...+q_D lambda^D,
```

after dividing by the first nonzero power of `lambda` if necessary, its
coefficients satisfy the deeper endpoint ladder

```text
G_v^(r) q_0 = 0,
G_v^(r) q_i - G_u^(r) q_{i-1} = 0        for 1<=i<=D,
G_u^(r) q_D = 0.                                      (FrontierLadder_r)
```

Thus a consecutive fixed-kernel frontier stack has the same finite exceptional
slope cost `c-b` as the three-shift case.  Iterating the frontier does not
introduce a new multiplicative slope loss; the only persistent alternative is
again a deeper endpoint-rank failure plus an explicit moving-kernel ladder.

### Proof

By Corollary 38.1, the consecutive fixed-kernel stack is exactly the single
deeper pencil `G_lambda^(r)=G_v^(r)-lambda G_u^(r)`.  The condition
`g_lambda^(r)>b` is equivalent to `rank G_lambda^(r)<c-b`, hence to the
vanishing of all `(c-b) x (c-b)` minors of this matrix.  Each such minor is a
polynomial in `lambda` of degree at most `c-b`.

If one minor is nonzero, it has at most `c-b` roots, giving the finite
alternative.  If all these minors vanish identically, then the constant and
top-degree coefficients of each minor show that all `(c-b) x (c-b)` minors of
both `G_v^(r)` and `G_u^(r)` vanish.  Therefore both endpoint maps have kernel
dimension greater than `b`.

Over `F(lambda)`, persistent vanishing of all `(c-b) x (c-b)` minors means
`dim ker G_lambda^(r)>=b+1`.  Clearing denominators gives moving kernels.
Substituting `Q(lambda)=sum_i q_i lambda^i` into

```text
(G_v^(r)-lambda G_u^(r))Q(lambda)=0
```

and comparing powers of `lambda` gives (FrontierLadder_r), after the same
initial-power division used in Corollary 37.

## Corollary 39: Three-Shift Common-Image Lines Are Shift-Persistent Or Endpoint

Keep `c=m-1` and assume `t>=2`.  For a nonzero image vector `y in F^t`, define
the sliding-persistence subspace

```text
W_y={ z in F^{t+2} :
        (z_i,z_{i+1},...,z_{i+t-1}) in F y for i=0,1,2 }.
```

Then `dim W_y<=1`.  Moreover `W_y` is nonzero only for the extended geometric
shift lines

```text
[y]=[1:theta:theta^2:...:theta^(t-1)]        with theta in F,
```

or for the point at infinity

```text
[y]=[0:0:...:0:1].
```

For these `q+1` projective lines over `F_q`, the space `W_y` is one-dimensional.
For every other projective image line, `W_y=0`.

Let

```text
Z_w(Q)=H_{t+2,c-1}(w)Q in F^{t+2}.
```

For the three-shift common-image direction map `C_y^G` from Corollary 37,

```text
ker C_y^G
 = { Q : Z_u(Q) in W_y and Z_v(Q) in W_y }.          (GCIShift)
```

Consequently, for every image line off the extended geometric shift curve,

```text
ker C_y^G
 = ker H_{t+2,c-1}(u) cap ker H_{t+2,c-1}(v).        (GCIOff)
```

Thus the non-shift-persistent part of the three-shift common-image ledger is
not an independent projective low-rank obstruction.  After the deeper endpoint
intersection has been charged, the only common-image lines that still need a
separate three-shift charge are the `q+1` extended geometric shift lines.

### Proof

The condition `z in W_y` means that there are scalars `a_0,a_1,a_2` such that

```text
(z_i,z_{i+1},...,z_{i+t-1})=a_i y,        i=0,1,2.
```

Writing `y=(y_0,...,y_{t-1})`, the overlaps of consecutive windows give

```text
a_0 y_s = a_1 y_{s-1},
a_1 y_s = a_2 y_{s-1},        1<=s<=t-1.             (Overlap)
```

Since `y` is nonzero and `t>=2`, some adjacent pair `(y_{s-1},y_s)` is nonzero.
For this `s`, the two linear equations in (Overlap) are independent equations
on `(a_0,a_1,a_2)`.  Hence the solution space for the scalars has dimension at
most one, and therefore `dim W_y<=1`.

Assume now that `W_y` is nonzero, and choose a nonzero scalar triple
`(a_0,a_1,a_2)` satisfying (Overlap).  If `a_0!=0` and `a_1=0`, then (Overlap)
forces `y_1=...=y_{t-1}=0`, so `[y]=[1:0:...:0]`, the case `theta=0`.  If
`a_0!=0` and `a_1!=0`, then (Overlap) gives

```text
y_s = theta y_{s-1},        theta=a_1/a_0,
```

for every `s`.  Since `y` is nonzero, this gives
`[y]=[1:theta:theta^2:...:theta^(t-1)]`; the second equation in (Overlap) then
forces `a_2/a_1=theta`.

It remains to consider `a_0=0`.  If `a_1!=0`, the first equation in (Overlap)
forces `y_0=...=y_{t-2}=0`, while the second forces also `y_{t-1}=0`, a
contradiction.  Thus `a_1=0`.  Since the triple is nonzero, `a_2!=0`, and the
second equation in (Overlap) gives `y_0=...=y_{t-2}=0`; hence
`[y]=[0:...:0:1]`.

Conversely, if `[y]=[1:theta:...:theta^(t-1)]`, then

```text
z=(1,theta,theta^2,...,theta^(t+1))
```

spans a nonzero `W_y` (with the evident interpretation at `theta=0`).  If
`[y]=[0:...:0:1]`, then `z=(0,...,0,1) in F^{t+2}` spans a nonzero `W_y`.
Together with the dimension bound, these cases have `dim W_y=1`.

Finally, the `i`-th length-`t` window of `Z_w(Q)=H_{t+2,c-1}(w)Q` is exactly
`H_{t,j}(w)X^iQ`.  Therefore `y wedge H_{t,j}(w)X^iQ=0` for
`w in {u,v}` and `i=0,1,2` is equivalent to
`Z_u(Q),Z_v(Q) in W_y`, proving (GCIShift).  If `[y]` is off the extended
geometric shift curve then `W_y=0`, giving (GCIOff).

## Corollary 40: Shift-Persistent Lines Are First-Difference Endpoint Ledgers

Keep the notation of Corollary 39.  For `theta in F`, define the first
difference of a syndrome vector by

```text
(Delta_theta w)_a = w_{a+1}-theta w_a.
```

Let

```text
y_theta=(1,theta,theta^2,...,theta^(t-1)) in F^t.
```

Then the finite shift-persistent common-image line satisfies

```text
ker C_[y_theta]^G
 = ker H_{t+1,c-1}(Delta_theta u)
   cap ker H_{t+1,c-1}(Delta_theta v).              (ShiftFinite)
```

For the point at infinity `y_infty=(0,...,0,1)`, one has

```text
ker C_[y_infty]^G
 = ker H_{t+1,c-1}(u) cap ker H_{t+1,c-1}(v).       (ShiftInfinity)
```

Consequently the `q+1` shift-persistent common-image lines from Corollary 39
are not new projective image-line ledgers.  They are ordinary endpoint
intersection ledgers for the `q` first-difference syndrome pairs
`(Delta_theta u,Delta_theta v)`, together with the infinity endpoint pair
`(u,v)`.

In particular, after charging the high-dimensional spaces in (ShiftFinite) and
(ShiftInfinity), the shift-persistent common-image part contributes at most

```text
(q+1) binom(n,b)
```

split cores at threshold `b`, with the same root-free `b/c` replacement after
common-root global core pieces have been charged.

### Proof

Let `Z_w(Q)=H_{t+2,c-1}(w)Q`.  For finite `theta`, Corollary 39 says that
`Q in ker C_[y_theta]^G` exactly when `Z_u(Q)` and `Z_v(Q)` lie in the
one-dimensional span of

```text
(1,theta,theta^2,...,theta^(t+1)).
```

A vector `z in F^{t+2}` lies in this span if and only if

```text
z_{a+1}-theta z_a=0,        0<=a<=t.
```

For `w in {u,v}`, the left side is

```text
sum_{h=0}^{c-1} (w_{a+1+h}-theta w_{a+h}) q_h,
```

which is the `a`-th row of `H_{t+1,c-1}(Delta_theta w)Q`.  Applying this to
both `u` and `v` proves (ShiftFinite).

For `y_infty`, Corollary 39 identifies `W_y` with the span of the last basis
vector in `F^{t+2}`.  Thus `Z_w(Q) in W_y` if and only if

```text
(Z_w(Q))_0=...=(Z_w(Q))_t=0,
```

which is exactly `H_{t+1,c-1}(w)Q=0`.  This proves (ShiftInfinity).  The
bounded-rank count then follows by summing the `q+1` endpoint-intersection
ledgers, and the root-free replacement is the same common-root slice argument
used in Corollary 30.1 and Corollary 36.

## Corollary 40.1: Consecutive Common-Image Stacks Are Endpoint-Only

Let `r>=1`, keep `t>=2`, and let `Q` range over degree-`<c` directions.  For a
nonzero image vector `y in F^t`, define

```text
W_y^(r)={ z in F^{t+r} :
          (z_i,z_{i+1},...,z_{i+t-1}) in F y for 0<=i<=r }.
```

Then `dim W_y^(r)<=1`.  Moreover `W_y^(r)` is nonzero only for the extended
geometric shift lines

```text
[y]=[1:theta:theta^2:...:theta^(t-1)]        with theta in F,
```

or for the point at infinity

```text
[y]=[0:0:...:0:1].
```

For these `q+1` projective lines over `F_q`, the space `W_y^(r)` is
one-dimensional.

Let

```text
Z_w^(r)(Q)=H_{t+r,c-1}(w)Q in F^{t+r}.
```

The consecutive common-image stack

```text
y wedge H_{t,c+r-1}(u)X^iQ = 0,
y wedge H_{t,c+r-1}(v)X^iQ = 0,        0<=i<=r,
```

is equivalent to

```text
Z_u^(r)(Q) in W_y^(r),        Z_v^(r)(Q) in W_y^(r).       (CI_r)
```

Consequently, for every image line off the extended geometric shift curve,
the consecutive common-image stack is just the deeper endpoint intersection

```text
ker H_{t+r,c-1}(u) cap ker H_{t+r,c-1}(v).
```

For a finite shift-persistent line `y_theta=(1,theta,...,theta^(t-1))`,

```text
ker C_[y_theta]^(r)
 = ker H_{t+r-1,c-1}(Delta_theta u)
   cap ker H_{t+r-1,c-1}(Delta_theta v).            (ShiftFinite_r)
```

For the point at infinity,

```text
ker C_[y_infty]^(r)
 = ker H_{t+r-1,c-1}(u)
   cap ker H_{t+r-1,c-1}(v).                        (ShiftInfinity_r)
```

Thus a consecutive common-image frontier stack never creates a fresh
projective image-line family.  After the deeper endpoint intersection is
charged, only the `q` first-difference endpoint ledgers and the infinity
endpoint ledger remain, exactly as in the three-shift case.

### Proof

The first two consecutive windows of any `z in W_y^(r)` satisfy the overlap
equations

```text
a_0 y_s = a_1 y_{s-1},        1<=s<=t-1,
```

for scalars `a_0,a_1`.  These are the same equations used in Corollary 39, and
already imply `dim W_y^(r)<=1` and the displayed list of possible projective
lines.  The geometric vector

```text
(1,theta,theta^2,...,theta^(t+r-1))
```

spans `W_y^(r)` for finite `theta`, and the last basis vector in `F^{t+r}`
spans the infinity case.

By Corollary 38.1, the `i`-th length-`t` window of `Z_w^(r)(Q)` is exactly
`H_{t,c+r-1}(w)X^iQ`.  Therefore the common-image equations for all
`0<=i<=r` are equivalent to `Z_u^(r)(Q),Z_v^(r)(Q) in W_y^(r)`, proving
(CI_r).  Off the shift curve `W_y^(r)=0`, giving the deeper endpoint
intersection.

For finite `theta`, a vector `z in F^{t+r}` lies in the span of
`(1,theta,...,theta^(t+r-1))` if and only if

```text
z_{a+1}-theta z_a=0,        0<=a<=t+r-2.
```

Applied to `z=Z_w^(r)(Q)`, these are exactly the rows of
`H_{t+r-1,c-1}(Delta_theta w)Q`.  Applying this for `w=u` and `w=v` gives
(ShiftFinite_r).  The infinity case says that the first `t+r-1` entries of
`Z_w^(r)(Q)` vanish, which is exactly `H_{t+r-1,c-1}(w)Q=0`.

## Corollary 40.2: Consecutive First-Difference Charges Have No Extra Parameter Loss

Keep `0<=b<c` and let `r>=1`.  Let `S` denote the syndrome shift
`(S w)_a=w_{a+1}`.  Define the two stacked endpoint maps on degree-`<c`
directions by

```text
B^(r)(Q)=(H_{t+r-1,c-1}(u)Q, H_{t+r-1,c-1}(v)Q),
A^(r)(Q)=(H_{t+r-1,c-1}(S u)Q, H_{t+r-1,c-1}(S v)Q).
```

For `theta in F`, put

```text
J_theta^(r)=A^(r)-theta B^(r),
```

equivalently

```text
J_theta^(r)(Q)=
  (H_{t+r-1,c-1}(Delta_theta u)Q,
   H_{t+r-1,c-1}(Delta_theta v)Q).
```

Write

```text
d_theta^(r)=dim ker J_theta^(r).
```

The bad first-difference parameter set

```text
Theta_{r,>b}={ theta in F : d_theta^(r)>b }
```

has the following dichotomy.

```text
finite first-difference alternative:
  |Theta_{r,>b}| <= c-b;

persistent first-difference alternative:
  d_theta^(r)>b for every theta.
```

More precisely, if some `(c-b) x (c-b)` minor of `J_theta^(r)` is not the zero
polynomial in `theta`, the finite alternative holds.  If every such minor
vanishes identically, then both stacked endpoint maps have direction dimension
`>b`:

```text
dim ker A^(r)>b,        dim ker B^(r)>b.
```

In the persistent case there are `b+1` independent moving first-difference
kernels over `F(theta)`.  For a single nonzero moving kernel

```text
Q(theta)=q_0+q_1 theta+...+q_D theta^D,
```

after dividing by the first nonzero power of `theta` if necessary, its
coefficients satisfy

```text
A^(r) q_0 = 0,
A^(r) q_i - B^(r) q_{i-1} = 0        for 1<=i<=D,
B^(r) q_D = 0.                                      (DiffLadder_r)
```

Thus the finite shift-persistent common-image ledgers from Corollary 40.1
also have no multiplicative parameter loss under consecutive frontier descent:
at each depth the finite exceptional `theta` cost is at most `c-b`, unless the
deeper ordinary and shifted endpoint intersections are themselves high
dimensional.

### Proof

The affine form `J_theta^(r)=A^(r)-theta B^(r)` follows directly from

```text
Delta_theta w = S w - theta w.
```

The condition `d_theta^(r)>b` is equivalent to `rank J_theta^(r)<c-b`, hence
to the vanishing of all `(c-b) x (c-b)` minors.  Each minor is a polynomial in
`theta` of degree at most `c-b`.

If one minor is nonzero, it has at most `c-b` roots.  If all such minors vanish
identically, then the constant and top-degree coefficients imply that all
`(c-b) x (c-b)` minors of both `A^(r)` and `B^(r)` vanish.  Hence both stacked
endpoint maps have kernel dimension greater than `b`.

The moving-kernel and coefficient-ladder statements are the same
rank-nullity-over-`F(theta)` argument as in Corollary 38.2, applied to
`A^(r)-theta B^(r)`.

## Corollary 40.3: Consecutive Frontier Closure Has Additive Parameter Cost

Keep `0<=b<c` and let `r>=1`.  Assume the four consecutive frontier endpoint
checks

```text
dim ker H_{t+r,c-1}(u) <= b,
dim ker H_{t+r,c-1}(v) <= b,
dim ker B^(r) <= b,
dim ker A^(r) <= b,                                  (FrontGood_r)
```

where `A^(r)` and `B^(r)` are the stacked shifted and ordinary endpoint maps
from Corollary 40.2.

Then the consecutive frontier ledgers have the following closure.

1. The high-dimensional fixed-kernel slope set satisfies

```text
|E_{r,>b}| <= c-b.
```

2. The high-dimensional first-difference parameter set satisfies

```text
|Theta_{r,>b}| <= c-b.
```

3. The common-image stack from Corollary 40.1 has no projective image-line
multiplier.  Off the `q+1` extended geometric shift lines, it is contained in

```text
ker H_{t+r,c-1}(u) cap ker H_{t+r,c-1}(v),
```

which has direction dimension at most `b`.  The infinity shift line is the
ordinary endpoint stack `ker B^(r)`, also of dimension at most `b`.  A finite
shift line `theta` has direction dimension at most `b` unless
`theta in Theta_{r,>b}`.

Consequently, after charging at most

```text
2(c-b)
```

finite parameter systems, namely `E_{r,>b}` and `Theta_{r,>b}`, every
uncharged finite fixed-kernel and consecutive common-image frontier ledger has
direction dimension at most `b`.  The charge is additive at the frontier
depth: it does not acquire a factor depending on the number of consecutive
shifts `r`, nor a factor from the projective image-line space.

### Proof

The first two estimates are Corollaries 38.2 and 40.2, because (FrontGood_r)
rules out the persistent alternatives in both dichotomies.

For the common-image stack, Corollary 40.1 says that every image line off the
extended geometric shift curve gives exactly the deeper endpoint intersection.
This intersection has dimension at most `b` because it is contained in each of
`ker H_{t+r,c-1}(u)` and `ker H_{t+r,c-1}(v)`.  The infinity line gives
`ker B^(r)`, which has dimension at most `b` by (FrontGood_r).  A finite shift
line gives `ker J_theta^(r)`, so it is high-dimensional only when
`theta in Theta_{r,>b}`.  Removing the two finite bad-parameter sets leaves
only direction spaces of dimension at most `b`.

## Corollary 40.4: Four Short Frontier Checks Close The Consecutive Ledger

Keep `h=c-b` and `r>=1`.  Define the short stacked endpoint maps

```text
B_h^(r)(Q)=(H_{t+r-1,h-1}(u)Q, H_{t+r-1,h-1}(v)Q),
A_h^(r)(Q)=(H_{t+r-1,h-1}(S u)Q, H_{t+r-1,h-1}(S v)Q),
```

on degree-`<h` directions.  Assume the four short frontier checks are
injective:

```text
ker H_{t+r,h-1}(u)=0,
ker H_{t+r,h-1}(v)=0,
ker B_h^(r)=0,
ker A_h^(r)=0.                                      (ShortFront_r)
```

Then the endpoint hypotheses (FrontGood_r) from Corollary 40.3 hold.  Hence
the consecutive frontier ledger closes after charging at most

```text
2h
```

finite parameter systems: at most `h` fixed-kernel slopes and at most `h`
first-difference parameters.  All remaining finite fixed-kernel and
consecutive common-image frontier ledgers have direction dimension at most
`b`, with no `r`-dependent multiplier and no projective image-line multiplier.

The short checks are dimensionally feasible only if

```text
h<=t+r             for the two single endpoint checks,
h<=2(t+r-1)        for the two stacked endpoint checks.
```

Outside these row-count ranges the corresponding short injectivity check is
impossible, so this particular closure route must be replaced by an endpoint
or short-annihilator charge.

### Proof

It is enough to show that (ShortFront_r) implies (FrontGood_r).  Consider the
single endpoint map `H_{t+r,c-1}(u):F^c -> F^{t+r}`.  If its kernel had
dimension greater than `b`, then it would meet the coordinate subspace of
degree-`<h` directions nontrivially, since

```text
dim ker H_{t+r,c-1}(u) + h > b + (c-b) = c.
```

That nonzero intersection vector would lie in `ker H_{t+r,h-1}(u)`,
contradicting (ShortFront_r).  Hence
`dim ker H_{t+r,c-1}(u)<=b`.  The same argument applies to `v`.

For the stacked maps, replace the endpoint map above by
`B^(r):F^c -> F^{2(t+r-1)}` and `A^(r):F^c -> F^{2(t+r-1)}`.  A
kernel of dimension greater than `b` would again meet degree-`<h` directions
nontrivially, contradicting injectivity of `B_h^(r)` or `A_h^(r)`.
Thus (FrontGood_r) holds.  Corollary 40.3 then gives the closure and the
`2(c-b)=2h` finite-parameter charge.

The row-count constraints are the necessary conditions for injectivity of maps
from an `h`-dimensional domain to the displayed codomains.

## Corollary 40.5: Finite Frontier Ladders Charge Additively

Keep `h=c-b`, and let `R` be a finite set of positive consecutive-frontier
depths.  Assume that the four short frontier checks (ShortFront_r) from
Corollary 40.4 hold for every `r in R`.

For each `r in R`, let `E_{r,>b}` be the high-dimensional fixed-kernel slope
set from Corollary 38.2, and let `Theta_{r,>b}` be the high-dimensional
first-difference parameter set from Corollary 40.2.  Form the depth-indexed
bad-system ledger

```text
Bad_R =
  { (r,lambda) : r in R, lambda in E_{r,>b} }
  union
  { (r,theta) : r in R, theta in Theta_{r,>b} }.
```

Then

```text
|Bad_R| <= 2h |R|.                                  (LadderAdd)
```

After charging the systems indexed by `Bad_R`, every uncharged finite
fixed-kernel frontier ledger and every uncharged consecutive common-image
frontier ledger at every depth `r in R` has direction dimension at most `b`.
Thus a finite consecutive-frontier ladder has additive parameter cost

```text
sum_{r in R} 2h,
```

not a multiplicative loss over rungs.  In particular, for a contiguous ladder
`R={1,2,...,L}`, the cost is at most `2hL` finite parameter systems, with no
projective image-line multiplier at any rung.

### Proof

For each fixed `r in R`, Corollary 40.4 gives

```text
|E_{r,>b}| <= h,        |Theta_{r,>b}| <= h,
```

and says that, after charging those systems, all remaining finite
fixed-kernel and consecutive common-image frontier ledgers at that depth have
direction dimension at most `b`.  Summing these depthwise estimates over the
finite set `R` gives (LadderAdd).  The ledger is indexed by `(depth,parameter)`
because the same field element can label different linear systems at different
frontier depths; counting depth-indexed systems is the conservative charge.

## Corollary 40.6: Short Frontier Failures Are Denominator Recurrences

Keep `h=c-b` and `r>=1`.  Failure of one of the four short frontier checks
(ShortFront_r) from Corollary 40.4 is exactly one of the following short
annihilator alternatives.

```text
Endpoint-u:
  exists 0!=Q, deg Q<h, with H_{t+r,h-1}(u)Q=0;

Endpoint-v:
  exists 0!=Q, deg Q<h, with H_{t+r,h-1}(v)Q=0;

Ordinary stacked endpoint:
  exists 0!=Q, deg Q<h, with
  H_{t+r-1,h-1}(u)Q=0 and H_{t+r-1,h-1}(v)Q=0;

Shifted stacked endpoint:
  exists 0!=Q, deg Q<h, with
  H_{t+r-1,h-1}(S u)Q=0 and H_{t+r-1,h-1}(S v)Q=0.
```

Each alternative is a denominator recurrence.  If

```text
Q(X)=q_0+...+q_eX^e,        D(T)=Q^*(T)=q_e+...+q_0T^e,
```

then `H_{s,h-1}(w)Q=0` is equivalent to

```text
D(T)W_w(T) = N(T)       mod T^{e+s},        deg N<e.
```

For the two stacked alternatives this congruence holds componentwise for the
two displayed syndrome series.

Moreover, domain-root factors strip losslessly.  If `Q=L_A R` with
`|A|=a<h`, then the four alternatives become the corresponding lower-order
recurrences

```text
Endpoint-u:
  H_{t+r,h-a-1}(Delta_A u)R=0;

Endpoint-v:
  H_{t+r,h-a-1}(Delta_A v)R=0;

Ordinary stacked endpoint:
  H_{t+r-1,h-a-1}(Delta_A u)R=0 and
  H_{t+r-1,h-a-1}(Delta_A v)R=0;

Shifted stacked endpoint:
  H_{t+r-1,h-a-1}(S Delta_A u)R=0 and
  H_{t+r-1,h-a-1}(S Delta_A v)R=0.
```

Thus a short frontier failure splits into fixed-root/root-slice charges plus a
root-free short denominator-recurrence obstruction for `u`, for `v`, for
`(u,v)`, or for the shifted pair `(S u,S v)`.

### Proof

The four alternatives are just the negations of the four injectivity checks in
(ShortFront_r).  Corollary 56 gives the denominator-recurrence congruence for
each scalar Hankel equation, and the stacked cases are the componentwise
application to the two displayed series.

The stripping statement is Corollary 49 with the appropriate window length
`s`.  For the shifted stacked case, use the identity

```text
Delta_alpha(S w)=S(Delta_alpha w),
```

and iterate over the multiset `A`.

## Corollary 40.7: Root-Free Recurrences Are The Only Short-Frontier Residual

Let `D subset F` be the evaluation domain, keep `h=c-b`, and let `R` be a
finite set of positive consecutive-frontier depths.  For `r in R`, call a
short frontier recurrence root-free if its witness `Q` has no root in `D`.

After charging all short frontier failures whose witnesses have a domain-root
factor, every uncharged failure of a short frontier check at a depth `r in R`
is one of the following root-free recurrence families:

```text
H_{t+r,h-1}(u)Q=0,
H_{t+r,h-1}(v)Q=0,

H_{t+r-1,h-1}(u)Q=H_{t+r-1,h-1}(v)Q=0,

H_{t+r-1,h-1}(S u)Q=H_{t+r-1,h-1}(S v)Q=0,
```

with `0!=Q`, `deg Q<h`, and `Q(alpha)!=0` for every `alpha in D`.

Consequently, for a finite frontier ladder, the route to Corollary 40.5 is
exactly:

1. charge fixed-root/root-slice short recurrence pieces using Corollary 40.6;
2. rule out, bound, or charge the four root-free recurrence families above at
   each depth `r in R`;
3. apply the additive depth-indexed parameter charge from Corollary 40.5 to
   the remaining finite fixed-kernel and consecutive common-image ledgers.

Thus the uncharged short-frontier obstruction is a root-free denominator
recurrence problem, not a new frontier-rank object.

### Proof

Corollary 40.6 says every failure of a short frontier check is a denominator
recurrence, and that every domain-root factor strips losslessly to a
fixed-root/root-slice recurrence at lower order.  Iterating the stripping until
no domain root remains leaves exactly one of the four displayed root-free
recurrence families, unless the original failure has already been fully
charged to fixed-root/root-slice ledgers.  Once those root-free residuals are
absent or charged at every depth in `R`, there is no uncharged short-frontier
failure left, so the additive closure of Corollary 40.5 applies to the
remaining ledgers.

## Corollary 40.8: Half-Window Frontier Residuals Have Primitive Denominators

Fix a frontier depth `r>=1` and assume

```text
h<=t+r.                                             (FrontHalf_r)
```

Then every root-free short-frontier residual from Corollary 40.7 is in the
half-window Pade range.

More explicitly, for each scalar residual family `u` or `v`, all root-free
degree-`<h` certificates for that family determine one reduced rational
function.  Its primitive denominator is reciprocal-domain-pole-free and divides
every certificate denominator.

For each paired residual family `(u,v)` or `(S u,S v)`, all root-free common
degree-`<h` certificates determine one reduced vector rational function.  Its
primitive vector denominator is reciprocal-domain-pole-free and divides every
common certificate denominator.

If the primitive denominator has degree `delta`, then every certificate
denominator in the same family lies in the explicit multiplier ledger

```text
D(T)=D_0(T)M(T),        deg M<=h-1-delta.
```

The primitive denominator itself remains a valid root-free certificate after
the multiplier is cancelled.  Thus, in the half-window frontier range, the
root-free short-frontier residual at depth `r` is a primitive
reciprocal-domain-pole-free denominator target for one of four objects:

```text
u,        v,        (u,v),        (S u,S v).
```

For a finite ladder `R`, the same conclusion holds simultaneously at all
depths satisfying `h<=t+r`.

### Proof

For the scalar endpoint residuals, the Hankel window length is `s=t+r`.  For
the ordinary and shifted paired residuals, the window length is `s=t+r-1`.
Since every certificate has degree `e<h`, the hypothesis `h<=t+r` gives

```text
e<=h-1<=t+r-1,
```

so all four residual families are in the half-window range `e<=s`.

Corollary 57 rewrites each recurrence as a truncated rational-denominator
certificate.  Corollary 58 identifies root-freeness with the absence of
reciprocal-domain denominator poles.  Corollary 59 gives the common reduced
scalar or vector rational function and its primitive denominator in the
half-window range.  Corollaries 60 and 61 give the multiplier ledger and show
that cancelling a multiplier leaves the primitive denominator as a valid
certificate.  These arguments are applied independently at each depth `r`.

## Corollary 40.9: Nested Frontier Ladders Charge At The Bottom Rung

Let `R` be a nonempty finite set of positive consecutive-frontier depths, and
put

```text
r_0=min R.
```

Assume the four short frontier checks (ShortFront_r) hold at `r=r_0`.  Then
they hold at every depth `r in R`.  Moreover the high-dimensional finite
parameter sets are nested:

```text
E_{r,>b} subset E_{r_0,>b},
Theta_{r,>b} subset Theta_{r_0,>b},        r in R.  (NestedBad)
```

Consequently, after charging only the bottom-rung finite parameter systems

```text
E_{r_0,>b} union Theta_{r_0,>b},
```

all uncharged finite fixed-kernel and consecutive common-image frontier
ledgers at every depth `r in R` have direction dimension at most `b`.  Under
the bottom short checks this costs at most

```text
2h
```

parameter values, not `2h|R|`.  Thus a nested consecutive frontier ladder
does not merely avoid multiplicative loss; its finite parameter charge is
paid at the bottom rung.

### Proof

For any syndrome vector `w`, the rows of `H_{t+r_0,h-1}(w)` are a subset of
the rows of `H_{t+r,h-1}(w)` whenever `r>=r_0`.  Hence injectivity at `r_0`
implies injectivity at `r`.  The same row-containment applies to the stacked
maps `B_h^(r)` and `A_h^(r)`.  Therefore (ShortFront_r) holds for all
`r in R`.

The same row-containment gives kernel inclusions

```text
ker G_lambda^(r) subset ker G_lambda^(r_0),
ker J_theta^(r)  subset ker J_theta^(r_0),
```

for every `r>=r_0`.  If the left-hand kernel has dimension greater than `b`,
then so does the right-hand kernel, proving (NestedBad).  Corollary 40.4 gives
`|E_{r_0,>b}|<=h` and `|Theta_{r_0,>b}|<=h`.  After those bottom-rung parameter
values are charged, the inclusions show that no deeper high-dimensional finite
parameter system remains.  The common-image ledgers at each depth are then
closed by Corollary 40.3.

## Corollary 40.10: Root-Free Residual Ladders Charge At The Bottom Rung

Let `D subset F` be the evaluation domain, let `R` be a nonempty finite set of
positive consecutive-frontier depths, and put `r_0=min R`.  For a depth `r`,
let `RF_r(u)`, `RF_r(v)`, `RF_r(u,v)`, and `RF_r(Su,Sv)` denote the four
root-free recurrence witness sets from Corollary 40.7.

Then the residual witness sets are nested:

```text
RF_r(u)       subset RF_{r_0}(u),
RF_r(v)       subset RF_{r_0}(v),
RF_r(u,v)     subset RF_{r_0}(u,v),
RF_r(Su,Sv)   subset RF_{r_0}(Su,Sv),        r in R.   (NestedRF)
```

Consequently, after fixed-root/root-slice recurrence pieces are charged, it is
enough to rule out, bound, or charge the four root-free recurrence families at
the bottom depth `r_0`.  Once those bottom residuals are absent or charged,
there is no uncharged root-free short-frontier residual at any deeper
`r in R`.

If in addition `h<=t+r_0`, then all bottom residual families are in the
half-window range of Corollary 40.8.  Thus the primitive
reciprocal-domain-pole-free denominator targets at the bottom depth control
the whole ladder.

### Proof

For any syndrome vector `w`, the row set of `H_{t+r_0,h-1}(w)` is contained in
the row set of `H_{t+r,h-1}(w)` when `r>=r_0`.  Hence every witness in
`RF_r(u)` or `RF_r(v)` is also a witness in the corresponding bottom set.

For the paired ordinary residuals, the row set of `H_{t+r_0-1,h-1}(w)` is
contained in that of `H_{t+r-1,h-1}(w)` for `w=u,v`.  This gives
`RF_r(u,v) subset RF_{r_0}(u,v)`.  The shifted pair is identical with
`w=Su,Sv`.  Root-freeness is a property of the same witness polynomial `Q`,
so it is preserved under these inclusions.

The final statement follows from Corollary 40.8 applied at `r_0`.  Since every
deeper root-free residual witness already lies in the bottom witness set,
charging the bottom primitive denominator targets charges the whole ladder.

## Corollary 40.11: Bottom Residual Charges Close A Finite Frontier Ladder

Let `R` be a nonempty finite set of positive consecutive-frontier depths and
put `r_0=min R`.  Work after the fixed-root/root-slice short recurrence pieces
from Corollary 40.6 have been charged.  Charge also the four bottom root-free
recurrence families

```text
RF_{r_0}(u),        RF_{r_0}(v),
RF_{r_0}(u,v),      RF_{r_0}(Su,Sv).
```

Then there are no uncharged failures of the four short frontier checks at any
depth `r in R`.  Hence the remaining finite fixed-kernel and consecutive
common-image frontier ledgers at all depths in `R` close after charging only
the bottom finite parameter sets

```text
E_{r_0,>b} union Theta_{r_0,>b},
```

which have total size at most `2h` on the uncharged ledger.

If `h<=t+r_0`, the four bottom root-free recurrence charges may equivalently
be recorded as the four bottom primitive reciprocal-domain-pole-free
denominator targets from Corollary 40.8, together with their certificate
multiplier ledgers when witnesses rather than parameter systems are counted.

Thus a finite nested frontier ladder is reduced to explicit bottom-rung
obligations:

1. fixed-root/root-slice short recurrence charges;
2. four bottom root-free primitive denominator targets;
3. at most `2h` bottom finite parameter systems.

No further `|R|` factor, projective image-line factor, or per-rung multiplier
is introduced by the consecutive frontier descent.

### Proof

After fixed-root/root-slice recurrence pieces are charged, Corollary 40.7 says
that every remaining short-frontier failure is root-free.  Corollary 40.10
says every deeper root-free residual witness lies in the corresponding bottom
family.  Therefore charging the four bottom root-free recurrence families
removes all uncharged short-frontier failures at every depth in `R`.

On the remaining ledger, the four short frontier checks hold at `r_0`, and
therefore at every deeper `r in R` by Corollary 40.9.  The same corollary
says that the deeper bad finite parameter sets are contained in the bottom
ones.  Corollary 40.4 gives the bottom bound
`|E_{r_0,>b}|+|Theta_{r_0,>b}|<=2h`, and Corollary 40.3 closes the uncharged
finite fixed-kernel and consecutive common-image frontier ledgers at each
depth.  The half-window reformulation is Corollary 40.8 at `r_0`.

## Corollary 40.12: Paired Residual Overlap Is Endpoint-Pair Residual

Fix a frontier depth `r>=1`, put `s=t+r-1`, and write
`H_m(w)=H_{m,h-1}(w)` in this corollary.  For every degree-`<h` polynomial
`Q`,

```text
H_s(u)Q=H_s(v)Q=0
and
H_s(S u)Q=H_s(S v)Q=0
```

if and only if

```text
H_{s+1}(u)Q=H_{s+1}(v)Q=0.                          (PairOverlap)
```

Equivalently, at depth `r`,

```text
RF_r(u,v) cap RF_r(Su,Sv) = RF_r(u) cap RF_r(v)
```

as root-free witness sets.

Consequently, after the endpoint-pair residual

```text
RF_r(u) cap RF_r(v)
```

has been charged, the ordinary paired residual target `(u,v)` and the shifted
paired residual target `(S u,S v)` have no common root-free witness.  In the
half-window range, if the same primitive denominator occurs in both paired
primitive denominator targets, then that primitive denominator is an
endpoint-pair residual denominator and belongs to the same endpoint-pair
charge.

### Proof

The first pair of equations gives the rows

```text
0,1,...,s-1
```

of the Hankel recurrences for both `u` and `v`.  The shifted pair gives the
rows

```text
1,2,...,s
```

because `H_s(S w)Q` is the recurrence row of `w` shifted forward by one.
Together these two row intervals are exactly

```text
0,1,...,s,
```

which is `H_{s+1}(w)Q=0` for `w=u,v`.  The converse is immediate by taking the
first `s` rows and the last `s` rows.  Root-freeness is a property of the same
witness `Q`, giving the root-free identity.

For primitive denominators in the half-window range, Corollary 61 says that
the primitive denominator remains a certificate after cancelling multipliers.
Thus a primitive denominator common to both paired targets gives a common
root-free witness for the ordinary and shifted pairs, hence an endpoint-pair
residual by (PairOverlap).

## Corollary 40.13: Consecutive Paired Residual Stacks Collapse To The Deepest Pair

Fix `r>=1` and `L>=0`, put `s=t+r-1`, and let `S` denote the syndrome shift.
For `i>=0`, define `RF_{r,i}(u,v)` to be the root-free degree-`<h` witness set
cut out by

```text
H_s(S^i u)Q=H_s(S^i v)Q=0.
```

Then

```text
cap_{i=0}^L RF_{r,i}(u,v) = RF_{r+L,0}(u,v).        (PairStack)
```

The right-hand side is interpreted at depth `r+L`, with window length
`t+(r+L)-1=s+L`.

Equivalently, for every degree-`<h` polynomial `Q`,

```text
H_s(S^i u)Q=H_s(S^i v)Q=0        for all 0<=i<=L
```

if and only if

```text
H_{s+L}(u)Q=H_{s+L}(v)Q=0.
```

Consequently, a consecutive block of shifted paired residuals has only one
common root-free obstruction: the deepest paired residual at depth `r+L`.
After that deepest paired residual is charged, the block has no common
uncharged root-free witness.  In the half-window range, any primitive
denominator common to all `L+1` shifted paired primitive-denominator targets
belongs to the deepest paired denominator charge.

For `L=1`, the identity says

```text
RF_{r,0}(u,v) cap RF_{r,1}(u,v) = RF_{r+1,0}(u,v),
```

which is Corollary 40.12, since `RF_{r+1,0}(u,v)=RF_r(u) cap RF_r(v)`.

### Proof

For a fixed shift `i`, the equations

```text
H_s(S^i w)Q=0
```

are exactly the recurrence rows

```text
i,i+1,...,i+s-1
```

of the unshifted syndrome `w`.  As `i` runs from `0` to `L`, these consecutive
row intervals cover exactly

```text
0,1,...,s+L-1.
```

Thus imposing the paired equations for every `0<=i<=L` is equivalent to
imposing

```text
H_{s+L}(u)Q=H_{s+L}(v)Q=0.
```

This is precisely the paired residual at depth `r+L`, because
`s+L=t+(r+L)-1`.  Root-freeness is again a property of the same witness `Q`.
The primitive-denominator statement follows from Corollary 61 as in
Corollary 40.12.

## Corollary 40.14: The Half-Window Tail Charges At Its First Half-Window Rung

Let `R` be a finite set of positive consecutive-frontier depths.  Put

```text
R_hw={ r in R : h<=t+r }.
```

Assume `R_hw` is nonempty, and let

```text
r_hw=min R_hw.
```

After the fixed-root/root-slice recurrence pieces from Corollary 40.6 have
been charged, every root-free short-frontier residual at a depth `r in R_hw`
is already a witness in one of the four root-free residual families at the
single cutoff depth `r_hw`:

```text
RF_r(u)       subset RF_{r_hw}(u),
RF_r(v)       subset RF_{r_hw}(v),
RF_r(u,v)     subset RF_{r_hw}(u,v),
RF_r(Su,Sv)   subset RF_{r_hw}(Su,Sv).              (HalfTail)
```

Consequently the whole half-window tail of the ladder is controlled by the
four primitive reciprocal-domain-pole-free denominator targets at `r_hw`.
There is no separate primitive-denominator target to charge at any deeper
depth `r in R_hw`.

Thus a finite ladder splits into two explicit parts:

1. the pre-half-window depths `r in R` with `h>t+r`, where the residual is a
   longer Pade or short-annihilator target not compressed by Corollary 40.8;
2. the half-window tail `R_hw`, where the primitive denominator charge is paid
   once at `r_hw`.

Within the half-window tail, the ordinary and shifted paired primitive targets
at the cutoff have the overlap described in Corollary 40.12, and any
consecutive shifted paired block in the tail has the deepest-pair overlap
described in Corollary 40.13.

### Proof

Apply Corollary 40.10 to the finite subset `R_hw`.  Its minimum depth is
`r_hw`, so row containment gives exactly the inclusions (HalfTail).  Since
`h<=t+r_hw`, Corollary 40.8 applies at `r_hw` and converts the four cutoff
root-free residual families into primitive reciprocal-domain-pole-free
denominator targets.  Every deeper tail witness lies in one of those cutoff
families, so no deeper primitive target is needed.

The depths outside `R_hw` are precisely those with `h>t+r`; Corollary 40.8
does not put them in the half-window range, so this corollary makes no
primitive-denominator claim for them.  The final overlap statements are
Corollaries 40.12 and 40.13 applied at the relevant cutoff or tail depth.

## Corollary 40.15: Mixed Ladders Close From Pre-Half Residuals And One Cutoff

Let `R` be a nonempty finite set of positive consecutive-frontier depths and
put

```text
r_0=min R,
R_pre={ r in R : h>t+r },
R_hw ={ r in R : h<=t+r }.
```

Work after fixed-root/root-slice short recurrence pieces have been charged.
Assume the following residual charges have also been made:

1. for every pre-half-window depth `r in R_pre`, the four root-free recurrence
   families from Corollary 40.7 at depth `r`;
2. if `R_hw` is nonempty, the four root-free recurrence families at
   `r_hw=min R_hw`, equivalently the four primitive
   reciprocal-domain-pole-free denominator targets at `r_hw`.

Then there are no uncharged failures of the four short frontier checks at any
depth `r in R`.  Consequently the remaining finite fixed-kernel and
consecutive common-image frontier ledgers at all depths in `R` close after
charging only the bottom finite parameter systems

```text
E_{r_0,>b} union Theta_{r_0,>b},
```

of total size at most `2h` on the remaining ledger.

Thus a mixed finite ladder has the explicit closure ledger

```text
fixed-root/root-slice pieces
+ pre-half-window longer-Pade residual families
+ four primitive denominator targets at the first half-window rung, if any
+ at most 2h bottom finite parameter systems.
```

There is no primitive-denominator charge at each half-window depth, no
`|R_hw|` multiplier, and no projective image-line multiplier in the
consecutive common-image part.

### Proof

After the fixed-root/root-slice pieces are charged, Corollary 40.7 says every
remaining short-frontier failure is one of the four root-free residual
families at its depth.  At depths in `R_pre`, those families are charged by
hypothesis.  At depths in `R_hw`, Corollary 40.14 puts every root-free
residual into one of the four cutoff families at `r_hw`, which are charged by
hypothesis.  Hence no uncharged short-frontier failure remains at any depth in
`R`.

In particular the four short checks hold on the remaining ledger at the bottom
depth `r_0`.  Corollary 40.9 then nests all deeper bad finite parameter
systems into the bottom systems `E_{r_0,>b}` and `Theta_{r_0,>b}`, and
Corollary 40.4 gives their total charge at most `2h` on that remaining
ledger.  Corollary 40.3 closes the uncharged finite fixed-kernel and
consecutive common-image ledgers after those bottom systems are charged.

## Corollary 40.16: Deeper Half-Window Primitive Denominators Refine The Cutoff

Keep the notation of Corollary 40.14, and fix one of the four residual
families

```text
u,        v,        (u,v),        (S u,S v).
```

Assume this family has a root-free half-window witness at the cutoff depth
`r_hw`, and let `D_hw(T)` be its primitive reduced denominator from
Corollary 40.8.  If the same family has a root-free witness at a deeper
half-window depth `r in R_hw`, and `D_r(T)` is the primitive reduced
denominator at that deeper depth, then

```text
D_hw(T) divides D_r(T).                             (TailDiv)
```

Moreover, writing

```text
D_r(T)=D_hw(T)M_r(T),
```

the multiplier satisfies

```text
deg M_r <= h-1-deg D_hw,
```

and has no reciprocal-domain zero whenever `D_r` is root-free.  Thus deeper
half-window primitive denominators do not introduce new primitive bases: they
lie inside the multiplier ledger attached to the cutoff primitive denominator
for the same residual family.

### Proof

By Corollary 40.10 applied to the half-window tail, every deeper witness in
the fixed family is also a cutoff-depth witness for that family.  Corollary 61
applied at the deeper depth says that the deeper primitive denominator `D_r`
itself is a valid root-free certificate at depth `r`.  Therefore `D_r` is also
a valid certificate at the cutoff depth `r_hw`.

At the cutoff depth, Corollary 59 gives a single reduced scalar or vector
rational function for the family, and Corollary 60 says that every
cutoff-depth certificate denominator is divisible by the cutoff primitive
denominator `D_hw`.  Applying this to the certificate denominator `D_r` gives
(TailDiv) and the displayed degree bound for the quotient.  If `D_r` is
root-free, Corollary 58 passes reciprocal-domain-pole-freeness to both
factors, so `M_r` has no reciprocal-domain zero.

## Corollary 40.17: The Half-Window Tail Has One Multiplier Ledger Per Family

Keep the notation of Corollary 40.16, and work over a finite field `F_q`.
Fix one of the four residual families

```text
u,        v,        (u,v),        (S u,S v).
```

If this family has no root-free witness at the first half-window depth
`r_hw`, then it has no root-free witness at any deeper depth in `R_hw`.

Otherwise let `D_hw` be the cutoff primitive denominator and put

```text
delta=deg D_hw.
```

Let `TailCert` be the set of projective certificate-denominator classes, and
let `TailPrim` be the set of projective primitive denominator classes, which
occur for this same residual family at depths `r in R_hw`.  Then every class
in `TailCert`, and hence every class in `TailPrim`, is represented by

```text
D_hw(T)M(T),        deg M<=h-1-delta,
```

where `M` has no reciprocal-domain zero.  Hence

```text
|TailCert| <= (q^{h-delta}-1)/(q-1),
|TailPrim| <= (q^{h-delta}-1)/(q-1).                (TailMult)
```

The deeper recurrence equations may cut this multiplier ledger further; the
displayed number is only the ambient multiplier count attached to the cutoff
primitive denominator.  In particular the number of primitive denominator
bases, and the number of projective certificate-denominator classes, needed for
the half-window tail is bounded independently of `|R_hw|`.

### Proof

If a deeper root-free witness exists, Corollary 40.10 applied to the
half-window tail puts it in the cutoff witness family, so absence at `r_hw`
implies absence at every deeper depth.

Assume a cutoff witness exists.  Any root-free certificate denominator at a
deeper tail depth is also a cutoff-depth certificate denominator by the same
nesting argument.  Corollary 60 applied at the cutoff depth says that every
such certificate denominator is divisible by `D_hw`, and that the quotient has
degree at most `h-1-delta`.  Corollary 58 passes reciprocal-domain
pole-freeness to the quotient.  Thus `TailCert`, and therefore also
`TailPrim`, injects into the projective multiplier ledger

```text
{ M != 0 : deg M<=h-1-delta } / F_q^*,
```

after restricting to the root-free and deeper-truncation subconditions.
The full projective space of such multipliers has size

```text
1+q+...+q^{h-1-delta}=(q^{h-delta}-1)/(q-1),
```

and the additional conditions only remove classes.  This proves (TailMult).

## Corollary 40.18: The Half-Window Tail Has A Depth-Independent Denominator Budget

Keep the notation of Corollary 40.17 and work over `F_q`.  Let

```text
Fam={ u, v, (u,v), (S u,S v) }.
```

For a family `F in Fam`, write `F` as active if it has a root-free witness at
the first half-window depth `r_hw`.  For active `F`, let `D_F` be its cutoff
primitive denominator and put

```text
delta_F=deg D_F.
```

Let `TailCert_all` and `TailPrim_all` be the sets of family-labelled
projective certificate-denominator classes and primitive denominator classes,
respectively, that occur for some family `F in Fam` at some half-window tail
depth `r in R_hw`.  Then

```text
|TailCert_all|
  <= sum_{F active} (q^{h-delta_F}-1)/(q-1),
|TailPrim_all|
  <= sum_{F active} (q^{h-delta_F}-1)/(q-1)
  <= 4 (q^h-1)/(q-1).                               (TailBudget)
```

The unlabelled set of denominator classes is bounded by the same right-hand
side, and may be smaller because a denominator class can be charged in more
than one family.  The paired-family overlaps are the endpoint-pair charges of
Corollaries 40.12 and 40.13; the scalar-paired overlaps are the one-sided
endpoint residuals isolated in Corollary 40.20 below; and the scalar-scalar
overlap is the endpoint-pair residual of Corollary 40.21.

Thus the half-window tail has a single denominator budget depending only on
the four cutoff primitive denominators, not on the number of depths in
`R_hw`.  Any improvement in the cutoff degrees `delta_F`, or any proof that a
cutoff family is absent, immediately improves the whole tail budget.

### Proof

For an inactive family, Corollary 40.17 says there is no deeper half-window
witness, so it contributes nothing to `TailCert_all` or `TailPrim_all`.  For
an active family `F`, the same corollary injects all tail
certificate-denominator classes, and therefore all tail primitive denominator
classes, for that family into the projective multiplier ledger attached to
`D_F`, whose size is at most

```text
(q^{h-delta_F}-1)/(q-1).
```

Summing over the at most four labelled families gives the first inequality.
Since each active `delta_F` is nonnegative, every summand is at most
`(q^h-1)/(q-1)`, giving the coarse second inequality.  Passing from labelled
to unlabelled classes can only identify classes and therefore cannot increase
the count.  The overlap references record Corollaries 40.19--40.21.

## Corollary 40.19: Paired Tail Overlaps Are Endpoint-Pair Charges

Keep the half-window tail notation above.  Let `TailCert(u,v)` and
`TailCert(Su,Sv)` be the unlabelled projective certificate-denominator classes
that occur somewhere in the half-window tail for the ordinary paired residual
family and the shifted paired residual family; define `TailPrim(u,v)` and
`TailPrim(Su,Sv)` analogously for primitive denominator classes.

If a denominator class `D` lies in `TailCert(u,v) cap TailCert(Su,Sv)`, then
`D` is an endpoint-pair certificate at the first half-window depth:

```text
H_{t+r_hw,h-1}(u)Q=H_{t+r_hw,h-1}(v)Q=0
```

for the reversed locator `Q` attached to `D`.  Consequently, after charging
the endpoint-pair residual at the cutoff depth, the ordinary paired tail and
the shifted paired tail have no common uncharged projective
certificate-denominator class, and hence no common primitive denominator class.
Equivalently, paired-family intersections in the half-window tail are not a
new tail budget; they are endpoint-pair residual multiplier charges.

### Proof

Suppose `D` occurs in the ordinary paired tail at depth `r_1 in R_hw` and in
the shifted paired tail at depth `r_2 in R_hw`.  By row nesting in the
half-window tail, the same denominator `D` is a valid cutoff-depth certificate
for the ordinary paired family and also for the shifted paired family.  Thus
the corresponding root-free locator `Q` satisfies

```text
H_s(u)Q=H_s(v)Q=0,
H_s(S u)Q=H_s(S v)Q=0,        s=t+r_hw-1.
```

Corollary 40.12 identifies this intersection with the endpoint-pair residual,
namely

```text
H_{s+1}(u)Q=H_{s+1}(v)Q=0.
```

Since `s+1=t+r_hw`, this is the displayed endpoint-pair certificate at the
cutoff depth.  Therefore any common paired-tail certificate denominator, and
hence any common primitive denominator, is charged when the cutoff
endpoint-pair residual and its multiplier ledger are charged.

## Corollary 40.20: Scalar-Paired Tail Overlaps Are One-Sided Endpoint Residuals

Keep the notation of Corollary 40.19 and put

```text
s=t+r_hw-1,        H_m(w)=H_{m,h-1}(w).
```

Let `TailCert(u)` and `TailCert(v)` denote the unlabelled projective
certificate-denominator classes occurring somewhere in the half-window tail for
the scalar residual families `u` and `v`, and define `TailPrim(u)` and
`TailPrim(v)` analogously for primitive denominator classes.  Keep the paired
notation from Corollary 40.19.

Every projective certificate-denominator class, hence every primitive
denominator class, common to a scalar half-window tail and a paired
half-window tail is a cutoff certificate for one of the following one-sided
endpoint residual systems:

```text
H_{s+1}(u)Q=0,        H_s(v)Q=0,                    (u | u,v)
H_s(u)Q=0,            H_{s+1}(v)Q=0,                (v | u,v)
H_{s+1}(u)Q=0,        H_s(S v)Q=0,                  (u | Su,Sv)
H_s(S u)Q=0,          H_{s+1}(v)Q=0.                (v | Su,Sv)
```

More explicitly:

* `TailCert(u) cap TailCert(u,v)` is contained in `(u | u,v)`;
* `TailCert(v) cap TailCert(u,v)` is contained in `(v | u,v)`;
* `TailCert(u) cap TailCert(Su,Sv)` is contained in `(u | Su,Sv)`;
* `TailCert(v) cap TailCert(Su,Sv)` is contained in `(v | Su,Sv)`.

Consequently, after these one-sided cutoff residual systems and their
multiplier ledgers are charged, scalar-paired tail intersections contribute no
new unlabelled half-window tail certificate-denominator classes, and hence no
new primitive denominator classes.

### Proof

Consider `TailCert(u) cap TailCert(u,v)`.  By row nesting in the half-window
tail, a common tail certificate-denominator class gives a cutoff-depth scalar
certificate for `u` and a cutoff-depth ordinary paired certificate for
`(u,v)`.  With `s=t+r_hw-1`, the scalar certificate is

```text
H_{s+1}(u)Q=0,
```

and the ordinary paired certificate is

```text
H_s(u)Q=H_s(v)Q=0.
```

The `H_s(u)` rows are contained in the `H_{s+1}(u)` rows, so the intersection
is exactly the first one-sided system displayed above.  The case
`TailCert(v) cap TailCert(u,v)` is symmetric.

For `TailCert(u) cap TailCert(Su,Sv)`, the scalar certificate
`H_{s+1}(u)Q=0` contains the shifted `u` rows `H_s(Su)Q=0`, leaving the
additional shifted `v` condition `H_s(Sv)Q=0`.  This gives `(u | Su,Sv)`.
The `v` scalar case is identical with `u` and `v` interchanged.

## Corollary 40.21: Scalar Tail Overlap Is Endpoint-Pair Residual

Keep the notation of Corollary 40.20.  If a projective certificate-denominator
class, hence a primitive denominator class, lies
in

```text
TailCert(u) cap TailCert(v),
```

then it is a cutoff endpoint-pair certificate:

```text
H_{t+r_hw,h-1}(u)Q=H_{t+r_hw,h-1}(v)Q=0.           (ScalarPairTail)
```

Consequently, after the cutoff endpoint-pair residual and its multiplier
ledger are charged, the two scalar half-window tails have no common uncharged
projective certificate-denominator class, and hence no common primitive
denominator class.

Together with Corollaries 40.19 and 40.20, this gives a pairwise classification
of overlaps in the unlabelled four-family half-window tail budget:

```text
scalar-scalar      -> endpoint-pair residual,
paired-paired      -> endpoint-pair residual,
scalar-paired      -> one-sided endpoint residual.
```

### Proof

Let a denominator class occur in both scalar tails.  By row nesting in the
half-window tail, this class is a valid cutoff-depth scalar certificate for
both series.  Hence its reversed locator `Q` satisfies

```text
H_{t+r_hw,h-1}(u)Q=0,        H_{t+r_hw,h-1}(v)Q=0.
```

This is exactly the cutoff endpoint-pair residual.  Charging that residual
therefore removes the common scalar-tail denominator class.  The final
pairwise classification combines this scalar-scalar case with the paired-tail
and scalar-paired classifications already proved.

## Corollary 40.22: After Overlap Charges The Half-Window Tail Is Family-Disjoint

Keep the notation of Corollary 40.18.  Charge the following cutoff overlap
residual systems, together with their multiplier ledgers:

1. the cutoff endpoint-pair residual from Corollaries 40.19 and 40.21;
2. the four one-sided cutoff endpoint residual systems from Corollary 40.20.

On the remaining ledger, every projective certificate-denominator class, and
hence every primitive denominator class, in the half-window tail belongs to at
most one of the four residual families

```text
u,        v,        (u,v),        (S u,S v).
```

Thus the uncharged unlabelled half-window tail is family-disjoint both for
certificate denominators and for primitive denominators.  Its
denominator-class count is bounded by the same depth-independent sum

```text
sum_{F active} (q^{h-delta_F}-1)/(q-1)
```

from Corollary 40.18, but now with no hidden cross-family intersections: every
remaining certificate-denominator class has a unique family label.

### Proof

Suppose an uncharged tail certificate-denominator class belonged to two
distinct residual families.  If both families are scalar, Corollary 40.21 puts
the class in the charged endpoint-pair residual.  If both families are paired,
Corollary 40.19 puts the class in the same charged endpoint-pair residual.  If
one family is scalar and the other is paired, Corollary 40.20 puts the class in
one of the charged one-sided endpoint residual systems.  All cases contradict
that the class is uncharged.  Hence every uncharged certificate-denominator
class has at most one family label.  Primitive denominator classes are a subset
of certificate-denominator classes, and the displayed count is then
Corollary 40.18 applied family by family.

## Corollary 40.23: Refined Mixed-Ladder Closure With A Disjoint Tail Budget

Let `R` be a nonempty finite set of positive consecutive-frontier depths, and
use the notation

```text
r_0=min R,
R_pre={ r in R : h>t+r },
R_hw ={ r in R : h<=t+r }.
```

Work over `F_q`, after fixed-root/root-slice short recurrence pieces have been
charged.  First charge the following residual ledgers:

1. for each `r in R_pre`, the four root-free recurrence families from
   Corollary 40.7;
2. if `R_hw` is nonempty, the cutoff endpoint-pair residual and the four
   one-sided cutoff endpoint residuals from Corollaries 40.19--40.21.

After these charges, the remaining half-window tail denominator ledger is
family-disjoint by Corollary 40.22.  It is then charged by the following
family ledgers: if `R_hw` is nonempty, for each active residual family `F` at
`r_hw=min R_hw`, the projective multiplier ledger attached to its cutoff
primitive denominator `D_F`, of size at most

```text
(q^{h-delta_F}-1)/(q-1),        delta_F=deg D_F.
```

The total family-labelled tail denominator budget is

```text
TailBudget_hw <= sum_{F active} (q^{h-delta_F}-1)/(q-1)
              <= 4(q^h-1)/(q-1),                   (RefinedTailBudget)
```

with absent cutoff families contributing zero.

After these residual charges, all four short frontier checks hold at every
depth in `R` on the remaining ledger.  Hence the remaining finite fixed-kernel
and consecutive common-image frontier ledgers at all depths in `R` close after
charging only the bottom finite parameter systems

```text
E_{r_0,>b} union Theta_{r_0,>b},
```

of total size at most `2h` on the remaining ledger.

Thus the refined mixed-ladder closure has no `|R_hw|` denominator multiplier,
no projective image-line multiplier, and no hidden cross-family overlap inside
the half-window tail.  The unresolved inputs are exactly the pre-half-window
residual ledgers, the cutoff primitive denominators and their allowed
multipliers, and the cutoff overlap ledgers.  Corollary 40.24 below refines
the latter into at most five half-window primitive/multiplier ledgers, and
Corollary 40.25 sharpens those overlap ledgers to lcms of the cutoff family
primitive denominators.  Corollary 40.30 packages the refined cutoff ledger
as a single consumable mixed-ladder upper bound.

### Proof

The pre-half-window depths are charged by item 1.  Corollary 40.22 says that,
after the overlap systems in item 2 are charged, the remaining half-window tail
classes are family-disjoint.  In that tail, Corollary 40.17 puts every
residual family into the multiplier ledger of its cutoff primitive
denominator, and those family ledgers charge all remaining tail classes.
Corollary 40.18 gives the displayed depth-independent tail budget.

Therefore no uncharged root-free residual from Corollary 40.7 remains at any
depth in `R`.  Corollary 40.15 then gives the closure from the bottom finite
parameter systems, with total size at most `2h` by Corollary 40.4 and nesting
by Corollary 40.9.

## Corollary 40.24: Cutoff Overlap Charges Have Half-Window Multiplier Ledgers

Keep the notation of Corollary 40.23 and assume `R_hw` is nonempty.  Put

```text
r_hw=min R_hw,        s=t+r_hw-1.
```

Work over `F_q`.  Consider the five cutoff overlap systems

```text
Omega_EP:   H_{s+1}(u)Q=0,        H_{s+1}(v)Q=0,

Omega_u:    H_{s+1}(u)Q=0,        H_s(v)Q=0,
Omega_v:    H_s(u)Q=0,            H_{s+1}(v)Q=0,

Omega_uS:   H_{s+1}(u)Q=0,        H_s(Sv)Q=0,
Omega_vS:   H_s(Su)Q=0,           H_{s+1}(v)Q=0.
```

The first is the endpoint-pair residual from Corollaries 40.19 and 40.21; the
last four are the one-sided endpoint residuals from Corollary 40.20.

Attach to these systems the following paired parent windows:

```text
Parent(Omega_EP)       = (u,v) at window s+1,
Parent(Omega_u)        = Parent(Omega_v)  = (u,v) at window s,
Parent(Omega_uS)       = Parent(Omega_vS) = (S u,S v) at window s.
```

For each active overlap system `Omega`, let `D_Omega` be the primitive vector
denominator supplied by Corollary 59 for its paired parent window, and put

```text
delta_Omega=deg D_Omega.
```

Then every projective root-free certificate-denominator class for `Omega` is
represented by

```text
D_Omega(T) M(T),        deg M<=h-1-delta_Omega,
```

where `M` has no reciprocal-domain zero.  Hence

```text
|Cert(Omega)| <= (q^{h-delta_Omega}-1)/(q-1).
```

Summing over active cutoff overlap systems gives the crude uniform bound

```text
sum_{Omega active} |Cert(Omega)| <= 5 (q^h-1)/(q-1).    (OverlapMult)
```

For the four one-sided systems, the extra endpoint row is an additional
linear condition on the multiplier `M`.  Thus `D_Omega` is a primitive
denominator for the paired parent ledger; it need not itself be a full
one-sided certificate.  The assertion is that the one-sided certificate set is
contained in this explicit half-window multiplier ledger.

### Proof

Since `r_hw` is the first half-window depth, `h<=t+r_hw=s+1`.  Every
certificate denominator under consideration has degree `e<h`, hence

```text
e<=h-1<=s.
```

Thus all five cutoff overlap systems lie in the half-window range for their
paired parent windows.

For `Omega_EP`, the paired parent window is exactly the endpoint-pair system
with window length `s+1`, so Corollaries 59 and 60 give the primitive vector
denominator and its multiplier ledger directly.

For `Omega_u` and `Omega_v`, the displayed equations include the shorter
paired parent equations

```text
H_s(u)Q=0,        H_s(v)Q=0.
```

Corollary 59 applied to this parent pair gives a single primitive vector
denominator dividing every certificate denominator, and Corollary 60 gives
the multiplier ledger.  The extra row in `H_{s+1}(u)` or `H_{s+1}(v)` only
cuts out a subset of that ledger.

For `Omega_uS`, the equation `H_{s+1}(u)Q=0` contains the shifted rows
`H_s(Su)Q=0`; together with `H_s(Sv)Q=0`, this puts the certificate in the
paired parent `(S u,S v)` at window `s`.  The proof for `Omega_vS` is the same,
using that `H_{s+1}(v)Q=0` contains `H_s(Sv)Q=0`.  Applying Corollaries 59 and
60 to this shifted paired parent gives the same multiplier ledger conclusion.

In every case root-freeness passes from the certificate denominator to both
the primitive parent denominator and the multiplier by Corollary 58.  The
projective multiplier count is the one in Corollary 60, and summing over at
most five overlap systems gives (OverlapMult).

## Corollary 40.25: Cutoff Overlap Ledgers Refine Family LCM Ledgers

Keep the notation of Corollaries 40.18 and 40.24.  For the four cutoff family
primitive denominators write

```text
D_u,        D_v,        D_uv,        D_S
```

for the scalar `u`, scalar `v`, ordinary paired `(u,v)`, and shifted paired
`(S u,S v)` families when they are active.  If a family is inactive, no
overlap system containing it is active.

For an active overlap system define the family-lcm denominator

```text
L_EP = lcm(D_u,D_v,D_uv,D_S),
L_u  = lcm(D_u,D_uv),
L_v  = lcm(D_v,D_uv),
L_uS = lcm(D_u,D_S),
L_vS = lcm(D_v,D_S),
```

attached respectively to

```text
Omega_EP,        Omega_u,        Omega_v,        Omega_uS,        Omega_vS.
```

Then every projective root-free certificate-denominator class for `Omega` is
represented by

```text
L_Omega(T) M(T),        deg M<=h-1-deg L_Omega,
```

where `M` has no reciprocal-domain zero.  Consequently, writing
`ell_Omega=deg L_Omega`,

```text
|Cert(Omega)| <= (q^{h-ell_Omega}-1)/(q-1)
```

for each active overlap system.  Thus the cutoff overlap budget can be charged
to intersections of the existing cutoff family multiplier ledgers, with no
independent primitive denominator beyond the four family primitives.

In particular, the endpoint-pair overlap is smallest when any one of the four
cutoff family primitive denominators is large, because every endpoint-pair
certificate is simultaneously a scalar `u`, scalar `v`, ordinary paired, and
shifted paired cutoff certificate.

### Proof

Let `D` be a root-free certificate denominator for one of the five overlap
systems.  By Corollary 40.24, `D` lies in the multiplier ledger of its paired
parent primitive denominator.  The same certificate also satisfies the
equations of every cutoff family listed in the corresponding lcm.

For `Omega_u`, the equations

```text
H_{s+1}(u)Q=0,        H_s(v)Q=0
```

make `D` both a scalar `u` certificate and an ordinary paired `(u,v)`
certificate.  Hence Corollary 59, applied to those two cutoff families, shows
that both `D_u` and `D_uv` divide `D`, so `L_u=lcm(D_u,D_uv)` divides `D`.
The `Omega_v`, `Omega_uS`, and `Omega_vS` cases are identical with the family
labels changed as displayed.

For `Omega_EP`, the equations

```text
H_{s+1}(u)Q=0,        H_{s+1}(v)Q=0
```

imply the scalar `u` and scalar `v` cutoff equations, the ordinary paired
cutoff equations `H_s(u)Q=H_s(v)Q=0`, and the shifted paired cutoff equations
`H_s(Su)Q=H_s(Sv)Q=0`.  Therefore all four primitive denominators
`D_u,D_v,D_uv,D_S` divide `D`, so `L_EP` divides `D`.

Since `D` has degree `<h`, each active `L_Omega` has degree `<h`, and the
quotient multiplier satisfies `deg M<=h-1-deg L_Omega`.  Root-freeness passes
to `M` by Corollary 58.  Counting projective nonzero multipliers of degree at
most `h-1-deg L_Omega` gives the displayed bound.  The actual overlap
certificate set may be smaller because the remaining truncation rows impose
additional linear conditions.

## Corollary 40.26: One-Sided Cutoff Overlaps Have A Row-Cut Dichotomy

Keep the cutoff notation above, and write `ell=(ell_0,...,ell_{h-1})` for a
degree-`<h` locator coefficient vector.  For a syndrome series `w`, let

```text
row_a(w)(ell)=sum_{i=0}^{h-1} ell_i w_{a+i}.
```

Set

```text
K_uv = ker H_s(u)  cap ker H_s(v),
K_S  = ker H_s(Su) cap ker H_s(Sv).
```

Then the four one-sided cutoff overlap locator spaces are exactly

```text
Omega_u  = K_uv cap ker row_s(u),
Omega_v  = K_uv cap ker row_s(v),
Omega_uS = K_S  cap ker row_0(u),
Omega_vS = K_S  cap ker row_0(v).                  (RowCut)
```

Consequently each one-sided overlap has the following dichotomy.  If the
displayed row functional is nonzero on its parent kernel `K`, then, writing
`P(Omega)` for the projectivization of the nonzero locator vectors in
`Omega`,

```text
dim Omega = dim K - 1,
|P(Omega)| <= (q^{dim K-1}-1)/(q-1)
```

over `F_q`; in particular the projective root-free certificate-denominator
classes in that one-sided overlap obey the same bound.  If the row functional
vanishes on `K`, then the parent paired cutoff kernel is endpoint-persistent:
every parent paired certificate already satisfies the corresponding one-sided
endpoint equation.

Thus a one-sided cutoff overlap can pay the full parent paired projective
ledger only in the explicit endpoint-persistent case; otherwise it gains one
linear row cut.

### Proof

For the ordinary paired parent, `K_uv` is exactly the locator space satisfying

```text
H_s(u)ell=0,        H_s(v)ell=0.
```

Adding `row_s(u)(ell)=0` is the same as adding the missing last row of
`H_{s+1}(u)ell=0`, so the resulting space is `Omega_u`.  Adding
`row_s(v)(ell)=0` gives `Omega_v`.

For the shifted paired parent, the rows of `H_s(Su)` are the rows
`row_1(u),...,row_s(u)`, and similarly for `v`.  Thus adding `row_0(u)` to
`K_S` gives exactly `H_{s+1}(u)ell=0` together with `H_s(Sv)ell=0`, which is
`Omega_uS`; adding `row_0(v)` gives `Omega_vS`.

The linear-algebra dichotomy is immediate: the kernel of a nonzero linear
functional on a finite-dimensional vector space has codimension one, while a
zero restriction means the whole parent space already satisfies the added
endpoint row.  Passing from projective locator classes to root-free
certificate-denominator classes can only remove classes, so the same
projective count bounds the denominator classes.

## Corollary 40.27: Endpoint Persistence Is A Stacked-Hankel Row-Span Test

Keep the notation of Corollary 40.26.  Let

```text
M_uv = [ H_s(u) ; H_s(v) ],
M_S  = [ H_s(Su) ; H_s(Sv) ].
```

For a row functional `rho`, write `rho in Row(M)` to mean that `rho` lies in
the row span of `M`.  Then:

1. `Omega_u` is endpoint-persistent precisely when

```text
row_s(u) in Row(M_uv).
```

2. `Omega_v` is endpoint-persistent precisely when

```text
row_s(v) in Row(M_uv).
```

3. `Omega_uS` is endpoint-persistent precisely when

```text
row_0(u) in Row(M_S).
```

4. `Omega_vS` is endpoint-persistent precisely when

```text
row_0(v) in Row(M_S).
```

Equivalently, in each case endpoint persistence is the rank equality

```text
rank [ M ; rho ] = rank M.                           (PersistRank)
```

Failure of this equality is the nonpersistent case of Corollary 40.26 and
forces a one-dimensional cut on the parent kernel.

The endpoint-pair overlap has the analogous two-row form.  With

```text
R_EP = span( row_s(u)|_{K_uv}, row_s(v)|_{K_uv} ) subset K_uv^*,
```

one has

```text
dim Omega_EP = dim K_uv - dim R_EP,
```

and therefore, over `F_q`,

```text
|P(Omega_EP)| <= (q^{dim K_uv-dim R_EP}-1)/(q-1).
```

Thus the endpoint-pair residual loses two projective dimensions from the
ordinary paired parent unless the two missing endpoint rows have rank `<2` on
`K_uv`; the exceptional alternatives are explicit stacked-Hankel row-span or
row-dependence conditions.

### Proof

For any matrix `M` and row `rho`,

```text
ker M subset ker rho
```

if and only if `rho` belongs to the row span of `M`.  Applying this with
`M=M_uv` and `rho=row_s(u)` says exactly that every ordinary paired cutoff
locator already satisfies the extra `u` endpoint row.  This is the
endpoint-persistent case for `Omega_u`.  The other three one-sided statements
are identical with the displayed parent matrix and row.

If `rho` is not in the row span, then the rank of `[M;rho]` is one larger than
the rank of `M`, so the kernel dimension drops by one.  This is the
nonpersistent case of Corollary 40.26.

For `Omega_EP`, the endpoint-pair locator space is

```text
K_uv cap ker row_s(u) cap ker row_s(v).
```

Restricting the two rows to `K_uv`, its codimension inside `K_uv` is the rank
of those two restricted functionals, namely `dim R_EP`.  The projective count
then follows by counting nonzero vectors in that kernel quotient and
projectivizing.  The alternative `dim R_EP=0` is precisely the case where both
missing endpoint rows already lie in `Row(M_uv)`.  The alternative
`dim R_EP=1` is precisely the case where the two restricted rows span only one
nonzero line on `K_uv`, including the subcase where exactly one missing row is
already in `Row(M_uv)`.

## Corollary 40.28: Rank-Refined Cutoff Overlap Budget

Keep the notation of Corollary 40.27 and work over `F_q`.  Put

```text
d_uv = dim K_uv,        d_S = dim K_S,
```

and define the missing-row ranks

```text
eps_u  = rank( row_s(u)|_{K_uv} ),
eps_v  = rank( row_s(v)|_{K_uv} ),
eps_uS = rank( row_0(u)|_{K_S} ),
eps_vS = rank( row_0(v)|_{K_S} ),
r_EP   = rank( row_s(u)|_{K_uv}, row_s(v)|_{K_uv} ).
```

Here each `eps_*` is either `0` or `1`, and `0<=r_EP<=2`.  Let

```text
Phi(m)=(q^m-1)/(q-1)        for m>=0.
```

Then the projective locator count in the five cutoff overlap systems is at
most

```text
Phi(d_uv-r_EP)
+ Phi(d_uv-eps_u)
+ Phi(d_uv-eps_v)
+ Phi(d_S-eps_uS)
+ Phi(d_S-eps_vS).                                  (RankOverlap)
```

The same expression also bounds the number of projective root-free
certificate-denominator classes supported by the cutoff overlap systems.

In the full-row-cut case

```text
r_EP=2,        eps_u=eps_v=eps_uS=eps_vS=1,
```

this becomes

```text
Phi(d_uv-2) + 2 Phi(d_uv-1) + 2 Phi(d_S-1).
```

Thus every failure of the full-row-cut saving is accounted for by at least one
explicit rank defect among

```text
r_EP<2,        eps_u=0,        eps_v=0,        eps_uS=0,        eps_vS=0.
```

Equivalently, the only way an overlap term pays its full parent projective
kernel is through one of the row-span or row-dependence conditions isolated in
Corollary 40.27.

### Proof

Corollary 40.27 gives

```text
dim Omega_EP = d_uv-r_EP.
```

Corollary 40.26 gives

```text
dim Omega_u  = d_uv-eps_u,
dim Omega_v  = d_uv-eps_v,
dim Omega_uS = d_S-eps_uS,
dim Omega_vS = d_S-eps_vS.
```

For an `m`-dimensional vector space over `F_q`, its projectivization has
`Phi(m)` points, with `Phi(0)=0`.  Summing the five projective locator counts
gives (RankOverlap).  Mapping a projective locator class to its root-free
certificate-denominator class can only identify or delete classes, so the same
sum bounds the denominator classes.  The displayed full-row-cut specialization
is obtained by substituting the full ranks.

## Corollary 40.29: Hybrid Rank-LCM Cutoff Overlap Budget

Keep the notation of Corollaries 40.25 and 40.28, and write

```text
ell_EP = deg L_EP,
ell_u  = deg L_u,
ell_v  = deg L_v,
ell_uS = deg L_uS,
ell_vS = deg L_vS.
```

For active overlap systems, the projective root-free certificate-denominator
classes in the cutoff overlap ledger are bounded by

```text
min( Phi(h-ell_EP), Phi(d_uv-r_EP) )
+ min( Phi(h-ell_u),  Phi(d_uv-eps_u) )
+ min( Phi(h-ell_v),  Phi(d_uv-eps_v) )
+ min( Phi(h-ell_uS), Phi(d_S-eps_uS) )
+ min( Phi(h-ell_vS), Phi(d_S-eps_vS) ).             (HybridOverlap)
```

Inactive overlap systems contribute zero, equivalently their corresponding
summand is omitted.

Thus the cutoff-overlap charge can be consumed term by term using whichever
certificate count is smaller:

1. the family-lcm multiplier ledger from Corollary 40.25; or
2. the endpoint-row rank ledger from Corollary 40.28.

In particular, a large family-lcm degree and a full endpoint-row cut are
independent savings mechanisms, and either one improves the corresponding
overlap summand.

### Proof

For each active overlap system `Omega`, Corollary 40.25 bounds its projective
root-free certificate-denominator classes by the corresponding lcm multiplier
count `Phi(h-ell_Omega)`.  Corollary 40.28 bounds the same set by the
corresponding projective locator count:

```text
Phi(d_uv-r_EP),        Phi(d_uv-eps_u),        Phi(d_uv-eps_v),
Phi(d_S-eps_uS),       Phi(d_S-eps_vS).
```

A set bounded by two quantities is bounded by their minimum.  Summing these
termwise minima over the active overlap systems gives (HybridOverlap).

## Corollary 40.30: Mixed-Ladder Closure With A Hybrid Cutoff Ledger

Keep the mixed-ladder notation of Corollary 40.23 and work over `F_q`.  Put

```text
Phi(m)=(q^m-1)/(q-1)        for m>=0.
```

If `R_hw` is nonempty, define

```text
FamilyBudget_hw = sum_{F active} Phi(h-delta_F)
```

with the four active cutoff residual families `F in {u,v,(u,v),(Su,Sv)}` as
in Corollary 40.18, and define `HybridOverlap_hw` by the right-hand side of
(HybridOverlap) in Corollary 40.29.  If `R_hw` is empty, set both budgets to
zero.

After the fixed-root/root-slice short recurrence pieces and the pre-half-window
root-free recurrence families have been charged, the whole half-window cutoff
part is charged by at most

```text
HybridOverlap_hw + FamilyBudget_hw
```

projective root-free certificate-denominator classes.  After those denominator
charges, all four short frontier checks hold at every depth in `R`, and the
remaining finite fixed-kernel and consecutive common-image frontier ledgers
close after charging only

```text
E_{r_0,>b} union Theta_{r_0,>b},
```

of total size at most `2h` on the remaining ledger.

Thus, apart from the pre-half-window longer-Pade residual families, the mixed
frontier ladder has the explicit consumable upper ledger

```text
HybridOverlap_hw + FamilyBudget_hw + 2h.             (HybridMixedLedger)
```

There is still no `|R_hw|` multiplier, no projective image-line multiplier, and
no hidden cross-family overlap term.  The displayed bound is intentionally an
upper ledger: the family budget is paid after overlap charges and may be
smaller in a sharper disjoint accounting.

### Proof

The pre-half-window depths are exactly the depths where Corollary 40.8 does
not put the root-free residuals into the half-window Pade range; these are
charged by hypothesis.  If `R_hw` is empty, no half-window denominator charge
is needed.

Assume `R_hw` is nonempty.  Corollary 40.29 charges the five cutoff overlap
systems by `HybridOverlap_hw`.  After those overlap charges, Corollary 40.22
makes the remaining half-window tail family-disjoint.  Corollary 40.18 then
charges the remaining family-labelled tail by `FamilyBudget_hw`.  This removes
all root-free residuals in the half-window tail.

Thus no uncharged root-free residual from Corollary 40.7 remains at any depth
in `R`.  Corollary 40.15 gives closure of the finite fixed-kernel and
consecutive common-image frontier ledgers from the bottom systems
`E_{r_0,>b} union Theta_{r_0,>b}`, and Corollary 40.4 bounds their total size
by `2h` on the remaining ledger.  Summing the displayed charges gives
(HybridMixedLedger).

## Corollary 40.31: Hybrid Overlaps Are A Separation Charge, Not A Raw Tail Addend

Keep the notation of Corollary 40.30, and let `TailUnion_hw` be the unlabelled
set of projective root-free certificate-denominator classes occurring anywhere
in the half-window tail, across the four cutoff residual families

```text
u,        v,        (u,v),        (S u,S v).
```

Then, for raw denominator-class counting,

```text
|TailUnion_hw| <= FamilyBudget_hw.                  (RawTailBudget)
```

In particular, `HybridOverlap_hw` is not an additional raw denominator-count
addend.  It is a separation charge: it gives an explicit way to remove the
cross-family overlap systems before applying the family-disjoint closure of
Corollary 40.22.

Thus there are two compatible ledgers:

1. raw half-window denominator count:

```text
FamilyBudget_hw;
```

2. proof-separation closure ledger:

```text
HybridOverlap_hw + FamilyBudget_hw,
```

where the second ledger intentionally pays the named overlap systems first so
that every remaining uncharged denominator class has a unique family label.

### Proof

The family-labelled set `TailCert_all` from Corollary 40.18 maps onto the
unlabelled union `TailUnion_hw` by forgetting the family label.  Therefore the
unlabelled raw count is at most the labelled count, which is bounded by
`FamilyBudget_hw`.

The five cutoff overlap systems of Corollaries 40.19--40.21 are subsets of
this same unlabelled half-window tail.  Corollary 40.29 bounds them by
`HybridOverlap_hw`; charging them first is useful because Corollary 40.22 then
makes the remaining tail family-disjoint.  This is a logical separation
ledger, not a claim that the raw union has size
`FamilyBudget_hw + HybridOverlap_hw`.

## Corollary 40.32: Cutoff Overlap Union Has An Inclusion-Exclusion Rank Budget

Keep the notation of Corollaries 40.27--40.28, and define the shifted
two-row rank

```text
r_S = rank( row_0(u)|_{K_S}, row_0(v)|_{K_S} ).
```

Let `Omega_all` be the union of the five cutoff overlap locator spaces

```text
Omega_EP,        Omega_u,        Omega_v,        Omega_uS,        Omega_vS.
```

Then

```text
Omega_all = Omega_u union Omega_v union Omega_uS union Omega_vS,
```

because `Omega_EP` is contained in each of the four one-sided spaces.  Hence,
over `F_q`, the projective locator count in the cutoff overlap union is at
most

```text
Phi(d_uv-eps_u) + Phi(d_uv-eps_v) - Phi(d_uv-r_EP)
+ Phi(d_S-eps_uS) + Phi(d_S-eps_vS) - Phi(d_S-r_S).   (UnionRankOverlap)
```

The same expression bounds the number of projective root-free
certificate-denominator classes in the cutoff overlap union.

In the full independent-row case

```text
r_EP=2,        r_S=2,
eps_u=eps_v=eps_uS=eps_vS=1,
```

this becomes

```text
2 Phi(d_uv-1) - Phi(d_uv-2)
+ 2 Phi(d_S-1) - Phi(d_S-2).
```

Thus the endpoint-pair residual need not be paid as a fifth independent
rank-budget summand when the four one-sided ambient overlap systems are
charged.

### Proof

If a locator lies in `Omega_EP`, then it satisfies

```text
H_{s+1}(u)ell=0,        H_{s+1}(v)ell=0.
```

It therefore satisfies `H_s(v)ell=0`, so it lies in `Omega_u`, and it satisfies
`H_s(u)ell=0`, so it lies in `Omega_v`.  Since `H_{s+1}(u)` contains the
shifted rows `H_s(Su)` and `H_{s+1}(v)` contains the shifted rows `H_s(Sv)`,
it also lies in `Omega_uS` and `Omega_vS`.  This proves the displayed union
identity.

Inside `K_uv`, the projective union `P(Omega_u) union P(Omega_v)` has size

```text
Phi(d_uv-eps_u) + Phi(d_uv-eps_v) - Phi(d_uv-r_EP),
```

because `Omega_u cap Omega_v=Omega_EP` has dimension `d_uv-r_EP`.  Similarly,
inside `K_S`, the projective union `P(Omega_uS) union P(Omega_vS)` has size

```text
Phi(d_S-eps_uS) + Phi(d_S-eps_vS) - Phi(d_S-r_S).
```

The full cutoff-overlap union is contained in the union of these two parent
unions, so summing the two bounds gives (UnionRankOverlap).  Passing from
projective locator classes to root-free certificate-denominator classes can
only identify or remove classes, so the same bound applies to denominator
classes.

## Corollary 40.33: Mixed-Ladder Closure With The Sharper Overlap-Union Charge

Keep the notation of Corollaries 40.30 and 40.32.  If `R_hw` is nonempty, let
`UnionRankOverlap_hw` be the right-hand side of (UnionRankOverlap), and put

```text
SideHybridOverlap_hw
 = min( Phi(h-ell_u),  Phi(d_uv-eps_u) )
 + min( Phi(h-ell_v),  Phi(d_uv-eps_v) )
 + min( Phi(h-ell_uS), Phi(d_S-eps_uS) )
 + min( Phi(h-ell_vS), Phi(d_S-eps_vS) ).
```

Inactive one-sided overlap systems contribute zero, equivalently their
corresponding summands are omitted.  Define

```text
OverlapSep_hw = min(SideHybridOverlap_hw, UnionRankOverlap_hw).
```

If `R_hw` is empty, set both `SideHybridOverlap_hw` and `OverlapSep_hw` to
zero.  Then the proof-separation half-window cutoff charge in Corollary 40.30
can be replaced by

```text
OverlapSep_hw + FamilyBudget_hw,
```

and the mixed frontier ladder has the sharper consumable upper ledger

```text
OverlapSep_hw + FamilyBudget_hw + 2h.               (SharpHybridMixedLedger)
```

The raw unlabelled half-window tail count remains bounded by `FamilyBudget_hw`
as in Corollary 40.31, and by the sharper divisor-arrangement budget in
Corollary 40.34 below.  The `OverlapSep_hw` term is only the cost of separating
the named cross-family overlap systems before applying the family-disjoint tail
closure.

### Proof

Corollary 40.32 shows that the endpoint-pair overlap is contained in each of
the four one-sided overlap systems.  Hence charging the four one-sided systems
already charges the endpoint-pair system.  Corollary 40.29, applied only to
those four one-sided systems, bounds their union by `SideHybridOverlap_hw`.
Corollary 40.32 also bounds the same union by `UnionRankOverlap_hw`.  Therefore
the union is bounded by their minimum, `OverlapSep_hw`.

Substitute this smaller separation charge for `HybridOverlap_hw` in the proof
of Corollary 40.30.  The raw-count statement is exactly Corollary 40.31.

## Corollary 40.34: Raw Half-Window Tail Has A Divisor-Arrangement Budget

Keep the notation of Corollaries 40.18 and 40.31, and suppose first that
`R_hw` is nonempty.  Let `A` be the set of active cutoff residual families
among

```text
u,        v,        (u,v),        (S u,S v),
```

with cutoff primitive denominators `D_F`.  For every nonempty subset
`I subset A`, put

```text
D_I = lcm( D_F : F in I ),        ell_I=deg D_I,
```

and define

```text
Psi(I)=Phi(h-ell_I)        if ell_I<h,
Psi(I)=0                  if ell_I>=h.
```

Set

```text
ArrBudget_hw =
  sum_{nonempty I subset A} (-1)^{|I|+1} Psi(I),     (DivisorArrangement)
```

where the sum ranges over nonempty `I`.  If `R_hw` is empty, set
`ArrBudget_hw=0`.  Then the unlabelled projective
certificate-denominator classes in the half-window tail satisfy

```text
|TailUnion_hw| <= ArrBudget_hw <= FamilyBudget_hw.   (RawArrangementTail)
```

The same bound holds for unlabelled projective primitive denominator classes.
Thus the raw half-window tail count can be sharpened from the four-family sum
to the inclusion-exclusion count of the divisor subspaces generated by the
active cutoff primitive denominators.  This is a raw-count refinement only:
it does not by itself prove the arrangement budget is small enough for M1.
The overlap-separation charge remains useful when one wants a family-disjoint
tail ledger, but the direct raw-tail closure in Corollary 40.36 below can
bypass that separation step.

### Proof

For an active family `F`, let

```text
U_F={ P in F_q[T] : deg P<h and D_F divides P }.
```

This is a vector space of dimension `h-deg D_F`, and Corollary 40.18 puts the
projective certificate-denominator classes for family `F` inside `P(U_F)`.
The unlabelled half-window tail is therefore contained in

```text
union_{F in A} P(U_F).
```

For a nonempty subset `I subset A`, the intersection

```text
cap_{F in I} U_F
```

is exactly the vector space of degree-`<h` polynomials divisible by
`D_I=lcm(D_F:F in I)`.  It has dimension `h-ell_I` when `ell_I<h`, and is zero
otherwise.  Hence its projectivization has size `Psi(I)`.  Inclusion-exclusion
for the finite union of projective subspaces gives the exact size of the
ambient divisor-subspace union as `ArrBudget_hw`, proving the first
inequality.  The second inequality is the elementary bound that a union has
size at most the sum of its four singleton projective subspace sizes, which is
`FamilyBudget_hw`.  Primitive denominator classes form a subset of
certificate-denominator classes, so the same estimate applies to them.

## Corollary 40.35: Mixed-Ladder Closure With The Divisor-Arrangement Tail

Keep the notation of Corollaries 40.33 and 40.34.  After the fixed-root/root-slice
short recurrence pieces and the pre-half-window root-free recurrence
families have been charged, the half-window cutoff part is charged by at most

```text
OverlapSep_hw + ArrBudget_hw
```

projective root-free certificate-denominator classes.  Consequently, apart
from the pre-half-window longer-Pade residual families, the mixed frontier
ladder has the sharper consumable upper ledger

```text
OverlapSep_hw + ArrBudget_hw + 2h.                  (ArrangementMixedLedger)
```

This improves Corollary 40.33 because `ArrBudget_hw<=FamilyBudget_hw`.  It is
still an upper ledger: `ArrBudget_hw` bounds the full unlabelled half-window
tail union, not just the complement of the charged overlap systems, so some
overlap classes may be counted in both `OverlapSep_hw` and `ArrBudget_hw`.

### Proof

If `R_hw` is empty, both `OverlapSep_hw` and `ArrBudget_hw` are zero and the
statement is Corollary 40.15 after the pre-half charges.

Assume `R_hw` is nonempty.  Corollary 40.33 charges the cutoff overlap union by
`OverlapSep_hw`.  Let `TailRemaining_hw` be the uncharged unlabelled
certificate-denominator classes still occurring in the half-window tail after
those overlap charges.  Then

```text
TailRemaining_hw subset TailUnion_hw.
```

Corollary 40.34 bounds `TailUnion_hw`, hence also `TailRemaining_hw`, by
`ArrBudget_hw`.  Charging these remaining classes removes every half-window
root-free residual.  The finite fixed-kernel and consecutive common-image
frontier ledgers then close from the bottom finite parameter set
`E_{r_0,>b} union Theta_{r_0,>b}`, of size at most `2h`, exactly as in
Corollary 40.30.  Summing the displayed charges gives
(ArrangementMixedLedger).

## Corollary 40.36: Direct Raw-Tail Closure Needs No Separate Overlap Charge

Keep the notation of Corollaries 40.31 and 40.34.  After the
fixed-root/root-slice short recurrence pieces and the pre-half-window root-free
recurrence families have been charged, the whole half-window cutoff part is
charged by at most

```text
ArrBudget_hw
```

projective root-free certificate-denominator classes.  Consequently, apart
from the pre-half-window longer-Pade residual families, the mixed frontier
ladder has the direct raw-denominator upper ledger

```text
ArrBudget_hw + 2h.                                  (RawArrangementMixedLedger)
```

This improves Corollary 40.35 whenever `OverlapSep_hw>0`.  The improvement is
not a new estimate for the overlap systems: it uses the fact that the overlap
systems are already subsets of the same unlabelled half-window tail union.
The structural overlap ledgers `OverlapSep_hw`, `SideHybridOverlap_hw`, and
`UnionRankOverlap_hw` remain useful diagnostics for family-disjoint proofs and
for auditing where the divisor arrangement has large intersections, but they
are not additional denominator-class charges in the direct raw-tail closure.

### Proof

If `R_hw` is empty, `ArrBudget_hw=0` and the claim again reduces to the finite
bottom closure after the pre-half charges.

Assume `R_hw` is nonempty.  By definition, `TailUnion_hw` is the unlabelled set
of projective root-free certificate-denominator classes occurring anywhere in
the half-window tail across the four cutoff residual families.  Corollary
40.31 notes that the cutoff endpoint-pair and one-sided overlap systems are
subsets of this same unlabelled tail.  Thus charging all classes in
`TailUnion_hw` removes both the named overlap residuals and the non-overlap
half-window residuals.

Corollary 40.34 bounds `TailUnion_hw` by `ArrBudget_hw`.  After these
denominator classes are charged, no half-window root-free residual from
Corollary 40.7 remains.  Corollary 40.15 then closes the finite fixed-kernel
and consecutive common-image frontier ledgers from the bottom parameter set
`E_{r_0,>b} union Theta_{r_0,>b}`, whose size is at most `2h` by Corollary
40.4.  This gives (RawArrangementMixedLedger).

## Corollary 40.37: The Raw Tail Arrangement Reduces To A Divisor Antichain

Keep the notation of Corollary 40.34.  Let `M_min` be the set of distinct
active cutoff primitive denominators that are divisibility-minimal among the
active family primitives:

```text
D in M_min
iff D=D_F for some active F, and there is no active G with D_G | D and D_G != D.
```

Then

```text
union_{F in A} P(U_F) = union_{D in M_min} P(U_D),
```

where `U_D={P: deg P<h and D divides P}`.  Consequently `ArrBudget_hw` can be
computed using only the denominator antichain `M_min`; all dominated active
families and duplicate primitive denominators contribute no new raw
half-window denominator classes.

In particular, if the active cutoff primitive denominators form one
divisibility chain, and `D_min` is the smallest denominator in that chain with
`delta_min=deg D_min`, then

```text
ArrBudget_hw = Phi(h-delta_min)
```

when `delta_min<h`, and `ArrBudget_hw=0` otherwise.  The direct raw-tail
mixed-ladder ledger of Corollary 40.36 then becomes

```text
Phi(h-delta_min) + 2h.                              (ChainTailLedger)
```

Thus any cutoff residual family whose primitive denominator is forced to be a
multiple of another active family's primitive is automatically absorbed in the
raw-tail denominator count.

### Proof

If `D_G` divides `D_F`, then every degree-`<h` polynomial divisible by `D_F`
is also divisible by `D_G`; hence

```text
U_F subset U_G.
```

Therefore deleting such a dominated family does not change the projective
union of divisor subspaces.  If two active families have the same primitive
denominator, they have the same divisor subspace, so keeping one representative
also does not change the union.  Iterating over all dominated active families
and identifying duplicate denominators leaves exactly the distinct
divisibility-minimal antichain `M_min` and proves the first claim.

If the active denominators form a chain, `M_min` has one element, represented
by `D_min`.  The projective divisor subspace has dimension `h-delta_min` when
`delta_min<h`, and is zero otherwise.  This gives the displayed value of
`ArrBudget_hw`; substituting it into Corollary 40.36 gives (ChainTailLedger).

## Corollary 40.38: Common-Core Factorization Of The Raw Tail Arrangement

Keep the notation of Corollary 40.37, and suppose `M_min` is nonempty.  Let

```text
C = gcd( D : D in M_min ),        gamma=deg C,
E_D = D/C                         for D in M_min.
```

Put `h'=h-gamma`.  If `h'<=0`, then `ArrBudget_hw=0`.  If `h'>0`, multiplication
by `C` gives a projective bijection

```text
union_{D in M_min} P({P: deg P<h and D|P})
  =
C * union_{D in M_min} P({Q: deg Q<h' and E_D|Q}).
```

Consequently the raw tail arrangement factors exactly through the common core:

```text
ArrBudget_hw =
  sum_{nonempty I subset M_min} (-1)^{|I|+1}
      Phi(h' - deg lcm(E_D : D in I)),              (CoreArrangement)
```

with the convention that `Phi(m)=0` for `m<=0` in this displayed formula.

In particular, if the quotient denominators `E_D` are pairwise coprime and
have degrees `e_D`, then

```text
ArrBudget_hw =
  sum_{nonempty I subset M_min} (-1)^{|I|+1}
      Phi(h' - sum_{D in I} e_D).                   (CoprimeCoreArrangement)
```

Thus a common denominator core of degree `gamma` is paid once across the whole
raw half-window tail, and only the quotient arrangement inside the shorter
window `h-gamma` remains.

### Proof

For every `D in M_min`, divisibility by `D=C E_D` is equivalent to writing
`P=CQ` with `E_D|Q`.  The degree condition `deg P<h` is then exactly
`deg Q<h-gamma`.  Multiplication by the nonzero polynomial `C` is an injective
linear map from degree-`<h'` polynomials to degree-`<h` polynomials, and it
identifies the quotient divisor subspace for `E_D` with the original divisor
subspace for `D`.  It therefore induces the displayed projective bijection on
the union.  If `h'<=0`, the quotient degree range has no nonzero polynomial,
so the projective union is empty.

For any nonempty subset `I`, one has

```text
lcm(C E_D : D in I) = C * lcm(E_D : D in I),
```

so the intersection dimension drops from `h-deg lcm(D:D in I)` to
`h'-deg lcm(E_D:D in I)`.  Applying the inclusion-exclusion formula of
Corollary 40.34 in the quotient window gives (CoreArrangement).  If the
quotient denominators are pairwise coprime, the lcm degree is the sum of their
degrees, giving (CoprimeCoreArrangement).

## Corollary 40.39: A Common Core Gives A One-Parameter Tail Bound

Keep the notation of Corollary 40.38.  With `gamma=deg C`, the raw
half-window tail satisfies

```text
ArrBudget_hw <= Phi(h-gamma)                       (CommonCoreTail)
```

with the convention that `Phi(m)=0` for `m<=0` in this displayed formula.
Consequently the direct raw-tail mixed-ladder ledger of Corollary 40.36 is at
most

```text
Phi(h-gamma) + 2h.                                 (CommonCoreMixedLedger)
```

In particular, if `gamma>=h`, then `ArrBudget_hw=0`: the half-window tail
contributes no raw denominator classes after the pre-half residuals have been
charged, and the remaining mixed-ladder finite frontier charge is at most
`2h`.

Thus a lower bound on the common denominator core degree is enough to control
the full raw half-window tail, without needing to understand the quotient
denominator arrangement.

### Proof

If `h-gamma<=0`, Corollary 40.38 already gives `ArrBudget_hw=0`.  Otherwise,
Corollary 40.38 identifies the raw tail arrangement with a union of projective
quotient divisor subspaces inside the full projective space of nonzero
degree-`<h-gamma` polynomials.  That ambient projective space has
`Phi(h-gamma)` points, so the union has at most that many points.  Substituting
this bound into Corollary 40.36 gives (CommonCoreMixedLedger).  The case
`gamma>=h` is the first sentence.

## Corollary 40.40: Minimum Quotient Degree Gives A Proper-Tail Saving

Keep the notation of Corollary 40.38, and suppose `M_min` is nonempty.  Put

```text
s=|M_min|,        e_min = min_{D in M_min} deg E_D.
```

Then

```text
ArrBudget_hw <= s Phi(h-gamma-e_min),              (MinQuotientTail)
```

again with the convention that `Phi(m)=0` for `m<=0` in this displayed formula.
Consequently the direct raw-tail mixed-ladder ledger is at most

```text
s Phi(h-gamma-e_min) + 2h.                         (MinQuotientMixedLedger)
```

In particular, if `gamma+e_min>=h`, the half-window tail contributes no raw
denominator classes.  If `s>=2`, then `e_min>=1`; hence every genuinely
multi-family denominator antichain gains at least one quotient degree beyond
the common-core bound of Corollary 40.39:

```text
ArrBudget_hw <= s Phi(h-gamma-1).
```

### Proof

By Corollary 40.38, after factoring the common core `C`, the raw tail
arrangement is the union over `D in M_min` of quotient divisor subspaces

```text
P({Q: deg Q<h-gamma and E_D|Q}).
```

The `D`-summand has projective size at most `Phi(h-gamma-deg E_D)`, hence at
most `Phi(h-gamma-e_min)`.  Summing over the `s` summands gives
(MinQuotientTail), and substituting in Corollary 40.36 gives
(MinQuotientMixedLedger).

If `gamma+e_min>=h`, the displayed bound is zero.  Finally, if `s>=2` and
`e_min=0`, then some quotient denominator is `E_D=1`, so `D=C` divides every
active denominator.  All other active denominators would then be dominated by
`D`, contradicting the definition of the distinct divisibility-minimal
antichain `M_min`.  Therefore `e_min>=1` when `s>=2`.

## Corollary 40.41: Residual Tail Dimension Is The Polynomial-Window Target

Keep the notation of Corollary 40.40, and put

```text
r_tail = max(0, h-gamma-e_min).
```

If `r_tail<=L`, then

```text
ArrBudget_hw <= s Phi(L) <= 4 Phi(L),              (ResidualTailBound)
```

and the direct raw-tail mixed-ladder ledger is bounded by

```text
4 Phi(L) + 2h.                                     (ResidualTailMixedLedger)
```

Equivalently, the half-window raw-tail part is polynomial-field controlled as
soon as the common core plus the smallest nontrivial quotient degree consumes
all but `L` denominator degrees:

```text
gamma + e_min >= h-L.                              (ResidualTailCriterion)
```

In particular, if `q<=n^a`, `h<=n`, and `L>=1` is fixed, then

```text
4 Phi(L) + 2h <= 4L n^{a(L-1)} + 2n.
```

Thus, in the polynomial-field window, the remaining raw half-window tail task
has been reduced to proving a lower bound on `gamma+e_min` up to a fixed
residual dimension `L`.

### Proof

Corollary 40.40 gives

```text
ArrBudget_hw <= s Phi(r_tail).
```

The function `Phi(m)` is nondecreasing for `m>=0`, and `s<=4` because there
are only four cutoff residual families.  Hence `r_tail<=L` gives
(ResidualTailBound), and Corollary 40.36 gives (ResidualTailMixedLedger).
The displayed criterion is just the inequality `r_tail<=L` rewritten.

For the polynomial-field consequence, when `L>=1`,

```text
Phi(L)=1+q+...+q^{L-1} <= L q^{L-1} <= L n^{a(L-1)}.
```

Also `h<=n` by hypothesis.  Substituting these two estimates gives the
displayed bound.

## Corollary 40.42: Two Surviving Denominators Have An Exact Tail Formula

Keep the notation of Corollary 40.38, and suppose the distinct
divisibility-minimal antichain has exactly two elements

```text
M_min={D_1,D_2}.
```

Let

```text
C=gcd(D_1,D_2),        gamma=deg C,
E_i=D_i/C,             e_i=deg E_i        for i=1,2.
```

Then `gcd(E_1,E_2)=1`, and the raw half-window tail arrangement is exactly

```text
ArrBudget_hw =
  Phi(h-gamma-e_1)
+ Phi(h-gamma-e_2)
- Phi(h-gamma-e_1-e_2),                            (TwoDenominatorTail)
```

with the convention that `Phi(m)=0` for `m<=0` in this displayed formula.
Consequently the direct raw-tail mixed-ladder ledger is

```text
Phi(h-gamma-e_1)
+ Phi(h-gamma-e_2)
- Phi(h-gamma-e_1-e_2)
+ 2h.                                              (TwoDenominatorMixedLedger)
```

In particular, if both `h-gamma-e_i<=L`, then the tail term is at most
`2 Phi(L)`, and if `gamma+min(e_1,e_2)>=h`, the half-window tail vanishes.

### Proof

Because `C` is the gcd of `D_1` and `D_2`, the quotient denominators
`E_1=D_1/C` and `E_2=D_2/C` are coprime.  Corollary 40.38 therefore applies
with two pairwise-coprime quotient denominators.  Inclusion-exclusion has only
the two singleton terms and their intersection.  The singleton divisor
subspaces have projective sizes `Phi(h-gamma-e_1)` and `Phi(h-gamma-e_2)`,
while their intersection is the divisor subspace for `E_1E_2`, of projective
size `Phi(h-gamma-e_1-e_2)`.  This proves (TwoDenominatorTail), and adding
the bottom finite frontier charge `2h` from Corollary 40.36 gives
(TwoDenominatorMixedLedger).

The final two statements are immediate from the displayed formula and the
nonnegativity convention for `Phi`.

## Corollary 40.43: The Bottom Residual Route Has No Pre-Half Depth Sum

Let `R` be a nonempty finite set of consecutive-frontier depths and put
`r_0=min R`.  Work after fixed-root/root-slice short recurrence pieces have
been charged.  If the four bottom root-free recurrence families

```text
RF_{r_0}(u),        RF_{r_0}(v),
RF_{r_0}(u,v),      RF_{r_0}(S u,S v)
```

are charged, then every root-free residual at every depth in `R` is charged.
Consequently the mixed frontier ladder closes after charging only the bottom
finite parameter systems

```text
E_{r_0,>b} union Theta_{r_0,>b},
```

of total size at most `2h` on the remaining ledger.

Thus the residual part of a mixed ladder has two compatible closure routes:

1. bottom route: charge the four bottom root-free residual families once, even
   if they are pre-half-window longer-Pade targets;
2. half-window route: leave the bottom longer-Pade targets as explicit
   obligations, and use the first half-window cutoff plus the raw-tail
   denominator arrangement of Corollaries 40.34--40.42.

The first route has no `|R_pre|` factor and no half-window denominator ledger.
The second route is useful only when one wants to keep the bottom pre-half
families as the named remaining obstruction and separately count the
half-window tail.

### Proof

This is Corollary 40.10 applied to the whole set `R`: for each of the four
residual families and every `r in R`, the root-free witness set at depth `r`
is contained in the corresponding witness set at `r_0`.  Therefore charging
the four bottom families removes every root-free residual in the ladder.
Corollary 40.11 then gives closure from the bottom finite parameter set, with
total size at most `2h`.  The comparison with the half-window route is exactly
the split used in Corollaries 40.14--40.42.

## Corollary 40.44: The Ladder Residual Bottleneck Is A Two-Route Minimum

Keep the notation of Corollary 40.43, and set

```text
R_pre={ r in R : h>t+r },
R_hw ={ r in R : h<=t+r }.
```

Write

```text
B_0 =
 RF_{r_0}(u) union RF_{r_0}(v)
 union RF_{r_0}(u,v) union RF_{r_0}(S u,S v)
```

for the four bottom root-free residual families, and write

```text
P_pre =
 union_{r in R_pre}
   ( RF_r(u) union RF_r(v) union RF_r(u,v) union RF_r(S u,S v) )
```

for the pre-half-window root-free residual families.  If `R_hw` is nonempty,
let `TailUnion_hw` be the unlabelled half-window certificate-denominator union
from Corollary 40.34; if `R_hw` is empty, set `TailUnion_hw=emptyset`.

After fixed-root/root-slice short recurrence pieces have been charged, the
root-free residual part of the ladder has two simultaneous descriptions:

1. bottom description: every root-free residual at every depth in `R` lies in
   the corresponding bottom family inside `B_0`;
2. split description: every root-free residual is either a pre-half residual
   in `P_pre`, or has a half-window certificate-denominator class in
   `TailUnion_hw`.

Consequently, if `Charge(B_0)` is any admissible charge for the four bottom
families and `Charge(P_pre)` is any admissible charge for the pre-half
families, then the root-free residual part may be closed using either ledger

```text
Charge(B_0)
```

or

```text
Charge(P_pre) + ArrBudget_hw.
```

After adding the bottom finite frontier charge, the consumable ladder ledger is

```text
min( Charge(B_0), Charge(P_pre) + ArrBudget_hw ) + 2h.        (ResidualRouteMin)
```

This is not a new estimate for `Charge(B_0)` or `Charge(P_pre)`.  It identifies
the precise residual bottleneck: either prove that the bottom longer-Pade
family `B_0` is small enough, or keep `P_pre` as the named obstruction and
prove that the half-window arrangement term is small, for example via the
criterion `gamma+e_min>=h-L` from Corollary 40.41.

### Proof

The bottom description is exactly Corollary 40.10 applied to the whole set
`R`.  It gives, for each of the four residual types and every `r in R`,

```text
RF_r(*) subset RF_{r_0}(*).
```

Thus charging `B_0` charges every root-free residual in the ladder.

For the split description, the depths in `R_pre` are charged by definition of
`P_pre`.  At depths in `R_hw`, Corollary 40.14 moves every root-free witness to
the first half-window depth `r_hw`, and Corollary 40.34 bounds the unlabelled
certificate-denominator classes arising from those cutoff families by
`ArrBudget_hw`.  Thus the half-window part is charged by the raw divisor
arrangement ledger.

Once either residual ledger has been charged, Corollary 40.11 closes the
remaining finite fixed-kernel and consecutive common-image frontier ledgers
from `E_{r_0,>b} union Theta_{r_0,>b}`, of total size at most `2h`.  Taking the
better of the two residual routes gives (ResidualRouteMin).

## Corollary 40.45: Root-Free Multipliers Sharpen The Raw Tail Arrangement

Keep the notation of Corollary 40.34 and work over `F_q`.  Assume `0 notin D`,
as in the multiplicative-domain M1 setting, and put `n=|D|`.  For `m>=1`,
let `RFPhi_D(m)` be the number of projective nonzero polynomials
`M(T)` of degree `<m` with no zero on the reciprocal domain

```text
D^vee={ alpha^{-1} : alpha in D }.
```

Set `RFPhi_D(m)=0` for `m<=0`.  Then

```text
RFPhi_D(m)
 = (1/(q-1)) sum_{j=0}^{min(n,m-1)}
      (-1)^j binom(n,j) (q^{m-j}-1).              (RootFreePhi)
```

For every nonempty `I subset A`, keep

```text
D_I=lcm(D_F:F in I),        ell_I=deg D_I.
```

Define the root-free divisor-arrangement budget

```text
RFArrBudget_hw =
  sum_{nonempty I subset A} (-1)^{|I|+1} RFPhi_D(h-ell_I),
```

with `RFArrBudget_hw=0` if `R_hw` is empty.  Then the unlabelled half-window
tail certificate-denominator classes satisfy

```text
|TailUnion_hw| <= RFArrBudget_hw <= ArrBudget_hw.  (RootFreeArrangementTail)
```

Consequently the direct raw-tail mixed-ladder ledger of Corollary 40.36 may be
sharpened, in the multiplicative-domain case, to

```text
RFArrBudget_hw + 2h,                               (RootFreeRawMixedLedger)
```

apart from whichever pre-half residual route is being used.

This refinement uses only the already-required root-free condition; it is not a
new structural estimate on which primitive denominators occur.  Its value is
that the ambient multiplier spaces in `ArrBudget_hw` can be replaced by the
exact MDS full-support counts on the reciprocal evaluation set.

### Proof

First count root-free multipliers.  For a fixed subset `J subset D^vee` of
size `j<m`, the space of degree-`<m` polynomials vanishing on every point of
`J` has dimension `m-j` by the Vandermonde independence of evaluations at
distinct points.  Hence it contains `q^{m-j}-1` nonzero polynomials.  If
`j>=m`, no nonzero degree-`<m` polynomial can vanish on all of `J`.  Inclusion-
exclusion over the zero events at the `n` reciprocal-domain points gives the
number of nonzero degree-`<m` polynomials with no such zero.  Dividing by
`q-1` gives (RootFreePhi), since scalar multiples have the same zero set.

For the arrangement, every active cutoff primitive denominator `D_F` is
reciprocal-domain-pole-free, so every lcm `D_I` is also
reciprocal-domain-pole-free.  A projective denominator class lies in the
intersection of the divisor ledgers indexed by `I` precisely when it has a
representative

```text
P(T)=D_I(T)M(T),        deg M<h-ell_I.
```

Because `D_I` has no zero on `D^vee`, the denominator `P` is root-free on
`D^vee` if and only if `M` is.  Thus that intersection has projective size
`RFPhi_D(h-ell_I)`.  Inclusion-exclusion over the active family divisor
ledgers gives the displayed `RFArrBudget_hw` for the ambient root-free union.
The actual half-window tail is a subset of this ambient union, proving the
first inequality.  The root-free ambient union is a subset of the full divisor
ambient union counted in Corollary 40.34, so its size is at most
`ArrBudget_hw`; this gives the second inequality.  Substituting this sharper
tail charge into Corollary 40.36 gives (RootFreeRawMixedLedger).

## Corollary 40.46: Root-Free Residual Dimension Gives A Smaller Tail Target

Keep the notation of Corollaries 40.41 and 40.45, and assume `0 notin D`.
Let

```text
r_tail=max(0,h-gamma-e_min).
```

If `r_tail<=L`, then the root-free raw half-window arrangement satisfies

```text
RFArrBudget_hw <= s RFPhi_D(L) <= 4 RFPhi_D(L),    (RootFreeResidualTail)
```

and the direct mixed-ladder ledger is bounded by

```text
4 RFPhi_D(L) + 2h.                                 (RootFreeResidualMixedLedger)
```

Thus the same structural target as Corollary 40.41,

```text
gamma+e_min>=h-L,
```

now pays only for root-free multipliers of residual dimension `L`, rather than
all projective multipliers of that dimension.

In particular,

```text
RFPhi_D(1)=1,
RFPhi_D(2)=q+1-n.
```

Hence residual dimension `L=1` gives ledger at most `4+2h`, and residual
dimension `L=2` gives ledger at most `4(q+1-n)+2h`.  For the full
multiplicative domain `n=q-1`, the latter is at most `8+2h`.

### Proof

As in Corollary 40.37, divisibility-dominated active denominators and duplicate
denominators do not change the divisor union.  The same is true after imposing
the root-free condition, because divisibility by a larger denominator still
implies divisibility by the smaller one and root-freeness is a property of the
final product.  Thus we may work with the distinct minimal antichain `M_min`.

After factoring the common core `C`, each distinct divisibility-minimal
denominator contributes a root-free multiplier ledger of projective size

```text
RFPhi_D(h-gamma-deg(D/C)).
```

Since `deg(D/C)>=e_min`, this parameter is at most `r_tail`, and hence at most
`L`.  The sets of root-free multipliers of degree `<m` are nested in `m`, so
each family contributes at most `RFPhi_D(L)`.  There are `s<=4` surviving
minimal denominator families, giving (RootFreeResidualTail).  Adding the
bottom finite frontier charge `2h` gives (RootFreeResidualMixedLedger).

The explicit values follow from (RootFreePhi).  For `m=1`, only nonzero
constants occur, giving one projective class.  For `m=2`,

```text
RFPhi_D(2)=((q^2-1)-n(q-1))/(q-1)=q+1-n.
```

Substitution gives the two displayed ledgers.

## Corollary 40.47: The Root-Free Tail Arrangement Has The Same Common-Core Formula

Keep the notation of Corollaries 40.38 and 40.45, and assume `0 notin D`.
Suppose `M_min` is nonempty.  Let

```text
C = gcd( D : D in M_min ),        gamma=deg C,
E_D = D/C                         for D in M_min,
h'=h-gamma.
```

If `h'<=0`, then `RFArrBudget_hw=0`.  If `h'>0`, multiplication by `C`
identifies the root-free raw tail arrangement with the root-free quotient
arrangement in the shorter window `h'`:

```text
RFArrBudget_hw =
  sum_{nonempty I subset M_min} (-1)^{|I|+1}
      RFPhi_D(h' - deg lcm(E_D : D in I)),          (RFCoreArrangement)
```

with the convention that `RFPhi_D(m)=0` for `m<=0`.

In particular, if the quotient denominators `E_D` are pairwise coprime with
degrees `e_D`, then

```text
RFArrBudget_hw =
  sum_{nonempty I subset M_min} (-1)^{|I|+1}
      RFPhi_D(h' - sum_{D in I} e_D).               (RFCoprimeCoreArrangement)
```

If exactly two distinct divisibility-minimal denominators survive,
`M_min={D_1,D_2}`, and

```text
C=gcd(D_1,D_2),        E_i=D_i/C,        e_i=deg E_i,
```

then `gcd(E_1,E_2)=1` and

```text
RFArrBudget_hw =
  RFPhi_D(h-gamma-e_1)
+ RFPhi_D(h-gamma-e_2)
- RFPhi_D(h-gamma-e_1-e_2).                         (RFTwoDenominatorTail)
```

The corresponding direct mixed-ladder ledger is obtained by adding the bottom
finite frontier charge `2h`.

Thus the root-free replacement does not disturb the denominator-core
invariants `gamma,e_D`: it only replaces each projective multiplier space
`Phi(*)` in the raw common-core formula by the exact full-support count
`RFPhi_D(*)`.

### Proof

Corollary 40.37 deletes dominated active denominators before the raw
arrangement is computed.  The same deletion is valid in the root-free
arrangement by the argument in Corollary 40.46, so we work with `M_min`.

Each active primitive denominator is reciprocal-domain-pole-free.  Hence its
common divisor `C`, every quotient denominator `E_D`, and every lcm appearing
below are also reciprocal-domain-pole-free.  Divisibility by `D=C E_D` is
equivalent to writing `P=CQ` with `E_D|Q`, and the degree condition is
`deg Q<h-gamma`.  Since `C` has no zero on `D^vee`, the product `P=CQ` is
root-free on `D^vee` if and only if `Q` is.

Therefore multiplication by `C` gives a projective bijection from the
root-free quotient divisor union in degree `<h'` to the original root-free
divisor union in degree `<h`.  Intersections are governed by

```text
lcm(C E_D : D in I) = C * lcm(E_D : D in I),
```

so inclusion-exclusion gives (RFCoreArrangement).  Pairwise coprime quotient
denominators turn the lcm degree into the sum of the quotient degrees, giving
(RFCoprimeCoreArrangement).  The two-denominator case is the special case
where the two quotients after factoring the gcd are automatically coprime.

## Corollary 40.48: Bottom Residual Kernels Close Under A Domain-MDS Test

Let `K` be any linear subspace of degree-`<h` polynomials over `F_q`, and let

```text
K(-J)={ Q in K : Q(alpha)=0 for every alpha in J },        J subset D.
```

Write `d=dim K`, and let `K^rf` be the projective set of nonzero classes
`[Q] in P(K)` with `Q(alpha)!=0` for every `alpha in D`.  Then

```text
|K^rf| =
  sum_{J subset D} (-1)^{|J|} Phi(dim K(-J)).       (KernelRootFreeIE)
```

If `K` is in domain-MDS position, meaning

```text
dim K(-J)=max(d-|J|,0)        for every J subset D,
```

then

```text
|K^rf| = RFPhi_D(d).                               (KernelRootFreeMDS)
```

Apply this to the four bottom residual kernels

```text
K_0(u)     = ker H_{t+r_0,h-1}(u),
K_0(v)     = ker H_{t+r_0,h-1}(v),
K_0(u,v)   = ker H_{t+r_0-1,h-1}(u) cap ker H_{t+r_0-1,h-1}(v),
K_0(Su,Sv) = ker H_{t+r_0-1,h-1}(S u) cap ker H_{t+r_0-1,h-1}(S v).
```

If these four kernels are in domain-MDS position and have dimensions
`d_F<=L`, then the bottom residual route of Corollary 40.43 closes the whole
mixed frontier ladder with residual charge

```text
sum_F RFPhi_D(d_F) <= 4 RFPhi_D(L),
```

and total direct ledger

```text
4 RFPhi_D(L) + 2h.                                 (BottomMDSMixedLedger)
```

No half-window hypothesis is used in this bottom route.  Thus the bottom
longer-Pade obstruction can be replaced by a finite linear-algebra target:
prove that the four bottom recurrence kernels have bounded dimension and that
domain-root evaluation cuts them in MDS position.

### Proof

For each `alpha in D`, let

```text
A_alpha=P({Q in K : Q(alpha)=0}).
```

The root-free projective set is

```text
P(K) \setminus union_{alpha in D} A_alpha.
```

For any `J subset D`, the intersection of the events `A_alpha` with
`alpha in J` is exactly `P(K(-J))`.  Inclusion-exclusion on the finite
projective set `P(K)` gives (KernelRootFreeIE), with the convention
`Phi(0)=0`.

If `K` is in domain-MDS position, then the summand depends only on
`j=|J|` and is zero for `j>=d`.  Therefore

```text
|K^rf| =
  sum_{j=0}^{min(|D|,d-1)} (-1)^j binom(|D|,j) Phi(d-j)
  = RFPhi_D(d),
```

which is (KernelRootFreeMDS).

The four bottom residual families in Corollary 40.43 are precisely the
root-free projective points in the four displayed bottom kernels.  Applying
(KernelRootFreeMDS) to each kernel gives `sum_F RFPhi_D(d_F)`.  If all
`d_F<=L`, monotonicity of the ambient root-free count gives
`RFPhi_D(d_F)<=RFPhi_D(L)`, so the residual charge is at most
`4 RFPhi_D(L)`.  Corollary 40.43 then adds only the bottom finite frontier
charge `2h`, giving (BottomMDSMixedLedger).

## Corollary 40.49: The Bottom Domain-MDS Test Is A Root-Slice Rank Test

Keep the notation of Corollary 40.48.  For a subset `J subset D`, let

```text
L_J(X)=prod_{alpha in J} (X-alpha),        a=|J|,
Delta_J=prod_{alpha in J} Delta_alpha.
```

For the four bottom residual families, define the stripped root-slice kernels

```text
K_J(u) =
  ker H_{t+r_0,h-a-1}(Delta_J u),

K_J(v) =
  ker H_{t+r_0,h-a-1}(Delta_J v),

K_J(u,v) =
  ker H_{t+r_0-1,h-a-1}(Delta_J u)
  cap ker H_{t+r_0-1,h-a-1}(Delta_J v),

K_J(Su,Sv) =
  ker H_{t+r_0-1,h-a-1}(S Delta_J u)
  cap ker H_{t+r_0-1,h-a-1}(S Delta_J v),
```

with the convention that the kernel is zero when `a>=h`.  Then multiplication
by `L_J` gives canonical linear isomorphisms

```text
K_0(F)(-J)  ~=  K_J(F),        F in {u,v,(u,v),(Su,Sv)}.      (RootSliceIso)
```

Consequently the exact bottom root-free count of Corollary 40.48 can be
written entirely in stripped root-slice ranks:

```text
|K_0(F)^rf|
 = sum_{J subset D} (-1)^{|J|} Phi(dim K_J(F)).     (RootSliceIE)
```

Moreover, the bottom kernel `K_0(F)` is in domain-MDS position if and only if

```text
dim K_J(F)=max(dim K_0(F)-|J|,0)        for every J subset D.  (NoRootSliceExcess)
```

Thus the hypothesis in Corollary 40.48 is exactly a fixed-root/root-slice
rank condition: after the standard root-slice charges, the bottom longer-Pade
route closes whenever the four stripped root-slice kernels have no excess
dimension beyond the MDS profile.

### Proof

A polynomial `Q` of degree `<h` vanishes on every `alpha in J` if and only if
`Q=L_J R` with `deg R<h-a`; for `a>=h` this leaves no nonzero `Q`.  Corollary
40.6, equivalently the stripping identity of Corollary 49, gives

```text
H_{s,h-1}(w)(L_J R)=0
iff
H_{s,h-a-1}(Delta_J w)R=0.
```

For scalar families this is exactly the displayed isomorphism.  For the
ordinary paired family, apply the same identity to both `u` and `v` and take
the intersection of the two stripped kernels.  For the shifted paired family,
use `Delta_alpha(Sw)=S(Delta_alpha w)` for every `alpha`, so the same
stripping gives the displayed shifted kernels.

Substituting these isomorphisms into (KernelRootFreeIE) gives (RootSliceIE).
The domain-MDS condition in Corollary 40.48 is the equality
`dim K_0(F)(-J)=max(dim K_0(F)-|J|,0)` for every `J`; replacing
`K_0(F)(-J)` by the isomorphic stripped root-slice kernel gives
(NoRootSliceExcess).

## Corollary 40.50: It Suffices To Test Top Root Slices

Let `K` be a `d`-dimensional subspace of degree-`<h` polynomials, and assume
`d<=|D|`.  The following are equivalent:

1. `K` is in domain-MDS position:

```text
dim K(-J)=max(d-|J|,0)        for every J subset D;
```

2. for every `J subset D` with `|J|=d`,

```text
K(-J)=0;                                           (NoTopRootSlice)
```

3. no nonzero polynomial in `K` has `d` distinct roots in `D`;
4. for one, equivalently every, basis `Q_1,...,Q_d` of `K`, every square
   evaluation determinant

```text
det( Q_i(alpha_j) )_{1<=i,j<=d},        {alpha_1,...,alpha_d} subset D,
```

is nonzero.

Consequently, in Corollary 40.48, if each bottom kernel has dimension
`d_F<=L<=|D|` and satisfies this top-root-slice test, then the bottom longer-
Pade route closes with

```text
sum_F RFPhi_D(d_F)+2h <= 4 RFPhi_D(L)+2h,
```

as in (BottomMDSMixedLedger).  Equivalently, by Corollary 40.49, it is enough
to prove that each stripped top root-slice kernel `K_J(F)` with
`|J|=d_F` is zero.

### Proof

The domain-MDS condition immediately implies `K(-J)=0` for every `|J|=d`.
That is equivalent to saying that no nonzero element of `K` vanishes on `d`
distinct domain points.  It is also equivalent to nonvanishing of the displayed
evaluation determinant for every `d`-set: the determinant is the matrix of the
evaluation map

```text
ev_J: K -> F^J
```

in the chosen basis, and `K(-J)=ker ev_J`.

It remains to show that the top-root-slice test implies the full domain-MDS
profile.  Let `A subset D` have size `a<d`.  Evaluation on `A` imposes at most
`a` independent linear conditions, so

```text
dim K(-A) >= d-a.
```

If strict inequality held, choose any `B subset D\A` of size `d-a`.  The extra
vanishing conditions at `B` can reduce dimension by at most `d-a`, hence

```text
dim K(-(A union B)) >= dim K(-A)-(d-a) > 0.
```

This produces a nonzero element of `K` vanishing on the `d` distinct points
`A union B`, contradicting the top-root-slice test.  Hence
`dim K(-A)=d-a` for all `a<d`, and `K(-J)=0` for all `|J|>=d` follows from
the `d`-subset case.  This is exactly domain-MDS position.

The final bottom-route statement is Corollary 40.48, and the stripped
top-root-slice formulation is Corollary 40.49 applied with `|J|=d_F`.

## Corollary 40.51: Two-Dimensional Bottom Kernels Are Evaluation-Line Counts

Let `K` be a two-dimensional subspace of degree-`<h` polynomials over `F_q`.
For `alpha in D`, let

```text
ev_alpha: K -> F_q,        Q |-> Q(alpha)
```

be the evaluation functional.  If `ev_alpha=0` for some `alpha in D`, then
`K^rf` is empty.  Otherwise each `ev_alpha` defines a projective evaluation
line

```text
[ev_alpha] in P(K^*).
```

Let

```text
s_K = |{ [ev_alpha] : alpha in D }|.
```

Then

```text
|K^rf| = q+1-s_K.                                  (TwoDimRootFreeLines)
```

Equivalently,

```text
|K^rf| = RFPhi_D(2) + (|D|-s_K)
       = q+1-|D| + (|D|-s_K).                      (TwoDimCollisionDefect)
```

Thus a two-dimensional bottom kernel is domain-MDS exactly when all evaluation
functionals are nonzero and the projective map

```text
D -> P(K^*),        alpha |-> [ev_alpha]
```

is injective.  In that case `|K^rf|=RFPhi_D(2)=q+1-|D|`.

Applied to the four bottom residual kernels, if every nonzero bottom kernel
has dimension at most two, no two-dimensional kernel has a zero evaluation
functional, and `s_F` denotes the number of distinct evaluation lines for the
two-dimensional family `F`, then the bottom route has residual charge

```text
sum_{d_F=1} 1  +  sum_{d_F=2} (q+1-s_F),
```

and the mixed ladder closes after adding the bottom finite frontier charge
`2h`.  In particular, if all two-dimensional bottom evaluation-line maps are
injective, this recovers the `L=2` ledger

```text
4(q+1-|D|)+2h,
```

with absent or one-dimensional families contributing less.

### Proof

If some `ev_alpha` is zero, then every polynomial in `K` vanishes at `alpha`,
so no nonzero projective class is root-free.

Assume all evaluation functionals are nonzero.  The projective space `P(K)` has
`q+1` points.  For each `alpha`, the set of projective classes vanishing at
`alpha` is the kernel point

```text
P(ker ev_alpha) subset P(K).
```

Two domain points remove the same point of `P(K)` exactly when their
evaluation functionals are scalar multiples, i.e. when they have the same
projective evaluation line in `P(K^*)`.  Hence the union of all vanishing
points has size `s_K`, and the complement, which is exactly `K^rf`, has size
`q+1-s_K`.  Since `RFPhi_D(2)=q+1-|D|`, the collision-defect formula follows.

The injectivity statement is the `d=2` case of Corollary 40.50: no nonzero
kernel element vanishes at two distinct domain points iff no two projective
evaluation lines coincide, and the no-one-root condition is exactly
`ev_alpha!=0` for every `alpha`.  The bottom-route statement sums this exact
count over the four bottom kernels and invokes Corollary 40.43.

## Corollary 40.52: Two-Dimensional Defect Is Charged By Pair Root Slices

Keep the notation of Corollary 40.51, and assume `dim K=2` and
`ev_alpha!=0` for every `alpha in D`.  Let

```text
C_K =
 |{ {alpha,beta} subset D : alpha!=beta and [ev_alpha]=[ev_beta] }|
```

be the number of unordered projective evaluation-line collision pairs.  Then

```text
|K^rf| <= RFPhi_D(2) + C_K.                        (TwoDimPairDefect)
```

Moreover, for distinct `alpha,beta in D`,

```text
[ev_alpha]=[ev_beta]
iff
K(-{alpha,beta}) != 0.                             (PairRootSliceCollision)
```

Thus, by Corollary 40.49, the defect over the ideal `RFPhi_D(2)` count is
charged by the stripped two-root kernels

```text
K_{ {alpha,beta} }(F)
```

of the corresponding bottom residual family.

Consequently, suppose every nonzero bottom residual kernel has dimension at
most two, and suppose every two-dimensional bottom kernel has no zero
evaluation functional.  Let `C_F` be the pair-collision count for each
two-dimensional family.  Then the bottom route closes with residual charge

```text
sum_{d_F=1} 1
+ sum_{d_F=2} ( RFPhi_D(2) + C_F ),
```

and hence with total ledger obtained by adding the bottom finite frontier
charge `2h`.  In particular, if the total pair-root-slice collision count
over the two-dimensional bottom families is at most `C`, the residual charge
is at most

```text
4 RFPhi_D(2) + C.
```

### Proof

Let the fibers of the projective evaluation-line map

```text
D -> P(K^*),        alpha |-> [ev_alpha]
```

have sizes `m_1,...,m_s`, where `s=s_K`.  Then

```text
|D|-s_K = sum_i (m_i-1),
C_K     = sum_i binom(m_i,2).
```

Since `m_i-1<=binom(m_i,2)` for every `m_i>=1`, Corollary 40.51 gives

```text
|K^rf| = RFPhi_D(2)+(|D|-s_K) <= RFPhi_D(2)+C_K.
```

For the equivalence, two nonzero linear functionals on the two-dimensional
space `K` are projectively equal exactly when they have the same one-
dimensional kernel.  Thus `[ev_alpha]=[ev_beta]` if and only if

```text
ker ev_alpha cap ker ev_beta
```

is nonzero, which is precisely `K(-{alpha,beta})!=0`.  Corollary 40.49
identifies this pair slice with the stripped two-root bottom kernel for the
same residual family.  Summing the displayed upper bound over the four bottom
families and invoking Corollary 40.43 gives the bottom-route ledger.

## Corollary 40.53: Projective Degree Bounds The Two-Dimensional Defect

Keep the notation of Corollary 40.51.  Let `K` be two-dimensional with basis
`Q_0,Q_1`, and let

```text
G=gcd(Q_0,Q_1),        A=Q_0/G,        B=Q_1/G.
```

Put

```text
r_K=max(deg A, deg B).
```

Then `r_K>=1` and is independent of the chosen basis.  Assume
`ev_alpha!=0` for every `alpha in D`.  The projective evaluation map

```text
phi_K : D -> P^1,        alpha |-> [A(alpha):B(alpha)]
```

has every fiber of size at most `r_K`.  Consequently

```text
|D|-s_K <= (1-1/r_K)|D|,                            (DegreeDefect)
C_K     <= ((r_K-1)/2)|D|.                          (DegreePairDefect)
```

Therefore

```text
|K^rf| <= RFPhi_D(2) + (1-1/r_K)|D|.                (DegreeTwoDimRootFree)
```

In particular, if `r_K=1`, then the projective evaluation map is injective on
`D`, so

```text
|K^rf|=RFPhi_D(2)=q+1-|D|.
```

Applied to the four bottom residual kernels, if every two-dimensional bottom
kernel has projective degree at most `r` and no zero evaluation functional,
then the total two-dimensional collision defect is at most

```text
4(1-1/r)|D|
```

for the exact line-count ledger, or at most `2(r-1)|D|` for the pair-collision
ledger of Corollary 40.52.  Degree-one bottom kernels contribute no defect
beyond the ideal `RFPhi_D(2)` term.

### Proof

Changing the basis of `K` applies an invertible linear change to the pair
`(Q_0,Q_1)`, which does not change the common divisor of all elements of `K`
or the degree of the induced base-point-free map after that divisor is
removed.  Since `K` has dimension two, the reduced pair `(A,B)` is not a
constant projective pair, so `r_K>=1`.

The assumption `ev_alpha!=0` says not both `Q_0(alpha)` and `Q_1(alpha)`
vanish.  Hence `G(alpha)!=0` and not both `A(alpha),B(alpha)` vanish, so
`phi_K` is defined on all of `D` and has the same projective evaluation lines
as the original kernel.

For a point `[u:v] in P^1`, the fiber of `phi_K` over `[u:v]` is cut out by

```text
v A(X)-u B(X)=0.
```

This polynomial has degree at most `r_K`, and it is not identically zero
because `(A,B)` is a reduced nonconstant projective pair.  Thus every fiber on
`D` has size at most `r_K`.

Let the nonempty fiber sizes be `m_1,...,m_s`, so `s=s_K` and
`sum_i m_i=|D|`.  Since every `m_i<=r_K`,

```text
m_i-1 <= (1-1/r_K)m_i,
binom(m_i,2) <= ((r_K-1)/2)m_i.
```

Summing these two inequalities over fibers gives (DegreeDefect) and
(DegreePairDefect).  Corollary 40.51 then gives
(DegreeTwoDimRootFree).  If `r_K=1`, every fiber has size at most one, so the
map is injective on `D` and Corollary 40.51 gives the exact ideal count.  The
bottom-route statements follow by summing over the at most four residual
families.

## Corollary 40.54: A Large Common Factor Forces Small Two-Dimensional Defect

Keep the notation of Corollary 40.53, and put

```text
gamma_K=deg G.
```

If `G(alpha)=0` for some `alpha in D`, then `K^rf` is empty.  Otherwise
`G` is root-free on `D`, the projective map of Corollary 40.53 is defined on
all of `D`.  Since `K/G` is two-dimensional inside the space of polynomials
of degree `<h-gamma_K`, necessarily `gamma_K<=h-2`, and

```text
r_K <= h-1-gamma_K.                                (CommonFactorDegree)
```

Consequently, for a two-dimensional bottom kernel with no zero evaluation
functional,

```text
|K^rf| <= RFPhi_D(2)
        + (1 - 1/(h-1-gamma_K)) |D|,               (CommonFactorTwoDim)
```

and

```text
C_K <= ((h-2-gamma_K)/2)|D|.                       (CommonFactorPairDefect)
```

In particular, if `gamma_K>=h-2`, then `r_K=1`, the evaluation-line map is
injective on `D`, and

```text
|K^rf|=RFPhi_D(2).
```

Thus, for the `L=2` bottom route, a two-dimensional bottom kernel with a
common factor of degree at least `h-2` contributes exactly the ideal
root-free count, and a common factor with `h-1-gamma_K` bounded contributes
only a bounded-degree collision defect.

### Proof

If `G(alpha)=0`, then both basis elements `Q_0,Q_1` vanish at `alpha`, so the
evaluation functional on `K` is zero and no projective class in `K` is
root-free.

Assume `G` has no domain root.  Since every element of `K` has degree `<h`,
the reduced basis elements `A=Q_0/G` and `B=Q_1/G` have degree
`<h-gamma_K`.  Hence

```text
r_K=max(deg A,deg B) <= h-1-gamma_K.
```

Substituting this bound for `r_K` in Corollary 40.53 gives
(CommonFactorTwoDim) and (CommonFactorPairDefect).  If
`gamma_K>=h-2`, then the two-dimensional quotient span is contained in the
two-dimensional space of polynomials of degree `<2`, so its reduced
projective degree is `r_K=1`.  Corollary 40.53 gives the exact ideal count.

## Corollary 40.55: A Maximal Common Factor Forces The Ideal Bottom Count

Let `K` be a `d`-dimensional subspace of degree-`<h` polynomials over `F_q`,
with `1<=d<=|D|`.  Let

```text
G_K = gcd( Q : Q in K ),        gamma_K=deg G_K.
```

If `G_K(alpha)=0` for some `alpha in D`, then `K^rf` is empty.  Otherwise
`G_K` is root-free on `D`, and necessarily

```text
gamma_K <= h-d.                                    (CommonFactorMax)
```

If equality holds, then multiplication by `G_K` identifies `K` with the full
space of polynomials of degree `<d`, and therefore

```text
|K^rf| = RFPhi_D(d).                               (MaxCommonFactorMDS)
```

Consequently, the bottom route of Corollary 40.43 closes with the ideal
root-free residual charge

```text
sum_F RFPhi_D(d_F) <= 4 RFPhi_D(L)
```

whenever every bottom residual kernel `K_0(F)` has dimension `d_F<=L` and its
common factor either has a domain root or has degree `h-d_F`.

Thus the domain-MDS condition in Corollary 40.48 is automatic for bottom
kernels whose common factor is as large as dimension permits.  Corollary 40.54
is the case `d=2`: the threshold `gamma_K=h-2` is exactly the maximal common
factor condition.

### Proof

If `G_K` has a domain root, then every element of `K` vanishes at that root,
so `K^rf` is empty.

Assume `G_K` is root-free on `D`.  Dividing by `G_K` embeds the `d`-dimensional
space `K/G_K` into the ambient space of polynomials of degree `<h-gamma_K`,
which has dimension `h-gamma_K`.  Hence `d<=h-gamma_K`, proving
(CommonFactorMax).

If `gamma_K=h-d`, then this ambient space also has dimension `d`.  Therefore
`K/G_K` is the whole space of polynomials of degree `<d`.  Multiplication by
the root-free polynomial `G_K` preserves zero sets on `D`, so root-free
projective classes in `K` are in bijection with root-free projective classes
of nonzero degree-`<d` polynomials.  The latter number is exactly
`RFPhi_D(d)` by the definition in Corollary 40.45.  Summing over the four
bottom residual families and applying Corollary 40.43 gives the displayed
bottom-route ledger.

## Corollary 40.56: A Common Factor Gives A Bottom Residual-Window Bound

Let `K` be a nonzero subspace of degree-`<h` polynomials over `F_q`, and let

```text
G_K = gcd( Q : Q in K ),        gamma_K=deg G_K,
m_K = h-gamma_K.
```

If `G_K(alpha)=0` for some `alpha in D`, then `K^rf` is empty.  Otherwise
multiplication by `G_K` identifies `K^rf` with a projective subset of the
root-free degree-`<m_K` polynomial classes, and therefore

```text
|K^rf| <= RFPhi_D(m_K).                            (BottomCommonFactorWindow)
```

Consequently, for the four bottom residual kernels `K_0(F)`, if

```text
h-deg gcd(K_0(F)) <= L
```

for every nonzero bottom family whose common factor is root-free on `D`, then
the bottom route closes with residual charge at most

```text
4 RFPhi_D(L),
```

and total mixed-ladder ledger at most

```text
4 RFPhi_D(L) + 2h.                                 (BottomCommonFactorMixedLedger)
```

This criterion does not require the bottom kernel to be domain-MDS.  It only
uses the size of the residual quotient window after the common factor is
removed.  Corollary 40.55 is the extremal case `m_K=dim K`, where the quotient
subspace fills the whole residual window and the ideal count is exact.

### Proof

If `G_K` has a domain root, then every element of `K` vanishes at that root,
so `K^rf` is empty.

Assume `G_K` is root-free on `D`.  Every `Q in K` can be written uniquely as

```text
Q=G_K R,        deg R<h-gamma_K=m_K.
```

Since `G_K` has no zero on `D`, `Q` is root-free on `D` if and only if `R` is
root-free on `D`.  Thus projective root-free classes in `K` inject into the
projective set of all nonzero root-free polynomials of degree `<m_K`, whose
cardinality is `RFPhi_D(m_K)` by Corollary 40.45.  This proves
(BottomCommonFactorWindow).

If each bottom residual family has residual window at most `L`, monotonicity
of the nested root-free polynomial spaces gives
`RFPhi_D(m_K)<=RFPhi_D(L)` for each of the at most four families.  Summing
over those families and applying Corollary 40.43 gives the displayed
mixed-ladder ledger.

## Corollary 40.57: Common-Factor Bottom Windows Refine The Two-Route Minimum

Keep the notation of Corollaries 40.44--40.56, and assume the
multiplicative-domain setting `0 notin D` of Corollary 40.45.  For each of the
four bottom residual families

```text
F in { u, v, (u,v), (S u,S v) },
```

let `K_0(F)` be the corresponding bottom recurrence kernel from Corollary
40.48.  Define its common-factor bottom-window charge by

```text
b_F=0
```

if `K_0(F)=0` or if `gcd(K_0(F))` has a root in `D`, and otherwise by

```text
b_F = RFPhi_D( h-deg gcd(K_0(F)) ).
```

Put

```text
BCF_0 = sum_F b_F.
```

After the fixed-root/root-slice short recurrence pieces have been charged, the
root-free residual part of the ladder can be closed with the refined ledger

```text
min( BCF_0, Charge(P_pre) + RFArrBudget_hw ) + 2h.      (CFRouteMin)
```

Here `Charge(P_pre)` is any admissible charge for the pre-half-window residual
families, as in Corollary 40.44.  Thus the same M1 ladder has two concrete
residual targets:

1. a bottom common-factor target, which asks for small residual windows
   `h-deg gcd(K_0(F))` in the four bottom kernels;
2. a half-window denominator target, which asks for a small root-free tail
   arrangement, for example through the common-core criteria of Corollaries
   40.46--40.47, together with whatever pre-half charge is used.

In particular, if every nonzero bottom family whose common factor is
root-free on `D` has

```text
h-deg gcd(K_0(F)) <= L,
```

then `BCF_0<=4 RFPhi_D(L)` and the bottom route alone gives the ledger
`4 RFPhi_D(L)+2h`, independently of the half-window arrangement.

### Proof

For each bottom family, Corollary 40.56 gives the bound

```text
|K_0(F)^rf| <= b_F.
```

The cases `K_0(F)=0` and `gcd(K_0(F))` having a domain root both contribute
zero root-free classes by definition and by Corollary 40.56.  Summing over the
four bottom families gives

```text
Charge(B_0) <= BCF_0.
```

Substitute this into the bottom side of Corollary 40.44.  On the split side,
replace the raw half-window arrangement budget by the root-free multiplier
budget `RFArrBudget_hw` from Corollary 40.45, since all remaining residual
certificates are root-free after the fixed-root/root-slice pieces have been
charged.  The finite frontier term is still the `2h` charge from Corollary
40.11.  This proves (CFRouteMin), and the fixed-`L` consequence follows from
monotonicity of `RFPhi_D(m)`.

## Corollary 40.58: Bottom Common-Factor Windows Are Hankel Row-Span Certificates

Keep the notation of Corollary 40.57 and fix `1<=L<=h`.  For a monic
polynomial `G` of degree `g`, let

```text
Rem_G : F_q[X]_{<h} -> F_q[X]_{<g}
```

be the remainder map modulo `G`, written as a `g x h` coefficient matrix in
the monomial bases.  For the four bottom families, write `A_0(F)` for the
bottom matrix defining `K_0(F)=ker A_0(F)`, namely

```text
A_0(u)     = H_{t+r_0,h-1}(u),
A_0(v)     = H_{t+r_0,h-1}(v),
A_0(u,v)   = [ H_{t+r_0-1,h-1}(u) ; H_{t+r_0-1,h-1}(v) ],
A_0(Su,Sv) = [ H_{t+r_0-1,h-1}(S u) ; H_{t+r_0-1,h-1}(S v) ].
```

Then, for each bottom family `F`, the following are equivalent:

1. every element of `K_0(F)` is divisible by `G`;
2. `K_0(F) subset G F_q[X]_{<h-g}`;
3. the remainder rows modulo `G` lie in the row span of the bottom Hankel
   matrix:

```text
row(Rem_G) subset row(A_0(F));                     (BottomRowSpanCert)
```

4. equivalently,

```text
rank A_0(F) = rank [ A_0(F) ; Rem_G ].             (BottomRankCert)
```

Consequently, the condition

```text
h-deg gcd(K_0(F)) <= L
```

from Corollary 40.57 is equivalent, for a nonzero bottom family, to the
existence of a monic polynomial `G_F` with `deg G_F>=h-L` satisfying
(BottomRowSpanCert) for that family.  If such certificates exist for all
nonzero bottom families, then:

* if `G_F` has a domain root, the corresponding root-free bottom family is
  empty;
* otherwise that family contributes at most `RFPhi_D(h-deg G_F)`, hence at
  most `RFPhi_D(L)`.

Thus the bottom side of the refined route minimum closes with

```text
BCF_0 <= 4 RFPhi_D(L),
```

and hence with total ledger `4 RFPhi_D(L)+2h`, whenever each of the four actual
bottom Hankel matrices admits a row-span certificate of degree at least
`h-L`.

This recasts the bottom common-factor target as a finite determinantal
Hankel problem.  For fixed `G`, (BottomRankCert) is a rank equality.  With
unknown coefficients of `G`, it is an explicit incidence condition between
the bottom Hankel row space and the polynomial remainder row space.

### Proof

For a monic `G` of degree `g`, a polynomial `Q` of degree `<h` has
remainder zero modulo `G` if and only if

```text
Q=G R,        deg R<h-g.
```

Thus

```text
ker Rem_G = G F_q[X]_{<h-g}.
```

Since `K_0(F)=ker A_0(F)`, conditions 1 and 2 are just the inclusion

```text
ker A_0(F) subset ker Rem_G.
```

For linear maps on a finite-dimensional vector space, kernel inclusion is
dual to row-space containment:

```text
ker A subset ker B    iff    row(B) subset row(A).
```

Applying this with `A=A_0(F)` and `B=Rem_G` gives
(BottomRowSpanCert), and row-space containment is equivalent to the displayed
rank equality after stacking the rows.

If `K_0(F)` is nonzero and `h-deg gcd(K_0(F))<=L`, choose `G_F` to be the
monic common gcd itself; then `deg G_F>=h-L` and every element of `K_0(F)` is
divisible by `G_F`, so the row-span certificate holds.  Conversely, any such
certificate with `deg G_F>=h-L` forces
`K_0(F) subset G_F F_q[X]_{<h-deg G_F}`, so `G_F` divides every element of
`K_0(F)` and the common gcd has degree at least `h-L`.

The root-free count consequence is the same quotient argument as Corollary
40.56, applied with the certified divisor `G_F`: a domain root of `G_F` kills
every root-free class, while a root-free `G_F` divides all witnesses and leaves
only a
degree-`<h-deg G_F` root-free quotient, which is at most the degree-`<L`
ambient root-free count.  Summing over the four bottom families and then
applying Corollary 40.43 gives the stated bottom-route ledger.

## Corollary 40.59: Split Bottom Certificates Are External-Anchor Row Tests

Keep the notation of Corollary 40.58.  Suppose first that the certified
divisor is squarefree and split over `F_q`:

```text
G(X)=prod_{i=1}^g (X-beta_i),        beta_i distinct.
```

For `beta in F_q`, write

```text
ev_beta=(1,beta,beta^2,...,beta^{h-1}) in (F_q[X]_{<h})^*.
```

Then, for each bottom family `F`,

```text
row(Rem_G) subset row(A_0(F))
```

is equivalent to the `g` external-anchor row tests

```text
ev_{beta_i} in row(A_0(F))        for every i.       (SplitAnchorCert)
```

Consequently, if the common-factor route is to close with a squarefree split
divisor of degree at least `h-L` and with no domain roots for a nonzero bottom
family, then that bottom Hankel row space must contain at least `h-L` distinct
non-domain evaluation rows.  Conversely, any such set of distinct non-domain
anchors gives that family a bottom row-span certificate with residual quotient
window at most `L`.

More generally, if over a splitting field

```text
G(X)=prod_beta (X-beta)^{m_beta},
```

then the same statement holds after scalar extension with `ev_beta` replaced
by the Hasse-jet rows

```text
ev_{beta,j}: Q |-> Q^{[j]}(beta),        0<=j<m_beta,
```

where `Q^{[j]}` denotes the `j`th Hasse derivative.  Thus repeated roots of a
bottom common factor are higher-order external-anchor row tests.

This identifies the row-span certificates of Corollary 40.58 with the
external-anchor geometry used earlier in the boundary-off normal form: a
large split common factor is not an abstract gcd event, but a large collection
of evaluation rows already generated by the bottom Hankel rows.

### Proof

For squarefree split `G`, a polynomial `Q` of degree `<h` is divisible by `G`
if and only if

```text
Q(beta_i)=0        for every i.
```

Thus the remainder map `Rem_G` and the evaluation map

```text
Ev_G : Q |-> (Q(beta_1),...,Q(beta_g))
```

have the same kernel on `F_q[X]_{<h}`.  Both maps have rank `g`, since the
`g x h` Vandermonde matrix on distinct `beta_i` has full row rank.  Therefore
their row spaces are equal:

```text
row(Rem_G)=span{ ev_{beta_1},...,ev_{beta_g} }.
```

Substituting this equality into (BottomRowSpanCert) gives
(SplitAnchorCert).

For the repeated-root variant, over a splitting field the condition
`G | Q` is equivalent to the vanishing of all Hasse derivatives
`Q^{[j]}(beta)` for `0<=j<m_beta` at every root `beta`.  The corresponding
Hermite evaluation matrix has rank `deg G` on polynomials of degree `<h`, so
again it has the same kernel and row space as `Rem_G` after scalar extension.
The row-containment statement follows exactly as in the squarefree case.

## Corollary 40.60: External-Anchor Membership Is Common-Root Duality

Let `A` be any of the four bottom matrices `A_0(F)`, and put

```text
K=ker A subset F_q[X]_{<h}.
```

For `beta in F_q`,

```text
ev_beta in row(A)
```

if and only if every polynomial in `K` vanishes at `beta`, equivalently

```text
X-beta divides gcd(K).                              (AnchorRootDuality)
```

More generally, for `m>=1`, the Hasse-jet rows

```text
ev_{beta,j}: Q |-> Q^{[j]}(beta),        0<=j<m,
```

all lie in `row(A)` if and only if `(X-beta)^m` divides `gcd(K)`.

Consequently, for split certificates, the degree contributed by simple
external anchors is exactly the number of field elements `beta notin D` for
which

```text
rank A = rank [ A ; ev_beta ].                      (AnchorRankTest)
```

Domain anchors satisfying the same rank test are not residual obstructions:
they force every element of `K` to vanish on a domain point and hence empty the
root-free bottom family.

Thus the bottom common-factor search has a direct rank-test form: count the
external points of the rational normal curve already lying in the bottom
Hankel row span, and include Hasse jets for repeated roots.

### Proof

Since `K=ker A`, the row space of `A` is the annihilator `K^perp` inside
`(F_q[X]_{<h})^*`.  Therefore

```text
ev_beta in row(A)
iff
ev_beta(Q)=0 for every Q in K
iff
Q(beta)=0 for every Q in K.
```

The last condition is exactly divisibility of the common gcd of `K` by
`X-beta`.  The Hasse-jet statement is identical: all rows
`ev_{beta,j}` for `0<=j<m` annihilate `K` if and only if every element of `K`
has a root of multiplicity at least `m` at `beta`, equivalently
`(X-beta)^m | gcd(K)`.

The rank test is the row-containment criterion for a single evaluation row.
If `beta in D` satisfies it, then every class in `P(K)` vanishes at the domain
point `beta`, so no class is root-free on `D`.

## Corollary 40.61: Rank-Matched Anchor Spans Give The Exact Bottom Count

Let `A` be any of the four bottom matrices `A_0(F)`, put

```text
K=ker A subset F_q[X]_{<h},        rho=rank A,
```

and assume `K` is nonzero.  If `K=0`, then the corresponding projective
root-free family is empty.  Let `B={beta_1,...,beta_g}` be a set of distinct
non-domain anchors in `F_q\D` such that

```text
ev_{beta_i} in row(A)        for every i.
```

Then `g<=rho`, and with

```text
G_B(X)=prod_{i=1}^g (X-beta_i)
```

one has

```text
G_B divides gcd(K),        K subset G_B F_q[X]_{<h-g}.
```

Consequently the corresponding root-free bottom family satisfies

```text
|K^rf| <= RFPhi_D(h-g).                            (AnchorWindowBound)
```

In particular, if `g>=h-L`, this one family contributes at most
`RFPhi_D(L)` to the bottom route.

If in addition `g=rho`, then

```text
row(A)=span{ev_{beta_1},...,ev_{beta_g}},
K=G_B F_q[X]_{<h-g},
```

and the bound is exact:

```text
|K^rf| = RFPhi_D(h-g).                             (RankMatchedAnchorExact)
```

Thus a rank-`h-L` bottom Hankel row space spanned by `h-L` non-domain
evaluation rows gives the exact ideal residual charge `RFPhi_D(L)`.  Summed
over the four bottom families, rank-matched external-anchor spans give the
bottom route ledger

```text
sum_F RFPhi_D(h-g_F) + 2h,
```

with the usual convention that any family whose row span contains a domain
evaluation row has empty root-free contribution.

### Proof

Since `K` is nonzero, `rho<h`.  If `g>rho`, choose any `rho+1` of the
evaluation rows.  These `rho+1<=h` distinct rows are linearly independent by
the Vandermonde determinant, contradicting that they all lie in the
`rho`-dimensional row space of `A`.  Hence `g<=rho`.

By Corollary 40.60, each row-containment condition says that `X-beta_i`
divides `gcd(K)`.  The roots are distinct, so their product `G_B` divides
`gcd(K)`, giving the inclusion `K subset G_B F_q[X]_{<h-g}`.  Since the
anchors are outside `D`, `G_B` is root-free on `D`, and the quotient argument
of Corollary 40.56 gives (AnchorWindowBound).

If `g=rho`, the independent rows `ev_{beta_i}` form a basis of `row(A)`.
Therefore `A` and the evaluation map at `B` have the same kernel.  That kernel
is precisely the set of degree-`<h` polynomials divisible by `G_B`, namely
`G_B F_q[X]_{<h-g}`.  Because `G_B` has no root in `D`, multiplication by
`G_B` bijects root-free quotient classes of degree `<h-g` with root-free
classes in `K`, proving the exact count.

## Corollary 40.62: Bottom Anchors Are Truncated Moment Certificates

Let `s>=1` and let `w` be a syndrome sequence long enough to form
`H_{s,h-1}(w)`.  For `beta in F_q`,

```text
ev_beta in row H_{s,h-1}(w)
```

if and only if there is a polynomial

```text
C(X)=c_0+c_1X+...+c_{s-1}X^{s-1}
```

such that

```text
sum_{a=0}^{s-1} c_a w_{a+b} = beta^b,        0<=b<h.       (ScalarAnchorMoment)
```

If, on the needed range, the syndrome has a moment expansion

```text
w_m=sum_{x in D} mu_x x^m,
```

then this is equivalently the truncated quadrature identity

```text
sum_{x in D} mu_x C(x) x^b = beta^b,        0<=b<h.        (ScalarQuadrature)
```

For a stacked paired bottom matrix

```text
A=[ H_{s,h-1}(u) ; H_{s,h-1}(v) ],
```

the condition `ev_beta in row(A)` is equivalent to the existence of two
polynomials `C_u,C_v` of degree `<s` such that

```text
sum_{a=0}^{s-1} c_{u,a} u_{a+b}
+ sum_{a=0}^{s-1} c_{v,a} v_{a+b}
= beta^b,        0<=b<h.                            (PairAnchorMoment)
```

If

```text
u_m=sum_{x in D} mu_x x^m,        v_m=sum_{x in D} nu_x x^m,
```

then this becomes

```text
sum_{x in D} ( mu_x C_u(x)+nu_x C_v(x) ) x^b
= beta^b,        0<=b<h.                            (PairQuadrature)
```

For the shifted paired matrix `[ H_{s,h-1}(S u) ; H_{s,h-1}(S v) ]`, the same
formula holds after replacing the weights `(mu_x,nu_x)` by
`(x mu_x,x nu_x)`.

Thus the non-domain anchor counts in Corollary 40.61 are not abstract
row-span coincidences: they are exactly short multiplier representations of
external point masses by the bottom syndrome moments.  In the four bottom
families one uses `s=t+r_0` for the scalar families and `s=t+r_0-1` for the
ordinary and shifted paired families.

### Proof

A row vector is in `row H_{s,h-1}(w)` precisely when it is a linear
combination of the rows.  Writing the coefficients as `c_0,...,c_{s-1}`, the
`b`-th coordinate of that linear combination is

```text
sum_{a=0}^{s-1} c_a w_{a+b}.
```

Equating this row with `ev_beta=(1,beta,...,beta^{h-1})` gives
(ScalarAnchorMoment).  If `w_m=sum_x mu_x x^m`, then

```text
sum_a c_a w_{a+b}
= sum_a c_a sum_x mu_x x^{a+b}
= sum_x mu_x C(x)x^b,
```

which proves (ScalarQuadrature).

The stacked paired statement is the same row-space computation with two
independent row combinations, one from the `u` block and one from the `v`
block.  Substituting the moment expansions gives (PairQuadrature).  Finally,
`(S w)_m=w_{m+1}=sum_x (x mu_x)x^m`, so the shifted paired case is the same
calculation with the displayed shifted weights.

## Corollary 40.63: Full-Domain Moment Windows Become Lagrange Degree Tests

Assume `D subset F_q` has size `n`, and let

```text
L_D(X)=prod_{x in D}(X-x).
```

For `beta notin D`, define the Lagrange weights

```text
lambda_beta(x)=prod_{y in D, y!=x} (beta-y)/(x-y)
              = L_D(beta)/((beta-x)L_D'(x)),        x in D.
```

Let the scalar syndrome sequence have moment form

```text
w_m=sum_{x in D} mu_x x^m.
```

If `h=n`, then

```text
ev_beta in row H_{s,n-1}(w)
```

if and only if there is a polynomial `C` of degree `<s` such that

```text
mu_x C(x)=lambda_beta(x)        for every x in D.   (ScalarLagrangeAnchor)
```

In particular, if any `mu_x=0`, no non-domain scalar anchor exists in the
full-domain moment window.  If all `mu_x` are nonzero, the condition is exactly
that the unique interpolant of the values `lambda_beta(x)/mu_x` on `D` has
degree `<s`.

For a paired bottom matrix with moment weights `(mu_x,nu_x)`, the full-domain
condition is

```text
mu_x C_u(x)+nu_x C_v(x)=lambda_beta(x)        for every x in D,       (PairLagrangeAnchor)
```

for some `deg C_u,deg C_v<s`.  For the shifted paired matrix, replace
`(mu_x,nu_x)` by `(x mu_x,x nu_x)`.

If `h>=n+1`, then no non-domain external anchor can lie in any row span coming
from `D`-supported moment data of the form in Corollary 40.62.  Equivalently,
all non-domain bottom-anchor certificates are confined to the short window
`h<=n`.

### Proof

For every polynomial `P` of degree `<n`, Lagrange interpolation gives

```text
P(beta)=sum_{x in D} lambda_beta(x) P(x).
```

Taking `P(X)=X^b` for `0<=b<n` shows that the vector
`(lambda_beta(x))_{x in D}` is the unique `D`-supported weight vector whose
first `n` moments are `(1,beta,...,beta^{n-1})`: uniqueness follows from the
invertibility of the `n x n` Vandermonde matrix on `D`.

Thus the scalar identity in Corollary 40.62 with `h=n` is equivalent to
`mu_x C(x)=lambda_beta(x)` for all `x in D`.  The paired and shifted paired
statements are the same uniqueness argument applied to the combined weights
`mu_x C_u(x)+nu_x C_v(x)` and, respectively,
`x mu_x C_u(x)+x nu_x C_v(x)`.

Finally suppose `h>=n+1` and a `D`-supported weight vector matched the first
`h` moments of `beta`.  The first `n` moments force the weights to be
`lambda_beta(x)`.  For the next moment, reduce `X^n` modulo the monic
polynomial `L_D`:

```text
X^n = L_D(X) + R(X),        deg R<n.
```

Since `L_D(x)=0` for `x in D`,

```text
sum_{x in D} lambda_beta(x)x^n
= sum_{x in D} lambda_beta(x)R(x)
= R(beta)
= beta^n-L_D(beta),
```

which is not `beta^n` because `beta notin D`.  Hence the first `n+1` moments
cannot match.

## Corollary 40.64: Full-Domain Paired Anchors Have A Dual Common-Zero Test

Keep the full-domain notation of Corollary 40.63 with `h=n=|D|`.  For weights
`mu_x,nu_x` on `D`, define the paired short-multiplier value space

```text
W_{mu,nu,s}
={ (mu_x C_u(x)+nu_x C_v(x))_{x in D} :
   deg C_u<s, deg C_v<s } subset F_q^D.
```

Define its polynomial dual annihilator

```text
Ann_{mu,nu,s}
={ P in F_q[X]_{<n} :
   sum_{x in D} P(x) mu_x x^a = 0 and
   sum_{x in D} P(x) nu_x x^a = 0,        0<=a<s }.
```

Then for `beta notin D`,

```text
lambda_beta in W_{mu,nu,s}
```

if and only if

```text
P(beta)=0        for every P in Ann_{mu,nu,s}.       (DualAnchorTest)
```

Equivalently, if `Ann_{mu,nu,s}` is nonzero and

```text
G_{mu,nu,s}=gcd( P : P in Ann_{mu,nu,s} ),
```

then the non-domain paired anchors are exactly the roots of `G_{mu,nu,s}` in
`F_q\D`.  In particular their number is at most `deg G_{mu,nu,s}`.  If
`Ann_{mu,nu,s}=0`, then `W_{mu,nu,s}=F_q^D`, so every non-domain `beta` passes
the paired full-domain anchor test; in the bottom-kernel interpretation this
is the full-row-rank case and the paired kernel is zero.

The scalar full-domain test is the special case obtained by deleting the
`nu` equations and the multiplier `C_v`.  The shifted paired test is obtained
by replacing `(mu_x,nu_x)` with `(x mu_x,x nu_x)`.

Thus the full-domain paired anchor problem is a common-zero problem for an
explicit low-moment annihilator space.  Counting anchors is equivalent to
bounding the degree of its common gcd, unless the bottom row space is already
full rank.

### Proof

Use the standard dot product on `F_q^D`.  The orthogonal complement of
`W_{mu,nu,s}` consists exactly of value vectors `(P(x))_{x in D}`, with
`deg P<n`, such that

```text
sum_{x in D} P(x) mu_x C_u(x)=0,
sum_{x in D} P(x) nu_x C_v(x)=0
```

for every `deg C_u,deg C_v<s`.  Testing on the monomials `X^a`,
`0<=a<s`, gives precisely `Ann_{mu,nu,s}`.  Therefore
`lambda_beta in W_{mu,nu,s}` if and only if it pairs to zero with every
`P in Ann_{mu,nu,s}`.

By Lagrange interpolation, for every `P` of degree `<n`,

```text
sum_{x in D} lambda_beta(x)P(x)=P(beta).
```

Hence the orthogonality condition is exactly (DualAnchorTest).  If the
annihilator is nonzero, common vanishing of all its polynomials at `beta` is
equivalent to vanishing of their gcd.  If the annihilator is zero, the
orthogonal complement of `W_{mu,nu,s}` is zero, hence `W_{mu,nu,s}=F_q^D`.

## Corollary 40.65: Short-Window Paired Anchors Have The Same Dual Test

Let `D subset F_q`, let `1<=h<=|D|`, and keep the paired moment notation of
Corollary 40.62.  Define the truncated moment map

```text
M_h(q)=( sum_{x in D} q_x x^b )_{0<=b<h} in F_q^h
```

and the paired short-multiplier value space

```text
W_{mu,nu,s}
={ (mu_x C_u(x)+nu_x C_v(x))_{x in D} :
   deg C_u<s, deg C_v<s } subset F_q^D.
```

Define the short-window polynomial annihilator

```text
Ann_{mu,nu,s}^{(h)}
={ P in F_q[X]_{<h} :
   sum_{x in D} P(x) mu_x x^a = 0 and
   sum_{x in D} P(x) nu_x x^a = 0,        0<=a<s }.
```

Then, for any `beta in F_q`, the paired truncated anchor identity

```text
(1,beta,...,beta^{h-1}) in M_h(W_{mu,nu,s})
```

holds if and only if

```text
P(beta)=0        for every P in Ann_{mu,nu,s}^{(h)}.        (ShortDualAnchorTest)
```

Consequently, if `Ann_{mu,nu,s}^{(h)}` is nonzero and

```text
G_{mu,nu,s}^{(h)}=gcd( P : P in Ann_{mu,nu,s}^{(h)} ),
```

then the non-domain paired anchors in the short window are exactly the roots
of `G_{mu,nu,s}^{(h)}` in `F_q\D`, and their number is at most
`deg G_{mu,nu,s}^{(h)}`.  If `Ann_{mu,nu,s}^{(h)}=0`, then
`M_h(W_{mu,nu,s})=F_q^h`, so every `beta in F_q` passes the truncated paired
moment test.

The scalar version is obtained by deleting the `nu` equations and the
multiplier `C_v`, and the shifted paired version is obtained by replacing
`(mu_x,nu_x)` with `(x mu_x,x nu_x)`.  For `h=|D|`, Corollary 40.64 is the
same statement transported through the full Vandermonde isomorphism and
written in Lagrange coordinates.

Thus the genuinely short-window bottom-anchor search is also a common-gcd
problem: count non-domain roots of a concrete degree-`<h` low-moment
annihilator space.  This is the direct dual target for proving or falsifying
the anchor-span route of Corollary 40.61.

### Proof

The dual of `F_q^h` is identified with polynomials

```text
P(X)=p_0+p_1X+...+p_{h-1}X^{h-1}
```

by pairing `P` with a moment vector `m=(m_b)` as `sum_b p_b m_b`.  Such a
polynomial annihilates `M_h(W_{mu,nu,s})` if and only if

```text
sum_{x in D} P(x)(mu_x C_u(x)+nu_x C_v(x))=0
```

for every `deg C_u,deg C_v<s`, which is equivalent to the displayed moment
conditions defining `Ann_{mu,nu,s}^{(h)}`.

A vector belongs to a subspace of `F_q^h` if and only if every functional
annihilating that subspace also annihilates the vector.  Applying this to
`(1,beta,...,beta^{h-1})` gives exactly `P(beta)=0` for every polynomial in
the annihilator.  The common-gcd and zero-annihilator consequences are
immediate.

## Corollary 40.66: Dual GCD Degrees Give A Bottom-Route Ledger

Assume the bottom syndrome sequences have moment expansions on the needed
range

```text
u_m=sum_{x in D} mu_x x^m,        v_m=sum_{x in D} nu_x x^m.
```

Let `s_1=t+r_0` for the scalar bottom families and `s_2=t+r_0-1` for the
paired bottom families.  Define four short-window annihilator spaces:

```text
Ann_u
={ P in F_q[X]_{<h} :
   sum_{x in D} P(x) mu_x x^a=0,        0<=a<s_1 },

Ann_v
={ P in F_q[X]_{<h} :
   sum_{x in D} P(x) nu_x x^a=0,        0<=a<s_1 },

Ann_uv
={ P in F_q[X]_{<h} :
   sum_{x in D} P(x) mu_x x^a=0 and
   sum_{x in D} P(x) nu_x x^a=0,        0<=a<s_2 },

Ann_Suv
={ P in F_q[X]_{<h} :
   sum_{x in D} P(x) mu_x x^{a+1}=0 and
   sum_{x in D} P(x) nu_x x^{a+1}=0,    0<=a<s_2 }.
```

For each family `F in {u,v,uv,Suv}`, if `Ann_F=0`, set `a_F=infty` and
declare the corresponding bottom family empty.  Otherwise let

```text
G_F=gcd(P : P in Ann_F).
```

If `G_F` has a root in `D`, the corresponding root-free bottom family is
empty.  If not, let

```text
a_F = #{ beta in F_q\D : G_F(beta)=0 }.
```

Then the four bottom root-free families have residual charge at most

```text
sum_{F : Ann_F!=0, G_F root-free on D} RFPhi_D(h-a_F).      (DualGCDBottomCharge)
```

and the bottom route closes with total ledger

```text
sum_F RFPhi_D(h-a_F) + 2h,                         (DualGCDBottomLedger)
```

where empty families contribute zero.  In particular, if every nonempty
root-free family has `a_F>=h-L`, then the bottom route closes with

```text
4 RFPhi_D(L) + 2h.
```

Thus one sufficient way to close the bottom common-factor route is to prove
that each nonzero dual annihilator has many distinct non-domain common roots,
or a domain common root, in these four explicit low-moment annihilator spaces.

### Proof

By Corollary 40.65, for the paired family `(u,v)` the anchors in `F_q` are
exactly the common roots of `Ann_uv`; the shifted family is the same statement
with weights `(x mu_x,x nu_x)`.  The scalar version is the scalar specialization
of the same duality.  Thus a root of `G_F` in `D` puts a domain evaluation row
in the corresponding bottom row span, so Corollary 40.60 empties the root-free
family.

If `Ann_F=0`, the corresponding truncated moment image is all of `F_q^h`, so
the bottom row space has rank `h` and its kernel is zero.  Hence that
projective bottom family is empty.

In the remaining case, the `a_F` distinct non-domain roots of `G_F` are
non-domain external-anchor rows in the bottom row span.  Corollary 40.61
therefore bounds that family by `RFPhi_D(h-a_F)`.  Summing over the four
families and applying the bottom residual route of Corollary 40.43 gives the
displayed ledgers.

## Corollary 40.67: The Dual-GCD Root Bound Is Extra Structure

The lower bound on the number of common roots in Corollary 40.66 is not a
formal consequence of the moment-dual setup alone.

Let `D subset F_q` have size `n`, let `s>=1`, and assume

```text
n>=s+2,        h>=2.
```

Then there is a nonzero weight vector `(mu_x)_{x in D}` such that the scalar
annihilator

```text
Ann_mu={ P in F_q[X]_{<h} :
         sum_{x in D} P(x) mu_x x^a=0,        0<=a<s }
```

has common gcd equal to `1`.  In particular, the scalar dual-gcd ledger gives
`a=0` for this formal moment datum.

The same obstruction occurs for the ordinary paired annihilator: there are
nonzero weights `mu_x,nu_x` such that

```text
Ann_{mu,nu,s}^{(h)}
```

contains both `1` and `X`, hence has common gcd `1`.  If additionally
`0 notin D`, the same is true for the shifted paired annihilator after
replacing the moment conditions by the shifted conditions of Corollary 40.66.

Therefore the dual-gcd bottom route is a genuine structural target.  It cannot
be closed by dimension counting, by the Hankel row-span formalism, or by the
existence of moment expansions alone; one must prove special common-root
structure for the actual M1 bottom syndromes, or else use the half-window
denominator route.

### Proof

The `s+1` linear conditions

```text
sum_{x in D} mu_x x^m=0,        0<=m<=s,
```

on the `n` unknowns `mu_x` have a nonzero solution because `n>=s+2`.  For such
a solution, both `P=1` and `P=X` lie in `Ann_mu`: the conditions for `1` are
the moments `0,...,s-1`, and the conditions for `X` are the moments
`1,...,s`.  Since `gcd(1,X)=1`, the common gcd of `Ann_mu` is `1`.

For the ordinary paired case, take any two nonzero solutions of the same
homogeneous system, for instance `mu=nu` equal to the scalar solution above.
Then `1` and `X` satisfy both the `mu` and `nu` moment conditions, so the
paired annihilator again has common gcd `1`.

For the shifted paired case with `0 notin D`, solve instead

```text
sum_{x in D} mu_x x^m=0,        1<=m<=s+1.
```

These are again at most `s+1` independent conditions on `n>=s+2` unknowns, so
there is a nonzero solution.  The shifted conditions for `P=1` use moments
`1,...,s`, and the shifted conditions for `P=X` use moments `2,...,s+1`.
Taking `mu=nu` gives `1,X` in the shifted paired annihilator, so its common
gcd is also `1`.

## Corollary 40.68: The Trivial Dual-GCD Obstruction Is Syndrome-Realizable

Keep the notation of Corollary 40.67.  In the standard Reed-Solomon
parity-check normalization, the syndrome coordinates of a word supported on
`D` have the form

```text
w_m=sum_{x in D} lambda_x y_x x^m,
```

where every column scalar `lambda_x` is nonzero.  Thus, after writing
`mu_x=lambda_x y_x`, every `D`-supported weight vector `(mu_x)` occurs as an
actual local syndrome moment sequence on any finite coordinate range contained
in the available syndrome window.

Consequently the scalar, ordinary paired, and, when `0 notin D`, shifted
paired trivial-gcd data constructed in Corollary 40.67 can be realized by
local Reed-Solomon syndrome windows whenever the required moments lie in the
available syndrome range.

This does not construct an active noncontained M1 bad line, and it does not
show that the four bottom families of Corollary 40.66 can be chosen
arbitrarily inside the active M1 geometry.  It only shows that the obstruction
in Corollary 40.67 is not an artifact of allowing formal moment sequences:
the dual-gcd route must use additional active-M1 structure tying together the
bottom syndrome windows, or else pass to the half-window denominator route.

### Proof

The parity-check column at `x` is `lambda_x(1,x,...,x^{r-1})` with
`lambda_x!=0`.  Given any weights `(mu_x)`, choose the supported word

```text
y_x=mu_x/lambda_x        (x in D).
```

Then its syndrome coordinates on the relevant range are

```text
Syn(y)_m=sum_{x in D} lambda_x y_x x^m
        =sum_{x in D} mu_x x^m.
```

The same argument applied to two supported words realizes arbitrary paired
weights `(mu_x,nu_x)`.  Applying it to the shifted weights used in
Corollary 40.67 realizes the shifted paired obstruction when `0 notin D`.

## Corollary 40.69: Half-Window Denominator Degree Is A Low-Degree Kernel Test

Return to the half-window notation of Corollaries 40.14--40.18, and assume
`R_hw` is nonempty with cutoff depth `r_hw`.  For a residual family

```text
F in { u, v, (u,v), (S u,S v) },
```

let `A_F(m)` denote the cutoff Hankel recurrence map on degree-`<m`
directions:

```text
A_u(m)       = H_{t+r_hw,m-1}(u),
A_v(m)       = H_{t+r_hw,m-1}(v),
A_uv(m)      = ( H_{t+r_hw-1,m-1}(u),
                 H_{t+r_hw-1,m-1}(v) ),
A_Suv(m)     = ( H_{t+r_hw-1,m-1}(S u),
                 H_{t+r_hw-1,m-1}(S v) ).
```

For an active family `F`, let `D_F` be its cutoff primitive denominator and
put `delta_F=deg D_F`.  For an inactive family set `delta_F=infty`.

Then, for every `1<=m<=h`,

```text
delta_F < m
```

if and only if `ker A_F(m)` contains a nonzero polynomial `Q` with no root in
`D`.  Equivalently,

```text
delta_F >= m
```

if and only if there is no degree-`<m` root-free cutoff recurrence in the
family `F`.

Consequently, with `m=h-L` and `0<=L<h`, the half-window denominator target

```text
delta_F >= h-L        for every active F
```

is exactly the absence of root-free low-degree cutoff kernels

```text
there is no 0!=Q in ker A_F(h-L) with Q(alpha)!=0 for all alpha in D
```

for the four families.  A useful sufficient linear test is the stronger
condition

```text
ker A_F(h-L)=0        for every F.                  (HWLowDegreeInject)
```

Under (HWLowDegreeInject), every active primitive denominator has degree at
least `h-L`.  In the multiplicative-domain setting of Corollary 40.45, the
root-free half-window arrangement therefore satisfies

```text
RFArrBudget_hw <= 4 RFPhi_D(L),
```

and the residual route from Corollary 40.57 gives

```text
min(BCF_0, Charge(P_pre)+4 RFPhi_D(L)) + 2h.
```

Thus the half-window side of the M1 residual bottleneck can be attacked by a
finite Hankel-rank problem at the single cutoff depth: prove there are no
low-degree root-free denominator recurrences, or prove the stronger
injectivity of the four displayed truncated maps.

### Proof

Assume first that `delta_F<m`.  By Corollary 40.8, equivalently Corollary 61,
the primitive denominator remains a valid root-free certificate after
cancelling multipliers.  Let `Q_F` be the reversal of `D_F`.  Then `Q_F` has
degree `delta_F<m`, has no root in `D`, and lies in `ker A_F(m)`.

Conversely, suppose `0!=Q in ker A_F(m)` has no root in `D`, and write
`e=deg Q<m`.  Since `m<=h` and the cutoff is in the half-window range, this
is one of the cutoff denominator certificates covered by Corollary 40.8.
Corollary 59 gives a unique reduced scalar or vector rational function for
the family, and its primitive denominator divides the reversed denominator
`Q^*`.  Hence `delta_F<=e<m`.  This proves the equivalence.

Putting `m=h-L` gives the displayed low-degree root-free kernel criterion.
If the stronger linear injectivity condition holds, then certainly no
root-free low-degree kernel exists, so all active `delta_F` are at least
`h-L`.  Equivalently, the residual tail parameter of Corollary 40.46 is at
most `L`, so that corollary gives
`RFArrBudget_hw<=4 RFPhi_D(L)`, and Corollary 40.57 substitutes this
half-window charge into the two-route residual minimum.

## Corollary 40.70: Half-Window Low-Degree Kernels Have A Root-Slice Count

Keep the notation of Corollary 40.69.  Put

```text
K_F(m)=ker A_F(m)
```

for one of the four cutoff families.  For `J subset D`, define

```text
K_F(m)(-J)={ Q in K_F(m) : Q(alpha)=0 for every alpha in J }.
```

Let `K_F(m)^rf` be the projective set of nonzero classes in `K_F(m)` with no
root in `D`.  Then

```text
|K_F(m)^rf|
 = sum_{J subset D} (-1)^{|J|} Phi(dim K_F(m)(-J)),       (HWKernelRFIE)
```

where `Phi(0)=0`, so terms with `|J|>=m` vanish.

Moreover these root slices are themselves cutoff Hankel kernels after
stripping domain roots.  If `a=|J|<m` and

```text
L_J(X)=prod_{alpha in J}(X-alpha),
```

then multiplication by `L_J` identifies `K_F(m)(-J)` with the corresponding
stripped kernel of degree `<m-a`:

```text
K_{u,J}(m-a)
  = ker H_{t+r_hw,m-a-1}(Delta_J u),

K_{v,J}(m-a)
  = ker H_{t+r_hw,m-a-1}(Delta_J v),

K_{uv,J}(m-a)
  = ker H_{t+r_hw-1,m-a-1}(Delta_J u)
    cap ker H_{t+r_hw-1,m-a-1}(Delta_J v),

K_{Suv,J}(m-a)
  = ker H_{t+r_hw-1,m-a-1}(S Delta_J u)
    cap ker H_{t+r_hw-1,m-a-1}(S Delta_J v).
```

Thus the exact half-window low-degree obstruction is computable from stripped
root-slice ranks:

```text
|K_F(m)^rf|
 = sum_{J subset D, |J|<m} (-1)^{|J|}
     Phi(dim K_{F,J}(m-|J|)).                       (HWStrippedRFIE)
```

Consequently, for `m=h-L`, the family `F` satisfies `delta_F>=h-L` if and
only if the right-hand side of (HWStrippedRFIE) is zero.  The four-family
half-window target is therefore an exact finite root-slice rank identity, not
only the stronger injectivity condition (HWLowDegreeInject).

### Proof

The first formula is inclusion-exclusion on the projective space `P(K_F(m))`
over the events

```text
Q(alpha)=0,        alpha in D.
```

For a fixed `J`, the intersection of these events is `P(K_F(m)(-J))`, whose
size is `Phi(dim K_F(m)(-J))`.  If `|J|>=m`, no nonzero polynomial of degree
`<m` can vanish on all of `J`, so the term is zero.

For the stripped-kernel identification, every `Q in K_F(m)(-J)` has a unique
factorization `Q=L_J R` with `deg R<m-|J|`.  Corollary 49 gives

```text
H_{s,m-1}(w)(L_J R)=0
iff
H_{s,m-|J|-1}(Delta_J w)R=0
```

for each scalar Hankel equation.  Applying this componentwise gives the
ordinary paired case.  For the shifted paired case use

```text
Delta_alpha(Sw)=S(Delta_alpha w)
```

and iterate over `J`.  Substituting these isomorphic stripped kernels into
(HWKernelRFIE) gives (HWStrippedRFIE).

Finally, Corollary 40.69 says `delta_F<h-L` if and only if
`K_F(h-L)^rf` is nonempty.  Since a finite projective set is empty exactly
when its cardinality is zero, (HWStrippedRFIE) gives the displayed exact
criterion.

## Corollary 40.71: Over Small Domains, Low-Degree Injectivity Is Exact Modulo Fixed Roots

Let `D subset F_q` satisfy `|D|<q`, and let

```text
K subset F_q[X]_{<m}
```

be any linear subspace.  Let `K^rf` be the projective set of nonzero classes
`[Q] in P(K)` such that `Q(alpha)!=0` for every `alpha in D`.

Then

```text
K^rf=emptyset
```

if and only if either `K=0`, or the common gcd of all polynomials in `K` has a
root in `D`.  Equivalently, if `K` is nonzero and has no common domain root,
then `K` contains a root-free polynomial.

Applied to the half-window cutoff kernels `K_F(m)=ker A_F(m)` of Corollary
40.70, this says that in the multiplicative-domain regime `0 notin D`:

```text
K_F(h-L)^rf=emptyset
```

if and only if either `K_F(h-L)=0`, or `K_F(h-L)` is wholly contained in the
fixed-root slice for some `alpha in D`.  Therefore, after the fixed-root and
root-slice pieces from Corollary 40.6 have been charged, the half-window
target

```text
delta_F >= h-L
```

is equivalent to the plain injectivity condition

```text
ker A_F(h-L)=0
```

on the remaining ledger.  The injectivity target of Corollary 40.69 is thus
not merely a sufficient shortcut in this range; it is exact modulo the
already-separated fixed-root/root-slice charges.

### Proof

If `K=0`, then `P(K)` is empty.  If the common gcd of `K` has a root
`alpha in D`, then every polynomial in `K` vanishes at `alpha`, so no
nonzero class in `P(K)` is root-free.

Conversely, assume `K` is nonzero and has no common root in `D`.  For each
`alpha in D`, the evaluation functional

```text
ev_alpha: K -> F_q,        Q |-> Q(alpha)
```

is nonzero, so its kernel is a proper hyperplane in the `d=dim K` dimensional
vector space `K`.  Each such hyperplane has `q^{d-1}` vectors.  Since
`|D|<q`,

```text
| union_{alpha in D} ker ev_alpha |
  <= |D| q^{d-1}
  < q^d
  = |K|.
```

Thus some `Q in K` lies outside every `ker ev_alpha`; this `Q` has no root in
`D`, so `[Q] in K^rf`.

For the half-window application, take `K=K_F(h-L)`.  A common domain root is
exactly the fixed-root/root-slice alternative isolated by Corollary 40.6 and
stripped in Corollary 40.70.  Once those pieces are charged, the only way for
`K_F(h-L)^rf` to be empty is `K_F(h-L)=0`.  Corollary 40.69 identifies this
root-free emptiness with the denominator threshold `delta_F>=h-L`.

## Corollary 40.72: Four Cutoff Minors Close The Half-Window Route

Keep the notation of Corollaries 40.69--40.71, assume `|D|<q`, and put

```text
m=h-L,        0<=L<h.
```

At the cutoff depth `r_hw`, form the four matrices representing

```text
A_u(m),        A_v(m),        A_uv(m),        A_Suv(m)
```

on the monomial basis of degree-`<m` polynomials.  Under the standing
half-window hypothesis `h<=t+r_hw` and `t>=2`, each of these four matrices has
at least `m` rows:

```text
t+r_hw >= m,
2(t+r_hw-1) >= m.
```

Suppose that, for each of the four families, at least one `m x m`
full-column minor of `A_F(m)` is nonzero.  Equivalently,

```text
ker A_F(m)=0        for F in {u,v,(u,v),(S u,S v)}.
```

Then every active half-window primitive denominator satisfies

```text
deg D_F >= h-L.
```

Consequently, in the multiplicative-domain root-free ledger,

```text
RFArrBudget_hw <= 4 RFPhi_D(L),
```

and the residual bottleneck from Corollary 40.57 closes with

```text
min(BCF_0, Charge(P_pre)+4 RFPhi_D(L)) + 2h.        (CutoffMinorLedger)
```

Conversely, after the fixed-root/root-slice recurrence pieces have been
charged, failure of full column rank for one of the four `A_F(m)` is exactly a
remaining low-degree half-window obstruction for that family: either it was a
charged common-domain-root slice, or it contains a root-free degree-`<m`
recurrence and hence has `deg D_F<m`.

Thus the half-window route has a finite, scanner-ready target at the single
cutoff depth: prove one full-column minor nonzero for each of the four
displayed Hankel matrices after fixed-root pieces are separated.

### Proof

The row-count inequalities follow from `m<=h<=t+r_hw`; for the paired maps,
the standing `t>=2` gives `t+r_hw>=2`, hence

```text
2(t+r_hw-1) >= t+r_hw >= m.
```

Full column rank of `A_F(m)` is equivalent to nonvanishing of some `m x m`
full-column minor, and also to `ker A_F(m)=0`.  Corollary 40.69 then gives
`deg D_F>=m=h-L` for every active family.  Corollary 40.46 gives the
root-free arrangement bound, and Corollary 40.57 substitutes it into the
two-route residual minimum.

For the converse on the charged-free ledger, if `ker A_F(m)` is nonzero and
has a common root in `D`, it is one of the fixed-root/root-slice recurrence
pieces already separated by Corollary 40.6.  If it has no common domain root,
Corollary 40.71 gives a root-free element of `ker A_F(m)`, and Corollary 40.69
identifies this with `deg D_F<m`.  Hence, once fixed-root pieces are removed,
rank failure is exactly the low-degree half-window residual.

## Corollary 40.73: The Cutoff-Minor Target Is Extra M1 Structure

The four cutoff-minor conditions in Corollary 40.72 are not consequences of
the Hankel or local syndrome formalism alone.

Let `D subset F_q` have size `n`, fix `s>=1`, and assume

```text
n>=s+1.
```

Then there is a nonzero weight vector `(mu_x)_{x in D}` such that

```text
sum_{x in D} mu_x x^a=0,        0<=a<s.
```

For the local moment sequence

```text
w_a=sum_{x in D} mu_x x^a,
```

the constant polynomial `Q=1` is root-free on `D` and lies in

```text
ker H_{s,m-1}(w)
```

for every `m>=1`.  Consequently, at a half-window cutoff with
`s_c=t+r_hw`, if `n>=s_c+1` and one sets `u=v=w` with the first `s_c` moments
vanishing, then `Q=1` lies in all four cutoff kernels

```text
A_u(m),        A_v(m),        A_uv(m),        A_Suv(m)
```

for every `m>=1`.  In particular all four full-column minor targets of
Corollary 40.72 can fail simultaneously for local moment data, with a
root-free low-degree recurrence.

Moreover this obstruction is realizable by local Reed-Solomon syndrome data:
after absorbing the nonzero parity-check column scalars as in Corollary 40.68,
choose the supported word values `y_x=mu_x/lambda_x`.

Thus the cutoff-minor route cannot be closed by row counts, moment expansions,
or generic syndrome normalization alone.  Any proof of the four minors in the
actual M1 problem must use the active noncontained line geometry, quotient or
aperiodic restrictions, or another structural input beyond arbitrary local
syndrome windows.

This does not construct an active noncontained M1 counterexample; it only
shows that the scanner-ready minor targets of Corollary 40.72 are genuine
M1-specific obligations.

### Proof

The `s` displayed moment conditions are homogeneous linear equations in the
`n>=s+1` unknowns `mu_x`, so they have a nonzero solution.  For the resulting
moment sequence, `w_0,...,w_{s-1}` all vanish.  Therefore

```text
H_{s,m-1}(w)1 = 0
```

for every `m>=1`.  The polynomial `1` has no root in `D`.

At the cutoff, the scalar maps use `H_{s_c,m-1}(u)` and
`H_{s_c,m-1}(v)`, while the ordinary paired map uses the first `s_c-1` rows
of both `u` and `v`.  The shifted paired map uses rows

```text
w_1,...,w_{s_c-1}.
```

All these entries vanish when the first `s_c` moments vanish and `u=v=w`, so
`Q=1` lies in all four kernels.  Corollary 40.68 supplies the syndrome
realization by choosing supported word coefficients with
`lambda_x y_x=mu_x`.

## Corollary 40.74: Cutoff Kernel Failure Is A Rational-Supercode Stratum

Let `0<=s<=r`, and write

```text
C^{(s)} = RS[F,D,n-s]
```

for the Reed-Solomon supercode cut out by the first `s` syndrome checks.  Thus
for any word `y:D->F`,

```text
y in C^{(s)}
iff
Syn(y)_a=0,        0<=a<s.
```

Let `w=Syn(y)` and let `Q in F[X]_{<m}`.  Then

```text
H_{s,m-1}(w)Q=0
```

if and only if the pointwise product word

```text
(Qy)(x)=Q(x)y(x)
```

lies in `C^{(s)}`.  If `Q` is root-free on `D`, this is equivalently a
rational-supercode representation

```text
y(x)=P(x)/Q(x)        on D,        deg P<n-s.
```

At the half-window cutoff `r_hw`, put `s_0=t+r_hw` and `s_1=t+r_hw-1`.  For a
root-free `Q` of degree `<m`, the four cutoff kernels have the following
coding interpretation:

```text
Q in ker A_u(m)       iff Qf in C^{(s_0)},
Q in ker A_v(m)       iff Qg in C^{(s_0)},
Q in ker A_uv(m)      iff Qf,Qg in C^{(s_1)},
Q in ker A_Suv(m)     iff XQf,XQg in C^{(s_1)}.
```

In the multiplicative-domain case `0 notin D`, the shifted condition is the
same as saying that both `f` and `g` have a common root-free denominator
`XQ` into the supercode `C^{(s_1)}`.

Thus, after fixed-root/root-slice pieces are separated, failure of the
half-window cutoff minors from Corollary 40.72 is exactly the existence of a
low-degree root-free rational representation of one endpoint, or of both
endpoints with a common denominator, into a larger Reed-Solomon supercode.
This is the structural object that must be ruled out or charged by active M1
geometry, quotient-periodic separation, or aperiodic packing estimates.

### Proof

Write

```text
Q(X)=sum_i q_i X^i.
```

For `0<=a<s`,

```text
Syn(Qy)_a
 = sum_{x in D} lambda_x Q(x)y(x)x^a
 = sum_i q_i sum_{x in D} lambda_x y(x)x^{a+i}
 = sum_i q_i w_{a+i}.
```

The last expression is the `a`-th row of `H_{s,m-1}(w)Q`.  Hence the Hankel
kernel equation is equivalent to the first `s` syndrome checks of `Qy`
vanishing, which is equivalent to `Qy in C^{(s)}` by the definition of the
supercode.  If `Q` is root-free on `D`, divide pointwise by `Q` to obtain
`y=P/Q` with `P` the degree-`<n-s` polynomial representing `Qy` on `D`.

The four cutoff interpretations are the same identity applied to
`y=f`, `y=g`, to both endpoint words simultaneously, and finally to

```text
Syn(XQy)_a = Syn(Qy)_{a+1},
```

which is the shifted Hankel equation.  If `0 notin D`, multiplication by `X`
does not introduce a domain zero, so `XQ` is root-free exactly when `Q` is.

## Corollary 40.75: Paired Rational-Supercode Strata Have At Most One Noncontained Slope

Let `C=RS[F,D,k]`, let `f,g:D->F`, and fix an agreement threshold `a`.  Suppose
there is a polynomial `Q` of degree `e`, root-free on `D`, such that

```text
Qf in RS[F,D,n-s],        Qg in RS[F,D,n-s].
```

Assume

```text
a >= max(n-s, k+e).                                  (InterpPair)
```

Then every finite slope `z` for which `f+zg` is explained by a codeword on at
least `a` domain points is in fact globally a codeword:

```text
f+zg in C.
```

Consequently a support-wise noncontained line has at most one such slope in
this paired rational-supercode stratum.

Applied to the ordinary paired cutoff kernel `A_uv(m)`, a root-free
`Q in ker A_uv(m)` has `s=t+r_hw-1`, so it contributes at most one
noncontained slope whenever (InterpPair) holds with `e=deg Q`.

In the multiplicative-domain shifted paired case `0 notin D`, a root-free
`Q in ker A_Suv(m)` gives the common denominator `R=XQ` of degree `e+1` into
the same supercode `RS[F,D,n-(t+r_hw-1)]`.  Hence it contributes at most one
noncontained slope whenever

```text
a >= max(n-(t+r_hw-1), k+e+1).
```

Thus paired low-degree cutoff-kernel failures are harmless once their
denominator degree and supercode codimension put them below the interpolation
threshold: they are either charged as fixed-root pieces, or they can create at
most one noncontained slope.

### Proof

Let `z` be explained on a set `S subset D` with `|S|>=a` by a codeword
`c_z in C`.  Choose polynomials `P_f,P_g` of degree `<n-s` representing
`Qf` and `Qg` on `D`, and a polynomial `C_z` of degree `<k` representing
`c_z`.  On `S`,

```text
P_f + z P_g = Q(f+zg) = Q C_z.
```

The left side has degree `<n-s`, while the right side has degree `<k+e`.
By (InterpPair), these two polynomials agree on more points than the maximum
of their degrees, so they are identical.  Since `Q` is root-free on `D`, this
identity implies `f+zg=c_z` on all of `D`, i.e. `f+zg in C`.

If two distinct finite slopes `z_1,z_2` are globally codewords, then

```text
g = (c_{z_2}-c_{z_1})/(z_2-z_1) in C,
f = c_{z_1}-z_1 g in C.
```

Then the line is support-wise contained on every support, so no slope on it is
noncontained.  Hence a noncontained line has at most one explained slope in
the stratum.  The two cutoff applications are Corollary 40.74 with
`s=t+r_hw-1`, using `Q` for the ordinary paired kernel and `R=XQ` for the
shifted paired kernel.

## Corollary 40.76: Scalar Rational-Supercode Strata Have A Pairwise-Intersection Charge

Let `C=RS[F,D,k]`, let `f,g:D->F`, and fix an agreement threshold `a`.  Suppose
there is a polynomial `Q` of degree `e`, root-free on `D`, and put

```text
d=max(n-s, k+e).
```

Assume the pairwise support-intersection threshold

```text
2a-n >= d.                                         (ScalarInterp)
```

Then each one-sided rational-supercode stratum contributes at most one
support-wise noncontained finite slope:

1. if `Qf in RS[F,D,n-s]`, then at most one finite slope explained on at
   least `a` points can be noncontained;
2. if `Qg in RS[F,D,n-s]`, then at most one finite slope explained on at
   least `a` points can be noncontained.

Applied to the scalar cutoff kernels, a root-free

```text
Q in ker A_u(m)        or        Q in ker A_v(m)
```

with `s=t+r_hw` and degree `e` contributes at most one noncontained finite
slope whenever

```text
2a-n >= max(n-(t+r_hw), k+e).
```

Thus scalar low-degree cutoff-kernel failures are one-slope charges in the
high-agreement range where any two agreement supports have enough overlap to
interpolate the induced degree-`<d` rational-supercode witnesses.

### Proof

First suppose `Qg in RS[F,D,n-s]`, represented by a polynomial `P_g` of degree
`<n-s`.  Let two distinct slopes `z_1,z_2` be explained on supports
`S_1,S_2` with `|S_i|>=a` by codewords `c_i`, represented by polynomials
`C_i` of degree `<k`.  Their intersection has size at least

```text
|S_1 cap S_2| >= 2a-n >= d.
```

On this intersection,

```text
Q C_i = Qf + z_i P_g,        i=1,2.
```

Subtracting gives

```text
Q(C_2-C_1) = (z_2-z_1)P_g.
```

The two sides have degree `<k+e` and `<n-s`, respectively, so the displayed
equality on at least `d` points is a polynomial identity.  Since `Q` is
root-free on `D`, it follows on `D` that

```text
g = (C_2-C_1)/(z_2-z_1),
```

so `g` is globally a codeword.  For any explained slope `z` on support `S`,
the identity `f+zg=c_z` on `S` then gives

```text
f|_S = (c_z-zg)|_S
```

with both right-hand terms codewords.  Hence every explained slope is
support-wise contained.  In particular two noncontained slopes cannot occur.

Now suppose `Qf in RS[F,D,n-s]`, represented by `P_f`.  If two distinct
nonzero slopes `z_1,z_2` are explained on supports `S_1,S_2`, define on each
support

```text
R_i=(Q C_i-P_f)/z_i.
```

Each `R_i` is a polynomial of degree `<d` agreeing with the word `Qg` on
`S_i`.  On `S_1 cap S_2`, the polynomials `R_1` and `R_2` agree, so
(ScalarInterp) makes them identical.  Therefore

```text
(Q C_1-P_f)/z_1 = (Q C_2-P_f)/z_2,
```

and hence

```text
(z_2-z_1)P_f = Q(z_2 C_1-z_1 C_2).
```

Dividing on `D` by the root-free `Q` shows that `f` is globally a codeword.
Then every nonzero explained slope is support-wise contained on its explaining
support.

It remains only to consider the possibility that slope `0` and a nonzero
slope are both noncontained.  If `z=0` is explained on `S_0`, then

```text
P_f = Q C_0
```

on `S_0`.  Since `|S_0|>=a>=d`, this is a polynomial identity, so `f` is
globally a codeword.  The preceding paragraph then makes every nonzero
explained slope contained.  Thus at most one finite slope in the `Qf`
one-sided stratum can be noncontained.

## Corollary 40.77: Scalar Rational-Supercode Strata Have A Support-Packing Bound

Keep the notation of Corollary 40.76, with

```text
d=max(n-s, k+e).
```

Assume

```text
1 <= d <= a.
```

Fix one of the two scalar rational-supercode strata

```text
Qf in RS[F,D,n-s]        or        Qg in RS[F,D,n-s],
```

with `Q` root-free on `D`.  Let `Bad_Q` be the set of finite slopes in this
stratum which are explained on at least `a` points and are support-wise
noncontained.  Then

```text
|Bad_Q| <= floor( binom(n,d) / binom(a,d) ).        (ScalarPack)
```

Equivalently, even when the global pairwise-intersection threshold
`2a-n>=d` fails, the surviving noncontained scalar slopes form a `d`-packing
of their agreement supports.  The one-slope charge of Corollary 40.76 is the
special case where every two `a`-supports already intersect in at least `d`
points.

Applied to the scalar cutoff kernels at the first half-window depth, put
`s=t+r_hw` and `e=deg Q`.  Whenever

```text
1 <= max(n-(t+r_hw), k+e) <= a,
```

the `A_u` and `A_v` scalar cutoff-kernel strata each contribute at most

```text
floor( binom(n, max(n-(t+r_hw), k+e)) /
       binom(a, max(n-(t+r_hw), k+e)) )
```

noncontained finite slopes after fixed-root/root-slice charges have been
separated.

### Proof

The proof of Corollary 40.76 is local in a pair of agreement supports.

First suppose `Qg in RS[F,D,n-s]`.  If two distinct noncontained slopes
`z_1,z_2` have explaining supports `S_1,S_2` with

```text
|S_1 cap S_2| >= d,
```

then the same subtraction argument gives the polynomial identity

```text
Q(C_2-C_1)=(z_2-z_1)P_g.
```

Thus `g` is a global codeword, and every explained slope is support-wise
contained on its explaining support.  This contradicts the choice of the two
slopes.  Hence any two noncontained slopes in the `Qg` stratum have agreement
supports whose intersection has size `<d`.

Now suppose `Qf in RS[F,D,n-s]`.  The same comparison of

```text
(Q C_i-P_f)/z_i
```

shows that two distinct nonzero noncontained slopes cannot have explaining
supports intersecting in at least `d` points.  Also, since `d<=a`, the zero
slope cannot coexist with a nonzero noncontained slope: if `z=0` is explained
on `S_0`, then `P_f=Q C_0` on at least `a>=d` points, so `f` is a global
codeword and every nonzero explained slope is support-wise contained.

Thus, in either scalar stratum, after choosing one explaining support `S_z`
for each slope in `Bad_Q`, the selected supports may be taken to satisfy

```text
|S_z cap S_w| < d        for z != w,
```

except for the harmless case where `Bad_Q` consists only of the zero slope.
Choose an `a`-element subset `T_z subset S_z` for each selected support.  Then
the `T_z` also have pairwise intersections of size `<d`, so no `d`-subset of
`D` can lie in two of them.  Counting pairs

```text
(z,J),        z in Bad_Q,        J subset T_z,        |J|=d,
```

gives

```text
|Bad_Q| binom(a,d) <= binom(n,d).
```

The displayed bound follows.  If `Bad_Q` consists only of the zero slope, the
same inequality is automatic because `d<=a<=n`.

## Corollary 40.78: The Scalar Packing Ledger Is Only A Log-Dimension Closure

For integers `1<=d<=a<=n`, put

```text
Pack(n,a,d)=binom(n,d)/binom(a,d).
```

Then

```text
Pack(n,a,d)=prod_{i=0}^{d-1} (n-i)/(a-i).           (PackProduct)
```

Consequently:

1. if `a<=alpha n` for a fixed `0<alpha<1`, then

   ```text
   Pack(n,a,d) >= alpha^{-d};
   ```

   hence a polynomial packing ledger `floor(Pack(n,a,d))<=n^B` forces

   ```text
   d <= (B log n + O(1))/log(1/alpha);
   ```

2. if `a>=alpha n` and `d<=a/2`, then

   ```text
   Pack(n,a,d) <= (2/alpha)^d.
   ```

Thus the scalar support-packing estimate from Corollary 40.77 is a polynomial
closure only when the interpolation dimension `d` is logarithmic in `n`, up to
fixed-rate constants.  If `a<=alpha n` and `d=omega(log n)`, the packing ledger
is superpolynomial; if `d>=c n` for fixed `c>0`, it is exponential in `n`.

In the corrected-reserve fixed-rate M1 window, with `k>=rho n` for fixed
`rho>0` and agreement threshold `a<=alpha n< n`, every scalar
rational-supercode stratum has

```text
d=max(n-s,k+e) >= k >= rho n.
```

Therefore Corollary 40.77 alone cannot prove the desired
`n^{1+o(1)}` aperiodic scalar contribution in that window.  The scalar branch
must still be closed by extra M1 structure: exclusion of the root-free scalar
cutoff kernels, collapse into paired or endpoint-global strata, quotient or
aperiodic denominator structure, or another active-geometry input.

### Proof

The product formula follows by cancelling factorials:

```text
binom(n,d)/binom(a,d)
 = n(n-1)...(n-d+1) / (a(a-1)...(a-d+1)).
```

For each `0<=i<d`,

```text
(n-i)/(a-i) >= n/a,
```

because `n>=a`.  If `a<=alpha n`, this gives
`Pack(n,a,d)>=(n/a)^d>=alpha^{-d}`.  If
`floor(Pack(n,a,d))<=n^B`, then `Pack(n,a,d)<n^B+1`, and the displayed
logarithmic upper bound on `d` follows.

For the upper estimate, if `a>=alpha n` and `d<=a/2`, then

```text
a-i >= a-d+1 >= a/2 >= alpha n/2
```

for all `0<=i<d`, while `n-i<=n`.  Hence every factor in (PackProduct) is at
most `2/alpha`, proving the upper bound.

The fixed-rate M1 conclusion is just the observation that the scalar
rational-supercode interpolation dimension satisfies `d>=k`, so it is linear
in `n` at fixed positive rate.  The previous lower bound then makes the
support-packing ledger exponential whenever the agreement threshold remains a
fixed positive distance below `n`.

## Corollary 40.79: Scalar Rational-Supercode Strata Inject Into Supercode Lists

Let `C=RS[F,D,k]`, let `f,g:D->F`, and fix an agreement threshold `a`.  Suppose
`Q` has degree `e`, is root-free on `D`, and put

```text
d=max(n-s,k+e).
```

Assume `d<=n`.  For a word `Y:D->F`, write

```text
List_d(Y,a)
 = { R in F[X]_<d : |{x in D : R(x)=Y(x)}|>=a }.
```

Since `d<=n`, this is the ordinary Reed-Solomon list for the supercode
`RS[F,D,d]`.

Then the scalar rational-supercode strata satisfy:

1. if `Qg in RS[F,D,n-s]`, then the support-wise noncontained finite slopes in
   this stratum inject into `List_d(Qf,a)`;
2. if `Qf in RS[F,D,n-s]`, then the nonzero support-wise noncontained finite
   slopes in this stratum inject into `List_d(Qg,a)`.  Consequently the full
   finite scalar stratum has size at most `1+|List_d(Qg,a)|`, with the extra
   `1` accounting only for the possible zero slope.

At the scalar half-window cutoff, where `s=t+r_hw`, any root-free
`Q in ker A_u(m)` or `Q in ker A_v(m)` with

```text
d=max(n-(t+r_hw), k+deg Q) <= n
```

therefore turns the one-sided scalar obstruction into an ordinary list problem
for the multiplied opposite endpoint, in the RS supercode of dimension `d`.
Thus the remaining scalar branch can be charged by a genuine list theorem for
these multiplied endpoint words, rather than by support packing alone.

### Proof

First suppose `Qg in RS[F,D,n-s]`, represented by `P_g` with `deg P_g<n-s`.
For each noncontained slope `z`, choose an explaining codeword `c_z` on a
support `S_z` with `|S_z|>=a`, and let `C_z` be its degree-`<k`
representative.  Define

```text
R_z = Q C_z - z P_g.
```

Then `deg R_z<d`.  On `S_z`,

```text
R_z = Q(c_z-zg)=Qf,
```

so `R_z in List_d(Qf,a)`.

The assignment is injective on noncontained slopes, after the arbitrary choice
of one witness per slope.  Indeed, if `z_1!=z_2` and `R_{z_1}=R_{z_2}`, then

```text
Q(C_{z_1}-C_{z_2}) = (z_1-z_2)P_g.
```

Dividing on `D` by the root-free `Q` shows that `g` agrees on all of `D` with
the degree-`<k` polynomial `(C_{z_1}-C_{z_2})/(z_1-z_2)`.  Hence `g` is a
global codeword.  For any explained slope in the stratum, the identity
`f+zg=c_z` on its support then expresses `f` there as a codeword as well.
Thus every such slope is support-wise contained, contradicting the choice of
`z_1,z_2` as noncontained slopes.

Now suppose `Qf in RS[F,D,n-s]`, represented by `P_f`.  For each nonzero
noncontained slope `z`, choose an explaining codeword `C_z` on `S_z` and set

```text
R_z = (Q C_z-P_f)/z.
```

Again `deg R_z<d`, and on `S_z` this polynomial agrees with `Qg`, so
`R_z in List_d(Qg,a)`.  If two distinct nonzero slopes give the same `R_z`,
then

```text
Q(z_2 C_{z_1}-z_1 C_{z_2}) = (z_2-z_1)P_f.
```

Dividing on `D` by `Q` shows that `f` is a global codeword.  Then every
nonzero explained slope is support-wise contained by solving
`g=(c_z-f)/z` on its explaining support.  Thus the nonzero noncontained slopes
inject into `List_d(Qg,a)`.  The zero slope has no such division by `z`, so it
is recorded as the single possible extra element.

## Corollary 40.80: Scalar Lists Live In A One-Generator Multiplier Extension

Keep the notation and hypotheses of Corollary 40.79, and define the multiplier
subspace

```text
Q C_k = { Q C : C in F[X]_<k }.
```

If `Qg in RS[F,D,n-s]` is represented by `P_g`, put

```text
V_g(Q)=Q C_k + F P_g        subset F[X]_<d.
```

If `Qf in RS[F,D,n-s]` is represented by `P_f`, put

```text
V_f(Q)=Q C_k + F P_f        subset F[X]_<d.
```

Then:

1. the noncontained finite slopes in the `Qg` scalar stratum inject into

   ```text
   List_d(Qf,a) cap V_g(Q);
   ```

2. the nonzero noncontained finite slopes in the `Qf` scalar stratum inject
   into

   ```text
   List_d(Qg,a) cap V_f(Q),
   ```

   so the full finite `Qf` scalar stratum has size at most
   `1+|List_d(Qg,a) cap V_f(Q)|`.

Moreover `dim V_g(Q)<=k+1` and `dim V_f(Q)<=k+1`, with equality unless the
corresponding endpoint is already represented by a degree-`<k` codeword after
division by `Q`.  Equivalently, the residue of every injected list polynomial
modulo `Q` lies on the one-dimensional line spanned by the numerator
`P_g mod Q` or `P_f mod Q`.

Thus the one-sided scalar cutoff obstruction is not an arbitrary list in the
larger dimension-`d` supercode.  It is a list inside a one-generator extension
of the multiplier code `Q RS[F,D,k]`.  This is a strictly sharper structural
target for a future scalar-branch closure.

### Proof

For the `Qg` stratum, Corollary 40.79 maps a noncontained slope `z` to

```text
R_z=Q C_z-zP_g.
```

This polynomial belongs to `Q C_k+F P_g` and agrees with `Qf` on the explaining
support, hence lies in `List_d(Qf,a) cap V_g(Q)`.  The injectivity proof is
exactly the proof of Corollary 40.79.

For the `Qf` stratum and a nonzero slope `z`, Corollary 40.79 maps `z` to

```text
R_z=(Q C_z-P_f)/z = Q(C_z/z) - (1/z)P_f.
```

Thus `R_z in V_f(Q)` and agrees with `Qg` on its explaining support.  Again
the injectivity proof is unchanged, and the zero slope is the only slope not
represented by this division.

The dimension bound follows because multiplication by the nonzero polynomial
`Q` is injective on `F[X]_<k`, so `dim Q C_k=k`.  Adjoining one vector
`P_g` or `P_f` increases the dimension by at most one.  It fails to increase
the dimension exactly when `P_g` or `P_f` lies in `Q C_k`, i.e. when
`P=QC` for some `deg C<k`; since `Q` is root-free on `D`, this means the
corresponding endpoint word is globally represented by the codeword `C`.
The final residue-line statement is the same membership condition reduced
modulo `Q`.

## Corollary 40.81: Scalar Strata Are Exact Constrained Multiplier Lists

Keep the notation and hypotheses of Corollary 40.80.

First suppose `Qg in RS[F,D,n-s]`, represented by `P_g`.

If

```text
P_g in Q C_k,
```

then `g` is a global codeword and the `Qg` scalar stratum contributes no
support-wise noncontained finite slope.

If `P_g notin Q C_k`, then

```text
V_g(Q)=Q C_k direct-sum F P_g.
```

Every `R in List_d(Qf,a) cap V_g(Q)` has a unique representation

```text
R=Q C - z P_g,        C in F[X]_<k,        z in F.
```

The coefficient map

```text
R |-> z
```

is a bijection from `List_d(Qf,a) cap V_g(Q)` to the finite slopes `z` for
which `f+zg` is explained by a degree-`<k` codeword on at least `a` points.
The noncontained `Qg`-scalar slopes are therefore exactly the noncontained
subfamily of this constrained multiplier-list coefficient set.

Similarly, suppose `Qf in RS[F,D,n-s]`, represented by `P_f`.  If
`P_f in Q C_k`, then `f` is a global codeword and the `Qf` scalar stratum
contributes no nonzero support-wise noncontained finite slope; the original
zero slope is still the separate scalar exception.  If `P_f notin Q C_k`, then

```text
V_f(Q)=Q C_k direct-sum F P_f.
```

Let

```text
List_d(Qg,a) cap V_f(Q)^{nonzero}
```

denote the entries whose unique `P_f`-coefficient is nonzero.  If

```text
R=Q C + mu P_f,        mu != 0,
```

then the coefficient map

```text
R |-> z=-1/mu
```

is a bijection from `List_d(Qg,a) cap V_f(Q)^{nonzero}` to the nonzero finite
slopes `z` for which `f+zg` is explained by a degree-`<k` codeword on at least
`a` points.  The possible zero slope remains the only scalar slope outside
this exact constrained-list parametrization.

### Proof

If `P_g=Q C_g` with `deg C_g<k`, then `g=C_g` on `D` because `Q` is root-free.
Whenever `f+zg=C_z` on a support `S`, we have

```text
f|_S=(C_z-zC_g)|_S,
```

with both terms degree-`<k` codewords.  Hence the slope is support-wise
contained.  This proves the first empty-branch claim.

Assume now `P_g notin Q C_k`.  The direct-sum statement is immediate from the
definition of `V_g(Q)`.  If `R=Q C-zP_g` lies in `List_d(Qf,a)`, choose a
support `S` of size at least `a` on which `R=Qf`.  Since `P_g=Qg` on `D`,

```text
Q(C-zg-f)=0        on S.
```

Root-freeness of `Q` on `D` gives `C=f+zg` on `S`, so slope `z` is explained.
Conversely, any explained slope `z` with codeword representative `C_z` gives
`R=Q C_z-zP_g` in the constrained list.  Uniqueness of the direct-sum
coefficient makes the two constructions inverse.

The `Qf` case is the same after exchanging the roles of the two endpoints and
inverting the nonzero coefficient.  If `P_f=Q C_f`, then `f` is global, and
any explanation `f+zg=C_z` on `S` with `z!=0` gives

```text
g|_S=((C_z-C_f)/z)|_S,
```

so nonzero explained slopes are contained.  This proves only that there is no
nonzero noncontained scalar slope; the zero slope remains the same exceptional
case as in Corollaries 40.79--40.80.

If `P_f notin Q C_k` and

```text
R=Q C + mu P_f,        mu != 0,
```

agrees with `Qg` on `S`, put `z=-1/mu`.  Multiplying the identity
`R=Qg` on `S` by `z` gives

```text
P_f+zQg=Q(zC)        on S,
```

so `f+zg=zC` on `S`.  Conversely, a nonzero explained slope `z` with
representative `C_z` gives

```text
R=(Q C_z-P_f)/z=Q(C_z/z)-(1/z)P_f,
```

whose `P_f`-coefficient is `-1/z`.  These constructions are inverse by the
direct-sum uniqueness.

## Corollary 40.82: Standard-Degree Scalar Strata Are Residue-Line Data

Keep the notation of Corollary 40.81, and assume

```text
1 <= e=deg Q <= r=n-k,        n-s <= k+e.            (StdDeg)
```

Then the scalar rational-supercode stratum is not a new object: after removing
the global quotient part of the represented endpoint, it is exactly a
degree-`e` residue-line datum in the sense of the Paper B normal form.

First suppose `Qg in RS[F,D,n-s]`, represented by `P_g`.  Since
`deg P_g<k+e`, divide

```text
P_g=Q H_g+R_g,        deg H_g<k,        deg R_g<e.
```

If `R_g=0`, then `g=H_g` on `D` and the scalar branch contributes no
noncontained slope.  If `R_g!=0`, put

```text
E=Q,        B_g=-R_g,        w_g=Qf.
```

Then the finite `Qg`-scalar slopes are exactly the slopes witnessed by the
degree-`e` residue-line datum `(E,B_g,w_g)` for the line

```text
f + z(g-H_g).
```

The support-wise noncontained slopes are the same as for the original line
`f+zg`, because subtracting the global direction `H_g` does not change
support-wise containment.

Similarly, suppose `Qf in RS[F,D,n-s]`, represented by `P_f`, and divide

```text
P_f=Q H_f+R_f,        deg H_f<k,        deg R_f<e.
```

If `R_f=0`, then `f=H_f` on `D` and the scalar branch contributes no nonzero
noncontained slope; the original zero slope remains separate.  If `R_f!=0`,
put

```text
E=Q,        B_f=-R_f,        w_f=Qg.
```

Then the nonzero finite `Qf`-scalar slopes `z` are exactly the reciprocal
parameters

```text
y=1/z
```

witnessed by the degree-`e` residue-line datum `(E,B_f,w_f)` for the line

```text
g + y(f-H_f).
```

The possible original zero slope is the only slope not represented by this
reciprocal residue-line datum.

### Proof

The degree assumptions give `deg P_g,deg P_f<k+e`, so Euclidean division by
the degree-`e` polynomial `Q` gives quotients of degree `<k` and remainders of
degree `<e`.

Consider the `Qg` case.  Since `Q` is root-free on `D`,

```text
g=H_g+R_g/Q        on D.
```

If `R_g=0`, the endpoint `g` is global and the branch is contained, as in
Corollary 40.81.  Otherwise the residue-line datum `(Q,-R_g,Qf)` has direction

```text
-B_g/E = R_g/Q = g-H_g.
```

If the original slope `z` is explained by `C_z` on a support `S`, then

```text
C_z-zH_g = f+z(g-H_g)        on S
```

is a degree-`<k` explanation for the residue-line datum.  Its denominator
cleared witness is

```text
Q(C_z-zH_g)+zB_g
 = Q C_z-z(QH_g+R_g)
 = Q C_z-zP_g,
```

which has degree `<k+e`, is congruent to `zB_g mod Q`, and equals `Qf` on
`S`.  Conversely, any witness for `(Q,B_g,Qf)` gives a degree-`<k` polynomial
`C` with `C=f+z(g-H_g)` on `S`; adding the global codeword `zH_g` gives an
explanation of the original line `f+zg` on the same support.  Containment is
unchanged by adding or subtracting the global direction `H_g`.

The `Qf` case is identical after swapping endpoints and using the reciprocal
parameter.  On `D`,

```text
f=H_f+R_f/Q.
```

For a nonzero original slope `z`, put `y=1/z`.  Then explaining
`f+zg=C_z` is equivalent to explaining

```text
g+y(f-H_f)=C_z/z-yH_f
```

for the reciprocal line.  The denominator-cleared witness is

```text
Q(C_z/z-yH_f)+yB_f
 = (Q C_z-P_f)/z,
```

which is the constrained-list polynomial from Corollary 40.81 and is
congruent to `yB_f mod Q`.  The converse and containment equivalence follow
by reversing these identities.  The original slope `z=0` has no reciprocal
parameter, so it remains the only exception.

## Corollary 40.83: Non-Standard Scalar Strata Are Enlarged Residue Lines With A Return Slice

Keep the notation of Corollary 40.81, and assume the complementary
non-standard range

```text
1 <= e=deg Q,        n-s > k+e.
```

Put

```text
K=n-s-e,        so K>k.
```

Then the scalar rational-supercode stratum is an exact degree-`e` residue-line
datum over the enlarged code `RS[F,D,K]`, together with an affine slice forcing
the explaining enlarged-code polynomial to return to the original
degree-`<k` code after the global quotient part is restored.

First suppose `Qg in RS[F,D,n-s]`, represented by `P_g`, and divide

```text
P_g=Q H_g+R_g,        deg H_g<K,        deg R_g<e.
```

Put

```text
E=Q,        B_g=-R_g,        w_g=Qf.
```

Then a finite slope `z` is explained in the original `Qg` scalar stratum on a
support `S` if and only if there exists `C'_z in F[X]_<K` such that

```text
Q C'_z + z B_g = w_g        on S,                  (EnlargedQg)
```

and the return-to-base condition holds:

```text
C'_z + z H_g in F[X]_<k.                           (ReturnQg)
```

Under this equivalence the original explaining codeword is

```text
C_z=C'_z+zH_g.
```

Thus the remaining non-standard `Qg` scalar branch is not an arbitrary
supercode list: it is a degree-`e` residue-line datum over dimension `K`,
cut by the affine return slice (ReturnQg).

Similarly, suppose `Qf in RS[F,D,n-s]`, represented by `P_f`, and divide

```text
P_f=Q H_f+R_f,        deg H_f<K,        deg R_f<e.
```

Put

```text
E=Q,        B_f=-R_f,        w_f=Qg.
```

For a nonzero original slope `z`, put `y=1/z`.  Then `z` is explained in the
original `Qf` scalar stratum on a support `S` if and only if there exists
`C'_y in F[X]_<K` such that

```text
Q C'_y + y B_f = w_f        on S,                  (EnlargedQf)
```

and the return-to-base condition holds:

```text
C'_y + y H_f in F[X]_<k.                           (ReturnQf)
```

The original explaining codeword is then

```text
C_z=z(C'_y+yH_f).
```

The original zero slope remains outside this reciprocal enlarged-residue
parametrization.

### Proof

Since `deg P_g,deg P_f<n-s=K+e`, Euclidean division by `Q` gives the displayed
quotients of degree `<K` and remainders of degree `<e`.

In the `Qg` case, `P_g=Qg` on `D`, so

```text
g=H_g+R_g/Q        on D.
```

If the original slope `z` is explained by `C_z in F[X]_<k` on `S`, set

```text
C'_z=C_z-zH_g.
```

Then `deg C'_z<K`, because `deg C_z<k<K` and `deg H_g<K`.  Also
`C'_z+zH_g=C_z`, giving (ReturnQg).  Multiplying the identity
`C_z=f+zg` on `S` by `Q` and substituting `P_g=QH_g+R_g` gives

```text
Q(C_z-zH_g)-zR_g = Qf        on S,
```

which is (EnlargedQg).

Conversely, if `C'_z` satisfies (EnlargedQg) and (ReturnQg), put
`C_z=C'_z+zH_g`.  Then `deg C_z<k`, and (EnlargedQg) gives

```text
Q C_z-z(QH_g+R_g)=Qf        on S.
```

Since `QH_g+R_g=P_g=Qg` on `D` and `Q` is root-free on `D`, this is exactly
`C_z=f+zg` on `S`.

The `Qf` case is the reciprocal version.  If a nonzero original slope `z` is
explained by `C_z`, put `y=1/z` and

```text
C'_y=C_z/z-yH_f.
```

Then `deg C'_y<K`, and

```text
C'_y+yH_f=C_z/z in F[X]_<k,
```

which is (ReturnQf).  The equality `f+zg=C_z` on `S` is equivalent to

```text
P_f+zQg=Q C_z        on S.
```

After dividing by `z` and substituting `P_f=QH_f+R_f`, this becomes

```text
Q(C_z/z-yH_f)-yR_f=Qg        on S,
```

which is (EnlargedQf).  Reversing the construction, (EnlargedQf) and
(ReturnQf) give `D_y=C'_y+yH_f in F[X]_<k`; with `z=1/y`,
`C_z=zD_y` has degree `<k` and explains the original slope.  The case `z=0`
has no reciprocal parameter, so it remains separate.

## Corollary 40.84: The Non-Standard Return Slice Is A High-Tail Line

Keep the notation of Corollary 40.83.  Let

```text
tau_K: F[X]_<K -> F^{K-k}
```

be the high-tail projection recording the coefficients of degrees
`k,k+1,...,K-1`.  Thus

```text
P in F[X]_<k        iff        tau_K(P)=0.
```

In the `Qg` non-standard scalar branch, the return condition (ReturnQg) is
equivalent to

```text
tau_K(C'_z) = - z tau_K(H_g).                       (TailQg)
```

Consequently every surviving enlarged residue-line witness has high tail in
the projective line spanned by `tau_K(H_g)`.  If `tau_K(H_g)=0`, then
(ReturnQg) is simply `C'_z in F[X]_<k`, and the `Qg` branch is already the
ordinary degree-`e` residue-line datum over the original code dimension `k`.
If `tau_K(H_g)!=0`, the slope `z` is determined by the high tail
`tau_K(C'_z)`.

In the `Qf` non-standard scalar branch, the reciprocal return condition
(ReturnQf) is equivalent to

```text
tau_K(C'_y) = - y tau_K(H_f).                       (TailQf)
```

Thus every surviving nonzero original slope has reciprocal parameter `y=1/z`
and an enlarged witness whose high tail lies on the line spanned by
`tau_K(H_f)`.  If `tau_K(H_f)=0`, the nonzero `Qf` branch is the ordinary
degree-`e` residue-line datum over the original code dimension `k`, with the
original zero slope still separate.  If `tau_K(H_f)!=0`, the reciprocal
parameter `y` is determined by the high tail `tau_K(C'_y)`.

Thus the non-standard scalar obstruction is an enlarged residue-line problem
with a one-dimensional high-tail incidence, not a full enlarged-code
residue-line list.

### Proof

The condition `C'_z+zH_g in F[X]_<k` is equivalent to vanishing of its
high-tail projection:

```text
0=tau_K(C'_z+zH_g)=tau_K(C'_z)+z tau_K(H_g),
```

which is (TailQg).  If `tau_K(H_g)=0`, this says `tau_K(C'_z)=0`, i.e.
`C'_z in F[X]_<k`; substituting this into Corollary 40.83 gives the ordinary
degree-`e` residue-line datum over the base code dimension.  If
`tau_K(H_g)!=0`, then any solution has `tau_K(C'_z)` equal to a scalar
multiple of `tau_K(H_g)`, and that scalar is `-z`, so it determines `z`.

The `Qf` statement is identical after replacing `z,H_g,C'_z` by the
reciprocal parameter `y`, `H_f`, and `C'_y`.  The original slope `z=0` has no
reciprocal parameter and is therefore unchanged from Corollary 40.83.

## Corollary 40.85: At The Scalar Cutoff, Non-Standard Means Short Denominator

Specialize Corollaries 40.82--40.84 to the scalar half-window cutoff

```text
s=t+r_hw,        t=r-j,        r=n-k.
```

Let `Q` be a scalar cutoff witness of degree

```text
e=deg Q.
```

Then

```text
n-s = k+j-r_hw.                                    (CutoffDim)
```

Consequently the standard-degree condition from Corollary 40.82 becomes

```text
e >= j-r_hw,
```

while the non-standard condition from Corollary 40.83 becomes

```text
e < j-r_hw.                                       (ShortScalar)
```

In the non-standard case, the enlarged dimension and high-tail length are

```text
K = k+j-r_hw-e,
K-k = j-r_hw-e.                                  (ShortTailLen)
```

Thus:

1. if `r_hw>=j`, there is no non-standard scalar cutoff range;
2. if `r_hw<j`, the only positive-degree scalar cutoff witnesses not already
   ordinary degree-`e` residue-line data have

   ```text
   1 <= e <= j-r_hw-1;
   ```

3. for such a positive short denominator, the return slice of Corollary 40.84
   is a one-dimensional high-tail incidence inside `F^{j-r_hw-e}`.

Therefore the scalar cutoff branch is completely split as follows.  Denominators
of degree at least `j-r_hw` fold into the usual base-dimension residue-line
normal form.  Positive denominators of degree below `j-r_hw` are enlarged
residue-line data with an explicitly bounded high-tail window of length
`j-r_hw-e`.  The constant case `e=0`, when it occurs, is a separate scalar
supercode-endpoint branch rather than a positive-degree residue-line datum; it
is isolated in Corollary 40.86 below.

### Proof

Using `t=r-j` and `r=n-k`,

```text
n-s = n-(t+r_hw)
    = n-(r-j+r_hw)
    = k+j-r_hw.
```

Substituting this into the standard condition `n-s<=k+e` gives
`k+j-r_hw<=k+e`, equivalently `e>=j-r_hw`.  The complementary strict
inequality is `e<j-r_hw`.  In that case Corollary 40.83 gives

```text
K=n-s-e=k+j-r_hw-e,
```

and hence `K-k=j-r_hw-e`.  The three listed consequences are immediate.

## Corollary 40.86: The Constant Scalar Cutoff Branch Is A Supercode Endpoint High-Tail Branch

Specialize to the scalar cutoff as in Corollary 40.85 and assume

```text
r_hw<j,        Q in F^*,        e=deg Q=0.
```

After scaling, take `Q=1`.  Put

```text
K=n-s=k+j-r_hw,
L=K-k=j-r_hw,
tau_K:F[X]_<K -> F^L
```

for the high-tail projection.

First suppose `g in RS[F,D,K]`, represented by `P_g in F[X]_<K`.  If

```text
tau_K(P_g)=0,
```

then `g` is a global codeword and this constant `Qg` scalar branch contributes
no support-wise noncontained finite slope.  If `tau_K(P_g)!=0`, then a finite
slope `z` is explained on a support `S` if and only if there exists
`R_z in F[X]_<K` such that

```text
R_z=f        on S,                                 (ConstQgList)
tau_K(R_z)=-z tau_K(P_g).                         (ConstQgTail)
```

Equivalently, `R_z=C_z-zP_g` for a unique original explaining codeword
`C_z in F[X]_<k`.  Thus the constant `Qg` branch is a one-direction supercode
list for `f`, with high tails constrained to the line spanned by `tau_K(P_g)`;
if that high tail is nonzero, it determines `z`.

Similarly, suppose `f in RS[F,D,K]`, represented by `P_f in F[X]_<K`.  If
`tau_K(P_f)=0`, then `f` is global and this constant `Qf` scalar branch
contributes no nonzero support-wise noncontained slope; the original zero
slope remains separate.  If `tau_K(P_f)!=0`, then nonzero original slopes
`z` are parametrized by reciprocal parameters `y=1/z` and by polynomials
`R_y in F[X]_<K` satisfying

```text
R_y=g        on S,                                 (ConstQfList)
tau_K(R_y)=-y tau_K(P_f).                         (ConstQfTail)
```

The original explaining codeword is `C_z=zR_y`.  The original zero slope is
again outside the reciprocal parametrization.

Thus the `e=0` scalar cutoff case is not a denominator-residue branch.  It is
the degree-zero endpoint-supercode analogue of Corollary 40.84: a supercode
list cut by a one-dimensional high-tail line.

### Proof

For `Q=1`, the scalar condition `Qg in RS[F,D,K]` is just `g=P_g` on `D` with
`deg P_g<K`.  If `tau_K(P_g)=0`, then `deg P_g<k`, so `g` is global and the
same containment argument as in Corollary 40.81 gives no noncontained finite
slope.

Otherwise, if `f+zg=C_z` on `S` with `deg C_z<k`, set

```text
R_z=C_z-zP_g.
```

Then `R_z=f` on `S` and

```text
tau_K(R_z)=tau_K(C_z)-z tau_K(P_g)=-z tau_K(P_g).
```

Conversely, if `R_z` satisfies (ConstQgList) and (ConstQgTail), then
`R_z+zP_g` has zero high tail, hence lies in `F[X]_<k`; putting
`C_z=R_z+zP_g` gives `C_z=f+zg` on `S`.  If `tau_K(P_g)!=0`, the scalar
`z` is determined by the displayed high-tail equation.

The `Qf` case is identical after swapping endpoints and using `y=1/z`.  If
`tau_K(P_f)=0`, then `f` is global, which kills all nonzero noncontained
slopes but not the formal zero-slope exception.  If `f+zg=C_z` with `z!=0`,
put `y=1/z` and `R_y=C_z/z-yP_f`; then `R_y=g` on `S` and
`tau_K(R_y)=-y tau_K(P_f)`.  Conversely, (ConstQfList) and (ConstQfTail) make
`R_y+yP_f` a degree-`<k` polynomial; multiplying by `z=1/y` gives the original
explaining codeword.

## Corollary 40.87: Short Scalar Return Slices Have Effective Dimension At Most k+1

Consider either a positive short scalar cutoff branch from Corollary 40.85 or
the constant scalar cutoff branch from Corollary 40.86.  Let

```text
K=k+L,        L>0,
tau_K:F[X]_<K -> F^L
```

be the high-tail projection.  Let `H` denote the quotient part whose high tail
controls the return condition: `H_g` or `H_f` in the positive-degree case, and
the endpoint representative `P_g` or `P_f` in the constant case.  Put

```text
h=tau_K(H).
```

If `h=0`, the return condition forces the enlarged witness polynomial itself
to lie in `F[X]_<k`; the branch collapses to the base-dimension datum described
above.

If `h!=0`, define the high-tail line subspace

```text
W_h={ A in F[X]_<K : tau_K(A) in F h }.
```

Then

```text
dim W_h = k+1,        codim_{F[X]_<K} W_h = L-1.
```

Every surviving enlarged witness polynomial in the short scalar branch lies in
`W_h`, and for each fixed scalar parameter `lambda` (`lambda=z` in the `Qg`
case and `lambda=y=1/z` in the reciprocal `Qf` case) the corresponding return
slice

```text
tau_K(A)=-lambda h
```

is an affine translate of `F[X]_<k`, hence has dimension `k`.

Thus the remaining short scalar obstruction is never a full `K`-dimensional
enlarged-code list: it is a `k+1` dimensional high-tail-line subcode, with a
fixed-parameter slice of dimension `k`.  The only short layer with no
high-tail codimension saving is the one-row case `L=1`; for every `L>=2`,
the line condition imposes at least one independent high-tail equation.

### Proof

The high-tail projection is surjective with kernel `F[X]_<k`, so

```text
dim ker tau_K = k.
```

If `h=0`, the equations in Corollaries 40.84 and 40.86 reduce to
`tau_K(A)=0`, i.e. `A in F[X]_<k`.

If `h!=0`, then `Fh` is a one-dimensional subspace of `F^L`.  Therefore

```text
W_h=tau_K^{-1}(Fh)
```

has dimension `k+1` and codimension `L-1` in the `K`-dimensional space
`F[X]_<K`.  For fixed `lambda`, the equation
`tau_K(A)=-lambda h` cuts out one fiber of `tau_K`, hence an affine translate
of the kernel `F[X]_<k`.  The membership assertions are exactly the high-tail
equations from Corollaries 40.84 and 40.86.

## Corollary 40.88: The One-Row Short Scalar Layer Is A Linear-Image List

Keep the notation of Corollary 40.87, and assume that

```text
L=1,        h=tau_K(H)!=0.
```

Write

```text
top(A)=tau_K(A)
```

for the coefficient of `X^k` in `A in F[X]_<k+1`.  In the four short scalar
charts, the branch equations have the common form

```text
Q A + lambda B = w        on S,                    (OneRowList)
top(A) = - lambda h.                               (OneRowTop)
```

Here:

1. in the positive-degree `Qg` chart, `A=C'_z`, `lambda=z`,
   `B=B_g=-R_g`, and `w=Qf`;
2. in the positive-degree `Qf` chart, `A=C'_y`, `lambda=y=1/z`,
   `B=B_f=-R_f`, and `w=Qg`;
3. in the constant `Qg` chart, `Q=1`, `B=0`, `A=R_z`, `lambda=z`,
   and `w=f`;
4. in the constant `Qf` chart, `Q=1`, `B=0`, `A=R_y`,
   `lambda=y=1/z`, and `w=g`.

As before, the reciprocal `Qf` charts parametrize the nonzero original slopes;
the original zero slope remains separate.

Define the linear map

```text
T_h:F[X]_<k+1 -> F[X]_<k+e+1,
T_h(A)=Q A - (top(A)/h) B.                         (OneRowImage)
```

In the constant charts this means `e=0`, `Q=1`, `B=0`, and hence `T_h(A)=A`.
Then (OneRowList) and (OneRowTop) are equivalent to the single support-list
condition

```text
T_h(A)=w        on S,                              (LinearImageList)
```

with the scalar parameter recovered by

```text
lambda=-top(A)/h.
```

Moreover `T_h` is injective.  Thus the only short scalar layer with no
high-tail codimension saving is still not a free two-parameter incidence: it
is exactly list decoding against the `k+1` dimensional linear image
`T_h(F[X]_<k+1)`, with the slope parameter a linear functional of the list
entry.

### Proof

The equation (OneRowTop) gives `lambda=-top(A)/h`.  Substituting this value
of `lambda` into (OneRowList) gives (LinearImageList).  Conversely, if
(LinearImageList) holds and `lambda=-top(A)/h`, then (OneRowTop) is automatic
and (OneRowList) is exactly the definition of `T_h`.

It remains to prove injectivity.  In the constant charts this is immediate
because `T_h` is the identity on `F[X]_<k+1`.  In the positive-degree charts,
suppose `T_h(A)=0`, and put `c=top(A)/h`.  Then

```text
Q A = c B.
```

If `c=0`, then `QA=0`, hence `A=0`.  If `c!=0`, then `Q` divides `B`; since
`deg B<deg Q`, this forces `B=0`, and again `QA=0`, so `A=0`.  Therefore
`ker T_h=0`.

## Corollary 40.89: The One-Row Layer Is A Rank-One Rational Extension Of RS_k

Keep the hypotheses and notation of Corollary 40.88.  In the positive-degree
charts, `Q` is root-free on `D` by the inherited scalar rational-supercode
setup; in the constant charts, take `Q=1`.  Put

```text
mu=top(A)/h,        A_0=A-mu h X^k in F[X]_<k,
Y=w/Q              on D.
```

Define the rank-one rational extension direction

```text
phi_h(x)=h x^k - B(x)/Q(x),        x in D,
```

and the evaluation code

```text
E_h = { A_0 + mu phi_h : A_0 in F[X]_<k, mu in F } subset F^D.
```

Then the one-row list condition from Corollary 40.88 is equivalent to

```text
A_0 + mu phi_h = Y        on S.                    (RankOneRSList)
```

The original scalar parameter is recovered as

```text
lambda=-mu.
```

Thus the one-row short scalar layer is exactly list decoding the word `Y`
against the `k+1` dimensional rank-one rational extension `E_h` of the base
Reed-Solomon code `RS[F,D,k]`.  Coordinate-wise multiplication by `Q` carries
`E_h` isomorphically to the linear-image code
`T_h(F[X]_<k+1)|_D`.  In the positive-degree charts the new generator has
denominator `Q` and numerator residue `-B mod Q`; in the constant charts it is
the polynomial generator `hX^k`.

Consequently, after the already separated reciprocal `Qf` zero-slope
exception, the only scalar cutoff layer with no high-tail codimension saving
is a concrete all-line residue-packing target for one-generator rational
extensions of `RS_k`, not an arbitrary enlarged-code list.

### Proof

Since `mu=top(A)/h`, the polynomial

```text
A_0=A-mu h X^k
```

has degree `<k`.  On `D`,

```text
T_h(A)
 = Q(A_0+mu h X^k)-mu B
 = Q(A_0+mu(hX^k-B/Q))
 = Q(A_0+mu phi_h).
```

Because `Q` is root-free on `D`, the equality `T_h(A)=w` on a support `S` is
equivalent to (RankOneRSList).  Conversely, given `A_0 in F[X]_<k` and
`mu in F`, set `A=A_0+mu h X^k`; then `top(A)=mu h`, and Corollary 40.88
recovers the scalar parameter as `lambda=-mu`.

The coordinate-wise multiplier by `Q` is invertible on `F^D`, so it identifies
`E_h` with the evaluation image of `T_h`.  In every one-row cutoff chart,
`deg T_h(A)<k+e+1=n-s<=n`, so evaluation on `D` is injective on this
polynomial image.  Corollary 40.88 proves that `T_h` is injective on the
`k+1` dimensional domain `F[X]_<k+1`; hence `dim E_h=k+1`.  Finally,

```text
Q phi_h = hQX^k-B,
```

so the residue of the new generator modulo `Q` is `-B`; if `Q=1` and `B=0`,
this specializes to the polynomial generator `hX^k`.

## Corollary 40.90: One-Row Rational Extensions Have Primitive Denominator Q/gcd(Q,B)

Keep the notation of Corollary 40.89.  In a positive-degree chart, let

```text
G=gcd(Q,B)
```

with the convention `G=Q` when `B=0`.  Put

```text
Q_prim=Q/G,        B_prim=B/G.
```

In a constant chart, take `Q_prim=1` and `B_prim=0`.  Then `Q_prim` is
root-free on `D`,

```text
gcd(Q_prim,B_prim)=1,
```

and the one-row rational extension direction from Corollary 40.89 has the
primitive form

```text
phi_h = hX^k - B_prim/Q_prim        on D.           (PrimitiveOneRow)
```

Equivalently, the numerator

```text
N_h=hX^k Q-B
```

has

```text
gcd(Q,N_h)=G,
```

so the reduced rational denominator of `phi_h` is exactly `Q_prim`.  Thus
nonprimitive presentations of the same one-row scalar layer do not create new
packing objects.  If `Q_prim=1`, the residual is the polynomial extension
`RS[F,D,k+1]`; otherwise it is a primitive one-generator rational extension
with denominator `Q_prim` and residue `-B_prim mod Q_prim`.

### Proof

Since `G` divides `Q` and `Q` has no root on `D`, the quotient `Q_prim` is
also root-free on `D`.  By construction, `gcd(Q_prim,B_prim)=1`.

The identity

```text
hX^k - B/Q = hX^k - B_prim/Q_prim
```

gives (PrimitiveOneRow).  For the numerator statement, a polynomial divisor
of `Q` divides `N_h=hX^kQ-B` if and only if it divides `B`, because
`N_h` is congruent to `-B` modulo `Q`.  Hence `gcd(Q,N_h)=gcd(Q,B)=G`.
The final alternatives are the cases `Q_prim=1` and `deg Q_prim>0`.

## Corollary 40.91: One-Row Primitive Extensions Have A Primitive-Degree Packing Bound

Keep the notation of Corollary 40.90, and put

```text
e_prim=deg Q_prim,
d_prim=k+e_prim+1.
```

Let `Y:D->F` be any word and let `a` be an agreement threshold.  Let
`Mu_h(Y,a)` be the set of coefficients `mu in F` for which there exist
`A_0 in F[X]_<k` and a support `S subset D`, `|S|>=a`, such that

```text
A_0 + mu(hX^k-B_prim/Q_prim) = Y        on S.       (PrimitiveList)
```

Then two distinct coefficients `mu_1!=mu_2` in `Mu_h(Y,a)` cannot be
witnessed on supports whose intersection has size at least `d_prim`.
Consequently, if `1<=d_prim<=a`, then

```text
|Mu_h(Y,a)| <= floor( binom(n,d_prim) / binom(a,d_prim) ).     (OneRowPack)
```

In particular, if `2a-n>=d_prim`, then `|Mu_h(Y,a)|<=1`.

For the one-row scalar cutoff branches of Corollaries 40.88--40.90, this
counts the possible scalar parameters `lambda=-mu` in the `Qg` charts and the
reciprocal parameters `lambda=y=1/z=-mu` in the `Qf` charts; the original
`Qf` zero slope remains separate.  The polynomial endpoint `Q_prim=1` has
`d_prim=k+1`.  Positive primitive denominator degree costs only `e_prim`,
not the unreduced degree of the original presentation.

### Proof

Choose witnesses `(A_i,S_i)` satisfying (PrimitiveList) for two coefficients
`mu_1!=mu_2`, and suppose

```text
|S_1 cap S_2| >= d_prim.
```

On the intersection, subtracting the two equalities gives

```text
(A_1-A_2) + (mu_1-mu_2)(hX^k-B_prim/Q_prim) = 0.
```

Multiplying by the root-free denominator `Q_prim`, the polynomial

```text
Q_prim(A_1-A_2) + (mu_1-mu_2)(hX^k Q_prim-B_prim)
```

vanishes on at least `d_prim` points of `D`.  Its degree is `<d_prim`, so it
is the zero polynomial.  If `e_prim=0`, then `Q_prim=1` and `B_prim=0`, so
the coefficient of `X^k` is `(mu_1-mu_2)h`, impossible because `h!=0`.
If `e_prim>0`, the identity implies

```text
Q_prim divides B_prim,
```

by reducing modulo `Q_prim`; this contradicts
`gcd(Q_prim,B_prim)=1`.  Hence distinct coefficients cannot have such a large
support intersection.

Assume now that `d_prim<=a`.  For every `mu in Mu_h(Y,a)`, choose an
`a`-element subset `T_mu` of its support.  The preceding paragraph shows that
the family `{T_mu}` has pairwise intersections of size `<d_prim`, so no
`d_prim`-subset of `D` lies in two selected supports.  Counting pairs

```text
(mu,J),        mu in Mu_h(Y,a),        J subset T_mu,        |J|=d_prim
```

gives (OneRowPack).  If `2a-n>=d_prim`, any two `a`-supports would have
intersection at least `d_prim`, so at most one coefficient can occur.

## Corollary 40.92: The One-Row Cutoff Charge Is Controlled By e_prim<t

Specialize Corollary 40.91 to the scalar half-window cutoff from
Corollary 40.85, and use the MCA agreement threshold attached to a
`j`-point complement:

```text
a=n-j=k+t,        t=r-j.
```

Assume the one-row case `L=1`, and let `e_prim=deg Q_prim` be the primitive
denominator degree from Corollary 40.90.  Then the one-row primitive packing
dimension is

```text
d_prim=k+e_prim+1.
```

Consequently:

1. the support-packing bound (OneRowPack) applies exactly in the range

   ```text
   e_prim <= t-1;
   ```

2. the one-coefficient pairwise-intersection charge applies exactly in the
   range

   ```text
   e_prim <= t-j-1;
   ```

3. in the polynomial endpoint `e_prim=0`, the packing bound applies for every
   `t>=1`, and the one-coefficient charge applies for `t>=j+1`.

For a positive one-row short denominator before primitive compression, the
unreduced degree is

```text
e=j-r_hw-1,
```

so `e_prim<=j-r_hw-1`.  Thus unreduced sufficient conditions are

```text
j-r_hw <= t        for packing,
2j-r_hw <= t       for one-coefficient charging.
```

Any common factor between `Q` and `B` improves these inequalities by replacing
`e` with the smaller `e_prim`.

### Proof

The identity `a=n-j=k+t` follows from `r=n-k` and `t=r-j`.  Therefore

```text
d_prim<=a
iff
k+e_prim+1 <= k+t
iff
e_prim <= t-1,
```

which is the packing range in Corollary 40.91.

For the pairwise-intersection range,

```text
2a-n = 2(k+t)-(k+j+t)=k+t-j.
```

Thus

```text
2a-n>=d_prim
iff
k+t-j >= k+e_prim+1
iff
e_prim <= t-j-1.
```

The polynomial endpoint statements set `e_prim=0`.  Finally, in the positive
one-row branch `L=K-k=j-r_hw-e=1`, so `e=j-r_hw-1`; Corollary 40.90 gives
`e_prim<=e`, yielding the two sufficient unreduced criteria.

## Corollary 40.93: The Unpacked One-Row Residual Has Primitive Degree At Least t

Keep the scalar cutoff hypotheses of Corollary 40.92, and work after applying
the primitive packing charge of Corollary 40.91.

The constant one-row branch is always covered by the support-packing charge
for `t>=1`.  In a positive one-row branch, write

```text
e=deg Q=j-r_hw-1,
G=gcd(Q,B),        g=deg G,
e_prim=deg(Q/G)=e-g.
```

Then:

1. the branch is covered by the support-packing charge if and only if

   ```text
   g >= j-r_hw-t;
   ```

2. the branch is covered by the one-coefficient charge if and only if

   ```text
   g >= 2j-r_hw-t;
   ```

3. every positive one-row branch not covered by the support-packing charge
   satisfies

   ```text
   t <= e_prim <= j-r_hw-1,
   g <= j-r_hw-t-1.
   ```

Thus the scalar one-row residual left for genuine M1 aperiodic residue packing
is exactly the primitive high-denominator range `e_prim>=t`; constant branches
and sufficiently nonprimitive positive branches have already been charged.

### Proof

The constant branch has `e_prim=0`, so Corollary 40.92 applies its packing
charge whenever `0<=t-1`, i.e. `t>=1`.

For a positive one-row branch, Corollary 40.92 says that packing applies
exactly when

```text
e_prim=e-g <= t-1.
```

Since `e=j-r_hw-1`, this is equivalent to

```text
g >= e-t+1 = j-r_hw-t.
```

The same substitution in the one-coefficient condition
`e_prim<=t-j-1` gives

```text
g >= e-(t-j-1) = 2j-r_hw-t.
```

If the packing charge does not apply, then `e_prim>=t`; also
`e_prim<=e=j-r_hw-1` and `g=e-e_prim<=j-r_hw-t-1`.

## Corollary 40.94: One-Row Coefficient Collisions Produce Short Quotient Residue Certificates

Keep the primitive one-row extension notation of Corollary 40.91.  Let
`mu_1!=mu_2` be two coefficients in `Mu_h(Y,a)`, witnessed by
`(A_i,S_i)`, and put

```text
I=S_1 cap S_2,        m=|I|,        delta=mu_1-mu_2.
```

Let

```text
L_I(X)=prod_{alpha in I}(X-alpha)
```

be the intersection locator.  Then necessarily `m<d_prim`.  Moreover there
exists a nonzero polynomial `M` with

```text
deg M < d_prim-m
```

such that

```text
L_I M == - delta B_prim        mod Q_prim.          (OneRowResidueCert)
```

Equivalently, after scaling `M` by `delta^{-1}`, every collision gives a
short quotient certificate

```text
L_I M' in F B_prim        mod Q_prim,        deg M'<d_prim-m.
```

Since `Q_prim` is root-free on `D`,

```text
gcd(Q_prim,L_I)=1.
```

Thus, for fixed positive-degree `Q_prim` and `B_prim`, coefficient collisions
beyond the support-packing range are controlled by the existence of a short
quotient multiplier `M` landing the intersection locator in the
one-dimensional residue line `F B_prim` modulo `Q_prim`.  For the polynomial
endpoint `Q_prim=1`, the congruence is vacuous and the obstruction is the
top-coefficient obstruction already used in Corollary 40.91.

At the scalar cutoff, with `a=k+t`, a pair of threshold supports whose
intersection has size `m=a-u` gives a certificate multiplier of degree

```text
deg M < e_prim+1-t+u.
```

In particular, in the first unpacked layer `e_prim=t`, one-exchange support
collisions (`u=1`) give `deg M<2`: they are exactly linear quotient-residue
landing certificates.

### Proof

On `I`, subtract the two primitive-list equations:

```text
(A_1-A_2) + delta(hX^k-B_prim/Q_prim)=0.
```

After multiplication by `Q_prim`, the polynomial

```text
P=Q_prim(A_1-A_2) + delta(hX^kQ_prim-B_prim)
```

vanishes on `I`.  Also `deg P<d_prim`.  Corollary 40.91 already shows that
`m>=d_prim` is impossible, so `m<d_prim`.  Therefore

```text
P=L_I M
```

for some polynomial `M` with `deg M<d_prim-m`.  The polynomial `P` is nonzero:
if it were zero, reducing modulo `Q_prim` would give
`Q_prim | B_prim`, contradicting `gcd(Q_prim,B_prim)=1` and `delta!=0`
(with the polynomial endpoint covered by the nonzero top coefficient argument
from Corollary 40.91).  Hence `M` is nonzero.

Reducing the identity `P=L_I M` modulo `Q_prim` gives
(OneRowResidueCert).  The gcd statement follows because all roots of `L_I`
lie in `D`, while `Q_prim` has no root in `D`.

For the cutoff specialization, `d_prim=k+e_prim+1` and `a=k+t`; if
`m=a-u`, then

```text
d_prim-m = k+e_prim+1-(k+t-u)=e_prim+1-t+u.
```

The final one-exchange claim is the case `e_prim=t` and `u=1`.

## Corollary 40.95: First-Unpacked One-Exchange Collisions Are Boundary-Anchor Landings

Keep the notation of Corollary 40.94, and specialize to the first unpacked
cutoff layer

```text
e_prim=t.
```

Suppose two threshold supports `S_1,S_2` satisfy

```text
|S_1|=|S_2|=a=k+t,        |S_1 cap S_2|=a-1.
```

Put `I=S_1 cap S_2`.  Then every coefficient collision between these supports
produces one of the following residue-line landing certificates modulo
`Q_prim`:

1. a core landing

   ```text
   L_I in F B_prim        mod Q_prim;
   ```

2. or a finite anchor landing

   ```text
   L_I(X-beta) in F B_prim        mod Q_prim
   ```

   for a unique `beta in F`.

If `beta in D\I`, the finite anchor landing is an all-domain one-exchange
locator landing.  If `beta notin D`, it is an external-anchor boundary landing
of the same type as the boundary-off normal form at the start of this note.
Thus the first layer not closed by support packing has no new collision
geometry at one-exchange scale: it is precisely a core or boundary-anchor
residue landing for the primitive denominator.

### Proof

Here `m=|I|=a-1` and `e_prim=t`, so Corollary 40.94 gives a nonzero
polynomial `M` with

```text
deg M < e_prim+1-t+1 = 2
```

and

```text
L_I M in F B_prim        mod Q_prim.
```

If `deg M=0`, scaling gives the core landing `L_I in F B_prim mod Q_prim`.
If `deg M=1`, scaling gives `M=X-beta` for a unique `beta in F`, and hence
the displayed finite anchor landing.  The cases `beta in D\I` and
`beta notin D` are exactly the all-domain one-exchange and external-anchor
boundary interpretations of the locator `L_I(X-beta)`.

## Corollary 40.96: One-Exchange Residuals Have A Unique Projective Multiplier Per Core

Keep the scalar cutoff and primitive positive-denominator hypotheses from
Corollaries 40.93--40.95.  Write

```text
e_prim=t+ell,        ell>=0.
```

Fix an `(a-1)`-element core `I subset D`, and define the one-exchange
multiplier space

```text
V_I^{ell}
 = { M in F[X]_{<=ell+1} : L_I M in F B_prim mod Q_prim }.
```

Then

```text
dim V_I^{ell} <= 1.                                (OneExMultLine)
```

Consequently, for fixed primitive datum `(Q_prim,B_prim)` and fixed
one-exchange core `I`, either no one-exchange coefficient collision over `I`
exists, or all such collisions produce the same projective multiplier
`[M] in P(V_I^{ell})`.  If that multiplier splits over `F`, it is a
bounded-anchor landing of degree at most `ell+1`; roots in `D` are fixed-root
or all-domain exchange pieces, while roots outside `D` are external-anchor
pieces.  If it does not split, the residual is an irreducible bounded-degree
multiplier landing, not an uncontrolled slope family.

### Proof

Since the setup is the unpacked positive-denominator residual, `Q_prim` has
positive degree `e_prim=t+ell` and `gcd(Q_prim,B_prim)=1`.  Also `t>=2`, so

```text
ell+1 < t+ell = e_prim.
```

Thus reduction modulo `Q_prim` is injective on `F[X]_{<=ell+1}`.

Let `M_1,M_2 in V_I^{ell}`.  Choose scalars `c_1,c_2` such that

```text
L_I M_i == c_i B_prim        mod Q_prim.
```

If `c_i=0`, then `L_I M_i==0 mod Q_prim`.  Since `Q_prim` is root-free on
`D`, it is coprime to `L_I`; hence `M_i==0 mod Q_prim`.  By the degree
injectivity just noted, `M_i=0`.  Therefore every nonzero multiplier has
`c_i!=0`.

For two nonzero multipliers,

```text
L_I(c_2 M_1-c_1 M_2) == 0        mod Q_prim.
```

Again `gcd(L_I,Q_prim)=1`, so `c_2 M_1-c_1 M_2==0 mod Q_prim`.  Its degree is
at most `ell+1<e_prim`; hence it is the zero polynomial.  Thus any two
nonzero elements of `V_I^{ell}` are proportional, proving (OneExMultLine).
The final assertions follow from Corollary 40.94, which puts every
one-exchange collision multiplier in `V_I^{ell}`.

## Corollary 40.97: One-Row Coefficients Pack Apart From Exceptional Multiplier Cores

Keep the notation and hypotheses of Corollary 40.96.  Define the exceptional
one-exchange core set

```text
Exc_ell(Q_prim,B_prim)
 = { I subset D : |I|=a-1,        V_I^{ell} != 0 }.
```

Let `Mu_h(Y,a)` be the coefficient set from Corollary 40.91.  Then

```text
|Mu_h(Y,a)|
 <= ( binom(n,a-1) + (n-a)|Exc_ell(Q_prim,B_prim)| ) / a.      (CorePack)
```

Equivalently, outside the explicit exceptional multiplier-core ledger, the
chosen threshold supports form an `(a-1)`-packing.  In particular, if
`Exc_ell(Q_prim,B_prim)` is empty, then

```text
|Mu_h(Y,a)| <= binom(n,a-1)/a.
```

### Proof

For each `mu in Mu_h(Y,a)`, choose one witnessing support of size at least
`a`, and then choose an `a`-element subset `T_mu` of it.  For an
`(a-1)`-subset `I subset D`, let

```text
r_I = |{ mu : I subset T_mu }|.
```

Then

```text
sum_{|I|=a-1} r_I = a |Mu_h(Y,a)|,                 (CoreCount)
```

because each selected `a`-set contains exactly `a` different `(a-1)`-cores.

If `I notin Exc_ell(Q_prim,B_prim)`, then `r_I<=1`.  Indeed, if two distinct
coefficients `mu_1,mu_2` had selected supports containing `I`, the subtraction
argument from Corollary 40.94, applied only on the common core `I`, would give
a nonzero `M in V_I^{ell}`, contradicting `I notin Exc_ell`.

For every `I`, trivially

```text
r_I <= n-a+1,
```

because there are only `n-(a-1)=n-a+1` possible `a`-subsets of `D` containing
`I`.  Therefore

```text
sum_I r_I
 <= (binom(n,a-1)-|Exc_ell|)
    + (n-a+1)|Exc_ell|
 = binom(n,a-1)+(n-a)|Exc_ell|.
```

Combining this with (CoreCount) proves (CorePack).

## Corollary 40.98: Exceptional One-Exchange Multipliers Are Primitive Modulo Q_prim

Keep the notation and hypotheses of Corollary 40.96.  If
`M in V_I^{ell}` is nonzero, then

```text
gcd(M,Q_prim)=1.
```

Consequently `M` is invertible in the quotient ring `F[X]/(Q_prim)`, and the
exceptional-core condition can be written as

```text
L_I in F B_prim M^{-1}        mod Q_prim.           (InvertibleCoreLanding)
```

Thus `Exc_ell(Q_prim,B_prim)` is controlled by primitive, invertible
low-degree multiplier residues modulo `Q_prim`; there is no separate branch
where the one-exchange multiplier shares a factor with the primitive
denominator.

### Proof

By definition of `V_I^{ell}`, there is a scalar `c in F` such that

```text
L_I M == c B_prim        mod Q_prim.                (E)
```

First `c!=0` for nonzero `M`: if `c=0`, then `Q_prim` divides `L_I M`.
Since `Q_prim` is root-free on `D`, it is coprime to `L_I`; hence
`Q_prim` divides `M`.  But `deg M<=ell+1<e_prim=deg Q_prim`, so `M=0`, a
contradiction.

Now let `H=gcd(M,Q_prim)`.  Reducing (E) modulo `H` gives

```text
c B_prim == 0        mod H.
```

Since `c!=0` and `gcd(B_prim,Q_prim)=1`, this forces `H=1`.  Therefore
`M` is invertible modulo `Q_prim`, and multiplying (E) by `M^{-1}` gives
(InvertibleCoreLanding).

## Corollary 40.99: Exceptional Cores Decompose Into Disjoint Residue-Line Fibers

Keep the notation and hypotheses of Corollary 40.98.  Let

```text
P_ell^x(Q_prim)
 = { [M] in P(F[X]_{<=ell+1}) : gcd(M,Q_prim)=1 }.
```

For `[M] in P_ell^x(Q_prim)`, define the residue line

```text
R_[M] = F (B_prim M^{-1})        in (F[X]/(Q_prim)) / F^*,
```

where `M^{-1}` is taken modulo `Q_prim`, and define the split-locator fiber

```text
Core_[M]
 = { I subset D : |I|=a-1,        L_I mod Q_prim lies in R_[M] }.
```

Then the exceptional core ledger from Corollary 40.97 is the disjoint union

```text
Exc_ell(Q_prim,B_prim)
 = disjoint_union_{[M] in P_ell^x(Q_prim)} Core_[M].            (ExcResidueSplit)
```

Consequently

```text
|Exc_ell(Q_prim,B_prim)|
 = sum_{[M] in P_ell^x(Q_prim)} |Core_[M]|.
```

Thus the only remaining one-exchange exceptional ledger is a sum of ordinary
split-locator residue-line fibers modulo the primitive denominator, indexed by
primitive low-degree multiplier classes.  There is no extra multiplicity from
choosing the multiplier once the core is fixed.

### Proof

If `I in Exc_ell`, then by Corollary 40.98 its nonzero multiplier `M` is
coprime to `Q_prim`, and

```text
L_I in F B_prim M^{-1}        mod Q_prim.
```

Thus `I in Core_[M]`.  Scaling `M` does not change the residue line `R_[M]`,
so this gives membership in a well-defined projective multiplier fiber.

Conversely, if `I in Core_[M]`, then for some scalar `c`,

```text
L_I == c B_prim M^{-1}        mod Q_prim.
```

Multiplying by `M` gives `L_I M in F B_prim mod Q_prim`, so
`M in V_I^{ell}` and `I in Exc_ell`.

It remains to prove disjointness.  Suppose `I in Core_[M] cap Core_[N]`.
Then there are nonzero scalars `c,d` such that

```text
L_I M == c B_prim,        L_I N == d B_prim        mod Q_prim.
```

Subtracting gives

```text
L_I(dM-cN) == 0        mod Q_prim.
```

Since `gcd(L_I,Q_prim)=1`, this implies `dM-cN==0 mod Q_prim`.  But
`deg(dM-cN)<=ell+1<deg Q_prim`, so `dM-cN=0` as a polynomial.  Hence
`[M]=[N]`, proving the union is disjoint.

## Corollary 41: The Global Common-Image Ledger Is Endpoint-Only

Let `GCI` be the set of monic degree-`c` split core locators `L` for which
there exists a projective image line `[y] in P(F^t)` such that

```text
y wedge H_{t,j}(u)X^iL = 0,
y wedge H_{t,j}(v)X^iL = 0,        i=0,1,2.          (GCI)
```

For `theta in F`, put

```text
E_theta={ L : H_{t+1,c}(Delta_theta u)L=0
              and H_{t+1,c}(Delta_theta v)L=0 },
```

and put

```text
E_infty={ L : H_{t+1,c}(u)L=0 and H_{t+1,c}(v)L=0 },
E_deep ={ L : H_{t+2,c}(u)L=0 and H_{t+2,c}(v)L=0 }.
```

Then

```text
GCI = E_deep union E_infty union union_{theta in F} E_theta.      (GCIEndpoint)
```

Thus the three-shift global common-image branch can be charged using only
endpoint-type ledgers: the deeper endpoint pair, the ordinary infinity endpoint
pair, and the `q` first-difference endpoint pairs.

In particular, if the direction dimensions of `E_deep`, `E_infty`, and every
`E_theta` are at most `b`, then

```text
|GCI| <= (q+2) binom(n,b),
```

with the same root-free `b/c` replacement after common-root global core pieces
have been charged.

### Proof

For a monic degree-`c` locator `L`, define

```text
Z_w(L)=H_{t+2,c}(w)L in F^{t+2}.
```

The `i`-th length-`t` window of `Z_w(L)` is `H_{t,j}(w)X^iL`.  Hence (GCI) is
equivalent to `Z_u(L),Z_v(L) in W_y`.

If `[y]` is off the extended geometric shift curve of Corollary 39, then
`W_y=0`, so `L in E_deep`.  If `[y]=[1:theta:...:theta^(t-1)]`, then the same
first-difference calculation as in Corollary 40 gives `L in E_theta`, now with
the affine degree-`c` Hankel matrices.  If `[y]=[0:...:0:1]`, the condition is
`L in E_infty`.

Conversely, `L in E_deep` makes all six three-shift Hankel images vanish, so
`L in GCI`.  If `L in E_theta`, then each of `Z_u(L)` and `Z_v(L)` is a scalar
multiple of `(1,theta,...,theta^(t+1))`, so the three length-`t` windows lie in
the image line `[1:theta:...:theta^(t-1)]`.  If `L in E_infty`, the only
possibly nonzero length-`t` window is the last one and it lies in
`[0:...:0:1]`.  This proves (GCIEndpoint).

The count follows from the usual row-rank split-locator bound applied to the
`q+2` affine endpoint systems.  The root-free refinement is again the
common-root slice replacement from Corollary 30.1 and Corollary 36.

## Corollary 42: Endpointized Global Full-Core Closure

Put `c=m-1` and fix `0<=b<c`.  Define the following affine charge systems on
monic degree-`c` split core locators:

```text
U={ L : H_{t+2,c}(u)L=0 },
V={ L : H_{t+2,c}(v)L=0 },

K_lambda={ L : H_{t+2,c}(v-lambda u)L=0 },        lambda in F,

D_theta={ L : H_{t+1,c}(Delta_theta u)L=0
              and H_{t+1,c}(Delta_theta v)L=0 },  theta in F,

D_infty={ L : H_{t+1,c}(u)L=0 and H_{t+1,c}(v)L=0 }.
```

Assume each of the associated homogeneous direction spaces has dimension at
most `b`.  Then the globally full core ledger satisfies

```text
|GlobalFullCore| <= (2q+3) binom(n,b).              (EndpointGFC)
```

After common-root global core pieces have been charged and `1<=b<=n/2`, the
same root-free replacement gives

```text
|GlobalFullCore| <= (2q+3) (b/c) binom(n,b).        (EndpointGFC_rf)
```

Thus the globally full common-image alternative no longer contributes a
projective image-line factor.  It is absorbed into the same endpoint-type
ledger family as the endpoint and fixed-kernel alternatives.

### Proof

Let `L` be a globally full core.  By Corollary 36, `L` satisfies at least one
of the following three-shift alternatives.

If `L` satisfies the `u` endpoint, then Corollary 38 in affine degree `c`
places `L` in `U`; if it satisfies the `v` endpoint, it lies in `V`.

If `L` satisfies the fixed-kernel alternative with finite slope `lambda`, then
Corollary 38 applied to `v-lambda u` places `L` in `K_lambda`.

It remains to consider the common-image alternative.  By Corollary 41, `L`
lies in

```text
E_deep union E_infty union union_{theta in F} E_theta.
```

The set `E_deep` is contained in `U cap V`, hence has already been charged by
the endpoint systems.  The set `E_infty` is exactly `D_infty`, and the sets
`E_theta` are exactly the first-difference systems `D_theta`.

Therefore `GlobalFullCore` is contained in the union of the `2q+3` affine
systems

```text
U, V, D_infty, {K_lambda}_{lambda in F}, {D_theta}_{theta in F}.
```

Each system has direction dimension at most `b` by hypothesis, so the standard
split-locator row-rank bound gives at most `binom(n,b)` split cores in each
system.  Summing gives (EndpointGFC).  The root-free estimate is the same
common-root slice replacement used in Corollaries 30.1, 36, and 41, applied to
each positive-dimensional affine charge system after its common-root pieces
have been removed.

## Corollary 43: Endpointized All-Anchor Full-Core Closure

Assume the hypotheses of Corollary 42.  After the high-dimensional endpointized
global full-core ledgers have been charged, the all-anchor rank-one incidence
satisfies

```text
|{ (beta,S) : rank M_S(beta)<=1,
                no (m-1)-core of S lies in a charged high-dimensional
                endpointized global full-core ledger }|
 <= ( (2q)/m + 2(n-m+1) ) binom(n,m-1)
    + q(n-m+1)(2q+3) binom(n,b).                    (EndpointAllFull)
```

After common-root global core pieces have been charged and `1<=b<=n/2`, the
last term has the root-free replacement

```text
q(n-m+1)(2q+3) (b/c) binom(n,b).                    (EndpointAllFull_rf)
```

Thus the all-anchor full-core component no longer carries the projective
common-image factor `(q^t-1)/(q-1)` in its globally full branch.  The remaining
field-size dependence there is the finite endpointized list of `2q+3` charge
systems from Corollary 42.

### Proof

Split the incidence according to whether a shadow `S` contains a globally full
`(m-1)`-core.

If no core of `S` lies in `GlobalFullCore`, Corollary 35 gives the direct
all-anchor bound

```text
( (2q)/m + 2(n-m+1) ) binom(n,m-1).
```

If `S` contains a globally full core, then after the high-dimensional
endpointized global full-core ledgers have been charged, Corollary 42 gives at
most

```text
(2q+3) binom(n,b)
```

uncharged globally full split cores.  Each such core extends to at most
`n-m+1` degree-`m` shadows and can occur with at most `q` anchors.  This
contributes at most

```text
q(n-m+1)(2q+3) binom(n,b).
```

Adding the two cases proves (EndpointAllFull).  The root-free version is
identical, using (EndpointGFC_rf) in place of (EndpointGFC).

## Corollary 44: First-Difference Endpoint Charges Are Determinantal

Put `c=m-1` and fix `0<=b<c`.  For a syndrome vector `w`, write

```text
w^+_a=w_{a+1},        Delta_theta w = w^+ - theta w.
```

For `theta in F`, let `J_theta` be the stacked first-difference endpoint
direction matrix on degree-`<c` core directions:

```text
J_theta Q =
  ( H_{t+1,c-1}(Delta_theta u)Q,
    H_{t+1,c-1}(Delta_theta v)Q ).
```

Put `d_theta=dim ker J_theta`, and define

```text
Theta_{>b}={ theta in F : d_theta>b }.
```

Then one of the following alternatives holds.

```text
finite first-difference alternative:
  |Theta_{>b}| <= c-b;

persistent first-difference alternative:
  d_theta>b for every theta in F.
```

More precisely, the finite alternative holds whenever at least one
`(c-b) x (c-b)` minor of `J_theta` is not the zero polynomial in `theta`.  If
every such minor vanishes identically, then both endpoint-intersection systems

```text
H_{t+1,c-1}(u)Q=H_{t+1,c-1}(v)Q=0,
H_{t+1,c-1}(u^+)Q=H_{t+1,c-1}(v^+)Q=0
```

have direction dimension `>b`, and there are `b+1` independent moving
first-difference endpoint kernels over `F(theta)`.

For a single nonzero moving kernel

```text
Q(theta)=q_0+q_1 theta+...+q_D theta^D,
```

after dividing by the first nonzero power of `theta` if necessary, its
coefficients satisfy the endpoint ladder

```text
J_+ q_0 = 0,
J_+ q_i - J_0 q_{i-1} = 0        for 1<=i<=D,
J_0 q_D = 0,                                          (FDEL)
```

where

```text
J_+ Q=(H_{t+1,c-1}(u^+)Q, H_{t+1,c-1}(v^+)Q),
J_0 Q=(H_{t+1,c-1}(u)Q,  H_{t+1,c-1}(v)Q).
```

Thus persistent first-difference degeneracy is not a new free endpointized
charge: it starts in the shifted endpoint intersection and ends in the
ordinary endpoint intersection.

### Proof

The matrix has affine form

```text
J_theta=J_+ - theta J_0.
```

The condition `d_theta>b` is equivalent to `rank J_theta<c-b`, i.e. to
vanishing of all `(c-b) x (c-b)` minors.  Each such minor is a polynomial of
degree at most `c-b` in `theta`.  If one minor is nonzero, it has at most
`c-b` roots, giving the finite alternative.

If all minors vanish identically, then the constant and top-degree
coefficients of those minors show that all `(c-b) x (c-b)` minors of both
`J_+` and `J_0` vanish.  Hence both endpoint-intersection systems have
direction dimension `>b`.  Over `F(theta)`, persistent minor vanishing is
equivalent to kernel dimension at least `b+1`; clearing denominators gives
`b+1` independent polynomial moving kernels.

Substituting `Q(theta)=sum_i q_i theta^i` into

```text
(J_+ - theta J_0)Q(theta)=0
```

and comparing powers of `theta` gives (FDEL).  If the first nonzero coefficient
of `Q` occurs at positive degree, divide by the corresponding power of
`theta` first.

## Corollary 45: Endpointized Charges Reduce To Four Base Endpoint Checks

Put `c=m-1` and fix `0<=b<c`.  Let

```text
Lambda_{K,>b}
 = { lambda in F : dim ker H_{t+2,c-1}(v-lambda u)>b },
```

and let `Theta_{D,>b}` be the first-difference bad-parameter set from
Corollary 44.  Also define the shifted endpoint-intersection matrix

```text
J_+ Q=(H_{t+1,c-1}(u^+)Q, H_{t+1,c-1}(v^+)Q),
```

and keep

```text
J_0 Q=(H_{t+1,c-1}(u)Q, H_{t+1,c-1}(v)Q).
```

Assume the four base endpoint direction spaces satisfy

```text
dim ker H_{t+2,c-1}(u) <= b,
dim ker H_{t+2,c-1}(v) <= b,
dim ker J_0            <= b,
dim ker J_+            <= b.                         (BaseEP)
```

Then the persistent fixed-kernel and persistent first-difference alternatives
are impossible, and

```text
|Lambda_{K,>b}| <= c-b,        |Theta_{D,>b}| <= c-b.               (EPFinite)
```

Consequently, after charging the endpointized finite-exception systems indexed
by

```text
Lambda_{K,>b} union Theta_{D,>b},
```

all remaining endpointized systems in Corollary 42 have direction dimension at
most `b`.  Thus Corollaries 42 and 43 apply to the uncharged globally full and
all-anchor full-core ledgers.

### Proof

By Corollaries 37 and 38, the fixed-kernel bad slopes are exactly the values of
`lambda` for which the direction space of

```text
H_{t+2,c-1}(v-lambda u)
```

has dimension `>b`.  If the persistent fixed-kernel alternative occurred, then
Corollary 37 would force both endpoint systems

```text
H_{t+2,c-1}(u),        H_{t+2,c-1}(v)
```

to have direction dimension `>b`, contradicting (BaseEP).  Hence the finite
alternative holds, and `|Lambda_{K,>b}|<=c-b`.

For the first-difference systems, Corollary 44 says that either
`|Theta_{D,>b}|<=c-b`, or the pencil `J_theta=J_+-theta J_0` is persistently
low-rank.  In the persistent case both `J_0` and `J_+` have direction
dimension `>b`, again contradicting (BaseEP).  Thus the finite alternative
holds for `Theta_{D,>b}` as well.

The fixed systems `U`, `V`, and `D_infty=J_0` from Corollary 42 are good by
(BaseEP).  The parameterized systems `K_lambda` and `D_theta` are good outside
the finite bad sets just bounded.  Therefore, after those finite exceptional
systems are charged, every remaining endpointized system in Corollary 42 has
direction dimension at most `b`, proving the final claim.

## Corollary 46: High-Dimensional Endpoint Charges Have Short-Annihilator Certificates

Put

```text
h=c-b.
```

For a finite first-difference parameter `theta`, let

```text
J_theta^(h) Q =
  ( H_{t+1,h-1}(Delta_theta u)Q,
    H_{t+1,h-1}(Delta_theta v)Q ),
        deg Q<h,
```

and define the two endpoint-intersection short systems

```text
J_0^(h) Q =
  ( H_{t+1,h-1}(u)Q,
    H_{t+1,h-1}(v)Q ),

J_+^(h) Q =
  ( H_{t+1,h-1}(u^+)Q,
    H_{t+1,h-1}(v^+)Q ).
```

Then every endpointized high-dimensional charge from Corollaries 42 and 45
has a short annihilator:

```text
dim ker H_{t+2,c-1}(w)>b
  => ker H_{t+2,h-1}(w) != 0,

dim ker H_{t+2,c-1}(v-lambda u)>b
  => ker H_{t+2,h-1}(v-lambda u) != 0,

dim ker J_theta>b
  => ker J_theta^(h) != 0.
```

In particular,

```text
Lambda_{K,>b}
 subset { lambda : ker H_{t+2,h-1}(v-lambda u) != 0 },

Theta_{D,>b}
 subset { theta : ker J_theta^(h) != 0 }.
```

Failure of the base endpoint hypothesis (BaseEP) from Corollary 45 forces at
least one of the four short systems

```text
H_{t+2,h-1}(u),        H_{t+2,h-1}(v),
J_0^(h),               J_+^(h)
```

to have a nonzero kernel.  Equivalently, if these four short systems are
injective, then (BaseEP) holds, and Corollary 45 gives the finite-exception
closure for the endpointized global full-core ledgers.

Thus the remaining endpointized high-dimensional charge is not an opaque
large-kernel condition: it always exposes a degree-`<c-b` annihilator for the
corresponding endpoint, fixed-kernel, or first-difference syndrome window.

### Proof

We use a single linear-algebra observation.  Let `A:F^c->Y` be any linear map,
and let `P_h subset F^c` be the coordinate subspace of vectors supported in
degrees `<h=c-b`.  If `dim ker A>b`, then

```text
dim(ker A cap P_h) >= dim ker A + dim P_h - c
                  >= (b+1)+(c-b)-c
                  = 1.
```

Hence `ker A` contains a nonzero vector of degree `<h`.

Apply this observation to the matrices

```text
H_{t+2,c-1}(w),        H_{t+2,c-1}(v-lambda u),
J_theta,              J_0,              J_+.
```

When the nonzero vector is supported in degrees `<h`, the corresponding
equations are exactly the short Hankel systems displayed above.  The inclusion
statements for `Lambda_{K,>b}` and `Theta_{D,>b}` follow from the definitions
of those bad-parameter sets.  The final assertion is the contrapositive:
if all four base short systems are injective, none of the four base endpoint
spaces can have dimension `>b`.

## Corollary 47: Short Bad Parameters Come From Projective Landing Varieties

Keep `h=c-b`.  For a nonzero degree-`<h` polynomial direction `Q`, put

```text
U_h(Q)=H_{t+2,h-1}(u)Q,        V_h(Q)=H_{t+2,h-1}(v)Q,
```

and

```text
P_0^h(Q)=(H_{t+1,h-1}(u)Q,   H_{t+1,h-1}(v)Q),
P_+^h(Q)=(H_{t+1,h-1}(u^+)Q, H_{t+1,h-1}(v^+)Q).
```

Define the short parameter sets

```text
Lambda_h={ lambda in F :
             exists Q !=0, deg Q<h, V_h(Q)=lambda U_h(Q) },

Theta_h ={ theta in F :
             exists Q !=0, deg Q<h, P_+^h(Q)=theta P_0^h(Q) }.
```

By Corollary 46,

```text
Lambda_{K,>b} subset Lambda_h,        Theta_{D,>b} subset Theta_h.
```

Let the common short endpoint kernels be

```text
C_K^h={ [Q] in P^{h-1} : U_h(Q)=0 and V_h(Q)=0 },

C_D^h={ [Q] in P^{h-1} : P_0^h(Q)=0 and P_+^h(Q)=0 }.
```

If `C_K^h` is nonempty, then `Lambda_h=F`.  If `C_K^h` is empty, then every
`lambda in Lambda_h` is obtained from a projective short locator in

```text
P_K^h={ [Q] in P^{h-1} :
          U_h(Q) != 0 and rank[ U_h(Q)  V_h(Q) ] <= 1 },
```

and the scalar is unique:

```text
V_h(Q)=lambda(Q) U_h(Q).
```

Consequently, when `C_K^h` is empty,

```text
|Lambda_{K,>b}| <= |Lambda_h| <= |P_K^h|.            (ShortK)
```

Similarly, if `C_D^h` is nonempty, then `Theta_h=F`.  If `C_D^h` is empty,
then every `theta in Theta_h` is obtained from a projective short locator in

```text
P_D^h={ [Q] in P^{h-1} :
          P_0^h(Q) != 0 and rank[ P_0^h(Q)  P_+^h(Q) ] <= 1 },
```

with unique scalar

```text
P_+^h(Q)=theta(Q) P_0^h(Q),
```

and hence

```text
|Theta_{D,>b}| <= |Theta_h| <= |P_D^h|.              (ShortD)
```

Thus the finite endpointized bad parameters are controlled by projective
rank-one landing varieties for short annihilators, apart from the explicit
common short endpoint kernels `C_K^h` and `C_D^h`.

### Proof

The inclusions from `Lambda_{K,>b}` and `Theta_{D,>b}` are exactly Corollary
46.

For the fixed-kernel statement, `lambda in Lambda_h` means there is a nonzero
`Q` with

```text
V_h(Q)-lambda U_h(Q)=0.
```

If `U_h(Q)=0`, then also `V_h(Q)=0`, so `[Q] in C_K^h`.  Thus, when `C_K^h`
is empty, every witness must have `U_h(Q)!=0`.  In that case the relation
forces `U_h(Q)` and `V_h(Q)` to be collinear, so `[Q] in P_K^h`.  Since
`U_h(Q)!=0`, the scalar `lambda` is unique.  Scaling `Q` does not change the
scalar, so this gives a well-defined map from `P_K^h` onto `Lambda_h`, proving
(ShortK).  If `C_K^h` is nonempty, the same common kernel vector satisfies
`V_h(Q)-lambda U_h(Q)=0` for every `lambda`, so `Lambda_h=F`.

The first-difference proof is identical with the stacked vectors `P_0^h(Q)`
and `P_+^h(Q)`.  If `P_0^h(Q)=0`, then a valid witness has `P_+^h(Q)=0`, hence
lies in `C_D^h`.  Away from `C_D^h`, every witness has `P_0^h(Q)!=0`, the
relation `P_+^h(Q)=theta P_0^h(Q)` is a rank-one landing condition, and
`theta` is unique.  A common short first-difference endpoint kernel gives a
witness for every `theta`.

## Corollary 48: One-Sided Short Endpoint Injectivity Bounds Bad Parameters

Keep `h=c-b`, and keep the notation of Corollary 47.

If either short fixed-kernel endpoint map

```text
H_{t+2,h-1}(u),        H_{t+2,h-1}(v)
```

is injective on degree-`<h` directions, then

```text
|Lambda_h| <= h,
```

and hence

```text
|Lambda_{K,>b}| <= h = c-b.                         (OneSideK)
```

Similarly, if either short first-difference endpoint map

```text
J_0^(h),        J_+^(h)
```

is injective, then

```text
|Theta_h| <= h,
```

and hence

```text
|Theta_{D,>b}| <= h = c-b.                          (OneSideD)
```

Equivalently, any short fixed-kernel parameter set with more than `h`
parameters forces both

```text
ker H_{t+2,h-1}(u) != 0,        ker H_{t+2,h-1}(v) != 0,
```

and any short first-difference parameter set with more than `h` parameters
forces both

```text
ker J_0^(h) != 0,        ker J_+^(h) != 0.
```

Thus a super-`h` endpoint exception family cannot arise from many unrelated
short slopes: it must already expose one-sided short endpoint annihilators at
both ends of the relevant pencil.

### Proof

Write

```text
A(lambda)=H_{t+2,h-1}(v-lambda u)
         =V_h-lambda U_h
```

as a linear map from the `h`-dimensional space of degree-`<h` directions to
`F^{t+2}`.  If `U_h` is injective, choose `h` rows on which `U_h` has nonzero
determinant.  The same rows of `A(lambda)` have determinant a polynomial in
`lambda` of degree at most `h`, with leading coefficient

```text
(-1)^h det U_h,rows != 0.
```

For every `lambda in Lambda_h`, the map `A(lambda)` has nonzero kernel, so all
`h x h` minors vanish, including this nonzero degree-`<=h` polynomial.  Hence
`|Lambda_h|<=h`.  If instead `V_h` is injective, choose `h` rows with
`det V_h,rows!=0`; the corresponding minor has nonzero constant term and again
has at most `h` roots.  Corollary 46 gives
`Lambda_{K,>b} subset Lambda_h`, proving (OneSideK).

For the first-difference set, write

```text
B(theta)=J_theta^(h)=P_+^h-theta P_0^h.
```

If `P_0^h=J_0^(h)` is injective, an `h x h` minor with nonzero leading
coefficient cuts all `theta in Theta_h`; if `P_+^h=J_+^(h)` is injective, an
`h x h` minor with nonzero constant coefficient does.  Thus `|Theta_h|<=h`,
and Corollary 46 gives (OneSideD).  The final statements are just the
contrapositives.

## Corollary 49: Short-Annihilator Root Stripping Is Lossless

For `alpha in F`, write

```text
(Delta_alpha w)_a=w_{a+1}-alpha w_a.
```

For an ordered list `A=(alpha_1,...,alpha_e)`, put

```text
L_A(X)=prod_{i=1}^e (X-alpha_i),
Delta_A=Delta_{alpha_e} ... Delta_{alpha_1}.
```

The operators `Delta_alpha` commute, so `Delta_A` depends only on the multiset
`A`.

Let `s>=1`, `d>=e`, and suppose

```text
Q(X)=L_A(X)R(X),        deg R<d+1-e.
```

Then the Hankel annihilator identity

```text
H_{s,d}(w)Q = H_{s,d-e}(Delta_A w)R                 (Strip)
```

holds.

Consequently, if a short fixed-kernel witness `Q` for `lambda in Lambda_h`
has `Q=L_A R` with `e<h`, then

```text
H_{t+2,h-e-1}(Delta_A(v-lambda u))R=0,
```

or equivalently

```text
H_{t+2,h-e-1}(Delta_A v - lambda Delta_A u)R=0.     (StripK)
```

If a short first-difference witness `Q` for `theta in Theta_h` has
`Q=L_A R` with `e<h`, then

```text
H_{t+1,h-e-1}(Delta_A Delta_theta u)R=0,
H_{t+1,h-e-1}(Delta_A Delta_theta v)R=0.             (StripD)
```

Thus every short annihilator with a domain-root factor is charged to the
choice of that fixed root factor and to the same short-annihilator problem at
smaller order for the differenced syndrome data.  The endpointized short
obstruction splits into fixed-root/root-slice pieces and root-free short
annihilators.

### Proof

It is enough to prove the case `e=1`; iteration gives the general identity.
Write `Q=(X-alpha)R`, with

```text
R(X)=sum_i r_i X^i.
```

The coefficient of `X^i` in `Q` is `r_{i-1}-alpha r_i`, with the conventions
`r_{-1}=0` and `r_i=0` outside the range of `R`.  Therefore the `a`-th row of
`H_{s,d}(w)Q` is

```text
sum_i w_{a+i}(r_{i-1}-alpha r_i)
 = sum_i (w_{a+i+1}-alpha w_{a+i}) r_i,
```

which is the `a`-th row of `H_{s,d-1}(Delta_alpha w)R`.  This proves the
one-root identity and hence (Strip).

If `Q` witnesses `lambda in Lambda_h`, then

```text
H_{t+2,h-1}(v-lambda u)Q=0.
```

Applying (Strip) with `w=v-lambda u` gives (StripK), using linearity of
`Delta_A`.  If `Q` witnesses `theta in Theta_h`, apply (Strip) separately to
`w=Delta_theta u` and `w=Delta_theta v`; commutativity of the `Delta` operators
gives (StripD).  Taking `A` to be the full domain-root divisor of `Q` leaves a
factor `R` with no roots in `D`, giving the stated root-slice/root-free split.

## Corollary 50: First-Difference Short Parameters Are Marked-Root Common Recurrences

Keep `h=c-b`.  Define the short common endpoint recurrence space

```text
C_h^+={ P in F[X] : deg P<=h,
        H_{t+1,h}(u)P=0 and H_{t+1,h}(v)P=0 }.
```

Then, for every `theta in F`, multiplication by `(X-theta)` gives an
isomorphism

```text
ker J_theta^(h)
  ~= { P in C_h^+ : P(theta)=0 },
        Q |-> (X-theta)Q.                            (MarkedRoot)
```

Consequently,

```text
Theta_h = { theta in F : exists nonzero P in C_h^+ with P(theta)=0 }.
```

Thus the short first-difference bad parameters are exactly the field roots of
the nonzero common endpoint recurrence polynomials of degree at most `h`.

In particular, if `F=F_q` and `g=dim C_h^+`, then

```text
|Theta_h| <= min(q, h (q^g-1)/(q-1)).                (RootCountTheta)
```

If `g=0`, then `Theta_h` is empty.  If `g=1`, then `Theta_h` is contained in
the root set of a single degree-`<=h` recurrence polynomial, so
`|Theta_h|<=h`.

### Proof

Corollary 49 with `A=(theta)` gives, for every degree-`<h` polynomial `Q`,

```text
H_{t+1,h}(w)(X-theta)Q
 = H_{t+1,h-1}(Delta_theta w)Q.                     (MR)
```

Applying (MR) to both `w=u` and `w=v` shows that `Q in ker J_theta^(h)` if and
only if `P=(X-theta)Q` lies in `C_h^+`.  Such a `P` also satisfies
`P(theta)=0`.

Conversely, if `P in C_h^+` and `P(theta)=0`, then `P=(X-theta)Q` for a unique
polynomial `Q` of degree `<h`.  Applying (MR) again gives
`Q in ker J_theta^(h)`.  This proves the isomorphism and the displayed
description of `Theta_h`.

Over `F_q`, every nonzero projective class `[P] in P(C_h^+)` contributes at
most `h` roots in `F_q`, and

```text
|P(C_h^+)|=(q^g-1)/(q-1)
```

when `g>0`.  Union-bounding the root sets and also using the trivial bound
`|Theta_h|<=q` proves (RootCountTheta).  The cases `g=0` and `g=1` are the
corresponding specializations.

## Corollary 51: Fixed-Kernel Short Parameters Have A Finite/Persistent Dichotomy

Keep `h=c-b`, and write

```text
U_h Q=H_{t+2,h-1}(u)Q,        V_h Q=H_{t+2,h-1}(v)Q.
```

Then the short fixed-kernel parameter set

```text
Lambda_h={ lambda in F : ker(V_h-lambda U_h) != 0 }
```

has the following dichotomy.

```text
finite short fixed-kernel alternative:
  |Lambda_h| <= h;

persistent short fixed-kernel alternative:
  every h x h minor of V_h-lambda U_h vanishes identically in lambda.
```

In the persistent alternative, `Lambda_h=F`, both endpoint maps have nonzero
short kernels,

```text
ker U_h != 0,        ker V_h != 0,
```

and there is a nonzero polynomial moving short kernel

```text
Q(lambda)=q_0+q_1 lambda+...+q_D lambda^D
```

satisfying

```text
(V_h-lambda U_h)Q(lambda)=0.
```

After dividing by the first nonzero power of `lambda` if necessary, the
coefficients satisfy the endpoint ladder

```text
V_h q_0 = 0,
V_h q_i - U_h q_{i-1} = 0        for 1<=i<=D,
U_h q_D = 0.                                           (ShortKEL)
```

Consequently, if the persistent short fixed-kernel alternative is absent, then

```text
|Lambda_{K,>b}| <= h = c-b.
```

If it is present, the remaining fixed-kernel endpoint obstruction is an
explicit moving short-recurrence certificate connecting the `v` and `u` short
endpoint kernels.

### Proof

The map `V_h-lambda U_h` has domain dimension `h`.  Hence
`lambda in Lambda_h` is equivalent to rank `<h`, i.e. to the vanishing at
`lambda` of every `h x h` minor.  Each such minor is a polynomial in `lambda`
of degree at most `h`.

If at least one `h x h` minor is not the zero polynomial, then `Lambda_h` is
contained in the root set of that nonzero polynomial, so `|Lambda_h|<=h`.

If every `h x h` minor vanishes identically, then the rank over `F(lambda)` is
`<h`, so the kernel over `F(lambda)` is nonzero.  Choosing a nonzero rational
kernel vector and clearing denominators gives a nonzero polynomial moving
short kernel `Q(lambda)`.  The constant and top-degree coefficients of the
identically vanishing minors show that all `h x h` minors of `V_h` and `U_h`
vanish, respectively, so both endpoint maps have nonzero kernel.

Substituting `Q(lambda)=sum_i q_i lambda^i` into

```text
(V_h-lambda U_h)Q(lambda)=0
```

and comparing coefficients gives (ShortKEL), after first dividing by the
lowest power of `lambda` appearing in `Q` if necessary.  The final bound on
`Lambda_{K,>b}` follows from Corollary 46, which gives
`Lambda_{K,>b} subset Lambda_h`.

## Corollary 52: Moving Short Certificates Have Lossless Common-Root Stripping

Let `A=(alpha_1,...,alpha_e)` be a list of field elements, with `e<h`, and
put `L_A` and `Delta_A` as in Corollary 49.

Suppose a moving short fixed-kernel certificate has a common `L_A` factor:

```text
Q(lambda,X)=L_A(X)R(lambda,X),        deg_X R<h-e,
```

and satisfies the polynomial identity

```text
H_{t+2,h-1}(v-lambda u)Q(lambda,X)=0
```

over `F[lambda]`.  Then

```text
H_{t+2,h-e-1}(Delta_A v - lambda Delta_A u)R(lambda,X)=0.    (MoveStripK)
```

In particular, after stripping the full common `D`-root divisor of the moving
certificate, the remaining fixed-kernel moving short certificate has no root in
`D` common to all parameter values.

Similarly, suppose a moving short first-difference certificate has a common
`L_A` factor:

```text
Q(theta,X)=L_A(X)R(theta,X),        deg_X R<h-e,
```

and satisfies

```text
H_{t+1,h-1}(Delta_theta u)Q(theta,X)=0,
H_{t+1,h-1}(Delta_theta v)Q(theta,X)=0
```

as polynomial identities in `theta`.  Then

```text
H_{t+1,h-e-1}(Delta_A Delta_theta u)R(theta,X)=0,
H_{t+1,h-e-1}(Delta_A Delta_theta v)R(theta,X)=0.             (MoveStripD)
```

Thus common domain-root factors in the moving-certificate alternatives are not
new obstructions: they are fixed-root/root-slice pieces plus lower-order moving
certificates for differenced syndrome data.  The genuinely new moving
short-certificate obstruction may be assumed common-root-free over `D`.

### Proof

Corollary 49 is an identity of coefficient vectors and therefore remains valid
over the polynomial coefficient rings `F[lambda]` and `F[theta]`.

For the fixed-kernel moving certificate, apply (Strip) with
`w=v-lambda u` and with coefficients in `F[lambda]`.  Linearity of `Delta_A`
over `F[lambda]` gives

```text
Delta_A(v-lambda u)=Delta_A v - lambda Delta_A u,
```

so the stripped identity is exactly (MoveStripK).

For the first-difference moving certificate, apply (Strip) over `F[theta]`
separately to `w=Delta_theta u` and `w=Delta_theta v`.  Since the difference
operators commute, this gives (MoveStripD).  Taking `A` to be the full
`D`-root divisor common to all coefficient polynomials of `Q` leaves a
nonzero moving certificate with no common root in `D`.

## Corollary 53: Four Short Injectivity Checks Close The Endpointized Charge

Keep `h=c-b`.  Assume the four short endpoint systems are injective:

```text
ker H_{t+2,h-1}(u)=0,
ker H_{t+2,h-1}(v)=0,
ker J_0^(h)=0,
ker J_+^(h)=0.                                      (ShortInj)
```

Then the four base endpoint checks (BaseEP) from Corollary 45 hold:

```text
dim ker H_{t+2,c-1}(u) <= b,
dim ker H_{t+2,c-1}(v) <= b,
dim ker J_0            <= b,
dim ker J_+            <= b.
```

Moreover the endpointized finite-exception sets satisfy

```text
|Lambda_{K,>b}| <= h,        |Theta_{D,>b}| <= h.    (ShortClose)
```

Consequently, after charging the at most `2h` endpointized exceptional
systems indexed by

```text
Lambda_{K,>b} union Theta_{D,>b},
```

every remaining endpointized system in Corollary 42 has direction dimension at
most `b`.  Hence the endpointized global full-core and all-anchor full-core
bounds of Corollaries 42 and 43 apply to the uncharged ledger, with the
root-free refinements after common-root global core pieces are charged.

Thus the endpointized charge can be closed by four short injectivity checks;
failure of those checks is exactly the short-annihilator obstruction analyzed
in Corollaries 46--52.

### Proof

Corollary 46 says that if any one of the four base endpoint direction spaces
had dimension `>b`, then the corresponding short system in (ShortInj) would
have nonzero kernel.  Therefore (ShortInj) implies (BaseEP).

For fixed-kernel parameters, Corollary 48 applies because both
`H_{t+2,h-1}(u)` and `H_{t+2,h-1}(v)` are injective.  Hence

```text
|Lambda_h| <= h.
```

Since Corollary 46 gives `Lambda_{K,>b} subset Lambda_h`, the first estimate
in (ShortClose) follows.

For first-difference parameters, Corollary 48 applies because both `J_0^(h)`
and `J_+^(h)` are injective.  Hence `|Theta_h|<=h`, and Corollary 46 gives
`Theta_{D,>b} subset Theta_h`, proving the second estimate in (ShortClose).

The systems `U`, `V`, and `D_infty=J_0` from Corollary 42 have direction
dimension at most `b` by (BaseEP).  Outside the finite sets
`Lambda_{K,>b}` and `Theta_{D,>b}`, the systems `K_lambda` and `D_theta` have
direction dimension at most `b` by definition.  Therefore, once those finite
exceptional systems are charged, the hypotheses of Corollaries 42 and 43 hold.

## Corollary 54: Short Injectivity Is A Concrete Hankel-Minor Target

Let

```text
H_{s,h-1}(w): F^h -> F^s
```

be the short Hankel map on degree-`<h` directions.

1. The single-syndrome short endpoint map `H_{s,h-1}(w)` can be injective only
   if `h<=s`.  If `h<=s`, its injectivity locus is a nonempty determinantal
   open condition in the syndrome entries of `w`.

2. The stacked two-syndrome short endpoint map

```text
Q |-> (H_{s,h-1}(a)Q, H_{s,h-1}(b)Q)
```

   can be injective only if `h<=2s`.  If `h<=2s`, its injectivity locus is a
   nonempty determinantal open condition in the entries of `(a,b)`.

Consequently, the short closure criterion of Corollary 53 is dimensionally
available only in the range

```text
h<=t+2        for the single endpoint maps H_{t+2,h-1}(u), H_{t+2,h-1}(v),
h<=2(t+1)    for the stacked maps J_0^(h), J_+^(h).
```

In those ranges, the four short injectivity checks are explicit nonvanishing
conditions on `h x h` Hankel minors.  Outside those ranges, failure of the
corresponding short injectivity check is forced by row count and must be
handled by the short-annihilator/moving-certificate ledgers rather than by
Corollary 53.

### Proof

The necessity of `h<=s` and `h<=2s` is just row rank.

For the single-syndrome sufficiency, assume `h<=s` and choose the first `h`
rows.  Set the syndrome entries by

```text
w_m=1 if m=h-1,        w_m=0 otherwise
```

for `0<=m<=2h-2`.  The resulting `h x h` Hankel submatrix has entries
`w_{a+b}` and is the anti-identity matrix, hence has determinant `+/-1`.
Thus the corresponding minor is not the zero polynomial in the entries of
`w`, so the injectivity locus is a nonempty determinantal open set.

For the stacked map, the case `h<=s` follows from the first part using the
first block.  Suppose `s<h<=2s`, and put `r=h-s`.  For the first block choose

```text
a_m=1 if m=s-1,        a_m=0 otherwise.
```

Then the first `s` rows of `H_{s,h-1}(a)` form an anti-identity on the first
`s` columns and vanish on the remaining `r` columns.  For the second block
choose

```text
b_m=1 if m=h-1,        b_m=0 otherwise.
```

Use the first `r` rows of `H_{s,h-1}(b)`.  On the first `s` columns these rows
vanish, while on the last `r` columns they form an anti-identity.  The
resulting `h x h` minor of the stacked matrix is block anti-triangular with
determinant `+/-1`.  Therefore the relevant determinant is not identically
zero, and the stacked injectivity locus is nonempty and determinantal open.

## Corollary 55: The Endpoint-Short Closure Threshold Is `b>=c-(t+2)`

Keep `h=c-b` and assume `t>=0`.  Define

```text
b_min=max(0, c-(t+2)).
```

If

```text
b < c-(t+2),
```

then `h>t+2`, so neither single short endpoint map

```text
H_{t+2,h-1}(u),        H_{t+2,h-1}(v)
```

can be injective.  Hence the four-short-injectivity closure criterion of
Corollary 53 is impossible by row count, and the endpointized charge must be
handled through the short-annihilator ledgers.

If

```text
b>=b_min,
```

then `h<=t+2`.  In this range there is no row-count obstruction to any of the
four short injectivity checks:

```text
h<=t+2        for H_{t+2,h-1}(u), H_{t+2,h-1}(v),
h<=2(t+1)    for J_0^(h), J_+^(h).
```

Thus, for every feasible threshold `b>=b_min`, Corollary 53 reduces the
endpointized charge to explicit nonvanishing of four `h x h` Hankel minors
and to charging the at most `2h` endpointized exceptional systems if those
minor targets hold.  The threshold `b_min` is the smallest rank threshold at
which this particular short-injectivity route can close the endpointized
global full-core ledger.

### Proof

The identity `h=c-b` gives

```text
h<=t+2  <=>  b>=c-(t+2).
```

If this fails, Corollary 54 says the single endpoint maps cannot be injective,
so Corollary 53 cannot apply.

If `b>=b_min`, then `h<=t+2`.  Since `t>=0`, this implies

```text
h<=t+2<=2(t+1),
```

so the stacked short maps also pass the row-count test.  Corollary 54 then
identifies all four injectivity checks as explicit nonvanishing Hankel-minor
conditions.  Corollary 53 gives the endpointized charge closure once those
conditions hold.

## Corollary 56: Root-Free Short Failures Are Denominator Recurrences

Let `D subset F` be the evaluation domain.  For a polynomial

```text
Q(X)=q_0+q_1X+...+q_eX^e,        e<h,
```

say that `Q` is `D`-root-free if `Q(alpha)!=0` for every `alpha in D`.

For any syndrome vector `w`, the short Hankel equation

```text
H_{s,h-1}(w)Q=0
```

is exactly the length-`s` recurrence

```text
sum_{i=0}^e q_i w_{a+i}=0,        0<=a<s.           (Rec_Q)
```

Consequently:

```text
ker H_{s,h-1}(w) != 0
```

if and only if the syndrome window of `w` admits a nonzero denominator
recurrence of degree `<h`.

After the root-stripping reduction of Corollary 49, any short endpoint
annihilator can be written as a fixed-root/root-slice factor times a
`D`-root-free denominator recurrence for differenced syndrome data.

More explicitly:

* A root-free short witness for `lambda in Lambda_h` is exactly a
  `D`-root-free polynomial `Q` of degree `<h` satisfying

```text
sum_i q_i (v_{a+i}-lambda u_{a+i})=0,        0<=a<t+2.
```

  Thus the fixed-kernel short obstruction is a root-free denominator
  recurrence for the combined syndrome `v-lambda u`.

* A root-free short witness for `theta in Theta_h` is exactly a
  `D`-root-free polynomial `Q` of degree `<h` satisfying the two recurrences

```text
sum_i q_i (u_{a+i+1}-theta u_{a+i})=0,
sum_i q_i (v_{a+i+1}-theta v_{a+i})=0,        0<=a<t+1.
```

  Thus the first-difference short obstruction is a common root-free
  denominator recurrence for the differenced pair
  `(Delta_theta u, Delta_theta v)`.

Therefore the failure of the four short injectivity checks from Corollary 53
splits into fixed-root/root-slice pieces and root-free short denominator
recurrences.  These are the endpoint-local denominator objects that must be
charged by quotient-periodic, aperiodic packing, endpoint, or active-codegree
input in the M1 residue-line program.

### Proof

The `a`-th row of `H_{s,h-1}(w)Q` is

```text
sum_{i=0}^{h-1} w_{a+i}q_i,
```

with `q_i=0` for `i>e`.  This is exactly (Rec_Q), proving the recurrence
equivalence.

If a short annihilator has roots in `D`, Corollary 49 strips its full
`D`-root divisor and replaces `w` by the corresponding differenced syndrome.
The remaining factor is `D`-root-free by construction and still satisfies a
short Hankel equation at smaller degree.

The fixed-kernel and first-difference displayed recurrences are obtained by
applying the recurrence equivalence to `w=v-lambda u` and to
`w=Delta_theta u, Delta_theta v`, respectively.  The final statement is just
the union of these alternatives with the fixed-root/root-slice factors
separated by Corollary 49.

## Corollary 57: Short Recurrences Are Truncated Rational Denominators

Keep the notation of Corollary 56, and write

```text
Q(X)=q_0+q_1X+...+q_eX^e,        q_e!=0,
```

with reversed polynomial

```text
Q^*(T)=q_e+q_{e-1}T+...+q_0T^e.
```

Let

```text
W_w(T)=sum_{a>=0} w_a T^a
```

denote the syndrome generating series, truncated wherever only finitely many
coefficients are available.  Then

```text
H_{s,h-1}(w)Q=0
```

if and only if there is a polynomial `N_{Q,w}(T)` of degree `<e` such that

```text
Q^*(T) W_w(T) = N_{Q,w}(T)       mod T^{e+s}.        (Pade_Q)
```

Equivalently,

```text
W_w(T) = N_{Q,w}(T)/Q^*(T)       mod T^{e+s}.
```

Thus the root-free short endpoint obstruction from Corollary 56 is a
truncated rational-denominator obstruction:

* a root-free fixed-kernel witness for `lambda` gives the degree-`<=e`
  denominator `Q^*` for the combined series `W_{v-lambda u}(T)` through order
  `e+t+2`;
* a root-free first-difference witness for `theta` gives the same denominator
  `Q^*` simultaneously for `W_{Delta_theta u}(T)` and
  `W_{Delta_theta v}(T)` through order `e+t+1`.

After the fixed-root/root-slice factors have been stripped, the remaining
endpoint-short failure is therefore a `D`-root-free Pade/residue-denominator
certificate for the combined or differenced syndrome series.  This is the same
kind of denominator object that appears in the all-line residue-packing
normal form.

### Proof

The coefficient of `T^{a+e}` in `Q^*(T)W_w(T)` is

```text
sum_{i=0}^e q_i w_{a+i}.
```

Therefore the recurrence from Corollary 56 for `0<=a<s` is exactly the
vanishing of all coefficients of `Q^*W_w` in degrees `e,e+1,...,e+s-1`.
Modulo `T^{e+s}`, only coefficients in degrees `<e` remain; these form the
polynomial `N_{Q,w}`.  The two endpoint specializations are obtained by taking
`w=v-lambda u` and `w=Delta_theta u, Delta_theta v`, respectively.

## Corollary 58: Root-Free Denominators Avoid Reciprocal Domain Poles

Let `Q` and `Q^*` be as in Corollary 57, and define the projective reciprocal
domain

```text
D^vee={1/alpha : alpha in D, alpha!=0} union ({infty} if 0 in D).
```

Then `Q` is `D`-root-free if and only if the reversed denominator `Q^*` has no
zero on `D^vee`, where the point `infty` is tested by the leading coefficient
of `Q^*` in degree `e`.

Equivalently, after Corollary 49 has stripped all domain-root factors from a
short endpoint annihilator, the rational denominator `Q^*` in Corollary 57 has
no reciprocal-domain potential poles.  Conversely, every nonzero domain root
`alpha` of `Q` gives the denominator factor

```text
1-alpha T
```

of `Q^*(T)`, and a domain root at `alpha=0` is exactly a missing top-degree
term of `Q^*`, i.e. a denominator zero at the projective point `infty`.

Thus the fixed-root/root-slice charge in locator language is the same as
removing reciprocal-domain denominator factors in the Pade/residue-denominator
language.  The remaining root-free endpoint-short obstruction is a rational
denominator whose possible poles avoid the reciprocal evaluation domain.

### Proof

For `alpha!=0`,

```text
Q(alpha)=alpha^e Q^*(1/alpha).
```

Hence `Q(alpha)=0` if and only if `Q^*(1/alpha)=0`.  If `0 in D`, then
`Q(0)=q_0`; this is nonzero if and only if the coefficient of `T^e` in `Q^*`
is nonzero, which is exactly nonvanishing at the reciprocal point `infty` in
the degree-`e` projective denominator.  The factor statement follows from

```text
(X-alpha)^*(T)=1-alpha T        (alpha!=0)
```

and from the same top-degree coefficient test for `alpha=0`.

## Corollary 59: Half-Window Pade Uniqueness Compresses Denominator Families

Let `w` be a syndrome series, and suppose two short denominators

```text
Q_i(X)=q_{i,0}+...+q_{i,e_i}X^{e_i},        q_{i,e_i}!=0,
```

with reversed denominators `D_i(T)=Q_i^*(T)` satisfy

```text
D_i(T) W_w(T) = N_i(T)       mod T^{e_i+s},        deg N_i<e_i
```

for `i=1,2`.  If

```text
s >= max(e_1,e_2),
```

then

```text
N_1(T)D_2(T)=N_2(T)D_1(T).
```

Consequently every order-`<=s` truncated rational-denominator certificate for
the same scalar syndrome series determines the same reduced rational function.
In particular, after reducing `N_i/D_i`, the reduced denominator divides every
certificate denominator `D_i=Q_i^*`.

The same statement holds componentwise for a pair of syndrome series
`(w_1,w_2)`: if a common denominator `D_i` gives numerators
`N_{i,1},N_{i,2}` for both series and `s>=max(e_1,e_2)`, then the reduced
vector rational function

```text
(N_{i,1},N_{i,2})/D_i
```

is independent of the chosen common certificate, and its primitive denominator
divides every common certificate denominator.

Thus, in the half-window range, the root-free endpoint-short obstruction is
compressed to a primitive reciprocal-domain-pole-free denominator plus
allowable root-free multipliers.  For the fixed-kernel endpoint witnesses this
applies whenever `e<=t+2`; for the first-difference common witnesses it
applies whenever `e<=t+1`.  Outside this range the remaining obstruction is
genuinely a longer vector-Pade problem rather than a uniqueness consequence.

### Proof

For `i=1,2`, write

```text
D_iW_w-N_i = T^{e_i+s} E_i(T)
```

in the truncated formal power series ring.  Multiplying the first congruence
by `D_2`, the second by `D_1`, and subtracting gives

```text
N_1D_2-N_2D_1 = T^{e_2+s}D_1E_2 - T^{e_1+s}D_2E_1.
```

Hence `N_1D_2-N_2D_1` is divisible by

```text
T^{min(e_1+s,e_2+s)}.
```

On the other hand,

```text
deg(N_1D_2-N_2D_1) < e_1+e_2.
```

The hypothesis `s>=max(e_1,e_2)` gives

```text
min(e_1+s,e_2+s) >= e_1+e_2,
```

so the polynomial must be zero.  This proves equality of the two rational
functions.  Reducing the common rational function then shows that its reduced
denominator divides each `D_i`.

For two syndrome series, apply the scalar argument to each component.  The
common reduced vector denominator is the least common multiple of the reduced
component denominators, and therefore divides every common denominator
certificate.  The endpoint interpretations are Corollaries 56--58 with
`s=t+2` for fixed-kernel witnesses and `s=t+1` for first-difference witnesses.

## Corollary 60: Half-Window Certificates Lie In A Multiplier Ledger

Assume the half-window hypothesis of Corollary 59 for all degree-`<h`
denominator certificates under consideration; equivalently, every certificate
degree `e<h` also satisfies `e<=s`.  Let `D_0(T)` be the primitive reduced
denominator supplied by Corollary 59 for a scalar syndrome series, or the
primitive vector denominator in the two-series case.  Write

```text
delta=deg D_0.
```

Then every degree-`<h` certificate denominator `D(T)=Q^*(T)` lies in the
multiplier ledger

```text
D(T)=D_0(T) M(T),        deg M <= h-1-delta.        (Mult)
```

If the certificate is root-free, then `M` has no zeros on the reciprocal
domain `D^vee` from Corollary 58, with the point at infinity tested in the
actual degree of the multiplier.  Hence, over a finite field `F_q`, the
projective number of root-free degree-`<h` certificate denominators attached
to a fixed primitive denominator is at most

```text
(q^{h-delta}-1)/(q-1).
```

The actual certificate set is a subset of this multiplier ledger, because the
truncation congruence may impose additional linear conditions on `M`.

Consequently, in the half-window endpoint-short range, the denominator-family
problem splits into two parts:

1. bound the primitive reciprocal-domain-pole-free denominators `D_0`;
2. pay only the explicit multiplier factor above for each such primitive
   denominator.

### Proof

By Corollary 59, the reduced scalar rational function, or reduced vector
rational function in the two-series case, is independent of the chosen
certificate.  Therefore its primitive denominator `D_0` divides every
certificate denominator `D=Q^*`.  Since `deg D<=deg Q<h`, the quotient
`M=D/D_0` satisfies `deg M<=h-1-delta`, proving (Mult).

If `D` has no reciprocal-domain zeros and `D_0` divides `D`, then `D_0` and
`M` separately have no reciprocal-domain zeros, with each factor read in its
own projective degree.  Conversely, any zero of `M` on `D^vee` would be a zero
of `D`, contradicting root-freeness.

The projective space of nonzero multipliers of degree at most `h-1-delta` has
size

```text
1+q+...+q^{h-1-delta}=(q^{h-delta}-1)/(q-1).
```

The root-free and truncation conditions only remove points from this projective
space, so this gives the claimed upper bound.

## Corollary 61: Primitive Denominators Remain Valid Certificates

In the half-window setting of Corollary 60, let `D=D_0M` be an order-`<h`
certificate denominator for a scalar syndrome series or for a pair of series.
Here the order is the locator degree `e` in `Q(X)` and the congruence modulus
`T^{e+s}`; the ordinary `T`-degree of the reversed denominator `D=Q^*` may be
smaller.  Let `D_0` be the primitive reduced denominator from Corollary 59.
Then `D_0` itself is a certificate denominator.  More precisely, if

```text
D(T)W_w(T)=N(T)       mod T^{e+s},
```

where `e` is the certificate order, and the reduced rational function is
`N_0/D_0`, then

```text
D_0(T)W_w(T)=N_0(T)       mod T^{delta+s},        delta=deg D_0.
```

The same holds componentwise for a pair of syndrome series with the primitive
vector denominator `D_0`.

If `D` is root-free in the sense of Corollary 58, then `D_0` is also
root-free.  Thus, in the half-window range, existence of a root-free
order-`<h` certificate is equivalent to existence of a root-free primitive
certificate denominator of degree `<h`; multipliers affect the number of
certificates, but not the existence of the underlying endpoint-short
obstruction.

### Proof

By Corollary 59, reducing `N/D` gives the same rational function `N_0/D_0`;
hence `D=D_0M` and `N=N_0M`.  Since `D=Q^*` is a reversed denominator with
nonzero constant term, `M(0)!=0`, so multiplication by `M` is invertible in
`F[[T]]`.  From

```text
M(D_0W_w-N_0)=DW_w-N
```

and the divisibility of `DW_w-N` by `T^{e+s}`, it follows that
`D_0W_w-N_0` is divisible by `T^{e+s}`, hence by `T^{delta+s}`.  The
componentwise statement is identical.  Root-freeness passes to factors by
Corollary 58.

## Corollary 62: Parameter Collisions Are Base Endpoint Denominators

Let `D(T)` be an order-`e` reversed denominator with `D(0)!=0` and `e<h`.

### Fixed-Kernel Parameters

Suppose two distinct parameters `lambda_1,lambda_2` satisfy

```text
D(T)W_{v-lambda_i u}(T)=N_i(T)       mod T^{e+t+2},
deg N_i<e,        i=1,2.
```

Then `D` is a common base endpoint denominator for `u` and `v`:

```text
D(T)W_u(T)= (N_1-N_2)/(lambda_2-lambda_1)       mod T^{e+t+2},
```

and

```text
D(T)W_v(T)= (lambda_2 N_1-lambda_1 N_2)/(lambda_2-lambda_1)
        mod T^{e+t+2}.
```

Equivalently, in locator language, the corresponding reversed locator lies in

```text
ker H_{t+2,h-1}(u) cap ker H_{t+2,h-1}(v).
```

### First-Difference Parameters

Suppose two distinct parameters `theta_1,theta_2` satisfy, for both
`w=u` and `w=v`,

```text
D(T)W_{Delta_{theta_i} w}(T)=N_{i,w}(T)       mod T^{e+t+1},
deg N_{i,w}<e,        i=1,2.
```

Then `D` is a common base endpoint denominator for `u` and `v` at depth
`t+1`:

```text
D(T)W_u(T)= (N_{1,u}-N_{2,u})/(theta_2-theta_1)       mod T^{e+t+1},
```

and

```text
D(T)W_v(T)= (N_{1,v}-N_{2,v})/(theta_2-theta_1)       mod T^{e+t+1}.
```

Equivalently, the reversed locator lies in

```text
ker H_{t+1,h-1}(u) cap ker H_{t+1,h-1}(v).
```

Consequently, after charging primitive denominators already lying in the
appropriate base endpoint intersections, the map from bad parameters to
primitive denominators is injective separately for the fixed-kernel family and
for the first-difference family.  Any remaining parameter multiplicity is
therefore an endpoint charge, not a new residue-line obstruction.

### Proof

For fixed-kernel parameters,

```text
W_{v-lambda_1u}-W_{v-lambda_2u}=(lambda_2-lambda_1)W_u.
```

Subtracting the two congruences gives the displayed congruence for `D W_u`;
substituting back into either congruence gives the displayed congruence for
`D W_v`.  These are exactly the denominator forms of the two Hankel endpoint
equations.

For first-difference parameters,

```text
W_{Delta_{theta_1}w}-W_{Delta_{theta_2}w}
        =(theta_2-theta_1)W_w.
```

Applying this identity for `w=u` and `w=v` gives the two displayed base
endpoint congruences.  The final injectivity statement follows from Corollary
61: if two uncharged parameters shared a primitive denominator, that primitive
denominator would itself be a certificate for both parameters and hence would
fall into the charged base endpoint intersection.

## Corollary 63: Base-Free Primitive Parameters Are Rank-One Landings

Let `D(T)` be an order-`d` reversed denominator with `d<h`.  For a syndrome
series `w`, define the tail coefficient vector

```text
R_s(D;w)=([T^d]D(T)W_w(T), ..., [T^{d+s-1}]D(T)W_w(T)) in F^s.
```

Then `D` is a denominator certificate for `w` through window length `s` if and
only if

```text
R_s(D;w)=0.
```

### Fixed-Kernel Parameters

Set

```text
U_D=R_{t+2}(D;u),        V_D=R_{t+2}(D;v).
```

Then `D` supports a finite fixed-kernel parameter `lambda` if and only if

```text
V_D=lambda U_D.                                      (FKLand)
```

If `D` is not in the base endpoint intersection

```text
U_D=0,        V_D=0,
```

then any supported `lambda` is unique, `U_D!=0`, and the condition is the
rank-one landing condition

```text
V_D in F U_D.
```

### First-Difference Parameters

Let `S w` denote the shifted syndrome `(S w)_a=w_{a+1}`.  Set

```text
B_D=(R_{t+1}(D;u), R_{t+1}(D;v)) in F^{2(t+1)},
A_D=(R_{t+1}(D;S u), R_{t+1}(D;S v)) in F^{2(t+1)}.
```

Then `D` supports a finite first-difference parameter `theta` if and only if

```text
A_D=theta B_D.                                      (FDLand)
```

If `D` is not in the base endpoint intersection

```text
B_D=0,
```

then any supported `theta` is unique, `B_D!=0`, and the condition is the
rank-one landing condition

```text
A_D in F B_D.
```

Consequently, after the base endpoint denominators from Corollary 62 are
charged, the remaining primitive denominator families are contained in two
explicit determinantal incidence loci in the denominator coefficients:

```text
V_D in F U_D,        U_D!=0,
```

for fixed-kernel parameters, and

```text
A_D in F B_D,        B_D!=0,
```

for first-difference parameters.  The entries of these vectors are linear in
the coefficients of `D`, so the landings are cut out by the corresponding
`2 x 2` minors, together with the root-free open condition from Corollary 58
and the primitive-denominator condition from Corollary 61.

### Proof

The congruence

```text
D(T)W_w(T)=N(T)       mod T^{d+s},        deg N<d,
```

is equivalent to the vanishing of the coefficients of `D W_w` in degrees
`d,d+1,...,d+s-1`, which is exactly `R_s(D;w)=0`.

For fixed-kernel parameters, apply this equivalence to
`w=v-lambda u`.  Linearity of `R_s` gives

```text
R_{t+2}(D;v-lambda u)=V_D-lambda U_D,
```

which proves (FKLand).  If `U_D=0`, then a supported finite `lambda` forces
`V_D=0`, i.e. the base endpoint intersection.  Outside that intersection
`U_D!=0`, and the scalar `lambda` is unique.

For first-difference parameters, use

```text
Delta_theta w=S w-theta w.
```

The two denominator equations for `u` and `v` are therefore equivalent to
`A_D-theta B_D=0`, proving (FDLand).  If `B_D=0`, support forces `A_D=0` and
the denominator is in the base endpoint intersection already charged in
Corollary 62.  Otherwise `B_D!=0`, and the scalar `theta` is unique.  The
determinantal description is the standard collinearity equations for two
vectors.

## Corollary 64: The Endpoint-Short Threshold Is Entirely Half-Window

Let

```text
h=c-b.
```

Assume the endpoint-short closure threshold from Corollary 55:

```text
b >= b_min=max(0,c-(t+2)).
```

Equivalently, in the nonvacuous range `h>0`,

```text
h <= t+2.
```

Then every order-`<h` endpoint-short denominator certificate lies in the
half-window range of Corollaries 59--63.

More explicitly:

* fixed-kernel certificates use the window length `s=t+2`; since
  `e<h<=t+2`, every certificate order satisfies `e<=s`;
* first-difference certificates use the window length `s=t+1`; since
  `e<h<=t+2`, every certificate order satisfies `e<=t+1=s`.

Therefore, at every threshold where the four short endpoint injectivity checks
from Corollary 53 are row-count feasible, the remaining root-free
endpoint-short obstruction has no longer vector-Pade part.  After fixed-root,
base endpoint, and parameter-collision charges, the only uncharged
endpoint-short denominator families are primitive reciprocal-domain-pole-free
rank-one landing loci from Corollary 63, with the explicit multiplier ledger
from Corollary 60.

Below this threshold, the single endpoint maps cannot be injective by row
count, so the short-injectivity closure route of Corollary 53 is already
unavailable.

### Proof

If `h=0`, there are no nonzero order-`<h` certificates, so the statement is
vacuous.  Otherwise, Corollary 55 gives `h<=t+2`.

For a fixed-kernel certificate, the window length is `s=t+2`.  Since
`e<h<=t+2`, we have `e<=s`, so the half-window hypothesis holds.

For a first-difference certificate, the window length is `s=t+1`.  Since
`e<h` and `h<=t+2`, we have `e<=h-1<=t+1=s`, so the half-window hypothesis
again holds.  Corollaries 59--63 then apply to every endpoint-short
certificate.  The below-threshold statement is exactly the row-count
obstruction from Corollary 55.

## Corollary 65: Zero-Dimensional Landing Layers Have Explicit Size

Fix an order `d<h`, and let

```text
P_d=P({order-d reversed denominators D(T)=a_0+...+a_dT^d})
```

be the projective denominator coefficient space.  The order condition
`D(0)!=0`, the reciprocal-domain root-free condition from Corollary 58, and the
base-free conditions from Corollaries 62--63 are all open conditions on `P_d`.

Let `L_d^K` be the projective rank-one landing locus cut out by the fixed-kernel
minors

```text
U_i(D)V_j(D)-U_j(D)V_i(D)=0,
```

where `U_D=R_{t+2}(D;u)` and `V_D=R_{t+2}(D;v)`.  Let `L_d^D` be the
first-difference landing locus cut out by the minors

```text
A_i(D)B_j(D)-A_j(D)B_i(D)=0,
```

where `A_D,B_D` are the doubled vectors from Corollary 63.  These minors are
homogeneous quadrics in the denominator coefficients.

If the projective closure of the base-free root-free part of `L_d^K` is
zero-dimensional over the algebraic closure, then it has at most

```text
2^d
```

geometric points, counted without multiplicity.  The same bound holds for
`L_d^D`.

Consequently, at the endpoint-short threshold of Corollary 64, if every
order layer `0<=d<h` of the base-free primitive fixed-kernel landing locus is
zero-dimensional, then after the endpoint and collision charges of Corollary
62 the remaining fixed-kernel bad parameters contribute at most

```text
sum_{d=0}^{h-1} 2^d = 2^h-1.
```

The identical bound holds for the first-difference bad parameters under the
same zero-dimensionality hypothesis for the first-difference landing layers.

Thus the remaining primitive-denominator task is sharpened to a dichotomy:
either the rank-one landing layers are finite and explicitly bounded by the
displayed Bezout ledger, or there is a positive-dimensional primitive
rank-one landing component to classify or charge.

### Proof

The maps `D -> U_D,V_D,A_D,B_D` are linear in the denominator coefficients by
Corollary 63, so the collinearity equations are homogeneous quadrics on
`P_d`.  Open conditions can only remove points from the projective closure.

A zero-dimensional projective subvariety of `P^d` cut out by quadrics has
degree at most `2^d` by the standard projective Bezout bound; hence it has at
most `2^d` geometric points.  This proves the order-layer bounds.  Corollary
62 makes the parameter-to-primitive-denominator map injective after the base
endpoint collision charges, so summing over `0<=d<h` gives the displayed
`2^h-1` bound.  If the zero-dimensionality hypothesis fails, the failure is
precisely a positive-dimensional primitive rank-one landing component.

## Corollary 66: Positive-Dimensional Landings Are Moving Denominator Certificates

Fix an order `d<h`, and work over an algebraic closure.  Let `C` be an
irreducible positive-dimensional component of the remaining base-free
root-free fixed-kernel landing locus from Corollary 63, after restricting to
the primitive denominator open set.  Let

```text
K=F(C)
```

be its function field.  Then the generic point of `C` gives:

* an order-`d` denominator

```text
D_C(T)=a_0+a_1T+...+a_dT^d in K[T],        a_0!=0,
```

  with no reciprocal-domain zeros over `K`;
* a unique parameter `lambda_C in K`;
* a numerator `N_C(T)` of degree `<d`;

such that

```text
D_C(T) W_{v-lambda_C u}(T)=N_C(T)       mod T^{d+t+2}.        (MoveK)
```

Moreover `lambda_C` is constant on `C` if and only if the component lies in a
fixed-parameter landing slice.  Otherwise `lambda_C` is a genuinely moving
parameter certificate.

Similarly, if `C` is an irreducible positive-dimensional component of the
remaining base-free root-free first-difference landing locus, then the generic
point gives an order-`d` denominator `D_C(T)` with no reciprocal-domain zeros,
a unique `theta_C in K`, and numerators `N_{C,u},N_{C,v}` of degree `<d` such
that

```text
D_C(T) W_{Delta_{theta_C} u}(T)=N_{C,u}(T)       mod T^{d+t+1},
D_C(T) W_{Delta_{theta_C} v}(T)=N_{C,v}(T)       mod T^{d+t+1}.        (MoveD)
```

Again `theta_C` is either constant on the component or is a genuinely moving
first-difference parameter.

Consequently, after the finite Bezout ledger of Corollary 65 is applied, every
remaining positive-dimensional primitive denominator obstruction is an
explicit moving denominator certificate over a function field.  Classifying or
charging M1 in this branch is therefore equivalent to ruling out, absorbing
into fixed-parameter endpoint charges, or otherwise controlling the moving
certificates (MoveK) and (MoveD).

### Proof

At the generic point of a component meeting the order, root-free, base-free,
and primitive opens, the denominator coefficients define `D_C(T)` with
`a_0!=0` and no reciprocal-domain zero.  In the fixed-kernel case, Corollary 63
gives

```text
V_{D_C} in K U_{D_C},        U_{D_C}!=0.
```

Hence there is a unique `lambda_C in K` with `V_{D_C}=lambda_C U_{D_C}`.  By
the same corollary, this is exactly the order-`d` denominator congruence
(MoveK), with `N_C` equal to the truncation of `D_C W_{v-lambda_Cu}` in
degrees `<d`.

The first-difference case is identical, using

```text
A_{D_C} in K B_{D_C},        B_{D_C}!=0,
```

to obtain the unique `theta_C` and the two congruences (MoveD).  A rational
function on `C` is constant exactly when it belongs to the constant field;
otherwise it is a moving parameter.  This proves the stated dichotomy.

## Corollary 67: Constant-Parameter Components Are High-Dimensional Fixed Slices

Fix an order `d<h`.

### Fixed-Kernel Slices

For a finite parameter `lambda`, define the order-`d` fixed-kernel recurrence
space

```text
K_{d,lambda}={D in F^{d+1} : R_{t+2}(D;v-lambda u)=0}.
```

If an irreducible positive-dimensional component from Corollary 66 has
constant fixed-kernel parameter `lambda_C=lambda`, then

```text
dim K_{d,lambda} >= 2.
```

Conversely, the projectivization `P(K_{d,lambda})` is exactly the
denominator landing slice with fixed parameter `lambda`; its root-free,
primitive, order-`d`, and base-free parts are obtained by imposing the
corresponding open conditions.

Thus constant-parameter fixed-kernel components are precisely
high-dimensional fixed-slice short-recurrence spaces for the combined syndrome
`v-lambda u`.

### First-Difference Slices

For a finite parameter `theta`, define

```text
D_{d,theta}={D in F^{d+1} :
  R_{t+1}(D;Delta_theta u)=0 and R_{t+1}(D;Delta_theta v)=0 }.
```

If an irreducible positive-dimensional component from Corollary 66 has
constant first-difference parameter `theta_C=theta`, then

```text
dim D_{d,theta} >= 2.
```

Conversely, `P(D_{d,theta})` is exactly the denominator landing slice with
fixed first-difference parameter `theta`, again up to the same root-free,
primitive, order, and base-free opens.

Consequently, after high-dimensional fixed-slice recurrence spaces are charged,
every positive-dimensional primitive landing component left by Corollary 65 has
genuinely nonconstant parameter.  The remaining moving-denominator obstruction
is therefore not a constant fixed-slope artifact.

### Proof

For fixed `lambda`, the equation `R_{t+2}(D;v-lambda u)=0` is linear in the
coefficients of `D`, and by Corollary 63 it is exactly the fixed-parameter
landing slice.  A positive-dimensional projective component contained in this
linear slice forces the underlying vector space to have dimension at least
two.  The open conditions only remove closed exceptional subsets, so the
converse description is immediate.

The first-difference case is the same with the two simultaneous linear
conditions for `Delta_theta u` and `Delta_theta v`.  The final statement is the
constant/moving dichotomy from Corollary 66 after the constant slices have
been charged.

## Corollary 68: Nonconstant Moving Components Are Persistent One-Parameter Kernels

Fix an order `d<h`, and work over an algebraic closure.  Let `Z` be an
indeterminate.

### Fixed-Kernel Pencil

Define the one-parameter linear pencil

```text
M_d^K(Z): F(Z)^{d+1} -> F(Z)^{t+2},
M_d^K(Z)D = R_{t+2}(D;v-Zu).
```

If a positive-dimensional primitive landing component from Corollary 66 has
genuinely nonconstant fixed-kernel parameter `lambda_C`, then

```text
ker M_d^K(Z) != 0        over F(Z).                 (PersK)
```

Equivalently, the order-`d` recurrence pencil for `v-Zu` has a persistent
generic denominator over the parameter line.  When full column rank is
row-count possible, this says that all full-column minors of `M_d^K(Z)` vanish
as polynomials in `Z`; when `d+1>t+2`, the kernel is row-count forced and the
remaining content is in the root-free, primitive, and base-free opens.

Conversely, any nonzero vector in `ker M_d^K(Z)` whose root-free, primitive,
order-`d`, and base-free conditions are not identically violated gives, after
clearing denominators and restricting to a nonempty open subset of the
parameter line, a positive-dimensional fixed-kernel landing family.

### First-Difference Pencil

Define the stacked one-parameter pencil

```text
M_d^D(Z): F(Z)^{d+1} -> F(Z)^{2(t+1)},
M_d^D(Z)D =
  (R_{t+1}(D;Delta_Z u), R_{t+1}(D;Delta_Z v)).
```

If a positive-dimensional primitive landing component from Corollary 66 has
genuinely nonconstant first-difference parameter `theta_C`, then

```text
ker M_d^D(Z) != 0        over F(Z).                 (PersD)
```

Equivalently, all full-column minors of the stacked first-difference recurrence
pencil vanish whenever full column rank is row-count possible.  Conversely, a
nonzero generic kernel vector satisfying the same nonempty open conditions
gives a positive-dimensional first-difference landing family over the
parameter line.

Thus, after the constant-parameter slices of Corollary 67 are charged, the only
remaining positive-dimensional primitive denominator obstruction is a
persistent one-parameter short-recurrence kernel for the fixed-kernel pencil
`v-Zu` or the first-difference pencil `(Delta_Z u, Delta_Z v)`.

### Proof

Let `C` be a component with nonconstant fixed-kernel parameter `lambda_C` and
function field `K=F(C)`.  Since the constant field is algebraically closed,
`lambda_C` is transcendental over `F`, so `F(lambda_C)` is isomorphic to
`F(Z)`.  Corollary 66 gives a nonzero vector

```text
D_C in K^{d+1}
```

with `M_d^K(lambda_C)D_C=0`.  Kernel dimension over a matrix field is unchanged
after extending scalars, so `M_d^K(Z)` already has nonzero kernel over `F(Z)`.
The full-column-minor formulation is the standard rank criterion, with the
row-count-forced exception as stated.

Conversely, a vector in `ker M_d^K(Z)` gives a rational denominator family over
the parameter line.  Clearing common denominators in `Z` and restricting away
from their poles gives a regular family.  If the root-free, primitive,
order-`d`, and base-free open conditions are not identically violated, a
nonempty open subset is a positive-dimensional landing family.

The first-difference proof is identical using the stacked matrix `M_d^D(Z)` and
the parameter `theta_C`.

## Corollary 69: Persistent Pencils Force Endpoint Rank Failure

Fix an order `d<h`.

### Fixed-Kernel Pencil

Let

```text
U_d(D)=R_{t+2}(D;u),        V_d(D)=R_{t+2}(D;v),
```

so that

```text
M_d^K(Z)=V_d-ZU_d.
```

Assume `d+1<=t+2`, so full column rank is row-count possible.  If

```text
ker M_d^K(Z) != 0        over F(Z),
```

then both endpoint maps fail to be injective:

```text
ker U_d != 0,        ker V_d != 0.
```

Equivalently, a persistent fixed-kernel denominator pencil of order `d` forces
short endpoint annihilators for both `u` and `v`.

### First-Difference Pencil

Let

```text
B_d(D)=(R_{t+1}(D;u), R_{t+1}(D;v)),
A_d(D)=(R_{t+1}(D;S u), R_{t+1}(D;S v)),
```

so that

```text
M_d^D(Z)=A_d-ZB_d.
```

Assume `d+1<=2(t+1)`, so full column rank is row-count possible.  If

```text
ker M_d^D(Z) != 0        over F(Z),
```

then both endpoint intersection maps fail to be injective:

```text
ker A_d != 0,        ker B_d != 0.
```

Equivalently, a persistent first-difference denominator pencil of order `d`
forces a common short endpoint annihilator for `(S u,S v)` and a common short
endpoint annihilator for `(u,v)`.

At the endpoint-short threshold of Corollary 64, every order `d<h` satisfies
the two row-count hypotheses above.  Therefore any persistent one-parameter
kernel left by Corollary 68 forces failure of one of the four short endpoint
injectivity checks from Corollary 53:

```text
H_{t+2,h-1}(u),        H_{t+2,h-1}(v),
J_0^(h),               J_+^(h).
```

Consequently, if those four short endpoint systems are injective, then there
are no nonconstant positive-dimensional primitive rank-one landing components
after the fixed-root, base endpoint, collision, and constant-slice charges.  In
that case the genuinely moving primitive denominator contribution is removed;
the remaining fixed-parameter positive slices are the finite/persistent
constant-slice ledger of Corollary 70.

### Proof

For the fixed-kernel pencil, `ker M_d^K(Z)!=0` and `d+1<=t+2` imply that every
`(d+1) x (d+1)` minor of `V_d-ZU_d` vanishes as a polynomial in `Z`.  The
constant coefficient of such a minor is the corresponding minor of `V_d`, and
the top-degree coefficient is, up to sign, the corresponding minor of `U_d`.
Thus all full-column minors of both `U_d` and `V_d` vanish, so neither endpoint
map has full column rank.

The first-difference argument is identical for the stacked pencil `A_d-ZB_d`.
At the endpoint-short threshold, `d<h<=t+2`, so `d+1<=t+2` for fixed-kernel
systems and `d+1<=t+2<=2(t+1)` for first-difference systems.  A kernel vector
for any order `d<h` is also a nonzero vector in the corresponding order-`<h`
short endpoint system, so injectivity of the four Corollary 53 systems rules
out all such persistent kernels.  The final statement combines this with
Corollaries 60, 65, 67, and 68.

## Corollary 70: Constant-Slice Parameters Have A Finite/Persistent Dichotomy

Fix an order `1<=d<h`, and keep the endpoint-short threshold of Corollary 64.

### Fixed-Kernel Slices

Let

```text
KBad_d={lambda : dim K_{d,lambda} >= 2},
```

where `K_{d,lambda}` is the fixed-kernel recurrence space from Corollary 67.
Equivalently, `lambda in KBad_d` if and only if

```text
rank(V_d-lambda U_d) <= d-1.
```

Then either

```text
|KBad_d| <= d,
```

or the pencil is persistently rank-deficient at level `d`:

```text
rank(V_d-ZU_d) <= d-1        over F(Z).
```

In the persistent case both endpoint maps have two-dimensional kernel:

```text
dim ker U_d >= 2,        dim ker V_d >= 2.
```

### First-Difference Slices

Let

```text
DBad_d={theta : dim D_{d,theta} >= 2},
```

where `D_{d,theta}` is the simultaneous first-difference recurrence space from
Corollary 67.  Equivalently,

```text
rank(A_d-theta B_d) <= d-1.
```

Then either

```text
|DBad_d| <= d,
```

or the stacked first-difference pencil is persistently rank-deficient:

```text
rank(A_d-ZB_d) <= d-1        over F(Z),
```

and in that case

```text
dim ker A_d >= 2,        dim ker B_d >= 2.
```

Consequently, after charging endpoint maps with two-dimensional short kernels,
the constant-parameter positive-dimensional landing slices contribute at most

```text
sum_{d=1}^{h-1} d = h(h-1)/2
```

parameters in each of the fixed-kernel and first-difference families.

### Proof

For fixed-kernel slices, `dim K_{d,lambda}>=2` is equivalent to rank at most
`d-1` for the `(t+2) x (d+1)` matrix `V_d-lambda U_d`, hence to vanishing of
all its `d x d` minors.  Each such minor is a polynomial in `lambda` of degree
at most `d`.  If one minor is nonzero, it has at most `d` roots, proving the
finite alternative.  If all `d x d` minors vanish identically in `Z`, then the
pencil has rank at most `d-1` over `F(Z)`.  The constant and top-degree
coefficients of these minors are the corresponding minors of `V_d` and `U_d`
up to sign, so all `d x d` minors of both endpoint matrices vanish.  Since the
domain dimension is `d+1`, both endpoint kernels have dimension at least two.

The first-difference proof is identical with the stacked pencil `A_d-ZB_d`.
At the endpoint-short threshold the row counts needed for these `d x d` minors
are available because `d<h<=t+2` and therefore `d<=t+1<=2(t+1)`.  Summing the
finite alternative over `1<=d<h` gives the displayed bound.

## Corollary 71: Short Injectivity Leaves Only Finite Parameter Ledgers

Keep `h=c-b`, assume the endpoint-short threshold of Corollary 64, and assume
the four short endpoint systems from Corollary 53 are injective:

```text
ker H_{t+2,h-1}(u)=0,
ker H_{t+2,h-1}(v)=0,
ker J_0^(h)=0,
ker J_+^(h)=0.                                      (ShortInj)
```

After the fixed-root/root-slice charges, base endpoint denominator charges,
and parameter-collision charges, the remaining primitive endpoint-short
denominator obstruction has the following finite parameter ledger in each of
the fixed-kernel and first-difference families:

1. the zero-dimensional base-free primitive landing layers contribute at most

```text
2^h-1
```

parameters, as in Corollary 65;

2. the constant-parameter positive-dimensional landing slices contribute at
most

```text
h(h-1)/2
```

parameters, as in Corollary 70; and

3. there are no nonconstant positive-dimensional moving primitive landing
components.

Thus, for the denominator-geometric accounting left after the standard charges,
the primitive endpoint-short parameter ledger is finite, with the explicit
per-family bound

```text
(2^h-1)+h(h-1)/2,
```

for bad parameters.  Corollary 60 supplies an extra multiplier ledger only when
one counts certificate witnesses rather than parameter values; Corollary 72
below records this separation.  This is a geometric finite-ledger statement.
It is not an improvement over Corollary 53's sharper direct
exceptional-parameter bound `|Lambda_{K,>b}|, |Theta_{D,>b}| <= h` under the
same short injectivity hypotheses.

### Proof

At the endpoint-short threshold, Corollary 64 puts every order `d<h` primitive
denominator in the half-window range.  Therefore Corollaries 63--66 apply to
the base-free root-free primitive denominator classes after the fixed-root,
base endpoint, and collision charges.

The four short injectivity checks imply that the order-`d` endpoint maps
appearing in Corollaries 69 and 70 have no kernel.  Indeed, `U_d` and `V_d`
are the restrictions of `H_{t+2,h-1}(u)` and `H_{t+2,h-1}(v)` to
order-`d` denominators.  Likewise `B_d` and `A_d` are the restrictions of
`J_0^(h)` and `J_+^(h)` to the same order layer.

Now take a positive-dimensional primitive landing component.  If its parameter
is nonconstant, Corollary 68 turns it into a persistent one-parameter kernel.
Corollary 69 says such a persistent kernel forces nonzero endpoint kernels for
the corresponding order-`d` maps, contradicting (ShortInj).  Hence nonconstant
moving components do not occur.

It remains to account for constant-parameter positive slices and
zero-dimensional layers.  Corollary 70 gives, for each order `1<=d<h`, at most
`d` constant-slice parameters unless the corresponding endpoint maps have
two-dimensional kernels.  Under (ShortInj) those two-dimensional endpoint
kernel alternatives are impossible, so the constant slices contribute at most
`sum_{d=1}^{h-1}d=h(h-1)/2` parameters per family.  Corollary 65 gives the
separate Bezout ledger `sum_{d=0}^{h-1}2^d=2^h-1` for zero-dimensional
base-free primitive landing layers.  Multipliers do not change the parameter
attached to an uncharged primitive denominator, as recorded in Corollary 72, so
no Corollary 60 multiplier factor is needed for parameter counting.  This
completes the finite parameter accounting.

## Corollary 72: Multipliers Do Not Multiply Endpoint-Short Parameters

Assume the half-window setting of Corollary 60, and charge the base endpoint
denominator intersections from Corollary 62.

### Fixed-Kernel Parameters

Let `D=D_0M` be a degree-`<h` certificate denominator for the fixed-kernel
parameter `lambda`, with primitive denominator `D_0` from Corollary 60.  Then
`D_0` supports the same parameter `lambda`.  If `D_0` supported any distinct
fixed-kernel parameter `lambda'`, then `D_0` would lie in the charged base
endpoint denominator intersection.

Consequently all uncharged multiplier certificates lying over the same
primitive denominator have the same fixed-kernel parameter.  The multiplier
ledger of Corollary 60 is therefore a witness-counting ledger, not a multiplier
for the number of fixed-kernel bad parameters.

### First-Difference Parameters

Let `D=D_0M` be a degree-`<h` common certificate denominator for the
first-difference parameter `theta`.  Then `D_0` supports the same parameter
`theta`.  If `D_0` supported any distinct first-difference parameter `theta'`,
then `D_0` would lie in the charged base endpoint denominator intersection at
depth `t+1`.

Consequently all uncharged multiplier certificates lying over the same
primitive denominator have the same first-difference parameter.  The
multiplier ledger of Corollary 60 is again certificate-only for parameter
counting.

Thus, after the standard collision charges, bad endpoint-short parameters
inject into primitive denominator classes.  Counting primitive denominators
already upper bounds the parameter sets; multipliers need be paid only for
claims that count certificates or locator witnesses themselves.

### Proof

For fixed-kernel parameters, Corollary 61 says that the primitive denominator
`D_0` remains a valid certificate after cancelling the multiplier `M`.  The
cancelled certificate has the same combined syndrome `v-lambda u`, so it
supports `lambda`.  If it also supported a distinct `lambda'`, Corollary 62
would make `D_0` a common base endpoint denominator for `u` and `v`, which is
one of the charged collision cases.

The first-difference proof is identical componentwise.  Corollary 61 leaves
`D_0` as a common certificate for `(Delta_theta u,Delta_theta v)`.  A second
parameter `theta'` for the same primitive denominator would be a Corollary 62
collision and hence a charged base endpoint denominator at depth `t+1`.

## Non-Claims

This note does not prove

```text
|Boundary_off| <= n^B.
```

It also does not prove the all-line M1 theorem, a corrected-reserve MCA bound,
or a prize threshold. It only proves the local external-anchor normal form and
the nondegenerate/ruled split for the boundary target image already isolated in
the variable-line packet lemma. Corollary 9 is a closure criterion: it says
which shadow-image estimates would imply a polynomial boundary-off bound in
the polynomial-field regime, not that those estimates have already been
proved. Corollary 10 does not prove that the common-image row-cut ranks are
large; it identifies the low-rank image-line locus as the remaining obstruction
inside that branch. Corollary 11 similarly does not prove large ranks for the
fixed-slope or contained row-cut systems; it records the exact rank certificates
needed for those ruled ledgers. Corollary 12 does not rule out the persistent
low-rank alternative; it shows that this persistent alternative is the only way
for the finite-slope row-rank obstruction to involve more than `m-b` slopes at
a fixed rank threshold. Corollary 13 does not bound the exceptional high-rank
fixed-slope shadows; it separates them from the bounded-rank residual so they
can be charged to the fixed-slope/root-slice ledger. Corollary 14 does not
prove that the persistent polynomial-kernel certificates cannot occur; it
turns that case into an explicit algebraic certificate to rule out, classify,
or charge. Corollary 15 shows that such certificates force endpoint low-rank
ledgers; it does not prove those endpoint ledgers are small without a separate
charge. Corollary 16 similarly makes the common-image low-rank locus
projective and determinantal; it does not bound the split shadows supported on
the exceptional projective low-rank lines without charging that locus.
Corollary 17 is conditional on those explicit low-rank charges and endpoint
rank hypotheses; it is not an unconditional ruled-branch theorem.
Corollary 17.1 does not remove the low-rank exceptional loci; it only sharpens
the bounded-rank row-rank ledgers after common-root subledgers have already
been charged to fixed-root/root-slice ledgers.
Corollary 18 does not bound the unique-neighbor nondegenerate shadows; it
separates them from the popular shadows that are already controlled by the
first three active exchange profiles. Corollary 19 is a sharpness statement for
the exchange-profile method; it does not assert that such separated families
occur as active Hankel locators in the M1 problem. Corollary 20 only moves
full anchor stars into fixed-root/root-slice algebraic factors; it does not
bound the remaining star-free unique-neighbor nondegenerate shadows.
Corollary 21 classifies repeated full-star factors of a single anchor minor;
it does not prove that the star-free zero set of that minor is small.
Corollary 22 is again per fixed anchor minor: it bounds the zeros left after
identically vanishing core-lines have been charged, but it does not bound the
number of such core-lines or the common zero set of all anchor minors.
Corollary 23 identifies those identically vanishing core-lines as explicit
lower-dimensional Hankel-wedge coefficient equations; it does not bound their
common zero set.
Corollary 24 classifies core-lines on which the full rank-one anchor gate
holds identically; it does not bound how many cores fall into the lower
endpoint, common-image, or fixed-kernel ruled ledgers.
Corollary 25 applies the core-line reduction to the full rank-one gate rather
than to one fixed minor; it still leaves the full core-line ledgers from
Corollary 24 to be bounded or charged separately.
Corollary 26 gives row-rank certificates for those full core-line ledgers; it
does not prove that the exceptional lower systems all have bounded direction
dimension without separate endpoint, image-line, or fixed-kernel charges.
Corollary 27 isolates the finite fixed-kernel part of the lower full-core
ledger; it still leaves the finite exceptional slopes or the persistent
lower-kernel alternative to be charged separately.
Corollary 28 shows that the persistent lower-kernel alternative forces lower
endpoint low-rank ledgers and has moving-core certificates; it does not bound
those endpoint ledgers without a separate charge.
Corollary 29 makes the lower common-image ledger projective-determinantal; it
does not bound the split cores on the exceptional low-rank image lines or rule
out the moving-image certificate without a separate charge.
Corollary 30 packages the fixed-anchor full-core analysis after lower
rank-ledger charges; it still leaves the one-root-loss residual and the
explicit charged exceptional ledgers as separate obligations.
Corollary 30.1 adds a root-free slice saving only after lower common-root core
subledgers have already been charged; it does not remove the Corollary 25
one-root-loss residual.
Corollary 31 bounds the number of endpoint-bad anchors only outside the
persistent endpoint-anchor alternative; that persistent case remains an
explicit moving-certificate ledger. Corollary 32 does not prove that the
two-parameter fixed-kernel bad pair locus is empty or small enough for M1 by
itself; it makes that locus determinantal and separates the finite pair-locus
case from the moving two-parameter certificate case. Corollary 33 similarly
does not prove that the common-image bad anchor-line incidence is empty; it
turns that incidence into a finite determinantal charge or a moving
anchor-image certificate. Corollary 34 is an all-anchor incidence closure after
explicit lower charges; it still leaves the charged loci, persistent
certificates, and one-root-loss residual as the remaining M1 obligations.
Corollary 35 does not classify globally full core-lines; it shows that all
other full-core lines have anchor multiplicity at most two. Corollary 36
classifies globally full core-lines into three-shift ruled ledgers, but it does
not prove the required high-dimensional three-shift row-rank charges are small.
Corollary 37 makes those charges determinantal; it still leaves endpoint
three-shift low rank and persistent moving certificates as explicit ledgers to
charge. Corollary 38 identifies the endpoint and fixed-kernel three-shift
ledgers with deeper Hankel windows; it does not prove those deeper windows have
large rank in every instance. Corollary 38.1 shows that consecutive frontier
shifts are lossless identities; it does not supply the lower-depth rank,
injectivity, or endpoint-charge bounds consumed by those identities.
Corollary 38.2 gives the same finite/persistent dichotomy for consecutive
fixed-kernel slope charges; it does not bound the deeper endpoint kernels in
the persistent alternative. Corollary 39 reduces the non-shift-persistent
common-image lines to the deeper endpoint intersection; it still leaves that
intersection and the `q+1` extended geometric shift lines to be charged.
Corollary 40 identifies those shift-persistent lines with first-difference
endpoint intersections; it does not prove all those endpoint intersections
have small dimension without a separate endpoint or quotient-periodic charge.
Corollary 40.1 shows the same endpoint-only common-image reduction for
consecutive shift stacks; it does not bound the resulting deeper endpoint,
first-difference, or infinity endpoint ledgers.
Corollary 40.2 gives the finite/persistent dichotomy for the resulting
first-difference parameters; it does not prove the ordinary or shifted stacked
endpoint maps are low-dimensional in the persistent alternative.
Corollary 40.3 packages these consecutive-frontier ledgers under four endpoint
rank hypotheses; it does not prove those endpoint hypotheses or close the
separate nondegenerate shadow ledger.
Corollary 40.4 reduces those endpoint hypotheses to four short frontier
injectivity checks; it does not prove the short checks in every instance or
remove the row-count restrictions for that route.
Corollary 40.5 sums the depthwise charges over a finite frontier ladder; it
does not prove the short checks uniformly over all depths or replace the
remaining endpoint and nondegenerate ledgers.
Corollary 40.6 identifies failures of those short checks as denominator
recurrences and strips domain-root factors; it does not bound the remaining
root-free recurrence families.
Corollary 40.7 identifies those root-free recurrence families as the remaining
short-frontier residual after fixed-root/root-slice charges; it does not prove
that the root-free residual is empty or small.
Corollary 40.8 compresses half-window root-free residuals to primitive
reciprocal-domain-pole-free denominators; it does not bound the number of
primitive denominators.
Corollary 40.9 uses nesting to charge a finite ladder at its bottom rung when
the bottom short checks hold; it does not prove those bottom short checks.
Corollary 40.10 shows root-free residual witnesses also nest to the bottom
rung; it does not bound the bottom root-free residual families.
Corollary 40.11 packages a bottom-rung closure criterion for finite nested
frontier ladders; it does not solve the bottom root-free primitive denominator
targets.
Corollary 40.12 identifies the overlap of the ordinary and shifted paired
root-free residuals with the endpoint-pair residual; it does not bound that
endpoint-pair residual.
Corollary 40.13 packages consecutive paired-overlap losslessness; it does not
bound the deepest paired residual itself.
Corollary 40.14 identifies the first half-window cutoff for primitive
denominator charges; it does not count the cutoff primitive denominators or
resolve the pre-half-window longer-Pade residuals.
Corollary 40.15 packages the mixed-ladder closure ledger; it does not prove
the pre-half residual charges or bound the first half-window primitive
denominator targets.
Corollary 40.16 proves tail primitive denominators refine the cutoff
denominator; it does not count the cutoff primitive bases or the allowed
multiplier refinements.
Corollary 40.17 bounds only the ambient multiplier ledger attached to a fixed
cutoff primitive denominator; it does not prove which multiplier classes
satisfy the deeper recurrence equations.
Corollary 40.18 sums those ambient ledgers over the four residual families; it
does not turn the denominator-class budget into an MCA slope count.
Corollary 40.19 identifies paired-tail overlaps with endpoint-pair residual
charges; it does not bound the endpoint-pair residual.
Corollary 40.20 identifies scalar-paired tail overlaps with one-sided endpoint
residual charges; it does not bound those one-sided residual systems.
Corollary 40.21 identifies scalar-scalar tail overlap with the endpoint-pair
residual; it does not bound that residual.
Corollary 40.22 makes the charged half-window tail family-disjoint; it does
not bound the endpoint-pair or one-sided overlap charges it assumes removed.
Corollary 40.23 packages the refined mixed-ladder closure; it does not prove
the pre-half residual, cutoff primitive-denominator, or cutoff overlap
charges it lists as inputs. Corollary 40.24 compresses the cutoff overlap
charges into at most five half-window multiplier ledgers; it does not bound the
parent primitive overlap denominators or prove that the one-sided extra rows
leave few multipliers. Corollary 40.25 shows those overlap ledgers refine lcms
of the cutoff family primitive denominators; it does not bound those family
primitive denominators themselves or prove the lcm degrees are large enough for
the desired M1 reserve. Corollary 40.26 gives a one-row saving for one-sided
cutoff overlaps unless the parent paired kernel is endpoint-persistent; it
does not rule out that persistence alternative. Corollary 40.27 turns endpoint
persistence into an explicit stacked-Hankel row-span test and gives the
two-row endpoint-pair codimension formula; it does not prove the missing rows
are independent in the M1 instances. Corollary 40.28 packages those ranks into
a cutoff-overlap projective budget; it does not prove the rank defects are
absent or that the resulting budget is below the final M1 reserve. Corollary
40.29 combines the rank budget with the lcm multiplier budget by termwise
minima; it does not prove either savings mechanism is always strong enough.
Corollary 40.30 packages these terms into a mixed-ladder upper ledger; it does
not prove the pre-half residuals are small or that this upper ledger is sharp.
Corollary 40.31 separates raw denominator counting from proof-separation
accounting; by itself it does not improve the raw `FamilyBudget_hw` count.
Corollary 40.32 gives an inclusion-exclusion rank budget for the
cutoff-overlap union; it does not prove the required endpoint-row ranks are
generically full.
Corollary 40.33 substitutes the smaller overlap-union separation charge into
the mixed-ladder upper ledger and removes the redundant endpoint-pair summand
from the hybrid side; it does not change the raw tail count or solve the
pre-half residuals.
Corollary 40.34 improves the raw unlabelled half-window tail count to the
divisor-arrangement inclusion-exclusion budget of the active cutoff primitive
denominators; it does not bound those primitive denominators, prove their lcm
degrees are large, or solve the pre-half residuals.
Corollary 40.35 packages that raw arrangement tail into the mixed-ladder
closure; it is still an upper ledger and does not prove the arrangement budget
is below the final M1 reserve.
Corollary 40.36 gives the direct raw-tail closure without a separate overlap
denominator charge; it does not make the overlap diagnostics unnecessary for
family-disjoint audits or prove the raw arrangement ledger clears the final M1
reserve.
Corollary 40.37 removes divisibility-dominated families from the raw tail
arrangement; it does not prove that the surviving antichain is small or that
the active denominators form a chain in the M1 instances.
Corollary 40.38 factors a common denominator core out of the raw tail
arrangement; it does not prove such a common core is large or that the quotient
denominators are pairwise coprime in the M1 instances.
Corollary 40.39 turns the common-core degree into a one-parameter raw-tail
bound; it does not prove the common-core degree reaches the displayed
thresholds.
Corollary 40.40 gives a minimum-quotient-degree saving after the common core
is factored; it does not prove that quotient degree is large enough in the M1
instances.
Corollary 40.41 identifies the residual dimension condition that would give a
polynomial-field raw-tail ledger; it does not prove the required lower bound
`gamma+e_min>=h-L`.
Corollary 40.42 gives an exact formula when two minimal denominators survive;
it does not prove the raw tail always reduces to two denominators or that the
two quotient degrees clear the reserve.
Corollary 40.43 removes any pre-half depth sum by charging the bottom
root-free residual families once; it does not bound those bottom residual
families.
Corollary 40.44 packages the residual bottleneck as a two-route minimum; it
does not estimate either the bottom longer-Pade family or the pre-half
residual family.
Corollary 40.45 replaces raw multiplier projective spaces by exact root-free
multiplier counts in the multiplicative-domain case; it does not prove which
primitive denominators occur or that the root-free arrangement clears the M1
reserve.
Corollary 40.46 improves the residual-tail criterion using those root-free
counts; it still depends on proving the structural lower bound
`gamma+e_min>=h-L`.
Corollary 40.47 gives the root-free common-core and two-denominator formulas;
it does not prove that a large common core exists, that only two minimal
denominators survive, or that the quotient degrees are large enough.
Corollary 40.48 gives a bottom-route root-free count under a domain-MDS test
on the bottom recurrence kernels; it does not prove those kernels are in
domain-MDS position or have bounded dimension in the M1 instances.
Corollary 40.49 identifies that domain-MDS test with the stripped
fixed-root/root-slice rank profile; it does not prove the no-excess
root-slice rank equalities for all root sets.
Corollary 40.50 reduces the domain-MDS check to top root slices or evaluation
determinants; it does not prove those determinants are nonzero in the M1
instances.
Corollary 40.51 gives an exact two-dimensional kernel count in terms of
projective evaluation-line collisions; it does not prove those collisions are
absent or small for the M1 bottom kernels.
Corollary 40.52 bounds the two-dimensional collision defect by pair root-slice
collisions; it does not prove the pair collision count is small in the M1
instances.
Corollary 40.53 bounds two-dimensional collision defects by projective degree;
it does not prove the bottom projective degrees are small in the M1 instances.
Corollary 40.54 bounds that projective degree using a common factor; it does
not prove the required large common factors occur in the M1 bottom kernels.
Corollary 40.55 shows maximal common factors force the ideal bottom count; it
does not prove the bottom kernels have maximal common factors.
Corollary 40.56 bounds bottom kernels by the residual quotient window after a
common factor is removed; it does not prove those residual windows are small in
the M1 instances.
Corollary 40.57 refines the ladder bottleneck by substituting the
common-factor bottom-window charge and the root-free half-window arrangement
charge into the two-route minimum; it does not prove either route satisfies
the required M1 reserve bound in the actual instances.
Corollary 40.58 identifies the bottom common-factor target with a Hankel
row-span/rank certificate modulo a divisor of degree at least `h-L`; it does
not prove that such divisors exist for the actual M1 bottom matrices.
Corollary 40.59 identifies split bottom certificates with external-anchor
evaluation rows, and repeated roots with Hasse-jet rows; it does not prove
that enough such anchors occur or that nonsplit certificates can be ignored.
Corollary 40.60 identifies external-anchor row membership with common roots of
the bottom kernel; it does not count enough external anchors in the actual M1
instances.
Corollary 40.61 turns non-domain anchor counts into bottom residual-window
bounds and gives an exact count in the rank-matched case; it does not prove
that the actual bottom Hankel row spaces contain enough such anchors.
Corollary 40.62 rewrites bottom-anchor membership as a short-multiplier
truncated moment certificate; it does not prove those moment certificates
exist for enough non-domain anchors.
Corollary 40.63 identifies the full-domain moment case with Lagrange
interpolation degree tests and rules out non-domain anchors in windows
`h>=|D|+1`; it does not solve the short-window case `h<|D|`.
Corollary 40.64 gives a dual common-zero test for full-domain paired anchors;
it reduces their count to a common-gcd degree but does not bound that degree
in the actual M1 instances.
Corollary 40.65 gives the corresponding short-window dual test; it reduces
short-window anchor counting to a degree-`<h` common-gcd problem but does not
bound that gcd in the actual M1 instances.
Corollary 40.66 packages the four bottom-family dual gcds into a bottom-route
ledger; it does not prove the required lower bounds on their non-domain root
counts in the actual M1 instances.
Corollary 40.67 shows those root lower bounds are extra structure by giving
formal moment data with trivial dual gcd; it does not rule out special M1
syndromes satisfying the needed bounds.
Corollary 40.68 shows that this trivial-gcd obstruction is realized by local
Reed-Solomon syndrome windows after absorbing the nonzero parity-check column
scalars; it still does not construct an active noncontained M1 counterexample.
Corollary 40.69 identifies the half-window denominator threshold with absence
of low-degree root-free cutoff Hankel kernels; it does not prove those kernels
are absent in the actual M1 instances.
Corollary 40.70 gives an exact root-slice inclusion-exclusion count for those
low-degree root-free kernels; it does not evaluate the resulting stripped-rank
identity in the actual M1 instances.
Corollary 40.71 shows that, when `|D|<q`, low-degree root-free emptiness is
equivalent to injectivity after common domain-root slices are charged; it does
not prove the resulting injectivity in the actual M1 instances.
Corollary 40.72 packages that injectivity target as four explicit full-column
Hankel minor tests at the first half-window cutoff; it does not prove those
minors are nonzero in the actual M1 instances.
Corollary 40.73 shows those cutoff minor targets are extra M1 structure by
constructing syndrome-realizable local moment data where all four fail via the
root-free constant recurrence; it does not construct an active noncontained
M1 counterexample.
Corollary 40.74 identifies cutoff kernel failure with a low-degree
rational-supercode representation of the endpoint words; it does not prove
that those strata are small or quotient-periodic in the actual M1 instances.
Corollary 40.75 shows paired rational-supercode strata contribute at most one
noncontained slope above the displayed interpolation threshold; it does not
settle scalar strata or paired strata above that threshold.
Corollary 40.76 gives an analogous one-slope charge for scalar
rational-supercode strata under the stronger pairwise-intersection threshold;
Corollary 40.77 extends the same local argument below that threshold to a
q-free support-packing bound when `d<=a`; it does not prove that this packing
ledger is small enough for the final M1 reserve or handle the `d>a` range.
Corollary 40.78 shows this limitation is structural in the fixed-rate reserve
window: since scalar strata have `d>=k`, pure support packing is exponential
unless additional M1 structure reduces or removes the scalar branch.
Corollary 40.79 gives one such reduction target: scalar rational-supercode
strata inject into ordinary lists for the multiplied opposite endpoint in the
dimension-`d` RS supercode, up to the zero-slope exception in the `Qf` case.
Corollary 40.80 sharpens this target to a one-generator extension of the
multiplier code `Q RS[F,D,k]`, equivalently a one-dimensional residue line
modulo `Q`.
Corollary 40.81 makes the reduction exact: unless the scalar endpoint is
already global, the relevant generator coefficient parametrizes exactly the
explained scalar slopes, with only the zero-slope exception in the `Qf` case.
Corollary 40.82 shows that in the standard-degree range `n-s<=k+deg Q`, these
exact constrained scalar lists are ordinary lower-degree residue-line data
after subtracting a global quotient part of the scalar endpoint.
Corollary 40.83 classifies the complementary range `n-s>k+deg Q` as the same
residue-line datum over the enlarged dimension `K=n-s-deg Q`, cut by an
explicit affine return-to-`RS[F,D,k]` slice.
Corollary 40.84 identifies that return slice with a one-dimensional high-tail
incidence; if the quotient high tail vanishes, the non-standard case collapses
to the ordinary base-dimension residue-line datum.
Corollary 40.85 translates this at the scalar cutoff: non-standard scalar
strata of positive denominator degree are exactly the range
`1<=deg Q<j-r_hw`, with high-tail window length `j-r_hw-deg Q`.
Corollary 40.86 isolates the remaining constant scalar cutoff case as a
supercode endpoint high-tail branch, not a positive-degree residue-line datum.
Corollary 40.87 packages all short scalar return slices as effective
dimension-`k+1` high-tail-line subcodes of the enlarged code, with codimension
`L-1` in a high-tail window of length `L`.
Corollary 40.88 identifies the remaining one-row layer `L=1` as a
dimension-`k+1` linear-image list whose slope parameter is recovered from the
top coefficient, with the reciprocal `Qf` zero-slope exception still separate.
Corollary 40.89 rewrites that same layer, after dividing by the root-free
denominator, as list decoding against the rank-one rational extension
`RS_k+F(hX^k-B/Q)`; this is the precise all-line residue-packing object left
by the scalar one-row residual.
Corollary 40.90 primitive-compresses this object by replacing `Q` with
`Q/gcd(Q,B)`; nonprimitive residue presentations therefore do not create new
one-row packing families, and the `B=0` case is just the polynomial
`RS_{k+1}` endpoint.
Corollary 40.91 gives the resulting primitive-degree packing bound: distinct
one-row scalar parameters have supports intersecting in fewer than
`k+deg(Q_prim)+1` points, hence the coefficient set is bounded by
`binom(n,d_prim)/binom(a,d_prim)` when `d_prim<=a` and by one coefficient in
the pairwise-intersection range.
Corollary 40.92 translates this into the scalar cutoff variables: the one-row
packing charge is available exactly when `deg(Q_prim)<=t-1`, and the
one-coefficient charge when `deg(Q_prim)<=t-j-1`.
Corollary 40.93 gives the resulting residual split: after this charge, the
only positive one-row scalar residual has primitive denominator degree at least
`t`; constant and sufficiently nonprimitive positive branches are already
covered.
Corollary 40.94 converts any remaining one-row coefficient collision into a
short quotient-residue certificate `L_I M in F B_prim mod Q_prim`; at the
first unpacked layer, one-exchange collisions are linear residue landings.
Corollary 40.95 identifies those first-unpacked one-exchange landings as
either core landings or finite-anchor locators `L_I(X-beta)`, with
`beta notin D` giving exactly the external-anchor boundary type.
Corollary 40.96 extends the one-exchange analysis to all unpacked layers:
for each fixed overlap core, the admissible low-degree multiplier space has
dimension at most one, so one-exchange collisions have a unique projective
multiplier certificate if they exist.
Corollary 40.97 converts this into a packing-with-exceptions ledger:
one-row coefficients are bounded by
`(binom(n,a-1)+(n-a)|Exc_ell|)/a`, where `Exc_ell` is the set of cores
supporting a nonzero projective multiplier certificate.
Corollary 40.98 shows that those exceptional multipliers are automatically
coprime to `Q_prim`; equivalently the exceptional cores land in residue lines
`F B_prim M^{-1}` modulo `Q_prim` for invertible low-degree multipliers.
Corollary 40.99 decomposes the exceptional core ledger as a disjoint sum of
ordinary split-locator residue-line fibers indexed by those projective
low-degree multiplier classes.
Corollary 41 packages the common-image branch into endpoint-type ledgers; it
does not prove the endpoint rank hypotheses needed for the displayed
`(q+2)binom(n,b)` bound. Corollary 42 packages the globally full core ledger
after endpointized charges; it is still conditional on bounding those
endpoint-type charge dimensions and on charging the moving-certificate loci.
Corollary 43 propagates that endpointized bound to the all-anchor full-core
incidence; it does not remove the Corollary 25 one-root-loss residual or the
separate nondegenerate unique-neighbor shadow ledger. Corollary 44 makes the
first-difference endpoint charges determinantal; it does not rule out the
persistent first-difference moving-kernel alternative. Corollary 45 reduces
the endpointized finite-exception charge to four base endpoint checks; it does
not prove those base endpoint dimensions are always at most `b`. Corollary 46
turns high-dimensional endpointized charges into degree-`<c-b`
short-annihilator certificates; it does not prove those short systems are
always injective or that the resulting short annihilators are already
quotient-periodic/root-slice charges. Corollary 47 organizes the short bad
parameters as images of projective short-locator landing varieties, except for
common short endpoint kernels; it does not bound those landing varieties.
Corollary 48 bounds the short parameter sets under one-sided short endpoint
injectivity; it does not prove that such injectivity always holds. Corollary
49 strips domain-root factors from short annihilators; it does not bound the
remaining root-free short-annihilator families. Corollary 50 identifies
first-difference short parameters with roots of common endpoint recurrences;
it does not bound the dimension of that common recurrence space. Corollary 51
turns fixed-kernel short parameters into a finite/persistent pencil dichotomy;
it does not rule out the persistent moving short-recurrence certificate.
Corollary 52 strips common domain-root factors from moving short certificates;
it does not rule out the resulting common-root-free moving certificates.
Corollary 53 is a conditional closure criterion; it does not prove the four
short endpoint systems are injective. Corollary 54 gives feasibility and
nonempty determinantal targets for those injectivity checks; it does not prove
the actual syndromes lie in the open injectivity loci. Corollary 55 identifies
the row-count threshold for this short-injectivity route; it does not prove
the required Hankel minors are nonzero above that threshold. Corollary 56
identifies the remaining root-free short failures as denominator recurrences;
Corollary 57 rewrites those recurrences as truncated rational-denominator
certificates; and Corollary 58 identifies the root-free condition with absence
of reciprocal-domain denominator poles. Corollary 59 gives uniqueness and
primitive-denominator compression only in the half-window range; it does not
bound the primitive denominators or the longer vector-Pade range. Corollary 60
only bounds the multiplier ledger attached to a fixed primitive denominator;
it does not bound how many primitive denominators occur. Corollary 61 removes
multiplier artifacts from existence questions, but not from certificate
counting. Corollary 62 charges parameter collisions to base endpoint
denominators; it does not bound the remaining injective set of primitive
denominators. Corollary 63 turns that remaining set into explicit rank-one
landing loci; it does not prove those loci have the required size. Corollary
64 shows that the longer vector-Pade range disappears at the endpoint-short
closure threshold; it does not bound the resulting primitive rank-one landing
loci. Corollary 65 bounds only zero-dimensional landing layers; it does not
exclude positive-dimensional primitive landing components. Corollary 66 turns
those components into moving denominator certificates, but does not classify or
bound those certificates. Corollary 67 identifies constant-parameter
components with high-dimensional fixed-slice recurrence spaces; it does not
bound the genuinely moving-parameter components. Corollary 68 turns
nonconstant components into persistent one-parameter kernels; it does not rule
out those persistent kernels or prove the required open conditions are empty.
Corollary 69 shows persistent kernels force endpoint rank failure in the
row-count feasible range; it does not prove the four endpoint systems are
always injective. Corollary 70 bounds constant-parameter positive slices only
after endpoint maps with two-dimensional short kernels have been charged.
Corollary 71 packages the primitive endpoint-short denominator obstruction
under the four short injectivity checks into a finite parameter ledger; it does
not prove those checks, improve Corollary 53's sharper `h` exceptional-parameter
bound, or eliminate the multiplier ledger attached to each primitive
denominator when certificates rather than parameters are being counted.
Corollary 72 separates parameter counts from certificate counts after collision
charges; it does not bound the number of certificate witnesses over a primitive
denominator beyond the Corollary 60 multiplier ledger.
