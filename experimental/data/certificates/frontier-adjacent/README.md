# Frontier-Adjacent Ledger: KoalaBear MCA Row — corrected pair {a0', a0'+1} = {1116047, 1116048}

- **Status:** EXPERIMENTAL / AUDIT.
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Scope:** the first `frontier-adjacent/*.json` packet (agents.md
  highest-value item 2), instantiating the declared threshold task — *"build
  the exact upper ledger for the adjacent safe-side step"* (agents-log
  2026-07-04, canonical spec: agents.md, "The complete upper ledger to build
  at `a0 + 1`") — as an honest status-labelled row packet.  Every number is
  recomputed by exact integer arithmetic in the verifier below; nothing is
  imported as a trusted print.
- **Filename note:** the JSON keeps its original name
  (`..._a1116043_a1116044.json`, the pair the packet was first built at);
  its coverage is now the interval `{1116043, ..., 1116048}`.

## MATERIAL CORRECTION (2026-07-05)

The packet's original verdict `UNDECIDED_WINDOW_OPEN` at `a = 1116044` was
**too conservative** (found in post-submission review by the external team).
Two statements already merged upstream compose directly:

1. `lem:v13f1-identity-prefix-floor` at `K = k+1`, `w = m-k-1`: a closed-ball
   list of `L(m) = ceil(C(n,m)/p^w)` distinct `RS[F,D,k+1]`-codewords around
   one received word, each agreeing on `>= m > k` points;
2. `prop:quantitative-deep-list-floor` (v12 main tex; sharp-denominator form
   = `thm:quant-deep-point`, strict352 section, stated for `LD_sw` verbatim):
   some single received line carries
   `M(m) = ceil( L(q-n) / (q-n + k(L-1)) )` support-wise MCA-bad finite
   slopes — **with no density trigger** (any `L >= 1` qualifies).

The exact five-point sweep (all recomputed in the verifier, both the sharp
`k(L-1)` and the printed `kL` denominator ceilings agree at every point):

| m | w | log2 L | log2 M | margin over B* | verdict |
|---|---|---|---|---|---|
| 1116044 | 67467 | 160.4336 | 160.4021 | **+102.4700 bits** | MCA-UNSAFE (was the open step) |
| 1116045 | 67468 | 129.2591 | 129.2591 | **+71.3269** | MCA-UNSAFE |
| 1116046 | 67469 | 98.0845 | 98.0845 | **+40.1523** | MCA-UNSAFE |
| 1116047 | 67470 | 66.9099 | 66.9099 (M = L, lossless) | **+8.9777** | MCA-UNSAFE — **the corrected edge a0'** |
| 1116048 | 67471 | 35.7352 | 35.7352 (M = L, lossless) | **-22.1969** | not flipped — **the corrected open step** |

Exact anchors: `L(1116044) =
1973967916468083369044358670918132115633867608112`, `M(1116044) =
1931247427137429416005585529088676636591240959005`, `M(1116047) = L(1116047)
= 138634741058327852652`, `M(1116048) = 57198030366`, `B* =
274980728111395087`.  The certified MCA-unsafe interval widens from
`[981109/2097152, 1/2)` to `[981105/2097152, 1/2) = [0.4678273..., 1/2)`.
The finite adjacent-pair prediction of `prob:v13f1-frontier` at this row
(`a* = 1116044`) is refuted; the conjectured pin moves to `a* >= 1116048`.
No proved-safe statement is contradicted, and the asymptotic ceiling
`1 - rho - g* = 0.4678266` (`def:v13f1-gstar`) survives.

Why the original packet under-claimed: it measured the certified list floor
only against the strong `(q+k)/k` deep-point **trigger** (the `thm:A`
contrapositive route inherited from `prop:v13f1-identity-frontier`), and
parked the `~2^160.40` quantitative number inside `B_ext` as hypothetical
pending condition (i) of `prop:v13-extension`.  Both cautions conflated
compiler hypotheses with the direct theorem: v12's own
`rem:quantitative-floor-vs-contrapositive` prescribes the quantitative form
for exactly this under-trigger case, and condition (i) governs only
extension-only *cell* attribution (the row verdict takes poles in
`Omega = F \ D` and never routes through the extension compiler).

The packet's former "5.4985-bit conversion-gap" framing is **RETIRED**: that
number is the gap to the strong `q/k` trigger and nothing else; **zero bits
of new mathematics** were needed to flip `1116044`.  The analogous residual
at the new open step `1116048` is different in kind: the conversion is
already lossless there (`M = L`), so the `-22.1969`-bit shortfall is the
prefix list floor itself — the next sharpening target is the floor, not the
conversion constant.

## Row-packet schema header (agents.md conventions)

