# Minimum-Window Coefficient-Curve Birationality

## 1. Status

This note proves that the source-coefficient curve is birational onto its
image at the lower endpoint of every surviving low-excess splitting-degree
window

\[
a\in\{12,13,14,15,16\}.
\]

It rules out a nontrivial covering of a lower-degree rational-normal or
scroll curve at those five endpoints. It does not exclude the birational
high-degree image and therefore does not prove the split-scroll cap.

## 2. Coefficient morphism

After removal of the persistent carrier core, write

\[
\overline P(t,X)
=
\sum_{j=1}^a
\overline Q_j(X)\lambda_j^*(t),
\tag{2.1}
\]

where

\[
\overline Q_j
=
\Lambda_{\Sigma\setminus\Sigma_j}\widetilde R_j.
\tag{2.2}
\]

The coefficient polynomials define

\[
\Phi:\mathbf P^1_X\longrightarrow\mathbf P^{a-1},
\qquad
X\longmapsto
[\overline Q_1(X):\cdots:\overline Q_a(X)].
\tag{2.3}
\]

This is a morphism with

\[
\boxed{\Phi^*\mathcal O(1)\simeq\mathcal O(D),\qquad D=c+h.}
\tag{2.4}
\]

Indeed, the \(\overline Q_j\) have no common zero. A common finite zero
would make \(\overline P(t,X)\) vanish identically in \(t\). Every regular
locator specialization would then vanish there, but each locator is monic,
has exact degree \(D\), and has all its roots in the fixed carrier. Such a
carrier zero would belong to the already removed persistent core, while a
zero outside the carrier is impossible. At parameter \(X=\infty\), the
monicity coefficient has exact degree \(D\), so there is no base point
there either.

The exact weighted-GRS theorem gives

\[
\dim\operatorname{span}
\{\overline Q_1,\ldots,\overline Q_a\}=a.
\tag{2.5}
\]

Hence the image curve is nondegenerate in \(\mathbf P^{a-1}\).

Let \(\widetilde{\mathcal C}\) be the normalization of the image and
factor

\[
\mathbf P^1_X
\xrightarrow{\ \psi\ }
\widetilde{\mathcal C}
\longrightarrow
\Phi(\mathbf P^1).
\tag{2.6}
\]

Write

\[
d_{\rm cov}=\deg\psi.
\]

Degree multiplicativity gives

\[
\boxed{
D=d_{\rm cov}\deg\Phi(\mathbf P^1).
}
\tag{2.7}
\]

In particular,

\[
d_{\rm cov}\mid D.
\tag{2.8}
\]

Moreover, every nonconstant ratio
\(\overline Q_j/\overline Q_k\) descends to the normalization. The
KoalaBear characteristic is larger than all degrees in this packet, so
the map is separable and

\[
\boxed{
d_{\rm cov}
\mid
\deg\left(\frac{\overline Q_j}{\overline Q_k}\right).
}
\tag{2.9}
\]

## 3. Two zero-slack finite source fibers

At the minimum of a surviving window, put

\[
h=h_{\min}(a),
\qquad
n_0=e-h+1,
\tag{3.1}
\]

and

\[
\mathcal B_a(h)
=
s-a(e-h)-(a-1).
\tag{3.2}
\]

For the \(a-1\) finite source values,

\[
n_j=n_0+\varepsilon_j,
\qquad
\deg\widetilde R_j\le\varepsilon_j,
\tag{3.3}
\]

while all \(\varepsilon_j\) are nonnegative integers and

\[
\sum_{j=1}^a\varepsilon_j=\mathcal B_a(h).
\tag{3.4}
\]

Thus at least

\[
(a-1)-\mathcal B_a(h)
\tag{3.5}
\]

finite source fibers have \(\varepsilon_j=0\). The exact endpoint table is

\[
\begin{array}{c|r|r|r|r|r}
a&
h_{\min}&
D=c+h_{\min}&
n_0=e-h_{\min}+1&
\mathcal B_a(h_{\min})&
(a-1)-\mathcal B_a(h_{\min})\\ \hline
12&118{,}077&185{,}549&16{,}868&1&10\\
13&119{,}375&186{,}847&15{,}570&7&5\\
14&120{,}487&187{,}959&14{,}458&5&8\\
15&121{,}451&188{,}923&13{,}494&7&7\\
16&122{,}294&189{,}766&12{,}651&1&14.
\end{array}
\tag{3.6}
\]

Every row supplies at least two zero-slack finite fibers. Choose two of
them, \(j\ne k\). Their residual multipliers are nonzero constants and
their source fibers are disjoint sets of the same cardinality \(n_0\).
Cancelling the common source factors in (2.2) gives

\[
\frac{\overline Q_j}{\overline Q_k}
=
u_{jk}
\frac{\Lambda_{\Sigma_k}}{\Lambda_{\Sigma_j}},
\qquad
u_{jk}\in F^\times.
\tag{3.7}
\]

The numerator and denominator in (3.7) are coprime and both have degree
\(n_0\). Therefore

\[
\boxed{
\deg\left(\frac{\overline Q_j}{\overline Q_k}\right)=n_0.
}
\tag{3.8}
\]

## 4. Birationality theorem

> **Theorem 4.1.**
> At the lower endpoint of every surviving window
> \(a=12,\ldots,16\), the coefficient morphism \(\Phi\) is birational onto
> its image.

### Proof

Equations (2.8), (2.9), and (3.8) give

\[
d_{\rm cov}\mid\gcd(D,n_0).
\]

For the five rows in (3.6),

\[
\begin{array}{c|ccccc}
a&12&13&14&15&16\\ \hline
\gcd(D,n_0)&1&1&1&1&1.
\end{array}
\tag{4.1}
\]

Hence \(d_{\rm cov}=1\) in every case. \(\square\)

## 5. Consequences

The image curve has exact degree

\[
\boxed{\deg\Phi(\mathbf P^1)=D.}
\tag{5.1}
\]

In particular, the minimum-window packet cannot be explained by a
nontrivial cover of:

* a rational normal curve of degree \(a-1\);
* a lower-degree coefficient curve;
* a low-degree scroll section obtained only after quotienting the
  \(X\)-parameter.

Any such route must instead produce an actual factorization of the
source-domain parameter, contradicting (4.1), or use additional owner
structure.

The birationality does not itself bound how many selected GRS vertices the
degree-\(D\) image curve can meet. The remaining endpoint theorem is:

> **Birational minimum-row complementary-defect rigidity.**
> A source-derived birational degree-\(D\) coefficient curve with the
> endpoint source divisors and residual budget cannot realize the forced
> selected minimum-row vertices without emitting an already enabled
> same-record owner.

## 6. Nonclaims

This note does not exclude the five minimum endpoints, the interiors of
the five windows, the general-excess descent, cap \(68\), or an owner
payment.
