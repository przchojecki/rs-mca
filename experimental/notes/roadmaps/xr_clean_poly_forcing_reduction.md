# XR clean-rate polynomial forcing reduction

- **Status:** PROVED compiler / CONDITIONAL consumer. The integer
  inequality below is verified exactly by
  `experimental/scripts/verify_xr_clean_poly_forcing.py` (stdlib only; current
  certificate target:
  `experimental/data/certificates/xr-clean-poly-forcing/xr_clean_poly_forcing_certificate.json`).
- **DAG:** `xr_clean_residual_any_gate`.
- **Parents:** `xr_target_budget_audit`, `dihedral_staircase` (QA21-G1), and
  the face-4 instance of `rigidity_kernel`.

## Critical-path role

This is the compiler step in the conditional prize proof path.  It does not
prove the algebraic residual bound; instead it proves the exact integer fact
that the clean-rate rows only need a polynomial post-strip cap.  In particular,
once the proof spine supplies

```text
R_post(u,v; A) <= 16 n^3,
```

the quotient and tangent ledgers plus this compiler put every clean-rate row
below `B*`.

This is why the remaining terminal node can be stated as the localized
`active_core_count_bound` / PTE polynomial residue rather than as a global
emptiness theorem.  The packet is unconditional arithmetic; the conditional
status enters only through the downstream algebraic input `R_post <= 16 n^3`.

## 1. Claim

For each of the six clean-rate decision candidates from the XR audit
(Row C and prize-max at rates `1/4`, `1/8`, `1/16`), define

```text
s_lo(A) = B* - B_quot_ub(A) - B_tan_max(A).
```

Then

```text
16 n^3 <= s_lo(A)
```

at every clean-rate candidate. Consequently, for a fixed pair `(u,v)`, if the
post-strip non-quotient/non-tangent residual slope count at that candidate is
at most `16 n^3`, then the pair is below the bad-slope budget `B*`.

Equivalently, after the proved quotient and tangent ledgers are charged, the
remaining clean-rate obligation is no longer an emptiness statement. It is the
polynomial forcing statement

```text
R_post(u,v; A) <= 16 n^3.
```

This note proves only the compiler. The algebraic input `R_post <= 16 n^3` is
exactly the remaining face-4 RK/dihedral-staircase obligation.

## 2. Proof

Fix one clean-rate row and one pair `(u,v)`. The XR audit gives a safe upper
bound for the already-paid slopes:

```text
paid(u,v; A) <= B_quot_ub(A) + B_tan_max(A).
```

Let `R_post(u,v; A)` be every remaining slope counted after that strip,
including primitive aperiodic residue and any dihedral/extension column not
already included in the two ledgers above. If `R_post(u,v; A) <= 16 n^3`, then

```text
total_bad_slopes(u,v; A)
  <= B_quot_ub(A) + B_tan_max(A) + 16 n^3
  <= B*.
```

The last inequality is exact integer arithmetic. The verifier recomputes
`B_quot_ub` with the same active-scale rule as `verify_xr_budget_audit.py`,
checks the audit pins for `A` and `s_lo`, and then checks `16 n^3 <= s_lo`
row by row.

## 3. Exact rows

```text
row    rate  A              log2 s_lo       log2(s_lo/n^3)  floor(s_lo/n^3)
RowC   1/4   261            121.999998833   91.999998833    4951756153316220974276265954
RowC   1/8   133            122.000000000   92.000000000    4951760157141520526864977065
RowC   1/16  67             121.999999999   91.999999999    4951760157009004832901345494
prize  1/4   558345748481   127.899999980   4.899999980     29
prize  1/8   283467841537   127.900000000   4.900000000     29
prize  1/16  141733920769   127.899999999   4.899999999     29
```

The prize rows are the limiting rows: they allow exactly `29 n^3` cubic units,
but not `30 n^3`. The proof reserves the cleaner `16 n^3` budget.

## 4. How to consume this

It suffices to prove any post-strip split whose total is bounded by `16 n^3`.
For example, the following much stronger-looking package is already small
enough:

```text
primitive aperiodic residue     <= n^3
dihedral staircase residue      <= n^2
extension/other paid remainder  <= n
```

because `n^3 + n^2 + n <= 16 n^3` for every row here. Thus even a quadratic
dihedral staircase cap is arithmetically enough for the clean-rate gate; the
expected linear staircase would be far inside the reserve.

The important point is that QA.21's crude support count is not such a cap:
`2*C((n-2)/2,(j-1)/2)` is a support universe, not a per-pair simultaneity
bound, and it exceeds `B*`. The missing theorem remains the per-pair
dihedral/primitive forcing statement, not this arithmetic composition.

## 5. Non-claims

- This does not prove the RK face-4 algebraic residual bound.
- This does not close `dihedral_staircase`; it states exactly how strong that
  result must be to compose.
- This does not apply to the pinned rate-`1/2` calibration row: at
  `n=512, A=507`, `s=0` and the tangent staircase exhausts `B*`.

## 6. Verifier

`experimental/scripts/verify_xr_clean_poly_forcing.py`

Current intended run:

```text
python3 experimental/scripts/verify_xr_clean_poly_forcing.py
```

The verifier checks the checked-in JSON certificate against a deterministic
rebuild, verifies the exact `B*` root for the prize rows, replays the audit
candidate pins, confirms strict quotient parity at odd `j`, proves
`16 n^3 <= s_lo`, and records the rate-half non-claim.
