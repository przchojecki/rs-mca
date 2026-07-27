---
title: KoalaBear second-successor upper intrinsic-plane descent
status: PROVED COMPLETE UPPER-STRATUM PAYMENT AND WHOLE R=67474 SLACK CLOSURE WITH ZERO ADDITIONAL CHARGE
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
counted_object: R=67474, X=1, E=67475 FULL-OUTSIDE COEFFICIENT-RANK-TWO LINES
direct_statement: In the sole remaining r=67474 stratum, the source multiplier spaces have dimensions 5 and 3 at cutoffs e and e-1. A second direction at cutoff e-2 emits the active tangent/source-rational owner, giving the exact prolongation W_e=W_(e-1)+XW_(e-1). Intrinsic base spans at most two are directly paid; spans three and four admit pointwise cubic base relations that confine every moving-root pair to a base plane and therefore the same p+1 image cap; full base span five descends by a resultant pencil to the paid source plane and is impossible after C5. Together with the lower companion packet, the complete r=67474 slack is paid with zero additional charge.
ledger_movement: 0
falsifier: A post-source-rational record with dim W_(e-2)>=2 but no global degree-at-most-e-2 source map; a survivor with W_e != W_(e-1)+XW_(e-1); a span-three reciprocal product matrix lacking a primitive cubic relation nonzero at every base carrier root; a span-four saturated left kernel lacking two pointwise independent cubic relations; a full-base-span-five survivor whose scalar pencil has no coprime exact member; or more than 4180882818326970 selected slopes in the complete upper stratum.
---

# KoalaBear second-successor upper intrinsic-plane descent

## 0. Result

At

\[
r=67{,}474
\]

the only stratum not paid by the lower source-plane packet is

\[
x=1,\qquad e=67{,}475,\qquad
s=134{,}947=2e-3.
\tag{0.1}
\]

This note proves the complete upper-stratum payment.

\[
\boxed{
\begin{array}{c|c}
\text{intrinsic base dimension }b&\text{outcome}\\ \hline
b\le2&\text{directly paid by at most }(p+1)(n-s)\text{ slopes},\\
b=3&\text{one primitive cubic base relation at every carrier root},\\
b=4&\text{two pointwise independent cubic base relations},\\
b=5&\text{empty after source-rational and C5 deletion}.
\end{array}}
\tag{0.2}
\]

The proof also establishes the pair-global normal form

\[
\boxed{
W_e=W_{e-1}+XW_{e-1},\qquad
\dim W_e=5,\quad
\dim W_{e-1}=3,\quad
\dim W_{e-2}=1
}
\tag{0.3}
\]

on every active survivor. The intersection is exact:

\[
W_{e-1}\cap XW_{e-1}=XW_{e-2}.
\tag{0.4}
\]

For \(b=3,4\), the displayed relations force all admitted source-pair
values at each moving root into a two-dimensional \(B\)-subspace of
\(F^2\). Such a plane has at most \(p+1\) projective directions. Therefore
all \(b\le4\) cases share the direct cap, and \(b=5\) is empty. The lower
companion theorem already pays the other \(r=67{,}474\) strata, so the
whole slack closes without changing the owner ledger.

## 1. Deployed arithmetic

Use

\[
\begin{aligned}
p&=2{,}130{,}706{,}433,&
n&=2{,}097{,}152,\\
k&=1{,}048{,}576,&
a&=1{,}116{,}048,\\
j&=981{,}104,&
r&=67{,}474.
\end{aligned}
\]

For \(x=1\), the upper reduced degree is

\[
e=67{,}475,\qquad
s=t+r+1=134{,}947=2e-3.
\tag{1.1}
\]

The carrier and complement sizes are

\[
|D\setminus\Sigma|=n-s=1{,}962{,}205,
\]

\[
|Y|=j+1=981{,}105,\qquad
|Z|=981{,}100=k-1-e.
\tag{1.2}
\]

Hence the forced split gcd is complete. The direct \(p+1\)-image cap is

\[
\boxed{
(p+1)(n-s)
=4{,}180{,}882{,}818{,}326{,}970
}
\tag{1.3}
\]

and its margin below the current reserve is

\[
\boxed{
270{,}780{,}212{,}960{,}575{,}880
-4{,}180{,}882{,}818{,}326{,}970
=266{,}599{,}330{,}142{,}248{,}910>0.
}
\tag{1.4}
\]

## 2. Multiplier hierarchy

Let

\[
A_\Sigma=F[X]/(\Lambda_\Sigma)
\]

