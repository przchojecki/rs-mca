# B1 Giant-Coset Certificate

This certificate pins the `b1_char0_giant_coset_theorem` verifier.

Run:

```bash
python3 experimental/scripts/verify_b1_giant_coset.py
```

The verifier checks exact cyclotomic arithmetic, full brute force at
`(n,t)=(16,4)`, rational-nullspace both-directions proofs at `(16,4)`,
`(32,4)`, and `(32,8)`, the least-2-power formula for `M`, the
signed-antipodal sanity witness, and the pinned JSON certificate.
