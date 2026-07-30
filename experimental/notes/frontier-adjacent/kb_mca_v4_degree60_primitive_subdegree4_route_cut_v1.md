---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Complete-source saturation puts all 24 pole units of a birational-quartic u=2 component on 12-line star vertices, with total repeated-vertex defect at most three. After the proved line/conic exclusions, every residual actual u=2 component induces a non-diagonal bidegree-(4,4) component of the degree-60 endpoint self-correspondence. Such a component gives geometric monodromy subdegree four. The exhaustive primitive-group classification in degree 60 has nine groups and none has subdegree four. Hence every residual actual u=2 survivor forces a geometric functional decomposition of the endpoint map.
architecture: null
partition_digest: null
atom_or_cell: K3_Q6_U2_PRIMITIVE_SUBDEGREE4_ROUTE_CUT
quantifier: every residual actual Q=6,s=6,u=2 birational-quartic outgoing component after the retained source reduction and the proved line/conic exclusions, independently of pole partition, signature, and simple/repeated/ramified quartic chart
projection_and_unit: geometric component/decomposition obstruction; not a distinct-slope count
claimed_bound: every birational-quartic source divisor has at least 21 distinct star vertices and only the printed defect types; primitive degree-60 monodromy is impossible; every residual surviving u=2 component lies in the decomposable endpoint-map branch
status: PROVED_CLASSIFICATION_BACKED_ROUTE_CUT_ROW_OPEN
impact: REMOVES_PRIMITIVE_U2_BRANCH_AND_REPLACES_QUARTIC_ATLAS_BY_DECOMPOSITION_ADAPTER
falsifier: a primitive permutation group of degree 60 with a point-stabilizer orbit of size four, a failure of the component/suborbit correspondence, or a residual actual birational-quartic u=2 component not descending to bidegree (4,4)
replay: python3 experimental/scripts/verify_kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.py --check --tamper-selftest && sage experimental/scripts/verify_kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.sage
---

# KoalaBear degree-\(60\) primitive-subdegree-four route cut

## 0. Verdict

The primitive residual \(u=2\) route is empty.

After the proved line/conic exclusions, every residual actual
\(Q=6,s=6,u=2\) birational-quartic outgoing component produces a
non-diagonal irreducible component of the endpoint self-correspondence

\[
f(T)=f(W)
\]

of bidegree \((4,4)\).  Therefore the geometric monodromy group of the
degree-\(60\) rational map \(f\) has a point-stabilizer orbit of size four.

There are exactly nine primitive permutation groups of degree \(60\), up
to permutation isomorphism.  Their nontrivial subdegrees are

\[
\begin{array}{c|r|l}
\text{\(\operatorname{PrimitiveGroup}(60,i)\)}&
|G|&\text{subdegrees}\\ \hline
1&3{,}600&12,12,15,20\\
2&7{,}200&15,20,24\\
3&7{,}200&15,20,24\\
4&7{,}200&12,12,15,20\\
5&14{,}400&15,20,24\\
6&102{,}660&59\\
7&205{,}320&59\\
8&|A_{60}|&59\\
9&|S_{60}|&59.
\end{array}
\tag{0.1}
\]

None contains subdegree four.  Thus the geometric monodromy is
imprimitive, equivalently \(f\) is geometrically functionally
decomposable.

Complete-source saturation also removes the former unbounded
repeated/ramified quartic charts.  All \(24\) pole multiplicity units map to
vertices of the complete twelve-line source star, and the rational quartic
genus budget gives

\[
\sum_v\binom{w_v}{2}\le3.
\tag{0.2}
\]

Consequently at least \(21\) distinct star vertices occur.  The only
nonsimple multiplicity patterns are up to three weight-two vertices, or one
weight-three vertex.

This is a global route cut, not yet a deletion or payment.  It replaces the
old primitive \(985\)-representative simple-quartic eliminant, together with
its repeated and ramified charts, by one source-bound functional-decomposition
adapter.  A decomposition must still be shown to preserve the evaluation
domain and all witness data, or be excluded directly.  No ledger value moves.

## 1. Imported component theorem

Work over the algebraic closure of the deployed field of characteristic

\[
p=2{,}130{,}706{,}433>60.
\]

The retained source reduction constructs the degree-\(60\) rational endpoint
map

\[
f=\frac{V_{\rm act}}{A^5}
\tag{1.1}
\]

and proves that every live component maps onto the self-correspondence of
\(f\).  More precisely, for an actual outgoing component \(H_0\) of
bidegree \((u,2u)\), the map

