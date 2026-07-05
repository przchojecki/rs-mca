# SOV Affine-Piece Partition Certificate Soundness

Status: PROVED.

Source DAG node: `sov_affine_piece_partition_certificate_soundness`.

## Statement

If a certificate partitions every forced-root conditioning cell into:

- disjoint affine pieces on which `c(L)=[X^{h-1}]L` has nonzero linear part;
  and
- paid or norm-structured exceptional pieces whose total size is below the
  declared character-sum budget;

then `sov_hminus1_affine_piece_decomposition` holds.

## Proof

Fix an official-shape row, an `h in (20,A]`, and a forced-root
higher-coefficient conditioning cell `Omega`.

The certificate gives a disjoint partition of `Omega` into affine pieces
`P_alpha` and exceptional pieces `E_beta`. On each `P_alpha`, the coefficient
map

```text
c(L) = [X^{h-1}]L
```

is certified affine-linear with nonzero linear part. The exceptional pieces
are certified paid or norm-structured, and their total size is below the
declared character-sum budget.

This is exactly the decomposition asserted by
`sov_hminus1_affine_piece_decomposition`: every conditioned cell is covered by
cancellative affine pieces plus budget-small paid or norm-structured
exceptions. The cancellation on each nonconstant affine piece is supplied by
`sov_nonconstant_affine_character_cancellation`.

Since the same argument applies to every row, `h`, and conditioning cell, the
certificate has the intended SOV affine-piece decomposition meaning.

## Non-Claims

This packet proves only partition-certificate semantics. It does not construct
the anchored-core partitions and does not prove the conditional
`sov_hminus1_affine_piece_decomposition` payload by itself.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_sov_affine_piece_partition_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_affine_piece_partition_certificate_soundness.py \
  --check experimental/data/certificates/sov-affine-piece-partition-certificate-soundness/sov_affine_piece_partition_certificate_soundness.json
```

The verifier checks note anchors and a toy certificate with coverage,
disjointness, nonzero-linear-part, exceptional-kind, and budget gates.
