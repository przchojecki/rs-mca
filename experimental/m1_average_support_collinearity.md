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

Equivalently, writing `s = k+t`,

```text
H_t(n,k,q)
  = sum_{j=1}^t binom(s,j) binom(n-s,j) q^(2-t-j),
```

one has

```text
Var X / (E X)^2
  <= (1 - p_t)/(N_s p_t) + H_t(n,k,q)/(N_s p_t^2).
```

For `q >= 2`, if along a parameter sequence

```text
N_s / ( q^(t-1)
        + q^t * sum_{j=1}^t (s(n-s)/q)^j / (j!)^2 ) -> infinity,
```

then `X / E X -> 1` in probability.

There is also a slope-resolved second moment. For fixed `z in F`, let
`X_z` be the number of supports contributing the slope `z`, and put

```text
a_t = q^(-t),        p_z = a_t(1 - a_t).
```

Then

```text
E X_z = N_s p_z.
```

For two supports with intersection `r`, define

```text
alpha_r =
  q^(-2t)             if r < k,
  q^(r-k-2t)          if k <= r <= k+t.
```

The exact second moment is

```text
E X_z^2
  = N_s * sum_{r=0}^{k+t} binom(k+t,r) binom(n-k-t,k+t-r)
      alpha_r(1 - 2q^(-t) + alpha_r).
```

In particular, fixed-slope covariance vanishes for support pairs intersecting
in at most `k` points.

In particular, if

```text
N_s / ( q^t
        + sum_{j=1}^{t-1} binom(k+t,j) binom(n-k-t,j) q^(t-j) )
  -> infinity,
```

then `|Bad_t(f,g)|/q -> 1` in probability.

Quantitatively, for `q >= 2`, put

```text
B_t = (1 - p_z)/(N_s p_z)
      + (4/N_s) * sum_{j=1}^{t-1}
          binom(k+t,j) binom(n-k-t,j) q^(t-j).
```

Then the missing-slope density satisfies

```text
E[1 - |Bad_t(f,g)|/q] <= B_t,

Pr[ |Bad_t(f,g)|/q <= 1 - epsilon ] <= B_t / epsilon.
```

More generally, the same slope-resolved estimate holds for any fixed support
subfamily. Let `A` be a deterministic family of `M >= 1` supports of size
`s = k+t`, and define the ordered strict high-overlap profile

```text
Delta_j(A)
  = |{(S,T) in A^2 : S != T and |S \ T| = |T \ S| = j}|,
      1 <= j <= t-1.
```

When `t = 1`, these strict-overlap sums are empty and are read as zero.

Let `X_z(A)` count supports in `A` contributing the fixed slope `z`, and let
`Bad_t(A;f,g)` be the set of slopes witnessed by supports in `A`. Then

```text
E X_z(A) = M p_z
```

and the strict high-overlap profile gives the exact variance identity

```text
Var X_z(A)
  = M p_z(1 - p_z)
    + sum_{j=1}^{t-1} Delta_j(A) K_j,

K_j = q^(-t-j)(1 - 2q^(-t) + q^(-t-j)) - p_z^2.
```

In particular,

```text
Var X_z(A) / (M p_z)^2
  <= (1 - p_z)/(M p_z)
     + (4/M^2) * sum_{j=1}^{t-1} Delta_j(A) q^(t-j).
```

Consequently, with

```text
B_t(A) = (1 - p_z)/(M p_z)
         + (4/M^2) * sum_{j=1}^{t-1} Delta_j(A) q^(t-j),
```

one has

```text
E[1 - |Bad_t(A;f,g)|/q] <= B_t(A),

Pr[ |Bad_t(A;f,g)|/q <= 1 - epsilon ] <= B_t(A) / epsilon.
```

A coarser sufficient form uses the maximum exchange codegree. If

```text
Gamma_j(A)
  = max_{S in A} |{T in A : |S \ T| = |T \ S| = j}|,
      1 <= j <= t-1,
```

then `Delta_j(A) <= M Gamma_j(A)`, so the same conclusion holds with

```text
B_t^max(A) = (1 - p_z)/(M p_z)
             + (4/M) * sum_{j=1}^{t-1} Gamma_j(A) q^(t-j).
```

