---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: For every geometric decomposition f=F composed with h of the residual degree-60 endpoint map, the 60 active parameter roots are complete unramified h-fibers and the twelve order-five source-parameter poles split according to h into complete unramified fibers and index-five exceptional fibers. The eight possible inner-degree rows are therefore exact. The m=5 row is impossible over K=F_{p^6}: Riemann-Hurwitz makes h a two-branch-point fifth-power cover, while fifth powering is bijective on K and cannot have a reduced five-point K-rational active fiber. The m=30 row factors through an inner degree-six map. If a separate same-record adapter identifies h with an m-fold map on the carrier D, only m=2 or 4 pass the necessary m-divides-2^21 gate.
architecture: null
partition_digest: null
atom_or_cell: K3_DEGREE60_DECOMPOSITION_SOURCE_FIBER_ADAPTER
quantifier: every geometric functional decomposition forced by the residual actual Q=6,s=6,u=2 component theorem
projection_and_unit: exact divisor and domain-compatibility route cut; not a distinct-slope payment
claimed_bound: one of eight pole profiles occurs on the challenge-field endpoint parameter line; inner degree 5 is deleted; inner degree 30 refines to inner degree 6 by exact fifth-power extraction; a hypothetical same-degree carrier fold is cardinality-compatible only for inner degrees 2 and 4, but the parameter-to-carrier bridge is not proved
status: PROVED_SOURCE_FIBER_ADAPTER_DEGREE5_DELETION_DEGREE30_REFINEMENT_ROW_OPEN
impact: TERMINATES_INNER_DEGREE_5_ROUTES_INNER_DEGREE_30_TO_6_AND_PARTITIONS_THE_OTHER_SIX_DECOMPOSITION_ROWS
falsifier: a decomposition violating the exact divisor pullback, a reduced five-point K-rational fiber of a K-rational fifth-power map when gcd(5,|K^x|)=1, failure of the degree-thirty fifth-power extraction, or a claimed carrier owner without an explicit parameter-to-carrier same-record bridge
replay: python3 experimental/scripts/verify_kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.py --check --tamper-selftest && sage experimental/scripts/verify_kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.sage
---

# KoalaBear degree-\(60\) decomposition source-fiber adapter

## 0. Verdict

The decomposition branch now has an exact source-bound interface.  One of
its eight rows is empty and one refines to an earlier row.

Let

\[
 f(T)=\frac{V_{\rm act}(T)}{A(T)^5}=F\circ h,
 \qquad \deg f=60,\quad \deg h=m,\quad \deg F=n.
\tag{0.1}
\]

The inherited fixed-domain packet has:

- sixty distinct active parameter roots in the challenge field
  \(K=\mathbf F_{p^6}\);
- twelve distinct source-parameter roots in \(K\), disjoint from the active
  roots;
- a squarefree active locator \(V_{\rm act}\);
- the exact pole divisor \(5\,\operatorname{div}_0(A)\).

For every geometric decomposition (0.1):

1. the active divisor is a union of \(n=60/m\) complete, unramified
   \(h\)-fibers of size \(m\);
2. each outer pole has order one or five;
3. an order-five outer pole pulls back to a complete unramified source
   fiber of size \(m\);
4. a simple outer pole pulls back to \(m/5\) source points, each of
   ramification index five.

This gives exactly the following table.

\[
\begin{array}{c|c|c|c|c|c|c|c}
m&n&a&b&\text{complete source points}&
\text{exceptional source points}&R_h^{\rm forced}&2m-2\\ \hline
2&30&6&0&12&0&0&2\\
3&20&4&0&12&0&0&4\\
4&15&3&0&12&0&0&6\\
5&12&2&2&10&2&8&8\\
6&10&2&0&12&0&0&10\\
10&6&1&1&10&2&8&18\\
12&5&1&0&12&0&0&22\\
30&2&0&2&0&12&48&58
\end{array}
\tag{0.2}
\]

Here \(a\) is the number of order-five outer poles and \(b\) the number
of simple outer poles.

The deployed carrier domain, in a different variable, has

