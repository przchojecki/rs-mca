# Postcritical Reciprocal-Cauchy Interpolation Target

## 1. Status

This is a weaker and more approachable successor to reciprocal-Cauchy
separation. Its original all-fields formulation is false. The corrected
KoalaBear specialization is not proved here.

The stronger degree-\((R-a+1)\) unisolvence statement is false. Asking that
the Hilbert function reach the full point count one degree later is also not
universal: there are exact characteristic-\(13\) counterexamples at
\((a,R)=(4,8)\), despite

\[
R\ge2a-2.
\]

The same integer configuration has full postcritical rank in
characteristics \(17\) and \(1{,}000{,}003\), but different exact
counterexamples occur in characteristics \(17,19,23\). The surviving useful
target is therefore a semantic-or-interpolation theorem that routes every
rank-deficient exception to a same-record owner. Pure KoalaBear-field
surjectivity remains a stronger optional target.

## 2. Hadamard-product model

Put

\[
n=a-1,\qquad d=R-n=R-a+1.
\]

For distinct source values \(\alpha_j\) and selected parameters \(t_i\),
define the line points

\[
u_i=
[\alpha_1-t_i:\cdots:\alpha_a-t_i]
\in\mathbf P^n.
\tag{2.1}
\]

The original Cauchy star vertices are fixed diagonal scalings of the
square-free \(n\)-fold Hadamard products

\[
\prod_{i\in I}^{\star}u_i,
\qquad |I|=n.
\]

This is the standard Hadamard construction of a codimension-\(n\) star
configuration from collinear points. See Bocci--Carlini--Kileel,
*Hadamard Products of Linear Spaces*, Theorem 4.7.

Let

\[
U_*=\prod_{i=1}^R{}^\star u_i.
\]

The Cremona-transformed vertices are

\[
y_I
=
U_*\star
\left(\prod_{i\in I}^{\star}u_i\right)^{\star(-1)}
=
\prod_{i\notin I}^{\star}u_i.
\tag{2.2}
\]

Thus

\[
\mathcal Y_{R,a}
=
\left\{
\prod_{i\in C}^{\star}u_i:
C\in\binom{[R]}d
\right\}
\subseteq\mathbf P^n.
\tag{2.3}
\]

This is the square-free complementary Hadamard power of the same line
points.

## 3. Corrected target theorem

> **Universal postcritical reciprocal-Cauchy interpolation, UPRCI
> (false).**
> Assume
> \[
> R\ge2a-2.
> \]
> For every distinct, source-disjoint choice of \(\alpha_j,t_i\), the
> evaluation map
> \[
> H^0\left(
> \mathbf P^{a-1},
> \mathcal O(R-a+2)
> \right)
> \longrightarrow
> F^{\mathcal Y_{R,a}}
> \tag{3.1}
> \]
> is surjective.

Equivalently, UPRCI would assert

\[
H_{\mathcal Y_{R,a}}(R-a+2)
=
\binom R{a-1}.
\tag{3.2}
\]

Section 7 gives an exact counterexample, so (3.1) is not a theorem with an
all-fields, all-configurations quantifier.

> **KoalaBear postcritical reciprocal-Cauchy interpolation, KPRCI.**
> Over the actual KoalaBear coefficient field, every source-disjoint
> reciprocal-Cauchy configuration arising in the normalized equality-wall
> packet, with
> \[
> 12\le a\le16,\qquad 53+a\le R\le69,
> \tag{3.3}
> \]
> has
> \[
> H_{\mathcal Y_{R,a}}(R-a+2)=\binom R{a-1}.
> \tag{3.4}
> \]

The preferred compiler-compatible target is:

> **Selected-record postcritical semantic-or-interpolation, SPSI.** Either
> (3.4) holds, or the
> same rank-deficient configuration emits an enabled quotient, planted,
> proper-field, baseline-free rank, or saturation owner at one of the same
> selected records, with its printed payment.

Either corrected statement is sufficient for the downstream use. SPSI is
strictly more realistic: the known counterexamples all factor through an
exact planted split-pencil identity.

## 4. Postcritical surjectivity gives one-degree-later separation

Let

\[
k=R-a+2.
\]

Assume postcritical surjectivity for the configuration under consideration
and fix \(v\notin\mathcal Y_{R,a}\). Choose a linear form
\(L\) nonzero at \(v\) and at every reciprocal-Cauchy vertex.

Surjectivity gives degree-\(k\) sections \(S_y\), one for each vertex, with

