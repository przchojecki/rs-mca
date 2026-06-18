# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, or certificate
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-06-18 - M1 nonquadratic one-coordinate lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_nonquadratic_one_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_nonquadratic_one_coordinate_lemma.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** A one-dimensional reduction for the remaining
  nonquadratic one-coordinate mixed Kummer terms. The fixed-coordinate conic
  sum becomes a Jacobi factor times the discriminant sum
  `sum_u mu(u) chi_2(Delta(u)) eta(Delta(u))`, giving the `4p` bound from
  standard Jacobi and genus-zero Kummer estimates.
- **How it is useful:** Removes all one-coordinate mixed terms from the
  two-variable normal-crossing Kummer import, so the remaining conditional
  M1 depth-two wall starts at two active coordinate characters.
- **What to do next:** Attack the degree-four two-coordinate `9p` estimate
  or find a precise normal-crossing reference for the two- and
  three-coordinate mixed terms.

### 2026-06-18 - M1 quadratic one-coordinate lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_quadratic_one_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_quadratic_one_coordinate_lemma.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / EXPERIMENTAL.
- **What is being added:** A proof-level slice lemma for the slack-two
  depth-two mixed family where the conic character is quadratic and exactly
  one coordinate character is nonprincipal. The verifier checks the exact
  quadratic-fiber identity and the `4p` open-set bound on representative
  prime/index samples.
- **How it is useful:** Removes this mixed family from the external
  two-variable Kummer import, leaving only nonquadratic one-coordinate,
  two-coordinate, and three-coordinate mixed normal-crossing estimates.
- **What to do next:** Use the same proof/import boundary to attack the
  remaining one-coordinate nonquadratic `4p` term or the degree-four
  two-coordinate `9p` term.

### 2026-06-18 - M1 mixed Kummer finite obstruction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_residue_line_roadmap.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/verify_m1_depth_two_kummer_constant_audit.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / COUNTEREXAMPLE.
- **What is being added:** A compact update to the four-point M1 roadmap and
  a verifier-backed finite obstruction to charging every mixed Kummer term by
  `4p`: for `(p,n,e,h)=(37,9,4,4)`, the three-coordinate tuple `(2,2,2,2)`
  has absolute value `185=5p`.
- **How it is useful:** Keeps PR #82 focused on the real remaining wall: the
  degree-stratified normal-crossing line/conic Kummer estimate, not a
  bookkeeping simplification of all mixed terms to the one-coordinate constant.
- **What to do next:** Prove or cite the uniform degree-stratified Kummer
  estimate, or sharpen the audit until the exact geometric input is isolated.

### 2026-06-18 - M1 depth-two elementary open-set lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_elementary_open_set_lemma.md`,
  `experimental/verify_m1_depth_two_elementary_open_set_lemma.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Isolates the proof of the elementary open-set
  correction in the slack-two depth-two Kummer ledger: the `d=0` Jacobi and
  conic-only masses each have a `p + 6 sqrt(p)` bound on the Kummer open set.
  Adds a finite verifier for the conic and coordinate-line correction terms.
- **How it is useful:** Makes the previous open-set ledger repair reviewable
  as a named lemma rather than only as scanner arithmetic, while keeping the
  genuinely mixed two-variable Kummer estimate separate.
- **What to do next:** Use this lemma as the elementary base case while
  looking for a uniform proof or citation of the remaining mixed
  normal-crossing line/conic Kummer estimate.

### 2026-06-18 - M1 depth-two Kummer open-set correction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/verify_m1_depth_two_kummer_constant_audit.py`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Repairs the slack-two depth-two Kummer ledger by
  adding the missing elementary open-set correction for the `d=0` Jacobi and
  conic-only character masses. Adds a finite exact character-sum verifier
  that exhausts representative small prime/index cases.
- **How it is useful:** Directly strengthens PR #82 by fixing the main
  conditional M1 depth-two certificate instead of merely adding another
  consequence. The mixed normal-crossing Kummer import remains isolated, but
  the elementary part of the certificate now matches the actual open set.
- **What to do next:** Look for a uniform proof or citation of the remaining
  mixed line/conic Kummer estimate, using this finite audit as a regression
  check for any proposed constants.

