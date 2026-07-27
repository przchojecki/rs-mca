# Rank-One Split Scroll: Source-Fiber Reduction

## 1. Status

This note advances the low-excess branch of the KoalaBear equality-wall
rank-one split-scroll target. It proves:

1. the primitive source scalar has simple projective roots exactly at the
   source-map values;
2. the scroll numerator has an exact source-fiber Lagrange decomposition;
3. the persistent carrier-root core consumes degree in every source-fiber
   coefficient;
4. after the \(q=1\) range \(\delta<c\) is excluded separately, exact
   pushforward degree \(q=2\) on the surviving low-excess range
   \(c\le\delta<e\) bounds the kernel splitting degree by \(16\) and leaves
   at least \(53+a\) regular records;
5. the source-degree and carrier-incidence budgets are incompatible for
   every \(2\le a\le11\); and
6. consequently, no hypothetical 69-record packet exists for
   \[
   3{,}912\le\delta<118{,}077.
   \]

The full rank-one split-scroll count remains open. The low-excess remainder
consists of the five splitting degrees

\[
a\in\{12,13,14,15,16\}.
\]

No equality-wall payment is booked by this partial result.

## 2. Input from the proved normalization

Use the fixed constants

\[
s=202{,}416,\qquad
e=134{,}944,\qquad
c=67{,}472,\qquad
J=981{,}105,
\]

so

\[
s=e+c=3c,\qquad e=2c.
\]

In the low-excess branch

\[
3{,}912\le\delta<e,
\]

the proved kernel-sheaf normalization supplies:

* a saturated generic kernel
  \[
  \mathcal K\simeq\mathcal O(-a),\qquad 0\le a\le56;
  \]
* at least
  \[
  R\ge13+a
  \]
  regular selected parameters;
* a primitive homogeneous generator
  \[
  G(t,X)=A_t(X)P(t,X);
  \]
* a coprime degree-\(e\) pencil \(A_t=U+tV\);
* a source scalar \(\lambda(t)\) satisfying
  \[
  G(t,\sigma)=\lambda(t)f_0(\sigma)
  \quad(\sigma\in\Sigma),
  \]
  where \(|\Sigma|=s\) and \(f_0(\sigma)\ne0\);
* degree bounds
  \[
  \deg_tP\le a-1,\qquad \deg_XP=d:=c+\delta<s;
  \]
* at every regular selected parameter \(t_i\),
  \[
  p_i(X)=\frac{P(t_i,X)}{\lambda(t_i)};
  \]
* monic squarefree \(p_i=\Lambda_{D_i}\), with
  \[
  D_i\subseteq U_0,\qquad |D_i|=d,
  \]
  on a fixed carrier set
  \[
  |U_0|=u:=J+c+\delta;
  \]
* disjoint source and carrier domains, \(\Sigma\cap U_0=\varnothing\).

The generator is primitive in the saturated line-bundle sense: its
coefficient vector has no common nonconstant projective parameter factor.
The bounds \(a\le56\) and \(R\ge13+a\) listed here are the coarse global
inputs; Section 6 replaces them by \(a\le16\) and \(R_{\rm reg}\ge53+a\)
on the surviving low-excess range.

Let

\[
f=[-U:V]\colon\mathbf P^1_X\to\mathbf P^1_t
\]

be the degree-\(e\) source map cut out by the pencil.

## 3. The source scalar has no spare multiplicity

Let \(\beta\in\mathbf P^1_t\) be a projective zero of \(\lambda\).

Suppose first that \(\beta\notin f(\Sigma)\). Then
\(A_\beta(\sigma)\ne0\) for every \(\sigma\in\Sigma\). Specializing

\[
A_t(\sigma)P(t,\sigma)=\lambda(t)f_0(\sigma)
\]

at \(t=\beta\) gives

\[
P(\beta,\sigma)=0
\qquad(\sigma\in\Sigma).
\]

The polynomial \(P(\beta,X)\) has \(X\)-degree at most \(d<s\), so it
vanishes identically. Hence the parameter linear form \(L_\beta(t)\)
divides every \(X\)-coefficient of \(P\), and therefore every coefficient
of \(G=A_tP\). This contradicts primitivity.

Now suppose \(\beta\in f(\Sigma)\) but \(\lambda\) has multiplicity at least
two at \(\beta\). If \(f(\sigma)\ne\beta\), the preceding specialization
again gives \(P(\beta,\sigma)=0\). If \(f(\sigma)=\beta\), then
\(A_t(\sigma)\) has a simple zero at \(\beta\), while the right side has a
zero of order at least two. Therefore \(P(t,\sigma)\) also vanishes at
\(\beta\). Thus \(P(\beta,X)\) vanishes on all \(s\) source points and is
again identically zero, contradicting primitivity.

It follows that every projective root of \(\lambda\) is a simple source-map
value. The converse was proved in the upstream normalization: every
source-map value is a root of \(\lambda\). Since the homogeneous source
scalar is a nonzero section of degree \(a\),

