# Exact-five onset and six-fibre terminal at ell = 11

Author: Manuel E. Rey-Álvarez Zafiria

## 1. Exact-five non-vacuity onset

Let `p = 331`, let `H` be the subgroup of order `ell = 11` in
`F_p^*`, and consider functions

```text
Gamma(X) = sum_(a in A) gamma_a X^a,
A subset {1,...,10}, |A| = 5, gamma_a != 0.
```

The complete projective kernel census gives the exact proportional
envelopes

```text
(S_6, S_7, S_8, S_9) = (20, 22, 24, 27).
```

It visits `2,509,920` projective four-root kernel rows. Exactly `2,472,120`
of them retain five-coordinate support. No rank-deficient cell occurs.
Vectors outside this kernel census have fibre cap at most three.

The state

```text
A = {1,3,5,7,9},
gamma = (1,15,45,179,176)
```

has spectrum `5^2 3^2 2^4 1^22`. Exact pointwise reconstruction gives
primitive, divisibility-minimal listed anchors for `tau = 6,7,8`.
Common-sector-dead padding gives a listed word in every positive-defect row

```text
(tau,m) = (6,8), (6,9), (6,10), (7,9), (7,10), (8,10).
```

Consequently every prime-field, background-free, `ell = 11`, exact-five,
positive-defect row with `tau >= 6` is non-vacuous.

## 2. Support dichotomy and parity quotient

For a five-subset `A` of `{1,...,10}`, define

```text
g_A = gcd { a-a_0 : a in A }.
```

Of the 252 supports, 250 have `g_A = 1`. The only supports with `g_A = 2`
are

```text
{1,3,5,7,9} and {2,4,6,8,10}.
```

The quotient-label orbit is projectively injective for `g_A = 1`. For
`g_A = 2` it has exact multiplicity two, induced by `r -> -r`.

Both parity supports reduce, by squaring and in the odd case inversion, to

```text
P(Z) = c_1 Z + c_2 Z^2 + c_3 Z^3 + c_4 Z^4 + c_5 Z^5,
c_i != 0.
```

Put `Q = F_p^*/H`, and let `Q^2` be the image of squaring on `Q`. The
quotient map has kernel `{H,-H}` and image `Q^2`; hence

```text
S_(2h)(Gamma) = 2 S_h(P restricted to Q^2).
```

The restriction to `Q^2` is essential.

## 3. Six-fibre exceptional characteristics

The normalized `6 x 6` cyclotomic norm table has only the prime divisors

```text
23, 67, 199, 419
```

that are congruent to one modulo 11. Thus every other characteristic has
fibre cap five. The first two primes have fewer than eleven quotient labels,
so they cannot realize the `tau = 5, m = 6` RS geometry considered here.
Complete projective censuses at the remaining primes give

```text
p = 199: S_6 = 20, profile 6^1 2^8 1^9;
p = 419: S_6 = 20, profile 6^1 2^5 1^32.
```

The available six-fibre exceptions therefore satisfy the target bound.

## 4. Scope

The four `tau = 5` positive-defect rows are not settled by the non-vacuity
construction. The 250 supports with `g_A = 1` are not globally classified
here. No extension-field, arbitrary-background, whole-ImgFib, list-grand,
or project-wide conclusion is claimed.

The accompanying JSON files are finite certificates. The independent Python
auditors reconstruct the exact-five witness family, deletion minimality,
parity transport, and the exceptional profiles directly from those files.
