---
status: PROVED COMPLEMENT-LOCATOR LINEARIZATION / EXACT FINITE CENSUS / GROWING-DIMENSIONAL INCIDENCE OPEN / ZERO LEDGER MOVEMENT
architecture_id: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1
direct_statement: At the first open full-outside KoalaBear slack, the two source quotient-interpolation tests are exactly equivalent to requiring the complementary split locator to lie in one two-dimensional residue subspace modulo the source locator.
---

# KoalaBear first-gap complement-locator linearization

## Status

This packet proves the next algebraic reduction after the first-gap source
interpolation pencil. It does not pay determinant mass or move the KoalaBear
ledger.

The proved reduction is:

```text
two nonlinear quotient-interpolation tests
    =
one two-dimensional complement-locator residue condition.
```

The remaining theorem is a growing-dimensional, worst-case split-locator
incidence bound with the actual determinant weights and same-selector source
semantics.

## 1. First-gap setup

Work at the lower open full-histogram endpoint

\[
r=67{,}471,\qquad x_L=1.
\]

The predecessor packet proves

\[
e=t=67{,}472,\qquad
s=|\Sigma|=2e=134{,}944,
\]

\[
j=981{,}104,\qquad
V=D\setminus\Sigma,\qquad |V|=2j=1{,}962{,}208.
\]

For a dangerous graph line, its full monic gcd is

\[
H_L=L_{Z_L},
\qquad
Z_L\subseteq V,
\qquad
|Z_L|=j-1.
\]

There is no additional outside-source common locator at this endpoint. Put

\[
Y_L=V\setminus Z_L,
\qquad |Y_L|=j+1,
\]

and write \(L_V=L_{Z_L}L_{Y_L}\).

Let

\[
A_\Sigma=F[X]/(L_\Sigma),
\qquad
L_\Sigma(X)=\prod_{h\in\Sigma}(X-h).
\]

Every locator supported in \(V\) is a unit in \(A_\Sigma\).

## 2. Source multiplier line

Let \((\epsilon _0,\epsilon _1)\) be the fixed translated source pair. The
first-gap source-pencil theorem gives the two-dimensional space

\[
\mathcal K_\Sigma(e)=
\left\{
(R,S)\in F[X]_{\le e}^2:
\epsilon _1(h)R(h)-\epsilon _0(h)S(h)=0
\quad(h\in\Sigma)
\right\}
\]

and proves

\[
\dim_F\mathcal K_\Sigma(e)=2.
\]

In \(A_\Sigma\), define

\[
u_0=L_V^{-1}\epsilon _0,
\qquad
u_1=L_V^{-1}\epsilon _1,
\]

and the linear multiplier map

\[
M_\Sigma:A_\Sigma\longrightarrow A_\Sigma^2,
\qquad
q\longmapsto(qu_0,qu_1).
\tag{2.1}
\]

At every source point at least one of
\(\epsilon _0,\epsilon _1\) is nonzero. Since \(L_V\) is nonzero there,
at least one of \(u_0,u_1\) is nonzero at every source point. The quotient
algebra \(A_\Sigma\) is the product of the source-point fields, so (2.1) is
injective.

Embed \(\mathcal K_\Sigma(e)\) into \(A_\Sigma^2\) by reduction modulo
\(L_\Sigma\), and define

\[
W_\Sigma=M_\Sigma^{-1}(\mathcal K_\Sigma(e)).
\tag{2.2}
\]

Every actual line supplies one element of the preimage. Injectivity and the
two-dimensional source-pencil theorem give the upper bound two. For the
reverse inclusion, every pair in \(\mathcal K_\Sigma(e)\) is pointwise
projectively proportional to \((\epsilon _0,\epsilon _1)\). That source pair
is nonzero at every point of \(\Sigma\), so in the product algebra
\(A_\Sigma\simeq\prod_{h\in\Sigma}F\) there is a unique multiplier \(q\)
with

\[
(R,S)=q(u_0,u_1).
\]

Thus \(\mathcal K_\Sigma(e)\subseteq\operatorname{im}M_\Sigma\), and the
restriction of \(M_\Sigma\) is an isomorphism

\[
W_\Sigma\xrightarrow{\sim}\mathcal K_\Sigma(e).
\]

The two-dimensional source-pencil theorem therefore gives

\[
\boxed{\dim_F W_\Sigma=2.}
\tag{2.3}
\]

## 3. Complement-locator linearization

### Theorem 3.1

For \(Z\subseteq V\), \(|Z|=j-1\), put \(Y=V\setminus Z\). Then

\[
\boxed{L_Z^{-1}=L_YL_V^{-1}\quad\text{in }A_\Sigma.}
\tag{3.1}
\]

Moreover, the two quotient vectors

\[
\left(\frac{\epsilon _0(h)}{L_Z(h)}\right)_{h\in\Sigma},
\qquad
\left(\frac{\epsilon _1(h)}{L_Z(h)}\right)_{h\in\Sigma}
\tag{3.2}
\]

both interpolate to degree at most \(e\) if and only if

\[
\boxed{Z\text{ is admissible}\iff[L_Y]\in W_\Sigma.}
\tag{3.3}
\]

