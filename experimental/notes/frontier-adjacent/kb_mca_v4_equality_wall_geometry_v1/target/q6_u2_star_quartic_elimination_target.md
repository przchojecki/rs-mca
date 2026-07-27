# \(Q=6,s=6,u=2\) Star-Quartic Elimination Target

## 1. Status

This is the smallest currently exposed proof target in the
pole-disjoint KoalaBear equality-wall branch. It is a subtarget of:

```text
target/pole_disjoint_conic_q6_component_interpolation_target.md
```

The exact geometric reduction is proved in:

```text
proof/q6_u2_plane_map_reduction.md
```

No owner payment is booked. The target below is intended for a
symbolic proof attempt or external review.

## 2. Proved input

Let \(H(T,\lambda)\) be the actual irreducible component of
bidegree \((2,4)\). Its pole-coefficient map

\[
\varphi_H:\mathbf P^1_\lambda\to\mathbf P^2
\]

is basepoint-free with pullback degree four. The six noninvariant
source evaluations define six lines
\(\mathscr L_1,\ldots,\mathscr L_6\) in general linear position:
no three are concurrent, and their fifteen vertices are the split
quadratics

\[
(T-\alpha_j)(T-\alpha_k).
\]

The exact divisor identity is

\[
\boxed{
\varphi_H^*\left(\sum_{j=1}^6\mathscr L_j\right)
=2\psi^*\mathcal K+E_H,}
\tag{2.1}
\]

where \(\deg\psi^*\mathcal K=10\) with ramification multiplicity
allowed, and \(E_H\) is the reduced divisor of the four free pole
edges owned by \(H\).

The image type is exactly one of:

\[
(r,d)=(4,1),\qquad(2,2),\qquad(1,4).
\tag{2.2}
\]

The first two branches first produce canonical quotient precursors:

* line:
  \[
  H=a(T)P(\lambda)+b(T)Q(\lambda),
  \qquad
  H=0\Longleftrightarrow[a:b]=[-Q:P];
  \]
* conic:
  \[
  H=(\operatorname{id}\times\chi)^*\overline H,
  \qquad \deg\chi=2,\quad
  \operatorname{bideg}\overline H=(2,2).
  \]

The actual row-divisor ledger now excludes the line branch. In the
conic branch it proves that the quotient differs from the deployed
deck quotient and excludes the cases in which one or both deck branch
points lie over \(\mathcal K\). Exact star-conic geometry further
excludes the \(P_3\sqcup C_3\) signature type, leaving \(405\)
labeled \(P_6\) or \(P_2\sqcup C_4\) graphs. After cycle-union routing,
quotienting by the exact automorphism group of the pole graph leaves:

\[
\begin{array}{c|c|c|c}
\text{pole cycles}&\text{pre-geometry open orbits}&
\text{open labeled cases}&\text{open orbits}\\ \hline
6&52&405&46\\
4+2&37&378&30\\
3+3&13&405&10\\
2+2+2&12&324&10
\end{array}
\tag{2.3}
\]

For each representative, the candidate conic involution is decided
by a \(7\times3\) exact pair matrix. A conic quotient exists only if
that matrix has rank at most two and its kernel defines a
nondegenerate involution. See:

```text
proof/q6_u2_line_conic_quotient_reduction.md
proof/q6_u2_star_conic_geometry_reduction.md
experiments/classify_q6_u2_conic_graph_orbits.py
experiments/q6_u2_conic_graph_orbits.json
```

The two free-root pairs already determine the candidate involution.
Writing their binary quadratics as
\(A_rX^2+B_rXY+C_rY^2\), the two rows

\[
(C_r,B_r,-A_r)
\]

have rank two and their cross product is the unique trace-zero
candidate. It must preserve the complete common binary decic. After
pole-graph symmetry and cycle-union payment, this stronger
preliminary gate has only:

\[
\begin{array}{c|c}
\text{pole cycles}&\text{open endpoint-row orbits}\\ \hline
6&3\\
4+2&3\\
3+3&2\\
2+2+2&1
\end{array}
\tag{2.4}
\]

