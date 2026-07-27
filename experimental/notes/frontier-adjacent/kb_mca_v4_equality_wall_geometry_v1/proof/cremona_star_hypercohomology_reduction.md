# Cremona-Star Hypercohomology Reduction for PRCI

## 1. Status

This note gives two exact reformulations of postcritical
reciprocal-Cauchy interpolation:

1. a one-step critical-kernel criterion; and
2. a hypercohomology vanishing on the permutohedral resolution of standard
   Cremona.

Neither reformulation proves the KoalaBear specialization. The original
all-fields theorem is false: exact \(a=4,R=8\) failures occur in
characteristics \(13,17,19,23\). In another exact configuration,
one fixed maximal minor and every coordinate permutation of that minor
vanish even though the full postcritical evaluation matrix has full row
rank. Every known rank failure is supported on coincident block lines and
emits an exact planted split-pencil identity. These facts replace the search
for one universal minor by a structured exactness or semantic-exception
problem.

Throughout, put

\[
n=a-1,\qquad d=R-n=R-a+1,
\]

and assume

\[
R\ge 2a-2,
\qquad\text{equivalently}\qquad d\ge n.
\]

Let

\[
X=X_{R,n}\subset\mathbf P^n_x
\]

be the codimension-\(n\) star configuration cut out by the \(R\) source
hyperplanes, and let

\[
Y=\operatorname{Cr}(X)\subset\mathbf P^n_y
\]

be its coordinatewise reciprocal image. Source/parameter disjointness puts
every point of \(X\) in the dense torus, so standard Cremona is defined and
invertible at every point of \(X\). The set \(Y\) is the complementary
Hadamard-product configuration \(\mathcal Y_{R,a}\) in the PRCI target.

Its cardinality is

\[
N=|X|=|Y|=\binom Rn.
\]

## 2. Critical-kernel formulation

For \(r\ge0\), let

\[
\operatorname{ev}_r:
H^0(\mathbf P^n_y,\mathcal O(r))\longrightarrow F^Y
\]

be evaluation on \(Y\). Define

\[
C_r=\operatorname{im}(\operatorname{ev}_r),
\qquad
K_r=C_r^\perp\subseteq F^Y
\]

under the standard coordinate pairing. Thus

\[
\dim K_r=N-H_Y(r).
\]

For the \(j\)-th homogeneous coordinate on \(\mathbf P^n_y\), write

\[
D_j=\operatorname{diag}\bigl(y_j(P):P\in Y\bigr).
\]

Every entry of every \(D_j\) is nonzero because \(Y\) lies in the torus.

### Proposition 2.1: one-step kernel identity

For every \(r\ge0\),

\[
\boxed{
K_{r+1}
=
\bigcap_{j=0}^n D_j^{-1}K_r.
}
\tag{2.1}
\]

Equivalently,

\[
\lambda\in K_{r+1}
\quad\Longleftrightarrow\quad
D_j\lambda\in K_r
\quad(0\le j\le n).
\tag{2.2}
\]

### Proof

The degree-\((r+1)\) forms are spanned by the products \(y_jM\), where
\(M\) ranges over degree-\(r\) monomials. Therefore

\[
\lambda\in K_{r+1}
\]

if and only if

\[
\sum_{P\in Y}\lambda_Py_j(P)M(P)=0
\]

for every \(j\) and every \(M\). This is exactly the condition

\[
D_j\lambda\in K_r
\]

for every \(j\). \(\square\)

### Corollary 2.2: exact postcritical kernel target

For each fixed configuration, postcritical surjectivity is equivalent to

\[
\boxed{
\bigcap_{j=0}^nD_j^{-1}K_d=\{0\}.
}
\tag{2.3}
\]

Thus the critical defect is allowed. The theorem says that no critical
relation survives simultaneous multiplication by all \(a=n+1\) coordinate
functions.

This explains the observed finite profiles: degree \(d\) can have a
nonzero relation space, while degree \(d+1\) is already full.

## 3. A support obstruction for a surviving relation

Let \(\lambda\in K_k\setminus\{0\}\), and let

\[
S=\operatorname{supp}\lambda\subseteq Y.
\]

For \(0\le r\le k\), multiplication by all degree-\(r\) monomials gives

\[
\operatorname{diag}(M|_S)\lambda\in K_{k-r}.
\]

Because every coordinate of \(\lambda|_S\) is nonzero, diagonal
multiplication by \(\lambda|_S\) is an isomorphism of \(F^S\). The span of
these vectors consequently has dimension \(H_S(r)\). Hence:

### Proposition 3.1: Hilbert support inequality

Every nonzero \(\lambda\in K_k\) satisfies

