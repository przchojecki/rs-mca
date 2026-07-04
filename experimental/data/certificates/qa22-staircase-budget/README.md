# QA.22 Staircase Budget Certificate

This certificate pins the staircase budget column for DAG node
`x4_exactlist_staircase_split`.

In this A3 packet, the certificate is consumed by:

```bash
python3 experimental/scripts/verify_a3_good_reduction.py
```

The full QA.22 arithmetic packet has its own verifier.  The A3 verifier only
checks the subset of this certificate needed by `a_closure_assembly.md`: the
six-row `16n^3` polynomial column.

The full QA.22 verifier computes, for the six clean-rate candidates in
`xr_budget_audit.md`:

- the X-4 fixed-tail quotient staircase terms
  `C(n/M - 1, floor(A/M))` for every `M | n`, `M > t`;
- the Chebyshev/dihedral fixed-tail analogue on the quotient row;
- max and sum columns, log2 displays, and transported quotient-row tables;
- the exact budget check
  `Staircase + B_tan_max + 16n^3 <= B*`.
