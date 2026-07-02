# M5 stratification partition certificate

This directory contains the deterministic JSON artifact emitted by:

```bash
python3 experimental/scripts/verify_m5_stratification_partition.py --emit
```

The packet verifies the first-match partition theorem for the v12 M5
stratification leaf layer.  It is a combinatorial accounting certificate, not a
Hankel root-table certificate.

The directory also includes two v12 packet-checker regression files:

```bash
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/m5-stratification-partition/valid_stratified_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/m5-stratification-partition/invalid_wrong_leaf_stratified_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/m5-stratification-partition/invalid_missing_removed_ledger_ref_packet.json
```

The valid packet demonstrates first-match dedup in an inline toy table.  The
invalid packet deliberately assigns a tangent-plus-quotient candidate to the
quotient leaf instead of the earlier tangent leaf.  The missing-reference packet
checks that removed-ledger claims point to an existing local certificate file.
