# M1 GAP-2 seam certificate

This directory contains the deterministic JSON artifact emitted by:

```bash
python3 experimental/scripts/verify_m1_gap2_seam_lemma.py --emit
```

The packet records the arithmetic closure of the rate-preserving
quotient-periodic seam: under `M | gcd(n,k)`, exact-bucket support divisibility
`M | j` is equivalent to window divisibility `M | t_win`.