\[
 D\le\mathbf F_p^\times,\qquad |D|=2^{21}.
\tag{0.3}
\]

The endpoint variable and carrier variable are not identified by the source
theorem.  If a separate same-record adapter transports \(h\) to an
\(m\)-fold complete-fiber map on \(D\), then necessarily \(m\mid2^{21}\);
among (0.2), only \(m=2,4\) pass that conditional gate.  This is not a
property of the endpoint map by itself and does **not** make either row a
quotient owner.  The parameter-to-carrier bridge, prime-field carrier
transport, declared-fold form, preservation of \(D\), received-data descent,
explaining-polynomial descent, and slope projection all remain open.

The \(m=5\) row is stronger: it is impossible.  Its two simple outer poles
force two totally ramified \(K\)-rational points of \(h\), using the complete
Riemann--Hurwitz budget.  Two reduced active fibers give a \(K\)-rational
target normalization of \(h\); source and target normalizations then put it
in the form \(cz^5\) over \(K\).  But

\[
 q=|K|=p^6\equiv4\pmod5,\qquad
 \gcd(5,q-1)=1.
\tag{0.4}
\]

Thus fifth powering is a permutation of \(K\), contradicting any reduced
five-point \(K\)-rational active fiber.  In the \(m=30\) row, the two
exceptional pole fibers
instead make \(h\) the fifth power of a degree-six rational map.  Thus that
row refines exactly to \(m=6\); it is not a separate producer.

The terminal partition is consequently:

\[
\begin{array}{c|l}
m&\text{status}\\ \hline
2,4&
\texttt{CONDITIONAL CARRIER CARDINALITY COMPATIBLE; BRIDGE OPEN}\\
5&\texttt{DELETED\_CHALLENGE\_FIELD\_FIFTH\_POWER\_FIBER\_CONTRADICTION}\\
30&\texttt{ROUTED\_TO\_INNER\_DEGREE\_6}\\
3,6,10,12&
\texttt{SAME-DEGREE CARRIER FOLD INCOMPATIBLE; BRIDGE/DELETION OPEN}.
\end{array}
\tag{0.5}
\]

This is a proved route cut with zero ledger movement.  It does not close
\(u=2\) or the KoalaBear row.

## 1. Imported fixed-domain statement

Let \(K=\mathbf F_{p^6}\) be the deployed challenge field and work
geometrically over \(\overline K\), where

\[
p=2^{31}-2^{24}+1=2{,}130{,}706{,}433>60.
\tag{1.1}
\]

The parent route cut supplies the geometric decomposition (0.1).  Its
source theorem imports

\[
 V_{\rm act}(T)=\prod_{t\in\mathcal T_{\rm act}}(T-t),
 \qquad
 A(T)=\prod_{j=1}^{12}(T-\alpha_j),
\tag{1.2}
\]

where:

\[
\#\mathcal T_{\rm act}=60,\qquad
\#\{\alpha_j\}=12,\qquad
\mathcal T_{\rm act}\cap\{\alpha_j\}=\varnothing.
\tag{1.3}
\]

The values in (1.2) are endpoint **parameter-line** values in \(K\).
They are not evaluation coordinates.  The deployed Reed--Solomon carrier is
the separate set

\[
D\le\mathbf F_p^\times,\qquad |D|=2^{21}.
\tag{1.4}
\]

The distinction is load-bearing.  The divisor adapter works on the endpoint
parameter line.  Equation (1.4) enters only conditionally: if a future
same-record theorem transports this endpoint decomposition to an
\(m\)-fold carrier-domain map, then \(m\mid|D|\) is necessary.  It is not
used in the degree-five deletion.

The imported source is the retained fixed-domain chain at source commit
`44542e91e459364a521870ed2ebde7f6fe5055bf`, especially equations
(1.1), (2.2), active/source separation, and the parameter-root
interpretation in
`pole_disjoint_conic_facet_collinearity_reduction.md`.  The deployed
prime-field subgroup is fixed separately in `tex/cs25_cap_v13_2.tex`.

## 2. Exact homogeneous pullback

Choose homogeneous presentations

