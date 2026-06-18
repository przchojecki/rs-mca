# M1 Depth-Two Infinity-Unramified Two-Coordinate Lemma

**Status:** CONDITIONAL / AUDIT.

## Claim

Assume the standard Jacobi-sum bound and the standard genus-zero
multiplicative Weil bound on `P^1`. Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and extend all multiplicative characters by zero at zero. Let `mu`, `nu`,
and `eta` be nonprincipal multiplicative characters satisfying

```text
mu nu eta^2 = 1.
```

Then the two-coordinate core sum satisfies

```text
|sum_{u,v} mu(u) nu(v) eta(A(u,v))| <= 2p + 2 sqrt(p).
```

After restoring the principal-coordinate exclusion `w!=0`, the open
two-coordinate sum satisfies

```text
|sum_{u,v} mu(u) nu(v) 1_{w!=0} eta(A(u,v))|
  <= 2p + 5 sqrt(p).
```

The same bounds hold for the active coordinate pairs `(u,w)` and `(v,w)` by
the symmetry of `A=uv+uw+vw-1` on the plane `u+v+w=-1`.

## Ratio Reduction

Only `u,v != 0` contribute to the core. Set

```text
t=u/v,        r=1/v.
```

The condition `mu nu eta^2=1` gives

```text
mu(u) nu(v) eta(A(u,v))
  = mu(t) eta(A(u,v)/v^2).
```

Since

```text
A(u,v)/v^2 = -(r^2+(t+1)r+(t^2+t+1)),
```

the core is

```text
sum_t mu(t) H_eta(t) - sum_t mu(t) eta(-(t^2+t+1)),

H_eta(t)=sum_r eta(-(r^2+(t+1)r+(t^2+t+1))).
```

The second term is a genus-zero Kummer sum with support contained in

```text
t=0,        t^2+t+1=0,        infinity,
```

so it has absolute value at most `2 sqrt(p)`.

## Nonquadratic `eta`

If `eta` is nonquadratic, complete the square in `r`. With

```text
Delta(t)=-3t^2-2t-3,
```

the standard quadratic-fiber identity gives

```text
H_eta(t)
  = eta(1/4) J(eta,chi_2) eta(Delta(t)) chi_2(Delta(t)).
```

The remaining `t`-sum has support contained in

```text
t=0,        Delta(t)=0,        infinity.
```

Because `eta chi_2` and `mu` are nonprincipal, this genus-zero Kummer sum is
bounded by `2 sqrt(p)`. The Jacobi factor has size `sqrt(p)`, so this part
contributes at most `2p`.

## Quadratic `eta`

If `eta=chi_2`, then

```text
H_eta(t) = -chi_2(-1) + p chi_2(-1) 1_{Delta(t)=0}.
```

The constant term cancels against `sum_t mu(t)=0`, and the exceptional
discriminant term has at most two summands. Thus the `H_eta` part is bounded
by `2p`. The same missing-`r=0` genus-zero correction above contributes at
most `2 sqrt(p)`.

## Line Correction

The removed line is `w=0`, i.e. `v=-1-u`. On this line,

```text
A(u,-1-u)=-(u^2+u+1).
```

The line correction

```text
sum_u mu(u) nu(-1-u) eta(-(u^2+u+1))
```

is a genus-zero Kummer sum with support contained in

```text
u=0,        u=-1,        u^2+u+1=0,        infinity.
```

The local monodromy at `u=0` is `mu`, so the sum is not a hidden character
power. The standard genus-zero bound gives `3 sqrt(p)`.

## Contribution to the M1 Trace-Family Target

This proves the full infinity-unramified two-coordinate subfamily predicted
by `experimental/m1_depth_two_two_coordinate_projective_euler_target.md`.
The remaining unresolved two-coordinate Kummer wall is therefore the
ramified-infinity case

```text
mu nu eta^2 != 1,
```

whose projective Euler target is the near-sharp `4p` coefficient.

The finite verifier

```bash
python3 experimental/verify_m1_depth_two_infinity_unramified_two_coordinate_lemma.py
```

checks the exact ratio identity, the line decomposition, and the claimed
finite bounds on representative Kummer-audit samples.
