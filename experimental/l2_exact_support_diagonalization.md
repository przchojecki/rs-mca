# L2 Exact-Support Diagonalization Lemma

## Claim

Let `C subset F^D` be a code of length `n`, let `U:D -> F`, and fix an
agreement size `a`. For a codeword `c in C`, write

```text
A_U(c) = { x in D : c(x) = U(x) }.
```

Assume:

1. every support of size at least `a` determines at most one codeword of `C`;
2. a family `L` of base codewords satisfies `|A_U(c)| = a` for every `c in L`.

For the equal-row interleaved received word

```text
U^Delta = (U,...,U) in (F^D)^mu,
```

consider interleaved codewords whose rows all come from `L`. Such a tuple is
within column-distance radius `1 - a/n` of `U^Delta` if and only if all its
rows are the same codeword. Hence the exact-support family contributes

```text
|L|
```

interleaved listed codewords, not `|L|^mu`.

For Reed-Solomon codes `RS[F,D,k]`, condition 1 holds whenever `a >= k`.

## Status

PROVED.

## Existing Paper Dependency

This targets the L2 question in `agents.md`: whether lower bounds multiply
under interleaving or share the same support structure. The answer for
exact-support certificates is precise: the equal-row lift is diagonal unless
there are repeated agreement supports or accidental larger agreements.

## Proof

Let

```text
c = (c_1,...,c_mu) in C^mu
```

with each `c_i in L`. The common agreement set of `c` with `U^Delta` is

```text
A_U(c_1) cap ... cap A_U(c_mu).
```

The tuple is within radius `1 - a/n` exactly when this intersection has size at
least `a`.

Each set `A_U(c_i)` has size exactly `a`. Therefore

```text
|A_U(c_1) cap ... cap A_U(c_mu)| >= a
```

if and only if all agreement sets are equal:

```text
A_U(c_1) = ... = A_U(c_mu).
```

By condition 1, a support of size `a` determines at most one codeword. Hence
all `c_i` are the same codeword. Conversely, every diagonal tuple

```text
(c,...,c),  c in L,
```

has common agreement set `A_U(c)` of size `a`, so it is listed. Thus the
number of listed tuples coming from `L^mu` is exactly `|L|`.

For `C = RS[F,D,k]`, if two codewords agree on at least `k` points, then their
difference is a degree-`< k` polynomial with at least `k` roots and is
therefore zero. Thus condition 1 holds for every `a >= k`.

## Quotient-Locator Consequence

Suppose a quotient-locator certificate produces base codewords indexed by
fixed-size quotient subsets

```text
B subset Q,   |B| = ell,
```

with certified agreement support

```text
S_B = pi^(-1)(B) subset D,
```

where each quotient fiber has size `h`, so `|S_B| = h ell = a`.

For equal-row interleaving, the certified common support of a tuple

```text
(c_B1,...,c_Bmu)
```

is contained in

```text
S_B1 cap ... cap S_Bmu = pi^(-1)(B_1 cap ... cap B_mu).
```

This certified support has size `h |B_1 cap ... cap B_mu|`, which is at least
`h ell = a` only when

```text
B_1 = ... = B_mu.
```

Therefore a quotient-locator lower-bound certificate with exact supports
certifies only the diagonal interleaved lower bound. It does not certify the
Cartesian-product lower bound.

Any genuine product-size interleaved lower bound would need extra structure:
for example, accidental agreement outside the locator-certified supports, a
larger radius with smaller required common agreement, repeated supports, or
rows chosen from correlated but non-identical received words.

## Ledger Impact

This gives a deterministic counterpart to the random simultaneous-support
baseline:

- upper-bound ledgers should avoid the trivial product exponent when a
  support-fiber theorem is available;
- lower-bound ledgers should also avoid assuming quotient-core obstructions
  multiply under equal-row interleaving;
- the operational quantity is the common support intersection, not the product
  of row-wise list sizes.

For protocol accounting, this means a base quotient-core obstruction of size
`L` gives a diagonal interleaved obstruction of size `L` for equal rows by
default. Treating it as `L^mu` requires a separate certificate proving that
off-diagonal tuples retain a large common agreement support.

## Non-Claim

The lemma does not rule out product-size interleaved lower bounds in other
models. It rules them out for exact-support lower-bound certificates lifted by
identical rows at the same agreement threshold. Interleaved lower bounds with
different row words, larger supports, or accidental extra agreements remain
separate objects to certify.
