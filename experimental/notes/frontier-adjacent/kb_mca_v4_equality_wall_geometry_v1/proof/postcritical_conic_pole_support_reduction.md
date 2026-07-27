# Postcritical Conic Pole-Support Reduction

## 1. Status

This note advances the irreducible-conic branch left after the complete
postcritical line exclusion.

For the principal KoalaBear row

\[
a=12,\qquad R=69,\qquad k=59,
\]

an irreducible-conic circuit has \(m=2k+2=120\) selected vertices. The
quadratic-coordinate correspondence has an effective source-pole
period. It proves:

1. any common selected locator root is impossible;
2. any overlap between the projective root divisors of two coordinate
   quadratics is impossible;
3. the only surviving endpoint has 24 disjoint coordinate-pole
   occurrences and an exact period
   \[
   \mathcal O_{\mathcal D}(12,-24)\simeq\mathcal O_{\mathcal D};
   \]
4. the selected supports form an exact
   \[
   1\text{-}(60,11,22)
   \]
   incidence design on 60 of the 69 selected roots;
5. the former degree-198 remainder is the divisor of a degree-nine
   polynomial whose roots are exactly the other nine selected roots.

This does not yet exclude that endpoint or emit its same-record planted
owner. It replaces the arbitrary 120-point irreducible-conic packet by
one exact fixed-domain design and polynomial identity.

## 2. Quadratic-coordinate normal form

Work after scalar extension to an algebraic closure. Let

\[
z_i(\lambda)
\qquad(1\le i\le a)
\]

be the nonzero binary quadratics obtained by restricting the ambient
coordinates to the normalization of the irreducible conic. Factor

\[
z_i
=
c_i\prod_{g=1}^b\ell_g^{e_{ig}},
\qquad
\sum_g e_{ig}=2.
\tag{2.1}
\]

The \(\ell_g\) are distinct projective linear factors. Put

\[
M_g=\sum_{i=1}^a e_{ig},
\qquad
\mu_g=\max_i e_{ig},
\qquad
\beta=\sum_{g=1}^b\mu_g.
\tag{2.2}
\]

Since the total degree of all coordinate quadratics is \(2a\),

\[
\boxed{\beta\le2a.}
\tag{2.3}
\]

The restricted ambient coordinates span the complete
three-dimensional space
\(H^0(\mathbf P^1,\mathcal O(2))\), because the conic is irreducible
and spans its plane. If \(\beta\le2\), every quadratic \(z_i\) would be
proportional to the same degree-two product dividing \(B\). Therefore

\[
\boxed{3\le\beta\le2a.}
\tag{2.3a}
\]

Let

\[
\Delta=\prod_{i=1}^az_i,
\qquad
H=\prod_g\ell_g^{M_g-\mu_g},
\qquad
B=\prod_g\ell_g^{\mu_g}.
\tag{2.4}
\]

The conic locator polynomial

\[
N_C(T,\lambda)
=
\sum_{i=1}^a
L_i(T)\frac{\Delta(\lambda)}{z_i(\lambda)}
\]

has the common horizontal factor \(H\). Dividing it gives

\[
\widetilde N(T,\lambda)
=
\sum_{i=1}^a
\kappa_iL_i(T)h_i(\lambda),
\qquad
h_i=\frac{B}{z_i},
\qquad
\kappa_i\ne0.
\tag{2.5}
\]

Thus

\[
\deg_\lambda\widetilde N=\beta-2.
\tag{2.6}
\]

Every actual conic parameter avoids every coordinate pole, so
\(H(\lambda_s)\ne0\), and its \(\widetilde N\)-fiber is a nonzero scalar
multiple of the selected degree-\((a-1)\) locator.

## 3. Common vertical component removal

Let \(C(T)\) be the gcd of the \(m\) actual selected locators and put

\[
d=\deg C.
\tag{3.1}
\]

Because

\[
m>\beta-2,
\]

every common selected root is a root of
\(\widetilde N(T,\lambda)\) identically in \(\lambda\). Hence

\[
C(T)\mid\widetilde N(T,\lambda).
\]

Define

\[
M(T,\lambda)
=
\frac{\widetilde N(T,\lambda)}{C(T)}
\tag{3.2}
\]

and

\[
u=a-1-d,
\qquad
v=\beta-2.
\tag{3.3}
\]

The curve

\[
\mathcal D=V(M)
\subseteq\mathbf P^1_T\times\mathbf P^1_\lambda
\]

has bidegree \((u,v)\), no vertical or horizontal component, and every
actual horizontal fiber is a squarefree degree-\(u\) locator on the
remaining \(R-d\) selected roots.

## 4. Effective conic source-pole period

Let

\[
A(T)=\prod_{i=1}^a(T-\alpha_i).
\]

### Lemma 4.1

