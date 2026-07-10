# F2 Newton empty-extremes lemma

- **Status:** PROVED elementary lemma; small verifier included.
- **Track:** `(Q)` / F2 quotient-prefix flatness lane. This records a finite
  edge-band fact for the guarded official extras floor.
- **Verifier:** `python3 experimental/scripts/verify_f2_newton_empty_extremes.py`

## Statement

Let `F` be a field of characteristic `p`, let `D <= F^x` be a cyclic root
domain of order `N`, and assume `t < N`. For `S subset D`, write

```text
p_j(S) = sum_{x in S} x^j.
```

Call `S` `t`-null if `p_j(S)=0` for every `p`-free index `1 <= j <= t`
(`p`-free means `p` does not divide `j`; indices divisible by `p` are
Frobenius-redundant).

Set

```text
m = min(t, p-1).
```

Then:

1. There is no nonempty `t`-null subset `S subset D` with `|S| <= m`.
2. By complementation in the full domain, there is no proper `t`-null subset
   `S subset D` with `N-m <= |S| < N`.
3. The only `t`-null subset in the closed top band `|S| >= N-m` is the full
   domain `D` itself.

The `p-1` in `m` is necessary: Newton inversion only uses coefficients
`1,...,|S|`, so the argument is characteristic-limited.

## Proof

Suppose `1 <= b = |S| <= m` and `S` is `t`-null. Since `b <= p-1`, the
integers `1,...,b` are invertible in `F`. Since `b <= t`, the hypotheses include

```text
p_1(S) = ... = p_b(S) = 0.
```

Let

```text
ell_S(X) = prod_{x in S} (X - x)
         = X^b - e_1(S) X^(b-1) + ... + (-1)^b e_b(S).
```

Newton's identities, triangularly inverted through degree `b`, give

```text
e_1(S) = ... = e_b(S) = 0.
```

But

```text
e_b(S) = prod_{x in S} x
```

is nonzero because `S subset F^x`. This contradiction proves the lower-band
claim.

For complementation, if `1 <= j <= t < N`, then

```text
sum_{x in D} x^j = 0
```

because `D` is a cyclic group of order `N` and `N` does not divide `j`.
Hence `S` is `t`-null if and only if `D \ S` is `t`-null. If
`N-m <= |S| < N`, then `D \ S` is a nonempty set of size at most `m`, which is
impossible by the lower-band claim. The full-domain case `S=D` remains and is
indeed `t`-null when `t<N`.

## Official-Row Consequence

For the F2 guarded official extras floor, the characteristic is about `2^31`
while the moment depth `t` is much larger than the characteristic but still
less than `N ~= 2^41`. Therefore the empty edge width is not `t`; it is the
characteristic-limited width

```text
m = p - 1 ~= 2^31.
```

This strictly strengthens any weak edge-band payment at the official rows:
all nontrivial t-null blocks must lie in the mid-band

```text
p <= |S| <= N - p.
```

The remaining F2 obligation is therefore a mid-band anti-concentration problem.
This lemma does not prove the full guarded extras floor and does not close
row-sharp `(Q)`.

## Relation To The Full-Ladder Dictionary

The full-ladder log-derivative dictionary says that `t`-nullity is exactly
coefficient vanishing at `p`-free indices of the reversed locator. The
empty-extremes lemma is the small-support consequence of that dictionary plus
the nonzero constant term of the locator. It is separated here because it is
often enough to remove edge bands without invoking any flatness or moment
estimate.