and let \(U_d\) be the source evaluation code represented by polynomials
of degree at most \(d\). Write the translated source coordinates as
\(u_0,u_1\in A_\Sigma\), with no simultaneous source zero. Define

\[
W_d=
\{q\in A_\Sigma:q u_0,q u_1\in U_d\}.
\tag{2.1}
\]

An actual complement locator \(q_*\) is a base-valued source unit, and

\[
q_*(u_0,u_1)=(R_*,S_*)
\tag{2.2}
\]

is the actual coprime reduced pair of exact projective degree \(e\).

### Lemma 2.1: the first two dimensions are exact

\[
\boxed{\dim_F W_e=5,\qquad \dim_F W_{e-1}=3.}
\tag{2.3}
\]

#### Proof

For a cutoff \(d\), the two multiplication tests impose

\[
2(s-d-1)
\]

linear conditions on the \(s\)-dimensional source residue algebra.
The expected nullities at \(d=e,e-1\) are respectively \(5,3\).

It remains to prove independence. A dependence among the source
constraints is represented, by Reed--Solomon duality, by two polynomials
\(P_0,P_1\) of degree at most

\[
s-d-2.
\]

Combining that dependence with (2.2) gives

\[
R_*P_1-S_*P_0=0
\quad\text{on }\Sigma.
\tag{2.4}
\]

For \(d=e\), its degree is at most

\[
e+(e-5)=2e-5<s.
\]

For \(d=e-1\), its degree is at most

\[
e+(e-4)=2e-4<s.
\]

Thus (2.4) is the zero polynomial in both cases. Coprimality and exact
degree of \((R_*,S_*)\) force \(P_0=P_1=0\). The constraints are
independent, proving (2.3). \(\square\)

At the next cutoff, dimension counting only gives

\[
\dim_F W_{e-2}\ge1.
\tag{2.5}
\]

The possibility of dimension two is real before first-match deletion; it
appears in the finite controls. The next lemma shows that it is not an
active residual branch.

## 3. Rank-one lower cutoff emits an earlier owner

### Lemma 3.1: two lower-cutoff directions give a global source map

If

\[
\dim_F W_{e-2}\ge2,
\tag{3.1}
\]

then the translated source labels are represented on every point of
\(\Sigma\) by one projective rational map of degree at most \(e-2\).

#### Proof

Choose independent \(q_0,q_1\in W_{e-2}\), and let

\[
P_{ir}=\operatorname{rep}_{\le e-2}(q_i u_r),
\qquad i,r\in\{0,1\}.
\]

The determinant

\[
\Delta=P_{00}P_{11}-P_{01}P_{10}
\]

vanishes on all \(s\) source points and has degree at most

\[
2e-4<s=2e-3.
\]

Hence \(\Delta=0\). Factor the polynomial rank-one matrix primitively:

\[
\begin{pmatrix}
P_{00}&P_{01}\\
P_{10}&P_{11}
\end{pmatrix}
=
\begin{pmatrix}H_0\\H_1\end{pmatrix}
\begin{pmatrix}A_0&A_1\end{pmatrix},
\tag{3.2}
\]

with

\[
\gcd(H_0,H_1)=1,\qquad
\gcd(A_0,A_1)=1.
\tag{3.3}
\]

At every \(h\in\Sigma\), some \(H_i(h)\) is nonzero. Equation (3.2) and
pointwise nonvanishing of \((u_0,u_1)\) then force \(q_i(h)\ne0\) and

\[
[u_0(h):u_1(h)]=[A_0(h):A_1(h)].
\tag{3.4}
\]

Both entries of the right side cannot vanish simultaneously by (3.3).
Also \(\max(\deg A_0,\deg A_1)\le e-2\), because every product in
(3.2) has degree at most \(e-2\). This proves the claim. \(\square\)

At (1.1),

\[
E(s)=\left\lfloor\frac{s-1}{2}\right\rfloor=e-2.
\]

A nonconstant map from Lemma 3.1 is exactly the already-active
pair-global source-rational predicate. A constant map puts every source
label at the same source-coordinate tangent value and is already removed
by the earlier tangent cell. Therefore an active survivor satisfies

\[
\boxed{\dim_F W_{e-2}=1.}
\tag{3.5}
\]

This is a semantic emission, not a new charge.

## 4. Exact first prolongation

