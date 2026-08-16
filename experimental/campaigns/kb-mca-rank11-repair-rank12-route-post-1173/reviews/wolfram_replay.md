# Wolfram exact replay

A stateless Wolfram Language replay independently evaluated:

- every displayed rank-twelve barrier resource, pair-type cap, direct cap,
  slack, and next-rank load;
- the rank-two endpoint values
  `131690`, `8550040`, `15`, `9`, `3`, `8829951`, and `279911`;
- the corrected rank-eleven recurrence;
- the residual-dimension weighted-line endpoint at `j=1`.

The selected rank-twelve output was:

```text
rank 11 -> ... -> rank 2 load 8,681,730
rank-two high                131,690
rank-two low               8,550,040
pair types max                    15
deficiency-one min                 3
capacity excess              279,911
```

All arithmetic was exact integer/rational arithmetic.  Wolfram is an
independent replay, not a source theorem.
