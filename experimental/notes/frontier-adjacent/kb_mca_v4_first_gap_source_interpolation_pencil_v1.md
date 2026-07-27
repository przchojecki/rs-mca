---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: At the first open full-outside slack r=67471, every dangerous x=1 post-source-rational rank-two record has reduced degree 67472, and all such reduced pairs across every rebuilt selector form one pair-global two-dimensional source interpolation pencil whose determinant is a nonzero scalar multiple of the source locator.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1
atom_or_cell: ACTIVE_FULL_OUTSIDE_FIRST_GAP_SOURCE_INTERPOLATION_PENCIL
quantifier: Per received line and fixed translated source, uniformly across every selector rebuilt after the six active owner deletions
projection_and_unit: Reduced polynomial pairs and distinct finite moving-root slopes per received line
claimed_bound: Exact source-kernel dimension two and unique projective map parameter for every off-source root/slope incidence
status: PROVED
impact: SOURCE_CORRELATION_REDUCTION_ONLY
falsifier: A qualifying r=67471, x=1 residual record of reduced degree other than 67472; source interpolation nullity other than two; a cross determinant not proportional to the source locator; or a noninvertible off-source evaluation map.
replay: python3 experimental/scripts/verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1.py --check
---

# KoalaBear first-gap source interpolation pencil

**PROVED SOURCE-BOUND NORMAL FORM / ZERO LEDGER MOVEMENT / DETERMINANT
PACKING OPEN.**

The active full-histogram replay leaves the exact full-outside
coefficient-rank-two interval

\[
67{,}471\le r\le209{,}568.
\]

This note resolves the source interpolation geometry at its first integer.
The point \(r=67{,}471\) is not merely the place where the scalar floor drops
from two to one. It is also the exact boundary of the pair-global
source-rational uniqueness theorem. Every dangerous \(x=1\) record has one
forced reduced degree, and all reduced pairs from all rebuilt selectors lie
in one two-dimensional vector space determined only by the translated
source.

The theorem does not yet bound the determinant-weighted graph-line mass. It
supplies the first pair-global correlation which a proof of that bound may
use.

## 1. Active input and exact endpoint arithmetic

Use the deployed row

\[
n=2{,}097{,}152,\qquad k=1{,}048{,}576,
\qquad A=1{,}116{,}048,
\]

\[
j=n-A=981{,}104,\qquad t=A-k=67{,}472.
\]

Fix one received line, its translated source pair
\((\epsilon _0,\epsilon _1)\), and

\[
\Sigma=\operatorname{supp}(\epsilon _0)
       \cup\operatorname{supp}(\epsilon _1).
\]

Work after the six active source-owner deletions and a complete-selector
restart. Fix a qualifying full-outside, coefficient-rank-two graph-line
record at

\[
r=t-1=67{,}471,\qquad x_L=1.
\tag{1.1}
\]

The source size is

\[
s=|\Sigma|=t+r+1=2t=134{,}944.
\tag{1.2}
\]

Write the polynomial lifts as

\[
P=H\bar P,\qquad Q=H\bar Q,\qquad
\gcd(\bar P,\bar Q)=1,
\]

and put

\[
e=\max\{\deg\bar P,\deg\bar Q\}.
\]

Post-source-rational deletion gives

\[
e\ge E(s)+1
 =\left\lfloor\frac{s-1}{2}\right\rfloor+1
 =67{,}472.
\tag{1.3}
\]

The full-outside source/degree contract gives

\[
e\le s+x_L-t-1=67{,}472.
\tag{1.4}
\]

Therefore

\[
\boxed{e=t=67{,}472,\qquad s=2e.}
\tag{1.5}
\]

There is also no unused common-factor degree. The forced outside-source
common-root set \(C_L\) has size

\[
c=A-x_L-s=981{,}103.
\tag{1.6}
\]

Its monic locator \(L_{C_L}\) divides the full monic gcd \(H\). The degree
contract and (1.5) give

\[
\deg H+e\le k-1,\qquad
\deg H\ge c,\qquad
c+e=k-1.
\]

Hence

\[
\boxed{H=L_{C_L},\qquad\deg H=981{,}103.}
\tag{1.7}
\]

Equations (1.5)--(1.7) are pointwise in every qualifying record. They use no
average over selectors or lines.

## 2. Pair-global interpolation kernel

Let \(F[X]_{\le e}\) denote the polynomials of degree at most \(e\). Define
the source interpolation kernel

\[
\mathcal K_\Sigma(e)=
\left\{
(R,S)\in F[X]_{\le e}^2:
\epsilon _1(h)R(h)-\epsilon _0(h)S(h)=0
\quad(h\in\Sigma)
\right\}.
\tag{2.1}
\]

This space depends only on the fixed translated source and the integer \(e\).
It contains no selector, carrier, graph line, support, basis, or determinant
weight.

At each source point the pair
\((\epsilon _0(h),\epsilon _1(h))\) is nonzero. Thus (2.1) says that
\((R(h),S(h))\) is projectively proportional to the source pair, allowing
the zero vector.