Here \([L_Y]\) denotes the residue class modulo \(L_\Sigma\).

#### Proof

The polynomial identity

\[
L_ZL_Y=L_V
\]

holds because \(Z\) and \(Y\) partition \(V\). All three factors are units
modulo \(L_\Sigma\), proving (3.1).

Multiplying (3.1) by the two source coordinates gives

\[
L_Z^{-1}(\epsilon _0,\epsilon _1)
=L_Y(L_V^{-1}\epsilon _0,L_V^{-1}\epsilon _1)
=M_\Sigma([L_Y]).
\tag{3.4}
\]

The left side of (3.4) is exactly the pair of quotient vectors in (3.2).
Those vectors have degree-at-most-\(e\) representatives satisfying the source
projective equations precisely when they belong to
\(\mathcal K_\Sigma(e)\). Definition (2.2) now proves (3.3).
\(\square\)

This theorem is selector-faithful. It uses the actual carrier \(V\), actual
source pair, and actual split locator from one rebuilt selector. It does not
transport a common-zero set or source pencil between selectors.

## 4. The exact polynomial cylinder

Let

\[
m=|Y|=j+1.
\]

The inverse image of \(W_\Sigma\) under

\[
F[X]_{\le m}\longrightarrow A_\Sigma
\]

is a linear polynomial space

\[
\widetilde W_\Sigma
=\{P\in F[X]_{\le m}:[P]\in W_\Sigma\}.
\tag{4.1}
\]

Because \(m\ge s\), the kernel consists of

\[
L_\Sigma F[X]_{\le m-s}
\]

and has dimension \(m-s+1\). Hence

\[
\dim_F\widetilde W_\Sigma
=(m-s+1)+2
=j-2e+4.
\tag{4.2}
\]

Its projective dimension is

\[
\boxed{d=j+3-2e=846{,}163.}
\tag{4.3}
\]

Since \(L_\Sigma\in\widetilde W_\Sigma\) and
\(L_\Sigma(x)\ne0\) for every \(x\in V\), this space has no common root on
\(V\). The fixed-dimensional Conjecture-F incidence theorem therefore gives
the formally valid bound

\[
\#\{Y\in\tbinom V{j+1}:L_Y\in\widetilde W_\Sigma\}
\le
\binom{2j}{d}.
\tag{4.4}
\]

At the deployed dimensions (4.4) is not budget-fitting. The reduction has
identified the open object, but the existing fixed-dimensional estimate does
not close it.

## 5. Exact collision separation

The residue formulation also supplies two packing guards.

