---
title: KoalaBear successor lower-stratum Segre-descent payment
status: PROVED LOWER-STRATUM PAYMENT; UPPER COMPANION PAID; SUCCESSOR SLACK CLOSED; ZERO ADDITIONAL CHARGE
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
counted_object: R=67473 FULL-OUTSIDE COEFFICIENT-RANK-TWO LINES OF REDUCED DEGREE 67473
direct_statement: In the lower reduced-degree stratum at r=67473, the forced-gcd branch is directly paid, the extra-gcd source space is a linear-polynomial tensor product, and any descended Segre quadric is forced split because Frobenius preserves the intrinsic lower-pencil factor. Hence the complete lower stratum is paid below the current reserve with zero additional owner charge.
ledger_movement: 0
falsifier: A lower-stratum record outside the stated slack split, an extra-gcd complement locator outside the Segre rank-one locus, a non-descended base rank-one locus exceeding the printed caps, or a full-base descended source quadric whose coefficient Frobenius exchanges rather than preserves the intrinsic linear-multiplier ruling.
---

# KoalaBear successor lower-stratum Segre-descent payment

## 0. Result

At

\[
r=67{,}473,\qquad s=134{,}946,
\]

this packet treats the lower reduced degree

\[
\boxed{e=67{,}473,\qquad s=2e.}
\tag{0.1}
\]

The exact slack simplex leaves two branches:

\[
(h,\ell)=(0,1)\quad\text{or}\quad(h,\ell)=(1,0).
\tag{0.2}
\]

The forced-gcd branch \(h=0\) is directly paid by the intrinsic
two-dimensional source-pencil image cap. In the extra-gcd branch \(h=1\),
adjoining one polynomial degree identifies the source space with

\[
F[X]_{\le1}\otimes_F\mathcal K_\Sigma(e).
\]

Actual complement locators are base-rational points of the resulting smooth
Segre quadric. Every non-descended branch is directly paid below the active
reserve. In the remaining descent case, the lower multiplier pencil has an
intrinsic characterization inside the enlarged space that is preserved by
coefficient Frobenius. Frobenius therefore preserves the linear-multiplier
ruling, so the descended quadric is split. Its quotient ruling has only
\(p+1\) directions and is directly paid as well.

Thus the complete lower stratum is paid with zero additional owner charge.
The companion upper theorem pays every occupied span, including the
span-three cyclic-quotient and span-four collective-rank branches. Together
the two packets close \(r=67{,}473\).

## 1. Exact slack split

Use

\[
n=2{,}097{,}152,\quad k=1{,}048{,}576,\quad
a=1{,}116{,}048,
\]

\[
j=981{,}104,\qquad t=67{,}472,\qquad x=1.
\]

The forced outside-source common-root count is

\[
c=a-x-s=981{,}101.
\tag{1.1}
\]

For the reduced degree in (0.1),

\[
u=e-x=67{,}472.
\]

The exact full-gcd slack identity

\[
h+u+\ell=r
\]

therefore becomes

\[
\boxed{h+\ell=1.}
\tag{1.2}
\]

Here

\[
h=\deg H-c,\qquad
\ell=k-1-\deg H-e.
\]

Thus (0.2) is exhaustive.

Put

\[
V=D\setminus\Sigma,\qquad |V|=n-s=1{,}962{,}206,
\]

and, for the actual common-zero set \(C\subseteq V\), put

\[
Y=V\setminus C,\qquad |Y|=j+1=981{,}105.
\tag{1.3}
\]

## 2. The degree-\(e\) source pencil

Define

\[
\mathcal K_e=
\left\{
(R,S)\in F[X]_{\le e}^2:
\epsilon_1(h)R(h)-\epsilon_0(h)S(h)=0
\quad(h\in\Sigma)
\right\}.
\tag{2.1}
\]

Since \(s=2e\), rank-nullity gives \(\dim_F\mathcal K_e\ge2\). The usual
leading-coefficient argument with the actual coprime exact-degree-\(e\) pair
gives equality:

\[
\boxed{\dim_F\mathcal K_e=2.}
\tag{2.2}
\]

For any basis \(U_0=(R_0,S_0),U_1=(R_1,S_1)\),

\[
\boxed{R_0S_1-R_1S_0=c_\Sigma\Lambda_\Sigma,\qquad
c_\Sigma\ne0.}
\tag{2.3}
\]

In particular, multiplication by a nonzero polynomial of degree at most one
cannot create a relation between \(U_0,U_1\).

## 3. Forced-gcd branch

If \(h=0\), then

\[
H=\Lambda_C.
\]

In the source residue algebra

\[
A_F=F[X]/(\Lambda_\Sigma)
\]

put

\[
u_i=\Lambda_V^{-1}\epsilon_i.
\]

The actual complement locator \(q_Y=[\Lambda_Y]\in A_B^\times\) satisfies

\[
q_Y(u_0,u_1)=(\bar P,\bar Q)\in\mathcal K_e.
\]

