# F17^32 M3 Low-Rank2-11 v10 Affine GCD Certificate

This directory contains a standalone Paper D v10 affine rank-drop certificate
for the synthetic low-rank M3 ladder at ranks `2..11` over the accepted row

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

The verifier uses only accepted upstream artifacts: the row descriptor, the
regular-window plan, the generic regular-minor certificate, and Paper D v10.
It does not import the broader unmerged low-rank packet.

For each of the `420` rank/agreement rows, the verifier displays two maximal
minors: the prefix rows `0..j` and the row-shifted rows `1..j+1`.  It computes
both from the low-rank Lagrange-kernel formula and checks that their gcd in
`F_17^32[Z]` is constant.  Since the Paper D v10 affine rank-drop gcd divides
the gcd of any two nonzero maximal minors, the canonical affine rank-drop root
set is empty for these structured branches.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_v10_affine_gcd.py \
  --write experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-v10-affine-gcd/f17_32_n512_k256_m3_low_rank2_11_v10_affine_gcd.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_v10_affine_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-v10-affine-gcd/f17_32_n512_k256_m3_low_rank2_11_v10_affine_gcd.json
```

Non-claims: this is a synthetic low-rank ladder certificate only, not an
arbitrary M3 row theorem, not an actual-row threshold certificate, and not a
singular pivot classification.  It proves only the finite affine v10
rank-drop closure; projective endpoint charging is left to a separate packet.
