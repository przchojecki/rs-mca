# Hankel Regular-Window Plan for the F17^32 Row

Status: AUDIT.

Tracked-artifact note: this file has accumulated draft packet descriptions
across several M3 branches.  The files present in the current tree are the row
descriptor, the regular-window plan, the generic regular-minor certificate, and
the synthetic endpoint/top-window rank-witness packets explicitly listed
below.  Later sidecar descriptions are plans or archived branch summaries
unless their referenced files are present.

This note fixes the arithmetic target for the M3 regular-window audit in
`towards-prize.md`.

For the row

```text
C = RS[F_17^32,H,256],    |H| = 512,
```

we have `n=512` and `k=256`.  For exact agreement `A`, the v9 Hankel parameters
are

```text
j = n - A,
t = A - k.
```

The regular overdetermined condition is

```text
t >= j+1,
```

equivalently `2A >= n+k+1`.  Therefore the first regular agreement is

```text
A = ceil((512+256+1)/2) = 385.
```

The tangent-exact theorem starts at

```text
A = n - floor((n-k)/3) = 512 - 85 = 427.
```

Thus the first prize-facing non-tangent regular window is exactly

```text
385 <= A <= 426.
```

The concrete field/domain descriptor for this row is

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

with domain hash

```text
35904a892e0319b3805e91438ec2733427a351a72ce9654428d6a33bd3575b92
```

For the prefix maximal minor with rows `0..j` and columns `0..j`, the largest
syndrome index used is `2j`.  Across the window this ranges from `254` down to
`172`, so every prefix minor is syntactically available from a syndrome vector
of length `n-k=256`.  The full Hankel window also uses no index beyond `255`.

The minor sizes run from `128` at `A=385` down to `87` at `A=426`.  Interpolating
one determinant polynomial per agreement would require `4557` determinant
evaluations in total.

The important negative audit is that degree bounds alone cannot close the
safe-side budget.  The finite-slope `2^-128` budget is

```text
floor(17^32 / 2^128) = 6,
```

while the regular degree-bound sum over this window is `4515`.  Therefore the
next useful M3 packet must compute actual root tables, or else identify the
first agreement where the regular bucket is singular and pass that residual to
pivot charts.  A degree-only certificate for this whole window would be far too
weak.

The follow-up note

```text
experimental/notes/m1/f17_32_m3_generic_regular_minor.md
```

proves that every maximal row-set minor is generically nonzero, with exact
degree `j+1`, for every agreement in this window.  Across the window this
covers
`155193154203428426778689566118132250614039201839551` formal row-set charts,
with `1806` contiguous charts singled out as the practical first-search
subatlas.  Thus vanished regular minors for an actual syndrome pencil are
special singular strata, not a forced failure of the regular Hankel chart.

The finite rank-node dichotomy

```text
experimental/notes/m1/hankel_rank_node_dichotomy.md
experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/
  f17_32_n512_k256_m3_rank_node_dichotomy.json
```

turns this into a replayable regular/singular gate.  For a `t x (j+1)` affine
Hankel pencil, one full-rank finite specialization gives a nonzero maximal
minor, while rank deficiency at `j+2` distinct finite nodes forces all maximal
minors to vanish identically.

The null-polynomial split-locator gate

```text
experimental/notes/m1/hankel_nullpolynomial_split_locator_gate.md
experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/
  f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json
```

records the next filter after an ambient root table is computed.  Finite
regular roots in nonsingular buckets are ambient Hankel null-polynomials; actual
split-locator witnesses must additionally be monic degree-`j` divisors of
`X^512-1` and satisfy the finite-affine noncontainment test `H(v)ell != 0`.

The projective split-locator gate

```text
experimental/notes/m1/hankel_projective_split_locator_gate.md
experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/
  f17_32_n512_k256_m3_projective_split_locator_gate.json
```

records the endpoint companion: ambient infinity vectors satisfy
`H(v)ell=0, H(u)ell!=0`, while actual support-wise endpoint witnesses must also
normalize to monic degree-`j` divisors of `X^512-1`.  This keeps the rank-6
endpoint-sensitive branch from counting a large ambient kernel as split-locator
evidence before the divisor gate is checked.

The rank-6 projective witness family

```text
experimental/notes/m1/hankel_rank6_projective_witness.md
experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/
  f17_32_n512_k256_m3_rank6_projective_witness.json
```

shows that this endpoint issue is not only ambient.  For `385 <= A <= 426`,
a Hankel-realizable direction-rank-6 prefix-plus-six-spikes family has empty
finite canonical root table and a genuine split-locator endpoint at `[0:1]`.
The first three agreements are closed by a boundary dual-gcd computation.  This
does not close rank 6, but it rules out endpoint emptiness as a universal
Hankel-realizability argument.

The support- and weight-uniform endpoint companion

```text
experimental/notes/m1/hankel_rank6_projective_endpoint_uniform.md
experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/
  f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json
```

removes the prefix/unit-weight specialization from the endpoint half: for any
disjoint base support of size `j+1`, any six direction nodes, and any nonzero
weights, the projective split-locator endpoint `[0:1]` is present.  It does
not compute finite root tables.

The separated six-spike closure companion

```text
experimental/notes/m1/hankel_rank6_separated_six_spike_closure.md
experimental/data/certificates/hankel-f17-32-m3-rank6-separated-six-spike-closure/
  f17_32_n512_k256_m3_rank6_separated_six_spike_closure.json
```

adds the finite-root half for the tall subwindow `388 <= A <= 426`: for the
same disjoint support/weight family, every finite slope has full column rank
by a weighted Vandermonde factorization on `X union Y`, so the projective total
is exactly the endpoint `1`.  It does not cover the boundary agreements
`A=385,386,387`.

The boundary barycentric obstruction companion

```text
experimental/notes/m1/hankel_rank6_boundary_barycentric_obstruction.md
experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/
  f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json
```

shows that this tall cutoff is sharp for support/weight-uniform separated
families: at `A=385,386,387`, barycentric residues on `S=X union Y` force the
constant locator into `ker H(u+v)` at the finite slope `z=1`.  Thus those
boundary agreements need a separate finite-root classification or payment
argument.

The barycentric split-filter companion

```text
experimental/notes/m1/hankel_rank6_barycentric_split_filter.md
experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/
  f17_32_n512_k256_m3_rank6_barycentric_split_filter.json
```

then applies the split-locator gate to that explicit root: the `z=1` kernel
has only polynomials of degree `< |S|-t` (`5,3,1`), so it contains no
degree-`j` split locator.  The obstruction is therefore ambient-table
sharpness, not a displayed support-wise bad slope.

The barycentric exact-root companion

```text
experimental/notes/m1/hankel_rank6_barycentric_exact_root_table.md
experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/
  f17_32_n512_k256_m3_rank6_barycentric_exact_root_table.json
```

