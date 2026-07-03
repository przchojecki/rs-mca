# Census Dodge Selection

## Status

PROVED-COMPILER-ARITHMETIC.

This note packages the DAG node `census_dodge_selection`.  It is a corollary
of the quotient census window compiler: once a row-specific quotient packet
prints an exact count `K` and a certified lower count `L`, the only unresolved
integer budgets are

```text
L <= B(q) < K,        B(q)=floor(q/2^128).
```

Rows whose printed budget lies outside this half-open interval dodge that
census window and already have a sign decision.

## Theorem

Let `K` be an exact quotient-census count and let `L <= K` be a certified
lower count for the same object.  Put `B=floor(q/2^128)`.

```text
B < L       => certified unsafe by the lower count;
B >= K      => certified safe by the exact upper count;
L <= B < K  => unresolved census window.
```

Equivalently, if the exact count is above budget, `K>B`, then it is enough to
certify any lower count

```text
L > B.
```

If the lower proof is written as `L=K-g`, the largest tolerable missing mass is

```text
g_max = K-B-1.
```

Thus an adjacent exact-census crossing does more than localize the scale: it
prints how much lower-bound slack the row can tolerate while still dodging the
unresolved window.

## Official-Rate Replay

The verifier applies this to the 2-power quotient count

```text
A_2(N', ell'),        ell' = rho N' + 1,
rho in {1/2,1/4,1/8,1/16},
```

at budget bits `64, 96, 128`.  For each rate and budget it records both:

```text
relaxed adjacent crossing over even N';
dyadic adjacent crossing over N'=2^a.
```

For the last safe scale `N_-` and first unsafe scale `N_+`, it verifies

```text
A_2(N_-,ell_-) <= B < A_2(N_+,ell_+),
```

and emits:

```text
safe_margin              = B - A_2(N_-,ell_-),
unsafe_missing_tolerance = A_2(N_+,ell_+) - B - 1.
```

All emitted official-rate rows have positive unsafe missing tolerance.  The
smallest tolerance in the replay still has `62` bits, so these adjacent
crossings are not knife-edge integer coincidences.

## Scope

This is a compiler-arithmetic result.  It does not prove a quotient-collision
lower bound, does not count primes inside any `q == 1 mod n` interval, and
does not resolve mixed-radix quotient counts.  A consumer must still supply the
row-specific lower certificate `L`; this packet tells the consumer exactly when
that certificate is strong enough to avoid the unresolved census interval.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_census_dodge_selection.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_census_dodge_selection.py \
  --check experimental/data/certificates/census-dodge-selection/census_dodge_selection.json
```