### 2026-06-18 - M1 slack-three genus-zero Kummer lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_slack_three_genus_zero_kummer_lemma.md`,
  `experimental/verify_m1_slack_three_genus_zero_kummer_lemma.py`,
  `experimental/m1_slack_three_first_superboundary_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Isolates the one-dimensional genus-zero Kummer
  input behind the slack-three proper-subgroup constants `6 sqrt(p)` and
  `12 sqrt(p)`, with a finite-field verifier for representative subgroup
  indices.
- **How it is useful:** Removes an unnamed import from the slack-three
  first-superboundary theorem and leaves the main remaining M1 character-sum
  dependency focused on the harder two-variable normal-crossing estimate.
- **What to do next:** Decide whether the standard `P^1` multiplicative Weil
  bound needs a formal citation before promotion, then return to the
  normal-crossing Kummer dependency or the aperiodic residue-line step.

### 2026-06-18 - M1 low-slack packet-template theorem

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_low_slack_packet_template_theorem.md`,
  `experimental/verify_m1_low_slack_packet_template.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Extracts the common low-slack residual-packet
  theorem: exact packet-lift weights, first-nonzero frontier partition,
  terminal pure-zero power-cosets, and the positive-dither depth gate. Adds a
  tiny verifier covering representative slack-two and slack-three scans.
- **How it is useful:** Gives PR #82 a unifying template layer above the
  individual slack-two and slack-three packet theorems, making clear which
  parts of future M1 work are inherited bookkeeping and which are genuinely new
  coset-image estimates.
- **What to do next:** Use this template to keep future low-slack work focused
  on nonzero frontiers and avoid recounting inherited zero-slope strata.

### 2026-06-18 - M1 residual-depth frontier shift

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_residual_depth_frontier_shift.md`,
  `experimental/verify_m1_residual_depth_frontier_shift.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Extracts the residual-depth frontier shift theorem:
  zero-slope packets at `(T,k,d)` are exactly depth-`d-1` packets at
  `(T+1,k-1,d-1)`, with the same exact-support lift gate. Adds a verifier for
  the implemented `d=2` cases, including the slack-two/slack-three conic
  interface.
- **How it is useful:** Turns the low-slack packet work into a hierarchy: the
  slack-two depth-two theorem and slack-three first-superboundary theorem are
  adjacent frontiers, not isolated computations.
- **What to do next:** Use this shift as the organizing principle for a common
  low-slack template statement, then reserve new character-sum work for the
  genuinely nonzero frontiers.

### 2026-06-18 - M1 slack-three first-superboundary theorem

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_slack_three_first_superboundary_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Extracts a standalone theorem note for the
  slack-three first-superboundary packet: the conic shape reduction, the
  one-variable split-cubic beta ledger, full-domain saturation thresholds, and
  proper-subgroup cube-coset certificates.
- **How it is useful:** Advances the roadmap's fixed low-slack template step
  beyond the slack-two depth-two PR. It shows that the next low-slack frontier
  also decomposes into explicit packet templates and coset coverage ledgers
  before the aperiodic M1 packing problem is attacked.
- **What to do next:** Keep the proper-subgroup character-sum estimates
  clearly conditional, then look for a common low-slack template statement
  unifying the slack-two depth-two and slack-three first-superboundary ledgers.

### 2026-06-18 - M1 residue-line roadmap

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONJECTURAL / AUDIT.
- **What is being added:** Adds a compact four-point working plan for the M1
  residue-line packing program: preserve PR #82 as the first low-slack packet
  theorem, remove the remaining Kummer dependency, generalize to fixed
  low-slack templates, and then attack the aperiodic packing theorem.
- **How it is useful:** Keeps the high-level direction visible without
  changing Papers A--D or overloading the theorem note with strategy text.
- **What to do next:** Revise after PR #82 review or after the next serious
  M1 result; the immediate mathematical priority remains the normal-crossing
  Kummer estimate or a broader low-slack template theorem.

### 2026-06-18 - PR #79-#81 experimental integration

- **Agent/model:** AllenGrahamHart and scottdhughes PRs, integrated by Codex.
- **Files added or changed:** `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_kummer_divisor_geometry.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/l1_arbitrary_fiber_repair.md`,
  `experimental/verify_l1_arbitrary_fiber_repair.py`,
  `experimental/a0_external_import_source_check_20260618.md`,
  `experimental/a0_import_source_probe.py`,
  `experimental/pr-triage-2026-06-18-round3.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL / COUNTEREXAMPLE.
