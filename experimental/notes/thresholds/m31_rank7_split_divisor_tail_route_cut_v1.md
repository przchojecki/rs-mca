---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Every cumulative planted-zero-deficit head in the residual rank-seven master-denominator list is one source-bound affine-span RS list. The resulting sharp head histogram survives all currently proved scalar resources, including an exact harmonic resource primal and an explicit joint q-b integer marginal transport. An exact GF(31) positive-w family shows that full-gcd exactness and lcm restoration alone do not imply the missing tail bound.
architecture: M31_BASE_FIELD_BOUNDARY_RANK7_SPLIT_DIVISOR_TAIL_V1
atom_or_cell: Rank-seven residual route cut; no v4 atom value and no signed-Xi payment.
quantifier: Every base-field boundary-anchor rank-at-most-seven shallow family supplied by the exact master-denominator predecessor, for every residual union size 72428<=g<=354972.
claimed_bound: N_{<=Q}<=floor(binomial(R-g+w+7,7)/binomial(w-Q+7,7)) for 0<=Q<=min(w,g-w-1).
status: PROVED LOCAL THEOREM AND EXACT ROUTE CUT / ROW OPEN
impact: SHARP CUMULATIVE HEAD COMPILER / MISSING JOINT FULL-GCD INCIDENCE FROZEN
falsifier: A source family violating the cumulative head inequality; an all-g arithmetic cell differing from the sealed scan; failure of the exact GF(31) gcd/lcm/rank assertions; or a derivation of rank-seven payment using only the scalar constraints survived by the printed integer primal.
replay: Exact Python big-integer exhaustion, optimized-mode parity, proof-critical mutations, independent Sage GF(31) replay, sealed predecessor replay, and fresh independent proof review.
---

# M31 rank-seven split-divisor tail route cut

## Status and exact scope

This packet proves one positive source-bound theorem and one negative
current-hypothesis theorem.

First, if

\[
q_i=\deg\gcd(P,f_i)=g-\deg G_i,
\tag{0.1}
\]

then every cumulative head

\[
N_{\le Q}=\#\{i:q_i\le Q\}
\tag{0.2}
\]

obeys

\[
N_{\le Q}\le
C_Q(g):=
\left\lfloor
\frac{\binom{R-g+w+7}{7}}
     {\binom{w-Q+7}{7}}
\right\rfloor
\tag{0.3}
\]

for

\[
0\le Q\le\min(w,g-w-1).
\tag{0.4}
\]

This implication is rigorous and source-bound.

Second, the exact histogram which saturates every bound (0.3) survives
every presently proved scalar slice, colored, cross-block, affine-line,
and codimension-one harmonic constraint.  The harmonic constraints admit
an explicit integer primal at every one of the \(282\,545\) residual
values of \(g\), and a certified integer transport couples its two
mismatch classes to every row of the deficit histogram.  The narrowest
feasible interval has width \(122\).
Thus these current hypotheses cannot close rank seven.

The histogram is not asserted to arise from a deployed received word.
The packet therefore moves no ledger atom and does not close rank seven,
rank at least eight, or the M31 LIST row.

## 1. Source-bound cumulative-head theorem

The immediate predecessor supplies an exact master-denominator family
over

\[
\begin{aligned}
p&=2^{31}-1, &
n&=2\,097\,152, &
K&=1\,048\,576,\\
a&=1\,116\,023, &
R&=981\,129, &
w&=67\,447.
\end{aligned}
\tag{1.1}
\]

There are at least

\[
L=15\,775\,933
\tag{1.2}
\]

shallow nonanchors in a forbidden row.  The master normalization has

\[
P=\mathop{\rm lcm}_i G_i,\qquad
g=\deg P,\qquad
f_i=(P/G_i)b_i,\qquad
\deg f_i<g-w.
\tag{1.3}
\]

It preserves distinct codewords and zero-anchored linear rank.  On the
fixed domain

\[
D_P=Z(P)\mathbin{\dot\cup}E_0
\tag{1.4}
\]

the polynomial \(f_i\) agrees with one received table at \(g+s_i\)
points.  Exactly \(q_i\) of those planted agreements lie on \(Z(P)\).
Consequently \(q_i\le Q\) implies at least

