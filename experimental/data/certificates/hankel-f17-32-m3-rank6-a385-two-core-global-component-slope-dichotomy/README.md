# F17^32 M3 Rank-6 A385 Two-Core Global-Component Slope Dichotomy

Status: PROVED / AUDIT.

This packet refines the fixed two-core global-component residual at `A=385`.
On an irreducible component contained in all direction-consistency conics, the
linear pairs `(N_y,D_y)` induce a well-defined rational slope map off its base
locus.  If that slope map is constant, the non-base branch contributes at most
one finite slope; with the endpoint its projective total is at most `2<=6`.

Conclusion:

```text
fixed two-core constant-slope global-component branch projective total <= 2 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_global_component_slope_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy/f17_32_n512_k256_m3_rank6_a385_two_core_global_component_slope_dichotomy.json
```

Nonclaims:

```text
does not close fixed two-core nonconstant moving-slope components;
does not close fixed two-core slope-free base loci or components;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
