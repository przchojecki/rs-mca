# F17^32 M3 One-Spike v10 Rank-Drop Certificate

This directory contains a Paper D v10 rank-drop certificate for the
non-proportional one-spike branch over the pinned row

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

The v10 regular-Hankel ledger uses the gcd of all nonzero maximal minors in an
exact-agreement bucket.  For this one-spike branch it is enough to display two
valid maximal minors: the prefix rows `0..j` and the row-shifted rows `1..j+1`.
The certificate checks that these two affine minors are coprime for every
`A=385..426`.  Since the canonical v10 gcd divides their gcd, the affine
rank-drop gcd is constant and the finite affine rank-drop root set is empty.

The projective endpoint `[0:1]` remains nonempty because the displayed affine
one-spike minors have degree `1 < j+1`.  The companion full-Hankel ledger
charges that endpoint to quotient-image, so the aperiodic projective residual
for this branch is `0`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_v10_rank_drop.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-v10-rank-drop/f17_32_n512_k256_m3_one_spike_v10_rank_drop.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_v10_rank_drop.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-v10-rank-drop/f17_32_n512_k256_m3_one_spike_v10_rank_drop.json
```

Non-claims: this is a synthetic one-spike branch only, not an arbitrary M3 row
theorem, not an actual-row threshold certificate, and not a singular pivot
classification.