Every qualifying reduced pair \((\bar P,\bar Q)\) belongs to
\(\mathcal K_\Sigma(e)\) by the full-outside source equations.

### Theorem 2.1 (exact source-pencil dimension)

Under (1.1)--(1.5),

\[
\boxed{\dim_F\mathcal K_\Sigma(e)=2.}
\tag{2.2}
\]

Moreover, if \((R_0,S_0),(R_1,S_1)\) is any basis, then

\[
\boxed{
R_0S_1-R_1S_0=c_\Sigma L_\Sigma,
\qquad c_\Sigma\in F^\times,
}
\tag{2.3}
\]

where

\[
L_\Sigma(X)=\prod_{h\in\Sigma}(X-h).
\]

#### Proof

The ambient vector space in (2.1) has dimension

\[
2(e+1)=2e+2=s+2.
\]

There are \(s\) homogeneous source equations, so rank-nullity gives

\[
\dim\mathcal K_\Sigma(e)\ge2.
\tag{2.4}
\]

Fix one actual qualifying coprime reduced pair
\((\bar P,\bar Q)\) of degree \(e\). Suppose
\((R,S)\in\mathcal K_\Sigma(e)\) has degree at most \(e-1\). The cross
determinant

\[
\Delta=R\bar Q-\bar P S
\]

vanishes at every point of \(\Sigma\), because both pairs satisfy the same
projective source equations. Its degree is at most

\[
(e-1)+e=2e-1=s-1.
\]

It has \(s\) distinct roots, so \(\Delta=0\). Since
\(\gcd(\bar P,\bar Q)=1\), there is a polynomial \(T\) with

\[
(R,S)=T(\bar P,\bar Q).
\]

A nonzero \(T\) would make the maximum degree at least \(e\), contrary to
\(\deg(R,S)\le e-1\). Therefore \(R=S=0\).

It follows that the leading-coefficient map

\[
\operatorname{lc}_e:
\mathcal K_\Sigma(e)\longrightarrow F^2,
\qquad
(R,S)\longmapsto([X^e]R,[X^e]S)
\tag{2.5}
\]

is injective. Hence

\[
\dim\mathcal K_\Sigma(e)\le2.
\]

Together with (2.4), this proves (2.2).

Choose the actual pair as the first basis vector and any independent second
vector. Their cross determinant is nonzero: otherwise coprimality and the
degree bound would make the second vector a constant multiple of the first.
The determinant vanishes on all \(s\) source points and has degree at most
\(2e=s\). Therefore it is a nonzero scalar multiple of the monic
degree-\(s\) locator \(L_\Sigma\). A change of basis multiplies the
determinant by a nonzero scalar, proving (2.3) for every basis. \(\square\)

### Corollary 2.2 (selector-independent projective parameter)

Every qualifying reduced pair from every complete selector rebuilt after
the six active deletions determines one point of

\[
\mathbf P(\mathcal K_\Sigma(e))\simeq\mathbf P^1(F).
\tag{2.6}
\]

This projective parameter space is pair-global. A selector may choose
different graph lines and common-root locators, but it cannot choose a
different source interpolation space.

There is no source-interpolation rank-at-least-three branch at this endpoint.
Any proposed rank owner based only on excess nullity of (2.1) is empty under
the printed hypotheses.

## 3. Off-source evaluation is an isomorphism

Fix \(x\in F\setminus\Sigma\). For a basis as in Theorem 2.1, the determinant
of the evaluation matrix

\[
\begin{pmatrix}
R_0(x)&S_0(x)\\
R_1(x)&S_1(x)
\end{pmatrix}
\]

is

\[
c_\Sigma L_\Sigma(x)\ne0.
\]

Therefore evaluation gives an isomorphism

\[
\boxed{
\operatorname{ev}_x:
\mathcal K_\Sigma(e)\longrightarrow F^2.
}
\tag{3.1}
\]

For every finite slope \(\eta\), the equation

\[
R(x)+\eta S(x)=0
\tag{3.2}
\]

cuts one projective point in
\(\mathbf P(\mathcal K_\Sigma(e))\). Thus:

> **Unique root/slope parameter.** For every
> \(x\in D\setminus\Sigma\) and every finite \(\eta\in F\), there is exactly
> one projective source-pencil parameter \([(R,S)]\) satisfying (3.2).

In particular, when a zero-deficit \(x_L=1\) selected slope has its unique
moving root \(x\), the pair \((x,\eta)\) determines the graph line's reduced
source-map parameter. Two records using the same moving root and slope cannot
carry different reduced maps.

This is a correlation absent from the scalar histogram extremizer, where
line blocks and basis blocks may be assigned independently.

### Corollary 3.1 (common-zero set determines the graph line)

Fix one rebuilt selector and its carrier \(V\). Put

\[
C_{\rm out}=D\setminus(V\cup\Sigma).
\]

For a dangerous line \(L\), let \(Z_L\subseteq V\) be its common-zero set.
Since \(W_L=V\setminus Z_L\), \(x_L=1\), and
\(|W_L|=j+1\),

