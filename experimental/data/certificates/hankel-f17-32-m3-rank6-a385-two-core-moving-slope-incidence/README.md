# F17^32 M3 Rank-6 A385 Two-Core Moving-Slope Incidence

Status: PROVED / AUDIT.

This packet records the fixed two-core moving-slope incidence budget at
`A=385`.  With `Q=E R` and `deg R<3`, a valid degree-`127` split locator has at
most four base-support roots: the two fixed core roots plus at most two roots
of `R`.  Thus a component with external forced core `e_G` needs at least
`123-e_G` non-forced external roots.

Conclusion:

```text
line components:               e_G <= 70 projective-safe;
irreducible conic components:  e_G <= 67 projective-safe by pair-overlap.
```

This is an incidence packet, not a high-core closure.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_moving_slope_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-moving-slope-incidence/f17_32_n512_k256_m3_rank6_a385_two_core_moving_slope_incidence.json
```

Nonclaims:

```text
does not close the full fixed two-core nonconstant moving-slope branch;
does not prove product collapse for A=385 high-core line or conic components;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