There is an effective Cartier divisor \(E\) on \(\mathcal D\) such that

\[
\boxed{
\operatorname{div}_{\mathcal D}(B)
=
\operatorname{div}_{\mathcal D}(A)+E.
}
\tag{4.1}
\]

Its degree is

\[
\boxed{
\deg E=2a-\beta(d+1).
}
\tag{4.2}
\]

Equivalently,

\[
\boxed{
\mathcal O_{\mathcal D}(a,-\beta)
\simeq
\mathcal O_{\mathcal D}(-E).
}
\tag{4.3}
\]

### Proof

At a source point,

\[
M(\alpha_i,\lambda)
=
\eta_i\frac{B(\lambda)}{z_i(\lambda)},
\qquad
\eta_i\ne0.
\tag{4.4}
\]

Thus the divisor of \(A|_{\mathcal D}\) consists of the zeros of
\(B/z_i\) over all \(i\), with total degree

\[
a(\beta-2)=av.
\]

This is the complete intersection degree of \(A=0\) with
\(\mathcal D\).

Fix a branch of the normalization of \(\mathcal D\) over a point
\((\alpha_i,\ell_g=0)\) with \(e_{ig}<\mu_g\). Put

\[
x=T-\alpha_i,
\qquad
y=\ell_g(\lambda),
\qquad
q=\mu_g-e_{ig}.
\]

Locally, (4.4) has the form

\[
y^qU(y)+xK(x,y)=0,
\qquad U(0)\ne0.
\tag{4.5}
\]

On the branch,

\[
\operatorname{ord}(x)
\le
q\,\operatorname{ord}(y)
\le
\mu_g\,\operatorname{ord}(y).
\]

The left side is the local order of \(A\); the final expression is the
local order of the factor \(\ell_g^{\mu_g}\) in \(B\). Hence

\[
\operatorname{div}_{\mathcal D}(B)
\ge
\operatorname{div}_{\mathcal D}(A).
\]

The degree difference is

\[
\beta u-av
=
\beta(a-1-d)-a(\beta-2)
=
2a-\beta(d+1).
\]

This proves the lemma.
\(\square\)

In particular,

\[
\boxed{\beta(d+1)\le2a.}
\tag{4.6}
\]

## 5. Grid section and degeneracy exclusion

Let

\[
V(T)=\prod_{t\in\mathcal T\setminus Z(C)}(T-t),
\qquad
L(\lambda)=\prod_{s=1}^{m}(\lambda-\lambda_s).
\]

The actual split fibers give

\[
0\ne\sigma_{\rm grid}
\in
H^0\!\left(
\mathcal D,
\mathcal O_{\mathcal D}(R-d,-m)
\right).
\tag{5.1}
\]

Using (4.3) five times gives an injection

\[
H^0\!\left(
\mathcal D,
\mathcal O_{\mathcal D}(R-d,-m)
\right)
\hookrightarrow
H^0\!\left(
\mathcal D,
\mathcal O_{\mathcal D}(R-d-5a,-m+5\beta)
\right).
\tag{5.2}
\]

For \(a=12,R=69,m=120\), the target bundle is

\[
\mathcal O_{\mathcal D}(9-d,-(120-5\beta)).
\tag{5.3}
\]

If \(\beta\le23\), then

\[
120-5\beta\ge5
\]

and

\[
0\le9-d\le u-1=10-d.
\]

The bidegree-curve Kunneth vanishing therefore contradicts (5.2).

Consequently every surviving irreducible-conic packet has

\[
\boxed{\beta=24=2a.}
\tag{5.4}
\]

Equation (4.6) then forces

\[
\boxed{d=0,\qquad E=0.}
\tag{5.5}
\]

Moreover, equality in (2.3) says that every projective root occurrence
belongs to exactly one coordinate quadratic. Therefore

\[
\boxed{\gcd(z_i,z_j)=1\quad(i\ne j).}
\tag{5.6}
\]

Repeated roots within one \(z_i\) are allowed; roots shared by two
different coordinate quadratics are not.

## 6. Exact degree-nine endpoint section

At the endpoint,

\[
\mathcal O_{\mathcal D}(12,-24)
\simeq
\mathcal O_{\mathcal D}.
\tag{6.1}
\]

Multiplying the grid section by the fifth power of the nowhere-zero
ratio \(B/A\) gives

\[
0\ne\tau
=
\frac{V(T)B(\lambda)^5}
{L(\lambda)A(T)^5}
\in
H^0(\mathcal D,\mathcal O_{\mathcal D}(9,0)).
\tag{6.2}
\]

Because \(\mathcal D\) has bidegree \((11,22)\), restriction gives an
isomorphism

\[
H^0(\mathbf P^1_T,\mathcal O(9))
\longrightarrow
H^0(\mathcal D,\mathcal O_{\mathcal D}(9,0)).
\tag{6.3}
\]