The first-moment side also restricts:

```text
E |Bad_t(A;f,g)|/q <= M / q^t.
```

The same pair kernel also gives a finite lower certificate for the expected
bad-slope density.  Put

```text
P_j = q^(-t-j)(1 - 2q^(-t) + q^(-t-j)),
        1 <= j <= t-1,
```

and define the ordered-pair correction

```text
C_t(A)
  = (M(M-1) - sum_{j=1}^{t-1} Delta_j(A)) p_z^2
    + sum_{j=1}^{t-1} Delta_j(A) P_j.
```

Then, for every fixed slope `z`,

```text
Pr[z in Bad_t(A;f,g)]
  >= M p_z - C_t(A)/2,
```

and hence

```text
E |Bad_t(A;f,g)|/q
  >= max(0, M p_z - C_t(A)/2).
```

This is just the first two Bonferroni terms applied to `X_z(A)>0`, using the
exact ordered pair probabilities above.  It is useful in the sparse and
transition regimes: if `M p_z` is small and `C_t(A)=o(M p_z)`, then the
expected distinct-slope density is asymptotic to the support-incidence
density `M p_z`.

In the slack-one case `t = 1`, the strict-overlap profile is empty. Therefore,
for every deterministic support family `A` of `k+1` point supports and every
fixed slope `z`,

```text
Var X_z(A) = M p_z(1 - p_z),        p_z = (q - 1)/q^2.
```

Consequently,

```text
E[1 - |Bad_1(A;f,g)|/q] <= (1 - p_z)/(M p_z) <= 2q/M.
```

Thus slack-one random-line slope density is governed only by the number of
available supports: `M/q -> 0` gives zero density in probability, while
`M/q -> infinity` gives density one in probability.

Thus a fixed support family has the same random-line phase diagram with
`binom(n,k+t)` replaced by its size and with the full Johnson-sphere correction
replaced by its measured strict high-overlap profile, or more coarsely by its
maximum exchange codegrees. This is the natural certificate format for
separating tangent, quotient-periodic, and aperiodic support families.

Combining this with the first-moment upper bound gives the random-line
slope-density phase diagram. Along any parameter sequence with `q >= 2`,

```text
N_s / q^t -> 0
```

implies `|Bad_t(f,g)|/q -> 0` in probability, while

```text
N_s / ( q^t
        + sum_{j=1}^{t-1} binom(k+t,j) binom(n-k-t,j) q^(t-j) )
  -> infinity
```

implies `|Bad_t(f,g)|/q -> 1` in probability. In particular, for fixed `t`
and `s(n-s)/q -> 0`, the transition is sharp at the entropy scale
`binom(n,k+t) ~ q^t`.

In logarithmic form, when the strict high-overlap correction is negligible,

```text
t log q - log binom(n,k+t) -> +infinity
```

is the random-line safe side, while

```text
log binom(n,k+t) - t log q -> +infinity
```

is the random-line failure side.

If `Bad_t(f,g)` is the set of distinct support-wise MCA-bad slopes at radius
`delta = 1 - (k+t)/n`, then

```text
E |Bad_t(f,g)|/q
  <= binom(n,k+t) * (q^t - 1) / q^(2t)
  <= binom(n,k+t) / q^t.
```

Consequently, for the radius `delta = 1 - (k+t)/n`,

```text
Pr[ Bad_t(f,g) is nonempty at radius delta ]
  <= binom(n,k+t) * (q^t - 1) / q^(2t - 1).
```

There is also a fixed-base version that separates the zero slope. For fixed
`f`, define

```text
A_t(f) = |{S subset D: |S| = k+t and Pi_S(f) = 0}|.
```

If `g` is uniform in `F^D`, then

```text
E_g |Inc_t(f,g)|
  = A_t(f)(1 - q^(-t)) + (N_s - A_t(f))(q - 1)/q^t.
```

If `Inc_t^*(f,g)` denotes the same incidence set with the zero slope removed,
then

```text
E_g |Inc_t^*(f,g)|
  = (N_s - A_t(f))(q - 1)/q^t
  <= N_s / q^(t - 1).
```