\[
h=[H_0:H_1],\qquad F=[P:Q],
\tag{2.1}
\]

where \(H_0,H_1\) are coprime binary forms of degree \(m\), and \(P,Q\)
are coprime binary forms of degree \(n\).  Since neither pair has a common
projective zero, neither do \(P(H_0,H_1)\) and \(Q(H_0,H_1)\).
Consequently there is no cancellation in the composition:

\[
\operatorname{div}_0(f)=h^*\operatorname{div}_0(F),
\qquad
\operatorname{div}_\infty(f)=h^*\operatorname{div}_\infty(F).
\tag{2.2}
\]

### Theorem 2.1 (active complete fibers)

Every zero of \(F\) is simple, and \(h\) is unramified above it.  There
are exactly \(n\) zero values of \(F\), and
\(\mathcal T_{\rm act}\) is their disjoint union of complete fibers, each
of size \(m\).

#### Proof

If \(y\) is a zero of \(F\) of order \(r\), and \(x\in h^{-1}(y)\) has
ramification index \(e_x\), then

\[
\operatorname{ord}_x(f)=r e_x.
\tag{2.3}
\]

The left side equals one because \(V_{\rm act}\) is squarefree and is
coprime to \(A\).  Hence \(r=e_x=1\).  Every zero of \(F\) is therefore
simple, its pullback consists of \(m\) distinct unramified points, and
the degree-\(n\) zero divisor of \(F\) has \(n\) points.  Their pullback
has \(mn=60\) points and is exactly (1.2). \(\square\)

Equivalently, after splitting the outer numerator,

\[
P(U,V)=c_P\prod_{\nu=1}^{n}Z_\nu(U,V),
\tag{2.4}
\]

the active locator has the exact homogeneous factorization

\[
V_{\rm act}\ \sim\
\prod_{\nu=1}^{n}Z_\nu(H_0,H_1),
\tag{2.5}
\]

where every degree-\(m\) pullback factor is squarefree and the factors
are pairwise coprime.

### Theorem 2.2 (source complete-plus-exceptional fibers)

Every pole of \(F\) has order one or five.  If \(a\) and \(b\) count
the poles of order five and one, respectively, then

\[
5a+b=n.
\tag{2.6}
\]

An order-five pole has \(m\) distinct unramified preimages.  A simple
pole is possible only when \(5\mid m\), and its fiber has \(m/5\)
distinct points, each of ramification index five.

#### Proof

For a pole \(y\) of \(F\), of order \(r\), and any
\(x\in h^{-1}(y)\),

\[
\operatorname{ord}_x(f)=-r e_x.
\tag{2.7}
\]

Every pole of \(f\) has order five, so \(r e_x=5\).  Thus
\((r,e_x)=(5,1)\) or \((1,5)\).  Summing pole orders on \(F\) gives
(2.6).  Summing ramification indices in a fiber gives the stated fiber
cardinalities. \(\square\)

After splitting the outer denominator,

\[
Q(U,V)=c_Q
\prod_{i=1}^{a}L_i(U,V)^5
\prod_{j=1}^{b}M_j(U,V),
\tag{2.8}
\]

there are squarefree binary forms \(R_j\) of degree \(m/5\) such that

\[
M_j(H_0,H_1)=c_jR_j^5
\tag{2.9}
\]

and

\[
A\ \sim\
\prod_{i=1}^{a}L_i(H_0,H_1)
\prod_{j=1}^{b}R_j.
\tag{2.10}
\]

All displayed source factors are pairwise coprime.  Formula (2.10) is
the promised exact source-bound quotient/remainder locator adapter: the
first product is the complete-fiber part, and the second is the
index-five exceptional part.  It is a locator theorem, not received-data
descent.

## 3. Exhaustive profile compiler

The simple-pole fibers force

\[
R_h^{\rm forced}
=b\frac m5(5-1)
=\frac{4bm}{5}.
\tag{3.1}
\]

Riemann--Hurwitz gives

\[
\frac{4bm}{5}\le2m-2.
\tag{3.2}
\]

