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
- **What is being added:** State the claim, note, scan, script, proof,
  heuristic, or computation
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-07-10 - BC moving-root toy verification

- **Agent/model:** Grok.
- **Files added or changed:** `experimental/notes/thresholds/bc_moving_root.md`, `experimental/data/certificates/bc-moving-root/bc_moving_root.json`, `experimental/scripts/verify_bc_moving_root.py`, `experimental/scripts/verify_bc_moving_root_check.py`, `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** Toy incidence verification of thm:bc-moving-root and cor:bc-one-pencil integers.
- **How it is useful:** Independent confirmation of the proved one-parameter BC pencil bound.
- **What to do next:** Higher-dimensional BC chart audit remains open.

### 2026-07-09 - Asymptotic RS MCA closed-ledger proof paper

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/asymptotic_rs_mca.tex`,
  `experimental/asymptotic_rs_mca.pdf`, `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL.
- **What is being added:** A compact amsart paper titled `Asymptotic RS MCA`
  consolidating the moduli-ledger drafts with the v13 raw and Grande Finale
  ledgers.  It states the closed paid ledger package explicitly, defines the
  cells `(C1)--(C9)`, cites the existing ledger results for their payments, and
  proves the asymptotic MCA frontier via the Sidon/Fourier cut, BSG, quasicube
  difference growth, primitive Q, Q-to-SP, and the identity-prefix lower side.
- **How it is useful:** This is the current compact prize-facing proof route
  for the asymptotic RS-MCA threshold: once the imported closed-ledger package
  is accepted from `cap25_cap_v13_raw.tex`, `grande_finale.tex`, and the
  moduli-ledger notes, no additional entropy-Freiman or rank-derivative
  theorem is needed for primitive Q.
- **What to do next:** Audit the cited closed-ledger package line by line
  against v13 raw and Grande Finale labels, then decide whether to promote this
  paper or merge its theorem/proof into the next main Paper D/towards-prize
  revision.

### 2026-07-09 - Reviewed PR integration for entropy-inverse, row-sharp Q, BC, and Route-D packets

- **Agent/model:** Holm Buar via PRs #414-#418, #420-#422, and #427-#430;
  AllenGrahamHart via PR #419; Scott Hughes via selected material from PR #423;
  DannyExperiments via PRs #424 and #426; Vadim Avdeev via PR #425; Codex for
  review, selective integration, and log consolidation.
- **Files added or changed:** Added Q/threshold notes under
  `experimental/notes/thresholds/`; a BC note under
  `experimental/notes/bc_near_pencil_chart_reduction.md`; a Lean audit under
  `experimental/notes/audits/lean_grande_finale_correspondence_audit.md`; L1
  stabilization material under `experimental/notes/l1/`; data and certificates
  under `experimental/data/`; verifier and audit scripts under
  `experimental/scripts/`; updated `experimental/scripts/README.md` with the
  singleton top-seam verifier commands.  PR #423 was deliberately reduced to its
  canonical status note and the high-signal packets v25, v45, v46, v48, v49,
  v51, v53, and v54 rather than importing the full v1-v54 archive.
- **Status:** PROVED / CONDITIONAL / EXPERIMENTAL / AUDIT / COUNTEREXAMPLE.
- **What is being added:** Integrated a batch of experimental packets around the
  current v13/Grande Finale bottlenecks: signed-`e_m` and masked participation
  ratio reformulations, the lift-class cost-model refutation, entropy-inverse
  toy dichotomy and missing-cell hunts, the `F_p`-span cell and its codimension,
  surjection, connectivity, and residual-control follow-ups, a row-sharp Q
  singleton top-seam Route-D compiler, a Q moment-floor route cut, the M31
  Chebyshev fixed-remainder floor audit, the BC near-pencil chart reduction,
  an L1 k3 record-stabilization extension, and a textual correspondence audit
  for the Grande Finale Lean package.
- **How it is useful:** The batch sharpens the proof map without claiming a
  deployed adjacent safe row.  The entropy-inverse material identifies and
  measures an `F_p`-span obstruction cell and distinguishes theorem-level toy
  facts from measured evidence.  The Q and Route-D packets clarify which
  shortcut payment routes are dead, conditional, or still open.  The BC packet
  reduces one saturated-chart family to a split-in-subspace residual tied to
  the existing Q/BC frontier.  The Lean audit records concrete docstring/label
  drift to fix before relying on the formalization as a paper map.
- **What to do next:** Do not promote these packets into Paper D or
  `grande_finale.tex` as theorem rows without separate proof review.  The next
  useful steps are: prove the row-sharp Q max-fiber bound or a precise residual
  cell theorem; close the BC chart decomposition beyond the near-pencil family;
  attack Scott's remaining Route-D wall `|T| <= H2`; fix the documented Lean
  label drift; and run selected verifier scripts only when their cost is
  acceptable for the local environment.

### 2026-07-08 - Grande Finale Lean package normalization

- **Agent/model:** Maintainer-added Lean files integrated by Codex.
- **Files added or changed:** `experimental/lean/grande_finale/GrandeFinale.lean`;
  `experimental/lean/grande_finale/GrandeFinale/BC.lean`;
  `experimental/lean/grande_finale/GrandeFinale/SP.lean`;
  `experimental/lean/grande_finale/GrandeFinale/Frontier.lean`;
  `experimental/lean/grande_finale/GrandeFinale/QFourierTao.lean`;
  `experimental/lean/grande_finale/GrandeFinale/QEntropyInverse.lean`;
  `experimental/lean/grande_finale/GrandeFinale/QPrimitiveCollision.lean`;
  `experimental/lean/grande_finale/README.md`;
  `experimental/lean/grande_finale/FORMALIZATION_SUMMARY.md`;
  `experimental/lean/grande_finale/lakefile.toml`;
  `experimental/lean/grande_finale/lake-manifest.json`.
- **Status:** FORMALIZATION / AUDIT.
- **What is being added:** Normalized the new Grande Finale Lean files away
  from placeholder `RequestProject` module names.  The package root is now
  `GrandeFinale`, with submodules under `GrandeFinale/`; package docs summarize
  the formalized kernels around Q, BC, SP, the frontier ledger, and
  log-moment/Fourier reductions.
- **How it is useful:** Gives the current `grande_finale.tex` program a cleaner
  Lean workbench focused on the real bottleneck: Q, namely the primitive
  entropic inverse theorem / row-sharp prefix-fiber bound.  The package records
  theorem-level reductions and deterministic atoms; it does not prove the full
  adjacent safe rows.
- **What to do next:** Build only in a controlled Mathlib-enabled environment.
  Audit correspondence between the Lean declaration docstrings and the labels
  in `experimental/grande_finale.tex`, then extend the formalization toward the
  Q inverse theorem and finite row-sharp Q constants.

### 2026-07-08 - Entropic inverse route and asymptotic closure in Grande Finale

- **Agent/model:** Maintainer-added TeX drafts integrated by Codex.
- **Files added or changed:** `experimental/grande_finale.tex`,
  `experimental/grande_finale.pdf`, `experimental/agents-log.md`.
- **Status:** CONDITIONAL / PROVED / AUDIT.
- **What is being added:** Integrated the standalone primitive entropic inverse
  theorem for Vandermonde slice sums as the clean additive-combinatorics atom
  behind Q.  Added the conditional asymptotic RS--MCA closure theorem showing
  that this inverse theorem, together with the printed first-match ledger
  hypotheses, gives the entropy--subfield threshold formula.  Also added a
  Fourier-flat sufficient condition for Q in large-characteristic leaves.
- **How it is useful:** This separates the remaining Q proof from RS-MCA
  language and makes the asymptotic prize route precise: prove the primitive
  inverse theorem, or find a new algebraic obstruction cell.  The Fourier
  theorem gives a theorem-level route in leaves where the explicit character
  sum error fits the frontier ledger.
- **What to do next:** Prove or refute the primitive entropic inverse theorem,
  including the entropy BSG/PFR or free-energy branch and the slice derivative
  back to Vandermonde rank defect.  For finite deployed rows, do not use the
  asymptotic theorem unless all constants fit the printed adjacent margins.

### 2026-07-08 - Reviewed PR integration for Q, BC, L1, and Lean packets

- **Agent/model:** DannyExperiments/Gia via PRs #389, #409, #411, and #413;
  Holm Buar/Claude Fable 5 via PRs #392, #393, #395, #396, #399, #400,
  #403, #407, #408, #410, and #412; AllenGrahamHart/Claude Opus 4.8 via PRs
  #404, #405, and #406; Scott Hughes via PRs #390, #391, #398, #401, and
  #402; Vadim Avdeev via PR #397; Codex for review, selective integration,
  deconflicting overlapping Lean updates, and logging.
- **Files added or changed:** Added threshold/Q/BC audit notes under
  `experimental/notes/thresholds/`; L1 notes under `experimental/notes/l1/`;
  route-cut notes under `experimental/notes/roadmaps/`; certificate/data
  packets under `experimental/data/`; verifier/evidence scripts under
  `experimental/scripts/`; Lean packages and modules under
  `experimental/lean/grande_finale/`, `experimental/lean/l1_threshold_ledger/`,
  and `experimental/lean/powersum_rigidity/`; updated
  `experimental/grande_finale.tex` with a mass-aware logmoment caveat.
- **Status:** PROVED / CONDITIONAL / EXPERIMENTAL / AUDIT / COUNTEREXAMPLE.
- **What is being added:** Integrated the reviewed PR packets without importing
  their individual log edits.  The batch adds Q route-cut audits
  (`p^{w/2}` concentration floor, signed-`e_m` masked residual audit,
  logmoment mass-awareness, moment-floor reconciliation, popular-fiber probe
  confound), row-sharp Q atom reductions and calibration, an independent replay
  of the four v13 adjacent pairs, a toy complete adjacent list-staircase
  certificate, BC L4 chart/second-moment reductions, L1 k3 and m=19 packets,
  the x4b moment-column subproblem packet, and Lean/finite-data certificates
  for Grande Finale composite-prefix descent and the L1 W3 collapse-edge
  mechanism.  The overlapping L1 Lean PRs were combined so the compact gate now
  includes origin summary, structural wrapper, graph mechanism, origin-dot, and
  origin-arithmetic checks.
- **How it is useful:** The Q material narrows the current bottleneck by ruling
  out several shortcut proof routes and by identifying the masked residual
  signed-prefix atom as the right target.  The v13 adjacent replay and toy
  staircase packet improve the certificate-scanner workflow.  The BC/L1 packets
  provide scoped reductions and counterexamples that help prevent overclaiming.
  The Lean additions improve formalization coverage for two high-priority
  tracks, but remain partial and do not prove Q or the adjacent safe rows.
- **What to do next:** Do not promote any of these packets into Paper D without
  a separate audit.  Run the lightweight verifiers individually before citing a
  certificate; run Lake only in a controlled Mathlib-enabled environment.  The
  open mathematical task remains row-sharp Q with finite constants, plus the
  finite BC chart-decomposition audit needed for the adjacent deployed rows.

### 2026-07-07 - Grande finale logarithmic-moment Q route

- **Agent/model:** Maintainer-added Q/Tao notes integrated by Codex.
- **Files added or changed:** `experimental/grande_finale.tex`,
  `experimental/grande_finale.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONJECTURAL / AUDIT.
- **What is being added:** Integrated the theorem-level equivalence between
  primitive logarithmic collision moments and primitive asymptotic Q, under
  the condition `w log |B| / r = o(n)`.  The paper now isolates the remaining
  additive-combinatorics input as an entropy-scale inverse theorem for
  primitive moment-curve subset sums, with a Vandermonde-rank closure showing
  why a low-rank output would finish asymptotic Q after paid cells are removed.
- **How it is useful:** This sharpens the asymptotic route: Q is no longer a
  vague max-fiber target but is equivalent to a logarithmic moment theorem.
  It also clarifies that standard polynomial-scale inverse Littlewood-Offord
  and Green-Ruzsa/Freiman results are templates, not black-box proofs at the
  exponential fiber scale.
- **What to do next:** Prove or refute the entropy-scale inverse theorem in
  `prob:entropy-inverse-q`.  For finite deployed adjacent rows, do not use the
  asymptotic `e^{o(n)}` statement as a certificate; the row still needs
  audited constants fitting the printed margins and the BC chart-decomposition
  audit.

### 2026-07-07 - Grande finale Q-attempt promotion and Lean cleanup

- **Agent/model:** Maintainer-added `grande_finale_q_attempt` reviewed and
  integrated by Codex.
- **Files added or changed:** `experimental/grande_finale.tex`;
  `experimental/grande_finale.pdf`; `experimental/lean/grande_finale/`;
  deleted `experimental/lean-certificates/`; updated `AGENTS.md` and
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Promoted the Q-attempt version to the canonical
  `experimental/grande_finale.tex`, preserving the composite-prefix
  `gcd(e,N)` multiplicity repair.  The note now records that SP is downstream
  from max-fiber Q, primitive one-parameter BC pencils are paid by the
  moving-root theorem, and the adjacent safe rows remain open at row-sharp Q
  plus the finite BC chart-decomposition audit.  The new
  `experimental/lean/grande_finale/` package was normalized under its Lake
  module layout and documented as a partial formalization.
- **How it is useful:** This makes the final-resolution target sharper:
  proving Q is now the main bottleneck, while BC/SP are either paid in the
  one-parameter case or downstream of Q subject to the finite chart audit.  The
  guide now also states that all Lean packages belong under `experimental/lean/`.
- **What to do next:** Attack `def:q-row-atom` / `prob:row-sharp-q` in
  `experimental/grande_finale.tex` and the corresponding v13 raw source
  ledger.  Build `experimental/lean/grande_finale/` in a Mathlib-enabled
  environment before calling any declaration Lean-certified, and add missing
  formalization for the row-sharp Q atom theorem and finite BC chart audit.

### 2026-07-07 - Reviewed PR integration for v13 adjacent ledgers

- **Agent/model:** Scott Hughes via PRs #362, #367, #377, #381, and #387;
  Holm Buar via PRs #363, #364, #365, #366, #368, #378, #379, #382, #383,
  and #384; Vadim Avdeev via PRs #385 and #386; Danny/Gia via PRs #376,
  #380, and #388; LegaSage/Ken via PRs #371--#375; Latif Kasuli via PR #369;
  Manifold Control via PR #370; Codex for review, selective integration, and
  site/log updates.
- **Files added or changed:** Added reviewed packets under
  `experimental/data/certificates/`, `experimental/notes/thresholds/`,
  `experimental/notes/l1/`, `experimental/notes/m1/`,
  `experimental/notes/certificate_scanner/`, `experimental/notes/roadmaps/`,
  `experimental/lean/`, and `experimental/scripts/`; repaired
  `experimental/grande_finale.tex` and
  `experimental/grande_finale_work/q_next_section.tex`; updated
  `experimental/scripts/README.md`; added #381 near-capacity cap examples to
  `site/data/rate-leaderboards.json` and the embedded site fallback.
- **Status:** PROVED / CONDITIONAL / EXPERIMENTAL / AUDIT / COUNTEREXAMPLE,
  depending on the individual packet.  No packet is promoted to Paper D here.
- **What is being added:** Banks a broad reviewed PR wave: Q first-match
  leakage and composite-multiplicity repairs; a conditional KB-MCA `A=1116048`
  first-match ledger; Gamma-r and saturated-BC budget audits; M31/KB Q-rung
  route cuts; BC lower-floor Lean formalization; L1 bounded-excess, T=7,
  min-`j`, W3 collapse-edge, ell=19, and dim-Syz refutation packets; M1/CAPG
  finite-testability, split-pencil, adjacent-pair, shift-pair, Q/R1, and
  nonconsecutive-window packets; multi-rate LD_sw adjacent pins and board cap
  examples; small standalone Lean toy certificates were reviewed later and
  removed as redundant with stronger Lean tracks.
- **How it is useful:** Turns the v13 adjacent program into a much more
  explicit proof ledger.  The unsafe/lower rows and arithmetic margins are
  better audited; several false or overstrong L1/Q routes are cut; and the
  remaining safe-side work is more sharply named as primitive Q/max-fiber,
  saturated BC/split-pencil, and finite first-match residual payment with
  exact constants.  The site now exposes Scott's near-capacity Paper D cap
  examples as public leaderboard rows while keeping them separate from exact
  threshold claims.
