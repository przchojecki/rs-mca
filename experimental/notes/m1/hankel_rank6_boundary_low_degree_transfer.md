# Hankel Rank-6 Boundary Low-Degree Transfer

Status: PROVED / AUDIT.

This note records the exact finite-root reduction for separated rank-6
supports at the boundary agreements

```text
A = 385, 386, 387.
```

It is the general version of the barycentric boundary calculation: arbitrary
nonzero weights reduce to a low-degree auxiliary polynomial and six consistency
equations.

Work with

```text
j = 512-A,       t = A-256,       m = j+1,
|X| = m,         |Y| = 6,         S = X union Y.
```

Let `a_x` and `b_y` be arbitrary nonzero weights.  Set

```text
h = |S|-t.
```

For the three boundary agreements,

```text
h = 5, 3, 1.
```

Let

```text
Omega_s = 1 / prod_{r in S, r != s} (s-r)
```

be the barycentric residues of the combined support.  The nullspace of the
first `t` Vandermonde rows on `S` is

```text
{ Omega_s Q(s) : deg Q < h }.
```

Thus a finite root `z` with ambient kernel polynomial `L` of degree `<m`
exists iff there is a nonzero `Q` with `deg Q<h` such that

```text
a_x L(x)       = Omega_x Q(x)        for x in X,
z b_y L(y)     = Omega_y Q(y)        for y in Y.
```

For fixed `Q`, the first set of equations determines a unique polynomial
`L_Q` of degree `<m`, because `|X|=m` and all `a_x` are nonzero.  The finite
root condition is therefore exactly the six direction-node consistency
equations

```text
z b_y L_Q(y) = Omega_y Q(y)          for y in Y.
```

Equivalently, all defined ratios

```text
Omega_y Q(y) / (b_y L_Q(y))
```

are equal, and any zero denominator has zero numerator.  This reduces the
boundary finite-root problem to projective `Q`-spaces of dimensions

```text
4, 2, 0
```

for `A=385,386,387`, respectively.  Any resulting `L_Q` still has to pass the
null-polynomial split-locator gate: it must normalize to a monic degree-`j`
divisor of `X^512-1`.

The barycentric exact-root packet is the special case `a_s=b_s=Omega_s`.  In
that case the consistency equations force the ambient root table `{1}`, and
the split-locator filter removes that root from finite support-wise counting.

At `A=385`, the first fixed-core closure companion is

```text
experimental/notes/m1/hankel_rank6_a385_base_core_closure.md
```

If all candidates in a separated branch share a forced base-root core of size
at least four, then `Q` vanishes at four distinct base nodes.  Since
`deg Q<5`, this leaves one projective `Q`-class, hence at most one finite
noncontained slope.  Adding the endpoint gives projective total `<=2<=6`.
Thus any over-budget separated `A=385` obstruction must avoid a common
four-point base core in the counted branch.

The next fixed-core companion is

```text
experimental/notes/m1/hankel_rank6_a385_three_core_quadratic_cut.md
```

After a fixed three-point base core is factored, the residual `Q`-space is a
projective line.  If at least one pairwise direction-consistency equation is a
nonzero binary quadratic on that line, it cuts the finite search to at most two
projective `Q`-classes.  With one slope per compatible non-slope-free class
and the endpoint added, the branch has projective total `<=3<=6`.  The
remaining fixed-three-core residual is exactly the ratio-identically-consistent
`Q`-line where all pairwise consistency quadratics vanish identically.
The fixed three-core residual closure companion closes that line: incidence is
projective-safe for `e_G<=70`, one global forced external root gives product
collapse `L_{E R}=H R` and excludes `71<=e_G<=122`, and the punctured tangent
tail is projective-safe for `e_G>=122`.

The fixed two-core companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_conic_pair_safety.md
```

After a fixed two-point base core is factored, the residual `Q`-space is a
projective plane.  If two direction-consistency conics on that plane have no
common component, Bezout gives at most four compatible `Q`-classes.  With one
slope per compatible non-slope-free class and the endpoint added, the branch
has projective total `<=5<=6`.  The remaining fixed-two-core residual is the
common-component branch on the residual `Q`-plane.

The fixed two-core component-cut companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_component_cut_safety.md
```

It refines that common-component branch: if every irreducible component of the
common component is cut by some direction-consistency conic, the component and
off-component Bezout bound gives at most four finite `Q`-classes, hence
projective total `<=5<=6` after adding the endpoint.  The remaining fixed
two-core residual is an irreducible global component contained in all
direction-consistency conics.

The fixed two-core global-component companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_global_component_slope_dichotomy.md
```

It splits that global component by its induced slope map.  The constant-slope
off-base-locus branch contributes at most one finite slope, hence total
projective contribution `<=2<=6` after adding the endpoint.  The remaining
fixed two-core global-component residuals are a determined nonconstant slope
map and a slope-free base locus or component.

The fixed two-core slope-free companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_slope_free_empty.md
```