Multiplication by \(X\) is injective on \(W_{e-1}\). Indeed, if \(Xq=0\)
in \(A_\Sigma\), then \(q\) vanishes at every nonzero source point. The
two degree-at-most-\((e-1)\) representatives of \(q u_0,q u_1\) have more
zeros than their degree and are zero. At a possible source point \(0\),
pointwise nonvanishing of the source pair forces \(q(0)=0\) as well.

Moreover,

\[
\boxed{
W_{e-1}\cap XW_{e-1}=XW_{e-2}.
}
\tag{4.1}
\]

The inclusion from right to left is immediate. Conversely, let
\(Xv=w\) with \(v,w\in W_{e-1}\). If \(P_r,Q_r\) are the
degree-at-most-\((e-1)\) representatives of \(vu_r,wu_r\), then

\[
XP_r-Q_r
\]

vanishes on \(\Sigma\), has degree at most \(e<s\), and is therefore zero.
Thus \(\deg P_r\le e-2\), so \(v\in W_{e-2}\). This proves (4.1).

Using (2.3), (3.5), and injectivity,

\[
\dim(W_{e-1}+XW_{e-1})=3+3-1=5=\dim W_e.
\]

Hence every active survivor has the exact normal form

\[
\boxed{W_e=W_{e-1}+XW_{e-1}.}
\tag{4.2}
\]

## 5. Intrinsic base span

Let \(B=\mathbf F_p\), let \(A_B=B[X]/(\Lambda_\Sigma)\), and put

\[
W_B=W_e\cap A_B,\qquad b=\dim_BW_B.
\tag{5.1}
\]

Every actual split complement locator belongs to \(W_B\), so \(b\ge1\).
Since \(\dim_FW_e=5\),

\[
b\in\{1,2,3,4,5\}.
\tag{5.2}
\]

If \(b\le2\), there are at most \(p+1\) projective base directions. The
actual moving-root equation puts every selected slope in the carrier image
of its actual direction. Each image has at most \(n-s\) elements, so the
complete branch is paid by (1.3).

## 6. A resultant-pencil descent

The remaining proved case is \(b=5\).

### Lemma 6.1: scalar pencil contains a coprime exact member

Let \(K\) be a field, let \(d\ge1\), and let

\[
A_i,B_i\in K[X]_{\le d}\qquad(i=0,1).
\]

Assume

\[
C_i=A_i+XB_i
\tag{6.1}
\]

are coprime and have exact projective degree \(d+1\). Then

\[
\mathcal R(T)=
\operatorname{Res}_X(A_0+TB_0,A_1+TB_1)
\tag{6.2}
\]

is a nonzero polynomial of degree at most \(2d\).

Consequently, if

\[
|K|>2d+1,
\tag{6.3}
\]

there is \(t\in K\) such that

\[
(A_0+tB_0,A_1+tB_1)
\]

is coprime and has exact projective degree \(d\).

#### Proof

The degree bound in (6.2) is the standard bihomogeneity bound for the
resultant. Suppose \(\mathcal R=0\). Over an algebraic closure, the two
polynomials

\[
A_i+TB_i\in\overline K[T,X]
\]

have a common irreducible factor \(H\).

If \(\deg_T H=0\), then \(H\) divides all four \(A_i,B_i\), and therefore
divides both \(C_i\), contradicting coprimality.

Otherwise \(\deg_T H=1\), because the two inputs are linear in \(T\).
Their cofactors are independent of \(T\), so

\[
A_i+TB_i=(h_0+Th_1)Q_i.
\tag{6.4}
\]

After putting \(T=X\),

\[
C_i=(h_0+Xh_1)Q_i.
\]

Coprimality forces \(h_0+Xh_1\) to be a nonzero constant. Exact degree
\(d+1\) then forces some \(Q_i\) to have degree \(d+1\). If \(h_1\ne0\),
the identity \(B_i=h_1Q_i\) contradicts \(\deg B_i\le d\). If \(h_1=0\),
then \(H=h_0\) is constant, also a contradiction. Thus \(\mathcal R\ne0\).

At most \(2d\) scalars are resultant roots. Exact degree can fail for at
most one further scalar, since the leading coefficient pair is affine in
\(t\) and \(C\) has degree \(d+1\). Condition (6.3) leaves a valid
scalar. \(\square\)

### Theorem 6.2: full base span five is empty after C5

Assume \(b=5\). Then \(W_e\) is the scalar extension of \(W_B\). The
intrinsic characterization

\[
W_{e-1}=\{v\in W_e:Xv\in W_e\}
\tag{6.5}
\]

follows by the same no-wrap argument as (4.1), so \(W_{e-1}\) is
base-defined.

