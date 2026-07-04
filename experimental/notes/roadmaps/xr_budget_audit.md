# XR step zero — the integer aperiodic allowance s at the clean-rate decision points

- **Status:** AUDIT — every number re-derived deterministically by
  `experimental/scripts/verify_xr_budget_audit.py` (stdlib python3, exact big
  integers, no randomness; current run **49 PASS, 0 FAIL, exit 0**).
- **DAG:** `xr_target_budget_audit` (feeds `xr_clean_residual_any_gate`).
- **Parents:** `proof_sketch/s2_paid_ledger.md` (B_tan/B_quot ledger, sect. 1/3/5),
  `qa3_e14_fm_margin_tables.md` (B*, A*, A_zero, GM conventions),
  `execution_queue.md` QA.7-QA.9 (census conventions), the #213 corridor packet
  (`git show fork/codex/q3r3-clean-rate-corridor:experimental/data/certificates/
  clean-rate-corridor-pipeline/clean_rate_corridor_pipeline_skeleton.json`,
  commit d642a419).

## 1. Question and conventions

At the safe-side decision candidate A of each clean-rate row, the exact integer

```text
s = B* - B_quot(A) - B_tan(A)
```

is the aperiodic count the gate still allows. s = 0 forces the emptiness form
(face 4 = rigidity); s >= 1 dissolves the singleton obstruction into
bounded-multiplicity forcing at multiplicity s+1.

- **B\*** = `floor(q_line / 2^128)` exact. Pinned: `17^32 >> 128 = 6`. Row C
  (idealized `q = 2^250`, prime unpinned — qa3 flag C1(b)): `2^122` exact.
  Prize (idealized `q = 2^255.9`): `floor(2^127.9)` = exact integer 10th root
  of `2^1279` = `317494674775468773183020924238786383963`.
- **B_quot** (census_bounded_scales / QA.7 conventions): coset-support classes
  at quotient scales `N' | n` active when `N' <= n/t` (s2 sect. 5), with
  forced ratio `l'/N' = j/n`, `j = n - A`. A union of `l'` cosets of size
  `M = n/N'` has exactly `j = l' M` disagreements, so `l'` must be integral
  (**strict** count; the **floor-rounded** variant is carried only as a
  conservative upper bound). Counts are char-0 `C(N', l')`: an UPPER bound on
  the value-set class count — collisions only make s LARGER, so the s
  lower bound below is the safe direction.
