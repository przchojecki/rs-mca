# F17^32 M3 Endpoint c=2 Quotient-Image Capacity

This certificate records the structural endpoint capacity for the synthetic M3
low-rank ladder in the window `385 <= A <= 426`.

For agreement `A`, put `j = 512-A`.  The projective endpoint `[0:1]` is
quotient-image witnessed by a `c=2` quotient-remainder support for every
synthetic rank

```text
2 <= rank <= 256 - floor(A/2) = ceil((512-A)/2).
```

The proof is a direct full-fiber capacity count.  A support of size `A` needs
`floor(A/2)` complete `c=2` fibers that avoid the update block `Y`.  In this
synthetic ladder, `Y` occupies `rank` distinct residues below the quotient
modulus, so exactly `256-rank` complete fibers avoid it.  For odd `A`, the
single residual point can be taken from the paired point of a blocked residue at
the boundary rank.

Thus endpoint quotient-image charging is available uniformly through rank `43`
across the whole M3 window, and through rank `64` at the low-agreement end.
This does not audit finite affine rank-drop roots; it is a reusable endpoint
subledger for future affine-gcd or pivot-chart packets.

Run:

```bash
python3 experimental/scripts/verify_f17_32_m3_endpoint_c2_capacity.py \
  --write experimental/data/certificates/hankel-f17-32-m3-endpoint-c2-capacity/f17_32_n512_k256_m3_endpoint_c2_capacity.json

python3 experimental/scripts/verify_f17_32_m3_endpoint_c2_capacity.py \
  --check experimental/data/certificates/hankel-f17-32-m3-endpoint-c2-capacity/f17_32_n512_k256_m3_endpoint_c2_capacity.json
```

Nonclaims: endpoint quotient-image witnesses only, synthetic low-rank update
blocks only, no finite affine regular-minor roots, no arbitrary-row M3
threshold theorem.
