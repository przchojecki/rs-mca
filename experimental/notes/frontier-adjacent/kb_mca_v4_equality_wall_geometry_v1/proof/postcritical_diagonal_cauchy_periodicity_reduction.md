# Postcritical Diagonal-Cauchy Periodicity Reduction

## 1. Status

This note closes the generic rational-normal branch of the
noncanonical overloaded-line target for every KoalaBear row currently
used by the equality-wall packet:

\[
(a,R)=(12,69),\qquad
(a,R)=(14,67),(14,68),(14,69).
\]

More precisely, an overloaded noncanonical line in any of these rows
cannot have distinct coordinate factors and full coefficient rank.
Therefore every such line must already lie in one of the two structural
branches isolated before the rational-normal reduction:

1. a common selected root; or
2. a coordinate-ratio/collective-rank defect.

This is a pure packing contradiction in the generic branch. It does not
by itself convert either remaining precursor into an active same-record
owner payment.

## 2. Generic diagonal-Cauchy curve

Put

\[
n=a-1.
\]

In the generic branch, after projective changes of the two parameters,
the line correspondence has the form

\[
N(T,\lambda)
=
A_\Sigma(T)B(\lambda)
\sum_{j=1}^{a}
\frac{w_j}
{(T-\alpha_j)(\lambda-\beta_j)},
\qquad w_j\ne0,
\tag{2.1}
\]

where

\[
A_\Sigma(T)=\prod_{j=1}^{a}(T-\alpha_j),
\qquad
B(\lambda)=\prod_{j=1}^{a}(\lambda-\beta_j),
\]

the \(\alpha_j\) are distinct, and the \(\beta_j\) are distinct. Thus
\(N\) has bidegree \((n,n)\).

Let

\[
\mathcal D=V(N)\subseteq\mathbf P^1_T\times\mathbf P^1_\lambda.
\]

No vertical line \(T=\alpha_i\) and no horizontal line
\(\lambda=\beta_j\) is a component of \(\mathcal D\).

## 3. Exact source-pole periodicity

### Lemma 3.1

On \(\mathcal D\),

\[
\boxed{
\mathcal O_{\mathcal D}(a,0)
\simeq
\mathcal O_{\mathcal D}(0,a).
}
\tag{3.1}
\]

Equivalently,

\[
\boxed{
\mathcal O_{\mathcal D}(a,-a)
\simeq
\mathcal O_{\mathcal D}.
}
\tag{3.2}
\]

### Proof

At \(T=\alpha_i\), every term in (2.1) vanishes except the \(i\)-th
term after cancellation. Hence

\[
N(\alpha_i,\lambda)
=
c_i\prod_{j\ne i}(\lambda-\beta_j),
\qquad c_i\ne0.
\tag{3.3}
\]

Similarly,

\[
N(T,\beta_j)
=
d_j\prod_{i\ne j}(T-\alpha_i),
\qquad d_j\ne0.
\tag{3.4}
\]

Therefore the zero divisor on \(\mathcal D\) of the restriction of
\(A_\Sigma(T)\) is supported at the off-diagonal points

\[
(\alpha_i,\beta_j),\qquad i\ne j,
\]

and the same is true for the restriction of \(B(\lambda)\).

There are exactly

\[
a(a-1)=an
\]

such points. This is the full intersection degree of either
\(\mathcal D\) with the divisor \(A_\Sigma=0\), of class \((a,0)\), or
with the divisor \(B=0\), of class \((0,a)\). Thus, once the local
multiplicity at every off-diagonal point is shown to be one, there can
be no additional zero or embedded contribution in either restricted
divisor.

The scheme multiplicities agree. Indeed, at an off-diagonal point
\((\alpha_i,\beta_j)\), put

\[
x=T-\alpha_i,\qquad y=\lambda-\beta_j.
\]

The two terms indexed by \(i\) and \(j\) give

\[
N=u_{ij}y+v_{ij}x+xyH_{ij}(x,y),
\qquad
u_{ij}v_{ij}\ne0.
\tag{3.5}
\]

