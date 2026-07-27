# Complement-Locator Interpolation and Source-Divisor Descent

## 1. Status

This note proves a new exact identity for every regular rank-one
split-scroll packet. It interpolates the complementary carrier locators and
shows that the resulting divisibility error contains the complete source
divisor.

The identity does not yet prove the cap \(68\), and it does not instantiate
one of the seven active owners. It supplies a lower parameter-degree object
whose carrier fibers are controlled exactly by the MDS deficits from
`regular_grs_mds_deficit_reduction.md`.

## 2. Input

Let

\[
\mathcal U=U_0\setminus C_0,
\qquad
R_{\mathcal U}(X)=\prod_{x\in\mathcal U}(X-x),
\qquad
|\mathcal U|=n=J+D.
\tag{2.1}
\]

For \(R\) distinct regular parameters \(t_1,\ldots,t_R\), write

\[
\overline p_i(X)=\frac{\overline P(t_i,X)}{\lambda(t_i)}.
\tag{2.2}
\]

Here \(\overline P=P/\Lambda_{C_0}\), every \(\overline p_i\) is monic,
squarefree, has degree \(D\), and splits on \(\mathcal U\).

Define its complementary carrier locator

\[
q_i(X)=\frac{R_{\mathcal U}(X)}{\overline p_i(X)}.
\tag{2.3}
\]

It is monic, squarefree, and has degree

\[
\deg q_i=n-D=J.
\tag{2.4}
\]

Let

\[
H_T(t)=\prod_{i=1}^R(t-t_i).
\tag{2.5}
\]

Choose an affine parameter chart containing the regular parameters. The
monicity-refined source normalization gives

\[
\deg_t\overline P\le a-1,
\qquad
[X^D]\overline P(t,X)=\lambda(t),
\qquad
\deg_t\lambda\le a-1.
\tag{2.6}
\]

## 3. Interpolated complementary locator

There is a unique polynomial

\[
Q(t,X)\in F[t,X],
\qquad
\deg_tQ<R,
\tag{3.1}
\]

such that

\[
Q(t_i,X)=q_i(X)
\qquad(1\le i\le R).
\tag{3.2}
\]

Coefficientwise Lagrange interpolation constructs it canonically from the
ordered regular packet. Since every \(q_i\) is monic of degree \(J\),

\[
\boxed{[X^J]Q(t,X)=1.}
\tag{3.3}
\]

At every selected parameter,

\[
\overline P(t_i,X)Q(t_i,X)
=
\lambda(t_i)\overline p_i(X)q_i(X)
=
\lambda(t_i)R_{\mathcal U}(X).
\tag{3.4}
\]

## 4. Exact source-divisor descent

> **Theorem 4.1: complement-interpolation descent.**
> There is a unique polynomial \(S(t,X)\) such that
> \[
> \boxed{
> \overline P(t,X)Q(t,X)
> -
> \lambda(t)R_{\mathcal U}(X)
> =
> H_T(t)\Lambda_\Sigma(X)S(t,X).
> }
> \tag{4.1}
> \]
> It satisfies
> \[
> \boxed{
> \deg_tS\le a-2,
> \qquad
> \deg_XS\le n-s-1.
> }
> \tag{4.2}
> \]

### Proof

Equation (3.4) and the distinctness of the \(t_i\) first give

\[
\overline P Q-\lambda R_{\mathcal U}=H_T S_0
\tag{4.3}
\]

coefficientwise in \(X\). The parameter degree of the left side is at most

\[
(a-1)+(R-1)=R+a-2.
\]

Hence

\[
\deg_tS_0\le a-2.
\tag{4.4}
\]

Now fix \(\sigma\in\Sigma_j\). The exact source-fiber normalization has

\[
\overline P(t,\sigma)
=
\kappa_\sigma\frac{\lambda(t)}{L_j(t)},
\qquad
\kappa_\sigma\ne0.
\tag{4.5}
\]

Consequently,

\[
\overline p_i(\sigma)
=
\frac{\kappa_\sigma}{L_j(t_i)}
\tag{4.6}
\]

and

\[
q_i(\sigma)
=
\frac{R_{\mathcal U}(\sigma)L_j(t_i)}
{\kappa_\sigma}.
\tag{4.7}
\]

The right side is a projective linear function of \(t_i\). Since
\(R\ge2\), its degree-\(<R\) interpolation is the same linear function:

\[
Q(t,\sigma)
=
\frac{R_{\mathcal U}(\sigma)L_j(t)}
{\kappa_\sigma}.
\tag{4.8}
\]

Multiplying (4.5) and (4.8) gives