Thus the base-word support-list mass contributes only to the zero slope
`z = 0`; after that slope is removed, a random direction pays the same
codimension `t-1` support-collinearity cost uniformly for every fixed base
word `f`.

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

## Fixed-Base Random Direction and Zero-Slope Separation

The random-line formula can be conditioned on one endpoint of the line. Fix
`f in F^D` and choose only `g` uniformly at random. Let

```text
A_t(f) = |{S subset D: |S| = k+t and Pi_S(f) = 0}|.
```

For a fixed support `S`, put `A = Pi_S(f)` and `B = Pi_S(g)`. As `g` varies,
`B` is uniform in `F^t`.

If `A = 0`, then `A + zB = 0` contributes only at the zero slope `z = 0`.
It contributes exactly when `B != 0`; when `B = 0`, both `f` and `g` are
degree-`< k` on `S`, so the noncontainment condition fails. Therefore

```text
Pr_g[S contributes | Pi_S(f) = 0] = 1 - q^(-t).
```

If `A != 0`, then a slope exists exactly when `B` is a nonzero scalar multiple
of `A`. There are `q-1` such vectors `B`, each giving one nonzero slope. Hence

```text
Pr_g[S contributes | Pi_S(f) != 0] = (q - 1)/q^t.
```

Summing over supports gives the exact conditional incidence formula

```text
E_g |Inc_t(f,g)|
  = A_t(f)(1 - q^(-t)) + (N_s - A_t(f))(q - 1)/q^t.
```

Removing the zero slope removes the entire `Pi_S(f)=0` contribution, so

```text
E_g |Inc_t^*(f,g)|
  = (N_s - A_t(f))(q - 1)/q^t
  <= N_s / q^(t - 1).
```

For distinct bad slopes this gives the sharper fixed-base density ledger

```text
E_g |Bad_t(f,g) \ {0}| / q
  <= (N_s - A_t(f))(q - 1) / q^(t+1),

E_g |Bad_t(f,g)| / q
  <= 1/q + (N_s - A_t(f))(q - 1) / q^(t+1).
```

Thus a base word with a large support-list fiber can create many
support/slope incidences, but all of that base-dependent excess is parked at
the single slope `z = 0`. The nonzero-slope random-direction baseline is
uniform in `f`. This is not a classification of the worst-case tangent-floor
construction; it only says that fixed basepoint list mass does not create
extra nonzero slopes for a random direction.

## Slope-Resolved Second Moment

The incidence count `X = |Inc_t(f,g)|` is the sum over all slopes. To understand
bad-slope density, fix one slope `z in F` and let

```text
X_z = |{S : (S,z) in Inc_t(f,g)}|.
```

Make the invertible linear change of random variables

```text
U = f + z g,       V = g.
```

Then `U,V` are independent uniform words in `F^D`. For a support `S`, let

```text
K_S = {v in F^D : Pi_S(v) = 0}.
```

The support `S` contributes to `X_z` exactly when

```text
U in K_S,       V notin K_S.
```

Indeed, `Pi_S(f) + z Pi_S(g) = Pi_S(U)`, and under this equation the
noncontainment condition fails exactly when `Pi_S(V)=0`.

For one support, `Pr[U in K_S] = q^(-t)` and `Pr[V notin K_S] = 1 - q^(-t)`,
so

```text
E X_z = N_s q^(-t)(1 - q^(-t)).
```

For two supports `S,T`, put `r = |S cap T|` and

```text
alpha_r = Pr[U in K_S cap K_T].
```

The same rank calculation as above gives

```text
alpha_r =
  q^(-2t)             if r < k,
  q^(r-k-2t)          if k <= r <= k+t.
```

Since `U` and `V` are independent, the pair probability is

```text
Pr[S,T both contribute to X_z]
  = alpha_r * Pr[V notin K_S union K_T]
  = alpha_r(1 - 2q^(-t) + alpha_r).
```

Thus the exact slope-resolved second moment is

```text
E X_z^2
  = N_s * sum_{r=0}^{k+t} binom(k+t,r) binom(n-k-t,k+t-r)
      alpha_r(1 - 2q^(-t) + alpha_r).
```