Thus \(x\) and \(y\) are associates in the local ring of
\(\mathcal D\). In particular, both intersections are transverse there.
Together with the degree count above, the two restricted sections have
the same complete Cartier divisor, so their ratio is a nowhere-vanishing
section of
\(\mathcal O_{\mathcal D}(a,-a)\). This proves (3.1)-(3.2).
\(\square\)

The periodicity is specific to the diagonal-Cauchy form. It is absent
for a general bidegree-\((n,n)\) curve.

## 4. The selected grid creates a low-degree section

Let

\[
t_1,\ldots,t_R
\]

be the selected source parameters and let

\[
\lambda_1,\ldots,\lambda_m
\]

be the actual points on the noncanonical line. Put

\[
V_T(T)=\prod_{i=1}^{R}(T-t_i),
\qquad
L_\Lambda(\lambda)
=
\prod_{s=1}^{m}(\lambda-\lambda_s).
\tag{4.1}
\]

Every actual line fiber is a squarefree locator:

\[
N(T,\lambda_s)=c_sP_{I_s}(T),
\qquad
P_{I_s}\mid V_T,
\qquad
c_s\ne0.
\tag{4.2}
\]

Consequently the horizontal divisor

\[
\sum_{s=1}^{m}\mathcal D\cap\{\lambda=\lambda_s\}
\]

is a subdivisor of the zero divisor of \(V_T|_{\mathcal D}\). Dividing
the two restricted sections gives a nonzero section

\[
\boxed{
0\ne\sigma_{\rm grid}
\in
H^0\!\left(
\mathcal D,\mathcal O_{\mathcal D}(R,-m)
\right).
}
\tag{4.3}
\]

Its zero divisor has degree

\[
n(R-m).
\tag{4.4}
\]

At minimum overload \(m=R-a+4\), this is

\[
n(a-4)=(a-1)(a-4),
\]

the same defect recorded by the GRS excess and the resultant remainder.

## 5. Two cohomological vanishing lemmas

### Lemma 5.1: subcritical first coordinate

Let \(\mathcal D\) be any bidegree-\((n,n)\) divisor. If

\[
0\le r\le n-1,\qquad s\ge1,
\]

then

\[
\boxed{
H^0\!\left(
\mathcal D,\mathcal O_{\mathcal D}(r,-s)
\right)=0.
}
\tag{5.1}
\]

### Proof

Tensoring the ideal sequence of \(\mathcal D\) by
\(\mathcal O(r,-s)\) gives

\[
0\longrightarrow
\mathcal O(r-n,-s-n)
\longrightarrow
\mathcal O(r,-s)
\longrightarrow
\mathcal O_{\mathcal D}(r,-s)
\longrightarrow0.
\tag{5.2}
\]

The middle term has no global sections. By the Kunneth formula,

\[
H^1\!\left(
\mathbf P^1\times\mathbf P^1,
\mathcal O(r-n,-s-n)
\right)=0:
\]

both factors have negative degree, and when \(r=n-1\) the first factor
is \(\mathcal O(-1)\), whose \(H^0\) and \(H^1\) both vanish. The long
exact sequence proves (5.1).
\(\square\)

### Lemma 5.2: full coefficient-rank boundary

Write

\[
N(T,\lambda)=\sum_{j=0}^{n}N_j(T)\lambda^j.
\tag{5.3}
\]

Assume

\[
\{N_0,\ldots,N_n\}
\]

is a basis of \(F[T]_{\le n}\). Then, for every \(s\ge2\),

\[
\boxed{
H^0\!\left(
\mathcal D,\mathcal O_{\mathcal D}(n,-s)
\right)=0.
}
\tag{5.4}
\]

### Proof

The only possible global sections are the kernel of

\[
H^1(\mathcal O(0,-s-n))
\xrightarrow{\ \times N\ }
H^1(\mathcal O(n,-s)).
\tag{5.5}
\]

Use the standard Laurent representatives. An element of the source is

\[
q(\lambda)
=
\sum_{h=1}^{s+n-1}c_h\lambda^{-h}.
\tag{5.6}
\]