Enumerate proper divisors \(m\mid60\), put \(n=60/m\), impose
(2.6), require \(5\mid m\) when \(b>0\), and impose (3.2).  This yields
exactly (0.2).  In particular \(m=15,20\) fail (3.2), while there are no
other proper divisors to consider.

The source-point count is a consistency identity:

\[
am+b\frac m5
=\frac m5(5a+b)
=\frac{mn}{5}
=12.
\tag{3.3}
\]

The active-point count is similarly \(nm=60\).

The exact number of labeled source partitions in (3.4) is

\[
\frac{12!}
{(m!)^a a!\,((m/5)!)^b b!}.
\tag{3.4a}
\]

In the table order \(m=2,3,4,5,6,10,12,30\), these counts are

\[
10395,\quad15400,\quad5775,\quad8316,\quad
462,\quad66,\quad1,\quad462.
\tag{3.4b}
\]

### Theorem 3.1 (binary source-pencil equivalence)

Fix one row \((m,n,a,b)\) of (0.2).  A geometric decomposition of that
profile is equivalent to the following source-bound pencil certificate.

Partition the twelve source-parameter points into:

\[
S_1,\ldots,S_a,\quad |S_i|=m,
\qquad
R_1,\ldots,R_b,\quad |R_j|=m/5.
\tag{3.4}
\]

For a finite point set \(E\), write \(A_E\) for its split homogeneous
locator.  There must exist a coprime two-dimensional pencil

\[
\mathcal W=\langle H_0,H_1\rangle
\subseteq H^0(\mathbf P^1,\mathcal O(m))
\tag{3.5}
\]

such that

\[
A_{S_i}\in\mathcal W\quad(1\le i\le a),
\qquad
A_{R_j}^5\in\mathcal W\quad(1\le j\le b),
\tag{3.6}
\]

and

\[
V_{\rm act}\in\operatorname{Sym}^n(\mathcal W).
\tag{3.7}
\]

Here (3.7) means that there is a binary outer form \(P(U,V)\) of degree
\(n\) with

\[
P(H_0,H_1)=V_{\rm act}.
\tag{3.8}
\]

#### Proof

Given \(f=F\circ h\), use \(h=[H_0:H_1]\).  Each order-five outer pole
has a squarefree complete pullback \(A_{S_i}\), while each simple outer
pole has pullback \(A_{R_j}^5\); both are linear forms in
\((H_0,H_1)\).  The outer numerator gives (3.8).

Conversely, choose the linear forms
\(\ell_i,\mu_j\) on the target pencil satisfying

\[
\ell_i(H_0,H_1)=A_{S_i},
\qquad
\mu_j(H_0,H_1)=A_{R_j}^5,
\tag{3.9}
\]

and put

\[
Q(U,V)=\prod_{i=1}^a\ell_i(U,V)^5
\prod_{j=1}^b\mu_j(U,V).
\tag{3.10}
\]

Then \(Q(H_0,H_1)=A^5\) up to scalar, while (3.8) gives the numerator.
The source blocks are disjoint, so their pencil elements are distinct;
coprimality of \(V_{\rm act}\) and \(A\) prevents cancellation between
\(P\) and \(Q\).  Squarefreeness of \(V_{\rm act}\) forces the outer zeros
and their pullbacks to be simple.  Hence

\[
\frac{V_{\rm act}}{A^5}
=\frac{P}{Q}\circ[H_0:H_1].
\tag{3.11}
\]

This proves the equivalence. \(\square\)

The certificate also exposes the exact self-correspondence factor:

\[
\Delta_h(T,W)
=H_0(T)H_1(W)-H_1(T)H_0(W)
\tag{3.12}
\]

divides the numerator of \(f(T)-f(W)\).  Thus every remaining row can be
attacked as a finite source-partition plus a two-dimensional linear-pencil
incidence, rather than by reconstructing arbitrary rational maps or
resuming the old quartic atlas.

### Theorem 3.2 (challenge-field descent of the right component)

Every geometric right component \(h\) in Theorem 3.1 has a target Möbius
transform defined over \(K\); with that transform, the outer map is also
defined over \(K\).