\[
S_y(y')=
\begin{cases}
L(y)^k,&y'=y,\\
0,&y'\ne y.
\end{cases}
\]

Put

\[
T=L^k-\sum_yS_y.
\]

The section \(T\) vanishes on the complete vertex set. If \(T(v)\ne0\),
it already separates \(v\) in degree \(k\). If \(T(v)=0\), then some
\(S_y(v)\ne0\). Choose a linear form \(\ell_y\) satisfying

\[
\ell_y(y)=0,\qquad \ell_y(v)\ne0.
\]

Then

\[
\ell_yS_y
\]

vanishes on every vertex and is nonzero at \(v\). Therefore:

\[
\boxed{
\operatorname{Bs}
I(\mathcal Y_{R,a})_{R-a+3}
=
\mathcal Y_{R,a}.
}
\tag{4.1}
\]

This proof is elementary and does not use the false critical-degree
unisolvence assertion.

## 5. Curve consequence

Let

\[
\Psi:\mathbf P^1\longrightarrow\mathbf P^{a-1}
\]

be the nonconstant source-partition Cremona curve, of degree at most
\(E_\Psi\). If \(N_{\min}\) distinct carrier points map into
\(\mathcal Y_{R,a}\), choose any image point outside this finite
configuration and apply (4.1). Pullback gives a nonzero section of degree
at most \((R-a+3)E_\Psi\), so

\[
\boxed{
N_{\min}\le(R-a+3)E_\Psi.
}
\tag{5.1}
\]

## 6. Exact KoalaBear payoff

For

\[
a=12,\qquad R=69,
\]

the exact ledgers give

\[
N_{\min}(h)
\ge
59(67{,}472+h)-10(981{,}105)
\tag{6.1}
\]

and

\[
E_\Psi(h)
\le
11h-1{,}281{,}978.
\tag{6.2}
\]

KPRCI and (5.1) would require

\[
N_{\min}(h)\le60E_\Psi(h).
\]

The contradiction margin is

\[
\boxed{
N_{\min}(h)-60E_\Psi(h)
\ge
71{,}088{,}478-601h.
}
\tag{6.3}
\]

This is positive exactly through

\[
\boxed{h\le118{,}283.}
\tag{6.4}
\]

At \(h=118{,}077\),

\[
1{,}136{,}341-60(16{,}869)
=
\boxed{124{,}201}.
\tag{6.5}
\]

Thus KPRCI would eliminate \(207\) values:

\[
118{,}077\le h\le118{,}283.
\]

The remaining all-regular interval would be

\[
118{,}284\le h\le118{,}599.
\]

## 7. Exact finite evidence

The deterministic regression computes the complete Hilbert function in
small generic models over \(\mathbf F_{1{,}000{,}003}\). Representative
sequences are:

\[
\begin{array}{c|c|l}
(a,R)&|\mathcal Y|&
H(0),H(1),\ldots\\ \hline
(3,6)&15&1,3,6,10,14,15\\
(4,8)&56&1,4,10,20,35,54,56\\
(4,9)&84&1,4,10,20,35,55,77,84\\
(5,10)&210&1,5,15,35,70,126,207,210\\
(5,11)&330&1,5,15,35,70,126,208,310,330.
\end{array}
\]

In each row the Hilbert function reaches the full point count by degree

\[
d+1=R-a+2,
\]

while it can be deficient at degree \(d\).

The threshold hypothesis is meaningful. For \((a,R)=(5,6)\), where
\(R<2a-2\), the degree-\((d+1)\) evaluation still has defect \(5\).

An independent exhaustive regression checks every finite affine
source/parameter partition in the following first threshold cases:

\[
\begin{array}{c|c|c|r}
F&a&R&|\mathcal Y|&
\text{configurations checked}\\ \hline
\mathbf F_7&3&4&6&35\\
\mathbf F_{11}&3&5&10&9{,}240\\
\mathbf F_{11}&4&6&20&2{,}310\\
\mathbf F_{11}&4&7&35&330\\
\mathbf F_{13}&5&8&70&1{,}287.
\end{array}
\]

All \(13{,}202\) configurations have full row rank in degree
\(R-a+2\). This is evidence for the universal quantifier, rather than
only for a generic determinant. It remains finite evidence and does not
prove the KoalaBear cases.

### Characteristic-\(13\) guardrail

The next threshold case supplies a counterexample to UPRCI. Over
\(\mathbf F_{13}\), take

\[
(\alpha_1,\ldots,\alpha_4)=(0,1,2,5)
\]

and

\[
(t_1,\ldots,t_8)=(3,4,6,7,8,9,11,12).
\]

The degree-\(6\) evaluation matrix has

\[
\operatorname{rank}=55<56=\binom83.
\]

The failure is structured. Since the four sources and eight selected values
leave one field element unused, translation normalizes that element to
zero. Exhaustion of the resulting \(495\) normalized partitions finds:

\[
\begin{array}{c|c}
\text{postcritical rank}&\text{normalized configurations}\\ \hline
54&3\\
55&18.
\end{array}
\]

Translation therefore gives \(273\) exceptional configurations among all
\(6{,}435\), comprising \(39\) rank-\(54\) and \(234\) rank-\(55\)
configurations.

The identical integer source/selected sets have rank \(56\) in
characteristics \(17\) and \(1{,}000{,}003\). Different exact defect-one
examples occur in characteristics \(17,19,23\), so the exceptional locus is
not confined to characteristic \(13\).

Every known exception has a canonical explanation. For a selected
\(a\)-block \(B\), its \(a\) vertices lie on an explicit line \(L_B\).
Two block lines coincide exactly when

\[
P_B-cP_C=(1-c)A_\Sigma.
\tag{7.1}
\]

In the complete \(\mathbf F_{13}\) census, the entire postcritical relation
space is generated by the relation spaces of coincident block lines. In
particular, the global defect and the block-line-generated dimension agree
in every one of the 495 normalized configurations:

\[
(0,0):474,\qquad(1,1):18,\qquad(2,2):3.
\]

Thus all 273 characteristic-\(13\) failures, and the printed
characteristic-\(17,19,23\) failures, emit an exact bounded split-pencil
planted precursor. See
`reciprocal_cauchy_block_line_emission.md`.

The same quotient-space computation is exact in two higher-dimensional
planted regressions:

\[
\begin{array}{c|c|c|c|c}
F&a&R&\dim K_{\rm global}&\dim K_{\rm block}\\ \hline
\mathbf F_{17}&5&10&2&2\\
\mathbf F_{17}&4&12&1&1.
\end{array}
\]

No known relation survives after quotienting by the block-line relation
spaces.

The first exact small-field case in which canonical-line capacity is
strictly below the relation threshold is

\[
\mathbf F_{13},\qquad(a,R)=(4,9).
\]

Here a canonical line has at most eight selected vertices, while a
postcritical line relation requires nine. Exhaustion of all
\(\binom{13}{4}=715\) source/selected partitions gives full rank \(84\)
in every case. This is finite evidence for the noncanonical-line branch,
not a proof in the KoalaBear range.

The replay commands are

```text
python verify_postcritical_reciprocal_cauchy_interpolation.py \
  --emit --check --tamper-selftest
python search_postcritical_interpolation_counterexamples.py \
  --emit --check --tamper-selftest
python verify_postcritical_characteristic13_guardrail.py \
  --emit --check --tamper-selftest
python verify_postcritical_block_line_relation_space.py \
  --emit --check --tamper-selftest
python verify_cremona_star_hypercohomology_reduction.py \
  --emit --check --tamper-selftest
```

## 8. Equivalent algebraic core

For a composition \(\boldsymbol m=(m_1,\ldots,m_a)\) of \(d+1\), put

\[
w_{\boldsymbol m}(t)
=
\prod_{j=1}^a(\alpha_j-t)^{m_j}.
\tag{8.1}
\]

The evaluation matrix in (3.1), after harmless row and column scalings,
is

\[
\mathsf M_{C,\boldsymbol m}
=
\prod_{r\in C}w_{\boldsymbol m}(t_r),
\qquad
C\in\binom{[R]}d.
\tag{8.2}
\]

Thus postcritical surjectivity is exactly the assertion that the vectors

\[
\left(
\prod_{r\in C}w_{\boldsymbol m}(t_r)
\right)_{\boldsymbol m}
\]

are linearly independent as \(C\) ranges over the \(d\)-subsets. The
characteristic-\(13\) guardrail proves that the determinant-zero locus is
nonempty in general. A proof of KPRCI must use the actual field/range, or
classify every relevant exception semantically.

## 9. Proof strategies

### 9.1 Complement-product evaluation matrix

Let \(\boldsymbol m=(m_1,\ldots,m_a)\), with

\[
\sum_jm_j=d+1.
\]

For a complement \(C\in\binom{[R]}d\), the matrix entry is

\[
\prod_{j=1}^a
\left(
\prod_{r\in C}(\alpha_j-t_r)
\right)^{m_j}
=
\prod_{r\in C}
\left(
\prod_{j=1}^a(\alpha_j-t_r)^{m_j}
\right).
\tag{9.1}
\]

The theorem asks for full row rank of this explicit matrix. A
block-triangular minor, determinant factorization, or exact kernel
factorization would prove the required postcritical surjectivity.

### 9.2 Induction in \((R,a)\)

Partition complements according to whether they contain \(t_R\), and
partition compositions according to one exponent. Finite differences in
\(t_R\) should separate the two blocks. The induction must explain both:

1. why degree \(d\) can retain a kernel; and
2. why multiplication by the \(a\) coordinate functions kills it at
   degree \(d+1\).

### 9.3 Critical-kernel multiplication

Let \(K_d\) be the left-kernel of critical degree-\(d\) evaluation, and
let \(D_j\) be multiplication by the \(j\)-th nonzero projective coordinate
on the point set. The exact identity proved in
`cremona_star_hypercohomology_reduction.md` is

\[
K_{d+1}=\bigcap_{j=0}^{a-1}D_j^{-1}K_d.
\]

Thus KPRCI says that no critical relation survives all coordinate
multiplications. A hypothetical survivor with support \(S\) also satisfies

\[
H_S(r)\le |\mathcal Y|-H_{\mathcal Y}(d+1-r)
\]

for every \(r\). Computing the critical defect and excluding such supports
is a focused combinatorial route.

### 9.4 Cremona-star hypercohomology

Pull the standard linear resolution of the original star configuration to
the permutohedral resolution of Cremona and twist by

\[
q^*\mathcal O(d+1).
\]

Postcritical surjectivity is equivalent to one total-degree-one
hypercohomology vanishing. This converts the target to exactness of a
finite complex of toric line-bundle cohomology spaces. Termwise vanishing
is not expected; the maps induced by the star-resolution differential are
load-bearing.

### 9.5 Star-configuration duality

The original \(n\)-fold products form a Chung-Yao/star configuration with
known interpolation. The complementary products are its coordinatewise
reciprocal. A regularity theorem for complementary square-free Hadamard
powers of a line would prove (3.2).

### 9.6 Generic factor plus semantic exception

A tropical or confluent specialization may prove that some maximal minor
is not the zero polynomial. This proves generic postcritical
surjectivity. To use it in the
packet, every remaining determinant-zero factor must then be classified
as a source quotient, planted relation, field descent, collective rank
defect, or saturation certificate at the same selected record.

### 9.7 Block-line emission

The block-line theorem proves SPSI's algebraic emission for every relation
generated by an overloaded family of coincident block lines. Distinct
full blocks carried by one line are pairwise disjoint. Every additional
vertex on a canonical block line is a near-full fiber of the same pencil
and consumes \(a-1\) new selected roots. Hence such a line contains at
most

\[
a\left\lfloor\frac Ra\right\rfloor
+
\mathbf1_{\{R\bmod a=a-1\}}
\]

selected vertices. Its exact degree-\((R-a+2)\) relation dimension is at
most

\[
\max\left\{
0,\,
a\left\lfloor\frac Ra\right\rfloor
+
\mathbf1_{\{R\bmod a=a-1\}}
-R+a-3
\right\}.
\]

At \(a=12,R=69\), this number is zero: at most 60 vertices lie on one
block line, while a relation requires 61. It is also zero for
\(a=14,R=67,68,69\). Hence every interpolation failure in those cases is
necessarily non-block-line.

For the other surviving parameter pairs, a block-line failure forces
several pairwise disjoint degree-\(a\) split locators into the pencil with
the source locator. The remaining classification target concerns
relations not generated by this planted branch, together with the
same-record payment adapter for the emitted pencil where it can occur.

## 10. Target hierarchy and nonclaims

KPRCI is weaker than the reciprocal-Cauchy separator statement in
`reciprocal_cauchy_separator_target.md`:

* KPRCI proves separation in degree \(R-a+3\);
* the stronger target asks for separation already in degree \(R-a+2\).

For \(a=12,R=69\), these are degree \(60\) and degree \(59\),
respectively. The stronger theorem would remove \(240\) values through
\(h=118{,}316\); KPRCI would remove \(207\) values through
\(h=118{,}283\). KPRCI remains a sufficient algebraic lemma, but SPSI is the
preferred immediate target because rank-deficient block-line packets are
already source-structured and should be paid rather than excluded.

UPRCI is false. KPRCI, SPSI's non-block-line branch, RCS, cap \(68\), and
the equality-wall payment remain open. The proved content here is the exact
reduction from postcritical surjectivity to degree-\((R-a+3)\) separation,
the conditional arithmetic (6.3)--(6.5), the finite-field guardrails, the
block-line planted emission and capacity theorems, the exact generation of
every known relation space by block-line relations, and the exact
critical-kernel/hypercohomology reformulations.

## Reference

C. Bocci, E. Carlini, and J. Kileel,
*Hadamard Products of Linear Spaces*, Journal of Algebra 448 (2016),
595--617, Theorem 4.7:
https://arxiv.org/abs/1504.04301
