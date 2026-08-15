# Rank-one minimizing-pair anticode router

## Statement

Let `C'=span(P_1,...,P_s)` be a subspace of the degree-`<K`
Reed--Solomon code, with `s<=10`. After the usual affine gauge, write every
actual minimizing pair as

\[
 a_e=a_*+\sum_{j=1}^s A_{e,j}P_j,\qquad
 b_e=b_*+\sum_{j=1}^s B_{e,j}P_j
\]

and set

\[
 M_e=\begin{pmatrix}A_e\\ B_e\end{pmatrix}\in\mathbb F^{2\times s}.
\]

Let

\[
 H_e=\{x:r_0(x)=a_e(x),\ r_1(x)=b_e(x)\}
\]

be its complete pair core.

### Theorem 1 (rank-one anticode classification)

If

\[
 \operatorname{rank}(M_e-M_f)\le1
 \qquad(e,f\in\mathcal E),
\]

then, after choosing one base pair `e_0`, one of the following descriptions
holds (a one-dimensional family may satisfy both).

**Fixed right factor.** There is a nonzero `v in F^s` and vectors
`u_e=(alpha_e,beta_e) in F^2` such that

\[
 M_e=M_{e_0}+u_ev^T.
\]

**Fixed left factor.** There is a nonzero `u=(alpha,beta) in F^2` and
vectors `v_e in F^s` such that

\[
 M_e=M_{e_0}+uv_e^T.
\]

#### Proof

Translate so that `M_{e_0}=0` and choose one nonzero member
`M_1=uv^T`. Every other nonzero member is `xy^T`. The condition
`rank(xy^T-uv^T)<=1` implies either `x` is proportional to `u` or `y` is
proportional to `v`: if both pairs were independent, the difference would
have rank two.

If one member uses the first alternative strictly and another uses the
second strictly, their difference again has rank two. Hence all nonzero
members share the same left factor, or all share the same right factor.
Members proportional to `uv^T` belong to both descriptions. Translating
back proves the claim. This is the elementary maximal-clique classification
for the rank-one bilinear-forms graph.

### Theorem 2 (maximal pair-core overlap enters Theorem 1)

For distinct pair types,

\[
 |H_e\cap H_f|=K-1
 \quad\Longrightarrow\quad
 \operatorname{rank}(M_e-M_f)=1.
\]

Consequently, any family with pairwise core intersection `K-1` is a
rank-one anticode and has one of the two forms above.

#### Proof

Every point of \(H_e\cap H_f\) is a common zero of the two degree-`<K`
polynomials `a_e-a_f` and `b_e-b_f`. If their coefficient rows were
independent, their gcd would have degree at most `K-2`, so they could have
at most `K-2` common roots. Rank zero would make the pair types equal.
The only remaining rank is one.

## Owner projection

For a selected slope `gamma` assigned to pair `e`, its explanation is

\[
 h_{e,\gamma}=a_e+\gamma b_e.
\]

### Fixed-right-factor branch: common-core-aware affine ray

Put `P=sum_j v_jP_j` and
`H_0(X,gamma)=a_{e_0}(X)+gamma b_{e_0}(X)`. Then

\[
 h_{e,\gamma}
 =H_0(X,\gamma)+(\alpha_e+\gamma\beta_e)P(X).
\]

The parent complete-ray theorem cannot be imported blindly here: its local
spread-core context excludes identically zero coordinate-error
polynomials, whereas the base minimizing pair may have a universal core.
The following direct affine-degree-one count retains that core.

Let

\[
 E_x(\gamma)=r_0(x)+\gamma r_1(x)-H_0(x,\gamma)
\]

and define

\[
 U=\{x:P(x)=0,\ E_x(\gamma)\equiv0\},\qquad u=|U|.
\]

Since \(P\ne0\) has degree `<K`, \(0\le u\le K-1\). Remove \(U\) from
every selected agreement support and put

\[
 n_u=n-u,\qquad m_u=m-u,\qquad
 q_u=\min\{K-1,m_u-1\}.
\]

For \(P(x)\ne0\), the affine function \(E_x/P(x)\) defines a clone class.
A clone class of size at least \(m_u\), together with \(U\), would give a
global affine codeword pair agreeing with the received pair on at least
\(m\) coordinates, contrary to the post-near pair-noncontainment
hypothesis.

