# MCA Unsafe

Status: PROVED.

Source DAG node: `mca_unsafe`.

## Statement

At the adjacent unsafe grid point,

```text
B_C(a_safe - 1) > B*.
```

The assembly consumes the cap theorem, the zone-(b) localization/input, and the
adjacent witness packet `unsafe_at_crossing`.

## Dependency Sub-DAG

```text
cap_theorem        -> mca_unsafe
zone_b             -> mca_unsafe
unsafe_at_crossing -> mca_unsafe
```

The integrated prize DAG marks all three inputs as `PROVED`.

## Proof

The cap theorem supplies the global cap location: the challenge threshold is
below the printed cap gap for the admissible fields and rates.  The zone-(b)
input identifies the relevant crossing-scale witness family and keeps the
unsafe-side comparison in the intended quotient/value-set corridor.

The `unsafe_at_crossing` packet then supplies the local adjacent witness:
for every admissible row, either the collision-free `qfloor_exact` route or
the collided `averaged_slope_conversion` route gives more than `B*` bad slopes
at `a_safe - 1`.

Combining the global cap location with that adjacent witness gives
`B_C(a_safe - 1) > B*`, which is the unsafe-side assembly claim.

## Non-Claims

This packet does not edit Paper D, does not recompute the universal-cap proof,
does not rerun zone-(b) collision checks, and does not choose deployed v13 row
primes.

## Replay

```bash
python3 experimental/scripts/verify_mca_unsafe.py --emit
python3 experimental/scripts/verify_mca_unsafe.py \
  --check experimental/data/certificates/mca-unsafe/mca_unsafe.json
```
