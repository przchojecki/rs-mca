# List Corridor Widths

Status: PROVED.

Source DAG node: `list_corridor_widths`.

## Statement

For the list-side clean-rate corridor, the gap between the constructive
list-unsafe endpoint and the image-fiber list-safe endpoint is:

| rate | W_list |
| --- | ---: |
| 1/4 | 1.612526496982 |
| 1/8 | 1.075136156735 |
| 1/16 | 1.328340157828 |

The units are cap-grid steps.  For rates `1/4` and `1/8`, the grid step is
`eta = 2^-9`; for rate `1/16`, it is `eta = 2^-10`.

## Endpoint Convention

Write the reserve coordinate as

```text
delta = 1 - rho - reserve.
```

The list-side endpoint convention is:

```text
unsafe reserve = H(rho) / 128
safe reserve   = tau_star(rho, log2 q = 256)
W_list          = (unsafe reserve - safe reserve) / eta
```

The replay certificate also records the dyadic audit edge `H(rho)/256`.  That
edge is not used as the safe endpoint; it is printed only to show that the
constructive quotient-core upper edge is within `0.021` cap-grid steps of
`tau_star` at the three clean rates.

## Proof

The replay script recomputes `H(rho)`, solves the entropy crossing defining
`tau_star(rho, 256)`, applies the cap-grid convention, and checks the three
recorded widths.  No row search, random sampling, or large-memory computation is
used.

## Non-Claims

This packet only prices the list-side corridor width at the three clean rates
`1/4`, `1/8`, and `1/16`.  It does not treat the rate-`1/2` band, does not by
itself prove a list adjacent threshold row, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_list_corridor_widths.py --emit
python3 experimental/scripts/verify_list_corridor_widths.py \
  --check experimental/data/certificates/list-corridor-widths/list_corridor_widths.json
```