- **What to do next:** Do not run the heavier verifiers casually.  For paper
  promotion, replay the relevant certificates independently, then distill only
  theorem-level material into the next CAP25 draft.  The live finite target is
  still the adjacent safe ledger at the v13 rows, especially KB-MCA
  `A=1116048`, with every residual branch paid by theorem, exact certificate,
  or explicitly labelled conjectural input.  Draft PR #355 remains unintegrated.

### 2026-07-06 - PRs #356-#361 experimental integration

- **Agent/model:** Holm Buar via PRs #358, #359, and #361; LegaSage via
  PRs #356 and #357; Scott Hughes via PR #360; Codex for static review,
  cleanup, and integration.
- **Files added or changed:** `experimental/data/certificates/annulus-corrected-cluster/`;
  `experimental/data/certificates/finite-reachability-map/`;
  `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_rung_audit_v1.json`;
  `experimental/data/certificates/l1-e3-law/`;
  `experimental/data/certificates/l1-ell19/`;
  `experimental/notes/m1/annulus_corrected_cluster.md`;
  `experimental/notes/m1/finite_reachability_map.md`;
  `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md`;
  `experimental/notes/l1/l1_e3_*.md`;
  `experimental/notes/l1/l1_ell19_attainment.md`;
  `experimental/notes/roadmaps/l1_e3_*.md`;
  `experimental/lean/l1_e3_level_set/`;
  `experimental/l1_e3_obligation*.md`;
  `experimental/scripts/verify_annulus_corrected_cluster*.py`;
  `experimental/scripts/verify_finite_reachability_map*.py`;
  `experimental/scripts/verify_kb_mca_conjq_rung_audit.py`;
  `experimental/scripts/verify_l1_e3_*.sage`;
  `experimental/scripts/verify_l1_e3_flint_crosscheck.py`;
  `experimental/scripts/verify_l1_e3_law_refuted.py`;
  `experimental/scripts/verify_l1_ell19_attainment.py`;
  and supporting Sage/GP/M2/Python scripts.
- **Status:** AUDIT / EXPERIMENTAL / COUNTEREXAMPLE / FORMALIZATION-SKELETON.
- **What is being added:** Banks five additive PR packets and a sanitized L1
  E3 proof-program packet.  The M1 packets add finite-reachability and
  annulus bounded-cluster insufficiency scope maps.  The threshold packet
  audits the KB-MCA `a0+1` divisor-lattice rungs and leaves the primitive
  `conj:Q` fiber as the named residual.  The L1 packets refute the proposed
  `E_3<=ell` law at `T>=5`, add an `ell=19` attainment witness, and reduce
  the sharper `E_3<=ell-2` ceiling to the `dim Syz<=K` rank crux with CAS
  cross-checks and a Lean skeleton containing an explicit `sorry`.
- **How it is useful:** Clarifies the current proof boundary for the v13 raw
  adjacent program: nonprimitive quotient rungs are ledger-audited for the
  KB-MCA row, while the finite max-fiber/L1 problem is narrowed to a concrete
  cyclotomic level-set rank statement.  The M1 maps mark which finite checks
  are only scope evidence and which growing-dimensional aperiodic branches
  remain live.
- **What to do next:** Do not promote these packets into Paper D without
  independent replay.  The expensive KB-MCA rung verifier should be run only
  intentionally.  The next proof work is the primitive `conj:Q` max-fiber
  bound, the L1 `dim Syz<=K` theorem for `K>=3`, and a growing-dimensional
  M1 aperiodic upper ledger.  Draft PR #355 was not integrated because it
  overwrites existing M1 triage paths and carries a large route-cut evidence
  archive that should be split or summarized first.

### 2026-07-06 - Threshold and F1 audit PR integration

- **Agent/model:** DannyExperiments via PRs #352 and #354; Latif Kasuli via
  draft PR #353; Codex for review and integration.
- **Files added or changed:** `experimental/notes/thresholds/cap25_v13_qfin_primitive_wall_synthesis.md`;
  `experimental/notes/thresholds/cap25_v13_near_rational_support_mismatch_audit.md`;
  `experimental/notes/frontier-adjacent/f1_effective_slack_translation_v1.md`;
  `experimental/notes/frontier-adjacent/f1_simple_pole_tge2_obstruction_v1.md`;
  `experimental/data/certificates/frontier-adjacent/f1_effective_slack_translation_v1.json`;
  `experimental/data/certificates/frontier-adjacent/f1_simple_pole_tge2_obstruction_v1.json`;
  `experimental/scripts/verify_f1_effective_slack_translation.py`;
  `experimental/scripts/verify_f1_simple_pole_tge2_obstruction.py`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL / PROVED-FOR-NAMED-PENCIL.
- **What is being added:** Two CAP25 v13 threshold notes and two F1
  frontier-adjacent packets.  The threshold notes isolate the live KB-MCA
  Q-fin primitive max-orbit wall and repair a near-rational support-mismatch
  overclaim.  The F1 packets translate deployed adjacent rows to the toy
  slack variable `t=a-k` and prove that the named simple-pole pencil has no
  `t>=2` bad slopes by a degree/root-count obstruction.
- **How it is useful:** Narrows the safe-side proof obligations without
  promoting them to solved results: the current KB-MCA adjacent row remains
  open, the near-rational branch needs an explicit support-wise first-match
  payment, and the F1 `t=1` toy growth branch should not be read as deployed
  adjacent-row evidence.
- **What to do next:** Audit constants against the v13 raw moved-frontier
  checker, repair the near-rational inference in the raw/compact manuscripts,
  and search for genuinely extension-valued `t>=2` pencils not killed by the
  simple-pole obstruction.

### 2026-07-06 - CAP25 v13 raw compact Lean integration

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/lean/cap25_cap_v13_raw_compact/`;
  `experimental/agents-log.md`.
- **Status:** FORMALIZATION / AUDIT.
- **What is being added:** A compact Lean package for the CAP25 v13 raw/compact
  frontier, with arithmetic unsafe-edge certificates, the identity-prefix floor,
  the simple-pole MCA conversion, deployed unsafe list/MCA rows, BC base-field
  census floors, and SP shift-pair to prefix-collision reductions.  The package
  was normalized away from placeholder `RequestProject` module names.
- **How it is useful:** Gives the v13 program a concrete Lean workbench for the
  unconditional unsafe side and structural residual-input machinery.
- **What to do next:** Run `lake build` only when a contributor intentionally
  audits this package locally.  The safe-side adjacent threshold certificates
  remain open and still require exact upper-ledger work for `Q`, `BC`, and
  `SP`; any TeX/Lean correspondence should be maintained by direct statement
  audit, not bulk source scanning.

### 2026-07-06 - CAP25 v13 raw Lean blueprint

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/lean/lean-blueprint.json`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / FORMALIZATION PLAN.
- **What is being added:** A machine-readable Lean formalization blueprint for
  `experimental/cap25_cap_v13_raw.tex`, organized as theorem, lemma,
  proposition, corollary, definition, remark, computation, and final-target
  nodes with dependency edges and reverse-support links.  The first pass keeps
  all `lean_file` and `lean_name` slots blank by design.
- **How it is useful:** Gives Lean agents a dependency graph for formalizing the
  v13 raw program, with special targets for Q prefix flatness, BC split-pencil
  census, SP primitive shift-pair control, finite adjacent deployed ledgers, and
  full RS-MCA resolution.
- **What to do next:** Assign nodes to concrete Lean files only after choosing
  module boundaries.  Treat syntactic dependencies and computation-support
  edges as an orientation map, then audit each proof dependency before
  mechanization.

### 2026-07-06 - Grande finale proof-plan note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/grande_finale.tex`;
  `experimental/grande_finale.pdf`; `experimental/agents-log.md`.
- **Status:** PROVED REDUCTIONS / CONJECTURAL / PROOF STRATEGY / AUDIT.
- **What is being added:** A standalone `amsart` note that isolates the final
  RS-MCA proof obligations and proves the reusable reductions currently needed
  for that attempt: identity-prefix witness exactness, prefix-collision
  rigidity, the exact second-moment ledger, pole-line transport from prefix
  fibers to support-wise MCA bad slopes, the fiber-to-slope averaging theorem
  that produces many distinct MCA-bad slopes from a large prefix fiber,
  quotient pullback for shift pairs, coefficient-scale quotient extraction for
  shift pairs,
  the primitive `L^2` ledger, twist-orbit symmetry, slope elimination, the
  interpolation-lattice split-pencil reduction, the fact that Q is the boundary
  split-pencil profile, and the base-field floor that any interior BC census
  must include.  It also proves the head-depth prefix-flatness theorem in the
  Weil range, including the solved KoalaBear head-depth part of Q.  It also
  adds the exponential aperiodic-floor theorem below the entropy-subfield
  envelope, ruling out the old unnormalized polynomial aperiodic-band target.
  A Fourier-audit proposition now explains why individual square-root
  character estimates cannot close Q by triangle inequality.  A rank-one
  pole-line floor shows the same base-field normalization is forced in the
  line/support census and is genuinely extension-valued.  The finite packet
  audit now explicitly separates historical adjacent-pair fields from the
  active moved MCA pairs and records the Mersenne-31 `c=2048` quiet watch item.
  The latest update also integrates the near-rational lattice dichotomy:
  small first shifted-degree words are exactly classified, and after the
  common-proximity paid branch is removed, the BC residual starts only in the
  balanced two-generator split-pencil core.  A deficiency-one split-test
  eliminant theorem now pays bounded SPI charts unless the chart is
  identically split or identically rank-deficient, in which case it is named
  as a residual rather than hidden in the BC estimate.  The note now also
  proves the two broad safe anchors directly: the self-contained deep-regime
  MCA bound below one third of minimum distance, and the reduction of MCA to
  CA plus explicit tangent slopes below half distance.  Subfield confinement
  is now included as a theorem too: any bad slope of a \(\mathbb B\)-valued
  pair over an extension row lies in \(\mathbb B\), so target-level extension
  failures must be genuinely extension-valued after common scalar removal.
  The BC floor has also been strengthened from a raw agreement-census lower
  bound to an interior split-pencil theorem: under the printed degree
  inequalities, the constructed \(\mathbb B\)-valued received word has
  minimal shifted degree exactly \(d_1\), so the base-field-normalized floor
  occurs in a genuine interior profile rather than only at the Q boundary.
  The Q section now includes a quantitative moment criterion:
  \(\log_2\Gamma_r+w\log_2|\mathbb B|\le r\Delta\) is the finite adjacent
  high-moment gate for proving a max-fiber ratio \(2^\Delta\), explaining why
  low fixed moments cannot settle the deployed one-step rows.  The lower-side
  MCA route is now self-contained as well: a quantitative simple-pole
  list-to-MCA theorem converts any \(L\)-word \(C^+\) list into at least
  \(\lceil L(q-n)/(q-n+k(L-1))\rceil\) bad finite slopes, matching the moved
  v13 raw MCA packet formula.
  The finite-adjacent section now packages the row-packet consequences as
  propositions: the four active rows have exact unsafe lower certificates at
  their printed \(a_0\)'s, the same lower route stops at \(a_0+1\), and the
  dyadic rung audit is only a lower-floor veto rather than a quotient-image
  upper bound.  The note now also includes a first-match upper-ledger
  definition and lemma, making the safe-side finite target precise: a
  row-specific certificate must cover every bad slope by ordered paid/residual
  cells and prove the sum of certified cell bounds is at most \(B^*\).  The
  integer-budget convention is now also proved explicitly, so all finite safe
  and unsafe statements reduce to comparisons with
  \(B^*=\lfloor\varepsilon^*Q\rfloor\).
  A finite safe-anchor gap proposition now records that the broad deep,
  half-distance, half-Johnson, and conditional BCHKS anchors miss the active
  adjacent agreements by hundreds of thousands of positions, so the final
  certificate must use row-specific first-match upper ledgers or a genuinely
  stronger theorem.
  It also proves that composite prefix directions descend
  exactly to quotient scales, justifying the divisor-lattice separation before
  primitive Q/SP flatness is attempted.  It now also proves twist-orbit moment
  amplification: a heavy primitive prefix fiber contributes an entire orbit to
  the high-moment ledger, while stabilized heavy values are quotient/composite
  objects.  The SP section adds a top-stratum quotient sieve showing that every
  non-primitive top-stratum shift pair descends to a quotient constant-shift
  cell, leaving only coefficient-primitive constant shifts in that residual.
  The BC section adds a distinct-slope extension-valued rank-one floor, so the
  base-field floor cannot be dismissed as a support-count artifact or a
  purely \(\mathbb B\)-rational phenomenon.
  The note now defines the closed-grid
  support-wise CA/MCA events directly, proves the CA-to-MCA comparison, and
  records the agreement-threshold monotonicity needed to interpret adjacent
  certificates as radius-threshold statements.  The note also records the finite-adjacent artifact status:
  active MCA lower-route values, the non-firing dyadic rung audit, and the
  extension-cell degree ceilings, with explicit warnings that these are not
  safe certificates.  The latest update turns the extension-cell ceilings into
  a formal full-extension target proposition: in the active packet grammar,
  any genuinely full-orbit extension chart fitting the adjacent margin must be
  zero-dimensional, with degree at most `4807520`, `4226236`, `9`, and `8` in
  the four deployed rows.  This is an exact arithmetic target for the missing
  branch, not a payment of that branch.  The Q section now also includes the
  exact `F_17^*`, `m=9`, `w=1` route cut showing raw mode-at-null is false
  (`N_9(0)=672`, `N_9(s)=673` for `s != 0`), so the finite Q target is
  primitive max-orbit flatness or exchange-compression after quotient routing.
  The BC/SPI part now also proves that an identically split deficiency-one
  chart is tangent-borne: the split-annihilator dictionary first turns a fixed
  split locator into a codeword-plus-error decomposition, constant-divisor
  rigidity makes the locator fixed, and the line contributes only tangent
  ratios rather than a new aperiodic split-pencil cell.  The safe-anchor
  section now records the exact high-agreement tangent paid cell as well:
  when \(A=n-r\) and \(3r\le n-k\), the maximum CA/MCA bad-slope numerator is
  exactly `r+1 = n-A+1`.  The finite adjacent closure theorem now uses a
  row-object numerator \(B(a)\), separating MCA bad-slope numerators from list
  numerators, so the four-row statement no longer silently treats list rows as
  MCA rows.
  The remaining inputs are Q prefix flatness, BC
  base-field-normalized interior split-pencil census, SP primitive shift-pair
  control, and the finite adjacent certificate program at the four deployed
  v13 raw rows.
- **How it is useful:** This gives agents a compact, publishable-style target
  document for the final resolution attempt without copying the long v13 raw
  manuscript.  It records which reductions are now theorem-level, what remains
  conjectural, which part of Q is already solved by direct Weil bounds, and
  what computations would pin the finite deployed thresholds.
- **What to do next:** Fill in Q, BC, and SP proof packets one by one, starting
  with exact rung audits and KoalaBear MCA at `a0+1 = 1116048`.  The next Q
  work must attack frontier-depth maximum fibers directly, not by a uniform
  per-character square-root bound.  Do not promote the conditional closure
  theorem until the safe upper ledgers are replayed and audited.

### 2026-07-06 - v13 raw final-form roadmap alignment

- **Agent/model:** Codex.
- **Files added or changed:** `towards-prize.md`;
  `experimental/cap25_v13_missing_inputs_strategy.md`;
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / CONJECTURAL / AUDIT.
- **What is being added:** The roadmap now records the v13 raw final-form
  update: the entropy-subfield envelope, the four exact deployed unsafe edges,
  the Q/BC/SP safe-side input split, the adjacent finite target pairs, and the
  explicit falsifier shape.  The missing-input strategy now separates proved
  anchors from the still-conjectural finite adjacent safe certificates.
- **How it is useful:** This aligns the human-facing roadmap with the v13 raw
  package without promoting it into Paper D.  It tells agents
  that the useful next work is exact safe-side certification at `a0+1`, or a
  primitive prefix-fiber / split-pencil counterexample that becomes a new floor.
- **What to do next:** Keep Paper D v12 as the paper authority until the v13 raw
  material is promoted and audited.  Build exact Q, BC, and
  SP certificates with constants fitting the `22.2 / 22.0 / 3.3 / 3.1` bit
  adjacent margins.

### 2026-07-06 - CAP25 v13 raw frontier status

- **Agent/model:** Maintainer-added v13 raw manuscript summarized and aligned
  by Codex.
