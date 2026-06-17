# L2 Interleaved Support-Fiber Bridge

**Status:** PROVED for the finite support injection; CONDITIONAL when a future
locator-fiber theorem is used as input.

This note isolates a useful L2 bridge.  The trivial protocol ledger bound

```text
|Lambda(Int(C,mu),delta)| <= |Lambda(C,delta)|^mu
```

can overcharge the interleaving arity.  If the available theorem bounds
agreement supports rather than only codewords, then column-distance interleaving
does not multiply the exponent by `mu`: all rows must agree on the same columns.

## Setup

Let `C=RS[F,H,k]` with `|H|=n`.  The same argument applies to any code whose
restriction to every support of size at least `k` is injective.  For a received
word `U:H -> F` and `a >= k`, write

```text
Fib_U(a) = {S subset H : |S|=a and U|S agrees with some c in C}.
```

For a `mu`-row received word

```text
U = (U_1,...,U_mu) in (F^H)^mu,
```

define the simultaneous feasible-support fiber

```text
Fib_U^cap(a) = Fib_U1(a) cap ... cap Fib_Umu(a).
```

The interleaved code `Int(C,mu)` uses column distance: a tuple
`(c_1,...,c_mu)` is within radius `1-a/n` of `U` iff there is a support
`A subset H` of size at least `a` on which every row agrees.

## Bridge Lemma

For every `mu >= 1`, every `a >= k`, and every interleaved received word `U`,

```text
|Lambda(Int(C,mu),1-a/n,U)| <= |Fib_U^cap(a)|.
```

Consequently,

```text
|Lambda(Int(C,mu),1-a/n,U)|
  <= min_i |Fib_Ui(a)|.
```

If a uniform support-fiber theorem proves

```text
|Fib_V(a)| <= n^B
```

for every received word `V`, then

```text
|Lambda(Int(C,mu),1-a/n)| <= n^B.
```

No `mu B` exponent is lost.

## Proof

Take an interleaved listed codeword

```text
c = (c_1,...,c_mu) in Int(C,mu)
```

that agrees with `U` on at least `a` columns.  Choose a canonical `a`-subset
`S_c` of its common agreement set.  Then `S_c in Fib_Ui(a)` for every row `i`,
so `S_c in Fib_U^cap(a)`.

The map `c -> S_c` is injective when `a >= k`.  Indeed, if two interleaved
codewords map to the same support `S`, then for each row `i` the two row
codewords agree with the same word `U_i` on `S`.  Since two codewords of a
Reed-Solomon code of dimension `k` are equal once they agree on at least `k`
evaluation points, the row codewords are equal for every `i`; hence the
interleaved codewords are equal.

Thus the interleaved list injects into the simultaneous feasible-support fiber.
The `min_i` bound follows from `Fib_U^cap(a) subset Fib_Ui(a)` for every row.

## Ledger Consequence

This bridge does not say that a base-code list-size bound transfers without a
`mu` exponent.  It says that a support-fiber theorem transfers without a `mu`
exponent.

That distinction matters for the L1/L2 program.  The locator local-limit target
in `agents.md` is naturally a bound on feasible agreement supports.  If it is
proved in that form, the interleaved-list ledger in `tex/snarks_v4.tex` can use
the same numerator for every constant arity `mu`, rather than the conservative
product numerator.

For an extension-code presentation `C_F` over an extension `F/B` of degree `e`,
the manuscript identity

```text
|Lambda(C_F,delta)| = |Lambda(Int(C_B,e),delta)|
```

can therefore consume a base-field simultaneous-support bound directly.  The
generated-field entropy ledger is unchanged, but the list-size-over-field term
need not pay a Cartesian-product support exponent if the locator theorem is
available in support-fiber form.

## Follow-Up Checks

- Match the manuscript's locator local-limit assumption to `Fib_U(a)` rather
  than only to `|Lambda(C,delta,U)|`.
- Test tiny `mu=2` examples where product list bounds are loose but
  simultaneous support fibers are small.
- Decide how certificate emitters should print both values: the conservative
  product bound and the sharper support-fiber bridge when its hypothesis is
  available.
