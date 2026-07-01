# F17^32 M3 Low-Rank-2 A=426 Packet

This directory contains a deterministic v9 packet for the low-rank Hankel
update template at the M3 endpoint `A=426`.

The extractor input is

```text
experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json
```

It uses

```text
u_m = sum_{x in X} x^m,  |X|=87,
v_m = y_1^m + y_2^m,
```

where `X` is the first 87 nodes of the pinned `F_17^32` row descriptor and
`y_1,y_2` are the next two descriptor nodes.  The prefix regular minor has
degree at most `2` by the low-rank Cauchy-Binet formula.  In this instance the
compressed quadratic splits over `F_17^32`, so the packet records the exact two
roots, a split-linear factorization certificate, and a quadratic discriminant
certificate.  It also records the compressed determinant-lemma sidecar

```text
Delta(Z)=det(H_X) det(I+ZK)
```

with `K` computed from the Lagrange kernel on `X`; the checker recomputes this
sidecar from the replay input and uses the same compressed determinant-lemma
coefficients for low-rank coefficient replay.  The kernel replay uses the
barycentric Lagrange formula with batch inversion, so verifier cost is driven
by the small update-rank kernel rather than by one large-field inversion for
each basis value.

Run:

```sh
python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --low-rank-update-count 2 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/f17_32_n512_k256_a426_low_rank2_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/f17_32_n512_k256_a426_low_rank2_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/invalid_low_rank2_coefficient_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/invalid_low_rank2_compression_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/invalid_low_rank2_omitted_root_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/invalid_low_rank2_quadratic_root_packet.json
```

The invalid fixture changes one determinant coefficient and must fail the
low-rank coefficient replay.  The compression fixture changes one Lagrange
kernel entry and must fail the low-rank compression sidecar replay.  The
omitted-root fixture removes one of the two split roots and must fail exact root
certificate replay.  The quadratic-root fixture changes the recorded square
root of the discriminant and must fail the quadratic formula replay.

Non-claims: this is a synthetic syndrome-pencil stress packet and exact-root
certificate, not an actual-row M3 root table, quotient/tangent subtraction
ledger, or safe-side MCA bound.
