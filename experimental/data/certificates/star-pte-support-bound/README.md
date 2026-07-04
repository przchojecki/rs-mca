# Star-PTE Support Bound Certificate

This certificate pins the `h_window_derivation` micro-lemma packet
`star_pte_support_bound.md`.

Run:

```bash
python3 experimental/scripts/verify_star_pte_support_bound.py
```

The verifier checks the row arithmetic for `H_max = A`, the corrected
mid/large-`h` gap, endpoint finite-field fixtures for `r=0` and `r=k-1`,
and that the pinned JSON certificate matches those constants.
