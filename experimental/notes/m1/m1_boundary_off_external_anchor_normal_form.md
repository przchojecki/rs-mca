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
Corollary 18 does not bound the unique-neighbor nondegenerate shadows; it
separates them from the popular shadows that are already controlled by the
first three active exchange profiles.
