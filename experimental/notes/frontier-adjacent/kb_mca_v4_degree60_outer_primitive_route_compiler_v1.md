---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every one of the 24 transverse types left after the inner-degree-12 parent cut is classified by exact outer primitive subdegrees and strict outer-decomposition routes. Eighteen types force an acyclic strict outer decomposition, the inner-degree-10 type (r,delta)=(4,10) is empty, and exactly five primitive-compatible types remain. Exact low-genus branch cycles compile the inner-degree-6 and inner-degree-10 survivors into 16 three-branch Nielsen passports with 18 simultaneous-conjugacy orbits; the parent already compiles the two inner-degree-12 survivors into six geometric families.
architecture: null
partition_digest: null
atom_or_cell: K3_OUTER_PRIMITIVE_ROUTE_AND_NIELSEN_COMPILER
quantifier: every actual residual u=2 transverse terminal emitted by the bound degree-60 source-pencil compiler
projection_and_unit: exact geometric route and branch-cycle compiler; not a challenge-field source-incidence classifier, same-record owner, or distinct-slope payment
claimed_bound: 26 parent types become two parent deletions, eighteen acyclic strict-decomposition routes, one new actual-producer contradiction, and five finite primitive targets
status: PROVED_OUTER_PRIMITIVE_ROUTE_AND_LOW_GENUS_NIELSEN_COMPILER_ROW_OPEN
impact: REDUCES_THE_GLOBAL_TRANSVERSE_SEARCH_TO_FIVE_FINITE_PRIMITIVE_TARGETS
falsifier: an omitted primitive subdegree, a viable outer-decomposition exit omitted from the route table, a degree-five right factor in the inner-degree-6 row, a product-one branch multiset in the primitive inner-degree-4 row, or a low-genus primitive inner-degree-6 or inner-degree-10 passport absent from the exact Nielsen ledger
replay: python3 experimental/scripts/verify_kb_mca_v4_degree60_outer_primitive_route_compiler_v1.py --check --tamper-selftest && HOME=/tmp/sage-k3-home /usr/local/bin/sage experimental/scripts/replay_kb_mca_v4_degree60_outer_primitive_route_compiler_v1.sage
---

# KoalaBear outer primitive route and low-genus Nielsen compiler

## 0. Verdict

The source-pencil compiler emitted \(26\) transverse types.  The
inner-degree-\(12\) parent cut deletes two of them, leaving \(24\).  This
packet gives the following exact first-match partition:

\[
\boxed{
24
=18\ {\rm strict\ outer\ decomposition}
+1\ {\rm new\ contradiction}
+5\ {\rm primitive\ compatible}.
}
\tag{0.1}
\]

The new empty type is

\[
 (m,n,r,\delta)=(10,6,4,10).
\tag{0.2}
\]

The five primitive-compatible types are

\[
\begin{split}
 &(6,10,3,8),\qquad (6,10,6,4),\\
 &(10,6,5,8),\\
 &(12,5,2,24),\qquad (12,5,4,12).
\end{split}
\tag{0.3}
\]

There is no anonymous decomposition loop.  The only apparent cycle,
\(m=6\to30\to6\), would require a degree-five right factor of the
degree-ten outer map; Section 4 proves that factor impossible over the
deployed field.  The normalized strict-decomposition graph is therefore
acyclic.

The geometric search inside (0.3) is also finite.  Exact branch-cycle
enumeration compiles the \(m=6\) and \(m=10\) types into \(16\)
three-branch Nielsen passports with \(18\) simultaneous-conjugacy orbits.
The parent packet already compiles the two \(m=12\) types into six
geometric quintic families.

This is a route and target compiler, not a payment.  It does not prove that
the remaining geometric maps descend to the challenge field, satisfy the
actual source-producer equations, or give a chronology-valid carrier,
received-data, explaining-polynomial, or slope owner.  No ledger quantity
moves.

## 1. Imported source-bound data

Fix

\[
 p=2\,130\,706\,433,\qquad K=\mathbf F_{p^6}.
\tag{1.1}
\]

