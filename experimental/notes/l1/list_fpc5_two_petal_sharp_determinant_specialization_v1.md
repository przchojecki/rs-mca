---
workboard_item: T
row: symbolic rate-half smooth RS FPC5 M=4,t=2 sharp source cell; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: shortened core agreement 3ell-2 on a core of size 5ell-5
B_star: not_applicable
direct_statement: the sharp guarded two-petal cell is a six-marked rational-map family, shortens to RS[C,2ell-1], and has one affine cross-cofactor coordinate whose gcd strata are exactly the common-error owners paid by the anchor determinant atlas
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed sharp guarded two-petal FPC5 source/pair cell
quantifier: every field and source tuple satisfying the printed hypotheses, every nonempty exact contributor cell, and every choice of anchor in that cell
projection_and_unit: distinct degree-below-(5ell-4) codewords in one fixed LIST source cell
claimed_bound: exact structural reductions and the fixed-owner minimum in equation (18); the maximal-intersection owner has at most two non-anchor neighbors; no aggregate owner or row bound
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a failure of shortening, a cross-coordinate collision, an owner-gcd mismatch, a marked-fiber violation, or a fixed-owner family exceeding the specialized atlas bound
replay: analytic proof; no computational claim
---

# Sharp FPC5 two-petal specialization of the anchor determinant atlas

## 1. Purpose and nonclaim

This note specializes the balanced-pencil anchor determinant atlas to the
sharp rate-half, four-petal, exactly-two-touched FPC5 cell. It banks three
compatible descriptions of the same contributor family:

1. a degree-`2ell-3` rational map with six distinct marked values on blocks
   that partition the full source domain;
2. an injection into one exact shell of `RS[C,2ell-1]`; and
3. an affine cross-cofactor coordinate of degree at most `ell-3` whose gcd
   with the anchor defect locator is exactly the common-error owner.

The third description identifies the fixed-owner bounds from
`list_balanced_pencil_anchor_determinant_atlas_v1.md` directly in the native
FPC5 coordinates. It removes coefficient-pair and fixed-owner multiplicity.
It does **not** bound the number of realized owners, prove a polynomial list
bound, deploy a finite row, or move a Prize endpoint.

## 2. Sharp guarded cell

Let `ell>=3`, put

```text
k=5ell-4,       n=2k=10ell-8,       d=2ell-3.        (1)
```

Let the evaluation domain be the disjoint union

```text
D=C disjoint_union B disjoint_union P_1 disjoint_union ... disjoint_union P_4,
|C|=5ell-5,       |B|=ell-3,       |P_i|=ell.        (2)
```

Write `L_0,L_1,...,L_4` for the monic locators of `B,P_1,...,P_4`.
Fix distinct nonzero labels `c_1,...,c_4` in the field. We study one exact
cell whose touched petals are `P_1,P_2`. Each contributor has cofactors

```text
deg A_1,deg A_2<=ell-3,       gcd(A_1,A_2)=1,        (3)
U_1=L_1A_1,       U_2=L_2A_2,
F=(U_1-U_2)/(c_2-c_1),
W=(c_2U_1-c_1U_2)/(c_2-c_1).                         (4)
```

The exact-cell guards are:

- `F` is monic, squarefree, has degree `d`, and splits on `C`;
- `gcd(F,W)=1`;
- `L_0|W`, so the entire background is fixed agreement;
- the contributor agrees on all of `P_1,P_2` and has no agreement on
  `P_3,P_4`; and
- on `C` its exact disagreement set is `Z(F)`.

These hypotheses are the native sharp-cell input. The conclusions below do
not assert that every point in the surrounding guarded linear slice obeys
the splitness or exactness filters.

## 3. Six-marked rational-map descriptor

Define the reduced rational function

```text
phi=U_1/U_2.                                           (5)
```

### Theorem 1: full-domain marked fibers

The numerator and denominator in `(5)` are coprime and `deg phi=d`. Every
contributor maps injectively to a rational function satisfying

```text
P_1 subset phi^(-1)(0),
P_2 subset phi^(-1)(infinity),
Z(F)=phi^(-1)(1),                         |Z(F)|=2ell-3,
B subset phi^(-1)(c_1/c_2),               |B|=ell-3,  (6)
P_u intersect phi^(-1)(alpha_u)=empty,    u=3,4,
alpha_u=(c_1-c_u)/(c_2-c_u).                          (7)
```

The six marked values

