# Regular Split-Scroll GRS and MDS-Deficit Reduction

## 1. Status

This note proves an exact code-theoretic refinement of the surviving
low-excess rank-one split-scroll branch.

It does not prove the cap \(68\). Its purpose is to replace two loose
statements,

\[
\dim\operatorname{span}\{p_i\}\le16
\quad\text{and}\quad
\sum_x m_x\le(a-1)|U|,
\]

by an exact weighted-GRS model and an exact MDS-deficit identity.

The strongest new consequence is for splitting degree \(a=12\): depending
on the number \(R\) of regular records, between \(394{,}145\) and
\(1{,}136{,}341\) carrier rows are forced to be minimum-weight
\(\mathrm{GRS}_{12}\) words even at the least rigid endpoint.

## 2. Inherited low-excess packet

Use the notation of
`rank_one_split_scroll_source_fiber_reduction.md`. Thus

\[
P(t,X)=\sum_{j=1}^a Q_j(X)\lambda_j^*(t),
\qquad
\lambda_j^*(t)=\frac{\lambda(t)}{L_j(t)},
\tag{2.1}
\]

where the \(L_j\) have distinct projective roots, the
\(\lambda_j^*\) form a basis of the degree-\((a-1)\) parameter forms, and

\[
Q_j(\sigma)\ne0\quad(\sigma\in\Sigma_j),
\qquad
Q_j(\sigma)=0\quad(\sigma\in\Sigma\setminus\Sigma_j).
\tag{2.2}
\]

In particular, \(Q_1,\ldots,Q_a\) are linearly independent: evaluating a
linear relation at any point of \(\Sigma_j\) kills every term except the
\(j\)-th.

Let \(t_1,\ldots,t_R\) be distinct regular selected parameters. Hence
\(\lambda(t_i)\ne0\), and

\[
p_i(X)=\frac{P(t_i,X)}{\lambda(t_i)}
\tag{2.3}
\]

is a monic fixed-domain split locator.

Choose a projective parameter chart in which the \(t_i\) and the source
values are finite. This loses no information because there are fewer than
the field size. Write the source values as \(\alpha_j\), absorb harmless
nonzero constants into \(Q_j\), and put

\[
\lambda(t)=\prod_{j=1}^a(t-\alpha_j),
\qquad
\ell_j(t)=\frac{\lambda(t)}{t-\alpha_j}.
\tag{2.4}
\]

Then

\[
p_i(X)
=
\frac1{\lambda(t_i)}
\sum_{j=1}^a Q_j(X)\ell_j(t_i).
\tag{2.5}
\]

## 3. Exact weighted-GRS theorem

For distinct evaluation points \(t_1,\ldots,t_R\) and nonzero multipliers
\(v_i=\lambda(t_i)^{-1}\), define

\[
\operatorname{GRS}_a(\mathbf t,\mathbf v)
=
\{(v_i f(t_i))_{i=1}^R:\deg f<a\}.
\tag{3.1}
\]

> **Theorem 3.1: regular locator GRS block.**
> If \(R\ge a\), the coefficient-row space of
> \[
> (p_1,\ldots,p_R)
> \]
> is exactly
> \[
> \boxed{\operatorname{GRS}_a(\mathbf t,\mathbf v).}
> \tag{3.2}
> \]
> It has dimension \(a\). If \(R\ge a+1\) and
> \(T=\operatorname{diag}(t_1,\ldots,t_R)\), then
> \[
> \boxed{
> \dim(C+TC)=a+1,
> \qquad
> C=\operatorname{GRS}_a(\mathbf t,\mathbf v).
> }
> \tag{3.3}
> \]

### Proof

The forms \(\ell_1,\ldots,\ell_a\) are a basis of \(F[t]_{<a}\). For every
coefficient functional \([X^r]\), equation (2.5) gives

\[
([X^r]p_i)_{i=1}^R
=
\left(
v_i\sum_{j=1}^a [X^r]Q_j\,\ell_j(t_i)
\right)_{i=1}^R,
\]

which belongs to the code in (3.1). Hence the coefficient-row space is a
subspace of that code.

Let \(\mathcal Q\) be the coefficient matrix with columns \(Q_j\), and let

