# Conjecture F dimension-two skeleton certificate

This directory contains the deterministic replay output for
`experimental/notes/m1/conjecture_f_dim2_skeleton.md`.

The verifier exhaustively enumerates every projective plane in
`F_17[X]_{<=3}` with `H=F_17^*`.  Common-root planes are routed to the paid
common-GCD branch.  Every remaining plane is checked for the all-or-none twin
rule, twin-branch division to a projective line, and the residual singleton
pair-counting bound.

Replay:

```bash
python3 experimental/scripts/verify_conjecture_f_dim2_skeleton.py --emit
python3 experimental/scripts/verify_conjecture_f_dim2_skeleton.py --check \
  experimental/data/certificates/conjecture-f-dim2-skeleton/conjecture_f_dim2_skeleton.json
```
