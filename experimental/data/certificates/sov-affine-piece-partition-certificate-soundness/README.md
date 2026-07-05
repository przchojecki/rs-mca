# SOV Affine-Piece Partition Certificate Soundness

This directory stores the replayable certificate for
`experimental/notes/sov/sov_affine_piece_partition_certificate_soundness.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_sov_affine_piece_partition_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_affine_piece_partition_certificate_soundness.py \
  --check experimental/data/certificates/sov-affine-piece-partition-certificate-soundness/sov_affine_piece_partition_certificate_soundness.json
```

The verifier checks note anchors and a toy partition-certificate schema. It
does not construct the actual SOV anchored-core partitions.
