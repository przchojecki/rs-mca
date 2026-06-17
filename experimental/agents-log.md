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

### 2026-06-17 - M1 random baseline strengthening

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_average_support_collinearity.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Strengthens the integrated M1 average baseline with
  a support-overlap second-moment bound and a fixed-base/random-direction
  formula. Support-pair covariance can begin only when two supports intersect
  in at least `k` points, the high-overlap contribution has an explicit
  exchanged-points variance criterion, fixed-slope support indicators have an
  exact second moment, the random-line bad-slope density has a two-sided phase
  diagram with a quantitative missing-slope bound, entropy-reserve
  interpretation, and field-ledger warning, and base-word support-list mass
  contributes only to the zero slope `z = 0`.
- **How it is useful:** Turns the first-moment random-line estimate into an
  overlap, concentration, slope-density, and basepoint-slope ledger for the M1
  residue-line packing problem, isolating the high-overlap correction to the
  entropy-reserve transition after zero-slope, tangent-floor, and
  quotient-periodic families are separated while keeping `q_line` distinct
  from `q_gen`.
- **What to do next:** Build a tiny-field `Pi_S` collinearity scanner and
  compare tangent, quotient-periodic, and aperiodic support sources against
  the expectation and high-overlap covariance baseline.