- **Files added or changed:** `experimental/cap25_cap_v13_raw.tex`;
  `experimental/cap25_v13_missing_inputs_strategy.md`; `agents.md`;
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / CONDITIONAL / AUDIT.
- **What is being added:** `cap25_cap_v13_raw.tex` is the extended
  raw-working master.  Its TLDR is: the unsafe side is exact and elementary via identity-prefix
  floors plus flexible simple-pole conversion; the generic safe anchors are
  deep-regime MCA, MCA-from-CA below half distance, and one isolated
  half-distance CA import; the near-capacity safe side is reduced to exactly
  three residual inputs Q, BC, and SP.
- **How it is useful:** This records the current experimental final-resolution
  target.  The moved finite adjacent predictions are KoalaBear MCA
  `1116047 -> 1116048`, KoalaBear list `1116046 -> 1116047`,
  Mersenne-31 MCA `1116023 -> 1116024`, and Mersenne-31 list
  `1116022 -> 1116023`.  Polynomial or `e^{o(n)}` Q/BC/SP would settle the
  asymptotic frontier with logarithmic reserve; exact constants fitting the
  printed `22.2 / 22.0 / 3.3 / 3.1` bit margins are needed for the finite
  adjacent pairs.
- **What to do next:** Do not promote v13 raw into Paper D until the
  safe upper ledgers are proved, replayed, and audited.  Work should focus on
  finite Q maximum-fiber certificates, finite BC split-pencil census
  certificates, finite SP primitive shift-pair certificates, and the matching
  certificate scanner rows.  The strategy note now maps the old `(A)` aperiodic
  umbrella to the current BC/SP inputs and should be kept compatible with the
  v13 raw source names.  This entry supersedes earlier log entries that
  mention `experimental/cap25_v13_experimental.tex` or the older `1116043`
  KoalaBear MCA experimental edge.

### 2026-07-06 - Experimental PR packet batch 281, 310, 322-351

- **Agent/model:** DannyExperiments, Scott Hughes, LegaSage, Vadim Avdeev,
  holmbuar, and Latif Kasuli; integrated by Codex.
- **Files added or changed:** Experimental notes, JSON packets, verifier
  scripts, optional GPU/provenance scripts, and Lean scaffolds under
  `experimental/data/`, `experimental/notes/`, `experimental/scripts/`, and
  `experimental/lean/`.  The PR-local `experimental/agents-log.md` edits were
  not merged directly; this entry is the combined project log.
- **Status:** EXPERIMENTAL / AUDIT / CONDITIONAL / COUNTEREXAMPLE /
  FORMALIZATION.
- **What is being added:** A broad integration batch from PRs `#281`, `#310`,
  and `#322`-`#351`: CAP25 v13 threshold route cuts, identity/frontier-adjacent
  row packets, KoalaBear adjacent-ledger checks, M1 a=327 `mu_8` triage,
  M1/M2/L1 local-limit packets, finite staircase rows, mode-at-null and
  prefix-collision ledgers, optional GPU engines with provenance checks, and
  Lean staircase/towards-prize arithmetic anchors.
- **How it is useful:** The batch strengthens the experimental v13 raw
  final-resolution spine without promoting it to Paper-D authority: it gives
  more exact packet material for the unsafe/safe adjacent staircase program,
  records several route cuts and counterexamples, and supplies verifier-facing
  artifacts for future audits.
- **What to do next:** Re-run individual verifier scripts before citing any
  packet.  Do not run the optional GPU engines or Lean/Lake builds unless a
  maintainer explicitly asks.  Keep the Scott `a=327, mu_8` packet as route-cut
  evidence, not a board-ready MCA/list claim, and keep all v13 raw adjacent
  rows experimental until the safe upper ledgers are printed and replayed.

### 2026-07-05 - Proximity Prize status memo for v12/v13 raw picture

- **Agent/model:** Maintainer-added status memo reviewed and integrated by
  Codex.
- **Files added or changed:** `experimental/rs_mca_proximity_prize_status.md`;
  `readme.md`; `agents.md`; `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / CONJECTURAL / AUDIT.
- **What is being added:** A committee-facing status draft summarizing the
  current CAP25 v12/v13 raw picture: the entropy-subfield-envelope thesis,
  exact unsafe-side certificates near the deployed frontier, proved
  high-agreement/safe-side components, and the remaining `(Q)` prefix-fiber /
  split-pencil safe-side inputs.
- **How it is useful:** It gives reviewers and future agents a compact map of
  what is proved, what is exact-integer/auditable, and what remains
  conjectural for turning the frontier into a full `delta^*` determination.
- **What to do next:** Keep this memo experimental until its claims are promoted
  into Paper D or `towards-prize`.  In particular, preserve the distinction
  between lower-floor unsafe cutoffs and a complete adjacent safe upper ledger.

### 2026-07-05 - AllenGrahamHart PR 282-321 packet integration

- **Agent/model:** AllenGrahamHart, integrated by Codex.
- **Files added or changed:** New packet notes, JSON certificates, and verifier
  scripts under `experimental/notes/`, `experimental/data/certificates/`, and
  `experimental/scripts/` from PRs `#282`-`#309` and `#311`-`#321`.  The PR-local
  `experimental/agents-log.md` hunks were not merged directly; this entry is
  the combined project log.
- **Status:** EXPERIMENTAL / AUDIT / CONDITIONAL.
- **What is being added:** A broad batch of experimental proof-program packets:
  XR light-profile and eliminant nonvanishing, L1 petal squarefree-kernel
  packets, F1 minimal-field descent, EF/E1/DLI/SOV/M720 soundness packets,
  Hankel termination and support-lattice packets, threshold/crossing/census
  ledgers, S0/rules/field-cap audits, qcore/deep-point/codegree packets, SPI
  component control, FM1/VTDV first-moment material, counting-frame packets, and
  E22 quotient-staircase/cofactor/tail-coset locator packets.
- **How it is useful:** The batch expands the certificate and roadmap layer for
  the v13 final-resolution spine, especially the `(A)` aperiodic M1 local-limit
  route, the `(Q)` quotient-fiber/equivalence route, and the adjacent
  threshold-ledger infrastructure.  It gives later agents many small,
  independently checkable packet scripts instead of only prose roadmaps.
- **What to do next:** Treat these as experimental packet inputs until the
  accompanying papers or notes promote specific claims.  Re-run individual
  verifier scripts before citing a packet, check whether any duplicated packet
  has been superseded, and keep constants/status labels explicit when moving
  material into Paper D or `towards-prize`.

### 2026-07-05 - CAP25 v13 raw auxiliary script batch for missing inputs

- **Agent/model:** Maintainer-added scripts reviewed by Codex.
- **Files added or changed:** frontier-check helper scripts under
  `experimental/scripts/towards v13/`;
  `experimental/scripts/towards v13/collision_margins.py`;
  `experimental/scripts/towards v13/gamma_census.py`;
  `experimental/scripts/towards v13/lattice_check.py`;
  `experimental/scripts/towards v13/lattice_check2.py`;
  `experimental/scripts/towards v13/prize_packing.py`;
  `experimental/scripts/towards v13/q_smooth_check.py`;
  `experimental/scripts/towards v13/q_unify_check.py`;
  `experimental/scripts/towards v13/r1_model.py`;
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** A small batch of auxiliary v13 raw scripts supporting
  the missing-inputs strategy: group-algebra collision census calibration,
  toy lattice dictionary checks, packing-bound negative calibration,
  twisted-smooth identity checks, quotient-unification checks, rank-one
  census model margins, moved-frontier integer checks, and collision-margin
  head/frontier rung calibration.
- **How it is useful:** These scripts help agents decide which proof routes are
  plausible for the `(A)` aperiodic local-limit input and `(Q)` quotient-fiber
  equidistribution input.  The cleanly running scripts show that naive packing
  and triangle-inequality character expansion are far too weak, the rank-one
  model is far below the adjacent deployed budget, and the proposed moved MCA
  frontier checks reduce to exact integer comparisons for the deployed rows.
- **What to do next:** Keep this batch experimental until an accompanying note
  or paper section states the exact claims.  The `numpy`-dependent scripts need
  either dependency documentation or pure-Python fallbacks.  `q_unify_check.py`
  currently verifies one toy regime only partially (`m=6,w=3` reports `54/60`),
  so its prescribed-prefix divisor identity should be repaired or restricted
  before being cited as a verifier.  The moved-frontier checker confirms the
  lower-floor cutoff, not a complete adjacent safe upper ledger.

### 2026-07-05 - CAP25 v13 missing-inputs proof strategy

- **Agent/model:** Maintainer-added strategy note reviewed and integrated by
  Codex.
- **Files added or changed:** `experimental/cap25_v13_missing_inputs_strategy.md`;
  `agents.md`; `experimental/agents-log.md`.
- **Status:** PROOF STRATEGY / CONJECTURAL / AUDIT.
- **What is being added:** A route map for the two missing experimental v13
  inputs: `(A)` the aperiodic band / worst-case M1 local-limit upper theorem,
  and `(Q)` the quotient-fiber / quotient-ledger equidistribution upper
  theorem.  The note separates asymptotic closure, where explicit polynomial
  losses may be absorbable, from finite adjacent deployed closure, where the
  constants must fit inside the printed bit margins.
- **How it is useful:** It gives agents concrete proof tasks: normalize the
  band edge against the entropy-subfield envelope, prove the split-top-chart
  and Hankel/Kronecker residual lemmas, build the exact prefix-collision
  ledger, audit divisor-rung margins, and test the mode-at-null /
  exchange-compression extremality conjectures.
- **What to do next:** Treat the note as strategy only.  Promote individual
  lemmas or computations only after they are written as separate proof notes or
  certificates, replayed where applicable, and linked back to the v13
  one-step/corridor machinery.

### 2026-07-05 - Towards-prize Lean formalization package

- **Agent/model:** Maintainer-added Lean package reviewed and normalized by
  Codex.
- **Files added or changed:** `experimental/lean/towards_prize/`;
  `experimental/lean/rs_mca_formalization/README.md`;
  `experimental/lean/rs_mca_formalization/CERTIFICATION_MAP.md`;
  `readme.md`; `agents.md`; `experimental/agents-log.md`.
- **Status:** FORMALIZATION / AUDIT.
- **What is being added:** A Mathlib-based Lean track for
  `tex/towards-prize.tex`, normalized to package `towards_prize`, library
  `TowardsPrize`, and entry point `TowardsPrize.lean`.  The integration removes
  generated citation/tagging boilerplate, points markdown readers at the actual
  Lean entry point, and keeps this track separate from the stdlib-only
  `rs_mca_formalization` certificate layer.
- **How it is useful:** The package formalizes the compact threshold note's
  finite-radius CA/MCA definitions, sparse layer, comparison chain,
  half-distance/deep-regime statements, identity-prefix floor, and deep-point
  conversion, giving reviewers a direct Lean target for the prize-facing note.
- **What to do next:** Build in a Mathlib-enabled Lean 4.28 environment, then
  add a theorem-by-theorem certification map.  Do not treat the deployed
  binomial-entropy cap rows as Lean-certified until they are explicitly
  formalized and mapped.

### 2026-07-05 - PR 271-280 conditional imports, toy staircases, sparse witness, and Lean anchor

- **Agent/model:** Codex integrating PR material from Vadim Avdeev
  (`#271`), latifkasuli / Claude Fable 5 (`#272`, `#273`, `#275`),
  DannyExperiments (`#274`), and LegaSage / Ken Webster (`#276`-`#280`).
- **Files added or changed:** `experimental/notes/audits/koalabear_bchks25_jmca_safe_edge_v1.md`;
  `experimental/notes/audits/koalabear_bchks25_jmca_param_squeeze_v2.md`;
  `experimental/notes/audits/koalabear_bchks25_parametric_list_mca_lemma_v1.md`;
  `experimental/notes/audits/audit_bchks25_thm46_conditional_johnson_import.md`;
  `experimental/notes/audits/audit_corridor_unconditional_safe_edges.md`;
  `experimental/notes/audits/audit_mca_ca_sparse_layer_gap_structure.md`;
  `experimental/notes/audits/paid_residual_ledger_source_drift.md`;
  `experimental/notes/thresholds/cap25_v13_seven_slope_ccl_tdd_split.md`;
  `experimental/notes/thresholds/m4_affine_eca_emca_staircase_q11.md`;
  `experimental/notes/m1/deployed_row_sparse_witness_f17_32.md`;
  `experimental/notes/m1/sigma_c_subcapacity_dichotomy_counterexample.md`;
  `experimental/data/certificates/koalabear-bchks25-jmca-*`;
  `experimental/data/certificates/corridor-unconditional-safe-edges/`;
  `experimental/data/certificates/mca-ca-sparse-layer-census/`;
  `experimental/data/certificates/deployed-sparse-witness-f17-32/`;
  `experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_m4_q11_rows.json`;
  `experimental/data/certificates/sigma-c-sparse-census/`;
  `experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py`;
  `experimental/scripts/verify_corridor_unconditional_safe_edges.py`;
  `experimental/scripts/verify_deployed_sparse_witness_f17_32.py`;
  `experimental/scripts/verify_exact_worstcase_eca_emca_affine_quotient.py`;
  `experimental/scripts/verify_f17_32_m3_low_rank2_12_*`;
  `experimental/lean/rs_mca_formalization/RsMca/EmcaStaircaseLedger.lean`;
  `experimental/lean/rs_mca_formalization/RsMca.lean`;
  `experimental/lean/rs_mca_formalization/README.md`;
  `experimental/lean/rs_mca_formalization/CERTIFICATION_MAP.md`;
  `site/data/updates.json`; `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL / PROVED-LOCAL, as tagged in
  the individual notes.  The BCHKS25 linear-in-`n` safe edge remains
  conditional; toy censuses and sparse witnesses are not leaderboard theorem
  rows.
- **What is being added:** The batch packages a conditional BCHKS25/Hab25
  KoalaBear JMCA safe-edge audit, unconditional below-band corridor safe-edge
  imports for clean-rate rows, MCA-vs-CA sparse-layer toy structure, a
  seven-slope CCL/TDD branch split, low-rank ledger replay repairs, a `k=1`
  sparse-census counterexample family, an exact `F_11,n=10,k=6` affine-shear
  eca/emca staircase, a deployed-shaped `F_17^32` sparse moving-zero witness,
  and a stdlib-only Lean finite anchor for the `(7,6,3)` EMCA staircase.
- **How it is useful:** The imported safe-edge material narrows what would be
  possible under audited external Johnson-regime MCA bounds while keeping
  proof status explicit.  The toy/sparse packets refine the sparse mutual
  layer and identify counterexample floors without changing the deployed
  threshold.  The Lean and replay-repair packets strengthen certificate
  hygiene for future adjacent-staircase work.
- **What to do next:** Re-audit external BCHKS25/Hab25/GKL24 sources before
  any Paper D promotion; do not add conditional safe edges as proved board rows.
  Run the heavier verifiers only on a dedicated machine.  Use the sparse and
  toy packets to guide the exact adjacent upper-ledger search, not as protocol
  claims.

### 2026-07-04 - CAP25 v13 identity-prefix frontier merge

- **Agent/model:** Codex reviewing and integrating a user-added experimental
  addendum and exact checker.
- **Files added or changed:** `experimental/cap25_v13_experimental.tex`;
  `experimental/scripts/towards v13/collision1b.py`;
  `experimental/scripts/towards v13/collision2.py`;
  `experimental/scripts/towards v13/frontier2.py`;
  `experimental/scripts/towards v13/frontier3.py`;
  `experimental/scripts/towards v13/cap25_v13_frontier_identity_exact_checks.py`;
  `site/data/rate-leaderboards.json`; `site/data/updates.json`;
  `site/index.html`; `experimental/agents-log.md`.  The standalone
  `experimental/cap25_v13_frontier_addendum.tex` and temporary
  `experimental/cap25_v13_body_merged_strict_plus_identity_frontier.tex` files
  were removed so the v13 experimental source is single-file again.
- **Status:** EXPERIMENTAL / CONDITIONAL / AUDIT.
- **What is being added:** The v13 experimental source now includes the
  identity-scale prefix floor, which supersedes the proposed `c=2` terminal
  addendum unless the identity map is intentionally excluded.  The new
  experimental KoalaBear MCA edge is
  `delta = 981109/2097152 ~= 0.4678292`, improving both the `c=2` edge
  `490557/1048576` and the older deployed edge `15331/32768`; the exact checker
  verifies the c=1 rows, the c=2 rows, and the older c=16/32 rows by integer
  inequalities.
- **How it is useful:** This sharpens the deployed `delta^*` upper-side
  frontier and identifies the next threshold task as an adjacent safe-side
  certificate at agreement `1116044`.  It is now shown on the site as a
  `rho=1/2` experimental MCA leaderboard row, while the active Paper D v12 draft
  remains unchanged.
- **What to do next:** Before promotion to Paper D, build the exact upper
  ledger for the adjacent safe-side step, keep polynomial-loss quotient
  equidistribution out of finite one-step claims unless constants fit inside
  the printed bit margin, and audit the aperiodic-band input separately.

### 2026-07-04 - PR 262-269 audit, sigma_C, and L1 frontier packets

- **Agent/model:** Codex integrating PR material from LegaSage/Ken Webster
  and Holm Buar.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/notes/audits/aperiodic_not_emitted_sentinel.md`;
  `experimental/notes/audits/cs25_v12_outstanding_corrections.md`;
  `experimental/notes/audits/certificate_provenance_normalization.md`;
  `experimental/scripts/verify_cluster_certificates.py`;
  `experimental/scripts/verify_cyclotomic_root_difference_germ.py`;
  `experimental/scripts/verify_exceptional_density.py`;
  `experimental/scripts/verify_graded_collision_radius.py`;
  `experimental/scripts/verify_height_only_impossibility.py`;
  `experimental/scripts/verify_m1_johnson_anticode_toolkit.py`;
  `experimental/scripts/verify_xr_e3_calculus.py`;
  `experimental/data/certificates/exact-worstcase-eca-emca-staircase/`;
  `experimental/notes/thresholds/exact_worstcase_eca_emca_staircase.md`;
  `experimental/scripts/verify_exact_worstcase_eca_emca_staircase.py`;
  `experimental/data/certificates/sigma-c-sparse-census/`;
  `experimental/notes/m1/sigma_c_sparse_census.md`;
  `experimental/scripts/verify_sigma_c_sparse_census.py`;
  `experimental/lean/rs_mca_formalization/RsMca/SigmaCSparseLedger.lean`;
  `experimental/lean/rs_mca_formalization/RsMca.lean`;
  `experimental/lean/rs_mca_formalization/README.md`;
  `experimental/lean/rs_mca_formalization/CERTIFICATION_MAP.md`;
  `experimental/notes/l1/l1_prime_ell_frontier_corrected.md`;
  `experimental/scripts/verify_l1_prime_ell_frontier_corrected.py`;
  `experimental/notes/l1/l1_petal_growth_nlist_e16.md`;
  `experimental/scripts/verify_l1_petal_growth_nlist_e16.py`.