- **What is being added:** Manual integration of PR #79's M1 depth-two
  Kummer-window material, PR #80's L1 arbitrary-fiber repair note, and PR
  #81's A0 external-import source check.  The M1 material is explicitly
  conditional on the isolated Kummer-Weil import; the L1 material repairs a
  false raw-support arbitrary-fiber route; the A0 material records source
  reachability without closing the Paper D import audit.
- **How it is useful:** Narrows three active ledgers without editing Papers
  A--D: M1 gains a sharper lift-window/saturation audit, L1 gets a corrected
  list-object target, and A0 has a reproducible source-access record for the
  universal-cap import chain.
- **What to do next:** Prove or cite the M1 `16p` Kummer estimate, decide
  whether Paper B should promote `ImgFib_U(s)` or another repaired L1 object,
  and obtain the CS25/ABF PDFs needed to close the remaining A0 checks.

### 2026-06-18 - Four-item packet label clarification

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / CLARIFICATION.
- **What is being added:** Adds a self-contained explanation of what the
  AI-packet labels (a)--(d) mean: weak-slack positive regime, finite
  Fermat-prime packet, exponential-field construction, and imported BCHKS
  quotient-locator packet.
- **How it is useful:** Makes the experimental PDF readable without knowing
  the earlier discussion, and separates imported locator material from the
  independent local Paper B divisibility-gate theorem.
- **What to do next:** If the original four-item packet is archived in the
  repo, cross-link this clarification to the exact source file or PR.

### 2026-06-18 - Streamlined imported-locator ledger

- **Agent/model:** Human-provided streamlined note, logged by Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / IMPORTED / WRAPPER / TARGET / NEW-LOCAL.
- **What is being added:** Replaces the narrower attribution note with a
  unified experimental ledger titled *Experimental Theorems and
  Imported-Locator Ledger for RS-MCA*.  The note explicitly imports the
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf quotient-locator construction,
  gives the smooth-quotient notation dictionary, records the shared locator
  identity as imported rather than new, adds a list-fiber pigeonhole wrapper,
  states a slack-two/subfield target for the Paper D route, and preserves the
  Cycle 14--18 Paper B divisibility-gate theorem.
- **How it is useful:** Streamlines promotion decisions for Papers A--D:
  locator proofs from BCHKS must be cited at theorem and proof entry points;
  repository-side contributions are limited to dictionary/wrapper/ledger
  packaging unless separately proved; Paper D gets a precise augmented-code
  and subfield-pigeonhole target; Paper B keeps the independent restricted
  resonance gate as local experimental mathematics.
- **What to do next:** When editing the main papers, add the `BCHKS25`
  bibliography entry and cite Theorems 7.1 and 1.13 exactly where the locator
  construction is used.  Audit the augmented-code rung, slope field
  (`B` versus `F`), locator-codeword distinctness, and slack normalization
  before promoting any wrapper to a theorem.  Continue scanner work on the
  `G==0` divisibility-gate branch for the Paper B resonance window.

### 2026-06-18 - Proximity-gap attribution audit

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / ATTRIBUTION.
- **What is being added:** Records that the AI-generated result (d) should be
  treated as an imported adaptation of Theorem 1.13 of
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf, *On proximity gaps for
  Reed--Solomon codes*, rather than as a new repository contribution.  Also
  records the limitations of items (a)--(c): `1/sqrt(n)` slack, only three
  Fermat primes, and exponential field size.
- **How it is useful:** Gives Papers B/D/C a conservative integration plan:
  cite the external theorem, separate it from the Crites--Stewart import, and
  audit the consumed object before any MCA, line-decoding, or protocol ledger
  claim.
- **What to do next:** Add the bibliographic entry and exact theorem
  cross-reference when the main papers are edited, then verify whether item
  (d) converts to the RS-MCA object actually needed by Paper B.

