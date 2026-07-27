# The \(Q=6,s=6,u=2\) Conic Source-Quotient Adapter

## 1. Status

The reduced conic component is not yet excluded and is not paid by an
active owner. The proved input is:

```text
proof/q6_u2_conic_free_pair_involution_reduction.md
proof/q6_u2_line_conic_quotient_reduction.md
verification/verify_q6_u2_line_conic_quotient_reduction.py
experiments/generate_q6_u2_conic_decic_gates.py
```

Every ramified common-pole case is excluded. In the reduced case, the
two endpoint free divisors determine a unique candidate involution.
Every survivor is reciprocal or has cyclic order \(4\) or \(5\),
and emits the component-rooted factorization

\[
q=\Theta\circ\psi,
\qquad
\deg\Theta\in\{2,4,5\}.
\tag{1.1}
\]

The map satisfies

\[
|\Theta(\mathcal K)|\le3
\tag{1.2}
\]

for the five common source labels, and it identifies the two
right-neighbor labels attached to each of the two actual endpoint
rows.

The noncommuting profiles are sharper:

* at order four, one label of \(\mathcal K\) is totally ramified of
  index four and the other four labels form one complete unramified
  fiber;
* at order five, all five labels of \(\mathcal K\) form one complete
  unramified fiber.

This is a source-label quotient precursor. It is not currently an
active owner payment.

## 2. Exact input packet

The adapter receives:

1. the deployed KoalaBear field and source-facet labels
   \(\alpha_1,\ldots,\alpha_{12}\);
2. the canonical deck quotient
   \[
   \psi:\mathbf P^1_\lambda\to\mathbf P^1_{\rm src}
   \]
   and deck involution \(b\);
3. the five-label common set \(\mathcal K\);
4. the two selected endpoint rows \(j,k\), their actual free
   quadratics, selected records, and owner slopes;
5. the unique nonsingular involution \(\iota\) recovered from those
   free quadratics;
6. the passed common-decic and fixed-root gates;
7. the full quotient \(q\) and the descended map \(\Theta\) in (1.1);
8. the exact endpoint identities
   \[
   \Theta(\alpha_\ell)=\Theta(\alpha_m)
   \]
   for the two right-neighbor pairs.

All records and maps must be derived from the actual component. An
abstract set of labels with the same cardinalities is not admissible.

## 3. Why the existing active source-rational owner does not apply

The active owner

```text
ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
```

is defined from the fixed translated source pair
\((\epsilon_0,\epsilon_1)\). It requires a unique rational map

\[
\Psi:\mathbf P^1_x\to\mathbf P^1_{\rm slope},
\qquad
\Psi([h:1])=[-\epsilon_0(h):\epsilon_1(h)]
\quad(h\in\Sigma),
\tag{3.1}
\]

of degree at most

\[
E(|\Sigma|)=\left\lfloor\frac{|\Sigma|-1}{2}\right\rfloor.
\tag{3.2}
\]

For the same selected finite slope \(\eta\), moving-root
transversality must supply

\[
x\in D\setminus\Sigma,
\qquad
[\eta:1]=\Psi([x:1]).
\tag{3.3}
\]

The conic map \(\Theta\) has a different source and target: it acts on
source-label values after \(\psi\). Equations (1.1)--(1.2) constrain
only the five common labels and four endpoint-neighbor labels. They
do not prove (3.1), and they do not identify either endpoint owner
slope with an outside-source value as in (3.3).

Thus even the reciprocal \(\deg\Theta=2\) branch is not automatically
paid by the active owner.

## 4. Target theorem

> **Conic source-quotient elimination-or-owner adapter
> \((\mathrm{CSQEA}_{6,2})\).**
> For every actual reduced \(Q=6,s=6,u=2\) conic packet satisfying
> Section 2, one of the following holds:
>
> 1. the binary-decic, fixed-root, interpolation, or source-signature
>    equations are inconsistent; or
> 2. one of the two attached endpoint records instantiates an existing
>    active owner predicate, and the corresponding printed payment
>    contains that same selected owner slope.

The second conclusion must print:

1. the exact existing owner ID;
2. all parameters required by that owner's verifier;
3. the derivation from the same endpoint record;
4. same-slope membership in the owner's bounded image;
5. the existing projection and charge bound; and
6. the whole-slope first-match deletion.

Introducing a new geometric name for \(\Theta\), or merely bounding
\(|\Theta(\mathcal K)|\), is not payment.

## 5. Focused algebraic alternative

A direct exclusion proof is sufficient and currently looks more
tractable. For each of the \(3,3,2,1\) open endpoint-row orbits:

1. form the unique candidate involution from the two free quadratics;
2. impose nonsingularity;
3. impose the binary-decic proportionality minors;
4. impose reduced fixed-root avoidance;
5. impose the degree-\((2,4)\) coefficient interpolation equations;
6. impose the exact five common-orbit source signatures; and
7. prove that the resulting ideal contains the nonsingularity
   denominator, or that the pole graph becomes a paid complete cycle.

The reciprocal branch has only \(2,2,1,1\) endpoint orbits after the
shared-neighbor exclusion. The noncommuting branch needs only the
orders

\[
4,\ 5.
\]

This finite family is the preferred next internal proof target.

## 6. Possible proof strategies

### 6.1 Branch-profile elimination

Use the explicit dihedral/Chebyshev branch profile of \(\Theta\).
The ten common pole points and the two free pairs prescribe
ramification and fiber incidences. Compare those fibers with the
six-line star-configuration intersections and the exact component
edge signatures. In particular, consume the exact order-four
"one totally ramified label plus one regular four-fiber" and
order-five "one regular five-fiber" forms before expanding general
degree-four or degree-five maps.

For the reciprocal branch, first use the cheaper source-quintic gate
already emitted by
`experiments/generate_q6_u2_conic_decic_gates.py`: the two endpoint
neighbor pairs determine one source involution, the common source
quintic must be invariant under it, and exactly one common label must
be fixed. This gate has five proportionality minors and avoids
reconstructing the ten pole roots.

### 6.2 Coefficient-minor factorization

Expand one nonzero common-decic proportionality minor after
substituting the free-pair candidate. Factor it modulo the endpoint
interpolation relations. A factor already known to be nonzero, or an
existing paid endpoint minor, eliminates the orbit.

### 6.3 Source-signature graph classification

For a surviving candidate, recover the five common orbits and attach
their actual source-row pairs. Quotient by pole-graph symmetry only
after the numeric/symbolic gate has passed. The
\(P_3\sqcup C_3\) signature has already been excluded by the exact
endpoint-fiber collision in
`proof/q6_u2_star_conic_geometry_reduction.md`. It remains to show
that every permitted \(P_6\) or \(P_2\sqcup C_4\) dihedral signature
either creates a complete four-edge cycle or violates a
divided-difference equation.

### 6.4 Existing-owner adapter

Attempt this only with the full endpoint record. It must construct the
active domain-to-slope map \(\Psi\), prove all source-anchor equations,
and derive the outside-source moving root for the same owner. The
label quotient \(\Theta\) alone is insufficient.

## 7. Valid completion and falsifier

A valid completion is either a uniform symbolic exclusion of all
open endpoint orbits or a verifier-checkable same-record payment
through an existing owner.

A valid falsifier must provide an actual deployed source-facet
component satisfying every decic, fixed-root, interpolation, and
signature equation, together with proof that both attached owners
survive all earlier cells. An abstract dihedral label configuration
or a convenient finite-field normalization is only a regression.