- **Status:** AUDIT / EXPERIMENTAL / PROVED-LOCAL / NUMERIC, as tagged in the
  individual notes.
- **What is being added:** This sweep accepts the guarded `not_emitted:`
  packet-reference sentinel, the Paper D v12 outstanding-corrections addendum,
  portable certificate provenance normalization, exact toy worst-case
  eca/emca staircases, expanded `sigma_C` sparse-census rows and a Lean finite
  anchor for the `(7,6,3,2)` row, Holm's corrected prime-`ell` listing frontier
  note, and the `N_list(7,p)` petal-growth evidence packet.
- **How it is useful:** The Paper D audit material keeps two concrete v12
  cleanup findings visible without editing the paper.  The `sigma_C` and
  exact-staircase packets provide finite anchors for the sparse mutual layer in
  `towards-prize.tex`.  The L1 packets correct the earlier `ceil(2ell/3)`
  frontier heuristic with explicit witnesses while keeping the lower vacancy
  theorem conditional on its stated KEY LEMMA.
- **What to do next:** Apply or reject the Paper D wording/rounding fixes in
  `tex/cs25_cap_v12.tex` deliberately.  Do not promote the `sigma_C` or L1
  packets to deployed leaderboard rows.  For the L1 frontier, separate the
  unconditional explicit witness/refutation content from the conditional
  vacancy law before any TeX promotion.

### 2026-07-04 - L1 coset-chart residue-line bridge normal form

- **Agent/model:** Vadim Avdeev, integrated by Codex.
- **Files added or changed:** `experimental/notes/l1/l1_coset_chart_residue_bridge_v1.md`;
  `experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py`;
  `experimental/scripts/README.md`;
  `experimental/data/certificates/l1-coset-chart-residue-bridge-v1/`;
  `experimental/notes/certificate_scanner/outputs/l1_coset_chart_residue_bridge_v1.report.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / NORMAL-FORM.
- **What is being added:** A full-petal coset-chart bridge: every capped
  coset-chart kernel set is either quotient-coset, or a nonzero residue block
  emits a low-degree projective residue pair.  After simultaneous active
  quotient-label basepoints are cancelled, the pair becomes ordinary
  residue-line data on the surviving labels.
- **How it is useful:** This classifies the non-quotient minimal-kernel
  examples from the L1 reconstruction-collapse ledger without claiming they
  are paid, absent, or globally negligible.  It is a useful interface between
  the coset-petal L1 packets and the residue-line/M1 packing program.
- **What to do next:** Use the bridge as input to residue-line packing and
  globalness work.  Do not promote it to a primitive-vacancy theorem or a full
  generated-field L1 local-limit theorem without a separate quantitative
  ledger bound.

### 2026-07-04 - Allowed DAG and roadmap overwrite pass

- **Agent/model:** Codex integrating the explicitly allowed overwrite subset
  from AllenGrahamHart's DAG-maintenance PR and LegaSage/Ken's replay PR.
- **Files added or changed:** `experimental/data/prize-dag/prize_dag.json`;
  `experimental/notes/roadmaps/a_closure_assembly.md`;
  `experimental/notes/roadmaps/qx13_pair_rank_ledger.md`;
  `experimental/notes/roadmaps/w4_direct_column_rewiring.md`;
  `experimental/notes/roadmaps/x12_h3_parametrization.md`;
  `experimental/notes/roadmaps/x24_char0_dyadic_descent.md`;
  `experimental/notes/roadmaps/x32_h4_terminal_dichotomy.md`;
  `experimental/notes/roadmaps/x81_minimal_trade_square_shift.md`;
  `experimental/notes/roadmaps/x82_square_shift_certifier_keys.md`;
  `experimental/notes/roadmaps/x83_uniform_square_shift_obstruction_gate.md`;
  `experimental/notes/roadmaps/xr_budget_audit.md`;
  `experimental/notes/roadmaps/xr_syzygy_flat_transport.md`;
  `experimental/notes/roadmaps/xr_triangle_eliminant_form.md`;
  `experimental/scripts/locator/locator_fiber_local_packet/run_locator_fiber_local_packet.py`.
- **Status:** EXPERIMENTAL / AUDIT / ROADMAP, as tagged in the individual
  files.
- **What is being added:** This pass accepts the central DAG rewrite and the
  existing roadmap-note rewrites that were intentionally skipped in the prior
  additive-only sweep.  It also accepts the small locator packet runner path
  fix from the replay tooling PR.
- **How it is useful:** The prize-DAG and roadmap notes now reflect the
  contributor-maintained dependency graph for the XR, square-shift, quotient,
  and closure-assembly proof programs.  The runner fix keeps the local packet
  path aligned with the current script layout without running the heavy replay.
- **What to do next:** Treat the DAG as experimental coordination metadata:
  reconcile it against `towards-prize.tex`, CAP25 v12/v13 notes, and the site
  before using it as a proof-status authority.  If any roadmap note is promoted
  into a paper, restate the claim in TeX and cite the exact certificate or
  theorem dependency.

### 2026-07-04 - Additive experimental evidence sweep

- **Agent/model:** Codex integrating additive PR material from AllenGrahamHart
  and LegaSage/Ken after the main PR 210-260 sweep.
- **Files added or changed:** `experimental/notes/roadmaps/xr_pair_orbit_globalness.md`;
  `experimental/notes/roadmaps/q3r2_link_leak_adjudication.md`;
  `experimental/data/certificates/xr-pair-orbit-globalness/`;
  `experimental/data/certificates/q3r2-link-leak-adjudication/`;
  `experimental/notes/audits/cs25_v12_consolidated_audit_2026-07-02.md`;
  `experimental/notes/audits/lean_build_verification.md`;
  `experimental/notes/audits/independent_replay_2026-07-02.md`;
  `experimental/notes/audits/independent_replay_2026-07-03.md`;
  `experimental/data/audits/`; selected new roadmap notes from the clean-rate
  DAG maintenance packet.
- **Status:** EXPERIMENTAL / AUDIT / STATUS REPORT, as tagged in the
  individual notes.
- **What is being added:** The XR pair-orbit/globalness packet and Q3R2
  link-leak adjudication are added as experimental falsifier/evidence
  material.  Additional audit receipts record Paper D v12 audit coverage,
  external Lean build verification, and independent verifier replay matrices.
  The extra roadmap files are additive status/proof-program notes only; the
  broad `prize_dag.json` rewrite and existing-note overwrites were not taken.
- **How it is useful:** This keeps potentially useful evidence in-repo without
  promoting it to theorem status.  In particular, the XR evidence warns that a
  narrow fixed-core/fixed-hole taxonomy needs a delta-character/link-leak
  branch, and the replay/Lean notes preserve external audit receipts for later
  human review.
- **What to do next:** Distill the XR evidence into the M1/XR proof-program
  summary, decide whether the subprocess replay harness should remain as
  tooling or be replaced by a lighter audit-only record, and only update the
  central DAG after reconciling it with the already integrated roadmap notes.

### 2026-07-04 - PR 210-260 integration sweep

- **Agent/model:** Codex integrating PR material from AllenGrahamHart, Holm
  Buar, Vadim Avdeev, DannyExperiments/Gia, LegaSage, and Latif Kasuli.
- **Files added or changed:** `experimental/cap25_v13_experimental.tex`;
  `experimental/notes/l1/`; `experimental/notes/m1/`;
  `experimental/notes/roadmaps/`; `experimental/notes/thresholds/`;
  `experimental/notes/audits/`; `experimental/data/certificates/`;
  `experimental/scripts/`; `experimental/lean/l1_threshold_ledger/`;
  `site/data/`.
- **Status:** PROVED / CONDITIONAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE, as tagged in the individual notes.
- **What is being added:** The sweep integrates the narrow CAP25 v13 SPI split
  repair, Vadim's A407/A408 residual-design finite-slope threshold row and
  site entry, the Holm Buar L1 reduction/refutation chain, a small L1 Lean
  ledger, sigma_C and Hankel-kernel experimental censuses, and Allen's
  clean-rate proof-spine packets for quotient/tangent budgeting, PTE and
  square-shift trades, good-reduction/GCD certification, XR residual
  decompositions, and the `16 n^3` clean-rate compiler target.
- **How it is useful:** The new public leaderboard item is the prime-field
  `A=406/A=407` finite-slope gate.  The rest is proof-program infrastructure:
  it narrows the CAP25 v13/M1 route, corrects the PTE half-size window to
  `h <= A`, records the primitive-vacancy L1 refutation, and makes the current
  clean-rate path auditable without promoting conditional roadmap packets into
  Paper D.
- **What to do next:** Replay only the lightweight verifier scripts selected
  for promotion, distill the clean-rate proof-spine into the next
  `towards-prize`/CAP25 planning note, decide whether broad DAG PRs should be
  merged separately, and avoid claiming official prize resolution until the
  terminal post-strip `R_post <= 16 n^3` input is proved or replaced.

### 2026-07-04 - Paper B Lean formalization package

- **Agent/model:** Aristotle/Harmonic draft reviewed and packaged by Codex.
- **Files added or changed:** `experimental/lean/slackMCA_v4/`;
  `experimental/agents-log.md`.
- **Status:** FORMALIZATION / AUDIT.
- **What is being added:** A normalized Lean package for selected finitary
  parts of `tex/slackMCA_v4.tex`, under the `slackMCA_v4.*` module namespace.
  It covers locator/list fibers, monomial-prefix and generated-field
  pigeonhole bounds, quotient-core lower bounds, the dyadic inverse-quotient
  theorem, finite entropy lower bounds, one-bad-parameter, exact slack,
  quotient locator identities, cyclotomic rigidity, and Fermat digit rigidity.
- **How it is useful:** This gives Paper B a substantial formalization track
  for the unconditional finite spine while keeping the full asymptotic L1/M1
  reserve program out of scope.
- **What to do next:** Build in a Mathlib-enabled Lean 4.28 environment and
  then decide which remaining Paper B inputs should become named Lean
  hypotheses versus future formalization targets.

### 2026-07-04 - CAP25 v13 experimental Lean package

- **Agent/model:** Aristotle/Harmonic draft reviewed and packaged by Codex.
- **Files added or changed:**
  `experimental/lean/cs25_cap_v13_experimental/`;
  `experimental/agents-log.md`.
- **Status:** FORMALIZATION / EXPERIMENTAL / AUDIT.
- **What is being added:** A normalized Lean package for selected
  self-contained compiler lemmas from `experimental/cap25_v13_experimental.tex`,
  under the `cs25_cap_v13_experimental.*` module namespace.  It formalizes
  threshold staircases/corridors, budget windows, extension-pole counting,
  quotient-census arithmetic, planted/list-side compiler pieces, fixed-excess
  counting, GAP-2 seam arithmetic, substitution injectivity,
  fixed-dimensional Conjecture-F tools, Hankel determinant, anticode packing,
  and Johnson-ball counting.
- **How it is useful:** This turns the v13 experimental insert into a more
  auditable compiler package without promoting the insert into Paper D.
- **What to do next:** Build in a Mathlib-enabled Lean 4.28 environment,
  review `native_decide` arithmetic certificates, and treat the omitted
  tangent, quotient-ledger, split-locator probability, spectral Johnson, and
  SPI eliminant pieces as separate formalization targets.

### 2026-07-03 - CAP25 v13 experimental insert

- **Agent/model:** Codex, reviewing a user-added experimental v13 insert.
- **Files added or changed:** `experimental/cap25_v13_experimental.tex`;
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT / CONDITIONAL.
- **What is being added:** A body-only TeX insert designed for possible future
  inclusion in `tex/cs25_cap_v12.tex` before the Discussion section.  It adds
  v13-labeled threshold staircase/corridor compilers, exact high-agreement
  tangent cells, quotient and extension paid-cell interfaces, planted
  quotient-core list compilers, sunflower residual charts, split-locator moment
  ledgers, Conjecture-F reductions, and a deficiency-one SPI
  eliminant-or-residual theorem.
- **How it is useful:** This is a clean experimental bridge from Paper D v12
  toward a possible v13: it sharpens the certificate grammar without merging
  into the main paper, and it names the remaining L1/M1 residual branches
  rather than hiding them inside point estimates.
- **What to do next:** Review the mathematical claims line by line before
  promotion into Paper D.  Source checks found all references resolved against
  the insert or `tex/cs25_cap_v12.tex`; a temporary Tectonic compile of v12
  with this insert succeeded with only underfull-box warnings.

### 2026-07-03 - Paper D CAP25 Lean skeleton package

- **Agent/model:** Aristotle/Harmonic draft reviewed and packaged by Codex.
- **Files added or changed:** `experimental/lean/cs25_cap_v12/`;
  `experimental/agents-log.md`.
- **Status:** FORMALIZATION / SKELETON / AUDIT.
- **What is being added:** A Lean package for `cs25_cap_v12.tex`, normalized
  under the `cs25_cap_v12.*` namespace.  It contains a substantial proved
  abstract core for CA/MCA definitions, Theorem A, safe-side/deep-regime
  bounds, Johnson counting, universal-cap reduction from a fiber-list input,
  RS sandwich wrappers, scanner soundness, and selected ledger primitives.
- **How it is useful:** This provides a formal roadmap for Paper D.  The
  construction-heavy parts are explicitly kept as named skeleton targets with
  `sorry`: fiber/map-smooth constructions, regular Hankel certificates,
  quotient-remainder floors, explicit interleaving witnesses, circle-code
  analogues, and ECFFT/rational-map caps.
- **What to do next:** Run `lake build` in a Mathlib-enabled environment, then
  attack the `Fiber.lean` skeleton first because it supplies the list-mass input
  consumed by the universal-cap reduction.

### 2026-07-03 - Paper A Lean formalization package

- **Agent/model:** Aristotle/Harmonic draft reviewed and packaged by Codex.
- **Files added or changed:** `experimental/lean/RS_disproof_v3/`;
  `experimental/agents-log.md`.
- **Status:** FORMALIZATION / SUBSTANTIAL / AUDIT.
- **What is being added:** A Lean package for Paper A (`RS_disproof_v3.tex`),
  including the quotient-locator core, support-wise line-MCA predicates,
  monotonicity, MCA lower bounds from restricted sums, the list lower bound
  with distinct-codeword injection, the density-to-MCA reduction, the 2-adic
  tower criterion, scalar-coset extension-field lift, and exact small finite
  verification records via `native_decide`.
- **How it is useful:** This is now a substantial Paper A formalization track,
  not just a locator-core stub.  It isolates which parts are Lean-proved and
  which are imported: Dias da Silva--Hamidoune, Siegel--Walfisz / the full
  cyclotomic sieve, and the general Fermat digit lemma remain external inputs,
  while selected finite Fermat/deployed arithmetic records are checked inside
  Lean.
- **What to do next:** Verify the package locally with Mathlib available.
  Then decide whether to formalize the remaining imported number-theoretic
  inputs or keep them as explicitly named hypotheses.

### 2026-07-03 - Consolidated threshold, M1, and L1 TeX notes

- **Agent/model:** Codex, consolidating threshold/M1/L1 material contributed
  primarily by AllenGrahamHart in the recent PR batch.
- **Files added or changed:** `experimental/thresholds.tex`;
  `experimental/thresholds.pdf`; `experimental/m1.tex`;
  `experimental/m1.pdf`; `experimental/l1.tex`; `experimental/l1.pdf`;
  `experimental/agents-log.md`.
- **Status:** DOCUMENTATION / COMPILER-NOTES / COMPILED.
- **What is being added:** Three self-contained experimental TeX notes:
  threshold certificate compilers for CAP25, the M1 residue-line and
  Conjecture-F proof program, and the L1 list-side compiler/petal program.
  The notes integrate the markdown material into paper-shaped statements,
  definitions, proof sketches, status warnings, and CAP25 integration
  checklists.
- **How it is useful:** This gives the project editable working-paper inputs
  for the next CAP25/towards-prize pass without requiring readers to reconstruct
  the story from many PR notes.  It also separates proved compiler arithmetic
  and local lemmas from evidence, conjectural reductions, and open theorem
  gaps.
- **What to do next:** Audit each theorem/lemma statement against the source
  PR notes before promoting it into Paper D or a submission-facing paper.
  In particular, keep L1 sunflower evidence and M1 Conjecture-F evidence out
  of the PROVED ledger until the corresponding residual bounds are complete.

### 2026-07-03 - PR batch: DAG, threshold compilers, and A425/A426 finite gate

- **Agent/model:** Codex integrating PRs from AllenGrahamHart, Vadim Avdeev,
  DannyExperiments/Gia, and Lean certification contributors.  AllenGrahamHart
  authored the majority of the batch; see
  `experimental/notes/roadmaps/pr_batch_2026_07_03_attribution.md` for the
  per-PR attribution ledger.
- **Files added or changed:** `experimental/data/prize-dag/`;
  `experimental/notes/roadmaps/`; `experimental/notes/thresholds/`;
  `experimental/notes/certificate_scanner/`;
  `experimental/notes/{m1,l1,f1,m5,x1,audits}/`;
  `experimental/data/certificates/`; `experimental/scripts/`;
  `experimental/lean/rs_mca_formalization/`; `scripts/aperiodic_eliminant_schema.json`;
  `scripts/check_aperiodic_eliminant_packet.py`; `site/data/frontier.json`;
  `site/data/rate-leaderboards.json`; `site/data/updates.json`; `site/index.html`.
- **Status:** MIXED: PROVED local finite-slope threshold row / AUDIT /
  EXPERIMENTAL evidence / ROADMAP infrastructure.
- **What is being added:** Integrated the reviewed experimental payload from
  PRs #178--#208, excluding stale README/site/towards-prize edits from older
  branch bases.  The main new public row is the prime-field A425/A426 adjacent
  finite-slope support-wise MCA gate: PR #204 gives the two-core upper bound
  `LD_sw(RS[F,D,256],426)=87`, PR #208 gives the direct A=425 unsafe witness,
  and the prime `p=22275*2^120+1` satisfies `87*2^128 < p < 88*2^128`.
  The batch also adds Allen's prize DAG maintenance packet, quotient-census and
  dodge-selection compilers, CAP25 sparse-sigma audits, Lean tier-one
  certification map updates, and many M1/L1/F1/M5 evidence/proof-program notes.
- **How it is useful:** The A425/A426 row is a new exact finite-slope
  threshold example for a smooth rate-1/2 prime-field row and is now visible on
  the site.  The other packets fill the towards-prize execution DAG with
  reproducible certificates, compiler arithmetic, red-team queues, and local
  proof sublemmas without promoting them to final Paper D authority.
- **What to do next:** Independently audit the two-core proof and Lucas prime
  certificate before citing the A425/A426 row externally.  For the broader PR
  batch, run only lightweight verifier syntax/JSON checks by default; execute
  heavier scanners only when a contributor opts in with explicit resources.
  Keep Paper D text unchanged unless explicitly requested.

### 2026-07-02 - Restore Paper D title and content

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v12.tex`; `cs25_cap_v12.pdf`;
  `site/papers/cs25_cap_v12.pdf`; `readme.md`; `towards-prize.md`;
  `site/data/papers.json`; `site/data/updates.json`; `site/index.html`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / REVERT / DOCUMENTATION.
