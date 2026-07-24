---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The exact lcm master-denominator normalization turns every rank-seven shallow family into one planted-zero fixed-syndrome RS list. Every proper fixed-G slice then has rank at most six and at most 9471941 members, while a pure full-union fixed-G family is impossible for g>=328678. A reciprocal-convex harmonic dual separately pays the 26 rank-seven union sizes 354973..354998, leaving 72428<=g<=354972.
architecture: M31_BASE_FIELD_BOUNDARY_RANK7_MASTER_DENOMINATOR_V1
atom_or_cell: Direct source-bound rank-seven residual cut; no v4 atom value and no signed-Xi payment.
quantifier: Every base-field boundary-anchor shallow family of zero-anchored linear rank seven supplied by the exact predecessor chain.
projection_and_unit: Exact canonical nonanchor pairs for one arbitrary base-field unit V. The normalization preserves distinct codewords, rank, exact agreement, and the full gcd.
claimed_bound: Local rank-seven fixed-slice theorem and a 26-value uniform codimension-one payment. Rank seven, every rank at least eight, and the M31 LIST row remain open.
status: PROVED LOCAL / ROW OPEN
impact: SOURCE-BOUND ROUTE CUT / RANK-SEVEN RESIDUAL SHRINK
falsifier: A proper G slice of rank seven; a failure of the exact gcd identity; a fixed-G list exceeding the printed affine-span cap; a harmonic dual weight of negative sign; a profile at 354973..354998 exceeding 15775932; or any attempt to sum per-G caps without a new global incidence theorem.
replay: Exact Python big-integer scan, optimized-mode parity, proof-critical mutations, independent Sage finite-field and arithmetic replay, sealed predecessor replay, and fresh independent proof review.
---

# M31 rank-seven shallow master-denominator cut

## Status and exact scope

This packet proves two new local theorems.

1.  The complete rank-seven shallow family has an exact
    master-denominator normalization.  Relative to its exact locator lcm
    \(P\), every proper fixed-\(G\) slice loses at least one linear rank.
    The recursive affine-span compiler then gives

    \[
    |\mathcal I_G|\le 9\,471\,941
    \qquad(G<P).
    \]

    The full-union slice \(G=P\) can retain rank seven, but a family
    supported only on that slice is impossible for

    \[
    g=\deg P\ge 328\,678.
    \]

2.  A sharpened dual for the proved codimension-one recursion pays all
    rank-seven union sizes

    \[
    354\,973\le g\le354\,998.
    \]

Together with the predecessor packet, every surviving rank-seven shallow
family now has

\[
72\,428\le g\le354\,972.
\tag{0.1}
\]

This is a proved local route cut, not row closure.  It does not sum caps
over different \(G\), exclude a mixed-\(G\) family, touch rank at least
eight, or move a Grande Finale v4 ledger atom.

## 1. Source-bound shallow family

The exact predecessor chain supplies a boundary-anchor family over
\(\mathbb F_p\), where

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

The boundary agreement and error locators \(A_0,L_0\) are coprime,
squarefree, and split, with

\[
\deg A_0=a,\qquad \deg L_0=R.
\]

The received word has the form \(U=A_0H_0\), where \(H_0\) is a unit
modulo \(L_0\), and \(V H_0\equiv1\pmod {L_0}\).

A canonical nonanchor pair is

\[
\begin{aligned}
&G\mid A_0,\qquad m=\deg G,\qquad w+1\le m\le R,\\
&0\ne b,\qquad \deg b<m-w,\qquad \gcd(b,G)=1,\\
&H=\gcd(L_0,G-bV),\qquad \deg H=m+s.
\end{aligned}
\tag{1.2}
\]

Its codeword is

\[
c=\frac{A_0}{G}b,
\tag{1.3}
\]

and its excess agreement is \(s\).  The proved deep-tail cut says that a
forbidden row leaves at least

\[
L=15\,775\,933
\tag{1.4}
\]

distinct shallow nonanchors satisfying

\[
0\le s\le366\,886.
\tag{1.5}
\]

This packet treats the stratum for which the linear span of the translated
codewords \(c\), after adjoining the zero boundary anchor, has dimension
exactly seven.  “Rank” below always means this zero-anchored linear rank.

## 2. Exact master denominator

Let \(\mathcal I\) be the complete selected shallow family and define

