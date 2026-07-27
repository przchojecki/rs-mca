---
title: KoalaBear second-successor lower source-plane payments
status: PROVED X=0 AND X=1 LOWER-STRATUM PAYMENTS; ZERO ADDITIONAL CHARGE; DIMENSION-FIVE UPPER STRATUM OPEN
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
counted_object: R=67474 FULL-OUTSIDE COEFFICIENT-RANK-TWO LINES WITH REDUCED DEGREE 67474
direct_statement: At r=67474, every reduced-degree-67474 branch descends to the same s=2e-1 source plane. For x=0 the split gcd is complete. For x=1, division by the one extra outside-source gcd factor produces the actual coprime degree-e pair without changing its selected slope. The source-plane theorem pays both strata by at most (p+1)(n-s) slopes.
ledger_movement: 0
falsifier: A reduced-degree-67474 record at r=67474 outside the exact s=2e-1 source-plane interface after removing its complete or one-extra gcd, a moving root at which the extra gcd factor vanishes while the selected reduced pair is nonzero, a post-C5 full-base-span source plane carrying a coprime exact-degree reduced pair, or more than 4180882818326970 selected slopes in either base-span-at-most-two branch.
---

# KoalaBear second-successor lower source-plane payments

## 1. Exact stratum

At the new first open slack

\[
r=67{,}474
\]

take \(x=0\). The source size is

\[
s=t+r+1=134{,}947.
\]

The source-rational threshold forces reduced degree at least

\[
\left\lfloor\frac{s-1}{2}\right\rfloor+1=67{,}474,
\]

while the full-outside upper contract gives

\[
e\le s+x-t-1=67{,}474.
\]

Therefore

\[
\boxed{e=67{,}474,\qquad s=2e-1.}
\tag{1.1}
\]

The forced common-root degree is

\[
a-x-s=981{,}101=k-1-e.
\tag{1.2}
\]

The carrier and actual complement sizes are

\[
|V|=n-s=1{,}962{,}205,\qquad |Y|=j+x=981{,}104,
\]

so

\[
|Z|=|V|-|Y|=981{,}101.
\tag{1.3}
\]

Thus the forced common divisor is exactly the complete split zero locator.
There is no defect root and no lower-degree alternative in this stratum.

## 2. Uniform source-plane theorem

The source interpolation space has

\[
2(e+1)-s=3
\]

dimensions. The proof in
`kb_mca_v4_next_slack_source_plane_closure_v1.md` uses only:

* \(s=2e-1\);
* a pointwise nonzero translated source pair;
* a coprime actual reduced pair of exact projective degree \(e\);
* the complete forced split gcd;
* \(e>2\) and \(s<p\); and
* active C5 deletion of reciprocal dimension two.

All six conditions hold in (1.1)--(1.3). Hence its source-constraint
independence, source-residue plane, full-base-span reciprocal kernel, and
three-by-three polynomial rank-one contradiction apply verbatim with
\(e=67{,}474\).

In particular, full base span three is impossible after C5: reciprocal
dimension two is C5-owned, while dimension at least three would force a
polynomial rational normal form incompatible with coprime exact degree.

## 3. Direct payment

Base span at most two has at most \(p+1\) projective source-residue
directions. For each direction the actual moving-root equation puts every
selected slope in one finite source-map image of size at most \(n-s\).
Therefore

\[
\begin{aligned}
\#\{\text{selected }x=0\text{ slopes at }r=67{,}474\}
&\le(p+1)(n-s)\\
&=2{,}130{,}706{,}434\cdot1{,}962{,}205\\
&=\boxed{4{,}180{,}882{,}818{,}326{,}970}.
\end{aligned}
\tag{3.1}
\]

The active reserve margin is

\[
270{,}780{,}212{,}960{,}575{,}880
-4{,}180{,}882{,}818{,}326{,}970
=266{,}599{,}330{,}142{,}248{,}910>0.
\tag{3.2}
\]

This is a direct branch payment and spends no owner charge.

## 4. The \(x=1\), lower-degree stratum

For \(x=1\), the lower reduced degree is again \(e=67{,}474\). The forced
outside-source split gcd has degree

\[
a-1-s=981{,}100,
\]

one less than \(k-1-e=981{,}101\). The exact slack identity therefore
supplies one additional common linear factor \(G\), with its root outside
\(\Sigma\). After removing the forced split gcd, write the actual pair as

\[
q_Y(u_0,u_1)=G(\overline P,\overline Q),
\qquad
\gcd(\overline P,\overline Q)=1,
\quad
\max(\deg\overline P,\deg\overline Q)=e.
\tag{4.1}
\]

Since \(G\) is a base polynomial and a source unit, define

\[
\overline q=G^{-1}q_Y\in A_\Sigma.
\tag{4.2}
\]

Then \(\overline q\) is base-rational and

\[
\overline q(u_0,u_1)=(\overline P,\overline Q).
\tag{4.3}
\]

For the actual moving root \(x_{\rm mov}\), the selected reduced pair is
nonzero. Equation (4.1) therefore forces \(G(x_{\rm mov})\ne0\), and
division by this scalar leaves the selected slope unchanged. Consequently
the selected slope lies in the same finite source-map image defined by
\(\overline q\).

The base span of all such \(\overline q\) directions is a subspace of the
same three-dimensional source plane. If its dimension is at most two, the
direct payment (3.1) applies. If it has dimension three, the reciprocal
kernel and polynomial rank-one proof consume only one actual base unit
whose source products are a coprime exact-degree pair. Equation (4.3)
supplies that unit. Reciprocal dimension two is active-C5-owned; dimension
at least three contradicts coprime exact degree. Hence the full-span branch
is empty after C5.

Thus the complete \(x=1,e=67{,}474\) stratum is paid by the same cap (3.1).

## 5. Remaining endpoint stratum

At the same slack \(r=67{,}474\), only the upper \(x=1\) degree remains.
The complete degree split was

\[
\begin{array}{c|c|c|c}
e&h&\ell&\text{source dimension}\\ \hline
67{,}474&1&0&3\\
67{,}475&0&1&5.
\end{array}
\]

The lower \(x=1\) branch is paid by Section 4. The sole remaining branch has

\[
x=1,\qquad e=67{,}475,\qquad s=2e-3,
\qquad \dim\mathcal K_\Sigma(e)=5.
\]

It has the complete forced split gcd. This dimension-five upper stratum is
not paid by this packet.

# PROVED