\[
\boxed{
\operatorname{div}(\lambda)
=
\sum_{\alpha\in f(\Sigma)}[\alpha],
\qquad
|f(\Sigma)|=a.
}
\tag{3.1}
\]

In particular, a source fiber contains at most \(e\) points and
\(s>e\), so

\[
\boxed{a\ge2.}
\tag{3.2}
\]

## 4. Exact source-fiber Lagrange decomposition

Enumerate the source-map values as

\[
f(\Sigma)=\{\alpha_1,\ldots,\alpha_a\},
\qquad
\Sigma_j=\{\sigma\in\Sigma:f(\sigma)=\alpha_j\},
\qquad
n_j=|\Sigma_j|.
\]

Let \(L_j(t)\) be the projective linear form vanishing at \(\alpha_j\), and
put

\[
\lambda_j^*(t)=\frac{\lambda(t)}{L_j(t)}.
\]

Because the roots of \(\lambda\) are simple, the \(a\) forms
\(\lambda_j^*\) are a basis of the degree-\((a-1)\) parameter forms.
Therefore there are unique polynomials \(Q_j(X)\) such that

\[
\boxed{
P(t,X)=\sum_{j=1}^a Q_j(X)\lambda_j^*(t).
}
\tag{4.1}
\]

At \(\sigma\in\Sigma_j\), the pencil member is a nonzero scalar multiple
of \(L_j(t)\). Dividing the source identity by that linear form gives

\[
P(t,\sigma)
=
\kappa_\sigma\lambda_j^*(t),
\qquad
\kappa_\sigma\ne0.
\]

Uniqueness in the Lagrange basis implies

\[
Q_j(\sigma)\ne0
\quad(\sigma\in\Sigma_j),
\qquad
Q_j(\sigma)=0
\quad(\sigma\in\Sigma\setminus\Sigma_j).
\]

Consequently,

\[
\boxed{
Q_j(X)
=
\Lambda_{\Sigma\setminus\Sigma_j}(X)R_j(X),
\qquad
\deg R_j\le \delta-e+n_j.
}
\tag{4.2}
\]

Since \(Q_j\ne0\), this also proves

\[
n_j\ge e-\delta.
\]

Summing over the \(a\) source fibers gives the necessary source-degree
condition

\[
\boxed{
a(e-\delta)\le s.
}
\tag{4.3}
\]

Equivalently,

\[
\delta\ge e-\left\lfloor\frac{s}{a}\right\rfloor.
\tag{4.4}
\]

## 5. Persistent carrier roots

Define the persistent carrier core

\[
C_0=\{x\in U_0:P(t,x)\equiv0\},
\qquad
g=|C_0|.
\]

By the Lagrange basis in (4.1), \(x\in C_0\) exactly when

\[
Q_1(x)=\cdots=Q_a(x)=0.
\]

The source and carrier sets are disjoint, so all source-locator factors in
(4.2) are units at \(x\in U_0\). Hence every persistent carrier root is a
root of every \(R_j\).

The monicity identity supplies a one-unit refinement. The affine leading
\(X\)-coefficient of \(P\) is \(\lambda(t)\), while
\(\deg_tP\le a-1\). The degree-\(a\) projective divisor of \(\lambda\)
therefore has exactly one root at parameter infinity. Index that source
value by \(a\). At every finite source value \(\alpha_j\), \(j<a\), the
specialization \(P(\alpha_j,X)\) loses its leading \(X\)-term. Consequently,

\[
\deg R_j\le\delta-e+n_j-1
\quad(1\le j<a),
\qquad
\deg R_a\le\delta-e+n_a.
\tag{5.1}
\]

Therefore

\[
ag\le
\sum_{j=1}^a\deg R_j
\le
a(\delta-e)+s-(a-1).
\]

Thus

\[
\boxed{
g\le
\delta-e+
\left\lfloor\frac{s-(a-1)}{a}\right\rfloor.
}
\tag{5.2}
\]

Put

\[
h=\delta-g.
\]

Then (5.2) becomes

\[
\boxed{
h\ge h_{\min}(a):=
e-\left\lfloor\frac{s-(a-1)}{a}\right\rfloor.
}
\tag{5.3}
\]

After removal of the persistent carrier factor, the total residual degree
available in the source-fiber coefficients is at most

\[
\boxed{
\kappa_a(h):=
s-a(e-h)-(a-1).
}
\tag{5.4}
\]

This quantity is nonnegative by (5.3).

## 6. Exact low-excess pushforward degree

First suppose

\[
3{,}912\le\delta<c.
\]

Then

\[
e<N=s+\delta<2e,
\]

so \(q=1\). The kernel and exceptional-divisor bounds give

\[
a\le m-1\le8,
\qquad
D_{\rm exc}\le8-a,
\qquad
R_{\rm reg}\ge61+a.
\tag{6.1}
\]

The source-degree condition (4.3) excludes \(a\ge3\), while (3.2) gives
\(a\ge2\). Hence only \(a=2\) could remain. The refined bound (5.3) gives

\[
h\ge33{,}737.
\]

Root incidence would require

\[
63(c+h)\le J+c+h,
\]

