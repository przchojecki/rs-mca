# The \(u=2\) Conic Free-Pair Involution Reduction

## 1. Status

This note sharpens:

```text
proof/q6_u2_line_conic_quotient_reduction.md
```

It proves that the two source rows carrying the four free roots
already determine the only possible conic involution. The five
common-pole pairs do not have to be guessed or included in the seed.
It also excludes the last ramified common-pole case, classifies every
reduced survivor by a short dihedral-order list, and emits a canonical
source-label quotient.

The remaining conic target is one exact binary-decic invariance and
source-signature test for each endpoint-row pair, followed by either
direct elimination or the adapter stated in
`target/q6_u2_conic_source_quotient_adapter_target.md`. No active
owner payment is booked.

The subsequent exact star-conic calculation in
`proof/q6_u2_star_conic_geometry_reduction.md` eliminates the complete
\(P_3\sqcup C_3\) signature type. Thus only \(P_6\) and
\(P_2\sqcup C_4\) enter that remaining test.

## 2. The two free divisors

In a conic-image component, exactly two noninvariant source rows
\(j\ne k\) carry free roots. Their complete free divisors are

\[
F_j=bZ_j,\qquad F_k=bZ_k.
\tag{2.1}
\]

They are disjoint, reduced degree-two divisors. Choose a homogeneous
pole coordinate and write

\[
\begin{aligned}
f_j(X,Y)&=A_jX^2+B_jXY+C_jY^2,\\
f_k(X,Y)&=A_kX^2+B_kXY+C_kY^2.
\end{aligned}
\tag{2.2}
\]

The conic deck involution \(\iota\) must exchange the two roots of
each form.

## 3. Two unordered pairs determine the involution

Represent a projective involution in odd characteristic by a
trace-zero matrix

\[
M=
\begin{pmatrix}
a&b\\
c&-a
\end{pmatrix},
\qquad
a^2+bc\ne0.
\tag{3.1}
\]

In an affine chart, \(M\) exchanges distinct finite points \(x,y\)
exactly when

\[
cxy-a(x+y)-b=0.
\tag{3.2}
\]

If

\[
f(X,Y)=A(X-xY)(X-yY)
=AX^2+BXY+CY^2,
\]

then \(B=-A(x+y)\) and \(C=Axy\). Therefore (3.2) is the homogeneous
linear equation

\[
\boxed{Cc+Ba-Ab=0.}
\tag{3.3}
\]

Define the pair row

\[
\ell(f)=(C,B,-A).
\tag{3.4}
\]

The two free divisors give the \(2\times3\) matrix

\[
L_{jk}=
\begin{pmatrix}
C_j&B_j&-A_j\\
C_k&B_k&-A_k
\end{pmatrix}.
\tag{3.5}
\]

The two rows are independent. Proportional rows would make
\(f_j\) and \(f_k\) proportional and hence give the same free
divisor, contrary to pole disjointness. Thus

\[
\operatorname{rank}L_{jk}=2.
\tag{3.6}
\]

Its kernel is one-dimensional. A canonical candidate is the cross
product

\[
\boxed{
(c_{jk},a_{jk},b_{jk})
=\ell(f_j)\times\ell(f_k).}
\tag{3.7}
\]

If

\[
a_{jk}^2+b_{jk}c_{jk}=0,
\tag{3.8}
\]

the candidate matrix is singular and the conic branch is impossible
for this endpoint pair. Otherwise (3.7) is the unique projective
involution exchanging both free pairs. Because its square is
\((a_{jk}^2+b_{jk}c_{jk})I\), the exchange equation in one direction
also gives the reverse exchange.

This improves the earlier seven-pair description: the two free pairs
already determine \(M\); the common points are tests on that fixed
matrix.

## 4. The common decic gate

Let

\[
\psi=[\psi_n:\psi_d]
\]

