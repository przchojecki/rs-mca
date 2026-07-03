# M1: averaged slope conversion from locator mean to distinct slopes

- **Status:** PROVED averaged conversion theorem / AUDIT for unsafe-side use.
- **Agent/model:** Codex.
- **Date:** 2026-07-03.
- **DAG target:** `averaged_slope_conversion`.
- **Inputs:** `fm1_exact_aperiodic_first_moment.md`,
  `m1_average_support_collinearity.md`, and the v8 one-slope-per-locator
  cap.

## Purpose

FM1 proves the exact random-pair locator mean

```text
E[N] = M (1 - q^(-t)) q^(1-t)
```

for a deterministic family of `M` split locators or exact supports.  The
unsafe side needs a distinct-slope statement: if the family is large enough,
some received pair `(u,v)` must have many finite bad slopes, not merely many
aligned locators.

This note gives the conversion.  The only loss is the explicit same-slope
collision budget, computed by the slope-resolved second moment.  After paid
fibers are removed or charged separately, the theorem applies to the remaining
family with its actual strict-overlap profile.

## Setup

Let `F = F_q`, let `D` have size `n`, and let `C=RS[F,D,k]`.  Fix

```text
s = k+t,       1 <= t <= n-k.
```

Let `A` be a deterministic family of exact supports of size `s`, or
equivalently their complementary split locators.  Write

```text
M = |A|.
```

For a support `S in A`, let `(a_S,b_S)` be the two `t`-coordinate syndrome
vectors of a random independent pair `(u,v)`.  The support is aligned if

```text
b_S != 0,       a_S in F b_S.
```

When this happens, the v8 cap gives a unique finite slope

```text
z_S = -a_i / b_i
```

for any nonzero coordinate `b_i`; consistency of the syndrome equations makes
the value independent of `i`.  Thus each aligned locator contributes to exactly
one finite slope.

For `z in F`, let

```text
X_z(A) = #{ S in A : S contributes slope z },
Y(A)   = |{ z in F : X_z(A) > 0 }|,
N(A)   = sum_z X_z(A).
```

Here `N(A)` is the aligned-locator count and `Y(A)` is the distinct finite bad
slope count witnessed by the family.

## Pair-correlation input

For a fixed slope `z`, set

```text
p_z = q^(-t)(1-q^(-t)).
```

Then

```text
E[X_z(A)] = M p_z,
E[N(A)]   = q M p_z = M(1-q^(-t))q^(1-t).
```

For two distinct supports `S,T in A`, let their exchange distance be

```text
d(S,T) = |S \ T| = |T \ S|.
```

The slope-resolved second moment gives exact independence for fixed `z` once
`d(S,T) >= t`.  For `1 <= d < t`, the same-slope pair probability is

```text
P_d = q^(-t-d)(1 - 2q^(-t) + q^(-t-d)).
```

Equivalently, after summing over the common slope `z`, a strict-overlap pair
contributes

```text
q P_d <= q^(1-t-d),
```

matching the closed-form same-slope scale `q^(1-t-min(d,t))`.  For distinct
prescribed slopes the two support equations are independent at scale
`q^(2-2t)`, so distinct-slope correlations do not reduce the occupancy lower
bound below; only same-slope collisions do.

Define the ordered strict-overlap profile

```text
Delta_d(A)
  = |{(S,T) in A^2 : S != T, d(S,T)=d}|,
      1 <= d <= t-1.
```

and the fixed-slope ordered collision correction

```text
C_t(A)
  = (M(M-1) - sum_{d=1}^{t-1} Delta_d(A)) p_z^2
    + sum_{d=1}^{t-1} Delta_d(A) P_d.
```

This is exactly `E[X_z(A)(X_z(A)-1)]`.

## Theorem: averaged locator-to-slope conversion

With notation as above,

```text
E[Y(A)] >= E[N(A)] - (q/2) C_t(A).
```

Consequently, for every integer `B >= 1`, if

```text
E[N(A)] - (q/2) C_t(A) > B - 1,
```

then there exists a received pair `(u,v)` whose family `A` witnesses at least
`B` distinct finite bad slopes.

In particular, for the prize denominator `B* = floor(q/2^128)`, the sufficient
unsafe-side certificate is

```text
M(1-q^(-t))q^(1-t) - (q/2) C_t(A) > B* - 1.
```

### Proof

For each slope `z`, the elementary occupancy inequality gives

```text
1_{X_z>0} >= X_z - X_z(X_z-1)/2.
```

Summing over `z` gives

```text
Y(A) >= N(A) - (1/2) sum_z X_z(A)(X_z(A)-1).
```

Taking expectation and using the fixed-slope second factorial moment
`E[X_z(A)(X_z(A)-1)] = C_t(A)`, which is independent of `z`, gives

```text
E[Y(A)] >= E[N(A)] - (q/2) C_t(A).
```

Since `Y(A)` is integer-valued, if its average is greater than `B-1`, at least
one pair has `Y(A) >= B`.  This proves the conversion.

## Paley-Zygmund form

The same conclusion can be phrased as a Paley-Zygmund-style existence
statement.  Put

```text
nu = E[N(A)] - (q/2) C_t(A).
```

The theorem gives `E[Y(A)] >= nu`.  Since `0 <= Y(A) <= q`,

```text
E[Y(A)^2] <= q E[Y(A)].
```

Therefore Paley-Zygmund gives, for every `0 <= theta < 1`,

```text
Pr[ Y(A) >= theta E[Y(A)] ]
  >= (1-theta)^2 E[Y(A)] / q
  >= (1-theta)^2 nu / q.
```

Taking `theta = (B-1)/nu` when `nu > B-1` gives positive probability of
`Y(A) >= B`.  The occupancy proof above is the deterministic extraction of the
same averaged fact.

## Paid-fiber exclusion

The theorem is deliberately stated for an arbitrary deterministic family `A`.
For prize use, `A` must be the post-dedup, post-paid family:

1. tangent, quotient-periodic, extension, and other already-paid fibers are
   removed or charged to their ledger before applying this conversion;
2. the first-match dedup convention chooses one owner for every support, so a
   support cannot be counted both as paid and unpaid;
3. the strict-overlap profile `Delta_d(A)` is computed after that exclusion.

If paid fibers are left in `A`, the theorem still proves the existence of many
distinct slopes, but it does not prove they are unpaid slopes.  The unsafe-side
collided branch must therefore use the paid-excluded family or explicitly add
the paid slopes to the final numerator.

## Useful sparse corollary

When `E[N(A)] <= q`, the independent same-slope collision term is at most
`E[N(A)]^2/q`, and the strict-overlap terms are exactly the displayed
`Delta_d(A)` correction.  Thus, in the prize-scale sparse occupancy regime,
crossing `B*` in FM mean converts to `B*` distinct slopes as soon as

```text
(q/2) C_t(A) < E[N(A)] - (B* - 1).
```

For `q < 2^256` and `E[N(A)]` near `q/2^128`, the independent occupancy loss is
`< 1/2`; any real obstruction must therefore come from the strict high-overlap
profile or from paid fibers that were not excluded.

## Existing checks

The formula for `C_t(A)` is the restricted-family fixed-slope second moment in
`m1_average_support_collinearity.md`.  The small verifier below checks the
occupancy inequality and the conversion arithmetic:

```bash
python3 experimental/scripts/verify_m1_averaged_slope_conversion.py
```
