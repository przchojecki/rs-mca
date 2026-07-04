# Exact Worst-Case eca/emca Staircase Certificates

This directory contains CPU-tier toy-row certificates for exact worst-case
finite-slope CA/MCA numerators.

Replay:

```powershell
python experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py --check experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_cpu_rows.json
```

Regenerate:

```powershell
python experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py --write
```

The verifier is stdlib-only. It uses syndrome-class representatives and
restricted-code parity checks; it does not materialize `q^k` codewords for the
high-rate rows.
