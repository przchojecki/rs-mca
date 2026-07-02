# WP-7.2 + WP-7.3 + WP-7.4 detail (L3): promotion, formal gates, the versioned dossier

- **Status:** governance/packaging detail; no new mathematics (and none
  pretended). Consumes the verified constants and gate structures of
  earlier notes; introduces no new numbers.
- **Executability:** WP-7.2 MAINT-gated (agents prepare, never touch
  `tex/`); WP-7.3/7.4 AGENT with MAINT sign-off at submission.
- **Parents:** r2 WP-7.2/7.3/7.4; consumes wp0_4 (harness), wp1_1/1_2
  (note + Lean tiers), wp6_3 (bridge ledger), wp0_2 (mechanics), s8_s9
  (verdict classes, partial ladder).

## 1. WP-7.2: promotion — the readiness checklist and the boundary

**The rule (unchanged, repo-constitutional):** agents never edit `tex/`;
promotion into Papers B/C/D is the maintainer's act. What agents own is
the PROMOTION DOSSIER for a candidate packet:

```text
readiness checklist (all mandatory):
  R1 harness green in promotion mode (stricter than CI: zero PENDING,
     negative controls red, certificate hashes pinned);
  R2 replayed at least twice (author run + one independent replay in the
     WP-0.3 format);
  R3 labels: only PROVED-cited content promotes; SKETCH/CONJECTURE stays
     in experimental/ by definition;
  R4 S0-conditioning explicit wherever the claim touches the official
     object (the wp1_1 §4 pattern);
  R5 every bridge crossing has its wp6_3 ledger row;
  R6 agents-log provenance chain intact (who, when, what verified).
```

**Acceptance test:** the promotion-readiness checker = WP-0.4 harness run
with `--promotion` (R1) + a checklist linter for R2-R6 emitting one
verdict per candidate packet. **Failure branch:** maintainer rejects ->
the rejection reasons re-enter the queue as WP items; nothing is lost
because the dossier records exactly which gate failed.

## 2. WP-7.3: formal gates — the certification map completed

Extends the wp1_2 tier structure to the full gate list, in priority
order (matching the official "formal verification encouraged" clause):

```text
G1 definitions file (MCA predicates — exists, Basic.lean)      [green]
G2 finite certificates: gate bracketing via addition
   certificates; staircase arithmetic; endpoint Rat facts      [tier 1]
G3 M4 dedup arithmetic mirrored in kernel-checked form
   (sums/comparisons vs B*, the H2/H5 checker logic)           [tier 2]
G4 descriptor regression in Lean: the wp3_2 constants for the
   slate rows as kernel-checked Nat/Rat facts (cheap, high
   assurance for every number a judge reads)                   [tier 2]
G5 FM1 / R2 / Conjecture F as named Props with hypothesis
   structure — TARGET markers, never claimed                   [tier 3]
```

**Acceptance test:** `lake build` green, zero sorry, and
`CERTIFICATION_MAP.md` COMPLETE in the strong sense: every claim row of
every dossier version (§3) carries exactly one of
`Lean-certified / harness-verified / cited-proof / conditional(H6, axes)`
— no unclassified claims. **Failure branch:** stdlib limits bite (no
polynomials/Finset) -> the boundary is already drawn at G5; nothing
above it depends on Mathlib.

## 3. WP-7.4: the versioned dossier — exact content per version

```text
v-PARTIAL (buildable NOW, ships conditioned on open S0 axes):
  pinned-row submission note (wp1_1) + envelope-map family statement
  (the small-q regime as a THEOREM FAMILY, not one row) + rules freeze
  and reconciliation tables + certification map (G1-G2) + verbatim
  non-claims + bridge ledger. Gate: harness green; S0 rows printed with
  their open/verified status; conditioning language per wp1_1 F1.
v-INTERIM (after P2/P2.5 + slate work):
  + window theorem (predicted aperiodic-0, whatever it actually says) +
  deficiency-1 packets (PR #172 line) + Row-C collision data (the first
  zone-(b) evidence) + second pin OR the Row-A wall dossier (wp3_3
  dichotomy — EITHER outcome is dossier content) + updated M4 tables
  with interval cells. Gate: + G3/G4 green; every table
  descriptor-generated.
v-FULL (after H6 = {R2, zone-(b)} + list-side {L1, a-regularity}):
  + the per-rate threshold theorems (s5_s0 shapes with H6 discharged) +
  compiler-emitted adjacent verdicts for the slate + both grand-
  challenge statements with the challenge-field denominators printed.
  Gate: compiler refusal rule passes with ZERO conditional cells on
  prize-facing rows.
```

**Assembly mechanics:** the dossier is a GENERATED document — descriptor
tables + harness report + certification map + bridge ledger + the notes,
stitched by a build script that stamps version, date, and the rules-
freeze hash it was built against (wp0_2 drift detector integration);
submission per the fetched mechanics (email; peer-review venue; ePrint/
arXiv posting for the timestamp; conflict disclosure).

**Acceptance test:** the build script REFUSES to emit any version whose
gate list is not green (the s8_s9 refusal rule, applied to the dossier
itself); a dry-run build of v-PARTIAL succeeds today up to the S0
conditioning language. **Failure branches:** judge/reviewer feedback ->
versioned revisions with changelogs (the ePrint timestamp protects
priority); rules drift -> the stamped freeze-hash mismatch forces a
rebuild — stale dossiers are unshippable BY CONSTRUCTION.

## 4. What this buys

The path from "theorem in experimental/" to "artifact a judge reads" is
now three checkable gates with no manual steps that can silently skip a
condition: promotion readiness is a linter verdict, certification status
is a total map, and a dossier that doesn't meet its version gate cannot
be built at all.