closes that barycentric boundary family: the ambient finite root table is
exactly `{1}`, that root is split-filtered, and the endpoint-uniform theorem
leaves support-wise projective total exactly `1`.

The boundary low-degree transfer companion

```text
experimental/notes/m1/hankel_rank6_boundary_low_degree_transfer.md
experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/
  f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json
```

is the general reduction for arbitrary nonzero separated-support weights at
`A=385,386,387`: every finite ambient root comes from a polynomial
`Q` of degree `< h`, with `h=5,3,1`, satisfying six direction-node consistency
equations before the split-locator gate is applied.

The `A=387` separated-boundary safety companion

```text
experimental/notes/m1/hankel_rank6_a387_separated_boundary_safety.md
experimental/data/certificates/hankel-f17-32-m3-rank6-a387-separated-boundary-safety/
  f17_32_n512_k256_m3_rank6_a387_separated_boundary_safety.json
```

uses the `h=1` case of this transfer to close arbitrary nonzero separated
weights at `A=387`: at most one finite split-locator root plus the endpoint,
so total projective contribution is at most `2 <= 6`.

The `A=386` conic-pair safety companion

```text
experimental/notes/m1/hankel_rank6_a386_conic_pair_safety.md
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/
  f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json
```

uses the `h=3` case of the transfer.  If two direction-ratio conics in the
projective `Q`-plane have no common component, Bezout gives at most four
finite roots; with the endpoint, the branch is projective-safe with total at
most `5`.  The common-component case is the next intermediate residual in the
`A=386` branch tree.

The `A=386` component-cut safety companion

```text
experimental/notes/m1/hankel_rank6_a386_component_cut_safety.md
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/
  f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json
```

narrows that residual.  If each irreducible component of a common conic
component of degree `1` or `2` is cut by some direction-ratio conic, the finite
roots are still bounded by `4`; with the endpoint, the projective total is at
most `5`.  The residual after this criterion is an irreducible component
contained in all direction-ratio conics.

The `A=386` global-component slope-map companion

```text
experimental/notes/m1/hankel_rank6_a386_global_component_slope_dichotomy.md
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/
  f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json
```

splits that residual further.  If the induced projective slope map on the
global component is constant, the non-base branch contributes at most one
finite slope plus the endpoint, so total is at most `2`.  The remaining cases
are a nonconstant moving-slope component and a slope-free base locus or
component.

The `A=386` slope-free containment companion

```text
experimental/notes/m1/hankel_rank6_a386_slope_free_containment.md
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/
  f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json
```

removes the displayed slope-free transfer vectors from the support-wise count:
they satisfy `H(v)L_Q=H(u)L_Q=0`, so they fail both finite-affine and
projective noncontainment gates.  If the same finite parameter has a different
independent noncontained vector, that parameter is charged once through the
non-slope-free branch; the slope-free vector is a contained shadow and adds no
second support-wise parameter.

The `A=386` moving-slope split-incidence companion

```text
experimental/notes/m1/hankel_rank6_a386_moving_slope_split_incidence.md
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/
  f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

attacks the remaining moving-slope component with the split-locator divisor
gate.  For an irreducible component `G` of degree `c` and forced split-root
core `r_G`, the unrefined finite source classes are bounded by
`floor(c(512-r_G)/(126-r_G))`.  The packet then uses the base-support cap
`deg Q<3` to sharpen this to `floor(c(385-e_G)/(124-e_G))` for forced external
core `e_G`.  Thus line components with `e_G<=71` are projective-safe after
adding the endpoint.  For irreducible conics, pair-overlap packing closes the
projective accounting for `e_G<=68`.

The high-core line branch first appears in quotient normal form: after
factoring the forced external core, the remaining split-locator degree is at
most `54`.  The forced-core product collapse closes this branch.  If a line
component has two distinct forced external roots, either it is a common-root
pencil with `L_{(T-alpha)S}=F*S`, `deg F<=125`, and at most one base root for
`F`, or modular reduction vanishes as `L_Q=R*Q` with `R` nonzero on the base
support.  A degree-`126` split locator would therefore require at least `124`
external forced roots, so the pre-tangent line range `72<=e_G<=120` is empty.

The high-core irreducible-conic branch has a global common forced core across
the whole `Q`-plane, and the product collapse closes it: the base interpolant
has its top two coefficients zero, so `L_Q=RQ`, and `e_G<=123` cannot supply a
degree-`126` split locator.  Thus line and irreducible-conic moving-slope
components are projective-safe for every external core size in the separated
positive-dimensional branch.

The packet still records the punctured-tangent and exact-agreement diagnostics.
The cofactor-span obstruction closes the punctured-tangent tail `e_G=120`:
seven tangent-star cofactors on the punctured row `(n',a')=(392,386)` would
arise, and at most one of the seven projective bad points is the original
endpoint.  Thus at least six independent cofactors must be finite `Q`-classes
on the component, while the fixed-core quotient family has vector dimension at
most `2` on a line and at most `3` on a conic.  More generally, top saturation
of the raw tangent bound `r'+1` is impossible whenever `r'` exceeds this
quotient dimension, so the cofactor-improved tangent bound is `r'`; `e_G=119`
is the next cofactor-current one-over tangent-tail diagnostic core and
`e_G>=120` is projective-safe.  Exact-agreement residual-budget splitting
closes the cofactor-current tangent tail `e_G=97..119` for lines and
`e_G=103..119` for irreducible conics.  The `d=r'+4` four-private branch closes
line cores `97..102` by a two-dimensional pencil disjoint-zero obstruction. The
`d=r'+3` three-private branch closes line cores `103..108` by cofactor span,
and closes conic cores `103..108` by a root-star Bezout obstruction: six
selected pairs on five residual coordinates force three pair-quadratic points
on one root-star line, impossible for an irreducible conic.  The `d=r'+2`
two-private branch closes lines and reduces conics `109..114` to a K4
boundary; the latter is closed by the pair-quadratic determinant
`prod_{i<j}(x_j-x_i)^2`.  The conic `d=r'+4` branch `97<=e_G<=102`
is not closed, but root-star Bezout closes all max-degree-at-least-3 graphs;
the only no-root-star survivors are two disjoint triangles or six-cycles, and
the six-cycle must satisfy the normalized hexagon factor
`a*b*d-a*c*d+a*c-a*d-b*c+c*d`.  The subgroup-coordinate nonvanishing route for
the six-cycle is false: exponents `0,255,417,261,6,356` give a deterministic
order-512 subgroup witness with zero hexagon factor and nonzero
alternating-line factor.  Thus the generic irreducible hexagon branch itself
is sharp at subgroup-coordinate level.  The six-cycle branch then splits by
one alternating-line factor: away from it the conic is
irreducible, while on it the conic is the union of the lines through cycle
edge triples `0,2,4` and `1,3,5`; the latter subbranch is closed for
irreducible conics by Bezout.  The two-triangle
branch is stronger: for every pair of disjoint residual triples, the six
pair-quadratic points are co-conic and no line contains three of them, so the
conic is irreducible; exponents `0,1,2,3,4,5` give the arithmetic replay.
After the line and conic product collapses, no separated positive-dimensional
moving-slope line or conic component remains live.  The line quotient-pencil
rows and the conic incidence, Pascal, and four-private rows remain as
pre-collapse diagnostics.  The packet still records the exact-current
diagnostic profile: before the line product collapse, the one-over range was
line `72..80`, the largest line projective bound was `18`, and line six-class
saturation had external slack `1..41`.  The sharpest diagnostic pressure case
was line `e_G=72` near-complete base splitting; it closed unless all six
classes had a base root and at least five had two.  Equivalently, line
`e_G=72` survival had base-root histogram `(0,0,6)` or `(0,1,5)`.  Exact
degree-`126` accounting left that line branch with either one unused nonforced
external root line or none.

