# F2 Weil-Newton arc bound

- **Status:** PROVED conditional only on the classical Weil bound for twisted
  polynomial character sums; replay verifier included.
- **Track:** `(Q)` / F2 quotient-prefix flatness lane.
- **Verifier:** `python3 experimental/scripts/verify_f2_weil_newton_arc_bound.py`

## Setting

Let `q` be an odd prime, let `H = mu_n subset F_q^x`, and fix the `t=2`
moment map

```text
Phi(S) = (p_1(S), p_2(S)).
```

For `lambda=(lambda_1,lambda_2) in F_q^2`, define

```text
f_lambda(x) = lambda_1 x + lambda_2 x^2,
E_b(lambda) = sum_{S subset H, |S|=b} psi(sum_{x in S} f_lambda(x)).
```

Equivalently, `E_b(lambda)` is the `b`th elementary symmetric coefficient of
the phase multiset

```text
Omega(lambda) = { psi(f_lambda(x)) : x in H }.
```

## Subgroup Weil Input

For every nonzero `lambda`,

```text
| sum_{x in H} psi(f_lambda(x)) | <= 2 sqrt(q).
```

Reason: expand `1_H` using multiplicative characters trivial on `H`. Each
inner sum over `F_q^x` is a standard twisted additive character sum for a
nonconstant polynomial of degree at most `2`; Weil gives the displayed bound
uniformly. Linear and trivial-character quadratic cases are Gauss-sum cases and
fit inside the same `2 sqrt(q)` envelope.

This is the only external theorem in the packet.

## Newton Majorization

Let a multiset of `n` complex numbers on the unit circle have power sums

```text
p_r = sum_i omega_i^r
```

with `|p_r| <= M` for `1 <= r <= b`. Then its elementary coefficient satisfies

```text
|e_b| <= [z^b] (1-z)^(-M)
      = M(M+1)...(M+b-1) / b!.
```

Proof. The generating function is

```text
sum_b e_b z^b = exp(sum_{r>=1} (-1)^(r+1) p_r z^r / r).
```

Expand the exponential coefficient by coefficient and apply the triangle
inequality termwise. Replacing each `|p_r|` by `M` gives

```text
exp(sum_{r>=1} M z^r/r) = (1-z)^(-M).
```

## Arc Bound

For `lambda != 0` and `1 <= r <= b < q`,

```text
p_r(Omega(lambda)) = sum_{x in H} psi(r f_lambda(x))
                   = sum_{x in H} psi(f_{r lambda}(x)).
```

Since `r lambda != 0` in `F_q^2`, the subgroup Weil input applies with
`M = 2 sqrt(q)`. Therefore

```text
|E_b(lambda)| <= W(q,b) := product_{a=0}^{b-1} (2 sqrt(q) + a) / b!.
```

Fourier inversion then gives the uniform zero-fiber bound

```text
N_b(0,0) <= binom(n,b)/q^2 + W(q,b),
```

because the nonzero arcs contribute at most `(q^2-1)W(q,b)/q^2 <= W(q,b)`.
By complementation in the full domain, the same bound applies to the mirrored
top band.

## Scope

This is an edge/minor-arc instrument. It is effective where `W(q,b)` is within
the target budget; it becomes useless at the official mid-band peak, where
`b` is much larger than `sqrt(q)`. Thus it does not close `(Q)` or the F2
guarded extras floor. It narrows the proof interface: edge bands can be paid
by this classical arc bound, while the official mid-band still needs the
separate lower-order/generic-class flatness mechanism.
