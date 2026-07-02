# Conjecture F reduction lemmas toy certificate

This directory contains the toy verifier output for
`experimental/notes/m1/conjecture_f_reduction_lemmas.md`.

- `conjecture_f_reductions_toy.json` records exact checks over `F_97` with
  `H = mu_16`: common-GCD reduction, quotient-pullback recursion,
  dimension-one voting, and the hyperplane-concurrency reformulation on
  random projective planes.  It also checks the vanishing-flat dimension bound,
  the weighted projective-plane pair-counting bound, including forced
  repeated-line planes, and the fixed-dimensional incidence bound with the
  sharp full-space case.  The final check forces common roots, divides them
  out, and verifies the reduced fixed-dimensional bound.
- The verifier is
  `experimental/scripts/verify_conjecture_f_reductions.py`.

Replay:

```bash
python3 experimental/scripts/verify_conjecture_f_reductions.py --emit
```
