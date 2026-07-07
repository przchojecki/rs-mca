# CAP25 v13 raw: precision reconciliation of the finite-Q moment-order floor `r0 = ceil(w log2|B| / Delta_Q)`

Status:
`AUDIT(4x2 exact floor table; two Delta_Q averaging conventions; maintainer table attributed)` /
`EXACT_ARITHMETIC(integer + Decimal at prec 60 and 140 give identical integers; every
ceiling certified > 1e-30 from the nearest integer; B* recomputed from the primes)`.

**Verifier:** `experimental/scripts/verify_q_moment_order_floor_reconciliation.py`
(zero-arg `~31s`, `--tamper-selftest` `~30s`, stdlib-only, deterministic; the pinned
certificate lives in the script -- no separate JSON).

**What this reconciles.** The maintainer's new `prop:q-moment-order-floor`
(`grande_finale.tex`, commit `b33609d`) prints the finite-Q moment-order floor
`r0 = ceil(w log2|B| / Delta_Q)` at the four deployed adjacent rows as
`94196 / 94991 / 641593 / 680397`. PR #384's `cap25_v13_gammar_order_floor.md` (Sec 3)
printed `94196 / 94992 / 641584 / 680397` for the same objects. This packet recomputes the
floor from scratch under **both** averaging conventions for the bit margin `Delta_Q`,
confirms the maintainer's four values exactly, and pins the exact source of the two #384
entries that differ. It is a precision (rounded-margin) refinement, not a correction of a hidden slip: the
#384 note (Sec 3, "computed from ... the 4-decimal `Delta` printed in `grande_finale.tex`'s
own adjacent-margin table") disclosed the rounded-margin input it used.

## Objects (all exact integers)

`n = 2^21`, `k = 2^20`; `w = a_+ - K`; `|B| = p` (the row prime, per `prop:q-moment-order-floor`'s
proof "the table uses the exact row prime in `log2|B|`"); budgets `B*` per `prop:q-exact-target`:

```text
row       a_+       K       w      p = |B|                    B*
KB-MCA    1116048   k+1     67471  2^31-2^24+1 = 2130706433   floor(p^6 / 2^128) = 274980728111395087
KB-list   1116047   k       67471  2130706433                274980728111395087
M31-MCA   1116024   k+1     67447  2^31-1     = 2147483647    floor(p^4 / 2^100) = 16777215
M31-list  1116023   k       67447  2147483647                16777215
```

Two conventions for the margin `Delta_Q` (differ only in how the average prefix fiber
`C(n,a_+)/p^w` is logged):

```text
real-avg :  Delta_Q = log2 B* - ( log2 C(n,a_+) - w log2 p )   = log2( B* / (C(n,a_+) p^-w) )
ceil-avg :  Delta_Q = log2 B* - log2 ceil( C(n,a_+) / p^w )
```

The floor numerator `w log2|B| = w log2 p` is identical in both.

## The exact table `[EXACT_ARITHMETIC]`

| row | `w` | `log2 B*` | `Delta_Q` (real-avg) | ceil-avg `r0` | real-avg `r0` | #384 shipped |
|---|---|---|---|---|---|---|
| KB-MCA | 67471 | 57.932108 | 22.196862 | 94196 | 94196 | 94196 |
| KB-list | 67471 | 57.932108 | 22.010942 | 94991 | 94991 | **94992** |
| M31-MCA | 67447 | 24.000000 | 3.258853 | **641594** | **641593** | **641584** |
| M31-list | 67447 | 24.000000 | 3.073000 | 680397 | 680397 | 680397 |

Recomputed at Decimal precision 60 and 140 with identical integer results; each ceiling is
certified by the argument's distance to the nearest integer exceeding `1e-30` (smallest such
distance is M31-MCA real-avg at `6.0e-2`). The exact real-average `Delta_Q` rounds to the
four printed 4-decimal margins `22.1969 / 22.0109 / 3.2589 / 3.0730` (checked in the verifier).

## Convention attribution `[AUDIT]`

The maintainer's `prop:q-moment-order-floor` table `94196 / 94991 / 641593 / 680397` equals
the **real-average** column exactly, all four rows. (Consistently, `prop:q-exact-target`'s
proof text logs `B*/(C(n,a_+)|B|^-w)` -- the un-ceiled, real average -- even though that
proposition's displayed ratio column tabulates `B*/ceil(C(n,a_+)/p^w)`; at 4-decimal print
the two agree, e.g. M31-MCA prints `3.2589` either way, so only the amplified `r0` reveals
the choice.)

## The two superseded #384 entries `[EXACT_ARITHMETIC]`