#### Proof

Choose two distinct active outer-zero fibers \(C_0,C_\infty\).  Each is a
reduced set of \(m\) individually \(K\)-rational active parameters.  Its
split locator \(L_0\), respectively \(L_\infty\), therefore belongs to
\(K[T_0,T_1]\).  As in (5.2),

\[
h_0=L_0/L_\infty\in K(T)
\tag{3.13}
\]

is a target Möbius transform of \(h\).  Write \(f=F_0\circ h_0\) over
\(\overline K\).  For every \(\sigma\in\operatorname{Gal}(\overline K/K)\),

\[
f=F_0^\sigma\circ h_0.
\tag{3.14}
\]

Substitution \(\overline K(Y)\to\overline K(T)\), \(Y\mapsto h_0(T)\),
is injective because \(h_0\) is nonconstant.  Hence
\(F_0^\sigma=F_0\), so \(F_0\in K(Y)\). \(\square\)

This descent is on the endpoint parameter line.  It supplies no action on
the carrier \(D\).

## 4. Conditional carrier-domain owner gate

Suppose a future same-record theorem identifies the endpoint inner map
\(h\), or a conjugate retaining its degree, with a complete \(m\)-fold map
on the finite carrier \(D\).  Such a map partitions \(D\) into fibers of
cardinality \(m\).  Therefore

\[
m\mid |D|=2^{21}.
\tag{4.1}
\]

For the eight rows in (0.2):

\[
\{m:m\mid2^{21}\}=\{2,4\}.
\tag{4.2}
\]

Thus:

- \(m=3,5,6,10,12,30\) cannot become a same-degree complete \(m\)-fold
  carrier owner;
- \(m=2,4\) merely survive this conditional cardinality test.

Both bullets are intentionally scoped.  The decomposition lives on the
challenge-field endpoint parameter line, while \(D\) is a prime-field
evaluation carrier.  No map between those variables is imported.  The
existing owner needs a declared carrier fold with the correct field of
definition and complete fibers on the entire domain, plus descent of the
received data, explaining polynomial, and slope projection.  None follows
from \(m\mid2^{21}\).

For the six incompatible rows, (4.1) is not an actual-producer deletion.
It rules out only the naive identification with a same-degree carrier fold.
Inner degree five is deleted below, inner degree thirty refines to degree
six, and the other four need either a different chronology-valid bridge or
direct geometric exclusion.

## 5. Exact deletion of inner degree five

Assume \(m=5\).  Table (0.2) gives \(a=2,b=2\).  Each of the two simple
outer poles has one preimage of ramification index five.  Their
ramification contribution is

\[
2(5-1)=8=2m-2.
\tag{5.1}
\]

They exhaust Riemann--Hurwitz, so \(h\) has exactly two ramification
points, both totally ramified.  They are the singleton fibers above the
two simple outer poles, hence they are two of the twelve source-parameter
values and belong to \(K\).

We first descend a target transform of \(h\) to \(K\).  Choose two distinct
active outer-zero fibers \(C_0,C_\infty\).  Each is a reduced divisor of
five \(K\)-rational active points.  Let their split binary locators be
\(L_0,L_\infty\in K[T_0,T_1]\).  Since the two divisors are fibers of
\(h\),

\[
\operatorname{div}(L_0/L_\infty)=C_0-C_\infty
=\operatorname{div}\!\left(
\frac{h-y_0}{h-y_\infty}\right).
\tag{5.2}
\]

Thus

\[
h_0:=L_0/L_\infty\in K(T)
\tag{5.3}
\]

is a target Möbius transform of \(h\).  No descent of the original
presentation is assumed.

The two totally ramified source points and their \(h_0\)-images are
distinct \(K\)-points.  Use source and target transformations in
\(\operatorname{PGL}_2(K)\) to send both ordered pairs to
\((0,\infty)\).  The resulting \(K\)-rational degree-five function has
divisor

\[
5[0]-5[\infty],
\tag{5.4}
\]

so it is \(cz^5\) for some \(c\in K^\times\).

Now \(p\equiv3\pmod5\), hence

