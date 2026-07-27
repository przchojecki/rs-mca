# Reciprocal-Cauchy Separator Target

## 1. Status

The source-partition Cremona descent exposes a finite interpolation
statement that would remove part of the hardest surviving KoalaBear
window. The corrected statement is a degree-\((R-a+2)\) separator
theorem. It is not proved here.

A stronger degree-\((R-a+1)\) unisolvence conjecture is false, including
for generic tested parameters with \(R>2a\). The finite regression records
this guardrail and supports the one-degree-weaker separator target.

If the separator theorem holds in the deployed range, it eliminates

\[
a=12,\qquad R=69,\qquad
118{,}077\le h\le118{,}316.
\]

It does not close the remaining \(283\) values of that window, the other
splitting degrees, or the general-excess descent.

## 2. Reciprocal-Cauchy vertices

Let

\[
\alpha_1,\ldots,\alpha_a
\]

be distinct source-map values and let

\[
t_1,\ldots,t_R
\]

be distinct regular selected parameters, disjoint from the source values.
After fixed nonzero row and column scalings, the regular weighted-GRS
hyperplanes have equations

\[
\ell_i(Z)
=
\sum_{j=1}^a\frac{Z_j}{t_i-\alpha_j}.
\tag{2.1}
\]

For

\[
I\in\binom{[R]}{a-1},
\qquad
N_I(T)=\prod_{i\in I}(T-t_i),
\]

let \(z_I\) be the unique projective intersection of the hyperplanes
\(\ell_i=0\), \(i\in I\). Partial fractions give

\[
(z_I)_j
\doteq
\frac{N_I(\alpha_j)}
{\prod_{k\ne j}(\alpha_j-\alpha_k)},
\tag{2.2}
\]

where \(\doteq\) permits fixed nonzero coordinate scalings.

Apply standard Cremona transformation. If

\[
G(T)=\prod_{i=1}^R(T-t_i),
\qquad
M_I(T)=\frac{G(T)}{N_I(T)},
\]

then

\[
\boxed{
y_I:=\operatorname{Cr}(z_I)
\doteq
\left(
\frac{M_I(\alpha_1)}{G(\alpha_1)},
\ldots,
\frac{M_I(\alpha_a)}{G(\alpha_a)}
\right).
}
\tag{2.3}
\]

Thus the transformed selected vertices are fixed diagonal scalings of
evaluation vectors of complementary split polynomials of degree

\[
d=R-a+1.
\tag{2.4}
\]

## 3. Failed unisolvence and exact target

Put

\[
\mathcal Y_{R,a}
=
\{y_I:I\in\binom{[R]}{a-1}\}
\subseteq\mathbf P^{a-1}.
\]

At degree \(d=R-a+1\), the dimensions match:

\[
\dim H^0(\mathbf P^{a-1},\mathcal O(d))
=
\binom{d+a-1}{a-1}
=
\binom R{a-1}
=
|\mathcal Y_{R,a}|.
\tag{3.1}
\]

It is tempting to assert that this square evaluation map is invertible.
The finite regression disproves that assertion: generic tested cases
\((a,R)=(4,9)\) and \((5,11)\) have defects \(7\) and \(20\),
respectively.

The exact sufficient statement is:

> **Reciprocal-Cauchy separation, RCS.**
> For all distinct source values and selected parameters in the deployed
> range, the common zero locus of
> \[
> I(\mathcal Y_{R,a})_{R-a+2}
> \]
> is exactly \(\mathcal Y_{R,a}\). Equivalently, for every
> \(v\notin\mathcal Y_{R,a}\), there is a homogeneous form of degree
> \(R-a+2\) that vanishes on every reciprocal-Cauchy vertex and is
> nonzero at \(v\).

For KoalaBear it is enough to prove RCS for

\[
12\le a\le16,
\qquad
53+a\le R\le69,
\tag{3.2}
\]

or to show that every separator failure emits an enabled same-record
owner.

## 4. Separator consequence

Assume RCS, and put

\[
r=R-a+2.
\]

Let

\[
\Psi:\mathbf P^1\longrightarrow\mathbf P^{a-1}
\]