\[
P=\operatorname{lcm}_{i\in\mathcal I}G_i,\qquad
g=\deg P,\qquad
Q_i=\frac P{G_i},\qquad
f_i=Q_i b_i.
\tag{2.1}
\]

Because every \(G_i\) divides the squarefree polynomial \(A_0\), so does
\(P\).  Put

\[
d=g-w,\qquad M=PL_0,\qquad Y=PH_0.
\tag{2.2}
\]

### Theorem 2.1 (master-denominator equivalence)

For every \(i\),

\[
\deg f_i<d,\qquad
c_i=\frac{A_0}{P}f_i,
\tag{2.3}
\]

and

\[
\gcd(M,Y-f_i)=Q_iH_i.
\tag{2.4}
\]

Consequently

\[
\deg\gcd(M,Y-f_i)=g+s_i.
\tag{2.5}
\]

Multiplication by \(A_0/P\) is injective, so

\[
\dim\operatorname{span}\{c_i\}
=
\dim\operatorname{span}\{f_i\}.
\tag{2.6}
\]

Moreover the \(f_i\) have no common zero on \(Z(P)\).

Conversely, for a nonzero polynomial \(f\) of degree \(<d\), put

\[
Q=\gcd(P,f),\qquad G=P/Q,\qquad b=f/Q.
\tag{2.7}
\]

Subject to the source degree gate \(w+1\le\deg G\le R\), the full gcd
condition in (2.4), and the shallow excess gate, (2.7) recovers the
canonical pair uniquely.  For a family, exactness of
\(P=\operatorname{lcm}G_i\) is equivalent to the absence of a common zero
on \(Z(P)\).

### Proof

The degree and codeword identities are immediate:

\[
\deg f_i
<
(g-m_i)+(m_i-w)=g-w
\]

and

\[
\frac{A_0}{P}f_i
=
\frac{A_0}{G_i}b_i.
\]

For the gcd identity, \(Y\) is divisible by \(P\), while
\(\gcd(b_i,G_i)=1\).  Since \(P=Q_iG_i\) is squarefree,

\[
\gcd(P,Y-f_i)=\gcd(P,f_i)=Q_i.
\tag{2.8}
\]

Modulo \(L_0\), multiplication by the units \(V\) and \(Q_i\) gives

\[
V(Y-f_i)
\equiv P-Q_i b_iV
=Q_i(G_i-b_iV).
\tag{2.9}
\]

Thus

\[
\gcd(L_0,Y-f_i)=\gcd(L_0,G_i-b_iV)=H_i.
\tag{2.10}
\]

The factors \(P\) and \(L_0\) are coprime, so (2.8)--(2.10) prove
(2.4).  Injectivity in (2.6) follows because \(\mathbb F_p[X]\) is a
domain.

If \(\alpha\in Z(P)\), exactness of the lcm supplies an index \(j\) with
\(\alpha\in Z(G_j)\).  Squarefreeness gives \(Q_j(\alpha)\ne0\), and
coprimality gives \(b_j(\alpha)\ne0\).  Hence
\(f_j(\alpha)\ne0\), proving the no-common-zero assertion.

Conversely, maximality of \(Q=\gcd(P,f)\), together with squarefreeness,
gives \(\gcd(b,G)=1\).  Reversing (2.8)--(2.10) recovers the canonical
full gcd \(H\), the agreement excess, and the original codeword.  Finally,
a common zero \(\alpha\in Z(P)\) occurs exactly when no recovered
denominator \(G_i\) contains \(\alpha\), which is exactly the failure of
their lcm to equal \(P\).

### Ordinary-RS interpretation

On the split evaluation domain

\[
D_P=Z(P)\mathbin{\dot\cup}E_0
\]

of size \(R+g\), let the received table be zero on \(Z(P)\) and
\(PH_0=P/V\) on \(E_0\).  Equation (2.4) says exactly that \(f_i\) has
\(g+s_i\) agreements with this table.  Thus the entire varying-locator
family is one ordinary polynomial list with:

\[
\text{message degree}<g-w,\qquad
\text{base agreement}=g,
\tag{2.11}
\]

plus the planted no-common-zero and recovered-denominator gates.

This is an exact source adapter, not a support relaxation.

## 3. Fixed-\(G\) slice theorem

For a monic divisor \(G\mid P\), let

\[
\mathcal I_G=\{i\in\mathcal I:G_i=G\},\qquad m=\deg G.
\]

