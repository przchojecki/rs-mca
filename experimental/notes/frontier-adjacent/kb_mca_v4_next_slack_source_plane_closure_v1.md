---
title: KoalaBear next-slack source-plane closure
status: PROVED ZERO-CHARGE BRANCH PAYMENT; ROW OPEN
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
counted_object: DISTINCT BAD FINITE SLOPES ON THE FULL-OUTSIDE COEFFICIENT-RANK-TWO BRANCH
direct_statement: At slack r=67472, every post-C5 full-outside coefficient-rank-two line either lies in at most p+1 source-map images and is below the current reserve, or would force an impossible rank-excess source plane. Hence the complete slack is paid with zero additional owner charge.
ledger_movement: 0
falsifier: A post-C5 r=67472 line whose base-rational source-residue span has dimension three and whose reduced pair is simultaneously coprime and of exact degree 67473, or more than 4180887079739838 residual slopes in the base-span-at-most-two branch.
---

# KoalaBear next-slack source-plane closure

## 0. Result

The first slack after the paid source pencil is

\[
r=67{,}472.
\]

On the exact seven-owner residual, the full-outside
coefficient-rank-two branch at this slack is paid without adding an owner
atom:

\[
\boxed{
\#\{\text{retained bad finite slopes at }r=67{,}472\}
\le
4{,}180{,}887{,}079{,}739{,}838
<
270{,}780{,}212{,}960{,}575{,}880.}
\tag{0.1}
\]

The proof is a source-plane dichotomy.

1. If the base-rational span of the intrinsic source residue plane has
   dimension at most two, all selected slopes lie in the union of at most
   \(p+1\) finite source-map images. This gives (0.1).
2. If that span has dimension three, three base residue directions define a
   canonical reciprocal multiplier kernel. Dimension two is already owned
   by the active C5/base cell. Dimension at least three forces a polynomial
   rank-one normal form which is incompatible with the actual line being
   both coprime and of exact reduced degree.

Thus the second alternative is empty after C5 deletion, while the first is
below the current reserve. No global owner charge is spent, and the active
partition digest is unchanged.

## 1. Exact deployed arithmetic

Use the fixed KoalaBear values

\[
\begin{aligned}
p&=2{,}130{,}706{,}433,\\
n&=2{,}097{,}152,\\
k&=1{,}048{,}576,\\
a&=1{,}116{,}048,\\
j&=981{,}104,\\
t&=67{,}472.
\end{aligned}
\]

At \(r=t\), with the dangerous full-outside value \(x=1\), the source
cardinality is

\[
s=t+r+1=134{,}945.
\tag{1.1}
\]

The active source-rational threshold is

\[
E(s)=\left\lfloor\frac{s-1}{2}\right\rfloor=t.
\]

Post-source-rational deletion therefore forces reduced degree at least
\(t+1\), while the full-outside upper contract gives

\[
s+x-t-1=t+1.
\]

Consequently the reduced degree is exactly

\[
\boxed{e=67{,}473,\qquad s=2e-1.}
\tag{1.2}
\]

The forced common-root count is

\[
a-x-s=981{,}102=k-1-e,
\tag{1.3}
\]

so the forced split locator is again the complete monic gcd. The maximal
full-outside carrier is forced to be

\[
V=D\setminus\Sigma,\qquad |V|=n-s=1{,}962{,}207.
\tag{1.4}
\]

For every dangerous line,

\[
|Z_L|=|V|-(j+1)=981{,}102,\qquad
Y_L=V\setminus Z_L,\qquad |Y_L|=j+1=981{,}105.
\tag{1.5}
\]

These equalities are exact; no selector-derived carrier is imported.

## 2. The source interpolation space is exactly three-dimensional

Let \(F\) be the evaluation field. Write the translated source coordinates
as \((\epsilon_0,\epsilon_1)\), with

\[
(\epsilon_0(h),\epsilon_1(h))\ne(0,0)
\quad(h\in\Sigma).
\tag{2.1}
\]

Define

\[
\mathcal K_\Sigma(e)=
\left\{
(R,S)\in F[X]_{\le e}^2:
\epsilon_1(h)R(h)-\epsilon_0(h)S(h)=0
\text{ for all }h\in\Sigma
\right\}.
\tag{2.2}
\]

There are \(2(e+1)\) coefficients and \(s=2e-1\) constraints, so

