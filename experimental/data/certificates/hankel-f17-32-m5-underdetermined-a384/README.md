# F17^32 M5 A384 planted chart packets

This directory contains declared real-row packets for the M5
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

The top-chart certificate is the nonzero prefix moment minor:

```text
det(S_{r+c})_{0<=r,c<128} = det(V)^2
```

where `V` is the Vandermonde matrix on the 128 planted support roots.  The
packet records both the Vandermonde determinant encoding and the prefix-minor
encoding.

The packet

```text
f17_32_n512_k256_a384_planted_low_degree.json
```

constructs a full-rank low-degree side-chart example.  It uses a degree-127
locator, perturbs only `S_255`, and records a nonzero shifted minor on columns
`1..128`.  Thus `c_128=0` but the row rank is still 128.

The packet

```text
f17_32_n512_k256_a384_planted_rank_drop.json
```

constructs a rank-drop side-chart example.  It uses a 126-root moment support,
records a nonzero prefix `126 x 126` moment minor `det(V)^2`, and verifies that
the `128 x 129` Hankel block has rank exactly 126 while a degree-128 split
locator lies in its kernel.

Replay:

```bash
python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py \
  --check-f17 experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/f17_32_n512_k256_a384_planted_top_chart.json

python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py \
  --check-f17-low-degree experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/f17_32_n512_k256_a384_planted_low_degree.json

python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py \
  --check-f17-rank-drop experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/f17_32_n512_k256_a384_planted_rank_drop.json
```

Non-claims: this is not a full `F_17^32` root table, threshold theorem, or
worst-case row bound.  It is a replayable real-row instantiation of the
deficiency-one top, low-degree, and rank-drop chart decomposition.
