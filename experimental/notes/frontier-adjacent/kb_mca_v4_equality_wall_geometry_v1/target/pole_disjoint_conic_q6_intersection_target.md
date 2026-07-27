# Pole-Disjoint Conic \(Q=6\) Intersection Target

## 1. Status

This is the first unresolved deck-pair value in the pole-disjoint
irreducible-conic endpoint.

```text
Q=1: EXCLUDED
Q=2,3,4: EXCLUDED
Q=5: EXCLUDED
Q=6: OPEN
PDCEC: OPEN
OWNER PAYMENT: NONE
```

The exact input is proved in:

```text
proof/pole_disjoint_conic_facet_collinearity_reduction.md
```

In particular, use Theorems 9.13, 9.19, and 9.23 and Corollaries
9.18--9.22. They give the outgoing/deck-conjugate intersection
ledger, the fixed-pole odd/even proportionality, the
invariant-coordinate source factors, the quotient-resultant
compression, and the quotient-pole capacity exclusion. The resolved
\(Q=5\) note remains useful as a model for how equality or small
slack can force a low-degree resultant.

## 2. Exact \(Q=6\) packet

Let \(X_{\rm out}\) be the union of the components assigned to the
outgoing side of one deck pair. Then

\[
\operatorname{bideg}X_{\rm out}=(6,12).
\]

Its deck conjugate \(bX_{\rm out}\) is coprime to it, and therefore

\[
X_{\rm out}\cdot bX_{\rm out}=4\cdot6^2=144.
\tag{2.1}
\]

For source label \(j\), let:

* \(O_j\) be the outgoing six-point divisor;
* \(Z_j\) be the degree-two coordinate divisor;
* \(E_j=Z_j+O_j\), which is \(b\)-invariant;
* \(\mathcal I=\{j:bZ_j=Z_j\}\);
* \(s=|\mathcal I|\).

Theorem 9.19 proves the exact dichotomy

\[
\deg\gcd(Z_j,bZ_j)
=2\mathbf1_{j\in\mathcal I}.
\tag{2.2}
\]

The exact fiber identity is

\[
\deg\gcd(O_j,bO_j)
=10+2\mathbf1_{j\in\mathcal I}.
\tag{2.3}
\]

Let \(r\in\{0,1,2\}\) be the number of deck fixed points occurring in
the coordinate divisors. A fixed coordinate pole is necessarily
double, so

\[
s\ge r.
\tag{2.4}
\]

At each fixed coordinate pole, Corollary 9.18 forces one additional
local intersection at each of its six source-section roots beyond
the fiber-gcd contribution. After adding these excesses and the
non-pole fixed horizontal fibers, Theorem 9.19 gives

\[
X_{\rm out}\cdot bX_{\rm out}
\ge
132+2s.
\tag{2.5}
\]

Hence the residual intersection degree away from these compulsory
points is

\[
\Delta
=144-(132+2s)
=12-2s.
\tag{2.6}
\]

\[
\boxed{0\le s\le6,\qquad\Delta\le12-2s.}
\tag{2.7}
\]

This supersedes the weaker \(r\)-dependent caps \(12,16,20\).
Every deck-invariant coordinate quadratic now decreases the residual
budget by two.

## 3. Involution normal form

Choose coordinates in which

\[
b[x:y]=[x:-y],
\qquad
w=[x^2:y^2].
\]

The outgoing equation has the unique decomposition

\[
F_{\rm out}(T,x,y)
=
E_6(T,w)+xy\,H_6(T,w),
\tag{3.1}
\]

with

\[
\operatorname{bideg}E_6=(6,6),
\qquad
\operatorname{bideg}H_6=(6,5).
\tag{3.2}
\]

If a fixed point \(\beta\) belongs to coordinate divisor \(Z_\ell\),
then \(Z_\ell=2\beta\). Corollary 9.18 gives a scalar
\(d_\beta\) such that

\[
H_6(T,w_\beta)=d_\beta E_6(T,w_\beta).
\tag{3.3}
\]

Moreover, \(E_6(T,w_\beta)\) is a squarefree degree-six source
divisor: its roots are exactly the six source labels assigned to the
outgoing side at \(\beta\).

Equation (3.3) is load-bearing. Any proposed \(r=1\) or \(r=2\)
configuration must preserve this exact fixed-fiber proportionality,
not merely the set-theoretic involution.

The invariant coordinate labels factor the odd form:

