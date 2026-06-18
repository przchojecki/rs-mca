# M1 Depth-Two Nonquadratic One-Coordinate Lemma

**Status:** CONDITIONAL / EXPERIMENTAL.

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

## Quadratic-Fiber Reduction

First ignore the two principal-coordinate exclusions `v!=0` and `w!=0`. For
fixed `u`, write

```text
T(u)=sum_v eta(-(v^2+(u+1)v+(u^2+u+1))).
```

The discriminant is

```text
Delta(u)=-3u^2-2u-3.
```

For any nontrivial nonquadratic `eta` and any split quadratic polynomial
`a(x-r1)(x-r2)`, the change of variables

```text
x = r1 + (r2-r1)t
```

gives, when `r1!=r2`,

```text
sum_x eta(a(x-r1)(x-r2))
  = eta(a) eta((r2-r1)^2) sum_t eta(t(t-1)).
```

When `r1=r2`, the same identity remains true with the right side interpreted
as zero: the left side is `eta(a) sum_x eta^2(x-r1)=0`, because `eta^2` is
nonprincipal, and the discriminant character value is also zero.

For nonsplit quadratics, the same identity picks up the quadratic character
of the discriminant. Equivalently, for all nontrivial nonquadratic `eta`,

```text
sum_x eta(ax^2+bx+c)
  = eta(a) chi_2(b^2-4ac) eta(b^2-4ac) J_eta,
```

where `chi_2` is extended by zero at zero and
`J_eta=sum_t eta(t(t-1))`.

In the present family `a=-1`, so for all `u`

```text
T(u)=eta(-1) chi_2(Delta(u)) eta(Delta(u)) J_eta.
```

Hence the unrestricted two-variable sum is

```text
eta(-1) J_eta sum_u mu(u) chi_2(Delta(u)) eta(Delta(u)).
```

## Bounds

The constant `J_eta` is a two-character Jacobi sum, so

```text
|J_eta| <= sqrt(p),
```

because `eta`, `eta`, and `eta^2` are nonprincipal.

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

checks the exact quadratic-fiber identity, the Jacobi/discriminant factor
bounds, the `2p` unrestricted bound, and the final `4p` open-set bound on the
representative prime/index samples used by the Kummer constant audit.