- **What is being added:** Paper D itself is restored to the pre-framing
  version, including its original title.  External docs and site metadata keep
  the stronger role description, but display the Paper D title as
  `Paper D: Two-Sided Cap and Certificate Grammar`.
- **How it is useful:** This preserves Paper D as a stable mathematical source
  while still telling contributors that it is the main submission reference for
  cap hypotheses, endpoint conventions, denominators, and proof status.
- **What to do next:** Do not edit Paper D wording for hierarchy/framing unless
  explicitly requested; make such hierarchy changes in README, roadmap, site,
  and logs only.

### 2026-07-02 - Paper D external submission-reference framing

- **Agent/model:** Codex.
- **Files added or changed:** `tex/towards-prize.tex`; `towards-prize.pdf`; `readme.md`;
  `towards-prize.md`; `site/data/papers.json`; `site/data/updates.json`;
  `site/index.html`; `site/papers/towards-prize.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / DOCUMENTATION / COMPILED.
- **What is being added:** External docs were adjusted to present Paper D as
  the main submission reference for the package, while preserving Paper D's
  own title and text.  The `towards-prize` note states that it is a compact
  companion, not a competing authority.
- **How it is useful:** This removes ambiguity in the package hierarchy:
  public rows, scanner outputs, and companion notes should cite Paper D v12 for
  final hypotheses, endpoint conventions, denominators, and proof status.
- **What to do next:** Keep hierarchy/framing edits outside Paper D unless
  explicitly requested; audit Paper D itself through theorem statements and
  certificate checks.

### 2026-07-02 - Towards-prize sparse note documentation pass

- **Agent/model:** Codex.
- **Files added or changed:** `readme.md`; `towards-prize.md`;
  `site/data/papers.json`; `site/data/updates.json`; `site/index.html`;
  `site/papers/towards-prize.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / DOCUMENTATION / SITE-REFERENCE.
- **What is being added:** The promoted `tex/towards-prize.tex` note is now
  referenced as the active compact prize-facing theorem note.  The README,
  roadmap, public site paper list, and update feed now describe the sparse
  residual layer and `delta^*` staircase role.
- **How it is useful:** This makes the current execution target visible
  without promoting the sparse note to a new numerical leaderboard record.  It
  records that the note is roadmap/theorem packaging: the remaining work is to
  audit the sparse reduction and produce CA/list or sparse-residual
  certificates.
- **What to do next:** Audit `emca=max(eca,sigma_C/q)`, endpoint conventions,
  and the rider-bound constants against Paper D v12 before using the sparse
  note as a proof authority.

### 2026-07-02 - Towards-prize best promotion with sparse residual layer

- **Agent/model:** Codex, reviewing maintainer-added
  `tex/towards-prize_best.tex`.
- **Files added or changed:** `tex/towards-prize.tex`; `towards-prize.pdf`;
  `archived/towards-prize_v3.tex`; `archived/towards-prize_v3.pdf`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE / COMPILED.
- **What is being added:** `towards-prize_best.tex` is promoted to the
  canonical `tex/towards-prize.tex`.  Compared with v3, it keeps the deployed
  staircase/certificate package and adds the sparse residual layer:
  exact sparsification of MCA as `max(eca, sigma_C/q)`, a sparse support
  threshold, Reed--Solomon pinning/normal form, match-rigidity, the sparse
  value-set wall, and a rider bound reducing the sub-half plain-CA band to
  deficient pair lists for doubly sparse far pairs.
- **How it is useful:** This is strictly stronger for determining `delta^*`:
  it replaces the older mutual-residual formulation by a sharper sparse
  counting problem while retaining the legacy shortening/pair-list statement
  for comparison.
- **What to do next:** Audit the sparse reductions against the current Paper D
  v12 notation, especially the `sigma_C` normalization, endpoint conventions,
  and the rider-bound pair-list constant.

### 2026-07-02 - PR sweep: G3 toy evidence, v12 audits, and M5 A384 atlas

- **Agent/model:** Codex, integrating PRs from Latif Kasuli and Allen Graham
  Hart.
- **Files added or changed:** `experimental/notes/g3/g3_rank_boundary_toy_evidence.md`;
  `experimental/data/certificates/g3-rank-boundary-toy/g3_rank_boundary_toy_evidence.json`;
  `experimental/notes/audits/cs25_v12_*_audit.md`;
  `experimental/notes/audits/towards_prize_v*_audit.md`;
  `experimental/data/certificates/cs25-v12-deployed-certificates/`;
  `experimental/data/certificates/towards-prize-v2-constant-audit/`;
  `experimental/scripts/verify_cs25_v12_*.py`;
  `experimental/scripts/verify_towards_prize_v*.py`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `tex/cs25_cap_v12.tex`.
- **Status:** EXPERIMENTAL / AUDIT / PROVED-LOCAL.
- **What is being added:** PR #175 is integrated as a rehomed G3 toy evidence
  packet: corrected `F_97,n=16,k=8,a=11` rank-boundary ledgers, a stable
  aperiodic `mu4` monomial family, and an explicit tangent-convention question.
  PR #177 is integrated as Paper D v12 and towards-prize audit notes, JSON
  packets, and small exact verifier scripts.  Its explicit-pair audit found a
  proof-writing rounding issue, now patched in `tex/cs25_cap_v12.tex` by adding
  the missing integer-valued slope-count step.  PR #176 is not merged wholesale;
  its reusable M5 deficiency-one Cramer-chart theorem is distilled into the
  existing A384 pivot note.
- **How it is useful:** #175 supplies budget-relevant toy evidence for the
  middle-band non-tangent/non-quotient residual program. #177 strengthens the
  current main audit focus around Paper D v12, including conversion radius,
  BCIKS normalization, deployed certificates, transport scope, and profile
  constants. #176 identifies the first underdetermined Hankel bucket atlas at
  `A=384`, relevant to the `B_mca(a)` staircase but not yet a threshold bound.
- **What to do next:** Answer the G3 tangent classifier convention question;
  rerun or independently audit the new exact verifier scripts when desired;
  request a smaller #176 follow-up if the large planted verifier/data packet
  should be merged; audit the patched `cs25_cap_v12.tex` explicit-pair proof in
  the next Paper D compile pass.

### 2026-07-02 - Towards-prize v3 staircase tightening

- **Agent/model:** Codex.
- **Files added or changed:** `tex/towards-prize.tex`;
  `towards-prize.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-TIGHTENING / COMPILED.
- **What is being added:** The v3 cap-paper package now explicitly defines the
  integer staircase numerator `B_mca(a)`, states the one-step threshold
  certificate, records the KoalaBear unsafe handle
  `(c,m,w,Delta)=(16,69748,4211,67392)`, and moves the circle row into a
  secondary remark.  It also adds the deployed subfield warning that
  base-valued KoalaBear lines have density at most `|B|/|F|<2^-154`, so
  target-level obstructions must be genuinely extension-valued.
- **How it is useful:** This makes `towards-prize.tex` sharper for determining
  `delta^*`: it names the exact finite object to certify and separates the
  prize-facing KoalaBear statement from contextual row examples.
- **What to do next:** Audit the staircase definition and KoalaBear handle
  against `tex/cs25_cap_v12.tex`, especially endpoint convention,
  `q_line`, and the confinement lemma for subfield rows.

### 2026-07-02 - Towards-prize v3 cap-paper package

- **Agent/model:** Codex.
- **Files added or changed:** `tex/towards-prize.tex`;
  `towards-prize.pdf`; `archived/towards-prize_v2.tex`;
  `archived/towards-prize_v2.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE / COMPILED.
- **What is being added:** `towards-prize.tex` now includes a compact
  cap-paper refinement theorem rather than copying Paper D v12's long scanner
  and transport sections.  The new package records the self-contained
  half-Johnson safe handle, finite staircase certificates for deployed
  multiplicative and circle rows, map/rational-smooth transfer scope, and the
  optimized failure profile.
- **How it is useful:** This makes the prize-facing note strictly stronger for
  determining `delta^*`: it improves the self-contained safe edge where the
  half-Johnson certificate beats the one-third-distance theorem, states concrete
  deployed two-sided intervals, and identifies which row-level claims are finite
  certificate checks in Paper D v12.
- **What to do next:** Audit the imported cap-paper package against
  `tex/cs25_cap_v12.tex`: half-Johnson constants, deployed interval endpoints,
  circle/genus-one transport hypotheses, and profile constants.

### 2026-07-02 - Towards-prize v2 promotion

- **Agent/model:** Codex, reviewing maintainer-added draft.
- **Files added or changed:** `tex/towards-prize.tex`;
  `towards-prize.pdf`; `archived/towards-prize_v1.tex`;
  `archived/towards-prize_v1.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE / COMPILED.
- **What is being added:** The maintainer-added `towards-prize_v2.tex` is
  promoted to the canonical `tex/towards-prize.tex`.  Compared with v1, it
  sharpens the unsafe edge using the ordinary locator cap, explicitly marks the
  top of the old plain-CA band as unsafe, and adds residual shortening-image and
  doubled-radius pair-list reductions for the mutual layer above half distance.
- **How it is useful:** This is strictly stronger as a prize-facing note: it
  narrows the remaining CA interval and replaces the broad "mutual layer"
  question with concrete finite objects, while preserving the v12 audit framing.
- **What to do next:** Audit the new numerical constants
  `alpha_rho`, the ordinary-locator entropy table, and the two residual
  reductions.  The promoted PDF was compiled with Tectonic; only minor box
  warnings were reported.

### 2026-07-02 - Paper D v12 reference sweep

- **Agent/model:** Codex.
- **Files added or changed:** `readme.md`; `agents.md`;
  `towards-prize.md`; `site/index.html`; `site/data/papers.json`;
  `site/data/rate-leaderboards.json`; `site/data/updates.json`;
  `site/papers/cs25_cap_v12.pdf`; selected `experimental/notes/`,
  `experimental/scripts/`, and `experimental/data/certificates/` references.
- **Status:** AUDIT / DOCUMENTATION / VERSION-PROMOTION.
- **What is being added:** Active Paper D references were moved to
  `tex/cs25_cap_v12.tex`, and contributor-facing text now says that v12 is the
  final-submission cap paper to audit.  The public site metadata and local PDF
  mirror were updated to point at the v12 package.
- **How it is useful:** Prevents new agents from following the superseded v10
  Hankel-ledger draft as the current cap-paper source, while preserving older
  v6--v10 audit/log entries as historical provenance.
- **What to do next:** Audit v12 directly: direct conversion/radius
  conventions, half-distance import scope, integer certificate replay, and the
  printed certificate grammar.

### 2026-07-02 - Paper D v12 and towards-prize audit focus

- **Agent/model:** Codex, reviewing maintainer-added drafts.
- **Files added or changed:** `tex/cs25_cap_v11.tex`;
  `tex/cs25_cap_v12.tex`; `tex/towards-prize.tex`;
  `cs25_cap_v11.pdf`; `cs25_cap_v12.pdf`; `towards-prize.pdf`;
  `AGENTS.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE.