```text
row:                   RS[F_p^6, D, 2^20]; p = 2^31 - 2^24 + 1 (KoalaBear);
                       D = multiplicative subgroup of F_p^x of order n = 2^21;
                       k = 2^20; rho = 1/2; MCA floors built at K = k+1 and
                       converted by (a) the thm:A deep-point trigger route and
                       (b) the quantitative deep-list floor
                       prop:quantitative-deep-list-floor (no trigger)
denominators:          q_gen = p = 2130706433;  q_line = q_chal = q_list = p^6
                       = 93571093019388561295270373781649880353786165192103559169
                       (finite_affine slope sampler; projective shift immaterial)
target:                epsilon* = 2^-128,
                       B* = floor(q_line/2^128) = 274980728111395087  (~2^57.9321)
agreement interval:    I = {1116043, ..., 1116048}
unsafe certificates:   trigger route: L(1116043) > B* (+25.6761 bits, exact);
                       quantitative route: M(m) > B* for m = 1116044..1116047
                       (+102.4700 / +71.3269 / +40.1523 / +8.9777 bits, exact),
                       failing at 1116048 (-22.1969); companion list objects:
                       c=1 at +71.5129 (holds through 1116046), c=2 at +1.8790
safe certificates:     NONE — no finite U(a) exists; the tangent-upper,
                       aperiodic, sparse/CA and extension-chart cells are OPEN
paid cells:            quotient SAFE_SUM (theorem-backed, declared family
                       {2,4,8,16,32}); tangent LOWER floor n-a+1 (theorem);
                       quantitative deep-list floors (exact certificates);
                       exact unsafe certificates as above
residual cells:        named: aperiodic underdetermined band (CONJECTURAL_WITH_
                       FALSIFIER, future input PR #282), extension chart
                       classification (CONDITIONAL_ON_NAMED_INPUT, future input
                       PR #284), sparse/plain-CA (OPEN), tangent-upper (OPEN);
                       the former conversion-gap residual is RETIRED (see the
                       material-correction section)
deduplication rule:    WP-2.3 first-match tree T0-T7 (first-match-wins IS the
                       convention); per-slope syndrome tangent filter u+zv=0
                       primary; no cross-cell total is formed in this packet,
                       so only the SAFE_SUM's internal union bound
                       (prop:v13-quotient-safe-sum + lem:one-support-one-line)
                       is exercised; lower certificates MAX, never sum
endpoint convention:   closed integer ball r = n - a; real supremum
                       (n - a* + 1)/n not attained (cor:v13-endpoint)
replay:                python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --check
                       (deterministic; no seed; JSON byte-compared)
status:                EXPERIMENTAL / AUDIT
```

## The per-cell table

Cells are status-valued per `paid_ledger_functions.md`; the five residual
labels are those of agents.md.  "floor" = unsafe lower mass; "upper" = safe
upper cell.  Full cell tables are printed at `1116043`, `1116044` and
`1116048`; the interior flipped rows `1116045`-`1116047` carry compact
verdict blocks (per `thm:v13-corridor` only the largest certified-unsafe
agreement and the first candidate safe step need full tables).