- **B_tan**: `B_tan(A) <= n - A + 1` (s2 sect. 1, PROVED-cited #147). Exact
  (`= n - A + 1`) on the fully-pinned staircase envelope `log2 q in
  [128, 166.4]` (s8_s9) — covers the pinned row (`130.80` bits) only. For the
  `2^250 / 2^255.9` rows staircase-activity is ambiguous; both variants
  (0 and `n - A + 1`) are carried per the task spec.
- **Reported range:** `s in [B* - B_quot_ub - (n-A+1), B* - B_quot_strict]`.

**Deciding-scale identity [PROVED-elementary, verified].** At the right edge
of the scale-N' plateau (`t = n/N'`) the forced l' is integral and equals
`N'(1-rho) - 1`, so the edge count is `C(N', rho N' + 1)` — the same argument
as prop:qfloor's `Acl(N', rho N'+1)` and the #213 `A_2`/planted families. The
deciding dyadic scales (smallest with edge count > B*, upward-closed, chain
certified to N' = n) are **256 / 256 / 512** at rates 1/4 / 1/8 / 1/16 — for
BOTH B* values, matching #213's `dyadic_A2_crossing` and
`planted_dyadic_crossing` exactly.

## 2. Locating the candidates

The strict census is spiky (zero at non-realizable j), so "total first drops
<= B*" is read as: first A beyond the LAST census-realizable unsafe point
(`A_last = k + n/N'_dec`, count `C(N'_dec, rho N'_dec + 1) > B*`); under the
floor-rounded (plateau-constant) variant this is literally the first drop.
Both conventions give `A = k + n/N'_dec + 1`. The pinned row is
tangent-decided instead: `n - A + 1 <= 6` first at A = 507 (the proved 506/507
threshold, qa3 F4).

## 3. The table (verifier output; exact integers)

```text
row    rate  A              B*                                        B_quot [strict, ub]                    B_tan-range          s-range at A
pinned 1/2   507            6                                         0 (exact)                              6 (exact, staircase) 0 (exact);  s(508) = 1 (exact)
RowC   1/4   261            2^122 = 5316911983139663491615228241121378304  [0, 4299074680733908773355584498352]   [0, 764]        [5316907684064982757706454885536879188, 2^122]
RowC   1/8   133            2^122                                     [0, 614965786765268072882]             [0, 892]             [5316911983139662876649441475853304530, 2^122]
RowC   1/16  67             2^122                                     [0, 142288257910922317410365606]       [0, 958]             [5316911982997375233704305923711011740, 2^122]
prize  1/4   558345748481   317494674775468773183020924238786383963   [0, 4299074680733908773355584498352]   [0, 1640677507072]   [317494670476394092449112149242524378539, B*]
prize  1/8   283467841537   same B*                                   [0, 614965786765268072882]             [0, 1915555414016]   [317494674775468772568055135557962897065, B*]
prize  1/16  141733920769   same B*                                   [0, 142288257910922317410365606]       [0, 2057289334784]   [317494674775326484925109999864086683573, B*]
```

At A+1 every s range shifts by +1 at the bottom end (same order); pinned
s(508) = 1 exactly.

## 4. Verdicts

- **Pinned (calibration): s = 0 EXACT at A = 507** — face 4 = rigidity/
  emptiness. The budget is exhausted by the tangent staircase alone
  (B_tan = 6 = B*), reproducing the proved tangent-pinned threshold. One step
  in, s(508) = 1.
- **All six clean-rate rows (Row C and prize-max, rates 1/4, 1/8, 1/16):
  s >= 1**, and in fact `log2 s ~ 122.00` (Row C) / `127.90` (prize) — the
  allowance is essentially the whole budget. Face 4 = bounded-multiplicity
  forcing at multiplicity s+1; **the emptiness form is NOT budget-forced at
  any clean-rate decision point.** The rigidity world is real only where the
  tangent staircase reaches B* (the small-q envelope), never at 2^250+ rows.

## 5. Findings and flags

- **F1 (robustness).** No clean-rate verdict depends on the B_tan ambiguity,
  the l'-rounding convention, or the collision direction: s_lo >= 1 holds
  under worst-case B_tan = n-A+1 AND the floor-rounded all-scale B_quot sum
  simultaneously, and collisions only raise s. No row is verdict-flagged.
- **F2 (pinned dedup is load-bearing).** Adding the Paper-B `A_2(2,2) = 1`
  trivial whole-line class to B_tan without dedup gives s = -1 at the
  PROVED-safe A = 507. The S1 dedup (trivial class inside the tangent count)
  is what makes the calibration row consistent — a knife-edge warning for any
  future exact-budget bookkeeping.
- **F3 (dyadic undershoot).** The census candidates sit LEFT of qa3 Table 2's
  continuous-beta `A_quot` by 2 / 0 / 0 steps (Row C) and 4305041496 /
  532831157 / 1452753378 steps (prize) — the s7-F2 2-power artifact. Verdicts
  are identical at both locations; all candidates satisfy `A >= A_zero = A*+2`
  (E14 reconciliation: ZM(A) < 0 at every candidate, exact for Row C,
  entropy-upper-bound for prize), so the aperiodic FM integer-zero statement
  already holds there — but the INTEGER allowance is what face 4 consumes.
- **F4 (realizable class at RowC 1/16, A+1).** At A = 68 (`j = 956 = 4*239`)
  a realizable scale-256 family exists (`C(256,17)` classes, ~2^83.5) — still
  36 bits under budget; recorded because it is the one candidate-adjacent
  point with nonzero strict census count.
- **F5 (what s excludes).** The node's formula subtracts only B_quot and
  B_tan. B_ext is poly-shaped (s2 sect. 1) and cannot dent a 2^122-scale s;
  any NON-census paid family (e.g. the candidate dihedral stratum,
  `dihedral_quotient_stratum`) would reduce the true allowance — its class
  count at these rows is [CITATION NEEDED] / open, flagged, not estimated.

## 6. Non-claims

- No claim on R2 / SPI / XR, imgfib, or zone-(b): s is the gate's arithmetic
  allowance, not a proof that s aperiodic slopes exist or are excludable.
- Char-0 census counts vs value sets: only the safe (lower-bound) direction
  is used; exact value-set counts are QA.6/QA.8 scope.
- Idealized q rows exactly as in qa3 (C1(b): Row C prime unpinned; prize
  `2^255.9` a convention); rate 1/2 is excluded from the clean-rate verdicts
  (pinned row is calibration only; prize rate 1/2 has the 2-power gap, qa3 F6).
- The staircase-active question at `log2 q in {250, 255.9}` remains open; it
  is bracketed, never resolved, here.

## 7. Verifier

`experimental/scripts/verify_xr_budget_audit.py` — standalone, stdlib-only,
deterministic. Re-derives: exact B* per row (incl. the 10th-root prize floor),
deciding scales + upward-closure of the unsafe chain, last realizable unsafe
points, strict and floor-rounded B_quot at A and A+1, the s ranges, the
pinned-row calibration (s = 0, s(508) = 1), ZM(A) < 0 and `A >= A*+2` E14
reconciliations, and the #213 dyadic-crossing match. Prints the table and
PASS per claim. Current run: **49 PASS, 0 FAIL, exit 0.**