When `r < k`, `alpha_r = q^(-2t)`, so the pair probability is exactly

```text
q^(-2t)(1 - q^(-t))^2 = Pr[S contributes]^2.
```

Thus fixed-slope support indicators are also exactly independent through
intersection `k`: covariance can only start when `|S cap T| > k`.

Let

```text
mu_z = E X_z,       p_z = q^(-t)(1 - q^(-t)).
```

For `q >= 2`, the relative variance is bounded by

```text
Var X_z / mu_z^2
  <= (1 - p_z)/(N_s p_z)
     + (4/N_s) * sum_{j=1}^{t-1}
         binom(k+t,j) binom(n-k-t,j) q^(t-j).
```

To see this, write `j = k+t-r` for the strict-overlap terms. The case `j = t`
is `r = k`, where `alpha_r = q^(-2t)` and the pair probability is exactly the
independent product. Thus only `1 <= j <= t-1` can contribute covariance. In
that range `alpha_r = q^(-t-j)`, while

```text
p_z^2 = q^(-2t)(1 - q^(-t))^2.
```

Since `1 - q^(-t) >= 1/2`, each strict high-overlap pair contributes at most
`4q^(t-j)` times the independent product probability. The diagonal term gives
`(1-p_z)/(N_s p_z)`.

Consequently, if

```text
N_s / ( q^t
        + sum_{j=1}^{t-1} binom(k+t,j) binom(n-k-t,j) q^(t-j) )
  -> infinity,
```

then `Var X_z / mu_z^2 -> 0`, uniformly in `z`.

The same calculation gives a useful finite-parameter missing-density bound.
Let

```text
B_t = (1 - p_z)/(N_s p_z)
      + (4/N_s) * sum_{j=1}^{t-1}
          binom(k+t,j) binom(n-k-t,j) q^(t-j).
```

Finally, the exact-support reduction above gives `z in Bad_t(f,g)` whenever
`X_z > 0`. Chebyshev's inequality gives

```text
Pr[X_z = 0] <= Var X_z / mu_z^2 <= B_t.
```

Averaging over `z` gives

```text
E[1 - |Bad_t(f,g)|/q] <= B_t.
```

Applying Markov to the missing-slope density gives, for every `epsilon > 0`,

```text
Pr[ |Bad_t(f,g)|/q <= 1 - epsilon ] <= B_t / epsilon.
```

In particular, the same asymptotic condition above implies

```text
|Bad_t(f,g)| / q -> 1
```

in probability. This is the random-line failure-side complement to the Markov
upper bound: above the slope-resolved entropy threshold, almost every slope is
support-wise MCA-bad for a random line, unless strict high-overlap covariance
dominates the displayed variance criterion.

## Restricted Support-Family Certificate

The fixed-slope argument did not use that all supports of size `s` are present.
This gives a reusable certificate for support families that arise after
separating tangent, quotient-periodic, or other structured sources.

Let `A` be a deterministic family of `M >= 1` supports of size `s = k+t`. For
`1 <= j <= t-1`, define

```text
Delta_j(A)
  = |{(S,T) in A^2 : S != T and |S \ T| = |T \ S| = j}|.
```

For `t = 1`, there are no such strict-overlap indices and the sums below are
empty.

Equivalently, `Delta_j(A)` counts ordered pairs of supports whose intersection
has size `s-j`. The range `1 <= j <= t-1` is exactly the strict high-overlap
range `|S cap T| > k`; intersections of size at most `k` have zero covariance
for fixed slope.

For a fixed `z`, let

```text
X_z(A) = |{S in A : (S,z) in Inc_t(f,g)}|.
```

The one-support calculation gives

```text
E X_z(A) = M p_z,        p_z = q^(-t)(1 - q^(-t)).
```

For two distinct supports with `j = s - |S cap T|`, the slope-resolved second
moment above gives exact independence when `j >= t`. When `1 <= j <= t-1`, it
gives

```text
Pr[S,T both contribute to X_z(A)]
  = q^(-t-j)(1 - 2q^(-t) + q^(-t-j)).
```

Thus the strict high-overlap profile is the complete fixed-slope covariance
ledger. If