\[
q=p^6\equiv4\pmod5,\qquad
\gcd(5,q-1)=1.
\tag{5.5}
\]

Therefore \(z\mapsto z^5\) is a bijection of \(K\).  In particular every
nonzero finite \(K\)-fiber of \(cz^5\) contains exactly one \(K\)-point.
But any active outer-zero fiber, transported through the \(K\)-rational
source and target transformations above, is a reduced fiber of five
distinct \(K\)-points.  This is the contradiction.  Thus:

\[
\boxed{\text{the inner-degree-five actual producer is empty}.}
\tag{5.6}
\]

The two split active fibers are load-bearing: they descend a target
transform of the geometric right component to \(K\).  The two
\(K\)-rational totally ramified source points are also load-bearing: they
make the fifth-power normal form split over \(K\).  The rejected attempt to
place the deck map in \(\operatorname{PGL}_2(\mathbf F_p)\) is preserved in
`experimental/dead_ends/`; it confused the parameter line with the carrier
domain.

## 6. Exact refinement of inner degree thirty

Assume \(m=30\).  Table (0.2) gives \(a=0,b=2\).  Send the two simple
outer poles to \(0,\infty\).  By Theorem 2.2, their pullbacks are

\[
h^*[0]=5R_0,\qquad h^*[\infty]=5R_\infty,
\tag{6.1}
\]

where \(R_0,R_\infty\) are reduced effective divisors of degree six with
disjoint support.  Choose coprime degree-six binary forms \(P_0,P_\infty\)
cutting out these divisors.  The divisor of \(h\) is

\[
\operatorname{div}(h)
=5R_0-5R_\infty
=\operatorname{div}\!\left((P_0/P_\infty)^5\right).
\tag{6.2}
\]

Hence, up to a nonzero target scalar,

\[
h=(P_0/P_\infty)^5=p_5\circ r,
\qquad
\deg r=6,\quad p_5(z)=z^5.
\tag{6.3}
\]

Therefore

\[
f=F\circ p_5\circ r=(F\circ p_5)\circ r
\tag{6.4}
\]

is already an inner-degree-six decomposition.  This is geometric and
requires no field-of-definition claim for \(R_0,R_\infty\).  Thus:

\[
\boxed{\text{every inner-degree-thirty producer routes to the
inner-degree-six row}.}
\tag{6.5}
\]

Equation (6.5) is a refinement, not deletion of the degree-six producer
and not a quotient payment.

## 7. Canonical inner-degree-twelve pencil

Assume \(m=12\).  The source partition is unique:

\[
a=1,\qquad b=0,\qquad S_1=\{\alpha_1,\ldots,\alpha_{12}\}.
\tag{7.1}
\]

Thus the source-pencil equivalence gives

\[
\mathcal W=\langle A,N\rangle
\tag{7.2}
\]

for some degree-twelve form \(N\), and

\[
V_{\rm act}
=c_0A^5+c_1A^4N+\cdots+c_5N^5,
\qquad c_5\ne0.
\tag{7.3}
\]

By Theorem 3.2, take \(A,N\) and the outer coefficients over \(K\).
Since \(\gcd(5,q-1)=1\), rescale \(N\) over \(K\) to make \(c_5=1\).
Modulo \(A\),

\[
N^5\equiv V_{\rm act}\pmod A.
\tag{7.4}
\]

The split squarefree algebra

\[
K[T]/(A)\simeq K^{12}
\tag{7.5}
\]

has bijective fifth-power map, coordinate by coordinate.  Therefore (7.4)
determines a unique residue \(N_0\bmod A\), represented with degree less
than twelve.  Every degree-twelve lift is

\[
N=N_0+cA,
\tag{7.6}
\]

which leaves the pencil \(\langle A,N\rangle=\langle A,N_0\rangle\)
unchanged and is only the target translation \(N/A\mapsto N/A+c\).

Hence there is one canonical candidate pencil per actual endpoint record:

\[
\boxed{
\mathcal W_{12}=\langle A,N_0\rangle,\qquad
N_0^5\equiv V_{\rm act}\pmod A.}
\tag{7.7}
\]

