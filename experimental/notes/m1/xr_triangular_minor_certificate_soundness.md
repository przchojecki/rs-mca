# XR Triangular Minor Certificate Soundness

Status: PROVED.

Source DAG node: `xr_triangular_minor_certificate_soundness`.

## Statement

For an XR light-profile normal-form matrix, suppose a certificate selects a
maximal square minor and an admissible chart specialization such that the
specialized minor matrix is triangular and every diagonal entry is nonzero.

Then the determinant at that specialization is nonzero, so the certificate is
a valid nonzero-minor specialization certificate for the XR minor-specialization
semantics.

## Proof

Let `A` be the specialized square minor matrix named by the certificate.
Because the specialization is admissible, the entries of `A` live in the
coefficient field of the profile chart.

If `A` is upper or lower triangular, its determinant is the product of its
diagonal entries:

```text
det(A) = prod_i A_{ii}.
```

This follows from the Leibniz determinant formula: every permutation except
the identity uses at least one entry on the zero side of the triangular matrix
and therefore contributes zero.

The certificate asserts that every diagonal entry is nonzero. Since the
coefficient ring after admissible specialization is a field, the product of
nonzero diagonal entries is nonzero. Hence `det(A) != 0`.

Therefore a triangular certificate with nonzero diagonal is a valid nonzero
minor specialization certificate.

## Non-Claims

This packet proves only one accepted certificate format. It does not construct
the profile inventory and does not claim that every profile has a triangular
certificate.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_xr_triangular_minor_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_triangular_minor_certificate_soundness.py \
  --check experimental/data/certificates/xr-triangular-minor-certificate-soundness/xr_triangular_minor_certificate_soundness.json
```
