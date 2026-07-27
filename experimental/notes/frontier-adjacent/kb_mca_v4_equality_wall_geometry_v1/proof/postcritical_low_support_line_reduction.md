# Postcritical Low-Support Line Reduction

## 1. Status

This note proves a low-support reduction for the selected-record
postcritical semantic-or-interpolation target.

It does not prove KoalaBear postcritical interpolation, cap \(68\), or a
same-record payment. It shows that every sufficiently sparse
postcritical relation contains an overloaded line, closes the canonical
block-line alternative at the hardest all-regular parameters, and gives
an exact one-parameter split-locator normal form for the remaining
noncanonical line.

## 2. Evaluation relations

Let

\[
X\subseteq\mathbf P^{a-1}(F)
\]

be any finite set of distinct points, and let

\[
\operatorname{ev}_k:
H^0(\mathbf P^{a-1},\mathcal O(k))
\longrightarrow F^X
\]

be degree-\(k\) evaluation. A relation is a nonzero vector

\[
\lambda=(\lambda_x)_{x\in X},
\qquad
\sum_{x\in X}\lambda_x f(x)=0
\]

for every degree-\(k\) form \(f\). Its support is

\[
S=\{x:\lambda_x\ne0\}.
\]

The KoalaBear postcritical degree is

\[
k=R-a+2.
\tag{2.1}
\]

## 3. Universal support floor

### Lemma 3.1

Every nonzero degree-\(k\) evaluation relation has

\[
\boxed{|S|\ge k+2.}
\tag{3.1}
\]

### Proof

Suppose \(|S|\le k+1\), and fix \(x\in S\). For each
\(y\in S\setminus\{x\}\), choose a hyperplane through \(y\) but not
through \(x\). Their product has degree \(|S|-1\le k\), vanishes on
\(S\setminus\{x\}\), and is nonzero at \(x\). Multiplying by a power of
one more linear form nonzero at \(x\) makes the degree exactly \(k\).
Pairing this separator with the relation gives \(\lambda_x=0\), contrary
to \(x\in S\). \(\square\)

### Lemma 3.2

If

\[
|S|=k+2,
\]

then all points of \(S\) are collinear.

### Proof

If \(S\) is not collinear, choose a noncollinear triple \(x,y,z\in S\).
There is a hyperplane through \(y,z\) but not \(x\). Cover each of the
remaining \(k-1\) points of \(S\setminus\{x,y,z\}\) by one hyperplane not
through \(x\). The product of these \(k\) hyperplanes separates \(x\)
from the rest of \(S\), again contradicting \(\lambda_x\ne0\).
\(\square\)

## 4. Low-support relations force an overloaded line

The previous argument extends from minimum support to the full interval
through \(2k+1\).

### Theorem 4.1

If a nonzero degree-\(k\) relation satisfies

\[
|S|\le2k+1,
\tag{4.1}
\]

then some line contains at least

\[
\boxed{k+2}
\tag{4.2}
\]

points of \(S\).

### Proof

Assume every line contains at most \(k+1\) points of \(S\). Fix
\(x\in S\), and partition \(S\setminus\{x\}\) according to the lines
through \(x\). Each part has size at most \(k\).

Write \(n=|S|-1\le2k\), and let \(g\) be the largest part size. The
vertices of this multipartite set can be covered by

\[
\max\{g,\lceil n/2\rceil\}\le k
\]

groups, each either a singleton or a pair from different parts. The
cover exists by greedily pairing vertices from the largest remaining
parts; if one part remains, its vertices are singletons.

For a paired group \(y,z\), the points \(x,y,z\) are not collinear, so
there is a hyperplane through \(y,z\) but not \(x\). For a singleton,
choose a hyperplane through it but not \(x\). The product of the at most
\(k\) hyperplanes separates \(x\) from \(S\setminus\{x\}\). Raise its
degree to \(k\) using a linear form nonzero at \(x\). Pairing with the
relation gives \(\lambda_x=0\), a contradiction. \(\square\)

This theorem is source-free but useful: it converts every low-support
postcritical failure into a single overloaded geometric line without
losing a selected record.

## 5. Canonical block lines

For a selected \(a\)-block \(B\), let \(L_B\) be the canonical line from
`reciprocal_cauchy_block_line_emission.md`. That note proves the exact
capacity