\[
\dim_F\mathcal K_\Sigma(e)\ge3.
\tag{2.3}
\]

The point constraints are in fact independent.

### Lemma 2.1: independence of the source constraints

Assume \(\mathcal K_\Sigma(e)\) contains the actual coprime pair
\((R_*,S_*)\) with

\[
\max(\deg R_*,\deg S_*)=e.
\tag{2.4}
\]

Then the \(2e-1\) constraints in (2.2) are linearly independent. Hence

\[
\boxed{\dim_F\mathcal K_\Sigma(e)=3.}
\tag{2.5}
\]

#### Proof

Let

\[
\Lambda_\Sigma(X)=\prod_{h\in\Sigma}(X-h),\qquad
\rho_h=\Lambda_\Sigma'(h)^{-1}.
\]

The dual of the length-\(s\) Reed--Solomon evaluation code

\[
U_e=\{(P(h))_{h\in\Sigma}:\deg P\le e\}
\]

is

\[
U_e^\perp
=
\left\{
(\rho_hP(h))_{h\in\Sigma}:
\deg P\le s-e-2=e-3
\right\}.
\tag{2.6}
\]

Suppose coefficients \(c_h\) give a dependence among the constraints.
Testing the dependence separately against all \(R\) and all \(S\) yields
polynomials \(P_1,P_0\), each of degree at most \(e-3\), such that

\[
c_h\epsilon_1(h)=\rho_hP_1(h),\qquad
c_h\epsilon_0(h)=\rho_hP_0(h).
\tag{2.7}
\]

Therefore

\[
\epsilon_0(h)P_1(h)=\epsilon_1(h)P_0(h)
\quad(h\in\Sigma).
\tag{2.8}
\]

The actual pair satisfies

\[
\epsilon_1(h)R_*(h)=\epsilon_0(h)S_*(h).
\tag{2.9}
\]

Combining (2.8) and (2.9) gives

\[
R_*P_1-S_*P_0=0
\quad\text{on }\Sigma.
\]

Its degree is at most

\[
e+(e-3)=2e-3<s,
\]

so it is the zero polynomial. Coprimality of \(R_*,S_*\) implies

\[
S_*\mid P_1,\qquad R_*\mid P_0.
\]

At least one of \(R_*,S_*\) has degree \(e\), while both \(P_i\) have degree
at most \(e-3\). Hence \(P_0=P_1=0\). Equation (2.7), together with (2.1),
then gives \(c_h=0\) for every \(h\). This proves independence and (2.5).
\(\square\)

The exact dimension three is the decisive difference from the preceding
slack, where \(s=2e\) and the source space is a projective line.

## 3. Complement locators form one source residue plane

Let

\[
A_F=F[X]/(\Lambda_\Sigma),\qquad
U_F=\operatorname{im}(F[X]_{\le e}\to A_F).
\]

Since \(V\cap\Sigma=\varnothing\), \(\Lambda_V\) is a unit in \(A_F\). Put

\[
u_i=\Lambda_V^{-1}\epsilon_i\in A_F,\qquad i=0,1,
\tag{3.1}
\]

and define

\[
M_\Sigma(q)=q(u_0,u_1).
\]

The pointwise nonvanishing in (2.1) makes \(M_\Sigma\) injective. Every
kernel pair in (2.2) is pointwise proportional to
\((\epsilon_0,\epsilon_1)\), so \(M_\Sigma\) identifies

\[
W_\Sigma
=
\{q\in A_F:q u_0,q u_1\in U_F\}
\tag{3.2}
\]

with \(\mathcal K_\Sigma(e)\). Therefore

\[
\boxed{\dim_F W_\Sigma=3.}
\tag{3.3}
\]

For a split complement \(Y\subseteq V\), put

\[
q_Y=[\Lambda_Y]\in A_F.
\]

The exact identity

\[
\Lambda_{Z_L}\Lambda_{Y_L}=\Lambda_V
\]

shows that the reduced pair obtained after removing the full gcd is exactly

\[
q_{Y_L}(u_0,u_1).
\tag{3.4}
\]

Thus

\[
\boxed{
Y_L\text{ is source-admissible}
\iff
q_{Y_L}\in W_\Sigma.}
\tag{3.5}
\]

Because \(Y_L\) is disjoint from \(\Sigma\), every actual \(q_{Y_L}\) is an
invertible base-valued residue.

## 4. Base span at most two is paid directly