be the deployed deck quotient and let \(\mathcal K\) be the five
common source labels. The complete common-pole divisor is cut out by
the binary decic

\[
\boxed{
C_{\mathcal K}(X,Y)
=
\prod_{\kappa\in\mathcal K}
\bigl(\psi_n(X,Y)-\alpha_\kappa\psi_d(X,Y)\bigr).}
\tag{4.1}
\]

This formula retains ramification multiplicity. A candidate
involution \(M_{jk}\) preserves the common divisor if and only if

\[
\boxed{
C_{\mathcal K}\bigl(M_{jk}(X,Y)\bigr)
\ \sim\
C_{\mathcal K}(X,Y),}
\tag{4.2}
\]

where \(\sim\) means equality up to a nonzero scalar. Equivalently,
the two length-eleven coefficient vectors have rank one. This gives
ten independent homogeneous coefficient-ratio gates, or any
complete set of \(2\times2\) minors.

If (4.2) fails, no conic component can have endpoint rows \(j,k\).
If it holds and the common divisor is reduced, the restriction of
\(M_{jk}\) partitions its ten roots into the five required common
pairs, provided no common root is fixed. The fixed-root condition is

\[
\gcd\!\left(
C_{\mathcal K},
c_{jk}X^2-2a_{jk}XY-b_{jk}Y^2
\right)=1.
\tag{4.3}
\]

When exactly one deck branch point lies over \(\mathcal K\), the
same identity (4.2) remains valid with multiplicity. The unique
double common root must be fixed by \(M_{jk}\), agreeing with the
local ramification theorem. Thus the binary-decic identity also
detects this case, although Section 5 excludes it uniformly before
any endpoint-row gate must be evaluated.

## 5. The one-branch-point case is impossible

The common divisor is invariant under both the deployed deck
involution \(b\) and the conic involution \(\iota\).

Suppose exactly one deck branch point \(\beta\) lies over
\(\mathcal K\). The local theorem in
`proof/q6_u2_line_conic_quotient_reduction.md` proves that \(\beta\)
is also a branch point of the conic quotient. Thus \(b\) and
\(\iota\) share the fixed point \(\beta\).

They are distinct. If they shared their second fixed point as well,
they would be equal, contradicting the free-root pairing. Conjugate
\(\beta\) to infinity. In odd characteristic the two involutions
then have affine forms

\[
b(x)=-x+r,\qquad
\iota(x)=-x+s,
\qquad r\ne s.
\tag{5.1}
\]

Their product is the nontrivial translation

\[
b\iota(x)=x+(r-s).
\tag{5.2}
\]

Over the KoalaBear field it has order

\[
p=2{,}130{,}706{,}433.
\]

The common divisor has one double branch point and eight other
simple points, so its support has nine points. It is invariant under
\(b\iota\). But every nonfixed orbit of a nontrivial translation has
length \(p>9\), while infinity is its only fixed point. The eight
finite common points cannot form an invariant set.

Therefore

\[
\boxed{
\text{The conic branch is empty when exactly one deck branch point
lies over }\mathcal K.}
\tag{5.3}
\]

Together with the earlier two-branch-point exclusion, every ramified
common-pole conic case is now closed.

## 6. The reduced branch has two noncommuting orders

It remains to consider the reduced common divisor, so neither
\(b\) nor \(\iota\) has a fixed point in its ten-point support.
Put

\[
g=b\iota.
\]

If \(b\) and \(\iota\) commute, then after normalizing
\(b(x)=-x\), the distinct involution has the form

\[
\boxed{\iota(x)=\mu/x.}
\tag{6.1}
\]

It descends through \(w=x^2\) to the reciprocal source involution

\[
w\longmapsto\mu^2/w.
\tag{6.2}
\]

Thus the common five-set is invariant under (6.2), and each free
pair has root product \(\mu\). Because the common five-set has odd
cardinality, it contains a fixed value of (6.2). The two fixed
values are \(\mu\) and \(-\mu\). The fiber \(w=\mu\) consists of the
two fixed points of \(\iota\), which are absent from the reduced
common divisor. Therefore the common labels have the exact form

