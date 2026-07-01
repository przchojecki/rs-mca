# F17^32 M3 A=426 Contiguous-GCD Packet

Status: PROVED / AUDIT for this synthetic finite replay.

This directory contains a replayable `aperiodic-hankel-eliminant-v1` packet for
a bounded common-gcd audit at `A=426` in the M3 regular non-tangent window of
`RS[F_17^32,H,256]`, `|H|=512`.

The input uses the same zero-`u` synthetic syndrome pencil as the A=426
rank-witness endpoint packet, but the extractor checks the first four
contiguous maximal row sets instead of only the prefix row set.  Each audited
minor has the form

```text
Delta_i(Z) = c_i Z^87,
```

with `c_i != 0`, so their monic common gcd is `Z^87` and the exact root table
is `{0}`.

This is a compact step toward the v10 canonical regular-minor gcd branch.  It
is still a bounded synthetic subatlas, not the all-minor canonical gcd, not a
worst-case row bound, and not a singular-bucket classification.

The raw root `{0}` is paid by the tangent ledger in:

```text
experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/
```

The subgroup line-value realization of the synthetic syndrome input is
recorded in:

```text
experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/
```

Regenerate and check:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --minor-gcd-contiguous-limit 4 \
  --write experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --minor-gcd-contiguous-limit 4 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json \
  --write experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/f17_32_n512_k256_a426_contiguous_gcd4_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/f17_32_n512_k256_a426_contiguous_gcd4_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/f17_32_n512_k256_a426_contiguous_gcd4_packet.json
```
