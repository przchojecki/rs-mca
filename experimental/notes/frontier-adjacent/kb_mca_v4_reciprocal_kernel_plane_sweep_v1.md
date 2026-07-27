---
title: KoalaBear reciprocal-kernel plane sweep
status: PROVED ZERO-CHARGE PAYMENT ON R=67475..134942; FIRST OPEN SLACK R=134943
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
counted_object: SCALAR-UNPAID FULL-OUTSIDE COEFFICIENT-RANK-TWO SLOPES AT FIXED SLACK
direct_statement: For a normalized source packet with source size s=2e-c and e>2c, the base reciprocal product matrix either emits the active projective-base C5 owner or has rank two; its saturated left kernel supplies b-2 pointwise independent base relations of total row degree at most c. Every moving-root pair therefore lies in a base plane and the complete packet has at most (p+1)(n-s) slopes. The full-outside range identities make e>2c uniform for every scalar-unpaid stratum at r=67475 through 134942, paying that interval with zero additional charge.
ledger_movement: 0
falsifier: A scalar-unpaid record in r=67475..134942 outside the normalized range x0(r)<=x<=1 and ceil(s/2)<=e<=r+x; an extra-gcd normalization that changes the selected slope; a reciprocal product matrix of polynomial rank other than two after C5; a saturated left kernel whose pointwise rank drops; a relation product wrapping modulo Lambda_Sigma despite e>2c; or more than (p+1)(n-s) selected slopes at a fixed slack.
---

# KoalaBear reciprocal-kernel plane sweep

## 0. Result

The cubic relation payment at \(r=67{,}474\) is one case of a uniform
source theorem.

> **Reciprocal-kernel plane theorem.** Let
> \(B\subset F\), \(D\subset B\), and let one fixed source packet have
> source support \(\Sigma\), source size
> \[
> s=2e-c,\qquad c\ge0,\qquad e>2c.
> \]
> Normalize every actual record by dividing all extra common roots outside
> \(\Sigma\). If the normalized multipliers are base-valued source units and
> their source pairs are coprime of projective degree at most \(e\), with
> one occupied pair of exact degree \(e\), then after active C5 deletion all
> selected slopes lie in at most
> \[
> (p+1)(n-s)
> \]
> same-moving-root source-map values.

At the active KoalaBear full-outside scalar gap, this theorem applies
uniformly for

\[
\boxed{67{,}475\le r\le134{,}942.}
\tag{0.1}
\]

The largest cap in the interval occurs at its lower endpoint:

\[
(p+1)(n-s)
=4{,}180{,}880{,}687{,}620{,}536
<
270{,}780{,}212{,}960{,}575{,}880.
\tag{0.2}
\]

No new owner is inserted and the reserve does not change. The first slack
not covered by the strict degree inequality is

\[
\boxed{r=134{,}943.}
\tag{0.3}
\]

## 1. Exact scalar-unpaid range

Use

\[
t=67{,}472,\qquad
s=t+r+1=r+67{,}473.
\tag{1.1}
\]

For a scalar-unpaid full-outside graph line, the proved source restart and
moving-zero compiler give

\[
x_0(r)=\left\lceil\frac{s}{2}\right\rceil-r
\le x\le1.
\tag{1.2}
\]

The source-rational predecessor and full-outside degree contract give

\[
\left\lceil\frac{s}{2}\right\rceil
\le e\le s+x-t-1=r+x.
\tag{1.3}
\]

Put

\[
h=r+x-e,\qquad c=2e-s.
\tag{1.4}
\]

Then \(h,c\ge0\). The forced split gcd is short of the complete common gcd
by exactly \(h\) roots, all outside \(\Sigma\).

Let \(H\in B[X]\) be that extra common factor. It is a source unit. If
\(q_Y\) is the actual split-complement residue, define

\[
\bar q=H^{-1}q_Y\in A_B.
\tag{1.5}
\]

The products

\[
\bar q(u_0,u_1)=(R,S)
\tag{1.6}
\]

are coprime and have exact projective degree \(e\). At the actual moving
root \(x_{\rm mov}\), the selected pair is nonzero, so
\(H(x_{\rm mov})\ne0\). Dividing by that common scalar preserves the
selected slope exactly.

For one fixed packet, choose the largest occupied normalized degree \(e\).
All lower-degree normalized multipliers lie in the same cutoff space
\(W_e\). Thus one application of the theorem pays all degree and extra-gcd
subcases in that packet; their caps are not summed.

## 2. Exact source dimension

Set

\[
A_F=F[X]/(\Lambda_\Sigma),\qquad
U_e=\operatorname{im}(F[X]_{\le e}\to A_F),
\]

and define

\[
W_e=\{q\in A_F:q u_0,q u_1\in U_e\}.
\tag{2.1}
\]

The two multiplication tests have \(2(s-e-1)\) rows. They are independent.
Indeed, a dependence gives polynomials \(P_0,P_1\) of degree at most

\[
s-e-2=e-c-2
\]

and, using the occupied coprime exact pair \((R,S)\),

\[
RP_1-SP_0=0\quad\text{on }\Sigma.
\tag{2.2}
\]

Its degree is at most

\[
e+(e-c-2)=s-2<s,
\]

so it is the zero polynomial. Coprimality and exact degree force
\(P_0=P_1=0\). Therefore

\[
\boxed{\dim_FW_e=2(e+1)-s=c+2.}
\tag{2.3}
\]

Let

\[
W_B=W_e\cap A_B,\qquad b=\dim_BW_B.
\tag{2.4}
\]

If \(b\le2\), the standard projective image payment already gives at most
\((p+1)(n-s)\) slopes. Assume \(b\ge3\), choose an occupied normalized unit
\(q_0\), and extend it to a \(B\)-basis