```text
K_j = q^(-t-j)(1 - 2q^(-t) + q^(-t-j)) - p_z^2,
```

then

```text
Var X_z(A)
  = M p_z(1 - p_z)
    + sum_{j=1}^{t-1} Delta_j(A) K_j.
```

Since `q >= 2`,

```text
q^(-t-j)(1 - 2q^(-t) + q^(-t-j))
  <= 4 q^(t-j) p_z^2.
```

Summing the diagonal variance and these strict high-overlap pair bounds yields

```text
Var X_z(A) / (M p_z)^2
  <= (1 - p_z)/(M p_z)
     + (4/M^2) * sum_{j=1}^{t-1} Delta_j(A) q^(t-j).
```

Therefore the finite-parameter missing-density bound also restricts to `A`.
With

```text
B_t(A) = (1 - p_z)/(M p_z)
         + (4/M^2) * sum_{j=1}^{t-1} Delta_j(A) q^(t-j),
```

Chebyshev gives

```text
Pr[X_z(A) = 0] <= B_t(A).
```

Averaging over `z` and applying Markov to the missing-slope density gives

```text
E[1 - |Bad_t(A;f,g)|/q] <= B_t(A),

Pr[ |Bad_t(A;f,g)|/q <= 1 - epsilon ] <= B_t(A) / epsilon.
```

Sometimes the ordered profile is more detail than a proof needs. Define the
maximum `j`-exchange codegree

```text
Gamma_j(A)
  = max_{S in A} |{T in A : |S \ T| = |T \ S| = j}|,
      1 <= j <= t-1.
```

Then `Delta_j(A) <= M Gamma_j(A)`, and hence the same missing-density
conclusion holds with

```text
B_t^max(A) = (1 - p_z)/(M p_z)
             + (4/M) * sum_{j=1}^{t-1} Gamma_j(A) q^(t-j).
```

The sparse side is just as important. Every slope witnessed by `A` has at least
one incidence from `A`, so

```text
E |Bad_t(A;f,g)|/q
  <= M * (q^t - 1) / q^(2t)
  <= M / q^t.
```

The first two Bonferroni terms give the complementary lower estimate.  Let

```text
P_j = q^(-t-j)(1 - 2q^(-t) + q^(-t-j)).
```

For a fixed slope, the ordered second factorial moment is

```text
E[X_z(A)(X_z(A)-1)]
  = (M(M-1) - sum_{j=1}^{t-1} Delta_j(A)) p_z^2
    + sum_{j=1}^{t-1} Delta_j(A) P_j.
```

Indeed, pairs outside the strict high-overlap range are exactly independent,
and strict pairs are counted by `Delta_j(A)` with the pair probability `P_j`.
Since

```text
Pr[X_z(A)>0]
  >= E X_z(A) - E[X_z(A)(X_z(A)-1)]/2,
```

averaging over slopes gives

```text
E |Bad_t(A;f,g)|/q
  >= max(0, M p_z - C_t(A)/2),
```

with `C_t(A)` as defined above.  Thus, in sparse regimes where the pair
correction is lower order than `M p_z`, the support-incidence density and
distinct-slope density agree to first order.

Thus, along a parameter sequence with `q >= 2`,

```text
M / q^t -> 0
```

forces `|Bad_t(A;f,g)|/q -> 0` in probability, while

```text
M / ( q^t + M^(-1) * sum_{j=1}^{t-1} Delta_j(A) q^(t-j) ) -> infinity
```

forces `|Bad_t(A;f,g)|/q -> 1` in probability.

The max-codegree version is the cleaner proof target:

```text
M / ( q^t + sum_{j=1}^{t-1} Gamma_j(A) q^(t-j) ) -> infinity
```

also forces `|Bad_t(A;f,g)|/q -> 1` in probability.

At slack one this becomes exact. If `t = 1`, then two distinct supports of size
`k+1` intersect in at most `k` points, so all distinct fixed-slope indicators
are pairwise independent. Hence

```text
Var X_z(A) = M p_z(1 - p_z),        p_z = (q - 1)/q^2.
```

Chebyshev gives

