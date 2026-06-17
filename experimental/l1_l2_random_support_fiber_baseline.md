# L1/L2 Random Simultaneous Support-Fiber Baseline

## Claim

Let `F` be a finite field of size `q`, let `D subset F` have size `n`, and let
`C = RS[F,D,k]`. Fix

```text
a = k + sigma,   0 <= sigma <= n - k.
```

For a received word `U:D -> F`, define the feasible support fiber

```text
Fib_U(a) = { S subset D : |S| = a and U|S agrees with some codeword of C }.
```

For `mu >= 1` and a `mu`-row received word `U = (U_1,...,U_mu)`, define the
simultaneous support fiber

```text
Fib_U^cap(a) = Fib_U1(a) cap ... cap Fib_Umu(a).
```

If the rows `U_1,...,U_mu` are independent and uniformly random in `F^D`, then

```text
E |Fib_U^cap(a)| = binom(n,a) / q^(mu sigma).
```

In particular, for `mu = 1`,

```text
E |Fib_U(a)| = binom(n,k+sigma) / q^sigma.
```

If `a >= k`, the column-distance interleaved list obeys

```text
E |Lambda(Int(C,mu), 1 - a/n, U)|
  <= binom(n,a) / q^(mu sigma).
```

Thus random interleaved received words pay for one common support family, not
`mu` independent support families.

## Status

PROVED.

## Existing Paper Dependency

This supports two high-priority targets in `agents.md`:

- L1, by giving the exact random locator/support-fiber entropy baseline;
- L2, by replacing independent base-list products with simultaneous
  agreement-support families for interleaved lists.

It is not a worst-case local-limit theorem. It identifies the random baseline
that worst-case L1/L2 statements have to beat or match after quotient and other
structured obstructions are separated.

## Proof of the Support-Fiber Formula

Fix a support `S subset D` with `|S| = a = k + sigma`.

The restriction map

```text
F_{<k}[X] -> F^S
```

is injective because `|S| >= k` and the evaluation points are distinct. Its
image has size `q^k` inside `F^S`, which has size `q^a`. Therefore, for one
uniform random row `U_i`,

```text
Pr[ S in Fib_Ui(a) ] = q^k / q^a = q^(-sigma).
```

The rows are independent, so

```text
Pr[ S in Fib_U^cap(a) ] = q^(-mu sigma).
```

Summing this indicator over the `binom(n,a)` supports gives

```text
E |Fib_U^cap(a)| = binom(n,a) q^(-mu sigma).
```

No independence between different supports is needed; this is just linearity of
expectation.

## Interleaved List Consequence

Let `Int(C,mu)` use column distance. If an interleaved codeword

```text
c = (c_1,...,c_mu)
```

is within radius `1 - a/n` of `U`, then there is a common agreement set
`A subset D` with `|A| >= a` on which every row `U_i` agrees with `c_i`.
Choose a canonical `a`-subset `S_c` of `A`. Then `S_c in Fib_U^cap(a)`.

The map `c -> S_c` is injective. If two interleaved codewords map to the same
support `S`, then for each row `i` the two row codewords agree with the same
word `U_i` on `S`. Since `|S| = a >= k`, Reed-Solomon uniqueness forces the
two row codewords to be equal. Hence the interleaved codewords are equal.

Therefore

```text
|Lambda(Int(C,mu), 1 - a/n, U)| <= |Fib_U^cap(a)|.
```

Taking expectations and applying the support-fiber formula proves the
interleaved list bound.

## Comparison With the Cartesian Product Heuristic

The single-row random baseline is

```text
E |Fib_U(a)| = binom(n,a) / q^sigma.
```

Multiplying this `mu` times would suggest

```text
(binom(n,a) / q^sigma)^mu.
```

But the simultaneous-support calculation gives

```text
binom(n,a) / q^(mu sigma).
```

The ratio is

```text
binom(n,a)^(mu - 1).
```

This is exactly the exponent that L2 seeks to avoid overpaying. The reason is
structural rather than probabilistic: column-distance interleaving requires the
same support columns for all rows.

## Markov Corollaries

For every `epsilon > 0`,

```text
Pr[ Fib_U^cap(a) is nonempty ]
  <= epsilon
```

whenever

```text
q^(mu sigma) >= epsilon^(-1) binom(n,a).
```

Likewise,

```text
Pr[ Lambda(Int(C,mu), 1 - a/n, U) is nonempty ]
  <= epsilon
```

under the same inequality.

For protocol ledger purposes, the expected list-size-over-field term for a
random `mu`-row word is bounded by

```text
E |Lambda(Int(C,mu), 1 - a/n, U)| / q
  <= binom(n,a) / q^(mu sigma + 1).
```

## Ledger Impact

This note separates three quantities that are easy to conflate:

- a base-code list count;
- a base-code support-fiber count;
- an interleaved simultaneous-support count.

The L2 target should be phrased in terms of the third quantity whenever the
protocol uses column-distance interleaving. Random rows satisfy the desired
support sharing exactly, with the exponent `mu sigma` in the denominator and
only one factor `binom(n,a)` in the numerator.

The remaining hard problem is worst-case structure: quotient-periodic,
low-denominator, or otherwise correlated received rows can force many supports
to align. This lemma does not rule those out; it gives the exact baseline
against which they should be measured.