- **What is being added:** Paper D v12 is now the main cap-paper candidate:
  it supersedes v10/v11 as the most complete draft, adding the safe-side
  pincer, half-distance MCA-from-CA reduction, map/rational smooth extensions,
  circle/genus-one transports, explicit witness machinery, optimized profile,
  and certificate grammar v2.  `tex/towards-prize.tex` is the compact
  prize-facing theorem note aligned with the v12 package.
- **How it is useful:** The project focus moves from collecting more frontier
  examples to auditing the cap package itself.  The main task is checking the
  CS25/Paper-D conversion pipeline, the optional BCIKS half-distance import,
  the integer certificates behind every deployed-row inequality, and the exact
  scope of the circle/genus-one model transfers.
- **What to do next:** Treat CS25/Paper-D auditing as the main focus.  Before
  promoting v12 as the stable Paper D, produce a short audit note covering:
  direct conversion/radius conventions, ABF/CA/MCA normalization, BCIKS import
  compatibility, exact-integer certificate replay paths, and whether
  `towards-prize.tex` states only the claims actually proved by v12.

### 2026-07-02 - Post-v10 PR sweep: M1 reductions, M3 synthetic packets, M5 underdetermined roadmap

- **Agent/model:** Codex, integrating and auditing contributions from
  AllenGrahamHart, DannyExperiments, and Gia.
- **Files added or changed:**
  `experimental/notes/triage/pr-triage-2026-07-02-post-v10.md`;
  `experimental/notes/audits/m0_prize_mca_definition_freeze.md`;
  `experimental/notes/m1/m1_simple_pole_projected_locator_wall.md`;
  `experimental/notes/m1/m1_dyadic_shifted_prefix_value_bridge.md`;
  `experimental/notes/m3/m3_low_rank_affine_spectral_reduction.md`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  selected `experimental/data/certificates/hankel-f17-32-m3-*` packets;
  selected `experimental/scripts/verify_f17_32_m3_*` scripts;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/notes/roadmaps/proximity_prize_execution_roadmap_post_v10_r2.md`;
  `experimental/notes/roadmaps/proof_sketch/`;
  `experimental/notes/roadmaps/wp_detail/`;
  `experimental/data/prize-dag/`;
  `experimental/scripts/verify_prize_dag.py`;
  `experimental/scripts/verify_roadmap_r2_numbers.py`;
  `experimental/scripts/plot_prize_dag.py`;
  `scripts/check_aperiodic_eliminant_packet.py`;
  `towards-prize.md`.
- **Status:** AUDIT / PROVED-LOCAL / EXPERIMENTAL / ROADMAP.  No leaderboard
  movement and no new prize-facing threshold claim.
- **What is being added:** The batch integrates Danny/Gia's M1 simple-pole and
  shifted-prefix reductions, Allen's synthetic low-rank M3/M4 packet material,
  Allen's M5 `A=384` underdetermined-boundary packet, and Allen's post-v10 r2
  roadmap/DAG as subordinate planning material.  From the large rank-witness
  PR only the M0 definition-freeze note and packet-checker enhancement were
  taken; the generated rank-6 sidecars remain held for split/replay.
- **How it is useful:** The main new strategic point is that the official
  prize band is entirely underdetermined, so regular M3 packets are a proving
  ground while M5 underdetermined charts are the real band-facing program.
  The M1 reductions isolate cleaner projected-value walls, and the M3
  low-rank packets provide scoped synthetic tests for the then-current v10
  ledger style, now superseded by Paper D v12.
- **What to do next:** Refine the `A=384` M5 Cramer/divisibility chart into an
  eliminant or named residual obstruction; replay or split any #171 rank-6
  material before integration; and keep new PRs to one theorem cluster or
  certificate packet at a time.

### 2026-07-01 - v10 guide and site metadata sync

- **Agent/model:** Codex.
- **Files added or changed:** `AGENTS.md`; `README.md`/`readme.md`;
  `site/index.html`; `site/papers/cs25_cap_v10.pdf`;
  `towards-prize.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / DOCUMENTATION.
- **What is being added:** The agent guide, repo overview, prize roadmap, and
  site paper metadata were then pointed at Paper D v10 as the cap/Hankel-ledger
  package.  Paper D v12 now supersedes this entry.  `AGENTS.md` also named the
  next concrete prize task: an M3/M4
  root-table and paid-root-subtraction packet for the `F_17^32`, `n=512`,
  `k=256` row over agreements `385 <= A <= 426`.
- **How it is useful:** Historical provenance for the v10 transition away from
  v9, strict264, and strict352 as the active frontier.  The current successor
  route is Paper D v12's safe-side pincer and certificate grammar.
- **What to do next:** Build the first M3/M4 table for selected agreements in
  `385 <= A <= 426`, including regular roots, tangent/quotient/extension
  subtraction, and residual chart labels.

### 2026-07-01 - PR 161--169 frontier integration

- **Agent/model:** Codex, integrating contributions from holmbuar,
  AllenGrahamHart, DannyExperiments, and Gia.
- **Files added or changed:** `tex/slackMCA_v3.tex`;
  `tex/slackMCA_v4.tex`; `tex/snarks_v4.tex`; `tex/snarks_v5.tex`;
  `experimental/notes/audits/pr161_169_integration_audit.md`;
  `experimental/notes/l1/l1_full_petal_growing_defect_witnesses.md`;
  `experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`;
  `experimental/data/certificates/l1-monomial-dyadic-descent/`;
  `experimental/notes/m1/m1_full_overlap_low_tail_completion_projection_wall.md`;
  `experimental/notes/m1/m1_beta2_conditional_close.md`;
  `experimental/notes/m1/m1_beta2_obstruction_floor.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/notes/m1/f17_32_m3_generic_regular_minor.md`;
  `experimental/notes/m1/f17_32_hankel_row_descriptor.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/thresholds/f17_32_high_agreement_tangent_table.md`;
  `experimental/lean/rs_mca_formalization/RsMca.lean`;
  `experimental/lean/rs_mca_formalization/RsMca/F1ExtensionLedger.lean`;
  `experimental/lean/rs_mca_formalization/RsMca/BetaTwoReductionLedger.lean`;
  selected verifier scripts and Hankel/L1 data packets.
- **Status:** AUDIT / PROVED-SUBPACKETS / CONDITIONAL / EXPERIMENTAL.
- **What is being added:** The L1 target in Papers B/C is repaired from raw
  support fibers to image fibers; full-petal L1 witnesses and a monomial
  dyadic replay packet are banked; M1 full-overlap and BETA_2 route-cut notes
  are integrated; F1/BETA Lean ledgers are wired; and selected M3 regular
  Hankel row-descriptor/window/minor artifacts are added from the large
  regular-minor PR.
- **How it is useful:** This turns the current PR wave into usable proof
  infrastructure for the v10 prize plan: L1 is now stated against the right
  object, M1 route cuts are named, F1/BETA algebra cores are formalized, and
  the `F_17^32` non-tangent regular window has compact row and generic-minor
  artifacts.
- **What to do next:** Use the M3 row descriptor and regular-minor extractor
  to compute actual root tables in `385 <= A <= 426`; compress any remaining
  generated PR #161 material into small audited proof packets before adding it;
  and seek a genuine BETA_2 monodromy/conductor theorem rather than promoting
  finite local data.

### 2026-07-01 - Paper D v10 milestone integration

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v10.tex`;
  `cs25_cap_v10.pdf`; `scripts/cs25_v10_*.py`;
  `experimental/data/certificates/cs25-v10-regular-hankel-examples/`;
  `experimental/notes/audits/paperD_v10_milestone_integration_audit.md`;
  `towards-prize.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED-CERTIFICATE-FRAMEWORK.
- **What is being added:** Integrated the four v10 milestone folders into Paper
  D v10: quantitative deep-list floors, heaviest prefix-fiber quotient lower
  ledgers, exact divisor-block support-union coefficients, gcd/lcm quotient
  image ledgers, extension-pole simple-pole witnesses, and canonical regular
  Hankel rank-drop gcd/lcm ledgers.
- **How it is useful:** This strengthens Paper D's completion program from a
  v9 chart atlas into scanner-ready lower, quotient, extension, and regular
  Hankel ledgers.  It also narrows the remaining prize-side work to structural
  exhaustion, singular buckets, and safe-side extension classification.
- **What to do next:** Run the regular Hankel checker on the `F_17^32` row in
  the `385 <= A <= 426` window, combine paid-root subtraction with quotient and
  tangent ledgers, and build pivot eliminants for any singular buckets.  For
  current citations, use Paper D v12 rather than this v10 milestone note.

### 2026-06-30 - M2 Hankel smoke packet

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/certificates/hankel-smoke-f17-506-507/`;
  `experimental/notes/thresholds/hankel_smoke_f17_506_507.md`;
  `experimental/scripts/verify_hankel_smoke_f17_506_507.py`;
  `towards-prize.md`; `tex/cs25_cap_v9.pdf`.
- **Status:** PROVED-SMOKE-PACKET / AUDIT.
- **What is being added:** The duplicate `tex/cs25_cap_v9.pdf` was removed,
  and the M2 v9 smoke packet was added for the settled
  `RS[F_17^32,H,256]`, `n=512`, `k=256` high-agreement threshold.  The packet
  records `A=506` with numerator `7` as unsafe and `A=507` with numerator `6`
  as safe, with declared aperiodic numerator `0` after tangent ledger removal.
- **How it is useful:** This validates the v9 packet format on a row whose
  answer is already known, giving future agents a concrete template before
  attacking the regular non-tangent window.
- **What to do next:** Use the same packet/checker workflow for M3:
  agreements `385 <= A <= 426`, where regular Hankel minors may close rows not
  covered by tangent exactness.

### 2026-06-30 - Aperiodic Hankel packet checker

- **Agent/model:** AllenGrahamHart / Codex, integrated by Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/aperiodic-hankel-regular-minor-toy/`;
  `experimental/notes/m1/aperiodic_hankel_regular_minor_toy_certificate.md`;
  `experimental/scripts/verify_aperiodic_hankel_regular_minor_toy.py`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED for the toy certificate.
- **What is being added:** A reusable checker for
  `scripts/aperiodic_eliminant_schema.json`, a deterministic `F_17`,
  `n=16`, `k=8`, `a=13` regular-overdetermined Hankel-minor toy packet, and
  an intentionally invalid packet for negative testing.
- **How it is useful:** This is the first concrete replay target for the Paper
  D v9 Hankel certificate workflow.  It checks schema conformance, `j=n-A`,
  `t=A-k`, regular-minor degree/root hashes, residual labels, and declared
  root-union numerators.
- **What to do next:** Extend the checker to real prize-facing rows and
  singular/residual buckets; keep every new packet tied to the v9 schema and a
  deterministic verifier.

### 2026-06-30 - Late PR M1/audit integration

- **Agent/model:** Codex, auditing and distilling PRs from AllenGrahamHart and
  Scott Hughes.
- **Files added or changed:** M1/audit notes and verifiers from PRs #150--#156
  and #158 under `experimental/notes/` and `experimental/scripts/`;
  `experimental/data/step5-envelope-map/envelope_map.json`;
  `experimental/notes/m1/m1_packet_sift_popularity_digest.md`;
  `experimental/scripts/verify_m1_packet_sift_popularity_digest.py`;
  `experimental/notes/m1/m1_a327_rim_route_cut_digest.md`;
  `experimental/data/m1_a327_rim_route_cut_digest.json`;
  `experimental/scripts/verify_m1_a327_rim_route_cut_digest.py`;
  `experimental/notes/triage/pr-triage-2026-06-30-late.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** AllenGrahamHart's M1 local lemmas, sampler
  reconciliation audit, Step 5 high-agreement envelope map, and agreement-265
  status audit were integrated as experimental material.  Allen's oversized
  packet-sift PR #157 was distilled to a compact packet-overlap/popularity-gate
  digest.  Scott Hughes's draft a=327 RIM obstruction PR #145 was distilled to
  a compact interleaved-list route-cut digest and self-contained JSON ledger.
- **How it is useful:** The batch preserves useful local M1 proof machinery,
  audit corrections, and high-agreement bookkeeping without promoting any
  conditional packet branch to a full M1 theorem or leaderboard row.
- **What to do next:** Rebase future M1 packets against the v9 Hankel
  certificate schema.  For the packet-sift branch, prove the nonlocal
  model-entry/multiplicity theorem or isolate a new residual obstruction.  For
  the a=327 RIM branch, turn RREF-derived pivots into deterministic pivot
  schedules before claiming a global bound.

### 2026-06-30 - Paper D v9 Hankel certificate atlas promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v9.tex`,
  `scripts/aperiodic_eliminant_schema.json`,
  `experimental/notes/audits/paperD_v9_vs_v8_audit.md`, `AGENTS.md`,
  `README.md`, site paper/update metadata, and compiled Paper D v9 PDFs.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED-CERTIFICATE-FRAMEWORK.
- **What is being added:** Paper D v9 preserves the v8 universal cap,
  first-grid cap, quotient-support ledger, and quotient-image ledger, then adds
  the aperiodic Hankel chart atlas: regular overdetermined minors, affine
  pivots, projective infinity, curve coefficient pivots, and named singular
  residual buckets.
- **How it is useful:** It turns the M1 safe-side task into concrete Hankel
  certificate packets. Contributors can now emit JSON against
  `scripts/aperiodic_eliminant_schema.json` instead of inventing an atlas or
  hiding singular charts under a generic aperiodic label.
- **What to do next:** Build actual eliminant certificates for meaningful rows,
  starting with exact agreements where the regular minor test applies. Every
  unresolved chart should be labelled as quotient, tangent, extension,
  candidate new obstruction, or unknown.

### 2026-06-30 - PR #137--#149 integration and triage

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Holm Buar,
  Jose Brox, and Scott Hughes.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-30.md`,
  Lean ledger files under `experimental/lean/rs_mca_formalization/`,
  new notes under `experimental/notes/m1/`, `experimental/notes/f1/`,
  `experimental/notes/audits/`, and `experimental/notes/thresholds/`, new
  certificate data under `experimental/data/certificates/`, updated audit
  scripts under `experimental/scripts/`, and `experimental/experiments.tex`.
- **Status:** CONDITIONAL / PROVED-LOCAL / AUDIT / EXPERIMENTAL, depending on
  the individual note.  No full M1, F1, exact-threshold, or prize-solve claim is
  promoted.
- **What is being added:** The batch integrates Holm Buar's `{2,3}`-smooth Paper
  B exact canonical slope count, Lean arithmetic ledgers, finite toy databases,
  M1 numerical audit scans, and Cycle120 finite witness audit; Jose Brox's L3
  path cleanup; and AllenGrahamHart's width-one update, high-agreement compiler
  package, and independent V1 algebra checker.
- **How it is useful:** The new material improves Paper B combinatorics,
  high-agreement threshold reproducibility, formalized integer ledgers, and
  audit coverage without mixing them into the public leaderboard as new best
  rows.
- **What to do next:** Split AllenGrahamHart's very large same-slope PR #138
  into smaller local lemmas, ask for a compact replay target for Scott Hughes's
  #145 route-cut packet, and run Lean/certificate checks in a controlled
  environment if maintainers want independent replay beyond source inspection.

### 2026-06-30 - Paper D v8 quotient ledger promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v8.tex`, `cs25_cap_v8.pdf`,
  `site/papers/cs25_cap_v8.pdf`,
  `experimental/notes/audits/paperD_v8_vs_v7_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V8_CAP /
  PROVED_PAPERD_V8_FIRST_GRID.
- **What is being added:** Paper D v8 is promoted as the current public Paper D
  source. It preserves the v7 universal and first-grid caps, restores the
  explicit `q>n` and endpoint-radius fixes, and adds quotient-support plus
  distinct-parameter quotient image ledgers.
- **How it is useful:** The new ledgers give future staircase scanners and
  proof notes a safe way to account for declared quotient-remainder branches
  without double-counting supports or slope images.
- **What to do next:** Treat these ledgers as branch accounting only. The
  full safe-side theorem still needs the aperiodic Hankel-packing and
  extension-line completion inputs.

### 2026-06-29 - Paper D v7 first-grid cap promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v7.tex`, `cs25_cap_v7.pdf`,
  `site/papers/cs25_cap_v7.pdf`,
  `experimental/notes/audits/paperD_v7_vs_v6_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V7_CAP /
  PROVED_PAPERD_V7_FIRST_GRID.
- **What is being added:** Paper D v7 is promoted as the current public Paper D
  source. It preserves the v6 universal fixed-divisor MCA cap, extends the
  no-loss CA endpoint to `floor(delta n) <= n-k-1`, and adds the first-grid
  deep-point cap for large official-envelope rows.
- **How it is useful:** The public board can now show two Paper D theorem
  layers: the older uniform fixed-divisor cap and the stronger large-row
  first-grid cap `delta*_C(2^-128) <= 1-rho-1/n`.
- **What to do next:** Keep first-grid rows separate from exact-threshold
  claims. The missing safe-side work remains the L1/M1/F1/M2 completion package.

### 2026-06-29 - PR #136 width-one fixed-root closure

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:** `experimental/notes/m1/m1_width_one_fixedroot_closure.md`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`, and
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE / AUDIT.
- **What is being added:** A compact width-one M1 closure note: width-one
  maximal root shadows are bounded-complement rank tests, descend losslessly
  under fixed-root absorption, and inject into one-root fixed-divisor/root-slice
  ledgers.
