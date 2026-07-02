# F17^32 M3/M4 Regular-Bucket Synthesis

Status: AUDIT.

This directory composes the current M3/M4 regular-window lemmas for the pinned
row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

It composes proved local certificates into a decision table for a regular pencil

```text
M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v).
```

Closed by current lemmas:

```text
v=0 and rank H(u)=j+1:
  no finite affine roots;
  projective infinity is tangent/common-code-line paid.

v!=0, u=c v, and rank H(v)=j+1:
  the unique finite root z=-c is tangent/common-code-line paid;
  projective infinity is excluded.

u=0 and rank H(v)=j+1:
  the c=0 proportional subcase.
```

Finite/projective-safe with projective kernel accounting:

```text
v!=0, u not proportional to v, rank H(v)<=5, and the finite regular bucket is
nonsingular:
  finite affine root count <=5 and has zero tangent overlap;
  projective infinity contributes at most one endpoint;
  finite + projective contribution <=6.

v!=0, u not proportional to v, rank H(v)=6, and the finite regular bucket is
nonsingular:
  finite affine root count <=6, so the finite sampler is safe;
  the projective sampler is endpoint-sensitive and needs endpoint empty/paid
  or an exact finite root table with at most 5 surviving roots.
```

Still residual:

```text
rank-deficient finite regular buckets not covered by a paid family;
non-proportional finite buckets with direction rank >6 unless exact root
tables improve the bound;
rank-6 projective endpoint-sensitive buckets when the endpoint is not paid and
six finite roots survive;
quotient, extension, and subfield overlap for future non-proportional root
tables.
```

For projective samplers, a nonempty infinity kernel chart contributes the single
endpoint `[0:1]`.  Thus a finite-affine rank-`<=5` bucket is projective-budget
safe without an endpoint payment, while rank `6` is exactly the endpoint-sensitive
boundary.

The ambient sharpness packet

```text
experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/
  f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json
```

shows that this boundary is real for arbitrary regular pencils: rank `6`, six
finite roots, and one projective endpoint can occur simultaneously.  The M3
rank-6 boundary must be attacked with Hankel-specific structure, exact root
tables, or a paid/empty endpoint ledger.

The rank-6 projective witness packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/
  f17_32_n512_k256_m3_rank6_projective_witness.json
```

proves that the endpoint part of the boundary is Hankel-realizable.  On
`385 <= A <= 426`, a prefix-plus-six-spikes Hankel family has direction rank
`6`, empty finite canonical root table, and a genuine split-locator endpoint
at `[0:1]`; the first three finite-root closures come from the boundary
dual-gcd packet.  Thus endpoint emptiness cannot be used as a universal rank-6
closure argument.

The endpoint-uniform packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/
  f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json
```

strengthens the endpoint half without touching finite roots: for any disjoint
base support of size `j+1`, any six direction nodes, and any nonzero weights,
the split-locator endpoint `[0:1]` is present.  Thus endpoint nonemptiness is
not a prefix-support artifact.

The separated six-spike closure packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-separated-six-spike-closure/
  f17_32_n512_k256_m3_rank6_separated_six_spike_closure.json
```

adds the finite-root half in the tall range `388 <= A <= 426`: for the same
disjoint support/weight family, `t>=j+7`, so every finite slope has full column
rank by weighted Vandermonde factorization.  The projective count is exactly
the single endpoint `[0:1]`.

The boundary barycentric obstruction packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/
  f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json
```

shows that the cutoff is sharp for support/weight-uniform separated families.
At `A=385,386,387`, barycentric-residue weights on `X union Y` make the
constant locator a finite kernel vector at slope `z=1`; the endpoint remains
present by the endpoint-uniform packet.

The barycentric split-filter packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/
  f17_32_n512_k256_m3_rank6_barycentric_split_filter.json
```

filters that displayed finite root through the null-polynomial split-locator
gate: the `z=1` kernel consists only of polynomials of degree `< |S|-t`, so it
contains no monic degree-`j` divisor of `X^512-1`.

The barycentric exact-root packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/
  f17_32_n512_k256_m3_rank6_barycentric_exact_root_table.json
```

proves the ambient finite root table of the same barycentric boundary family
is exactly `{1}`.  After the split filter, the finite support-wise contribution
is zero and the endpoint-uniform packet leaves projective total `1`.

The boundary low-degree transfer packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/
  f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json