or \(62(c+h)\le J\). At the smallest possible \(h\), this fails by

\[
\boxed{
62(67{,}472+33{,}737)-981{,}105
=5{,}293{,}853.
}
\tag{6.2}
\]

Thus the entire interval \(\delta<c\) is empty.

Now consider the only surviving low-excess range

\[
c\le\delta<e.
\]

The graph-polynomial degree is \(N=s+\delta\). Since \(s+c=2e\),

\[
2e\le N<3e.
\]

Therefore the pushforward splitting integer is exactly

\[
\boxed{q=\left\lfloor\frac Ne\right\rfloor=2.}
\tag{6.3}
\]

Let \(m=\dim W\le9\). For the rank-one kernel
\(\mathcal K\simeq\mathcal O(-a)\), the kernel-degree and exceptional-divisor
theorems now give

\[
\boxed{a\le q(m-1)\le16}
\tag{6.4}
\]

and

\[
D_{\rm exc}
\le q(m-1)-a
\le16-a.
\tag{6.5}
\]

Among the 69 selected parameters, at least

\[
\boxed{R_{\rm reg}\ge53+a}
\tag{6.6}
\]

are regular rank-one specializations.

## 7. Strengthened carrier incidence

For \(x\in U_0\setminus C_0\), the parameter polynomial \(P(t,x)\) is
nonzero and has degree at most \(a-1\). It can therefore vanish at at most
\(a-1\) distinct regular selected parameters.

Every regular locator has \(d-g=c+h\) roots outside the persistent core,
while the available carrier outside that core has size

\[
u-g=J+c+h.
\]

Counting root incidences gives

\[
\boxed{
R_{\rm reg}(c+h)\le(a-1)(J+c+h).
}
\tag{7.1}
\]

Using \(R_{\rm reg}\ge53+a\), a necessary condition is

\[
\boxed{
54(c+h)\le(a-1)J.
}
\tag{7.2}
\]

For \(a=3\), the conservative unrefined source bound gives \(h\ge c\),
while (6.6) gives \(R_{\rm reg}\ge56\). Equation (7.1) would imply

\[
56(2c)\le2(J+2c).
\]

The exact contradiction margin is

\[
\begin{aligned}
56(134{,}944)-2(981{,}105+134{,}944)
&=54(134{,}944)-2(981{,}105)\\
&=\boxed{5{,}324{,}766}>0.
\end{aligned}
\tag{7.3}
\]

Hence the actual three-source-fiber branch is empty. More generally,
combining (5.3) and (7.2) excludes every

\[
\boxed{2\le a\le11.}
\tag{7.4}
\]

## 8. Closed low-excess range

Section 6 proves that the range \(\delta<c\) is empty.

For \(a\ge12\), (5.3) gives

\[
h\ge h_{\min}(12)=118{,}077.
\]

Since \(h=\delta-g\le\delta\), no surviving packet has
\(\delta<118{,}077\). Therefore:

> **Theorem 8.1: exact-\(q\) low-excess exclusion.**
> A hypothetical normalized 69-record equality-wall packet cannot lie in
> \[
> \boxed{3{,}912\le\delta<118{,}077.}
> \]

This removes \(114{,}165\) integer excess values. In particular, the
previously isolated three-source-fiber split-plane target is proved empty
for the actual equality-wall packet. The stronger standalone assertion
about arbitrary three-dimensional split planes is neither needed nor
proved.

## 9. Exact surviving low-excess windows

The complete arithmetic windows left by (5.3), (7.2), and \(h<e\) are

\[
\begin{array}{c|c|c|c}
a&R_{\rm reg}\text{ lower bound}&h_{\min}&h_{\max}\\ \hline
12&65&118{,}077&132{,}382\\
13&66&119{,}375&134{,}943\\
14&67&120{,}487&134{,}943\\
15&68&121{,}451&134{,}943\\
16&69&122{,}294&134{,}943.
\end{array}
\tag{9.1}
\]

These five cases are not eliminated by the present first-incidence or
pair-intersection ledgers.

## 10. Revised remaining target

The next useful theorem is:

> **Exact-\(q\) five-degree split-scroll cap.**
> For each \(a\in\{12,\ldots,16\}\), no normalized low-excess rank-one
> packet in the corresponding window (9.1) contains \(53+a\) regular
> monic squarefree specializations split over the same fixed carrier, with
> the source-fiber decomposition (4.1), the refined residual budget (5.4),
> and pair-gcd degree at most \(h\).

The target may equivalently emit an existing same-record owner from one of
those regular specializations.

The complete cap \(68\) and the descended general-excess branch
\(\delta\ge e\) remain open.

## 11. Proof authority and nonclaims

This note consumes the rank-one normalization from:

```text
experimental/notes/frontier-adjacent/
  kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md
  kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.md
```

It proves a source-fiber refinement and a partial parameter exclusion. It
does not:

* prove the full universal-kernel split-quotient lemma;
* prove cap \(68\);
* identify a new active owner;
* cover \(\delta\ge e\);
* justify treating an auxiliary source-fiber coefficient as an owner; or
* book any slope payment.