The `A=386` separated-boundary closure companion now composes these local
packets into a closed separated-support branch theorem: arbitrary nonzero
separated rank-6 boundary weights at `A=386` are projective-budget safe.  This
uses the conic-pair, component-cut, global-component, slope-free, and
moving-slope packets as a case partition; it does not cover `A=385`,
overlapping supports, endpoint payment, or row-level M3 closure.

The diagnostic extremal line `e_G=72` branch is a degree-`54` quotient-pencil
obstruction: any survivor would need six fully split fibers of sizes `52^6` or
`53,52^5`, covering all or all but one nonforced external root.  More
generally, line cores `e_G=72..80` would require six full-split pencil fibers
of degrees `54..46`.  The line quotient-pencil and conic secant, Pascal, and
quotient-conic catalogs are retained as pre-collapse diagnostics only.
Across the full endpoint-only one-over range, the line histogram counts are
`2,16,27,28^6` for `e_G=72..80`, and the conic counts are `2,16,27,28^5`
for `e_G=69..76`.
The packet also constructs abstract incidence-only sharpness witnesses for
every one of those finite-incidence cores: line witnesses have six disjoint
external-root classes, and conic witnesses have pairwise intersections of
multiplicity at most one with no triple-used external line.  Thus these rows
cannot be closed by incidence and pair-overlap counting alone; the next input
must pay the endpoint, force a finite-slope collision, or use algebraic
quotient-fiber structure.
The packet also records a single-saving closure ledger for the finite-incidence
one-over diagnostic rows, line `e_G=72..80` and conic `e_G=69..76`, plus the
formerly raw line/conic punctured-tangent tail at `e_G=120`.  The subsequent
exact-agreement filter closes the cofactor-current tangent-tail rows
`e_G=97..119` for lines.  The exact-current rows are recorded as a
pre-collapse minimal obstruction profile: before product collapse, any
over-budget witness had to be one of the line cores `72..80`, with exactly six
finite source classes, six distinct finite slopes, and an unpaid projective
endpoint, plus the printed saturated base-root and external-slack conditions.
After both line and conic product collapses, that post-collapse profile is
empty.

The first concrete large-field stress packets for this window are the endpoint
rank-witness packets

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/
  f17_32_n512_k256_a385_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json
```

They use synthetic `F_17^32` syndrome pencils at `A=385` and `A=426` and prove
nonzero regular minors by rank witnesses.  This exercises the pinned
field/domain arithmetic at the largest and smallest minor sizes in the window,
and each endpoint packet carries the exact synthetic root table `{0}`.  The
fixed top-window packet

```text
experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/
  f17_32_n512_k256_a421_426_fixed_prefix92_packet.json
```

is a single v9 packet for one synthetic syndrome pencil covering
`421 <= A <= 426`; it has root union `{0}` across the six exact agreements.
These packets are not worst-case safe-side bounds.  They are selected
synthetic replays that replace degree-only evidence by exact finite root tables
for a small audited part of the window.

The bounded common-gcd replay

```text
experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/
  f17_32_n512_k256_a426_contiguous_gcd4_packet.json
```

checks the first four contiguous maximal row sets at `A=426`.  Each nonzero
minor is a scalar multiple of `Z^87`, so the monic common gcd is `Z^87` with
exact root table `{0}`.  This is still a synthetic bounded subatlas, but it
tests the v10 common-gcd packet path rather than only a selected prefix minor.

The formula companion

```text
experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/
  f17_32_n512_k256_a426_contiguous_gcd_formula.json
```

proves the same common-gcd conclusion for every contiguous row window at
`A=426`, not just the four replayed windows.  For `R_s={s,...,s+86}`, the
leading determinant factors as

```text
(prod_{x in X} x)^s * Vandermonde(X)^2
```

where `X` is the first `87` support nodes in the synthetic input.  This covers
all `84` contiguous row starts `0..83`.  It is still a contiguous-subatlas
result, not the all-row-set canonical gcd.

The all-window formula companion

```text
experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/
  f17_32_n512_k256_m3_contiguous_gcd_formula_window.json
```

extends the same zero-`u` nested-prefix formula to every agreement
`385 <= A <= 426`.  For each agreement, let `X_A` be the first `j+1`
descriptor-domain elements.  For a contiguous row set `R_s={s,...,s+j}`, the
leading determinant is

```text
(prod_{x in X_A} x)^s * Vandermonde(X_A)^2.
```

The first `128` descriptor-domain elements are distinct and nonzero, so this
coefficient is nonzero for every nested prefix and every allowed contiguous
start.  The certificate covers all `1806` contiguous row windows in the M3
regular window and proves that the monic contiguous-subatlas common gcd at
agreement `A` is `Z^(j+1)` with root table `{0}`.  This upgrades the synthetic
contiguous audit from one endpoint to the full M3 window, but still does not
claim the canonical all-row-set gcd/lcm ledger for arbitrary row data.

The canonical formula companion

```text
experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/
  f17_32_n512_k256_m3_canonical_gcd_formula_window.json
```

removes the contiguous-row-set restriction for this synthetic family.  For any
maximal row set `R={r_0<...<r_j}`,

```text
Delta_{A,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i} * det(x_i^b)_{i,0<=b<=j}.
```

Thus every nonzero maximal row-set minor is a scalar multiple of `Z^(j+1)`.
The prefix row set is nonzero by Vandermonde, so the v10 canonical monic gcd
over all nonzero maximal row-set minors is exactly `Z^(j+1)` at every
agreement in `385 <= A <= 426`.  This covers all
`155193154203428426778689566118132250614039201839551` formal row-set charts
for the synthetic zero-`u` nested-prefix family.  The remaining gap is
arbitrary row data, not the canonical-gcd object for this family.

The support-uniform companion

```text
experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/
  f17_32_n512_k256_m3_support_uniform_canonical_gcd.json
