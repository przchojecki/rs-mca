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

### 2026-06-18 - M1 depth-two lift-window theorem note

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A compact theorem-level note extracting the
  slack-two depth-two lift-window theory from the scanner: the exact
  quotient-window reduction for `R=N-L`, the lift-limited slope ceiling, and
  the conditional fixed-window Kummer saturation certificate with `R^3`
  weights, plus the quotient-window union Kummer certificate with exact
  quotient-label triple count `T_R(N)` and sharpened nonprincipal
  ambient-character L1 bound built from `C_R(N)`, with an exact `R=2`
  quotient-L1 distribution.
- **How it is useful:** Gives reviewers a single mathematical statement for
  the M1 contribution in PR #79, separating proved quotient-fiber algebra
  from the imported Kummer-Weil estimate and showing how the `R=1`, `R=2`,
  `R=3`, fixed-window, and union-window examples fit one mechanism.
- **What to do next:** Prove or cite the Kummer-Weil estimate as a standalone
  algebraic-geometry input, then extend the quotient-window method beyond the
  canonical slack-two depth-two frontier.

### 2026-06-18 - M1 depth-two Kummer-Weil saturation wall

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** A Kummer-Weil coset-saturation criterion and
  resulting index-window label for the slack-two depth-two first-nonzero
  frontier. Under the standard degree-five two-variable character-sum bound,
  low-index proper subgroups hit every nonzero `D^2`-coset in the raw
  normalized shape catalog; the scanner combines this with the lift gate,
  the complement-fiber gate `N-L>=min(4,N)`, and the high-index ceiling. A
  divisor-exponent audit proves that no nonprincipal character tuple is a
  hidden Kummer power, the imported `16p` constant is traced to the
  squarefree radical divisor degree `1+1+1+2=5`, the principal open-set count
  and admissibility-line loss are computed exactly, and a verifier checks
  these plus low-index proper-subgroup samples against exact enumeration.
- **How it is useful:** Complements PR #78's high-index ceiling by showing
  that small-index proper subgroups are raw-saturated rather than sparse, and
  identifies the exact elementary gate needed to transfer that statement to
  exact supports. It also adds a lift-limited exact-support slope ceiling
  depending on `R=N-L`, so cases with too few remaining quotient fibers can
  be certified sparse even when the raw shape catalog is large. In the
  extreme `R=1` case, the active layer is reduced exactly to the depth-two
  shape catalog on the quotient kernel, expanded by ambient `D^2`. A
  further two-fiber Kummer certificate shows that, under the same imported
  degree-five character-sum estimate, one fixed window `K union cK` already
  hits every nonzero `D^2`-coset once the conservative lower numerator is
  positive; whenever `R>=2`, this promotes directly to exact-support
  saturation. The scanner also records the exact `R=2` union reduction:
  active shapes are the union of the two-fiber windows `C_2^(2)(K union cK)`,
  and the verifier checks a finite case where no single fixed window
  saturates but the union does. The scanner label now promotes such cases to
  `r2_union_saturated` instead of leaving them in a raw-only or intermediate
  bucket. A general quotient-window reduction unifies the lift-limited layer:
  for every `R<min(4,N)`, active shapes are exactly the union over quotient
  windows of size `R` containing the kernel fiber, and the verifier checks
  the `R=1,2,3` reductions on the running `p=97,n=48,N=6` sample. The same
  character-sum method now gives a fixed `R`-window Kummer certificate with
  principal and error weights `R^3`; the verifier checks a positive `R=3`
  full-domain `p=2213,N=4` instance against exact fixed-window enumeration.
  The quotient-window union certificate replaces the fixed-window weight by
  the exact number `T_R(N)` of quotient-label triples touching at most `R`
  fibers, then sharpens the nonprincipal coefficient from the crude
  support-size bound `T_R(N)` to `C_2(N)=3N-6` and
  `C_3(N)=max(6,(N-2)(N-3))`, while still accounting for the ambient
  character triples that restrict trivially to `D/K`. For `R=2`, it replaces
  the bound by the exact parity-dependent distribution of zero subset sums,
  giving an exact quotient L1 term. The verifier audits an exact `R=2`
  threshold improvement at `p=181,N=3` and the bounded `R=3` improvement at
  `p=257,N=4`, where the previous numerator is still negative but the
  sharpened active union is certified saturated.
  This leaves a narrower intermediate/lift-limited window for M1 slope-image
  bounds.
- **What to do next:** Prove or replace the imported Kummer-Weil constant in
  a standalone algebraic-geometry note, then attack the residual `R=1`
  kernel catalog and extend the quotient-window union certificate beyond this
  canonical depth-two layer.

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
