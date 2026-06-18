# M1 Depth-Two Nonquadratic One-Coordinate Lemma

**Status:** CONDITIONAL / AUDIT.

## Claim

Assume the standard Jacobi-sum bound and the standard genus-zero
multiplicative Weil bound on `P^1`. Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and extend all multiplicative characters by zero at zero. Let `eta` be a
nontrivial nonquadratic multiplicative character, so `eta^2` is nonprincipal,
and let `mu` be a nonprincipal multiplicative character. Then

```text
|sum_{u,v} mu(u) 1_{v!=0} 1_{w!=0} eta(A(u,v))| <= 4p.
```

The same bound holds with the nonprincipal coordinate character on `v` or
`w`.

## Fixed-Coordinate Reduction

First ignore the two principal-coordinate exclusions `v!=0` and `w!=0`. For
fixed `u`, complete the square:

```text
A(u,v) = Delta(u)/4 - (v+(u+1)/2)^2,
Delta(u) = -3u^2 - 2u - 3.
```

For every `c in F_p`,

```text
sum_x eta(c-x^2) = eta(c) chi_2(c) J(eta,chi_2),
```

where `chi_2` is the quadratic character and the right side is also zero
when `c=0`. Indeed, if `c!=0`, then

```text
sum_x eta(c-x^2)
  = sum_y eta(y) chi_2(c-y)
  = eta(c) chi_2(c) sum_t eta(t) chi_2(1-t).
```

If `c=0`, the left side is `eta(-1) sum_x eta^2(x)`, which is zero because
`eta^2` is nonprincipal. Therefore

```text
sum_v eta(A(u,v))
  = eta(1/4) J(eta,chi_2) eta(Delta(u)) chi_2(Delta(u)).
```

Hence the unrestricted two-variable sum is

```text
eta(1/4) J(eta,chi_2)
  sum_u mu(u) chi_2(Delta(u)) eta(Delta(u)).
```

## Bounds

The constant `J(eta,chi_2)` has absolute value `sqrt(p)`, because `eta`,
`chi_2`, and `eta chi_2` are nonprincipal.

The one-variable discriminant sum has zero-pole support contained in

```text
u=0,        Delta(u)=0,        infinity.
```

The quadratic `Delta` has two distinct geometric roots for `p>3`. The
character on `Delta` is `eta chi_2`, which is nonprincipal because `eta` is
nonquadratic, and the coefficient at `u=0` is nonzero because `mu` is
nonprincipal. Thus the rational function is not a character-order power, and
the genus-zero Kummer bound gives

```text
|sum_u mu(u) chi_2(Delta(u)) eta(Delta(u))| <= 2 sqrt(p).
```

The unrestricted two-variable sum is therefore bounded by `2p`.

Restoring the two principal-coordinate exclusions removes the union of the
lines `v=0` and `w=0`, which has `2p-1` affine points. Each summand has
absolute value at most one, so the correction has absolute value at most
`2p-1`. The open-set sum is bounded by `4p`.

The polynomial `A=uv+uw+vw-1` on the plane `u+v+w=-1` is symmetric in
`u,v,w`, so the cases with the active coordinate on `v` or `w` are identical.

## Contribution to M1

Together with
`experimental/m1_depth_two_quadratic_one_coordinate_lemma.md`, this removes
all one-coordinate mixed terms from the external two-variable
normal-crossing Kummer import in the slack-two depth-two ledger. The remaining
import begins at:

```text
d!=0, two coordinates active:     9p
d!=0, three coordinates active:  16p
```

The finite verifier

```bash
python3 experimental/verify_m1_depth_two_nonquadratic_one_coordinate_lemma.py
```

checks the exact fixed-coordinate identity, the Jacobi/discriminant factor
bounds, the `2p` unrestricted bound, and the final `4p` open-set bound on the
representative prime/index samples used by the Kummer constant audit.
