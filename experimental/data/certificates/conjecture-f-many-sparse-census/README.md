# Conjecture F Many-Sparse Census Certificate

This directory stores the exact toy E9/QF.8 census emitted by:

```bash
python3 experimental/scripts/verify_conjecture_f_many_sparse_census.py --emit
```

The certificate enumerates all codimension-one projective flats in
`P(F_17[X]_{<=3})` and `P(F_17[X]_{<=4})`, counts sparse dual words of support
`1`, `2`, and `3`, and records the resulting common-root, twin,
support-3-only, and dual-distance-`>=4` buckets.