```

extends this from the nested-prefix support to every distinct support subset
`S={x_0,...,x_j}` of the descriptor domain with `|S|=j+1`.  For every maximal
row set `R={r_0<...<r_j}`,

```text
(v_{r_a+b})_{a,b} = (x_i^{r_a})_{a,i} * (x_i^b)_{i,b},
Delta_{A,S,R}(Z)
  = Z^(j+1) * det(x_i^{r_a})_{a,i} * det(x_i^b)_{i,0<=b<=j}.
```

The prefix row set is nonzero for every such `S` by Vandermonde.  Hence the
v10 canonical gcd is again `Z^(j+1)` with root table `{0}`, uniformly over all
support choices of size `j+1`.  This removes support-choice dependence inside
the zero-`u` rank-size power-sum branch, but does not classify arbitrary M3
syndrome pencils or supports of other sizes.

The weight-uniform companion

```text
experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/
  f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json
```

further extends the same branch from unit weights to arbitrary nonzero residue
weights.  For

```text
v_m = sum_i w_i x_i^m,        w_i in F_17^32^*,
```

the Hankel block factors as

```text
(v_{r_a+b})_{a,b}
  = (x_i^{r_a})_{a,i} * diag(w_i) * (x_i^b)_{i,b}.
```

The determinant is therefore `Z^(j+1)` times two alternants and
`prod_i w_i`.  The prefix row set is nonzero for every distinct support and
nonzero weight vector, so the v10 canonical gcd remains `Z^(j+1)` with root
table `{0}`.  This classifies the simple rank-size zero-`u` weighted
power-sum branch; arbitrary length-256 M3 pencils remain open.

The lower-rank companion

```text
experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/
  f17_32_n512_k256_m3_lower_rank_contained.json
```

classifies the adjacent singular bucket for the same family.  If the weighted
support rank is `r <= j`, then all `(j+1)x(j+1)` regular minors vanish because
`rank H(v) <= r`.  This is not an aperiodic residual: any agreement-at-least
`A` explanation has at least `A-r >= A-j = 2A-512 >= 258 > k` zeros outside
the rank support, so the explaining codeword is forced to be zero.  The
agreement support is contained in the complement of the rank support, where
both line generators are zero codeword restrictions.  Thus this lower-rank
singular bucket is removed by the contained/common-code-line filter and
contributes no support-wise noncontained aperiodic slopes.

The zero-`u` rank dichotomy companion

```text
experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/
  f17_32_n512_k256_m3_zero_u_rank_dichotomy.json
```

is the general regular-bucket version of these zero-`u` certificates.  For any
zero-`u` syndrome vector `v`,

```text
H_{t,j}(u)+Z H_{t,j}(v) = Z H_{t,j}(v),
Delta_R(Z)=Z^(j+1) det(H_R(v)).
```

Therefore full column rank of `H_{t,j}(v)` closes the regular bucket with
canonical gcd `Z^(j+1)` and paid root `Z=0`, while rank deficiency is exactly
the singular boundary that must be sent to M5 pivots or to a separate paid
classification.  The lower-rank weighted power-sum certificate is one such
paid singular classification; arbitrary rank-deficient zero-`u` data remains
outside this claim.

The syndrome-realizability sidecar

```text
experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/
  f17_32_n512_k256_rank_witness_syndrome_realizability.json
```

checks that the synthetic rank-witness syndrome pencils are actual row data.
It audits the pinned subgroup as the powers of an exact order-512 generator and
uses character orthogonality for exponents `-255..255` to verify the inverse
section

```text
y_s(x)=sum_{a=0}^{255} s_a x^(-a-1)
```

for the weighted syndrome map.  Thus the remaining M3 regular-window gap is
not construction of actual received-line values for these packets; it is
universal classification of arbitrary length-256 syndrome pencils after
tangent, quotient, and extension-confined branches are removed.

The zero-slope subtraction sidecar

```text
experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/
  f17_32_n512_k256_rank_witness_zero_slope_subtraction.json
```

checks the endpoint, top-window, and contiguous-gcd rank-witness packets above.
In all four source inputs, the `u` syndrome is identically zero.  Therefore the
raw root `Z=0` is a zero-syndrome common-code-line slope, paid by the tangent
ledger, and the residual synthetic aperiodic numerator after this subtraction is
`0`.
The resulting synthetic total upper bound is `1 <= 6` against the finite-slope
budget.  This is an M4 no-double-counting sidecar for the synthetic packets
only, not a universal row table.

The reusable theorem behind this realizability audit is the subgroup-section
identity

```text
experimental/notes/m1/subgroup_syndrome_section.md
experimental/data/certificates/subgroup-syndrome-section/
  subgroup_syndrome_section_certificate.json
```

This theorem is now a checked packet.  For the whole M3 window it applies
uniformly.  Since every exact bucket has

```text
t+j = (A-k)+(n-A) = n-k = 256 <= |H| = 512,
```

the same line-value section is available for any length-256 syndrome pencil;
the current sidecar records it for the four synthetic rank-witness inputs.

For the synthetic packets above, the sidecar records this M4 mini-table:

```text
B_tan=1,
B_quot_support=B_quot_image=0,
B_ap_regular_before_removed=1,
B_ap_after_removed=0,
B_ext=0,
B_projective_infinity=0,
deduped total upper bound = 1 <= budget 6.
```

This closes only the subtraction/budget table for that synthetic packet; the
universal row table still requires arbitrary length-256 syndrome pencils to be
classified by root table or singular-bucket outcome.

The status ledger also consumes

```text
experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/
  hankel_proportional_pencil_tangent_lemma_certificate.json
```

For this M3 window, `t+j=256` is exactly the stored syndrome length for every
agreement.  Therefore the lemma's tail caveat disappears here: if a length-256
syndrome pencil satisfies `u=c v`, then the branch is tangent/common-code-line
after the slope `Z=-c` and contributes no residual aperiodic roots.  This
classifies a universal proportional branch of arbitrary pencils, but it still
does not classify non-proportional pencils.

The certificate is replayed by

```sh
python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json
```

The finite tangent-overlap converse is:

```text
experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/
  f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json
```

It records that a finite root can be tangent/common-code-line only when
`u+zv=0` in the full stored syndrome.  Since `t+j=256` in this window, this is
equivalent to a proportional pencil, apart from the degenerate `u=v=0`
codeword-line branch.  Thus non-proportional finite root tables have no
tangent/common-code-line overlap.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_finite_tangent_overlap_criterion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json
```

The M5 finite-affine kernel filter is:

```text
experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/
  f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json
```

For a fixed finite root `z`, set `M_z=H(u)+zH(v)`.  The ambient affine
noncontainment chart `M_z ell=0, H(v)ell!=0` is empty iff
`ker M_z subset ker H(v)`, equivalently iff
`rank stack(M_z,H(v)) = rank M_z`.  If containment fails, the root contributes
at most the single finite parameter `z`.  This is a per-root filter for future
root tables, not a root table by itself.