\[
g+s_i-q_i\ge g-Q
\tag{1.5}
\]

agreements on \(E_0\).

The restriction of the complete normalized span to \(E_0\) has dimension
at most seven and message degree

\[
<g-w.
\tag{1.6}
\]

Evaluation on \(E_0\) is injective because \(g-w<R\), so this restriction
does not increase or ambiguously redefine the code-space dimension.
Therefore the \(q_i\le Q\) members lie in one rank-at-most-seven affine-span
list for

\[
\operatorname{RS}(E_0,g-w)
\tag{1.7}
\]

at agreement at least

\[
g-Q=(g-w)+(w-Q).
\tag{1.8}
\]

If their actual linear rank is \(k\le7\), the proved recursive affine-span
compiler gives the raw bound

\[
\frac{\binom{R-g+w+k}{k}}{\binom{w-Q+k}{k}}.
\tag{1.9}
\]

These raw bounds are nondecreasing in \(k\), because

\[
\frac{B^{\rm raw}_{k+1}}{B^{\rm raw}_k}
=
\frac{R-g+w+k+1}{w-Q+k+1}
\ge1;
\tag{1.10}
\]

the last inequality is \(R-g+Q\ge0\) on the deployed residual range.
Taking floors preserves the comparison.  Substitution of \(k=7\) now
gives

\[
\left\lfloor
\frac{\binom{R-(g-w)+7}{7}}
     {\binom{w-Q+7}{7}}
\right\rfloor,
\tag{1.11}
\]

which is exactly (0.3).

The upper restriction \(Q\le w\) keeps the excess in (1.8)
nonnegative.  Since \(f_i\ne0\), a divisor of \(f_i\) has degree at most
\(g-w-1\), giving the other restriction in (0.4).

No caps indexed by distinct exact divisors are summed here.  The theorem
uses one fixed received table and one cumulative subset of the complete
rank-seven span.

## 2. Exact \(Q_\star\) frontier

Put

\[
B_\star=16\,777\,215,\qquad
\text{deep}=1\,001\,282,\qquad
T=L-1=15\,775\,932.
\tag{2.1}
\]

For each residual \(g\), define

\[
Q_\star(g)=
\max\{Q:C_Q(g)\le T\},
\tag{2.2}
\]

with \(Q_\star(g)=-1\) when \(C_0(g)>T\).

The exact all-integer scan proves:

\[
Q_\star(g)=-1
\quad(72\,428\le g\le328\,677),
\tag{2.3}
\]

\[
Q_\star(328\,678)=0,
\qquad
Q_\star(354\,972)=2\,463.
\tag{2.4}
\]

There are \(2\,465\) maximal constant-\(Q_\star\) intervals.  Their
canonical interval-list hash is

```text
e3c0bc60f3c1e3918a2499cf1baa746f8dfd363c6d74f26af1a345ab5453787f
```

and their length histogram is

```text
7: 1, 10: 805, 11: 1658, 256250: 1.
```

At the final cell,

\[
\begin{aligned}
C_0(354\,972)&=12\,158\,497,\\
C_{2463}(354\,972)&=15\,774\,894,\\
C_{2464}(354\,972)&=15\,776\,593.
\end{aligned}
\tag{2.5}
\]

Thus a forbidden family would require at least

\[
L-C_{2463}(354\,972)=1\,039
\tag{2.6}
\]

members with \(q_i\ge2\,464\).  A closing theorem at this cell must bound
that tail by \(1\,038\).

Across the high-\(g\) frontier, the weakest required tail upper bound is

\[
U_{\rm tail}(g)=T-C_{Q_\star(g)}(g).
\tag{2.7}
\]

It ranges from \(0\) to \(1\,696\).  Seventeen exact cells require an empty
tail; the maximum \(1\,696\) occurs at

\[
(g,Q_\star)=(354\,165,2\,387).
\tag{2.8}
\]

## 3. Sharp histogram allowed by all head bounds

When \(Q_\star\ge0\), define

\[
\begin{aligned}
h_0&=C_0,\\
h_q&=C_q-C_{q-1}\quad(1\le q\le Q_\star),\\
h_{Q_\star+1}&=L-C_{Q_\star}.
\end{aligned}
\tag{3.1}
\]

