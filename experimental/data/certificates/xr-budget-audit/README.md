# XR Budget Audit Certificate

This directory pins the deterministic integer budget audit for DAG node
`xr_target_budget_audit`.

Run:

```bash
python3 experimental/scripts/verify_xr_budget_audit.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_xr_budget_audit.py --write-certificate
```

The verifier recomputes the pinned calibration row, all six clean-rate
decision rows, quotient/tangent budget ranges, and the exact clean-rate
allowance table recorded in `xr_budget_audit_certificate.json`.
