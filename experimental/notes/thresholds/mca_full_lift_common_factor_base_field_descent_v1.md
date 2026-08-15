# Full-lift common-factor base-field descent

## Scope

This packet descends the degree-`2..43` geometric factor branch to
components defined over the deployed coefficient field.  It does not
classify those components.

## Conjugate intersection

The deployed row has

```text
F=F_(p^4),       p=2^31-1>43.
```

Factor `rad(P)=product_i R_i` geometrically, with component degrees
`delta_i` summing to at most `d`.  The characteristic guard excludes a
nontrivial purely inseparable component field of definition in degree at
most 43.

If `R_i` is not defined over `F(X)`, it has a distinct conjugate.
Every `F(X)`-rational polynomial pair on `R_i` also lies on that
conjugate, so Bezout permits at most `delta_i^2` such pairs.  Across all
non-base-field components the loss is at most

```text
sum_i delta_i^2<=d^2.
```

## Retained mass

For every `2<=d<=43`,

```text
base-field pairs
 >= 7583-(52-d)^2-d^2
 >= 5079.
```

At most `d` components share this mass, and the exact minimum of the
largest-component pigeonhole is 132.  Applying core incidence to the full
base-field component union gives

```text
factor points >=126263,
inside exceptions <=3974.
```

The 126,263-point conclusion belongs to the union, not to the one
132-section component.  Reducible unions remain allowed.

## Replay

```bash
python3 experimental/verify_mca_full_lift_common_factor_base_field_descent_v1.py
python3 experimental/audit_mca_full_lift_common_factor_base_field_descent_v1.py
```