It closes the slope-free residual.  In the fixed two-core branch, write
`Q=E R` with `deg R<3`; slope-free forces the six direction numerators
`N_y(R)=Omega_y E(y)R(y)` to vanish.  Since the direction nodes are distinct
and disjoint from the fixed base core, a nonzero `R` would have six roots,
impossible for degree `<3`.  Thus the fixed two-core slope-free base locus or
global component is empty.

The fixed two-core moving-slope incidence companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_moving_slope_incidence.md
```

It gives the first split-locator incidence budget for the remaining
nonconstant moving-slope branch.  A degree-`127` split locator has at most four
base roots in this fixed two-core branch, so it needs at least `123-e_G`
non-forced external roots.  Line components are projective-safe for
`e_G<=70`; irreducible conics are projective-safe for `e_G<=67` after the
pair-overlap saving.  High-core line/conic branches remain residual.

The fixed two-core high-core quotient companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_high_core_quotient.md
```

It puts those residual high-core branches in quotient normal form.  The line
branch is a quotient pencil of degree at most `127-71=56`.  For an irreducible
conic, containment in a root hyperplane forces the external root functional to
vanish on the whole residual plane, so the branch is a quotient family of
degree at most `127-68=59`.  At this quotient-normal-form stage, the quotient
branches remain unclosed.