Choose an actual base complement locator \(q\). By (4.2), write

\[
q=a+Xb,\qquad a,b\in W_{e-1}(B).
\tag{6.6}
\]

Let \(A_i,B_i\) be the degree-at-most-\((e-1)\) representatives of
\(a u_i,b u_i\). No wrap gives the polynomial identity

\[
\operatorname{rep}_{\le e}(q u_i)=A_i+XB_i.
\tag{6.7}
\]

The left side is the actual coprime exact-degree-\(e\) pair. Apply
Lemma 6.1 with \(d=e-1\). The deployed inequality

\[
p>2e-1
\tag{6.8}
\]

produces \(t\in B\) such that

\[
c=a+tb\in W_{e-1}(B)
\tag{6.9}
\]

has a coprime exact-degree-\((e-1)\) source pair.

Now

\[
s=2(e-1)-1,
\]

so \(W_{e-1}\) is exactly the three-dimensional source plane already
treated by the uniform source-plane theorem. Its base span is all three
dimensions. If its reciprocal dimension is two, the translated source
plane is base-defined and the active pair-global C5 owner deletes the
incoming residual. If its reciprocal dimension is at least three, the
three-by-three polynomial rank-one theorem contradicts the coprime exact
pair supplied by (6.9).

Thus no post-C5 \(b=5\) record survives:

\[
\boxed{b=5\Longrightarrow\text{earlier owner or contradiction}.}
\tag{6.10}
\]

The auxiliary pencil member is used only to prove a pair-global C5
conclusion or an algebraic contradiction. It is not charged as an
unrooted selected-slope image.

## 7. Reciprocal product matrix

It remains to pay \(b=3,4\). Choose a \(B\)-basis

\[
q_0,q_1,\ldots,q_{b-1}
\tag{7.1}
\]

of \(W_B\), with \(q_0\) an actual split-complement locator. Define the
base reciprocal space

\[
\mathcal R_b=
\{v\in A_B:q_iv\in U_B\text{ for }0\le i<b\},
\tag{7.2}
\]

where \(U_B\) is the degree-at-most-\(e\) source evaluation code. The
translated source coordinates belong to
\(F\otimes_B\mathcal R_b\), so

\[
\dim_B\mathcal R_b\ge2.
\tag{7.3}
\]

If equality holds, the source pair spans the scalar extension of one
base plane. This is precisely the pair-global projective-base C5
predicate and the incoming record has already been deleted. Thus a
post-C5 survivor has

\[
\dim_B\mathcal R_b\ge3.
\tag{7.4}
\]

Every source evaluation functional on \(\mathcal R_b\) is nonzero,
because its scalar extension contains the source pair and that pair has
no simultaneous source zero. Since \(s<p\), the union of the \(s\)
proper evaluation hyperplanes cannot cover \(\mathcal R_b\). Choose

\[
v_0\in\mathcal R_b
\quad\text{with}\quad
v_0(h)\ne0\quad(h\in\Sigma).
\tag{7.5}
\]

For \(v\in\mathcal R_b\), let \(P_{i,v}\in B[X]_{\le e}\) be the unique
representative of \(q_iv\). The full reciprocal graph has polynomial
rank at least two. Indeed, otherwise its scalar extension, evaluated on
the two source coordinates, would give

\[
R_*P_{i,1}-S_*P_{i,0}=0
\tag{7.6}
\]

for every \(i\), where \((R_*,S_*)=q_0(u_0,u_1)\) is the actual coprime
pair of exact projective degree \(e\). Coprimality gives

\[
(P_{i,0},P_{i,1})=H_i(R_*,S_*).
\]

The degree bound and exact degree \(e\) force every \(H_i\) to be a
constant. Pointwise nonvanishing of the source pair then makes every
\(q_i\) a constant multiple of \(q_0\), contrary to (7.1).

Consequently, \(v_0\) can be extended to independent
\(v_0,v_1,v_2\in\mathcal R_b\) such that the \(b\)-by-three matrix

\[
\mathcal P(X)=
\bigl(P_{i,v_j}(X)\bigr)_{
0\le i<b,\ 0\le j<3}
\tag{7.7}
\]

has polynomial rank at least two.

### Lemma 7.1: the reciprocal product matrix has rank two

\[
\boxed{\operatorname{rank}_{B(X)}\mathcal P=2.}
\tag{7.8}
\]

Every \(2\)-by-\(2\) minor of \(\mathcal P\) vanishes on \(\Sigma\), since