\[
\mathcal E_{j,i}=v_i\ell_j(t_i).
\]

The matrix \(\mathcal Q\) has column rank \(a\) by (2.2). The matrix
\(\mathcal E\) has row rank \(a\), because it is a weighted evaluation
matrix for the basis \(\ell_j\) at \(R\ge a\) distinct points. Therefore

\[
(p_1,\ldots,p_R)=\mathcal Q\mathcal E
\]

has rank \(a\). The contained row space and
\(\operatorname{GRS}_a(\mathbf t,\mathbf v)\) have the same dimension, so
they are equal.

Multiplication by \(T\) sends the evaluation of \(f(t)\) to the evaluation
of \(tf(t)\). Consequently

\[
C+TC=\operatorname{GRS}_{a+1}(\mathbf t,\mathbf v),
\]

which has dimension \(a+1\) when \(R\ge a+1\). \(\square\)

Dividing every \(p_i\) by the fixed monic persistent factor
\(\Lambda_{C_0}\) applies one injective triangular coefficient
transformation to all columns. It therefore preserves (3.2) and (3.3).

This proves that the regular restriction is one exact weighted-GRS block.
No mixed Kronecker-block ambiguity remains on the regular coordinates.

## 4. Exact carrier-row deficit

After removing the persistent carrier core, put

\[
D=c+h,
\qquad
n=J+D.
\tag{4.1}
\]

Every normalized regular locator has exactly \(D\) roots in the
\(n\)-point carrier. For a carrier coordinate \(x\), let

\[
m_x=\#\{i:p_i(x)=0\}.
\tag{4.2}
\]

The row

\[
(p_i(x))_{i=1}^R
\]

is a codeword in the exact GRS code (3.2). It is nonzero by the definition
of the removed persistent core. The MDS property therefore gives

\[
0\le m_x\le a-1.
\tag{4.3}
\]

Define its MDS deficit by

\[
\eta_x=(a-1)-m_x.
\tag{4.4}
\]

Double-counting carrier incidences gives the identity

\[
\sum_xm_x=RD.
\]

Therefore:

> **Theorem 4.1: exact MDS-deficit identity.**
> \[
> \boxed{
> \Delta_R:=\sum_x\eta_x
> =(a-1)(J+D)-RD
> =(a-1)J-(R-a+1)D.
> }
> \tag{4.5}
> \]
> In particular, the number \(N_{\min}\) of carrier rows with
> \(m_x=a-1\), equivalently minimum-weight GRS rows, satisfies
> \[
> \boxed{
> N_{\min}\ge n-\Delta_R.
> }
> \tag{4.6}
> \]
> More generally,
> \[
> \#\{x:\eta_x\ge r\}\le\frac{\Delta_R}{r}
> \qquad(r\ge1).
> \tag{4.7}
> \]

Equation (4.5) also recovers the first-incidence constraint
\(\Delta_R\ge0\), now with its exact coding-theoretic meaning.

## 5. Complete \(a=12\) regular-count ledger

For \(a=12\), the exact source and exceptional-divisor reductions give

\[
65\le R\le69,
\qquad
h\ge118{,}077.
\tag{5.1}
\]

Applying \(\Delta_R\ge0\) separately for every possible \(R\) yields:

\[
\begin{array}{c|c|c|r|r|r}
R&h_{\min}&h_{\max}&
\Delta_R(h_{\min})&
N_{\min}(h_{\min})&
N_{\min}(h_{\max})&
B(h_{\max})\\ \hline
65&118{,}077&132{,}382&772{,}509&394{,}145&1{,}180{,}920&171{,}661\\
66&118{,}077&128{,}749&586{,}960&579{,}694&1{,}177{,}326&128{,}065\\
67&118{,}077&125{,}245&401{,}411&765{,}243&1{,}173{,}819&86{,}017\\
68&118{,}077&121{,}864&215{,}862&950{,}792&1{,}170{,}438&45{,}445\\
69&118{,}077&118{,}599& 30{,}313&1{,}136{,}341&1{,}167{,}139&6{,}265.
\end{array}
\tag{5.2}
\]

Here

\[
B(h)
:=
\sum_{j=1}^{12}\deg\widetilde R_j
\le
s-12(e-h)-11
=
12h-1{,}416{,}923.
\tag{5.3}
\]