On \(E_0\), division by \(Q=P/G\) identifies this slice with the
polynomials \(b_i\) of degree \(<m-w\).  They agree with the fixed received
table

\[
r_{G,V}(x)=G(x)H_0(x)=G(x)/V(x)
\qquad(x\in E_0)
\tag{3.1}
\]

at exactly the \(\deg H_i=m+s_i\) roots of \(H_i\).  Hence the slice is
contained in the ordinary list

\[
\operatorname{RS}(E_0,m-w)
\quad\text{at agreement at least }m=(m-w)+w.
\tag{3.2}
\]

Evaluation is injective because

\[
1\le m-w<R.
\]

If the linear span of this slice has dimension \(k\), the proved recursive
affine-span compiler gives

\[
|\mathcal I_G|
\le
B_k(m):=
\left\lfloor
\frac{\binom{R-m+w+k}{k}}
     {\binom{w+k}{k}}
\right\rfloor.
\tag{3.3}
\]

The compiler is applied to the linear flat spanned by the \(b_i\).  It may
count zero or other additional polynomials, which only enlarges the slice.
There is therefore no anchor subtraction or affine-rank \(+1\).

### Theorem 3.1 (proper-slice rank loss)

If the whole family has rank seven and \(G<P\), then

\[
\dim\operatorname{span}\{b_i:i\in\mathcal I_G\}\le6.
\tag{3.4}
\]

Consequently

\[
|\mathcal I_G|\le9\,471\,941.
\tag{3.5}
\]

### Proof

Put \(Q=P/G\).  Every \(f_i\) in the slice is divisible by \(Q\), so its
span lies in

\[
W\cap Q\mathbb F_p[X],
\qquad
W=\operatorname{span}\{f_i:i\in\mathcal I\}.
\]

This intersection is proper.  Indeed, choose
\(\alpha\in Z(Q)=Z(P)\setminus Z(G)\).  Exactness of the lcm supplies
some \(G_j\) containing \(\alpha\), and the proof of Theorem 2.1 gives
\(f_j(\alpha)\ne0\).  Thus \(W\) is not contained in
\(Q\mathbb F_p[X]\).  Since \(\dim W=7\), (3.4) follows.

For \(1\le m-w\le5\), the respective exact caps from (3.3), using
\(k\le m-w\), are

\[
14,\quad211,\quad3\,077,\quad44\,769,\quad651\,202.
\tag{3.6}
\]

For \(m-w\ge6\), the unfloored expression in (3.3) is nondecreasing in
\(k\le6\) and nonincreasing in \(m\).  Therefore

\[
B_k(m)\le B_6(w+6)=9\,471\,941.
\tag{3.7}
\]

This proves (3.5).

### Corollary 3.2 (pure fixed-\(G\) cutoff)

The exceptional full-union slice \(G=P\) may have rank seven, but

\[
|\mathcal I_P|\le B_7(g).
\tag{3.8}
\]

The right side is nonincreasing in \(g\), and exact integer arithmetic gives

\[
B_7(328\,677)=15\,776\,081,
\tag{3.9}
\]

\[
B_7(328\,678)=15\,775\,927.
\tag{3.10}
\]

Since a forbidden shallow family requires \(15\,775\,933\) members, a pure
fixed-\(G\) rank-seven family is impossible for every

\[
328\,678\le g\le R.
\tag{3.11}
\]

If a forbidden mixed family has union size \(g\) in this range, at least

\[
15\,775\,933-B_7(g)
\tag{3.12}
\]

of its members lie in proper slices.  The exact lower bounds at
\(g=328\,678,340\,000,350\,000,354\,972\) are respectively

\[
6,\quad1\,656\,948,\quad2\,994\,067,\quad3\,617\,436.
\tag{3.13}
\]

These are source-bound lower bounds on mixed mass.  They are not a license
to sum the proper-slice upper bounds.

## 4. Harmonic endpoint refinement

The second result is independent of the master-denominator slice argument.
It strengthens the dual used by the predecessor codimension-one compiler.

### Lemma 4.1 (reciprocal-convex harmonic dual)

Let

\[
P(z)=\prod_{i=1}^j(a_i+z),
\qquad a_i>0,
\qquad 0<e\le Q.
\tag{4.1}
\]

Then the nonnegative weights

\[
x=\frac1{eP(0)}-\frac{Q-e}{eQP(e)},
\qquad
y=\frac1{QP(e)}
\tag{4.2}
\]

