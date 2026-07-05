# XR Profile Minor Record-Inventory Soundness

Status: PROVED.

Source DAG node: `xr_profile_minor_record_inventory_soundness`.

## Statement

If an inventory covers every budget-meeting unpaid non-boundary
light-triangle profile and assigns each profile an admissible record of an
accepted nonzero-minor type, then `xr_profile_minor_certificate_payload` holds.

Accepted record types are:

- triangular maximal-minor specializations with nonzero diagonal;
- monomial/noncancellation certificates for a named maximal minor; and
- complete remote certificate-table entries giving a nonzero maximal-minor
  specialization.

## Proof

Let `P` be the set of budget-meeting unpaid non-boundary light-triangle
profiles. Assume an inventory `I` covers `P`, meaning every profile in `P`
appears with exactly one payload record or with a declared disjoint record
class whose multiplicity is accounted for.

For each profile, the record has one of the accepted forms.

For a triangular record, the proved triangular-minor certificate soundness
packet shows that an admissible specialized maximal-minor matrix with nonzero
diagonal has nonzero determinant.

For a monomial/noncancellation record, the record includes the named maximal
minor and the certified noncancelling monomial or specialization value, so it
directly supplies a nonzero determinant witness under the payload schema.

For a remote table record, completeness of the table entry means the row names
the profile, the maximal minor, the admissible specialization, and the nonzero
determinant value. Thus it also supplies an accepted nonzero-minor payload
record.

Since every profile in `P` is covered by one accepted record, the inventory
supplies exactly the profile-by-profile payload required by
`xr_profile_minor_certificate_payload`.

## Non-Claims

This packet does not construct the inventory. It only proves that a complete
inventory with accepted record types is sound for the XR profile-minor payload.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_xr_profile_minor_record_inventory_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_profile_minor_record_inventory_soundness.py \
  --check experimental/data/certificates/xr-profile-minor-record-inventory-soundness/xr_profile_minor_record_inventory_soundness.json
```
