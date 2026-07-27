# Source-Partition Cremona Descent

## 1. Status

This note gives an exact lower-degree model of every low-excess
source-coefficient curve. Standard projective Cremona transformation removes
the repeated source-locator products from the coefficient coordinates.

At the lower endpoints of the five surviving windows, it replaces a
degree-\(D\) coefficient curve, where \(185{,}549\le D\le189{,}766\), by
a birational source-partition curve of degree at most

\[
12{,}652\le E_\Psi\le16{,}869.
\]

The selected split-locator equations become explicit degree-\((a-1)\)
hypersurfaces on this smaller curve. This preserves the selected-record
incidence pattern exactly.

## 2. Source-factor coordinates

Put

\[
F_j(X)=\Lambda_{\Sigma_j}(X),
\qquad
L(X)=\Lambda_\Sigma(X)=\prod_{j=1}^aF_j(X),
\tag{2.1}
\]

and write the persistent-core-normalized source coefficients as

\[
\overline Q_j(X)
=
\frac{L(X)}{F_j(X)}\widetilde R_j(X),
\qquad
\widetilde R_j\ne0.
\tag{2.2}
\]

Set

\[
R_*(X)=\prod_{j=1}^a\widetilde R_j(X).
\tag{2.3}
\]

The coefficient map is

\[
\Phi(X)
=
[\overline Q_1(X):\cdots:\overline Q_a(X)].
\tag{2.4}
\]

## 3. Exact Cremona transform

Let

\[
\operatorname{Cr}
:
[Z_1:\cdots:Z_a]
\dashrightarrow
\left[
\prod_{k\ne1}Z_k:
\cdots:
\prod_{k\ne a}Z_k
\right]
\tag{3.1}
\]

be standard Cremona transformation. Substituting (2.2) gives

\[
\prod_{k\ne j}\overline Q_k
=
L^{a-2}
F_j
\prod_{k\ne j}\widetilde R_k.
\tag{3.2}
\]

After removing the common factor \(L^{a-2}\), define

\[
\boxed{
\Psi_j(X)
=
F_j(X)
\prod_{k\ne j}\widetilde R_k(X).
}
\tag{3.3}
\]

Thus

\[
\boxed{
\Psi
:=
[\Psi_1:\cdots:\Psi_a]
=
\operatorname{Cr}\circ\Phi
}
\tag{3.4}
\]

where both sides are defined.

Applying Cremona again gives the exact inverse relation

\[
\prod_{k\ne j}\Psi_k
=
R_*^{\,a-2}\overline Q_j.
\tag{3.5}
\]

Consequently, \(\Phi\) and \(\Psi\) generate the same function field. In
particular, they have the same covering degree onto their respective image
normalizations.

## 4. Degree descent

Write

\[
b_j=\deg\widetilde R_j,
\qquad
b_*=\sum_jb_j.
\]

Equation (3.3) gives

\[
\boxed{
\deg\Psi_j
=
n_j+b_*-b_j.
}
\tag{4.1}
\]

At a minimum-window endpoint, the source-fiber ledger has

\[
n_j=n_0+\varepsilon_j
\quad(j<a),
\qquad
n_a=n_0-1+\varepsilon_a,
\tag{4.2}
\]

with

\[
b_j\le\varepsilon_j,
\qquad
\sum_j\varepsilon_j=\mathcal B_a(h_{\min}).
\tag{4.3}
\]

Therefore

\[
\boxed{
E_\Psi:=\max_j\deg\Psi_j
\le
n_0+\mathcal B_a(h_{\min}).
}
\tag{4.4}
\]

The exact endpoint caps are

\[
\begin{array}{c|r|r|r}
a&n_0&\mathcal B_a(h_{\min})&E_\Psi\text{ upper bound}\\ \hline
12&16{,}868&1&16{,}869\\
13&15{,}570&7&15{,}577\\
14&14{,}458&5&14{,}463\\
15&13{,}494&7&13{,}501\\
16&12{,}651&1&12{,}652.
\end{array}
\tag{4.5}
\]

By minimum-window coefficient-curve birationality and (3.4), \(\Psi\) is
also birational onto its image in all five rows.

## 5. Transformed selected-locator equations

For a regular selected parameter \(t_i\), write

\[
c_{ij}=\frac{1}{L_j(t_i)}
\]

after absorbing the fixed nonzero Lagrange scalars. Then

\[
\overline p_i(X)
=
\sum_{j=1}^ac_{ij}\overline Q_j(X).
\tag{5.1}
\]

Define the degree-\((a-1)\) Cremona transform of this hyperplane by

\[
\mathfrak H_i(Y_1,\ldots,Y_a)
=
\sum_{j=1}^a
c_{ij}
\prod_{k\ne j}Y_k.
\tag{5.2}
\]

Using (3.5),

\[
\boxed{
\mathfrak H_i(\Psi(X))
=
R_*(X)^{a-2}\overline p_i(X).
}
\tag{5.3}
\]

Thus every transformed hypersurface has exactly:

1. the common residual divisor \(R_*^{a-2}\); and
2. the fixed-domain split divisor of the same selected locator
   \(\overline p_i\).

No owner or support is exchanged by this transformation.

For a minimum-weight carrier row \(x\), exactly \(a-1\) selected locators
vanish. Therefore \(\Psi(x)\) lies on exactly those same \(a-1\)
hypersurfaces \(\mathfrak H_i\), unless \(x\) is already in the printed
common residual divisor. The selected incidence pattern is unchanged.

## 6. Corrected geometric target

The minimum-window target can now be stated on the smaller curve:

> **Cremona-descended selected-vertex rigidity.**
> A birational source-partition curve
> \[
> \Psi_j
> =
> \Lambda_{\Sigma_j}\prod_{k\ne j}\widetilde R_k
> \]
> of degree bounded by (4.5) cannot meet the transformed selected-vertex
> arrangement with the forced weighted-GRS minimum-row census after the
> common divisor \(R_*^{a-2}\) is removed, unless an enabled same-record
> owner is emitted.

This target is equivalent to the endpoint minimum-row problem, but its
curve degree is smaller by approximately a factor \(a-1\). Its
hypersurfaces have degree \(a-1\), so a proof must exploit their common
Cauchy/Cremona form rather than apply a generic Bézout bound.

## 7. Nonclaims

This note does not prove the selected-vertex rigidity theorem, exclude a
minimum endpoint, handle window interiors, prove cap \(68\), or emit an
owner payment.