\[
m_{\rm can}(R,a)
=
a\left\lfloor\frac Ra\right\rfloor
+
\mathbf1_{\{R\bmod a=a-1\}}.
\tag{5.1}
\]

The additional indicator accounts for one near-full fiber of the pencil
\(\operatorname{span}\{P_B,A_\Sigma\}\). It is essential: small-field
configurations can have vertices on \(L_B\) that are not facets of a
full selected \(a\)-block.

At the surviving parameters,

\[
\begin{array}{c|c|c|c}
a&R&k+2&m_{\rm can}\\ \hline
12&69&61&60\\
14&67&57&56\\
14&68&58&56\\
14&69&59&57.
\end{array}
\tag{5.2}
\]

Therefore no canonical block line can carry the overloaded line from
Theorem 4.1 in these four cases.

In particular, at \(a=12,R=69\), every relation of support at most

\[
2k+1=119
\tag{5.3}
\]

forces at least 61 points on a genuinely noncanonical line.

## 6. Exact noncanonical-line locator normal form

Let \(\ell\subseteq\mathbf P^{a-1}\) be any line. Choose affine line
coordinates

\[
z_j(\lambda)=u_j+\lambda v_j
\qquad(1\le j\le a).
\tag{6.1}
\]

Suppose a reciprocal-Cauchy vertex on \(\ell\) corresponds to the monic
locator \(P_\lambda(T)\) of degree \(a-1\). Its projective coordinates
give

\[
P_\lambda(\alpha_j)
=
\frac{c(\lambda)}{u_j+\lambda v_j}.
\tag{6.2}
\]

Let \(L_j(T)\) be the source Lagrange basis:

\[
L_j(\alpha_i)=\mathbf1_{i=j}.
\]

Put

\[
\Delta(\lambda)
=
\prod_{j=1}^a(u_j+\lambda v_j)
\tag{6.3}
\]

and

\[
N(T,\lambda)
=
\sum_{j=1}^a
L_j(T)
\frac{\Delta(\lambda)}
{u_j+\lambda v_j}.
\tag{6.4}
\]

This is polynomial in \(\lambda\), with

\[
\deg_\lambda N\le a-1.
\tag{6.5}
\]

Let

\[
D(\lambda)=[T^{a-1}]N(T,\lambda).
\tag{6.6}
\]

At every actual reciprocal-Cauchy vertex on the line,
\(D(\lambda)\ne0\), and uniqueness of degree-\((a-1)\) interpolation
gives

\[
\boxed{
P_\lambda(T)=\frac{N(T,\lambda)}{D(\lambda)}.
}
\tag{6.7}
\]

For each selected parameter \(t\), define

\[
N_t(\lambda)=N(t,\lambda).
\tag{6.8}
\]

Then

\[
t\text{ is a root of }P_\lambda
\quad\Longleftrightarrow\quad
N_t(\lambda)=0.
\tag{6.9}
\]

Thus an overloaded line is an exact one-parameter family of split
degree-\((a-1)\) locators, controlled by \(R\) univariate root
polynomials of degree at most \(a-1\).

## 7. Rank-or-rational-normal dichotomy

Write

\[
\ell_j(\lambda)=u_j+\lambda v_j,
\qquad
g_j(\lambda)=\prod_{r\ne j}\ell_r(\lambda).
\]

Then

\[
N(T,\lambda)=\sum_{j=1}^aL_j(T)g_j(\lambda).
\tag{7.1}
\]

If two projective factors \([\ell_j]\) and \([\ell_r]\) coincide, the line
has the exact constant-coordinate-ratio identity

\[
\frac{z_j(\lambda)}{z_r(\lambda)}
=\text{constant}.
\tag{7.2}
\]

Equivalently, the coefficient span of the \(g_j\) has dimension less
than \(a\). This prints a collective rank/coordinate-ratio precursor.
Converting it to an active owner remains a semantic step.

Assume instead that the \(a\) projective linear factors are distinct.
Then the \(g_j\) form a basis of \(F[\lambda]_{\le a-1}\). Indeed,
evaluation at the root of \(\ell_i\) kills every \(g_j\) except \(g_i\).
Consequently, as \(t\) varies,