\[
\boxed{
H_6(T,w)
=P_{\mathcal I}(T)\overline H_6(T,w),
\qquad
\operatorname{bideg}\overline H_6=(6-s,5).
}
\tag{3.4}
\]

Moreover,

\[
\deg_T\operatorname{Res}_w(E_6,\overline H_6)
=66-6s,
\tag{3.5}
\]

and its source divisor contains

\[
5\sum_{j\notin\mathcal I}[\alpha_j].
\tag{3.6}
\]

More exactly, there is an effective divisor \(D_s\) such that

\[
\boxed{
\operatorname{div}\operatorname{Res}_w(E_6,\overline H_6)
=
5\sum_{j\notin\mathcal I}[\alpha_j]+D_s,
\qquad
\deg D_s=6-s.}
\tag{3.7}
\]

Thus its divisor away from the source points has degree at most

\[
\boxed{6-s.}
\tag{3.8}
\]

If \(\beta\) is a fixed coordinate pole, evaluating (3.3) at its own
label forces \(d_\beta=0\), and hence

\[
\boxed{\overline H_6(T,w_\beta)\equiv0.}
\tag{3.9}
\]

Each fixed coordinate pole therefore supplies a horizontal quotient
factor of \(\overline H_6\).

### 3.1 Exact \(s=6\) endpoint

If \(s=6\), put

\[
\mathcal R=\{1,\ldots,12\}\setminus\mathcal I.
\]

Corollary 9.21 proves

\[
H_6=P_{\mathcal I}(T)h(w),
\qquad
\deg h=5,
\tag{3.10}
\]

where \(h\) is squarefree and its root divisor consists of five of
the twelve reduced source poles:

\[
\operatorname{div}(h)
=
\sum_{k\in\mathcal K}[\alpha_k],
\qquad
|\mathcal K|=5.
\tag{3.10a}
\]

\[
\operatorname{div}\operatorname{Res}_w(E_6,h)
=
5\sum_{j\in\mathcal R}[\alpha_j],
\tag{3.11}
\]

and the exact rectangular-grid normal form

\[
E_6(T,w)
=
P_{\mathcal R}(T)A(w)
+
h(w)(a_1(T)w+a_0(T)),
\qquad
\gcd(A,h)=1.
\tag{3.12}
\]

There is no residual quotient point. A proof of the \(s=6\) case
may start from (3.10)--(3.12); it no longer needs to recover the
resultant support.

Corollary 9.24 also converts every deck-conjugate block pair into a
split-pencil secant through one fixed source locator. If

\[
G_\lambda=\gcd(U_\lambda,U_{b\lambda}),
\qquad
A_\lambda=U_\lambda/G_\lambda,
\qquad
B_\lambda=U_{b\lambda}/G_\lambda,
\]

then \(\deg G_\lambda=5\), the monic degree-six locators
\(A_\lambda,B_\lambda\) have disjoint active-root sets, and

\[
\boxed{
A_\lambda-c_\lambda B_\lambda
=(1-c_\lambda)P_{\mathcal I},
\qquad c_\lambda\ne0,1.}
\tag{3.12a}
\]

This holds for all sixty deck pairs. Thus the \(s=6\) endpoint is
simultaneously a rectangular intersection grid and a sixty-secant
star through the same six-source split form.

There is also a canonical source-label map. Every invariant
coordinate divisor is one complete source fiber:

\[
Z_j=\psi^*[\alpha_{\sigma(j)}],
\qquad
\sigma(j)\ne j
\qquad(j\in\mathcal I).
\tag{3.12b}
\]

The map \(\sigma\) is injective. With
\(\mathcal L=\sigma(\mathcal I)\), the five horizontal source poles
in \(\mathcal K\) satisfy

\[
\boxed{
\mathcal K\subseteq\mathcal I\cap\mathcal L,
\qquad
|\mathcal I\cap\mathcal L|\ge5.}
\tag{3.12c}
\]

Thus \(\mathcal L=\mathcal I\), with \(\sigma\) a derangement, or
the two six-sets differ by exactly one label. The six noninvariant
coordinate divisors form a diagonal-free two-regular bipartite pole
incidence between \(\mathcal I^c\) and \(\mathcal L^c\).

### 3.2 Quotient-pole capacity exclusion

Theorem 9.23 eliminates every intermediate invariant-coordinate
count:

