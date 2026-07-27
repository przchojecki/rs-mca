# Postcritical Grouped-Cauchy Component Reduction

## 1. Status

This note closes the complete overloaded-line branch of the KoalaBear
postcritical reciprocal-Cauchy packet. It includes the two degeneracies
left open by the distinct-pole argument:

1. a common selected root in every line locator; and
2. proportional line-coordinate factors, equivalently a
   coordinate-ratio rank defect.

After removing the common vertical and horizontal components, the
correspondence has a grouped-Cauchy normal form. Its source-pole divisors
satisfy an effective version of the earlier period:

\[
\mathcal O_{\mathcal D}(a,-b)
\simeq
\mathcal O_{\mathcal D}(-E),
\qquad E\ge0,
\tag{1.1}
\]

where \(b\) is the number of distinct projective line-coordinate
factors. The selected split grid then produces a section of a line
bundle whose untwisted enlargement has no global sections.

Consequently, no line, canonical or noncanonical, reaches

\[
m\ge R-a+4
\]

in any of the rows

\[
(a,R)=(12,69),(14,67),(14,68),(14,69).
\]

The line branch therefore needs no same-record semantic adapter. The
conic, cubic, and support-at-least-\(3k+1\) circuit branches remain
separate.

## 2. Line-coordinate grouping

Let

\[
n=a-1
\]

and write the projective line coordinates as nonzero linear forms

\[
z_j(\lambda)=u_j+\lambda v_j,
\qquad 1\le j\le a.
\]

Group proportional forms. After a projective change of \(\lambda\), all
group roots and all actual selected line parameters are finite. Thus

\[
z_j(\lambda)=c_j\ell_{\gamma(j)}(\lambda),
\qquad
\ell_g(\lambda)=\lambda-\beta_g,
\]

where

\[
\beta_1,\ldots,\beta_b
\]

are distinct and the nonempty groups

\[
G_g=\gamma^{-1}(g)
\]

partition \(\{1,\ldots,a\}\). Put

\[
m_g=|G_g|,
\qquad
\sum_{g=1}^b m_g=a.
\tag{2.1}
\]

There must be at least two groups. If \(b=1\), all projective coordinate
ratios are constant and the purported line is one projective point, so
it cannot contain two distinct reciprocal-Cauchy vertices.

Let \(L_j(T)\) be the source Lagrange basis and define

\[
N(T,\lambda)
=
\sum_{j=1}^a
L_j(T)
\prod_{r\ne j}z_r(\lambda).
\tag{2.2}
\]

The common horizontal factor is

\[
H(\lambda)
=
\prod_{g=1}^b
\ell_g(\lambda)^{m_g-1}.
\tag{2.3}
\]

After dividing by \(H\), one obtains

\[
\widetilde N(T,\lambda)
=
\sum_{g=1}^b
G_g(T)h_g(\lambda),
\tag{2.4}
\]

where

\[
h_g(\lambda)
=
\prod_{\substack{r=1\\r\ne g}}^b\ell_r(\lambda)
\tag{2.5}
\]

and

\[
G_g(T)
=
\sum_{j\in G_g}\kappa_jL_j(T),
\qquad
\kappa_j\ne0.
\tag{2.6}
\]

The \(h_g\) form a basis of \(F[\lambda]_{\le b-1}\).

At an actual reciprocal-Cauchy point \(\lambda_s\), every coordinate
\(z_j(\lambda_s)\) is nonzero. Hence

\[
H(\lambda_s)\ne0.
\tag{2.7}
\]

The actual fiber of \(\widetilde N\) is therefore a nonzero scalar
multiple of the monic selected locator \(P_s(T)\).

## 3. Removing all common selected roots

Let

\[
C(T)=\gcd_s P_s(T)
\]

and put

\[
d=\deg C.
\tag{3.1}
\]

Every root of \(C\) is selected, because every \(P_s\) is a squarefree
locator on the selected set.

