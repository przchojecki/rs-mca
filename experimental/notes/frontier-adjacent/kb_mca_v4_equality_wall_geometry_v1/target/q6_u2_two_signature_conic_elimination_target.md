# Two-Signature Elimination for the Reduced \(Q=6,u=2\) Conic

## 1. Status and role

This is the next finite algebraic target inside the
\(Q=6,s=6,u=2\) conic-image branch.

The following branches are already closed:

* line image;
* one or two deck branch points over the common divisor;
* conic common-signature type \(P_3\sqcup C_3\);
* reduced dihedral orders \(8\) and \(10\).

Every surviving reduced conic has:

\[
\boxed{
\text{signature graph }P_6\text{ or }P_2\sqcup C_4,
\qquad
\text{quotient profile reciprocal, }D_4,\text{ or }D_5.}
\tag{1.1}
\]

No active owner payment is booked. The goal is either to eliminate
both remaining signature geometries or to convert one of their exact
component-rooted quotient records into an existing same-record owner.

## 2. Proved source-plane geometry

Let the six noninvariant source labels be
\(\alpha_0,\ldots,\alpha_5\). Their tangent-star lines in the
coefficient plane are

\[
\mathscr L_i:
A\alpha_i^2+B\alpha_i+C=0,
\]

with vertices

\[
v_{ij}
=
[1,-(\alpha_i+\alpha_j),\alpha_i\alpha_j].
\tag{2.1}
\]

Use the universal normalization

\[
(\alpha_0,\ldots,\alpha_5)=(0,1,-1,x,y,z).
\tag{2.2}
\]

The common vertices determine one unique candidate conic. Put

\[
\mathfrak f=xyz+xy+xz-x-2yz,
\tag{2.3}
\]

\[
\mathfrak g=xyz-2xy+xz+yz-z,
\tag{2.4}
\]

\[
\mathfrak h=xy+xz-2yz+y-z.
\tag{2.5}
\]

For \(P_6\), nonsingularity and exact signature support require

\[
\boxed{\mathfrak f\ne0,\qquad\mathfrak h\ne0.}
\tag{2.6}
\]

For \(P_2\sqcup C_4\), they require

\[
\boxed{\mathfrak f\ne0,\qquad\mathfrak g\ne0.}
\tag{2.7}
\]

All omitted factors in the conic discriminants and unselected-vertex
evaluations are source-label collision factors and are already
nonzero.

## 3. Exact endpoint image points

Parameterize \(\mathscr L_a\) by

\[
\ell_a(t)=[1,-(a+t),at].
\tag{3.1}
\]

For \(P_6\), take common edges

\[
01,12,23,34,45.
\]

The endpoint rows are \(0,5\), and their free image points are

\[
\ell_0(\beta_0),\qquad
\beta_0=
-\frac{xyz+xy+2xz-yz+y}
{xz-x-2yz-z-1},
\tag{3.2}
\]

\[
\ell_z(\beta_5),\qquad
\beta_5=
\frac{x(xy+xz-2yz+y-z)}
{x^2y-x^2z+xy+xz-2yz}.
\tag{3.3}
\]

For \(P_2\sqcup C_4\), take common edges

\[
01,23,34,45,25.
\]

The endpoint rows are \(0,1\), and their free image points are

\[
\ell_0(\beta_0),\qquad
\beta_0=
\frac{xyz+xy-2xz+yz-y}
{xz-x+2y-z-1},
\tag{3.4}
\]

\[
\ell_1(\beta_1),\qquad
\beta_1=
\frac{xyz+xy-xz+yz}
{xz+y}.
\tag{3.5}
\]

Equations (3.2)--(3.5) are homogeneous/projective; a vanishing
denominator means that the second root is infinity.

## 4. Proved pole-side quotient data

For the two endpoint rows \(j,k\), their actual complete free
divisors are

\[
F_j=bZ_j,\qquad F_k=bZ_k.
\]

They are disjoint reduced binary quadratics. Their coefficient rows

\[
(C_j,B_j,-A_j),\qquad(C_k,B_k,-A_k)
\]

have rank two and determine a unique projective involution
\(\iota\). A conic component can exist only if:

1. the common binary decic \(C_{\mathcal K}\) is invariant under
   \(\iota\);
2. no common root is fixed by \(\iota\);
3. the induced five common pairs have exactly the selected
   \(P_6\) or \(P_2\sqcup C_4\) source signatures;
4. the deck/conic involution pair is reciprocal or generates a tame
   cyclic quotient of order \(4\) or \(5\).

In the noncommuting cases, after normalization

\[
g(u)=\zeta u,\qquad b(u)=a/u,
\]

the source-label quotient has Dickson form

\[
D_4(w,a)=w^4-4aw^2+2a^2,
\tag{4.1}
\]

or

\[
D_5(w,a)=w^5-5aw^3+5a^2w,
\tag{4.2}
\]

where \(w=u+a/u\).

The order-four common set consists of one totally ramified label and
one complete regular four-fiber. The order-five common set is one
complete regular five-fiber.

In the reciprocal case, the endpoint neighbor pairs determine a
source involution \(J\). The common source quintic must satisfy