satisfy, for every \(0\le b\le e\),

\[
x(e-b)P(b)+y(Q-e+b)P(b)\ge1.
\tag{4.3}
\]

Consequently the two-resource codimension-one theorem gives

\[
L\le
\left\lfloor
\frac{d^{\underline j}}{P(0)}
+
\frac{d^{\underline j}(d-j-Q+e)}{QP(e)}
\right\rfloor.
\tag{4.4}
\]

### Proof

Because \(P(e)\ge P(0)\) and \(e\le Q\), both weights in (4.2) are
nonnegative.  Direct algebra reduces the left side of (4.3) to

\[
P(b)\left(
\frac{e-b}{eP(0)}+\frac{b}{eP(e)}
\right).
\tag{4.5}
\]

The function

\[
z\longmapsto\frac1{P(z)}
\]

is convex on \(z\ge0\), because

\[
\frac{(1/P)''}{1/P}
=
\left(\sum_i\frac1{a_i+z}\right)^2
+
\sum_i\frac1{(a_i+z)^2}>0.
\]

The chord inequality on \([0,e]\) is

\[
\frac1{P(b)}
\le
\frac{e-b}{eP(0)}+\frac{b}{eP(e)}.
\tag{4.6}
\]

Multiplying by \(P(b)\) proves (4.3).

The two resources have capacities

\[
e\,d^{\underline j},
\qquad
d^{\underline{j+1}}.
\]

Multiplication by (4.2) gives

\[
\frac{d^{\underline j}}{P(0)}
-\frac{(Q-e)d^{\underline j}}{QP(e)}
+\frac{d^{\underline{j+1}}}{QP(e)},
\]

which is exactly (4.4).

The floor in (4.4) applies to the whole rational expression.  Its displayed
second summand can be negative for abstract parameters; it must not be
floored or interpreted separately.  The unsimplified dual capacity
\(xe\,d^{\underline j}+y\,d^{\underline{j+1}}\) is nonnegative.

### M31 specialization

For the rank-seven codimension-one profile, put

\[
j=6,\qquad d=d_6,\qquad
e=R+g-d_6,\qquad Q=w+1,
\tag{4.7}
\]

and

\[
\Pi_b=(d_6-R+b)\prod_{i=1}^{5}(w+i+b).
\tag{4.8}
\]

When \(e\le Q\), Lemma 4.1 yields

\[
L\le
\left\lfloor
\frac{d_6^{\underline6}}{\Pi_0}
+
\frac{d_6^{\underline6}(d_6-6-Q+e)}{Q\Pi_e}
\right\rfloor.
\tag{4.9}
\]

Here

\[
d_6-6-Q+e=R+g-Q-6
\tag{4.10}
\]

is independent of \(d_6\).

For \(e>Q\), the packet keeps the already-proved predecessor dual.  The
exact \(q_6\) envelope bounds

\[
D_{6,\min}\le d_6\le D_{6,\min}+Q_6(g),
\qquad
D_{6,\min}=1\,048\,582.
\tag{4.11}
\]

On the \(e>Q\) subinterval, the verifier replays the predecessor
low-piece/high-endpoint majorants.  On the \(e\le Q\) endpoint interval,
both terms of (4.9) are increasing once
\(d_6\ge1\,177\,354\): the first monotonicity is the proved predecessor
turning-point calculation, while in the second term the falling numerator
increases and \(\Pi_e\) decreases as \(d_6\) increases.  Thus the right
endpoint is a valid uniform majorant.

Exact rational arithmetic gives

\[
\begin{array}{c|c|c}
g&\text{uniform floor}&
15\,775\,932-\text{floor}\\ \hline
354\,972&15\,776\,055&-123\\
354\,973&15\,775\,843&89\\
354\,998&15\,768\,132&7\,800.
\end{array}
\tag{4.12}
\]

The verifier checks every integer between the displayed endpoints.  Hence
all 26 values

\[
354\,973\le g\le354\,998
\tag{4.13}
\]

are paid.  The adjacent value \(354\,972\) remains open by this bound.
The predecessor already pays every \(g\ge354\,999\).

## 5. Exact residual and next primitive theorem

Combining the new harmonic payment with the predecessor interval gives the
rank-seven residual (0.1), containing exactly

\[
354\,972-72\,428+1=282\,545
\tag{5.1}
\]

