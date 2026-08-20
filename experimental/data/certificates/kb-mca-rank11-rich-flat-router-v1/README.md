# KoalaBear rank-eleven rich-flat router certificate

This directory freezes the exact output of
`experimental/scripts/verify_kb_mca_rank11_rich_flat_router_v1.py` for the
one-commit successor to PR #1172.

Canonical theorem cell:

```text
tau                 1547
h                   42452
emitted core        42453
total               274978720888758363
slack               2007222636724
```

Run from the repository root:

```sh
python3 experimental/scripts/verify_kb_mca_rank11_rich_flat_router_v1.py
python3 -O experimental/scripts/verify_kb_mca_rank11_rich_flat_router_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_rich_flat_router_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank11_rich_flat_router_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_rich_flat_manifest_v1.py
```
