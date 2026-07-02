# Theorem-Label Map Across the Four Papers

- **Status:** AUDIT.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This is a review aid for the four paper files named in
  `agents.md`.  It does not change proof status and it is not a substitute for
  the source statements.  Labels are local to a single `.tex` file; for example
  `thm:main` appears in more than one paper and must be read with its filename.

## Status Key

- **PROVED:** The paper presents the statement as proved, possibly using named
  external theorems cited in that statement.
- **CONDITIONAL:** The statement depends on an explicit assumption or imported
  theorem whose verification is outside the paper.
- **CONJECTURAL:** The statement is a conjecture or local-limit target.
- **COUNTEREXAMPLE:** The statement is the target being refuted, or a proved
  disproof of that target.
- **AUDIT:** Definition, remark, example, open problem, or ledger item whose
  role is organizational rather than a new theorem.

## Dependency Spine

1. `tex/RS_disproof_v3.tex` proves the no-slack obstruction.  Its main theorem
   uses the quotient locator, restricted-sum coverage, monotonicity, Fermat
   digit checks, and the cyclotomic sieve.
2. `tex/slackMCA_v4.tex` separates the corrected list and MCA ledgers and
   promotes the high-agreement line/list/curve boundary layer into Paper B.
3. `tex/cs25_cap_v6.tex` proves the universal MCA cap through a self-contained
   deep-point conversion and records the prize-facing completion program.
4. `tex/snarks_v5.tex` consumes the previous papers as protocol ledger inputs:
   entropy reserve, quotient profile, list/interleaving, MCA or line-decoding,
   field separation, and failure-ladder audits.

## Paper A: No-Slack Obstruction

- `tex/RS_disproof_v3.tex` `conj:capacity`
  - Kind/status: conjecture; COUNTEREXAMPLE target.
  - Role: no-slack support-wise line-MCA statement refuted by the paper.
- `tex/RS_disproof_v3.tex` `def:mca`
  - Kind/status: definition; AUDIT.
  - Role: local definition of support-wise line-MCA error.
- `tex/RS_disproof_v3.tex` `thm:main`
  - Kind/status: theorem; PROVED / COUNTEREXAMPLE.
  - Role: proves the no-slack conjecture false and gives list lower bounds.
- `tex/RS_disproof_v3.tex` `rem:status-scope`
  - Kind/status: remark; AUDIT.
  - Role: records which parts are elementary and which use the sieve.
- `tex/RS_disproof_v3.tex` `lem:locator`
  - Kind/status: lemma; PROVED.
  - Role: quotient-locator identity producing bad line slopes.
- `tex/RS_disproof_v3.tex` `lem:dsh`
  - Kind/status: lemma; PROVED using imported Dias da Silva--Hamidoune.
  - Role: restricted-sum coverage input for bad-slope fullness.
- `tex/RS_disproof_v3.tex` `lem:monotone`
  - Kind/status: lemma; PROVED.
  - Role: propagates badness to larger radii.
- `tex/RS_disproof_v3.tex` `lem:fermat`
  - Kind/status: lemma; PROVED.
  - Role: digit lemma for Fermat-prime deployed examples.
- `tex/RS_disproof_v3.tex` `lem:value-family`
  - Kind/status: lemma; PROVED.
  - Role: exact-support value family used by later finite checks.
- `tex/RS_disproof_v3.tex` `lem:granularity`
  - Kind/status: lemma; PROVED.
  - Role: converts quotient-order choices into density granularity.
- `tex/RS_disproof_v3.tex` `thm:sieve`
  - Kind/status: theorem; PROVED using a Siegel--Walfisz input.
  - Role: supplies infinitely many logarithmic quotient examples.
- `tex/RS_disproof_v3.tex` `thm:ext-smooth-towers`
  - Kind/status: theorem; PROVED.
  - Role: extension-tower density of smooth obstruction instances.
- `tex/RS_disproof_v3.tex` `prop:ext-density`
  - Kind/status: proposition; PROVED.
  - Role: box-density extension bound for generated-field examples.

## Paper B: Slack, Entropy, Quotients, and MCA

- `tex/slackMCA_v3.tex` `thm:integrated-package`
  - Kind/status: theorem package; AUDIT.
  - Role: built-in map of proved, conditional, and conjectural components.
- `tex/slackMCA_v3.tex` `def:locator-fiber`
  - Kind/status: definition; AUDIT.
  - Role: locator-fiber object used for list-size statements.
- `tex/slackMCA_v3.tex` `prop:monomial-fiber`
  - Kind/status: proposition; PROVED.
  - Role: identifies monomial-prefix words with exact prefix fibers.
