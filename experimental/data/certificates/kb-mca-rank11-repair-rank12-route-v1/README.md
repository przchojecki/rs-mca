# KoalaBear raw-low rank-eleven repair certificate

This certificate freezes the uniform weighted-line theorem, the corrected
raw-low rank-eleven induction, the guarded dense-core theorem, the
rank-twelve single-threshold method wall, and all nonclaims.

Run:

```bash
python3 experimental/scripts/verify_kb_mca_rank11_repair_rank12_route_v1.py
python3 -O experimental/scripts/verify_kb_mca_rank11_repair_rank12_route_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_repair_rank12_route_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank11_repair_rank12_route_v1.py
HOME=/private/tmp /usr/local/bin/sage \
  experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/controls/gf11_truncated_margin_counterexample.sage
python3 experimental/scripts/verify_kb_mca_rank11_repair_rank12_route_manifest_v1.py
```

Maintainers regenerate the manifest only after every packet-bound file is
frozen, using the manifest verifier with its write flag.

The normal manifest command is fail-closed: it reconstructs the complete
expected manifest and rejects any missing, stale, or extra packet metadata.