| cell | a0 = 1116043 | 1116044 (flipped by the correction) | a0'+1 = 1116048 (new open step) | label |
|---|---|---|---|---|
| quantitative deep-list MCA floor | (trigger route already certifies) | PASSES, +102.4700 bits | FAILS, -22.1969 bits | PAID_BY_EXACT_CERTIFICATE at 1116044-1116047 (COUNTEREXAMPLE_NEW_FLOOR vs the original packet); failure recorded at 1116048 |
| c=1 identity-prefix MCA floor (trigger route) | PASSES, +25.6761 bits | FAILS, -5.4985 bits (trigger only) | FAILS | PAID_BY_EXACT_CERTIFICATE at a0; the 1116044 failure is against the strong trigger, superseded by the quantitative route |
| c=1 LIST route (companion list object) | (also passes) | PASSES, +71.5129 bits; holds through a=1116046 (+9.1637), fails 1116047 (-22.0109) | FAILS | PAID_BY_EXACT_CERTIFICATE (list object only) |
| c=2 LIST edge m=558022 | — | PASSES, +1.8790 bits, adjacent-tight (m=558023 fails) | — | PAID_BY_EXACT_CERTIFICATE (list object only) |
| c=2 / c=4 MCA controls | c=2 edge at a=1116038 (+18.3914) | c=2 fails (-75.1323), c=4 fails; no c>=8 grid contains a | (dominated by the quantitative route) | PAID_BY_EXACT_CERTIFICATE (controls) |
| `B_tan` lower floor `n-a+1` | 981110 | 981109 | 981105 (dominated by the quantitative floor 57198030366) | PAID_BY_THEOREM (LOWER floor only) |
| `B_tan` upper/exact cell | UNAVAILABLE (r=981109 > R_tan=349525) | UNAVAILABLE | UNAVAILABLE (r=981104 > R_tan) | OPEN |
| `B_quot_support` (SAFE_SUM, C={2,4,8,16,32}) | exact, ~2^1045455 (fingerprinted) | exact | exact | PAID_BY_THEOREM (upper; astronomically above B*, documented honestly) |
| `B_quot_image` | NO_CERTIFICATE | NO_CERTIFICATE | NO_CERTIFICATE | OPEN |
| zone gate | all declared N' in ZONE_A_NORM_EXACT; gate holds to N'=60, fails at 62; zone-(b) vacuous | same | same (t=67472, n/t~31.08) | printed arithmetic |
| `B_ap_regular` | NONEXISTENT (deficiency 913643) | NONEXISTENT (deficiency 913641) | NONEXISTENT (t=67472 < j+1=981105; deficiency 913633) | CONJECTURAL_WITH_FALSIFIER |
| `B_ap_pivot` | OPEN (M5/WP-2.6 exists only at deficiency 1, toy row) | OPEN | OPEN | CONJECTURAL_WITH_FALSIFIER (named future input: PR #282 XR) |
| `B_ext` | proper extension row; S6 chart classification undischarged; ExtPole printed as hypothetical CELL value only | same | same | CONDITIONAL_ON_NAMED_INPUT (named future input: PR #284 F1 descent); condition (i) gates only cell attribution, NOT row verdicts |
| sparse / plain-CA | OPEN | OPEN | OPEN — no theorem at delta ~ 0.4678 (exact landmark table in the JSON) | OPEN |
| mu4 monomial family | +4 empirical | +4 empirical | +4 empirical (dominated; never summed) | EMPIRICAL / not-a-theorem-at-this-row |
| deduped total upper bound | NOT FINITE (open cells) | NOT FINITE | NOT FINITE | — |
| verdict | **UNSAFE_BY_PROVED_LOWER_BOUND** | **UNSAFE_BY_PROVED_LOWER_BOUND** (was UNDECIDED_WINDOW_OPEN) | **UNDECIDED_WINDOW_OPEN** | thm:v13-windows |

## Verdicts

- `a = 1116043` is **certified MCA-unsafe** by the trigger route (margin
  +25.6761 bits; reproduces upstream's printed `+25.7`).
- `a = 1116044, 1116045, 1116046, 1116047` are **certified MCA-unsafe** by
  the quantitative deep-list route (margins +102.4700 / +71.3269 / +40.1523 /
  +8.9777 bits; exact integer comparisons).  The corrected MCA-unsafe edge is
  **a0' = 1116047**.
- `a0'+1 = 1116048` is the **undecided window** per `thm:v13-windows`: known
  proved lower mass is the quantitative floor `57198030366 ~ 2^35.7352`
  (which dominates the tangent floor `981105`; lower certificates max, never
  sum) against `B* ~ 2^57.9321` — a deficit of `274980670913364722` — and
  **no safety theorem is in range** (the proved Hab25-quadratic import
  reaches only `delta ~ 0.2045`; the `~0.2881` edge is conditional, gap G4;
  Johnson is 366862 agreement steps away).
- Corridor (`thm:v13-corridor`): `1 + max A_unsafe = 1116048 <= a*`.

## Replay

```sh
python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --check
```

Runtime: ~120 s measured (dominated by the exact five-divisor `U_sum` plus
its modular cross-check; the c=2 branch alone is most of it, ~1M-bit
incremental big-integer steps; the ~2M-bit anchor binomials take ~0.2-0.3 s
each via Legendre factorization + product tree).  `--check` reruns the full
recomputation and byte-compares the regenerated JSON.  Integers above ~2^200
(the `U_sum` values) are stored as exact fingerprints (bit length, sha256 of
big-endian bytes, residues mod 2^64 / M61 / M31, log2); the verifier
recomputes the exact integers, re-derives every fingerprint, and additionally
recomputes every `U_sum` cell modulo `2^61 - 1` through an independent
factorial-table path at all three fully-tabled agreements.  Floats are
informational (4 decimals); all verdicts are exact integer comparisons.

## Non-claims

- **No adjacent pin is claimed.** `a* >= 1116048` is proved; `a* = 1116048`
  is conjectural (the original `prob:v13f1-frontier` prediction
  `a* = 1116044` is refuted by this packet's correction); the packet
  supplies no `U(1116048) <= B*` certificate and none exists: the upper
  ledger has OPEN cells (tangent-upper, aperiodic, sparse/CA,
  extension-chart), so no finite deduped total is printed, and the window at
  `1116048` stays open per `thm:v13-windows`.
- The LIST-route certificates at `1116044` concern the companion list
  object; the MCA verdict there is decided by the separate quantitative
  certificate `quant_mca_m1116044`.
- The ExtPole value remains hypothetical as an extension-only **cell** value
  (condition (i) of `prop:v13-extension` is not certified at this row); the
  row verdicts never route through the extension compiler.
- `U_sum` covers only the declared dyadic quotient cells `{2,4,8,16,32}`;
  it is not global quotient exhaustion.
- The mu4 `+4` is empirical toy-row evidence and is never added to a
  theorem-backed total (lower certificates max; it is dominated here).
- PRs #282 and #284 are cited as named future inputs only, not audited or
  consumed here.
- Polynomial-loss quotient equidistribution is kept out of every finite
  claim (a factor `n^C` costs `21C` bits at `n = 2^21`; the tightest printed
  margin is the +8.9777-bit edge certificate), per the task instruction.

Companion audit note (including the dated material-correction section):
`experimental/notes/audits/audit_koalabear_frontier_adjacent_ledger.md`.
