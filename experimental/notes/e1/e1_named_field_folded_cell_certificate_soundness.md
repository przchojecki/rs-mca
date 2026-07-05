# E1 Named-Field Folded Cell Certificate Soundness

Status: PROVED.

Source DAG node: `e1_named_field_folded_cell_certificate_soundness`.

## Statement

For each `N' in {128,256}`, if:

- `e1_pocklington_250bit_exhibit_field` supplies a prime field `F_p` with
  `p = 1 mod N'` and a primitive `N'`th root;
- the corresponding no-vector payload supplies a complete folded-kernel
  certificate over that named field; and
- the certificate records zero nonzero non-cyclotomic folded vectors;

then `e1_folded_certificate_cell_N_payload` holds for that cell.

## Proof

Fix `N' in {128,256}`.

The E1 cell payload asks for a named exhibit field, a primitive `N'`th root
for the folded equation, and a complete certificate excluding every nonzero
non-cyclotomic folded vector in `{-2,-1,0,1,2}^{N'/2}`.

The proved field packet supplies the first two pieces: a prime field `F_p`
with `p = 1 mod N'` and a displayed primitive `N'`th root.  The corresponding
no-vector payload supplies the remaining piece: a complete certificate, over
that exact named field/root, whose result count is zero.

Combining those records gives exactly the cell schema: named field, primitive
root, complete folded certificate, and zero nonzero folded vectors.  Hence the
cell payload holds.

## Non-Claims

This packet does not supply either no-vector payload.  It only proves that the
named field/root plus a complete zero folded certificate satisfies the cell
schema.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_e1_named_field_folded_cell_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_named_field_folded_cell_certificate_soundness.py \
  --check experimental/data/certificates/e1-named-field-folded-cell-certificate-soundness/e1_named_field_folded_cell_certificate_soundness.json
```
