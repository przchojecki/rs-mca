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
```

Nonclaims:

```text
no solution of the Q-consistency equations for arbitrary weights;
no overlapping-support rank-6 classification;
no endpoint payment theorem;
no row-level M3 safe-side bound.
```