The fixed two-core conic product-collapse companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_conic_product_collapse.md
```

It closes most of the irreducible-conic high-core quotient branch.  If the
global forced external core has size `e_G`, comparison of the remainders of
`G`, `T G`, and `T^2 G` modulo `P_X` forces the top two coefficients of the
common factor `H` to vanish, so `L_{E R}=H R` with `deg H<=125`.  Thus
`e_G<=122` cannot pass the degree-`127` split-locator gate, while `e_G>=124`
is impossible.  The remaining irreducible-conic high-core tail from this
packet is exactly `e_G=123`.

The fixed two-core high-core closure companion is

```text
experimental/notes/m1/hankel_rank6_a385_two_core_high_core_closure.md
```

It closes the separated fixed two-core high-core line/conic residual.  On line
components, two forced external roots imply either a common-root pencil or
product without modular reduction; in both cases a degree-`127` split locator
needs `e_G>=123`, closing line cores `71<=e_G<=122`.  After puncturing a forced
external core, the projective tangent bound is `128-e_G`, so the tail
`e_G>=122` is projective-budget safe.  Together with incidence, this covers
the line range `e_G>=71` and the conic range `e_G>=68`.

The fixed-core synthesis companion is

```text
experimental/notes/m1/hankel_rank6_a385_fixed_core_synthesis.md
```

It composes the fixed four-core, fixed three-core, fixed three-core residual,
and fixed two-core packet tree.  The result is that every separated `A=385`
rank-6 branch with a fixed forced base split-root core of size at least two is
projective-budget safe.  Thus any remaining separated `A=385` over-budget
obstruction must avoid a fixed forced two-point base core in the counted
branch; the remaining frontier is moving-core/no-common-core behavior,
overlapping support, and row-level M3 synthesis.

The no-fixed-core pressure companion is

```text
experimental/notes/m1/hankel_rank6_a385_no_fixed_core_pressure.md
```

It turns that remaining separated frontier into a large pair-core target.  A
projective over-budget survivor must have six finite classes plus an unpaid
endpoint.  Since `deg Q<5`, each finite class has at most four base roots, so
the six degree-`127` split locators have at least `738` external-root
incidences in the `384` external subgroup points.  Hence total pairwise
external overlap is at least `354`, and some pair of finite classes shares at
least `24` external roots.

The pair-core quotient-reduction companion is

```text
experimental/notes/m1/hankel_rank6_a385_pair_core_quotient_reduction.md
```

It uses linearity of the low-degree transfer to show that the forced pair spans
a projective `Q`-line on which every locator factors through the common
external core: `L_Q=C_E R_Q`.  At the guaranteed core size, the ambient quotient
family has vector dimension at most `104`, and the two split quotient members
have degree at most `103`.

The pair-core rank-test companion is

```text
experimental/notes/m1/hankel_rank6_a385_pair_core_rank_test.md
```

It states the same target as a linear-algebra gate.  For a common external core
`E`, the matrix with rows `ev_s(Q)=L_Q(s)` has five columns, and a two-class
pair line forces `rank M_E<=3`.  Thus a pressure-forced survivor needs a
`24 x 5` external-evaluation matrix with all `4 x 4` minors vanishing.
The Cauchy-moment companion then writes those rows explicitly as
`P_X(s) sum_x W_x x^r/((s-x)P_X'(x))`, or after removing nonzero row factors,
as the weighted Cauchy-moment matrix
`C_{E,X} diag(W_x/P_X'(x)) V_X`.

At `A=387`, this transfer already closes the separated branch for arbitrary
nonzero weights: `h=1`, so the projective `Q`-space is a point and there is at
most one finite slope.  The companion note

```text
experimental/notes/m1/hankel_rank6_a387_separated_boundary_safety.md
```

records the resulting projective bound `1 finite + 1 endpoint <= 2`.

At `A=386`, the transfer leaves a projective plane of `Q` classes.  The
companion conic-pair criterion

```text
experimental/notes/m1/hankel_rank6_a386_conic_pair_safety.md
```

shows that if two direction-consistency conics have no common component, then
Bezout bounds the finite root count by `4`, and the endpoint gives total
`<=5<=6`.  The common-component case is the next intermediate residual in the
branch tree.

The next companion

```text
experimental/notes/m1/hankel_rank6_a386_component_cut_safety.md
```

refines that residual: if each irreducible component of a common component of
degree `1` or `2` is cut by some direction-consistency conic, the component
plus off-component Bezout bound gives at most four finite `Q`-classes and
again total projective contribution `<=5<=6`.  The remaining residual is an
irreducible component contained in all direction-consistency conics.

The global-component slope-map companion

```text
experimental/notes/m1/hankel_rank6_a386_global_component_slope_dichotomy.md
```

then proves the constant-slope non-base subcase projective-safe with total
`<=2<=6`.  The residuals after that are a determined nonconstant slope map and
a slope-free base locus or component.

The slope-free containment companion

```text
experimental/notes/m1/hankel_rank6_a386_slope_free_containment.md
```

then filters the displayed slope-free transfer vectors: they lie in both
`ker H(v)` and `ker H(u)`, so they fail finite and projective noncontainment
gates.  If a slope with a slope-free contained vector also has an independent
noncontained vector, that finite parameter is charged once through the
non-slope-free branch; the slope-free vector adds no second count.  The
remaining branch is therefore the nonconstant moving-slope case.

The moving-slope split-incidence companion

```text
experimental/notes/m1/hankel_rank6_a386_moving_slope_split_incidence.md
```

then applies the split-locator divisor gate to the moving component.  If an
irreducible component `G` has degree `c` and forced split-root core `r_G`, its
finite split-locator source classes are bounded by

```text
floor(c(512-r_G)/(126-r_G)).
```

Using the additional base-support fact that `Q` has at most two roots on `X`,
the packet sharpens this to

```text
floor(c(385-e_G)/(124-e_G))
```

for forced external split-root core `e_G`.  In particular, a line component
with `e_G<=71` is projective-safe after adding the endpoint.  For irreducible
conics, pair-overlap packing closes the projective accounting for `e_G<=68`.
The high-core line branch first appears as a dual-evaluation-fiber quotient
pencil of degree at most `54`, but two distinct forced external roots force a
product collapse: either the component is a common-root pencil with
`L_{(T-alpha)S}=F*S`, `deg F<=125`, and at most one base root for `F`, or
modular reduction vanishes as `L_Q=R*Q` with `R` nonzero on the base support.
Hence any degree-`126` split locator on the high-core line branch would require
at least `124` external forced roots, closing the pre-tangent line range
`72<=e_G<=120`.

The high-core irreducible-conic branch has a global common forced core across
the whole `Q`-plane, and this collapses further: the base interpolant has its
top two coefficients zero, so `L_Q=RQ`; hence `e_G<=123` cannot supply a
degree-`126` split locator.  Together with the punctured tangent tail
`e_G>=121`, this closes both line and irreducible-conic moving-slope components
for every external core size in the separated positive-dimensional branch.

The line quotient-pencil rows and the conic incidence, Pascal, and
quotient-conic ledgers remain in the packet as pre-collapse diagnostics showing
why incidence counting alone was insufficient.

The separated-boundary closure companion

```text
experimental/notes/m1/hankel_rank6_a386_separated_boundary_closure.md
```

packages the full `A=386` separated branch: no-common-component conic pairs,
component-cut common components, constant-slope global components, slope-free
contained shadows, and nonconstant moving-slope line/conic components.  The
result is projective-budget safety for arbitrary nonzero separated weights at
`A=386`.  The remaining nonclaims are `A=385`, overlapping support, endpoint
payment, and row-level M3 closure.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_low_degree_transfer.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_base_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-base-core-closure/f17_32_n512_k256_m3_rank6_a385_base_core_closure.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_quadratic_cut.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_residual_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-residual-closure/f17_32_n512_k256_m3_rank6_a385_three_core_residual_closure.json

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

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_high_core_quotient.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-high-core-quotient/f17_32_n512_k256_m3_rank6_a385_two_core_high_core_quotient.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_conic_product_collapse.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-product-collapse/f17_32_n512_k256_m3_rank6_a385_two_core_conic_product_collapse.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_high_core_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-high-core-closure/f17_32_n512_k256_m3_rank6_a385_two_core_high_core_closure.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_fixed_core_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-fixed-core-synthesis/f17_32_n512_k256_m3_rank6_a385_fixed_core_synthesis.json

python3 experimental/scripts/verify_f17_32_m3_rank6_a385_no_fixed_core_pressure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-no-fixed-core-pressure/f17_32_n512_k256_m3_rank6_a385_no_fixed_core_pressure.json
```

Nonclaims:

```text
no solution of the Q-consistency equations for arbitrary weights;
no overlapping-support rank-6 classification;
no endpoint payment theorem;
no row-level M3 safe-side bound.
```
