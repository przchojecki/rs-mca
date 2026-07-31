---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the inner-degree-12 terminal emitted by the source-pencil compiler, the degree-five outer self-correspondence types r=1 and r=3 are impossible. Primitive degree-five monodromy has no subdegree three. A subdegree-one component would make the outer cover cyclic of degree five; its rational total pole and second rational branch point give a K-rational form a*x^5+b, contradicting the five distinct K-rational outer zeros because fifth powering is bijective on K=F_(p^6). Only (r,delta)=(2,24),(4,12) remain at m=12.
architecture: null
partition_digest: null
atom_or_cell: K3_M12_OUTER_SUBDEGREE_ROUTE_CUT
quantifier: every actual inner-degree-12 transverse terminal satisfying the imported source-pencil compiler hypotheses
projection_and_unit: exact geometric outer-correspondence route cut; not a carrier owner, received-line theorem, or distinct-slope payment
claimed_bound: two of the four inner-degree-12 transverse types are empty; the global transverse frontier falls from 26 to 24 types
status: PROVED_M12_OUTER_SUBDEGREE_ROUTE_CUT_ROW_OPEN
impact: DELETES_M12_R1_AND_R3_TRANSVERSE_TYPES_AND_LEAVES_EXACTLY_R2_AND_R4
falsifier: a primitive degree-five group with subdegree three, or a degree-five cyclic cover over K with one rational total pole and five distinct simple rational zeros
replay: python3 experimental/scripts/verify_kb_mca_v4_m12_outer_subdegree_route_cut_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-12 outer-subdegree route cut

## 0. Verdict

The degree-12 transverse row of the source-pencil compiler has only two
remaining geometric types:

\[
  \boxed{(r,\delta)=(2,24),(4,12).}
\tag{0.1}
\]

The compiler initially emits

\[
  (r,\delta)=(1,48),(2,24),(3,16),(4,12).
\tag{0.2}
\]

Primitive degree-5 monodromy excludes \(r=3\).  If \(r=1\), the
correspondence is the graph of a nonidentity deck transformation.  The
degree-5 cover is then cyclic.  Its two total branch points are rational
over the challenge field, so the outer map has a challenge-field normal form
\(a x^5+b\).  Fifth powering is bijective on the challenge field, whereas
the imported source-fiber theorem gives five distinct rational simple outer
zeros.  This contradiction excludes \(r=1\).

This is a route cut, not a payment.  It does not eliminate either survivor
in (0.1), close inner degree \(12\), close \(u=2\) or K3, identify an
evaluation-carrier owner, or move any ledger quantity.

## 1. Imported geometric terminal

Let

\[
  K=\mathbf F_{p^6},\qquad p=2{,}130{,}706{,}433.
\tag{1.1}
\]

The parent source-pencil compiler starts from a geometric irreducible
bidegree-\((4,4)\) actual component \(\Gamma\), routes the inner map to a
geometrically indecomposable right component \(h\), and proves that every
terminal survivor is transverse to the fibers of \(h\).  In the
inner-degree-12 row,

\[
  f=F\circ h,\qquad \deg h=12,\qquad \deg F=5.
\tag{1.2}
\]

The geometric image

\[
  C=\overline{(h\times h)(\Gamma)}
     \subset\{F(Y)=F(Z)\}
\tag{1.3}
\]

is geometrically irreducible and non-diagonal.  Write
\(\operatorname{bideg}C=(r,r)\) and
\(\delta=\deg(\Gamma\to C)\).  The exact projection ledger is

\[
  \delta r=4\deg h=48,
  \qquad \delta\le(\deg h)^2=144,
  \qquad 1\le r\le \deg F-1=4.
\tag{1.4}
\]

Equation (1.4) gives exactly the four types in (0.2).

The parent source-fiber theorem also gives the outer divisor profile.  There
is one pole \(P\) of order five and five distinct simple zeros.  The inner
pencil and outer map descend to \(K\).  The unique pole is therefore
\(K\)-rational.  Each outer zero is the \(h\)-value of a complete active
fiber consisting of individually \(K\)-rational points, so all five outer
zeros are individually \(K\)-rational.

