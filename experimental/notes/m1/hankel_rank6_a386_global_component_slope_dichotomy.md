# Hankel Rank-6 A386 Global-Component Slope Dichotomy

Status: PROVED / AUDIT.

This note records the next refinement of the separated rank-6 boundary at

```text
A = 386.
```

It consumes the component-cut packet.  After that packet, the remaining
positive-dimensional `Q`-plane residual is an irreducible component contained
in all pairwise direction-consistency conics.  This note splits that residual
into a safe constant-slope off-base-locus case and two named residual cases.

At `A=386`, the boundary low-degree transfer gives

```text
h = 3,        [Q] in P^2.
```

For each of the six direction nodes `y`, put

```text
N_y(Q) = Omega_y Q(y),
D_y(Q) = b_y L_Q(y).
```

Both are linear forms in `Q`: evaluation of `Q` is linear, and `L_Q` is the
linear interpolation output from the base support.  A finite root must satisfy

```text
z D_y(Q) = N_y(Q)
```

for every direction node.  Equivalently, before zero-denominator checks, the
six projective pairs `[N_y(Q):D_y(Q)]` must agree.  The pairwise consistency
conics are

```text
C_{y,y'}(Q) = N_y(Q)D_{y'}(Q) - N_{y'}(Q)D_y(Q).
```

Let `G` be an irreducible component of `P^2` contained in all these pairwise
conics.

If some pair `(N_y,D_y)` is not identically zero on `G`, then

```text
zeta_G = [N_y:D_y] : G --> P^1
```

is a rational projective slope map.  The pairwise conics make this map
independent of the chosen `y` on common domains of definition: whenever two
pairs are both defined, their cross product is zero on `G`.

Every finite root represented by a `Q`-class on the domain of definition of
`zeta_G` has finite slope

```text
z = N_y(Q) / D_y(Q)
```

for this induced map, before the null-polynomial split-locator gate possibly
removes it.

Therefore, if `zeta_G` is constant, the non-base part of the component
contributes at most one finite slope.  The endpoint-uniform theorem contributes
one projective endpoint `[0:1]`, so the projective contribution of this
non-base branch is at most

```text
1 + 1 = 2 <= 6.
```

The base locus of `zeta_G`, where all six pairs `(N_y,D_y)` vanish at the same
`Q`-class, is not closed by this argument.  It remains a slope-free residual
unless the split-locator gate removes it or a paid ledger identifies it.

The companion note

```text
experimental/notes/m1/hankel_rank6_a386_slope_free_containment.md
```

applies the existing finite-affine and projective noncontainment gates to that
slope-free locus.  The displayed slope-free transfer vectors satisfy
`H(v)L_Q=H(u)L_Q=0`, so they contribute no finite noncontained slope and no
projective endpoint witness.  A different independent noncontained vector at
the same finite parameter is charged once through the non-slope-free branch;
the slope-free vector is a contained shadow and adds no second support-wise
parameter.

The split-incidence companion

```text
experimental/notes/m1/hankel_rank6_a386_moving_slope_split_incidence.md
```

applies the split-locator divisor gate to the moving-slope component.  It
proves the incidence budget

```text
finite Q-classes on G <= floor(c(512-r_G)/(126-r_G)),
```

where `c` is the component degree and `r_G` is the forced split-root core.
Using the base-support fact that nonzero `Q` has at most two roots on `X`, it
sharpens the useful bound to

```text
finite Q-classes on G <= floor(c(385-e_G)/(124-e_G)),
```

where `e_G` is the forced external split-root core.  This closes line
components with `e_G<=71` in projective accounting and leaves large-external-
core lines and irreducible conics for the forced-core analysis.

For irreducible conics, the same companion adds a pair-overlap packing step:
two distinct `Q`-classes can share at most one non-forced external root line.
This closes conic components with `e_G<=68` in projective accounting, leaving
only large-external-core conics as residual.

The high-external-core branch is then put in quotient normal form: after
factoring the forced external core `C_E`, the remaining split-locator gate is a
quotient divisor condition.  A line is a dual-evaluation-fiber quotient pencil
of degree at most `54`; an irreducible conic has a global common forced core
across the whole `Q`-plane and becomes a quotient family of degree at most
`57`.

The companion packet now closes both high-core branches by product collapse.
For a line component, two distinct forced external roots force either a
common-root pencil with `L_{(T-alpha)S}=F*S`, `deg F<=125`, and at most one
base root for `F`, or a product branch `L_Q=R*Q` with `R` nonzero on the base
support.  Hence a degree-`126` split locator would require at least `124`
external forced roots, closing the pre-tangent line range `72<=e_G<=120`.  For
an irreducible conic, the global forced core makes the base interpolant's top
two coefficients vanish, so `L_Q=RQ`, and `e_G<=123` cannot supply a
degree-`126` split locator.  The projective tangent staircase closes the
remaining very-high-core tail `e_G>=121`.  Thus no separated
positive-dimensional line or irreducible-conic moving-slope component remains
live after these product collapses.

The packet still records the older quotient and incidence rows as diagnostics.
Before the product collapses, the projective proof envelope was only one over
budget for line cores `72<=e_G<=80` and `e_G=120`, and for conic cores
`69<=e_G<=76` and `e_G=120`; the worst diagnostic projective upper bounds in
the middle were `18` and `26`, respectively.  The endpoint-only finite-incidence
subranges have explicit saturation targets: line six-class saturation has
external slack `1..41`, and conic six-class saturation needs `0..14` forced
pair-overlap events before external excess.  A pre-collapse over-budget
diagnostic witness also had to have six distinct finite slopes and an unpaid
endpoint; the sharpest pressure cases were line `e_G=72` near-complete base
splitting and conic `e_G=69` almost-complete secants.  The line `e_G=72` case
closed unless all six classes had a base root and at least five had two; the
conic `e_G=69` case closed unless at least `14` of `15` pair secants occurred,
forcing at least `16` secant triangles.  Equivalently, line
`e_G=72` survival has base-root histogram `(0,0,6)` or `(0,1,5)`, and conic
`e_G=69` survival has secant graph `K6` or `K6` minus one edge.
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
Across the full endpoint-only one-over range, the line histogram counts are
`2,16,27,28^6` for `e_G=72..80`, and the conic counts are `2,16,27,28^5`
for `e_G=69..76`.
The packet also records a single-saving closure ledger for all `19` one-over
moving-slope residual rows: line `e_G=72..80`, conic `e_G=69..76`, and the
line/conic punctured-tangent tail at `e_G=120`.
Those rows split by first available saving mechanism into line base-active
`72..74`, line external-slack `75..80`, conic base+secant `69..71`, conic
secant-only `72..74`, conic endpoint/duplicate-only `75..76`, and the
punctured-tangent tail `120`.

The other cases remain residual:

```text
determined nonconstant slope map:
  zeta_G is nonconstant, so Bezout root counting has been replaced by a
  moving one-dimensional slope image.  This must be cut by the split-locator
  divisor gate or identified as quotient/tangent/extension structure.

slope-free component:
  every pair (N_y,D_y) vanishes at a base point, or identically on G.  Then
  the finite consistency equations impose no slope there before further
  Hankel/split analysis.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_global_component_slope_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json
```

Nonclaims:

```text
no proof that all global components have constant slope;
no closure of moving-slope global components;
no closure of slope-free base points or global components;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
