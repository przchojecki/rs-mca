# F17^32 M5 A384 planted top-chart packet

This directory contains the first declared real-row packet for the M5
underdetermined boundary `A=384` of

```text
RS[F_17^32, H, 256],  |H|=512.
```

The packet

```text
f17_32_n512_k256_a384_planted_top_chart.json
```

uses the pinned row descriptor in
`experimental/data/certificates/hankel-f17-32-row-descriptor/`.  It constructs
a degree-128 locator from the first 128 descriptor-domain roots, generates the
annihilated moment window, and verifies that a nonconstant syndrome pencil
hits that window at a planted finite slope.

Replay:

```bash
python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py \
  --check-f17 experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/f17_32_n512_k256_a384_planted_top_chart.json
```

Non-claims: this is not a full `F_17^32` root table, threshold theorem, or
worst-case row bound.  It is a replayable real-row instantiation of the
deficiency-one top chart.
