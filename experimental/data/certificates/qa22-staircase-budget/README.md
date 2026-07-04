# QA.22 Staircase Budget Certificate

This certificate pins the staircase budget column for DAG node
`x4_exactlist_staircase_split`.

Run:

```bash
python3 experimental/scripts/verify_qa22_staircase_budget.py
```

The verifier computes, for the six clean-rate candidates in
`xr_budget_audit.md`:

- the X-4 fixed-tail quotient staircase terms
  `C(n/M - 1, floor(A/M))` for every `M | n`, `M > t`;
- the Chebyshev/dihedral fixed-tail analogue on the quotient row;
- max and sum columns, log2 displays, and transported quotient-row tables;
- the exact budget check
  `Staircase + B_tan_max + 16n^3 <= B*`.