\[
\boxed{s\notin\{2,3,4,5\}.}
\tag{3.13}
\]

For each \(j\notin\mathcal I\), the degree-five divisor
\(\overline H_6(\alpha_j,w)\) is supported on the twelve reduced
source poles. If no horizontal specialization
\(\overline H_6(T,\alpha_k)\) vanishes identically, the resulting
incidence count is

\[
5(12-s)\le12(6-s).
\tag{3.14}
\]

For \(2\le s\le5\), failure of (3.14) forces a horizontal factor
common to \(E_6\) and \(\overline H_6\), hence a forbidden common
component of the outgoing curve and its deck conjugate.

The same common-component argument shows that the unique invariant
coordinate divisor at \(s=1\) cannot be a fixed double pole. Thus the
only live alternatives are

\[
\boxed{s=0,\qquad s=1\text{ nonfixed},\qquad s=6.}
\tag{3.15}
\]

## 4. Component alternatives

The outgoing \(u\)-degrees sum to six.

### 4.1 Graph-containing branch

If a \(u=1\) component occurs, its deck conjugate supplies the second
quadratic graph. The dihedral factorization used in the \(Q=1\) proof
makes all coordinate poles generic, so

\[
r=0,\qquad s\in\{0,1\},\qquad\Delta\le12-2s.
\tag{4.1}
\]

The graph and its deck conjugate have one free, off-source common
quotient root, which must occur in the exact correction divisor
\(D_s\); Theorem 9.23 then excludes \(s=2,\ldots,5\).

Write the outgoing curve as a graph plus a \((5,10)\) residual
curve. If

\[
t_j=\deg\gcd(Q_j,bZ_j),
\qquad
T_0=\sum_jt_j,
\]

then Corollary 9.22 proves

\[
\boxed{4\le T_0\le9-s.}
\tag{4.2}
\]

The \(s=5\) equality calculation in Corollary 9.22 is retained as an
intermediate ledger but is now superseded by Theorem 9.23: such a
packet cannot exist.

The target in this branch is:

> For \(s=0\) or \(s=1\), use the two graph factors and the exact
> degree-\((6-s)\) correction divisor \(D_s\)
> to force either a third reciprocal row into their coordinate pencil
> or a rank-two selected triple.

The proof must preserve the actual endpoint labels and cannot replace
the selected blocks by another block with the same syndrome.

### 4.2 Graph-free branch

The only possible component partitions are

\[
\boxed{
6,\qquad4+2,\qquad3+3,\qquad2+2+2.
}
\tag{4.3}
\]

Every component has bidegree \((u,2u)\), and its deck conjugate has
the same bidegree. The target is to show that none of the four
partitions can realize the remaining cases \(s=0\), \(s=1\)
nonfixed, or the exact \(s=6\) grid, together with (2.2)--(2.7), the
factorization (3.4), and the residual resultant cap (3.8), without
forcing a rank-two selected triple.

## 5. Target lemma

### \(Q=6\) small-slack component theorem

Under the exact packet above, one of the following holds:

1. three selected endpoint blocks lie in one 12-set;
2. three selected endpoint blocks lie in a 13-set whose three
   complement quadratics are linearly dependent;
3. three selected reciprocal rows have rank at most two; or
4. the outgoing component packet violates its intersection budget or
   fixed-pole proportionality.

Any conclusion closes the \(Q=6\) branch. The first three contradict
the irreducible rank-three conic realization; the fourth contradicts
the exact endpoint identity.

An equivalent direct form is:

> No coprime pair \(X_{\rm out},bX_{\rm out}\) of bidegree
> \((6,12)\) can realize all twelve source divisors (2.3), the
> fixed-point data (2.4), the residual budget (2.7), the component
> partitions (4.3), and the selected reciprocal rank-three packet.

## 6. Promising proof routes

### 6.1 Residual-intersection classification

Separate the compulsory source and fixed-point intersections from the
residual divisor of degree \(\Delta\). Classify the remaining divisor
under \(b\). Non-fixed residual points occur in conjugate pairs, so
parity and orbit length further constrain (2.7). On the quotient,
only \(6-s\) residual points remain.

The strongest expected use is in the graph branch, where one residual
quotient point is already consumed by the two graph factors.

### 6.2 Componentwise intersection matrix

For outgoing components \(C_a\) of degrees \(u_a\), form

\[
m_{ab}=C_a\cdot bC_b.
\]

