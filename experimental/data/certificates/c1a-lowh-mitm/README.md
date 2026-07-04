# C1a Low-h MITM Certificates

This directory pins the Row-C stand-in certificates for DAG node
`c1a_lowh_direct_certificates`.

Light review commands:

```bash
python3 experimental/scripts/verify_c1a_lowh_mitm.py
python3 experimental/scripts/verify_c1a_lowh_mitm.py --verify-cert
```

The default command replays validation gates, including the non-toral
detection gate at the exceptional `(16,4,F17)` row. The `--verify-cert`
command checks the emitted Row-C JSON certificates for schema consistency,
zero non-toral primitive trades, toral totals, and the stand-in prime
condition. The full production replay is available with `--all`, but it is
intentionally not the default review command.
