# MCA full-lift residue-zero direction router v1

## Status

PROVED / EXACT FINITE CALIBRATION / STRUCTURAL ROUTER.

## Statement

Let `D` be the exact deficit-`H` boundary layer on direction support `E`,
`|E|=e`, and put `c=K-1` and `A=2H-e`. Assume

```text
A>0, A^2>e*c, N-e>m-H>c.
```

Fixing an anchor in `D`, every other member determines a nonzero normalized
codeword direction agreeing with the gauged direction on at least `A`
coordinates. Distinct directions have intrinsic agreement sets meeting in
at most `c` coordinates. Hence the number of direction classes is at most

```text
J=floor(e(A-c)/(A^2-e*c)).
```

Every class together with the anchor is one affine codeword line. Its
outside common core is contained in the zero set of a nonzero degree-`<K`
codeword, so outside-core packing gives

```text
Q=floor((N-e-c)/(m-H-c)),
|D|<=1+J(Q-1).
```

If `P_(H-1)` is the independently truncated prefix and `T` is the
synchronized top union, then

```text
|Z|<=P_(H-1)+1+J(Q-1)+|T|.
```

## Official endpoint

At Mersenne-31 `e=98232`,

```text
(s,H,A)       = (32742,65489,32746),
J             = 3,
Q             = 484,
|D|           <= 1450,
P_(H-1)       = 16432695,
prefix + D    = 16434145.
```

An unsafe family therefore needs `|T|>=343071`. If `g` is the top line's
total common core, line packing

```text
|T|(m-g)<=N-g
```

forces `g>=67452=m-2`.

## Nonclaims

This does not prove safety or unsafety at `e=98232`. The Mersenne residual
interval remains `98232<=e<=1044241`. The next task is the exact
classification of affine lines whose members have only one or two private
agreement coordinates beyond the total common core.

## Replay

```bash
python3 experimental/verify_mca_full_lift_residue_zero_direction_router_v1.py
python3 -O experimental/verify_mca_full_lift_residue_zero_direction_router_v1.py
python3 experimental/audit_mca_full_lift_residue_zero_direction_router_v1.py
```
