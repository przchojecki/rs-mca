# CS25 v12 Deployed Certificate Audit

This directory contains a machine-readable version of the deployed-row
certificate tuples printed in `tex/cs25_cap_v12.tex`, together with the
adjacent deployed profile corollary check.

Replay:

```bash
python3 experimental/scripts/verify_cs25_v12_deployed_certificates.py
```

The verifier uses exact integer arithmetic only.  Passing this packet is an
`AUDIT` result: it checks the printed integer inequalities, not the surrounding
mathematical theorem chain.