be a nonconstant descended coefficient map of degree at most \(E_\Psi\).
If \(N_{\min}\) distinct carrier points map into
\(\mathcal Y_{R,a}\), choose a point of the image outside this finite set.
RCS gives a degree-\(r\) form that vanishes on every vertex but not at
that image point. Its pullback is nonzero, so

\[
\boxed{
N_{\min}\le(R-a+2)E_\Psi.
}
\tag{4.1}
\]

This is the exact bridge from RCS to the selected-vertex count.

## 5. Hardest-window arithmetic

Take

\[
a=12,\qquad R=69.
\]

The exact weighted-GRS deficit gives

\[
N_{\min}(h)
\ge
59(67{,}472+h)-10(981{,}105).
\tag{5.1}
\]

The source-partition Cremona descent gives

\[
E_\Psi(h)
\le
(134{,}944-h+1)
+
\bigl(12h-1{,}416{,}923\bigr)
=
11h-1{,}281{,}978.
\tag{5.2}
\]

Therefore

\[
\boxed{
N_{\min}(h)-59E_\Psi(h)
\ge
69{,}806{,}500-590h.
}
\tag{5.3}
\]

The right side is positive exactly through

\[
\boxed{h\le118{,}316.}
\tag{5.4}
\]

At the first endpoint the margin is

\[
1{,}136{,}341-59(16{,}869)
=
\boxed{141{,}070}.
\tag{5.5}
\]

Thus RCS would eliminate the \(240\) values

\[
118{,}077\le h\le118{,}316
\]

from the all-regular \(a=12\) branch. The remaining all-regular interval
would be

\[
118{,}317\le h\le118{,}599.
\]

## 6. Finite evidence and guardrail

The deterministic finite-field regression forms the complete evaluation
matrices in six small generic cases:

\[
\begin{array}{c|c|c|c|c}
a&R&|\mathcal Y_{R,a}|&
\text{degree-}d\text{ defect}&
\text{degree-}(d+1)\text{ defect}\\ \hline
3&6&15&1&0\\
3&7&21&0&0\\
4&8&56&2&0\\
4&9&84&7&0\\
5&10&210&3&0\\
5&11&330&20&0.
\end{array}
\]

For every row, adjoining five generic off-configuration points increases
the degree-\((d+1)\) evaluation rank by exactly five. This supports RCS
and explains why the one-degree correction is natural. It is finite
evidence, not a proof of the full base-locus statement.

## 7. Proof routes

### 7.1 Hilbert function and regularity

Using (2.3), a matrix entry indexed by a composition
\(\boldsymbol m=(m_1,\ldots,m_a)\), \(\sum m_j=d\), and a complement
\(J=[R]\setminus I\), \(|J|=d\), is

\[
\prod_{j=1}^aM_I(\alpha_j)^{m_j}
=
\prod_{r\in J}
\left(
\prod_{j=1}^a(\alpha_j-t_r)^{m_j}
\right).
\tag{7.1}
\]

The primary target is to prove that the reciprocal-Cauchy point scheme has
regularity at most \(R-a+2\), and that its saturated ideal has no
positive-dimensional base component in that degree. The degree-\(d\)
kernel must be retained as a genuine syzygy rather than mistaken for a
separator failure.

### 7.2 Complement-product induction

Partition rows according to whether a distinguished parameter belongs to
\(J\), and partition monomials by one exponent. Finite differences in the
distinguished parameter may block-triangularize the degree-\((d+1)\)
evaluation map and give an induction in \((R,a)\). The observed
degree-\(d\) defects must occur explicitly without entering the saturated
base locus.

### 7.3 Interpolation duality

The original Cauchy vertices form a Chung-Yao lattice. Formula (2.3)
identifies the transformed vertices with evaluations of complementary
split products. A dual Chung-Yao or Gasca-Maeztu regularity theorem would
prove RCS without asserting false degree-\(d\) poisedness.

### 7.4 Fail-closed exception

If RCS has exceptional parameter loci, genericity cannot be assumed.
A positive-dimensional base component must instead produce a canonical
source quotient, planted relation, proper-field descent, baseline-free
rank defect, or saturation certificate at one of the same selected
records.

## 8. Nonclaims

This note does not prove RCS, selected-vertex rigidity, any owner payment,
cap \(68\), or the equality-wall result. Its proved content is the exact
vertex formula, the separator implication, and the conditional arithmetic
reduction (5.3)--(5.5).