When \(Q_\star=-1\), put \(h_0=L\).

Every entry is nonnegative, the total is \(L\), and

\[
\sum_{q=0}^Qh_q=C_Q
\qquad(0\le Q\le Q_\star).
\tag{3.2}
\]

Hence (3.1) saturates every cumulative head constraint.
Equivalently, among all deficit histograms satisfying those constraints,
it is stochastically smallest.  It therefore minimizes every
nondecreasing scalar cost of \(q\).

The exact layer-cake identity is

\[
\sum_q qh_q
=
\sum_{Q=0}^{Q_\star}(L-C_Q).
\tag{3.3}
\]

At \(g=354\,972\), it equals

\[
4\,678\,598\,254.
\tag{3.4}
\]

The largest proper bucket in the complete scan has size \(1\,700\), at

\[
(g,q)=(354\,957,2\,462).
\tag{3.5}
\]

Among the applicable rank-six fixed-slice ceilings, the smallest is

\[
B_6(354\,971)=1\,182\,429.
\]

Indeed every proper denominator has degree \(m\le354\,971\), and \(B_6(m)\)
is nonincreasing in \(m\), so every applicable ceiling is at least this
number.  The largest bucket is \(1\,180\,729\) below even that smallest
ceiling.  This only says the abstract load does not violate a numerical
slice ceiling.  An upper ceiling does not prove that a bucket is
source-realizable, nor that an aggregate degree bucket is one actual
fixed-divisor slice.  The uniform proper-slice upper theorem remains the
weaker global value \(9\,471\,941\).

## 4. Existing scalar inequalities do not close

Let

\[
M_1=\sum_q qh_q,\qquad
M_2=\sum_q q^2h_q.
\tag{4.1}
\]

The verifier substitutes (3.1), with common-support variables set to their
most permissive zero values, into the already proved resources:

\[
Lg(w+6)^{\underline6}
\le(R+g)^{\underline7},
\tag{4.2}
\]

\[
(gL-M_1)(w+6)^{\underline6}
\le R(R+g-1)^{\underline6},
\tag{4.3}
\]

\[
M_1(w+6)^{\underline6}
\le g(R+g-1)^{\underline6},
\tag{4.4}
\]

\[
(gM_1-M_2)\binom{w+5}{5}
\le gR\binom{R+g-2}{5},
\tag{4.5}
\]

and

\[
Lg\binom{w+6}{5}
\le15(R+g)\binom{R+g-1}{5}.
\tag{4.6}
\]

Every inequality holds at every residual \(g\).  The worst cells for
(4.2)--(4.6), in order, are

```text
(163521,-1), (196225,-1), (354972,2463),
(354972,2463), (196225,-1).
```

The exact ratios are sealed in the certificate.  Since one numerical
assignment satisfies all five inequalities simultaneously, no
nonnegative combination of these displayed scalar inequalities can
contradict it.

## 5. Exact harmonic primal and joint \(q\)--\(b\) marginal transport

The strongest presently available codimension-one envelope chooses the
proved truncated rank-six cap \(q_6(g)\), then sets

\[
d_6=1\,048\,582+q_6(g),
\qquad
e=R+g-d_6,
\qquad
\mathcal Q=w+1=67\,448.
\tag{5.1}
\]

For every residual cell,

\[
1\le e\le\mathcal Q.
\tag{5.2}
\]

Put

\[
\Pi_b=(d_6-R+b)\prod_{i=1}^5(w+i+b).
\tag{5.3}
\]

The exact two-point primal places \(x\) abstract members at mismatch
\(b=0\) and \(L-x\) at mismatch \(b=e\).  Its two resources are

\[
xe\Pi_0\le e\,d_6^{\underline6},
\tag{5.4}
\]

\[
x(\mathcal Q-e)\Pi_0
+(L-x)\mathcal Q\Pi_e
\le d_6^{\underline7}.
\tag{5.5}
\]

Thus

\[
\begin{aligned}
x_{\min}
&=
\max\left(
0,
\left\lceil
\frac{L\mathcal Q\Pi_e-d_6^{\underline7}}
     {\mathcal Q\Pi_e-(\mathcal Q-e)\Pi_0}
\right\rceil
\right),\\
x_{\max}
&=
\min\left(
L,
\left\lfloor\frac{d_6^{\underline6}}{\Pi_0}\right\rfloor
\right).
\end{aligned}
\tag{5.6}
\]