```

records the general separated-support boundary reduction: arbitrary nonzero
weights at `A=385,386,387` reduce to an auxiliary `Q` of degree `< h` with
`h=5,3,1`, six direction-node consistency equations, and then the
split-locator gate.

The `A=387` separated-boundary safety packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a387-separated-boundary-safety/
  f17_32_n512_k256_m3_rank6_a387_separated_boundary_safety.json
```

uses the `h=1` specialization to close arbitrary nonzero separated weights at
`A=387`: at most one finite split-locator root plus the endpoint, so projective
total is at most `2`.

The `A=386` conic-pair safety packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/
  f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json
```

uses the `h=3` transfer.  If two direction-ratio conics in the `Q`-plane have
no common component, Bezout gives at most four finite roots; with the endpoint,
the projective total is at most `5`.

The `A=386` component-cut safety packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/
  f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json
```

handles part of the common-component residual.  If each irreducible component
of a common conic component of degree `1` or `2` is cut by some direction
conic, the component cut plus the off-component residual intersection gives at
most four finite roots; with the endpoint, the projective total is at most `5`.
The remaining residual is an irreducible component contained in all direction
conics.

The `A=386` global-component slope-map packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/
  f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json
```

splits that residual.  A constant induced slope map gives at most one finite
slope off its base locus plus the endpoint, hence total at most `2` for that
non-base branch.  The remaining residuals are a nonconstant moving-slope
component and a slope-free base locus or component.

The `A=386` slope-free containment packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/
  f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json
```

filters the displayed slope-free transfer vectors.  They satisfy
`H(v)L_Q=H(u)L_Q=0`, so they fail both finite-affine and projective
noncontainment gates and do not contribute support-wise parameters by
themselves.

The `A=386` moving-slope split-incidence packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/
  f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