union sizes.

The fixed-\(G\) theorem gives the sharper type partition

\[
\begin{array}{c|c}
g\text{ interval}&\text{possible primitive type}\\ \hline
72\,428\ldots72\,859&\text{mixed }G\text{ only}\\
72\,860\ldots328\,677&\text{pure fixed }G\text{ or mixed }G\\
328\,678\ldots354\,972&\text{mixed }G\text{ only}.
\end{array}
\tag{5.2}
\]

The maximal remaining rank-seven theorem is therefore an aggregate
mixed-denominator incidence bound, not another per-slice compiler.

An exact divisor formulation freezes that target.  For

\[
M=PL_0,\qquad Y=PH_0,\qquad
W=\operatorname{span}\{f_i\},\qquad\dim W=7,
\]

let \(A\mid M\) be monic of degree

\[
h=g+s.
\]

Write

\[
f_A=\operatorname{rem}_A(Y),\qquad
B_A=\operatorname{quo}_A(Y).
\tag{5.3}
\]

The full-gcd incidence is exactly

\[
0\ne f_A\in W,\qquad
\deg f_A<g-w,\qquad
\gcd(B_A,M/A)=1,
\tag{5.4}
\]

together with the recovered-denominator degree and exact-union gates.

If \(U\) is a coefficient matrix for a basis of \(W\), the matrix

\[
[\operatorname{Mult}_A\mid U]
\tag{5.5}
\]

has \(R+g\) rows and \(R-s+7\) columns and always has full column rank.
Indeed, a relation \(AB+u=0\) with
\(\deg u<g-w<h=\deg A\) forces \(B=u=0\).  Compatibility with \(Y\)
therefore has exact codimension

\[
(R+g)-(R-s+7)=g+s-7=h-7.
\tag{5.6}
\]

Equivalently, \(w+s\) upper remainder coefficients vanish and the
remaining degree-\(<g-w\) remainder lies in a seven-dimensional space,
imposing another \(g-w-7\) equations.  Their total is again \(h-7\).

Thus there is no universal coefficient-matrix rank-drop component to
classify.  The remaining object is the split-divisor, fixed-syndrome
incidence (5.4), including its full gcd and exact-union gates.

## 6. Proof audit

Statement audited:

- the exact master-denominator equivalence;
- the proper fixed-\(G\) rank loss and affine-span cap;
- the pure fixed-\(G\) threshold \(328\,678\);
- the harmonic dual lemma and the new 26-value payment;
- the resulting residual partition.

Dependencies:

- PROVEN upstream: the all-weight anchor-exchange bijection, scalar descent,
  boundary forcing, shallow-tail size, zero-anchored rank convention,
  recursive affine-span compiler, generalized-weight \(q_6\) envelope, and
  codimension-one two-resource recursion.
- PROVED HERE: Theorems 2.1 and 3.1, Corollary 3.2, and Lemma 4.1.
- EXACT FINITE ARITHMETIC: every printed deployed integer and all 27
  transition cells in (4.12)--(4.13).
- UNPROVEN: aggregation across several \(G\)-slices, the mixed incidence
  (5.4), rank at least eight, and row closure.

Parameter dependence:

Every deployed constant is fixed in (1.1)--(1.5).  There is no asymptotic
or hidden field-size dependence.

Layer-cake / dyadic summability:

Not applicable.  The predecessor shallow/deep partition is a direct finite
list partition.

Moment / Markov / Chebyshev:

Not applicable.  No probabilistic moment estimate is used.  “Chebyshev”
elsewhere names the fixed evaluation-domain construction.

Edge cases:

- \(P\) is the exact family lcm, not a chosen larger divisor.
- \(P\) is squarefree because \(P\mid A_0\).
- The zero boundary anchor fixes the linear-rank convention; there is no
  affine \(+1\).
- When \(m-w<6\), the actual message-space dimension replaces six in the
  slice cap.
- The exceptional slice \(G=P\) may retain rank seven.
- A cap for each slice cannot be summed over an uncontrolled number of
  different divisors.
- Lemma 4.1 is used only when \(e\le Q\); the predecessor dual remains in
  force when \(e>Q\).

Verdict:

GREEN for the local statements in this packet.

YELLOW for the rank-seven stratum as a whole.

RED for any claim that this packet closes the M31 LIST row or supplies a
Grande Finale v4 ledger payment.