```text
Pr[X_z(A) = 0] <= (1 - p_z)/(M p_z).
```

For `q >= 2`, this is at most `2q/M`. Averaging over slopes gives

```text
E[1 - |Bad_1(A;f,g)|/q] <= 2q/M.
```

Together with the first-moment bound `E |Bad_1(A;f,g)|/q <= M/q`, this gives
the slack-one phase diagram for every fixed support family: `M/q -> 0` forces
zero bad-slope density in probability, while `M/q -> infinity` forces density
one in probability.

For the full support family `A = binom(D,s)`, one has `M = N_s` and

```text
Delta_j(A) = N_s binom(s,j) binom(n-s,j),

Gamma_j(A) = binom(s,j) binom(n-s,j),
```

so this certificate recovers the all-support slope-density criterion. For a
proper subfamily, the full Johnson-sphere correction is replaced by the actual
strict high-overlap profile of that family. This is a concrete object a scanner
or a future inverse theorem can target: after the known tangent and quotient
floors are removed, an aperiodic family must either be sparse relative to
`q^t` or exhibit a large certified strict high-overlap profile.

## Random-Line Slope-Density Phase Diagram

The random-line baseline now has a two-sided slope-density statement. Let

```text
R_t(n,k,q)
  = sum_{j=1}^{t-1} binom(k+t,j) binom(n-k-t,j) q^(t-j).
```

The sparse side follows from the first-moment bound:

```text
E |Bad_t(f,g)| / q <= N_s / q^t.
```

Therefore, if

```text
N_s / q^t -> 0,
```

then Markov's inequality gives

```text
|Bad_t(f,g)| / q -> 0
```

in probability.

The dense side follows from the slope-resolved second moment. If

```text
N_s / (q^t + R_t(n,k,q)) -> infinity,
```

then, uniformly in the slope `z`,

```text
Pr[z notin Bad_t(f,g)] -> 0.
```

Equivalently, the expected missing-slope density tends to zero. Markov's
inequality then gives

```text
|Bad_t(f,g)| / q -> 1
```

in probability.

Thus the only gap between the sparse and dense random-line regimes is the
strict high-overlap correction `R_t`. In the random-overlap range where `t` is
fixed and

```text
s(n-s)/q -> 0,
```

one has `R_t = o(q^t)`, so the random-line bad-slope density has a sharp
threshold at

```text
binom(n,k+t) ~= q^t.
```

This is the random analogue of the M1 entropy ledger. A worst-case theorem
cannot hope to follow from random-line heuristics alone; it must separately
control tangent, quotient-periodic, and strict high-overlap structured line
data.

## Entropy-Reserve Reading

The phase diagram can be read in exactly the reserve language used in Paper B.
Ignoring strict high-overlap corrections, the random-line transition occurs when

```text
q^t ~= binom(n,k+t).
```

Equivalently, using any fixed logarithm base,

```text
t log q ~= log binom(n,k+t).
```

Thus the random-line entropy reserve is

```text
t log q - log binom(n,k+t).
```

On the positive random side,

```text
t log q - log binom(n,k+t) -> +infinity
```

forces the bad-slope density to vanish. On the failure random side, provided
the strict high-overlap correction `R_t` is negligible,

```text
log binom(n,k+t) - t log q -> +infinity
```

forces the bad-slope density to tend to one.

For fixed rate `rho = k/n` and slack fraction `eta = t/n`, Stirling's formula
turns the threshold into

```text
eta log q ~= H(rho + eta),
```

up to lower-order terms after dividing by `n`, with `H` measured in the same
logarithm base. This is only a random-line statement, but it explains why the
worst-case M1 conjecture has to be calibrated against the same generated-field
entropy ledger as the locator-fiber problem, with tangent, quotient-periodic,
and strict high-overlap families accounted for separately.

Field-ledger warning: in this note `q` is the field from which the random line
data `f,g` are sampled. Thus the displayed reserve is a `q_line` reserve. It
matches the generated-field entropy ledger only in setups where the line field
and generated field have been explicitly identified. It should not be used to
pay a `q_gen` entropy bill with a larger extension challenge field unless a
separate transfer theorem justifies that replacement.

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

