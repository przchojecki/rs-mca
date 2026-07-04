# Parametric list-MCA bridge lemma v1

Status: `PROPOSED_BRIDGE_LEMMA_FOR_REVIEW`

This note states the exact optimized statement used by the KoalaBear squeeze
appendix. It is not the displayed BCHKS25 Theorem 4.6 formula. It is the
same interpolation/Hensel/useful-factor proof skeleton with symbolic degree
parameters retained until the final integer certificate.

The PR headline does not depend on this note. The headline safe edge uses only
BCHKS25 Theorem 4.6 as displayed.

## Source dependency

This proposed bridge lemma is a parameter-retained extraction from the following
source, not an independent proof from first principles:

```text
Ben-Sasson, Carmon, Habock, Kopparty, Saraf,
On Proximity Gaps for Reed-Solomon Codes.
PDF: https://www.math.toronto.edu/swastik/rs-proximity-gaps-2025.pdf
DOI: https://dl.acm.org/doi/10.1145/3798129.3800827
PDF date: 2025-11-11
Accessed: 2026-07-04
PDF SHA256: 4ADDED3E55B83C15FCC8A698FB57E137F5BD83E79EA25CE79382817C1AD26A46
```

The exact imported ingredients are:

1. Theorem 4.6, "List correlated agreement, up to Johnson bound", pp. 27-28,
   for the support-wise list-MCA predicate and the `M=1` specialization.
2. Section 3.2, "Improved bound on a in terms of D_X, D_Y, D_Z", especially
   the unnumbered Step 4 Hensel/useful-factor statement on pp. 23-25: for a
   separable pair `(R,H)`, if

```text
|S_{x0,R,H}| > 2 D_X D_Y^(R) D_Y^(H) D_Z^(R),
```

then there is a polynomial `P(X,Z)=v0(X)+Z v1(X)` with `deg_X P <= k`,
`deg_Z P <= 1`, and a subset `S'` of size at least

```text
|S'| >= |S_{x0,R,H}| - D_Y^(R) D_Y^(H) D_Z^(R)
```

such that `P(X,z)=P_z(X)` for all `z in S'`.
3. The paragraph immediately after Theorem 4.6 on p. 28, which says the proof
   generalizes Section 3.2 by looking at all useful factors rather than a
   single factor for list correlated agreement.

Thus the appendix status is
`CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1`: reviewers must verify that the
symbolic extraction below preserves the constants of these source steps.

## Notation

Let `F` be a field, `D subset F` have size `n`, and

```text
C = RS_{<=k}[F,D]
```

be the Reed-Solomon code of evaluations of polynomials of degree at most `k`.
Thus the code dimension is `k+1`. For the deployed KoalaBear row, the repo uses
polynomials of degree `< K` with `K=2^20`, so the BCHKS degree parameter is
`k=K-1=2^20-1`.

Fix words `u0,u1 : D -> F`, an integer radius `r`, and `A=n-r`. Define the
support-wise list-MCA exceptional set `E_r(u0,u1)` to be the set of all
`z in F` for which there are a set `Az subset D` and a polynomial `pz in C`
such that

```text
|Az| >= A,
u0(x) + z u1(x) = pz(x) for all x in Az,
```

but there are no `p0,p1 in C` with

```text
u0(x)=p0(x) and u1(x)=p1(x) for all x in Az.
```

This is the `M=1` support-wise predicate in BCHKS25 Theorem 4.6.

Use Hasse derivatives throughout. This avoids characteristic restrictions in
multiplicity statements.

## Theorem

Let `m >= 1` be an integer and let `D_X,D_Y,D_Z` be positive rational numbers.
Put

```text
U = ceil(D_X),  V = ceil(D_Y),  W = ceil(D_Z).
```

Assume:

```text
V >= m,
W >= V,
U > k(V-1),
```

and the interpolation inequality

```text
sum_{j=0}^{V-1} (U-kj)(W-j)
  > n * sum_{s=0}^{m-1} (W-s)(m-s).        (I)
```

Assume also the root/agreement inequality

```text
D_X < mA.                                        (R)
```

Then for all `u0,u1 : D -> F`,

```text
|E_r(u0,u1)| <= 2 D_X D_Y^2 D_Z + (r+1)D_Y.      (B)
```

Consequently, since the left side is an integer, it is enough for a soundness
certificate to check

```text
ceil(2 D_X D_Y^2 D_Z + (r+1)D_Y) < budget.
```

## Proof

### 1. Interpolation inequality

Consider polynomials

```text
Q(X,Y,Z) = sum q_{i,j,h} X^i Y^j Z^h
```

with monomial support

