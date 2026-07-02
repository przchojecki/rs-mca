# M1 displacement-uniform certificate

This directory contains the deterministic JSON artifact emitted by:

```bash
python3 experimental/scripts/verify_m1_displacement_uniform.py --emit
```

The packet verifies the subgroup Hankel `V^T D V` factorization, determinant
lemma reduction, Toeplitz-Cauchy rank-one displacement, and Lagrange-Cauchy
factorization over `(F_13, mu_4)`, `(F_17, mu_16)`, and `(F_49, mu_16)`.