\[
t\longmapsto[N_t(\lambda)]
\tag{7.3}
\]

is a rational normal curve of degree \(a-1\) in
\(\mathbf P(F[\lambda]_{\le a-1})\): its coordinates in the \(g_j\)
basis are the source Lagrange coordinates

\[
[L_1(t):\cdots:L_a(t)].
\]

Thus every noncanonical overloaded line has the exact dichotomy

\[
\boxed{
\text{coordinate-ratio rank defect}
\quad\text{or}\quad
\text{degree-}(a-1)\text{ rational-normal near-split packet}.
}
\tag{7.4}
\]

### 7.1 Exact diagonal Cauchy kernel

The generic rational-normal branch has less freedom than an arbitrary
full-rank bidegree-\((a-1,a-1)\) form.

Put

\[
A_\Sigma(T)=\prod_{j=1}^a(T-\alpha_j).
\]

Then

\[
L_j(T)
=
\frac{A_\Sigma(T)}
{(T-\alpha_j)A_\Sigma'(\alpha_j)}.
\tag{7.5}
\]

After a projective change of the line parameter, all roots of the
distinct factors \(\ell_j\) may be placed in the affine chart. Write

\[
\ell_j(\lambda)=c_j(\lambda-\beta_j),
\qquad
c_j\ne0,
\qquad
\beta_j\ne\beta_r\ (j\ne r),
\]

and put

\[
B(\lambda)=\prod_{j=1}^a(\lambda-\beta_j).
\]

Substitution in (7.1) gives

\[
\boxed{
N(T,\lambda)
=
A_\Sigma(T)B(\lambda)
\sum_{j=1}^a
\frac{w_j}
{(T-\alpha_j)(\lambda-\beta_j)},
}
\tag{7.6}
\]

for explicit nonzero weights \(w_j\). The displayed expression is
polynomial because each denominator cancels its corresponding factor in
\(A_\Sigma B\).

At every selected \(t\) and every actual line parameter \(\lambda\), the
outer factors in (7.6) are nonzero. Therefore the incidence relation is
exactly

\[
\boxed{
N(t,\lambda)=0
\quad\Longleftrightarrow\quad
\sum_{j=1}^a
\frac{w_j}
{(t-\alpha_j)(\lambda-\beta_j)}
=0.
}
\tag{7.7}
\]

The two vectors

\[
x(t)=\left(\frac1{t-\alpha_j}\right)_{j=1}^a,
\qquad
y(\lambda)=\left(\frac1{\lambda-\beta_j}\right)_{j=1}^a
\]

parameterize two rational normal curves after projective rescaling.
Equation (7.7) is their orthogonality under the nondegenerate diagonal
form \(\operatorname{diag}(w_1,\ldots,w_a)\).

This also reproves the full coefficient rank without a determinant
calculation: the \(L_j\) and \(B/(\lambda-\beta_j)\) are bases and all
\(w_j\) are nonzero. Thus the generic target is an incidence theorem for
two rational normal curves under one nondegenerate diagonal pairing, not
an arbitrary bidegree form.

### 7.2 Higher-order intersection law

Let \(\lambda_1,\ldots,\lambda_d\) be distinct actual points on the
noncanonical line, with \(1\le d\le a\). The corresponding vectors
\(y(\lambda_s)\) are linearly independent because any \(a\) points on a
rational normal curve are independent. Their orthogonal hyperplanes
therefore meet in a projective subspace of dimension

\[
(a-1)-d.
\]

Any \(r\)-plane contains at most \(r+1\) distinct points of a rational
normal curve. Applying this to the source curve \(x(t)\) gives

\[
\boxed{
\left|
\bigcap_{s=1}^d I_{\lambda_s}
\right|
\le a-d.
}
\tag{7.8}
\]

For \(d=1\), equality is the degree-\((a-1)\) locator condition. For
\(d=2\), (7.8) gives \(a-2\); genuine noncanonicity improves this by one
to \(a-3\). For \(d\ge3\), (7.8) supplies higher-order information not
contained in the pairwise bound alone.

If equality holds in (7.8), the \(a-d\) common source-curve points span
the entire intersection subspace. Equivalently, the \(d\) locators have
a common split factor of degree \(a-d\), and their residual
degree-\((d-1)\) factors span the complete quotient section. This is the
exact equality template available to a planted or quotient adapter.

### 7.3 Two-anchor quotient identity

Choose two distinct actual line locators \(P_0,P_\infty\). Their
reciprocal evaluation vectors span the line. For every other locator
\(P_\lambda\), there are nonzero projective coefficients
\([r_\lambda:s_\lambda]\), a nonzero scalar \(c_\lambda\), and

\[
H_\lambda(T)
=
r_\lambda P_\infty(T)+s_\lambda P_0(T)
\tag{7.9}
\]

such that, at every source point,

\[
P_\lambda H_\lambda
=
c_\lambda P_0P_\infty.
\]

The difference has degree at most \(2a-2\) and vanishes on all \(a\)
source points. Therefore

\[
\boxed{
P_\lambda H_\lambda
-
c_\lambda P_0P_\infty
=
A_\Sigma Q_\lambda,
\qquad
\deg Q_\lambda\le a-2.
}
\tag{7.10}
\]

This is an exact polynomial identity, not only an equality of evaluation
vectors.

Every selected root shared by \(P_\lambda\) and \(P_0P_\infty\) is a
root of \(Q_\lambda\). Hence either

\[
\boxed{
|I_\lambda\cap(I_0\cup I_\infty)|\le a-2,
}
\tag{7.11}
\]

or \(Q_\lambda=0\). In the latter case,

\[
P_\lambda\mid P_0P_\infty,
\]

so the third locator is obtained by selecting its complete root set from
the two anchor root sets. This is an exact two-anchor split template.

If equality holds in (7.11), \(Q_\lambda\) is itself, up to scalar, the
locator of the shared roots. Thus the boundary case also prints a
degree-\((a-2)\) split quotient.

There is one more exact guard. If two vertex locators \(P_\lambda\) and
\(P_\mu\) on a noncanonical line shared \(a-2\) selected roots, their
root sets would be two facets of the same selected \(a\)-block. Their
line would then be that block's canonical line. Therefore

\[
\boxed{
\deg\gcd(P_\lambda,P_\mu)\le a-3
}
\tag{7.12}
\]

for distinct vertices on a genuinely noncanonical line.

## 8. Common-root or near-saturated incidence

If some \(N_t\) is identically zero, then every locator on the line has
the common selected root \(t\). This is an exact common-factor/quotient
precursor rooted in all selected records on the line.

Assume no \(N_t\) is identically zero. If the line contains \(m\)
selected reciprocal-Cauchy vertices, then each selected \(t\) occurs in
at most \(a-1\) of their locators. Counting root incidences gives

\[
m(a-1)\le R(a-1),
\qquad
m\le R.
\tag{8.1}
\]

At the minimum overloaded size

\[
m=k+2=R-a+4,
\tag{8.2}
\]

put

\[
n_t
=
\#\{\lambda:t\mid P_\lambda\},
\qquad
\delta_t=(a-1)-n_t.
\]

Then

\[
\boxed{
\sum_{t=1}^R\delta_t
=(R-m)(a-1)
=(a-4)(a-1).
}
\tag{8.3}
\]

Consequently at least

\[
\boxed{
R-\left\lfloor
\frac{(a-4)(a-1)}2
\right\rfloor
}
\tag{8.4}
\]

selected parameters occur in at least \(a-2\) of the line locators.

For the hardest case,

\[
a=12,\qquad R=69,\qquad m=61,
\]

equations (7.3)--(7.4) give

\[
\sum_t(11-n_t)=88
\tag{8.5}
\]

and

\[
\boxed{
\#\{t:n_t\ge10\}\ge25.
}
\tag{8.6}
\]

If the line contains more than 61 vertices, these bounds only strengthen.

Combining (7.4)--(8.6), the generic hardest-case packet consists of at
least 25 points on one degree-11 rational normal curve, each represented
by a degree-11 polynomial having at least 10 roots in the same 61-point
parameter set, while any two of the 61 locator supports intersect in at
most nine roots.

There is an equivalent coding-theoretic ledger. Evaluate the
degree-\(\le a-1\) polynomials \(N_t(\lambda)\) at the \(m\) actual line
parameters. They form a generalized Reed--Solomon code of length \(m\),
dimension \(a\), and minimum distance

\[
d_{\rm GRS}=m-a+1.
\]

The word indexed by \(t\) has weight

\[
\operatorname{wt}(N_t)=m-n_t
=d_{\rm GRS}+\delta_t.
\tag{8.7}
\]

At minimum overload, the total excess above minimum distance is exactly

\[
\boxed{
\sum_{t=1}^R
\bigl(\operatorname{wt}(N_t)-d_{\rm GRS}\bigr)
=(a-4)(a-1).
}
\tag{8.8}
\]

For \(a=12,R=69,m=61\), this is a \([61,12,50]\) GRS code containing 69
codewords on a second rational normal curve, with total weight excess
only \(88\). At least 25 of those words have weight at most 51.

This dual-GRS formulation is exact and keeps both source curves. A
source-free classification of arbitrary near-minimum GRS words is not
enough; the 69 coefficient vectors must also lie on the selected
rational normal curve determined by (7.7).

### 8.1 Global resultant remainder

Let

\[
L(\lambda)=\prod_{s=1}^m(\lambda-\lambda_s).
\]

The fixed-selected-root resultant is

\[
\mathcal R(\lambda)
=
\prod_{i=1}^R N(t_i,\lambda).
\tag{8.9}
\]

At every actual line parameter \(\lambda_s\), exactly \(a-1\) selected
roots occur in \(P_{\lambda_s}\). Hence

\[
\boxed{
L(\lambda)^{a-1}\mid\mathcal R(\lambda).
}
\tag{8.10}
\]

Since every \(N(t_i,\lambda)\) has degree at most \(a-1\),

\[
\deg
\frac{\mathcal R}{L^{a-1}}
\le
(R-m)(a-1).
\tag{8.11}
\]

At minimum overload this is

\[
\boxed{
\deg
\frac{\mathcal R}{L^{a-1}}
\le
(a-4)(a-1).
}
\tag{8.12}
\]

For \(a=12,R=69,m=61\), the complete failure of all 69 horizontal
polynomials to be minimum-weight words is therefore stored in one
residual polynomial of degree at most 88. Multiple incidence roots only
reduce the remaining degree. A continuation may either factor this
residual through a bounded template or show that the diagonal-Cauchy
kernel cannot support it.

## 9. Corrected next lemma

The low-support branch of SPSI reduces to:

> **Noncanonical overloaded-line emission.**
> In an actual KoalaBear equality-wall reciprocal-Cauchy packet, a
> noncanonical line carrying at least \(R-a+4\) selected vertices in the
> normal form (6.7) emits an enabled same-record quotient, planted,
> proper-field, collective-rank, or saturation cell.

For \(a=12,R=69\), a proof may use either:

1. the common-root precursor \(N_t\equiv0\); or
2. the coordinate-ratio rank precursor (7.2); or
3. the rational-normal packet with 61 split degree-11 locators, pairwise
   intersection at most nine, and at least 25 selected roots occurring
   with multiplicity at least 10.

The branch of relations with support greater than \(2k+1\) remains
separate. A full SPSI proof must either sparsify such a relation without
losing its selected owner or classify its larger support directly.

## 10. Finite guardrails

The exact verifier

```text
verify_postcritical_block_line_relation_space.py
```

checks:

* all 495 normalized \(\mathbf F_{13}\) configurations;
* all 715 \(\mathbf F_{13}\) configurations at
  \((a,R)=(4,9)\), where canonical-line capacity is eight and a relation
  requires nine points;
* exact generation of every known relation space by canonical block-line
  relations;
* exact exceptions in characteristics \(17,19,23\);
* two- and three-block higher-dimensional planted examples;
* canonical and noncanonical rich-line incidence;
* the complete surviving KoalaBear capacity table.

The small-field census contains noncanonical collinear triples and, over
the complete normalized \(\mathbf F_{13}\) family, noncanonical lines of
size four. Therefore the statement “every rich line is canonical” is
false and is not used here. None of those small-field noncanonical lines
reaches its postcritical overload threshold. All 715 configurations in
the exact first zero-canonical-capacity census have full postcritical rank
84. Their maximum noncanonical line incidence is five, versus the required
nine. The exact maximum-pair distribution is

```text
(canonical max, noncanonical max, configurations)
(5,4,442), (8,4,195), (8,5,78).
```
