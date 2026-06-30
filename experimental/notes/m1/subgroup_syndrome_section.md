# Subgroup Syndrome Section

Status: PROVED / AUDIT.

This note records the row-data adapter used by the `F_17^32` M3 line-value
lift.  It is a small theorem, but it is useful because the regular-minor
extractor consumes syndrome pencils while Paper D's Hankel atlas starts from
actual line values on the evaluation domain.

Let `H <= F^*` be a multiplicative subgroup of order `n`, and let

```text
C = RS[F,H,k],        r = n-k.
```

For `x in H`, the Reed-Solomon dual weight is

```text
lambda_x = 1 / prod_{y in H, y != x}(x-y).
```

Since `prod_{y in H}(X-y)=X^n-1`, we have

```text
prod_{y != x}(x-y) = n x^(n-1),
```

and therefore

```text
lambda_x = x/n.
```

For any syndrome vector `s=(s_0,...,s_{r-1})`, define

```text
y_s(x) = sum_{0 <= m < r} s_m x^(-m-1),        x in H.
```

Then for `0 <= a < r`,

```text
Syn(y_s)_a
  = sum_{x in H} lambda_x x^a y_s(x)
  = (1/n) sum_m s_m sum_{x in H} x^(a-m)
  = s_a,
```

because `r <= n`, so `a-m` is divisible by `n` only when `a=m`, and the usual
subgroup orthogonality gives `sum_{x in H} x^(a-m)=n` in that case and `0`
otherwise.

Thus the weighted syndrome map has an explicit inverse section on every
syndrome vector of length at most `n`.

The verifier

```text
experimental/scripts/verify_m1_subgroup_syndrome_section.py
```

checks this theorem on:

```text
F_17^*, r=8;
F_17^32, |H|=512, r=256,
```

and cross-checks the `F_17^32` section hashes against the fixed top-window
line-value lift.

Non-claims: this note does not compute a worst-case MCA bound, remove quotient
or tangent ledgers, or classify singular pivot buckets.  It only supplies the
line-values-to-syndromes adapter for subgroup rows.
