# Conjecture F reduction lemmas toy certificate

This directory contains the toy verifier output for
`experimental/notes/m1/conjecture_f_reduction_lemmas.md`.

- `conjecture_f_reductions_toy.json` records exact checks over `F_97` with
  `H = mu_16`: common-GCD reduction, quotient-pullback recursion,
  dimension-one voting, and the hyperplane-concurrency reformulation on
  random projective planes.
- The verifier is
  `experimental/scripts/verify_conjecture_f_reductions.py`.

Replay:

```bash
python3 experimental/scripts/verify_conjecture_f_reductions.py --emit
```