Exact exhaustion proves \(x_{\min}\le x_{\max}\) for every \(g\).  The
narrowest interval is at the final cell:

\[
\begin{aligned}
d_6&=1\,270\,586,&
e&=65\,515,\\
x_{\min}&=10\,411\,669,&
x_{\max}&=10\,411\,790.
\end{aligned}
\tag{5.7}
\]

It contains exactly \(122\) integers.

To make coexistence with the deficit histogram explicit, the verifier
constructs a nonnegative integer table

\[
n_{q,0},\qquad n_{q,e}.
\tag{5.8}
\]

It greedily fills the \(b=0\) column in increasing \(q\) order and puts
the remaining mass in the \(b=e\) column.  Thus

\[
n_{q,0}+n_{q,e}=h_q,\qquad
\sum_qn_{q,0}=x_{\min},\qquad
\sum_qn_{q,e}=L-x_{\min}.
\tag{5.9}
\]

For a word in row \(q\) and mismatch class \(b\), its minimum
\(E_0\)-agreement count \(g-q\) is split as \(e-b\) agreements on the
new support layer and

\[
g-q-(e-b)
\tag{5.10}
\]

agreements outside that layer.  Every cell placement is cardinality
feasible once

\[
g-q_{\max}-e\ge0,\qquad g+e\le R.
\tag{5.11}
\]

The verifier checks every nonzero table cell directly.  It also checks
(5.11) over the complete residual range: the smallest first margin is
\(72\,427\), and the smallest second margin is \(560\,642\).  The full
endpoint table is emitted in the certificate with canonical hash

```text
e2e89b305b732bad92e139d2bf89c0476f5bf89eb73b314a02b36361bba509ca
```

This is an exact integer point in the joint \(q\)--\(b\) marginal
relaxation, stronger than observing that a dual bound misses.  It does
not construct one common support layer \(T\), a rank-six hyperplane,
codeword agreement sets, a full-gcd family, or a received word.

## 6. Prefix-fiber full-gcd lemma

The failure of a tail-only argument is not merely numerical.

### Lemma 6.1 (prefix-fiber source family)

Let \(P=QG\) and \(L\) be coprime squarefree split polynomials over a
field.  Put \(Y=P\), corresponding to the unit choice \(H_0=V=1\).
Suppose \(A_E\mid L\) is monic,

\[
\deg A_E=\deg G=m,
\qquad
\deg(G-A_E)<m-w.
\tag{6.1}
\]

Define

\[
f=Q(G-A_E)=P-QA_E.
\tag{6.2}
\]

Then

\[
\deg f<\deg P-w,
\tag{6.3}
\]

\[
\gcd(P,f)=Q,
\qquad
\gcd(L,Y-f)=A_E,
\tag{6.4}
\]

and therefore

\[
\gcd(PL,Y-f)=QA_E.
\tag{6.5}
\]

The recovered canonical pair is

\[
G=P/Q,\qquad b=G-A_E,
\tag{6.6}
\]

with \(\gcd(b,G)=1\).

If in addition a monic \(A_\ast\mid L\) satisfies

\[
\deg A_\ast=\deg P,
\qquad
\deg(P-A_\ast)<\deg P-w,
\tag{6.7}
\]

then

\[
f_\ast=P-A_\ast
\tag{6.8}
\]

has \(\gcd(P,f_\ast)=1\), recovered denominator \(P\), and exact full gcd
\(A_\ast\).  Adding \(f_\ast\) restores the denominator lcm to \(P\).

### Proof

Equation (6.3) follows immediately from (6.1).  Since the roots of \(G\)
and \(A_E\) lie in the disjoint root sets of \(P\) and \(L\),

\[
\gcd(G,G-A_E)=\gcd(G,A_E)=1.
\]

This gives the first identity in (6.4).  Also

\[
Y-f=QA_E,
\]

and \(Q\mid P\) is coprime to \(L\), giving the second identity and (6.5).
The same argument with \(Q=1,G=P,A_E=A_\ast\) proves the restorer claim.

