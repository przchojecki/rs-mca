# M1 Depth-Two Quadratic One-Coordinate Lemma

**Status:** PROVED / EXPERIMENTAL.

## Claim

Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and extend all multiplicative characters by zero at zero. Let `eta` be the
quadratic character of `F_p^*`, and let `mu` be a nonprincipal multiplicative
character. Then

```text
|sum_{u,v} mu(u) 1_{v!=0} 1_{w!=0} eta(A(u,v))| <= 4p.
```

The same bound holds with the nonprincipal coordinate character on `v` or
`w`.

## Proof

Ignore first the two principal-coordinate exclusions `v!=0` and `w!=0`.
For fixed `u`, the inner sum is

```text
T(u)=sum_v eta(-(v^2+(u+1)v+(u^2+u+1))).
```

The discriminant is

```text
Delta(u)=-3u^2-2u-3.
```

For a nonconstant quadratic polynomial `aX^2+bX+c` over `F_p`, the standard
quadratic-character identity gives

```text
sum_x eta(ax^2+bx+c) = -eta(a)       if b^2-4ac != 0,
                     = (p-1) eta(a)  if b^2-4ac = 0.
```

Here `a=-1`, so

```text
T(u) = -eta(-1) + p eta(-1) 1_{Delta(u)=0}.
```

Since `sum_u mu(u)=0`, the constant part cancels and the unrestricted sum is

```text
p eta(-1) sum_{Delta(u)=0} mu(u).
```

The quadratic `Delta` has at most two roots, hence the unrestricted part has
absolute value at most `2p`.

Restoring the two principal-coordinate exclusions removes the union of the
lines `v=0` and `w=0`. This union has `2p-1` affine points, and each summand
has absolute value at most one. Thus the correction has absolute value at
most `2p-1`, giving the open-set bound `4p`.

The polynomial `A=uv+uw+vw-1` on the plane `u+v+w=-1` is symmetric in
`u,v,w`, so the cases with the active coordinate on `v` or `w` are identical.

## Contribution to M1

This lemma removes the quadratic one-coordinate mixed family from the
two-variable normal-crossing Kummer import in the slack-two depth-two ledger.
After this elementary slice calculation, the remaining mixed import consists
only of:

```text
d!=0, one coordinate active, nonquadratic conic character: 4p
d!=0, two coordinates active:                              9p
d!=0, three coordinates active:                           16p
```

The finite verifier

```bash
python3 experimental/verify_m1_depth_two_quadratic_one_coordinate_lemma.py
```

checks the exact fiber identity, the `2p` unrestricted bound, the `2p-1`
open-set correction, and the final `4p` bound on the representative
prime/index samples used by the Kummer constant audit.
