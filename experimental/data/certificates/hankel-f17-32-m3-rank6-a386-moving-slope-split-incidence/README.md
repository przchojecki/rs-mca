# F17^32 M3 Rank-6 A386 Moving-Slope Split Incidence

Status: PROVED / AUDIT.

This packet adds a split-locator incidence budget for the moving-slope
component left by the `A=386` global-component slope dichotomy.

For an irreducible moving-slope component `G` of degree `c in {1,2}` in the
`Q`-plane, let `r_G` be the number of subgroup roots forced for every
interpolated polynomial `L_Q` on `G`.  Since a split locator has degree
`j=126`, Bezout with the remaining root hyperplanes gives

```text
finite Q-classes on G <= floor(c (512-r_G)/(126-r_G)).
```

The packet then sharpens this with the base support.  On the base support `X`,
`L_Q(x)=0` is equivalent to `Q(x)=0`, and nonzero `Q` has degree `<3`, so each
candidate has at most two base roots.  If `e_G` is the number of forced
external roots among `H\\X`, then

```text
finite Q-classes on G <= floor(c (385-e_G)/(124-e_G)).
```

The base interpolation map `Q -> L_Q` is injective, so a positive-dimensional
component cannot have `r_G >= 126`; otherwise all `L_Q` would be scalar
multiples of the same degree-126 divisor.

The useful closed subcase is:

```text
line component, e_G <= 71:
  finite slopes <= 5,
  endpoint = 1,
  projective total <= 6.
```

For irreducible conics, a pair-overlap packing step gives the missing saving:
two distinct `Q`-classes can share at most one non-forced external root line.
Therefore six conic `Q`-classes are impossible for `e_G<=68`, and conic
components are projective-safe in that range.  Line components with `e_G>=72`
and conic components with `e_G>=69` remain residual for a sharper
split-locator, paid-ledger, or exact-root-table argument.

The residual is still reduced exactly.  If `E` is the forced external
split-root core and `C_E=prod_{s in E}(X-s)`, then every locator in the
component factors as

```text
L_Q = C_E R_Q.
```

The remaining split-locator gate is the quotient condition

```text
R_Q | (X^512-1)/C_E
```

plus normalization, exact degree, and noncontainment filters.  Thus residual
lines reduce to quotient degree at most `54`, and residual conics reduce to
quotient degree at most `57`.

After puncturing away the forced core, these same residuals are in the
very-high-agreement tangent range of the punctured row:

```text
line threshold e=72:  n'=440, r'=54 <= floor((440-256)/3), tangent numerator 55
conic threshold e=69: n'=443, r'=57 <= floor((443-256)/3), tangent numerator 58
```

This records tangent-ledger eligibility on the punctured row.  It is not a
claim that the original-row projective numerator is within budget.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

Nonclaims:

```text
does not prove every moving-slope component is covered by the separated line/conic positive-dimensional branch;
line quotient-pencil and conic Pascal/four-private diagnostics are not used as the closure mechanism, because the product collapses supersede them;
does not claim the high-core quotient diagnostic problems are empty or paid;
does not claim the punctured tangent numerator at the residual threshold is within the original row budget;
does not prove existence or nonexistence of another independent noncontained vector at the same finite slope; such a parameter is charged through the non-slope-free branch and the slope-free shadow adds no extra count;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
