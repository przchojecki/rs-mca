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

### 2026-06-17 - A0 Crites-Stewart import audit

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/a0_cs25_import_audit.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A conservative audit note for the Crites-Stewart
  list-to-agreement import, separating the internally checked eta-`1/2`
  contrapositive algebra from unresolved external theorem-matching questions.
- **How it is useful:** This targets A0 by making the universal-cap dependency
  explicit: the local cap proof is coherent conditional on the displayed import,
  but the exact source theorem still needs radius, augmentation, normalization,
  sampling-field, and constant checks.
- **What to do next:** Manually compare the note's unresolved checklist against
  CS25 Theorem 2 and the ABF Theorem 5.3 restatement, then update the manuscript
  import wording if any hypothesis or constant changes.
