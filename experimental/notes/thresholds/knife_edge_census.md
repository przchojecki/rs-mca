# Knife-Edge Census

Status: PROVED.

Source DAG node: `knife_edge_census`.

## Statement

For each knife-edge rate/candidate cell, let

```text
K = exact raw count for the deciding quotient stratum,
L = certified distinct lower count,
B(q) = floor(q / 2^128).
```

Then the unresolved budget values are exactly

```text
B(q) in [L, K).
```

As the certified lower count `L` rises to the exact count `K`, the unresolved
window shrinks monotonically and vanishes at `L = K`.  The residual census is
therefore finite exact arithmetic once the bounded-scale exact count and the
certified value-set lower bound are available.

## Dependency Sub-DAG

```text
census_bounded_scales    -> census_exact_counts
census_exact_counts      -> census_window_arithmetic
census_window_arithmetic -> knife_edge_census
certified_valueset_lower -> knife_edge_census
```

The current upstream packet `quotient_census_window_compiler` covers the
bounded-scale and exact-window arithmetic side, including
`census_window_arithmetic`.  The companion packet
`certified_valueset_lower.md` supplies the certified lower-bound input.

## Proof

The exact count `K` is an upper endpoint for the row's deciding stratum.  The
certified lower count `L` is a witnessed family of pairwise distinct `e1` values
modulo the row prime, so it is a genuine lower endpoint for the value set.

For a row with budget `B(q)`, there are three cases.

```text
B(q) < L       certified lower family already exceeds the budget;
L <= B(q) < K  the knife-edge cell remains in the exact residual window;
B(q) >= K      the deciding stratum's exact count is at or below budget.
```

Thus the residual set is exactly the integer interval `[L,K)`.  The interval is
monotone in `L`, and is empty when `L = K`.  This is the assembly content of
`knife_edge_census`: all non-window cells are decided by the certified lower or
the exact upper count, and the surviving cells are explicit finite windows.

## Non-Claims

This packet does not count primes inside the residual windows, does not choose
deployed v13 row primes, does not replace row-specific certificates, and does
not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_knife_edge_census.py --emit
python3 experimental/scripts/verify_knife_edge_census.py \
  --check experimental/data/certificates/knife-edge-census/knife_edge_census.json
```
