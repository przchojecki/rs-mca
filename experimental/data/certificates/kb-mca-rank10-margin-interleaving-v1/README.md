# Rank-ten margin/interleaving certificate

Replay from the repository root:

```bash
python3 experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.py
python3 -O experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.py
python3 experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.py --tamper-selftest
sage experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.sage
```

The primary verifier scans all (67{,}471) legal thresholds for explanation
ranks 9--12 with exact integers/rationals.  It checks the sextic field guard,
the first paying threshold, the unique optimum, adjacent totals, rank-11
nonpayment, and the exact GF(11) multiplicity fixture.

Wolfram Cloud independently replayed the (T=667) components and slack on
2026-08-13.  Exa reviewed 20 research results across two targeted searches;
the relevant literature concerns broader interleaved/list-recovery bounds,
not this elementary finite-field projection identity, so no external lemma is
load-bearing.
