# F1 Fixed-Rate Extension-Line Counterexample

## Claim

Let `p` be an odd prime, let `B = F_p`, and let

```text
F = B[alpha],        alpha^2 = d,
```

where `d in B` is a nonsquare. Let `H = B^*`, so `n = p-1`, and let
`C_F = RS[F,H,k]`. Put

```text
a = k + 1,        delta = 1 - a/n,
```

with `2 <= a <= n`. Define the extension-valued line over `H`

```text
f(x) = x^a / (x - alpha),
g(x) = -1 / (x - alpha),
u_z(x) = f(x) + z g(x) = (x^a - z) / (x - alpha).
```

For every `a`-subset `S subset H`, write

```text
L_S(X) = product_{s in S} (X - s),
Q_S(X) = X^a - L_S(X),
z_S = Q_S(alpha).
```

Then `z_S` is support-wise MCA-bad at radius `delta` for the line `f+zg`.
Moreover, after fixing any `(a-2)`-subset `T subset H`, the slopes

```text
z_{T union {x,y}},        {x,y} subset H \ T
```

are distinct as the unordered pair `{x,y}` varies. Consequently

```text
emca(C_F, delta)
  >= binom(p-a+1, 2) / p^2.
```

In particular, along any fixed-rate sequence

```text
k = floor(rho (p-1)),        0 < rho < 1,
```

one has `a = k+1` and

```text
emca(C_F, 1 - (k+1)/(p-1))
  >= (1-rho)^2/2 - o(1).
```

This gives a fixed-rate counterexample to the unrestricted
numerator-preserving extension-line lift: the base-field MCA numerator can be
taken trivially as `p`, while the extension-valued line over `F_{p^2}` has
constant bad-slope density, not `p^{1+o(1)}/p^2`.

More generally, the same construction works over any finite extension
`F/F_p` containing an element `alpha notin F_p`. If `|F|=p^e` with `e >= 2`,
then

```text
emca(C_F, delta)
  >= binom(p-a+1, 2) / p^e,

|F| * emca(C_F, delta)
  >= binom(p-a+1, 2).
```

Thus the extension-line numerator forced by this sigma-one family is
`Theta(p^2)` at fixed rate, independent of the extension degree. For `e=2`
this is a constant-density counterexample. For `e>2` the density is diluted by
the larger challenge field, but it is still a factor `Theta(p)` larger than
the numerator `p` supplied by a base-field MCA bound.

## Status

PROVED / COUNTEREXAMPLE.

This is a sigma-one counterexample, with agreement size `k+1`. It does not
refute a repaired extension-line theorem in the corrected-reserve regime
`sigma >= C n/log n`. It does refute any unrestricted route that bounds
extension-line MCA by taking a base-field numerator and dividing by the larger
extension challenge field. The extension-degree corollary shows that the issue
is numerator preservation, not merely constant density in quadratic extensions.

## Proof

First note that `alpha notin B`, so `x - alpha` is nonzero for every
`x in H`.

Fix an `a`-subset `S subset H`. Since `L_S` is monic of degree `a`,
`Q_S = X^a - L_S` has degree at most `a-1 = k`. By definition,
`Q_S(alpha) = z_S`, so `Q_S(X)-z_S` is divisible by `X-alpha`. Put

```text
P_S(X) = (Q_S(X) - z_S) / (X - alpha).
```

Then

```text
deg P_S <= k - 1,
```

so `P_S` is a codeword polynomial for `C_F`. For `x in S`, `L_S(x)=0`, hence
`Q_S(x)=x^a`, and therefore

```text
P_S(x)
  = (x^a - z_S)/(x-alpha)
  = u_{z_S}(x).
```

Thus the line point `u_{z_S}` is code-explained on `S`.

It remains to prove same-support noncontainment. Suppose, for contradiction,
that `g|S` agrees with a degree-`<k` polynomial `G`. Then

```text
R(X) = (X-alpha)G(X) + 1
```

