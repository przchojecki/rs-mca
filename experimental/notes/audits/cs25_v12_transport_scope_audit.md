# Paper D v12 Circle and Genus-One Transport Scope Audit

- **Status:** AUDIT / exact deployed arithmetic and small-field algebra check.
- **Source:** `tex/cs25_cap_v12.tex`, sections on circle geometry,
  stereographic transport, and rational-scale/genus-one floors; compact use in
  `tex/towards-prize.tex`.
- **Verifier:** `experimental/scripts/verify_cs25_v12_transport_scope.py`.

This audit checks the fourth current `agents.md` priority for Paper D v12:
the rational-scale/genus-one and circle/stereographic transports against the
deployed code models.

The audit is scoped.  It does not reprove the full transport theorems.  It
checks the deployed parameter gates, field-of-definition split, stereographic
model algebra on exhaustive small fields, and the exact integer inequalities
that are consumed by the certificate grammar.

## Circle Standard-Position Gates

For the deployed Mersenne-31 circle row,

```text
p = 2^31 - 1,       p+1 = 2^31,       M = 2^21.
```

The standard-position hypothesis in Paper D uses an element of order

```text
ord(g) = 4M = 2^23.
```

The verifier checks that `ord(g)` divides `p+1` but does not divide `2M`, so
the twin-coset all-scales hypothesis used by the Chebyshev-fiber lemma is
consistent with the deployed model.  It also checks the concrete dyadic scales:

```text
circle line round:       a = M/256 = 2^13,
bivariate circle code:   a = 2M/256 = 2^14,
explicit head scale:     c = 16 with 2c | M.
```

## Field-of-Definition Split

Since `p = 3 mod 4`, `-1` is nonsquare over `F_p`, and `F_{p^r}` contains `i`
if and only if `r` is even.  The verifier checks this parity for `r<=8`.
Consequently:

```text
F_p and F_{p^3}:      no i and q < 2^100,
F_{p^5}:              first no-i extension with q >= 2^100,
F_{p^2}, F_{p^4}:     i present; torus uniformization applies.
```

This matches the split in `cor:circle-anyfield`.

## Stereographic Algebra

For small primes `p=7,11,19,31,43` with `p=3 mod 4`, the verifier exhausts all
`s in F_p` and checks:

```text
x = (1-s^2)/(1+s^2),       y = 2s/(1+s^2)
```

has `x^2+y^2=1`, recovers `s=y/(1+x)`, and has nonzero denominator
`1+s^2`.

It also checks the tangent-halving involution

```text
psi(s) = (s^2-1)/(2s),       psi(s) = psi(-1/s),
```

for all nonzero `s` in those fields.  Finally, for `w=1..7`, it checks that
the cleared stereographic basis

```text
(1-s^2)^j(1+s^2)^(w-j),             0 <= j <= w,
2s(1-s^2)^j(1+s^2)^(w-1-j),         0 <= j < w,
```

has full rank `2w+1` in `F_p[s]_{<=2w}`.  This is the finite-field version of
the basis-change argument in `lem:stereographic`.

## Deployed Circle Arithmetic

The verifier checks the deployed line-round and bivariate-circle arithmetic:

```text
line round:     n=2^21,  k=2^20,      a=2^13,  ell2=130,
circle code:    n_c=2^22, k_c=2^21+1, a=2^14,  ell2=130.
```

It checks the exact entropy gates

```text
binom(256,130) * k   > p * (p^4 + k),
binom(256,130) * k_c > p^2 * (p^4 + k_c),
```

which are the integer forms of the `|B|(q/k+1)` hypotheses.  It also checks
the printed error gates:

```text
line round:   n/q < 2^-102 and converted error > 2^-22,
circle code:  n_c/q < 2^-101 and converted error > 2^-23.
```

## No-i Stereographic RF Gate

For the no-`i` field-of-definition branch, the verifier checks the rational
floor tuple printed in Paper D:

```text
m = 2^20 + 2^15 + 1,       w = 2^16.
```

It verifies the rational-floor hypotheses for `K in {k_c,k_c+1}`, the exact
integer inequality

```text
binom(2^21,m) > p^w * 2^256,
```

and separately checks that this same certificate dominates the `K=k_c` list
threshold at target `2^-100`, where the prefix exponent is `w+1`.  It also
checks the Theorem A integer-admissibility gate and the containment of the edge in

```text
[1-rho_c-2^-6, 1-rho_c).
```

It also checks that for `q >= p^5`, the converted error exceeds `2^-23`.

## Genus-One Boundary Gates

For the genus-one `(psi,2)` rational-scale corollary, the verifier checks the
boundary case declared in the proof:

```text
n = 2^14,      |B| = 2^64,      q = 2^256 - 1,
rho in {1/2, 1/4, 1/8, 1/16}.
```

At these boundary rows it verifies the two exact integer inequalities
corresponding to the MCA/CA floor and the list floor.  This is a boundary
check of the printed proof's monotone/crude estimate, not an exhaustive proof
over all larger `n`.

## Result

The current verifier reports:

```text
implemented PASS: 6   FAIL: 0
```

No transport-scope discrepancy was found in the checked circle,
stereographic, or genus-one gates.  The remaining caution is that the
genus-one statement still depends on the row being genuinely `(psi,2)`-smooth
of degree type `(2,1)`; this audit checks the certificate arithmetic once that
structural hypothesis is supplied, not the ECFFT domain construction itself.