\[
(T,\lambda)\longmapsto (T,W=\psi(\lambda))
\tag{1.2}
\]

maps \(H_0\) onto a non-diagonal irreducible component \(\Gamma\) of the
equation

\[
f(T)=f(W).
\tag{1.3}
\]

In the residual birational-quartic branch this map is birational and
\(\Gamma\) has bidegree

\[
(2u,2u).
\tag{1.4}
\]

This is Corollary 9.5 of
`experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/`
`proof/pole_disjoint_conic_facet_collinearity_reduction.md` at source commit
`44542e91e459364a521870ed2ebde7f6fe5055bf`; its theorem status was retained
by manual integration commit
`0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d`.

For completeness, the birationality gate is not being imported silently.
Let \(\sigma\) be the involution induced by the quadratic deck map
\(\psi\).  If \(\sigma(H_0)=H_0\), then the bidegree-\((u,2u)\) divisor
descends through \(\mathbf P^1_\lambda/\langle\sigma\rangle\); for \(u=2\)
its pole-coefficient map therefore factors through a degree-two quotient
and has image of degree at most two.  That is precisely the already
excluded line/conic coefficient-image branch.  Hence a residual
birational-quartic \(H_0\) and \(\sigma(H_0)\) are distinct components of
the quadratic base change over the same \(\Gamma\).  Each has generic
degree one over \(\Gamma\), because the total base-change degree is two.
Thus \(H_0\to\Gamma\) is birational, and the projection-degree argument in
Corollary 9.5 gives (1.4).

For \(u=2\), (1.4) gives

\[
\boxed{\operatorname{bideg}\Gamma=(4,4).}
\tag{1.5}
\]