```text
i + k j < D_X,
j < D_Y,
j + h < D_Z.
```

For a fixed `j`, the number of admissible `i` is `U-kj`, and the number of
admissible `h` is `W-j`. Therefore the number of variables is exactly

```text
N_vars = sum_{j=0}^{V-1} (U-kj)(W-j).
```

For each `x in D`, impose multiplicity `m` at the graph of

```text
u(x,Z) = u0(x) + Z u1(x)
```

by requiring

```text
Q^{[a,b]}(x, u(x,Z), Z) = 0
```

as a polynomial in `Z` for all Hasse partials with `a,b >= 0` and `a+b < m`.
For fixed `b=s`, after substitution the `Z`-degree is `< D_Z-s`, hence there
are `W-s` scalar linear equations. There are `m-s` choices of `a` with
`a+s<m`. Thus the number of homogeneous linear equations is

```text
N_eqs = n * sum_{s=0}^{m-1} (W-s)(m-s).
```

By `(I)`, `N_vars > N_eqs`, so a nonzero interpolant `Q` with the stated degree
bounds exists.

### 2. Root/agreement condition

Fix `z in E_r(u0,u1)` and one bad witness `(Az,pz)`. Define

```text
G_z(X) = Q(X, pz(X), z).
```

Every monomial `X^i Y^j Z^h` contributes `X`-degree at most `i+k j`, hence

```text
deg_X G_z < D_X.
```

For every `x in Az`, the equality `pz(x)=u0(x)+z u1(x)` and the multiplicity
conditions on `Q` imply that `G_z` has a root of multiplicity at least `m` at
`x`. This follows directly from the Hasse-chain expansion after substituting
`Y=pz(X)` and `Z=z`.

Therefore `G_z` has at least `m|Az| >= mA` roots counted with multiplicity.
By `(R)`, this is more than its degree, so

```text
Q(X, pz(X), z) == 0.                            (1)
```

This converts every exceptional slope into a polynomial root witness.

### 3. Separability and multiplicity normalization

Factor `Q` over an algebraic closure after removing the content in `Y`:

```text
Q(X,Y,Z) = C(X,Z) * product_i R_i(X,Y,Z)^{e_i}.
```

Only distinct slope witnesses are counted. Multiplicities `e_i` can therefore
be discarded. In positive characteristic, if an irreducible factor is
inseparable in `Y`, write it as a polynomial in `Y^{p^t}` and replace it by its
separable `p^t`-root factor. This cannot increase any of the relevant degree
sums and does not create new distinct witnesses. Thus it suffices to count the
separable, squarefree, content-free factors `R_i`.

Choose a starting point `x0` outside the finite exceptional set where leading
coefficients or discriminants vanish. Equivalently, work over a harmless finite
extension if needed; this does not change the set of base-field slopes being
counted. Decompose

```text
R_i(x0,Y,Z) = C_i(Z) * product_j H_{i,j}(Y,Z),
```

where the `H_{i,j}` are irreducible, nonconstant in `Y`, and separable in `Y`.
Let

```text
a_i     = deg_Y R_i,
b_{i,j} = deg_Y H_{i,j},
c_i     = weighted deg_{Y,Z} of the content-free part of R_i(x0,Y,Z),
d_C     = deg_Z(C(X,Z) * product_i C_i(Z)).
```

The bad slopes for which the content vanishes are paid for by `d_C`. Every
other slope satisfying `(1)` is assigned to at least one pair `(i,j)` with

```text
R_i(X,pz(X),z) == 0,
H_{i,j}(pz(x0),z) = 0.
```

Denote the assigned set by `S_{i,j}`.

The degree sums obey

```text
sum_j b_{i,j} = a_i,
sum_i a_i <= D_Y,
c_i <= D_Z - d_C.
```

The last inequality is the content-free `D_Z` bookkeeping: the `Z`-degree paid
by `C` and the `C_i` has been separated as `d_C`; the remaining weighted
`(Y,Z)` degree is available to the `R_i`.

### 4. Hensel lift and useful factors

Use the BCHKS25 Section 3.2 Step 4 Hensel/useful-factor sublemma in the
following symbolic form.
For a fixed separable pair `(R_i,H_{i,j})`, if

```text
|S_{i,j}| > 2 D_X a_i b_{i,j} c_i,
```

then there is a polynomial

```text
P(X,Z) = v0(X) + Z v1(X),  deg v0,deg v1 <= k,
```

and a subset `T_{i,j} subset S_{i,j}` with

```text
|T_{i,j}| >= |S_{i,j}| - a_i b_{i,j} c_i
```

such that