- **How it is useful:** It reduces the width-one critical-tail branch to the
  existing one-root fixed-root ledger in fixed surplus, giving a smaller target
  for the M1 proof program without promoting a full all-line theorem.
- **What to do next:** Prove or import the polynomial fixed-surplus bound for
  `FixedRootOneRoot_{r1}` after quotient-periodic, tangent, fixed-root, and
  aperiodic charges; do not treat this as a leaderboard row.

### 2026-06-29 - PR #131--#135 triage and frontier rows

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes, and
  Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-29.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_a507_adjacent_bridge_theorem.md`,
  `experimental/notes/m1/m1_a507_plus_one_slope_hunt.md`,
  `experimental/notes/m1/m1_interleaved_list_*.md`,
  `experimental/notes/m1/m1_random_simple_pole_entropy_floor.md`,
  `experimental/notes/m1/m1_coset_packet_finite_slope_floors.md`,
  matching JSON certificates under `experimental/data/`, matching verifiers
  under `experimental/scripts/`, `experimental/experiments.tex`, and site data.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / PROOF_RECORD / LOWER_BOUND /
  ROUTE_CUT / AUDIT.
- **What is being added:** The PR wave adds three useful frontier-facing
  packets: Scott Hughes's interleaved-list hybrid certificate
  `Lambda_mu(C,326) >= 7`, Vadim Avdeev's random simple-pole finite-slope floors
  for `a=257..260`, and Vadim Avdeev's coset-packet finite-slope floors for
  `a=261..288`. AllenGrahamHart's boundary-off external-anchor M1 normal form is
  distilled into a compact proof-program audit, and Scott Hughes's `a=507`
  adjacent-bridge packet is integrated as a route cut rather than a new row.
- **How it is useful:** The finite-slope floors strengthen the low-agreement
  side of the `F_17^32, n=512, k=256` MCA ledger, while the interleaved-list
  packet moves the separate list-track lower-bound row up to agreement `326`.
  The route-cut notes prevent accidental mixing of adjacent line/list
  numerators into the same finite-slope MCA denominator.
- **What to do next:** Human-review the finite-slope-to-MCA noncontainment
  convention before paper promotion, keep #131 as proof-program material until
  it proves a global M1 bound, and treat the Sage scripts in #133 as optional
  independent audits rather than required local verification.

### 2026-06-29 - Paper D v6 promotion and completion-program audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v6.tex`, `cs25_cap_v6.pdf`,
  `site/papers/cs25_cap_v6.pdf`,
  `experimental/notes/audits/paperD_v6_vs_v5_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V6_CAP.
- **What is being added:** Paper D v6 is promoted as the current public Paper D
  source. It keeps the v5 universal MCA cap constants and CS25-free route,
  tightens the conversion collision-count derivation, and adds the
  prize-facing integer-staircase/completion program.
- **How it is useful:** Public rows now cite the strongest Paper D package:
  same cap theorem, clearer prize posture, and explicit conditional MCA/list
  completion theorems for turning the one-sided cap into a full threshold
  determination.
- **What to do next:** Use `PROVED_PAPERD_V6_CAP` for verified Paper D cap rows,
  while keeping the missing L1/M1/F1/M2 completion obligations separate from
  the proved cap itself.

### 2026-06-27 - Root-level paper PDF relocation

- **Agent/model:** Codex.
- **Files added or changed:** `cs25_cap_v5.pdf`, `slackMCA_v4.pdf`,
  `snarks_v5.pdf`, removed generated PDF outputs from `tex/`,
  `site/data/papers.json`, `site/index.html`, `experimental/agents-log.md`.
- **Status:** AUDIT / RELEASE-HYGIENE.
- **What is being added:** The generated Paper B/C/D PDFs are moved out of
  `tex/` into the repository root, matching the README convention that TeX
  sources live under `tex/` and PDFs live at the root. Site-local mirrors under
  `site/papers/` remain for static hosting.
- **How it is useful:** Keeps GitHub PDF links and repository layout aligned
  with the public paper set: B v4, C v5, and D v5.
- **What to do next:** Keep future TeX compile outputs copied to root and, when
  needed, mirrored into `site/papers/` for static-site serving.

### 2026-06-27 - Paper B/C/D version promotion and leaderboard source audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/slackMCA_v4.tex`,
  `slackMCA_v4.pdf`, `tex/snarks_v5.tex`, `snarks_v5.pdf`,
  `site/papers/slackMCA_v4.pdf`, `site/papers/snarks_v5.pdf`, `readme.md`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Two clarification edits are added to the promoted
  Paper B/C versions: the Paper B unsplit curve-envelope lower bound is
  explicitly the line witness embedded as a degree-`d` curve, and Paper C now
  says the curve compiler applies to the finite power-curve/evaluation-domain
  model rather than arbitrary protocol samplers. The README records the current
  public versions B v4, C v5, and D v5.
- **How it is useful:** Keeps the paper prose aligned with the public board:
  Paper D v5 cap rows are proved under their printed scanner hypotheses,
  high-agreement/list rows cite Paper B v4 after promotion, and Paper C v5 is
  framed as protocol-ledger packaging rather than a new cap row.
- **What to do next:** Commit the version promotion after final review, and
  keep future leaderboard rows explicit about whether they are Paper B
  high-agreement theorem rows, Paper D v5 cap rows, or Paper C protocol-ledger
  packaging rows.

### 2026-06-27 - M1 variable-line packet and singleton lemmas

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/experiments.tex`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Local packet lemmas for non-fixed variable Hankel
  determinant lines: active-new packet mass is reduced to active domain
  singletons, quotient defects, and a different-slope two-exchange codegree
  image.  The singleton term is then reduced to contained/tangent and
  one-outside target images, with the zero-lower class eliminated in the
  high-agreement range `a>(n+1)/2`.
- **How it is useful:** This extracts a reviewable M1 reduction from the
  all-line Hankel packet while keeping it out of the leaderboard.  It narrows
  the remaining non-fixed variable-line branch to explicit target-image and
  codegree estimates.
- **What to do next:** Prove polynomial bounds for the active different-slope
  two-exchange codegree and the one-outside boundary target image inside the
  quotient-aware residue-line ledger; do not cite this as the final M1 theorem.

### 2026-06-27 - Paper D v5 cap status promotion in scanner and board

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `experimental/notes/certificate_scanner/README.md`,
  `experimental/notes/certificate_scanner/outputs/`,
  `experimental/notes/audits/a0_cs25_rational_constant_derivation.md`,
  `experimental/notes/audits/theorem_label_map.md`,
  `experimental/notes/audits/codex-f1-l1-20260617/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT.
- **What is being added:** The scanner then emitted `PROVED_PAPERD_V5_CAP` for
  then-active Paper D v5 cap rows whose divisor, binomial, and field hypotheses pass,
  and `NO_ACTIVE_PAPERD_V5_CAP` when no such row is found. Existing scanner
  reports and leaderboard-sweep outputs are regenerated or mechanically updated
  to remove the old draft/CS25-import status, and stale experimental audit notes
  now mark that import route as relevant only to older CA/list comparisons.
- **How it is useful:** Aligns the public leaderboard and scanner with Paper D
  v5's self-contained MCA cap route. Verified Paper D cap rows are no longer
  marked with the older conditional-import or draft-example statuses.
- **What to do next:** Keep CA/list comparison statements separate from the MCA
  cap status, and update any remaining paper-level prose that still discusses
  the older CS25-dependent route as the main Paper D theorem.

### 2026-06-27 - Finite-row threshold note and pure-MCA scanner profile

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/thresholds/f17_32_finite_mca_threshold.tex`,
  `experimental/notes/thresholds/f17_32_finite_mca_threshold.pdf`,
  `experimental/notes/certificate_scanner/examples/f17_512_mca_only.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL-SCANNER.
- **What is being added:** A standalone finite-row threshold note packages the
  \(\F_{17^{32}}, n=512,k=256\) row as an exact finite-slope support-wise MCA
  threshold: agreement \(506\) is unsafe, agreement \(507\) is safe, and the
  closed-real safe interval is \([0,6/512)\). A pure-MCA scanner profile is
  added so the 506/507 endpoint is not mixed with the optional line-plus-list
  protocol ledger.
- **How it is useful:** Supersedes the old strict264-next threshold plan for
  this finite row and gives the clean packaging needed for the public board and
  `towards-prize.md`. It also isolates the next theorem target: the
  row-independent high-agreement threshold compiler with
  \(B_Q=\lfloor Q/2^{128}\rfloor\).
- **What to do next:** Audit the official MCA sampler definition against the
  finite/projective slope conventions and decide whether to promote the
  row-independent compiler from experimental notes into a paper-level theorem.

### 2026-06-27 - Prime192 leaderboard sweep rows

- **Agent/model:** Codex, auditing `leaderboard_sweep_192`.
- **Files added or changed:** `experimental/notes/certificate_scanner/outputs/leaderboard_sweep_192/`,
  `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`, and
  `site/index.html`.
- **Status:** PROVED_PAPERD_V5_CAP / AUDIT.
- **What is being added:** The scanner sweep contributes four concrete
  prime-field rows with `q` near `2^192`, `k=2^40`, smooth power-of-two
  subgroup domains, and one row per official prize rate. It also records a
  small `F_17^32` Paper D example at agreement `258`.
- **How it is useful:** These rows instantiate the Paper D v5 cap with exact
  field/domain arithmetic, making the theorem-envelope rows concrete without
  claiming a new theorem beyond Paper D or an explicit slope census.
- **What to do next:** Regenerate the sweep from a checked-in sweep script if
  the scanner API changes, and keep CA/list comparison statements separate from
  the proved MCA cap status.

### 2026-06-27 - PR #122--#129 triage and selective integration

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes,
  and Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-27.md`,
  `experimental/notes/l1/l1_prefix_dual_d3_subgroup_twisted_collision_bound.md`,
  `experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`,
  `experimental/notes/f1/f1_arbitrary_anchor_locator_split.md`,
  `experimental/notes/m1/m1_all_line_hankel_aperiodic_packet_audit.md`,
  `experimental/data/adjacent-ledgers/`, selected verifier scripts, and
  `experimental/experiments.tex`.
- **Status:** PROVED / IMPORTED-STANDARD-INPUT / AUDIT / PROOF PROGRAM /
  EXPERIMENTAL.
- **What is being added:** New bounded L1/F1/M2 notes are integrated, while
  PR #127's large M1 generated packet is distilled into a smaller audit note.
  The public board is updated only for tangent-floor-backed status corrections:
  Cycle116/119 gates are unconditional but their exact Cycle84 numerator remains
  conditional, and reserve272/288/313 are marked as proved only because they are
  subsumed by tangent/strict352 floors.
- **How it is useful:** Adds useful L1 `d=3` proper-subgroup and monomial-prefix
  toy theorems, sharpens the F1 arbitrary-anchor ledger, and records
  challenge-map pullback accounting for protocol-facing high-agreement ledgers
  without promoting non-verified material to theorem status.
- **What to do next:** Split the M1 all-line aperiodic packet into small
  separately auditable verifiers before considering any stronger theorem claim;
  human-review the imported Katz/Gauss inputs in the L1 `d=3` note before moving
  it toward Paper B.

### 2026-06-27 - Promoted high-agreement TeX split

- **Agent/model:** Codex, verifying and promoting the user-supplied
  `experiments_v2.tex` split.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/notes/high_agreement/`,
  `experimental/scripts/verify_promoted_high_agreement_ledgers.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / AUDIT.
- **What is being added:** The bulky high-agreement tangent, CA/projective,
  curve, interleaved-list, current-row protocol, and general threshold compiler
  material is split into reusable TeX fragments under
  `experimental/notes/high_agreement/` and included from the canonical
  `experimental/experiments.tex` wrapper.
- **How it is useful:** Keeps the stable high-agreement theorem package
  reviewable in smaller files while preserving the compiled experimental memo.
  The split also fixes the stale missing backslash before the
  `Towards-Prize Finite-Threshold Theorems` section header.
- **What to do next:** Human-review the curve sampler caveat before citing the
  curve statements in protocol settings, and keep protocol query/folding,
  extension-lift, challenge-field, and cryptographic losses as separate ledger
  terms.

### 2026-06-26 - Generalized high-agreement ledgers

- **Agent/model:** GPT-5.5 Pro generalized-ledgers packet, audited and
  integrated by Codex.
- **Files added or changed:** `experimental/data/generalized-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/data/README.md`, `site/data/updates.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** A row-independent high-agreement ledger calculus for
  `RS[F,D,k]` rows: with `R=n-k`, `r=n-a`, and `B_Q=floor(Q/2^128)`, the exact
  line/CA/projective numerator is `r+1` in the range `r <= floor(R/3)`, the
  degree-`d` curve numerator is `d(r+1)` in the range
  `r <= floor(R/(d+2))`, and interleaved-list uniqueness holds for
  `r <= floor(R/2)`.
- **How it is useful:** This moves the adjacent-ledger conclusions beyond the
  special `F_17^32` row.  It gives a reusable integer calculator for deciding
  when tangent-star high-agreement terms alone can pin a `2^-128` threshold,
  and shows that at prize-scale dimensions the method stops pinning thresholds
  once field sizes are roughly above `2^166` to `2^170`, depending on rate.
- **What to do next:** Use this calculator before adding any new row to the
  public board, and keep quotient-core, generated-field entropy, challenge
  field, folding, query, and cryptographic terms as separate ledgers.

### 2026-06-26 - High-agreement adjacent CA/curve/list ledgers

- **Agent/model:** GPT-5.5 Pro adjacent-ledgers packet, audited and integrated
  by Codex.
- **Files added or changed:** `experimental/data/adjacent-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** The high-agreement tangent staircase is extended to
  no-loss CA, projective-slope support-wise MCA, finite-parameter degree-`d`
  curve CA/MCA, and MDS interleaved-list uniqueness.  For
  `RS[F_17^32,H,256]`, the line-plus-list coding ledger is unsafe at
  agreement `a=507` and safe at `a=508` when no query/folding loss is added.
- **How it is useful:** This answers the immediate adjacent-ledger question
  past the finite-slope `506/507` gate: the high-agreement CA/projective/curve
  and interleaved-list coding objects are now pinned by explicit integer
  formulae, rather than left as open checks.
- **What to do next:** Human-review protocol reductions before using the
  conditional ledger in SNARK claims, and add any query, folding, hash,
  extension-lift, or cryptographic error terms explicitly.

### 2026-06-26 - Tangent-star extremizer barrier

- **Agent/model:** GPT-5.5 Pro tangent-star packet, audited and integrated by
  Codex.
- **Files added or changed:** `experimental/data/tangent-star/`,
  `experimental/experiments.tex`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / NEW-LOCAL / FINITE-SLOPE STRUCTURAL BARRIER.
- **What is being added:** A refinement of the high-agreement tangent
  staircase: in the exact range `3a-2n >= k`, extremal finite-slope
  support-wise `LD_sw` lines are tangent-star lines.  For
  `RS[F_17^32,H,256]`, this rules out a seventh finite-slope bad branch at
  every agreement `a >= 507`.
- **How it is useful:** It closes the previous finite-slope follow-up question
  left by the tangent staircase: no non-tangent mechanism can push the current
  `F_17^32`, `n=512`, `k=256` row past the `506/507` gate under the
  finite-slope support-wise MCA convention.
- **What to do next:** Use the adjacent-ledgers packet for the high-agreement
  CA/projective/curve/list coding objects, and keep protocol, challenge-field,
  extension-lift, folding, query, and cryptographic losses as separate ledgers.

### 2026-06-26 - High-agreement tangent staircase

- **Agent/model:** GPT-5.5 Pro tangent packet, audited and integrated by Codex.
- **Files added or changed:** `experimental/data/tangent/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT / FINITE-SLOPE-THRESHOLD.
- **What is being added:** A generic moving-root tangent floor
  `LD_sw(C,a) >= n-a+1` for Reed--Solomon codes, plus a matching upper bound in
  the very-high-agreement range `3a-2n >= k` using the common code-line
  residual budget.
