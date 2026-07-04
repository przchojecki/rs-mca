# QA.25: boundary-scale zero-sum column

- **DAG:** `u2c_boundary_scale_column`.
- **Task:** QA.25.
- **Status:** arithmetic gate passed; residual dichotomy remains open.
- **Verifier:** `experimental/scripts/verify_qa25_boundary_scale_column.py`.
- **Certificate:**
  `experimental/data/certificates/qa25-boundary-scale-column/qa25_boundary_scale_column.json`.

## Critical-path role

This is a budget-column repair packet for the conditional prize proof path.
It adds the boundary zero-sum column missing from the strict `M > t`
staircase arithmetic and checks that the repaired total still fits the same
compiler inequality used by `xr_clean_poly_forcing_reduction.md`.

The packet closes the arithmetic side of the boundary-scale issue only.  It
does not prove the structural U2-C residual dichotomy; if that dichotomy
produces a new primitive residue, the budget must be revisited with that extra
column.

## Convention

QA.22 prices the strict quotient staircase at dyadic scales `M > t`.  X-8
found the missing boundary mechanism: at the first boundary scale, primitive
quotient patterns with zero quotient sum are chargeable and must be added as a
separate column.

The six campaign rows have 2-power domains but their exact `t = A-k` values
are not themselves powers of two.  The verifier therefore records the dyadic
boundary predecessor

```text
M0 = 2^floor(log2 t),        M0 <= t < 2 M0,
R  = n/M0.
```

It also records whether the literal subgroup equality `M0 = t` holds.  It does
not: all six rows use the non-2-power row-shape boundary proxy described in the
DAG node.

For the primitive boundary column, the budgeted count is the X-8
antipodal-free quotient count

```text
ceil(2^(R/2) / q_min^e),     e = floor(t/M0),
q_min = B* 2^128.
```

The verifier also emits a diagnostic unstripped count `ceil(2^R/q_min^e)`.
That diagnostic is not budgeted here; it is the all-quotient-subset count, not
the primitive boundary column after the antipodal/next-scale strip.

## Exact Crossover

For raw primitive pattern count `P = 2^(R/2)`, the exact `B*` crossover is the
smallest integer `B` satisfying

```text
ceil(P / (B 2^128)^e) <= B,
```

equivalently

```text
P <= B^(e+1) 2^(128e).
```

This is computed by exact integer roots.  Every campaign row lies above its
crossover before any floating-point approximation is used.

## Result

All six rows pass after adding the boundary column to the QA.22 total.

```text
row    rate   M0              R     ceil boundary   log2 B*_cross   q-margin above crossover
RowC   1/4    4               256   1               0.0             122.0 bits
RowC   1/8    4               256   1               0.0             122.0 bits
RowC   1/16   2               512   64              64.0             58.0 bits
prize  1/4    2^33            256   1               0.0             127.9 bits
prize  1/8    2^33            256   1               0.0             127.9 bits
prize  1/16   2^32            512   2               64.0             63.9 bits
```

The repaired full budget check is still dominated by the earlier QA.22 total:

```text
boundary ceil column = 1, 1, 64, 1, 1, 2.
```

Adding these to `QA.22 total = staircase + B_tan_max + 16n^3` preserves

```text
QA.22 total + QA.25 boundary column <= B*
```

at every row.  The prize rows keep the same visible `~0.9`-bit aggregate margin
because the new column is at most `2`, while the existing `16n^3` reserve is
already `2^127`.

## Honest Residual

This closes the arithmetic gate only.  The structural U2-C' statement still
needs the separate residual-dichotomy proof or falsifier:

```text
every t-null block is a union of mu_M-cosets with M >= t, including the
boundary zero-sum column, or else a new primitive residue must be reported.
```

That is the `U2C-PRIME` follow-up, not part of QA.25.

## Verification

Run:

```bash
python3 experimental/scripts/verify_qa25_boundary_scale_column.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_qa25_boundary_scale_column.py --write-certificate
```

Current certificate replay: **34 PASS, 0 FAIL**.