Let \(B=\mathbf F_p\), let

\[
A_B=B[X]/(\Lambda_\Sigma),
\]

and define the intrinsic base span

\[
W_B=W_\Sigma\cap A_B,\qquad b=\dim_BW_B.
\tag{4.1}
\]

Every actual complement locator lies in \(W_B\), so \(b\ge1\). Since base
independence remains independence after extending scalars and
\(\dim_FW_\Sigma=3\),

\[
b\in\{1,2,3\}.
\tag{4.2}
\]

The base-rational projective locus is exactly

\[
\mathbf P(W_B),
\]

and therefore has

\[
\frac{p^b-1}{p-1}
\tag{4.3}
\]

points.

Assume first that \(b\le2\). Then there are at most \(p+1\) projective
residue directions. For each direction \([q]\), let
\((R_q,S_q)\) be the unique degree-at-most-\(e\) representatives of
\(q(u_0,u_1)\), cancel their polynomial gcd, and define the finite image

\[
\mathcal I_q=
\left\{
\eta\in F:
[\eta:1]=[-R_q(x):S_q(x)]
\text{ for some }x\in D\setminus\Sigma
\right\}.
\tag{4.4}
\]

Uniqueness of the representatives follows from \(s>e\). The image has at
most \(n-s\) elements, without any injectivity assumption:

\[
|\mathcal I_q|\le n-s=1{,}962{,}207.
\tag{4.5}
\]

For every actual selected slope, the moving-root equation supplies
\(x\in D\setminus\Sigma\) and its actual \(q_Y\) such that

\[
R_{q_Y}(x)+\eta S_{q_Y}(x)=0,
\]

with the two values not both zero. Hence the same slope belongs to
\(\mathcal I_{q_Y}\). Therefore

\[
\begin{aligned}
\#\{\text{selected slopes}\}
&\le(p+1)(n-s)\\
&=2{,}130{,}706{,}434\cdot1{,}962{,}207\\
&=\boxed{4{,}180{,}887{,}079{,}739{,}838}.
\end{aligned}
\tag{4.6}
\]

The current reserve is

\[
B_{\rm rem}=270{,}780{,}212{,}960{,}575{,}880,
\]

and the exact margin is

\[
\boxed{
B_{\rm rem}-(p+1)(n-s)
=266{,}599{,}325{,}880{,}836{,}042>0.}
\tag{4.7}
\]

This is a direct branch count. It does not add the cap to the paid-owner
ledger.

## 5. Full base span and the triple reciprocal kernel

It remains to consider \(b=3\). Then \(W_\Sigma\) is the scalar extension
of \(W_B\). Choose an actual unit \(q_0=q_Y\) and extend it to a base basis

\[
q_0,q_1,q_2
\tag{5.1}
\]

of \(W_B\).

Define

\[
\mathcal R_3=
\{v\in A_B:q_iv\in U_B\text{ for }i=0,1,2\},
\tag{5.2}
\]

where \(U_B\) is the degree-at-most-\(e\) source evaluation code over \(B\).
If \(H_e\) is a parity matrix for \(U_B\), then

\[
\mathcal R_3
=
\ker
\begin{bmatrix}
H_e\operatorname{diag}(q_0)\\
H_e\operatorname{diag}(q_1)\\
H_e\operatorname{diag}(q_2)
\end{bmatrix}.
\tag{5.3}
\]

Here \(H_e\) has

\[
s-(e+1)=e-2=67{,}471
\]

rows. The matrix (5.3) is therefore canonical and base-defined, with
\(3(e-2)\) rows and \(2e-1\) columns.

Both actual source coordinates \(u_0,u_1\) belong to the scalar extension
of \(\mathcal R_3\), and they are independent. Thus

\[
\dim_B\mathcal R_3\ge2.
\tag{5.4}
\]

If equality holds, a base basis of \(\mathcal R_3\) spans the translated
source pair after extending scalars. Multiplication by the base-valued
carrier locator \(\Lambda_V\) gives a base-valued basis of the received
source pair. This is exactly the intrinsic projective-base conclusion
already removed by the active C5/base owner.

Consequently every nonempty post-C5 \(b=3\) branch would have to satisfy

\[
\dim_B\mathcal R_3\ge3.
\tag{5.5}
\]

The next section proves that (5.5) is incompatible with an actual coprime
exact-degree line.