has degree at most `k` and vanishes on all `a=k+1` points of `S`. Hence
`R` is identically zero. But `R(alpha)=1`, a contradiction. Thus `g` is not
code-explained on `S`, so no pair of degree-`<k` codewords explains `f` and
`g` simultaneously on `S`. Therefore every `z_S` is support-wise MCA-bad.

Now fix `T subset H` with `|T| = a-2`. Let

```text
C_T = product_{t in T} (alpha - t).
```

This is nonzero. For distinct `x,y in H\T`,

```text
L_{T union {x,y}}(alpha)
  = C_T (alpha-x)(alpha-y)
  = C_T (alpha^2 - (x+y)alpha + xy).
```

If two unordered pairs `{x,y}` and `{x',y'}` outside `T` give the same slope,
then their locator values at `alpha` agree, and hence

```text
alpha^2 - (x+y)alpha + xy
  = alpha^2 - (x'+y')alpha + x'y'.
```

Rearranging gives

```text
((x+y) - (x'+y')) alpha = xy - x'y'.
```

The left side is a `B`-multiple of `alpha` and the right side lies in `B`.
Since `1, alpha` are linearly independent over `B`, both sides are zero. Thus

```text
x+y = x'+y',        xy = x'y'.
```

The unordered pair is determined by its sum and product, so
`{x,y} = {x',y'}`. This proves injectivity on the slice through `T`.

The same injectivity proof only used the `B`-linear independence of `1` and
`alpha`; it did not use that `F` is quadratic. Therefore it applies verbatim in
any finite extension `F/F_p` with `alpha notin F_p`.

The number of available points outside `T` is

```text
|H \ T| = (p-1) - (a-2) = p-a+1.
```

Therefore there are at least

```text
binom(p-a+1, 2)
```

distinct bad slopes in `F`. If `|F|=p^e`, this gives the extension-degree
lower bound

```text
emca(C_F, delta) >= binom(p-a+1, 2) / p^e.
```

For fixed rate `k=floor(rho(p-1))`, the numerator ratio

```text
binom(p-a+1, 2) / p^2
```

tends to `(1-rho)^2/2`, since `a=k+1`. Equivalently,
`|F|*emca(C_F,delta)` is at least `((1-rho)^2/2-o(1))p^2` for every fixed
extension degree `e>=2`.

Finally, over the base field `B`, the trivial bound

```text
emca(C_B, delta) <= 1 = p/p
```

is a numerator-`p` bound. An unrestricted numerator-preserving lift would turn
that into an extension-field estimate of size `p^{1+o(1)}/p^e`. The lower
bound above has numerator `Theta(p^2)`, so even in higher extensions the
unrestricted same-numerator lift undercounts the forced extension-valued
residue-line numerator by a factor `Theta(p)`.

## Ledger Impact

This proof isolates the exact obstruction in the F1 direction. The bad line is
not a base-valued line whose slopes are merely being reinterpreted in a larger
field. Its denominator `X-alpha` is genuinely extension-valued, and the bad
slopes record base-field pair sums and products through evaluation at `alpha`.

Consequently a protocol ledger cannot safely take an MCA numerator proved over
`q_line = |B|` and divide it by an extension challenge field `|F|` for arbitrary
`F`-valued lines. The sigma-one extension numerator is already quadratic in
`|B|`, even when `|F|` is a higher extension. A repaired F1 theorem must
either:

- prove MCA directly over the actual extension line field;
- add an extension-valued residue-line numerator term;
- restrict to a corrected-reserve regime where this sigma-one construction is
  excluded; or
- reformulate extension-valued lines as structured affine-subspace or
  interleaved-base objects over `B`.

## Relation To Existing Experimental Material

This note extracts a clean proof from the F1 audit bundle. The existing
verifier

```text
experimental/2026-06-17-codex-f1-l1-audit/verifiers/verify_f1_fixed_rate_slice.py
```

checks finite instances of the injective slice used above. The theorem here is
the general finite-field proof of that slice mechanism.