The line branch was already excluded, and the complete-source theorem in
PR \(\#1128\) excludes the conic branch.  Therefore every residual \(u=2\)
component is birational-quartic, the birationality gate above applies, and
(1.5) holds uniformly on the residual branch.

## 2. Complete-source quartic defect gate

The local equality in the complete-source theorem did not use the conic
hypothesis.  Let \(x\) be a geometric root of \(B\), of multiplicity
\(m_x\in\{1,2\}\).  Every source row

\[
q_i(X)=H(\alpha_i,X)
\]

divides \(B\), while the nonzero quadratic \(H(T,x)\) vanishes at at most
two distinct source labels.  The saturated local equality

\[
\sum_i\operatorname{ord}_xq_i=2m_x
\tag{2.1}
\]

therefore has exactly two nonzero summands, both equal to \(m_x\).
Consequently the coefficient-map point \(\varphi_H(x)\) is the transverse
star vertex

\[
\mathscr L_i\cap\mathscr L_j,
\qquad i\ne j,
\tag{2.2}
\]

and the normalization branch at \(x\) has multiplicity \(m_x\) there.
There is no tangent/double-root alternative: one source row cannot carry
both units in (2.1), because its order is at most \(m_x\).

For a star vertex \(v\), let

\[
w_v=\sum_{\varphi_H(x)=v}m_x.
\tag{2.3}
\]

The two source lines through \(v\) are local transverse coordinates.
Their pullbacks along every normalization branch over \(v\) both have
order \(m_x\), so

\[
\operatorname{mult}_v C=w_v.
\tag{2.4}
\]

For a reduced plane-curve singularity of multiplicity \(w_v\),

\[
\delta_v\ge\binom{w_v}{2}.
\tag{2.5}
\]

The image \(C\) is an irreducible rational plane quartic.  Its arithmetic
genus is three, hence

\[
\sum_{z\in\operatorname{Sing}C}\delta_z=3,
\qquad
\sum_{\substack{v\ \mathrm{a\ source}\\\mathrm{star\ vertex}}}\delta_v\le3.
\tag{2.6}
\]

Since \(\sum_vw_v=\deg B=24\), (2.5)--(2.6) give

\[
\boxed{
\sum_v\binom{w_v}{2}\le3,\qquad
24-\#\{v:w_v>0\}\le3.}
\tag{2.7}
\]

Thus \(C\) meets at least \(21\) distinct vertices of the complete
twelve-line star.  No weight is at least four.  The exhaustive defect list
is:

\[
\begin{array}{c|c|c}
\text{weight-two vertices}&\text{weight-three vertices}&
\text{defect cost}\\ \hline
0,1,2,\text{ or }3&0&0,1,2,\text{ or }3\\
0&1&3.
\end{array}
\tag{2.8}
\]

This includes reduced, repeated-preimage, and deck-ramified source divisors
uniformly.  It does not eliminate the all-simple case.

## 3. Components are point-stabilizer suborbits

Let \(K=\overline{\mathbf F}_p\), put \(t=f(W)\), and let \(L\) be the
Galois closure of \(K(W)/K(t)\).  The geometric monodromy group

\[
G=\operatorname{Gal}(L/K(t))
\]

acts transitively on the \(60\) geometric sheets of \(f\).

Fix the sheet represented by \(W\), with stabilizer \(G_W\).  Over
\(K(W)\), the polynomial equation

\[
f(T)-f(W)=0
\tag{3.1}
\]

has its irreducible factors indexed by the \(G_W\)-orbits on the \(60\)
sheets.  The degree in \(T\) of a factor is the size of the corresponding
orbit.  Equivalently, the bidegrees of irreducible components of the
self-fiber product are the geometric subdegrees of \(G\).  The fixed sheet
gives the diagonal component and subdegree one.

The non-diagonal component \(\Gamma\) in (1.5) therefore supplies

\[
\boxed{\text{\(G\) has subdegree \(4\).}}
\tag{3.2}
\]

No source-label normalization or numerical specialization enters this
implication.  Because \(p>60\), the map is separable and the ordinary
geometric monodromy/suborbit dictionary applies without an inseparable
exception.

## 4. Exhaustive primitive degree-\(60\) classification

The GAP `PrimGrp` library contains, up to permutation isomorphism, every
primitive permutation group of degree below \(4096\).  Its degree-\(60\)
catalogue has exactly nine entries.  The exact replay computes, for each
entry,

\[
\left\{|G_W\cdot x|:x\in\{1,\ldots,60\}\right\}.
\tag{4.1}
\]

The full output is (0.1), including the diagonal orbit of size one.  In GAP
identifiers and structural descriptions:

\[
\begin{array}{c|l|l}
i&\text{structure}&\text{complete subdegree multiset}\\ \hline
1&A_5\times A_5&1,12,12,15,20\\
2&A_5:S_5&1,15,20,24\\
3&(A_5\times A_5):C_2&1,15,20,24\\
4&(A_5\times A_5):C_2&1,12,12,15,20\\
5&(A_5\times A_5):(C_2\times C_2)&1,15,20,24\\
6&\operatorname{PSL}_2(59)&1,59\\
7&\operatorname{PGL}_2(59)&1,59\\
8&A_{60}&1,59\\
9&S_{60}&1,59.
\end{array}
\tag{4.2}
\]

The five product-action groups in the first block are not
two-transitive, so their full subdegree rows are load-bearing; it is not
enough to check only the four familiar two-transitive entries.

The replay uses Sage \(10.9\), GAP \(4.14.0\), and the installed stable
`PrimGrp` catalogue identifiers.  The installed version-\(3.4.4\)
documentation and the
[official `PrimGrp` manual](https://gap-packages.github.io/primgrp/doc/chap1_mj.html)
state catalogue completeness in this degree and stability of the index
`PrimitiveGroup(n,i)`.  The classification sources named by that
documentation include Dixon--Mortimer, Roney-Dougal, and Quick.

As an independent arithmetic implementation, Wolfram Language reconstructs
the nine permutation groups from explicit generator cycles and recomputes
the point-stabilizer orbits.  It returns exactly the nine rows in (4.2).
That replay checks the group orders and orbit arithmetic independently of
GAP; catalogue completeness remains the imported classification input.

Combining (3.2) with (4.2) gives:

\[
\boxed{\text{The geometric monodromy group \(G\) is not primitive.}}
\tag{4.3}
\]

## 5. Functional-decomposition consequence

For a separable rational map on \(\mathbf P^1\), geometric
indecomposability is equivalent to primitivity of geometric monodromy.
Indeed, an intermediate rational-function field produces a nontrivial
block system; conversely a nontrivial block system gives an intermediate
field, which is rational by Lüroth's theorem.

Therefore (4.3) implies a geometric decomposition

\[
\boxed{
f=F\circ h,\qquad
1<\deg h<60,\quad
1<\deg F<60.}
\tag{5.1}
\]

This is the terminal

```text
ROUTED_TO_GEOMETRIC_FUNCTIONAL_DECOMPOSITION_ADAPTER
```

for every residual actual \(u=2\) survivor.

It is deliberately not labeled as the existing invariant-quotient owner.
The active owner requires a declared uniform folding that preserves the
evaluation domain, received data, explaining polynomial, and slope
projection.  Equation (5.1) alone supplies none of those semantic gates.

## 6. Exact pole-profile ladder for the adapter

The special pole divisor of (1.1) makes the remaining adapter finite.
Write

\[
m=\deg h,\qquad n=\deg F,\qquad mn=60.
\]

Every pole of \(f\) has exact order five.  If a pole of \(F\) has order
\(r\), then for every point \(x\) over it,

\[
e_h(x)\,r=5.
\tag{6.1}
\]

Thus \(r\in\{1,5\}\):

- over an order-five pole of \(F\), \(h\) is unramified;
- over an order-one pole of \(F\), every point has ramification index five.

Let \(a\) and \(b\) be the numbers of order-five and order-one poles of
\(F\).  Then

\[
5a+b=n.
\tag{6.2}
\]

If \(b>0\), then \(5\mid m\).  Moreover each order-one pole contributes
\(4m/5\) to the ramification divisor of \(h\).  Riemann--Hurwitz gives

\[
b\frac{4m}{5}\le2m-2.
\tag{6.3}
\]

Enumerating the proper divisors of \(60\) leaves exactly:

\[
\begin{array}{c|c|c|c}
m&n&a&b\\ \hline
2&30&6&0\\
3&20&4&0\\
4&15&3&0\\
5&12&2&2\\
6&10&2&0\\
10&6&1&1\\
12&5&1&0\\
30&2&0&2.
\end{array}
\tag{6.4}
\]

The prospective inner degrees \(15\) and \(20\) are impossible: they would
require respectively four and three order-one outer poles, exceeding
(6.3).  This table is a necessary-condition compiler, not a proof that any
row occurs.

## 7. Consequence for the quartic frontier

The previous simple-vertex birational-quartic target had up to \(985\)
pole-graph orbit representatives, followed by separate repeated-vertex and
ramified local-intersection charts.  Equation (2.7) folds the latter into
five exact defect types, while the monodromy theorem shows that every one of
these computations can only study the decomposable branch.  They cannot
close a primitive residue because no primitive residue exists.

The next maximal theorem is therefore not another quartic-chart eliminant.
It is the source-bound decomposition adapter for the eight rows in (6.4):

1. recover the block map \(h\) from the actual component;
2. test whether its fibers preserve the complete evaluation domain;
3. test whether all witness data and the explaining polynomial descend;
4. if so, route to a chronology-valid same-record quotient owner;
5. otherwise use the failed semantic gate to delete the actual producer.

Only after all eight rows terminate may the \(u=2\) branch be called closed.
The \(u=3\) branch, cap \(68\), the active row compiler, and the KoalaBear
numerator remain open.

## 8. Exact replays and evidence status

Python verifies the canonical certificate, all nine group rows, the exact
pole-profile enumeration, and mutation resistance.  It also binds the
\(\#1128\) parent head/path/blob/payload and the imported source
commit/path/blob plus manual-integration commit:

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.py \
  --check --tamper-selftest
```

Sage/GAP independently queries the exhaustive primitive catalogue and
recomputes every stabilizer orbit:

```bash
sage \
  experimental/scripts/verify_kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.sage
```

Wolfram Language independently reconstructs the nine explicit permutation
groups and recomputes their orders and stabilizer-orbit sizes.  The direct
plugin replay returned

```text
{3600,{1,12,12,15,20}}
{7200,{1,15,20,24}}
{7200,{1,15,20,24}}
{7200,{1,12,12,15,20}}
{14400,{1,15,20,24}}
{102660,{1,59}}
{205320,{1,59}}
{|A60|,{1,59}}
{|S60|,{1,59}}
```

The exact group computation proves the classification-backed finite gate.
It does not prove the imported component theorem, the classical
monodromy/decomposition dictionary, or a source-semantic owner.

## 9. Scope and nonclaims

- **Proved:** the complete-source quartic defect bound (2.7), degree-\(60\)
  primitive monodromy has no subdegree four, every residual actual
  birational-quartic \(u=2\) component therefore forces geometric functional
  decomposition, and the eight-row pole-profile ladder (6.4) is exhaustive.
- **Imported:** the actual-component descent to a non-diagonal
  bidegree-\((4,4)\) self-correspondence, primitive-group catalogue
  completeness, and the classical primitivity/decomposition equivalence.
- **Not proved:** exclusion of decomposable endpoint maps, domain-compatible
  data descent, a same-record quotient owner, \(u=2\) closure, \(u=3\),
  cap \(68\), or the KoalaBear row.
- **Ledger:** unchanged; movement is zero.