\[
\overline P(t,\sigma)Q(t,\sigma)
=
\lambda(t)R_{\mathcal U}(\sigma)
\]

identically in \(t\). Hence \(S_0(t,\sigma)=0\) for every
\(\sigma\in\Sigma\). Each \(t\)-coefficient of \(S_0\) is divisible by the
squarefree source locator \(\Lambda_\Sigma\), proving (4.1).

Finally, (3.3) and (2.6) show that the degree-\(n\) terms of
\(\overline P Q\) and \(\lambda R_{\mathcal U}\) agree. Thus their
difference has \(X\)-degree at most \(n-1\). Dividing by the degree-\(s\)
source locator gives

\[
\deg_XS\le n-s-1.
\]

This proves the theorem. \(\square\)

## 5. Affine source residue and high-mode descent

Equation (4.8) proves more than the divisibility of \(S_0\). Modulo the
source locator, the entire interpolated complementary locator is affine in
the parameter:

\[
\boxed{
Q(t,X)
\equiv
Q_0(X)+tQ_1(X)
\pmod{\Lambda_\Sigma(X)}.
}
\tag{5.1}
\]

Equivalently, there is a polynomial \(Q_+(t,X)\) such that

\[
\boxed{
Q(t,X)
=
Q_0(X)+tQ_1(X)+\Lambda_\Sigma(X)Q_+(t,X),
}
\tag{5.2}
\]

with

\[
\deg_XQ_+\le J-s.
\tag{5.3}
\]

Here \(Q_0,Q_1\) are the actual constant and linear \(t\)-coefficients of
\(Q\), rather than reduced representatives modulo \(\Lambda_\Sigma\).
Every coefficient of \(t^k\), \(k\ge2\), vanishes on all source points by
(4.8), while every \(X\)-coefficient of \(Q\) has degree at most \(J\).
Moreover, (3.3) implies

\[
[X^J]Q_0=1,
\qquad
\deg_XQ_1\le J-1.
\]

The source evaluation matrix of the complementary locators therefore has
rank exactly two:

\[
\boxed{
\operatorname{rank}
\bigl(q_i(\sigma)\bigr)_{\sigma\in\Sigma,\,1\le i\le R}
=2.
}
\tag{5.4}
\]

The upper bound follows from (4.7). Equality follows because the source map
has at least two distinct values, so two forms \(L_j\) are independent, and
all scaling factors in (4.7) are nonzero.

This is a support-side source-residue statement. It is not by itself the
active complement-locator or selected-multiplier owner predicate.

Define the affine source representative

\[
Q_{\rm aff}(t,X)=Q_0(X)+tQ_1(X)
\]

and the descended companion

\[
\boxed{
C(t,X)=
\frac{\overline P(t,X)Q_{\rm aff}(t,X)
-\lambda(t)R_{\mathcal U}(X)}
{\Lambda_\Sigma(X)}.
}
\tag{5.5}
\]

The numerator vanishes on \(\Sigma\) by (4.5)--(4.8), so \(C\) is a
polynomial. The leading \(X^n\) terms cancel, and therefore

\[
\boxed{
\deg_tC\le a,
\qquad
\deg_XC\le n-s-1.
}
\tag{5.6}
\]

Substituting (5.2) into (4.1) and cancelling the source locator gives the
exact lower-degree relation

\[
\boxed{
C(t,X)+\overline P(t,X)Q_+(t,X)=H_T(t)S(t,X).
}
\tag{5.7}
\]

For every carrier coordinate \(x\in\mathcal U\),
\(R_{\mathcal U}(x)=0\) and \(\Lambda_\Sigma(x)\ne0\), so (5.5) gives

\[
\boxed{
C(t,x)
=
\overline P(t,x)
\frac{Q_{\rm aff}(t,x)}{\Lambda_\Sigma(x)}.
}
\tag{5.8}
\]

Thus every carrier specialization of \(\overline P\) divides the
corresponding specialization of \(C\), with an affine parameter quotient.
The remaining question is whether these \(n\) simultaneous divisibilities
force \(C\) to be a global polynomial multiple of \(\overline P\), which
would yield a second kernel relation.

## 6. Exact carrier-row factorization

For \(x\in\mathcal U\), define

\[
I_x=\{i:\overline p_i(x)=0\},
\qquad
m_x=|I_x|.
\tag{6.1}
\]

Because \(q_i\) is the complementary locator,

\[
q_i(x)=0
\quad\Longleftrightarrow\quad
i\notin I_x.
\tag{6.2}
\]

The persistent core has already been removed, so
\(\overline P(t,x)\not\equiv0\). The weighted-GRS theorem gives

