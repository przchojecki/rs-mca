# List Corridor Ledger

Status: PROVED.

Source DAG node: `list_corridor_ledger`.

Depends on: `list_corridor_widths`.

## Statement

At the three clean rates, the list-side corridor width deficit is covered by the
scale-free quotient-remainder floor.  The ledger inequality is

```text
available_gain(rate) >= W_list(rate) - 1.
```

Using the width packet and the exact floor-gain fractions:

| rate | W_list - 1 | scale-free floor gain | margin |
| --- | ---: | ---: | ---: |
| 1/4 | 0.612526496982 | 81/128 = 0.6328125 | 0.020286003018 |
| 1/8 | 0.075136156735 | 203/2048 = 0.09912109375 | 0.023984937015 |
| 1/16 | 0.328340157828 | 3/8 = 0.375 | 0.046659842172 |

All three clean-rate rows pass with positive margin.

## Proof

The replay certificate first checks the `list_corridor_widths` certificate.
It then replays the exact integer sweep for the three scale-free floor points:

```text
rate 1/4:  c = 2^25, d = 209
rate 1/8:  c = 2^21, d = 2251
rate 1/16: c = 2^28, d = 11
```

For each point, it checks the quotient-remainder floor hypotheses, the exact
trigger inequality

```text
binom(N, m) > 2^(256 d - e),
```

the maximality of `d`, and the printed grid-step gain fraction.  It then
compares each exact gain to `W_list - 1`.

## Consequence

For rates `1/4`, `1/8`, and `1/16`, the clean-rate list corridor has no
remaining width deficit once `list_corridor_widths` is admitted.  This is the
list-side mirror of the MCA corridor ledger: exact widths plus a scale-free
floor eater collapse the clean-rate bracket to adjacency.

## Non-Claims

This packet does not treat the rate-`1/2` band, does not prove any missing
list-safe or list-unsafe endpoint formula, and does not alter Papers A-D.  It
is an implication packet for the clean-rate corridor arithmetic.

## Replay

```bash
python3 experimental/scripts/verify_list_corridor_ledger.py --emit
python3 experimental/scripts/verify_list_corridor_ledger.py \
  --check experimental/data/certificates/list-corridor-ledger/list_corridor_ledger.json
```