The parent source-pencil theorem supplies an actual endpoint map of degree
\(60\), an irreducible bidegree-\((4,4)\) self-correspondence
\(\Gamma\), and the six terminal inner degrees

\[
 m\in\{2,3,4,6,10,12\},\qquad n=60/m.
\tag{1.2}
\]

For the non-diagonal outer image \(C\), write

\[
 \operatorname{bideg}C=(r,r),\qquad
 \delta=\deg(\Gamma\longrightarrow C).
\tag{1.3}
\]

The imported degree identities are

\[
 \delta r=4m,\qquad \delta\le m^2,\qquad r\le n-1.
\tag{1.4}
\]

The source component is birational to an actual bidegree-\((2,4)\)
component.  Hence

\[
 g(\widetilde\Gamma)\le(2-1)(4-1)=3.
\tag{1.5}
\]

The inner-degree-\(12\) parent cut deletes

\[
 (r,\delta)=(1,48),(3,16)
\tag{1.6}
\]

and retains \((2,24),(4,12)\).

## 2. Primitive outer subdegrees

Let \(F:\mathbf P^1\to\mathbf P^1\) be the outer map of degree \(n\).
If \(F\) is geometrically indecomposable, its geometric monodromy action is
primitive.  The irreducible components of

\[
 F(Y)=F(Z)
\tag{2.1}
\]

correspond to the point-stabilizer suborbits.  The diagonal component
accounts for exactly one suborbit of length one.  A non-diagonal component
of bidegree \((r,r)\) therefore gives a non-diagonal subdegree \(r\).

The complete primitive catalogues needed here are:

\[
\begin{array}{c|c|l}
n&\#\operatorname{PrimGrp}(n)&\text{complete subdegree rows}\\ \hline
30&4&(1,29)\quad\text{four times}\\
20&4&(1,19)\quad\text{four times}\\
15&6&(1,14)\quad\text{four times};\ (1,6,8)\quad\text{twice}\\
10&9&(1,3,6)\quad\text{twice};\ (1,9)\quad\text{seven times}\\
6&4&(1,5)\quad\text{four times}\\
5&5&(1,1,1,1,1),\ (1,2,2),\ (1,4)\quad\text{three times}.
\end{array}
\tag{2.2}
\]

For \(r=1\), one diagonal suborbit must be removed.  Thus only the cyclic
degree-five group supplies a non-diagonal subdegree one.  The Sage/GAP
replay regenerates every group, order, stabilizer orbit, and multiplicity
in (2.2); catalogue completeness is an imported finite classification fact.

If \(r\) does not occur in the relevant non-diagonal primitive catalogue,
the contrapositive forces a strict geometric decomposition of \(F\).  It
does not by itself delete or pay the endpoint record.

## 3. Exact strict-decomposition transition

Suppose

\[
 F=G\circ s,\qquad e=\deg s>1,
\tag{3.1}
\]

