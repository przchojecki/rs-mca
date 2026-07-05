# Frontier-Adjacent Upper Ledger: KoalaBear MCA Row at {a0, a0+1} = {1116043, 1116044}

- **Status:** EXPERIMENTAL / AUDIT.
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Scope:** the first `frontier-adjacent/*.json` packet (agents.md
  highest-value item 2), instantiating the declared threshold task — *"build
  the exact upper ledger for the adjacent safe-side step"* at agreement
  `1116044` (agents-log 2026-07-04, canonical spec: agents.md, "The complete
  upper ledger to build at `a0 + 1`") — as an honest status-labelled row
  packet.  Every number is recomputed by exact integer arithmetic in the
  verifier below; nothing is imported as a trusted print.

## Row-packet schema header (agents.md conventions)

```text
row:                   RS[F_p^6, D, 2^20]; p = 2^31 - 2^24 + 1 (KoalaBear);
                       D = multiplicative subgroup of F_p^x of order n = 2^21;
                       k = 2^20; rho = 1/2; MCA floors built at K = k+1 and
                       converted by the thm:A deep-point conversion
denominators:          q_gen = p = 2130706433;  q_line = q_chal = q_list = p^6
                       = 93571093019388561295270373781649880353786165192103559169
                       (finite_affine slope sampler; projective shift immaterial)
target:                epsilon* = 2^-128,
                       B* = floor(q_line/2^128) = 274980728111395087  (~2^57.9321)
agreement interval:    I = {1116043, 1116044}
unsafe certificates:   L(1116043) > B*  (c=1 identity-prefix MCA floor,
                       +25.6761 bits, exact);  at 1116044 the MCA route FAILS
                       (-5.4985 bits) and only the companion list object is
                       certified unsafe (c=1 at +71.5129, c=2 at +1.8790)
safe certificates:     NONE — no finite U(a) exists; the tangent-upper,
                       aperiodic, sparse/CA and extension-chart cells are OPEN
paid cells:            quotient SAFE_SUM (theorem-backed, declared family
                       {2,4,8,16,32}); tangent LOWER floor n-a+1 (theorem);
                       exact unsafe certificates as above
residual cells:        named: aperiodic underdetermined band (CONJECTURAL_WITH_
                       FALSIFIER, future input PR #282), extension chart
                       classification (CONDITIONAL_ON_NAMED_INPUT, future input
                       PR #284), sparse/plain-CA (OPEN), tangent-upper (OPEN),
                       conversion gap (CONJECTURAL_WITH_FALSIFIER)
deduplication rule:    WP-2.3 first-match tree T0-T7 (first-match-wins IS the
                       convention); per-slope syndrome tangent filter u+zv=0
                       primary; no cross-cell total is formed in this packet,
                       so only the SAFE_SUM's internal union bound
                       (prop:v13-quotient-safe-sum + lem:one-support-one-line)
                       is exercised
endpoint convention:   closed integer ball r = n - a; real supremum
                       (n - a* + 1)/n not attained (cor:v13-endpoint)
replay:                python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --check
                       (deterministic; no seed; JSON byte-compared)
status:                EXPERIMENTAL / AUDIT
```

## The per-cell table at both agreements

Cells are status-valued per `paid_ledger_functions.md`; the five residual
labels are those of agents.md.  "floor" = unsafe lower mass; "upper" = safe
upper cell.

| cell | a0 = 1116043 | a0+1 = 1116044 | label |
|---|---|---|---|
| c=1 identity-prefix MCA floor | PASSES, +25.6761 bits | FAILS, -5.4985 bits | PAID_BY_EXACT_CERTIFICATE at a0; failure recorded at a0+1 |
| c=1 LIST route (companion list object) | (also passes) | PASSES, +71.5129 bits; holds through a=1116046 (+9.1637), fails 1116047 (-22.0109) | PAID_BY_EXACT_CERTIFICATE (list object only) |
| c=2 LIST edge m=558022 | — | PASSES, +1.8790 bits, adjacent-tight (m=558023 fails) | PAID_BY_EXACT_CERTIFICATE (list object only) |
| c=2 / c=4 MCA controls | c=2 edge at a=1116038 (+18.3914) | c=2 fails (-75.1323), c=4 fails; no c>=8 grid contains a | PAID_BY_EXACT_CERTIFICATE (controls) |
| `B_tan` lower floor `n-a+1` | 981110 | 981109 | PAID_BY_THEOREM (LOWER floor only) |
| `B_tan` upper/exact cell | UNAVAILABLE (r=981109 > R_tan=349525) | UNAVAILABLE (r=981108 > R_tan) | OPEN |
| `B_quot_support` (SAFE_SUM, C={2,4,8,16,32}) | exact, ~2^1045455 (fingerprinted) | exact, ~2^1045455 | PAID_BY_THEOREM (upper; astronomically above B*, documented honestly) |
| `B_quot_image` | NO_CERTIFICATE | NO_CERTIFICATE | OPEN |
| zone gate | all declared N' in ZONE_A_NORM_EXACT; gate holds to N'=60, fails at 62; zone-(b) vacuous | same (t=67468, n/t~31.08) | printed arithmetic |
| `B_ap_regular` | NONEXISTENT (t=67467 < j+1=981110; deficiency 913643) | NONEXISTENT (t=67468 < j+1=981109; deficiency 913641) | CONJECTURAL_WITH_FALSIFIER |
| `B_ap_pivot` | OPEN (M5/WP-2.6 exists only at deficiency 1, toy row) | OPEN | CONJECTURAL_WITH_FALSIFIER (named future input: PR #282 XR) |
| `B_ext` | proper extension row; S6 chart classification undischarged; ExtPole arithmetic printed as hypothetical only | same | CONDITIONAL_ON_NAMED_INPUT (named future input: PR #284 F1 descent) |
| sparse / plain-CA | OPEN | OPEN — no theorem at delta ~ 0.4678 (exact landmark table in the JSON) | OPEN |
| mu4 monomial family | +4 empirical (toy-exhaustive F_97 n=16/32; 4 divides p-1 holds) | +4 empirical | EMPIRICAL / not-a-theorem-at-this-row |
| deduped total upper bound | NOT FINITE (open cells) | NOT FINITE (open cells) | — |
| verdict | **UNSAFE_BY_PROVED_LOWER_BOUND** | **UNDECIDED_WINDOW_OPEN** | thm:v13-windows |

## Verdict

- `a0 = 1116043` is **certified MCA-unsafe** by exact integer comparison
  (margin +25.6761 bits; reproduces upstream's printed `+25.7`).
- `a0+1 = 1116044` is an **undecided window** per `thm:v13-windows`: known
  proved lower mass is `981109 ~ 2^19.9041` against `B* ~ 2^57.9321` — a
  deficit of `274980728110413979`, i.e. unknown families would have to carry
  99.9999999996% of the budget — and **no safety theorem is in range** (the
  proved Hab25-quadratic import reaches only `delta ~ 0.2045`; the `~0.2881`
  edge is conditional, gap G4; Johnson is 366866 agreement steps away).

## The conversion-gap target (the packet's discovery)

At `a0+1 = 1116044` the c=1 identity-prefix floor certifies, by exact integer
arithmetic, a list of size `2^160.4336` in `RS[F,D,k+1]`, while the deep-point
list-to-MCA conversion threshold `(q+k)/k` sits at `2^165.9321`.  **The
conversion is missed by exactly 5.4985 bits — a factor of ~45.21.**  Any
sharpening of the `thm:A` list-to-MCA conversion (or of the pigeonhole floor)
worth `>= 5.4985` bits at this radius flips `a = 1116044` MCA-unsafe and pins
the staircase adjacently.  This is framed as CONJECTURAL_WITH_FALSIFIER: the
falsifier/next-target is the conversion sharpening; the alternative mass route
needs `~2^57.93` of new bad-slope mass, ~38.03 bits above every known
structured family.  A remarkable structural coincidence recorded in the
packet: `a = 1116044` is *exactly* the adjacent-tight c=2 LIST-route edge
(`m = 558022`, +1.8790 bits), a second independent list-unsafety certificate
at precisely this agreement.

## Replay

```sh
python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --check
```

Runtime: ~131 s measured (of which ~129 s is the exact five-divisor
`U_sum` plus its modular cross-check; the c=2 branch alone is ~110 s of
~1M-bit incremental big-integer steps; the ~2M-bit anchor binomials take
~0.2-0.3 s each via Legendre factorization + product tree).  `--check` reruns the full recomputation and
byte-compares the regenerated JSON.  Integers above ~2^200 (the `U_sum`
values) are stored as exact fingerprints (bit length, sha256 of big-endian
bytes, residues mod 2^64 / M61 / M31, log2); the verifier recomputes the
exact integers, re-derives every fingerprint, and additionally recomputes
every `U_sum` cell modulo `2^61 - 1` through an independent factorial-table
path.  Floats are informational (4 decimals); all verdicts are exact integer
comparisons.

## Non-claims

- **No adjacent pin is claimed.** `a* = 1116044` remains conjectural
  (prob:v13f1-frontier); the packet supplies no `U(a0+1) <= B*` certificate
  and none exists: the upper ledger has OPEN cells (tangent-upper, aperiodic,
  sparse/CA, extension-chart), so no finite deduped total is printed, and the
  window at `1116044` stays open per `thm:v13-windows`.
- The LIST-route certificates at `1116044` concern the companion list object,
  not the MCA verdict.
- The ExtPole value is hypothetical arithmetic (condition (i) of
  `prop:v13-extension` is not certified at this row); it is NOT a floor.
- `U_sum` covers only the declared dyadic quotient cells `{2,4,8,16,32}`;
  it is not global quotient exhaustion.
- The mu4 `+4` is empirical toy-row evidence and is never added to a
  theorem-backed total.
- PRs #282 and #284 are cited as named future inputs only, not audited or
  consumed here.
- Polynomial-loss quotient equidistribution is kept out of every finite
  claim (a factor `n^C` costs `21C` bits at `n = 2^21` against a 5.4985-bit
  margin), per the task instruction.

Companion audit note:
`experimental/notes/audits/audit_koalabear_frontier_adjacent_ledger.md`.