\[
A_{\mathcal K}\circ J\sim A_{\mathcal K},
\tag{4.3}
\]

and exactly one common label is fixed. This is an exact five-minor
gate.

## 5. Exact target theorem

> **Two-signature conic elimination-or-owner theorem.**
> For every actual source-labelled \(Q=6,s=6,u=2\) conic component
> satisfying Sections 2--4, one of the following holds:
>
> 1. a printed discriminant, extra-vertex, common-decic,
>    fixed-root, source-signature, reciprocal, \(D_4\), or \(D_5\)
>    equation fails, so the component is impossible; or
> 2. the same equations construct a validated earlier cell
>    containing one of the two attached endpoint owners.

The owner conclusion must use the exact selected record. The
component-rooted source-label quotient is not itself the active
source-rational owner: the latter is a domain-to-slope map agreeing
with all fixed translated source anchors and must return the same
selected slope on an outside-source moving root.

## 6. Finite census

After cycle-union routing and exclusion of all \(60\) labeled
\(P_3\sqcup C_3\) graphs in the reduced common-signature universe,
the exact pole-graph orbit census is:

\[
\begin{array}{c|r|r}
\text{pole cycles}&\text{open labeled cases}&\text{open orbits}\\ \hline
6&405&46\\
4+2&378&30\\
3+3&405&10\\
2+2+2&324&10.
\end{array}
\tag{6.1}
\]

The first numeric column is a labeled-case count after a pole-cycle
type has been fixed. The second is an orbit count under that pole
graph's incidence-preserving automorphism group. In particular,
\(46,30,10,10\) are four separate orbit censuses; they are not a
partition of the \(405\) total labeled survivors.

The free-pair quotient should be applied before this list. It leaves
only \(3,3,2,1\) endpoint-row orbits for the four pole-cycle types,
and the reciprocal right-neighbor gate leaves \(2,2,1,1\).

Thus a practical eliminator need not expand all cases in (6.1).
It should:

1. select one canonical endpoint-row orbit;
2. construct its two actual free quadratics;
3. recover \(\iota\);
4. apply common-decic invariance and the fixed-root test;
5. reconstruct the surviving source-signature graph;
6. substitute the exact star-conic equations (2.6)--(3.5);
7. test reciprocal, \(D_4\), and \(D_5\) compatibility.

## 7. Promising proof routes

### 7.1 Direct eliminant

Use the two endpoint free quadratics to eliminate the three
coefficients of \(\iota\). Reduce the five decic proportionality
minors modulo:

* the selected pole-graph equations;
* \(\mathfrak f\), \(\mathfrak g\), or \(\mathfrak h\) nonvanishing;
* the endpoint formulas (3.2)--(3.5);
* the appropriate reciprocal/Dickson fiber equations.

A successful factorization should leave only collision factors,
already-paid four-cycles, or one existing owner determinant.

### 7.2 Symmetric biquadratic classification

Substitute (2.1) into the candidate conic equation. This gives a
symmetric bidegree-\((2,2)\) correspondence

\[
R(a,b)=0.
\]

Classify its automorphism group under the five prescribed edges.
For \(P_6\), the path should force an iterated correspondence from
\(\alpha_0\) to \(\alpha_5\); for \(P_2\sqcup C_4\), the four-cycle
gives a periodicity constraint. Compare that periodicity directly
with the reciprocal, \(D_4\), and \(D_5\) normal forms.

### 7.3 Existing-owner adapter

Use this only after an exact component survives. The proof must
recover the deployed domain-to-slope map

\[
\Psi([h:1])=[-\epsilon_0(h):\epsilon_1(h)]
\]

from the full selected endpoint record, verify every source anchor,
and exhibit the outside-source moving root for the same slope.

## 8. Route cuts

The following are insufficient:

* the abstract existence of a degree-\(2,4,\) or \(5\) label quotient;
* the 405-case graph census by itself;
* a convenient finite-field normalization not derived from the
  deployed source labels;
* a cyclic annihilator or per-record interpolation rank drop;
* an owner certificate attached to another record with the same
  syndrome.

## 9. Valid completion or falsifier

A completion must either eliminate every endpoint orbit or print a
same-record paid cell with all canonical parameters and projection
bounds.

A falsifier must instantiate an actual deployed source-facet
component, including the pole graph, deck, source labels, endpoint
free quadratics, common decic, selected owners, and all prior
semantic deletions. An abstract six-line configuration is only a
guardrail.

## 10. Supporting artifacts

```text
proof/q6_u2_star_conic_geometry_reduction.md
proof/q6_u2_conic_free_pair_involution_reduction.md
proof/q6_u2_line_conic_quotient_reduction.md
target/q6_u2_conic_source_quotient_adapter_target.md
verification/verify_q6_u2_star_conic_geometry.py
verification/q6_u2_star_conic_geometry_certificate.json
experiments/classify_q6_u2_conic_graph_orbits.py
experiments/q6_u2_conic_graph_orbits.json
experiments/generate_q6_u2_conic_decic_gates.py
experiments/q6_u2_conic_decic_gate_templates.json
```
