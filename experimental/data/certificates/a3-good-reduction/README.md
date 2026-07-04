# A3 Good-Reduction Certificate

This certificate pins the `a3_good_reduction_lemma` packet and its
conditional `(A)` closure assembly arithmetic.

Run:

```bash
python3 experimental/scripts/verify_a3_good_reduction.py
```

The verifier checks the symbolic square-shift graph identities, the
`n=16,h=3` end-to-end good-reduction toy mechanism, exact anchored/orbit
accounting, the QA.22/W4 arithmetic consumed by the closure assembly, and
that the pinned JSON certificate matches those constants.
