# X-10 Consumer Tolerance Ladder Certificate

This certificate records the exponent tolerance ladder for consumers of
`anchored_nontoral_pte_bound`.

Run:

```bash
python3 experimental/scripts/verify_x10_consumer_tolerance_ladder.py
```

The verifier reads the QA.22 and QA.25 arithmetic certificates, checks the
banked X-10 consumer dependencies, and emits exact row-room comparisons for
candidate bounds of the form `A_h^nt <= h*n^alpha`.
