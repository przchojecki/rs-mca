# M1 Average Support-Collinearity Bound

## Claim

Let `F` be a finite field of size `q`, let `D` be an evaluation set of size
`n`, and let `C = RS[F,D,k]`. Fix an agreement size

```text
s = k + t,  1 <= t <= n - k.
```

For each support `S subset D` with `|S| = s`, let `I_S(v)` be the unique
degree-`< s` interpolant of `v|S`, and define

```text
Pi_S(v) = (coeff_X^k I_S(v), ..., coeff_X^(s-1) I_S(v)) in F^t.
```

Choose `f,g` independently and uniformly from `F^D`. Let `Inc_t(f,g)` be the
set of exact-support MCA incidences

```text
(S,z),  |S| = k + t,
Pi_S(f) + z Pi_S(g) = 0,
not both Pi_S(f), Pi_S(g) vanish.
```

Then

```text
E |Inc_t(f,g)|
  = binom(n,k+t) * (q^t - 1) / q^(2t - 1)
  <= binom(n,k+t) / q^(t - 1).
```

Let `X = |Inc_t(f,g)|`, let `N_s = binom(n,k+t)`, and put

```text
p_t = (q^t - 1) / q^(2t - 1).
```

Then support pairs with intersection `< k` contribute exactly independently,
and the second moment obeys

```text
Var X
  <= N_s p_t(1 - p_t)
     + N_s * sum_{r=k}^{k+t-1} binom(k+t,r) binom(n-k-t,k+t-r)
         q^(r-k-2t+2).
```

Thus all possible random-line covariance is confined to pairs of supports
intersecting in at least `k` points.

If `Bad_t(f,g)` is the set of distinct support-wise MCA-bad slopes at radius
`delta = 1 - (k+t)/n`, then

```text
E |Bad_t(f,g)|/q
  <= binom(n,k+t) * (q^t - 1) / q^(2t)
  <= binom(n,k+t) / q^t.
```

Consequently, for the radius `delta = 1 - (k+t)/n`,

```text
Pr[ f + z g has any support-wise MCA-bad slope at radius delta ]
  <= binom(n,k+t) * (q^t - 1) / q^(2t - 1).
```

This is an average-case statement for random lines. It is not a worst-case M1
local-limit theorem.

## Status

PROVED.

## Existing Paper Dependency

This supports Paper B's M1 residue-line local-limit problem. Paper B reduces
all-line MCA to residue-line packing and carries the tangent floor and
quotient-periodic floors separately. The lemma here gives the exact random-line
baseline behind that picture: for `t >= 2`, support collinearity has codimension
`t - 1` over the line field.

## Proof

Fix a support `S` of size `s = k + t`.

The interpolation map

```text
F^S -> F_{<s}[X],  v|S -> I_S(v)
```

is a linear isomorphism. Projection to the top `t` coefficients

```text
F_{<s}[X] -> F^t
```

is surjective. Therefore, when `v` is uniform in `F^D`, the vector `Pi_S(v)`
is uniform in `F^t`. For independent uniform `f,g`, the pair

```text
(A,B) = (Pi_S(f), Pi_S(g))
```

is uniform in `F^t x F^t`.

For fixed `S`, count the number of pairs `(A,B)` that contribute a slope.
If `B = 0`, then either `A = 0`, in which case the noncontainment condition
fails, or `A != 0`, in which case no slope solves `A + zB = 0`.

If `B != 0`, then a slope exists exactly when `A` lies in the one-dimensional
span of `B`. There are `q^t - 1` choices for `B` and `q` choices for `A` in
that span. Each such pair gives exactly one slope, namely `z = -lambda` when
`A = lambda B`. Hence the number of contributing pairs is

```text
q * (q^t - 1).
```

Dividing by the total number `q^(2t)` of pairs gives, for this fixed support,

```text
Pr[S contributes an incidence]
  = (q^t - 1) / q^(2t - 1).
```

A fixed support contributes at most one slope, so this is also the expected
number of `(S,z)` incidences contributed by this `S`. Summing over the
`binom(n,k+t)` supports gives

```text
E |Inc_t(f,g)|
  = binom(n,k+t) * (q^t - 1) / q^(2t - 1).
```

The inequality follows from `(q^t - 1)/q^(2t - 1) <= 1/q^(t - 1)`.

## Exact-Support Reduction for the Probability Bound

At radius `delta = 1 - (k+t)/n`, any support-wise MCA-bad slope has a witness
of exactly `k+t` points. Indeed, if a larger support `S` witnesses badness,
then `f + z g` is code-explained on every subset of `S`. Since `f` and `g` are
not both code-explained on `S`, one of them is not degree-`< k` on `S`; choose a
`(k+1)`-subset on which that failure already occurs and extend it inside `S`
to a subset of size `k+t`. This smaller support still explains `f + z g` but
still does not explain both `f` and `g`.

The `(k+1)`-subset exists because otherwise any fixed `k` points of `S` would
interpolate a degree-`< k` polynomial, and adding each remaining point one at a
time would force the same polynomial to agree with the word on all of `S`.

Therefore the event that any bad slope exists at radius `1 - (k+t)/n` is
contained in the event `Inc_t(f,g) != empty`. Markov's inequality gives

```text
Pr[Inc_t(f,g) != empty] <= E |Inc_t(f,g)|,
```

which is the displayed probability bound.

The expected bad-slope density bound follows from the same incidence count:
every distinct bad slope has at least one exact-support incidence, so
`|Bad_t(f,g)| <= |Inc_t(f,g)|`. Dividing the expectation by `q` gives

