# M1 Residual-Depth Frontier Shift

**Status:** PROVED / AUDIT.

This note isolates the residual-depth hierarchy behind the low-slack M1 packet
templates. It explains why the slack-two depth-two conic and the slack-three
first-superboundary conic are the same object.

## General Shift

Fix slack `T`, residual depth `d>=1`, and a multiplicative subgroup
`D subset F_p^*`. A normalized residual packet of size `T+d` is written

```text
P = {1,u_1,...,u_(T+d-1)}.
```

The depth-`d` catalog is cut out by

```text
e_1(P)=...=e_(T-1)(P)=0.
```

Its first slope coefficient is

```text
c_{T,d}(P)=(-1)^T e_T(P).
```

If `d>=2`, then the zero-slope subcatalog satisfies

```text
c_{T,d}(P)=0
  <=> e_1(P)=...=e_T(P)=0
  <=> P lies in the depth-(d-1) catalog at slack T+1.
```

At fixed exact support size this is the dimension shift

```text
(T,k,d) -> (T+1,k-1,d-1).
```

The quotient-lift gate is unchanged, because both sides have the same residual
packet size `T+d` and the same exact support size.

## Frontier Partition

Iterating the shift partitions a depth-`d` packet by its first nonzero
coefficient. For `0<=j<d`, define

```text
F_{T,d}^{(j)} = { P : |P|=T+d,
                  e_1(P)=...=e_(T+j-1)(P)=0,
                  e_(T+j)(P) != 0 }.
```

The terminal stratum is

```text
F_{T,d}^{(infty)} = { P : |P|=T+d,
                      e_1(P)=...=e_(T+d-1)(P)=0 }.
```

On `F_{T,d}^{(j)}`, after `j` shifts the first nonzero slope is

```text
z_j(P)=(-1)^(T+j) e_(T+j)(P),
```

and scaling by `x in D` sends it to `x^(T+j) z_j(P)`. Thus the `j`-frontier
slope image is a union of `D^(T+j)` cosets. In the original slack-`T`
catalog, only `j=0` contributes nonzero slopes; later frontiers are inherited
zero-slope packets for that original slack.

## First Concrete Interface

For `T=2,d=2`, write

```text
P={1,u,v,w},        w=-1-u-v.
```

The slack-two depth-two slope coefficient is

```text
A(u,v)=-(u^2+v^2+uv+u+v+1).
```

Hence the zero-slope slice `A(u,v)=0` is exactly

```text
C_3(D) = { (u,v) in D^2 :
           w=-1-u-v in D,
           1,u,v,w distinct,
           u^2+v^2+uv+u+v+1=0 },
```

the slack-three first-superboundary conic shape set. This is why the
slack-two depth-two theorem and the slack-three first-superboundary theorem are
not isolated low-slack facts: they are adjacent frontiers in the same
residual-depth hierarchy.

## Verification

The dedicated verifier

```bash
python3 experimental/verify_m1_residual_depth_frontier_shift.py
```

checks the first concrete shift using the scanner's second-superboundary and
next-slack first-superboundary ledgers. It compares parameter counts, active
parameter counts, packet counts, and exact-support weighted support counts in
both active and inactive quotient-lift gates.
