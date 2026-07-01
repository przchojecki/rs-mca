# F17^32 M3 Rank-6 A386 Component-Cut Safety

Status: PROVED / AUDIT.

This packet refines the common-component residual left by the `A=386`
conic-pair criterion for separated rank-6 boundary buckets.

At `A=386`, the low-degree transfer has `h=3`, so the auxiliary `Q`-space is
`P^2`.  Suppose two direction-consistency conics have a full common component
`G` of degree `c in {1,2}`.  If each irreducible component of `G` is cut by
some direction-consistency conic, then the points on `G` contribute at most
`2c` in total.  The off-component residual intersection has degree at most
`(2-c)^2`.  Hence the finite ambient `Q`-classes are bounded by

```text
2c + (2-c)^2 <= 4.
```

The split-locator gate cannot increase this finite count, and the
endpoint-uniform theorem contributes the single endpoint `[0:1]`.  Therefore
the support-wise projective total under the component-cut criterion is at most

```text
4 + 1 = 5 <= 6.
```

The remaining residual is narrower: an irreducible component contained in all
direction-consistency conics.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_component_cut_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json
```

Nonclaims:

```text
does not prove every A=386 common-component case satisfies the cut criterion;
does not classify the global-component residual;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
