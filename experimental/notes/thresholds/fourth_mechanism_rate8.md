# Fourth Mechanism Rate 1/8

Status: PROVED.

Source DAG node: `fourth_mechanism_rate8`.

Depends on: `cap_end_sharpening`.

## Statement

The clean-rate corridor at rate `1/8` needs a fourth-mechanism gain of at least
`0.00707` cap-grid steps.  Route (a), cap-end sharpening, supplies

```text
1/16 = 0.0625
```

cap-grid steps, which is more than `8.8` times the required wedge.

## Proof

The replay certificate checks the `cap_end_sharpening` certificate and consumes
its exact gain:

```text
cap_end_gain = 17 * 2^9 / 8192 - 1 = 1/16.
```

Since

```text
1/16 > 0.00707,
```

the `fourth_mechanism_rate8` predicate holds by route (a).  No tau-star reserve
tightening or census crossing pinning route is needed for this node.

## Consequence

The rate-`1/8` fourth-mechanism wedge is closed.  This is the input that the
corridor ledger needs in its rate-`1/8` row.

## Non-Claims

This packet only proves the fourth-mechanism predicate at rate `1/8`.  It does
not assemble the full clean-rate corridor ledger, does not treat the rate-`1/2`
band, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_fourth_mechanism_rate8.py --emit
python3 experimental/scripts/verify_fourth_mechanism_rate8.py \
  --check experimental/data/certificates/fourth-mechanism-rate8/fourth_mechanism_rate8.json
```
