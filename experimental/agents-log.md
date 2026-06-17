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

### 2026-06-17 - M1 quotient-periodic overlap profile

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Gives the exact overlap, strict high-overlap, and
  max exchange-codegree profile for support families formed by unions of equal
  quotient fibers, including the exact-support divisibility guardrail that this
  whole-fiber family is absent unless the fiber size divides `s = k+t` and the
  finite quotient-prefix form of the strict-overlap correction.
- **How it is useful:** Supplies the quotient-periodic input to the M1
  support-family ledger, so this structured exception can be separated
  quantitatively before attacking the aperiodic residue-line local-limit
  problem; it also records the exact-support form of dimension/slack dithering
  for this support source.
- **What to do next:** Have a tiny M1 scanner emit `|A|`, `Delta_j(A)`, and
  `Gamma_j(A)` by labelled support class, verifying that the quotient-periodic
  class matches the closed formulas here.

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
