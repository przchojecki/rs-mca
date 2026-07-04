# QA.21 — the dihedral budget column at the clean-rate candidates

- **Status:** AUDIT FOLLOW-UP / **NEGATIVE RESULT — GAP REPORTED.** Every
  number re-derived deterministically by
  `experimental/scripts/verify_qa21_dihedral_budget.py` (stdlib python3,
  exact big integers for Row C, rigorous integer inequalities + Robbins
  log2 brackets for prize scale; current run **76 PASS, 0 FAIL, exit 0**).
- **DAG:** mandatory follow-up to `xr_target_budget_audit` flag F5
  (`xr_budget_audit.md`: dihedral class count "[CITATION NEEDED] / open");
  touches `dihedral_quotient_stratum`.
- **Parents:** `xr_budget_audit.md` (candidates, conventions, per-pair
  frame), `e30_dim3_flat_census.md` finding 1 (odd-j dihedral clause),
  E26 note (`git show fork/codex/e26-dihedral-window-arithmetic:
  experimental/notes/roadmaps/e26_dihedral_window_arithmetic.md`, window
  count `C(n/m, ell)` at scale `d = m*ell`), E25 note
  (`git show fork/codex/e25-dihedral-toy-audit:...e25_dihedral_toy_audit.md`,
  toy dihedral charging), v8 one-slope-per-locator cap
  (`proof_sketch/prize_proof_sketch_spine.md` sect. 8,
  `proof_sketch/s3b_iii_1_divisor_pencil_incidence.md` sect. 1).

## 1. Question

The audit's allowance `s = B* - B_quot - B_tan` subtracts only the quotient
and tangent ledgers. This packet computes the dihedral column and re-emits

```text
s' = B* - B_quot_ub - B_tan_max - B_dih
```

at all six clean-rate candidates (Row C `n = 1024`, A = 261/133/67; prize-max
`n = 2^41`, A = 558345748481/283467841537/141733920769). Safe direction
throughout: **B_dih is an UPPER bound**, so s' is a LOWER bound on the true
allowance.

## 2. Counting model (explicit)

- **Frame:** the audit's per-pair frame. `B*` bounds the bad slopes of a
  single line (pair); each ledger column must bound the slopes A SINGLE
  FIXED PAIR can align that are charged to that stratum.
- **Supports:** evaluation domain `mu_n`, n even, inversion has exactly two
  fixed points `{+1, -1}`. All six candidates have `j = n - A` **odd**
  (verified), so an inversion-closed size-j support is exactly one of
  `{+1, -1}` plus `(j-1)/2` moving inverse pairs (E30 finding 1; word shape
  `lambda_a = -+ a^{-j+2m} lambda_{a^-1}`). Crude support count:

```text
N_dih(n, j) = 2 * C((n-2)/2, (j-1)/2).
```

- **Per-support slope cap:** the v8 ledger — at most ONE slope per aligned
  locator per pair. Hence the crude column `B_dih <= N_dih * 1`. (N_dih
  over-counts: it includes inversion-closed supports whose aligned word, if
  any, is not dihedral-shaped — consistent with the upper-bound direction.)
- **E26-style window column:** window scales `d = m * ell`, twin-fiber size
  `m in {2, 4, 8, ...}`, count `C(n/m, ell)`. Every such `d` is EVEN, so at
  odd j the strict window count is **0** — the same parity that makes
  B_quot strictly 0. **BUT this column is UNSAFE as a bound:** E30 finding 1
  exhibits real dihedral words at odd j, living exactly on the
  fixed-point-bearing supports that the `n/m`-fiber count omits (`+-1` are
  singleton fibers, not twin fibers). Unlike B_quot's strict zero (a
  realizability theorem), the E26 zero is a model blind spot, contradicted
  at word level. Both columns are reported; only the crude one is valid.

## 3. LOUD FLAG: the crude count exceeds B* on its own — at ALL SIX candidates

`N_dih > B*` outright (exact for Row C; for prize, rigorous via
`C(P, K) >= (P/m)^m >= 2^m`, `m = min(K, P-K)`, `P >= 2m`, `m >= 128 =
bitlen(B*)` — margins of ~10^11 bits):

```text
row    rate  A              j              log2 N_dih        excess over log2 B*
RowC   1/4   261            763            414.4651          +292.47 bits
RowC   1/8   133            891            280.4193          +158.42 bits
RowC   1/16  67             957            173.6759          +51.68  bits
prize  1/4   558345748481   1640677507071  898752770296.23   ~ +9.0e11 bits
prize  1/8   283467841537   1915555414015  609603247008.73   ~ +6.1e11 bits
prize  1/16  141733920769   2057289334783  379193192042.78   ~ +3.8e11 bits
```

