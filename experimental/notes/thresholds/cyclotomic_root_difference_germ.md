# Cyclotomic Root-Difference Germ

Status: PROVED / CERTIFICATION-ARITHMETIC.

This note packages the root-difference primitive used by the
generator-economy lane.  It is deliberately smaller than a generator-economy
construction: it proves the exact factorization and norm formula for single
roots, which is the base template that design searches try to lift from roots
to `ell`-sums.

The companion verifier is:

```text
python3 experimental/scripts/verify_cyclotomic_root_difference_germ.py
```

The emitted certificate is:

```text
experimental/data/certificates/cyclotomic-root-difference-germ/cyclotomic_root_difference_germ.json
```

## Convention Block

```text
object:              quotient e_1 value-set certification primitive
number field:        K_N = Q(zeta_N)
root difference:     zeta_N^a - zeta_N^b
reduction prime:     p, supplied by consumers
denominator role:    p is not a slope denominator; consumers print q_line/q_chal
```

## Theorem: Factorization And Norm

Let `zeta_N` be a primitive `N`-th root of unity.  For integers `a,b`, put
`d = a-b mod N`.  Then

```text
zeta_N^a - zeta_N^b = zeta_N^b (zeta_N^d - 1).
```

If `d = 0`, the difference is zero.  If `d != 0`, set

```text
M = N / gcd(N,d).
```

Then `zeta_N^d` is a primitive `M`-th root of unity and

```text
|Norm_{Q(zeta_N)/Q}(zeta_N^a - zeta_N^b)|
  = Phi_M(1)^( phi(N) / phi(M) ),
```

where

```text
Phi_M(1) =
  q   if M is a positive power of the prime q,
  1   if M has at least two distinct prime factors.
```

Proof.  The factorization is immediate after factoring out `zeta_N^b`.
Cyclotomic units have norm `1`, so the norm is the norm of `1-zeta_N^d`.
Since `zeta_N^d` is primitive of order `M`, this element lies in `Q(zeta_M)`.
Taking norms through the tower gives

```text
Norm_{Q(zeta_N)/Q}(1-zeta_M)
  = Norm_{Q(zeta_M)/Q}(1-zeta_M)^(phi(N)/phi(M)).
```

Finally

```text
Norm_{Q(zeta_M)/Q}(1-zeta_M) = Phi_M(1),
```

and the displayed evaluation of `Phi_M(1)` is the standard cyclotomic value at
`1`: it is the underlying prime for prime-power `M` and `1` otherwise.

## Consequence For Generator Economy

For single roots, every pair difference is a cyclotomic unit times one of the
base factors

```text
zeta_N^d - 1,       1 <= d < N.
```

After identifying `d` with `N-d` up to sign and unit, there are at most
`floor(N/2)` unit/sign templates.  A row-specific certificate therefore needs
only the corresponding base-factor norm checks.  For `N` a power of two, the
norm formula shows these checks are powers of `2`, hence automatically avoid
every odd reduction prime.

The open generator-economy problem is to lift this compression from singleton
root differences to `ell`-sum differences.  This note proves the base germ
only; it does not construct large all-pairs-certified `ell`-sum families.
