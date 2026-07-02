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
`<=5<=6`.  The common-component case is the named residual.

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
gates.  The remaining unclosed branch is the nonconstant moving-slope case, or
another independent noncontained vector at a slope that also has a slope-free
contained vector.

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
Large-external-core lines and conics remain residual, but the packet factors
their forced external core more precisely: a high-core line is a
dual-evaluation-fiber quotient pencil of degree at most `54`, while a high-core
irreducible conic has a global common forced core across the whole `Q`-plane
and becomes a quotient family of degree at most `57`.  It also records that,
after puncturing the forced core, those quotient branches are inside the
very-high-agreement tangent range of the punctured row.  The projective
tangent staircase closes the tail `e_G>=121`, so the remaining unclosed ranges
are `72<=e_G<=120` for lines and `69<=e_G<=120` for irreducible conics.
Within those ranges the current projective proof envelope is only one over
budget for line cores `72<=e_G<=80` and `e_G=120`, and for conic cores
`69<=e_G<=76` and `e_G=120`; the worst current projective upper bounds in the
middle are `18` for lines and `26` for conics.  The endpoint-only
finite-incidence subranges now have explicit saturation targets: line
six-class saturation has external slack `1..41`, and conic six-class
saturation needs `0..14` forced pair-overlap events before external excess.  A
genuine over-budget witness must also have six distinct finite slopes and an
unpaid endpoint; the strongest remaining pressure cases are line `e_G=72`
near-complete base splitting and conic `e_G=69` almost-complete secants.  The
line `e_G=72` case closes unless all six classes have a base root and at least
five have two; the conic `e_G=69` case closes unless at least `14` of `15`
pair secants occur, forcing at least `16` secant triangles.  Equivalently, line
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

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_low_degree_transfer.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json
```

Nonclaims:

```text
no solution of the Q-consistency equations for arbitrary weights;
no overlapping-support rank-6 classification;
no endpoint payment theorem;
no row-level M3 safe-side bound.
```
