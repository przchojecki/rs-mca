# Cap End Sharpening

Status: PROVED.

Source DAG node: `cap_end_sharpening`.

## Statement

At rate `rho = 1/8`, the Paper D cap reserve can be sharpened by one part in
`8192`, which is `1/16` of a cap-grid step.  This is enough to cover the
rate-`1/8` fourth-mechanism wedge.

The exact point is:

```text
n = 2^41, k = 2^38, q < 2^256
c = 2^28, N = 8192, d = 17, m = 1041, s = 0
```

The replay certificate verifies:

```text
L >= binom(8192, 1041) / 2^(256 * 16) > 2^398,
```

so the trigger threshold `(q - n) / k < 2^218` is cleared by more than `180`
bits.

## Proof

Use the quotient-remainder floor at full fiber `s = 0`.  The charged prefix
coefficient count is

```text
w_c(0, 17c - 1) = 16.
```

The replay script checks the floor hypotheses, the exact integer trigger

```text
binom(8192, 1041) > 2^(256 * 17 - 38),
```

and the grid-step gain

```text
17 * 2^9 / 8192 - 1 = 1/16.
```

Thus the unsafe boundary moves from `7152/8192` to `7151/8192`.

## Non-Claims

This packet proves only the rate-`1/8` cap-end sharpening route.  It does not
claim a full clean-rate corridor ledger, does not treat list decoding, and does
not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_cap_end_sharpening.py --emit
python3 experimental/scripts/verify_cap_end_sharpening.py \
  --check experimental/data/certificates/cap-end-sharpening/cap_end_sharpening.json
```