\[
\boxed{
H_S(r)\le \dim K_{k-r}=N-H_Y(k-r)
\qquad(0\le r\le k).
}
\tag{3.1}
\]

For a hypothetical postcritical failure, \(k=d+1\), so in particular

\[
H_S(1)\le N-H_Y(d).
\tag{3.2}
\]

Therefore the support of every surviving postcritical relation lies in a
projective subspace whose dimension is bounded by the critical defect minus
one. A proof of PRCI can close through either of the following:

* compute or bound the critical defect and prove that no sufficiently large
  subset of \(Y\) lies in such a small subspace; or
* combine (3.1) for several \(r\) with the star-configuration incidence
  structure until no support Hilbert function is possible.

This is stronger than selecting one maximal minor: it constrains every
possible relation and adapts automatically to configurations where the
preferred minor degenerates.

## 4. The original star-configuration resolution

The ideal of the codimension-\(n\) star configuration \(X\) has the standard
linear resolution

\[
0\longrightarrow F_n\longrightarrow\cdots
\longrightarrow F_2\longrightarrow F_1
\longrightarrow I_X\longrightarrow0,
\tag{4.1}
\]

where

\[
F_i=
\mathcal O_{\mathbf P^n_x}(-(d+i))^{\beta_i},
\qquad
1\le i\le n,
\tag{4.2}
\]

and

\[
\boxed{
\beta_i=
\binom R{n-i}
\binom{R-n+i-1}{i-1}.
}
\tag{4.3}
\]

For example, when \(n=2\), this is

\[
0\longrightarrow
\mathcal O(-R)^{R-1}
\longrightarrow
\mathcal O(-(R-1))^R
\longrightarrow I_X\longrightarrow0.
\]

The shifts begin at \(d+1\), which is the critical interpolation threshold
for the original star configuration.

## 5. Pullback to the Cremona resolution

Let \(Z=\operatorname{Perm}_n\) be the permutohedral toric variety resolving
standard Cremona, with birational toric morphisms

\[
\begin{array}{ccc}
&Z&\\[-1mm]
p\swarrow&&\searrow q\\[-1mm]
\mathbf P^n_x&&\mathbf P^n_y.
\end{array}
\tag{5.1}
\]

Let \(\widetilde X=p^{-1}(X)\). Since \(X\) lies in the torus:

* \(p\) is an isomorphism on a neighborhood of \(X\);
* \(\widetilde X\cong X\);
* \(q|_{\widetilde X}\) identifies \(\widetilde X\) with \(Y\).

Pulling (4.1) back by \(p\) remains exact. Indeed, away from \(X\), the
stalk of \(I_X\) is the free rank-one module, while over \(X\), the map
\(p\) is an isomorphism. Thus all pullback Tor sheaves vanish, and

\[
0\longrightarrow p^*F_n\longrightarrow\cdots
\longrightarrow p^*F_1
\longrightarrow I_{\widetilde X}\longrightarrow0
\tag{5.2}
\]

is a locally free resolution.

Put

\[
L=q^*\mathcal O_{\mathbf P^n_y}(d+1).
\tag{5.3}
\]

After twisting (5.2), define the explicit complex

\[
\mathcal C^{-i+1}
=
q^*\mathcal O(d+1)
\otimes
p^*\mathcal O(-(d+i))^{\beta_i},
\qquad 1\le i\le n,
\tag{5.4}
\]

with \(\mathcal C^0\) in homological degree zero. This complex is
quasi-isomorphic to \(I_{\widetilde X}\otimes L\).

## 6. Exact hypercohomology target

Because \(L\) is nef on the smooth complete toric variety \(Z\), toric
vanishing gives

\[
H^j(Z,L)=0
\qquad(j>0).
\tag{6.1}
\]

The restriction sequence

\[
0\longrightarrow I_{\widetilde X}\otimes L
\longrightarrow L
\longrightarrow L|_{\widetilde X}
\longrightarrow0
\tag{6.2}
\]

therefore shows that degree-\((d+1)\) evaluation on \(Y\) is surjective if
and only if

\[
H^1(Z,I_{\widetilde X}\otimes L)=0.
\tag{6.3}
\]

Using (5.4), this is:

> **Cremona-star hypercohomology vanishing, CSHV.**
> For a fixed source-disjoint \(R\)-hyperplane star configuration with
> \(d\ge n\),
> \[
> \boxed{
> \mathbb H^1(Z,\mathcal C^\bullet)=0.
> }
> \tag{6.4}
> \]

### Theorem 6.1: configuration-wise equivalence

\[
\boxed{
\text{postcritical surjectivity for }Y
\iff
\mathrm{CSHV}\text{ for }\widetilde X.
}
\tag{6.5}
\]