\[
|Z_L|=|V|-j-1.
\tag{3.3}
\]

The exact full gcd from (1.7) is

\[
\boxed{
H_L=L_{C_{\rm out}}L_{Z_L}.
}
\tag{3.4}
\]

At every \(h\in\Sigma\), this locator is nonzero and the source equations
become

\[
\bar P_L(h)=
\frac{\epsilon _0(h)}
     {L_{C_{\rm out}}(h)L_{Z_L}(h)},
\qquad
\bar Q_L(h)=
\frac{\epsilon _1(h)}
     {L_{C_{\rm out}}(h)L_{Z_L}(h)}.
\tag{3.5}
\]

Each right side must be the restriction of a degree-at-most-\(e\)
polynomial on all \(s=2e\) source points. Such a polynomial, if it exists,
is unique because \(s>e\). Thus \(Z_L\) determines
\((\bar P_L,\bar Q_L)\), then \(P_L,Q_L\), then \(a_L,b_L\), and finally the
affine graph line in the fixed \(K_0\) coordinates.

Consequently:

\[
\boxed{
Z_L=Z_{L'}\quad\Longrightarrow\quad L=L'.
}
\tag{3.6}
\]

This gives an exact candidate compiler. A subset

\[
Z\subseteq V,\qquad |Z|=|V|-j-1,
\]

can support a dangerous line only if both quotient vectors in (3.5) lie in
the length-\(s\), dimension-\(e+1\) source evaluation code. Each coordinate
therefore satisfies

\[
s-(e+1)=e-1=67{,}471
\tag{3.7}
\]

overdetermined Reed--Solomon parity conditions. These conditions depend on
the actual split locator \(L_Z\); they are absent from the scalar packing.

## 4. Exact threshold sharpness

The equality \(s=2e\) is load-bearing. If only \(s=2e-1\) source conditions
are imposed, rank-nullity gives a kernel of dimension at least three, and the
conclusion can fail.

An exact control over \(\mathbf F_{17}\) takes

\[
e=2,\qquad
f=X(X-1),\qquad
g=(X-2)(X-3),
\]

\[
\Sigma=\{0,1,2,3\},\qquad
(\epsilon _0,\epsilon _1)=(f,g).
\]

The degree-two interpolation kernel is exactly

\[
\operatorname{span}\{(f,0),(0,g)\},
\]

and its determinant is

\[
fg=L_\Sigma.
\]

For every \(x\notin\Sigma\), the projective map

\[
[u:v]\longmapsto[-u f(x):v g(x)]
\]

is a bijection of \(\mathbf P^1(\mathbf F_{17})\).

If the source set is shortened to \(\{0,1,2\}\), the same degree-two
interpolation kernel has dimension three. This is an exact negative
regression against weakening \(s=2e\) to \(s\ge2e-1\).

## 5. Consequence for the active bridge

At the first open slack, the missing determinant theorem may now assume:

```text
r=67,471
x_L=1 on every dangerous line
reduced degree e=67,472
full gcd H equals the forced split locator
one pair-global two-dimensional source interpolation pencil
cross determinant exactly c*L_Sigma
off-source evaluation is invertible
moving root + slope determines the reduced-map parameter
common-zero set Z_L determines the complete graph line
each Z_L satisfies 67,471 source RS parity conditions per coordinate
```

The remaining task is no longer to synchronize arbitrary high-degree source
maps. It is to combine this fixed source pencil with:

```text
the affine graph-line parameters in K_0
the eight actual outlier directions
the regular split-locator equations
the determinant weights beta_L
the complete-selector coverage condition
```

and prove either:

1. the determinant-weighted rich-line mass fits the active reserve; or
2. a degeneration emits a same-slope active owner and forces a selector
   restart.

The natural next lemma is:

> **First-gap graph-line/source-pencil incidence.** In one complete selector
> at \(r=67{,}471\), bind every dangerous graph line to its point of
> \(\mathbf P(\mathcal K_\Sigma(e))\) and to its unique split-locator
> candidate \(Z_L\). Use the two quotient-interpolation tests, the unique
> root/slope parameter, and the eight-outlier determinant equations to prove
> a budget-fitting bound for
>
> \[
> \sum_{L:J_L\ge21}\beta_L(J_L-20),
> \]
>
> or emit a same-slope quotient, planted, field, collective-rank,
> saturation, twist, or Frobenius owner.

## 6. Scope and nonclaims

This packet proves a source-bound normal form. It does not:

* bound the determinant-weighted graph-line sum;
* prove complete-selector coverage or existence;
* pay any additional slopes;
* treat \(r>67{,}471\), \(x_L>1\), non-full-outside source load, Q,
  balanced core, or the final complement;
* infer that two graph lines with the same reduced map have the same common
  factor or determinant bases;
* replace the required same-selector provenance by pair-global source data;
* close KoalaBear.

The active ledger and partition digest are unchanged.

# PROVED
