# Full-lift linear-factor projective-star router

## Scope

This packet classifies the degree-one branch of the Mersenne `e=130237`
common interpolation factor.  It routes the branch to an `F`-rational
projective star; it does not pay that star or treat factor degree at least
two.

## Polynomial-section parameter

Write a primitive linear factor over the algebraic closure as

```text
P=A(X)Y+B(X)Z+C(X),       gcd(A,B,C)=1.
```

The common-factor mass theorem supplies at least 4,982 distinct pairs
`(a_i,b_i) in F[X]_<6^2` satisfying `P(X,a_i,b_i)=0` identically.

Subtracting two section equations and removing `gcd(A,B)` gives

```text
(a_i,b_i)=(a_0+B*t_i,b_0-A*t_i),
deg t_i<=s=5-max(deg A,deg B).
```

Primitivity is essential here: one section shows that `gcd(A,B)` also
divides `C`, so it is a unit.  In particular `deg A,deg B<=5`.

## Johnson exclusion

Since `A,B` are coprime, they do not vanish simultaneously on the evaluation
domain.  The received pair induces a scalar extension-field word `tau` such
that every `t_i` agrees with `tau` on its at-least-807-point core.

For degree `s`, the ordinary constant-block Johnson cap is

```text
J_s=floor(130237*(807-s)/(807^2-130237*s)).
```

The exact values are

```text
s       0    1    2    3    4       5
J_s   161  201  268  401  802  1632032.
```

If either `A` or `B` is nonconstant, then `s<=4`, contradicting
`4982>802`.  Hence `A,B` are constants and `deg C<=5`.

## Projective star

The center is `F`-rational despite the initial algebraic-closure
factorization.  If `A!=0`, two distinct captured `F`-rational pairs give

```text
gamma_*=B/A in F,
c_*=-C/A=a_i+gamma_* b_i in RS_6.
```

All captured affine explanation lines pass through `(gamma_*,c_*)`.  If
`A=0`, every captured pair has the same direction codeword `b_*=-C/B`; this
is the projective center at slope infinity.

Thus the degree-one branch is exactly an `F`-rational projective-star shape.
This identifies the relevant primitive-star obstruction but does not prove
its population bound.

## Replay

```bash
python3 experimental/verify_mca_full_lift_linear_factor_projective_star_router_v1.py
python3 experimental/audit_mca_full_lift_linear_factor_projective_star_router_v1.py
```