This equivalence is exact for every source and selected parameter choice.
The universal quantification is false in characteristic \(13\). The open
KoalaBear target is CSHV for the actual field and the ranges
\(12\le a\le16\), \(53+a\le R\le69\), or a same-record semantic owner for
every failure.

## 7. Why termwise vanishing is not the target

The individual bundles

\[
q^*\mathcal O(d+1)\otimes p^*\mathcal O(-(d+i))
\tag{7.1}
\]

need not have vanishing higher cohomology. Even in dimension two, mixed
positive/negative pullbacks on the blowup model can carry large higher
cohomology.

Therefore it is generally false that CSHV follows by proving each row of
the hypercohomology spectral sequence zero. The load-bearing statement is
the exactness of the maps induced by the pulled-back star-resolution
differentials between these toric cohomology spaces.

This isolates a finite, structured calculation:

1. compute the toric cohomology of the bundles (7.1);
2. describe the maps induced by the star-resolution differential;
3. prove exactness in total degree one.

The line bundles and their cohomology depend only on \((n,d)\). The
differentials carry the source hyperplane parameters. A universal proof
must establish exactness for every source-disjoint member of that
one-parameter hyperplane pencil, or classify a rank-drop specialization as
an enabled same-record semantic owner.

## 8. Fixed-minor route cut

Finite exact calculations show two distinct guardrails:

* Over \(\mathbf F_{11}\) at \((a,R)=(3,6)\), a maximal postcritical minor
  selected from one configuration and every coordinate permutation of that
  minor can vanish on another source-disjoint configuration, while the
  complete matrix still has full row rank.
* Over \(\mathbf F_{13}\) at \((a,R)=(4,8)\), there are genuine
  postcritical rank drops. Affine-normalized exhaustion finds 21 exceptional
  partitions among 495, corresponding to 273 among all 6,435 partitions.
  Every defect is accounted for by coincident complementary block lines.
* Exact defect-one examples in characteristics \(17,19,23\) have the same
  block-line structure.

The exact line-coincidence criterion is

\[
P_B-cP_C=(1-c)A_\Sigma.
\tag{8.1}
\]

It is a canonical bounded split-pencil planted precursor; see
`reciprocal_cauchy_block_line_emission.md`.

Thus a proof based on one canonical maximal minor, or only its coordinate
orbit, is insufficient. A KoalaBear proof must use an adaptive minor cover,
prove that the common zero locus is absent in the actual characteristic and
range, or route that locus through a same-record semantic owner.

The kernel identity (2.3) and CSHV (6.4) encode that common-radical problem
without selecting a minor.

## 9. Focused proof routes

### 9.1 Critical relation support

Compute \(N-H_Y(d)\), then use (3.1) and the complementary-product
incidences to rule out a support with the required Hilbert function. The
characteristic-\(13\) examples describe exactly what this argument must
allow or classify. This is the most elementary route if the critical
defect has a manageable closed formula.

### 9.2 Toric hypercohomology

Use a torus-equivariant Cech or polyhedral model for the line-bundle
cohomology in (7.1). The star differential is linear in the source
hyperplane coefficients. The desired statement is exactness of one finite
complex in total degree one.

### 9.3 Induction through the star resolution

Delete the last hyperplane and use the standard basic-double-link recursion
for star configurations. Track its pullback through Cremona and prove that
the postcritical obstruction group maps injectively into a lower
\((R,a)\)-group that vanishes at the threshold \(d=n\).

### 9.4 Common-radical plus semantic exception

Prove generic exactness by one nonzero determinant, then analyze the common
radical of all maximal minors. Any exceptional source relation must be
converted into a quotient, planted, field, rank, or saturation owner at the
same selected record. The fixed-minor route cut shows why one determinant
factorization alone is not enough.

## 10. KoalaBear consequence and boundary

For \(a=12,R=69\), KPRCI is degree-\(59\) surjectivity and gives
degree-\(60\) separation. Combined with the existing Cremona curve ledger,
it eliminates

\[
118{,}077\le h\le118{,}283.
\]

The endpoint contradiction margin is \(124{,}201\).

Neither the critical-kernel identity nor the CSHV reformulation books this
conditional
payoff. The remaining proof obligation is exactly one of:

\[
\bigcap_{j=0}^{11}D_j^{-1}K_{58}=\{0\},
\]

or equivalently

\[
\mathbb H^1(Z,\mathcal C^\bullet)=0
\]

for the corresponding \(n=11,d=58\) Cremona-star complex, uniformly over
the source-disjoint parameters.

Universal PRCI is false. KPRCI, the low-excess cap \(68\), the
general-excess descent, and the equality-wall payment remain open.