## 6. Three-by-three polynomial rank-one theorem

Put

\[
r_3=\dim_B\mathcal R_3
\]

and assume \(r_3\ge3\). For \(v\in\mathcal R_3\), let

\[
P_v=(P_{0,v},P_{1,v},P_{2,v})^T\in B[X]_{\le e}^3
\tag{6.1}
\]

be the unique polynomial representatives of
\((q_0v,q_1v,q_2v)\).

Every source evaluation functional on \(\mathcal R_3\) is nonzero. Indeed,
its scalar extension contains \(u_0,u_1\), which are not simultaneously
zero at any source point. The union of the \(s\) resulting proper
hyperplanes has at most

\[
s p^{r_3-1}<p^{r_3}
\]

elements because \(s<p\). Hence there is a base vector
\(v_0\in\mathcal R_3\) which is nonzero at every source point. Extend it to
three independent vectors \(v_0,v_1,v_2\), and form

\[
\mathcal P(X)=
\begin{bmatrix}
P_{0,v_0}&P_{0,v_1}&P_{0,v_2}\\
P_{1,v_0}&P_{1,v_1}&P_{1,v_2}\\
P_{2,v_0}&P_{2,v_1}&P_{2,v_2}
\end{bmatrix}.
\tag{6.2}
\]

At every \(h\in\Sigma\),

\[
\mathcal P(h)
=
\begin{bmatrix}q_0(h)\\q_1(h)\\q_2(h)\end{bmatrix}
\begin{bmatrix}v_0(h)&v_1(h)&v_2(h)\end{bmatrix},
\tag{6.3}
\]

so it has rank one.

### Lemma 6.1: all polynomial minors vanish

\[
\boxed{\operatorname{adj}\mathcal P=0.}
\tag{6.4}
\]

#### Proof

Every \(2\times2\) minor has degree at most \(2e\), vanishes on all
\(2e-1\) source points, and is therefore \(\Lambda_\Sigma\) times a
polynomial of degree at most one. Thus

\[
\operatorname{adj}\mathcal P=\Lambda_\Sigma L(X),
\qquad \deg L_{ij}\le1.
\tag{6.5}
\]

Because \(\mathcal P(h)\) has rank at most one,
\(\operatorname{adj}\mathcal P(h)=0\). Jacobi's derivative formula gives

