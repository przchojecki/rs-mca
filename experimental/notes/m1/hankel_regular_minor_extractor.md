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

reads a prime-field syndrome-pencil input.  For each exact agreement `A`, it
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
is recovered by interpolation from numeric determinants over `F_p`, rather than
by a factorial permutation determinant.  This is the right algorithmic shape
for the future `385 <= A <= 426` window once row data and extension-field
arithmetic are supplied.

When the field is small enough, the extractor enumerates roots in `F_p`.  When
the domain is supplied and the split-locator subset count is small enough, it
also enumerates split co-support bad slopes and checks that they are contained
in the extracted root set.

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

## Non-Claims

This does not solve the `F_17^32` regular window.  In particular, it does not
yet provide:

```text
an F_17^32 row-data adapter;
extension-field determinant/interpolation arithmetic;
quotient/tangent subtraction for 385 <= A <= 426;
singular pivot charts.
```

Those are the next M3/M4 steps.  The present contribution is the reusable
prime-field extractor and a replayable toy packet showing that the extractor
emits v9 packets accepted by the integrated checker.

## Verification

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json
```
