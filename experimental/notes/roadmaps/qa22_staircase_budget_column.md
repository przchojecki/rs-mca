# QA.22: staircase budget column

- **DAG:** `x4_exactlist_staircase_split`.
- **Status:** AUDIT / arithmetic gate passed.
- **Verifier:** `experimental/scripts/verify_qa22_staircase_budget.py`.

## Critical-path role

This is a budget-column packet for the conditional prize proof path.  It
prices the quotient and dihedral staircase terms that must coexist with the
`16 n^3` post-strip residual reserve from
`xr_clean_poly_forcing_reduction.md`.  The exact check shows that these
staircase columns do not consume the polynomial-residue room at any of the six
clean-rate rows.

Thus the staircase arithmetic is not the terminal obstruction.  The remaining
conditional work stays localized in the algebraic post-strip split-pair/PTE
residue, while this packet certifies that the known staircase columns fit
inside the compiler budget.

## Conventions

For each of the six clean-rate candidates from `xr_budget_audit.md`, write
`A = k+t`.  The X-4 staircase term is interpreted literally as the fixed-tail
quotient-coset count

```text
Q_M = C(n/M - 1, floor(A/M)),        M | n, M > t.
```

This is the term named in the DAG node: the tail `B` is fixed, and the count is
over the full quotient cosets selected after that tail.  The verifier does not
multiply by arbitrary choices of the tail inside a size-`M` coset; that is a
different and unsupported column.

For the dihedral/Chebyshev analogue, the verifier uses the exact fixed-tail
orbit count on the quotient row of length `N=n/M`.  Inversion has two fixed
points and `(N-2)/2` moving pairs.

If `A = hM + b`:

```text
b = 0:  D_M = # inversion-closed h-subsets of the quotient row.
b > 0:  D_M = # inversion-closed h-subsets after one fixed tail cell is removed.
```

The charged staircase column is

```text
Staircase = sum_M Q_M + sum_M D_M.
```

The exact gate checked is

```text
Staircase + B_tan_max + 16 n^3 <= B*.
```

## Verdict

All six candidates pass.

```text
row    rate  A              log2 Qsum  log2 Dsum  log2 total  total margin  staircase room after 16n^3+Btan
RowC   1/4   261             99.8063    48.3804    99.8063      22.1937       22.1937
RowC   1/8   133             66.1465    31.8508    66.1465      55.8535       55.8535
RowC   1/16  67              82.9664    40.2857    82.9664      39.0336       39.0336
prize  1/4   558345748481    99.8063    48.3804   127.0000       0.9000       26.9863
prize  1/8   283467841537    66.1465    31.8508   127.0000       0.9000       60.6460
prize  1/16  141733920769    82.9664    40.2857   127.0000       0.9000       43.8261
```

The row-wise maximum is always the first admissible scale:

```text
RowC 1/4 and prize 1/4:   M first gives N=n/M=128, h=32, log2 Q_M=99.8063.
RowC 1/8 and prize 1/8:   N=128, h=16, log2 Q_M=66.1465.
RowC 1/16 and prize 1/16: N=256, h=16, log2 Q_M=82.9664.
```

## Important Finding

The rough expectation "13--23 bits of room at prize rows" is not the margin for
the full requested inequality.  In the prize rows,

```text
16 n^3 = 2^127,        log2 B* = 127.9,
```

so the full total margin is only about `0.9` bits.  The staircase column itself
is far below the remaining allowance after `16n^3 + B_tan_max` is removed:
`26.99`, `60.65`, and `43.83` bits of staircase room at rates `1/4`, `1/8`,
and `1/16`.

No row fails the gate, but the full prize-row inequality is dominated by the
pre-existing `16n^3` compiler allowance, not by the X-4 staircase column.

## Transported Quotient-Row Table

The complete transported table is pinned in
`experimental/data/certificates/qa22-staircase-budget/qa22_staircase_budget.json`
under `transported_quotient_row_table`.  Each entry records:

```text
M, scale_n_over_M, quotient_k_floor, quotient_A_floor, tail_b,
Q_M, D_M.
```

These are the same quotient-row scales consumed by TR's per-leaf split.

## Verification

Run:

```bash
python3 experimental/scripts/verify_qa22_staircase_budget.py
```

Current certificate replay: **27 PASS, 0 FAIL**.
