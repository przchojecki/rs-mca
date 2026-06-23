# M1 Cycle84 Witness Fixtures

Status: AUDIT / FINITE-MODEL-WITNESS.

This directory contains compact witness data for the Cycle84 finite model used
by `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`.

`slot_logs.json` gives one discrete log certificate for each of the 336
normalized slot values. It is checked by:

```sh
python3 experimental/scripts/verify_m1_cycle84_projected_log_certificate.py
```

The verifier checks that every log exponentiates to the current normalized slot
value, verifies colors and residue vectors, and checks the tau-pair projected
log structure. It does not rerun the projected duplicate-bin census.
