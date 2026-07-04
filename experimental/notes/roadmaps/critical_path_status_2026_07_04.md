# Critical-path status: the clean-rate determination (2026-07-04)

- **Status:** STATUS REPORT (no new mathematics in this note; every
  claim below is a pointer to a verifier-backed packet, an open PR, or
  an explicitly-labeled open item).
- **Audience:** maintainer. Companion to the incoming packet PR wave
  (#232-#241 and successors) and to `campaign_report_00/01/02`.
- **One line:** the clean-rate (rho in {1/4, 1/8, 1/16}) MCA safe-side
  determination is reduced, through a machine-verified chain, to a
  PROVED structural dichotomy plus an enumerated list of five
  certification/counting blockers — each blocker owned, three of the
  five in active execution.

## The structure (what is proved)

1. **The compiler.** The determination obligation compiles to one
   counting column: `R_PTE <= n^3` primitive trades per row
   (poly-forcing compiler + budget audit + W4 column rewiring; exact
   integer sufficiency at all six candidate rows; in the packet wave).
2. **The taxonomy.** Charged = the pullback class, completely
   classified (star-PTE normal form #232; tame Laurent-Ritt / toral
   stabilizer #233; dihedral branch; boundary/coset and moment forms).
3. **The dichotomy (the campaign's centerpiece).** Every finite-row
   minimal h-trade, for every h, is either full-fiber (paid, possible
   only at 2-power h) or a p-specific norm-gate event: the row prime
   divides an explicit nonzero cyclotomic obstruction norm. Chain:
   X24 char-0 dyadic descent (#234-adjacent; packet in wave) + X81
   square-shift normal form (#238) + X82 certifier keys (#239) + X83
   uniform obstruction gate (#240) + X32 h=4 dichotomy (#241).
4. **Good reduction (A3).** The obstruction variety is a *graph* in
   coefficient space (h-only, scaling-equivariant); away from an
   explicit finite exceptional-prime set D(n,h), finite-row trades do
   not exceed the char-0 classification — which is EMPTY of
   non-fiber trades (X24). Validated end-to-end at (n,h) = (16,3):
   the predicted exceptional set {7, 17, 97} matches brute force in
   both directions. The historically-observed "exceptional primes"
   are exactly the bad-reduction primes of this lemma.
5. **The giant regime, char-0 half (B1).** Over characteristic zero,
   every 0/1 t-null block is a union of mu_M-cosets (M = least
   2-power > t) — Galois-orbit argument, exhaustively toy-verified.
   The boundary (M = t, zero-sum-pattern) class at finite rows is
   exactly counted and fits its column.

## The conditional critical path (the five blockers)

The determination follows from the above plus:

| # | Blocker | Content | State |
|---|---------|---------|-------|
| 1 | C1a | Direct per-row MITM certificates, h = 4(-5), n = 1024, official Row-C primes | pipeline running (validation-gated) |
| 2 | C1b | Descent-injection certificate, h <= ~10 (band-pair pushforward; seed identity verified) | injection lemma in proof |
| 3 | mid/large h | h in (~10, A], A = 67/133/261 per rate: neither pipeline reaches it | routes mapped; an active-core injection argument (via the graph structure) in attempt; fallback = per-h certificates or emptiness lemma |
| 4 | B2b | Giant-regime mod-p no-concentration: non-coset t-null count <= n^3 = 2^123 (first-moment balanced to ~2%; the cushion is 123 bits) | balance-point falsifier scan running; proof brief follows its verdict |
| 5 | C2 + micro-lemma | Per-row GCD certification (harness BUILT, self-test recovers {7,17,97} exactly) + the star-PTE support bound h <= A vs 2h <= A | mechanical once 1-3 land; micro-lemma in draft |

Honest notes: (i) the brute-force certificate computation was
*measured infeasible* at n = 1024 (elimination dies at n = 32) — that
finding forced blockers 2-3 and is recorded, not hidden; (ii) the
h-window cap previously assumed (2 log2 n) has NO derivation — the
audit replaced it with H_max = A, *widening* the declared gap
(blocker 3); (iii) the giant regime sits within ~2% of the counting
threshold, so blocker 4 cannot close by counting alone — the 123-bit
budget cushion is what makes it tractable.

## What supports the claim right now

- Ten scoped packet PRs (#232-#241) carrying the taxonomy + dichotomy
  chain, each with note + green verifier + certificate + 5-line body.
- The updated prize DAG in this PR (validator green: structure, refs,
  acyclicity, reachability, status propagation) with the critical
  path exactly as stated above; ~100 PROVED nodes verifier-backed.
- The falsification ledger (report 02, in draft): twelve
  falsified-and-repaired statements — the program's
  falsify-before-prove discipline, including three self-inflicted
  corrections caught this week (the h-only uniformity, the 4-level
  descent claim, the unfounded window cap).

## Asks

None blocking. Visibility + (when convenient) the integration sweep
and the Reading-B / rules-freeze items from report 00. Packet PRs
land in dependency order; this status note will be refreshed when
blockers flip.