Suppose \(Y,Y'\subseteq V\) have size \(m\), and put

\[
c=|Y\cap Y'|,
\qquad
\Delta=m-c.
\]

If

\[
L_Y\equiv L_{Y'}\pmod{L_\Sigma},
\]

then after factoring the common locator, the difference of two monic
degree-\(\Delta\) locators has degree at most \(\Delta-1\) and is divisible
by \(L_\Sigma\). Distinct locators consequently satisfy

\[
\boxed{\Delta\ge s+1=2e+1.}
\tag{5.1}
\]

More generally, if

\[
L_Y\equiv c_0L_{Y'}\pmod{L_\Sigma}
\qquad(c_0\ne0),
\]

then the reduced difference has degree at most \(\Delta\), giving

\[
\boxed{\Delta\ge s=2e.}
\tag{5.2}
\]

Thus exact residue fibers and projective residue fibers are constant-weight
codes with the printed Johnson-distance floors. These floors are exact
guards, not a deployed determinant-mass bound.

## 6. Finite exact census

The verifier exhausts all split-locator complements in three prime-field
rows. For every tested source it checks:

1. the original two quotient-interpolation predicates;
2. the single linear residue-line predicate;
3. equality of the two candidate sets;
4. dimension two of \(W_\Sigma\);
5. the exact and projective exchange floors.

The `F17_E2_J6` row additionally enumerates every projective line spanned by
occupied complement-locator residues. It records:

```text
split-locator complements                         792
occupied projective residue points                775
projective residue lines checked               69,179
unrestricted maximum line occupancy                14
coprime exact-degree source-realizable maximum      12
```

The verifier checks residue lines in descending occupancy. The unique
occupancy-`14` line and all nine occupancy-`13` lines fail the coprime
exact-degree source-realization test. The first realizable occupancy-`12`
line has the explicit reduced pair

\[
R=X^2+14X,\qquad S=1
\quad\text{over }\mathbf F_{17}.
\]

The other two rows exhaust their locator domains but sample source pairs with
a deterministic seed; those sampled source maxima are diagnostic and are
labelled as such in the certificate.

The emitted certificate contains the resulting counts. They are finite
evidence only. They do not imply a growing-dimensional worst-case estimate.

## 7. Residue-line realization guardrail

The two-dimensional residue line is not automatically a narrow
source-specific subclass of all residue lines.

Fix a nonzero occupied residue \(q_0=[L_{Y_0}]\) and another vector \(q_1\)
spanning a target residue line \(W\). In the source-point algebra put

\[
u=q_1/q_0
\]

and define

\[
\mathcal V_u=
\{R\in F[X]_{\le e}:uR\text{ has a degree-at-most-}e
\text{ representative modulo }L_\Sigma\}.
\tag{7.1}
\]

The map from the \((e+1)\)-dimensional space \(F[X]_{\le e}\) to the
\((e-1)\) forbidden high coefficients has kernel \(\mathcal V_u\).
Therefore

\[
\dim\mathcal V_u\ge2.
\tag{7.2}
\]

If \(\mathcal V_u\) contains a coprime pair \((R,S)\) of exact maximum degree
\(e\), define source values by

\[
(\epsilon _0,\epsilon _1)
=L_{Z_0}(R,S)\quad\text{on }\Sigma.
\tag{7.3}
\]

The multiplier space then contains \(\operatorname{span}\{1,u\}\). The
first-gap dimension theorem says it has dimension exactly two, so the
complement-locator residue line produced by (7.3) is exactly \(W\).

Thus an arbitrary occupied residue line is source-realizable whenever the
kernel (7.1) has a coprime exact-degree pair. Failure of that condition is a
common-divisor or degree-defect branch that must be routed semantically; it is
not generic source flatness.

More precisely, the following admission dichotomy is exact:

1. if \(\dim\mathcal V_u>2\), the line has a multiplier-admission rank-excess
   precursor;
2. if \(\dim\mathcal V_u=2\) and every element has degree at most \(e-1\),
   the line has a degree defect;
3. if \(\dim\mathcal V_u=2\), has an exact-degree element, and the gcd of a
   basis is nonconstant, every possible source pair has that common divisor
   and reduces below degree \(e\);
4. otherwise a basis is a coprime exact-degree pair and realizes \(W\).

The gcd in item 3 is basis-independent. In the two-dimensional case, a
constant gcd and one exact-degree element make any basis a coprime
exact-degree realization after replacing its second vector if necessary.
The source-pencil dimension theorem then prevents a larger multiplier line.

Items 2 and 3 reduce the rational-map degree to at most \(e-1\). A
nonconstant reduced map is inside the exact threshold owned by the
pair-global source-rational cell. A constant reduced map has its sole finite
slope in the earlier source-coordinate tangent image. Item 1 is a rank
precursor, not automatically a paid rank cell; it still needs the same-owner
collective-rank projection required by the active atlas.

The exhaustive `F17_E2_J6` census finds universal maximum residue-line
occupancy `14`. For every one of its 14 occupied choices of \(q_0\), the
space \(\mathcal V_u\) has dimension two and a common linear divisor. For
example, one base gives

\[
\mathcal V_u
=\operatorname{span}\{X+4,X^2+1\}
=(X+4)\operatorname{span}\{1,X+13\}.
\]

Thus the maximum line reduces to degree one after cancelling the common
factor and belongs to the source-rational type already removed before the
first-gap residual. All nine occupancy-`13` lines also fail through a common
divisor or degree defect. The first coprime exact-degree line has occupancy
`12`.

This gives both a route cut and positive evidence:

```text
arbitrary residue-line maximum = 14 is not an active source line;
coprime exact-degree source-line maximum = 12 in the exact F17 row.
```

The finite separation suggests the right inverse statement: an unusually
large residue-line occupancy either forces a common divisor or degree defect,
or lies in the genuinely coprime exact-degree branch that must be bounded
using regular split-locator geometry, outlier determinant weights, and
complete-selector constraints. It does not prove the corresponding
growing-dimensional statement.

## 8. Remaining target

The first open source-bound bridge problem is now the following.

> **First-gap growing-dimensional residue-cylinder incidence.** For the
> actual six-owner residual, one rebuilt complete selector, and its
> admitted coprime exact-degree two-dimensional source residue line
> \(W_\Sigma\), after routing multiplier rank excess, degree defects, and
> common divisors, bound the
> determinant-weighted rich-line contribution from
>
> \[
> \{Y\in\tbinom V{j+1}:[L_Y]\in W_\Sigma\}
> \]
>
> by the active reserve, or emit a same-slope quotient, planted,
> proper-field, collective-rank, saturation, common-twist, or
> Frobenius-9208 owner.

The proof must use more than the dimension of the cylinder. The likely
load-bearing inputs are:

* the eight actual outlier directions defining \(\beta_L\);
* the regular split-locator equations;
* complete-selector coverage;
* first-match exclusion of quotient, base-field, twist, and Frobenius
  degeneracies;
* a worst-case, growing-dimensional flatness or inverse theorem for the
  remaining aperiodic residue cylinder.

The exact linearization makes this a standard source-bound split-locator
incidence problem rather than two unrelated interpolation tests.

## 9. Scope and nonclaims

This packet does not:

* bound \(\sum_L\beta_L(J_L-20)\);
* prove complete-selector existence or coverage;
* turn the fixed-dimensional binomial estimate into a usable row bound;
* classify the maximizing residue cylinder;
* pay a slope or move the ledger;
* treat later open slacks, Q, balanced core, or the final complement;
* close KoalaBear.

# PROVED