- `tex/slackMCA_v3.tex` `def:taustar`
  - Kind/status: definition; AUDIT.
  - Role: generated-field entropy gap.
- `tex/slackMCA_v3.tex` `thm:pigeonhole`
  - Kind/status: theorem; PROVED.
  - Role: coefficient pigeonhole lower bound for list size.
- `tex/slackMCA_v3.tex` `cor:genfield-pigeonhole`
  - Kind/status: corollary; PROVED.
  - Role: strengthens the entropy floor to the generated field.
- `tex/slackMCA_v3.tex` `cor:entropy-lower`
  - Kind/status: corollary; PROVED.
  - Role: exponential lists below the entropy gap.
- `tex/slackMCA_v3.tex` `thm:qcore`
  - Kind/status: theorem; PROVED.
  - Role: quotient-core list obstruction at active divisor scales.
- `tex/slackMCA_v3.tex` `cor:one-scale-false`
  - Kind/status: corollary; PROVED.
  - Role: refutes the one-scale ambient-field entropy prediction.
- `tex/slackMCA_v3.tex` `def:qprofile`
  - Kind/status: definition; AUDIT.
  - Role: quotient-core profile consumed by Paper C certificates.
- `tex/slackMCA_v3.tex` `conj:listprofile`
  - Kind/status: conjecture; CONJECTURAL.
  - Role: corrected list entropy gap with quotient exceptions.
- `tex/slackMCA_v3.tex` `thm:upstairs`
  - Kind/status: theorem; PROVED.
  - Role: characteristic-zero inverse quotient theorem.
- `tex/slackMCA_v3.tex` `cor:upstairs-poly`
  - Kind/status: corollary; PROVED.
  - Role: polynomial characteristic-zero prefix fibers above quotient reserve.
- `tex/slackMCA_v3.tex` `thm:no-collision`
  - Kind/status: theorem; PROVED.
  - Role: Galois-amplified finite-field no-collision bound.
- `tex/slackMCA_v3.tex` `cor:quasipoly-upper`
  - Kind/status: corollary; PROVED.
  - Role: monomial-prefix upper bound in quasi-polynomial split primes.
- `tex/slackMCA_v3.tex` `conj:prefix-local`
  - Kind/status: conjecture; CONJECTURAL.
  - Role: prefix local limit with quotient exceptions.
- `tex/slackMCA_v3.tex` `conj:arbitrary-local`
  - Kind/status: conjecture; CONJECTURAL.
  - Role: arbitrary received-word locator-fiber local limit.
- `tex/slackMCA_v3.tex` `thm:conditional-list`
  - Kind/status: theorem; CONDITIONAL.
  - Role: positive list theorem conditional on local-limit inputs.
- `tex/slackMCA_v3.tex` `def:mca`
  - Kind/status: definition; AUDIT.
  - Role: line-MCA error definition used in Paper B.
- `tex/slackMCA_v3.tex` `thm:onez`
  - Kind/status: theorem; PROVED.
  - Role: one bad parameter per support.
- `tex/slackMCA_v3.tex` `prop:floor`
  - Kind/status: proposition; PROVED.
  - Role: tangent floor for MCA numerators.
- `tex/slackMCA_v3.tex` `def:badset`
  - Kind/status: definition; AUDIT.
  - Role: multi-symmetric bad-slope image.
- `tex/slackMCA_v3.tex` `thm:exactslack`
  - Kind/status: theorem; PROVED.
  - Role: exact slack characterization for canonical lines.
- `tex/slackMCA_v3.tex` `lem:tlocator`
  - Kind/status: lemma; PROVED.
  - Role: quotient locator for the slack/MCA setting.
- `tex/slackMCA_v3.tex` `thm:slackt`
  - Kind/status: theorem; PROVED.
  - Role: slack-t lower bound.
- `tex/slackMCA_v3.tex` `prop:collapse`
  - Kind/status: proposition; PROVED.
  - Role: subgroup-symmetric slack collapses to the one-condition ladder.
- `tex/slackMCA_v3.tex` `cor:certified`
  - Kind/status: corollary; PROVED.
  - Role: certified slack at the root barrier.
- `tex/slackMCA_v3.tex` `thm:twomoment`
  - Kind/status: theorem; PROVED.
  - Role: two-moment fullness in the square-root range.
- `tex/slackMCA_v3.tex` `cor:twomomentmca`
  - Kind/status: corollary; PROVED.
  - Role: slack-two monomial-line failure at the root barrier.
- `tex/slackMCA_v3.tex` `thm:ladder`
  - Kind/status: theorem; CONDITIONAL.
  - Role: polynomial-range free-pool ladder from an exponential-sum input.
- `tex/slackMCA_v3.tex` `thm:descent`
  - Kind/status: theorem; PROVED.
  - Role: dyadic descent giving error one at dyadic slack.