When \(m_u>K-1\), remove every clone class of size at least \(K\). There
are at most

\[
 L_u=\left\lfloor\frac{n_u}{K}\right\rfloor
\]

such classes, and each associated global affine codeword line owns at most
\(n-m+1\) slopes. When \(m_u\le K-1\), put \(L_u=0\); all clone classes
already have size at most \(m_u-1=q_u\).

Coordinates with \(P(x)=0\) outside \(U\) have a nonzero affine error and
therefore one root slope. At any selected slope they form one additional
part of size at most \(K-1-u\le q_u\). Thus, after the large clone classes
are removed, the \(m_u\) nonuniversal coordinates of a selected exact
support split into parts of size at most \(q_u\). Since \(m_u\le2q_u\),
the number of unordered pairs drawn from different parts is at least

\[
 q_u(m_u-q_u).
\]

A pair from two different graph clone classes determines at most one slope,
because two distinct affine functions agree at most once. A vertical/graph
pair also determines at most one slope. Double counting gives

\[
 R(u)=L_u(n-m+1)+
 \left\lfloor
 \frac{\binom{n-u}{2}}{q_u(m-u-q_u)}
 \right\rfloor .
\]

The exact integer scan over \(0\le u\le K-1\) gives

\[
 \max_u R(u)=R(K-1)=8\,147\,918.
\]

The endpoint has
\(m_{K-1}=67473\), \(q_{K-1}=67472\), and \(L_{K-1}=0\).
Therefore the entire fixed-right-factor anticode owns at most
\(8\,147\,918\) distinct selected slopes.

### Fixed-left-factor branch: one affine correction space

Put `P_e=sum_j(v_e)_jP_j` and
`W=span{P_e:e in E}`, of dimension `r<=s<=10`. Then

\[
 h_{e,\gamma}
 =H_0(X,\gamma)+(\alpha+\gamma\beta)P_e(X)
 \in H_0(X,\gamma)+W.
\]

Use the actual correction
`Q_{e,gamma}=(alpha+gamma beta)P_e in W` as parameter. Relative to a basis
`Q_1,...,Q_r` of `W`, every coordinate agreement equation is affine linear
in the `r+1` variables `(gamma,c_1,...,c_r)`:

\[
 F_x(\gamma,\mathbf c)
 =r_0(x)+\gamma r_1(x)-H_0(x,\gamma)
  -\sum_{j=1}^r c_jQ_j(x)=0.
\]

Call the arrangement **proper** when every `r+1` coordinate hyperplanes
have empty intersection or a single affine point. If it is proper, double
counting pairs `(selected point,J)`, where `J` is an `(r+1)`-subset of its
agreement support, gives

\[
 |Z|\binom m{r+1}\le\binom n{r+1}.
\]

For the KoalaBear row the right quotient is increasing for `0<=r<=10` and

\[
 |Z|\le
 \left\lfloor\frac{\binom n{11}}{\binom m{11}}\right\rfloor
 =1031.
\]

If properness fails, one obtains an explicit `(r+1)`-tuple of coordinates
whose affine agreement hyperplanes have a nonempty positive-dimensional
intersection. This is a degree-one, dimension-at-most-ten correction
component, not an untyped pair-core terminal.

The factor `alpha+gamma beta` may vanish at one slope. At that slope all
pair labels map to the single correction parameter `Q=0`; because slopes
are counted once, injectivity at the record level is unchanged.

## Exact KoalaBear arithmetic

\[
\begin{aligned}
n&=2097152,&K&=1048576,&m&=1116048,\\
B_*&=274980728111395087.
\end{aligned}
\]

The two paid branch caps are

\[
8\,147\,918<B_*,\qquad 1031<B_*.
\]

Their respective slacks are

\[
274980728103247169,\qquad
274980728111394056.
\]

## What this proves and does not prove

It proves a source-level cross-pair compatibility router. In particular,
pairwise maximal-overlap cliques are reduced to named correction
geometries, and the affine-ray branch is paid without assuming away the
base pair's universal core.

It does not prove that the full rank-eleven pair collection contains one
large rank-one anticode, and it does not authorize summing the displayed
caps over unrelated anticodes. The unresolved aggregate branch contains
rank-two pair differences or the emitted positive-dimensional linear
correction component.
