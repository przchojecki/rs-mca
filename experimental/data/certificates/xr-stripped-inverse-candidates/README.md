# XR Stripped Inverse Candidate Certificate

This directory stores the E11/E2b candidate-family scan emitted by:

```bash
python3 experimental/scripts/verify_xr_stripped_inverse_candidates.py --emit
```

The certificate ranks fixed-core, fixed-hole, and quotient block-profile cells
by exact Johnson `E_3` energy for `J(16,8)` and `J(32,16)`, then records the
top list after quotient-profile cells are stripped.
