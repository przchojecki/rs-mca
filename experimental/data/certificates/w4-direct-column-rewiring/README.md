# W4 Direct-Column Rewiring Certificate

This certificate pins the `w4_direct_column_rewiring` verifier.

Run:

```bash
python3 experimental/scripts/verify_w4_direct_column_rewiring.py
```

The verifier reads the bundled W4 DAG fixture plus QA25, X10, and B-writeup
certificate inputs, checks that the U1/B consumers share a single primitive
split-pair column, checks exact row-wise `n^3` budget room, and confirms that
the pinned JSON certificate matches the recomputed summary.  The fixture is a
verifier input for this packet, not the final DAG update.