- **KB-list `94992 -> 94991`.** `94992 = ceil(w log2 p / 22.0109)` used the 4-decimal
  *printed* margin directly as `Delta_Q`; the exact real-average `Delta_Q = 22.010942...`
  (which itself rounds to that same `22.0109`) gives `94991`.
- **M31-MCA `641584 -> 641593`.** `641584 = ceil(w log2 p / 3.2589)` on the same printed
  margin; the exact real-average `Delta_Q = 3.258853...` gives `641593` (`641594` under
  ceil-average), a nine-step move because the printed `3.2589` exceeds the exact `Delta_Q` by
  `4.7e-5` and the small M31 margin amplifies that by `num/Delta_Q^2 ~= 1.97e5`.

Root cause (one fact, no arithmetic error): the mismatch is a rounded *input* -- the
4-decimal margin -- not the ceiling arithmetic, which the #384 note carried out exactly. For
M31-MCA the value `641584` was unanimous across the three concordant computations the #384
note cites (its own exact-arithmetic ceiling, Lane N's `laneN_compute.py`, and
`laneN_analysis.md`'s prose), all fed that same rounded margin, so their agreement to the
digit could not surface the input rounding; recomputing `Delta_Q` at full precision lands on
`641593`. The other two rows (KB-MCA `94196`, M31-list `680397`) are convention- and
rounding-robust: the coarse input coincidentally reproduces the exact floor.

## M31-MCA convention-sensitivity pin `[EXACT_ARITHMETIC]`

M31-MCA is the unique convention-sensitive row (`r_ceil - r_real = 1`; the other three have
`r_ceil = r_real`). The ceiling `L = ceil(C(n,a_+)/p^w) = 1752700` matches the value
displayed in `prop:q-exact-target`. The `log2(ceil)` vs `log2(real)` gap is
`Delta_real - Delta_ceil = 6.14e-7`, amplified by `num/Delta_Q^2 ~= 1.97e5` into a `0.1208`
shift of the r-argument `w log2 p / Delta_Q`, which straddles the integer `641593`:

```text
ceil-avg  arg frac = 0.0608501482325313804389337200342645513549   -> ceil 641594
real-avg  arg frac = 0.9400176511939683414672191182406133937095   -> ceil 641593
```

Both fractional parts are pinned as certified decimal strings and re-checked to 30 digits.

## Replay

```bash
python3 experimental/scripts/verify_q_moment_order_floor_reconciliation.py
python3 experimental/scripts/verify_q_moment_order_floor_reconciliation.py --tamper-selftest
```

## Relationship to concurrent / recent work

- **`b33609d` ("Promote grande finale Q attempt", same day).** Confirms
  `prop:q-moment-order-floor` and `prop:q-exact-target` to the digit and adds the explicit
  two-convention split plus the exact-vs-rounded-margin account behind the printed table.
- **PR #384 (`cap25_v13_gammar_order_floor.md`).** Supersedes exactly two Section-3 table
  entries (KB-list `94992 -> 94991`, M31-MCA `641584 -> 641593`). It changes nothing else in
  #384: `94196`, `680397`, the L4-rung `5886`, the measured `Gamma_r` data, Brick 1's floor
  law, Brick 2's monotone certificate, and both verifier and JSON files all stand; this
  packet supersedes only the two numeric table cells, in this note, and does not touch #384's
  files.
- No other open PR is in contact.

## Refs

- `experimental/grande_finale.tex` (commit `b33609d`) --
  `\label{prop:q-moment-order-floor}` (L1875), `\label{prop:q-exact-target}` (L1843),
  `\label{thm:moment-q}` (L721), `\label{prop:moment-sandwich}` (L705),
  `\label{rem:finite-moment-order}` (L752). The floor formula, budgets `B*`, and the
  four printed margins reconciled here.
- `experimental/notes/thresholds/cap25_v13_gammar_order_floor.md` (PR #384) and its verifier
  `experimental/scripts/verify_gammar_order_floor.py` -- the Section-3 floor table whose two
  entries (`94992`, `641584`) this packet supersedes; root cause pinned in its lines 216-217
  and the verifier's `DELTA_*` constants (the 4-decimal printed margins).
- `experimental/notes/thresholds/cap25_v13_saturated_bc_budget_fit.md` (PR #383) -- its
  margin identity `margin = log2 B* - log2 B_B(a_+)`, with `B_B(a_+) = ceil(C(n,a_+) p^-w)`,
  is the same `Delta_Q` up to the ceil-vs-real average distinction pinned above.
- `experimental/scripts/verify_q_moment_order_floor_reconciliation.py` -- this note's
  certificate and verifier.
