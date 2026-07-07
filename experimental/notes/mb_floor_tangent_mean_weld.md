# M_B(d1) is the tangent-column first moment; the subfield correction is
# one level deep at the deployed rows

- **Status:** AUDIT / EXPERIMENTAL (interpretive identity + replay +
  one scoping observation for the BC chart audit).
- **Script:** `experimental/scripts/verify_mb_floor_tangent_mean.py`
  (~1 minute).
- **Data:** `experimental/data/mb_floor_tangent_mean.json`.

## 1. The identity

In prop:capg-census-floor's notation, m' = K − 1 + d1 gives
d1 − 1 = m' − K, so

    M_B(d1) = C(m',m) · ⌈C(n,m') · p^−(d1−1)⌉
            = C(m',m) · ⌈C(n,m') · p^(K−m')⌉ ,

and C(n,m')·p^(K−m') is exactly the first-moment mean of base-field
codewords at agreement m' (p^K codewords × p^−m' per fixed m'-set), each
spraying C(m',m) size-m supports through the binomial-moment formula of
prop:capfr1-lattice-census(c). So the proved subfield floors say: the
identity-prefix witnesses achieve the base tangent-column MEAN, by prefix
pigeonhole. Two corollaries worth having on the page:

- the deployed pair locations are first-moment-predictable because the
  list-row unsafe comparison IS "base tangent mean > ⌊q·eps*⌋" (and the
  MCA row the same with the one-p pencil shift) — verified to every
  printed decimal in the companion replay packet;
- any census model that is base-field-normalized at the first-moment
  level automatically carries the M_B floors (they are its mean), which
  is a compact way to state why the corrections at the end of
  sec:capg-subfield are exactly the right ones.

## 2. Replay

The eight printed floor values reproduce exactly (KoalaBear list:
67.1 / 56.0 / 43.9 / 31.3; Mersenne-31 list: 52.1 / 41.0 / 28.9 / 16.2),
with boundary values re-verified in exact integer arithmetic (67.10,
52.11). NB the printed interior values are the unclamped products — the
ceiling in part (b) only strengthens them (at d1 = w'+4 the clamped floor
C(m',m)·1 = 2^57.7 exceeds the printed 2^31.3).

## 3. One level deep (scoping observation for the BC audit)

Evaluating the same floor with p replaced by p^d for the intermediate
subfields d | 6 at the deployed KoalaBear profiles:

    level p^1: +67.1 / +56.0 bits      level p^2: −2,090,740 / −2,090,782
    level p^3: −4,181,546 / −4,181,619  level p^6: −10,453,966 / −10,454,132

Only the base level carries mass; every intermediate subfield level is
dead by millions of bits (and the p^6 column is the challenge-field-scale
model that prop:capg-census-floor itself refutes as a global normalizer).
So at KoalaBear-shaped rows the base-field-normalized census corrections
need exactly ONE subfield stratum, not a lattice of them — which prunes
the chart space the finite BC chart-decomposition audit has to cover.

## What to do next

If useful, fold the identity into the restatement remarks of
sec:capg-subfield (it is a rewriting, not a new claim); use the
one-level-deep table to scope the BC chart audit's subfield strata at the
deployed rows.