See:

```text
proof/q6_u2_conic_free_pair_involution_reduction.md
experiments/generate_q6_u2_conic_decic_gates.py
experiments/q6_u2_conic_decic_gate_templates.json
```

That reduction also excludes the case with exactly one deck branch
point over \(\mathcal K\). Two distinct involutions sharing that
fixed point have a nontrivial translation as their product, of order
the KoalaBear characteristic, and cannot preserve the other eight
common points. Thus every ramified common-pole conic case is closed.

In the remaining reduced branch, a surviving candidate is either:

1. a reciprocal normalizer \(\iota(x)=\mu/x\), inducing
   \(w\mapsto\mu^2/w\) on the deck quotient; or
2. part of a tame dihedral group whose rotation has exact order
   \(4\) or \(5\).

The reciprocal branch forces disjoint right neighborhoods at the two
endpoint rows; otherwise the same quotient label would have two
images, and equality of both neighbor pairs would be the already-paid
four-cycle. It therefore has only \(2,2,1,1\) open endpoint orbits
for pole types \(6,4+2,3+3,2+2+2\).

Every surviving reciprocal or dihedral candidate emits a
component-rooted source-label quotient

\[
\Theta:\mathbf P^1_w\to\mathbf P^1
\]

of degree \(2,4,\) or \(5\). It maps the five common labels to
at most three values and collapses each endpoint row's two right
neighbors. This is rooted in the same component and endpoint rows,
but it acts after the deck map and is not the deployed pair-global
domain-to-slope owner. The exact distinction and adapter target are
recorded in `q6_u2_conic_source_quotient_adapter_target.md`.

## 3. Main target: birational quartic

Assume \(\varphi_H\) is birational onto an irreducible rational
plane quartic \(C\).

### 3.1 Simple-vertex branch

First assume \(\psi^*\mathcal K\) is reduced and its ten points map
to ten distinct star vertices. Let \(G\subset K_6\) be the graph of
selected vertices and let \(\overline G\) be its complement.
Then:

\[
|E(G)|=10,\qquad |E(\overline G)|=5,
\]

and, if \(e_j\in\{0,1,2\}\) counts the owned free pole edges on
\(\mathscr L_j\),

\[
\deg_{\overline G}(j)=1+e_j.
\tag{3.1}
\]

There are exactly:

\[
\boxed{
1{,}455\text{ admissible complement graphs and }
11{,}130\text{ graph/free-edge cases}.}
\tag{3.2}
\]

They split into:

\[
\begin{array}{c|c|c}
&\text{graphs}&\text{cases}\\ \hline
\text{connected trees}&1{,}170&8{,}730\\
\text{disconnected cyclic}&285&2{,}400.
\end{array}
\tag{3.3}
\]

The relevant symmetry is the bipartition-preserving automorphism
group of the actual pole graph, not the full \(S_6\). Quotienting all
\(11{,}130\) cases by that group gives:

\[
\begin{array}{c|c|c|c|c}
\text{pole cycles}&\text{all orbits}&
\text{tree orbits}&\text{cyclic orbits}&
\text{open after cycle-union}\\ \hline
6&985&768&217&985\\
4+2&490&359&131&488\\
3+3&188&138&50&188\\
2+2+2&79&53&26&77
\end{array}
\tag{3.4}
\]

Thus the largest exact simple-vertex eliminant has \(985\)
representatives, not \(11{,}130\). The classification and
tamper-checked certificate are:

```text
proof/q6_u2_quartic_orbit_reduction.md
experiments/classify_q6_u2_quartic_graph_orbits.py
experiments/q6_u2_quartic_graph_orbits.json
```

For one case, let \(R_j\) be the quartic section of
\(\mathscr L_j\) whose zeros are the selected star vertices on that
line and its \(e_j\) selected free points. The restrictions of the
quartic equation are

\[
F_C|_{\mathscr L_j}=c_jR_j.
\]

