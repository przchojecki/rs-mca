# F17^32 M3 One-Spike Window Projective-Line Packet

This directory contains a Paper D v9 projective-line packet for the
non-proportional one-spike branch over the pinned row

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

For each exact agreement `A`, the affine regular minor has the one-spike form
`C0(A)+Z*C1(A)` and therefore one finite root.  In the projective-line
homogenization the determinant has degree `1 < j+1`, so the shared endpoint
`[0:1]` is nonempty.  The packet's v9 numerator is therefore `42 + 1 = 43`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_window_projective_packet.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-window-projective-line/f17_32_n512_k256_m3_one_spike_window_projective_line_packet.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_window_projective_packet.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-window-projective-line/f17_32_n512_k256_m3_one_spike_window_projective_line_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-one-spike-window-projective-line/f17_32_n512_k256_m3_one_spike_window_projective_line_packet.json
```

This projective packet is deliberately paired with the full-Hankel ledger in
`../hankel-f17-32-m3-one-spike-window-full-hankel/`: the v9 projective packet
records the regular-minor endpoint, while the full-Hankel ledger proves that
all finite roots are shifted-minor artifacts and the endpoint is charged to
quotient-image, leaving aperiodic full-Hankel residual `0`.

Non-claims: this is a synthetic one-spike packet only, not an arbitrary M3 row
theorem and not an actual-row threshold certificate.
