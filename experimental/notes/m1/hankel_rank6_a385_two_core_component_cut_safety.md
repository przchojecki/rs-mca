# Hankel Rank-6 A385 Two-Core Component-Cut Safety

Status: PROVED / AUDIT.

This note refines the fixed two-core residual left by

```text
experimental/notes/m1/hankel_rank6_a385_two_core_conic_pair_safety.md
```

It applies to the separated rank-6 boundary at

```text
A = 385.
```

After a fixed forced two-point base core is factored, the boundary transfer has

```text
Q = E R,       deg R < 3,
```

so the residual `Q`-space is a projective plane.  The conic-pair packet closes
the no-common-component case.  This packet handles the next case, where two
direction-consistency conics have a full common component `G`.

Let `G` have total degree

```text
c in {1,2}.
```

Write the irreducible components of `G` as `G_i`, with degrees `c_i`.  If each
`G_i` is cut by some direction-consistency conic, meaning that conic does not
contain `G_i`, then the compatible points on `G_i` have length at most

```text
2 c_i
```

by Bezout.  Summing over components gives at most `2c` points on `G`.

Away from the full common component `G`, the two original conics leave coprime
residual curves of degree `2-c`, so the off-component contribution has length
at most

```text
(2-c)^2.
```

Thus the finite `Q`-classes are bounded by

```text
2c + (2-c)^2.
```

For `c=1` this is `3`; for `c=2` this is `4`.  The split-locator gate cannot
increase the finite ambient count, and each compatible non-slope-free
`Q`-class determines at most one finite slope.  Adding the single projective
endpoint gives

```text
support-wise projective contribution <= 5 <= 6.
```

The remaining fixed two-core residual is no longer an arbitrary common
component.  It is a global-component branch: an irreducible component of the
residual `Q`-plane is contained in all direction-consistency conics.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_component_cut_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-component-cut-safety/f17_32_n512_k256_m3_rank6_a385_two_core_component_cut_safety.json
```

Nonclaims:

```text
no proof that every fixed two-core common-component branch satisfies the cut criterion;
no closure of the fixed two-core global-component residual;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