\[
\boxed{
\mathcal K=
\{-\mu,\ r,\ \mu^2/r,\ s,\ \mu^2/s\}.}
\tag{6.3}
\]

This gives a source-line gate before the pole decic is expanded. Let

\[
A_{\mathcal K}(X,Y)
=\prod_{\kappa\in\mathcal K}(X-\alpha_\kappa Y)
\]

and form the two binary quadratics whose roots are the two endpoint
right-neighbor pairs. Applying the pair-row construction
(3.3)--(3.7) to those source quadratics gives the unique candidate
source involution \(J\). The reciprocal branch requires:

\[
\boxed{
\det J\ne0,\qquad
A_{\mathcal K}(J(X,Y))\sim A_{\mathcal K}(X,Y),\qquad
\deg\gcd(A_{\mathcal K},\operatorname{Fix}(J))=1.}
\]

The proportionality test has only five coefficient-ratio minors. The
last condition says that exactly one of the two fixed source values is
in \(\mathcal K\), as in (6.3). Failure of this source-quintic gate
excludes the reciprocal branch without reconstructing the ten pole
roots. The machine-readable gate packet includes an exact finite-field
regression and semantic tamper.

There is also an exact pole-graph restriction. The two quotient
labels incident to each endpoint row are exchanged by (6.2). If
the endpoint rows shared exactly one right neighbor \(\ell\), then
the same involution would send \(\alpha_\ell\) to two different
other neighbors. Hence the other neighbors must coincide too. The
two rows then have the same two neighbors and form a complete
four-edge pole cycle, which is already paid.

Consequently every open reciprocal branch has disjoint right
neighborhoods. Applied to the endpoint orbits in Section 7, this
leaves:

\[
\boxed{
\begin{array}{c|r}
\text{pole cycles}&\text{open reciprocal endpoint orbits}\\ \hline
6&2\\
4+2&2\\
3+3&1\\
2+2+2&1
\end{array}}
\tag{6.4}
\]

This is the exact commuting reciprocal-quotient branch.

Now suppose they do not commute. Then
\(\langle b,\iota\rangle\) is a tame dihedral group and \(g\) has
order \(n\ge3\). It preserves the ten common points. Since a
nonidentity projective transformation fixes at most two points, some
common point has a full \(g\)-orbit. Hence

\[
n\le10.
\tag{6.5}
\]

Let \(f\) be the number of the two fixed points of \(g\) lying in
the common divisor. Every other \(g\)-orbit has length \(n\), so

\[
n\mid 10-f.
\tag{6.6}
\]

The relation \(bgb=g^{-1}\) makes \(b\) preserve the two-point fixed
set of \(g\). If it fixes one of those points individually, that
point is deck fixed and is not in the reduced common divisor. If it
swaps them, divisor invariance includes either both or neither.
Therefore

\[
f\in\{0,2\}.
\tag{6.7}
\]

For \(f=0\), equations (6.5)--(6.7) initially give \(n=5\) or \(10\).
For \(f=2\), they initially give \(n=4\) or \(8\).

The reduced hypothesis removes the even-orbit alternatives. Consider
one full \(g\)-orbit \(\mathcal O\) outside the fixed points of \(g\).
If \(b\) preserves \(\mathcal O\), identify it with
\(\mathbf Z/n\mathbf Z\) so that

\[
g(x)=x+1,\qquad b(x)=c-x.
\tag{6.8}
\]

Since \(\iota=bg\),

\[
\iota(x)=c-1-x.
\tag{6.9}
\]

If \(n\) is odd, each of

\[
2x=c,\qquad 2x=c-1
\]