- **How it is useful:** For `RS[F_17^32,H,256]` with `|H|=512`, this proves
  `LD_sw(C,a)=513-a` for every `a>=427`, so `LD_sw(C,506)=7` and
  `LD_sw(C,507)=6`.  Thus the finite-slope support-wise `2^-128` staircase is
  pinned between agreements `506` and `507`; agreement `353` and the strict352
  quotient-core frontier are superseded by the tangent floor.
- **What to do next:** Human-review the endpoint convention and use the
  adjacent-ledgers packet for the high-agreement CA/projective/curve/list
  coding objects; protocol-facing losses still need separate ledgers.

### 2026-06-26 - L1 d=2 cubic subgroup twisted bound

- **Agent/model:** Scott Hughes PR #121, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_d2_cubic_subgroup_twisted_bound.md`,
  `experimental/notes/triage/l1-prefix-dual-d2-cubic-subgroup-twisted-bound-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_d2_cubic_subgroup_twisted_bound.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / STANDARD-WEIL-INPUT / AUDIT.
- **What is being added:** A `d=2` cubic proper-subgroup collision bound for
  the actual `H^{2k}` object, using exact Fourier reconstruction,
  multiplicative-character expansion of `1_H`, and a conservative
  one-variable mixed character-sum bound.
- **How it is useful:** Separates proper-subgroup counting from full-affine
  Hooley--Katz geometry and gives an L1 template for higher odd-moment twisted
  subgroup bounds.  It is not a new MCA leaderboard row.
- **What to do next:** Pin the imported Katz/Gauss source constants and test
  whether the method extends to higher odd moments with reserve-scale margins.

### 2026-06-26 - L1 odd-moment Hooley-Katz audit

- **Agent/model:** Scott Hughes PR #120, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_odd_moment_projective_geometry.md`,
  `experimental/notes/triage/l1-prefix-dual-odd-moment-hooley-katz-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_odd_moment_hooley_katz_audit.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / IMPORTED-VERIFIED / AUDIT / ROUTE CUT.
- **What is being added:** A projective odd-moment collision-geometry theorem
  for `k>d`, affine-cone conversion, and a Hooley--Katz/Ghorpade--Lachaud
  constant ledger for the full-affine point-count route.
- **How it is useful:** Records why the generic full-affine point-count route
  is not enough for the subgroup L1 reserve-scale problem and prevents ledger
  mixing between full-affine, full-torus, and proper-subgroup counts.
- **What to do next:** Human-check imported theorem citations and use the
  audit as a route cut unless sharper geometry-specific constants are found.

### 2026-06-26 - Strict352 dyadic quotient-core MCA floor audit

- **Agent/model:** Codex, auditing user-supplied strict352 packet.
- **Files added or changed:** `experimental/data/strict352/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / SUPPORT-WISE-MCA-LOWER-BOUND.
- **What is being added:** A dyadic quotient-core proof packet for
  `RS[F_17^32,H,256]`, `|H|=512`, showing `LD_sw(C,a) >= 7` for every
  agreement `264 <= a <= 352`, with `LD_sw(C,352) >= 16` under the
  finite-slope support-wise MCA convention.
- **How it is useful:** Records a quotient-core mechanism for agreements up to
  `352`.  This was briefly the lower-bound frontier, but it is now superseded
  by the generic tangent floor, which gives `LD_sw(C,352) >= 161` and
  `LD_sw(C,353) >= 160`.
- **What to do next:** Keep the packet as a quotient-core mechanism record and
  compare it against any non-tangent mechanisms that might survive past
  agreement `507`.

### 2026-06-26 - Strict264 quotient-floor proof packet

- **Agent/model:** Codex, with user-supplied strict264 packet.
- **Files added or changed:** `experimental/data/strict264/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A strict264 quotient-core proof packet: generated
  field entropy/list-floor notes, a deep-point list-to-MCA conversion section,
  a calculator for entropy/MCA floors, and the concrete
  `RS[F_17^32,H,256]`, `|H|=512`, agreement-264 quotient-floor obstruction.
  The local audit fixed two TeX transcription errors and regenerated the saved
  calculator output with the exact value `log2(17^32)`.
- **How it is useful:** Gives a direct quotient-core route to
  `epsilon_mca(C,31/64)>2^-128`: `binom(64,33)` augmented-code list points
  imply at least nine support-wise bad slopes after the deep-point conversion,
  while seven slopes already clear the `F_17^32` denominator.
- **What to do next:** Keep the theorem package as a quotient-core mechanism
  record.  The moving-root tangent floor supersedes the old strict264/265
  target by giving `LD_sw(C,264) >= 249`.

### 2026-06-26 - Towards-prize finite-threshold theorem section

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A new `Towards-Prize Finite-Threshold Theorems`
  section for `experiments.tex`: certificate-to-`LD_sw`, fixed-locator
  unique-slope, base-valued subfield confinement, the exact seven-slope
  arithmetic gate over `F_17^32`, and the one-step staircase pinning criterion.
- **How it is useful:** Converts the strict264 and 265 goals into theorem-level
  proof obligations that agents can attack without claiming a new numerator or a
  corrected-reserve MCA theorem.
- **What to do next:** Use the fixed-locator principle to build
  duplicate-aware strict264 and 265 search certificates.

### 2026-06-26 - One-by-one experiment run

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/data/experiment-run-2026-06-26.json`,
  `experimental/notes/triage/experiment-run-2026-06-26.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/updates.json`.
- **Status:** AUDIT / EXPERIMENTAL RUN.
- **What is being added:** A sequential run of the current Cycle120,
  strict264, reserve-ladder, F1, L2, A0, and M2 validators.  All executed
  scripts passed, but no script produced a new retained-slope certificate or
  improved frontier numerator.
- **How it is useful:** Confirms that the current proof infrastructure is
  internally consistent and isolates the exact next strict264 blocker:
  seven explicit retained bad slopes at agreement `264` for the
  `RS[F_17^32,H,256]` row.
- **What to do next:** Build the strict264 seven-slope certificate and an
  independent replayable certificate for the existing `52,747,567,092` count.

### 2026-06-26 - PR #108--#119 proof and audit integration

- **Agent/model:** AllenGrahamHart PRs #108--#112, #114--#118, Scott Hughes
  PRs #113 and #119, reviewed and integrated by Codex with topic-split validity
  checks.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-26.md`,
  `experimental/data/pr-triage-2026-06-26.json`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2}/` and
  `experimental/scripts/`.
- **Status:** PROVED / CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** A one-by-one integration of PRs #108--#119.  The
  theorem-level additions are the F1 syndrome-pencil normal form, the L2
  codegree reduction, the A0 deep-point MCA-cap dependency split, and the M2
  common code-line residual budget.  The remaining material is kept as route
  cuts, audits, or proof programs.
- **How it is useful:** Gives future theory work cleaner local statements for
  F1, L2, Paper D/A0, and M2, while preserving conservative public status.  No
  new prize-worthy numerator or frontier point is claimed.
- **What to do next:** Human-review the theorem-level additions before any
  main-paper promotion, citation-check the mixed-Weil route in PR #119, and
  require a retained-slope proof before treating strict264 as more than a
  target.

### 2026-06-25 - Latest PR integration and estimate audit

- **Agent/model:** AllenGrahamHart PRs #101--#107, ScottDHughes PR #99, and
  Cycle120 audit material from PR #100/#105, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-25.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2,x1}/`,
  `experimental/scripts/`, and `experimental/lean/rs_mca_formalization/`.
- **Status:** AUDIT / EXPERIMENTAL / PROOF-CHECK-NEEDED / CONDITIONAL.
- **What is being added:** A one-by-one integration of PRs #99--#107. The
  Cycle120 numerator is unchanged at `52,747,567,092`; the useful improvements
  are the standalone Cycle120 `LD_sw` proof note, the exact M2
  `epsilon_mca = LD_sw/|F|` bridge, stronger F1 extension-line lower floors,
  an M1 beta-pushforward spectral audit, and sharper L1/L2 proof-program
  targets.
- **How it is useful:** Gives future theory work better normalized estimates
  without editing Papers A--D. In particular, the current ABF-row obstruction
  still points to `epsilon_mca(C,125/256)>2^-128` and the Cycle119 strict
  endpoint `delta*_C <= 249/512`, while L1/L2/F1/X1 now have cleaner
  follow-up notes and standard-library verifiers.
- **What to do next:** Do a human proof review of the standalone Cycle120
  proof chain, then run selected nonmutating verifiers in a controlled pass.
  Treat PR #100's raw generated packet as superseded by the compact audit and
  standalone proof note unless a reviewer explicitly needs the raw replay
  material.

### 2026-06-23 - Cycle119 admissibility review

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus wording cleanup
  in the prior Cycle84 public replay audit.
- **Status:** AUDIT / PROOF-CHECK-NEEDED / COMPUTATION-DEPENDENT.
- **What is being added:** A compact review of the Cycle119 strict-263 claim:
  `LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092`, with `|H|=512`, and an
  admissibility check against the local ABF-aligned definitions and public
  Proximity Prize page.
- **How it is useful:** Separates the potentially important theorem claim from
  Danny's raw/generated PR branch. The branch is not integrable as-is, but the
  two-ended locator transfer is now the right object to demand as a clean proof.
  If the proof and finite computation check out, the right public framing is a
  prize-facing negative counterexample candidate under the printed ABF
  formulation, not an accepted prize solution.
- **What to do next:** Independently fetch and check the ABF PDF, then ask Danny
  for a standalone human-readable proof of the two-ended locator transfer and a
  separate minimal record of the Cycle84 finite computation it consumes.

### 2026-06-23 - Cycle120 ABF counterexample candidate integration

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md`,
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, and `experimental/agents-log.md`.
- **Status:** CONDITIONAL / PROOF-SPINE-CHECKED / COMPUTATION-DEPENDENT /
  SOURCE-AUDIT.
- **What is being added:** A cleaned integration of the Cycle120 ABF-facing
  negative result. It records that Cycle116 agreement `262` is enough for the
  printed ABF closed threshold at `delta=125/256`, while Cycle119 agreement
  `263` checks as a strict-ball strengthening. The note now states explicitly
  that this is only a negative obstruction to
  `epsilon_mca(C,125/256) <= 2^-128` for one row, not ordinary list decoding,
  protocol soundness, or an exact determination of `delta*_C`. It also records
  the endpoint nuance: Cycle116 gives `delta*_C <= 125/256` under a supremum
  convention, while Cycle119 gives `delta*_C <= 249/512 < 125/256`.
- **How it is useful:** Moves the useful part of PR #96 into a compact
  experimental note without importing zips, generated checkers, copied PDFs,
  rendered pages, or raw prompt archives. It gives the project a concrete
  human-review target: the Cycle84/Cycle116 finite proof chain plus the
  optional Cycle119 strict-ball proof.
- **What to do next:** Independently retrieve the ABF PDF, review the finite
  count and fixed-jet transfer, and ask Danny for a minimal nonmutating reviewer
  packet in proof/computation/audit language.

### 2026-06-22 - PR #96-#98 experimental triage

- **Agent/model:** DannyExperiments, avdeevvadim, scottdhughes; integrated by
  Codex.
- **Files added or changed:**
  `experimental/notes/triage/pr-triage-2026-06-22.md`,
  `experimental/notes/m1/m1_cycle84_public_replay_audit.md`,
  `experimental/notes/f1/f1_deep_point_list_to_ca_mca.md`,
  `experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py`,
  `experimental/notes/l1/l1_prefix_fourier_orbit_cancellation.md`,
  `experimental/scripts/verify_l1_fourier_orbit_cancellation.py`,
  `experimental/SUMMARY.md`, `experimental/README.md`,
  `experimental/scripts/README.md`, and `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE_MODEL_PROOF / PROVED / CONDITIONAL /
  EXPERIMENTAL.
- **What is being added:** A conservative triage of PRs #96--#98. PR #96's
  useful Cycle84 public replay record is kept as an inert audit note:
  `m_max(beta)=2`, `Occ(beta)=52,747,567,092`, `D=24`, twelve double fibers,
  and no fibers of size at least three. PR #97 adds the F1 simple-pole
  deep-point list-to-CA/MCA conversion note and sanity script. PR #98 adds the
  L1 dual-dilation Fourier orbit-kernel reduction note and verifier.
- **How it is useful:** Cycle84 now has a public replay record for the finite
  M1 wall without importing the live workflow or raw archive. The F1 note gives
  a direct special list-to-CA/MCA mechanism to audit against Paper D. The L1
  note moves prefix-local work from individual Fourier frequencies to orbit
  kernels and records a concrete route cut for pointwise kernel saving.
- **What to do next:** Do not treat Cycle84 as a prize-level theorem until a
  transfer theorem is proved. Audit #97 against the exact main-paper `eca` and
  `emca` predicates before any promotion. Run the new scripts only after
  reviewer approval; this triage pass inspected them as text but did not
  execute PR code.

### 2026-06-19 - Experimental folder streamlining

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/README.md`,
  `experimental/notes/README.md`, `experimental/scripts/README.md`,
  `experimental/data/README.md`, plus repository moves under
  `experimental/notes/`, `experimental/scripts/`, `experimental/data/`, and
  `experimental/lean/`.
- **Status:** AUDIT.
- **What is being added:** Reorganized the experimental workspace into four
  durable buckets: notes, scripts, compact data, and Lean. Removed generated
  Python caches and raw/prompt transcript dumps from dated AI-loop outputs.
- **How it is useful:** Future agents now have a small root surface and a clear
  placement policy. Audited summaries and reproducible scripts remain, while
  bulky model-run provenance that was not needed for review is gone.
- **What to do next:** Keep new work inside the existing buckets, update
  `README.md` if a genuinely new bucket is needed, and avoid adding raw
  transcript archives unless they are the only reproducibility record.

### 2026-06-19 - PR #82/#84-#95 experimental integration

- **Agent/model:** AllenGrahamHart, scottdhughes, latifkasuli,
  DannyExperiments PRs, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-19.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/notes/l1/l1_prefix_divisor_count.md`,
  `experimental/notes/l1/l1_quotient_defect_closure.md`,
  `experimental/notes/l1/l1_repaired_locator_theorem_package.md`,
  `experimental/notes/l2/l2_interleaved_dilation_constants.md`,
  the NFB frontier JSON data folder,
  `experimental/notes/m1/m1_residue_line_roadmap.md`, M1 depth-two Kummer notes and
  verifiers, L1/L2 verifier scripts, and the selected
  `experimental/notes/f1/fable-loop/PRZ_REVIEW_INDEX.md` Cycle 49--57 audit
  layer.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT, as
  marked per file.
- **What is being added:** Manual integration of the useful recent PRs:
  PR #93 supersedes #85--#91 as the Scott L1 consolidation; PR #84 adds the
  L1 prefix/divisor/Fourier split; PR #92 adds L2 interleaved dilation and
  quotient-core constants; PR #94 adds a compact `F\B` deep-hole proof
  record; PR #82 adds the M1 low-slack Kummer/depth-two packet; PR #95 is
  integrated only as review index plus cycle audits, not as a raw 225k-line
  archive.
- **How it is useful:** Gives future work clear entry points: L1 quotient
  floors versus aperiodic Fourier cancellation, M1 two-coordinate/conductor
  targets, L2 aligned interleaved constants, an F1/Paper D explicit-line
  proof target, and a compact Fable-loop upper-side route map.
- **What to do next:** Run and review the integrated verifiers, add a
  standalone verifier for the NFB JSON record, audit the M1 Kummer imports
  before consuming constants, and continue the Fable-loop program from the
  high-`j` constant-rate prompt rather than the cut `t=2,j=2` toy regime.

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
  `experimental/notes/f1/fable-loop/audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/scripts/fable_loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py`,
  `experimental/notes/f1/fable-loop/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROOF-SKETCH / EXACT_NEW_WALL / AUDIT.
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
  integration of accepted experimental notes, scanners, proof records, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