\[
m_x\le a-1.
\tag{6.3}
\]

If \(m_x\ge1\), there are polynomials \(A_x,B_x\) satisfying

\[
\overline P(t,x)
=
\prod_{i\in I_x}(t-t_i)A_x(t),
\qquad
\deg A_x\le a-1-m_x,
\tag{6.4}
\]

and

\[
Q(t,x)
=
\prod_{i\notin I_x}(t-t_i)B_x(t),
\qquad
\deg B_x\le m_x-1.
\tag{6.5}
\]

Substitution into (4.1), using
\(R_{\mathcal U}(x)=0\) and \(\Lambda_\Sigma(x)\ne0\), gives

\[
\boxed{
A_x(t)B_x(t)=\Lambda_\Sigma(x)S(t,x).
}
\tag{6.6}
\]

Write

\[
\eta_x=(a-1)-m_x.
\tag{6.7}
\]

Then

\[
\boxed{
\deg A_x\le\eta_x,
\qquad
\deg B_x\le a-2-\eta_x.
}
\tag{6.8}
\]

If \(m_x=0\), then \(Q(t,x)\) vanishes at all \(R\) interpolation points
and has degree \(<R\), so

\[
Q(t,x)\equiv0,
\qquad
S(t,x)\equiv0.
\tag{6.9}
\]

For a minimum-weight carrier row, \(\eta_x=0\). Therefore

\[
\boxed{
\overline P(t,x)
=
c_x\prod_{i\in I_x}(t-t_i),
\qquad
S(t,x)
=
c_x\Lambda_\Sigma(x)^{-1}B_x(t),
\quad
\deg B_x\le a-2.
}
\tag{6.10}
\]

Thus the exact MDS-deficit sum

\[
\Delta_R=\sum_x\eta_x
\tag{6.11}
\]

counts the total degree allowed in the \(A_x\)-side of the descended
factorization.

## 7. Consequences for the \(a=12\), \(R=69\) branch

The proved ledger gives

\[
118{,}077\le h\le118{,}599,
\tag{7.1}
\]

\[
\Delta_{69}\le30{,}313
\quad\text{at }h=118{,}077,
\tag{7.2}
\]

and at least

\[
1{,}136{,}341
\tag{7.3}
\]

carrier rows with \(\eta_x=0\).

On every one of those rows, the degree-\(10\) descended polynomial
\(S(t,x)\) is exactly the complementary interpolation defect after the
\(58\) selected nonincidences have been removed from \(Q(t,x)\).

## 8. Exact homogeneous resultant factorization

The companion note

```text
homogeneous_resultant_factorization.md
```

computes the projective parameter resultant exactly:

\[
\boxed{
\operatorname{Res}_{[T_0:T_1]}(\overline P,C)
=
\zeta R_{\mathcal U}^{\,a-1}
\prod_{j=1}^a\widetilde R_j,
\qquad
\zeta\in F^\times.
}
\tag{8.1}
\]

The \(\widetilde R_j\) are the actual post-core residual source-fiber
multipliers, and

\[
\sum_j\deg\widetilde R_j
\le
\mathcal B_a(h)
=
s-a(e-h)-(a-1).
\tag{8.2}
\]

Thus the resultant is nonzero, every carrier point occurs with multiplicity
\(a-1\), and every remaining resultant root is already one of the residual
source-multiplier roots. A bare resultant argument cannot produce a second
kernel or an excess-multiplicity contradiction.

The fixed-domain information survives only before taking the resultant, in
the simultaneous row factorizations (6.6).

## 9. Semantic boundary and next target

The polynomial \(q_i=R_{\mathcal U}/\overline p_i\) is the locator of the
support \(Y_i\) inside \(U_0\). It is not the original active complement
locator \(\Lambda_{Z_i}=\Lambda_{Z_0}\overline p_i\). Therefore (4.1) does
not instantiate the active pair-global source-rational owner.

Likewise, \(S\) is a packet-level interpolation correction, not the actual
selected-slope multiplier required by the Frobenius owner.

The useful next theorem is:

> **Minimum-row complementary-defect rigidity.**
> In the surviving \(a=12\) packet, the simultaneous factorizations
> (5.7)--(5.8), (6.4)--(6.10), the source-slack allocation, and
> fixed-domain splitting emit an already enabled cell at one of the same
> selected records.

A proof may equivalently show that the degree-\(10\) family \(S(t,x)\)
cannot occur on the forced minimum-weight carrier rows.

## 10. Nonclaims

This note does not prove the \(a=12\) cap, iteration through all source-zero
levels, a new owner payment, or the final equality-wall cap \(68\).