has one solution, so both involutions have a fixed point in
\(\mathcal O\). If \(n\) is even, exactly one of \(c,c-1\) is even;
the corresponding equation has two solutions and the other has none.
Thus at least one of \(b,\iota\) has a fixed point in
\(\mathcal O\) in every case.

This contradicts reducedness. Hence no nonfixed \(g\)-orbit in the
common divisor is \(b\)-stable. Such orbits must occur in pairs
interchanged by \(b\). Therefore

\[
\boxed{\frac{10-f}{n}\ \text{is even}.}
\tag{6.10}
\]

For \(f=0\), this excludes \(n=10\) and retains \(n=5\). For \(f=2\),
it excludes \(n=8\) and retains \(n=4\). Consequently

\[
\boxed{n\in\{4,5\}.}
\tag{6.11}
\]

The reduced conic branch is therefore either:

1. the reciprocal normalizer branch (6.1)--(6.2); or
2. a tame cyclic pole quotient of exact order \(4\) or \(5\).

### 6.1 Source-quotient emission

Let \(\mathcal D=\langle b,\iota\rangle\). Its full quotient

\[
q:\mathbf P^1_\lambda\longrightarrow
\mathbf P^1_\lambda/\mathcal D
\]

is \(b\)-invariant. It therefore factors through the deployed deck
quotient:

\[
\boxed{q=\Theta\circ\psi.}
\tag{6.12}
\]

In the reciprocal commuting branch \(\deg\Theta=2\). In the
noncommuting branch \(|\mathcal D|=2n\), so

\[
\deg\Theta=n\in\{4,5\}.
\tag{6.13}
\]

The common divisor is \(\mathcal D\)-invariant. Its orbit
decompositions from (6.5)--(6.11) give:

\[
\begin{array}{c|c}
\deg\Theta&\#q(\operatorname{supp}D_{\mathcal K})\\ \hline
2&\le3\\
4&\le2\\
5&1
\end{array}
\tag{6.14}
\]

The two noncommuting rows have sharper exact fiber profiles.

For \(n=4\), the two \(g\)-fixed common poles are interchanged by
\(b\). They give one source label \(\kappa_0\in\mathcal K\) at which
\(\Theta\) is totally ramified of index four. The other eight common
poles are two \(g\)-orbits interchanged by \(b\); after the deck
quotient they give four distinct unramified source labels in one
complete fiber of \(\Theta\). Hence

\[
\boxed{
\mathcal K=\{\kappa_0\}\sqcup
\Theta^{-1}(v)\quad\text{on source labels},\qquad
e_{\kappa_0}(\Theta)=4.}
\tag{6.15}
\]

For \(n=5\), the ten common poles are two \(g\)-orbits interchanged
by \(b\), hence one free \(\mathcal D\)-orbit. Their five source
labels form one complete unramified fiber:

\[
\boxed{\mathcal K=\Theta^{-1}(v)\quad\text{with five distinct points}.}
\tag{6.16}
\]

The map \(\Theta\) is not an arbitrary map of degree four or five.
This is the same dihedral normal-form mechanism proved for the
all-component deck in Theorem 9.9 of
`proof/pole_disjoint_conic_facet_collinearity_reduction.md`, applied
here to the second involution of one \(u=2\) conic component.
Over the algebraic closure, normalize

\[
g(x)=\zeta x,\qquad b(x)=a/x,
\]

where \(\zeta\) has order \(n\) and \(a\ne0\). A deck quotient and the
full dihedral quotient are

\[
w=x+a/x,\qquad q=x^n+(a/x)^n.
\]

Hence

\[
\boxed{\Theta(w)=D_n(w,a),}
\]

up to projective changes of source and target, where

\[
\begin{aligned}
D_4(w,a)&=w^4-4aw^2+2a^2,\\
D_5(w,a)&=w^5-5aw^3+5a^2w.
\end{aligned}
\]

Thus the remaining noncommuting gate has one Dickson parameter and
two projective normalizations, rather than the coefficients of a
general degree-four or degree-five rational map. The focused verifier
checks both defining Laurent identities exactly over a finite-field
regression; the displayed derivation is the proof.