```text
E |Bad_t(f,g)|/q
  <= E |Inc_t(f,g)|/q
  = binom(n,k+t) * (q^t - 1) / q^(2t).
```

## Support-Overlap Second Moment

Let `X = |Inc_t(f,g)|`, and for each support `S` of size `s = k+t` let `I_S`
be the indicator that `S` contributes an exact-support incidence. The preceding
calculation gives

```text
Pr[I_S = 1] = p_t = (q^t - 1) / q^(2t - 1).
```

For two supports `S,T` of size `s`, put `r = |S cap T|`.

First suppose `r < k`. The combined linear map

```text
v -> (Pi_S(v), Pi_T(v))
```

is surjective onto `F^t x F^t`. Indeed, the kernel consists of words whose
restrictions to `S` and `T` are both degree-`< k`. On `S union T`, such a word
is specified by a pair of degree-`< k` polynomials that agree on the `r` common
points. Since `r < k`, there are `q^k q^(k-r)` such pairs. The union has size
`2s-r = 2k+2t-r`, so the kernel dimension is `2k-r` and the rank is `2t`.
Thus the two top-coefficient vectors are independent uniform vectors in
`F^t`, and the same holds separately for `f` and `g`. Consequently,

```text
Pr[I_S = I_T = 1] = p_t^2        when |S cap T| < k.
```

Now suppose `r >= k`, and write `h = r-k`. The same kernel count shows that
the rank of `v -> (Pi_S(v),Pi_T(v))` is `2t-h`: the two degree-`< k`
interpolants must be identical once they agree on at least `k` points.

For fixed `g`, write

```text
B = (Pi_S(g), Pi_T(g))
```

in the image subspace `V` of dimension `2t-h`. For `S` and `T` both to
contribute incidences, the corresponding vector

```text
A = (Pi_S(f), Pi_T(f))
```

must lie in

```text
span(Pi_S(g)) x span(Pi_T(g)).
```

Intersecting this two-parameter set with `V` gives at most `q^2` choices for
`A`. Since `B` ranges over at most `q^(2t-h)` image values and `A` is uniform
in the same image subspace, this gives the crude but explicit high-overlap
bound

```text
Pr[I_S = I_T = 1] <= q^(h - 2t + 2)
                  = q^(r - k - 2t + 2)
```

for distinct supports with `k <= r <= k+t-1`.

For each fixed `S`, the number of supports `T` with `|S cap T| = r` is

```text
binom(k+t,r) binom(n-k-t,k+t-r).
```

Combining the exact independence below `k` with the high-overlap bound gives
the variance estimate stated in the claim:

```text
Var X
  <= N_s p_t(1 - p_t)
     + N_s * sum_{r=k}^{k+t-1} binom(k+t,r) binom(n-k-t,k+t-r)
         q^(r-k-2t+2).
```

Equivalently,

```text
Var X / (E X)^2
  <= (1 - p_t)/(N_s p_t)
     + (1/(N_s p_t^2))
       * sum_{r=k}^{k+t-1} binom(k+t,r) binom(n-k-t,k+t-r)
           q^(r-k-2t+2).
```

Whenever this relative variance tends to zero, `X / E X -> 1` in probability.
The criterion isolates the same threshold that appears throughout the
Reed-Solomon theory: support overlaps below `k` behave randomly, while
overlaps of size at least `k` are the only possible source of structured
covariance.

## Constants and Interpretation

The bound has three useful regimes.

- `t = 1`: the factor is `1 - 1/q`. A random support with nonzero direction
  obstruction contributes a slope. This is the linear-algebra shadow of the
  tangent floor and explains why the M1 conjecture must carry an additive
  `n/q`-scale correction.
- `t = 2`: each support contributes with probability approximately `1/q`.
  This is the first genuinely codimension-one collinearity regime.
- general `t`: the support-collinearity cost is approximately `q^(t-1)`.
  Thus random lines have no bad support with high probability once
  `q^(t-1)` dominates `binom(n,k+t)`, while their expected MCA contribution
  is already at most the entropy-scale quantity `binom(n,k+t)/q^t`.

Equivalently, for any `epsilon > 0`, if

```text
q^(t - 1) >= epsilon^(-1) * binom(n,k+t),
```

then a random line has no support-wise MCA-bad slope at radius
`1 - (k+t)/n` with probability at least `1 - epsilon`.

This is much stronger than the conjectured worst-case polynomial packing bound,
but only for random `f,g`. The gap between this average-case lemma and the M1
worst-case problem is precisely where tangent, quotient-periodic, and
structured residue-line families live.

## Ledger Impact

This lemma gives a rigorous random-line baseline for the M1 ledger:

```text
expected support/slope incidences
  = binom(n,k+t) / q^(t-1)  up to the factor 1 - q^(-t).

expected bad-slope density
  <= binom(n,k+t) / q^t.
```

The second-moment bound adds the overlap ledger:

```text
random support covariance starts only at |S cap T| >= k.
```

Together these formulas justify treating the aperiodic part of residue-line
packing as an incidence problem rather than as an arbitrary list-size problem.
They also identify the exact obstruction to promoting the estimate to a
worst-case theorem: one must rule out line data for which many high-overlap
supports have aligned top-coefficient vectors `Pi_S(f)` and `Pi_S(g)` after the
known tangent and quotient-periodic families are separated.

## Suggested Next Step

The natural follow-up is a scanner that, for tiny fields, computes the vectors
`Pi_S(f), Pi_S(g)` over all supports of size `k+t`, records the distinct slopes
arising from collinearity, and labels whether each support is tangent,
quotient-periodic, or aperiodic. The average formula above gives an exact
baseline for interpreting those scans.
