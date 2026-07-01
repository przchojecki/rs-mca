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

The base interpolation map `Q -> L_Q` is injective, so a positive-dimensional
component cannot have `r_G >= 126`; otherwise all `L_Q` would be scalar
multiples of the same degree-126 divisor.

The useful closed subcase is:

```text
line component, r_G <= 48:
  finite slopes <= 5,
  endpoint = 1,
  projective total <= 6.
```

Conic components and line components with large forced core remain named
residuals for a sharper split-locator, paid-ledger, or exact-root-table
argument.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

Nonclaims:

```text
does not prove every moving-slope component is a line;
does not close line components with forced split-root core >=49 in projective accounting;
does not close irreducible conic moving-slope components;
does not rule out another independent noncontained vector at the same finite slope;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
