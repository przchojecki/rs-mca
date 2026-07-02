# WP-1.1 + WP-1.2 detail (L3): the finite-row submission note + Lean gates

- **Status:** packaging plan over PROVED-cited material; the Lean scope is
  pinned by the repo's stdlib-only constraint. Witnesses machine-checked.
- **Executability:** AGENT (writing + Lean); submission itself is MAINT
  sign-off (WP-7.4). Official context: the live prize statement
  *encourages* partial results AND formal verification (wp0_2 fetch) —
  both packages have direct submission value.
- **Parents:** r2 WP-1.1/1.2; consumes s2 (two-regime picture), s5_s0
  (axes), wp0_2 (mechanics), wp3_2 (descriptor as constants source).

## 1. WP-1.1: the submission note, section by section

**Deliverable:** `experimental/notes/submission/f17_32_partial_note.md`.

```text
§1 row + conventions block: C = RS[F_17^32, mu_512, 256]; BOTH gates
   (B*_aff = B*_proj = 6); endpoint convention (closed grid, supremum
   3/256 unattained); q_gen = q_line (generating, ord(17 mod 512) = 32);
   delta-regime label: TANGENT REGIME, delta ~ 0.0117 << Johnson 0.293 —
   explicitly NOT band content (standing order 11).
§2 the claim (adjacent pin): LD_sw(C,506) = 7 > B* = 6 >= LD_sw(C,507);
   radius form: safe closed grid radius 5/512; first unsafe 6/512 = 3/256.
§3 proof summary: staircase compiler (B_Q = 6 <= cap = 85 => a_safe =
   n - B_Q + 1 = 507) + TWO independent numerator replays already on
   main (#147 package; #148 independent GF(17^32) tower) + the M2 smoke
   packet (aperiodic numerator 0 — tangent pays everything).
§4 official-language column: the claim restated against the ABF sampler
   WITH the S0 axes table (axes 3/5/7 verified; 1/2/4 open) — the note
   CONDITIONS on the open axes instead of asserting equivalence; cites
   the step-1 reconciliation and the M0 freeze as the audit trail.
§5 non-claims block: no band content; no rate-family statement; no
   official-acceptance implication (towards-prize §9 list, verbatim).
§6 prize-relevance: quotes the partial-results and award-split clauses
   from the rules freeze (wp0_2), positioning this as the worked example
   of the small-q regime (s2: every row with q < 2^128 (n-k)/3 pins the
   same way — the envelope map generalizes this note to a FAMILY).
```

**Acceptance test:** every number in the note is emitted by the wp3_2
descriptor (zero hand constants); the WP-0.4 harness is green on the four
cited verifiers; the two replays agree (already met); submission
checklist per the fetched mechanics (email; peer-review path; ePrint/arXiv
posting for timestamp; conflict disclosure) is attached as front matter.

**Failure branches:** S0 axes stay open at submission time -> submit as
"repo-convention theorem + documented reconciliation" (honest and still
eligible under the partial clause); rules drift (wp0_2 detector fires) ->
regenerate §4/§6 from the new freeze.

## 2. WP-1.2: Lean gates — exactly what stdlib can certify

**Constraint (respected, not fought):** the repo's Lean is stdlib-only by
maintainer choice — no Mathlib, hence no polynomials/Finset; certifiable
content is Nat/Int/Rat arithmetic and abstract Props as named targets.

**Tier 1 (provable NOW, kernel-checkable — the submission gates):**

```text
gate bracketing via ADDITION CERTIFICATES (machine-checked witnesses):
  6 * 2^128 + 326217393234836465063858652730341978625  = 17^32
  17^32     + 14064973686101998399515954701426232831   = 7 * 2^128
  (two Nat equalities the kernel verifies by computation — no decide
  on comparisons needed, no numeral-performance risk);
staircase arithmetic: B_Q = 6 <= 85 = (512 - 256)/3; a_safe = 507;
endpoint conversions over Rat: 5/512 < 6/512 = 3/256; r = n - a maps.
```

**Tier 2 (when the M4 table exists):** the dedup arithmetic — sums and
comparisons of per-ledger Nat contributions against B*, mirroring the
WP-0.4 checker's H2/H5 logic in kernel-checked form.

**Tier 3 (statements only, no proofs pretended):** FM1, R2, Conjecture F
as named Props with their hypothesis structure — the certification map
marks these TARGET, never proved (the honest boundary of stdlib).

**Assets:** `experimental/lean/rs_mca_formalization/` builds green today
(Basic, DeepPoint — mine, BetaTwoReductionLedger, F1ExtensionLedger).

**Acceptance test:** `lake build` green, ZERO sorry; tier-1 theorems
present; a `CERTIFICATION_MAP.md` mapping each Lean theorem to the note
claim it certifies (what a judge consumes, per the official
formal-verification encouragement). **Failure branches:** kernel numeral
performance (already dodged via addition certificates); scope creep
toward Mathlib (foreclosed — tier 3 stays Props).

## 3. What this buys

The first submittable artifact of the program: a fully conditioned,
convention-explicit partial result whose every constant is
machine-generated, whose arithmetic core is kernel-certified, and whose
claims are fenced by the same S0 gate the rest of the plan enforces —
the template every later dossier rung (s8_s9 §3 ladder) reuses.
