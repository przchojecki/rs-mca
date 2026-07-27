# Homogeneous Resultant Factorization for the Complement Descent

## 1. Status

This note computes the parameter resultant of the complement-descended pair
exactly. The computation proves that the ordinary resultant route cannot
close the remaining KoalaBear split-scroll packet.

The result is

\[
\boxed{
\operatorname{Res}_{[T_0:T_1]}(\overline P,C)
=
\zeta R_{\mathcal U}^{\,a-1}
\prod_{j=1}^a\widetilde R_j,
\qquad
\zeta\in F^\times.
}
\tag{1.1}
\]

Here the \(\widetilde R_j\) are the actual residual source-fiber
multipliers after removal of the persistent carrier core.

In particular, the resultant is nonzero. Its complete divisor is already
accounted for by the carrier and source-fiber ledgers, so neither a bare
resultant-degree contradiction nor a resultant-zero second-kernel
alternative remains available.

## 2. Homogeneous input

Use homogeneous parameter coordinates \([T_0:T_1]\). Let

\[
\boldsymbol\lambda(T_0,T_1)
=
\prod_{j=1}^aL_j(T_0,T_1)
\tag{2.1}
\]

be the degree-\(a\) source scalar. The persistent-core-normalized scroll
polynomial

\[
\overline P(T_0,T_1;X)
\]

is homogeneous of parameter degree \(a-1\) and has the exact source
Lagrange decomposition

\[
\overline P
=
\sum_{j=1}^a
\overline Q_j(X)
\boldsymbol\lambda_j^*(T_0,T_1),
\qquad
\boldsymbol\lambda_j^*
=
\frac{\boldsymbol\lambda}{L_j}.
\tag{2.2}
\]

Write

\[
\Sigma_j
=
\{\sigma\in\Sigma:f(\sigma)=\alpha_j\}.
\]

The source-fiber theorem gives

\[
\boxed{
\overline Q_j(X)
=
\Lambda_{\Sigma\setminus\Sigma_j}(X)
\widetilde R_j(X),
\qquad
\widetilde R_j\ne0.
}
\tag{2.3}
\]

Let

\[
\mathcal U=U_0\setminus C_0,
\qquad
R_{\mathcal U}(X)=\prod_{x\in\mathcal U}(X-x),
\qquad
|\mathcal U|=n.
\tag{2.4}
\]

The complement-interpolation theorem supplies a homogeneous linear form
in the parameter,

\[
Q_{\rm aff}(T_0,T_1;X),
\]

and a parameter-degree-\(a\) polynomial \(C\) satisfying

\[
\boxed{
\Lambda_\Sigma(X)C
=
\overline P Q_{\rm aff}
-
\boldsymbol\lambda R_{\mathcal U}.
}
\tag{2.5}
\]

## 3. Exact resultant theorem

> **Theorem 3.1.**
> Under the input above, the homogeneous parameter resultant satisfies
> (1.1).

### Proof

Put

\[
\mathcal R(X)
=
\operatorname{Res}_{[T_0:T_1]}(\overline P,C),
\]

where the two forms have parameter degrees \(a-1\) and \(a\),
respectively.

Scaling the second form by the parameter-independent polynomial
\(\Lambda_\Sigma(X)\) gives

\[
\operatorname{Res}(\overline P,\Lambda_\Sigma C)
=
\Lambda_\Sigma^{\,a-1}\mathcal R.
\tag{3.1}
\]

Adding a homogeneous linear multiple of the first form to the second does
not change this resultant. Equation (2.5) therefore gives

\[
\begin{aligned}
\Lambda_\Sigma^{\,a-1}\mathcal R
&=
\operatorname{Res}
\left(
\overline P,
\overline P Q_{\rm aff}
-
\boldsymbol\lambda R_{\mathcal U}
\right)\\
&=
\operatorname{Res}
\left(
\overline P,
-
\boldsymbol\lambda R_{\mathcal U}
\right)\\
&=
\zeta_0
R_{\mathcal U}^{\,a-1}
\operatorname{Res}
\left(
\overline P,
\boldsymbol\lambda
\right)
\end{aligned}
\tag{3.2}
\]

for a sign \(\zeta_0\in F^\times\).

The source scalar has the \(a\) distinct projective roots
\(\alpha_1,\ldots,\alpha_a\). Evaluating (2.2) at \(\alpha_j\) leaves only
the \(j\)-th Lagrange term:

\[
\overline P(\alpha_j,X)
=
u_j\overline Q_j(X),
\qquad
u_j\in F^\times.
\tag{3.3}
\]

The root-product formula for the homogeneous resultant now gives

\[
\operatorname{Res}
\left(
\overline P,
\boldsymbol\lambda
\right)
=
\zeta_1\prod_{j=1}^a\overline Q_j(X),
\qquad
\zeta_1\in F^\times.
\tag{3.4}
\]