Indeed, the kernel and obstruction groups come from
\(\mathcal O(-2,-22)\), whose \(H^0\) and \(H^1\) both vanish.

Therefore there is a unique nonzero polynomial \(Q_9(T)\), of degree at
most nine, such that on \(\mathcal D\),

\[
\boxed{
\frac{V(T)B(\lambda)^5}
{L(\lambda)A(T)^5}
=
Q_9(T).
}
\tag{6.4}
\]

Equivalently, for some bihomogeneous \(W(T,\lambda)\),

\[
\boxed{
V(T)B(\lambda)^5
-
Q_9(T)L(\lambda)A(T)^5
=
M(T,\lambda)W(T,\lambda).
}
\tag{6.5}
\]

The bidegree of \(W\) is \((58,98)\).

## 7. Exact \(1\)-design

For a selected root \(t\), let

\[
n_t
=
\#\{s:t\text{ is a root of the locator at }\lambda_s\}.
\tag{7.1}
\]

### Lemma 7.1

If \(n_t>0\), then

\[
\boxed{n_t=22}
\tag{7.2}
\]

and \(Q_9(t)\ne0\).

### Proof

The divisor form of (6.4) is

\[
\operatorname{div}_{\mathcal D}(V)
-
\operatorname{div}_{\mathcal D}(L)
=
\operatorname{div}_{\mathcal D}(Q_9).
\tag{7.3}
\]

Choose an actual grid point \((t,\lambda_s)\). If \(Q_9(t)=0\) with
multiplicity \(q\ge1\), then on any branch through that point, (7.3)
would give

\[
\operatorname{ord}(T-t)
-
\operatorname{ord}(\lambda-\lambda_s)
=
q\,\operatorname{ord}(T-t),
\]

which is impossible because both local orders are positive.
Therefore \(Q_9(t)\ne0\).

Equation (7.3) then has no residual divisor over \(T=t\). The complete
degree-22 vertical fiber is exactly the sum of its actual grid points,
each with the multiplicity supplied by \(L\). At an actual grid point,
the horizontal fiber \(M(T,\lambda_s)\) is a squarefree locator, so
\(\partial M/\partial T\ne0\). Hence
\(\lambda-\lambda_s\) is a local uniformizer and contributes
multiplicity one. Since the actual \(\lambda_s\) are distinct, there
are exactly 22 of them.
\(\square\)

The total selected-root incidence is

\[
\sum_tn_t
=
120\cdot11
=
1320
=
60\cdot22.
\tag{7.4}
\]

Lemma 7.1 therefore implies that exactly 60 selected roots have
multiplicity 22 and the remaining nine have multiplicity zero.

For an inactive selected root \(t\), the full vertical fiber remains in
the left side of (7.3), so \(Q_9(t)=0\). Hence

\[
\boxed{
Q_9(T)
=
c\prod_{t\in\mathcal T_{\rm inactive}}(T-t),
\qquad
c\ne0.
}
\tag{7.5}
\]

In particular \(Q_9\) has exact degree nine and simple selected roots.

Let \(\mathcal T_{\rm active}\) be the 60 active selected roots and let
\(\mathcal I\) be the 120 locator supports. Then

\[
\boxed{
\begin{aligned}
&I\subseteq\mathcal T_{\rm active},\qquad |I|=11
&& (I\in\mathcal I),\\
&|\mathcal I|=120,\\
&\#\{I\in\mathcal I:t\in I\}=22
&& (t\in\mathcal T_{\rm active}).
\end{aligned}
}
\tag{7.6}
\]

Thus \((\mathcal T_{\rm active},\mathcal I)\) is an exact
\(1\)-\((60,11,22)\) design.

## 8. Sharpened remaining target

The principal irreducible-conic branch is now exactly:

> **Pole-disjoint conic endpoint.** Exclude, or route to an enabled
> same-record planted owner, an actual reciprocal-Cauchy irreducible
> conic whose coordinate quadratics have pairwise disjoint projective
> root divisors and whose 120 split locators form the
> \(1\)-\((60,11,22)\) design (7.6), with the exact polynomial identity
> (6.5) and inactive-root locator (7.5).

This is strictly narrower than the previous degree-198 resultant
target. The entire remainder has become one printed degree-nine split
locator and one regular fixed-domain incidence design.

For the \(a=14,R=68\) row, the same argument with four periods has

\[
r=12-d=u-1,
\qquad
s=114-4\beta\ge2,
\]

even at \(\beta=28\). Hence the irreducible-conic branch is completely
impossible in that row.

The \(a=14,R=67\) endpoint and the \(a=14,R=69\) boundary require
separate treatment. Reducible conics, cubic complete intersections, and
circuits of support at least \(3k+1\) also remain separate.