```text
0, infinity, 1, c_1/c_2, alpha_3, alpha_4             (8)
```

are pairwise distinct. The `1`-fiber is complete and reduced. Moreover, the
blocks carrying these conditions exhaust the official source domain because

```text
(5ell-5)+(ell-3)+4ell=10ell-8=n.                      (9)
```

#### Proof

A common root of `U_1,U_2` outside `P_1 union P_2` would be a common root of
`A_1,A_2`. A common root on either touched petal would also be a root of
`U_1-U_2`, hence of `F`, contrary to the disjoint supports in `(2)`. Thus
`U_1,U_2` are coprime. Since their difference is the nonzero scalar
`(c_2-c_1)F` of degree `d`, the reduced map has degree `d`.

The touched-petal locators give the zero and pole containments. Also

```text
phi=1  iff  U_1-U_2=0  iff  F=0.
```

The denominator cannot vanish at a root of `F`, and the squarefree degree-`d`
locator `F` supplies all `d` points of this fiber. Thus the `1`-fiber is
complete and reduced.

The equation `W=0` is equivalent to `phi=c_1/c_2`. At a background point,
`W=0` and

```text
W-c_2F=U_2=-c_2F!=0,
```

so the displayed ratio is defined. For `u=3,4`, direct substitution gives

```text
W-c_uF=((c_2-c_u)U_1+(c_u-c_1)U_2)/(c_2-c_1),       (10)
```

whose vanishing is equivalent to `phi=alpha_u`. The untouched-petal
nonagreement guard proves `(7)`.

The fractional-linear map `z -> (c_1-z)/(c_2-z)` is injective away from
`c_2`. Distinct nonzero labels therefore make the values in `(8)` pairwise
distinct. Finally, a reduced `phi` determines `(U_1,U_2)` up to common
scalar, and the requirement that `F` be monic fixes that scalar. Equations
`(4)` then recover `(F,W)`. The recovered `F` fixes the contributor's
agreement set

```text
(B union P_1 union P_2) union (C\Z(F)),
(ell-3)+2ell+(3ell-2)=6ell-5>k.
```

On this set the contributor equals the fixed received word, so these values
determine its degree-below-`k` polynomial uniquely. This proves injectivity.
Equation `(9)` is immediate from `(2)`. QED.

## 4. Fixed-agreement shortening

Let

```text
S_0=B union P_1 union P_2,       |S_0|=3ell-3.       (11)
```

Fix the received word `U` for this source. Let `Q_0` be its interpolating
polynomial on `S_0`, of degree below `3ell-3`, and let `L_(S_0)` be the
locator of `S_0`.

### Theorem 2: exact residual shell

Every contributor polynomial `P`, with `deg P<k`, has a unique form

```text
P=Q_0+L_(S_0)T,       deg T<2ell-1.                  (12)
```

On `C`, define

```text
v(x)=(U(x)-Q_0(x))/L_(S_0)(x).                       (13)
```

Then `P -> T` injects the contributor cell into the exact shell of

```text
RS[C,2ell-1] around v,
N=5ell-5,       K_0=2ell-1,
agreement m'=3ell-2,       radius omega=2ell-3.       (14)
```

In particular,

```text
omega=floor(2(N-K_0)/3).                             (15)
```

#### Proof

Every contributor agrees with `U` on `S_0`, so `P-Q_0` is divisible by
`L_(S_0)`. The quotient in `(12)` is unique and

```text
deg T <= (k-1)-|S_0|=2ell-2.
```

The denominator in `(13)` is nonzero on the disjoint core. Equation `(12)`
therefore gives `P(x)=U(x)` if and only if `T(x)=v(x)`. The exact core defect
has size `2ell-3`, so `T` has `(5ell-5)-(2ell-3)=3ell-2` agreements. Finally,
`N-K_0=3ell-4`, which proves `(15)`. QED.

### Corollary 2.1: specialized fixed-owner bounds

The shell `(14)` has the balanced-atlas parameters

```text
w=m'-K_0=ell-1,
s=omega-w=ell-2.                                     (16)
```

Fix an exact anchor with defect locator `F_0`. For a distinct contributor
with defect locator `F`, put

```text
D_0=gcd(F_0,F),       deg D_0=ell-3-j,
0<=j<=ell-3.                                           (17)
```

Theorem 3 of `list_balanced_pencil_anchor_determinant_atlas_v1.md` bounds
the non-anchor neighbors with this fixed owner by