So the support-count-times-v8-cap model is VACUOUS here: it cannot certify
any positive allowance.

## 4. The s' table

`B_quot_ub` and `B_tan_max = n - A + 1` exactly as the audit (B_quot strict
= 0 at every candidate, j odd — verified). Two B_dih columns:

```text
row    rate  s'_crude (B_dih = N_dih, VALID bound)   s'_E26strict (B_dih = 0, INVALID)
RowC   1/4   < 0  (exact; = -2^414.47)               2^121.99999883  (= audit s_lo)
RowC   1/8   < 0  (exact; = -2^280.42)               2^122.0-eps     (= audit s_lo)
RowC   1/16  < 0  (exact; = -2^173.68)               2^122.0-eps     (= audit s_lo)
prize  1/4   < 0  (rigorous; |s'| ~ 2^(9.0e11))      2^127.89999998  (= audit s_lo)
prize  1/8   < 0  (rigorous; |s'| ~ 2^(6.1e11))      2^127.9-eps     (= audit s_lo)
prize  1/16  < 0  (rigorous; |s'| ~ 2^(3.8e11))      2^127.9-eps     (= audit s_lo)
```

(Exact s'_E26strict integers = the audit table's s bottom ends, matched
digit-for-digit by the verifier.)

## 5. Verdict per candidate and the gap

**Under the only VALID in-repo bound, s' < 0 at all six candidates: the
2^100 loud-flag threshold FAILS everywhere.** The E26-strict column would
keep s' = audit-s_lo >= 2^121.99 (>= 2^100), but it is not a bound (sect. 2).

**GAP QA21-G1 (precise statement).** What is missing is an upper bound,
strictly below `B* - B_quot_ub - B_tan_max`, on

```text
#{ inversion-closed S, |S| = j, such that a FIXED pair (u,v)
   has a v8-aligned slope with disagreement support S }.
```

The v8 cap bounds this only by N_dih (one slope per support), and no in-repo
lemma bounds per-pair dihedral SIMULTANEITY below that. To restore
`s' >= 2^100`, the per-pair simultaneously-aligned fraction of dihedral
supports must be at most `(audit s_lo - 2^100) / N_dih`, i.e. a suppression
by (verifier-pinned):

```text
RowC 1/4: 2^-292.4652   RowC 1/8: 2^-158.4193   RowC 1/16: 2^-51.6759
prize:    2^-8.99e11 / 2^-6.10e11 / 2^-3.79e11  (rates 1/4 / 1/8 / 1/16)
```

E25's toys are consistent with strong suppression (92 audited supports,
only 100/64 dihedral-charged alignments across ALL 36 basis lines at
n = 16) but prove nothing per-pair at scale. **We do not invent a bound:**
the dihedral column is OPEN, and the audit's `s ~ 2^122 / 2^127.9`
allowance survives only if QA21-G1 is closed (e.g. a dihedral analogue of
the census class-count argument, or E25's "paid/absorbed" verdict promoted
to a per-pair ledger with its own cap).

## 6. Non-claims

- NOT claiming the budget is actually blown: N_dih counts supports, not
  proven-aligned slopes; s' < 0 means the BOUND is missing, not that
  >B* dihedral slopes exist for some pair.
- No claim that the dihedral stratum is paid (E25 is toy-level; E26 is
  arithmetic-only and conditional on E25).
- The E26 zero column is reported for parity bookkeeping only; it is
  explicitly disclaimed as a bound.
- Idealized-q conventions, rate-1/2 exclusions, and the staircase-activity
  ambiguity are inherited from the audit unchanged.

## 7. Verifier

`experimental/scripts/verify_qa21_dihedral_budget.py` — standalone,
stdlib-only, deterministic, < 1 s. Recomputes per row: candidate A (audit
pin), j oddness, B_quot strict = 0 and B_quot_ub (audit machinery),
B_tan_max, the E26-strict zero, N_dih (exact big int for Row C; for prize
the rigorous `2^m`-route inequalities plus a Robbins log2 bracket),
`N_dih > B*` (LOUD), `s'_crude < 0`, s'_E26strict == audit s-bottom pins,
the 2^100 flag outcomes, and the required suppression exponents. Current
run: **76 PASS, 0 FAIL, exit 0.**
