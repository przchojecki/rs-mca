# M1 Depth-Two Equal-Line Diagonal Reduction

**Status:** CONDITIONAL / AUDIT.

## Claim

Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
B(s)=s^2+s+1,
```

and extend multiplicative characters by zero at `0`. Let `mu`, `eta`, and
`mu eta` be nonprincipal. Define the diagonal two-coordinate open sum

```text
S_open(mu,eta) =
  sum_{u,v in F_p} mu(u) mu(v) 1_{w!=0} eta(A(u,v)).
```

Then

```text
S_open(mu,eta) =
  J^-(mu,eta) sum_{s!=-1} (mu eta)(B(s))
  + R(mu,eta),
```

where

```text
J^-(mu,eta) = sum_t mu(t) eta(t-1),

R(mu,eta) =
  sum_{s!=-1} sum_t
    chi_2(s^2-4t) mu(t) eta(t-B(s)).
```

The first term is already one-dimensional and satisfies

```text
|J^-(mu,eta) sum_{s!=-1} (mu eta)(B(s))|
  <= p + sqrt(p).
```

Thus, in the equal-line-monodromy subfamily, the remaining analytic work is
concentrated in the residual trace `R(mu,eta)`.

## Equal-Line Monodromy

For the canonical active pair `(a,b,c)=(a,b,0)`, use a common character order
`h` and let the coordinate-character lift be `g=h/e`. The projective line
monodromies on the two active coordinate lines and infinity have exponents

```text
ga,        gb,        -(ga+gb+2d)       mod h.
```

The equal-line diagonal case is therefore

```text
a=b,        2d + 3ga == 0 mod h.
```

When `h=2e`, this is the congruence seen in the numerical stress scan:

```text
d == -3a mod e.
```

In character notation this says

```text
mu^3 eta^2 = 1.
```

If also `mu eta=1`, then `eta=mu^{-1}` and the equality above forces
`mu=1`, contradicting the two-coordinate hypothesis. Hence the Jacobi
factor in the reduction is nondegenerate throughout the equal-line
remaining-wall family.

## Proof of the Reduction

Set

```text
s=u+v,        t=uv.
```

For fixed `(s,t)`, the number of ordered pairs `(u,v)` with
`u+v=s` and `uv=t` is

```text
1 + chi_2(s^2-4t).
```

Moreover

```text
mu(u)mu(v)=mu(t),
A(u,v)=t-B(s),
w!=0  <=>  s!=-1.
```

Therefore

```text
S_open(mu,eta) =
  sum_{s!=-1} sum_t
    (1+chi_2(s^2-4t)) mu(t) eta(t-B(s)).
```

Splitting the `1` and `chi_2` terms gives the displayed formula, except that
the first part is still

```text
sum_{s!=-1} sum_t mu(t) eta(t-B(s)).
```

For `B(s)!=0`, substituting `t=B(s)x` gives

```text
sum_t mu(t) eta(t-B(s))
  = (mu eta)(B(s)) J^-(mu,eta).
```

For `B(s)=0`, both sides are zero because `mu eta` is nonprincipal and is
extended by zero at `0`. This proves the identity.

The bound on the first term is standard: since `mu`, `eta`, and `mu eta`
are nonprincipal, the Jacobi sum has size `sqrt(p)`. The polynomial
`B(s)=s^2+s+1` is separable for `p>3`; the genus-zero Kummer bound gives

```text
|sum_s (mu eta)(B(s))| <= sqrt(p),
```

and deleting the single value `s=-1` costs at most `1`.

## Contribution to the Remaining M1 Wall

The stress scan in
`experimental/m1_remaining_two_coordinate_wall_experiment.md` found that the
largest remaining-wall examples all lie in this equal-line diagonal family.
For the two largest rows, the reduction gives:

```text
(421,20,21,42),  (5,5,0,6):
  |S|/p = 3.9771715522,
  Jacobi part = 1.0485702499p,
  residual R = 2.9290031282p.

(461,20,23,46),  (18,18,0,15):
  |S|/p = 3.9643175123,
  Jacobi part = 1.0465694143p,
  residual R = 2.9412840316p.
```

This suggests the next proof target should be a sharp bound for the residual
quadratic-discriminant trace `R(mu,eta)`, ideally explaining a `3p`
top-dimensional coefficient in the equal-line case.

The finite verifier is

```bash
python3 experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py
```
