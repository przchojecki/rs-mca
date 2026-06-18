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

### 2026-06-18 - Experimental theorem note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments/experiments.tex`,
  `experimental/experiments/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** PROVED / HEURISTIC / AUDIT.
- **What is being added:** A standalone LaTeX note collecting restricted
  Cycle 14--18 theorems and heuristics, including the Cycle 18
  divisibility-gate theorem with proof.
- **How it is useful:** Gives the experimental proof material a citable,
  compiled form without editing Papers A--D.
- **What to do next:** Extend the scanner to test the `G==0` gate and decide
  whether any source-valid growing-prime family has two-dimensional slope-map
  image.

### 2026-06-18 - M1 slack-two depth-two high-index ceiling

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** An unconditional high-index ceiling for the
  slack-two depth-two frontier: for a subgroup `D` of size `n`, the nonzero
  frontier is contained in at most `n^2` square cosets, hence has slope count
  at most `min(p,1+n^3/gcd(2,n))`. The scanner now reports and checks this
  bound.
- **How it is useful:** Complements the full-domain saturation theorem by
  identifying the subgroup-size regime where this first nonzero frontier is
  automatically non-field-filling.
- **What to do next:** Replace the coarse `n^2` shape bound by character-sum
  coset-image estimates for intermediate subgroup index.

### 2026-06-18 - M1 slack-two depth-two full-domain saturation

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_slack_two_depth_two_full_domain.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** A full-domain theorem for the first nonzero
  slack-two depth-two frontier: for `D=F_p^*` and `p>=11`, the polynomial
  `-(u^2+v^2+uv+u+v+1)` hits both quadratic classes on admissible shapes, so
  the nonzero slope image is all of `F_p^*`. The proof uses a character-sum
  margin for `p>=23` and a finite verifier for `p=11,13,17,19`.
- **How it is useful:** Gives the first explicit nonzero-frontier image result
  after the residual-depth partition, showing that the full-domain toy case
  saturates nonzero slopes rather than giving a small M1 bound.
- **What to do next:** Move from full domains to proper multiplicative
  subgroups, where nontrivial coset-image bounds may still reduce M1 packing.

### 2026-06-18 - M1 first-nonzero residual frontier partition

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** An exact disjoint partition of the depth-`d`
  residual-packet catalog into first-nonzero coefficient frontiers
  `e_(T+j) != 0` and the terminal pure-zero stratum. The scanner now records
  this partition and checks that only the `j=0` frontier contributes nonzero
  slopes at the original slack.
- **How it is useful:** Converts the residual-depth hierarchy into separate
  coset-image targets, so future M1 work can attack each nonzero frontier
  without mixing it with inherited zero strata.
- **What to do next:** Bound the nonzero frontier images, starting with the
  depth-two surfaces already exposed by the PR.

### 2026-06-18 - M1 terminal pure-zero residual-depth ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** An explicit formula for the terminal pure-zero
  residual-depth stratum: depth `d` with `h=T+d<m` contributes only
  `h`-power cosets, with lift gate `m | k-d`, touched-fiber count
  `h/gcd(h,m)`, and exact support multiplicity. The scanner now checks this
  ledger on small canonical M1 scans.
- **How it is useful:** Closes the inherited-zero side of the residual-depth
  hierarchy from the M1 PR, so later work can focus on first-nonzero
  coefficient images rather than recounting terminal zero strata.
- **What to do next:** Use the terminal-zero check as a gate before attacking
  the nonzero frontier images at depth `d>=2`.

### 2026-06-18 - M1 residual-depth transition theorem

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A general residual-depth transition theorem:
  second-superboundary packets at slack `T` have a normalized `(T+2)!` shape
  quotient, slope cosets `b_T(u)D^T`, and lift gate `m | k-2`; its zero-slope
  slice is exactly the first-superboundary shape catalog for slack `T+1`.
  The `T=2` case gives the conic
  `u^2+v^2+uv+u+v+1=0`. The note also records the general residual-depth
  shift: zero slope at `(T,k,d)` is the depth-`d-1` catalog at
  `(T+1,k-1,d-1)`. The scanner audits the `d=2` instance and the specialized
  slack-two 24-fold square-coset ledger against direct support histograms.
- **How it is useful:** Deepens the M1 low-slack residual-packet theory by
  showing that next-slack first-superboundary catalogs are transition loci for
  depth-two residual packets, rather than isolated toy equations. Iterating
  the shift separates inherited zero strata from the genuinely new
  first-nonzero-coefficient frontier.
- **What to do next:** Use this depth-link pattern to study higher
  superboundary layers and sharper coset counts for the slack-three
  depth-two packet surface.

### 2026-06-18 - Cycle 18 resonance slope-map reconstruction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/2026-06-18-fable-loop/audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/2026-06-18-fable-loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py`,
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
