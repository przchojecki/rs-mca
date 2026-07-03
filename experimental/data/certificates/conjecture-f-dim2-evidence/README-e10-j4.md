# E10 j=4 Grassmannian census

This companion artifact extends the E7 dimension-two evidence packet with the
pre-registered E10 `j=4` Grassmannian census over `F_17^*`.

Replay:

```bash
python3 experimental/scripts/verify_conjecture_f_dim2_j4_grassmannian.py --emit
python3 experimental/scripts/verify_conjecture_f_dim2_j4_grassmannian.py \
  --check experimental/data/certificates/conjecture-f-dim2-evidence/conjecture_f_dim2_j4_grassmannian.json
```

The replay enumerates all `25,734,890` projective planes in
`P(F_17[X]_{<=4})`, using the dual Grassmannian of projective lines in `P^4`.
It is intentionally heavier than the base E7 verifier.
