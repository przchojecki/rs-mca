# F17^32 M3 Rank-6 A385 Two-Core Component-Cut Safety

Status: PROVED / AUDIT.

This packet refines the fixed two-core common-component residual at `A=385`.
After factoring the two-point base core, the residual `Q`-space is a projective
plane.  If two direction-consistency conics have a common component `G` and
`G` is their full common component, and each irreducible component of `G` is
cut by some direction-consistency conic, then Bezout bounds the finite
`Q`-classes by at most `4`; with the endpoint the projective total is at most
`5<=6`.

Conclusion:

```text
fixed two-core component-cut branch projective total <= 5 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_component_cut_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-component-cut-safety/f17_32_n512_k256_m3_rank6_a385_two_core_component_cut_safety.json
```

Nonclaims:

```text
does not close the fixed two-core global-component residual;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