It is useful to rewrite the high-overlap sum by the number of points exchanged
between the two supports. Put `s = k+t` and let

```text
j = s - r.
```

Then `k <= r <= k+t-1` is the same as `1 <= j <= t`, and

```text
r - k - 2t + 2 = 2 - t - j.
```

Therefore the high-overlap part is exactly

```text
H_t(n,k,q)
  = sum_{j=1}^t binom(s,j) binom(n-s,j) q^(2-t-j).
```

The relative-variance estimate becomes

```text
Var X / (E X)^2
  <= (1 - p_t)/(N_s p_t) + H_t(n,k,q)/(N_s p_t^2).
```

For a rough closed sufficient condition, use

```text
binom(s,j) binom(n-s,j)
  <= (s(n-s))^j / (j!)^2
```

and, for `q >= 2`,

```text
p_t = q^(1-t)(1 - q^(-t)) >= 1/(2 q^(t-1)).
```

Then

```text
Var X / (E X)^2
  <= 2 q^(t-1)/N_s
     + (4 q^t/N_s)
       * sum_{j=1}^t (s(n-s)/q)^j / (j!)^2.
```

Consequently, along any parameter sequence satisfying

```text
N_s / ( q^(t-1)
        + q^t * sum_{j=1}^t (s(n-s)/q)^j / (j!)^2 ) -> infinity,
```

the random-line support-incidence count concentrates:

```text
X / E X -> 1 in probability.
```

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

The fixed-base refinement separates the zero slope:

```text
nonzero random-direction incidence mass
  <= binom(n,k+t) / q^(t-1)  for every fixed base word.

nonzero random-direction bad-slope density
  <= binom(n,k+t) / q^t      for every fixed base word.
```

The all-slope second-moment bound adds the overlap ledger:

```text
random support covariance starts only at |S cap T| >= k.

relative variance is controlled by exchanged points
  j = 1,...,t with weights binom(k+t,j) binom(n-k-t,j) q^(2-t-j).
```

The slope-resolved ledger adds the failure-side threshold:

```text
if the fixed-slope relative variance tends to zero, then
  |Bad_t(f,g)| / q -> 1 in probability.

expected missing-slope density is at most the fixed-slope relative variance
bound B_t.

fixed-slope covariance starts only at |S cap T| > k.

for any fixed support family A, Delta_j(A) exactly determines the fixed-slope
variance contribution from strict high-overlap pairs.

at slack t = 1, fixed-slope indicators are pairwise independent for every
fixed support family, so the random-line transition is M ~= q.

random-line slope density transitions at binom(n,k+t) ~= q^t
when strict high-overlap corrections are negligible.

entropy reserve:
  t log q - log binom(n,k+t).

field ledger:
  q is q_line here; do not replace q_gen by an extension q_line without a
  transfer theorem.
```

The restricted-family certificate makes this ledger reusable:

```text
for a fixed support family A, replace binom(n,k+t) by |A|
and replace the full Johnson correction by Delta_j(A), j = 1,...,t-1.

The coarser proof target is the max exchange codegree Gamma_j(A).
```

Together these formulas justify treating the aperiodic part of residue-line
packing as an incidence problem rather than as an arbitrary list-size problem.
They also identify the exact obstruction to promoting the estimate to a
worst-case theorem: after the zero-slope basepoint term, the known
tangent-floor constructions, and quotient-periodic families are separated, one
must rule out line data for which many strict high-overlap supports have aligned
top-coefficient vectors `Pi_S(f)` and `Pi_S(g)`.

## Suggested Next Step

The natural follow-up is a scanner that, for tiny fields, computes the vectors
`Pi_S(f), Pi_S(g)` over all supports of size `k+t`, records the distinct slopes
arising from collinearity, and labels whether each support is tangent,
quotient-periodic, or aperiodic. For each labelled support family it should
also report `Delta_j(A)` and `Gamma_j(A)` for `1 <= j <= t-1`. The average
formula above gives an exact baseline for interpreting those scans, while the
restricted-family certificate says when the labelled aperiodic part is behaving
like the random model and when it is carrying a genuine strict-overlap
obstruction.
