# Hankel Rank-6 A386 Moving-Slope Split Incidence

Status: PROVED / AUDIT.

This note records a split-locator incidence budget for the remaining
moving-slope part of the separated rank-6 boundary at

```text
A = 386.
```

It consumes the global-component slope dichotomy and the slope-free containment
filter.  It does not close every moving-slope component.

At `A=386`, the low-degree transfer gives

```text
j = 126,       h = 3,       [Q] in P^2.
```

For a moving-slope residual component `G` in the `Q`-plane, write

```text
L_Q
```

for the interpolated degree-`<127` kernel polynomial.  For each subgroup point
`s in H`, define the root hyperplane

```text
E_s = { Q : L_Q(s) = 0 }.
```

The split-locator gate requires `L_Q` to normalize to a monic degree-`126`
divisor of `X^512-1`.  Thus a valid `Q` must lie on root hyperplanes for at
least `126` subgroup points.

Let `G` be an irreducible positive-dimensional component of degree

```text
c in {1,2}.
```

Let `r_G` be the forced split-root core: the number of subgroup points `s` for
which

```text
G subset E_s.
```

The base interpolation map `Q -> L_Q` is injective.  Indeed, if `L_Q=0`, then
`Q` vanishes on the base support `X`, which has size `127`; since `deg Q<3`,
this forces `Q=0`.  Consequently a positive-dimensional component cannot have
`r_G >= 126`: all `L_Q` would then be scalar multiples of the same degree-126
divisor, contradicting projective injectivity.

For `r_G < 126`, each valid split locator on `G` needs at least

```text
126 - r_G
```

additional intersections with the non-forced root hyperplanes.  Every
non-forced root hyperplane cuts `G` in length at most `c` by Bezout.  Therefore
the number of valid `Q`-classes on `G`, and hence the number of finite slopes
represented by this component, is at most

```text
floor( c (512-r_G) / (126-r_G) ).
```

This gives a projective-safe line criterion:

```text
c = 1 and r_G <= 48
  => finite slopes <= 5,
     endpoint contribution = 1,
     total projective contribution <= 6.
```

The finite-only line criterion is slightly weaker:

```text
c = 1 and r_G <= 61
  => finite slopes <= 6.
```

For an irreducible conic component (`c=2`), the same incidence budget is not
strong enough: even at `r_G=0` it gives `floor(1024/126)=8` finite `Q`-classes.
Those components remain residual unless a sharper split-locator, paid-ledger,
or exact-root-table argument cuts them further.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

Nonclaims:

```text
no proof that every moving-slope component is a line;
no closure of line components with forced split-root core >=49 in projective accounting;
no closure of irreducible conic moving-slope components;
no exclusion of another independent noncontained vector at the same finite slope;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
