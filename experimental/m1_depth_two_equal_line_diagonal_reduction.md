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

The residual trace has a further one-parameter form. Let

```text
rho = mu eta chi_2,
lambda(s) = s^2 / (4B(s)),
H(lambda) = sum_x mu(x) eta(x-1) chi_2(x-lambda).
```

Then

```text
R(mu,eta) =
  chi_2(-4) sum_{s!=-1, B(s)!=0} rho(B(s)) H(lambda(s))
  + E_B(mu,eta),
```

where `E_B` is supported on the at most two roots of `B(s)=0`, and

```text
|E_B(mu,eta)| <= 2 sqrt(p).
```

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

Let

```text
alpha = mu eta.
```

Then the equal-line relation gives the single-character normal form

```text
mu = alpha^(-2),        eta = alpha^3,        rho = alpha chi_2.
```

Thus `alpha` and `alpha chi_2` are nonprincipal in the remaining-wall case:
if `alpha=1`, then `eta=mu^{-1}` is reciprocal; if `alpha=chi_2`, then
`mu=1`.

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

## Hypergeometric Pullback for `R`

For `B(s)!=0`, scale `t=B(s)x`. Then

```text
chi_2(s^2-4t) mu(t) eta(t-B(s))
  = chi_2(-4) rho(B(s))
    mu(x) eta(x-1) chi_2(x-lambda(s)).
```

This gives the displayed pullback formula. The trace `H(lambda)` is the
three-point hypergeometric trace with moving branch point `lambda`; the
outer variable only sees its pullback along

```text
lambda = s^2 / (4(s^2+s+1)).
```

If `B(s)=0`, then `s!=0` and the inner residual fiber is

```text
sum_t chi_2(s^2-4t) (mu eta)(t)
  = (mu eta)(s^2/4) J(mu eta, chi_2).
```

In the equal-line remaining-wall case, both `mu eta` and `mu eta chi_2` are
nonprincipal. Hence each exceptional fiber has size `sqrt(p)`, giving the
`2 sqrt(p)` bound above.

For the two largest rows, the residual pullback decomposition gives:

```text
(421,20,21,42),  (5,5,0,6):
  residual R = 2.9290031282p,
  pullback main = 2.9043632895p,
  exceptional contribution = 1.0000000000 sqrt(p).

(461,20,23,46),  (18,18,0,15):
  residual R = 2.9412840316p,
  pullback main = 2.9412840316p,
  exceptional contribution = 0.
```

Thus the next geometric target is not the original two-variable surface sum,
but the middle cohomology of this pulled-back three-point hypergeometric
sheaf. A `3p` bound for the pullback main term, plus the exceptional
`2 sqrt(p)` correction, would explain the observed near-`4p` diagonal
examples.

Using the single-character notation `alpha=mu eta`, the pullback main is
equivalently

```text
chi_2(-1) sum_{s!=-1, B(s)!=0} sum_x
  alpha(B(s)) alpha^(-2)(x) alpha^3(x-1)
  chi_2(4B(s)x-s^2).
```

This is the most concrete current form of the near-sharp diagonal problem:
one nonquadratic character `alpha`, one quadratic factor, and the divisor

```text
B(s),        x,        x-1,        4B(s)x-s^2.
```

The finite pullback scanner
`experimental/search_m1_equal_line_pullback.py` directly stress-tests the
target

```text
|M_alpha| <= 3p
```

for this single-character main term. Its report preset exhausts all
equal-line canonical active-pair tuples with `p <= 500` and `e <= 24`.
It tests `4804` tuples and finds no `3p` violation. The largest rows are:

```text
(461,20,23,46),  (18,18,0,15),  alpha=5:
  |M_alpha|/p = 2.9412840316,

(281,20,14,28),  (1,1,0,25),    alpha=27:
  |M_alpha|/p = 2.9391353527,

(397,44,9,18),   (1,1,0,15),    alpha=17:
  |M_alpha|/p = 2.9357869704.
```

## Pullback Branch Checklist

The rational pullback

```text
lambda(s) = s^2 / (4B(s)),        B(s)=s^2+s+1,
```

has the following exact geometry for `p>3`:

```text
lambda=0:        s=0, with ramification index 2,
lambda=infinity: B(s)=0, two simple geometric points,
lambda=1:        C(s)=3s^2+4s+4=0, two simple geometric points.
```

The derivative is

```text
lambda'(s) = s(s+2) / (4B(s)^2).
```

Thus the second ramification point is `s=-2`, and it maps to the regular
value `lambda=1/3`. The deleted open point `s=-1` maps to the regular value
`lambda=1/4`. The finite branch and singular polynomials

```text
s,        B(s),        C(s),        s+1,        s+2
```

are pairwise separated in the ways needed above:

```text
B(0)=1,        C(0)=4,
B(-1)=1,       C(-1)=3,
B(-2)=3,       C(-2)=8.
```

Consequently, the remaining `3p` target can be phrased as a conductor
problem for the middle extension of

```text
rho(B(s)) H(lambda(s))
```

on the `s`-line, with geometric singular support contained in

```text
s=0,        B(s)=0,        C(s)=0,        infinity,
```

and with the regular deleted point `s=-1` handled separately by the usual
pointwise genus-zero bound for `H(1/4)`.

The finite verifier is

```bash
python3 experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py
```
