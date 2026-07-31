---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the inner-degree-12 transverse terminal, the derived kernel of the five-block action is a subdirect product of five isomorphic simple degree-12 socles. Scott's lemma and primitivity of the degree-five block action leave only the independent product and one full diagonal strip. The actual size-four suborbit excludes the independent product. Exact degree-12 point-stabilizer orbits, including a paired-generator audit of the two M12 actions, then force outer subdegree four and equivalent socle actions on all five blocks. The normalizer of this diagonal socle preserves twelve blocks of size five, forcing a second geometric decomposition of the endpoint map with inner degree five. The inherited source-fiber adapter deletes every such decomposition over the challenge field. Hence the entire inner-degree-12 row is empty.
architecture: null
partition_digest: null
atom_or_cell: K3_M12_DIAGONAL_SOCLE_DEGREE5_CLOSE
quantifier: every actual inner-degree-12 transverse terminal satisfying the imported source-pencil, outer-subdegree, and source-fiber packets
projection_and_unit: exact geometric route deletion; not a carrier owner, received-line theorem, or distinct-slope payment
claimed_bound: both remaining inner-degree-12 transverse types are empty; the global transverse frontier falls from 24 to 22 types and the live decomposition degrees are 2,3,4,6,10
status: PROVED_M12_DECOMPOSITION_ROW_EMPTY_OTHER_K3_ROWS_OPEN
impact: DELETES_THE_COMPLETE_INNER_DEGREE_12_ROW_BY_A_SECONDARY_INNER_DEGREE_5_CONTRADICTION
falsifier: failure of the six-group degree-12 catalogue, a nontrivial kernel projection missing the simple socle, a third Scott-strip support partition, a shorter opposite-action M12 orbit, a nontrivial centralizer of the two-transitive socle, or a monodromy block system of size five not yielding an inner-degree-five decomposition
replay: python3 experimental/scripts/verify_kb_mca_v4_m12_diagonal_socle_degree5_close_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-12 diagonal-socle close

## 0. Verdict

The complete inner-degree-\(12\) decomposition row is empty:

\[
  \boxed{m=12\quad\Longrightarrow\quad\text{no actual transverse terminal}.}
\tag{0.1}
\]

The parent route cut left

\[
  (r,\delta)=(2,24),(4,12).
\tag{0.2}
\]

The argument below first deletes \(r=2\), then shows that every \(r=4\)
terminal would force a second decomposition of the same degree-\(60\)
endpoint map with inner degree \(5\).  The already-proved source-fiber
adapter deletes every such degree-\(5\) decomposition over the challenge
field.  Thus both rows in (0.2), and hence all six geometric outer families
printed by the normal-form compiler, have no actual producer.

This is an \(m=12\) route closure with zero ledger movement.  It does not
close \(u=2\), K3, or the KoalaBear row.

## 1. Imported terminal

Let \(G\) be the geometric monodromy group of

\[
  f=F\circ h,
  \qquad \deg h=12,
  \qquad \deg F=5.
\tag{1.1}
\]

The action has five blocks \(B_0,\ldots,B_4\), each of size \(12\).  Let
\(N\triangleleft G\) be the kernel of the action on these blocks.  The
source-pencil compiler and the outer-subdegree route cut supply:

- the terminal inner map \(h\) is geometrically indecomposable, so its
  separable degree-\(12\) monodromy is primitive;
- the actual bidegree-\((4,4)\) component is not a same-inner-fiber
  component;
- a point stabilizer of \(G\) therefore has an actual suborbit
  \(\Delta\) of size \(4\) which meets a block other than its home block;
- the block projection of \(\Delta\) is an outer point-stabilizer suborbit
  of size \(r\in\{2,4\}\).

The source-fiber adapter independently proves that **every** geometric
decomposition of this endpoint map with inner degree \(5\) is impossible
over \(K=\mathbf F_{p^6}\), \(p=2{,}130{,}706{,}433\).

