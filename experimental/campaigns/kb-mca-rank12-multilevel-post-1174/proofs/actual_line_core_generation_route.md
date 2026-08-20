# Actual-line supported-dual generation and received-pair defect route

## Setup

Let \(D\subseteq\mathbb F\) be an evaluation domain, \(U\subseteq D\), and
let \(C_K(U)\subseteq\mathbb F^U\) be the restriction of the
degree-\((<K)\) Reed--Solomon code.  For a core \(H\subseteq U\), embed in
\((\mathbb F^U)^*\) the supported dual-annihilator

\[
A_H=\{\lambda:\operatorname{supp}(\lambda)\subseteq H,
                 \ \lambda(C_K(U))=0\}.
\]

For a finite core family \(\mathcal H=\{H_e:e\in E\}\), put

\[
A(\mathcal H)=\sum_{e\in E}A_{H_e},\qquad W=A_U,
\]

and define the local polynomial section space

\[
L(\mathcal H)=
\{f\in\mathbb F^U:f|_{H_e}\in C_K(H_e)\text{ for every }e\}.
\]

## The exact criterion

With the ordinary perfect pairing on \(\mathbb F^U\),

\[
A(\mathcal H)^\perp=L(\mathcal H),
\qquad W^\perp=C_K(U).
\]

Indeed, orthogonality to the zero-extended annihilator \(A_H\) is exactly the
condition that the restriction to \(H\) belongs to \(C_K(H)\); intersections
of these orthogonal complements correspond to the orthogonal complement of
the sum.  Consequently

\[
q(\mathcal H):=\dim W-\dim A(\mathcal H)
=\dim L(\mathcal H)-\dim C_K(U).
\tag{1}
\]

In particular, the supported duals generate the union shortened dual if and
only if every function that is polynomial on each core glues to one global
degree-\((<K)\) polynomial on \(U\).

## Actual received-pair compiler

Fix one actual received line \(r_0+\gamma r_1\).  Let \(E\ne\varnothing\),
and for every index \(e\) retain one selected affine slope \(\gamma_e\), one
exact pair-noncontained size-\(m\) support \(S_e\), its explanation \(h_e\),
and assume all \(h_e\) lie in one affine translate \(h_*+C'\).  Choose
\(b_e\in C'\) minimizing the raw margin
\(|\{x\in S_e:r_1(x)\ne b_e(x)\}|\).  Put
\(a_e=h_e-\gamma_e b_e\) and

\[
H_e=\{x\in D:r_0(x)=a_e(x),\ r_1(x)=b_e(x)\}.
\]

Put \(U=\bigcup_{e\in E}H_e\).

Assume the indexed slopes are distinct and belong to the intrinsic post-near
set \(Z=Z_{\rm bad}\setminus N\), where \(N\) is the proved near-rational
stratum.  Then \(r_0|_U,r_1|_U\in L(\mathcal H)\), because on \(H_e\)
their restrictions are the degree-\((<K)\) polynomials \(a_e,b_e\).  Let

\[
Q(\mathcal H)=L(\mathcal H)/C_K(U)
\]

and define the received-pair defect rank

\[
c(\mathcal H)=
\dim\operatorname{span}\{[r_0|_U],[r_1|_U]\}\le\min\{2,q(\mathcal H)\}.
\tag{2}
\]

Every such actual family has exactly one of three terminals:

1. \(c=0\): both received restrictions are global degree-\((<K)\)
   evaluation words on \(U\).  On the initial rank-twelve row, if
   \(|U|\ge m\), this branch has at most
   \[
   981104+\left\lfloor
   \frac{3313389801746721900417-981104}{67473}
   \right\rfloor
   =49106899082787469
   \]
   distinct slopes, with slack \(199599500258500901\) to the rank-ten
   child target;
2. \(c=1\): the kernel of
   \((\alpha,\beta)\mapsto[\alpha r_0+\beta r_1]\) is one-dimensional, so
   exactly one projective scalar combination is globally polynomial on \(U\);
3. \(c=2\): the kernel is zero, so no nonzero projective combination is
   globally polynomial on \(U\).

For the rank-zero bound, split the exact selected records by raw support
margin.  If the margin is at most \(d\), its support meets its complete pair
core in at least \(m-d=K\) coordinates.  The selected pair must therefore
equal the global pair on \(U\).  Distinct raw-low slopes then use disjoint
nonempty exception sets outside the complete common core, so there are at
most \(n-m=981104\) of them.  If their count is \(L_0\), the nonuniform
margin resource bounds the remaining records by
\(\lfloor(C_{11}(R)-L_0)/(d+1)\rfloor\).  The sum is nondecreasing in
\(0\le L_0\le981104\), giving the displayed endpoint.

This is a same-line, same-core statement.  It changes neither slopes nor
owners and imports no multiplicity.

The old inference \(c=0\Rightarrow\gamma\in N\) is false: it confuses
\(n-m\) with \(w=m-K\).  The shipped \(\mathbb F_{11}\) regression has
\((n,K,m,w)=(10,3,4,1)\), six post-near slopes, and a size-four common
rank-zero union.  It is a mandatory boundary control for the payment above.

## A sufficient generating condition and its boundary

Assume every \(H_e\) has size at least \(K\).  If the cores admit an ordering

\[
H_1,\ldots,H_t
\quad\text{with}\quad
|H_i\cap(H_1\cup\cdots\cup H_{i-1})|\ge K
\quad(i\ge2),
\tag{3}
\]

then \(q(\mathcal H)=0\).  To prove this, choose a degree-\((<K)\) polynomial
representing a local section on \(H_1\).  At step \(i\), the new local
polynomial agrees with the previously glued polynomial on at least \(K\)
evaluation points, hence is identical by Reed--Solomon uniqueness.  Induct.

Therefore condition \((3)\) gives \(q=0\), hence \(c=0\), and routes the
initial rank-twelve family to the paid terminal above.  This is the first
source-bound combinatorial conclusion beyond the scalar resource barrier.

The converse is false.  The public SYZ25 control at \((n,K)=(6,3)\) has
three size-four cores with nominal excess equal to \(|U|-K=3\), but their supported
duals span only dimension two.  The shipped Sage replay verifies

\[
q=1,\qquad \dim L=4,\qquad \dim C_K(U)=3.
\]

So neither overbudget core count nor dimension bookkeeping may be promoted
to generation.

## Route-cut boundary

This compiler does not pay rank twelve.  It replaces the vague phrase
"cross-pair compatibility" by a precise actual-record obstruction:

\[
\boxed{\text{a local-polynomial gluing quotient }Q(\mathcal H),
       \text{ with }c=0\text{ paid and residual }c\in\{1,2\}.}
\]

The maximal next theorem must count or route actual core families in these
two defect classes.  The \(c=1\) branch should be compared with the proved
one-function/projective-pencil owners; the \(c=2\) branch with the public
dual-plane/Segre circuit routers.  Any transport must preserve the identical
received line, supports, slopes, field, and first-match chronology.

The initial-row exact-support, union-size, and margin-resource hypotheses are
load-bearing for the numerical rank-zero payment.  Outside that domain,
\(c=0\) remains an explicit
`COMMON_PAIR_CORE_PRESENT_WITH_LOCAL_BAD_SUPPORTS` terminal.
