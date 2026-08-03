# Cubic-divisor and decorated product-line reductions for Paper D

Author: Manuel E. Rey-Álvarez Zafiria

## 1. Cross-pair cubic-divisor identity

Let `H = mu_n(F_p)`, where `n = 2^s >= 8`, and let `T_sm(H)` count
unordered common-scale orbits of smooth disjoint quartic trades. For an
oriented trade, choose `x` on the first side and `y` on the second side,
scale by `y^(-1)`, and put `r = x/y`. If `P` and `Q` are the cubic locators
left after deleting `r` and `1`, then

```text
(X-1)Q(X) = (X-r)P(X) - (1-r)P(1).
```

Writing `P = X^3-uX^2+vX-w`, the induced affine coefficient transform is

```text
u' = u+r-1,
v' = v+(r-1)(u-1),
w' = w+(r-1)(v-u+1).
```

Let `C_r` count records for which both cubics split simply on `H`, the
completed quartets are disjoint, and their common centered-Hadamard invariant
is smooth. Exact orbit counting gives

```text
sum_(r in H\{1}) C_r = 32 T_sm(H).
```

There is a second exact currency. Orient a trade, choose `y` on its second
side, normalize `y = 1`, and let `(d,e)` be the ordered products of the two
normalized quartets. If `K(d,e)` counts these records, then

```text
sum_(d,e in H, d != e) K(d,e) = 8 T_sm(H).
```

Consequently the smooth Paper-D target `T_sm(H) <= n^2/2` is equivalent to
either aggregate inequality

```text
sum_r C_r <= 16 n^2,
sum_(d != e) K(d,e) <= 4 n^2.
```

## 2. Decorated product-line identity

For a normalized smooth cross-pair record

```text
A = {r,a,b,c},  B = {1,t,u,v},  w = abc,  W = tuv,
```

define

```text
L = -ar+at+a+rt+r-t^2-t-1,
R = a^2+ar-at-a+r^2-rt-r+t.
```

Once the two residual quadratics are required to split simply in `H`, the
cubic transform is equivalent to the affine product line

```text
-aLW + tRw + at(t-a)(a-1)(r-1)(r-t) = 0.
```

The constant term is nonzero on every valid record, and exact elimination
gives

```text
Res_a(L,R) = (r-1)^2 (r-t)^2.
```

Thus the line is never doubly degenerate. The generic two-variable branch
and the two one-sided degeneracies form an exhaustive, disjoint partition.
Each cross-pair record has nine decorations, so

```text
9 sum_r C_r = 288 T_sm(H).
```

Both one-sided branches occur in genuine smooth trades and cannot be
discarded.

## 3. Finite checks and scope

The independent exhaustive rows are

```text
(n,p,T_sm,max K) = (16,17,0,0), (32,97,9,2), (32,193,1,2).
```

The pointwise conjecture `K(d,e) <= 4` is false without a
large-characteristic hypothesis: at `n = 128, p = 257`, exact enumeration
gives `T_sm = 22476`, `max K = 26`, and `max C_r = 5789`. In particular the
global target itself fails outside the active regime.

The identities and multiplicities above are exact. This note does not prove
the active-characteristic aggregate line-energy inequality and does not by
itself close a Paper-D row.