Condition (6.1) says that the top \(w\) nonleading coefficients of \(G\)
and \(A_E\) agree.  Thus the size of this exact source family is a genuine
prefix-fiber incidence problem, not a consequence of gcd exactness alone.

## 7. Exact positive-\(w\) GF(31) fixture

Take

\[
\begin{aligned}
F&=\mathbb F_{31},&
P&=\prod_{r=0}^7(X-r),&
L&=\prod_{r=8}^{30}(X-r),\\
w&=1,&
g&=8,&
\deg f&<7.
\end{aligned}
\tag{7.1}
\]

For each seven-subset

\[
T\subset\{8,\ldots,30\},
\qquad
\sum_{t\in T}t=28\pmod {31},
\tag{7.2}
\]

let

\[
H_T=\prod_{t\in T}(X-t),\qquad
G=P/X,\qquad
f_T=X(G-H_T)=P-XH_T.
\tag{7.3}
\]

Both \(G\) and \(H_T\) are monic of degree seven with root sum \(28\).
Hence \(\deg(G-H_T)<6\) and \(\deg f_T<7\).  Lemma 6.1 gives

\[
\gcd(P,f_T)=X,
\qquad
\gcd(PL,P-f_T)=XH_T.
\tag{7.4}
\]

Exact enumeration gives

\[
\#\{T\text{ satisfying }(7.2)\}=7\,864.
\tag{7.5}
\]

For the lcm restorer, take

\[
T_\ast=\{8,9,10,11,12,13,28,30\}.
\tag{7.6}
\]

Its root sum is also \(28\pmod {31}\).  With

\[
H_\ast=\prod_{t\in T_\ast}(X-t),
\qquad
f_\ast=P-H_\ast,
\tag{7.7}
\]

we have \(\deg f_\ast<7\),

\[
\gcd(P,f_\ast)=1,
\qquad
\gcd(PL,P-f_\ast)=H_\ast.
\tag{7.8}
\]

The \(7\,865\) messages are distinct, have exact linear rank seven, agree
with \(Y=P\) on exactly eight of the 31 field points, have no common zero
on \(Z(P)\), and have recovered-denominator lcm exactly \(P\).  Their
deficit histogram is

\[
h_0=1,\qquad h_1=7\,864.
\tag{7.9}
\]

Python and an independent Sage implementation replay every gcd and rank
claim.  Replacing the final restorer root \(30\) by \(29\) breaks the
degree gate, providing a negative control.

This is a rigorous small-field source family.  It is not a lower bound for
the deployed M31 list.

## 8. Frozen missing theorem

For

\[
328\,678\le g\le354\,972,
\tag{8.1}
\]

the exact missing high-\(g\) statement is

\[
\#\{i:q_i\ge Q_\star(g)+1\}
\le
15\,775\,932-C_{Q_\star(g)}(g).
\tag{8.2}
\]

It must use more than exact full gcds, the absence of a common planted
zero, and lcm restoration, because Section 7 satisfies all three gates.
The natural missing input is a joint prefix-fiber/full-gcd incidence
theorem coupling the tail divisors to the received table and the
rank-seven span.

For

\[
72\,428\le g\le328\,677,
\tag{8.3}
\]

we have \(C_0(g)\ge L\).  A tail theorem alone cannot close these cells.
They require either a stronger deterministic fixed-\(G\) ordinary-RS
bound or a genuine head-tail coexistence/refund theorem.

The unified terminal is therefore

```text
JOINT_HEAD_TAIL_FULL_GCD_INCIDENCE
```

with an explicit low-\(g\) ordinary-RS branch.

## 9. Verdict

- **GREEN, local theorem:** the cumulative bound (0.3).
- **GREEN, exact arithmetic:** the full \(282\,545\)-cell frontier and
  sharp histogram.
- **GREEN, route cut:** one exact harmonic resource primal and joint
  \(q\)--\(b\) marginal transport survive every current scalar resource.
- **GREEN, small-field control:** the GF(31) full-gcd/lcm-restored
  rank-seven source family.
- **YELLOW, global proof:** rank seven and the M31 LIST row remain open.

There is no layer-cake summability issue beyond the finite exact identity
(3.3), and no Markov, moment optimization, or asymptotic passage is used.
