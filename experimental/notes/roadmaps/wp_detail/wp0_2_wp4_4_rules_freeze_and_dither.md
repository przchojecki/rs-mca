# WP-0.2 + WP-4.4 detail (L3): official rules freeze + hypothesis/dither coverage

- **Status:** AUDIT plan, grounded by a LIVE fetch of proximityprize.org on
  2026-07-02 (quotes below; the statement self-describes as preliminary).
- **Executability:** AGENT throughout — lookups, tables, one small checker.
- **Parents:** r2 WP-0.2, WP-4.4; consumes `proof_sketch/s5_s0` (axes 8, 9)
  and the master constants table.

## 1. Live-fetch findings (2026-07-02) — and the discrepancies that matter

```text
(a) RATES EXACT: "the rate rho(C) := k/|Z| is one of {1/2, 1/4, 1/8, 1/16}"
    — no latitude/dither language. S0 axis 9 provisionally resolves
    ADVERSE: exact rates => 2-power k on 2-power domains => the maximal
    dyadic quotient structure STANDS (s5_s0 F2's half-reserve swing is
    off the table under current wording, but see the drift monitor below).
(b) FIELD CAP NOT ON THE PAGE: the live statement says only "|F|
    sufficiently large so that delta*_C exists" — the repo's working
    constants k <= 2^40 and |F| < 2^256 were NOT found there. They must
    be confirmed against ePrint 2026/680 (repo readme records them, so
    they likely live in the paper). All corridor formulas parameterize in
    log2 q and survive either way, but B*'s magnitude and the "~90-bit
    open band" statement (s8_s9) DEPEND on the 2^256 cap. HIGH PRIORITY.
(c) "SMOOTH" UNDEFINED ON THE PAGE: "smooth evaluation domain Z <= F" —
    2-power vs general smooth must be pinned from the paper. Note the
    direction is favorable: 2-power domains are the MOST quotient-rich,
    so the sketch's adverse quotient analysis is conservative for any
    broader smooth class [SKETCH].
(d) LIST QUANTIFIER AMBIGUOUS: "|Lambda(C^{==m}, delta*)| <= eps* |F|,
    constant m" — for-all m or exists m? If FOR-ALL: verified this turn,
    the clique cap n >= k + m^2(a-k) bounds m <= sqrt((n-k)/t) ~ 16..31
    near-cap across the rates — uniform-in-m handling is FINITE and
    affordable; the budgets of s7 §3 need an m-sweep, not new math.
(e) PARTIAL RESULTS EXPLICITLY ENCOURAGED; awards splittable at judges'
    discretion — the partial ladder (s8_s9 §3) is submission-relevant.
(f) FORMAL VERIFICATION "encouraged" — WP-7.3's Lean gates have direct
    official value, not just internal assurance.
(g) PRELIMINARY: "details may still change" — a drift monitor is
    mandatory, not paranoia.
```

## 2. WP-0.2 deliverable: the freeze note + drift detector

**Deliverable:** `experimental/notes/audits/prize_rules_freeze.md` — a
pinned-quote table, one row per operative constraint:

```text
columns: item | exact quote | source (URL/ePrint section) + fetch date |
         repo working assumption | status MATCH / DISCREPANT / UNSTATED
rows:    rates; k-range; field cap; field type (prime/extension allowed);
         "smooth" definition; domain-in-F* vs F; MCA statement verbatim;
         list statement verbatim; m quantifier; list denominator |F|;
         per-row eligibility; award splits; submission format
         (email + peer review + ePrint/arXiv posting); formal-verification
         clause; conflict disclosure; preliminary disclaimer.
```

**Acceptance test (verifier-runnable):**
`experimental/scripts/verify_prize_rules_freeze.py` stores the SHA-256 of
each quoted block plus its fetch date; PASS = all quoted blocks present in
the note and hashes match the stored values. Re-running after a re-fetch
diffs the hashes — a RULES-DRIFT DETECTOR with the dither axis (a) and the
field cap (b) as its two highest-value tripwires.

**Route:** one WebFetch pass of the site (done above) + one read of ePrint
2026/680 §(challenge statements) to resolve (b), (c), (d); write the
table; script the hasher. Prerequisites: none. Effort: one turn of
execution when scheduled.

**Failure branches:**

```text
site vs ePrint conflict  -> freeze BOTH with dates; flag to maintainer;
                            plan against the stricter reading until the
                            organizers clarify.
(b) cap absent in ePrint -> re-state the coverage split parametrically in
                            log2 q (formulas already are); the dossier
                            quotes thresholds as functions, not numbers.
(c) smooth broader       -> sketch analysis stands as the conservative
                            (most-adverse) case; add a "domain class"
                            hypothesis line to the S5 tables.
(d) for-all m            -> run the s7 budgets as an m-sweep to the
                            clique-cap bound (finite, verified above).
```

## 3. WP-4.4 deliverable: the hypothesis-coverage table

**Deliverable:** `experimental/notes/audits/hypothesis_coverage.md` +
generator script. Grid:

```text
rows:    (rate rho) x (field class: prime / extension-generating /
         extension-non-generating) x (n from the k-range once (b) pins it)
columns: H1 exact rate (rules: EXACT, per (a));
         H2 admissibility (cap per (b) — parametric until pinned);
         H3 generating (ord computation; non-generating => imported S7
             window binds, s6);
         H4 conventions (both gates printed; +1 edge iff 2^128 | q+1);
         H5 quotient profile (dyadic-maximal, forced by (a));
         H6 condition set {R2, Conj F, zone-(b)} — which verdict class
             each row's corridor cells land in (s8_s9 contract);
         binding mechanism column (S2 corridor vs imported S7 window);
         m-sweep cap (per (d), sqrt((n-k)/t) at the row's corridor).
```

**Acceptance test:** the table is GENERATED by a script from the master
constants (re-deriving the s5_s0 numbers — which are already
machine-verified — and the ord/gate computations per row); every cell
carries a pointer to the note that justifies it; the checker refuses rows
with any UNSTATED rules cell (ties into the WP-7.1 refusal rule).

**Failure branches:** any rules cell flips (drift detector fires) ->
regenerate; the table is cheap by construction, which is the point.

## 4. What this buys the plan

WP-0.2/4.4 convert the sketch's two biggest non-mathematical sensitivities
(dither latitude — now provisionally closed adverse; field cap — now
flagged genuinely unresolved) into monitored, hash-pinned facts with a
regeneration path, so no downstream theorem or dossier ever silently
depends on a stale reading of a preliminary statement.