```text
pz(X) = P(X,z) for all z in T_{i,j}.
```

This is precisely the unnumbered Step 4 Hensel statement in BCHKS25 Section 3.2
with `D_X,a_i,b_{i,j},c_i` kept symbolic. The factor `2D_X` is the
approximate-to-exact threshold printed there; the subtraction `a_i b_{i,j} c_i`
is the exceptional specialization count printed there. Separability of
`H_{i,j}` is exactly what gives a unique local branch; inseparable
multiplicities were removed in the normalization step, following the same
Section 3.2 discussion and its pointer to the BCI+20 Appendix C treatment.

Now suppose, toward contradiction, that for some pair

```text
|S_{i,j}| > 2 D_X a_i b_{i,j} c_i + r + 1.       (2)
```

The Hensel sublemma gives a set `T_{i,j}` of more than `r+1` slopes lying on the
same line-valued polynomial `P(X,Z)=v0(X)+Zv1(X)`. The usual collinearity lemma
then gives

```text
|{x in D : (u0(x),u1(x)) != (v0(x),v1(x))}| <= r.       (3)
```

Here is the exact count. Let `T=T_{i,j}` and let

```text
B = {x in D : (u0(x),u1(x)) != (v0(x),v1(x))}.
```

For a fixed `x in B`, the equation

```text
u0(x)+z u1(x) = v0(x)+z v1(x)
```

has at most one solution `z`. Hence, among the `|T|` selected slopes, this
coordinate is missing from at least `|T|-1` of the agreement sets. Since each
selected slope has at most `r` missing coordinates,

```text
|B|(|T|-1) <= |T|r.
```

If `|T|>r+1`, then `|B| < r+1`; as `|B|` is an integer, `|B| <= r`.

For a list-MCA exceptional `z in T_{i,j}`, the chosen bad set `Az` cannot be
fully contained in the good set from `(3)`. Hence it contains a coordinate
`x` where `(u0,u1)!=(v0,v1)`, but

```text
u0(x)+z u1(x) = v0(x)+z v1(x).
```

For a fixed bad coordinate `x`, this linear equation has at most one solution
`z`. By `(3)`, there are at most `r` such slopes, contradicting the fact that
`T_{i,j}` has more than `r+1` slopes. Therefore `(2)` is impossible, and every
pair satisfies

```text
|S_{i,j}| <= 2 D_X a_i b_{i,j} c_i + r + 1.      (4)
```

This is the useful-factor/non-useful-factor split: non-useful pairs are bounded
by the Hensel threshold, and useful pairs have all but at most `r+1` of their
slopes explained by a common list branch.

### 5. Derivation of the final `R` bound

Sum `(4)` over all factor pairs and add the content roots:

```text
|E_r(u0,u1)|
  <= d_C + sum_i sum_j (2 D_X a_i b_{i,j} c_i + r + 1).
```

The number of pairs is at most `sum_i a_i <= D_Y`, so the additive term is at
most `(r+1)D_Y`. For the Hensel threshold term,

```text
sum_i sum_j a_i b_{i,j} c_i
  = sum_i a_i c_i * sum_j b_{i,j}
  = sum_i a_i^2 c_i
  <= D_Y * (D_Z-d_C) * sum_i a_i
  <= D_Y^2 (D_Z-d_C).
```

Thus

```text
|E_r(u0,u1)|
  <= d_C + 2 D_X D_Y^2 (D_Z-d_C) + (r+1)D_Y
  <= 2 D_X D_Y^2 D_Z + (r+1)D_Y,
```

where the last inequality uses `2D_XD_Y^2 >= 1`, which is automatic in the
KoalaBear certificate and in any nontrivial budget-clearing application.

This proves `(B)`.

## KoalaBear instantiation checked by the verifier

The verifier instantiates the theorem with

```text
n = 2^21
k = 2^20 - 1
r = 611983
A = 1485169
m = 119
epsilon = 2^-64
D_X = 176735110 + epsilon
D_Y = 168 + epsilon
D_Z = 27542 + epsilon
```

The exact checks are:

```text
ceil(D_X) = 176735111
ceil(D_Y) = 169
ceil(D_Z) = 27543
m*A - D_X = 1 - 2^-64 > 0

N_vars = 411830702773581
N_eqs  = 411830698639360
N_vars - N_eqs = 4134221

ceil(2D_XD_Y^2D_Z + (r+1)D_Y)
  = 274768452484563073
budget
  = 274980728111395087
margin
  = 212275626832014
```

The same verifier exhausts the optimized integer-ceiling family for `r=611984`
under the theorem admissibility constraints and finds no budget-clearing cell.