- `tex/slackMCA_v3.tex` `thm:diag`
  - Kind/status: theorem; PROVED.
  - Role: two-sided canonical-line theorem.
- `tex/slackMCA_v3.tex` `thm:allbasesdir`
  - Kind/status: theorem; PROVED.
  - Role: Newton obstruction criterion replacing a false all-bases claim.
- `tex/slackMCA_v3.tex` `ex:falseallbasesdir`
  - Kind/status: example; COUNTEREXAMPLE.
  - Role: explains why the earlier all-bases non-dyadic theorem was false.
- `tex/slackMCA_v3.tex` `thm:stable`
  - Kind/status: theorem; PROVED.
  - Role: exactness in the stable range for proved strata.
- `tex/slackMCA_v3.tex` `thm:normalform`
  - Kind/status: theorem; PROVED.
  - Role: exact residue-line normal form.
- `tex/slackMCA_v3.tex` `prob:perfiber`
  - Kind/status: problem; CONJECTURAL.
  - Role: open per-fiber collision problem for the positive MCA side.
- `tex/slackMCA_v3.tex` `conj:B`
  - Kind/status: conjecture; CONJECTURAL.
  - Role: floor- and quotient-corrected slack MCA threshold.
- `tex/slackMCA_v3.tex` `prop:qfloor`
  - Kind/status: proposition; PROVED.
  - Role: quotient-exact floor above norm threshold.
- `tex/slackMCA_v3.tex` `thm:qnecessity`
  - Kind/status: theorem; PROVED.
  - Role: quotient profile is necessary for polynomial MCA bounds.
- `tex/slackMCA_v3.tex` `prop:prize`
  - Kind/status: proposition; PROVED.
  - Role: grand-challenge cap below roughly 150--162 bits.
- `tex/slackMCA_v3.tex` `thm:capimport`
  - Kind/status: theorem; CONDITIONAL.
  - Role: older imported list-to-agreement conversion used by CA/list comparison routes; superseded for the main MCA cap by Paper D v6.
- `tex/slackMCA_v3.tex` `thm:cap`
  - Kind/status: theorem; CONDITIONAL in Paper B v3; superseded by Paper D v6 for the main MCA cap.
  - Role: older universal-cap route; Paper D v6 is the self-contained reference for the proved MCA cap.
- `tex/slackMCA_v3.tex` `thm:subfield`
  - Kind/status: theorem; PROVED.
  - Role: subfield confinement for base-valued line witnesses.
- `tex/slackMCA_v3.tex` `cor:decouple`
  - Kind/status: corollary; PROVED.
  - Role: separates extension-field MCA lines from base-list obstructions.
- `tex/slackMCA_v3.tex` `thm:chebqcore`
  - Kind/status: theorem; PROVED.
  - Role: quotient cores for Chebyshev domains.
- `tex/slackMCA_v3.tex` `thm:23rigidity`
  - Kind/status: theorem; CONDITIONAL.
  - Role: mixed-radix rigidity using an imported vanishing-sums theorem.
- `tex/slackMCA_v3.tex` `thm:templates`
  - Kind/status: theorem; CONDITIONAL.
  - Role: torsion-coset template structure under an imported bound.
- `tex/slackMCA_v3.tex` `conj:final-locator`
  - Kind/status: conjecture; CONJECTURAL.
  - Role: final locator local limit.
- `tex/slackMCA_v3.tex` `conj:final-mca`
  - Kind/status: conjecture; CONJECTURAL.
  - Role: final floor- and quotient-corrected MCA asymptotic.

## Paper D: Universal Cap

- `tex/cs25_cap_v12.tex` `thm:A`
  - Kind/status: imported theorem; CONDITIONAL.
  - Role: Crites--Stewart list-to-agreement conversion.
- `tex/cs25_cap_v12.tex` `thm:B`
  - Kind/status: imported theorem; CONDITIONAL.
  - Role: independent slacked conversion route.
- `tex/cs25_cap_v12.tex` `rem:import`
  - Kind/status: remark; AUDIT.
  - Role: due-diligence checklist for the imported conversions.
- `tex/cs25_cap_v12.tex` `lem:fiber`
  - Kind/status: lemma; PROVED.
  - Role: locator fibers produce list lower bounds over the field of definition.
- `tex/cs25_cap_v12.tex` `lem:inter`
  - Kind/status: lemma; PROVED.
  - Role: interleaving transfer for CA and MCA errors.
- `tex/cs25_cap_v12.tex` `thm:main`
  - Kind/status: theorem; CONDITIONAL.
  - Role: universal cap using the imported Crites--Stewart conversion.