\[
(\det\mathcal P)'(h)
=
\operatorname{tr}
\bigl(\operatorname{adj}\mathcal P(h)\mathcal P'(h)\bigr)
=0.
\]

Thus every source point is a double root of \(\det\mathcal P\), and

\[
\Lambda_\Sigma^2\mid\det\mathcal P.
\]

But

\[
\deg\Lambda_\Sigma^2=4e-2>3e\ge\deg\det\mathcal P
\]

because \(e>2\). Hence

\[
\det\mathcal P=0.
\tag{6.6}
\]

Over \(B(X)\), the adjugate of a singular \(3\times3\) matrix has rank at
most one, so \(L\) has rank at most one. A nonzero rank-one matrix over the
PID \(B[X]\) factors as

\[
L=g\,a\,b^T
\tag{6.7}
\]

with primitive polynomial vectors \(a,b\). Since every entry has degree at
most one,

\[
\deg g+\max_i\deg a_i+\max_j\deg b_j\le1.
\]

Therefore at least one of \(a,b\) is a nonzero constant vector.

The identities

\[
\mathcal P L=L\mathcal P=0
\tag{6.8}
\]

follow from (6.5), (6.6), and the adjugate identities. If \(a\) is constant,
\(\mathcal P a=0\), giving a constant linear dependence among
\(v_0,v_1,v_2\): evaluate on \(\Sigma\) and use that \(q_0\) is a unit.
If \(b\) is constant, \(b^T\mathcal P=0\), giving a constant linear
dependence among \(q_0,q_1,q_2\): at each source point the vector of
\(v_i\)-values is nonzero because \(v_0\) was chosen to be a unit.
Both conclusions contradict the chosen bases.

Hence \(L=0\), proving (6.4). \(\square\)

The same argument, always retaining the unit \(v_0\) and adjoining an
arbitrary reciprocal vector to a suitable independent triple, shows that
every graph vector has zero cross minors with the initial graph columns.
Vectors already in their span satisfy this by linearity. Hence every two
graph vectors have all cross minors equal to zero.

### Lemma 6.2: reciprocal rational normal form

There is a primitive polynomial triple

\[
A=(A_0,A_1,A_2)\in B[X]^3,
\qquad \gcd(A_0,A_1,A_2)=1,
\tag{6.9}
\]

such that

\[
\boxed{
\{P_v:v\in\mathcal R_3\}
=
\{A\,T:T\in B[X]_{\le e-d}\},}
\tag{6.10}
\]

where

\[
\boxed{
d=\max_i\deg A_i=e-r_3+1\le e-2.}
\tag{6.11}
\]

Moreover,

\[
\boxed{
q_iA_0=q_0A_i
\quad\text{in }A_B,\qquad i=1,2.}
\tag{6.12}
\]

#### Proof

Factor the polynomial gcd from one nonzero graph vector, obtaining the
primitive triple \(A\). Vanishing of all \(2\times2\) minors makes every
other graph vector proportional to \(A\) over \(B(X)\). Since \(A\) is
primitive and \(B[X]\) is a PID, the proportionality factor is a polynomial.
The degree bound is at most \(e-d\).

At every source point, \(v_0\) is nonzero. Comparing
\(q_i v=A_iT\) and \(q_0v=A_0T\) at such a vector gives (6.12).

Conversely, because \(q_0\) is a unit, for every
\(T\in B[X]_{\le e-d}\) the residue

\[
v=q_0^{-1}[A_0T]
\]

satisfies \(q_iv=[A_iT]\in U_B\). Thus every allowed \(T\) occurs. Taking
dimensions gives \(r_3=e-d+1\), proving (6.10)--(6.11). \(\square\)

## 7. Rank excess contradicts the actual line

Recall that \(q_0=q_Y\) was chosen from an actual admitted complement
locator. The scalar extension of (6.10) applies to the actual source
coordinates:

\[
q_0u_0=A_0T_0,\qquad
q_0u_1=A_0T_1,
\qquad
\deg T_i\le e-d.
\tag{7.1}
\]

By (3.4), the left side is exactly the actual reduced polynomial pair after
removing the complete forced gcd. That pair is coprime and has exact
projective degree \(e\).

Coprimality in (7.1) forces \(A_0\) to be constant. Exact degree then
requires

\[
e\le e-d,
\]

so \(d=0\). All three \(A_i\) are constants. Since \(A_0\ne0\), (6.12)
then says that \(q_1,q_2\) are constant multiples of \(q_0\), contradicting
their base-field independence.

Therefore

\[
\boxed{
b=3,\quad \dim_B\mathcal R_3\ge3,\quad
\text{coprime exact degree }e
\quad\text{cannot occur}.}
\tag{7.2}
\]

The only \(b=3\) possibility has reciprocal dimension two and is already
removed by the active C5/base owner.

## 8. Exact branch closure

On the post-C5 seven-owner residual:

* \(b=3\) is empty by Sections 5--7;
* \(b\le2\) has at most the number of slopes in (4.6).

Since (4.6) is below the current reserve, the entire full-outside
coefficient-rank-two branch at \(r=67{,}472\) is paid.

This theorem does not:

* add a new owner cap to \(U_{\rm paid}\);
* change the active partition digest;
* import a historical selector;
* assume injectivity of any rational map;
* pay any slack \(r\ge67{,}473\);
* pay Q or balanced core; or
* close the KoalaBear row.

The exact successor open interval after the zero-charge branch replay is

```text
67,473..213,050
```

before any later reserve-dependent improvement.

## 9. Finite exact controls

The verifier contains the following non-load-bearing controls.

1. It exhausts all \(100{,}842\) coprime pairs over \(\mathbf F_7\) with
   a monic cubic first coordinate, a degree-at-most-two second coordinate,
   and no common source zero on five points. Every source kernel has
   dimension three and every full-base-span reciprocal kernel has dimension
   two.
2. It checks a structured rank-excess example at \(e=4,s=7\):
   \(u=(1,X^2)\), \(W=\langle1,X,X^2\rangle\), and
   \(\dim\mathcal R_3=3\). The resulting reduced degree is only two, so the
   example is rejected by the exact-degree guard, as the theorem predicts.
3. It checks the projective point counts \(1,4,13\) for base dimensions
   \(1,2,3\) over \(\mathbf F_3\).
4. It checks the exact deployed arithmetic and the strict reserve margin in
   (4.7).

# PROVED