The same packet proves the rank-stratification corollary:

```text
rank H(v) > rank M_z
  => z survives the ambient finite-affine kernel filter.
```

Consequently full-direction-rank finite regular roots cannot be removed by
same-support containment; after root-table computation they must be handled by
quotient, extension, subfield, or split-locator audits.

The regular-root rank-drop bridge is:

```text
experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/
  f17_32_n512_k256_m3_m5_regular_root_rank_drop.json
```

It proves that finite roots of the v10 canonical regular gcd are exactly finite
rank-drop slopes in nonsingular regular buckets.  Therefore root tables should
be read as rank-drop tables before applying the finite-affine kernel filter.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m5_finite_affine_kernel_chart.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json

python3 experimental/scripts/verify_m1_hankel_m5_regular_root_rank_drop.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/f17_32_n512_k256_m3_m5_regular_root_rank_drop.json
```

The projective-infinity endpoint criterion is:

```text
experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/
  f17_32_n512_k256_m3_projective_infinity_rank_criterion.json
```

For the homogenized pencil
`Z0 H_{t,j}(u)+Z1 H_{t,j}(v)`, every maximal minor specializes at infinity to
`det(H_R(v))`.  Hence full column rank of the direction Hankel block excludes
the projective endpoint `[0:1]`, while direction-rank deficiency is a singular
infinity chart to send to M5 or to a separate paid endpoint classification.

The M5 kernel-containment refinement is:

```text
experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/
  f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json
```

It proves that the ambient projective-infinity chart
`H(v) ell=0, H(u) ell!=0` is empty iff
`ker H(v) subset ker H(u)`, equivalently iff
`rank stack(H(v),H(u)) = rank H(v)`.  If the containment fails, the packet uses
a one-point `dimension_degree` fallback for `[0:1]`; it does not claim the
split-locator chart is nonempty.  In particular, proportional pencils have
empty projective-infinity chart even when `H(v)` is rank-deficient.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_projective_infinity_rank_criterion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/f17_32_n512_k256_m3_projective_infinity_rank_criterion.json

python3 experimental/scripts/verify_m1_hankel_m5_projective_infinity_kernel_chart.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json
```

The zero-direction-syndrome endpoint companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/
  f17_32_n512_k256_m3_zero_v_projective_endpoint.json
```

If `v=0`, the finite affine pencil is constant.  Full rank of `H_{t,j}(u)`
excludes finite affine roots; finite rank deficiency remains singular.  The
projective endpoint `[0:1]` is nevertheless paid in both cases, because the
direction syndrome is zero and hence the endpoint is a codeword direction.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_zero_v_projective_endpoint.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/f17_32_n512_k256_m3_zero_v_projective_endpoint.json
```

The finite direction-rank degree cap is:

```text
experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/
  f17_32_n512_k256_m3_direction_rank_degree_cap.json
```

For an arbitrary regular pencil, if `r=rank H_{t,j}(v)`, then every maximal
minor `det(H_R(u)+Z H_R(v))` has degree at most `r`; hence any nonsingular
canonical regular gcd has degree at most `r`.  Since the finite-slope budget is
`6`, direction rank at most `6` is finite-root budget safe at each exact
agreement.  This does not by itself close projective infinity for deficient
direction rank; the projective endpoint criterion above handles that
accounting.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_direction_rank_degree_cap.py \
  --check experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/f17_32_n512_k256_m3_direction_rank_degree_cap.json
```

The M4 projective budget split is:

```text
experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/
  f17_32_n512_k256_m3_m4_projective_budget_split.json
```

It combines the finite direction-rank cap with the one-point projective
infinity chart.  For this row the finite and projective budgets are both `6`.
Therefore direction rank at most `5` is projective-safe without endpoint
payment, while direction rank `6` is finite-safe but endpoint-sensitive.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_projective_budget_split.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/f17_32_n512_k256_m3_m4_projective_budget_split.json
```

The rank-6 ambient sharpness companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/
  f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json
```

For every agreement in the M3 window it constructs an ambient regular pencil
with direction rank `6`, six finite canonical roots, and a nonempty projective
endpoint.  The construction is

```text
C_{r,i}=alpha_r^i,
M(Z)=C diag(Z-1,...,Z-6,1,...,1),
```

so every maximal minor is a nonzero Vandermonde scalar times
`prod_{a=1}^6 (Z-a)`.  This is not a Hankel moment-pencil example; its role is
to prove that the rank-6 boundary cannot be closed by ambient rank and endpoint
accounting alone.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_rank6_ambient_sharpness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json
```

The rank-6 projective witness companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/
  f17_32_n512_k256_m3_rank6_projective_witness.json
