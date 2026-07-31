---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every inner-degree-10 transverse terminal routes strictly to inner degree 2, 3, or 6. If the six-block kernel is trivial, the global degree-60 action is the A6 or S6 point/two-subset flag action, and its exact subdegrees exclude the actual quartic suborbit. Otherwise the derived kernel is subdirect in six simple degree-10 socles. Scott strips have support size 1,2,3,6; size one is impossible, while the other sizes preserve synchronized column blocks and force a second decomposition of that smaller inner degree.
architecture: null
partition_digest: null
atom_or_cell: K3_M10_SCOTT_STRIP_LOWER_DEGREE_ROUTER
quantifier: every actual inner-degree-10 transverse terminal satisfying the imported source-pencil compiler
projection_and_unit: exact geometric strict-decomposition route; not a carrier owner, received-line theorem, or distinct-slope payment
claimed_bound: all four inner-degree-10 transverse types cease to be independent producers; the global independent transverse frontier falls from 22 to 18 types in inner degrees 2,3,4,6
status: PROVED_M10_ROUTED_TO_INNER_DEGREES_2_3_6_OTHER_K3_ROWS_OPEN
impact: REMOVES_M10_AS_A_TERMINAL_PRODUCER_BY_KERNEL_FREE_FLAG_EXCLUSION_OR_SCOTT_STRIP_COLUMNS
falsifier: a kernel-free A6 or S6 flag action with subdegree four, a Scott support size outside 1,2,3,6, an unrealized degree-10 socle automorphism, a nontrivial action centralizer, or a synchronized strip column that fails to yield an inner-degree-t decomposition
replay: python3 experimental/scripts/verify_kb_mca_v4_m10_scott_strip_lower_degree_router_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-10 Scott-strip router

## 0. Verdict

Every actual inner-degree-\(10\) transverse terminal routes strictly to a
smaller decomposition:

\[
  \boxed{m=10\quad\Longrightarrow\quad m'\in\{2,3,6\}.}
\tag{0.1}
\]

This removes the four \(m=10\) types as independent producers. Combined
with the proved \(m=12\) close, the transverse frontier is \(18\) types in
degrees \(2,3,4,6\).

Equation (0.1) is routing, not nonexistence of every degree-\(10\)
decomposition. It moves no ledger and does not close \(u=2\), K3, or the
KoalaBear row.

## 1. Imported terminal

The source-pencil compiler supplies

\[
 f=F\circ h,\qquad \deg h=10,\qquad\deg F=6,
\tag{1.1}
\]

with six monodromy blocks \(B_0,\ldots,B_5\) of size ten. The inner map is
geometrically indecomposable, its monodromy is primitive, and the actual
quartic component gives a transverse point-stabilizer suborbit
\(\Delta\) of size four.

Let \(N\) be the kernel on the six blocks, \(H_i\) the induced group on
\(B_i\), and \(P_i\) the image of \(N\) there. The complete catalogue is

\[
\begin{array}{c|r|c|c}
H_i&|H_i|&\operatorname{soc}(H_i)&\text{subdegrees}\\ \hline
A_5&60&A_5&1,3,6\\
S_5&120&A_5&1,3,6\\
\operatorname{PSL}(2,9)&360&A_6&1,9\\
\operatorname{PGL}(2,9)&720&A_6&1,9\\
\operatorname{P\Sigma L}(2,9)&720&A_6&1,9\\
M_{10}&720&A_6&1,9\\
\operatorname{P\Gamma L}(2,9)&1440&A_6&1,9\\
A_{10}&10!/2&A_{10}&1,9\\
S_{10}&10!&A_{10}&1,9.
\end{array}
\tag{1.2}
\]

## 2. Kernel-free exceptions

The quotient \(H_i/P_i\) comes from an outer point stabilizer, so
\[
  |H_i/P_i|\leq5!=120.
\tag{2.1}
\]

If \(P_i=1\), only \(A_5,S_5\) remain. All coordinate projections of \(N\)
then vanish, hence \(N=1\). The outer block stabilizer maps faithfully onto
\(H_i\): the only possible extra case would require an order-two normal
subgroup of \(S_5\). Thus \(G=A_6\) or \(S_6\), acting on the 60 flags

\[
  \Omega=\{(i,A):i\in\{1,\ldots,6\},\
                    A\subset\{1,\ldots,6\}\setminus\{i\},\ |A|=2\}.
\tag{2.2}
\]

Exact stabilizer enumeration gives

\[
\begin{array}{c|l}
A_6&1,2,3,3,3,6,6,6,6,6,6,6,6\\
S_6&1,2,3,3,3,6,6,6,6,6,6,12.
\end{array}
\tag{2.3}
\]

Neither row contains four, contradicting \(|\Delta|=4\). Hence the kernel
projection is nontrivial.

## 3. Scott strips

Let \(S_i=\operatorname{soc}(H_i)\) and \(D=[N,N]\). Almost simplicity gives

\[
 D\leq S_0\times\cdots\times S_5,\qquad
 \operatorname{pr}_i(D)=S_i.
\tag{3.1}
\]

Scott's lemma partitions the coordinates into full diagonal strips. The
partition is invariant under the transitive outer action, so every support
has a common size

\[
  t\in\{1,2,3,6\}.
\tag{3.2}
\]

For \(t=1\), \(D_\alpha\) contains a full transitive ten-point factor on
every other block. Since \(\Delta\) meets another block, this contradicts
\(|\Delta|=4\). Thus \(t>1\).

All automorphisms of the three possible socles are realized in their
degree-10 actions: by \(S_5\), \(\operatorname{Aut}(A_6)=
\operatorname{P\Gamma L}(2,9)\), and \(S_{10}\), respectively. Each socle
point stabilizer has exactly one fixed point by (1.2), so its permutation
centralizer is trivial.

Untwist the actions in one Scott support \(T\) and identify their ten-point
sets with \(X_T\). For any \(g\in G\), the restrictions of \(g\) on all
blocks in \(T\) implement one common socle isomorphism. Their pairwise
ratios centralize the socle and are therefore equal. Hence \(G\) preserves
the synchronized columns

\[
  C_{T,x}=\{(x,i):i\in T\},\qquad |C_{T,x}|=t.
\tag{3.3}
\]

The monodromy/intermediate-field correspondence and Luroth's theorem turn
(3.3) into a second geometric decomposition of inner degree
\(t\in\{2,3,6\}\), proving (0.1).

## 4. Frontier and sources

The imported compiler had four \(m=10\) types:

\[
 (r,\delta)=(1,40),(2,20),(4,10),(5,8).
\tag{4.1}
\]

All route downward, so the combined \(22\)-type frontier after the \(m=12\)
close becomes \(18\). No lower-degree type is deleted.

The exact finite sources are GAP PrimGrp commit
5612e113d50ac23a7d10945383936e20440b4e14, whose 1272-byte
PRIMGRP[10] entry has SHA-256
9cf136ffbea68f3156bc2ff386b5aec7b510a77e13e77ad6a09904b02382a69e;
the online ATLAS ten-point representation of
\(\operatorname{Aut}(A_6)\); and Scott's lemma, Proc. Symp. Pure Math. 37
(1980), p.328, DOI 10.1090/pspum/037/604599.

The replay reconstructs both kernel-free flag actions, checks all route
arithmetic and historical bindings, and rejects semantic mutations. It
performs no endpoint search.