## 2. The derived block kernel is subdirect

Let \(H_i\) be the block stabilizer induced on \(B_i\), and let \(P_i\) be
the projection of \(N\) to \(H_i\).  The complete terminal catalogue is

\[
\begin{array}{c|r|c|c}
H_i&|H_i|&\operatorname{soc}(H_i)&\text{subdegrees}\\ \hline
M_{11}&7{,}920&M_{11}&1,11\\
M_{12}&95{,}040&M_{12}&1,11\\
\operatorname{PSL}(2,11)&660&\operatorname{PSL}(2,11)&1,11\\
\operatorname{PGL}(2,11)&1{,}320&\operatorname{PSL}(2,11)&1,11\\
A_{12}&12!/2&A_{12}&1,11\\
S_{12}&12!&A_{12}&1,11.
\end{array}
\tag{2.1}
\]

The subgroup \(P_i\triangleleft H_i\) is nontrivial.  Otherwise the action
of \(H_i\) would factor through an outer point stabilizer, whose order is at
most \(24\), whereas every group in (2.1) has order at least \(660\).
Since \(H_i\) is almost simple, \(P_i\) contains its simple socle \(S_i\),
and

\[
  [P_i,P_i]=S_i.
\tag{2.2}
\]

Put \(D=[N,N]\).  Projection commutes with taking the derived subgroup, so
\(D\leq\prod_i S_i\) projects onto every \(S_i\).  It is a subdirect product
of five isomorphic nonabelian simple groups.

## 3. Scott strips force a full diagonal

Scott's subdirect-product lemma writes \(D\) as a direct product of full
diagonal strips whose supports partition the five coordinates.  Since
\(D\char N\triangleleft G\), the degree-\(5\) block action preserves the
support partition.  A transitive group of prime degree is primitive, so
only two support partitions are possible:

\[
 D=S_0\times\cdots\times S_4,
 \qquad\text{or}\qquad
 D\cong S\text{ is one full twisted diagonal strip}.
\tag{3.1}
\]

Fix \(\alpha\in B_0\).  In the independent case, \(D_\alpha\) contains the
full transitive factor \(S_j\) on every \(B_j\ne B_0\).  Any orbit meeting a
different block then has at least \(12\) points.  This contradicts the
actual \(|\Delta|=4\).  Therefore \(D\) is one full diagonal strip.

## 4. The outer subdegree is four

Identify \(D\) with its simple factor \(S\), and put \(A=D_\alpha\).  For
each equivalent degree-\(12\) action, \(A\) has orbits \(1,11\), hence one
fixed point.  The only possible inequivalent cross-action is between the
two degree-\(12\) actions of \(M_{12}\), exchanged by its outer
automorphism.

The verifier aligns the ATLAS standard generators in the \(12a\) and
\(12b\) representations and reconstructs their paired image exactly.  It
has order \(95{,}040\); a \(12a\)-point stabilizer has order \(7{,}920\),
same-action orbits \(1,11\), and is transitive on all \(12\) points of the
\(12b\) action.  Thus an opposite \(M_{12}\) action offers no short
cross-orbit.

Because \(D_\alpha\triangleleft G_\alpha\), every \(D_\alpha\)-orbit
through a point of \(\Delta\) lies in \(\Delta\).  Each block met by
\(\Delta\) therefore contributes exactly its unique fixed point, and an
opposite \(M_{12}\) block cannot be met.  Hence

\[
  r=\#\{B_i:B_i\cap\Delta\ne\varnothing\}=|\Delta|=4.
\tag{4.1}
\]

This deletes \((r,\delta)=(2,24)\).  Since the \(r=4\) orbit meets all four
other blocks, all five \(S\)-actions are equivalent, including when
\(S=M_{12}\).

## 5. A secondary degree-five decomposition