The multiplier space

\[
W_e=\{q:q u_0,q u_1\in U_e\}
\]

is isomorphic to \(\mathcal K_e\), hence has \(F\)-dimension two. Its
base-rational projective locus has at most \(p+1\) points. Each point defines
one reduced rational map whose finite image on \(D\setminus\Sigma\) has at
most \(n-s\) values. Therefore

\[
\#\Gamma_{h=0}
\le(p+1)(n-s)
=\boxed{4{,}180{,}884{,}949{,}033{,}404}.
\tag{3.1}
\]

The reserve margin is

\[
\boxed{266{,}599{,}328{,}011{,}542{,}476.}
\tag{3.2}
\]

This branch is paid with no new owner charge.

## 4. One-extra-gcd tensor normal form

Assume \(h=1\). Then

\[
H=\Lambda_CG,\qquad \deg G=1,
\tag{4.1}
\]

where \(G\) has no zero on \(\Sigma\). The source coupling and
\(\Lambda_V=\Lambda_C\Lambda_Y\) give

\[
\boxed{
q_Y(u_0,u_1)=G(\bar P,\bar Q).}
\tag{4.2}
\]

Define the degree-\(e+1\) source space

\[
\mathcal K_{e+1}=
\left\{
(R,S)\in F[X]_{\le e+1}^2:
\epsilon_1(h)R(h)-\epsilon_0(h)S(h)=0
\quad(h\in\Sigma)
\right\}.
\tag{4.3}
\]

Its constraints are independent. A dependence is represented by dual RS
polynomials of degree at most

\[
s-(e+1)-2=e-3.
\]

Crossing with the actual coprime exact-degree-\(e\) pair gives a polynomial
of degree at most \(2e-3<s=2e\), hence zero; coprimality then kills the dual
pair. Therefore

\[
\boxed{\dim_F\mathcal K_{e+1}=4.}
\tag{4.4}
\]

Multiplication gives a linear map

\[
\mu:F[X]_{\le1}\otimes_F\mathcal K_e
\longrightarrow\mathcal K_{e+1}.
\tag{4.5}
\]

It is injective. If

\[
A(X)U_0+B(X)U_1=0,\qquad \deg A,\deg B\le1,
\]

crossing with \(U_0\) and using (2.3) gives

\[
B\,c_\Sigma\Lambda_\Sigma=0,
\]

so \(B=0\), and then \(A=0\). Both sides of (4.5) have dimension four, so

\[
\boxed{\mathcal K_{e+1}\simeq
F[X]_{\le1}\otimes_F\mathcal K_e.}
\tag{4.6}
\]

The rank-one tensors form the smooth Segre quadric

\[
\mathcal Q\simeq\mathbf P^1_F\times\mathbf P^1_F
\subseteq\mathbf P(\mathcal K_{e+1})\simeq\mathbf P^3_F.
\tag{4.7}
\]

Under the multiplier isomorphism

\[
W_{e+1}=\{q:q u_0,q u_1\in U_{e+1}\}
\simeq\mathcal K_{e+1},
\tag{4.8}
\]

equation (4.2) says:

\[
\boxed{[q_Y]\in\mathcal Q.}
\tag{4.9}
\]

This is rooted at the actual complement locator; it is not an abstract
rank-one replacement.

## 5. Base-point counting

Put

\[
W_B=W_{e+1}\cap A_B,\qquad b=\dim_BW_B\le4.
\tag{5.1}
\]

Every actual \(q_Y\) lies in \(\mathbf P(W_B)\cap\mathcal Q\).

### 5.1 Base dimension at most two

If \(b\le2\), there are at most \(p+1\) projective points, giving the cap
(3.1).

### 5.2 Base dimension three

If \(b=3\), \(\mathbf P(W_B)\) is a projective plane. A smooth quadric
surface contains no projective plane, so the restriction of its quadratic
equation is nonzero. At least one base-coordinate component is a nonzero
homogeneous quadratic on \(\mathbf P^2_B\), with at most \(2(p+1)\)
base points. Hence

\[
\#\Gamma_{b=3}
\le2(p+1)(n-s)
=\boxed{8{,}361{,}769{,}898{,}066{,}808}.
\tag{5.2}
\]

### 5.3 Full base span without quadric descent

Assume \(b=4\), so a \(B\)-basis of \(W_B\) is also an \(F\)-basis of
\(W_{e+1}\). Write the Segre equation in that basis and expand its
coefficients in a fixed \(B\)-basis of \(F\):

\[
Q=\theta_1Q_1+\cdots+\theta_cQ_c,
\qquad Q_i\in B[z_0,z_1,z_2,z_3]_2.
\tag{5.3}
\]

Here \(1\le c\le[F:B]=6\). A base point lies on \(\mathcal Q\) exactly when
all \(Q_i\) vanish.

If \(c\ge2\), their common projective zero set has dimension at most one.
Otherwise it would contain a surface whose defining factor divides every
\(Q_i\), making the smooth irreducible quadric \(Q\) reducible or making
all coefficient components proportional. Bézout gives total degree at most

