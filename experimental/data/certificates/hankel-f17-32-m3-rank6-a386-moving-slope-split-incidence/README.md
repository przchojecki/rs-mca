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

Conic components are finite-safe for `e_G<=19` but remain one endpoint over the
projective budget under this incidence bound.  Line components with
`e_G>=72` also remain residual for a sharper split-locator, paid-ledger, or
exact-root-table argument.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

Nonclaims:

```text
does not prove every moving-slope component is a line;
does not close line components with forced external split-root core >=72 in projective accounting;
does not close irreducible conic moving-slope components;
does not rule out another independent noncontained vector at the same finite slope;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