Since \(D_{\mathcal K}=\psi^*\mathcal K\), this is the exact
source-image statement

\[
\boxed{|\Theta(\mathcal K)|\le3.}
\tag{6.17}
\]

Moreover, let \(\ell,m\) be the two right-neighbor labels of one
endpoint row. Its two free points are exchanged by \(\iota\), so
they have the same full quotient value. Hence

\[
\boxed{\Theta(\alpha_\ell)=\Theta(\alpha_m).}
\tag{6.18}
\]

This holds for both endpoint rows. Thus every surviving reduced
conic emits a canonical degree-\(2,4,\) or \(5\) source-label
quotient map which:

1. maps the five common labels to at most three values; and
2. collapses each of the two actual endpoint-row neighbor pairs.

The map is derived from the same component and the same selected
endpoint rows. It is therefore a component-rooted source-quotient
precursor.

It is not yet the deployed pair-global source-rational owner. That
owner requires a unique domain-to-slope map agreeing with every
fixed translated source anchor and, for the same selected finite
slope, an outside-source moving root in its image. Here \(\Theta\)
acts on source-label values after the deck quotient and is constrained
on at most nine labels. Neither full source-anchor agreement nor
same-slope outside-source image membership follows from
(6.12)--(6.18). The exact missing adapter is stated separately in
`target/q6_u2_conic_source_quotient_adapter_target.md`.

## 7. Endpoint-row orbit quotient

There are only

\[
\binom62=15
\]

unordered choices of the two endpoint rows. The four free pole edges
are then forced: they are the two complete edge stars at those rows.
Quotienting by the bipartition-preserving automorphism group of the
actual pole graph gives:

\[
\boxed{
\begin{array}{c|r|r|r}
\text{pole cycles}&\text{all endpoint orbits}&
\text{cycle-union orbits}&\text{open endpoint orbits}\\ \hline
6&3&0&3\\
4+2&4&1&3\\
3+3&2&0&2\\
2+2+2&2&1&1
\end{array}}
\tag{7.1}
\]

The exact representatives and orbit sizes are emitted by:

```text
experiments/classify_q6_u2_conic_graph_orbits.py
experiments/q6_u2_conic_graph_orbits.json
experiments/generate_q6_u2_conic_decic_gates.py
experiments/q6_u2_conic_decic_gate_templates.json
```

The already-paid endpoint orbit is the pair of rows forming an
entire four-edge pole cycle. After removing it, the preliminary
conic eliminant has at most three endpoint-row representatives for
any pole graph, not 52 common-signature graph representatives.

The 52-case graph quotient remains relevant only after a candidate
passes (3.8), (4.2), and the fixed-point gate: it then checks whether
the induced five common orbits carry a permitted source-signature
graph.

## 8. Exact remaining conic target

For each open endpoint-row representative:

1. construct the two actual free quadratics \(bZ_j,bZ_k\);
2. form \(M_{jk}\) by (3.7);
3. reject a singular candidate using (3.8);
4. test the binary-decic identity (4.2);
5. apply the reduced fixed-root condition (4.3);
6. only for surviving candidates, recover the five common orbits and
   test their source-row signatures.

A complete proof may factor one failed coefficient minor in (4.2)
through an existing endpoint minor, or prove directly that the
coefficient vectors cannot be proportional.

## 9. Guardrails

This reduction does not assume that an arbitrary pole-graph
automorphism fixes the deployed numeric source labels. It uses the
automorphism quotient only as a uniform symbolic relabelling of the
full source-labelled equations.

The free-pair orbit census alone is not a conic contradiction.
Likewise, a numerical failure of (4.2) for one convenient source
normalization is evidence only. The deployed source-facet formulas,
ramification multiplicities, and same-record endpoint rows remain
load-bearing.