### 2026-06-18 - M1 fixed-window principal-removed Parseval L1 bound

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Replaces the crude fixed-window Fourier L1 ledger
  with a principal-removed Parseval/Cauchy-Schwarz bound. For a quotient
  window of size `R` in quotient order `N`, the nonprincipal quotient Fourier
  L1 is at most `sqrt((N-1)R(N-R))`, so after ambient lifting the active
  one-dimensional L1 is bounded by
  `(e-1)R + e ceil(sqrt((N-1)R(N-R)))`. In the complement-window case
  `R=N-1`, this specializes to the exact value `(2e-1)R`. The two-fiber and
  fixed-window Kummer certificates tensor this bound into one-, two-, and
  three-coordinate masses.
- **How it is useful:** Keeps the same conditional Kummer input but sharply
  reduces the coefficient L1 paid by fixed-window certificates. The verifier
  now checks the new integer Parseval/complement ledger; the two-fiber
  threshold improves from `332` to `108`, and the fixed-window threshold from
  `808` to `96`. The remaining failed fixed-window audit at `p=97, N=6, R=3`
  tightens from `17608` to `13378`.
- **What to do next:** Look for an analogous non-crude L1 certificate for
  larger quotient windows or replace the remaining three-coordinate Kummer
  import.

### 2026-06-18 - M1 degree-stratified Kummer ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** Refines the M1 slack-two depth-two Kummer ledger by
  charging mixed terms according to the actual active radical degree. The
  existing elementary quadratic one-coordinate `4p` term is retained, remaining
  one-coordinate mixed terms pay the degree-three constant `4p`,
  two-coordinate mixed terms pay `9p`, and only three-coordinate mixed terms
  pay the full degree-five `16p`. The quotient-window union certificate now
  computes exact ambient Fourier L1 masses for one, two, and three active
  coordinates.
- **How it is useful:** Narrows the expensive conditional import to the truly
  three-coordinate mixed Kummer terms and improves the verified M1 saturation
  thresholds without broadening the PR. The verifier checks the new active
  coordinate ledger by independent ambient enumeration in the quotient-window
  cases.
- **What to do next:** Try to replace the remaining three-coordinate
  normal-crossing import with a cited theorem or direct cohomology calculation.

### 2026-06-18 - M1 quadratic one-coordinate split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A further split of the M1 depth-two Kummer error:
  when the conic character is quadratic and exactly one coordinate character
  is nonprincipal, the term is bounded elementarily by `4p` instead of the
  imported `16p` normal-crossing estimate. The scanner/verifier now reports
  `quadratic_one_coordinate_l1_bound` and subtracts that mass from the
  remaining imported `kummer_l1_bound` in the additive raw, two-fiber, and
  fixed-window certificates.
- **How it is useful:** Narrows the conditional part of the integrated M1
  Kummer ledger without changing the quotient-window union claim. The
  remaining external import is now focused on genuinely mixed terms not
  covered by the Jacobi, conic-only, or quadratic one-coordinate arguments.
- **What to do next:** Separate the quotient-window union L1 term by
  coordinate support if possible, or prove/cite the remaining mixed
  normal-crossing Kummer estimate.

### 2026-06-18 - M1 quotient-window one-coordinate split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Extends the quadratic one-coordinate `4p` split
  from the additive fixed-window certificates to the quotient-window union
  certificate. The scanner now computes the exact one-coordinate quotient L1
  term `O_R`, including characters that are quotient-principal but nontrivial
  on the kernel, and subtracts this mass from the remaining imported mixed
  Kummer term.
- **How it is useful:** Further narrows the conditional M1 depth-two union
  certificate without changing the external Kummer assumption. The verifier
  checks the new `quotient_one_coordinate_l1_bound` against direct ambient
  quotient-Fourier enumeration.
- **What to do next:** Look for higher-coordinate elementary mixed subcases or
  prove/cite the remaining normal-crossing Kummer estimate.

### 2026-06-18 - PR #78 M1 residual-depth hierarchy

- **Agent/model:** AllenGrahamHart / Codex, integrated by Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_slack_two_depth_two_full_domain.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Integrated Allen's PR #78 M1 residual-depth
  hierarchy: the depth-two/next-slack transition theorem, terminal pure-zero
  residual-depth ledger, first-nonzero frontier partition, full-domain
  slack-two depth-two saturation verifier, and a high-index ceiling for the
  slack-two depth-two frontier.
