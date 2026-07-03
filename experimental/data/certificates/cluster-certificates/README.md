# Cluster Certificates

This directory contains the replayable arithmetic packet for
`experimental/notes/thresholds/cluster_certificates.md`.

Replay:

```text
python3 experimental/scripts/verify_cluster_certificates.py
```

Regenerate:

```text
python3 experimental/scripts/verify_cluster_certificates.py --emit
```

The packet checks local free cliques, multiplicative cross-cluster
certification, and integer-factor certification in small cyclotomic fields.
