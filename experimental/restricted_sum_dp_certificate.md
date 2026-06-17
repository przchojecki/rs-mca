# Restricted-Sum DP Certificate

**Status:** `PROVED` for the finite dynamic-programming recurrence below.
Individual parameter runs are `AUDIT`.

**Target:** Paper A finite-claim audits and the P2 certificate-scanner lane.

**Companion script:** `experimental/restricted_sum_dp.py`

## Claim

Let `p` be prime, let

```text
A = {a_1, ..., a_m} subset F_p
```

have distinct elements, and let `0 <= r <= m`. The restricted sumset is

```text
r^wedge A = {a_{i_1} + ... + a_{i_r} : i_1, ..., i_r distinct}.
```

The script computes this set exactly over `F_p` by dynamic programming.

## Status

`PROVED` for the recurrence:

after processing the first `t` elements of `A`, `state[j]` is exactly the set
of sums of `j` distinct processed elements.

The script's comparison with Dias da Silva-Hamidoune is an `AUDIT` use of the
imported theorem already cited in Paper A:

```text
|r^wedge A| >= min(p, r(m-r)+1).
```

When `r(m-r)+1 >= p`, that theorem certifies full field coverage. Otherwise,
the DP result is an exact finite computation for the specific input.

## Parameters

The script supports two input modes:

```text
--elements        explicit comma-separated elements of F_p
--subgroup-order  construct the multiplicative subgroup of this order
```

Subgroup mode requires `subgroup_order | p-1`. If no generator is supplied,
the script finds a primitive root of `F_p` and constructs the unique subgroup
of the requested order.

## Existing Paper Dependency

Paper A uses restricted sums in the quotient locator identity: if `Q` is a
quotient subgroup and `z` lies in `-r^wedge Q`, then the corresponding line has
a bad slope witness at the stated radius. This certificate only verifies the
finite restricted-sum object; it does not prove MCA, list decoding, line
decoding, curve-MCA, or protocol soundness.

## Proof

Initialize

```text
state[0] = {0}
state[j] = empty for j > 0.
```

Suppose the invariant holds after processing a prefix `B` of the input list.
Let the next element be `x`. Every `j`-element subset of `B union {x}` either:

1. does not contain `x`, in which case its sum is already in `state[j]`, or
2. contains `x`, in which case it is `x` plus the sum of a `(j-1)`-element
   subset of `B`.

Therefore the update

```text
state[j] <- state[j] union {s + x mod p : s in state[j-1]}
```

is exact. Updating `j` in descending order ensures that `x` is not used twice
in one step. By induction, after all elements are processed, `state[r]` is
exactly `r^wedge A`.

## Ledger Impact

The output gives:

```text
input parameters
exact object checked
|r^wedge A|
coverage and missing residues
DSH lower-bound metadata
negated bad-slope samples
JSON or human-readable output
```

This supports Paper A finite verification records and the P2 goal of replacing
hand-computed finite tables with reproducible certificates.

## Reproducibility

Fermat-prime toy check:

```bash
python3 experimental/restricted_sum_dp.py --p 17 --subgroup-order 8 --r 3 --expect-size 16
```

Paper A style subgroup check:

```bash
python3 experimental/restricted_sum_dp.py --p 257 --subgroup-order 16 --r 9 --expect-size 256
```

JSON output:

```bash
python3 experimental/restricted_sum_dp.py --p 17 --subgroup-order 8 --r 3 --format json
```

Each run should be interpreted as an `AUDIT` certificate for the specified
finite field and subset.