\[
\mathcal P(h)=
\bigl(q_i(h)\bigr)_i
\bigl(v_j(h)\bigr)_j
\tag{7.9}
\]

has rank one. Hence each such minor is

\[
\Lambda_\Sigma C(X),\qquad \deg C\le 2e-s=3.
\tag{7.10}
\]

Every \(3\)-by-\(3\) minor has a double zero at every source point. To see
this, differentiate its determinant: the adjugate of the rank-at-most-one
matrix at a source point is zero. Thus the derivative also vanishes.
Therefore

\[
\Lambda_\Sigma^2\mid\det\mathcal P_I
\tag{7.11}
\]

for every three-row submatrix \(\mathcal P_I\). But

\[
2s=4e-6>3e\ge\deg\det\mathcal P_I
\tag{7.12}
\]

at the deployed \(e\), so all three-by-three minors vanish. Together with
the rank lower bound above, this proves (7.8). \(\square\)

The cubic quotients in (7.10), rather than a linear shift chain, pay the
two proper base spans.

## 8. Base span three

Assume \(b=3\). Select two independent columns of \(\mathcal P\). Their
three signed \(2\)-by-\(2\) minors form a nonzero left-kernel vector.
After dividing by \(\Lambda_\Sigma\) and then by the polynomial gcd, one
obtains

\[
\mathbf a(X)=(a_0,a_1,a_2)\in B[X]^3,
\qquad
\max_i\deg a_i\le3,
\tag{8.1}
\]

such that

\[
\mathbf a^T\mathcal P=0,\qquad
\gcd(a_0,a_1,a_2)=1.
\tag{8.2}
\]

The relation annihilates every column because \(\mathcal P\) has rank
two. Primitivity implies

\[
\mathbf a(x)\ne0
\quad\text{for every }x\text{ in every extension of }B.
\tag{8.3}
\]

Apply (8.2) to the unit reciprocal column \(v_0\). At a source point,

\[
0=\sum_i a_i(h)q_i(h)v_0(h).
\]

Since \(v_0(h)\ne0\), this gives the source-algebra relation

\[
\sum_i a_iq_i=0\quad\text{in }A_B.
\tag{8.4}
\]

Let \(R_i,S_i\in F[X]_{\le e}\) represent \(q_i u_0,q_i u_1\). Multiplying
(8.4) by either source coordinate gives a polynomial of degree at most

\[
e+3<s=2e-3.
\tag{8.5}
\]

It vanishes on \(\Sigma\), so it is identically zero:

\[
\sum_i a_iR_i=0,\qquad
\sum_i a_iS_i=0.
\tag{8.6}
\]

Now use the deployed domain contract \(D\subset B\). At every carrier root
\(x\in D\setminus\Sigma\), (8.3) and (8.6) give a nonzero \(B\)-linear
relation among

\[
(R_i(x),S_i(x))\in F^2,\qquad 0\le i<3.
\tag{8.7}
\]

Their \(B\)-span therefore has dimension at most two.

## 9. Base span four

Assume \(b=4\), and choose two independent columns \(Q\) of
\(\mathcal P\). Put

\[
\mathcal K=\{\mathbf a\in B[X]^4:\mathbf a^TQ=0\}.
\tag{9.1}
\]

This rank-two polynomial module is saturated: if
\(\phi\mathbf a\in\mathcal K\) for nonzero \(\phi\in B[X]\), then
\(\phi(\mathbf a^TQ)=0\) in the domain \(B[X]\), and hence
\(\mathbf a\in\mathcal K\).

### Lemma 9.1: saturated polynomial kernel

There is a two-row basis matrix

\[
\mathcal A(X)\in B[X]^{2\times4}
\tag{9.2}
\]

of \(\mathcal K\) such that

\[
\deg_{\rm row}\mathcal A_1+
\deg_{\rm row}\mathcal A_2\le3
\tag{9.3}
\]

and

\[
\boxed{\operatorname{rank}_B\mathcal A(x)=2
\quad\text{for every }x\in\overline B.}
\tag{9.4}
\]

#### Proof

The \(2\)-by-\(2\) minors of \(Q\) are
\(\Lambda_\Sigma\) times cubics by (7.10). Divide those cubic quotients by
their common gcd. Their signed complementary coordinates are the
primitive Pluecker vector of \(\mathcal K\).