For each \(1\le r\le s-1\), the coefficient of
\(\lambda^{-r}\) in the target is

\[
\sum_{j=0}^{n}c_{j+r}N_j(T).
\tag{5.7}
\]

If the image is zero, basis independence of the \(N_j\) forces

\[
c_r=c_{r+1}=\cdots=c_{r+n}=0
\]

for every \(1\le r\le s-1\). These consecutive windows cover all
coefficients in (5.6), so \(q=0\). Thus (5.5) is injective and (5.4)
follows.
\(\square\)

In the generic diagonal-Cauchy branch, the hypothesis of Lemma 5.2 is
automatic. Indeed,

\[
N(T,\lambda)
=
\sum_{j=1}^{a}c_jL_j(T)g_j(\lambda),
\qquad c_j\ne0,
\tag{5.8}
\]

where the \(L_j\) and \(g_j\) are two bases of the degree-\(\le n\)
polynomial spaces.

## 6. KoalaBear rows

By Lemma 3.1, for every integer \(q\),

\[
\mathcal O_{\mathcal D}(R,-m)
\simeq
\mathcal O_{\mathcal D}(R-qa,-m+qa).
\tag{6.1}
\]

### 6.1 The \(a=12,\ R=69\) row

Here

\[
n=11,\qquad61\le m\le69.
\]

Taking \(q=5\) gives

\[
\mathcal O_{\mathcal D}(69,-m)
\simeq
\mathcal O_{\mathcal D}(9,-s),
\qquad
s=m-60\in[1,9].
\]

Lemma 5.1 contradicts the grid section (4.3).

### 6.2 The \(a=14,\ R=67\) row

Here

\[
n=13,\qquad57\le m\le67.
\]

Taking \(q=4\) gives

\[
\mathcal O_{\mathcal D}(67,-m)
\simeq
\mathcal O_{\mathcal D}(11,-s),
\qquad
s=m-56\in[1,11].
\]

Lemma 5.1 gives the contradiction.

### 6.3 The \(a=14,\ R=68\) row

Here

\[
58\le m\le68,
\]

and

\[
\mathcal O_{\mathcal D}(68,-m)
\simeq
\mathcal O_{\mathcal D}(12,-s),
\qquad
s=m-56\in[2,12].
\]

Again Lemma 5.1 applies.

### 6.4 The \(a=14,\ R=69\) row

Here

\[
59\le m\le69,
\]

and

\[
\mathcal O_{\mathcal D}(69,-m)
\simeq
\mathcal O_{\mathcal D}(13,-s),
\qquad
s=m-56\in[3,13].
\]

This is the boundary \(r=n\). The generic diagonal-Cauchy coefficient
polynomials form a basis, and \(s\ge2\), so Lemma 5.2 contradicts
(4.3).

## 7. Theorem

> **Generic noncanonical overload exclusion.**
> In each KoalaBear row
> \[
> (a,R)=(12,69),(14,67),(14,68),(14,69),
> \]
> a noncanonical locator line with at least
> \[
> m\ge R-a+4
> \]
> selected vertices cannot lie in the generic diagonal-Cauchy branch.

Therefore the complete low-support line alternative reduces to

\[
\boxed{
\text{common selected root}
\quad\text{or}\quad
\text{coordinate-ratio/collective-rank defect}.
}
\tag{7.1}
\]

The 61-record diagonal-Cauchy/GRS packet itself is impossible. The
degree-88 remainder is the divisor degree of the forbidden section, not
an additional surviving branch.

## 8. Subsequent grouped completion

The generic branch needs no owner adapter. The subsequent note
`postcritical_grouped_cauchy_component_reduction.md` proves that the two
outputs in (7.1) are impossible at the overload threshold as well:

1. common selected roots are removed as vertical components;
2. proportional coordinate factors are grouped after removing their
   common horizontal component;
3. the resulting source-pole relation differs from the exact period only
   by an effective negative divisor.

Thus no overloaded line packet remains. The conic, cubic, and
support-at-least-\(3k+1\) circuit branches remain separate.
