# Sharp prime-uniform parity bound for ell=11 exact-five sectors

**Author:** Manuel E. Rey-Álvarez Zafiria

Let `p` be prime with `p=1 mod 11`, let `H=mu_11` in `F_p^*`, and set
`Q=F_p^*/H`. Write `Q^2` for the image of squaring on `Q`.

For a reduced quintic

```text
P(Z)=c1 Z+c2 Z^2+c3 Z^3+c4 Z^4+c5 Z^5,  ci != 0,
```

let `mu_P(rH)` be the largest fibre of `P` on `rH`, and let
`S_h(P|Q^2)` be the sum of the `h` largest values on `Q^2`.

## Theorem

For every such `p` and `P`,

```text
S_3(P|Q^2) <= 10.
```

The bound is sharp. Consequently both ell=11 exact-five parity supports
`{2,4,6,8,10}` and `{1,3,5,7,9}` satisfy the sharp prime-uniform bound

```text
S_6(Gamma) <= 20.
```

## Four-fibre branch

A quintic fibre has size at most five. If no five-point fibre exists and
`S_3>10`, two quotient labels carry four-point fibres. After normalizing one
label, the 30 four-root translation classes give 465 unordered cells. Six
stacked `5x5` minors in `Q(zeta_11)[t]` are saturated by all powers of
`t^11-1`. Every characteristic-zero residual gcd is one.

Exact Bezout norms leave 602 candidate primes and 2,472 prime-cell
incidences. All 24,720 cyclotomic specializations are audited. The 510
residual rows yield 252 distinct exact-five projective states in 29 primes.
Their complete spectra satisfy `max S_3(P|Q^2)=10`.

## Five-fibre branch

Normalize a five-point fibre to `H`. There are 42 five-root translation
classes and 15 triple-root classes. The five-fibre fixes `P` projectively.
Across all 630 five/triple cells, the saturated characteristic-zero gcd is
one. Exact norms leave 80 candidate primes and 2,115 prime-cell incidences.

All 21,150 specializations are audited. There are no anchor rank drops. The
610 field events form 241 exact-five states in 24 primes. Complete spectra
again give `max S_3(P|Q^2)=10`. States with no distinct triple event obey
the stronger envelope `5+2+2=9`.

## Transport and equality

For the even support, `Gamma(X)=P(X^2)`. The map `Q -> Q^2` is two-to-one, so

```text
S_(2h)(Gamma)=2 S_h(P|Q^2).
```

The odd support reduces to the same identity by inversion. Over `F_199`,

```text
P(Z)=Z+115 Z^2+41 Z^3+28 Z^4+146 Z^5
```

has square-quotient spectrum `4^2 2^2 1^5`, hence `S_3=10`; the associated
even support has spectrum `4^4 2^4 1^10` and `S_6=20`.

## Scope

This theorem covers exactly the two parity supports. It does not cover the
remaining 250 exact-five supports with support-difference gcd one, extension
fields, arbitrary background sectors, the full ImgFib conjecture, or the
global list bound.
