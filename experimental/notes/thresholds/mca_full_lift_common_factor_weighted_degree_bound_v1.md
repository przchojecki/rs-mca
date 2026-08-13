# Full-lift common-factor weighted-degree bound

## Scope

This packet sharpens the common interpolation gcd at the first Mersenne
residual `e=130237`.  It does not assume the gcd is irreducible and does
not pay either remaining factor branch.

## Quotient dimension

Let `P` be the primitive full gcd and put

```text
w=wdeg_(1,5,5)(P).
```

Gauss's lemma makes `P` a polynomial divisor of every kernel member.
Weighted degree is additive under multiplication, so division embeds the
kernel into weighted degree at most `264-w`.  The kernel dimension is at
least 938.

For weighted degree `D`, the exact monomial count is

```text
M(D)=sum_(s=0)^floor(D/5) (s+1)(D-5s+1).
```

The adjacent threshold is

```text
M(46)=935 < 938 <= 990=M(47).
```

Therefore

```text
w<=217,              deg_(Y,Z)(P)<=43.
```

## Higher-degree mass

The degree-one branch is classified separately.  If `d>=2`, the existing
cofactor Bezout theorem gives

```text
on-factor pairs >= 7583-(52-d)^2 >= 5083.
```

The size-807 cores and pairwise intersection cap five then give

```text
factor points
 >= ceil(5083*807^2/(807+5*(5083-1)))
 = 126266,
exceptions <= 130237-126266 = 3971.
```

The full gcd may be a product of lower-degree factors.  No component
population or split-pencil conclusion is claimed.

## Replay

```bash
python3 experimental/verify_mca_full_lift_common_factor_weighted_degree_bound_v1.py
python3 experimental/audit_mca_full_lift_common_factor_weighted_degree_bound_v1.py
```