Because \(B[X]\) is a PID and \(\mathcal K\) is saturated, it has a
left-prime row basis whose maximal minors are exactly that primitive
Pluecker vector, up to a nonzero scalar. Put the basis in row-reduced
form. If its row degrees are \(\delta_1,\delta_2\), independence of the
leading row vectors gives a maximal minor of degree
\(\delta_1+\delta_2\). Every primitive Pluecker coordinate has degree at
most three, proving (9.3).

If the rank dropped at \(x\), all maximal minors would vanish there and
\(X-x\) would divide their gcd over \(\overline B[X]\), contradicting
primitivity. This proves (9.4). \(\square\)

Since the columns of \(Q\) span the rank-two column space of
\(\mathcal P\) over \(B(X)\), the polynomial identities extend to

\[
\mathcal A\mathcal P=0.
\tag{9.5}
\]

The unit column \(v_0\) again turns both rows of (9.5) into relations among
\(q_0,\ldots,q_3\) in \(A_B\). The same no-wrap calculation (8.5) turns
them into exact relations among the representative source pairs.
Evaluating at \(x\in D\subset B\), (9.4) supplies two independent
\(B\)-linear relations among the four vectors

\[
(R_i(x),S_i(x)),\qquad 0\le i<4.
\tag{9.6}
\]

Their \(B\)-span also has dimension at most two.

## 10. Direct payment and endpoint closure

For \(b=3\) or \(4\), fix a carrier root \(x\). Sections 8 and 9 place all
basis-pair values, and therefore the values of every actual
\(q\in W_B\), in one \(B\)-subspace

\[
V_x\subset F^2,\qquad \dim_BV_x\le2.
\tag{10.1}
\]

The actual moving-root pair is nonzero. Its slope is therefore one of at
most

\[
|\mathbf P(V_x)(B)|\le p+1
\tag{10.2}
\]

projective directions. Summing over the \(n-s\) carrier roots gives

\[
\#\{\text{selected slopes in the }b=3,4\text{ branches}\}
\le(p+1)(n-s),
\tag{10.3}
\]

the same cap as in the \(b\le2\) branch. The alternatives are disjoint,
so the complete \(b\le4\) upper stratum still has the single union cap
(1.3), not four added charges. Section 6 excludes \(b=5\).

Thus all five intrinsic base spans are paid:

\[
\boxed{
\#\{\text{selected slopes at }r=67{,}474,\ x=1,\ e=67{,}475\}
\le4{,}180{,}882{,}818{,}326{,}970
<B_{\rm rem}.}
\tag{10.4}
\]

The lower companion packet already pays \(x=0,e=67{,}474\) and
\(x=1,e=67{,}474\). Consequently

\[
\boxed{\text{the complete }r=67{,}474\text{ slack is paid}}
\tag{10.5}
\]

with zero additional owner charge and no partition change.

## 11. Finite regression

The hierarchy regression uses \(e=5\), \(s=7=2e-3\). Over \(1{,}000\)
deterministic coprime \(\mathbf F_{13}\) source pairs it finds:

```text
(dim W_e, dim W_(e-1), dim W_(e-2))
  (5,3,1): 999
  (5,3,2):   1

(dim(W_(e-1)+XW_(e-1)), dim intersection)
  (5,1): 999
  (4,2):   1
```

The exceptional row has the rank-one lower-cutoff behavior of Lemma 3.1.

A second scan uses \(250\) \(\mathbf F_{17}\) source pairs and all
\(\binom{10}{5}=252\) fixed-size split-locator ratios. It retains the
negative linear-shift guardrail:

```text
proper occupied span 3 with no linear shift relation: 34
proper occupied span 4 with only one linear shift direction: 6
```

It then computes all source relations with coefficient degree at most
three and evaluates their coefficient rows at every element of
\(\mathbf F_{17}\). The evaluated cubic relation rank profile is:

```text
(occupied span, minimum pointwise rank, maximum pointwise rank)
  (3,2,2):  2
  (3,2,3): 34
  (4,3,4):  6
```

This is stronger than the theorem's required ranks \(1\) and \(2\).
The finite calculations verify the construction and normalization; the
deployed proof is Lemmas 7.1 and 9.1.

# PROVED

* exact dimensions \(5,3\);
* lower-cutoff owner emission and survivor dimension one;
* exact first-prolongation normal form;
* reciprocal product-matrix rank two;
* direct payment for base spans one through four;
* full-base-span-five exclusion;
* complete upper-stratum payment;
* complete \(r=67{,}474\) slack closure with zero additional charge.

# CLOSED ENDPOINT

The post-\(r=67{,}474\) full-histogram replay is the next ledger action.
