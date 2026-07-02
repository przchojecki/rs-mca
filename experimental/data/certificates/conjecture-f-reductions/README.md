# Conjecture F reduction lemmas toy certificate

This directory contains the toy verifier output for
`experimental/notes/m1/conjecture_f_reduction_lemmas.md`.

- `conjecture_f_reductions_toy.json` records exact checks over `F_97` with
  `H = mu_16`: common-GCD reduction, quotient-pullback recursion,
  dimension-one voting, and the hyperplane-concurrency reformulation on
  random projective planes.  It also checks the vanishing-flat dimension bound,
  the weighted projective-plane pair-counting bound, including forced
  repeated-line planes, the twin-line decomposition into common-GCD line
  charts plus a sharp simple-line residual, the sparse-dependence
  closure/descent rule, the dual-distance moment frame, and the
  fixed-dimensional incidence bound with the sharp full-space case.  The
  later checks force
  common roots, divide them out, verify the reduced fixed-dimensional bound,
  descend quotient-pullback strata, sum proper quotient-union bounds, test
  affine chart consumers, print exponent budgets, test the polynomial
  chart-atlas consumer, and check Johnson-ball/FM1 high-overlap common-core
  covers.
- The verifier is
  `experimental/scripts/verify_conjecture_f_reductions.py`.

Replay:

```bash
python3 experimental/scripts/verify_conjecture_f_reductions.py --emit
```