```

Unlike the ambient sharpness packet, this is a Hankel moment-pencil family.  On
`385 <= A <= 426`, it has direction rank `6`, empty finite canonical root
table, and an actual split-locator projective endpoint.  The finite roots at
`A=385,386,387` are excluded by the boundary dual-gcd packet.  Thus the
endpoint half of the rank-6 boundary survives Hankel realizability, although
the packet does not show simultaneous six finite roots.

The endpoint-uniform companion strengthens only that endpoint half: any
separated rank-6 support/weight choice admits a split-locator endpoint by
leaving seven base nodes alive and applying a weighted Vandermonde argument.

The separated six-spike closure companion closes the finite side of that same
support/weight-uniform family in the tall range `388 <= A <= 426`: since
`t >= j+7`, every finite pencil block on `X union Y` has full column rank, so
no finite canonical roots remain and the projective count is exactly `1`.

The boundary barycentric obstruction shows that the cutoff at `A=388` is
genuine for support/weight-uniform separated families.  For `A=385,386,387`,
choosing barycentric-residue weights on `S=X union Y` makes the constant
locator vanish at finite slope `z=1`, while the endpoint remains present.
The split-filter companion proves that this displayed root has only
low-degree kernel polynomials and no degree-`j` split-locator witness.
The exact-root companion proves there are no other finite ambient roots in
that barycentric family, so after filtering only the endpoint remains.
The low-degree transfer theorem gives the corresponding search object for
arbitrary separated-support boundary weights: projective `Q`-spaces of
dimensions `4,2,0` plus six consistency equations and the split-locator gate.
For `A=385`, a common forced four-point base split-root core collapses the
`P^4` auxiliary space to a single `Q`-class, so that fixed-core branch is
projective-safe with total at most `2`; any over-budget separated branch must
avoid such a common base core.
The next fixed-core reduction factors a common three-point base core.  If a
pairwise direction-consistency equation is nonzero on the residual projective
`Q`-line, then at most two finite noncontained slopes survive and the endpoint
gives total at most `3`.  The only residual in that fixed-three-core subcase is
the ratio-identically-consistent `Q`-line.
With a common two-point base core, the residual `Q`-space is a projective
plane.  A no-common-component pair of direction-consistency conics gives at
most four finite noncontained slopes by Bezout, hence total at most `5` after
the endpoint.  The fixed two-core residual is now the common-component branch
on that plane.
The fixed two-core component-cut companion narrows that residual further: a
common component cut by some other direction-consistency conic remains
projective-safe with total at most `5`; the only fixed two-core residual left
by this branch is a global component contained in all direction-consistency
conics.
The fixed two-core global-component slope-map companion closes the
constant-slope off-base-locus subcase with total at most `2`; the remaining
fixed two-core global-component residuals are nonconstant moving-slope and
slope-free branches.
The fixed two-core slope-free companion closes the slope-free branch: after
`Q=E R` with `deg R<3`, slope-free forces `R` to vanish at all six direction
nodes, impossible for a nonzero residual polynomial.  The only fixed two-core
global-component residual left is therefore the determined nonconstant
moving-slope branch.
The fixed two-core moving-slope incidence companion gives the first thresholds
for that branch: line components are projective-safe for external forced core
`e_G<=70`, and irreducible conics are projective-safe for `e_G<=67` after
pair-overlap packing.  The high-core line/conic ranges remain open for
product-collapse, quotient, tangent-tail, or split-locator analysis.
For `A=387`, the projective `Q`-space is a point, so the arbitrary-weight
separated branch is already projective-safe with total at most `2`.
For `A=386`, a no-common-component pair of direction conics gives projective
safety by Bezout, and the separated-boundary closure companion now closes the
common-component tree for line/conic global components.  The remaining boundary
work here is `A=385`, overlapping support, and non-separated row-level
stratification.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/f17_32_n512_k256_m3_rank6_projective_witness.json

python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/f17_32_n512_k256_m3_rank6_boundary_dual_gcd.json

python3 experimental/scripts/verify_f17_32_m3_rank6_projective_endpoint_uniform.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json

python3 experimental/scripts/verify_f17_32_m3_rank6_separated_six_spike_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-separated-six-spike-closure/f17_32_n512_k256_m3_rank6_separated_six_spike_closure.json

python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_barycentric_obstruction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json

python3 experimental/scripts/verify_f17_32_m3_rank6_barycentric_split_filter.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/f17_32_n512_k256_m3_rank6_barycentric_split_filter.json

python3 experimental/scripts/verify_f17_32_m3_rank6_barycentric_exact_root_table.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/f17_32_n512_k256_m3_rank6_barycentric_exact_root_table.json

python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_low_degree_transfer.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_base_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-base-core-closure/f17_32_n512_k256_m3_rank6_a385_base_core_closure.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_quadratic_cut.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_conic_pair_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-pair-safety/f17_32_n512_k256_m3_rank6_a385_two_core_conic_pair_safety.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_component_cut_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-component-cut-safety/f17_32_n512_k256_m3_rank6_a385_two_core_component_cut_safety.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_global_component_slope_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy/f17_32_n512_k256_m3_rank6_a385_two_core_global_component_slope_dichotomy.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_slope_free_empty.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-slope-free-empty/f17_32_n512_k256_m3_rank6_a385_two_core_slope_free_empty.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_moving_slope_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-moving-slope-incidence/f17_32_n512_k256_m3_rank6_a385_two_core_moving_slope_incidence.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a387_separated_boundary_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a387-separated-boundary-safety/f17_32_n512_k256_m3_rank6_a387_separated_boundary_safety.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a386_conic_pair_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a386_component_cut_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a386_global_component_slope_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a386_slope_free_containment.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a386_separated_boundary_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-separated-boundary-closure/f17_32_n512_k256_m3_rank6_a386_separated_boundary_closure.json
```

The affine-pivot compression theorem is:

```text
experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/
  f17_32_n512_k256_m3_m4_affine_pivot_compression.json
```

For a row-set chart with finite pivot `z0` and `M_R(z0)` invertible, a rank
factorization `H_R(v)=P_R Q_R` gives

```text
det M_R(z0+w)
  = det M_R(z0) det(I_r + w Q_R M_R(z0)^(-1) P_R).
```

Thus the endpoint-sensitive rank-6 finite-root problem has a concrete `6 x 6`
compressed determinant target on each affine pivot chart.  This complements the
ambient sharpness packet: rank-only accounting is insufficient, but exact
rank-6 root tables need not be computed from the full `87..128` dimensional
minors.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_compression.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/f17_32_n512_k256_m3_m4_affine_pivot_compression.json
```

The affine-pivot gcd-equivalence packet is:

```text
experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/
  f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json
```

It records two facts needed to use compression inside the v10 canonical gcd
ledger.  First, a nonzero rank-6 minor has at most six bad pivots over
`F_17^32`, so good finite pivots are abundant.  Second, replacing each nonzero
row-set determinant by its affine-pivot compressed determinant only rescales
that gcd input by a nonzero constant after translating the local compressed
polynomial back to the global slope variable, so the monic gcd and root table
are unchanged.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_gcd_equivalence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json
```

The current M4 regular-bucket synthesis table is:

```text
experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/
  f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json
```

It composes the zero-`u`, proportional, tangent-overlap, M5 finite-affine
kernel, M5 regular-root rank-drop, projective-infinity, zero-`v`, M5
infinity-kernel, projective-budget, lower-rank-contained, and direction-rank
certificates into one decision table.  It marks the currently closed branches,
the projective-safe rank-`<=5` branch, the endpoint-sensitive rank-`6`
boundary, and the residual branches still requiring root tables, quotient,
extension, or subfield ledgers.

Replay:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json
```

The corresponding F1 denominator audit is

```text
experimental/notes/f1/f17_32_m3_extension_denominator_audit.md
experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/
  f17_32_n512_k256_a421_426_extension_denominator_audit.json
```

It verifies that `g` is non-base-valued at all 512 positions, so finite affine
slopes for this packet are sampled from `F_17^32` and the denominator is
`q_line=17^32`.

The extractor has a reusable non-proportional one-spike mode.  For moments
`u_m=sum_{x in X}x^m` with a one-spike direction `v_m=y^m`, the prefix
determinant is affine in the slope by Cauchy-Binet.  Thus such directions have
at most one selected-prefix regular-minor root per exact agreement, with
explicit coefficients replayed by the packet checker.

This mode is instantiated at the M3 endpoint `A=426` by

```text
experimental/data/hankel-regular-minor-inputs/
  f17_32_n512_k256_a426_one_spike_input.json

experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/
  f17_32_n512_k256_a426_one_spike_packet.json