then applies the split-locator divisor gate to the moving component.  If an
irreducible component `G` has degree `c` and forced split-root core `r_G`, its
unrefined finite source classes are bounded by `floor(c(512-r_G)/(126-r_G))`.
Using the base-support cap that `deg Q<3`, this sharpens to
`floor(c(385-e_G)/(124-e_G))` for forced external split-root core `e_G`.  Line
components with `e_G<=71` are projective-safe after the endpoint.  For
irreducible conics, pair-overlap packing closes projective accounting for
`e_G<=68`.  Large-external-core lines and conics remain residual, but their
forced cores now have a sharper structure: a high-core line is a
dual-evaluation-fiber quotient pencil of degree at most `54`, while a high-core
irreducible conic has a global common forced core and becomes a quotient family
of degree at most `57`.  After puncturing the forced core, the projective
tangent staircase bounds finite slopes and infinity together by `127-e_G`;
hence the very-high-core tail `e_G>=121` is projective-safe.  The boundary row
`e_G=120` is also projective-safe by a cofactor-span obstruction: seven
tangent-star cofactors on the punctured row would arise, and at most one of the
seven projective bad points is the original endpoint.  Hence at least six
independent cofactors must be finite `Q`-classes on the component, but the
fixed-core quotient family has vector dimension at most `2` on a line and at
most `3` on an irreducible conic.  More generally, top saturation of the raw
tangent bound `r'+1` is impossible whenever `r'` exceeds this quotient-family
dimension, so the cofactor-improved tangent bound is `r'`; `e_G=119` is the
next cofactor-current one-over tangent-tail core and `e_G>=120` is
projective-safe.  Exact-agreement residual-budget splitting closes the
cofactor-current tangent tail `e_G=97..119` for lines and `e_G=103..119` for
irreducible conics.  The `d=r'+4` four-private branch closes line cores
`97..102` by a two-dimensional pencil disjoint-zero obstruction.  The
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
order-512 subgroup witness with zero hexagon factor.  The six-cycle branch
then splits by one alternating-line factor: away from it the conic is
irreducible, while on it the conic is the union of the lines through cycle
edge triples `0,2,4` and `1,3,5`; the latter subbranch is closed for
irreducible conics by Bezout.  The two-triangle
branch is stronger: for every pair of disjoint residual triples, the six
pair-quadratic points are co-conic and no line contains three of them, so the
conic is irreducible; exponents `0,1,2,3,4,5` give the arithmetic replay.
Thus the remaining unclosed intermediate ranges are `72<=e_G<=96` for lines
and `69<=e_G<=102` for irreducible conics.
The exact-current residual profile has live one-over ranges line
`e_G=72..80` and irreducible conic `e_G=69..76`; the largest conic projective
bound drops from `26` to `25`.
Inside these ranges the cofactor-current proof envelope has finite-incidence
one-over-budget subranges `72<=e_G<=80` for lines and `69<=e_G<=76` for
irreducible conics; the worst current projective upper bounds in the middle are
`18` and `25`, respectively.  The endpoint-only finite-incidence subranges now
carry saturation constraints: line six-class saturation has external slack
`1..41`, while conic six-class saturation needs `0..14` forced pair-overlap
events before external excess.  A genuine finite-incidence over-budget witness
must also have six distinct finite slopes and an unpaid endpoint; the strongest
remaining pressure cases are line `e_G=72` near-complete base splitting and
conic `e_G=69` almost-complete secants.  The line `e_G=72` case closes unless
all six classes have a base root and at least five have two; the conic
`e_G=69` case closes unless at least `14` of `15` pair secants occur, forcing
at least `16` secant triangles.  Equivalently, line `e_G=72` survival has
base-root histogram `(0,0,6)` or `(0,1,5)`, and conic `e_G=69` survival has
secant graph `K6` or `K6` minus one edge.
The packet also constructs abstract incidence-only sharpness witnesses for
every finite-incidence one-over core: line witnesses have six disjoint
external-root classes, while conic witnesses have pairwise intersections of
multiplicity at most one and no triple-used external line.  These witnesses are
not Hankel-realizability claims; they show that incidence and pair-overlap
counting alone cannot close the remaining finite-incidence one-over rows.
Exact degree-`126` accounting leaves line `e_G=72` with either one unused
nonforced external root line or none, and conic `e_G=69` with either `14`
pair-overlaps or all `15`.
Combining the shape and root-budget constraints leaves two line partition
shapes and three conic secant-cover shapes.
Equivalently, the line multiplicity profiles are `(1,312,0)` and `(0,313,0)`,
while the conic multiplicity profiles are `(1,300,15)`, `(0,302,14)`, and
`(0,301,15)`.
The local line singleton sequences are `52^6` or `(53,52^5)`, and the local
conic secant/singleton profiles are `(5^6;50^6)`,
`((4,4,5,5,5,5);(51,51,50,50,50,50))`, or
`(5^6;(51,50,50,50,50,50))`.
The extremal line `e_G=72` branch is now a degree-`54` quotient-pencil
obstruction: any survivor needs six fully split fibers of sizes `52^6` or
`53,52^5`, covering all or all but one nonforced external root.
The exact-current finite-incidence residuals now have a quotient obstruction
catalog: line cores `e_G=72..80` require six full-split pencil fibers of
degrees `54..46`, while conic cores `e_G=69..76` require six full-split
quotient-conic members of degrees `57..50` with the printed overlap ranges.
The extremal conic `e_G=69` branch now has a Pascal obstruction profile:
`K6` secant covers force `60` Pascal collinearities among opposite external
secant intersections, while `K6` minus one edge forces `36`; failure of these
relations in the actual external root-line arrangement would close the
corresponding extremal branch.
Across the full endpoint-only one-over range, the line histogram counts are
`2,16,27,28^6` for `e_G=72..80`, and the conic counts are `2,16,27,28^5`
for `e_G=69..76`.
The packet also records a single-saving closure ledger for all cofactor-current
one-over moving-slope residual rows: line `e_G=72..80`, conic `e_G=69..76`,
and the line/conic punctured-tangent tail at `e_G=120`.  The subsequent
exact-agreement filter closes the cofactor-current tangent-tail rows
`e_G=97..119` for lines and `e_G=103..119` for conics, using the four-private
line-pencil obstruction, the K4 determinant, and three-private root-star
arguments, while reducing the conic four-private rows `e_G=97..102` to the
two-triangle or hexagon-factor residuals.
The exact-current rows are also recorded as a minimal obstruction profile:
any remaining over-budget witness must be one of the line cores `72..80` or
conic cores `69..76`, with exactly six finite source classes, six distinct
finite slopes, and an unpaid projective endpoint, plus the printed saturated
base-root, external-slack, and secant-overlap conditions.
The exact-current residuals now also carry a multi-saving closure ledger:
line cores `72..96` require saving depths `1..5`, while conic cores `69..102`
require depths up to `19`; conic cores `101,102` are governed by the
cofactor-improved projective tangent envelope rather than the pair-overlap
envelope.  This is a row-local closure criterion, not a proof that the listed
savings occur.
Those rows split by first available saving mechanism into line base-active
`72..74`, line external-slack `75..80`, conic base+secant `69..71`, conic
secant-only `72..74`, conic endpoint/duplicate-only `75..76`, and the
punctured-tangent tail `120`, which is now closed by the cofactor-span
obstruction.

