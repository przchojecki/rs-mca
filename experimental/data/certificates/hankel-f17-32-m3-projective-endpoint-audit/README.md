# F17^32 M3 Projective Endpoint Audit

This directory contains a compact sidecar audit for the fixed synthetic
top-window packet

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The source v9 packet is finite-affine.  This audit checks the extra
projective slope `[0:1]`: for every `A=421..426`, the prefix regular-minor
determinant is a nonzero scalar times `Z^(j+1)`, so its homogenization is
nonzero at `[0:1]`.  Hence projectivizing this fixed synthetic stress packet
adds no infinity root.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_projective_endpoint_audit.py \
  --write experimental/data/certificates/hankel-f17-32-m3-projective-endpoint-audit/f17_32_n512_k256_a421_426_projective_endpoint_audit.json

python3 experimental/scripts/verify_f17_32_m3_projective_endpoint_audit.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-endpoint-audit/f17_32_n512_k256_a421_426_projective_endpoint_audit.json
```

Non-claims: this is not actual M3 row data, not a worst-case MCA bound, and
not a replacement for a projective v9 packet.  It only audits the missing
endpoint for the existing fixed synthetic packet.