Since the number \(m\) of actual line points is greater than
\(b-1=\deg_\lambda\widetilde N\), every root of \(C\) is a root of
\(\widetilde N(T,\lambda)\) identically in \(\lambda\). Therefore

\[
C(T)\mid \widetilde N(T,\lambda).
\]

Define

\[
M(T,\lambda)
=
\frac{\widetilde N(T,\lambda)}{C(T)}
=
\sum_{g=1}^b
G'_g(T)h_g(\lambda),
\qquad
G'_g=\frac{G_g}{C}.
\tag{3.2}
\]

Put

\[
u=a-1-d,
\qquad
v=b-1.
\tag{3.3}
\]

Then \(M\) has bidegree \((u,v)\), and every actual fiber is a
squarefree degree-\(u\) locator on the remaining \(R-d\) selected
points.

The coefficient polynomials

\[
G'_1,\ldots,G'_b
\tag{3.4}
\]

are linearly independent. Indeed, if source index \(i\) belongs to
group \(G_g\), then

\[
G'_r(\alpha_i)=0\quad(r\ne g),
\qquad
G'_g(\alpha_i)\ne0,
\tag{3.5}
\]

because \(C(\alpha_i)\ne0\). Evaluation at one member of each group
kills every coefficient in a linear relation.

Equation (3.5) also implies

\[
m_g\ge d+1.
\tag{3.6}
\]

