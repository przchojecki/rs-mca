# X24 Characteristic-Zero Dyadic-Descent Certificate

This certificate pins the `x24_char0_dyadic_descent` theorem packet.

Run:

```bash
python3 experimental/scripts/verify_x24_char0_dyadic_descent.py
```

The verifier enumerates exact small characteristic-zero dyadic rows,
checks that all trades match the full-fiber classifier, verifies non-power
`h` emptiness in the checked rows, and confirms that the pinned JSON
certificate matches the recomputed summary.