\[
q_0,\ldots,q_{b-1}
\tag{2.5}
\]

of \(W_B\).

## 3. Reciprocal product matrix

Define

\[
\mathcal R_b=
\{v\in A_B:q_iv\in U_B\text{ for every }i\},
\tag{3.1}
\]

where \(U_B\) is the base degree-\(e\) evaluation code. The source
coordinates belong to \(F\otimes_B\mathcal R_b\), so
\(\dim_B\mathcal R_b\ge2\).

If equality holds, the source pair spans a base-defined plane after scalar
extension. This is exactly the active pair-global projective-base C5
predicate. A post-C5 survivor therefore has

\[
\dim_B\mathcal R_b\ge3.
\tag{3.2}
\]

Because \(s<p\), choose \(v_0\in\mathcal R_b\) nonzero at every source
point. Extend it to independent \(v_0,v_1,v_2\) for which the product matrix

\[
\mathcal P(X)=
\left(
\operatorname{rep}_{\le e}(q_i v_j)
\right)_{
0\le i<b,\ 0\le j<3}
\tag{3.3}
\]

has polynomial rank at least two. Such a choice exists: if the complete
reciprocal graph had rank one, its scalar extension on the source pair,
together with the coprime exact row belonging to \(q_0\), would make every
\(q_i\) a constant multiple of \(q_0\).

Every two-by-two minor vanishes on \(\Sigma\). Hence

\[
\det\mathcal P_{I,J}
=\Lambda_\Sigma C_{I,J},
\qquad
\deg C_{I,J}\le2e-s=c.
\tag{3.4}
\]

Every three-by-three minor has a double zero at each source point, because
the matrix there has rank at most one and therefore zero adjugate. Thus it
is divisible by \(\Lambda_\Sigma^2\). The strict hypothesis gives

\[
2s=4e-2c>3e,
\tag{3.5}
\]

so all three-by-three minors vanish. Consequently

\[
\boxed{\operatorname{rank}_{B(X)}\mathcal P=2.}
\tag{3.6}
\]

## 4. Saturated relation kernel

Choose two independent columns \(Q\) of \(\mathcal P\), and let

\[
\mathcal K=\{\mathbf a\in B[X]^b:\mathbf a^TQ=0\}.
\tag{4.1}
\]

This is a saturated free module of rank \(b-2\). The maximal minors of a
left-prime basis of \(\mathcal K\) are the signed complementary Pluecker
coordinates of \(Q\), after dividing their common factor. By (3.4), their
degrees are at most \(c\).

Choose a row-reduced basis matrix

\[
\mathcal A(X)\in B[X]^{(b-2)\times b}.
\tag{4.2}
\]

If its row degrees are \(\delta_1,\ldots,\delta_{b-2}\), row reduction and
the primitive maximal minors give

\[
\sum_i\delta_i\le c
\tag{4.3}
\]

and

\[
\boxed{\operatorname{rank}\mathcal A(x)=b-2
\quad(x\in\overline B).}
\tag{4.4}
\]

Because \(Q\) spans the rank-two column space of \(\mathcal P\),

\[
\mathcal A\mathcal P=0.
\tag{4.5}
\]

Apply this identity to the reciprocal unit \(v_0\). Its nonvanishing on
\(\Sigma\) turns every row into a source-algebra relation among the \(q_i\).
Multiplying by either source coordinate has polynomial degree at most

\[
e+\max_i\delta_i\le e+c<s=2e-c,
\tag{4.6}
\]

where the strict inequality is exactly \(e>2c\). Thus there is no modular
wrap: the \(b-2\) relations are exact polynomial identities among the
source-pair representatives.

At every moving root \(x\in D\subset B\), (4.4) supplies \(b-2\)
independent \(B\)-linear relations. Hence all \(b\) pair values span a
subspace

\[
V_x\subset F^2,\qquad \dim_BV_x\le2.
\tag{4.7}
\]

Every actual normalized multiplier belongs to their \(B\)-span. Its
nonzero moving-root value gives one of at most

\[
|\mathbf P(V_x)(B)|\le p+1
\tag{4.8}
\]

slopes. Summing over \(D\setminus\Sigma\) proves the theorem.

## 5. KoalaBear interval arithmetic

For every scalar-unpaid stratum, \(e\le r+1\). Therefore

\[
c=2e-s
\le2(r+1)-(r+67{,}473)
=r-67{,}471.
\tag{5.1}
\]

The worst case is \(e=r+1\). Its strict margin is

\[
e-2c
\ge(r+1)-2(r-67{,}471)
=134{,}943-r.
\tag{5.2}
\]

This is positive exactly for

\[
r\le134{,}942.
\]

At the lower and upper paid endpoints:

```text
r       s       e_max   c_max   e_max-2c_max   carrier
 67,475 134,948  67,476       4          67,468 1,962,204
134,942 202,415 134,943  67,471               1 1,894,737
```

The direct cap decreases with \(r\). At the first excluded slack:

```text
r=134,943
s=202,416
e_max=134,944
c_max=67,472
e_max-2c_max=0.
```

Both degree arguments fail sharply there:

\[
2s=3e_{\max},
\qquad
e_{\max}+c_{\max}=s.
\tag{5.3}
\]

Thus the theorem neither asserts nor suggests payment at \(r=134{,}943\).
That equality case is the exact next target.

## 6. Scope

This packet proves a direct zero-charge payment on the scalar-unpaid
full-outside interval (0.1). It does not:

* add an owner or change the partition digest;
* import a historical selector;
* assert the theorem when \(e\le2c\);
* pay \(r=134{,}943\);
* pay Q or balanced core; or
* close the KoalaBear row.

# PROVED
