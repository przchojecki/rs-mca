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