and let \(C'\) be the image of \(C\) under \(s\times s\).

If \(C'\) is diagonal, \(C\) is contained in a non-diagonal component of
the same-\(s\)-fiber divisor, so

\[
 r\le e-1.
\tag{3.2}
\]

If \(C'\) has bidegree \((r',r')\) and the induced map
\(C\to C'\) has degree \(\epsilon\), projection degrees give

\[
 \epsilon r'=er,\qquad \epsilon\le e^2.
\tag{3.3}
\]

The coarsened inner degree \(m'=me\) must belong to the exhaustive source
profile set

\[
 \{2,3,4,5,6,10,12,30\}.
\tag{3.4}
\]

The \(m'=5\) row is already empty and \(m'=30\) is refined by the parent
packet to \(m'=6\).  Applying (3.2)--(3.4) to every proper divisor \(e\mid n\)
gives the complete transition table in the certificate.

For (0.2), \(e=2\) would give the forbidden source profile \(m'=20\).
For \(e=3\), the diagonal-image branch fails because

\[
 r=4>e-1=2.
\tag{3.5}
\]

The remaining outer map has degree two, so a non-diagonal image has
\(r'=1\).  Equation (3.3) would then require

\[
 \epsilon=er=12>e^2=9,
\tag{3.6}
\]

also impossible.  Thus (0.2) is an actual-producer contradiction.

## 4. Deleting the \(m=6\to30\to6\) loop

In the \(m=6\) source-pencil row, choose the \(K\)-basis

\[
 H_0=L_{S_0},\qquad H_1=L_{S_\infty},\qquad z=H_0/H_1.
\tag{4.1}
\]

The outer function \(F\in K(z)\) has exactly two \(K\)-rational poles,
\(z=0,\infty\), each of order five, and ten distinct simple
\(K\)-rational zeros.

Assume \(F=G_2\circ s_5\) geometrically.  Pulling back the pole divisor
forces \(G_2\) to have two simple poles and \(s_5\) to be totally ramified
at \(0\) and \(\infty\).  Riemann--Hurwitz is exhausted:

\[
 2\deg s_5-2=8=(5-1)+(5-1).
\tag{4.2}
\]

Consequently, after a geometric target coordinate change,

\[
 s_5=c z^5,\qquad c\ne0.
\tag{4.3}
\]

Each simple zero of \(G_2\) pulls back to five distinct points among the
\(K\)-rational zeros of \(F\).  Two points in such a fiber have a ratio
equal to a nontrivial fifth root of unity in \(K\).  But

\[
 p\equiv3\pmod5,\qquad p^6\equiv4\pmod5,\qquad
 \gcd(5,p^6-1)=1.
\tag{4.4}
\]

Thus \(K\) has no nontrivial fifth root of unity, a contradiction.  The
degree-five right-factor edge is empty.  The only decomposable \(m=6\)
outer route is the degree-two right factor, which strictly coarsens to
\(m=12\).

Notice that (4.3) is geometric; no unjustified descent of the target
coordinate is used.  The source coordinate \(z\) and the five points in
one fiber are \(K\)-rational, which is exactly what makes their ratios lie
in \(K\).

## 5. The \(m=4,r=8\) primitive branch-cycle contradiction

The only primitive degree-\(15\) candidates with subdegree eight are
\(A_6\) and \(S_6\) in their actions on the fifteen two-subsets of six
letters.  The corresponding ordered orbital has degree

\[
 15\cdot8=120.
\tag{5.1}
\]

Here \(\delta=2\).  From (1.5) and Riemann--Hurwitz,

\[
 g(\widetilde C)\le2.
\tag{5.2}
\]

The point cover has total branch index \(2\cdot15-2=28\), and the
degree-\(120\) component has total index in

\[
 \{238,240,242\}.
\tag{5.3}
\]

The pole cycle type \(5^3\) in degree fifteen comes from natural
\(S_6\)-type \((5,1)\).  Exact enumeration over every nonidentity natural
cycle type gives no \(A_6\) class multiset satisfying (5.3).  In \(S_6\)
there is exactly one necessary multiset:

\[
 2(5,1)+(2,1,1,1,1).
\tag{5.4}
\]

Its product sign is \(-1\), so it cannot be a product-one branch tuple.
The primitive \(m=4,r=8\) realization is empty.  The row itself is not
empty: its viable strict-decomposition route is retained among the
eighteen routes in (0.1).

## 6. Exact low-genus Nielsen compiler

For each primitive-compatible \(m=6\) or \(m=10\) row,
\(\delta\ge4\).  Equations (1.5) and Riemann--Hurwitz imply

\[
 g(\widetilde C)\le1.
\tag{6.1}
\]

The exhaustive compiler enumerates every nonidentity conjugacy class in
the relevant primitive group, imposes:

\[
\sum\operatorname{ind}_{\rm point}=2n-2,
\tag{6.2}
\]

the required pole class \(5^2\) for \(n=10\) or \(5\,1\) for \(n=6\), and
the component-genus bound (6.1).  Every surviving class vector has exactly
three branch values.  Full element enumeration then checks product one,
generation of the declared primitive group, and simultaneous-conjugacy
orbits.

The result is:

\[
\begin{array}{c|c|c|c|c}
m&r&G_{\rm geom}&\text{point passport}&g(C)\\ \hline
6&3&A_5&(5^2),(3^3 1),(2^4 1^2)&0\\
6&3&S_5&(5^2),(2^3 1^4),(6,3,1)&1\\
6&3&S_5&(5^2),(2^3 1^4),(4^2,2)&0\\
6&6&A_5&(5^2),(3^3 1),(2^4 1^2)&0\\
6&6&S_5&(5^2),(2^3 1^4),(4^2,2)&1\\ \hline
10&5&A_5&(5,1),(2^2 1^2),(3^2)&0\\
10&5&S_5&(5,1),(4,1^2),(2^3)&1\\
10&5&A_6&(5,1),(2^2 1^2),(4,2)&1\\
10&5&A_6&(5,1),(3,1^3),(3^2)&1\\
10&5&S_6&(5,1),(2,1^4),(6)&0\\
10&5&S_6&(5,1),(2^3),(3,2,1)&1.
\end{array}
\tag{6.3}
\]

Splitting of conjugacy classes creates \(7\) exact \(m=6\) passport rows
and \(9\) exact \(m=10\) passport rows in the certificate.  Two \(A_6\)
rows each have two simultaneous-conjugacy orbits.  Altogether there are

\[
 16\ \text{passport rows},\qquad
 18\ \text{simultaneous-conjugacy orbits}.
\tag{6.4}
\]

The canonical JSON includes one explicit product-one generating triple for
every orbit.  The Python verifier independently checks every point cycle
type, product, generated group order, stabilizer orbital, component index,
and genus.  Sage/GAP independently replays the class and tuple
exhaustiveness.  Wolfram exact arithmetic independently checks the
point/component index sums and genera.

The two \(m=12\) types are bound to the parent normal-form compiler: the
\(r=2\) row is dihedral/Dickson, while \(r=4\) lies in five printed
\(A_5/S_5\) quintic families.  Those six families are not re-proved here.

## 7. Complete row partition

Combining primitive subdegrees, profile filters, and every viable
decomposition exit gives:

\[
\begin{array}{c|c|c|c}
m&\text{parent-deleted}&\text{forced decomposition}&
  \text{primitive-compatible}\\ \hline
2&-&r=2,4,8&-\\
3&-&r=2,3,4,6,12&-\\
4&-&r=1,2,4,8&-\\
6&-&r=1,2,4,8&r=3,6\\
10&-&r=1,2&r=5\\
12&r=1,3&-&r=2,4.
\end{array}
\tag{7.1}
\]

The \(m=10,r=4\) type is the additional contradiction (0.2), so it does
not appear in either live column of (7.1).  Counts are

\[
26=2_{\rm parent\ deleted}
  +18_{\rm decomposed}
  +1_{\rm new\ contradiction}
  +5_{\rm primitive}.
\tag{7.2}
\]

After deleting the field-impossible \(m=6\to30\) edge, the normalized route
graph has no nontrivial strongly connected component.  Therefore recursive
application terminates.

## 8. Exact stopping point

For every remaining primitive passport or normal form, the next theorem
must combine the outer relation with the actual source producer.  In the
notation of the parent packets, the load-bearing equations include

\[
 R_C(Y,Z)\mid P(Y)Q(Z)-P(Z)Q(Y),
\tag{8.1}
\]

\[
 H(T,X)\mid M(T,X),
\tag{8.2}
\]

\[
 H(T,X)\mid
 R_C\!\left(h(T),h(\psi(X))\right),
\tag{8.3}
\]

and, at all twelve source rows,

\[
 H(\alpha_i,X)\mid \frac{B(X)}{z_i(X)},\qquad
 \prod_{i=1}^{12}H(\alpha_i,X)\sim B(X)^2.
\tag{8.4}
\]

Every component must terminate in an actual-producer contradiction, a
strict coarser decomposition, a chronology-valid same-record owner, or an
explicit unpaid primitive source-incidence component.  A branch passport
alone is none of these.

Layer-cake, dyadic summability, moments, Markov, and Chebyshev are not
applicable.  All computations are exact finite group, permutation, or
integer arithmetic; none is sampling or asymptotic evidence.

The \(u=2\) branch, K3 item, and KoalaBear row remain open.  No exact
distinct-slope charge or ledger field changes.