```

This packet uses a non-proportional synthetic `F_17^32` syndrome pencil and
proves a degree-1 prefix regular minor with one explicit root.  The checker
replays both the declared moments and the Cauchy-Binet coefficients.  It is
still not a universal M3 row table or a safe-side MCA bound.

The canonical-gcd companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/
  f17_32_n512_k256_m3_one_spike_canonical_empty.json
```

It proves that the selected-prefix root is an overcount for the v10 regular
branch.  For every `385 <= A <= 426` and every finite slope `z`, the full
overdetermined Hankel matrix for the one-spike family has rank `j+1`; hence the
canonical finite root table is empty.  The same rank argument works after
scalar extension, so the canonical gcd is constant.  At projective infinity,
`H(v)` has rank one while `H(u)` has full column rank, so the M5 kernel chart
gives the one-point dimension-degree fallback.

The projective-infinity split witness is:

```text
experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/
  f17_32_n512_k256_m3_one_spike_projective_witness.json
```

For each agreement it chooses the split locator with roots consisting of the
spike node and the first `j-1` base nodes.  The direction syndrome vanishes on
this locator, while the base syndrome survives on the two remaining base nodes.
Thus the projective endpoint `[0:1]` is actually present, not merely bounded by
dimension degree.

The support-and-weight uniform one-spike theorem is:

```text
experimental/data/certificates/hankel-f17-32-m3-one-spike-uniform/
  f17_32_n512_k256_m3_one_spike_uniform.json
```

It removes the prefix and unit-weight restrictions.  For any descriptor-domain
support `X` of size `j+1`, any spike `y` outside `X`, and any nonzero weights,
the finite canonical root table is empty and the projective endpoint is exactly
present.  This is the reusable one-spike result; the prefix packets above are
special-case replays of it.

The M4 budget companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/
  f17_32_n512_k256_m3_one_spike_m4_budget.json
```

It prints both sampler denominators and turns the canonical closure into a
safe-side upper-bound table for this synthetic family:

```text
finite affine numerator: 0 <= floor(|F|/2^128) = 6,
projective numerator:    1 = 1 <= floor((|F|+1)/2^128) = 6.
```

A broader low-rank update theorem is recorded in

```text
experimental/notes/m1/hankel_low_rank_update_template.md
experimental/data/certificates/hankel-low-rank-update-template/
  hankel_low_rank_update_template_certificate.json
```

It proves that if

```text
u_m = sum_{x in X} x^m,    v_m = sum_{y in Y} y^m,
```

then every prefix determinant has degree at most `|Y|` in the slope, with
Cauchy-Binet coefficients indexed by how many update nodes are selected.  Thus
small-rank non-proportional directions give regular-minor root bounds
independent of the minor size; identically zero determinants are explicitly
singular residual buckets for the pivot atlas, not aperiodic evidence.
The v4 certificate also records the corrected M3 budget envelope and packet
gate: because both
the finite and projective `F_17^32` budget numerators are `6`, every nonzero
regular low-rank update chart of rank `s <= 6` is finite-root budget safe.
Projective automatic safety without a separate infinity exclusion holds for
`s <= 5`; rank `6` needs infinity exclusion, finite-root slack, or an
equivalent deduplication/removal certificate before projective accounting.

The corresponding rank-2 `F_17^32` endpoint packet is

```text
experimental/data/hankel-regular-minor-inputs/
  f17_32_n512_k256_a426_low_rank2_input.json

experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/
  f17_32_n512_k256_a426_low_rank2_packet.json
```

It proves a degree-2 prefix regular-minor bound at `A=426`.  The compressed
quadratic now splits over `F_17^32`, so the packet records the exact two roots,
their split-linear factorization certificate, and a quadratic discriminant
certificate; the checker replays the determinant coefficients, the compressed
kernel sidecar, and the root certificate from the low-rank input.

The same rank-2 construction has an all-window synthetic family certificate:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/
  f17_32_n512_k256_m3_low_rank2_family_certificate.json
```

For every `385 <= A <= 426`, it uses the first `j+1` descriptor-domain nodes as
the square base and the next two descriptor-domain nodes as the low-rank
update.  The degree cap is `84`, versus the generic window sum `4515`.
Applying the rank-2 discriminant gate gives exact roots: 20 rows split, 22 rows
have nonsquare discriminant, and the exact finite-root total is `40`.  The
family also audits the projective endpoint `[0:1]`: every leading coefficient
of the compressed quadratic is nonzero, but the original regular-minor
projective endpoint is not excluded because the update direction has rank
`2 < j+1`.  Infinity therefore contributes one projective point in every row,
and every agreement has at most 3 projective regular roots against budget
numerator 6.  It also compares the 40 finite roots against the common-code-line
tangent ledger: at every finite root, the full syndrome has nonzero witness
`Syn_0(u+zv)=|X|+2z`, so no finite low-rank-family root is
tangent/common-code-line.  The family cross-checks the `A=426` endpoint against
the exact-root v9 packet.

The rank-3 companion certificate is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/
  f17_32_n512_k256_m3_low_rank3_family_certificate.json
```

It uses the same nested prefixes and the next three descriptor-domain nodes as
the update set.  The degree cap is `3 * 42 = 126`, and the exact finite-root
count is computed by `gcd(Delta,Z^q-Z)`: 12 rows have no finite roots, 24 rows
have one finite root, and 6 rows have three finite roots, for total `42`.  The
original regular-minor projective endpoint is not excluded, so infinity
contributes one projective point in every row and every agreement has at most 4
projective regular roots against budget numerator 6.  The common-code-line
tangent overlap is also zero, because the Frobenius gcd is nonzero at the only
possible slope from `Syn_0(u+zv)=|X|+3z`.

The rank-4 budget companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/
  f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json
```

It uses the next four descriptor nodes for `Y` and verifies that every
compressed determinant has degree exactly `4`.  Exact finite roots are not
enumerated, because the v4 low-rank packet gate makes degree-only accounting
strong enough at rank `4`: at most four finite roots plus the corrected
projective infinity contribution gives at most five projective regular roots
per agreement, below budget numerator `6`.

The rank-5 budget companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/
  f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json
```

It uses the next five descriptor nodes for `Y` and verifies that every
compressed determinant has degree exactly `5`, using Newton identities from the
traces of powers of the compressed kernel.  This is the last automatically
projective-safe rank in the v4 gate: at most five finite roots plus the
corrected projective infinity contribution gives at most six projective regular
roots per agreement, exactly the budget numerator `6`.

The rank-6 finite-slack companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/
  f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json
```

It uses the next six descriptor nodes for `Y`.  Degree-only accounting would
give `6+1=7`, so the certificate computes exact finite roots with
`gcd(Delta,Z^q-Z)`.  The root histogram is `{0:16, 1:17, 2:9}`, hence every
agreement has at most two finite roots and at most three projective regular
roots after the corrected infinity point.  This supplies the finite-root slack
that the v4 gate requires at rank `6`.