Choose \(D\)-equivariant identifications \(B_i\simeq X\), \(|X|=12\), so
that \(s\in S\) acts by

\[
  (x,i)\longmapsto(sx,i).
\tag{5.1}
\]

The action of \(S\) on \(X\) is faithful and two-transitive.  Its
centralizer in \(\operatorname{Sym}(X)\) is trivial.  Indeed, a centralizer
element fixing one point fixes all points by transitivity.  If it sends
\(\alpha\) to \(\beta\ne\alpha\), then the transitive point stabilizer
\(S_\alpha\) fixes \(\beta\), a contradiction.

For \(g\in G\), let \(\pi_g\) be its permutation of the five original
blocks and let \(n_i:B_i\to B_{\pi_g(i)}\) be its restriction in the chosen
\(X\)-coordinates.  Normality of \(D\) gives one
\(\phi_g\in\operatorname{Aut}(S)\) with

\[
  n_i s n_i^{-1}=\phi_g(s)\quad\text{for every }i.
\tag{5.2}
\]

Thus \(n_j^{-1}n_i\) centralizes \(S\), so all \(n_i\) equal one
permutation \(n_g\).  Every \(g\) has the form

\[
  g(x,i)=(n_g(x),\pi_g(i)).
\tag{5.3}
\]

Consequently \(G\) preserves the twelve columns

\[
  C_x=\{(x,0),\ldots,(x,4)\},\qquad x\in X.
\tag{5.4}
\]

These are monodromy blocks of size \(5\).  The
monodromy/intermediate-field correspondence and Luroth's theorem therefore
give a second geometric functional decomposition of the same endpoint map,
now with inner degree \(5\) and outer degree \(12\).

The imported source-fiber adapter applies to every geometric decomposition.
For inner degree \(5\), two rational total ramification points exhaust the
Riemann--Hurwitz budget and force a fifth-power cover over \(K\).  But

\[
  \gcd(5,p^6-1)=1,
\tag{5.5}
\]

so fifth powering permutes \(K\) and cannot contain a reduced five-point
\(K\)-rational active fiber.  This contradiction deletes the remaining
\((r,\delta)=(4,12)\) row and proves (0.1).

## 6. Exact frontier and nonclaims

The outer-subdegree packet reduced the compiler's \(26\) transverse types
to \(24\).  This packet deletes the two remaining \(m=12\) types, leaving
\(22\) transverse types in inner degrees

\[
  \boxed{m\in\{2,3,4,6,10\}.}
\tag{6.1}
\]

The following remain open:

- elimination or ownership of those \(22\) transverse types;
- the parameter-to-carrier, received-data, explaining-polynomial, and
  slope bridges;
- \(u=2\), K3, and KoalaBear row closure;
- every numerical ledger payment and the final prize inequalities.

No endpoint record is enumerated, no owner is constructed, and no ledger
quantity moves.

## 7. Source custody and replay

The certificate binds immutable copies of the parent route-cut packet, the
source-fiber adapter, and the optional six-family normal-form compiler.  The
finite group inputs are:

- GAP PrimGrp commit
  5612e113d50ac23a7d10945383936e20440b4e14, file data/gps1.g,
  degree-\(12\) entry SHA-256
  9165e7e00ecebd79aaa1272ac83747529839a86191c859b56d49c01d88d12166;
- Leonard L. Scott, *Representations in characteristic p*, Proc. Symp. Pure
  Math. 37 (1980), 319--331, lemma on page 328,
  DOI 10.1090/pspum/037/604599;
- ATLAS standard-generator files for M12G1-p12aB0 and M12G1-p12bB0,
  concatenated SHA-256
  55af41251add2886aedb2ebf04dfb522776768a245dd9e6cd8369094cf84aa38.

The replay checks the complete arithmetic and group ledger, enumerates the
paired \(M_{12}\) group, verifies source custody, and rejects deterministic
semantic mutations.  It performs no broad endpoint search.