This budget has an exact source-fiber allocation. Index the projective
source value at parameter infinity by \(12\), and write

\[
n_j=e-h+1+\varepsilon_j
\quad(1\le j<12),
\qquad
n_{12}=e-h+\varepsilon_{12}.
\tag{5.4}
\]

The nonzero residual multipliers force \(\varepsilon_j\ge0\), and summing
the source-fiber sizes gives

\[
\boxed{
\sum_{j=1}^{12}\varepsilon_j=B(h).
}
\tag{5.5}
\]

Moreover,

\[
\deg\widetilde R_j\le\varepsilon_j
\quad(j<12).
\tag{5.6}
\]

For the infinity fiber, monicity says that \(\overline Q_{12}\) carries the
degree-\(D\) leading coefficient. Hence its upper degree bound is attained:

\[
\boxed{
\deg\widetilde R_{12}=\varepsilon_{12}.
}
\tag{5.7}
\]

At the first surviving endpoint,

\[
\boxed{B(118{,}077)\le1.}
\tag{5.8}
\]

Thus eleven residual multipliers are constant and the twelfth has degree
at most one. More precisely, either the infinity-fiber multiplier is
linear and all finite-fiber multipliers are constant, or the unique source
occupancy slack lies at one finite fiber and only that finite multiplier
may be linear.

Thus a packet with all \(69\) records regular is confined to only

\[
118{,}077\le h\le118{,}599
\tag{5.9}
\]

and at least \(1{,}136{,}341\) carrier coordinates already give
minimum-weight \(\operatorname{GRS}_{12}\) words.

Each minimum-weight row has a unique zero set

\[
I_x\in\binom{[R]}{11}.
\tag{5.10}
\]

For a fixed \(I\), all corresponding carrier coordinates are common roots
of every pair of locators indexed by \(I\). The pair-gcd bound therefore
gives

\[
\#\{x:I_x=I\}\le h.
\tag{5.11}
\]

Uniformly at the lower endpoint, the number of distinct realized
minimum-word vertices is at least:

\[
\begin{array}{c|ccccc}
R&65&66&67&68&69\\ \hline
\#\{I_x\}&4&5&7&9&10.
\end{array}
\tag{5.12}
\]

These bounds are rigorous, but they do not yet contradict the packet.

## 6. Sharpened remaining low-excess lemma

The first unresolved case can now be stated without a small-expansion
classification:

> **Selected fixed-domain GRS-vertex lemma, \(a=12\).**
> There is no source-fiber rational curve
> \[
> x\longmapsto
> [\overline Q_1(x):\cdots:\overline Q_{12}(x)]
> \in\mathbf P^{11}
> \]
> satisfying the inherited source divisors, monicity, residual-degree
> budget, and no-persistent-root condition, whose evaluations on the fixed
> KoalaBear carrier produce \(R\in\{65,\ldots,69\}\) monic split locator
> columns, the MDS-deficit ledger (5.2), and the total multiplier-degree
> and slack-allocation constraints (5.3)--(5.7).

Equivalently, prove that the curve cannot meet the minimum-weight vertices
of the \(R\)-point weighted-GRS hyperplane arrangement with the
multiplicities forced by (5.2), while retaining the pair-gcd cap \(h\).

A valid alternative is a canonical already-paid semantic cell rooted at
one of the same regular records.

## 7. What this changes

The low-excess problem is easier in a precise sense:

* the regular locator code is classified exactly, rather than merely
  having dimension at most \(16\);
* the one-step expansion is exactly \(a+1\);
* all incidence slack is concentrated in the explicit nonnegative
  invariant \(\Delta_R\);
* \(R=69\) at \(a=12\) is restricted to a \(523\)-value interval for \(h\);
* the selected carrier curve is forced through hundreds of thousands of
  minimum-weight rows; and
* the all-regular branch has only \(6{,}265\) total post-core multiplier
  degrees, dropping to one at the first endpoint.

It is not yet routine. Arbitrary GRS codes admit all of these weight
patterns. The remaining proof must use the fixed-domain split condition
and the source-fiber divisors of the coefficient curve. A code-only,
first-incidence, or pair-incidence argument cannot finish the case.