These are imported facts.  This packet does not reconstruct an endpoint
record or enumerate the records passing the degree-12 pencil test.

## 2. Exclusion of \(r=3\)

Because \(F\) has prime degree five, it is geometrically indecomposable.
Its characteristic is greater than five, so it is separable and its
geometric monodromy group is primitive of degree five.

Over an algebraic closure, irreducible components of
\(F(Y)=F(Z)\) correspond to point-stabilizer suborbits.  The degree in either
coordinate is the associated subdegree.  The complete primitive
degree-5 catalogue is

\[
\begin{array}{c|c}
\text{group}&\text{subdegrees}\ \hline
C_5&(1,1,1,1,1)\\
D_{10}&(1,2,2)\\
\operatorname{AGL}(1,5)&(1,4)\\
A_5&(1,4)\\
S_5&(1,4).
\end{array}
\tag{2.1}
\]

No row in (2.1) has subdegree three.  Since \(C\) in (1.3) is a geometric
irreducible component, \(r=3\) is impossible.  This deletes
\((r,\delta)=(3,16)\).

## 3. Exclusion of \(r=1\)

Assume \(r=1\).  A geometrically irreducible curve of bidegree \((1,1)\)
in \(\mathbf P^1\times\mathbf P^1\) is the graph of a Mobius
transformation \(\sigma\).  Since \(C\) is non-diagonal,
\(\sigma\ne1\), while (1.3) gives

\[
  F\circ\sigma=F.
\tag{3.1}
\]

Thus \(\sigma\) is a nontrivial automorphism of the separable function-field
extension

\[
  \overline K(Y)/\overline K(F),
\tag{3.2}
\]

which has prime degree five.  The automorphism-group order divides the
extension degree.  It is therefore five, and (3.2) is a cyclic Galois
extension.

A tame cyclic subgroup of order five in
\(\operatorname{PGL}_2(\overline K)\) has exactly two fixed points.  The
quotient map \(F:\mathbf P^1\to\mathbf P^1\) is totally ramified at those
two points and nowhere else.  One is the unique pole \(P\).  Let the other
be \(Q\).  The ramification divisor is defined over \(K\); after removing
the unique \(K\)-rational point \(P\), its other uniquely determined point
\(Q\) is also \(K\)-rational.

Choose \(\phi\in\operatorname{PGL}_2(K)\) sending \(Q\) to zero and \(P\)
to infinity.  Because \(F(Q)\in K\), the divisor of
\(F\circ\phi^{-1}-F(Q)\) is

\[
  5[0]-5[\infty].
\tag{3.3}
\]

Consequently

\[
  F\circ\phi^{-1}(x)=a x^5+b,qquad a\in K^*,\quad b\in K.
\tag{3.4}
\]

Now

\[
  p\equiv3\pmod5,qquad p^6\equiv4\pmod5,qquad
  \gcd(5,p^6-1)=1.
\tag{3.5}
\]

Hence \(x\mapsto x^5\) permutes \(K\).  If \(b=0\), (3.4) has one zero
of multiplicity five.  If \(b\ne0\), it has exactly one \(K\)-rational
zero.  Neither case permits the five distinct simple \(K\)-rational zeros
imported in Section 1.  Therefore \(r=1\) is impossible, deleting
\((r,\delta)=(1,48)\).

## 4. Exact frontier and nonclaims

Removing the two impossible rows from (0.2) proves (0.1).  Across all six
inner degrees, the parent compiler emitted \(26\) transverse
\((m,r,\delta)\) types.  This packet deletes exactly two and leaves \(24\).

The following remain open:

- elimination or ownership of the \((2,24)\) and \((4,12)\) types;
- elimination or ownership of every transverse type in the other inner
  degrees;
- a same-record parameter-to-carrier, received-data, explaining-polynomial,
  or slope bridge;
- inner-degree-12, \(u=2\), K3, and KoalaBear row closure.

No endpoint record is enumerated, no survivor is paid, and no ledger
quantity moves.
