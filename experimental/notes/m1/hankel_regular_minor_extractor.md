# Regular Hankel-Minor Extractor

**Status:** EXPERIMENTAL / AUDIT, with a proved finite toy replay.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records the first reusable extractor for the regular overdetermined
bucket in the Paper D v9 Hankel atlas.  It addresses the next item in
`towards-prize.md`:

```text
Regular-minor extractor.
Given row data and exact agreement A, compute candidate nonzero minors
and root-count bounds.
```

## Extractor Scope

The script

```text
experimental/scripts/extract_regular_hankel_minors.py
```

reads a syndrome-pencil input over either a prime field `F_p` or an explicit
polynomial-basis extension field.  For each exact agreement `A`, it
sets

```text
j = n-A,
t = A-k.
```

If `t >= j+1`, it tries candidate `(j+1) x (j+1)` Hankel row minors of

```text
H_{t,j}(u) + Z H_{t,j}(v).
```

The current candidate schedule is data-driven: explicit row sets, prefix row
sets, or a bounded scan of contiguous row windows.  The determinant polynomial
is recovered by interpolation from numeric determinants, rather than by a
factorial permutation determinant.  This is the right algorithmic shape for the
future `385 <= A <= 426` window once row data for the `F_17^32` row are
supplied.

When the field is small enough, the extractor enumerates roots in the full
finite slope field.  For extension fields, root-table elements are encoded as
base-`p` low-to-high integers so the existing v9 packet checker can audit root
hashes and declared numerators.  When the domain is supplied and the
split-locator subset count is small enough, it also enumerates split co-support
bad slopes and checks that they are contained in the extracted root set.

## Toy Replay

The replay input is

```text
experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json
```

and the output packet is

```text
experimental/data/certificates/regular-minor-extractor-toy/
  f17_n16_k8_a13_regular_minor_extractor_packet.json
```

It uses the same toy row as the first regular-minor certificate:

```text
F = F_17,
D = F_17^*,
n = 16,
k = 8,
A = 13,14,15,16.
```

The extractor finds nonzero prefix minors in all four exact agreements, with
degrees `4,3,2,1` and closed-range root union `{0,2,10,11}`.

The extension-field replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json
experimental/data/certificates/regular-minor-extractor-f17-2-toy/
```

It views the same scalar syndrome pencil inside
`F_17^2 = F_17[x]/(x^2-3)` and enumerates all `289` finite slopes.  The full
extension-field root union is again `{0,2,10,11}`, encoded as base-17 integers,
and the packet is accepted by the same v9 checker.

The non-base-root extension replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json
experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/
```

Here the prefix minor is

```text
[[Z, x],
 [x, Z]]
```

over `F_17[x]/(x^2-3)`, so the determinant is `Z^2-3` and the two roots are the
non-base elements `x` and `-x`, encoded as `17` and `272`.  The integrated
checker now evaluates encoded polynomial-basis extension roots, so this packet
is a genuine extension-root validation rather than only a hash check.

## Non-Claims

This does not solve the `F_17^32` regular window.  In particular, it does not
yet provide:

```text
an F_17^32 row-data adapter;
quotient/tangent subtraction for 385 <= A <= 426;
singular pivot charts.
```

Those are the next M3/M4 steps.  The present contribution is the reusable
regular-minor extractor, with prime-field and explicit polynomial-basis
extension-field replays showing that it emits v9 packets accepted by the
integrated checker.

## Verification

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json
```