- `tex/cs25_cap_v12.tex` `cor:grand`
  - Kind/status: corollary; CONDITIONAL.
  - Role: field-size cap for the challenge envelope.
- `tex/cs25_cap_v12.tex` `cor:deployed`
  - Kind/status: corollary; CONDITIONAL.
  - Role: KoalaBear sextic deployed-parameter consequence.
- `tex/cs25_cap_v12.tex` `cor:rows`
  - Kind/status: corollary; CONDITIONAL.
  - Role: applies the cap to interleaved rows from the survey tables.
- `tex/cs25_cap_v12.tex` `prop:slacked`
  - Kind/status: proposition; CONDITIONAL.
  - Role: independent slacked variant via the second imported theorem.
- `tex/cs25_cap_v12.tex` `lem:confine`
  - Kind/status: lemma; PROVED.
  - Role: subfield confinement for base-valued line witnesses.
- `tex/cs25_cap_v12.tex` `cor:Fvalued`
  - Kind/status: corollary; PROVED.
  - Role: certifying lines over extensions must be genuinely extension-valued.
- `tex/cs25_cap_v12.tex` `prob:explicit`
  - Kind/status: problem; CONJECTURAL.
  - Role: asks for explicit extension-valued bad lines.
- `tex/cs25_cap_v12.tex` `prob:errorone`
  - Kind/status: problem; CONJECTURAL.
  - Role: asks whether the cap can be strengthened to error one.

## Paper C: Protocol Ledger and Certificates

- `tex/snarks_v4.tex` `def:fiber`
  - Kind/status: definition; AUDIT.
  - Role: feasible locator fiber used by the protocol list bridge.
- `tex/snarks_v4.tex` `lem:fiber-list`
  - Kind/status: lemma; PROVED.
  - Role: turns fiber bounds into list bounds.
- `tex/snarks_v4.tex` `def:list-arity`
  - Kind/status: definition; AUDIT.
  - Role: records the protocol list arity consumed by the ledger.
- `tex/snarks_v4.tex` `ass:extension-mca-lift`
  - Kind/status: assumption; CONJECTURAL.
  - Role: separates base-field MCA from extension-line MCA.
- `tex/snarks_v4.tex` `ass:locator`
  - Kind/status: assumption; CONJECTURAL.
  - Role: field-aware locator local limit needed for positive list ledgers.
- `tex/snarks_v4.tex` `ass:mca`
  - Kind/status: assumption; CONJECTURAL.
  - Role: corrected MCA or line-decoding local limit over the actual line field.
- `tex/snarks_v4.tex` `rem:no-substitution`
  - Kind/status: remark; AUDIT.
  - Role: warns against replacing `q_gen` by `q_chal` without a theorem.
- `tex/snarks_v4.tex` `def:cert`
  - Kind/status: definition; AUDIT.
  - Role: field-separated proximity reserve certificate.
- `tex/snarks_v4.tex` `rule:reserve`
  - Kind/status: design rule; AUDIT.
  - Role: corrected reserve rule combining entropy, quotients, lists, and MCA.
- `tex/snarks_v4.tex` `thm:ledger`
  - Kind/status: theorem; CONDITIONAL.
  - Role: ledger theorem once the cited assumptions and checks apply.
- `tex/snarks_v4.tex` `ex:toy-ledger`
  - Kind/status: example; AUDIT.
  - Role: worked instantiation for the ABF toy protocol.
- `tex/snarks_v4.tex` `prop:dyadic-hygiene`
  - Kind/status: proposition; PROVED.
  - Role: one-step dyadic dimension dither empties exact quotient cores.
- `tex/snarks_v4.tex` `lem:max-remainder`
  - Kind/status: lemma; PROVED.
  - Role: maximal-remainder hygiene for deployed dyadic rates.

## Immediate Uses For Agents

- Use `thm:integrated-package` in Paper B before changing any proof-status
  claim; it is the local summary of which lanes are proved or conjectural.
- Use Paper C's `def:cert`, `rule:reserve`, and `thm:ledger` when adding a
  script or certificate field, and cite the exact upstream theorem or
  assumption that pays for each ledger entry.
- Treat Paper D's `thm:A`, `thm:B`, `thm:main`, and `cor:grand` as conditional
  on the imported conversion until the import is separately audited.
- Treat extension-line work as a separate lane: Paper C's
  `ass:extension-mca-lift` is conjectural, while Paper D's `cor:Fvalued`
  says the missing witnesses, if made explicit, must be genuinely
  extension-valued.

## Follow-Up Checks

- Add line-number regeneration if the map is promoted into a generated index.
- Extend the map to include every verification appendix item once the appendix
  labels are stable.
- Cross-link future scripts to the exact labels they certify.