The row and column sums are fixed by the bidegrees, while source
fibers prescribe large diagonal or paired contributions. Analyze the
four partitions in (4.3) separately. A successful argument must use
local multiplicities or fixed-fiber data; aggregate Bézout counts
alone can admit spurious integer matrices.

### 6.3 Fixed-pole derivative propagation

Only the graph-free \(s=6\) branch can still have a fixed coordinate
pole. In that branch use

\[
\overline H_6(T,w_\beta)=0
\]

at one or both fixed fibers. The remaining task is to combine these
horizontal factors with the exact source-labelled factorization
(3.10a)--(3.12) and the component partition. Theorem 9.23 has already
eliminated every fixed-pole case with \(s<6\).

### 6.4 Resultant compression

Study

\[
\operatorname{Res}_w(E_6,\overline H_6)
\]

\(T\)-degree is \(66-6s\), and all but at most \(6-s\) of that degree
is already source-supported. Classify these at most six residual
points without replacing the signed/source-coupled packet by an
arbitrary resultant.

### 6.5 Low-subdegree monodromy

For a component of degree \(u=2\) or \(3\), use the induced
self-correspondence and quadratic lift. The partitions \(3+3\) and
\(2+2+2\) should be attacked through the compatibility of several
low-degree correspondences sharing the same twelve source fibers.

### 6.6 Fixed split-pencil star at \(s=6\)

Classify sixty pairs of disjoint active split sextics
\((A_\lambda,B_\lambda)\) satisfying (3.12a), together with their
five-root common block cores \(G_\lambda\). A useful closure would
show that three corresponding eleven-root block locators have a
common 12-set or a dependent complementary quadratic packet.

This route is source-coupled: \(P_{\mathcal I}\) is the actual
six-source locator, not a freely chosen split polynomial. A
classification of arbitrary secants through one point is
insufficient unless it also retains the active-root domain, the
sixty deck pairings, and the \(1\)-\((60,11,22)\) incidence ledger.

## 7. Existing inputs

A proof may consume all of the following established facts:

```text
exact 1-(60,11,22) locator design
reciprocal rank exactly three
facet and quadratic-pencil collinearity exclusions
component bidegree law (u,2u)
exact grid vertex derivative identity
uniform deck-pair intersection ledger
Q=1 dihedral coordinate-pencil exclusion
Q=2,3,4 Bezout exclusion
Q=5 fixed-pole derivative exclusion
fixed-pole odd/even proportionality for every Q>=2
invariant-coordinate source factors
Q=6 quotient-resultant residual degree at most 6-s
Q=6, s=6 rectangular-grid normal form
Q=6 graph-branch capacity 4 <= T0 <= 9-s
Q=6 invariant-coordinate counts s=2,3,4,5 excluded
Q=6 remaining counts s=0, s=1 nonfixed, s=6
Q=6 graph branch has s=0 or s=1 and no fixed coordinate pole
Q=6, s=6 gives sixty split-sextic secants through P_I
Q=6, s=6 source-label sets agree in at least five labels
Q=6, s=6 pencil has at most ten distinct active sextic fibers
Q=6, s=6 pole graph has the four graph-free component partitions
```

The verifier prints the exact \(Q=6\) totals and rejects a forged
slack cap.

## 8. Guardrails

The following do not prove the target:

1. an arbitrary \(1\)-\((60,11,22)\) design;
2. a component partition or integer intersection matrix without
   local source multiplicities;
3. a rank defect belonging to unselected records;
4. a source-free conic or correspondence classification;
5. treating the \(Q=5\) equality argument as if equality still held;
6. booking an owner payment without a same-record certificate.

The cyclic design-only guardrail has been strengthened accordingly.
It admits an explicit perfect matching of its 120 blocks such that
every matched pair intersects in five points, every active point
occurs in five matched common cores, and every active point occurs
in twelve matched one-sided differences. Thus even the exact paired
\(Q=6\) incidence ledger is not a combinatorial contradiction.
What that guardrail does not supply is the fixed-source split-pencil
identity (3.12a), the quotient grid, or the reciprocal rank-three
realization.

## 9. Valid closure

A valid proof must print either:

* a selected rank-two triple and its block labels;
* a contradiction to (2.1)--(2.6) in every component partition; or
* a source-derived owner certificate containing one of the same
  selected records.

Until then:

```text
Q=6: OPEN
PDCEC: OPEN
PAYMENT: NONE
```
