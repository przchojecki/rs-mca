# Exact Star-Conic Geometry in the Reduced \(Q=6,u=2\) Branch

## 1. Status

This note sharpens the reduced conic-image endpoint in:

```text
proof/q6_u2_line_conic_quotient_reduction.md
proof/q6_u2_conic_free_pair_involution_reduction.md
```

The five common signatures were previously known to have one of
three graph types:

\[
P_6,\qquad P_3\sqcup C_3,\qquad P_2\sqcup C_4.
\]

The exact six-line star geometry proves that all \(60\) labeled
\(P_3\sqcup C_3\) common-signature graphs in this reduced,
source-derived \(Q=6,u=2\) conic universe are impossible. It also
supplies closed discriminant and endpoint-intersection formulas for
the other two types. This is not a classification of arbitrary
six-line configurations. No owner payment is booked.

## 2. Six-line coordinates

For six distinct noninvariant source labels \(\alpha_0,\ldots,\alpha_5\),
the source lines in the coefficient plane are

\[
\mathscr L_i:
A\alpha_i^2+B\alpha_i+C=0.
\]

Their star vertex is

\[
v_{ij}:=\mathscr L_i\cap\mathscr L_j
=
\bigl[1,-(\alpha_i+\alpha_j),\alpha_i\alpha_j\bigr],
\tag{2.1}
\]

the coefficient point of
\((T-\alpha_i)(T-\alpha_j)\).

Five distinct star vertices impose five linear equations on the six
coefficients of a plane conic. In the reduced conic branch these
equations have rank five, so the candidate conic is unique.

The identities below are projectively invariant. They can be checked
on the universal affine chart

\[
(\alpha_0,\ldots,\alpha_5)=(0,1,-1,x,y,z).
\tag{2.2}
\]

The calculation takes the signed \(5\times5\) maximal minors of the
matrix whose row at \([A:B:C]\) is

\[
(A^2,AB,AC,B^2,BC,C^2).
\tag{2.3}
\]

After removing the nonzero common factor from each cofactor vector,
the following discriminants result.

Because the resulting identities are polynomial after clearing the
displayed coordinate factors, the universal-chart calculation
specializes to every six-tangent configuration over the KoalaBear
field. Its characteristic is odd and none of the numerical constants
below vanish.

## 3. Exact conic discriminants

Use the canonical edge representatives

\[
\begin{aligned}
P_6:\quad&
01,12,23,34,45,\\
P_3\sqcup C_3:\quad&
01,12,34,45,35,\\
P_2\sqcup C_4:\quad&
01,23,34,45,25.
\end{aligned}
\tag{3.1}
\]

If a conic is written as

\[
q_{00}A^2+q_{01}AB+q_{02}AC
+q_{11}B^2+q_{12}BC+q_{22}C^2,
\]

its degeneracy is detected by

\[
\det
\begin{pmatrix}
2q_{00}&q_{01}&q_{02}\\
q_{01}&2q_{11}&q_{12}\\
q_{02}&q_{12}&2q_{22}
\end{pmatrix}.
\tag{3.2}
\]

The exact factorizations are as follows.

For \(P_3\sqcup C_3\),

\[
\begin{aligned}
\Delta_{3+3}={}&
-2xyz(x-1)(x+1)(y-1)(y+1)(z-1)(z+1).
\end{aligned}
\tag{3.3}
\]

Every factor in (3.3) is nonzero for six distinct labels in the
normalization (2.2). Thus its candidate conic is always nonsingular.

Put

\[
\mathfrak f=xyz+xy+xz-x-2yz
\tag{3.4}
\]

and

\[
\mathfrak g=xyz-2xy+xz+yz-z.
\tag{3.5}
\]

For \(P_6\),

\[
\begin{aligned}
\Delta_{6}={}&
4xy(x-1)^2(x+1)(x-y)\\
&\cdot(y-1)(y+1)^2(z-1)(z+1)\mathfrak f.
\end{aligned}
\tag{3.6}
\]

For \(P_2\sqcup C_4\),

\[
\begin{aligned}
\Delta_{2+4}={}&
-4xyz(x-1)(x+1)(x-y)\\
&\cdot(y-1)(y-z)(z-1)(z+1)
\mathfrak f\mathfrak g.
\end{aligned}
\tag{3.7}
\]

Consequently the only noncollision degeneracy gates are
\(\mathfrak f=0\) for \(P_6\), and
\(\mathfrak f\mathfrak g=0\) for \(P_2\sqcup C_4\).
An irreducible-conic packet must avoid them.

## 4. Endpoint second intersections

Parameterize \(\mathscr L_a\) by its second source root:

\[
\ell_a(t)=
\bigl[1,-(a+t),at\bigr].
\tag{4.1}
\]

Restrict the candidate conic to \(\ell_a(t)\). One root is the
neighbor of \(a\) in the common-signature graph. Dividing by that
known linear factor gives the other intersection exactly.

For \(P_3\sqcup C_3\), the path endpoints are \(0\) and \(2\), both
adjacent to \(1\). The two calculations give

\[
\boxed{
\beta_0=-1=\alpha_2,\qquad
\beta_2=0=\alpha_0.}
\tag{4.2}
\]

Thus both endpoint lines have the same second conic intersection:

\[
\ell_0(\beta_0)
=
\ell_{-1}(\beta_2)
=
v_{02}
=[1,0,0].
\tag{4.3}
\]

Equivalently, the six vertices of the two complementary tangent-line
triangles

\[
\{v_{01},v_{12},v_{02}\}
\quad\text{and}\quad
\{v_{34},v_{45},v_{35}\}
\]

lie on the same nonsingular conic.

For later elimination, the same division gives the two surviving
endpoint pairs. In the \(P_6\) case,

\[
\beta_0=
-\frac{xyz+xy+2xz-yz+y}
{xz-x-2yz-z-1},
\tag{4.4}
\]

\[
\beta_5=
\frac{x(xy+xz-2yz+y-z)}
{x^2y-x^2z+xy+xz-2yz}.
\tag{4.5}
\]

In the \(P_2\sqcup C_4\) case,

\[
\beta_0=
\frac{xyz+xy-2xz+yz-y}
{xz-x+2y-z-1},
\tag{4.6}
\]

\[
\beta_1=
\frac{xyz+xy-xz+yz}
{xz+y}.
\tag{4.7}
\]

These are projective formulas: a zero denominator records the point
at infinity on the corresponding source line.

There is one additional noncollision gate in the \(P_6\) case. The
unselected vertex \(v_{05}\) lies on the candidate conic precisely
when

\[
\boxed{
xy+xz-2yz+y-z=0.}
\tag{4.8}
\]

That equality would create a sixth common signature, so an actual
reduced \(P_6\) packet must avoid it.

## 5. The \(P_3\sqcup C_3\) contradiction

### 5.1 Inherited divisor facts

This argument imports four facts from the preceding reduction. Their
exact provenance and notation translation are:

| Parent theorem | Hypotheses transferred | Conclusion used here | Variable translation |
| --- | --- | --- | --- |
| `q6_u2_plane_map_reduction.md`, (7.1)--(7.3) | actual irreducible bidegree-\((2,4)\) component with smooth conic coefficient image | \(\varphi_H=\nu\circ\chi\), with \(\deg\chi=2\) and \(\nu\) the conic normalization | the parent pole coordinate is the \(\lambda\) used below |
| `q6_u2_line_conic_quotient_reduction.md`, (2.1)--(2.2) | the reduced \(Q=6,u=2\) divisor ledger and pole-disjoint actual free edges | each endpoint free divisor is reduced, effective, and has degree two; the two endpoint free divisors are disjoint | the parent divisor \(bZ_j\) is denoted \(F_j\); the endpoint rows are \(j=0,2\) |
| `q6_u2_line_conic_quotient_reduction.md`, (4.1)--(4.4) and (5.1) | separable conic pullback and reduced common-pole branch | each endpoint free pair is one complete \(\chi\)-fiber and has one-label signature | the parent row divisor \(D_j\) contains the child free fiber \(F_j=bZ_j\) |
| Section 4 of this note, especially (4.3) | the exact six-line coefficient coordinates for the \(P_3\sqcup C_3\) graph | the second conic intersection of both endpoint source lines is \(v_{02}\) | the two endpoint lines are \(\mathscr L_0,\mathscr L_2\) |

The first three rows are inherited statements. The fourth is the new
star-coordinate calculation in this note. No other geometric or
owner assertion is imported.

In the reduced conic branch the coefficient map factors as

\[
\varphi_H=\nu\circ\chi,
\qquad
\deg\chi=2,
\]

where \(\nu\) is the conic normalization. The two degree-one vertices
of the common-signature graph are exactly the two endpoint rows.
Each endpoint row contributes its complete free divisor:

\[
F_0=bZ_0,\qquad F_2=bZ_2.
\]

The imported statements above prove:

1. \(F_0\) and \(F_2\) are reduced effective divisors of degree two;
2. they are disjoint by pole disjointness;
3. each is a complete fiber of \(\chi\);
4. its image under \(\nu\circ\chi\) is the second intersection of
   the corresponding source line with the conic.

By (4.3), both complete fibers map to \(v_{02}\). Since \(\nu\) is an
isomorphism onto the nonsingular conic, both are fibers of \(\chi\)
over the same normalization point. A degree-two morphism has a unique
degree-two scheme-theoretic fiber over a point. Therefore

\[
F_0=F_2,
\]

contradicting their disjointness.

Hence, within the reduced common-signature universe,

\[
\boxed{\text{all \(60\) labeled \(P_3\sqcup C_3\) graphs are
impossible}.}
\tag{5.1}
\]

The reduced common-signature list is now

\[
\boxed{P_6\quad\text{or}\quad P_2\sqcup C_4.}
\tag{5.2}
\]

## 6. Remaining target

The exact conic wall now consists only of the \(P_6\) and
\(P_2\sqcup C_4\) source-label configurations, subject to:

1. the nondegeneracy gates (3.6)--(3.7);
2. the two-free-divisor involution gate;
3. the common-decic invariance and fixed-root gates;
4. the reciprocal, \(D_4\), or \(D_5\) source-quotient profile;
5. the same-record elimination-or-owner adapter.

The focused form of this remaining problem is:

```text
target/q6_u2_two_signature_conic_elimination_target.md
```

The proof is replayed by:

```text
python verification/verify_q6_u2_star_conic_geometry.py --check
python verification/verify_q6_u2_star_conic_geometry.py --tamper-selftest
```