The exact terminal test is

\[
\boxed{
V_{\rm act}\in
\operatorname{span}_K
\{A^5,A^4N_0,A^3N_0^2,A^2N_0^3,AN_0^4,N_0^5\}.}
\tag{7.8}
\]

Failure of (7.8), or \(\gcd(A,N_0)\ne1\), deletes the \(m=12\) producer.
Passing (7.8) emits one exact parameter-line decomposition candidate; it
does not emit a carrier owner or slope payment.

## 8. Degree-two challenge-field and conditional carrier stabilizer gate

Assume \(m=2\).  Every separable degree-two rational map has a unique
nontrivial deck involution \(\tau\).  By Theorem 2.1, \(\tau\) exchanges
the two points in every active fiber.  Since the active parameter set lies
in \(K\), three-point descent gives

\[
\boxed{\tau\in\operatorname{PGL}_2(K).}
\tag{8.1}
\]

This already removes a geometric field-of-definition ambiguity for the
deck map.  It does not place \(\tau\) in
\(\operatorname{PGL}_2(\mathbf F_p)\), identify the endpoint parameter
with a carrier coordinate, or show that any induced action preserves
\(D\).

If a future same-record bridge does produce a prime-field projective action
on the carrier, the latter gate has an exact classification.  Write the
deployed subgroup as

\[
D=\{x\in\mathbf F_p^\times:x^N=1\},
\qquad N=2^{21}<p,
\tag{8.2}
\]

and suppose

\[
\gamma(x)=\frac{ax+b}{cx+d}\in\operatorname{PGL}_2(\mathbf F_p)
\quad\text{satisfies}\quad
\gamma(D)=D.
\tag{8.3}
\]

Then

\[
\boxed{\gamma(x)=\kappa x\quad\text{or}\quad
\gamma(x)=\frac{\kappa}{x},\qquad \kappa\in D.}
\tag{8.4}
\]

Indeed, the denominator in (8.3) is nonzero on \(D\), and

\[
R(X)=(aX+b)^N-(cX+d)^N
\tag{8.5}
\]

vanishes on all \(N\) distinct roots of \(X^N-1\).  It has degree at most
\(N\), so

\[
R(X)=C(X^N-1).
\tag{8.6}
\]

Because \(N<p\), every intermediate binomial coefficient
\(\binom Nk\), \(1\le k<N\), is nonzero in \(\mathbf F_p\).  Thus

\[
a^kb^{N-k}=c^kd^{N-k}
\qquad(1\le k<N).
\tag{8.7}
\]

If \(a,b,c,d\) were all nonzero, the equations for \(k=1,2\) would give
\(ad=bc\), contradicting invertibility.  If one entry vanishes, (8.7)
forces the opposite entry to vanish: \(b=c=0\) or \(a=d=0\).  These are
exactly the two forms in (8.4), and evaluating at \(1\) gives
\(\kappa\in D\).  The converse is immediate.

Suppose, in addition to the present packet, that a bridge identifies the
deck action with a nontrivial involution \(\gamma\) satisfying (8.3).
Then exactly two carrier-fold types remain:

\[
\begin{array}{c|c|c}
\text{deck involution}&\text{quotient coordinate}&
\text{uniformity condition}\\ \hline
x\mapsto-x&x^2&\text{always two-to-one on \(D\)}\\
x\mapsto\kappa/x&x+\kappa/x&
\kappa\in D\setminus D^2.
\end{array}
\tag{8.8}
\]

For the second row, a fixed point in \(D\) exists exactly when
\(x^2=\kappa\) is solvable in \(D\); hence the nonsquare condition is
equivalent to complete two-point fibers.

Thus the \(m=2\) row has the exact fail-closed interface

```text
no parameter-to-carrier same-record bridge
    -> UNPAID_PARAMETER_LINE_DECOMPOSITION

bridge proves a prime-field involution preserving D
    -> POWER_PAIR or RECIPROCAL_PAIR;
       received-data, explaining-polynomial, slope, and chronology gates open
```