At each complement edge \(v_{jk}\),

\[
\boxed{c_jR_j(v_{jk})=c_kR_k(v_{jk}).}
\tag{3.5}
\]

For a tree, (3.5) determines the \(c_j\)'s up to scale. For a
disconnected complement, each cycle supplies an exact product-ratio
gate. Every compatible scalar solution glues to a unique quartic,
because

\[
0\to\mathcal O_{\mathbf P^2}(-2)
\to\mathcal O_{\mathbf P^2}(4)
\to\mathcal O_{\cup_j\mathscr L_j}(4)\to0
\]

has zero \(H^0\) and \(H^1\) on the kernel.

### Required conclusion

For every exact pole-graph orbit representative satisfying (3.5),
prove one
of:

1. the interpolated quartic is reducible;
2. its geometric genus is positive;
3. its normalization cannot realize (2.1);
4. the selected source rows emit one of the existing endpoint
   minors;
5. the four free edges form a union of complete pole-graph cycles.

This is an exact finite graph-type elimination, but the labels remain
symbolic. A numerical check of one normalization is insufficient.

### 3.2 Repeated-vertex branch

If \(\psi^*\mathcal K\) is reduced but several normalization points
map to the same star vertex, write \(n_v\) for the fiber size. Since
a rational plane quartic has total \(\delta\)-invariant three,

\[
\boxed{\sum_v(n_v-1)\le3.}
\tag{3.5}
\]

Thus only one, two, or three duplicate-preimage units need be added
to the simple branch. Classify their local branch types and repeat
the restriction gluing with the corresponding singularity
conditions.

### 3.3 Ramified common-pole branch

If \(\psi^*\mathcal K\) is nonreduced, one normalization point can
carry pullback multiplicity without a second branch. The proof must
use the local intersection orders

\[
\operatorname{ord}_\lambda H(\alpha_j,\lambda)
\]

at the ramified deck-fixed point. It must not replace the degree-ten
divisor by ten distinct points.

The useful target is a finite list of local multiplicity partitions
compatible with:

\[
\sum_j\operatorname{div}H(\alpha_j,\lambda)
=2\psi^*\mathcal K+E_H
\]

and the quartic singularity budget.

## 4. Parallel conic second-involution target

The line branch needs no adapter because it is excluded directly.
For the conic branch, equality
\(\chi\sim\psi\) is also impossible: their involutions pair the free
roots differently.

In the reduced branch, the two actual free-root pairs determine the
unique candidate involution. First test its nondegeneracy and common
binary-decic invariance on the endpoint-row representatives in
(2.4). Only if a candidate survives does one recover its five common
orbits and test the source-signature graph representatives in (2.3).
Prove that no open representative passes these gates, unless the same
equations emit an existing endpoint minor or a valid same-record
cell.

No ramified common-pole case remains. The zero-branch-point target
must eliminate or pay the reciprocal branch and the four exact
dihedral orders.

## 5. Guarded finite evidence

The packet includes:

```text
experiments/q6_u2_normalized_model_search_report.md
```

In its printed unramified normalization, the exhaustive rank-three
and weighted-GRS search found no fixture. The result supports the
target but does not handle arbitrary actual labels or ramification.

## 6. Completion boundary

Closing all three image types proves the \(u=2\) part of the
component cycle-union lemma. The global \(Q=6,s=6\) endpoint would
still require:

1. the analogous \(u=3\) component theorem; or
2. a direct argument that every nontrivial component partition
   necessarily exposes a paid \(u=2\) branch.

The immediate recommended order is:

1. conic candidate-involution/common-decic elimination on the at
   most three open endpoint-row representatives per pole graph;
2. eliminate or pay the reciprocal normalizer and cyclic orders
   \(4,5\), then apply the source-signature pair matrix only to
   surviving candidates;
3. simple-vertex quartic elimination on the pole-graph orbit
   representatives, starting with the \(79\)-orbit \(2+2+2\) branch;
4. repeated/ramified quartic local types;
5. \(u=3\).