Every source point \(\sigma\in\Sigma_k\) occurs in
\(\Lambda_{\Sigma\setminus\Sigma_j}\) for exactly the \(a-1\) indices
\(j\ne k\). Consequently, (2.3) implies

\[
\prod_{j=1}^a\overline Q_j
=
\Lambda_\Sigma^{\,a-1}
\prod_{j=1}^a\widetilde R_j.
\tag{3.5}
\]

Substituting (3.4)--(3.5) into (3.2) and cancelling the nonzero polynomial
\(\Lambda_\Sigma^{a-1}\) proves

\[
\mathcal R
=
\zeta
R_{\mathcal U}^{\,a-1}
\prod_{j=1}^a\widetilde R_j
\]

for \(\zeta=\zeta_0\zeta_1\in F^\times\). \(\square\)

## 4. Exact divisor and degree ledger

The theorem gives the complete resultant divisor:

\[
\boxed{
\operatorname{div}\mathcal R
=
(a-1)\sum_{x\in\mathcal U}[x]
+
\sum_{j=1}^a\operatorname{div}\widetilde R_j.
}
\tag{4.1}
\]

In particular,

\[
\boxed{
\deg_X\mathcal R
=
(a-1)n+b_{\rm act},
\qquad
b_{\rm act}
:=
\sum_{j=1}^a\deg\widetilde R_j.
}
\tag{4.2}
\]

The monicity-refined source-fiber theorem gives

\[
0\le b_{\rm act}\le
\mathcal B_a(h)
:=
s-a(e-h)-(a-1).
\tag{4.3}
\]

Thus the previous upper bound

\[
\deg_X\mathcal R
\le
(a-1)n+\mathcal B_a(h)
\]

is attained precisely to the actual residual multiplier degree. The
weighted-GRS deficit does not provide additional resultant roots: it only
records which selected parameter roots account for the fixed carrier
multiplicity \(a-1\).

For \(a=12\), \(R=69\), and \(h=118{,}077\),

\[
\mathcal B_{12}(h)=1,
\]

so

\[
\operatorname{Res}(\overline P,C)
=
\zeta R_{\mathcal U}^{11}E(X),
\qquad
\deg E\le1.
\tag{4.4}
\]

At \(h=118{,}599\), the only possible noncarrier factor has degree at most
\(6{,}265\).

## 5. Consequences

### 5.1 The resultant is never the second kernel

Every \(\widetilde R_j\) is nonzero, and \(R_{\mathcal U}\ne0\). Hence

\[
\boxed{
\operatorname{Res}(\overline P,C)\ne0.
}
\tag{5.1}
\]

Equivalently, \(\overline P\) and \(C\) are coprime over \(F(X)\) as
parameter polynomials. The earlier speculative alternative in which their
resultant vanishes and directly produces a second generic kernel is
therefore unavailable.

### 5.2 Extra intersection multiplicity is already classified

Every carrier coordinate has resultant multiplicity at least \(a-1\).
Any multiplicity beyond \(a-1\), and every resultant root outside the
carrier, comes exactly from the residual source multipliers
\(\widetilde R_j\).

Therefore a proof cannot obtain a contradiction merely by finding more
than the selected \(RD\) incidences. It must produce a root or
multiplicity not already contained in

\[
R_{\mathcal U}^{a-1}\prod_j\widetilde R_j,
\]

which Theorem 3.1 proves impossible for this resultant.

### 5.3 The useful information is pre-resultant

The remaining structure is the rowwise factorization

\[
A_x(t)B_x(t)
=
\Lambda_\Sigma(x)S(t,x),
\]

with

\[
\deg A_x\le\eta_x,
\qquad
\deg B_x\le a-2-\eta_x.
\]

Taking the resultant erases the partition of the fixed carrier among the
selected records and retains only the already-known source multipliers.
Any successful proof must use the simultaneous family of factors
\(A_x,B_x,S(t,x)\) before this information is collapsed.

## 6. Corrected next target

> **Minimum-row complementary-defect rigidity.**
> In each surviving low-excess packet, the source-derived polynomial
> \(S(t,X)\), together with the fixed-domain factorizations
> \[
> A_xB_x=\Lambda_\Sigma(x)S(t,x),
> \]
> cannot realize the forced weighted-GRS minimum rows and the printed
> source-multiplier budget unless an already enabled same-record owner is
> emitted.

For the all-regular \(a=12\) branch, this asks for a classification of the
degree-\(10\) polynomials \(S(t,x)\) on at least \(1{,}136{,}341\)
minimum-weight carrier rows.

A useful proof must retain which \(11\) selected records own each minimum
row. A scalar resultant, determinant degree, or total incidence count no
longer contains that information.

## 7. Nonclaims

This note does not prove minimum-row complementary-defect rigidity, the
low-excess cap, the general-excess descent, cap \(68\), or an owner
payment.
