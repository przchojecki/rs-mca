# F17^32 M3 Rank-6 A385 Two-Core Slope-Free Empty

Status: PROVED / AUDIT.

This packet closes the fixed two-core slope-free residual at `A=385`.  After
factoring the two forced base roots, `Q=E R` with `deg R<3`.  Slope-free would
force all six direction numerators

```text
N_y(R)=Omega_y E(y) R(y)
```

to vanish.  Since the six direction nodes are distinct and disjoint from the
fixed base core, this forces the nonzero residual polynomial `R` to have six
roots, impossible for degree `<3`.

Conclusion:

```text
fixed two-core slope-free base locus/global component is empty.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_slope_free_empty.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-slope-free-empty/f17_32_n512_k256_m3_rank6_a385_two_core_slope_free_empty.json
```

Nonclaims:

```text
does not close fixed two-core nonconstant moving-slope components;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