The rank-node dichotomy packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/
  f17_32_n512_k256_m3_rank_node_dichotomy.json
```

gives the finite regular/singular gate.  If one tested finite slope has full
column rank, row elimination supplies a nonzero maximal minor.  If all `j+2`
deterministic finite test nodes have rank at most `j`, then every maximal minor
vanishes identically and the bucket is genuinely singular.

The null-polynomial split-locator gate

```text
experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/
  f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json
```

separates ambient regular roots from actual support-wise split locators.  In a
nonsingular bucket, finite canonical roots are exactly ambient null-polynomials
`H(u+zv)ell=0`; a root becomes a split-locator witness only after `ell`
normalizes to a monic degree-`j` divisor of `X^512-1` and satisfies
`H(v)ell != 0`.

The projective split-locator gate

```text
experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/
  f17_32_n512_k256_m3_projective_split_locator_gate.json
```

is the endpoint companion.  The ambient infinity chart is
`H(v)ell=0, H(u)ell!=0`, but an actual support-wise endpoint witness still
requires `ell` to normalize to a monic degree-`j` divisor of `X^512-1`.  Thus
the rank-6 endpoint-sensitive branch must test the split-locator divisor gate
before counting or paying the projective endpoint.

The affine-pivot compression packet

```text
experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/
  f17_32_n512_k256_m3_m4_affine_pivot_compression.json
```

gives the finite-root table route a smaller target.  On a row-set chart with
finite pivot `z0` and `rank H_R(v)<=6`, the original `87..128` dimensional
maximal-minor determinant compresses to a `6 x 6` determinant with the same
finite roots in that affine pivot chart.

The gcd-equivalence companion

```text
experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/
  f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json
```

shows that good pivots are plentiful for nonzero rank-6 minors and that the
v10 canonical gcd root set is preserved after replacing each chart by its
compressed determinant translated back to the global slope variable.

For finite affine roots, the M5 kernel chart gives a per-root filter:

```text
z survives the ambient affine noncontainment test
  iff ker(H(u)+zH(v)) is not contained in ker H(v).
```

If the containment holds, that root contributes nothing to the support-wise
noncontainment numerator.  If containment fails, it contributes at most the
single finite parameter `z` before split-locator, quotient, and extension
audits.

The regular-root rank-drop bridge explains why this filter applies directly to
v10 root tables:

```text
z root of canonical regular gcd
  => rank(H(u)+zH(v)) <= j.
```

In a nonsingular regular bucket the converse also holds for finite field
slopes.  Thus a regular root table is a rank-drop table.  Combining this with
the kernel filter shows that full-direction-rank regular roots always survive
same-support containment and must be handled by root counts plus the remaining
quotient, extension, subfield, or split-locator audits.

The filter also has a rank-stratification corollary: if
`rank H(v) > rank(H(u)+zH(v))`, then containment is impossible and `z` survives
the ambient noncontainment test.  Thus full-direction-rank finite regular roots
cannot be removed by this same-support kernel filter; they need actual root
tables and then quotient/extension/subfield audits.

This is not a worst-case row bound.  It is the current M4 decision table for
regular buckets after composing the proved local certificates.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json

python3 experimental/scripts/verify_m1_hankel_m4_projective_budget_split.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/f17_32_n512_k256_m3_m4_projective_budget_split.json

python3 experimental/scripts/verify_m1_hankel_m4_rank6_ambient_sharpness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json

python3 experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/f17_32_n512_k256_m3_rank6_projective_witness.json

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

python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/f17_32_n512_k256_m3_rank6_boundary_dual_gcd.json

python3 experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/f17_32_n512_k256_m3_rank_node_dichotomy.json

python3 experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json

python3 experimental/scripts/verify_m1_hankel_m3_projective_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/f17_32_n512_k256_m3_projective_split_locator_gate.json

python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_compression.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/f17_32_n512_k256_m3_m4_affine_pivot_compression.json

python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_gcd_equivalence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json

python3 experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json
```