\[
2^c\le64.
\]

The standard projective degree bound therefore gives at most
\(64(p+1)\) base points. Consequently

\[
\#\Gamma_{c\ge2}
\le64(p+1)(n-s)
=\boxed{267{,}576{,}636{,}738{,}137{,}856},
\tag{5.4}
\]

which is below the active reserve by

\[
\boxed{3{,}203{,}576{,}222{,}438{,}024.}
\tag{5.5}
\]

The conservative factor \(64\) is intentional: it avoids choosing two
generic coefficient quadrics and still fits the deployed ledger.

## 6. Every descended source quadric is split

The only remaining case has

\[
b=4,\qquad c=1.
\tag{6.1}
\]

After scaling, \(\mathcal Q\) is a smooth quadric defined over \(B\). We
now show that its abstract nonsplit form cannot occur for this source
tensor.

Let

\[
\mathscr W_e=\{q:q u_0,q u_1\in U_e\},
\qquad
\mathscr W_{e+1}=\{q:q u_0,q u_1\in U_{e+1}\}.
\tag{6.2}
\]

Inside the source residue algebra, the lower pencil has the intrinsic
description

\[
\boxed{
\mathscr W_e=
\{q\in\mathscr W_{e+1}:Xq\in\mathscr W_{e+1}\}.}
\tag{6.3}
\]

The forward containment is immediate. Conversely, let
\(q,Xq\in\mathscr W_{e+1}\), and write

\[
q(u_0,u_1)=(R,S),\qquad \deg R,\deg S\le e+1.
\]

The products \(XR,XS\) also have representatives of degree at most
\(e+1\). Here

\[
e+2<s=2e,
\tag{6.4}
\]

so multiplication by \(X\) does not wrap modulo the source locator.
Therefore neither \(R\) nor \(S\) can have a nonzero coefficient in degree
\(e+1\), proving \(\deg R,\deg S\le e\) and hence (6.3).

Let \(\sigma:c\mapsto c^p\) be coefficient Frobenius. Full base span
\(b=4\) says

\[
\mathscr W_{e+1}=F\otimes_BW_B,
\]

so \(\sigma\) preserves \(\mathscr W_{e+1}\). Since \(X\in B[X]\),
\(\sigma(Xq)=X\sigma(q)\). Equation (6.3) therefore proves

\[
\boxed{\sigma(\mathscr W_e)=\mathscr W_e.}
\tag{6.5}
\]

The other tensor factor \(F[X]_{\le1}\) is visibly defined over \(B\), and
the multiplication isomorphism

\[
F[X]_{\le1}\otimes_F\mathscr W_e
\xrightarrow{\ \sim\ }\mathscr W_{e+1}
\tag{6.6}
\]

commutes with \(\sigma\). Thus both ruling factors of the Segre surface
descend separately to \(B\). Equivalently, coefficient Frobenius preserves
each ruling family. A nonsplit smooth quadric over a finite field is
characterized by Frobenius exchanging its two rulings, so it is impossible
here:

\[
\boxed{\text{every descended source quadric in (6.1) is split over }B.}
\tag{6.7}
\]

The quotient-source-pencil ruling therefore has a \(B\)-form and only
\(p+1\) projective quotient directions. Each contributes at most \(n-s\)
finite slopes, giving the direct cap (3.1).

## 7. Exact current boundary

All lower-stratum branches are paid with zero additional owner charge:

\[
\boxed{
\#\Gamma_{\rm lower}
\le
267{,}576{,}636{,}738{,}137{,}856
<
270{,}780{,}212{,}960{,}575{,}880.}
\tag{7.1}
\]

The alternatives in Sections 5--6 are determined by the one fixed
pair-global space \(W_B\) and its one coefficient quadric; they are not
record-by-record owner sets. Consequently (7.1) uses the maximum branch cap,
not a sum of mutually exclusive geometric cases.

The upper stratum at the same slack independently pays occupied span at
most two, span three by its one-dimensional cyclic quotient, and span four
by its transverse/three-step source images. The seven-owner ledger is
unchanged, and \(r=67{,}473\) is closed with zero additional charge.

## 8. Finite controls

The verifier checks:

* the exact deployed slack split and all four caps;
* the split smooth quadric over \(\mathbf F_7\), with \((p+1)^2=64\)
  points but only \(p+1=8\) quotient directions;
* a nonsplit smooth quadric over \(\mathbf F_7\), with \(p^2+1=50\)
  points, as a guardrail for the abstract form excluded by (6.7);
* an exact \(\mathbf F_{49}\), \(e=2\), \(s=4\) source-pencil instance in
  which ten base complement-residue points collapse to eight quotient-map
  directions; this boundary-size example is diagnostic only because
  \(e+2=s\), whereas the deployed no-wrap gate (6.4) is strict; and
* fail-closed status mutations.

# PROVED