```text
|C_(D_0)| <= min {
  floor(binom(3ell-2,j+1)/binom(ell+j,j+1)),
  max_(1<=r<=j+1)
    floor(binom(3ell-2,r)/(ell+j-r+1))
}.                                                    (18)
```

At maximal intersection, `j=0`, this becomes

```text
|C_(D_0)|<=floor((3ell-2)/ell)=2.                    (19)
```

This is a per-owner bound. The atlas does not permit summing `(18)` over all
divisors of `F_0` as a polynomial payment.

## 5. Native cross-cofactor coordinate

The background guard in `(4)` is the congruence

```text
c_2L_1A_1 == c_1L_2A_2  (mod L_0).                  (20)
```

Let `M` be the complete affine chart of pairs `(A'_1,A'_2)` satisfying
`(20)` whose associated locator `F` from `(4)` is monic of degree `d`. Fix
one exact anchor `(A_1,A_2,F_0)` in this chart. Define

```text
Delta_A=A_1A'_2-A'_1A_2,
E=Delta_A/L_0.                                        (21)
```

### Theorem 3: affine coordinate and exact owner recovery

The quotient in `(21)` is a polynomial of degree at most `ell-3`, and

```text
M -> F[X]_(<=ell-3),       (A'_1,A'_2) -> E           (22)
```

is an affine bijection sending the anchor to zero. Thus `E` determines the
guarded pair `(F,W)` before splitness and the remaining exactness filters are
imposed. For every distinct exact contributor,

```text
E!=0,       gcd(E,F_0)=gcd(F,F_0).                   (23)
```

Consequently the owner in `(17)` is the gcd stratum of one explicit
low-degree coordinate body, not an independently selected pencil.

#### Proof

The petal locators and labels are units modulo `L_0`. Thus `(20)` says that
there is one unit `mu` modulo `L_0` with

```text
A'_2=mu A'_1,       A_2=mu A_1  (mod L_0).
```

Hence `L_0|Delta_A`. The cofactor caps give
`deg Delta_A<=2ell-6`, so `deg E<=ell-3`.

The vector space of cofactor pairs in `(20)` has dimension `ell-1`: the
ambient pair space has dimension `2ell-4`, and the congruence has full rank
`ell-3`. Monicity cuts a nonempty affine hyperplane, so `M` has dimension
`ell-2`, equal to the dimension of `F[X]_(<=ell-3)`.

Suppose two points in `M` have the same coordinate. Their difference
`(B_1,B_2)` satisfies

```text
A_1B_2-B_1A_2=0.                                     (24)
```

Primitivity of the anchor gives `(B_1,B_2)=T(A_1,A_2)` for a polynomial
`T`. Since `(4)` is linear, the corresponding locator difference is
`TF_0`. But two monic degree-`d` locators differ in degree at most `d-1`,
whereas a nonzero `TF_0` has degree at least `d`. Therefore `T=0`.
The map is injective, and equality of affine dimensions proves `(22)`.

For `(23)`, let `x` be a root of the squarefree `F_0`. It lies in `C`, where
`L_0,L_1,L_2` are nonzero. The nonzero anchor vector
`(A_1(x),A_2(x))` lies in the one-dimensional kernel of

```text
(u,v) -> L_1(x)u-L_2(x)v.                            (25)
```

Since `L_0(x)!=0`, the equality `E(x)=0` says precisely that the second
cofactor vector is proportional to the anchor vector. This is equivalent to
the second vector lying in the kernel `(25)`, which by `(4)` is equivalent
to `F(x)=0`. Thus `E` and `F` have the same roots on `Z(F_0)`. Squarefreeness
of `F_0` proves the gcd equality. The bijection sends only the anchor to
zero, so a distinct contributor has `E!=0`. QED.

## 6. Exact remaining bridge

Relative to one anchor, the complete guarded monic slice is now the affine
coordinate body `F[X]_(<=ell-3)`. The still-open sharp count is exactly the
number of coordinates `E` for which the reconstructed locator `F_E`

- splits squarefreely on `C`;
- is primitive relative to the reconstructed numerator;
- satisfies the two untouched-petal exclusions in `(7)`; and
- survives any chronology or first-owner filters used by the surrounding
  LIST ledger.

Equivalently, one needs an aggregate gcd-owner coalescence theorem for this
single marked family. Theorems 1--3 show that neither enumeration of
background subsets, coefficient-pair multiplicity, nor a separate payment
for each fixed pencil is the missing step.