The reciprocal quotient in (8.8) is a Laurent/Chebyshev-type domain fold.
This packet does not silently identify it with the existing polynomial
power owner.

Finally, whenever a composite inner map \(h\) decomposes further, the
endpoint map has the smaller inner factor as a decomposition.  Hence the
remaining compiler may take \(h\) geometrically indecomposable.  In
particular, decomposable degree four routes to degree two, decomposable
degree six routes to degree two or three, decomposable degree ten routes
to degree two or the deleted degree five row, and decomposable degree
twelve routes to one of degrees \(2,3,4,6\).  Only the indecomposable
subrows are genuinely new.

## 9. Remaining exact attack surface

The decomposition adapter leaves:

1. **Inner degrees \(2,4\):** prove a declared full-domain fold and all
   witness/data/slope descent gates, or delete the actual producer.
2. **Inner degrees \(3,6,10\):** a same-degree full-domain \(m\)-fold
   carrier owner is impossible by cardinality; supply a different
   chronology-valid bridge or delete the producer.
3. **Inner degree \(12\):** run the unique canonical pencil test (7.8),
   then either delete the producer or bridge its single survivor.
4. **Inner degree \(5\):** deleted by (5.6).
5. **Inner degree \(30\):** routed to inner degree six by (6.5).

For \(m=2\), the challenge-field deck involution is exact, and the
prime-field stabilizer theorem tells a future bridge exactly what it must
emit.  The bridge itself is not proved here.

No \(u=3\) work is authorized by this packet.  The \(u=2\) branch still
has six live inner-degree rows, and the active row numerator is
unchanged.

## 10. Exact replays

The Python verifier reconstructs all eight rows from divisibility,
pole-order, and Riemann--Hurwitz constraints; checks every source/active
count and terminal; binds the parent certificate and imported source
objects; verifies the degree-five challenge-field fifth-power obstruction,
the conditional carrier gate, and the degree-thirty refinement; and rejects
the mutation suite:

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.py \
  --check --tamper-selftest
```

Sage independently enumerates the rows and replays the challenge-field,
degree-five, conditional carrier, and degree-thirty arithmetic:

```bash
sage \
  experimental/scripts/verify_kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.sage
```

Wolfram Language independently enumerates the same integer profiles,
source split, Riemann--Hurwitz slack, conditional \(2^{21}\)-divisibility
gate, \(q=p^6\) fifth-power bijectivity, and degree-thirty refinement.
These computations certify finite arithmetic and exhaustiveness; they do
not replace the divisor proof, right-component descent, or the inherited
parameter-line statement.

## 11. Proof tier and nonclaims

- **Proved here:** exact active/source pullback, exhaustive eight-row
  profile table, binary source-pencil equivalence, challenge-field descent
  of the right component, conditional carrier-cardinality partition,
  deletion of inner degree five over \(K\), refinement of inner degree
  thirty to degree six, the canonical inner-degree-twelve pencil, descent
  of the degree-two deck involution to \(K\), and the full
  \(\operatorname{PGL}_2(\mathbf F_p)\) carrier-stabilizer classification
  conditional on a separate parameter-to-carrier bridge.
- **Imported:** the actual component forces a geometric decomposition;
  the endpoint locators have sixty distinct \(K\)-rational active parameter
  roots and twelve distinct \(K\)-rational source-parameter poles of order
  five.
- **Not proved:** a full-domain fold for \(m=2\) or \(m=4\); any
  parameter-to-carrier same-record bridge; any
  received-data, explaining-polynomial, or slope descent; deletion of
  \(m=3,6,10,12\); deletion of the routed \(m=30\) producer; \(u=2\)
  closure; \(u=3\); cap \(68\); a ledger payment; or KoalaBear closure.
- **Layer cake / moments:** not applicable.
- **Parameter dependence:** fixed deployed
  \(p=2{,}130{,}706{,}433\), \(K=\mathbf F_{p^6}\),
  \(D\le\mathbf F_p^\times\), \(|D|=2^{21}\), and the exact degree-\(60\)
  endpoint parameter line.
- **Ledger:** unchanged.