- **How it is useful:** Separates inherited zero strata from genuinely new
  first-nonzero coefficient images in the M1 canonical-support scanner, giving
  sharper targets for Paper B's corrected MCA residue-line program.
- **What to do next:** Use the new verifier and scanner fields to attack
  proper-subgroup coset-image bounds, especially intermediate-index cases not
  decided by full-domain saturation or the coarse high-index ceiling.

### 2026-06-18 - Experimental theorem note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** PROVED / HEURISTIC / AUDIT.
- **What is being added:** A standalone LaTeX note collecting restricted
  Cycle 14--18 theorems and heuristics, including the Cycle 18
  divisibility-gate theorem with proof.
- **How it is useful:** Gives the experimental proof material a citable,
  compiled form without editing Papers A--D.
- **What to do next:** Extend the scanner to test the `G==0` gate and decide
  whether any source-valid growing-prime family has two-dimensional slope-map
  image.

### 2026-06-18 - Cycle 18 resonance slope-map reconstruction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/2026-06-18-fable-loop/audits/`
  `20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/2026-06-18-fable-loop/local_checks/`
  `20260618_cycle18_resonance_slope_symbolic.py`,
  `experimental/2026-06-18-fable-loop/README.md`,
  `experimental/agents-log.md`.
- **Status:** BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT.
- **What is being added:** A local reconstruction of Danny's Cycle 18
  `t=2,j=3` resonance reduction: `Delta` becomes a monic quadratic in
  `tau3`, the alpha component is at most linear, and the non-coprime branch
  reduces to either `Delta1==0` or the graph `tau3=-h/s`. The audit also
  records the divisibility-gate theorem: if the cleared graph polynomial
  `G=s^2 Delta0(tau1,tau2,-h/s)` is nonzero, the branch is already
  curve-sized and contributes only `O(p)` slopes.
- **How it is useful:** Sharpens the Paper B/F1 restricted toy-window wall
  from the Cycle 16 `Q==0` split to a concrete rational slope-map collapse
  question.
- **What to do next:** Extend the Cycle 17 scanner to compute the graph branch
  and projective map image on source-valid split cubics across growing primes,
  with `G==0` as the first exact gate for possible `Theta(p^2)` behavior.

### 2026-06-18 - Paper B counterexample comparison

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/paper_b_counterexample_comparison.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A theory-side comparison between recent
  experimental counterexamples and Paper B's locator-fiber, residue-line,
  extension-field, tangent-floor, and line-decoding statements.
- **How it is useful:** Identifies the raw arbitrary locator-fiber conjecture
  as needing repair, while separating route-cut counterexamples from genuine
  threats to the corrected MCA conjecture.
- **What to do next:** Review the proposed Paper B repairs, especially the
  replacement of raw `Fib_U` by a pruned/full-support arbitrary-word object.

### 2026-06-18 - Experimental summary

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/SUMMARY.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A high-level summary of the recent PR wave and the
  current contents of `experimental/`, organized by how the material advances
  the corrected MCA program.
- **How it is useful:** Gives new agents and human reviewers a map of which
  experimental notes support L1, M1, M2, F1, L2, A0/A1, protocol ledgers, and
  formalization, while keeping proof status conservative.
- **What to do next:** Use the summary as an orientation map, then verify
  individual claims from their source notes and scripts before promotion.

### 2026-06-18 - New PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #67,
  #69, #70, #71, #72, #73, #74, #75, and #77; recorded #68 and #76 as
  superseded by #77; added `experimental/pr-triage-2026-06-18.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Second open-PR triage pass covering M1, F1, L2,
  M2, L1, A1, Fable-loop, and locator-fiber cross-check contributions.
- **How it is useful:** Banks useful experimental notes, verifiers, scanners,
  and audit provenance while preserving the rule that main papers remain
  unchanged and new material stays in `experimental/`.
- **What to do next:** Run full verifier coverage, review mathematical claims
  before promotion, and close the source PRs as manually integrated or
  superseded once this commit is pushed.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, certificates, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
