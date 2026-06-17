# M1 Quotient-Periodic Support Overlap Profile

## Claim

Let `D` be a finite set partitioned into `N` disjoint fibers

```text
D = B_1 disjoint union ... disjoint union B_N,
|B_i| = m.
```

Fix `0 <= L <= N`, put `s = Lm`, and let `A_QP` be the quotient-periodic
support family

```text
A_QP = { union_{i in I} B_i : I subset {1,...,N}, |I| = L }.
```

Then

```text
|A_QP| = binom(N,L).
```

For ordered pairs of supports in `A_QP`, the whole overlap profile is the
Johnson overlap profile on the quotient, scaled by the fiber size. More
precisely, for any function `w:{0,...,s}->R`,

```text
sum_{S,T in A_QP} w(|S \ T|)
  = binom(N,L) * sum_{h=0}^{min(L,N-L)}
      binom(L,h) binom(N-L,h) w(hm).
```

Consequently the ordered exchange profile

```text
Delta_j(A_QP)
  = |{(S,T) in A_QP^2 : S != T and |S \ T| = |T \ S| = j}|
```

is

```text
Delta_j(A_QP) = 0       if m does not divide j,

Delta_{hm}(A_QP)
  = binom(N,L) binom(L,h) binom(N-L,h)
```

for `1 <= h <= min(L,N-L)`. The corresponding maximum exchange codegree is

```text
Gamma_j(A_QP) = 0       if m does not divide j,

Gamma_{hm}(A_QP)
  = binom(L,h) binom(N-L,h).
```

Now suppose this support family is used at agreement size `s = k+t`. The strict
M1 high-overlap range is `|S cap T| > k`, equivalently `|S \ T| < t`. Therefore
only quotient exchanges with

```text
1 <= hm <= t-1
```

can contribute to any strict-overlap support-family certificate. In particular,
if `t <= m`, then the quotient-periodic support family has no strict
high-overlap pairs.

More generally, for any line-field size `q`, the strict-overlap weighted
profile that appears in random-line M1 variance certificates evaluates to

```text
R_QP(t,q)
  = sum_{1 <= h <= min(L,N-L), hm <= t-1}
      binom(L,h) binom(N-L,h) q^(t-hm).
```

This is the exact quotient-periodic input to the max-codegree form of the
support-family certificate. The ordered-pair form is

```text
binom(N,L) * R_QP(t,q).
```

Equivalently, at a fixed exact agreement size `s = k+t`, the whole-fiber
quotient-periodic support family at this quotient scale is empty unless
`m | s`. If `m | s`, then `L = s/m` and the formulas above apply. Hence this
exact whole-fiber source has no strict high-overlap pairs whenever either

```text
m does not divide s,
```

or

```text
t <= m.
```

## Status

PROVED.

This is a finite combinatorial support-profile theorem. It does not prove the
M1 residue-line local limit; it supplies the exact overlap ledger for the
quotient-periodic support family that the local-limit problem must separate.

## Proof

Every support in `A_QP` is determined uniquely by a quotient index set
`I subset {1,...,N}` of size `L`. Thus `|A_QP| = binom(N,L)`.

Fix one support

```text
S_I = union_{i in I} B_i.
```

A second support `S_J` differs from `S_I` by exactly `h` quotient fibers if and
only if

```text
|I \ J| = |J \ I| = h.
```

For fixed `I`, the number of such `J` is

```text
binom(L,h) binom(N-L,h),
```

because one chooses the `h` fibers to remove from `I` and the `h` fibers to add
from the complement of `I`. Since every fiber has size `m`,

```text
|S_I \ S_J| = |S_J \ S_I| = hm,

|S_I cap S_J| = (L-h)m = s - hm.
```

Summing over all `binom(N,L)` choices of `I` gives the weighted identity

```text
sum_{S,T in A_QP} w(|S \ T|)
  = binom(N,L) * sum_h binom(L,h) binom(N-L,h) w(hm).
```

Taking `w` to be the indicator of one exchange size `j` gives the displayed
formula for `Delta_j(A_QP)` after deleting the `h=0` diagonal. Maximizing over
the starting support `S_I` gives the same count without the leading
`binom(N,L)`, which is the formula for `Gamma_j(A_QP)`.

For the M1 strict-overlap range, write `s = k+t`. A pair contributes to strict
high-overlap exactly when

```text
|S cap T| > k
  <=> s - |S \ T| > s - t
  <=> |S \ T| < t.
```

For quotient-periodic supports, `|S \ T| = hm`, so the only possible strict
high-overlap exchange sizes satisfy `1 <= hm <= t-1`. Substituting the formula
for `Gamma_{hm}(A_QP)` into a weighted sum with weights `q^(t-hm)` gives
`R_QP(t,q)`, and multiplying by `|A_QP| = binom(N,L)` gives the ordered-pair
version.

Finally, at exact support size `s`, a support that is a union of whole fibers
has size `Lm` for some integer `L`. Thus no such exact-support family exists
unless `m | s`; when it exists, `L = s/m`. The strict-overlap assertion is then
the preceding `hm < t` condition. If `t <= m`, no positive multiple of `m` is
less than `t`, so the strict-overlap profile is empty.

## M1 Impact

This note turns one of the main structured exceptions in the M1 program into an
exact overlap ledger. The quotient-periodic support family is not random, but
its exchange profile, and hence its strict high-overlap profile after
restricting to `j < t`, is completely explicit:

```text
support size               Lm
family size                binom(N,L)
strict exchange sizes      hm < t
max codegree at hm         binom(L,h) binom(N-L,h).
```

Thus after a residue-line argument separates quotient-periodic supports from an
aperiodic family `A`, the quotient-periodic part can be accounted for exactly,
and the remaining M1 task is to prove that the aperiodic part has small
`Delta_j(A)` or `Gamma_j(A)` in the strict range `j < t`.

Two immediate readings are useful.

1. If `m` does not divide the exact support size `s = k+t`, this whole-fiber
   quotient-periodic support family is absent at that exact agreement size.
   This is the exact-support version of dimension/slack dithering.
2. If `t <= m`, quotient-periodic supports have no strict high-overlap pairs.
   In that regime they may still be an algebraic bad-slope source, but they do
   not create strict-overlap covariance in the random-line support-family
   ledger.
3. If `t > m`, all strict-overlap mass comes from whole-fiber exchanges. The
   correction term is the finite quotient sum `R_QP(t,q)`, not a full
   Johnson-sphere sum over point exchanges.

This makes the quotient-periodic exception quantitatively separable from the
aperiodic local-limit problem targeted by M1.

## Suggested Next Step

For a concrete M1 scanner, label each support by its quotient-fiber content and
emit three statistics for each support class:

```text
|A|,    Delta_j(A),    Gamma_j(A)    for 1 <= j < t.
```

The quotient-periodic class should match the closed formulas above. Any excess
strict-overlap profile in the remaining supports is then a direct witness for
the aperiodic obstruction that a future local-limit proof must control.