The polynomial \(G'_g\) has degree at most \(u\) and already vanishes
at the \(a-m_g\) source points outside \(G_g\). Thus

\[
a-m_g\le a-1-d.
\]

Summing (3.6) gives the useful structural constraint

\[
\boxed{a\ge b(d+1).}
\tag{3.7}
\]

## 4. Effective source-pole period

Let

\[
\mathcal D=V(M)
\subseteq
\mathbf P^1_T\times\mathbf P^1_\lambda.
\tag{4.1}
\]

There is no vertical or horizontal component. A vertical component
would be a common root of every actual residual locator, contrary to
the definition of \(C\). A horizontal component at \(\lambda=\beta_g\)
would require \(G'_g=0\), contrary to (3.4).

Put

\[
A(T)=\prod_{i=1}^a(T-\alpha_i),
\qquad
B(\lambda)=\prod_{g=1}^b(\lambda-\beta_g).
\tag{4.2}
\]

### Lemma 4.1

There is an effective Cartier divisor \(E\) on \(\mathcal D\) such that

\[
\boxed{
\operatorname{div}_{\mathcal D}(B)
=
\operatorname{div}_{\mathcal D}(A)+E.
}
\tag{4.3}
\]

Its degree is

\[
\boxed{
\deg E=a-b(d+1).
}
\tag{4.4}
\]

In particular,

\[
\boxed{
\mathcal O_{\mathcal D}(a,-b)
\simeq
\mathcal O_{\mathcal D}(-E).
}
\tag{4.5}
\]

### Proof

If \(i\in G_g\), then (3.5) gives

\[
M(\alpha_i,\lambda)
=
\eta_i h_g(\lambda),
\qquad
\eta_i\ne0.
\tag{4.6}
\]

Hence the restriction of \(A\) to \(\mathcal D\) has simple zeros at
all off-block points

\[
(\alpha_i,\beta_r),
\qquad
i\notin G_r.
\tag{4.7}
\]

There are

\[
\sum_{r=1}^b(a-m_r)=a(b-1)=av
\]

such points, exactly the full intersection degree of the divisor
\(A=0\), of class \((a,0)\), with a curve of bidegree \((u,v)\).
Thus (4.7), with multiplicity one, is the complete divisor of
\(A|_{\mathcal D}\).

At \(\lambda=\beta_r\), only the \(r\)-th term of (3.2) survives:

\[
M(T,\beta_r)=\theta_rG'_r(T),
\qquad
\theta_r\ne0.
\tag{4.8}
\]

Every off-block source point in (4.7) is therefore also a zero of
\(B|_{\mathcal D}\). Moreover, (4.6) has a simple zero in the
\(\lambda\)-direction there, so \(\mathcal D\) is smooth at that point
and \(A|_{\mathcal D}\) has local order one. The local order of
\(B|_{\mathcal D}\) is at least one. Consequently

\[
\operatorname{div}_{\mathcal D}(B)
-
\operatorname{div}_{\mathcal D}(A)
\]

is effective.

The two divisor degrees are

\[
\deg\operatorname{div}_{\mathcal D}(B)=bu,
\qquad
\deg\operatorname{div}_{\mathcal D}(A)=av.
\]

Their difference is

\[
bu-av
=
b(a-1-d)-a(b-1)
=
a-b(d+1),
\]

which is nonnegative by (3.7). This proves (4.3)-(4.5).
\(\square\)

When \(d=0\) and \(b=a\), \(E=0\) and (4.5) is the exact
diagonal-Cauchy period. Common roots and repeated coordinate factors
only add the effective negative twist \(-E\).

## 5. The selected grid section

Let the remaining selected roots be

\[
t_1,\ldots,t_{R-d}
\]

and the actual line parameters be

\[
\lambda_1,\ldots,\lambda_m.
\]

Put

\[
V(T)=\prod_{i=1}^{R-d}(T-t_i),
\qquad
L(\lambda)=\prod_{s=1}^m(\lambda-\lambda_s).
\tag{5.1}
\]

Every actual fiber \(M(T,\lambda_s)\) is a squarefree degree-\(u\)
locator dividing \(V(T)\). Therefore the horizontal divisor over the
\(\lambda_s\) is a subdivisor of \(\operatorname{div}(V|_{\mathcal D})\).
The quotient gives a nonzero section

\[
\boxed{
0\ne\sigma_{\rm grid}
\in
H^0\!\left(
\mathcal D,
\mathcal O_{\mathcal D}(R-d,-m)
\right).
}
\tag{5.2}
\]

For every integer \(q\ge0\), (4.5) gives

\[
\mathcal O_{\mathcal D}(R-d,-m)
\simeq
\mathcal O_{\mathcal D}
(R-d-qa,-m+qb)
\otimes
\mathcal O_{\mathcal D}(-qE).
\tag{5.3}
\]

Because \(E\) is effective,

\[
\mathcal O_{\mathcal D}(-qE)
\hookrightarrow
\mathcal O_{\mathcal D}.
\]

Thus (5.2) implies

\[
\boxed{
H^0\!\left(
\mathcal D,
\mathcal O_{\mathcal D}(R-d-qa,-m+qb)
\right)\ne0.
}
\tag{5.4}
\]

## 6. Vanishing on an arbitrary bidegree curve

### Lemma 6.1

Let \(\mathcal D\) be a bidegree-\((u,v)\) divisor. If

\[
0\le r\le u-1,
\qquad
s\ge1,
\]

then

\[
\boxed{
H^0(\mathcal D,\mathcal O_{\mathcal D}(r,-s))=0.
}
\tag{6.1}
\]

### Proof

Tensor the ideal sequence of \(\mathcal D\) by
\(\mathcal O(r,-s)\):

\[
0\to
\mathcal O(r-u,-s-v)
\to
\mathcal O(r,-s)
\to
\mathcal O_{\mathcal D}(r,-s)
\to0.
\tag{6.2}
\]

The middle term has no global sections. In the first term, both factors
have negative degree, with

\[
-u\le r-u\le-1,
\qquad
-s-v\le-2
\]

because \(v=b-1\ge1\). Kunneth therefore gives

\[
H^1(\mathcal O(r-u,-s-v))=0.
\]

The long exact sequence proves (6.1).
\(\square\)

### Lemma 6.2: boundary first degree

Write

\[
M(T,\lambda)=\sum_{j=0}^v M_j(T)\lambda^j
\tag{6.3}
\]

and assume

\[
M_0,\ldots,M_v
\]

are linearly independent. If \(s\ge2\), then

\[
\boxed{
H^0(\mathcal D,\mathcal O_{\mathcal D}(u,-s))=0.
}
\tag{6.4}
\]

### Proof

The only possible sections are the kernel of

\[
H^1(\mathcal O(0,-s-v))
\xrightarrow{\ \times M\ }
H^1(\mathcal O(u,-s)).
\tag{6.5}
\]

Represent a source class by

\[
q(\lambda)
=
\sum_{h=1}^{s+v-1}c_h\lambda^{-h}.
\tag{6.6}
\]

For every \(1\le r\le s-1\), the coefficient of
\(\lambda^{-r}\) in the target is

\[
\sum_{j=0}^v c_{r+j}M_j(T).
\tag{6.7}
\]

Linear independence forces

\[
c_r=\cdots=c_{r+v}=0.
\]

The consecutive windows for \(r=1,\ldots,s-1\) cover all coefficients
in (6.6), so \(q=0\). Thus (6.5) is injective.
\(\square\)

In the grouped-Cauchy form, the \(h_g\) are a basis of the
degree-\(\le v\) lambda polynomials and the \(G'_g\) are independent by
(3.4). Therefore the coefficient polynomials \(M_0,\ldots,M_v\) are
independent, and Lemma 6.2 applies.

## 7. KoalaBear row exclusion

The structural constraint (3.7) and \(b\ge2\) imply

\[
d\le\frac a2-1.
\tag{7.1}
\]

In particular all reduced first degrees below are nonnegative.

### 7.1 Row \((a,R)=(12,69)\)

Take \(q=5\). Then

\[
r=R-d-qa=9-d,
\qquad
u=11-d,
\]

so

\[
0\le r\le u-1.
\]

Also

\[
s=m-qb=m-5b
\ge61-5\cdot12
=1.
\]

Equation (5.4) contradicts Lemma 6.1.

### 7.2 Row \((a,R)=(14,67)\)

Take \(q=4\). Then

\[
r=11-d,
\qquad
u=13-d,
\qquad
r\le u-1,
\]

and

\[
s=m-4b
\ge57-4\cdot14
=1.
\]

Lemma 6.1 gives the contradiction.

### 7.3 Row \((a,R)=(14,68)\)

Again take \(q=4\). Now

\[
r=12-d=u-1
\]

and

\[
s=m-4b
\ge58-56
=2.
\]

Lemma 6.1 applies.

### 7.4 Row \((a,R)=(14,69)\)

Take \(q=4\). Here

\[
r=13-d=u
\]

and

\[
s=m-4b
\ge59-56
=3.
\]

The grouped coefficient polynomials are independent, so Lemma 6.2
contradicts (5.4).

## 8. Theorem and exact boundary

> **Complete postcritical overloaded-line exclusion.**
> In each KoalaBear row
> \[
> (a,R)=(12,69),(14,67),(14,68),(14,69),
> \]
> no projective line contains \(m\ge R-a+4\) distinct actual
> reciprocal-Cauchy vertices.

This includes:

1. canonical block lines;
2. noncanonical lines with a common selected root;
3. noncanonical lines with proportional coordinate factors; and
4. the generic diagonal-Cauchy branch.

Thus every postcritical circuit of support at most \(2k+1\), which the
minimal-linked-point theorem places on a line with at least \(k+2\)
selected vertices, is impossible.

No semantic owner or payment is needed for this branch. The next
postcritical targets are:

1. selected-record emission or exclusion for the \(2k+2\)-point conic;
2. the \(3k\)-point cubic/degree-\(k\) complete intersection; and
3. reduction of circuits with support at least \(3k+1\).

For the principal row \(a=12,R=69,k=59\), these support thresholds are

\[
120,\qquad177,\qquad178.
\]
