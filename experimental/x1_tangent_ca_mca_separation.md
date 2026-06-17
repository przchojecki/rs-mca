# X1 Tangent Separation Between CA and Support-Wise MCA

## Claim

Let `C = RS[F,D,k]`, with `|D| = n`, `|F| = q`, and let
`0 < delta < 1 - k/n`. Put

```text
m = floor(delta n).
```

Assume `m >= 1`. Then there are words `f,g in F^D` and at least `m` distinct
slopes `z` such that:

1. `z` is support-wise MCA-bad for the line `f + z g` at radius `delta`;
2. the same pair `(f,g)` has no CA-bad slopes at no-proximity-loss radius
   `delta`, because `(f,g)` is already `delta`-close to `C^2`.

Consequently, a CA-to-MCA bridge cannot be true without an additive tangent
correction of order `floor(delta n)/q`, or an equivalent exclusion of tangent
support patterns.

## Status

PROVED.

This is a pairwise separation. It does not say that the global CA error
`eca(C,delta)` is zero; it says that the tangent slopes contributing to
support-wise MCA for this line are invisible to the CA predicate for the same
line.

## Construction

Choose a set `E subset D` with `|E| = m`, and choose an injective map

```text
a : E -> F.
```

This is possible because `m <= n <= q`. Fix two codewords `P1,P2 in C`. Define
error words `e_f,e_g` by

```text
e_f(x) = a(x)  for x in E,      e_f(x) = 0  for x notin E,
e_g(x) = 1     for x in E,      e_g(x) = 0  for x notin E,
```

and set

```text
f = P1 + e_f,       g = P2 + e_g.
```

For each `x in E`, define

```text
z_x = -a(x),        S_x = (D \ E) union {x}.
```

The slopes `z_x` are distinct because `a` is injective.

## MCA Badness

First, `S_x` is large enough:

```text
|S_x| = n - m + 1 >= (1 - delta)n.
```

On `S_x`, the line point `f + z_x g` agrees with the codeword
`P1 + z_x P2`. Indeed, outside `E` both error words vanish, while at the
point `x`,

```text
e_f(x) + z_x e_g(x) = a(x) - a(x) = 0.
```

Thus `f + z_x g` is code-explained on `S_x`.

It remains to show support-wise noncontainment on `S_x`. Since
`delta < 1 - k/n`,

```text
m = floor(delta n) < n - k,
```

so `|D \ E| = n - m > k`. If a degree-`< k` codeword explained `f` on `S_x`,
then it would agree with `P1` on the more-than-`k` points of `D \ E`, hence it
would equal `P1`. Similarly, any degree-`< k` codeword explaining `g` on
`S_x` would equal `P2`. But at the point `x`, `g(x) = P2(x) + 1`, so `P2`
does not explain `g` on `S_x`. Therefore no pair of codewords explains
`f` and `g` simultaneously on `S_x`.

Hence every `z_x` is support-wise MCA-bad at radius `delta`, giving at least
`m` bad slopes and the lower bound

```text
emca(C,delta) >= m/q
```

from this line family alone.

## CA Invisibility

For correlated agreement at the same no-proximity-loss radius `delta`, compare
the pair `(f,g)` with the interleaved codeword `(P1,P2)`. The two words differ
from `(P1,P2)` only on the set `E`, so the interleaved column distance is

```text
dist_2((f,g), C^2) <= |E|/n = m/n <= delta.
```

The CA-bad predicate requires the pair distance from `C^2` to be strictly
larger than `delta`. Therefore this fixed pair `(f,g)` has no CA-bad slopes at
radius `delta`, even though the `m` slopes above are support-wise MCA-bad.

For those same slopes, the line point is actually close to `C`: it agrees with
`P1 + z_x P2` on `S_x`, hence has relative distance at most `(m - 1)/n`.
The CA predicate misses them solely because the pair is globally close to
`C^2`.

## Ledger Impact

This explains why the X1 direction "list/CA implies MCA" cannot be a clean
equivalence at the same radius without a support-wise correction. CA only asks
whether the pair `(f,g)` is globally farther than `delta` from `C^2`. MCA asks
whether the same support that explains `f + z g` also explains `f` and `g`
separately. Tangent supports exploit exactly the gap between these predicates.

The unavoidable correction has the same scale as Paper B's tangent floor:

```text
floor(delta n) / q.
```

Thus any positive MCA theorem should either:

- carry an additive `n/q`-scale tangent term;
- quotient out or separately certify tangent support patterns; or
- strengthen the CA predicate to remember the explaining support.

This is also consistent with the M1 residue-line picture: the tangent floor is
the `t = 1` support-collinearity regime, where every nonzero direction
obstruction is automatically collinear with the anchor obstruction.

## Non-Claim

This note does not compare the global maxima `eca(C,delta)` and
`emca(C,delta)` in the opposite direction. The known implication

```text
eca(C,delta) <= emca(C,delta)
```

is unaffected. The point is that the converse cannot be obtained by inspecting
only CA-bad slopes of the same line; support-wise MCA contains tangent
phenomena that CA deliberately excludes.