The rank-7 finite-slack companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/
  f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json
```

It uses the next seven descriptor nodes for `Y`, beyond the v4 low-rank degree
envelope.  Degree-only accounting would give finite bound `7` and projective
bound `8`, both above budget numerator `6`.  Exact finite-root counts have
histogram `{0:16, 1:15, 2:6, 3:4, 4:1}`, so finite-root slack still gives at
most five projective regular roots per agreement.

The rank-8 finite-slack companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/
  f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json
```

It uses the next eight descriptor nodes for `Y`, another step beyond the v4
low-rank degree envelope.  Degree-only accounting would give finite bound `8`
and projective bound `9`, both above budget numerator `6`.  Exact finite-root
counts have histogram `{0:22, 1:10, 2:7, 3:2, 4:1}`, so finite-root slack again
gives at most five projective regular roots per agreement.

The rank-9..11 finite-slack sweep is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/
  f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json
```

It records a compact multi-rank replay rather than separate bulky kernel
sidecars.  Exact finite-root histograms are `{0:17, 1:17, 2:6, 3:2}` for rank
`9`, `{0:8, 1:23, 2:9, 3:2}` for rank `10`, and
`{0:15, 1:16, 2:5, 3:6}` for rank `11`.  Thus the checked sweep has at most
three finite roots, and at most four projective regular roots after the
corrected infinity point, despite degree-only projective bounds `10`, `11`,
and `12`.

The low-rank projective-infinity companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/
  f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json
```

It proves that the corrected projective endpoint `[0:1]` is an actual
support-wise noncontained endpoint for the synthetic low-rank ladder at ranks
`2..11`, not merely a point left unexcluded by the top-degree regular minor.
The witness support is `D \ Y`, and simultaneous containment is ruled out by
Vandermonde independence on `X union Y`.

The endpoint quotient-support companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/
  f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json
```

It checks the same actual supports `D \ Y` against all nontrivial proper
quotient fiber sizes `c in {2,4,8,16,32,64,128,256}`.  Since the consecutive
update block `Y` always meets more than `ceil(|Y|/c)` quotient fibers, these
endpoint supports are not quotient-remainder supports.  This is not an audit of
the trivial fiber sizes `c=1,512`, finite affine roots, or quotient-image
supports.

The first v9 projective-infinity pivot packet extracted from this audit is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/
  f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json
```

It packages the rank-6, `A=426` endpoint as a projective-line `pivot_atlas`
record.  The `projective_infinity` chart is nonempty with contribution one,
verified by the v9 packet checker through a coverage reference to the same
Vandermonde endpoint witness.  Finite affine roots are deliberately not
enumerated in this chart packet.

The finite-affine v9 companion for the same synthetic row is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-finite-affine/
  f17_32_n512_k256_a426_rank6_finite_affine_packet.json
```

It records the rank-6, `A=426` prefix regular minor with degree `6` and one
exact finite root.  The packet checker replays both the low-rank update input
and the `gcd(Delta,Z^q-Z)` certificate, giving one concrete v9 finite/projective
chart pair inside the synthetic low-rank ladder.

The tangent/common-code-line exclusion companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/
  f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json
```

For rank `s`, moment zero gives `Syn_0(u+zv)=|X|+s z`, so the only possible
common-code-line slope is `z=-|X|/s`.  Since `6 <= s <= 11` is nonzero in
characteristic `17`, the verifier checks `Delta_s(-|X|/s) != 0` for every
rank/agreement pair.  This proves that the `238` finite roots counted by the
rank `6..11` slack certificates have zero common-code-line tangent overlap.

The proper-subfield/confinement companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/
  f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json
```

It checks the proper subfields `F_17^d` for `d in {1,2,4,8,16}` by Frobenius
fixedness on listed roots and by subfield gcds on count-only rows.  The result
is zero proper-subfield overlap for the same `238` counted finite roots.

The rank-6..11 known-ledger table is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/
  f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json
```

It combines the exact finite-root counts, projective-infinity endpoint,
tangent exclusion, and proper-subfield exclusion into one M4-style residual
table.  Across all `252` rank/agreement rows, the maximum residual projective
regular-root upper count after these known ledgers is `5 <= 6`.  Quotient
support/image subtraction for finite affine roots is deliberately recorded as
`not_audited`.

The current status ledger

```text
experimental/data/certificates/hankel-f17-32-m3-regular-window-status/
  f17_32_n512_k256_m3_regular_window_status.json
```

hashes the plan, generic certificate, synthetic family certificates, and fixed
top-window packet.  It records, per agreement, that the generic/synthetic facts
are proved but actual `F_17^32` row-data root tables and singular-bucket
outcomes remain unsupplied.

Reproduce the audit packet:

```sh
python3 experimental/scripts/plan_f17_regular_hankel_window.py \
  --check experimental/data/certificates/hankel-regular-window-f17-385-426/f17_32_n512_k256_regular_window_plan.json

python3 experimental/scripts/verify_f17_32_m3_regular_window_status.py \
  --check experimental/data/certificates/hankel-f17-32-m3-regular-window-status/f17_32_n512_k256_m3_regular_window_status.json

python3 experimental/scripts/verify_f17_32_m3_line_value_lift.py \
  --check experimental/data/certificates/hankel-f17-32-m3-line-value-lift/f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json

python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --check experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json

python3 experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/f17_32_n512_k256_m3_rank_node_dichotomy.json

python3 experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json

python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_a421_426_zero_slope_subtraction.json

python3 experimental/scripts/verify_f17_32_m3_extension_denominator_audit.py \
  --check experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/f17_32_n512_k256_a421_426_extension_denominator_audit.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --one-spike-linear \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_canonical_empty.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/f17_32_n512_k256_m3_one_spike_canonical_empty.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/f17_32_n512_k256_m3_one_spike_projective_witness.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_uniform.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-uniform/f17_32_n512_k256_m3_one_spike_uniform.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_m4_budget.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/f17_32_n512_k256_m3_one_spike_m4_budget.json

python3 experimental/scripts/verify_m1_hankel_low_rank_update_template.py \
  --check experimental/data/certificates/hankel-low-rank-update-template/hankel_low_rank_update_template_certificate.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --low-rank-update-count 2 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/f17_32_n512_k256_a426_low_rank2_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/f17_32_n512_k256_a426_low_rank2_packet.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/f17_32_n512_k256_m3_low_rank2_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank3_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/f17_32_n512_k256_m3_low_rank3_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank4_budget_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank5_budget_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank7_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank8_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank9_11_slack_sweep.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_projective_infinity.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_projective_pivot.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_tangent_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_subfield_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_known_ledger_table.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json
```

Non-claims: this note does not enumerate universal root sets for arbitrary
syndrome pencils, classify singular buckets, or prove a safe-side MCA bound.
